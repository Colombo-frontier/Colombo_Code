"""Real AgentService formatting feedback, without model or external calls."""
from pathlib import Path
import asyncio
import hashlib
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.configuration import load_config
from colombo.brain.research_store import Store, StoreError
from colombo.brain.cell_package import build_package, register_literal_formatting
from colombo.brain.mcp_server import AgentService, create_server
from colombo.brain.submission_validation import ContractError
from controller_fixtures import event_task
from brain_fixtures import SETTING, write_review_package


class PackageFormattingServiceTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / "validation"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="package-format-service-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.store = Store.create(Path(self.temp.name) / "run", "A fixed Goal", [], load_config())
        self.formula = "=1+[2(d+1)/d^2](t^2+t)<=1."
        self.second = "D^2 f(x)[u](u,v)=0"
        self.path = "input/source.md"
        self.raw = ("# Fixed input\n\n" + self.formula + "\n" + self.second + "\n").encode("utf-8")
        self.store.safe_path(self.path).write_bytes(self.raw)
        self.ref = self.store.write_record("material", {"title": "Source",
            "artifacts": [{"path": self.path, "size": len(self.raw)}]})
        self.sidecar = self.store.safe_path("runtime/package_formatting.json")

    def service(self, role="brain", stage="plan", call_id="FORMAT-PLAN"):
        work = self.store.root / "brain/calls" / call_id
        work.mkdir(parents=True)
        context = {"role": role, "stage": stage, "call_id": call_id, "dispatch_remaining": 6}
        if role == "verifier":
            context["review_package_ref"] = write_review_package(self.store, {
                "allowed_refs": [self.ref["id"]], "required_checked_refs": [self.ref["id"]]})
        (work / "context.json").write_text(json.dumps(context), encoding="utf-8")
        (work / "call.json").write_text(json.dumps(context), encoding="utf-8")
        self.store.set_meta(pending_call=context)
        return AgentService(self.store.root, role, stage, call_id)

    def register(self, literal=None, **kwargs):
        args = {"store": self.store, "ref": self.ref, "path": self.path,
                "literal_text": self.formula if literal is None else literal,
                "reason": "Inspected equation is literal mathematics", "actor": {"operator": "unit-test"}}
        args.update(kwargs)
        return register_literal_formatting(**args)

    def test_exact_literal_registration_preserves_source_and_records_provenance(self):
        reply = self.register()
        self.assertTrue(reply["original_unchanged"])
        self.assertEqual(reply["applies_to"], "unpublished_package_copies")
        self.assertEqual(self.store.safe_path(self.path).read_bytes(), self.raw)
        entries = json.loads(self.sidecar.read_text(encoding="utf-8"))["artifacts"]
        saved = entries[self.path]
        self.assertEqual(saved["source_sha256"], hashlib.sha256(self.raw).hexdigest())
        self.assertEqual(saved["source_ref"], self.ref)
        self.assertEqual(saved["actor"], {"operator": "unit-test"})
        events = [e for e in self.store.events() if e["name"] == "package_literal_formatting"]
        self.assertEqual(len(events), 1)

    def test_invalid_reference_path_and_nonunique_expression_are_rejected(self):
        cases = [
            {"ref": self.store.get_meta("goal_ref")},
            {"ref": "material-does-not-exist"},
            {"path": "../other-run/proof.md"},
            {"path": "input/not-authorized.md"},
            {"literal_text": "unmatched literal"},
            {"literal_text": "\n"},
            {"literal_text": self.formula, "reason": ""},
        ]
        for changes in cases:
            with self.subTest(changes=changes):
                with self.assertRaises((StoreError, ValueError)):
                    self.register(**changes)
                self.assertFalse(self.sidecar.exists())
                self.assertEqual(self.store.safe_path(self.path).read_bytes(), self.raw)

    def test_hash_change_rejects_registration_without_overwriting_existing_audit(self):
        self.register()
        original_sidecar = self.sidecar.read_bytes()
        self.store.safe_path(self.path).write_bytes(self.raw + b"More text\n")
        with self.assertRaisesRegex(StoreError, "(?i)hash|sha256"):
            self.register(self.second)
        self.assertEqual(self.sidecar.read_bytes(), original_sidecar)

    def test_two_distinct_literals_merge_without_duplicate_spans(self):
        second_reason = "The second expression is a multilinear evaluation"
        first_reason = "The first expression is an ellipsoid inequality"
        self.register(self.second, reason=second_reason)
        self.register(self.formula, reason=first_reason)
        self.register(self.formula, reason=first_reason)
        entry = json.loads(self.sidecar.read_text(encoding="utf-8"))["artifacts"][self.path]
        self.assertEqual([span["expected"] for span in entry["literal_spans"]], [self.formula, self.second])
        self.assertEqual([span["reason"] for span in entry["literal_spans"]], [first_reason, second_reason])
        self.assertEqual(self.store.safe_path(self.path).read_bytes(), self.raw)

    def test_only_active_brain_plan_call_can_register_formatting(self):
        for role, stage in (("brain", "integrate"), ("brain", "process_results"),
                            ("verifier", "verify-progress")):
            with self.subTest(role=role, stage=stage):
                service = self.service(role, stage, role + "-" + stage)
                with self.assertRaisesRegex(ValueError, "only to Brain during plan"):
                    service.format_package_literal(self.ref["id"], self.path, self.formula, "Literal equation")
                self.assertFalse(self.sidecar.exists())
        service = self.service(call_id="STALE-PLAN")
        self.store.set_meta(pending_call=None)
        with self.assertRaisesRegex(ValueError, "no longer active"):
            service.format_package_literal(self.ref["id"], self.path, self.formula, "Literal equation")
        self.assertFalse(self.sidecar.exists())

    def test_mcp_inventory_exposes_formatting_only_during_brain_plan(self):
        for role, stage, expected in (("brain", "plan", True), ("brain", "integrate", False),
                                      ("verifier", "verify-progress", False)):
            with self.subTest(role=role, stage=stage):
                call_id = "INVENTORY-" + role + "-" + stage
                self.service(role, stage, call_id)
                server = create_server(self.store.root, role, stage, call_id)
                names = {tool.name for tool in asyncio.run(server.list_tools())}
                self.assertEqual("format_package_literal" in names, expected)

    def test_rejected_preflight_can_be_corrected_and_resubmitted_in_same_call(self):
        service = self.service()
        self.store.set_meta(dispatch_count=6)
        task = event_task("Use the returned material")
        task["package"]["items"] = [{"ref": self.ref["id"], "importance": "required",
            "purpose": "Use the fixed argument", "limitations": "No extra mathematical certification"}]
        payload = {"rationale": "Continue the same target", "tasks": [task], "setting_specification": SETTING}
        with self.assertRaisesRegex(ContractError, "t\\^2\\+t"):
            service.submit("plan", payload)
        self.assertEqual(self.store.reference_count("plan"), 0)
        self.assertFalse((service.work / "submission.json").exists())
        self.assertEqual(self.store.get_meta("dispatch_count"), 6)
        for literal in (self.formula, self.second):
            service.format_package_literal(self.ref["id"], self.path, literal, "Inspected literal equation")
        receipt = service.submit("plan", payload)
        self.assertEqual(receipt["status"], "submitted")
        self.assertEqual(self.store.reference_count("plan"), 1)
        self.assertTrue((service.work / "submission.json").is_file())
        self.assertEqual(self.store.get_meta("dispatch_count"), 6)
        self.assertEqual(self.store.safe_path(self.path).read_bytes(), self.raw)
        jobs = self.store.plan_jobs(receipt["ref"])
        self.assertEqual(len(jobs), 1)
        destination = self.store.root / "tasks" / jobs[0]["task_id"] / "input/package"
        manifest = build_package(self.store, jobs[0]["task_id"], jobs[0]["spec"], destination)
        copy = manifest["items"][0]["artifacts"][0]
        self.assertEqual((destination / copy["package_path"]).read_text(encoding="utf-8"),
                         self.raw.decode("utf-8").replace(self.formula, "`" + self.formula + "`")
                         .replace(self.second, "`" + self.second + "`"))


if __name__ == "__main__":
    unittest.main()
