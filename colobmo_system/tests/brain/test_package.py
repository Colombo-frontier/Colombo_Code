from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from colombo.configuration import load_config
from colombo.brain.research_store import Store, StoreError
from colombo.brain.cell_package import build_package
from colombo.shared.file_io import io_path, json_bytes


class PackageTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / "validation"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=parent)
        self.base = Path(self.temp.name)
        source = self.base / "evidence.txt"
        source.write_text("Full result, including its limitations.", encoding="utf-8")
        self.store = Store.create(self.base / "run", "goal", [], load_config(), [source])
        self.ref = self.store.get_meta("material_refs")[0]
        self.spec = {"package":{"background":"Relevant goal", "selection_reason":"Needed as input",
            "items":[{"ref":self.ref["id"], "importance":"required", "purpose":"Check applicability",
                      "limitations":"Not an independently certified theorem"}]}}
        self.destination = self.store.root / "tasks/T001/input/package"

    def tearDown(self):
        self.temp.cleanup()

    def test_package_includes_record_and_full_material(self):
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        artifact = manifest["items"][0]["artifacts"][0]
        self.assertEqual((self.destination / artifact["package_path"]).read_text(), "Full result, including its limitations.")
        self.assertTrue((self.destination / manifest["items"][0]["record_path"]).is_file())
        self.assertIn("Check applicability", (self.destination / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(build_package(self.store,"T001",self.spec,self.destination),manifest)

    def test_missing_reference_rejects_before_publishing(self):
        self.spec["package"]["items"][0]["ref"] = "result-missing"
        with self.assertRaises(StoreError):
            build_package(self.store,"T001",self.spec,self.destination)
        self.assertFalse(self.destination.exists())

    def test_changed_selection_cannot_replace_frozen_package(self):
        build_package(self.store,"T001",self.spec,self.destination)
        self.spec["package"]["items"][0]["purpose"] = "Different purpose"
        with self.assertRaises(StoreError):
            build_package(self.store,"T001",self.spec,self.destination)

    def test_local_dependency_closure_is_copied_without_selecting_all_history(self):
        theorem = self.store.write_record("material", {"title": "Dependent theorem",
            "dependency_refs": [self.ref], "artifacts": []})
        unrelated = self.store.write_record("material", {"title": "Unrelated history", "artifacts": []})
        self.spec["package"]["items"][0]["ref"] = theorem["id"]
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        refs = {item["source_ref"]["id"] for item in manifest["items"]}
        self.assertEqual(refs, {theorem["id"], self.ref["id"]})
        self.assertNotIn(unrelated["id"], refs)

    def test_relative_local_links_remain_self_contained(self):
        folder = self.store.root / "input/local"
        folder.mkdir()
        (folder / "proof.md").write_text("Use [definitions](definitions.md).", encoding="utf-8")
        (folder / "definitions.md").write_text("The complete definitions.", encoding="utf-8")
        ref = self.store.write_record("material", {"artifacts": [
            {"path": "input/local/proof.md"}, {"path": "input/local/definitions.md"}]})
        self.spec["package"]["items"][0].update(ref=ref["id"], artifact_paths=["input/local/proof.md"])
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        copies = {item["source_path"]: item["package_path"] for item in manifest["items"][0]["artifacts"]}
        proof = self.destination / copies["input/local/proof.md"]
        self.assertEqual((proof.parent / "definitions.md").read_text(), "The complete definitions.")

    def markdown_material(self, body, dependency="lemma proof.md"):
        folder = self.store.root / "input/markdown"
        folder.mkdir(exist_ok=True)
        (folder / "proof.md").write_text(body, encoding="utf-8")
        (folder / dependency).write_text("Complete local Lemma.", encoding="utf-8")
        ref = self.store.write_record("material", {"artifacts": [
            {"path": "input/markdown/proof.md"}, {"path": "input/markdown/" + dependency}]})
        self.spec["package"]["items"][0].update(ref=ref["id"], artifact_paths=["input/markdown/proof.md"])

    def test_windows_file_uri_and_unc_links_cannot_escape_package(self):
        targets = ["D:/other-cell/live/lemma.md", "file:///D:/other-cell/live/lemma.md",
                   r"\\server\share\lemma.md", "file://server/share/lemma.md",
                   "D%3A/other-cell/live/lemma.md", "//server/share/lemma.md"]
        for target in targets:
            with self.subTest(target=target):
                self.markdown_material(f"Required [Lemma](<{target}>).")
                with self.assertRaisesRegex(StoreError, "local dependency"):
                    build_package(self.store, "T001", self.spec, self.destination)
                self.assertFalse(self.destination.exists())

    def test_commonmark_reference_definitions_and_encoded_or_angle_spaces(self):
        self.markdown_material("Use [Lemma][proof]. Also [inline](<lemma proof.md>) and "
                               "[encoded](lemma%20proof.md).\n\n[proof]: <lemma proof.md> \"Full Proof\"\n")
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        copies = {a["source_path"]: a["package_path"] for a in manifest["items"][0]["artifacts"]}
        proof = self.destination / copies["input/markdown/proof.md"]
        self.assertEqual((proof.parent / "lemma proof.md").read_text(), "Complete local Lemma.")
        self.assertIn("[proof]: <lemma proof.md>", proof.read_text())

    def test_missing_reference_style_dependency_is_rejected_before_publication(self):
        self.markdown_material("Use [Lemma][p].\n\n[p]: missing.md\n")
        with self.assertRaisesRegex(StoreError, "missing local dependency"):
            build_package(self.store, "T001", self.spec, self.destination)
        self.assertFalse(self.destination.exists())

    def test_authorized_absolute_file_links_are_relocated_in_package_copy_only(self):
        local = self.store.root / "input/markdown/lemma proof.md"
        self.markdown_material(f"Use [Lemma](<{local.as_uri()}>).")
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        proof = next(a for a in manifest["items"][0]["artifacts"] if a["source_path"].endswith("/proof.md"))
        rewritten = (self.destination / proof["package_path"]).read_text()
        self.assertEqual(rewritten, "Use [Lemma](<lemma%20proof.md>).")
        self.assertIn("file:", (self.store.root / "input/markdown/proof.md").read_text())

    def test_code_examples_do_not_create_file_dependencies_but_html_links_do(self):
        self.markdown_material("`[not a link](D:/live/file.md)`\n\n```md\n[x](file:///bad.md)\n```\n")
        build_package(self.store, "T001", self.spec, self.destination)
        from colombo.brain.cell_package import resolve_markdown
        with self.assertRaisesRegex(StoreError, "local dependency"):
            resolve_markdown(self.store.root, "input/markdown/proof.md",
                '<a href="file:///D:/other-cell/live/file.md">Lemma</a>', {})

    def test_dependency_error_locates_link_not_earlier_plain_text(self):
        from colombo.brain.cell_package import resolve_markdown, PackageDependencyError
        body = 'The pair (u,v) appears first.\r\n\r\nHere is [D](u,v).\r\n'
        with self.assertRaises(PackageDependencyError) as caught:
            resolve_markdown(self.store.root, 'source.md', body, {})
        self.assertEqual(caught.exception.details['line'], 3)
        self.assertEqual(caught.exception.details['source'], 'source.md')

    def test_fixed_setting_and_selected_bracket_are_automatic_required_inputs(self):
        self.store.set_meta(config={"workflow": {"version": 3}})
        setting = {"oracle": "fixed first-order Oracle"}
        (self.store.root / "input/setting.json").write_text(json.dumps(setting), encoding="utf-8")
        progress = {"overall": "Two regimes", "bracket": {"bounds": [
            {"id": "b1", "expression": "n"}, {"id": "b2", "expression": "n^2"}], "regimes": [
            {"id": "r1", "lower_bound_ids": ["b1"], "upper_bound_ids": ["b1"]},
            {"id": "r2", "lower_bound_ids": ["b2"], "upper_bound_ids": ["b2"]}]}}
        ref = self.store.write_record("goal_progress", {"progress": progress})
        self.store.set_meta(progress_ref=ref)
        self.spec["package"].update(items=[], regime_ids=["r1"])
        build_package(self.store, "T001", self.spec, self.destination)
        self.assertEqual(json.loads((self.destination / "setting.json").read_text()), setting)
        bracket = json.loads((self.destination / "bracket_snapshot.json").read_text())["bracket"]
        self.assertEqual([r["id"] for r in bracket["regimes"]], ["r1"])
        self.assertEqual([b["id"] for b in bracket["bounds"]], ["b1"])
        from colombo.brain.cell_dispatch import _required_review_files
        self.assertIn("inputs/package/setting.json", _required_review_files(self.destination))
        self.assertIn("inputs/package/bracket_snapshot.json", _required_review_files(self.destination))

    def test_missing_local_link_is_rejected_and_mutated_package_is_detected(self):
        source = self.store.root / "input/missing.md"
        source.write_text("[Missing premise](missing-premise.md)", encoding="utf-8")
        ref = self.store.write_record("material", {"artifacts": [{"path": "input/missing.md"}]})
        self.spec["package"]["items"][0]["ref"] = ref["id"]
        with self.assertRaisesRegex(StoreError, "missing local dependency"):
            build_package(self.store, "T001", self.spec, self.destination)

        self.spec["package"]["items"][0]["ref"] = self.ref["id"]
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        (self.destination / manifest["files"][0]["path"]).write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(StoreError, "content differs"):
            build_package(self.store, "T001", self.spec, self.destination)

    def test_bracket_proof_dependencies_are_copied_without_full_attempt_history(self):
        self.store.set_meta(config={"workflow": {"version": 3}})
        prefix = "tasks/T-source/results/A0001/artifacts/"
        artifacts = []
        for name, content in (("manuscript.md", "Complete scoped proof"), ("notes/private.md", "Earlier dead end")):
            path = self.store.safe_path(prefix + name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            artifacts.append({"path": prefix + name})
        result = self.store.write_record("result", {"artifacts": artifacts, "accepted": True})
        progress = {"bracket": {"bounds": [{"id": "b1", "result_ref": result["id"]}],
            "regimes": [{"id": "r1", "lower_bound_ids": ["b1"], "upper_bound_ids": ["b1"]}]}}
        ref = self.store.write_record("goal_progress", {"progress": progress})
        self.store.set_meta(progress_ref=ref)
        self.spec["package"].update(items=[], regime_ids=["r1"])
        manifest = build_package(self.store, "T001", self.spec, self.destination)
        paths = [a["source_path"] for item in manifest["items"] for a in item["artifacts"]]
        self.assertIn(prefix + "manuscript.md", paths)
        self.assertNotIn(prefix + "notes/private.md", paths)



    def test_empty_package_requires_reason_but_is_allowed(self):
        self.spec["package"]["items"] = []
        self.spec["package"]["selection_reason"] = "Self-contained task, no prior results"
        manifest = build_package(self.store,"T001",self.spec,self.destination)
        self.assertEqual(manifest["items"],[])
        self.assertEqual(len(manifest["files"]),1)


    def test_outside_destination_and_duplicate_refs_rejected(self):
        with self.assertRaises(StoreError):
            build_package(self.store,"T001",self.spec,self.base / "outside")
        self.spec["package"]["items"] *= 2
        with self.assertRaises(StoreError):
            build_package(self.store,"T001",self.spec,self.destination)

    def test_long_run_package_copies_and_replays_above_300_characters(self):
        parent = self.base / ("r" * 95)
        root = parent / ("n" * 95) / "long-run"
        try:
            source = self.base / "evidence.txt"
            store = Store.create(root,"Long goal",[],load_config(),[source])
            ref = store.get_meta("material_refs")[0]
            spec = {"package":{**self.spec["package"],"items":[
                {**self.spec["package"]["items"][0],"ref":ref["id"]}]}}
            destination = store.root / "tasks/T0001/input/package"
            manifest = build_package(store,"T0001",spec,destination)
            artifact_path = manifest["items"][0]["artifacts"][0]["package_path"]
            self.assertGreaterEqual(len(str(destination / artifact_path)),300)
            self.assertLess(len(artifact_path),100)
            self.assertNotIn(ref["id"],artifact_path)
            self.assertEqual((destination / artifact_path).read_text(encoding="utf-8"),source.read_text(encoding="utf-8"))
            self.assertEqual(manifest,build_package(store,"T0001",spec,destination))
        finally:
            if parent.exists():
                shutil.rmtree(io_path(parent))



if __name__ == "__main__":
    unittest.main()
