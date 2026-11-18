"""Exact artifact proof reuse, with real Store permission and UTF-8 checks."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.brain.submission_validation import ContractError
from colombo.brain.record_formats import TEXT
from colombo.brain.proof_draft import resolve_proof_source
from colombo.shared.file_io import atomic_write
from colombo.brain.research_store import Store
from colombo.configuration import load_config


class ProofSourceTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.store = Store.create(Path(self.temp.name) / "run", "Prove the goal", [], load_config())
        self.sequence = 0

    def tearDown(self):
        self.temp.cleanup()

    def proof(self, text="Complete proof.\n", *, accepted=True, kind="result", data=None, artifacts=None):
        self.sequence += 1
        path = f"tasks/T0001/results/A{self.sequence:04d}/artifacts/manuscript.md"
        atomic_write(self.store.safe_path(path), text.encode("utf-8") if data is None else data)
        ref = self.store.write_record(kind, {"task_id": "T0001", "attempt_id": f"A{self.sequence:04d}",
            "accepted": accepted, "artifacts": artifacts if artifacts is not None else [{"path": path, "kind": "manuscript"}]})
        return {"body_source": {"result_ref": ref["id"], "path": path},
                "steps": [{"id": "S1", "evidence": [ref]}]}

    def test_reads_complete_original_text_without_mutation_or_write(self):
        text = "  # Complete Proof\r\n\r\n" + "∀ x, the conclusion holds.\n" * 2000 + "\r\n  "
        proof = self.proof(text)
        original = copy.deepcopy(proof)
        before = self.store.snapshot()
        with patch.object(self.store, "write_record", side_effect=AssertionError("read only")):
            resolved = resolve_proof_source(self.store, proof)
        self.assertEqual(resolved["body"], text)
        self.assertEqual(resolved["body_source"], proof["body_source"])
        self.assertEqual(proof, original)
        self.assertEqual(before, self.store.snapshot())
        resolved["steps"][0]["id"] = "changed"
        resolved["body_source"]["path"] = "changed"
        self.assertEqual(proof, original)

    def test_explicit_body_is_deep_copied_without_touching_store(self):
        proof = {"body": "  Original proof.\r\n", "steps": [{"id": "S1"}]}
        with patch.object(self.store, "read_record", side_effect=AssertionError("unnecessary read")):
            resolved = resolve_proof_source(self.store, proof)
        self.assertEqual(resolved, proof)
        resolved["steps"][0]["id"] = "S2"
        self.assertEqual(proof["steps"][0]["id"], "S1")

    def test_rejects_both_body_and_source_even_if_body_empty_or_null(self):
        proof = self.proof()
        for body in ("Other proof", "", None):
            with self.subTest(body=body), self.assertRaisesRegex(ContractError, "not both"):
                resolve_proof_source(self.store, {**proof, "body": body})

    def test_source_shape_and_path_are_explicit(self):
        proof = self.proof()
        for source in (None, [], {}, {**proof["body_source"], "extra": 1},
                       {"result_ref": proof["body_source"]["result_ref"], "path": " "}):
            with self.subTest(source=source), self.assertRaises(ContractError):
                resolve_proof_source(self.store, {**proof, "body_source": source})
        with self.assertRaises(ContractError):
            resolve_proof_source(self.store, [])

    def test_requires_result_kind_and_strict_local_acceptance(self):
        with self.assertRaisesRegex(ContractError, "Result reference"):
            resolve_proof_source(self.store, self.proof(kind="material"))
        for accepted in (False, None, 1, "true"):
            with self.subTest(accepted=accepted), self.assertRaisesRegex(ContractError, "locally accepted"):
                resolve_proof_source(self.store, self.proof(accepted=accepted))

    def test_unknown_and_wrong_revision_never_fall_back(self):
        proof = self.proof()
        ref = self.store.record_ref(proof["body_source"]["result_ref"])
        for bad_ref in ("missing-result", {**ref, "revision": ref["revision"] + 1}):
            with self.subTest(ref=bad_ref), self.assertRaises(ContractError):
                resolve_proof_source(self.store, {**proof, "body_source": {**proof["body_source"], "result_ref": bad_ref}})
        pinned = {**proof, "body_source": {**proof["body_source"], "result_ref": ref}}
        self.assertEqual(resolve_proof_source(self.store, pinned)["body"], "Complete proof.\n")

    def test_rejects_traversal_absolute_and_other_results_artifacts(self):
        proof, other = self.proof(), self.proof("Other proof")
        for path in ("../outside.md", str(self.store.root / "input/goal.md"),
                     other["body_source"]["path"], "input/goal.md"):
            with self.subTest(path=path), self.assertRaises(ContractError):
                resolve_proof_source(self.store, {**proof, "body_source": {**proof["body_source"], "path": path}})

    def test_rejects_missing_and_invalid_utf8_files(self):
        proof = self.proof()
        self.store.safe_path(proof["body_source"]["path"]).unlink()
        with self.assertRaisesRegex(ContractError, "Missing artifact"):
            resolve_proof_source(self.store, proof)
        with self.assertRaisesRegex(ContractError, "UTF-8"):
            resolve_proof_source(self.store, self.proof(data=b"\xff\xfe\x00"))

    def test_rejects_empty_whitespace_and_oversize_but_accepts_exact_limit(self):
        for text in ("", " \r\n\t", "x" * (TEXT["maxLength"] + 1)):
            with self.subTest(length=len(text)), self.assertRaises(ContractError):
                resolve_proof_source(self.store, self.proof(text))
        text = "№" * TEXT["maxLength"]
        self.assertEqual(resolve_proof_source(self.store, self.proof(text))["body"], text)

    def test_authorized_artifact_identity_must_be_unique(self):
        path = "input/goal.md"
        proof = self.proof(artifacts=[{"path": path}, {"path": path}])
        proof["body_source"]["path"] = path
        with self.assertRaisesRegex(ContractError, "unique artifact"):
            resolve_proof_source(self.store, proof)

    def test_only_selected_file_is_read_even_if_sibling_is_missing(self):
        proof = self.proof()
        payload = self.store.read_record(proof["body_source"]["result_ref"])
        ref = self.store.write_record("result", {**payload, "attempt_id": "A9999", "artifacts": [
            *payload["artifacts"], {"path": "missing-sibling.md"}]})
        proof["body_source"]["result_ref"] = ref["id"]
        self.assertEqual(resolve_proof_source(self.store, proof)["body"], "Complete proof.\n")


if __name__ == "__main__":
    unittest.main()
