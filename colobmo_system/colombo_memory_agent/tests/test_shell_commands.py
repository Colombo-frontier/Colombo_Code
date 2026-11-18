"""Generated read-only query commands must run in the host platform's shell."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(PACKAGE.parent / "src"),
               str(PACKAGE / "runtime")]
from colombo_memory_agent import workflow as workflow_module
from colombo_memory_agent.store import WriterStore
from colombo_memory_agent.workflow import Workflow


class QueryShellCommandTests(unittest.TestCase):
    def test_posix_command_preserves_argument_boundaries(self):
        arguments = ["/path with space/python", "query", "apostrophe's", "$(not-executed)"]
        with patch.object(workflow_module.os, "name", "posix"):
            command = workflow_module._shell_command(arguments)
        self.assertEqual(shlex.split(command), arguments)

    @unittest.skipUnless(os.name == "nt", "PowerShell integration is Windows-specific")
    def test_powershell_preserves_literal_arguments(self):
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if shell is None:
            self.skipTest("PowerShell is unavailable")
        values = ["space in value", "apostrophe's", "$(throw 'must not execute')", "ampersand & semicolon ;"]
        arguments = [sys.executable, "-c", "import json,sys; print(json.dumps(sys.argv[1:]))", *values]
        result = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command",
                                 workflow_module._shell_command(arguments)],
                                capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), values)

    @unittest.skipUnless(os.name == "nt", "PowerShell integration is Windows-specific")
    def test_generated_role_query_runs_read_only_in_powershell(self):
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if shell is None:
            self.skipTest("PowerShell is unavailable")
        with tempfile.TemporaryDirectory(prefix="memory shell ") as temporary:
            root = Path(temporary)
            store = WriterStore(root / "memory's & records")
            store.initialize()
            before = {p.relative_to(root).as_posix(): p.read_bytes()
                      for p in root.rglob("*") if p.is_file()}
            request = root / "query request.json"
            request.write_text(json.dumps({"mode": "overview"}), encoding="utf-8")
            workflow = Workflow(store, None, PACKAGE, jobs_root=root / "jobs")
            prompt = workflow._role_prompt("curator", {}, root / "job", "")
            line = next(line for line in prompt.splitlines() if line.startswith("Use the read-only query command: "))
            command = line.removeprefix("Use the read-only query command: ").removesuffix(" '<JSON request>'.")
            command += " '@" + str(request).replace("'", "''") + "'"
            result = subprocess.run([shell, "-NoProfile", "-NonInteractive", "-Command", command],
                                    capture_output=True, text=True, encoding="utf-8", timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(sum(json.loads(result.stdout)["counts"].values()), 0)
            after = {p.relative_to(root).as_posix(): p.read_bytes()
                     for p in root.rglob("*") if p.is_file() and p != request}
            self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
