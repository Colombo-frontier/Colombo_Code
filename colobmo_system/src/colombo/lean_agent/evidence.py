"""Validate saved Lean evidence without executing a compiler or a model.

These checks establish completeness and internal consistency of a local report.
They are not a signature, an independent recompilation, or protection against an
operator who can replace both evidence and its receipts.
"""
from __future__ import annotations

import hashlib
import re

from colombo.downstream.handoff import digest
from colombo.lean_agent.compiler import _NAME, _TOOLCHAIN, _source_policy, audit_declarations
from colombo.shared.file_io import json_bytes


EVIDENCE_VERSION = 1
_SHA256 = re.compile(r"[0-9a-f]{64}")


def _require(condition, message):
    if not condition:
        raise ValueError("Invalid Lean evidence: " + message)


def _hash_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _is_hash(value):
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def _names(value):
    return (isinstance(value, list) and bool(value)
            and all(isinstance(v, str) and _NAME.fullmatch(v) for v in value)
            and len(value) == len(set(value)))


def validate_compiler_evidence(source, declarations, build):
    """Check the embedded source, command output, declaration and axiom receipts."""
    _require(isinstance(source, str) and bool(source.strip()), "missing Lean source")
    uses_mathlib = _source_policy(source)
    _require(_names(declarations), "invalid or duplicate declaration names")
    _require(isinstance(build, dict) and build.get("status") == "passed",
             "compiler did not pass")
    _require(build.get("diagnostics") == [], "compiler has unresolved diagnostics")
    _require(build.get("semantic_correspondence") == "not_checked",
             "compiler evidence must not certify informal correspondence")
    _require(build.get("declarations") == declarations, "compiler declaration coverage differs")
    _require(build.get("source_sha256") == _hash_text(source), "source hash differs")
    files = build.get("source_files")
    allowed = {"Main.lean", "lean-toolchain", "lakefile.toml", "lakefile.lean", "lake-manifest.json"}
    _require(isinstance(files, dict) and {"Main.lean", "lean-toolchain"}.issubset(files)
             and set(files).issubset(allowed)
             and len(set(files) & {"lakefile.toml", "lakefile.lean"}) == 1
             and all(_is_hash(value) for value in files.values()), "incomplete project file hashes")
    _require(not uses_mathlib or "lake-manifest.json" in files,
             "Mathlib source lacks its pinned dependency manifest hash")
    _require(files["Main.lean"] == build["source_sha256"], "project source hash differs")
    _require(build.get("project_sha256") == hashlib.sha256(json_bytes(files)).hexdigest(),
             "project hash differs")
    toolchain = build.get("toolchain")
    match = _TOOLCHAIN.fullmatch(toolchain) if isinstance(toolchain, str) else None
    _require(match is not None, "missing pinned Lean toolchain")
    _require(_is_hash(build.get("compiled_sha256")), "missing compiled object hash")
    audit = "import Main\nset_option pp.all true\n" + "".join(
        f"#check {name}\n#print {name}\n#print axioms {name}\n" for name in declarations)
    _require(build.get("audit_sha256") == _hash_text(audit), "audit command hash differs")

    commands = build.get("commands")
    _require(isinstance(commands, list) and len(commands) == 3, "missing compiler command receipts")
    for phase, command in zip(("version", "compile", "audit"), commands):
        _require(isinstance(command, dict) and command.get("phase") == phase,
                 "compiler command phases differ")
        _require(type(command.get("returncode")) is int and command["returncode"] == 0
                 and command.get("timed_out") is False
                 and command.get("process_tree_terminated") is True,
                 "compiler command did not finish successfully: " + phase)
        argv = command.get("argv")
        _require(isinstance(argv, list) and bool(argv)
                 and all(isinstance(v, str) and v for v in argv), "missing command arguments")
        if phase == "version":
            _require(argv[-3:] == ["env", "lean", "--version"], "unexpected version command")
        elif phase == "compile":
            _require(len(argv) >= 6 and argv[-5:-2] == ["env", "lean", "-o"]
                     and argv[-1] == "Main.lean", "unexpected compile command")
        else:
            _require(len(argv) >= 4 and argv[-3:-1] == ["env", "lean"]
                     and argv[-1].replace("\\", "/").endswith("/Audit.lean"),
                     "unexpected audit command")
        for stream in ("stdout", "stderr"):
            value = command.get(stream)
            _require(isinstance(value, str), "missing embedded compiler " + stream)
            _require(command.get(stream + "_sha256") == _hash_text(value),
                     "compiler output hash differs: " + stream)
    _require(re.search(r"\bversion " + re.escape(match[1]) + r"[, )]", commands[0]["stdout"]),
             "recorded compiler version differs from toolchain")
    printout = build.get("declaration_printout")
    _require(isinstance(printout, str) and printout == commands[-1]["stdout"],
             "declaration printout differs from audit output")
    _require(build.get("axioms") == audit_declarations(printout, declarations),
             "axiom list differs from declaration audit")
    return build


