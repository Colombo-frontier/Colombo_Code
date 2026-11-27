"""Check six-family navigation without merging scientific tasks or rate claims."""
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
COUNTS = {'single_objective': 275, 'online_bandit': 68, 'minimax': 30,
          'matrix_computation': 30, 'bilevel': 26, 'variational_inequality': 16}
MOVES = {'CV_S_SIMPLEX_MATRIX_GAME': 'minimax',
         'CV_S_FS_SADDLE_GAP': 'minimax',
         'CV_S_STRICT_MATRIX_SADDLE_COMPARE': 'matrix_computation',
         'CV_S_NONSTRICT_MATRIX_SADDLE_COMPARE': 'matrix_computation'}


def read(relative):
    return json.loads((ROOT / relative).read_text())


def resolve(value, pointer):
    for token in pointer.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


class TaskFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profiles = {path.parent.name: json.loads(path.read_text())
                        for path in (ROOT / 'data/settings').glob('*/profile.json')}
        cls.overview = read('data/derived/atlas_overview.json')
        cls.points = {point['id']: point for point in cls.overview['points']}

    def test_primary_families_partition_the_inventory_in_contiguous_blocks(self):
        self.assertEqual(Counter(p['primary_domain'] for p in self.profiles.values()), COUNTS)
        catalog = read('data/derived/catalog.json')['profiles']
        self.assertEqual({row['id'] for row in catalog}, set(self.profiles))
        blocks = [task for task, _ in itertools.groupby(row['domain'] for row in catalog)]
        self.assertEqual(len(blocks), len(set(blocks)))
        self.assertEqual(set(blocks), set(COUNTS))
        self.assertEqual([row['order'] for row in catalog], list(range(1, 446)))
        for row in catalog:
            self.assertEqual(row['domain'], self.profiles[row['id']]['primary_domain'])

    def test_four_reassigned_tasks_bind_to_their_actual_source_values(self):
        for sid, family in MOVES.items():
            with self.subTest(setting=sid):
                profile = self.profiles[sid]
                self.assertEqual(profile['primary_domain'], family)
                classification = read(f'data/settings/{sid}/classification.json')
                self.assertEqual(classification['profile_sha256'], hashlib.sha256(
                    (ROOT / f'data/settings/{sid}/profile.json').read_bytes()).hexdigest())
                families = [tag for tag in classification['tags']
                            if tag['axis'] == 'TASK' and tag['group'] == 'task_family']
                self.assertIn(family, {tag['value'] for tag in families})
                for tag in families:
                    self.assertIn(tag['value'], COUNTS)
                    for pointer in tag['source_pointers']:
                        self.assertEqual(resolve(profile, pointer), tag['value'])
                self.assertEqual(self.points[sid]['task'], family)

    def test_all_five_vocabularies_expose_only_the_six_navigation_families(self):
        for name in ('taxonomy', 'tags', 'human_tags', 'machine_tags', 'browse_facets'):
            with self.subTest(vocabulary=name):
                vocabulary = read(f'data/vocabulary/{name}.json')
                records = [node for node in walk(vocabulary)
                           if node.get('axis') == 'TASK'
                           and node.get('group') in ('family', 'task_family')
                           and 'value' in node]
                self.assertEqual({node['value'] for node in records}, set(COUNTS))
                ids = {node.get('id', node.get('concept_id')) for node in walk(vocabulary)}
                self.assertNotIn('TASK:family:saddle_point', ids)
                self.assertNotIn('TASK:task_family:saddle_point', ids)
        self.assertEqual(set(self.overview['tasks']), set(COUNTS))
        nebula = read('data/derived/atlas_nebula.json')
        self.assertEqual({cluster['task']: cluster['count'] for cluster in nebula['clusters']}, COUNTS)
        for point in self.points.values():
            self.assertNotIn('TASK:family:saddle_point', point['memberships'])

    def test_cross_navigation_is_preserved_without_creating_extra_primary_tasks(self):
        sid = 'CV_S_SEPARATED_SADDLE'
        profile = self.profiles[sid]
        self.assertEqual(profile['primary_domain'], 'matrix_computation')
        self.assertEqual(set(profile['common_specification']['task']['navigation_domains']),
                         {'matrix_computation', 'minimax'})
        tags = read(f'data/settings/{sid}/human_tags.json')
        self.assertEqual({cid for cid in tags['views'][0]['facet_ids']
                          if cid.startswith('TASK:family:')},
                         {'TASK:family:matrix_computation', 'TASK:family:minimax'})
        for family in ('matrix_computation', 'minimax'):
            self.assertIn('TASK:family:' + family, self.points[sid]['memberships'])
        # The mixed-strategy game keeps matrix navigation only for its declared
        # deterministic view. Reclassification must not widen the other view.
        tags = read('data/settings/CV_S_SIMPLEX_MATRIX_GAME/human_tags.json')
        views = {view['view_id']: set(view['facet_ids']) for view in tags['views']}
        self.assertIn('TASK:family:matrix_computation', views['deterministic_risk'])
        self.assertNotIn('TASK:family:matrix_computation', views['randomized_accuracy'])
        self.assertIn('TASK:family:minimax', views['randomized_accuracy'])

    def test_higher_order_saddle_metrics_and_adopted_support_survive_under_minimax(self):
        contributions = read('data/derived/colombo_contributions.json')['settings']
        metrics = []
        for sid in ('CV_S_HIGH_SADDLE_gap', 'CV_S_HIGH_SADDLE_tan'):
            with self.subTest(setting=sid):
                profile = self.profiles[sid]
                self.assertEqual(profile['primary_domain'], 'minimax')
                self.assertIn('saddle-point', profile['title'].lower())
                self.assertEqual(profile['common_specification']['task']['formulation_code'],
                                 'convex_concave_saddle')
                metrics.append(profile['common_specification']['metric']['base_expression'])
                entry = contributions[sid]
                self.assertEqual(entry['state'], 'adopted')
                self.assertEqual(self.points[sid]['colombo']['state'], 'adopted')
                comparisons = {c['comparison_id']: c for c in profile['comparisons']}
                self.assertTrue(entry['comparison_ids'])
                self.assertTrue(set(entry['comparison_ids']) <= set(comparisons))
                for cid in entry['comparison_ids']:
                    # The scientific comparison retains its nontrivial parameter
                    # guard; moving a family cannot turn it into an unscoped row.
                    self.assertTrue(comparisons[cid].get('predicate_text'))
        self.assertNotEqual(*metrics)
        self.assertIn('\\max', metrics[0])
        self.assertIn('dist', metrics[1])

    def test_reclassification_does_not_close_unresolved_matrix_game_regions(self):
        profile = self.profiles['CV_S_SIMPLEX_MATRIX_GAME']
        codes = {comparison['status']['code'] for comparison in profile['comparisons']}
        self.assertIn('polynomial_gap', codes)
        self.assertIn('missing_lower', codes)
        self.assertNotIn('fully_optimal',
                         {badge['code'] for badge in profile['summary_status']['badges']})


if __name__ == '__main__':
    unittest.main()
