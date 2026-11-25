"""Independent Lean Agent: frozen package -> formalization -> compiler -> review.

The model adapter is injected and owns native process execution/reconciliation.
This module has no Brain, Store, Cell, or MCP dependency.
"""
from __future__ import annotations

import json
import math
import re
import shutil
import time

import jsonschema

from colombo.downstream.handoff import digest as _digest
from colombo.lean_agent.compiler import verify_lean
from colombo.lean_agent.evidence import (
    EVIDENCE_VERSION, review_binding, validate_compiler_evidence, validate_lean_result,
)
from colombo.shared.file_io import Path, atomic_write, json_bytes


def _object(properties):
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


_TEXT = {"type": "string", "minLength": 1}
_STRINGS = {"type": "array", "items": _TEXT}
_MAPPING = _object({"claim_id": _TEXT, "declaration": _TEXT, "correspondence": _TEXT})
SCHEMAS = {
    "lean-check": _object({"proof_sha256": _TEXT,
        "status": {"type": "string", "enum": ["candidate", "incomplete"]},
        "source": {"type": "string"}, "mapping": {"type": "array", "items": _MAPPING},
        "limitations": _STRINGS}),
    "lean-review": _object({"proof_sha256": _TEXT,
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "checked_claim_ids": _STRINGS, "findings": _STRINGS}),
}
_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9']*(?:\.[A-Za-z_][A-Za-z_0-9']*)*")
_GENERATE = (
    "Use .agents/skills/lean-check/SKILL.md in formalization mode. Translate the frozen package "
    "into Main.lean. Return only final JSON matching the supplied schema. This is an independent "
    "Lean Agent, with no Brain/Cell/MCP tools. The runner compiles your source after this response "
    "and supplies actual diagnostics on another attempt. Preserve the main Claim, all required "
    "Claims, definitions, quantifiers, assumptions and conclusions. Address previous compiler or "
    "correspondence feedback without changing the mathematics. Use incomplete when full faithful "
    "formalization cannot be completed; retain useful source and list remaining obligations."
)
_REVIEW = (
    "Use .agents/skills/lean-check/SKILL.md in correspondence-review mode. Independently compare "
    "the frozen ProofDraft and Setting with the actual source, compiled declaration printout and "
    "axiom audit. Review all required Claims, quantifiers, definitions, domains, assumptions, "
    "Oracle/Resource accounting, parameter dependence and conclusions. Reject tautologies, extra "
    "assumptions, vacuous encodings and weaker results. Compiler success alone does not establish "
    "correspondence. Return only final JSON matching the schema; do not edit or repair the source. "
    "Use pass only with complete coverage and no unresolved findings."
)


def _write(path, value):
    atomic_write(path, json_bytes(value))


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _validate_package(package):
    if not isinstance(package, dict) or not isinstance(package.get("proof"), dict):
        raise ValueError("Lean Agent requires a frozen ProofDraft package")
    if package.get("proof_sha256") != _digest(package["proof"]):
        raise ValueError("ProofDraft hash does not match package proof_sha256")
    required = package.get("required_claim_ids")
    if (not isinstance(required, list) or not required
            or any(not isinstance(v, str) or not v.strip() for v in required)
            or len(required) != len(set(required)) or not isinstance(package.get("setting"), dict)):
        raise ValueError("Package requires a Setting and unique required Claim IDs")


def _validate_response(stage, value, package):
    jsonschema.Draft202012Validator(SCHEMAS[stage]).validate(value)
    if value["proof_sha256"] != package["proof_sha256"]:
        raise ValueError("Model response is bound to a different ProofDraft")
    required = set(package["required_claim_ids"])
    if stage == "lean-check":
        mapping = value["mapping"]
        ids = [entry["claim_id"] for entry in mapping]
        names = [entry["declaration"] for entry in mapping]
        if (len(ids) != len(set(ids)) or len(names) != len(set(names))
                or not set(ids).issubset(required)
                or any(not _NAME.fullmatch(n) for n in names)
                or any(not item["correspondence"].strip() for item in mapping)):
            raise ValueError("Lean mapping must have unique valid theorem names and required Claim IDs")
        if value["status"] == "candidate" and (
                set(ids) != required or not value["source"].strip() or value["limitations"]):
            raise ValueError("Candidate must cover every required Claim without unresolved limitations")
        if value["status"] == "incomplete" and not value["limitations"]:
            raise ValueError("Incomplete formalization must explain remaining obligations")
    elif len(value["checked_claim_ids"]) != len(set(value["checked_claim_ids"])):
        # Provider output schemas do not support uniqueItems; enforce the same
        # gate locally for both passing and failing correspondence reviews.
        raise ValueError("Correspondence review requires unique Claim IDs")
    elif value["verdict"] == "pass" and (
            set(value["checked_claim_ids"]) != required or value["findings"]):
        raise ValueError("Correspondence pass requires complete Claim coverage and no findings")
    elif not set(value["checked_claim_ids"]).issubset(required):
        raise ValueError("Correspondence review references unknown Claim IDs")


