#!/usr/bin/env python3
"""Build an explicitly derived, privacy-safe Memory replica, never a new review.

The source Store is read-only. This command writes a fresh output pair only and
does not publish, start a model, copy runtime evidence, or alter the source.
Historical review hashes retain their original identity. Projected record hashes
are different objects and are labelled as such in the manifest and disclosure.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys


SCHEMA = "colombo-memory-privacy-projection/1"
TRANSFORMATION = "local-locators-and-pinned-hashes-v1"
DISCLOSURE_FILE = "PRIVACY_PROJECTION.json"
HASH_TOKEN = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
PUBLIC_URL = re.compile(r"https?://[^\s<>\"'`]+", re.IGNORECASE)
LOCAL_START = re.compile(
    r"file://|/(?:Users|private|tmp|home|Applications|Volumes|var/folders)/"
    r"|(?<![A-Za-z0-9])[A-Za-z]:[\\/](?:Users|Windows|Program Files(?: \(x86\))?|"
    r"Documents and Settings|Temp|tmp|private|home|workspace|projects|work|repo|code)(?:[\\/]|$)",
    re.IGNORECASE,
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def pointer_part(value):
    return str(value).replace("~", "~0").replace("/", "~1")


def string_leaves(value, pointer="#"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from string_leaves(child, pointer + "/" + pointer_part(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from string_leaves(child, pointer + "/" + str(index))
    elif isinstance(value, str):
        yield pointer, value


def local_matches(value):
    # A public URL may legitimately contain /home/ or a similar path segment.
    # Never classify characters inside an HTTP(S) URL as a local locator.
    public = [(match.start(), match.end()) for match in PUBLIC_URL.finditer(value)]
    return [match for match in LOCAL_START.finditer(value)
            if not any(start <= match.start() < end for start, end in public)]


def contains_local(value):
    return any(local_matches(text) for _, text in string_leaves(value))


def public_urls(value):
    return Counter(match.group(0) for _, text in string_leaves(value)
                   for match in PUBLIC_URL.finditer(text))


def artifact_uri(parent):
    # Use an existing material SHA rather than commit to a private pathname.
    # If a parent has multiple unrelated hashes, do not guess their meaning.
    candidates = []
    if isinstance(parent, dict):
        for key in ("content_hash", "sha256", "original_sha256", "artifact_sha256"):
            value = parent.get(key)
            if isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value):
                candidates.append(value)
    values = set(candidates)
    if len(values) == 1:
        return "urn:colombo:artifact:sha256:" + next(iter(values))
    return "urn:colombo:local-locator-redacted"


def redact_locator(value, parent, pointer):
    matches = local_matches(value)
    if not matches:
        return value, False
    # Scientific content is not rewritten. All observed source payload locators
    # are whole path strings except this explicit labelled manifest locator.
    # Reject an unfamiliar mixed-prose case rather than deleting its argument.
    if matches[0].start() == 0:
        need(not PUBLIC_URL.search(value) and "\n" not in value and "$" not in value,
             "Ambiguous mixed local locator at " + pointer)
        return artifact_uri(parent), True
    label = "Pages-manifest snapshot: "
    if value.startswith(label) and matches[0].start() == len(label):
        need(not PUBLIC_URL.search(value) and "\n" not in value and "$" not in value,
             "Ambiguous labelled local locator at " + pointer)
        return label + artifact_uri(parent), True
    raise ValueError("Unsupported embedded local locator at " + pointer)


def transform(value, resolve_hash, changes, pointer="#", parent=None):
    if isinstance(value, dict):
        # Keys in the scientific schema are not locator data. Refuse unexpected
        # private keys instead of silently altering the object structure.
        need(not any(local_matches(str(key)) for key in value),
             "Local locator in a JSON object key at " + pointer)
        return {key: transform(child, resolve_hash, changes,
                               pointer + "/" + pointer_part(key), value)
                for key, child in value.items()}
    if isinstance(value, list):
        return [transform(child, resolve_hash, changes,
                          pointer + "/" + str(index), value)
                for index, child in enumerate(value)]
    if not isinstance(value, str):
        return deepcopy(value)
    changed, redacted = redact_locator(value, parent, pointer)
    if redacted:
        changes.append({"pointer": pointer, "operation": "local_locator_redacted"})
    # Hash references to another scientific record are processed as a DAG.
    # PDF/source bytes hashes are unaffected unless they are literally a known
    # canonical record digest, an ambiguity that is checked by the caller.
    replacements = []

    def replacement(match):
        original = match.group(0)
        projected = resolve_hash(original)
        if projected != original:
            replacements.append((original, projected))
        return projected

    result = HASH_TOKEN.sub(replacement, changed)
    for original, projected in replacements:
        changes.append({"pointer": pointer, "operation": "pinned_record_hash_remapped",
                        "original_content_hash": original,
                        "projected_content_hash": projected})
    return result


def export_note(original_hash, projected_hash, changes):
    return {"schema": SCHEMA, "transformation": TRANSFORMATION,
            "original_content_hash": original_hash,
            "projected_content_hash": projected_hash,
            "no_new_review": True,
            "change_pointers": sorted({row["pointer"] for row in changes}),
            "meaning": "Derived privacy projection. Original review applies to the original content hash; no new Reviewer acceptance is asserted for projected bytes."}


def build(args):
    live_root = args.live_memory_root.resolve()
    live_state = live_root.with_name("." + live_root.name + "_state")
    component = args.component_repo.resolve()
    out = args.output_root.resolve()
    need(live_root.name == "long_term_memory", "Expected the explicit live Memory root")
    need(not out.is_relative_to(live_root.parent), "Output must be outside the source system directory")
    need(not (live_state / ".writer.lock").exists(), "Source Writer is active; wait without deleting its lock")
    need(not out.exists() or (out.is_dir() and not any(out.iterdir())), "Projection output must be an empty directory")
    source_pointers = {name: (live_state / name).read_bytes() for name in ("CURRENT.json", "LEADS.json")}
    sys.path[:0] = [str(component / "src"),
                    str(component / "colombo_memory_agent/runtime")]
    from colombo.memory.contracts import LIBRARIES, canonical_bytes, digest, validate_record, validate_review
    from colombo.memory.integration import _validate_store
    from colombo.memory.store import Store, atomic_json
    from colombo_memory_agent.store import WriterStore

    live = Store(live_root)
    _validate_store(live)
    manifest = live.manifest()
    original_manifest_digest = digest(manifest)
    leads = live.lead_manifest()
    originals = {}
    original_bytes = {}
    history_refs = {}
    identity_hashes = {}

    def register(ref):
        ident, kind, revision, old_hash = (ref[key] for key in ("id", "kind", "revision", "content_hash"))
        need(ref.get("tier") == "published", "Published history ref has a different tier")
        identity = (ident, kind, revision)
        need(identity not in identity_hashes or identity_hashes[identity] == old_hash,
             "Conflicting published identity: " + ident)
        identity_hashes[identity] = old_hash
        relative = f"history/{LIBRARIES[kind]}/{ident}/r{revision:06d}-{old_hash}.json"
        path = live._state_inside(relative)
        need(path.is_file() and not path.is_symlink(), "Missing regular historical object: " + ident)
        data = path.read_bytes()
        record = json.loads(data)
        need(digest(record) == old_hash, "Historical object hash mismatch: " + ident)
        need((record["id"], record["kind"], record["revision"]) == identity,
             "Historical object identity mismatch: " + ident)
        validate_record(record, require_revision=True)
        if old_hash in originals:
            need(originals[old_hash] == record, "Canonical digest identity collision")
        originals[old_hash] = record
        original_bytes[old_hash] = data
        history_refs[old_hash] = {key: ref[key] for key in ("id", "kind", "revision", "content_hash", "tier")}

    for ref in manifest["entries"].values():
        register(ref)
    for receipt in manifest["receipts"].values():
        for ref in receipt["published_refs"]:
            register(ref)
    lead_hashes = set()
    lead_raw = {}
    for ident, entry in leads["entries"].items():
        path = live.current_path(ident, entry["kind"])
        need(path.is_file() and not path.is_symlink(), "Missing regular lead: " + ident)
        data = path.read_bytes()
        record = json.loads(data)
        old_hash = digest(record)
        need(old_hash == entry["content_hash"] and record["evidence"]["readiness"] == "lead",
             "Lead hash/readiness mismatch: " + ident)
        need(ident not in manifest["entries"], "Lead/publication overlap: " + ident)
        validate_record(record)
        originals[old_hash] = record
        original_bytes[old_hash] = data
        lead_hashes.add(old_hash)
        lead_raw[ident] = data

    projected = {}
    mapping = {}
    changes_by_hash = {}
    visiting = set()

    def resolve(old_hash):
        if old_hash not in originals:
            return old_hash
        if old_hash in mapping:
            return mapping[old_hash]
        need(old_hash not in visiting, "Cycle in pinned scientific digest references")
        visiting.add(old_hash)
        original = originals[old_hash]
        changes = []
        result = transform(original, resolve, changes)
        need(public_urls(result) == public_urls(original), "Public URLs changed: " + original["id"])
        need(not contains_local(result), "Projected record still has a local locator: " + original["id"])
        need(all(result[key] == original[key] for key in ("id", "kind", "revision", "schema")),
             "Scientific identity changed: " + original["id"])
        validate_record(result, require_revision=old_hash not in lead_hashes)
        new_hash = digest(result)
        projected[old_hash] = result
        changes_by_hash[old_hash] = changes
        mapping[old_hash] = new_hash
        visiting.remove(old_hash)
        return new_hash

    for old_hash in sorted(originals):
        resolve(old_hash)
    # Parent-provided material hashes are original-file identities, never a
    # canonical scientific record reference. Reject an accidental ambiguity.
    for old_hash, record in originals.items():
        if record["kind"] == "source":
            for material in record["content"].get("original_material", []):
                for key in ("content_hash", "sha256"):
                    material_hash = material.get(key)
                    need(not material_hash or material_hash not in originals,
                         "Source-material/scientific-record digest ambiguity")

    out.mkdir(parents=True, exist_ok=True)
    target_root = out / "long_term_memory"
    target = WriterStore(target_root)
    for library in set(LIBRARIES.values()):
        (target_root / library).mkdir(parents=True, exist_ok=True)
    target.state_root.mkdir(parents=True, exist_ok=True)
    safe_evidence = target.state_root / "evidence"

    def write_object(path, old_hash):
        path.parent.mkdir(parents=True, exist_ok=True)
        data = original_bytes[old_hash] if mapping[old_hash] == old_hash else canonical_bytes(projected[old_hash])
        path.write_bytes(data)
        need(digest(json.loads(data)) == mapping[old_hash], "Written projection hash mismatch")

    for old_hash, ref in sorted(history_refs.items()):
        relative = f"history/{LIBRARIES[ref['kind']]}/{ref['id']}/r{ref['revision']:06d}-{mapping[old_hash]}.json"
        write_object(target._state_inside(relative), old_hash)
    for ident, entry in manifest["entries"].items():
        current = read(live.current_path(ident, entry["kind"]))
        need(digest(current) == entry["content_hash"], "Current source record differs from pinned history: " + ident)
        write_object(target.current_path(ident, entry["kind"]), entry["content_hash"])
    for old_hash in lead_hashes:
        record = projected[old_hash]
        write_object(target.current_path(record["id"], record["kind"]), old_hash)

    derived = deepcopy(manifest)
    need(not contains_local(derived), "Original manifest metadata contains local locators; do not rewrite accepted review scopes")
    for ident, entry in derived["entries"].items():
        old_hash = entry["content_hash"]
        new_hash = mapping[old_hash]
        entry["content_hash"] = new_hash
        entry["path"] = f"history/{LIBRARIES[entry['kind']]}/{ident}/r{entry['revision']:06d}-{new_hash}.json"
        need(entry["review_scope"]["record_hash"] == old_hash and entry["review_scope"]["decision"] == "accept",
             "Original current review does not accept its exact original record: " + ident)
        if new_hash != old_hash:
            entry["privacy_projection"] = export_note(old_hash, new_hash, changes_by_hash[old_hash])
    native_receipt_bytes = {}
    expected_receipt_digests = {digest(value) for value in manifest["receipts"].values()}
    for path in sorted((live_state / "staging").glob("*/receipt.json")):
        data = path.read_bytes()
        value = json.loads(data)
        value_hash = digest(value)
        if value_hash in expected_receipt_digests:
            native_receipt_bytes.setdefault(value_hash, data)
    need(set(native_receipt_bytes) == expected_receipt_digests,
         "Actual native receipt artifacts are incomplete")
    original_receipts = []
    for proposal_digest, receipt in sorted(manifest["receipts"].items()):
        original_receipt_digest = digest(receipt)
        need(receipt["proposal_digest"] == proposal_digest, "Original receipt/proposal commitment mismatch")
        original_path = None
        if not contains_local(receipt):
            original_path = "evidence/original_receipts/" + original_receipt_digest + ".json"
            # Preserve exact original native receipt file bytes. This is not a
            # fabricated receipt or a new acceptance of the projected objects.
            path = target._state_inside(original_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(native_receipt_bytes[original_receipt_digest])
        projected_refs = []
        for ref in receipt["published_refs"]:
            row = deepcopy(ref)
            row["content_hash"] = mapping[ref["content_hash"]]
            projected_refs.append(row)
        exported_receipt = deepcopy(receipt)
        exported_receipt.update(
            schema="colombo-memory-privacy-projection-receipt/1",
            status="privacy_projected",
            published_refs=projected_refs,
            original_receipt_digest=original_receipt_digest,
            original_proposal_digest=proposal_digest,
            original_review_digest=receipt["review_digest"],
            original_receipt_path=original_path,
            no_new_review=True,
            meaning="Derived relocation receipt only; original acceptance and publication commitments are retained without asserting review of projected hashes.",
        )
        derived["receipts"][proposal_digest] = exported_receipt
        original_receipts.append({"original_proposal_digest": proposal_digest,
                                  "original_receipt_digest": original_receipt_digest,
                                  "original_review_digest": receipt["review_digest"],
                                  "original_receipt_path": original_path,
                                  "original_file_sha256": sha_bytes(native_receipt_bytes[original_receipt_digest]) if original_path else None,
                                  "original_published_refs": deepcopy(receipt["published_refs"]),
                                  "projected_published_refs": projected_refs})

    expected_review_digests = {receipt["review_digest"] for receipt in manifest["receipts"].values()}
    review_files = {}
    for path in sorted((live_state / "staging").glob("*/review.json")):
        review = read(path)
        value_hash = digest(review)
        if value_hash not in expected_review_digests:
            continue
        proposal = read(path.with_name("proposal.json"))
        proposal_digest = proposal["digest"]
        need(digest({key: value for key, value in proposal.items() if key != "digest"}) == proposal_digest,
             "Published original proposal changed")
        need(proposal_digest in manifest["receipts"] and manifest["receipts"][proposal_digest]["review_digest"] == value_hash,
             "Original accepted review has no matching receipt")
        validate_review(proposal, review)
        need(review.get("backend") == "codex_cli", "Original review is not a native model review")
        review_files[value_hash] = (path, review)
    for ident, entry in manifest["entries"].items():
        need(entry["review_digest"] in review_files, "Current entry lacks its original review artifact: " + ident)
        review = review_files[entry["review_digest"]][1]
        matching = [item for item in review["items"] if item["id"] == ident]
        need(len(matching) == 1 and matching[0] == entry["review_scope"],
             "Current review scope differs from its actual original review: " + ident)
        need(entry["reviewer_run_id"] == review["reviewer_run_id"]
             and entry["review_backend"] == review["backend"],
             "Current review identity differs from its actual original review: " + ident)
    original_reviews = []
    for review_hash in sorted(expected_review_digests):
        need(review_hash in review_files, "Actual original review artifact unavailable")
        path, review = review_files[review_hash]
        exported_path = None
        raw_digest = None
        if not contains_local(review):
            exported_path = "evidence/original_reviews/" + review_hash + ".json"
            dest = target._state_inside(exported_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            data = path.read_bytes()
            dest.write_bytes(data)
            raw_digest = sha_bytes(data)
        original_reviews.append({"original_review_digest": review_hash,
                                 "original_review_path": exported_path,
                                 "original_file_sha256": raw_digest,
                                 "omitted_due_to_private_locators": exported_path is None})

    rows = []
    for old_hash, ref in sorted(history_refs.items(), key=lambda item: (item[1]["id"], item[1]["revision"], item[0])):
        row = {key: ref[key] for key in ("id", "kind", "revision", "tier")}
        row.update(export_note(old_hash, mapping[old_hash], changes_by_hash[old_hash]))
        row["changes"] = changes_by_hash[old_hash]
        rows.append(row)
    lead_rows = []
    for old_hash in sorted(lead_hashes, key=lambda value: originals[value]["id"]):
        record = originals[old_hash]
        row = {key: record[key] for key in ("id", "kind", "revision")}
        row.update(export_note(old_hash, mapping[old_hash], changes_by_hash[old_hash]))
        row["tier"] = "lead"
        row["changes"] = changes_by_hash[old_hash]
        lead_rows.append(row)
    derived["privacy_projection"] = {"schema": SCHEMA, "disclosure_path": DISCLOSURE_FILE,
                                     "no_new_review": True, "transformation": TRANSFORMATION}
    disclosure = {"schema": SCHEMA, "transformation": TRANSFORMATION,
                  "created_at": datetime.now(timezone.utc).isoformat(),
                  "no_new_review": True,
                  "meaning": "Privacy-safe derived replica of previously published Memory. Original Reviewer decisions bind original hashes, not changed projected bytes. No model was run and no new canonical publication occurred.",
                  "policy": {"changes": ["local locator values replaced with non-local artifact URIs", "pinned scientific record digest references recursively remapped"],
                             "unchanged": ["record IDs, kinds, revisions and publication/lead membership", "public URLs and scientific claims", "original review scopes and review digests"],
                             "excluded": ["local job and model-run files", "prompts and commands", "source/seed files and source manifests", "credentials and operational locks", "original proposals containing private locator data", "archives and runtime caches"]},
                  "source_manifest_digest": original_manifest_digest,
                  "source_pointer_commitments": {name: sha_bytes(data) for name, data in source_pointers.items()},
                  "records": rows, "lead_records": lead_rows,
                  "original_receipts": original_receipts, "original_reviews": original_reviews,
                  "counts": {"current_published": len(manifest["entries"]), "current_leads": len(leads["entries"]),
                             "published_history_revisions": len(history_refs),
                             "changed_published_history_revisions": sum(mapping[value] != value for value in history_refs),
                             "changed_current_published": sum(mapping[entry["content_hash"]] != entry["content_hash"] for entry in manifest["entries"].values()),
                             "changed_leads": sum(mapping[value] != value for value in lead_hashes),
                             "original_publication_receipts": len(original_receipts)}}
    need(not contains_local(disclosure), "Disclosure contains local locator information")
    atomic_json(target.state_root / DISCLOSURE_FILE, disclosure)
    with target.writer():
        target._save_lead_catalog([projected[value] for value in sorted(lead_hashes)])
        target._commit_generation(derived)
    _validate_store(Store(target_root))
    stable = all((live_state / name).read_bytes() == data for name, data in source_pointers.items())
    need(stable and not (live_state / ".writer.lock").exists(), "Live Store changed or Writer became active during export; reject this projection and retry from a fresh output")
    report = {"status": "passed", "schema": SCHEMA, "no_new_review": True,
              "source_store_modified": False, "model_calls": 0,
              "source_snapshot_stable": True, "source_writer_lock_absent": True,
              "native_store_validation": "passed", **disclosure["counts"],
              "original_review_artifacts_exported": sum(row["original_review_path"] is not None for row in original_reviews),
              "original_review_artifacts_omitted_for_privacy": sum(row["original_review_path"] is None for row in original_reviews),
              "original_receipt_artifacts_exported": sum(row["original_receipt_path"] is not None for row in original_receipts),
              "record_changes": [{key: row[key] for key in ("id", "kind", "revision", "tier", "original_content_hash", "projected_content_hash", "change_pointers", "changes")}
                                 for row in rows + lead_rows if row["change_pointers"]],
              "public_projection_disclosure_sha256": sha_bytes((target.state_root / DISCLOSURE_FILE).read_bytes())}
    need(not contains_local(report), "Build report contains local locator information")
    report_path = args.report_path.resolve()
    need(not report_path.is_relative_to(live_root.parent), "Report must not modify the live system directory")
    atomic_json(report_path, report)
    return {key: value for key, value in report.items() if key != "record_changes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live-memory-root", type=Path, required=True)
    parser.add_argument("--component-repo", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True, help="Empty directory for the projected Memory pair")
    parser.add_argument("--report-path", type=Path, required=True, help="Task-local build report; never the live Store")
    args = parser.parse_args()
    try:
        result = build(args)
    except Exception as error:
        # Exception messages contain identities/pointers only, never source path
        # values. Do not expose a traceback carrying operational arguments.
        print(json.dumps({"status": "failed", "error": str(error), "model_calls": 0,
                          "source_store_modified": False}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
