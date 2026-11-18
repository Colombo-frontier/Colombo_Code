"""The controller supplies only small descriptors of authorized fixed sources; cloning does not replace scientific research or approval."""
from copy import deepcopy
import json

import pytest

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import digest
from oracle_atlas.workflow.engine import Engine


class ArtifactBag:
    def __init__(self):
        self.items = {}

    def put(self, kind, data, *args):
        ref = 'sha256:' + digest({'kind': kind, 'data': data})
        self.items[ref] = {'kind': kind, 'data': deepcopy(data), 'producer': 'controller-fixture'}
        return ref

    def get(self, ref):
        if ref not in self.items:
            raise ProtocolError('Missing synthetic source record')
        return deepcopy(self.items[ref])


class CaseRecorder:
    def __init__(self):
        self.saved = []

    def save_case(self, case):
        self.saved.append(deepcopy(case))


@pytest.fixture
def seed():
    e = object.__new__(Engine)
    e.artifacts = ArtifactBag()
    e.ws = CaseRecorder()
    e.put = e.artifacts.put
    candidate = e.put('candidate', {'candidate_id': 'engineering-source-descriptor-only'})
    identity = e.put('identity', {'candidate_ref': candidate, 'decision': 'existing', 'setting_id': 'SEED_SETTING'})
    profile = {'setting_id': 'SEED_SETTING', 'reader_markdown': 'DO_NOT_EMBED_PROFILE_BODY_' * 8000,
               'common_specification': {'task': {'summary': 'No scientific claim in this fixture.'}}}
    base = e.put('native_record', {'setting_id': 'SEED_SETTING', 'version': 'target-fixture-fixed', 'content': profile})
    case = {'case_id': 'clone-seed-case', 'candidate_ref': candidate, 'budget_scope': 'fixture-scope', 'jobs': {}}
    inputs = {'candidate_ref': candidate, 'identity_ref': identity, 'setting_id': 'SEED_SETTING',
              'base_profile_ref': base, 'base_version': 'target-fixture-fixed'}
    return {'e': e, 'case': case, 'inputs': inputs, 'profile': profile, 'base': base,
            'candidate': candidate, 'identity': identity}


def prior_research(c, *, candidate=None, identity=None, setting_id='SEED_SETTING', profile_kind='profile', profile_setting=None):
    profile = {**c['profile'], 'setting_id': profile_setting or setting_id}
    pref = c['e'].put(profile_kind, profile)
    ref = c['e'].put('research', {'candidate_ref': candidate or c['candidate'], 'identity_ref': identity or c['identity'],
                                 'setting_id': setting_id, 'profile_ref': pref})
    case = {**c['case'], 'previous_artifact_ref': ref}
    return case, pref, profile


def test_existing_seed_uses_fixed_native_content_digest(seed):
    source = seed['e']._profile_clone_source(seed['case'], seed['inputs'])
    assert source == {'source_ref': seed['base'], 'source_pointer': '/content', 'expected_digest': digest(seed['profile'])}
    assert len(json.dumps(source)) < 400


def test_research_revision_prefers_same_candidate_identity_frozen_profile(seed):
    case, pref, profile = prior_research(seed)
    source = seed['e']._profile_clone_source(case, seed['inputs'])
    assert source == {'source_ref': pref, 'source_pointer': '', 'expected_digest': digest(profile)}
    assert source['source_ref'] != seed['base']


def test_initial_new_research_has_no_clone_seed(seed):
    inputs = {k: v for k, v in seed['inputs'].items() if k not in {'base_profile_ref', 'base_version'}}
    inputs.update(setting_id=None, base_version=None)
    assert seed['e']._profile_clone_source(seed['case'], inputs) is None


def test_new_research_revision_can_copy_its_assigned_setting_without_inventing_identity(seed):
    case, pref, profile = prior_research(seed, setting_id='ASSIGNED_NEW_SETTING')
    inputs = {k: v for k, v in seed['inputs'].items() if k != 'base_profile_ref'}
    inputs.update(setting_id=None, base_version=None)
    assert seed['e']._profile_clone_source(case, inputs) == {
        'source_ref': pref, 'source_pointer': '', 'expected_digest': digest(profile)}