def review_binding(package, source, mapping, build, review):
    """Host-owned receipt for the exact input and output of correspondence review."""
    candidate = {"proof_sha256": package["proof_sha256"], "status": "candidate",
                 "source": source, "mapping": mapping, "limitations": []}
    return {"package_sha256": digest(package), "proof_sha256": package["proof_sha256"],
            "source_sha256": _hash_text(source), "project_sha256": build["project_sha256"],
            "compiler_sha256": digest(build), "mapping_sha256": digest(mapping),
            "review_input_sha256": digest({**package, "candidate": candidate, "compiler": build}),
            "review_sha256": digest(review)}


def validate_lean_result(package, result, *, require_passed=True):
    """Common fresh-result, cache-replay and Writing-import gate.

Portable imports validate embedded evidence, without reading its original local
paths. Trust in the producer is still required; no recompilation happens here.
"""
    _require(isinstance(result, dict), "result must be an object")
    _require(type(result.get("evidence_version")) is int
             and result["evidence_version"] == EVIDENCE_VERSION,
             "missing or unsupported evidence version; rerun Lean in a new output directory")
    _require(package.get("proof_sha256") == digest(package.get("proof")), "ProofDraft hash differs")
    _require(result.get("proof_sha256") == package["proof_sha256"], "result belongs to another proof")
    _require(result.get("package_sha256") == digest(package), "result belongs to another handoff package")
    required = package.get("required_claim_ids")
    _require(isinstance(required, list) and bool(required)
             and all(isinstance(v, str) and v.strip() for v in required)
             and len(required) == len(set(required)), "invalid required Claim IDs")
    _require(result.get("required_claim_ids") == required, "result Claim coverage differs")
    status = result.get("status")
    _require(status in ("passed", "failed", "blocked", "incomplete"), "unknown result status")
    if status != "passed":
        _require(not require_passed, "Writing requires a passed Lean result")
        return result
    _require(result.get("diagnostics") == [], "passing result has unresolved diagnostics")
    mapping = result.get("mapping")
    _require(isinstance(mapping, list) and len(mapping) == len(required), "incomplete Claim mapping")
    _require(all(isinstance(m, dict) and set(m) == {"claim_id", "declaration", "correspondence"}
                 and isinstance(m["claim_id"], str) and isinstance(m["correspondence"], str)
                 and m["correspondence"].strip() for m in mapping), "invalid Claim mapping")
    ids = [m["claim_id"] for m in mapping]
    declarations = [m["declaration"] for m in mapping]
    _require(len(ids) == len(set(ids)) and set(ids) == set(required), "Claim mapping coverage differs")
    build = validate_compiler_evidence(result.get("source"), declarations, result.get("compiler"))
    review = result.get("semantic_review")
    _require(isinstance(review, dict) and set(review) == {
        "proof_sha256", "verdict", "checked_claim_ids", "findings"}, "missing correspondence review")
    checked = review["checked_claim_ids"]
    _require(review["proof_sha256"] == package["proof_sha256"] and review["verdict"] == "pass"
             and review["findings"] == [] and isinstance(checked, list)
             and all(isinstance(v, str) for v in checked) and len(checked) == len(set(checked))
             and set(checked) == set(required), "incomplete or mismatched correspondence review")
    _require(result.get("semantic_review_binding") == review_binding(
        package, result["source"], mapping, build, review), "correspondence evidence binding differs")
    return result
