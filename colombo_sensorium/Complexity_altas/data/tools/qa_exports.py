#!/usr/bin/env python3
"""Read-only PDF QA against the frozen current export manifest.

Run with the bundled Python that contains pypdf/pdfplumber/Pillow. All PDFs
are read only; contact sheets and page renders are written under tmp/pdfs.
Layout heuristics produce review alerts, never an assertion of scientific
correctness. --reviewed-setting records actual agent visual review, not an
automatic inference from successful rendering.
"""
from __future__ import annotations

import argparse
import collections
import copy
import concurrent.futures
import hashlib
import json
import logging
import pathlib
import re
import subprocess
import sys
import unicodedata
import warnings
from datetime import datetime, timezone
from urllib.parse import unquote, urlsplit, urlunsplit

import pdfplumber
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / 'data/audit/exports.json'
DEFAULT_OUTPUT = ROOT / 'data/audit/exports_pdf_qa.json'
DEFAULT_WORK = ROOT / 'tmp/pdfs/full_qa'
DEFAULT_RENDERER = 'pdftoppm'
REPRESENTATIVES = [
    'CV_S_HIGH_VI', 'CV_S_HIGH_SADDLE_tan', 'CV_S_FS_NCSC_AS',
    'CV_S_NCSC_UNLOCALIZED', 'CV_S_SIMPLEX_MATRIX_GAME',
    'BL_SPEC_det_derivative', 'BL_SPEC_direct_reduced', 'BL_SPEC_stoch_derivative',
    'BL_SPEC_two_point_coupled', 'BL_SPEC_zo_common_sample',
    'MX_S_stream_bits', 'MX_S_noisy_power', 'MX_S_matmul_rect',
    'ON_FC_S', 'ONX_FED_TWO_LINEAR', 'ONX_NS_VAR_QKNOWN_VUNKNOWN',
    'SO_FO_C05_full_FG', 'SO_FO_N05_SD', 'SO_FO_O02_hidden_curve',
    'SO_HO_HOI01_S', 'SO_HO_HOS04_S_hvp', 'SO_HO_HOS04_S_higher',
    'SO_HO_HOC09_S', 'SO_HO_HON09_S_convexQh',
    'SO_ZO_N04a_gaussian', 'SO_ZO_N04b_variance_class',
    'SO_ZO_B05_rand_multi_resource', 'SO_ZO_S02_rand_native',
]


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def normalize_url(value):
    parts = urlsplit(unquote(str(value)))
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip('/'), parts.query, parts.fragment))