@pytest.mark.parametrize('field', ['candidate', 'identity'])
def test_prior_research_from_another_candidate_or_identity_is_rejected(seed, field):
    case, _, _ = prior_research(seed, **{field: 'sha256:' + 'f' * 64})
    with pytest.raises(ProtocolError):
        seed['e']._profile_clone_source(case, seed['inputs'])


def test_prior_research_source_must_be_profile(seed):
    case, _, _ = prior_research(seed, profile_kind='native_record')
    with pytest.raises(ProtocolError):
        seed['e']._profile_clone_source(case, seed['inputs'])


def test_prior_profile_setting_must_match_research(seed):
    case, _, _ = prior_research(seed, profile_setting='OTHER_SETTING')
    with pytest.raises(ProtocolError):
        seed['e']._profile_clone_source(case, seed['inputs'])


def test_existing_revision_cannot_change_current_setting(seed):
    case, _, _ = prior_research(seed, setting_id='OTHER_SETTING')
    with pytest.raises(ProtocolError):
        seed['e']._profile_clone_source(case, seed['inputs'])


@pytest.mark.parametrize('change', ['wrong_kind', 'wrong_version', 'wrong_setting', 'wrong_content_setting'])
def test_existing_native_seed_kind_version_and_setting_are_bound(seed, change):
    data = {'setting_id': 'SEED_SETTING', 'version': 'target-fixture-fixed', 'content': deepcopy(seed['profile'])}
    kind = 'native_record'
    if change == 'wrong_kind':
        kind = 'profile'
    elif change == 'wrong_version':
        data['version'] = 'target-other'
    elif change == 'wrong_setting':
        data['setting_id'] = 'OTHER_SETTING'
    else:
        data['content']['setting_id'] = 'OTHER_SETTING'
    inputs = {**seed['inputs'], 'base_profile_ref': seed['e'].put(kind, data)}
    with pytest.raises(ProtocolError):
        seed['e']._profile_clone_source(seed['case'], inputs)


@pytest.mark.parametrize('role,revision', [('bound_updater', False), ('bound_updater', True), ('profile_researcher', True)])
def test_stage_handoff_has_small_descriptor_and_formal_refs_without_profile_body(seed, monkeypatch, role, revision):
    e = seed['e']; case = deepcopy(seed['case']); inputs = deepcopy(seed['inputs'])
    if revision:
        case, _, _ = prior_research(seed)
        case.update(revision=1)
    if role == 'profile_researcher':
        inputs.pop('base_profile_ref'); inputs.update(setting_id=None, base_version=None)
    captured = []

    def job(role, values, scope):
        captured.append((role, deepcopy(values), scope))
        return {'id': 'paused-producer-fixture', 'status': 'queued'}, None

    monkeypatch.setattr(e, '_job', job)
    assert e._stage(case, role, inputs) is None
    _, values, scope = captured[0]
    assert scope == 'fixture-scope'
    assert set(values['profile_clone_source']) == {'source_ref', 'source_pointer', 'expected_digest'}
    assert 'DO_NOT_EMBED_PROFILE_BODY_' not in json.dumps(values)
    assert len(json.dumps(values)) < 2500
    assert values['coverage_scope_ref'].startswith('sha256:')
    assert e.ws.saved[-1]['jobs'][role] == 'paused-producer-fixture'


def test_first_new_stage_does_not_offer_or_embed_a_baseline(seed, monkeypatch):
    inputs = {k: v for k, v in seed['inputs'].items() if k != 'base_profile_ref'}
    inputs.update(setting_id=None, base_version=None)
    captured = []
    monkeypatch.setattr(seed['e'], '_job', lambda role, values, scope: (captured.append(values) or {'id': 'new-first', 'status': 'queued'}, None))
    seed['e']._stage(seed['case'], 'profile_researcher', inputs)
    assert 'profile_clone_source' not in captured[0]
    assert 'DO_NOT_EMBED_PROFILE_BODY_' not in json.dumps(captured[0])
