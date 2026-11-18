"""Bounded public-source recovery; no scientific/read/approval credit is granted.

The caller retains the existing cache/provider lock order and original Agents
fetch callable. This module never changes TLS, public-URL or redirect policy.
The private append-only download ledger is accounting, not scientific evidence.
"""
from __future__ import annotations

from contextlib import contextmanager
import copy
import fcntl
import hashlib
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import stat
import time
import unicodedata
import uuid
from urllib.parse import unquote, urlsplit, urlunsplit

from oracle_atlas.discovery.http import DiscoveryError, atomic_write, display_url


INITIAL_BYTES = 20_000_000
FILE_BYTES = 80_000_000
CYCLE_BYTES = 160_000_000
MAX_ATTEMPTS = 16
_DECLARED_SIZE = 'The download exceeds max_bytes; increase the file budget if needed.'
_BODY_SIZE = 'The download exceeds max_bytes; the source has not been truncated and presented as complete.'
_DECOMPRESSED_SIZE = 'The decompressed literature exceeds max_bytes.'
_SOURCE_SIZE = 'The source exceeds max_bytes.'
_ARXIV = re.compile(r'(?P<id>\d{4}\.\d{4,5}|[a-z][a-z.-]*/\d{7})(?:v(?P<version>[1-9]\d*))?', re.I)


def _dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _hash(value):
    return hashlib.sha256(_dump(value).encode()).hexdigest()


class SourceRecoveryError(RuntimeError):
    def __init__(self, code, details=None):
        self.code = code
        self.details = {'code': code, 'scientific_approval': False, 'source_read_credit': False,
                        'failure_resolved': False, **(details or {})}
        super().__init__('Bounded source recovery stopped: ' + code)


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + ' must be a positive integer')
    return value


def _url(url):
    # Original fetch_source/HTTPClient still performs DNS and redirect checks.
    # Do not perform a second DNS request when its callable is a local test fake.
    if not isinstance(url, str) or len(url) > 20000:
        raise SourceRecoveryError('unsafe_url')
    parsed = urlsplit(url)
    if parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username or parsed.password:
        raise SourceRecoveryError('unsafe_url')
    host = parsed.hostname.lower()
    if host == 'localhost' or host.endswith(('.localhost', '.local')):
        raise SourceRecoveryError('unsafe_url')
    try:
        address = ipaddress.ip_address(host.split('%')[0])
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise SourceRecoveryError('unsafe_url')
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ''))


def _is_arxiv(url):
    host = urlsplit(url).hostname or ''
    return host == 'arxiv.org' or host.endswith('.arxiv.org')


def _arxiv_identity(value):
    value = unquote(str(value)).strip()
    value = re.sub(r'^(?:arxiv:|https?://(?:export\.)?arxiv\.org/(?:abs|pdf|html)/)', '', value, flags=re.I)
    value = re.sub(r'\.pdf$', '', value, flags=re.I)
    match = _ARXIV.fullmatch(value)
    if not match:
        raise ValueError('An exact arXiv identifier is required')
    return match['id'].lower(), int(match['version']) if match['version'] else None


def _doi(value):
    value = unquote(str(value)).strip().lower()
    value = re.sub(r'^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)', '', value)
    if not re.fullmatch(r'10\.\d{4,9}/\S+', value):
        raise ValueError('An exact DOI identifier is required')
    return value


def _identity(value):
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError('Expected source identity must be an object')
    value = copy.deepcopy(value)
    if value.get('kind') in {'doi', 'arxiv'}:
        value.setdefault(value['kind'], value.get('value'))
    result = {}
    arxiv = value.get('arxiv_id', value.get('arxiv'))
    if arxiv:
        identifier, version = _arxiv_identity(arxiv)
        supplied = value.get('arxiv_version', value.get('version'))
        if supplied is not None:
            supplied = str(supplied).removeprefix('v')
            if not supplied.isdecimal() or int(supplied) < 1 or version not in {None, int(supplied)}:
                raise ValueError('Conflicting arXiv version')
            version = int(supplied)
        result.update(arxiv_id=identifier, arxiv_version=version)
    if value.get('doi'):
        result['doi'] = _doi(value['doi'])
    if value.get('content_hash', value.get('sha256')):
        digest = value.get('content_hash', value.get('sha256'))
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Expected content hash must be64 lower-case hex characters')
        result['content_hash'] = digest
    if value.get('title'):
        if not isinstance(value['title'], str) or len(value['title']) > 1000:
            raise ValueError('Expected title must be bounded text')
        result['title'] = value['title']
    return result


