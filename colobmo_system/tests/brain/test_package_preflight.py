"""Package preflight and audited formatting recovery never alter scientific inputs."""
from pathlib import Path
from contextlib import closing
import hashlib
import json
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.configuration import load_config
from colombo.brain.research_store import Store, StoreError
from colombo.brain.cell_package import build_package, preflight_package
from colombo.brain.submission_validation import ContractError, validate_semantics
from controller_fixtures import event_task
from brain_fixtures import SETTING


class PackagePreflightTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / "validation"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="package-preflight-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.store = Store.create(Path(self.temp.name) / "run", "Keep the fixed goal", [], load_config())
        self.store.set_meta(dispatch_count=11, round_no=2, phase="preparing")
        self.spec = event_task("Use only the selected evidence")
        self.destination = self.store.root / "tasks/T001/input/package"
        self.source_path = "input/evidence/proof.md"

    def material(self, raw, *, extra_files=None):
        if isinstance(raw, str):
            raw = raw.encode("utf-8")
        files = {self.source_path: raw, **(extra_files or {})}
        for relative, data in files.items():
            path = self.store.safe_path(relative)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        ref = self.store.write_record("material", {
            "title": "A fixed returned input",
            "artifacts": [{"path": relative} for relative in files],
        })
        self.spec["package"]["items"] = [{
            "ref": ref["id"], "importance": "required", "purpose": "Use the complete fixed argument",
            "limitations": "Formatting does not certify a Claim", "artifact_paths": [self.source_path],
        }]
        return ref

    def repair(self, formula, *, raw=None, reason="Reviewed literal equation; no content changes"):
        raw = raw if raw is not None else self.store.safe_path(self.source_path).read_bytes()
        body = raw.decode("utf-8-sig")
        start = body.index(formula)
        entry = {"source_sha256": hashlib.sha256(raw).hexdigest(), "reason": reason,
                 "literal_spans": [{"start": start, "end": start + len(formula), "expected": formula}]}
        self.write_repair(entry)
        return entry

    def write_repair(self, entry):
        path = self.store.safe_path("runtime/package_formatting.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"schema_version": 1, "artifacts": {self.source_path: entry}}),
                        encoding="utf-8")

    def snapshot(self):
        # SQLite read transactions may create transient WAL bookkeeping files;
        # compare the complete logical database plus every non-database artifact.
        with closing(sqlite3.connect(self.store.db_path)) as db:
            database = tuple(db.iterdump())
        files = {p.relative_to(self.store.root).as_posix(): p.read_bytes()
                 for p in self.store.root.rglob("*")
                 if p.is_file() and p.name not in {"state.sqlite", "state.sqlite-wal", "state.sqlite-shm"}}
        directories = {p.relative_to(self.store.root).as_posix()
                       for p in self.store.root.rglob("*") if p.is_dir()}
        return database, files, directories

    def test_failed_preflight_does_not_create_packages_or_spend_dispatches(self):
        self.material("The argument uses [a necessary Lemma](missing.md).")
        before = self.snapshot()
        with self.assertRaisesRegex(StoreError, "missing.md"):
            preflight_package(self.store, self.spec)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.store.get_meta("dispatch_count"), 11)
        self.assertFalse(self.destination.exists())

    def test_successful_preflight_checks_recursive_local_links_without_writing(self):
        self.material("Use [Lemma](lemma.md).", extra_files={
            "input/evidence/lemma.md": "Use [definitions](definitions.md).",
            "input/evidence/definitions.md": "Complete definitions.",
        })
        before = self.snapshot()
        preflight_package(self.store, self.spec)
        self.assertEqual(self.snapshot(), before)
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        included = {a["source_path"] for item in manifest["items"] for a in item["artifacts"]}
        self.assertEqual(included, {self.source_path, "input/evidence/lemma.md", "input/evidence/definitions.md"})

    def test_preflight_includes_typed_dependencies_of_selected_records(self):
        dependency = self.material("The referenced argument needs [a file](absent.md).")
        outer = self.store.write_record("material", {"title": "Explicit dependency",
            "dependency_refs": [dependency], "artifacts": []})
        self.spec["package"]["items"][0].update(ref=outer["id"], artifact_paths=[])
        before = self.snapshot()
        with self.assertRaisesRegex(StoreError, "absent.md"):
            preflight_package(self.store, self.spec)
        self.assertEqual(self.snapshot(), before)

    def test_bad_package_is_rejected_during_plan_submission_before_commit(self):
        self.material("Use [Lemma](missing.md).")
        payload = {"rationale": "Use an earlier result", "tasks": [self.spec],
                   "setting_specification": SETTING}
        before = self.snapshot()
        with self.assertRaisesRegex(ContractError, "missing.md"):
            validate_semantics("plan", payload, self.store, {})
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.store.reference_count("plan"), 0)
        self.assertEqual(self.store.get_meta("dispatch_count"), 11)

    def test_reviewed_formatting_changes_copy_only_and_records_both_hashes(self):
        formula = "=1+[2(d+1)/d^2](t^2+t)<=1."
        raw = ("\ufeff# Fixed Result\r\n\r\n" + formula + "\r\nUse [Lemma](lemma.md).\r\n").encode("utf-8")
        self.material(raw, extra_files={"input/evidence/lemma.md": "The full Lemma."})
        entry = self.repair(formula, raw=raw)
        before = self.snapshot()
        preflight_package(self.store, self.spec)
        self.assertEqual(self.snapshot(), before)
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        artifact = next(a for i in manifest["items"] for a in i["artifacts"]
                        if a["source_path"] == self.source_path)
        copied = (self.destination / artifact["package_path"]).read_bytes()
        self.assertEqual(copied.decode("utf-8"), raw.decode("utf-8-sig").replace(formula, "`" + formula + "`"))
        self.assertEqual(self.store.safe_path(self.source_path).read_bytes(), raw)
        audit = artifact["formatting_repair"]
        self.assertEqual(audit["source_sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(audit["output_sha256"], hashlib.sha256(copied).hexdigest())
        self.assertEqual(audit["reason"], entry["reason"])
        self.assertEqual([{key: span[key] for key in ("start", "end", "expected")}
                          for span in audit["literal_spans"]], entry["literal_spans"])
        self.assertEqual(audit["literal_spans"][0]["replacement"], "`" + formula + "`")
        paths = {a["source_path"] for i in manifest["items"] for a in i["artifacts"]}
        self.assertIn("input/evidence/lemma.md", paths)
        self.assertEqual(self.store.get_meta("dispatch_count"), 11)

    def test_stale_source_hash_cannot_apply_a_repair_to_changed_content(self):
        formula = "[coefficient](u,v)"
        self.material(formula)
        self.repair(formula)
        self.store.safe_path(self.source_path).write_text(formula + "\nNew content", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaisesRegex(StoreError, "(?i)hash|sha256"):
            preflight_package(self.store, self.spec)
        with self.assertRaisesRegex(StoreError, "(?i)hash|sha256"):
            build_package(self.store, "T001", self.spec, self.destination)
        self.assertEqual(self.snapshot(), before)

    def test_reviewed_formula_does_not_suppress_another_extensionless_dependency(self):
        formula = "=1+[2(d+1)/d^2](t^2+t)<=1."
        self.material(formula + "\n\nRequired [data](u,v).")
        self.repair(formula)
        with self.assertRaisesRegex(StoreError, "u,v"):
            preflight_package(self.store, self.spec)
        with self.assertRaisesRegex(StoreError, "u,v"):
            build_package(self.store, "T001", self.spec, self.destination)
        self.assertFalse(self.destination.exists())

    def test_explicit_math_does_not_hide_genuine_links_outside_math(self):
        self.material("$$\n[2(d+1)/d^2](t^2+t)\n$$\n\nRequired [Lemma](missing.md).")
        with self.assertRaisesRegex(StoreError, "missing.md"):
            preflight_package(self.store, self.spec)
        self.assertFalse(self.destination.exists())

    def test_published_package_replay_retains_its_original_formatting_audit(self):
        formula = "=1+[2(d+1)/d^2](t^2+t)<=1."
        self.material(formula)
        entry = self.repair(formula)
        first = build_package(self.store, "T001", self.spec, self.destination)
        package_bytes = {p.relative_to(self.destination).as_posix(): p.read_bytes()
                         for p in self.destination.rglob("*") if p.is_file()}
        # A later correction instruction cannot rewrite a published package or
        # retroactively change what its consumers received.
        self.write_repair({**entry, "reason": "A different later operator note"})
        self.assertEqual(build_package(self.store, "T001", self.spec, self.destination), first)
        self.assertEqual({p.relative_to(self.destination).as_posix(): p.read_bytes()
                          for p in self.destination.rglob("*") if p.is_file()}, package_bytes)


if __name__ == "__main__":
    unittest.main()