def _settings(config):
    selected = {"lean_project": str(config.get("lean_project") or ""),
        "lake_bin": str(config.get("lake_bin") or "lake"),
        "max_compile_attempts": config.get("max_compile_attempts", 3),
        "compile_timeout_seconds": config.get("compile_timeout_seconds", 120),
        "timeout_seconds": config.get("timeout_seconds", 1800)}
    for key in ("compile_timeout_seconds", "timeout_seconds"):
        value = selected[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(key + " must be finite and positive")
    if type(selected["max_compile_attempts"]) is not int or selected["max_compile_attempts"] <= 0:
        raise ValueError("max_compile_attempts must be a positive integer")
    return selected


def _template(path, root):
    template = Path(path)
    if not path or not template.is_absolute() or not (template / "lean-toolchain").is_file():
        raise FileNotFoundError("Configure lean_project with an absolute provisioned Lean project path")
    template = template.resolve()
    if template == root or template.is_relative_to(root) or root.is_relative_to(template):
        raise ValueError("Lean template and Agent work directory must be separate")
    for item in template.rglob("*"):
        if item.is_symlink() or (hasattr(item, "is_junction") and item.is_junction()):
            raise ValueError("Lean template must contain ordinary local files without links")
    return template


def run(package: dict, work_dir: Path, config: dict, model) -> dict:
    """Run a bounded independent Agent and preserve every candidate and receipt.

    model.invoke(stage, work_dir, prompt, context, schema, timeout_seconds) returns
    JSON. Its deterministic call directories must reconcile completed/uncertain
    native calls before any relaunch. Completed Agent results are idempotent;
    another package or configuration requires another work directory.
    """
    _validate_package(package)
    # Isolate the frozen package from caller/model mutation.
    package = json.loads(json_bytes(package))
    settings = _settings(config)
    root = Path(work_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    lock = root / ".agent.lock"
    try:
        with lock.open("x", encoding="utf-8") as stream:
            stream.write("Independent Lean Agent active; reconcile before removing this lock.\n")
    except FileExistsError:
        return {"status": "blocked", "proof_sha256": package["proof_sha256"],
                "diagnostics": ["Lean Agent lock exists; reconcile the previous process before retrying"]}
    try:
        return _run_package(package, root, settings, model)
    finally:
        lock.unlink(missing_ok=True)


def _run_package(package, root, settings, model):
    identity = {"package_sha256": _digest(package), "config_sha256": _digest(settings)}
    state_path, result_path = root / "state.json", root / "result.json"
    if state_path.is_file():
        state = _load(state_path)
        if any(state.get(k) != v for k, v in identity.items()):
            raise ValueError("Lean Agent work directory is bound to another package or configuration")
        if (type(state.get("evidence_version")) is not int or state["evidence_version"] != EVIDENCE_VERSION
                or not isinstance(state.get("artifact_sha256"), dict)):
            raise ValueError("Legacy Lean cache has no evidence receipts; rerun Lean in a new output directory")
        if result_path.is_file():
            result = _load(result_path)
            if (not state.get("result_sha256") or _digest(result) != state["result_sha256"]
                    or result.get("status") != state.get("status")):
                raise ValueError("Saved Lean result changed or lacks its receipt; use a new output directory")
            validate_lean_result(package, result, require_passed=False)
            return result
    else:
        if any(p.name != ".agent.lock" for p in root.iterdir()):
            raise ValueError("Lean workspace has orphaned artifacts; rerun Lean in a new output directory")
        state = {**identity, "deadline_unix": time.time() + settings["timeout_seconds"],
                 "attempts_started": 0, "status": "running", "evidence_version": EVIDENCE_VERSION,
                 "artifact_sha256": {}, "review_inputs": {}}
        _write(root / "package.json", package)
        _write(root / "config.json", settings)
        _write(state_path, state)
    report = {"status": "incomplete", "evidence_version": EVIDENCE_VERSION,
        "package_sha256": identity["package_sha256"], "proof_sha256": package["proof_sha256"],
        "required_claim_ids": package["required_claim_ids"], "diagnostics": [],
        "attempts": [], "mapping": [], "source": "", "compiler": None,
        "semantic_review": None, "semantic_review_binding": None}

    def load_artifact(path):
        value = _load(path)
        if state["artifact_sha256"].get(path.relative_to(root).as_posix()) != _digest(value):
            raise ValueError("Cached Lean artifact changed or lacks its receipt: " + path.name
                             + "; rerun Lean in a new output directory")
        return value

    def save_artifact(path, value):
        _write(path, value)
        state["artifact_sha256"][path.relative_to(root).as_posix()] = _digest(value)
        _write(state_path, state)

    def finish(status, reason=None):
        report["status"] = status
        if reason:
            report["diagnostics"].append(reason)
        validate_lean_result(package, report, require_passed=False)
        _write(result_path, report)
        _write(state_path, {**state, "status": status, "result_sha256": _digest(report)})
        return report

    def remaining():
        seconds = state["deadline_unix"] - time.time()
        if seconds <= 0:
            raise TimeoutError("Lean Agent time allowance exhausted")
        return seconds

    try:
        template = _template(settings["lean_project"], root)
        feedback = None
        for number in range(1, settings["max_compile_attempts"] + 1):
            remaining()
            folder = root / "attempts" / f"A{number:04d}"
            folder.mkdir(parents=True, exist_ok=True)
            state["attempts_started"] = max(number, state["attempts_started"])
            _write(state_path, state)
            entry = {"number": number, "directory": str(folder)}
            report["attempts"].append(entry)
            candidate_path = folder / "candidate.json"
            if candidate_path.is_file():
                candidate = load_artifact(candidate_path)
            else:
                ctx = {**package, "attempt": number, "max_compile_attempts": settings["max_compile_attempts"],
                       "lean_project": str(template), "previous_feedback": feedback}
                candidate = model.invoke("lean-check", folder / "generate", _GENERATE, ctx,
                                         SCHEMAS["lean-check"], remaining())
                save_artifact(candidate_path, candidate)
            try:
                _validate_response("lean-check", candidate, package)
            except (ValueError, jsonschema.ValidationError) as exc:
                feedback = {"status": "invalid_response", "diagnostics": [str(exc)]}
                entry["feedback"] = feedback
                _write(folder / "feedback.json", feedback)
                continue
            report.update(source=candidate["source"], mapping=candidate["mapping"])
            if candidate["status"] == "incomplete":
                return finish("incomplete", "; ".join(candidate["limitations"]))
            compiler_path = folder / "compiler.json"
            if compiler_path.is_file():
                build = load_artifact(compiler_path)
            else:
                target = folder / "project"
                if target.exists():
                    return finish("blocked", "Interrupted compiler attempt requires reconciliation: " + str(target))
                shutil.copytree(template, target, ignore=shutil.ignore_patterns(
                    ".git", ".colombo-lean-check", "Main.lean", "Main.olean", "Audit.lean"))
                atomic_write(target / "Main.lean", candidate["source"].encode("utf-8"))
                build = verify_lean(target, [m["declaration"] for m in candidate["mapping"]],
                    timeout_seconds=min(settings["compile_timeout_seconds"], remaining()),
                    lake_bin=settings["lake_bin"])
                save_artifact(compiler_path, build)
            report["compiler"] = build
            entry["compiler_status"] = build.get("status")
            if build.get("status") == "blocked":
                return finish("blocked", "; ".join(build.get("diagnostics", [])))
            if build.get("status") != "passed":
                feedback = {"candidate": candidate, "compiler": build}
                _write(folder / "feedback.json", feedback)
                continue
            validate_compiler_evidence(candidate["source"],
                [m["declaration"] for m in candidate["mapping"]], build)
            review_path = folder / "review.json"
            review_context = {**package, "candidate": candidate, "compiler": build}
            review_key = review_path.relative_to(root).as_posix()
            expected_input = _digest(review_context)
            if review_path.is_file():
                if state.get("review_inputs", {}).get(review_key) != expected_input:
                    return finish("failed", "Cached correspondence review belongs to different evidence; "
                                  "rerun Lean in a new output directory")
                review = load_artifact(review_path)
            else:
                state.setdefault("review_inputs", {})[review_key] = expected_input
                _write(state_path, state)
                review = model.invoke("lean-review", folder / "semantic-review", _REVIEW,
                    review_context,
                    SCHEMAS["lean-review"], remaining())
                save_artifact(review_path, review)
            report["semantic_review"] = review
            try:
                _validate_response("lean-review", review, package)
            except (ValueError, jsonschema.ValidationError) as exc:
                feedback = {"candidate": candidate, "semantic_review": review, "diagnostics": [str(exc)]}
                entry["feedback"] = {"status": "invalid_review", "diagnostics": [str(exc)]}
                _write(folder / "feedback.json", feedback)
                continue
            entry["semantic_verdict"] = review["verdict"]
            if review["verdict"] == "pass":
                report["semantic_review_binding"] = review_binding(
                    package, candidate["source"], candidate["mapping"], build, review)
                remaining()
                return finish("passed")
            feedback = {"candidate": candidate, "compiler": build, "semantic_review": review}
            _write(folder / "feedback.json", feedback)
        return finish("failed", "Formalization attempt allowance exhausted without a full Lean Check pass")
    except TimeoutError as exc:
        return finish("incomplete", str(exc))
    except (OSError, RuntimeError) as exc:
        return finish("blocked", str(exc))
    except (ValueError, jsonschema.ValidationError) as exc:
        return finish("failed", str(exc))
