"""Read-only native maintenance appendices; canonical science is never edited.

This module returns text/tree nodes, HTML and integrity ledgers. It grants no
source-read, review, theorem or publication credit and never writes artifacts.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import html
import json
import re
from pathlib import Path

import export_profiles as _legacy_export
import vendor_renderer as _vendor

HERE = Path(__file__).resolve().parent
for _module, _name in ((_legacy_export, "export_profiles.py"), (_vendor, "vendor_renderer.py")):
    if Path(_module.__file__).resolve() != HERE / _name:
        raise ValueError("Load the adjacent Atlas render modules in a clean process: " + _name)
_LEGACY_NODES = _legacy_export.profile_nodes
DISCLAIMER = ("Read-only presentation of the stored native record. Integrity hashes identify source values; "
              "this appendix grants no new theorem, source-read credit, review or approval.")
COMPARISON_KEY_FIELDS = ("setting_id", "view_id", "guarantee_id", "quantity_id",
                         "resource_projection_id", "regime_id")


def canonical_hash(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def pointer_child(pointer, token):
    return pointer + "/" + str(token).replace("~", "~0").replace("/", "~1")


def value_kind(value):
    if value is None:
        return "null"
    if type(value) is bool:
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "object" if value else "empty_object"
    if isinstance(value, list):
        return "array" if value else "empty_array"
    if type(value) in (int, float):
        return "number"
    raise ValueError("Native render values must be JSON values")


def value_text(value):
    if isinstance(value, str) and value.strip():
        return value
    return json.dumps(value, ensure_ascii=False, allow_nan=False)


def tree_records(value, pointer):
    """One exact entry for every scalar, empty container and nonempty section."""
    record = {"pointer": pointer, "canonical_sha256": canonical_hash(value), "kind": value_kind(value)}
    if isinstance(value, (dict, list)):
        record["record_count"] = len(value)
    yield record
    children = value.items() if isinstance(value, dict) else enumerate(value) if isinstance(value, list) else ()
    for key, child in children:
        yield from tree_records(child, pointer_child(pointer, key))


def leaf_records(value, pointer):
    for record in tree_records(value, pointer):
        if record["kind"] not in {"object", "array"}:
            yield record


def display_profile(profile):
    """Adapt only legacy display aliases/fallbacks on an independent deep copy."""
    if not isinstance(profile, dict):
        raise ValueError("A native profile must be an object")
    result, aliases, fallbacks, seen = deepcopy(profile), [], [], set()
    # These are equal-value aliases already accepted by the native binding
    # validator. Only legacy display lookups are supplied; no identity is
    # inferred from neighboring records or scientific content.
    for collection, alternate in (("references", "source_id"), ("bounds", "bound_id")):
        rows = result.get(collection, [])
        if not isinstance(rows, list):
            raise ValueError("Native " + collection + " must be an array")
        identities = set()
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                raise ValueError("Every native " + collection + " record must be an object")
            values = [row[key] for key in ("id", alternate) if key in row]
            if (not values or any(not isinstance(value, str) or not value.strip() for value in values)
                    or len(set(values)) != 1):
                raise ValueError("Missing, invalid or conflicting id/" + alternate + " aliases")
            identity = values[0]
            if identity in identities:
                raise ValueError("Duplicate native " + collection + " identity: " + identity)
            identities.add(identity)
            if "id" not in row:
                row["id"] = identity
                aliases.append({"pointer": "/" + collection + "/" + str(index),
                                "source_field": alternate, "display_field": "id", "value": identity})
    comparisons = result.get("comparisons", [])
    if not isinstance(comparisons, list):
        raise ValueError("Native comparisons must be an array")
    for index, comparison in enumerate(comparisons):
        if not isinstance(comparison, dict):
            raise ValueError("Every native comparison must be an object")
        if "comparison_key" not in comparison:
            continue
        key = comparison["comparison_key"]
        if not isinstance(key, dict):
            raise ValueError("A native comparison_key must be an object")
        for field in COMPARISON_KEY_FIELDS:
            if field not in key:
                continue
            if field in comparison and (type(comparison[field]) is not type(key[field])
                                        or comparison[field] != key[field]):
                raise ValueError("Flat comparison identity conflicts with comparison_key: " + field)
            if field not in comparison:
                comparison[field] = deepcopy(key[field])
                aliases.append({"pointer": "/comparisons/" + str(index),
                                "source_field": "comparison_key/" + field,
                                "display_field": field, "value": deepcopy(key[field])})
    for index, comparison in enumerate(comparisons):
        guards = comparison.get("bracket", {}).get("claim_guards", {})
        for identity, value in list(guards.items()):
            if isinstance(value, str):
                guards[identity] = [{"predicate_text": value}]
                aliases.append({"pointer": "/comparisons/" + str(index) + "/bracket/claim_guards/" + identity,
                                "source_kind": "string", "display_kind": "predicate_text_array", "value": value})
    proofs = result.get("proofs", [])
    if not isinstance(proofs, list):
        raise ValueError("Native proofs must be an array")
    for index, proof in enumerate(proofs):
        if not isinstance(proof, dict):
            raise ValueError("Every native proof must be an object")
        values = [proof[key] for key in ("id", "proof_id") if key in proof]
        if (not values or any(not isinstance(value, str) or not value.strip() for value in values)
                or len(set(values)) != 1):
            raise ValueError("Missing, invalid or conflicting id/proof_id aliases")
        identity = values[0]
        if identity in seen:
            raise ValueError("Duplicate native proof identity: " + identity)
        seen.add(identity)
        if "proof_id" not in proof:
            proof["proof_id"] = identity
            aliases.append({"pointer": f"/proofs/{index}", "source_field": "id",
                            "display_field": "proof_id", "value": identity})
        # The old renderer cannot concatenate a non-string title or cite a
        # non-list source_refs value. Their full originals go in the appendix.
        if "title" in proof and not isinstance(proof["title"], str):
            proof["title"] = "Native proof " + identity
            fallbacks.append({"pointer": f"/proofs/{index}/title", "reason": "non-string legacy title"})
        if "source_refs" in proof and (not isinstance(proof["source_refs"], list)
                                      or not all(isinstance(x, str) for x in proof["source_refs"])):
            proof["source_refs"] = []
            fallbacks.append({"pointer": f"/proofs/{index}/source_refs", "reason": "non-list legacy citations"})
    return result, aliases, fallbacks


def normalise_display_profile(profile):
    """Return an independent legacy render copy; never a native-file update."""
    return display_profile(profile)[0]


def _simple_text(value):
    return ((isinstance(value, str) and bool(value.strip()))
            or (isinstance(value, list) and bool(value)
                and all(isinstance(item, str) and item.strip() for item in value)))


def _legacy_proof_fields(proof):
    fields = {key for key in ("scope", "algorithm_scope", "statement", "limitations")
              if key in proof and _simple_text(proof[key])}
    if isinstance(proof.get("title"), str) and proof["title"].strip():
        fields.add("title")
    selected = "body" if proof.get("body") else "proof"
    if selected in proof and _simple_text(proof[selected]):
        fields.add(selected)
    # A legacy node can display a rewritten sentence. Such a field is not
    # original-text coverage: append its complete native value instead.
    return {key for key in fields if not any(
        re.search(r"Information interface|\bcoverage\b", text, re.I)
        for text in ([proof[key]] if isinstance(proof[key], str) else proof[key]))}


def _source_node(value, pointer):
    return ("p", "Native pointer: " + pointer + "; canonical SHA-256: " + canonical_hash(value))


def _tree_nodes(value, pointer, label, depth=0):
    """Readable hierarchical nodes; no blob conversion of a dict/list."""
    nodes = [("h3" if depth == 0 else "h4", label), _source_node(value, pointer)]
    if isinstance(value, dict) and value:
        for key, child in value.items():
            nodes.extend(_tree_nodes(child, pointer_child(pointer, key), "Native field: " + str(key), depth + 1))
    elif isinstance(value, list) and value:
        for index, child in enumerate(value):
            nodes.extend(_tree_nodes(child, pointer_child(pointer, index), "Native item " + str(index + 1), depth + 1))
    elif isinstance(value, str) and value.strip():
        nodes.append(("literal", value))
    else:
        nodes.append(("p", "Native value (" + value_kind(value) + "): " + value_text(value)))
    return nodes


def maintenance_nodes(profile):
    """Return (nodes, integrity ledger), inserting appendices before References.

    Existing core nodes retain the upstream historical terminology policy.
    New native appendices preserve their original text, including coverage.
    """
    original = deepcopy(profile)
    shown, aliases, fallbacks = display_profile(original)
    # Free-form native proofs are rendered exactly once in the literal appendix.
    # Their historical parser can interpret IDs/JSON escapes as mathematics.
    shown["proofs"] = []
    legacy = list(_LEGACY_NODES(shown))
    appendix, leaves, sections, records = [], [], [], []
    if "proofs" in original:
        proofs = original["proofs"]
        sections.extend(tree_records(proofs, "/proofs"))
        appendix.extend([("h2", "Maintenance appendix: Native proof extensions"), ("p", DISCLAIMER),
                         _source_node(proofs, "/proofs")])
        if not proofs:
            appendix.append(("p", "Native value (empty_array): []"))
            leaves.append({**next(leaf_records(proofs, "/proofs")), "route": "appendix"})
        for index, proof in enumerate(proofs):
            pointer = "/proofs/" + str(index)
            identity = proof.get("proof_id", proof.get("id"))
            records.append({"pointer": pointer, "canonical_sha256": canonical_hash(proof), "proof_id": identity})
            appendix.extend([("h3", "Native proof: " + identity), _source_node(proof, pointer)])
            legacy_fields = set()
            for key, value in proof.items():
                path = pointer_child(pointer, key)
                if key in {"id", "proof_id"}:
                    route = "appendix.identifier_header"
                elif key in legacy_fields:
                    route = "legacy.simple_field"
                else:
                    route = "appendix"
                    appendix.extend(_tree_nodes(value, path, "Native field: " + str(key), 1))
                leaves.extend({**leaf, "route": route} for leaf in leaf_records(value, path))
    if "joint_analysis" in original:
        joint = original["joint_analysis"]
        appendix.extend([("h2", "Maintenance appendix: Complete native joint analysis"), ("p", DISCLAIMER)])
        appendix.extend(_tree_nodes(joint, "/joint_analysis", "Native joint analysis"))
        sections.extend(tree_records(joint, "/joint_analysis"))
        leaves.extend({**leaf, "route": "appendix"} for leaf in leaf_records(joint, "/joint_analysis"))
    insertion = next((i for i, node in enumerate(legacy) if node == ("h2", "References")), len(legacy))
    nodes = legacy[:insertion] + appendix + legacy[insertion:]
    roots = [{"pointer": "/" + key, "canonical_sha256": canonical_hash(original[key])}
             for key in ("proofs", "joint_analysis") if key in original]
    ledger = {"render_input_canonical_sha256": canonical_hash(original),
              "canonical_sections": roots, "proof_records": records, "sections": sections, "leaves": leaves,
              "display_aliases": aliases, "legacy_display_fallbacks": fallbacks,
              "appendix_node_range": [insertion, insertion + len(appendix)],
              "nodes_canonical_sha256": canonical_hash(nodes),
              "coverage_scope": "Native proof and joint-analysis text/tree nodes, not compiled PDF or scientific validation.",
              "tool_read_credit": False, "approval_credit": False}
    return nodes, ledger


def _html_tree(value, pointer, label):
    metadata = (' data-native-pointer="' + html.escape(pointer, quote=True) + '" data-canonical-sha256="'
                + canonical_hash(value) + '" data-native-kind="' + value_kind(value) + '"')
    title = html.escape(label, quote=True)
    source = '<small class="native-source">' + html.escape(pointer) + ' · SHA-256 ' + canonical_hash(value) + '</small>'
    if isinstance(value, (dict, list)) and value:
        children = value.items() if isinstance(value, dict) else enumerate(value)
        inner = ''.join(_html_tree(child, pointer_child(pointer, key), str(key) if isinstance(value, dict)
                                  else "Native item " + str(key + 1)) for key, child in children)
        return '<details class="native-record"' + metadata + '><summary>' + title + '</summary>' + source + inner + '</details>'
    text = html.escape(value_text(value), quote=True)
    return ('<div class="native-leaf"' + metadata + '><div class="native-label">' + title + '</div>' + source
            + '<div class="native-value" style="white-space:pre-wrap">' + text + '</div></div>')


def maintenance_html(profile):
    """Folded complete native trees, with escaped original math/prose strings."""
    original = deepcopy(profile)
    display_profile(original)  # Enforce exactly the same proof-identity fence.
    pieces = []
    for key, attribute, title in (("proofs", "data-native-proof-appendix", "Native proof records"),
                                  ("joint_analysis", "data-native-analysis-appendix", "Complete native joint analysis")):
        if key not in original:
            continue
        pieces.append('<section class="maintenance-native-appendix" ' + attribute + '=\'true\'><h2>' + title + '</h2><p>' + html.escape(DISCLAIMER) + '</p>'
                      + _html_tree(original[key], "/" + key, title) + '</section>')
    return '\n'.join(pieces)
