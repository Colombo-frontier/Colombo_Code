"""Engineering regressions for exposing target native schemas, traceable adaptation, and rejection of remote resolution."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from oracle_atlas.atlas.tags import canonical_bytes
from oracle_atlas.atlas.target_schema import (
    SOURCE_FIELDS, TargetSchemaError, adapt_profile, read_target_schema,
    schema_manifest, validate_profile_target, validate_target_files,
)
from test_atlas import profile as synthetic_profile


FIXTURE = Path(__file__).parent / "fixtures" / "native_atlas" / "data"


class TargetSchemaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(FIXTURE / "schemas", self.root / "schemas")
        self.original = synthetic_profile("SYNTHETIC_TARGET_SCHEMA")
        self.original["schema_version"] = "6.1.0"
        self.original["provenance"] = {
            "synthetic": True, "source_schema_version": "6.1.0",
            "source_snapshot": "synthetic-target-schema-v1",
            "source_profile": "urn:structural-exploration:synthetic-target-schema",
            "source_json_sha256": hashlib.sha256(b"Synthetic schema-adaptation fixture only.").hexdigest(),
            "source_order": 42,
        }
        seed = self.root / "settings" / self.original["setting_id"]
        seed.mkdir(parents=True)
        self.original["provenance"]["source_order"] = 42
        (seed / "profile.json").write_text(json.dumps(self.original))
        self.incoming = deepcopy(self.original)
        self.incoming["setting_id"] = "NEW_PROFILE_FOR_SCHEMA_TEST"
        self.incoming["schema_version"] = "1.0.0"
        self.incoming["provenance"] = {"note": "This is unapproved test input, not a research result."}

    def test_all_six_target_errors_are_returned_together(self):
        errors = validate_profile_target(self.incoming, self.root)
        self.assertEqual(len(errors), 6, errors)
        self.assertEqual(sum(e["code"] == "target_schema_const" for e in errors), 1)
        self.assertEqual(sum(e["code"] == "target_schema_required" for e in errors), 5)
        for field in SOURCE_FIELDS:
            self.assertTrue(any(field in error["message"] for error in errors), field)
        json.dumps(errors)  # Directly archivable by tools, without validator/exception objects.

    def test_adaptation_is_traceable_and_does_not_change_science(self):
        before = deepcopy(self.incoming)
        expected_hash = hashlib.sha256(canonical_bytes(before)).hexdigest()
        result = adapt_profile(before, self.root, source_ref="urn:oracle-atlas:draft:job:draft@3", inventory_version="inventory-test-v1")
        profile = result["profile"]
        self.assertEqual(validate_profile_target(profile, self.root), [])
        self.assertEqual(profile["schema_version"], "6.1.0")
        provenance = profile["provenance"]
        self.assertEqual(provenance["source_schema_version"], "1.0.0")
        self.assertEqual(provenance["source_json_sha256"], expected_hash)
        self.assertEqual(provenance["source_profile"], "urn:oracle-atlas:draft:job:draft@3")
        self.assertEqual(provenance["source_snapshot"], "inventory-test-v1")
        self.assertEqual(provenance["source_order"], 43)
        self.assertEqual(len(result["changes"]), 6)
        for key in before.keys() - {"schema_version", "provenance"}:
            self.assertEqual(profile[key], before[key], key)
        self.assertEqual(before, self.incoming, "Adaptation must not mutate its input")
        self.assertEqual(len(list((self.root / "settings").glob("*/profile.json"))), 1)

    def test_second_prepare_keeps_frozen_hash_and_provenance(self):
        first = adapt_profile(self.incoming, self.root, source_ref="urn:oracle-atlas:draft:original@1", inventory_version="v1")
        second = adapt_profile(first["profile"], self.root, source_ref="urn:oracle-atlas:draft:later@5", inventory_version="v2")
        self.assertEqual(second["changes"], [])
        self.assertEqual(canonical_bytes(first["profile"]), canonical_bytes(second["profile"]))

    def test_existing_source_lineage_and_extensions_are_preserved(self):
        previous = deepcopy(self.original)
        previous["provenance"]["legacy_extension"] = {"source": "retained"}
        incoming = deepcopy(previous)
        incoming["schema_version"] = "1.0.0"
        incoming["provenance"] = {"source_profile": "attempted replacement", "new_extension": "allowed"}
        result = adapt_profile(incoming, self.root, previous=previous)
        for field in SOURCE_FIELDS:
            self.assertEqual(result["profile"]["provenance"][field], previous["provenance"][field])
        self.assertEqual(result["profile"]["provenance"]["legacy_extension"], {"source": "retained"})
        self.assertEqual(result["profile"]["provenance"]["new_extension"], "allowed")
        self.assertEqual(result["profile"]["common_specification"], previous["common_specification"])

    def test_missing_source_ref_uses_real_input_hash_not_fake_historical_file(self):
        result = adapt_profile(self.incoming, self.root)["profile"]["provenance"]
        code = hashlib.sha256(canonical_bytes(self.incoming)).hexdigest()
        self.assertEqual(result["source_profile"], "urn:oracle-atlas:input-profile:sha256:" + code)
        self.assertEqual(result["source_snapshot"], "oracle-atlas-draft-sha256:" + code)

    def test_manifest_is_bounded_and_exposes_target_requirements(self):
        result = schema_manifest(self.root, limit=1)
        self.assertEqual(len(result["items"]), 1)
        self.assertEqual(result["next_offset"], 1)
        self.assertEqual(result["profile_contract"]["schema_version"]["const"], "6.1.0")
        self.assertEqual(result["profile_contract"]["provenance_required"], list(SOURCE_FIELDS))
        self.assertNotIn("common_specification", result["items"][0])
        self.assertEqual(schema_manifest(self.root.parent / self.root.name, offset=999)["items"], [])

    def test_full_schema_is_paginated_and_pointer_addressable(self):
        page = read_target_schema(self.root, "profile", "/properties/provenance")
        self.assertEqual(page["data"]["required"], list(SOURCE_FIELDS))
        chunks, offset = [], 0
        while True:
            page = read_target_schema(self.root, "atlas-schema:profile.schema.json", offset=offset, limit=37)
            chunks.append(page["text"])
            if page["next_offset"] is None:
                break
            offset = page["next_offset"]
        self.assertEqual(json.loads("".join(chunks)), json.loads((self.root / "schemas/profile.schema.json").read_text()))

    def test_escaped_names_and_symlink_files_are_rejected(self):
        for name in ("../outside.json", "/tmp/outside.schema.json", "file:///tmp/outside.schema.json", "..\\outside.json"):
            with self.subTest(name=name), self.assertRaises(TargetSchemaError):
                read_target_schema(self.root, name)
        outside = self.root / "outside.schema.json"
        outside.write_text('{}')
        (self.root / "schemas/escape.schema.json").symlink_to(outside)
        with self.assertRaises(TargetSchemaError):
            read_target_schema(self.root, "escape.schema.json")
        errors = validate_profile_target(self.incoming, self.root)
        self.assertEqual(errors[0]["code"], "target_schema_resource")

    def test_manifest_refs_preserve_arbitrary_local_schema_filenames(self):
        folder = self.root / "schemas" / "defs"
        folder.mkdir()
        (folder / "common.json").write_text(json.dumps({"$defs": {"x": {"type": "string"}}}))
        manifest = schema_manifest(self.root)
        item = next(row for row in manifest["items"] if row["name"] == "defs/common.json")
        result = read_target_schema(self.root, item["schema_ref"], "/$defs/x")
        self.assertEqual(result["data"], {"type": "string"})

    def test_symlink_schema_directory_cannot_leave_data_root(self):
        with tempfile.TemporaryDirectory() as external, tempfile.TemporaryDirectory() as target:
            outside, root = Path(external), Path(target)
            (outside / "profile.schema.json").write_text('{}')
            (root / "schemas").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(TargetSchemaError):
                schema_manifest(root)
            with self.assertRaises(TargetSchemaError):
                adapt_profile(self.incoming, root)

    def test_no_target_schema_keeps_generic_profiles_unchanged(self):
        with tempfile.TemporaryDirectory() as target:
            profile = {"schema_version": "1.0.0", "setting_id": "S"}
            self.assertEqual(adapt_profile(profile, target), {"profile": profile, "changes": []})
            self.assertEqual(validate_profile_target(profile, target), [])
            self.assertFalse(schema_manifest(target)["target_schema_available"])

    def test_invalid_provenance_type_is_diagnosed_not_coerced(self):
        profile = deepcopy(self.incoming)
        profile["provenance"] = "not an object"
        adapted = adapt_profile(profile, self.root)["profile"]
        self.assertEqual(adapted["provenance"], "not an object")
        self.assertTrue(any(e["code"] == "target_schema_type" for e in validate_profile_target(adapted, self.root)))


class LocalSchemaReferencesTests(unittest.TestCase):
    def test_registered_http_namespace_resolves_only_to_local_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "schemas").mkdir()
            main = {"$id": "https://atlas.invalid/schemas/profile.schema.json", "type": "object", "properties": {"setting_id": {"$ref": "common.schema.json#/$defs/id"}}}
            (root / "schemas/profile.schema.json").write_text(json.dumps(main))
            (root / "schemas/common.schema.json").write_text(json.dumps({"$defs": {"id": {"type": "string", "pattern": "^MATRIX_"}}}))
            with patch("urllib.request.urlopen") as network:
                self.assertEqual(validate_profile_target({"setting_id": "MATRIX_OK"}, root), [])
                errors = validate_profile_target({"setting_id": "WRONG"}, root)
                self.assertEqual(errors[0]["code"], "target_schema_pattern")
                network.assert_not_called()

    def test_unknown_remote_ref_is_rejected_even_in_unvisited_field(self):
        for keyword in ("$ref", "$dynamicRef"):
            with self.subTest(keyword=keyword), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); (root / "schemas").mkdir()
                main = {"type": "object", "properties": {"unused": {keyword: "https://unregistered.invalid/remote.schema.json"}}}
                (root / "schemas/profile.schema.json").write_text(json.dumps(main))
                with patch("urllib.request.urlopen") as network:
                    errors = validate_profile_target({}, root)
                    self.assertEqual(errors[0]["code"], "target_schema_unresolved_ref")
                    network.assert_not_called()
                json.dumps(errors)

    def test_target_file_diagnostics_are_aggregated_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "schemas").mkdir()
            for name in ("profile", "identity"):
                (root / f"schemas/{name}.schema.json").write_text(json.dumps({"required": ["setting_id"]}))
            errors = validate_target_files({"profile.json": {}, "identity.json": {}}, root)
            self.assertEqual({e["file"] for e in errors}, {"profile.json", "identity.json"})


if __name__ == "__main__":
    unittest.main()
