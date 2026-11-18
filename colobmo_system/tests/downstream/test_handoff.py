"""File handoff uses real completed Brain exports, without opening their Store."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(PROJECT / "src"), str(PROJECT / "tests/brain")]

from colombo.brain.controller import OracleController
from colombo.brain.research_store import Store
from colombo.configuration import load_config
from colombo.downstream.handoff import digest, from_brain_run, ident, validate_package
from controller_fixtures import FakeCell
from test_oracle_workflow import Backend
from test_integration_structure import DraftBackend


def tree_bytes(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file()}


class BrainHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = PROJECT / "validation/decoupling"
        parent.mkdir(parents=True, exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(prefix="handoff-", dir=parent)
        cls.fixture_root = Path(cls.temporary.name)
        cls.completed = cls.make_run("completed", Backend())
        cls.partial = cls.make_run("partial", DraftBackend(partial=True))
        cls.export_bytes = {name: (cls.completed / name).read_bytes()
                            for name in ("research.json", "proof_draft.json", "output/final.md")}

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    @classmethod
    def make_run(cls, name, backend):
        config = load_config()
        config["limits"].update(max_rounds=1, max_dispatches_per_wave=1, max_parallel_cells=2)
        root = cls.fixture_root / name
        Store.create(root, "fixture", [], config)
        OracleController(PROJECT, root, backend=backend, adapter=FakeCell()).run()
        return root

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="case-", dir=self.fixture_root)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name, data in self.export_bytes.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def edit_export(self, name, edit):
        path = self.root / name
        value = json.loads(path.read_bytes())
        edit(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def proof_entry(exported):
        return exported["versions"][ident(exported["current_ref"])]

    def test_actual_completed_exports_match_bridge_and_stay_byte_identical(self):
        before = tree_bytes(self.completed)
        with patch("sqlite3.connect", side_effect=AssertionError("handoff must not open SQLite")):
            package = from_brain_run(self.completed)
        self.assertEqual(tree_bytes(self.completed), before)
        research = json.loads(self.export_bytes["research.json"])
        exported = json.loads(self.export_bytes["proof_draft.json"])
        entry = self.proof_entry(exported)
        self.assertEqual(package["proof"], entry["proof_draft"])
        self.assertEqual(package["proof_sha256"], digest(entry["proof_draft"]))
        self.assertEqual(package["setting"], research["goal"]["setting_specification"])
        self.assertEqual(package["goal"], research["goal"]["definition"])
        self.assertEqual(package["brain_check"]["proof_ref"], exported["current_ref"])
        self.assertEqual(package["brain_check"]["review_ref"], entry["review_ref"])
        self.assertEqual(package["brain_check"]["review"], entry["reviews"][ident(entry["review_ref"])] )
        self.assertEqual(package["required_claim_ids"], ["main", "P0"])
        self.assertEqual(package["source_exports"], {
            name: hashlib.sha256(data).hexdigest() for name, data in self.export_bytes.items()})

    def test_package_is_self_contained_with_complete_selected_drafts(self):
        draft = self.root / "selected-draft.md"
        text = "# Selected draft\n\nA complete supplementary Lemma, with parameter μ.\n"
        draft.write_text(text, encoding="utf-8")
        before = tree_bytes(self.root)
        package = from_brain_run(self.root, materials=[draft])
        self.assertEqual(tree_bytes(self.root), before)
        source = {item["name"]: item for item in package["source_materials"]}
        self.assertEqual(source["selected-draft.md"]["text"], text)
        self.assertEqual(source["final.md"]["text"], self.export_bytes["output/final.md"].decode("utf-8-sig"))
        for value in source.values():
            self.assertEqual(value["sha256"], hashlib.sha256(value["text"].encode()).hexdigest())
        # Downstream can reload only the JSON package after every original file
        # access becomes unavailable; it does not follow Brain artifact refs.
        frozen = json.loads(json.dumps(package))
        with patch.object(Path, "read_bytes", side_effect=AssertionError("unexpected source read")), \
                patch.object(Path, "read_text", side_effect=AssertionError("unexpected source read")):
            self.assertEqual(validate_package(frozen), package)

    def test_missing_review_ref_is_rejected(self):
        self.edit_export("proof_draft.json", lambda d: self.proof_entry(d).pop("review_ref"))
        with self.assertRaisesRegex(ValueError, "review"):
            from_brain_run(self.root)

    def test_missing_review_body_is_rejected(self):
        self.edit_export("proof_draft.json", lambda d: self.proof_entry(d).update(reviews={}))
        with self.assertRaisesRegex(ValueError, "review"):
            from_brain_run(self.root)

    def test_failed_review_is_rejected_even_with_completed_conclusion(self):
        def fail_review(exported):
            entry = self.proof_entry(exported)
            entry["reviews"][ident(entry["review_ref"])]["verdict"] = "revise"
        self.edit_export("proof_draft.json", fail_review)
        with self.assertRaisesRegex(ValueError, "review"):
            from_brain_run(self.root)

    def test_actual_partial_brain_conclusion_is_rejected(self):
        before = tree_bytes(self.partial)
        with self.assertRaisesRegex(ValueError, "not completed"):
            from_brain_run(self.partial)
        self.assertEqual(tree_bytes(self.partial), before)

    def test_failed_conclusion_is_rejected(self):
        def fail_conclusion(research):
            next(iter(research["conclusion"].values()))["status"] = "failed"
        self.edit_export("research.json", fail_conclusion)
        with self.assertRaisesRegex(ValueError, "not completed"):
            from_brain_run(self.root)

    def test_generation_mismatch_is_rejected(self):
        self.edit_export("research.json", lambda d: d.update(generation=d["generation"] + 1))
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            from_brain_run(self.root)

    def test_progress_proof_ref_mismatch_is_rejected(self):
        def stale_progress(research):
            progress = research["goal_progress"]
            progress["versions"][ident(progress["current_ref"])]["proof_ref"] = {
                "id": "another-proof", "revision": 1}
        self.edit_export("research.json", stale_progress)
        with self.assertRaisesRegex(ValueError, "review/progress"):
            from_brain_run(self.root)

    def test_final_review_must_check_adopted_proof_id(self):
        def stale_review(exported):
            entry = self.proof_entry(exported)
            entry["reviews"][ident(entry["review_ref"])]["checked_refs"] = ["another-proof"]
        self.edit_export("proof_draft.json", stale_review)
        with self.assertRaisesRegex(ValueError, "review/progress"):
            from_brain_run(self.root)

    def test_tampered_proof_hash_is_rejected(self):
        package = copy.deepcopy(from_brain_run(self.root))
        package["proof"]["body"] += "\nUnreviewed alteration."
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            validate_package(package)

    def test_tampered_source_material_hash_is_rejected(self):
        package = copy.deepcopy(from_brain_run(self.root))
        package["source_materials"][0]["text"] += "\nUnreviewed alteration."
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            validate_package(package)

    def test_exports_changed_during_handoff_are_rejected(self):
        original = Path.read_bytes
        reads = 0
        def changing_read(path):
            nonlocal reads
            data = original(path)
            if path == self.root / "research.json":
                reads += 1
                if reads == 2:
                    return data + b"\n"
            return data
        with patch.object(Path, "read_bytes", changing_read):
            with self.assertRaisesRegex(ValueError, "changed during handoff"):
                from_brain_run(self.root)


if __name__ == "__main__":
    unittest.main()