def _infer(url):
    parsed = urlsplit(url)
    if _is_arxiv(url) and re.match(r'^/(?:abs|pdf|html)/', parsed.path):
        try:
            return _identity({'arxiv': re.sub(r'^/(?:abs|pdf|html)/', '', parsed.path)})
        except ValueError:
            return {}
    if parsed.hostname in {'doi.org', 'dx.doi.org'}:
        try:
            return _identity({'doi': parsed.path.lstrip('/')})
        except ValueError:
            return {}
    return {}


def _merged_identity(url, expected_identity):
    """One URL/metadata merge rule for both fresh and cached source checks."""
    original = _url(url)
    explicit = _identity(expected_identity)
    inferred = _infer(original)
    if explicit and inferred and any(explicit[k] != inferred[k] for k in ('arxiv_id','arxiv_version','doi') if explicit.get(k) is not None and k in inferred):
        raise SourceRecoveryError('request_identity_mismatch')
    return original, explicit, {**inferred,**{key:value for key,value in explicit.items() if value is not None}}


def _normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text).casefold() if c.isalnum())


class SourceRecovery:
    def __init__(self, atlas_root, cache_dir, context, config, *, fetch_source,
                 remaining_seconds=None, before_attempt=None):
        self.cache_dir = Path(cache_dir).resolve()
        self.sources = self.cache_dir / 'sources'
        self.fetch_source = fetch_source
        self.remaining_seconds = remaining_seconds
        self.before_attempt = before_attempt
        options = copy.deepcopy(config.get('literature', {}))
        self.limits = {'initial_bytes': _positive(options.get('max_bytes', INITIAL_BYTES), 'literature.max_bytes'),
            'file_bytes': _positive(options.get('max_source_file_bytes', FILE_BYTES), 'literature.max_source_file_bytes'),
            'cycle_bytes': _positive(options.get('max_source_download_bytes', CYCLE_BYTES), 'literature.max_source_download_bytes'),
            'attempts': _positive(options.get('max_source_download_attempts', MAX_ATTEMPTS), 'literature.max_source_download_attempts'),
            'replacements': options.get('max_source_replacements', 2)}
        if type(self.limits['replacements']) is not int or self.limits['replacements'] < 0:
            raise ValueError('literature.max_source_replacements must be nonnegative')
        if self.limits['initial_bytes'] > self.limits['file_bytes'] or self.limits['file_bytes'] > FILE_BYTES or \
                self.limits['cycle_bytes'] > CYCLE_BYTES or self.limits['attempts'] > MAX_ATTEMPTS or self.limits['replacements'] > 2:
            raise ValueError('Source recovery limits exceed the fixed80MB/160MB/16-attempt/2-replacement policy')
        self.timeout = float(options.get('timeout', 30))
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError('literature.timeout must be positive and finite')
        self.identity = {'atlas_root': str(Path(atlas_root).resolve()), 'sid': context.get('setting_id'),
            'base_version': context.get('base_version'), 'cutoff': context.get('cutoff'),
            'semantics': context.get('semantics', context.get('contract_hash', 'legacy-unspecified'))}
        if any(not isinstance(v, str) or not v for v in self.identity.values()):
            raise ValueError('Download accounting requires a fixed Atlas/setting/baseline/cutoff identity')
        self.cycle_key = _hash(self.identity)
        self.directory = self.cache_dir / 'source-recovery' / self.cycle_key
        if any(p.is_symlink() for p in (self.cache_dir, self.cache_dir / 'source-recovery', self.directory)):
            raise SourceRecoveryError('unsafe_ledger_path')
        self.directory.mkdir(parents=True, exist_ok=True)
        self.journal = self.directory / 'journal.jsonl'
        with self._lock():
            binding = self.directory / 'binding.json'
            expected = {'version': 1, 'identity': self.identity, 'limits': self.limits}
            if binding.exists():
                if binding.is_symlink() or json.loads(binding.read_text()) != expected:
                    raise SourceRecoveryError('immutable_cycle_policy_changed')
            else:
                if self.journal.exists():
                    raise SourceRecoveryError('missing_cycle_policy_binding')
                atomic_write(binding, _dump(expected).encode())
            self._records()

    @contextmanager
    def _lock(self):
        path = self.directory / 'ledger.lock'
        descriptor = os.open(path, os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        try:
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise SourceRecoveryError('unsafe_ledger_path')
            fcntl.flock(descriptor, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
            os.close(descriptor)

    def _records(self):
        if not self.journal.exists():
            return []
        if self.journal.is_symlink() or not self.journal.is_file():
            raise SourceRecoveryError('unsafe_ledger_path')
        records, previous = [], None
        try:
            if self.journal.stat().st_size > 1_000_000:
                raise ValueError('Oversized ledger')
            for i, line in enumerate(self.journal.read_text().splitlines()):
                row = json.loads(line)
                if row['sequence'] != i or row['previous_hash'] != previous or row['record_hash'] != _hash({k:v for k,v in row.items() if k != 'record_hash'}):
                    raise ValueError('Journal chain changed')
                previous = row['record_hash']; records.append(row)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise SourceRecoveryError('invalid_download_journal') from exc
        return records

    def _append(self, kind, body, records):
        value = {'sequence': len(records), 'previous_hash': records[-1]['record_hash'] if records else None,
                 'kind': kind, 'body': body}
        value['record_hash'] = _hash(value)
        descriptor = os.open(self.journal, os.O_CREAT | os.O_APPEND | os.O_WRONLY | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        with os.fdopen(descriptor, 'a') as stream:
            stream.write(_dump(value) + '\n'); stream.flush(); os.fsync(stream.fileno())

    def _state(self, records):
        try:
            return self._derive_state(records)
        except SourceRecoveryError:
            raise
        except (KeyError, TypeError, ValueError) as exc:
            raise SourceRecoveryError('invalid_download_journal') from exc

    def _derive_state(self, records):
        reserved, settled = {}, {}
        for row in records:
            body = row['body']; identifier = body['attempt_id']
            if row['kind'] == 'reserve' and identifier not in reserved:
                if not isinstance(identifier,str) or not re.fullmatch('[0-9a-f]{32}',identifier) or \
                        type(body.get('max_bytes')) is not int or not 1 <= body['max_bytes'] <= self.limits['file_bytes'] or \
                        body.get('reserved_bytes') != body['max_bytes'] + 1:
                    raise SourceRecoveryError('invalid_download_journal')
                reserved[identifier] = body
            elif row['kind'] == 'settle' and identifier in reserved and identifier not in settled:
                if type(body.get('charged_bytes')) is not int or not 0 <= body['charged_bytes'] <= reserved[identifier]['reserved_bytes']:
                    raise SourceRecoveryError('invalid_download_journal')
                settled[identifier] = body
            else:
                raise SourceRecoveryError('invalid_download_journal')
        used = sum(row['charged_bytes'] for row in settled.values())
        held = sum(row['reserved_bytes'] for key,row in reserved.items() if key not in settled)
        if used + held > self.limits['cycle_bytes'] or len(reserved) > self.limits['attempts']:
            raise SourceRecoveryError('invalid_download_journal')
        return {'cycle_key': self.cycle_key, 'limits': copy.deepcopy(self.limits), 'used_bytes': used,
                'reserved_bytes': held, 'remaining_bytes': self.limits['cycle_bytes'] - used - held,
                'attempts': len(reserved), 'remaining_attempts': self.limits['attempts'] - len(reserved),
                'outstanding_attempt_ids': [key for key in reserved if key not in settled],
                'unknown_byte_attempts': sum(row.get('bytes_known') is False for row in settled.values()),
                'journal_head': records[-1]['record_hash'] if records else None,
                'accounting_basis': 'archived_body_bytes_on_success;proven_prebody_zero;unknown_failure_reserved_max_plus_one',
                'wire_bytes_not_observable': True, 'source_read_credit': False, 'scientific_approval': False}

    def snapshot(self):
        with self._lock():
            return self._state(self._records())

    def _reserve(self, url, requested, index, obligation_id):
        with self._lock():
            records = self._records(); state = self._state(records)
            if state['outstanding_attempt_ids']:
                raise SourceRecoveryError('outstanding_download_attempt', {'accounting': state})
            if state['remaining_attempts'] <= 0 or state['remaining_bytes'] < 2:
                raise SourceRecoveryError('download_budget_exhausted', {'accounting': state})
            maximum = min(requested, self.limits['file_bytes'], state['remaining_bytes'] - 1)
            attempt = {'attempt_id': uuid.uuid4().hex, 'url': display_url(url), 'url_sha256': hashlib.sha256(url.encode()).hexdigest(),
                       'max_bytes': maximum, 'reserved_bytes': maximum + 1, 'recovery_index': index,
                       'obligation_id': obligation_id}
            self._append('reserve', attempt, records)
            return attempt

    def _settle(self, attempt, *, charged, known, code, source_hash=None):
        body = {'attempt_id': attempt['attempt_id'], 'charged_bytes': charged, 'bytes_known': known,
                'code': code, 'source_hash': source_hash, 'declared_bytes': None}
        with self._lock():
            records = self._records(); state = self._state(records)
            if attempt['attempt_id'] not in state['outstanding_attempt_ids']:
                raise SourceRecoveryError('download_settlement_changed')
            self._append('settle', body, records)
        return {**attempt, **body}

    def _remaining(self):
        if self.remaining_seconds is None:
            return self.timeout
        value = self.remaining_seconds()
        if isinstance(value, bool) or not isinstance(value, (float,int)) or not math.isfinite(value) or value <= 0:
            raise SourceRecoveryError('stage_time_exhausted')
        return min(self.timeout, value)

    def _raw_measure(self, saved, maximum):
        path = saved.get('path')
        if path:
            path = Path(path)
            if path.is_symlink() or not path.resolve().is_relative_to(self.sources.resolve()) or not path.is_file():
                raise SourceRecoveryError('invalid_archived_source')
            count = path.stat().st_size
            if count > maximum:
                raise SourceRecoveryError('invalid_archived_source')
            checksum=hashlib.sha256()
            with path.open('rb') as stream:
                for block in iter(lambda:stream.read(1_000_000),b''):
                    self._remaining(); checksum.update(block)
            if checksum.hexdigest() != saved.get('content_hash'):
                raise SourceRecoveryError('invalid_archived_source')
            return count, True
        return maximum + 1, False  # Legacy injected opaque fake: no invented byte count.

    def _archived_header(self, saved):
        metadata = saved.get('metadata', {})
        text_path = metadata.get('text_path')
        if not text_path or not Path(text_path).resolve().is_relative_to(self.sources.resolve()) or Path(text_path).is_symlink():
            return None
        checksum, prefix = hashlib.sha256(), bytearray()
        with Path(text_path).open('rb') as stream:
            for block in iter(lambda:stream.read(1_000_000),b''):
                self._remaining(); checksum.update(block)
                if len(prefix) < 120000:
                    prefix.extend(block[:120000-len(prefix)])
        if checksum.hexdigest() != metadata.get('text_sha256'):
            return None
        return bytes(prefix).decode('utf-8',errors='ignore')[:30000]

    def _matches(self, saved, identity):
        if not any(k in identity for k in ('arxiv_id','doi','content_hash')):
            return False
        if identity.get('content_hash') and identity['content_hash'] != saved.get('content_hash'):
            return False
        metadata = saved.get('metadata', {})
        final = _url(metadata.get('final_url', saved.get('url', '')))
        observed = _infer(final)
        if identity.get('arxiv_id') and observed.get('arxiv_id') and any(observed.get(k) != identity.get(k) for k in ('arxiv_id','arxiv_version') if identity.get(k) is not None):
            return False
        if identity.get('doi') and observed.get('doi') and observed['doi'] != identity['doi']:
            return False
        header = self._archived_header(saved)
        if header is None:
            return bool(identity.get('content_hash')) and not any(k in identity for k in ('doi','arxiv_id','title'))
        if identity.get('arxiv_id'):
            token = identity['arxiv_id'] + ('v' + str(identity['arxiv_version']) if identity.get('arxiv_version') else '')
            pattern = r'(?<![\w.])' + r'\s*'.join(re.escape(c) for c in token) + r'(?![\w.])'
            if not re.search(pattern,header.casefold()):
                return False
        if identity.get('doi'):
            pattern = r'(?<![\w.])' + r'\s*'.join(re.escape(c) for c in identity['doi']) + r'(?![\w/])'
            if not re.search(pattern,header.casefold()):
                return False
        if identity.get('title') and _normalized(identity['title']) not in _normalized(header):
            return False
        return True

    def verify_cached(self, saved, url, expected_identity=None):
        """Verify existing bytes only; never reserve, refetch, read-credit or resolve."""
        original, explicit, identity = _merged_identity(url, expected_identity)
        if not isinstance(saved,dict) or not isinstance(saved.get('content_hash'),str) or not re.fullmatch('[0-9a-f]{64}',saved['content_hash']):
            raise SourceRecoveryError('invalid_cached_source')
        try:
            count, known = self._raw_measure(saved,self.limits['file_bytes'])
            _url(saved.get('metadata',{}).get('final_url',saved.get('url',original)))
            if not known or self._archived_header(saved) is None:
                raise SourceRecoveryError('invalid_cached_source')
            checked = self._matches(saved,identity)
        except SourceRecoveryError:
            raise
        except (OSError,ValueError,TypeError,KeyError) as exc:
            raise SourceRecoveryError('invalid_cached_source') from exc
        if any(k in identity for k in ('doi','arxiv_id','content_hash')) and not checked:
            raise SourceRecoveryError('cache_identity_mismatch',{'expected_identity':identity,'source_hash':saved['content_hash']})
        return {'identity_checked':checked,'expected_identity':copy.deepcopy(identity),'source_hash':saved['content_hash'],
                'text_sha256':saved['metadata']['text_sha256'],'archived_bytes':count,'cache_integrity_checked':True,
                'source_read_credit':False,'scientific_approval':False,'failure_resolved':False}

    def _alternatives(self, original, identity, official_urls):
        candidates = []
        if _is_arxiv(original) and identity.get('arxiv_id') and identity.get('arxiv_version'):
            token = identity['arxiv_id'] + 'v' + str(identity['arxiv_version'])
            candidates += ['https://arxiv.org/html/' + token, 'https://arxiv.org/pdf/' + token]
        elif urlsplit(original).hostname in {'doi.org','dx.doi.org'} and identity.get('doi'):
            candidates += ['https://doi.org/' + identity['doi'], 'https://dx.doi.org/' + identity['doi']]
        if official_urls and not any(k in identity for k in ('doi','arxiv_id','content_hash')):
            raise SourceRecoveryError('alternate_identity_required')
        for url in official_urls:
            checked = _url(url)
            if urlsplit(checked).scheme != 'https' or _is_arxiv(checked) and not _is_arxiv(original):
                raise SourceRecoveryError('unsafe_alternate')
            candidates.append(checked)
        result = []
        for url in candidates:
            url = _url(url)
            if url != original and url not in result:
                result.append(url)
        return result[:self.limits['replacements']]

    def fetch(self, url, expected_identity=None, official_urls=(), obligation_id=None):
        original, explicit, identity = _merged_identity(url, expected_identity)
        if obligation_id is not None and (not isinstance(obligation_id,str) or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,200}',obligation_id)):
            raise ValueError('obligation_id must be a bounded identifier')
        if not isinstance(official_urls,(tuple,list)) or len(official_urls) > 2:
            raise ValueError('At most2 predeclared official equivalents are accepted')
        alternatives = self._alternatives(original,identity,official_urls)
        attempts, queue, retried_size = [], [(original,self.limits['initial_bytes'])], False
        while queue:
            current, maximum = queue.pop(0)
            try:
                timeout = self._remaining()
                admission = self.snapshot()
                if admission['outstanding_attempt_ids']:
                    raise SourceRecoveryError('outstanding_download_attempt')
                if not admission['remaining_attempts'] or admission['remaining_bytes'] < 2:
                    raise SourceRecoveryError('download_budget_exhausted')
                if attempts and _is_arxiv(current) and self.before_attempt is None:
                    raise SourceRecoveryError('provider_spacing_hook_required')
                if self.before_attempt:
                    self.before_attempt(current,len(attempts))
                timeout = min(timeout,self._remaining())
            except Exception as exc:
                code = exc.code if isinstance(exc,SourceRecoveryError) else 'pre_attempt_aborted'
                raise SourceRecoveryError(code,{'attempts':attempts,'accounting':self.snapshot()}) from exc
            attempt = self._reserve(current,maximum,len(attempts),obligation_id)
            try:
                saved = self.fetch_source(current,self.sources,timeout=timeout,max_bytes=attempt['max_bytes'],refresh=True)
                if not isinstance(saved,dict) or not isinstance(saved.get('content_hash'),str) or not re.fullmatch('[0-9a-f]{64}',saved['content_hash']):
                    raise SourceRecoveryError('invalid_archived_source')
                _url(saved.get('metadata',{}).get('final_url',saved.get('url','')))
                count,known = self._raw_measure(saved,attempt['max_bytes'])
                # Initial legacy fetches do not gain new identity credit implicitly.
                verified = self._matches(saved,identity) if explicit or attempts else False
                if (explicit or attempts and current != original) and not verified:
                    attempts.append(self._settle(attempt,charged=count,known=known,code='identity_mismatch',source_hash=saved['content_hash']))
                else:
                    self._remaining()
                    attempts.append(self._settle(attempt,charged=count,known=known,code='success',source_hash=saved['content_hash']))
                    result=copy.deepcopy(saved)
                    result['url']=display_url(result.get('url',current))
                    if result.get('metadata',{}).get('final_url'):
                        result['metadata']['final_url']=display_url(result['metadata']['final_url'])
                    result['_recovery']={'attempts':attempts,'accounting':self.snapshot(),'expected_identity':identity,
                        'identity_verified':verified,'identity_check':'URL contradiction checks plus archived header identifiers/title; never mathematical applicability',
                        'requires_source_read':True,'source_read_credit':False,'scientific_approval':False,'failure_resolved':False}
                    return result
            except BaseException as exc:
                # A settled identity mismatch must not be charged twice.
                if not attempts or attempts[-1]['attempt_id'] != attempt['attempt_id']:
                    declared = isinstance(exc,DiscoveryError) and str(exc)==_DECLARED_SIZE
                    size = isinstance(exc,DiscoveryError) and str(exc) in {_DECLARED_SIZE,_BODY_SIZE,_DECOMPRESSED_SIZE,_SOURCE_SIZE}
                    code = 'size_limit_declared' if declared else 'size_limit_unknown_bytes' if size else exc.code if isinstance(exc,SourceRecoveryError) else 'download_failed'
                    attempts.append(self._settle(attempt,charged=0 if declared else attempt['reserved_bytes'],known=declared,code=code))
                else:
                    size=False; code='identity_mismatch'
                if isinstance(exc,(KeyboardInterrupt,SystemExit)):
                    raise
                if isinstance(exc,SourceRecoveryError) and exc.code=='stage_time_exhausted':
                    raise SourceRecoveryError(exc.code,{'attempts':attempts,'accounting':self.snapshot()}) from exc
                if isinstance(exc,SourceRecoveryError) and exc.code in {'unsafe_url','invalid_archived_source'}:
                    raise SourceRecoveryError(exc.code,{'attempts':attempts,'accounting':self.snapshot()}) from exc
                rate_limited=isinstance(exc,DiscoveryError) and 'HTTP 429' in str(exc)
                if rate_limited:
                    raise SourceRecoveryError('rate_limited',{'attempts':attempts,'accounting':self.snapshot()}) from exc
                if size and current==original and not retried_size and attempt['max_bytes']<self.limits['file_bytes']:
                    retried_size=True;queue.insert(0,(original,self.limits['file_bytes']));continue
            if alternatives:
                queue.append((alternatives.pop(0),self.limits['file_bytes']))
        accounting=self.snapshot()
        code='download_budget_exhausted' if accounting['remaining_bytes']<2 or not accounting['remaining_attempts'] else 'recovery_exhausted'
        raise SourceRecoveryError(code,{'attempts':attempts,'accounting':accounting})
