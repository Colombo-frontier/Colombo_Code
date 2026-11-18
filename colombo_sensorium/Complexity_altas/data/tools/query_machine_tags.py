#!/usr/bin/env python3
"""Look up exact machine concept IDs in the released Atlas tag records."""

import argparse
import hashlib
import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1]


def read_json(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def profile_hash(profile):
    canonical = json.dumps(profile, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def query(data_dir, concept_ids, setting_id=None, axis=None):
    vocabulary = read_json(data_dir / "vocabulary" / "machine_tags.json")
    concepts = {concept["concept_id"]: concept for concept in vocabulary["concepts"]}
    axes = {item["id"] for item in vocabulary["axes"]}
    concept_ids = list(dict.fromkeys(concept_ids))
    if not concept_ids:
        raise ValueError("Specify at least one exact machine concept ID.")
    unknown = [concept_id for concept_id in concept_ids if concept_id not in concepts]
    if unknown:
        raise ValueError("Unknown exact machine concept ID(s): " + ", ".join(unknown))
    if axis is not None:
        if axis not in axes:
            raise ValueError(f"Unknown taxonomy axis: {axis}")
        if any(concepts[concept_id]["axis"] != axis for concept_id in concept_ids):
            raise ValueError(f"With --axis {axis}, all concepts must belong to {axis}.")

    profiles = {path.parent.name: path for path in
                sorted((data_dir / "settings").glob("*/profile.json"))}
    if not profiles:
        raise ValueError(f"No Atlas profiles found under {data_dir / 'settings'}.")
    if setting_id is not None:
        if setting_id not in profiles:
            raise ValueError(f"Unknown canonical setting ID: {setting_id}")
        profiles = {setting_id: profiles[setting_id]}

    matches = []
    for profile_id, path in profiles.items():
        profile = read_json(path)
        tags = read_json(path.with_name("machine_tags.json"))
        digest = profile_hash(profile)
        if (profile["setting_id"] != profile_id or tags["setting_id"] != profile_id
                or tags["profile_sha256"] != digest
                or tags["vocabulary_version"] != vocabulary["version"]):
            raise ValueError(f"Machine labels are stale or mismatched for {profile_id}.")
        views = [view["view_id"] for view in profile["views"]]
        if set(views) != set(tags["view_ids"]):
            raise ValueError(f"Machine labels have a different view inventory for {profile_id}.")

        selected = [feature for feature in tags["features"]
                    if feature["concept_id"] in concept_ids]
        view_ids_by_concept = {concept_id: set() for concept_id in concept_ids}
        for feature in selected:
            view_ids_by_concept[feature["concept_id"]].update(feature["view_ids"])
        matched_views = [view_id for view_id in views if
                         all(view_id in support for support in view_ids_by_concept.values())]
        if not matched_views:
            continue
        match_scope = set(matched_views)
        matches.append({
            "setting_id": profile_id,
            "title": profile["title"],
            "profile_sha256": digest,
            "matching_view_ids": matched_views,
            "matched_features": [feature for feature in selected
                                 if match_scope.intersection(feature["view_ids"])],
            "operation_bindings": [binding for binding in tags["operation_bindings"]
                                   if match_scope.intersection(binding["view_ids"])],
        })

    return {
        "vocabulary_version": vocabulary["version"],
        "query": {"concept_ids": concept_ids, "setting_id": setting_id, "axis": axis},
        "settings_checked": len(profiles),
        "settings_matched": len(matches),
        "matches": matches,
        "semantics": {
            "conjunction": "exact_concept_ids_in_one_view",
            "operation_bindings": "original_oracle_context_of_matching_views",
            "unrecorded_features": "unknown",
            "identity_authority": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concept", action="append", required=True,
                        help="Exact machine concept ID. Repeat to require all IDs in one view.")
    parser.add_argument("--setting", help="Restrict lookup to one canonical setting ID.")
    parser.add_argument("--axis", help="Require all requested concepts to belong to this axis.")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR,
                        help="Atlas data directory. Defaults to the data directory containing this script.")
    args = parser.parse_args()
    try:
        result = query(args.data_dir, args.concept, args.setting, args.axis)
    except (OSError, ValueError, KeyError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
