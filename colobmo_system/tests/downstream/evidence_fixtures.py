"""Complete, explicitly simulated compiler reports for offline boundary tests."""
import hashlib

from colombo.shared.file_io import json_bytes


def compiler_fixture(source, declarations):
    def sha(text):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    printout = "".join(f"theorem {name} : True := True.intro\n"
                       f"'{name}' does not depend on any axioms\n" for name in declarations)
    audit = "import Main\nset_option pp.all true\n" + "".join(
        f"#check {name}\n#print {name}\n#print axioms {name}\n" for name in declarations)
    files = {"Main.lean": sha(source), "lean-toolchain": sha("leanprover/lean4:v4.19.0\n"),
             "lakefile.toml": sha('name = "formalization"\n')}
    commands = []
    for phase, args, stdout in [
            ("version", ["--version"], "Lean (version 4.19.0, release)\n"),
            ("compile", ["-o", "/fixture/Main.olean", "Main.lean"], ""),
            ("audit", ["/fixture/Audit.lean"], printout)]:
        commands.append({"phase": phase, "argv": ["lake", "env", "lean", *args],
                         "returncode": 0, "timed_out": False, "process_tree_terminated": True,
                         "stdout": stdout, "stderr": "", "stdout_sha256": sha(stdout),
                         "stderr_sha256": sha("")})
    return {"status": "passed", "diagnostics": [], "semantic_correspondence": "not_checked",
            "source_sha256": files["Main.lean"], "source_files": files,
            "project_sha256": hashlib.sha256(json_bytes(files)).hexdigest(),
            "toolchain": "leanprover/lean4:v4.19.0", "compiled_sha256": sha("simulated object"),
            "audit_sha256": sha(audit), "commands": commands, "declarations": list(declarations),
            "axioms": {name: [] for name in declarations}, "declaration_printout": printout}