def cleaned_text(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', value or '')).strip()


def inspect_one(record):
    sid = record['setting_id']
    result = {'setting_id': sid, 'pdf_status': record.get('pdf_status'), 'errors': [], 'alerts': [],
              'compilation': record.get('compilation', {}), 'pages': [], 'reference_urls': [],
              'uri_annotations': [], 'readable': False, 'page_count': 0}
    texts = []
    try:
        source = ROOT / record['source']
        profile = load(source)
        result['primary_domain'] = profile['primary_domain']
        result['source_sha256'] = sha(source)
        if result['source_sha256'] != record['source_sha256']:
            result['errors'].append('Source profile differs from export manifest')
        classification = source.with_name('classification.json')
        if record.get('classification_sha256') and sha(classification) != record['classification_sha256']:
            result['errors'].append('Classification differs from export manifest')
        for field in ['tex', 'markdown', 'pdf']:
            if not record.get(field):
                result['errors'].append('Export manifest has no ' + field + ' output')
                continue
            path = ROOT / record[field]
            if not path.exists():
                result['errors'].append('Output missing: ' + record[field])
            elif sha(path) != record.get(field + '_sha256'):
                result['errors'].append(field + ' hash differs from export manifest')
        if record.get('pdf_status') != 'compiled' or not record.get('pdf'):
            result['errors'].append('PDF is not a compiled final output')
            return result, texts
        pdf = ROOT / record['pdf']
        result['pdf'] = record['pdf']
        result['pdf_sha256'] = sha(pdf)
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter('always')
            reader = PdfReader(str(pdf), strict=False)
            result['page_count'] = len(reader.pages)
            if reader.is_encrypted:
                result['errors'].append('PDF is encrypted')
            for page_number, page in enumerate(reader.pages, 1):
                for reference in page.get('/Annots', []):
                    annotation = reference.get_object()
                    action = annotation.get('/A')
                    if action:
                        action = action.get_object()
                    if action and action.get('/S') == '/URI':
                        uri = str(action.get('/URI', ''))
                        result['uri_annotations'].append({'page': page_number, 'uri': uri,
                                                          'subtype': str(annotation.get('/Subtype'))})
            result['reader_warnings'] = [str(item.message) for item in captured]
        expected = [item['url'] for item in profile.get('references', []) if item.get('url')]
        actual = {normalize_url(item['uri']) for item in result['uri_annotations']}
        result['reference_urls'] = expected
        result['missing_reference_urls'] = [url for url in expected if normalize_url(url) not in actual]
        if result['missing_reference_urls']:
            result['errors'].append('Reference URL absent from real PDF URI annotations')
        if expected and not result['uri_annotations']:
            result['errors'].append('PDF contains no URI link annotations')
        with pdfplumber.open(pdf) as document:
            for page_number, page in enumerate(document.pages, 1):
                raw = page.extract_text(layout=False) or ''
                normalized = cleaned_text(raw)
                texts.append(normalized)
                chars = [item for item in page.chars if str(item.get('text', '')).strip()]
                body = [item for item in chars if item['top'] >= 43 and item['bottom'] <= page.height - 35]
                physical = [item for item in chars
                            if item['x0'] < -1 or item['x1'] > page.width + 1
                            or item['top'] < -1 or item['bottom'] > page.height + 1]
                marginal = [item for item in body if item['x0'] < 35 or item['x1'] > page.width - 35]
                mathchars = [item for item in body if any(word in str(item.get('fontname', '')).lower()
                                                       for word in ['math', 'cmmi', 'cmsy', 'cmex', 'msam', 'msbm'])]
                small = [item for item in mathchars if 0 < float(item.get('size', 0)) < 3.6]
                bbox = ([round(min(item['x0'] for item in body), 2), round(min(item['top'] for item in body), 2),
                         round(max(item['x1'] for item in body), 2), round(max(item['bottom'] for item in body), 2)]
                        if body else None)
                stat = {'page': page_number, 'width_pt': round(page.width, 2), 'height_pt': round(page.height, 2),
                        'body_characters': len(body), 'body_bbox_pt': bbox,
                        'physical_overflow_count': len(physical), 'margin_alert_characters': len(marginal),
                        'small_math_character_count': len(small), 'math_character_count': len(mathchars),
                        'minimum_math_font_pt': round(min((float(item['size']) for item in mathchars), default=0), 2),
                        'body_text_excerpt': normalized[:180]}
                result['pages'].append(stat)
                for pattern, message in [(r'\bCoverage\b', 'Excluded Coverage label'),
                                         (r'information\s+interface', 'Old Information interface label')]:
                    if re.search(pattern, normalized, re.IGNORECASE):
                        result['errors'].append(message + ' on page ' + str(page_number))
                if '\ufffd' in raw:
                    result['errors'].append('Replacement character U+FFFD on page ' + str(page_number))
                if re.search(r'\(cid:\d+\)', raw):
                    result['alerts'].append({'page': page_number, 'kind': 'unmapped_character_identifier',
                                             'detail': 'Text mapping may be incomplete; verify rendered glyphs.'})
                if any(char in raw for char in ['\u25a0', '\u25a1', '\u2610']):
                    result['alerts'].append({'page': page_number, 'kind': 'square_glyph',
                                             'detail': 'May be a valid mathematical square or a missing glyph; visual review required.'})
                if not body:
                    result['errors'].append('Blank content page ' + str(page_number))
                elif len(body) < 25:
                    result['alerts'].append({'page': page_number, 'kind': 'sparse_page', 'detail': str(len(body)) + ' body characters'})
                if physical:
                    result['errors'].append('Character bounds exceed physical page ' + str(page_number))
                if marginal:
                    result['alerts'].append({'page': page_number, 'kind': 'margin_proximity',
                                             'detail': 'Content comes within 35pt of a left or right page edge.',
                                             'characters': ''.join(item['text'] for item in marginal)[:150]})
                if len(small) >= 5:
                    result['alerts'].append({'page': page_number, 'kind': 'small_math_glyphs',
                                             'detail': 'At least five math glyphs have a font size below 3.6pt; superscripts may be legitimate.',
                                             'characters': ''.join(item['text'] for item in small)[:150]})
                if hasattr(page, 'close'):
                    page.close()
        result['readable'] = bool(result['page_count'] and texts)
        if len(texts) != result['page_count']:
            result['errors'].append('Reader and text extractor disagree on page count')
        if not texts or sum(len(item) for item in texts) < 100:
            result['errors'].append('Extracted profile content is unexpectedly empty')
        compile_warnings = record.get('compilation', {}).get('warnings', [])
        if any(re.search(r'missing character|undefined control sequence|font.*not found', item, re.IGNORECASE)
               for item in compile_warnings):
            result['errors'].append('Compilation reports a missing glyph/font or undefined control sequence')
        if compile_warnings:
            result['alerts'].append({'kind': 'compilation_warnings', 'detail': compile_warnings})
    except Exception as error:
        result['errors'].append(type(error).__name__ + ': ' + str(error))
    return result, texts


def select_representatives(records, results, count):
    available = {result['setting_id']: result for result in results if result.get('readable')}
    ordered = [sid for sid in REPRESENTATIVES if sid in available]
    domains = collections.defaultdict(list)
    for record in records:
        result = available.get(record['setting_id'])
        if result:
            domains[result['primary_domain']].append(result['setting_id'])
    selected_domains = {available[sid]['primary_domain'] for sid in ordered}
    for domain, ids in domains.items():
        if domain not in selected_domains:
            ordered.insert(0, ids[0])
    if len(ordered) > count:
        # Keep domain-mandatory additions and then the requested special cases.
        ordered = ordered[:count]
    for record in records:
        sid = record['setting_id']
        if len(ordered) >= count:
            break
        if sid in available and sid not in ordered:
            ordered.append(sid)
    return ordered


def page_choices(result, texts):
    first = next((index for index, value in enumerate(texts) if 'Complexity bracket' in value), 0)
    end = next((index for index in range(first, len(texts)) if 'Bounds and supporting evidence' in texts[index]), len(texts) - 1)
    candidates = range(first, min(len(texts), max(first + 1, end + 1)))
    def complexity(index):
        value = texts[index]
        return (value.count('Lower bound') + value.count('Upper bound')) * 80 + result['pages'][index]['math_character_count'] + len(re.findall(r'[ΩΘε∇κβΔ≤≥]', value)) * 3
    bracket = max(candidates, key=complexity)
    return [{'role': 'opening', 'page': 1}, {'role': 'complex_bracket', 'page': bracket + 1},
            {'role': 'ending', 'page': result['page_count']}]


def render_page(pdf, page_number, output, dpi, renderer):
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = output.with_suffix('.json')
    fingerprint = {'pdf_sha256': sha(pdf), 'page': page_number, 'dpi': dpi}
    if output.exists() and metadata.exists() and load(metadata) == fingerprint:
        return {'path': rel(output), 'page': page_number, 'dpi': dpi, 'sha256': sha(output), 'cached': True}
    prefix = output.with_suffix('')
    command = [renderer, '-f', str(page_number), '-l', str(page_number), '-singlefile',
               '-r', str(dpi), '-png', str(pdf), str(prefix)]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if completed.returncode or not output.exists():
        raise RuntimeError('Page render failed: ' + (completed.stderr or completed.stdout)[-1200:])
    write(metadata, fingerprint)
    return {'path': rel(output), 'page': page_number, 'dpi': dpi, 'sha256': sha(output), 'cached': False}


def make_contact(sid, pages, output):
    thumb_width, head_height, caption_height, gap = 340, 42, 28, 12
    images = []
    for item in pages:
        with Image.open(ROOT / item['path']) as original:
            target_height = round(original.height * thumb_width / original.width)
            images.append(original.convert('RGB').resize((thumb_width, target_height), Image.Resampling.LANCZOS))
    height = max(image.height for image in images) + head_height + caption_height + gap
    canvas = Image.new('RGB', (len(images) * (thumb_width + gap) + gap, height), '#e4e8e5')
    draw = ImageDraw.Draw(canvas)
    draw.text((gap, 10), sid, fill='#18334c')
    for index, (image, item) in enumerate(zip(images, pages)):
        x = gap + index * (thumb_width + gap)
        draw.text((x, head_height), item['role'] + ' / page ' + str(item['page']), fill='#18334c')
        canvas.paste(image, (x, head_height + caption_height))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    return {'path': rel(output), 'sha256': sha(output), 'width': canvas.width, 'height': canvas.height}


def reusable_inspection(record, previous):
    """Reuse PDF parsing only for exactly unchanged PDF and source bytes."""
    if not previous or previous.get('errors') or not previous.get('readable'):
        return None
    if previous.get('pdf_sha256') != record.get('pdf_sha256') or previous.get('source_sha256') != record.get('source_sha256'):
        return None
    for field, hash_field in [('source', 'source_sha256'), ('tex', 'tex_sha256'),
                              ('markdown', 'markdown_sha256'), ('pdf', 'pdf_sha256')]:
        path = ROOT / record.get(field, '')
        if not path.is_file() or sha(path) != record.get(hash_field):
            return None
    source = ROOT / record['source']
    if record.get('classification_sha256') and sha(source.with_name('classification.json')) != record['classification_sha256']:
        return None
    result = copy.deepcopy(previous)
    result['compilation'] = record.get('compilation', {})
    result['pdf_status'] = record.get('pdf_status')
    result['reused_unchanged_pdf_inspection'] = True
    result['alerts'] = [item for item in result['alerts'] if item['kind'] != 'compilation_warnings']
    if result['compilation'].get('warnings'):
        result['alerts'].append({'kind': 'compilation_warnings', 'detail': result['compilation']['warnings']})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--output', type=pathlib.Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--work', type=pathlib.Path, default=DEFAULT_WORK)
    parser.add_argument('--renderer', default=DEFAULT_RENDERER)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--representatives', type=int, default=28)
    parser.add_argument('--risk-pages', type=int, default=12)
    parser.add_argument('--setting-id', action='append')
    parser.add_argument('--skip-render', action='store_true')
    parser.add_argument('--reuse-machine-report', type=pathlib.Path,
                        help='Reuse prior successful parsing only when PDF and source bytes still match; all current manifest hashes are rechecked')
    parser.add_argument('--review-log', type=pathlib.Path, default=DEFAULT_WORK / 'visual_reviews.json')
    parser.add_argument('--record-reviewed-setting', action='append', default=[],
                        help='Record actual inspection of the existing contact sheet and its original PDF hash, then exit without scanning')
    parser.add_argument('--reviewed-setting', action='append', default=[],
                        help='Record an actually visually inspected representative contact sheet for this unchanged PDF')
    args = parser.parse_args()
    if args.record_reviewed_setting:
        previous = load(args.output)
        samples = {item['setting_id']: item for item in previous['representatives']}
        review_log = load(args.review_log) if args.review_log.exists() else {'schema_version': '1.0.0', 'reviews': []}
        for sid in args.record_reviewed_setting:
            sample = samples[sid]
            contact = ROOT / sample['contact_sheet']['path']
            if sha(contact) != sample['contact_sheet']['sha256']:
                parser.error('Contact sheet differs from the inspected report: ' + sid)
            review_log['reviews'].append({'setting_id': sid, 'pdf_sha256': sample['pdf_sha256'],
                                          'contact_sha256': sample['contact_sheet']['sha256'],
                                          'pages': [item['page'] for item in sample['pages']],
                                          'reviewed_at_utc': datetime.now(timezone.utc).isoformat(),
                                          'reviewer': 'agent_actual_visual_inspection'})
        write(args.review_log, review_log)
        print(json.dumps({'recorded': args.record_reviewed_setting, 'review_log': rel(args.review_log)}))
        return 0
    manifest_hash = sha(args.manifest)
    manifest = load(args.manifest)
    records = manifest['profiles']
    if args.setting_id:
        records = [record for record in records if record['setting_id'] in args.setting_id]
    if not records:
        parser.error('No selected export records')
    results, texts = [], {}
    previous_report = load(args.reuse_machine_report) if args.reuse_machine_report and args.reuse_machine_report.exists() else {}
    previous_by_id = {item['setting_id']: item for item in previous_report.get('profiles', [])}
    previous_samples = {item['setting_id']: item for item in previous_report.get('representatives', [])}
    queued = []
    for record in records:
        reused = reusable_inspection(record, previous_by_id.get(record['setting_id']))
        if reused is None:
            queued.append(record)
        else:
            results.append(reused)
    reused_count = len(results)
    if reused_count:
        print(json.dumps({'reused_unchanged_pdf_scans': reused_count, 'new_scans': len(queued)}), flush=True)
    logging.getLogger('pypdf').setLevel(logging.ERROR)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(inspect_one, record): record['setting_id'] for record in queued}
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result, page_texts = future.result()
            results.append(result)
            texts[result['setting_id']] = page_texts
            if index % 40 == 0 or index == len(queued):
                print(json.dumps({'inspected': index + reused_count, 'of': len(records)}, ensure_ascii=False), flush=True)
    order = {record['setting_id']: index for index, record in enumerate(records)}
    results.sort(key=lambda item: order[item['setting_id']])
    by_id = {result['setting_id']: result for result in results}
    representative_ids = select_representatives(records, results, args.representatives)
    review_log = load(args.review_log) if args.review_log.exists() else {'reviews': []}
    reviewed_hashes = {(item['setting_id'], item['pdf_sha256'], item['contact_sha256']) for item in review_log['reviews']}
    samples, render_errors = [], []
    for sid in representative_ids:
        result = by_id[sid]
        if sid in texts:
            pages = page_choices(result, texts[sid])
        elif sid in previous_samples and previous_samples[sid]['pdf_sha256'] == result['pdf_sha256']:
            pages = [{key: item[key] for key in ['role', 'page']} for item in previous_samples[sid]['pages']]
        else:
            with pdfplumber.open(ROOT / result['pdf']) as document:
                pages = page_choices(result, [cleaned_text(page.extract_text() or '') for page in document.pages])
        sample = {'setting_id': sid, 'primary_domain': result['primary_domain'],
                  'pdf_sha256': result['pdf_sha256'], 'page_count': result['page_count'], 'pages': pages,
                  'visual_review': 'confirmed_by_agent' if sid in args.reviewed_setting else 'pending'}
        if not args.skip_render:
            try:
                for item in pages:
                    item.update(render_page(ROOT / result['pdf'], item['page'],
                                            args.work / 'pages' / sid / (item['role'] + '.png'), 80, args.renderer))
                sample['contact_sheet'] = make_contact(sid, pages, args.work / 'contacts' / (sid + '.png'))
                if (sid, result['pdf_sha256'], sample['contact_sheet']['sha256']) in reviewed_hashes:
                    sample['visual_review'] = 'confirmed_by_agent_for_this_pdf_sha256'
            except Exception as error:
                render_errors.append({'setting_id': sid, 'error': str(error)})
        samples.append(sample)
    risk = []
    for result in results:
        for alert in result['alerts']:
            if alert.get('page'):
                risk.append((result, alert['page'], alert['kind']))
    priority = {'margin_proximity': 0, 'small_math_glyphs': 1, 'sparse_page': 2, 'square_glyph': 3,
                'unmapped_character_identifier': 4}
    risk.sort(key=lambda item: (priority.get(item[2], 9), order[item[0]['setting_id']], item[1]))
    seen, seen_profiles, diverse, remaining = set(), set(), [], []
    for item in risk:
        result, page, reason = item
        key = (result['setting_id'], page)
        if key in seen:
            continue
        seen.add(key)
        if result['setting_id'] not in seen_profiles:
            diverse.append(item)
            seen_profiles.add(result['setting_id'])
        else:
            remaining.append(item)
    risk = diverse + remaining
    # Dense/small mathematical pages are still inspected if no heuristic alerts exist.
    densest = sorted(((result, page['page'], 'dense_mathematical_page') for result in results for page in result['pages']),
                     key=lambda item: (item[0]['pages'][item[1] - 1]['small_math_character_count'],
                                       item[0]['pages'][item[1] - 1]['math_character_count']), reverse=True)
    for item in densest:
        if len(risk) >= args.risk_pages:
            break
        if (item[0]['setting_id'], item[1]) not in seen:
            risk.append(item)
            seen.add((item[0]['setting_id'], item[1]))
    risk_renders = []
    if not args.skip_render:
        for result, page, reason in risk[:args.risk_pages]:
            try:
                item = render_page(ROOT / result['pdf'], page,
                                   args.work / 'risk' / (result['setting_id'] + '-p' + str(page) + '.png'), 170, args.renderer)
                risk_renders.append({'setting_id': result['setting_id'], 'reason': reason, **item})
            except Exception as error:
                render_errors.append({'setting_id': result['setting_id'], 'page': page, 'error': str(error)})
    manifest_unchanged = sha(args.manifest) == manifest_hash
    errors = [{'setting_id': result['setting_id'], 'detail': error} for result in results for error in result['errors']]
    if not manifest_unchanged:
        errors.append({'detail': 'exports.json changed during QA; rerun against the final frozen manifest'})
    if manifest.get('renderer_sha256') and sha(ROOT / manifest['renderer']) != manifest['renderer_sha256']:
        errors.append({'detail': 'Current renderer differs from the export manifest'})
    warnings_summary = [{'setting_id': result['setting_id'], 'warnings': result['compilation'].get('warnings', [])}
                        for result in results if result['compilation'].get('warnings')]
    alert_count = sum(len(result['alerts']) for result in results)
    visually_reviewed = sum(sample['visual_review'].startswith('confirmed_by_agent') for sample in samples)
    report = {
        'schema_version': '1.0.0', 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'manifest': rel(args.manifest), 'manifest_sha256': manifest_hash, 'manifest_unchanged': manifest_unchanged,
        'selection': 'all_exported_profiles' if not args.setting_id else args.setting_id,
        'profile_count': len(results), 'page_count': sum(result['page_count'] for result in results),
        'reused_unchanged_pdf_inspections': reused_count,
        'readable_pdf_count': sum(result['readable'] for result in results),
        'reference_url_count': sum(len(result['reference_urls']) for result in results),
        'uri_annotation_count': sum(len(result['uri_annotations']) for result in results),
        'machine_checks_passed': not errors and not render_errors, 'errors': errors, 'render_errors': render_errors,
        'alert_count': alert_count, 'compilation_warnings': warnings_summary,
        'representative_profile_count': len(samples), 'representatives': samples, 'high_resolution_risk_pages': risk_renders,
        'visual_review': {'status': 'complete_for_representatives' if visually_reviewed == len(samples) and samples else 'pending_or_partial',
                          'reviewed_representatives': visually_reviewed, 'total_representatives': len(samples),
                          'scope': 'Opening, complex-bracket and ending pages for the selected representative PDFs; the entire corpus receives machine checks.'},
        'profiles': results,
        'limitations': ['Text extraction and bounding-box checks do not establish mathematical correctness or all glyph shapes.',
                        'Margin, square-glyph and small-font alerts require rendered-page assessment; they are not silently treated as passes.',
                        'Only actual inspection may be recorded using --reviewed-setting. High-resolution risk pages remain separately listed.'],
    }
    report['passed'] = report['machine_checks_passed'] and report['visual_review']['status'] == 'complete_for_representatives' and not alert_count
    write(args.output, report)
    print(json.dumps({key: report[key] for key in ['profile_count', 'page_count', 'readable_pdf_count',
                     'machine_checks_passed', 'alert_count', 'representative_profile_count', 'passed']}, ensure_ascii=False), flush=True)
    return 0 if report['machine_checks_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
