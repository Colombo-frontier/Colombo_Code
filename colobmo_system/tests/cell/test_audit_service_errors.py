"""Preparation failures are recorded without changing mathematical certification."""
from __future__ import annotations

import copy
import json
import os
import tempfile
import unittest
from unittest.mock import Mock
from unittest.mock import patch

import colombo.cell.verifier.local_audit as auditing
from colombo.shared.experiment_artifacts import manifest_for
from colombo.cell.record_store import Store
from colombo.cell.record_store import StoreError
from colombo.shared.file_io import Path
from colombo.cell.settings import get_settings


ROOT = Path(__file__).resolve().parents[2]
PASS = {"verdict": "pass", "summary": "The supplied equality is reflexive.",
        "findings": [], "properties": []}


def ref(record):
    return {key: record[key] for key in ("kind", "id", "revision")}


class AuditServiceErrorTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        self.addCleanup(environment.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        directory = tempfile.TemporaryDirectory(prefix=".audit-errors-", dir=str(ROOT))
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "problem.md").write_text("Prove x=x for all real x.", encoding="utf-8")
        self.store = Store(self.root / "memory")

    def candidate(self):
        return self.store.archive("arguments", {"statement": "For every real x, x=x.",
                                                  "proof": "Equality is reflexive.", "status": "candidate"})

    def check_error(self, original, result, stage):
        review = result["review"]
        payload = review["payload"]
        self.assertEqual(payload["verdict"], "service_error")
        self.assertEqual(payload["error_stage"], stage)
        self.assertTrue(payload["error_type"])
        self.assertIn(stage, payload["findings"][0])
        self.assertEqual(payload["properties"], [])
        self.assertEqual(payload["target"], ref(original))
        self.assertEqual(self.store.get("reviews", review["id"], review["revision"])["payload"], payload)
        current = self.store.get(original["kind"], original["id"])
        self.assertEqual(current["revision"], original["revision"])
        self.assertEqual(current["payload"], original["payload"])
        self.assertEqual(result["record"]["revision"], original["revision"])

    def test_preparation_failures_are_saved_with_the_failing_stage(self):
        original_mkdir = Path.mkdir
        original_read = Path.read_text
        original_write = Path.write_text

        def denied_workspace(path, *args, **kwargs):
            if path.parent.name == "audits":
                raise FileNotFoundError("Cannot create deep audit workspace")
            return original_mkdir(path, *args, **kwargs)

        def denied_problem(path, *args, **kwargs):
            if path.name == "problem.md":
                raise PermissionError("Cannot read the problem")
            return original_read(path, *args, **kwargs)

        def denied_write(name):
            def write(path, *args, **kwargs):
                if path.name == name and path.parent.parent.name == "audits":
                    raise OSError("Cannot save audit input")
                return original_write(path, *args, **kwargs)
            return write

        failures = [
            ("collect_support", patch.object(Store, "audit_context", side_effect=OSError("Unreadable support"))),
            ("collect_evidence", patch.object(Store, "evidence_bundle", side_effect=StoreError("Missing experiment file"))),
            ("read_problem", patch.object(Path, "read_text", new=denied_problem)),
            ("create_workspace", patch.object(Path, "mkdir", new=denied_workspace)),
            ("copy_evidence", patch.object(auditing, "copy_artifacts", side_effect=OSError("Cannot copy evidence"))),
            ("write_instructions", patch.object(Path, "write_text", new=denied_write("AGENTS.md"))),
            ("write_input", patch.object(Path, "write_text", new=denied_write("input.json"))),
            ("load_configuration", patch.object(auditing, "get_settings", side_effect=ValueError("Invalid saved config"))),
        ]
        for stage, failure in failures:
            with self.subTest(stage=stage):
                candidate = self.candidate()
                reviewer = Mock(return_value=copy.deepcopy(PASS))
                with failure:
                    result = auditing.audit(self.root, "arguments", candidate["id"], candidate["revision"],
                                            reviewer=reviewer)
                reviewer.assert_not_called()
                self.check_error(candidate, result, stage)

    def test_invalid_caller_requests_remain_errors_without_creating_reviews(self):
        candidate = self.candidate()
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "zero", "statement": "x is zero", "status": "pending"}]})
        claim = self.store.archive("claims", {"statement": "x=x"})
        requests = [
            ("arguments", candidate["id"], 1, ["unknown"]),
            ("examples", example["id"], 1, "zero"),
            ("examples", example["id"], 1, {"zero": True}),
            ("examples", example["id"], 1, [None]),
            ("examples", example["id"], 1, ["zero", "zero"]),
            ("examples", example["id"], 1, []),
            ("claims", claim["id"], 1, None),
        ]
        reviewer = Mock(return_value=PASS)
        for kind, identifier, revision, properties in requests:
            with self.subTest(kind=kind, properties=properties), self.assertRaises(ValueError):
                auditing.audit(self.root, kind, identifier, revision, properties, reviewer=reviewer)
        with self.assertRaises(KeyError):
            auditing.audit(self.root, "arguments", "missing", 1, reviewer=reviewer)
        reviewer.assert_not_called()
        self.assertEqual(self.store.retrieve(kinds=["reviews"])["count"], 0)
        self.assertFalse((self.root / "audits").exists())

    def test_startup_failure_is_not_a_mathematical_failure(self):
        candidate = self.candidate()
        with patch.object(auditing, "run_agent", side_effect=FileNotFoundError("Model process did not start")):
            result = auditing.audit(self.root, "arguments", candidate["id"], 1)
        self.check_error(candidate, result, "run_reviewer")

    def test_invalid_model_output_is_saved_as_response_failure(self):
        for output in ("{invalid JSON", {"returncode": 17, "text": ""},
                       {**PASS, "verdict": "pass", "findings": ["Contradiction"]}):
            with self.subTest(output=output):
                candidate = self.candidate()
                result = auditing.audit(self.root, "arguments", candidate["id"], 1,
                                        reviewer=lambda *_: copy.deepcopy(output))
                self.check_error(candidate, result, "validate_response")

    def test_failed_post_review_evidence_check_does_not_promote_argument(self):
        candidate = self.candidate()
        with patch.object(auditing, "read_artifact_groups", side_effect=OSError("Evidence became unreadable")):
            result = auditing.audit(self.root, "arguments", candidate["id"], 1,
                                    reviewer=lambda *_: copy.deepcopy(PASS))
        self.check_error(candidate, result, "recheck_evidence")

    def test_service_failure_does_not_revoke_or_challenge_existing_certificate(self):
        candidate = self.candidate()
        proved = auditing.audit(self.root, "arguments", candidate["id"], 1,
                                reviewer=lambda *_: copy.deepcopy(PASS))["record"]
        with patch.object(auditing, "copy_artifacts", side_effect=OSError("Copy failed")), \
                patch("colombo.cell.verifier.challenge.challenge_from_audit") as challenge:
            result = auditing.audit(self.root, "arguments", proved["id"], proved["revision"])
        challenge.assert_not_called()
        self.check_error(proved, result, "copy_evidence")
        self.assertEqual(result["record"]["current_trust"]["state"], "supported")

    def test_service_failure_preserves_checked_example_properties(self):
        example = self.store.archive("examples", {"construction": "x=0", "properties": [
            {"id": "zero", "statement": "x is zero", "status": "pending"}]})
        passed = {**PASS, "properties": [{"id": "zero", "verdict": "pass", "reason": "By construction."}]}
        checked = auditing.audit(self.root, "examples", example["id"], 1,
                                 reviewer=lambda *_: copy.deepcopy(passed))["record"]
        with patch.object(auditing, "copy_artifacts", side_effect=OSError("Copy failed")):
            result = auditing.audit(self.root, "examples", checked["id"], checked["revision"])
        self.check_error(checked, result, "copy_evidence")
        self.assertEqual(result["record"]["payload"]["properties"][0]["status"], "checked")

    def test_math_pass_fail_and_uncertain_remain_distinct(self):
        for verdict in ("pass", "fail", "uncertain"):
            with self.subTest(verdict=verdict):
                candidate = self.candidate()
                output = {**PASS, "verdict": verdict,
                          "findings": [] if verdict == "pass" else ["The supplied inference needs correction."]}
                result = auditing.audit(self.root, "arguments", candidate["id"], 1,
                                        reviewer=lambda *_: copy.deepcopy(output))
                self.assertEqual(result["review"]["payload"]["verdict"], verdict)
                self.assertNotIn("error_stage", result["review"]["payload"])
                expected = "proved" if verdict == "pass" else "candidate"
                self.assertEqual(result["record"]["payload"]["status"], expected)

    def test_missing_declared_experiment_file_is_recorded_before_reviewer_starts(self):
        target = self.store.archive("claims", {"statement": "The computed value is zero."})
        name = "experiments/exp-audit/code.py"
        data = b"assert 0 == 0\n"
        path = self.root / name
        path.parent.mkdir(parents=True)
        path.write_bytes(data)
        settings = get_settings(self.root)
        experiment = self.store.write_experiment_result("exp-audit", {
            "question": "Check the value zero.", "target_ref": ref(target), "parameters": {},
            "code_file": "experiments/e1/code.py", "input_files": [],
            "execution": {"status": "completed", "backend": "test_fixture", "model": "fake",
                          "started_at": 100, "deadline_at": 200,
                          "artifact_limits": {key: settings["experiment"][key] for key in
                                              ("artifact_max_bytes", "max_total_artifact_bytes", "max_files")}},
            "artifacts": manifest_for({name: data})})
        candidate = self.store.archive("arguments", {"proof": "Use the declared exact computation.",
                                                       "status": "candidate", "dependencies": [ref(experiment)]})
        path.unlink()
        reviewer = Mock(return_value=PASS)
        result = auditing.audit(self.root, "arguments", candidate["id"], 1, reviewer=reviewer)
        reviewer.assert_not_called()
        self.check_error(candidate, result, "collect_evidence")
        self.assertIn("missing or size changed", result["review"]["payload"]["findings"][0])


if __name__ == "__main__":
    unittest.main()
