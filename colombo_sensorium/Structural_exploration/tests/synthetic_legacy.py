"""Generate legacy-format compatibility records from synthetic test premises.

No production setting, paper, source archive or private acceptance snapshot is
included. Records are generated only inside the caller's temporary test Atlas.
"""
import hashlib
import json
from pathlib import Path

from oracle_atlas.atlas import Atlas
from oracle_atlas.atlas.store import json_bytes
from oracle_atlas.core.store import digest


SETTING_IDS = ("SYNTHETIC_LEGACY_VALUE", "SYNTHETIC_LEGACY_MATRIX")


def create_synthetic_legacy_atlas(directory):
    # Import only after test_atlas has defined its explicit synthetic helpers.
    from test_atlas import approve, facts, profile

    atlas = Atlas(directory)
    for sid in SETTING_IDS:
        p = profile(sid)
        p["schema_version"] = "6.1.0"
        p["title"] = "[SYNTHETIC LEGACY] Compatibility record " + sid
        p["aliases"] = [{"legacy_id": sid + "_legacy", "view_id": "randomized"}]
        p["provenance"] = {"synthetic": True, "purpose": "Generated software compatibility fixture; no mathematical adoption."}
        prepared = atlas.prepare(p, facts(p))
        atlas.commit(prepared, approve(prepared), "synthetic-legacy-seed:" + sid)

        # Deliberately emulate a historical native record predating joint v2.
        # Keep the five-file profile-hash bindings coherent for read tests.
        folder = atlas.settings / sid
        legacy = atlas.read(sid)
        legacy.pop("joint_analysis")
        raw = json_bytes(legacy)
        pretty_hash, canonical_hash = hashlib.sha256(raw).hexdigest(), digest(legacy)
        (folder / "profile.json").write_bytes(raw)
        for name in ("identity.json", "classification.json", "human_tags.json", "machine_tags.json"):
            path = folder / name
            obj = json.loads(path.read_text("utf-8"))
            obj["profile_sha256"] = pretty_hash if name in {"identity.json", "classification.json"} else canonical_hash
            if name == "machine_tags.json":
                obj["source_classification_profile_sha256"] = pretty_hash
            path.write_bytes(json_bytes(obj))
    return Path(directory)
