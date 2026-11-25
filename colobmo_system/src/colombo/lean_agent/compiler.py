"""Compile a provisioned Lean project and audit the named declarations.

This gate establishes kernel/axiom evidence, not correspondence to an informal
ProofDraft. The caller must review that correspondence independently. Dependencies
and the Lean executable are trusted, provisioned inputs, never model downloads.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import time
import tomllib
import uuid

from colombo.shared.file_io import Path, atomic_write, json_bytes
from colombo.shared.process_control import managed_popen, terminate_tree


ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
_NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9']*(?:\.[A-Za-z_][A-Za-z_0-9']*)*")
_REV = re.compile(r"[0-9a-f]{40}")
_TOOLCHAIN = re.compile(r"leanprover/lean4:v(4\.\d+\.\d+(?:-rc\d+)?)")
_MATHLIB = {"https://github.com/leanprover-community/mathlib4",
            "https://github.com/leanprover-community/mathlib4.git"}
_FORBIDDEN = re.compile(
    r"\b(?:sorry|sorryAx|admit|axiom|unsafe|extern|implemented_by|"
    r"macro|macro_rules|syntax|elab|elab_rules|initialize|builtin_initialize|"
    r"run_tac|run_elab|run_meta|native_decide|attribute|register_option|"
    r"declare_syntax_cat|notation|infix|infixl|infixr|prefix|postfix)\b|#|@\[")


def _code(text):
    """Remove nested Lean comments and string contents, preserving token spacing."""
    out, i, depth = [], 0, 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            out.append("  ")
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            out.append("  ")
            i += 2
        elif depth:
            out.append("\n" if text[i] == "\n" else " ")
            i += 1
        elif text.startswith("--", i):
            end = text.find("\n", i)
            i = len(text) if end == -1 else end
            out.append(" ")
        elif text[i] == '"':
            out.append('"')
            i += 1
            while i < len(text) and text[i] != '"':
                i += 2 if text[i] == "\\" else 1
            if i >= len(text):
                raise ValueError("Unterminated Lean string")
            out.append('"')
            i += 1
        else:
            out.append(text[i])
            i += 1
    if depth:
        raise ValueError("Unterminated Lean comment")
    return "".join(out)


def _source_policy(source):
    code = _code(source)
    match = _FORBIDDEN.search(code)
    if match:
        raise ValueError("Unsupported generated Lean token: " + match.group())
    # Resource limits may be raised; options that alter checking may not.
    code = re.sub(r"(?m)^\s*set_option (?:maxRecDepth|maxHeartbeats) [0-9]+\s*$", "", code)
    if re.search(r"\bset_option\b", code):
        raise ValueError("Only maxRecDepth/maxHeartbeats options are supported")
    imports = re.findall(r"(?m)^\s*(?:public\s+)?import\s+([^\n]+)", code)
    for line in imports:
        if not all(re.fullmatch(r"(?:Mathlib|Init|Lean)(?:\.[A-Za-z_0-9]+)*", name)
                   for name in line.split()):
            raise ValueError("Generated source may import only provisioned Mathlib, Init or Lean")
    without_imports = re.sub(r"(?m)^\s*(?:public\s+)?import\s+[^\n]+", "", code)
    if re.search(r"\bimport\b", without_imports):
        raise ValueError("Unsupported import syntax")
    return any(name.startswith("Mathlib") for line in imports for name in line.split())


def _project_inputs(root):
    required = ["Main.lean", "lean-toolchain"]
    configs = [name for name in ("lakefile.toml", "lakefile.lean") if (root / name).is_file()]
    if len(configs) != 1:
        raise ValueError("Provide exactly one declarative lakefile.toml or lakefile.lean")
    required += configs
    if (root / "lake-manifest.json").is_file():
        required.append("lake-manifest.json")
    contents = {}
    for name in required:
        path = root / name
        if path.is_symlink() or not path.is_file() or path.resolve().parent != root:
            raise ValueError("Missing or nonlocal project input: " + name)
        contents[name] = path.read_bytes()
    toolchain = contents["lean-toolchain"].decode("utf-8-sig").strip()
    match = _TOOLCHAIN.fullmatch(toolchain)
    if not match:
        raise ValueError("lean-toolchain must pin a stable Lean 4 release or release candidate")
    uses_mathlib = _source_policy(contents["Main.lean"].decode("utf-8-sig"))
    if configs[0] == "lakefile.toml":
        config = tomllib.loads(contents[configs[0]].decode("utf-8-sig"))
        if set(config) - {"name", "version", "defaultTargets", "lean_lib", "require"}:
            raise ValueError("Unsupported Lake configuration; use a minimal declarative project")
        if not isinstance(config.get("name"), str) or not _NAME.fullmatch(config["name"]):
            raise ValueError("Invalid Lake package name")
        for lib in config.get("lean_lib", []):
            if not isinstance(lib, dict) or set(lib) != {"name"} or not _NAME.fullmatch(str(lib["name"])):
                raise ValueError("Lean libraries may specify only their name")
        dependencies = config.get("require", [])
        if not isinstance(dependencies, list) or len(dependencies) > 1:
            raise ValueError("Only the pinned mathlib dependency is supported")
        for dep in dependencies:
            if (not isinstance(dep, dict) or set(dep) != {"name", "git", "rev"}
                    or dep["name"] != "mathlib" or dep["git"] not in _MATHLIB
                    or not _REV.fullmatch(str(dep["rev"]))):
                raise ValueError("mathlib must use its official repository and a full commit hash")
    else:
        # Lake's Lean format is executable. Accept only this small declarative
        # grammar, not arbitrary code from a generated package configuration.
        config = contents[configs[0]].decode("utf-8-sig")
        grammar = (r'\s*import Lake\s+open Lake DSL\s+package ([A-Za-z_][A-Za-z_0-9]*)'
                   r'(?:\s+where)?\s*(?:require mathlib from git "([^"]+)" @ "([^"]+)"\s*)?'
                   r'(?:lean_lib [A-Za-z_][A-Za-z_0-9]*(?:\s+where)?\s*)?')
        parsed = re.fullmatch(grammar, config)
        if not parsed or (parsed[2] and (parsed[2] not in _MATHLIB or not _REV.fullmatch(parsed[3]))):
            raise ValueError("Unsupported lakefile.lean; use a minimal declarative lakefile.toml")
        dependencies = [{"rev": parsed[3]}] if parsed[2] else []
    if uses_mathlib and not dependencies:
        raise ValueError("Mathlib imports require a pinned mathlib dependency")
    if dependencies:
        if "lake-manifest.json" not in contents:
            raise ValueError("Pinned mathlib requires a provisioned lake-manifest.json")
        manifest = json.loads(contents["lake-manifest.json"])
        if not isinstance(manifest, dict):
            raise ValueError("Invalid Lake dependency manifest")
        packages = manifest.get("packages", [])
        if not isinstance(packages, list) or any(not isinstance(p, dict) for p in packages):
            raise ValueError("Invalid Lake dependency packages")
        mathlib = [p for p in packages if p.get("name") == "mathlib"]
        if len(mathlib) != 1 or mathlib[0].get("rev") != dependencies[0]["rev"]:
            raise ValueError("mathlib manifest commit does not match the pinned dependency")
        for package in packages:
            name = package.get("name", "")
            if (not _NAME.fullmatch(name) or package.get("type") != "git"
                    or not _REV.fullmatch(str(package.get("rev", "")))):
                raise ValueError("All provisioned dependencies must have pinned git commits")
            if not (root / ".lake/packages" / name).is_dir():
                raise FileNotFoundError("Dependency is not provisioned: " + name)
    return contents, toolchain, match[1]


def _run(root, logs, label, arguments, deadline):
    stdout, stderr = logs / (label + ".stdout.log"), logs / (label + ".stderr.log")
    result = {"argv": arguments, "returncode": None, "stdout_log": str(stdout),
              "stderr_log": str(stderr), "timed_out": False}
    env = dict(os.environ)
    for key in ("LEAN", "LEAN_SYSROOT", "LAKE_OVERRIDE_LEAN", "LEAN_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = str(root / ".lake/build/lib/lean")
    with stdout.open("wb") as out, stderr.open("wb") as err:
        process = managed_popen(arguments, cwd=str(root), stdout=out, stderr=err,
                                stdin=subprocess.DEVNULL, env=env)
        try:
            result["returncode"] = process.wait(timeout=max(0.001, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            result["timed_out"] = True
        finally:
            result["process_tree_terminated"] = terminate_tree(process, timeout=5)
    # Preserve CRLF exactly: the embedded text and the log-file hashes must bind
    # the same bytes on Windows and Unix. Invalid UTF-8 cannot be reused as a
    # complete textual compiler receipt and causes the enclosing check to fail.
    for name, path in (("stdout", stdout), ("stderr", stderr)):
        raw = path.read_bytes()
        result[name] = raw.decode("utf-8")
        result[name + "_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


def audit_declarations(printout, declarations):
    """Parse actual Lean theorem/axiom output; reused when checking saved evidence."""
    axioms_by_name = {}
    for name in declarations:
        if not re.search(r"(?m)^theorem " + re.escape(name) + r"(?:\.\{[^}\n]*\})?(?=[\s:])", printout):
            raise ValueError("Requested declaration is not a proved theorem: " + name)
        pattern = (r"'" + re.escape(name) + r"' (?:does not depend on any axioms|"
                   r"depends on axioms:\s*\[([^\]]*)\])")
        matches = list(re.finditer(pattern, printout))
        if len(matches) != 1:
            raise ValueError("Missing or ambiguous axiom audit for " + name)
        axioms = [s.strip() for s in (matches[0][1] or "").split(",") if s.strip()]
        unexpected = set(axioms) - ALLOWED_AXIOMS
        if unexpected:
            raise ValueError("Unapproved axioms for " + name + ": " + ", ".join(sorted(unexpected)))
        axioms_by_name[name] = axioms
    return axioms_by_name


def verify_lean(project_dir, declarations: list[str], *, timeout_seconds=120, lake_bin="lake") -> dict:
    """Return passed/failed/blocked with real compiler logs; never certify semantics.

    Use a fresh, exclusive project copy for each candidate. Source policy is a
    conservative supported subset, not an OS sandbox for untrusted Lean plugins.
    Provision the toolchain and dependency cache before invoking this function.
    """
    root = Path(project_dir).resolve()
    report = {"status": "failed", "diagnostics": [], "commands": [], "axioms": {},
              "declarations": declarations, "semantic_correspondence": "not_checked"}
    try:
        if (not isinstance(declarations, list) or not declarations
                or any(not isinstance(n, str) or not _NAME.fullmatch(n) for n in declarations)
                or len(set(declarations)) != len(declarations)):
            raise ValueError("Provide a nonempty list of unique Lean declaration names")
        if (isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (float, int))
                or not math.isfinite(timeout_seconds) or timeout_seconds <= 0):
            raise ValueError("timeout_seconds must be a finite positive number")
        contents, toolchain, version = _project_inputs(root)
        report["toolchain"] = toolchain
        report["source_files"] = {name: hashlib.sha256(data).hexdigest() for name, data in contents.items()}
        report["source_sha256"] = report["source_files"]["Main.lean"]
        report["project_sha256"] = hashlib.sha256(json_bytes(report["source_files"])).hexdigest()
        executable = shutil.which(str(lake_bin))
        if not executable:
            raise FileNotFoundError("Lake executable is not installed: " + str(lake_bin))
        prefix = [executable]
        # Elan's proxy installs missing toolchains implicitly; `elan run` without
        # --install does not. Preserve the lightweight, preprovisioned boundary.
        suffix = ".exe" if Path(executable).suffix.lower() == ".exe" else ""
        elan = Path(executable).with_name("elan" + suffix)
        if elan.is_file():
            prefix = [str(elan), "run", toolchain, "lake"]
        logs = root / ".colombo-lean-check" / uuid.uuid4().hex
        if not logs.resolve().is_relative_to(root):
            raise ValueError("Evidence directory must remain inside the project")
        logs.mkdir(parents=True)
        report["evidence_dir"] = str(logs)
        output = root / ".lake/build/lib/lean/Main.olean"
        if not output.resolve().is_relative_to(root):
            raise ValueError("Compiler output must remain inside the project")
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.is_symlink():
            raise ValueError("Compiler output must not be a symlink")
        output.unlink(missing_ok=True)  # A stale object cannot satisfy this run.
        audit = "import Main\nset_option pp.all true\n" + "".join(
            f"#check {name}\n#print {name}\n#print axioms {name}\n" for name in declarations)
        audit_path = logs / "Audit.lean"
        atomic_write(audit_path, audit.encode("utf-8"))
        report["audit_sha256"] = hashlib.sha256(audit.encode("utf-8")).hexdigest()
        deadline = time.monotonic() + timeout_seconds
        commands = [("version", [*prefix, "env", "lean", "--version"]),
                    ("compile", [*prefix, "env", "lean", "-o", str(output), "Main.lean"]),
                    ("audit", [*prefix, "env", "lean", str(audit_path)])]
        for label, arguments in commands:
            result = _run(root, logs, label, arguments, deadline)
            result["phase"] = label
            report["commands"].append(result)
            if result["timed_out"]:
                raise ValueError("Lean Check timed out during " + label)
            if not result["process_tree_terminated"]:
                raise ValueError("Lean process tree exit is unconfirmed")
            if result["returncode"] != 0:
                raise ValueError("Lean command failed during " + label)
            if label == "version" and not re.search(r"\bversion " + re.escape(version) + r"[, )]", result["stdout"]):
                raise ValueError("Compiler version does not match lean-toolchain")
            if label == "compile" and not output.is_file():
                raise ValueError("Compiler did not produce Main.olean")
        report["compiled_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
        report["declaration_printout"] = report["commands"][-1]["stdout"]
        report["axioms"] = audit_declarations(report["declaration_printout"], declarations)
        if any((root / name).read_bytes() != data for name, data in contents.items()):
            raise ValueError("Project inputs changed during Lean Check")
        report["status"] = "passed"
    except FileNotFoundError as exc:
        report["status"] = "blocked"
        report["diagnostics"].append(str(exc))
    except (ValueError, TypeError, OSError) as exc:
        report["diagnostics"].append(str(exc))
    if report.get("evidence_dir"):
        atomic_write(Path(report["evidence_dir"]) / "report.json", json_bytes(report))
    return report
