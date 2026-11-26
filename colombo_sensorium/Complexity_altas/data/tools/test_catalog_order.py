"""Check task-contiguous display ordinals without changing setting identities."""
from copy import deepcopy
import importlib.util
import itertools
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    'atlas_catalog_order', ROOT / 'visualization/src/catalog_order.py')
ordering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ordering)


def families(rows):
    return [family for family, _ in itertools.groupby(row['domain'] for row in rows)]


class CatalogOrderTests(unittest.TestCase):
    def test_interleaved_tasks_form_stable_contiguous_blocks(self):
        domains = ['minimax', 'single_objective', 'bilevel', 'minimax',
                   'online_bandit', 'bilevel', 'single_objective', 'online_bandit']
        catalog = {'profiles': [{'id': str(index), 'domain': domain, 'order': 100 + index,
                                 'views': ['frozen'], 'statusCodes': ['missing_lower']}
                                for index, domain in enumerate(domains)],
                   'schema_version': 'untouched'}
        before = deepcopy(catalog)
        result = ordering.order_catalog(catalog)
        self.assertEqual(families(result['profiles']),
                         ['single_objective', 'minimax', 'bilevel', 'online_bandit'])
        self.assertEqual([row['id'] for row in result['profiles']],
                         ['1', '6', '0', '3', '2', '5', '4', '7'])
        self.assertEqual([row['order'] for row in result['profiles']], list(range(1, 9)))
        self.assertEqual(ordering.order_catalog(result), result)
        self.assertEqual(catalog, before)
        original = {row['id']: row for row in catalog['profiles']}
        for row in result['profiles']:
            self.assertEqual({key: value for key, value in row.items() if key != 'order'},
                             {key: value for key, value in original[row['id']].items()
                              if key != 'order'})

    def test_absent_single_objective_and_new_task_keep_first_appearance_order(self):
        catalog = {'profiles': [{'id': str(index), 'domain': task}
                                for index, task in enumerate(
                                    ['bilevel', 'future_task', 'bilevel', 'future_task'])]}
        result = ordering.order_catalog(catalog)
        self.assertEqual(families(result['profiles']), ['bilevel', 'future_task'])
        self.assertEqual([row['id'] for row in result['profiles']], ['0', '2', '1', '3'])
        self.assertEqual(ordering.order_catalog(result), result)

    def test_empty_catalog_remains_empty(self):
        result = ordering.order_catalog({'profiles': []})
        self.assertEqual(result['profiles'], [])
        self.assertEqual(ordering.order_catalog(result), result)

    def test_saved_catalog_uses_the_same_grouping_and_is_idempotent(self):
        catalog = {'profiles': [{'id': 'a', 'domain': 'bilevel'},
                                {'id': 'b', 'domain': 'minimax'},
                                {'id': 'c', 'domain': 'bilevel'}]}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'catalog.json'
            path.write_text(json.dumps(catalog))
            path.chmod(0o640)
            expected = ordering.order_catalog(catalog)
            self.assertEqual(ordering.load_ordered_catalog(path), expected)
            self.assertEqual(json.loads(path.read_text()), expected)
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            contents = path.read_bytes()
            modified = path.stat().st_mtime_ns
            self.assertEqual(ordering.load_ordered_catalog(path), expected)
            self.assertEqual(path.read_bytes(), contents)
            self.assertEqual(path.stat().st_mtime_ns, modified)

    def test_current_inventory_groups_every_primary_task_without_scientific_edits(self):
        catalog = json.loads((ROOT / 'data/derived/catalog.json').read_text())
        native = {path.parent.name: json.loads(path.read_text())
                  for path in (ROOT / 'data/settings').glob('*/profile.json')}
        self.assertEqual({row['id'] for row in catalog['profiles']}, set(native))
        result = ordering.order_catalog(catalog)
        task_blocks = families(result['profiles'])
        self.assertEqual(len(task_blocks), len(set(task_blocks)))
        self.assertEqual(set(task_blocks), {profile['primary_domain'] for profile in native.values()})
        self.assertEqual(task_blocks[0], 'single_objective')
        self.assertEqual([row['order'] for row in result['profiles']],
                         list(range(1, len(native) + 1)))
        old_by_task = {task: [row['id'] for row in catalog['profiles'] if row['domain'] == task]
                       for task in task_blocks}
        for task in task_blocks:
            self.assertEqual([row['id'] for row in result['profiles'] if row['domain'] == task],
                             old_by_task[task])
        for row in result['profiles']:
            self.assertEqual(row['domain'], native[row['id']]['primary_domain'])
        self.assertEqual(ordering.order_catalog(result), result)


if __name__ == '__main__':
    unittest.main()
