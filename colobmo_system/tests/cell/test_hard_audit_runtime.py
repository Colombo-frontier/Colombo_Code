"""Research jobs share root budgets; finite RPC requests do not own audit time."""
from __future__ import annotations

from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import colombo.cell.verifier.local_audit as auditing
from colombo.cell.record_store import Store
import colombo.cell.model_calls as processes
import colombo.cell.settings as settings


ROOT = Path(__file__).resolve().parents[2]


class HardAuditRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".hard-audit-runtime-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ))
        for key in tuple(os.environ):
            if key.startswith("CELL_"):
                os.environ.pop(key)
        os.environ["OPENAI_API_KEY"] = "test-fixture-no-network"
        self.auth = self.root / "empty-auth"
        self.auth.mkdir()
        self.stack.enter_context(patch.object(processes, "ROOT", self.root / "runtime-project"))
        self.stack.enter_context(patch.object(processes, "_user_home", return_value=self.auth))
        self.stack.enter_context(patch.object(processes, "_user_settings", return_value={}))

    def prepare(self, selected, role):
        work = self.root / role
        work.mkdir(exist_ok=True)
        home = processes._prepare_home(work, role, None, False, {}, settings=selected)
        config = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
        snapshot = json.loads((home / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot, selected)
        self.assertFalse((home / "auth.json").exists())
        self.assertNotIn("test-fixture-no-network", (home / "config.toml").read_text())
        return config

    def test_transport_and_research_time_are_separate_policies(self):
        for profile in ("standard", "hard"):
            selected, _ = settings.load_defaults(profile=profile)
            self.assertEqual(selected["agents"]["audit_timeout_seconds"], "unlimited")
            for role in ("prover", "subcell", "verifier"):
                config = self.prepare(selected, role)
                self.assertEqual(config["mcp_servers"]["research"]["tool_timeout_sec"],
                                 selected["runtime"]["mcp_tool_timeout_seconds"])
                self.assertEqual(selected["agents"][f"{role}_timeout_seconds"], "unlimited")

    def test_audit_inherits_policy_and_returns_certified_result(self):
        for profile, expected in (("standard", "unlimited"), ("hard", "unlimited")):
            with self.subTest(profile=profile):
                selected, _ = settings.load_defaults(profile=profile)
                work = self.root / ("audit-task-" + profile)
                work.mkdir()
                (work / "run.json").write_text(json.dumps({"settings": selected}), encoding="utf-8")
                (work / "problem.md").write_text("Prove x = x for all real x.", encoding="utf-8")
                store = Store(work / "memory")
                candidate = store.archive("arguments", {
                    "statement": "For every real x, x = x.",
                    "proof": "Equality is reflexive.", "status": "candidate"})
                captured = []

                def local_auditor(prompt, directory, output, **kwargs):
                    captured.append(kwargs)
                    # Local audits have no MCP of their own: this is the inner
                    # model process, nested beneath the caller's tool timeout.
                    config = self.prepare(kwargs["settings"], kwargs["role"])
                    self.assertNotIn("mcp_servers", config)
                    return {"returncode": 0, "text": json.dumps({
                        "verdict": "pass", "summary": "Reflexivity establishes the claim.",
                        "findings": [], "properties": []})}

                with patch.object(auditing, "run_agent", side_effect=local_auditor):
                    result = auditing.audit(work, "arguments", candidate["id"], candidate["revision"])
                self.assertEqual(len(captured), 1)
                self.assertEqual(captured[0]["role"], "audit")
                self.assertEqual(captured[0]["timeout"], expected)
                self.assertEqual(result["review"]["payload"]["verdict"], "pass")
                self.assertEqual(result["record"]["payload"]["status"], "proved")

    def test_transport_changes_are_owned_by_outer_config(self):
        selected, _ = settings.load_defaults(profile="standard")
        with self.assertRaisesRegex(ValueError, "outer config"):
            settings.reject_budget_overrides({"runtime": {"mcp_tool_timeout_seconds": 444}})
        self.assertGreater(selected["runtime"]["mcp_tool_timeout_seconds"], 0)

    def test_direct_budget_overrides_are_rejected(self):
        hard, _ = settings.load_defaults(profile="hard")
        with self.assertRaisesRegex(ValueError, "config.toml"):
            settings.apply_overrides(hard, timeout=90)
        self.assertEqual(hard["agents"]["audit_timeout_seconds"], "unlimited")

    def test_hard_local_audit_can_finish_after_the_old_transport_cutoff(self):
        selected, _ = settings.load_defaults(profile="hard")
        selected["runtime"]["process_poll_seconds"] = 100
        work = self.root / "long-local-audit"
        output = work / "response.txt"
        clock = [0.0]

        class ModelProcess:
            stdin = io.StringIO()
            returncode = None

            def poll(self):
                if self.returncode is None and clock[0] >= 800:
                    output.write_text("Saved audit result", encoding="utf-8")
                    self.returncode = 0
                return self.returncode

        def advance(seconds):
            clock[0] += seconds

        with patch.object(processes.time, "monotonic", side_effect=lambda: clock[0]), \
                patch.object(processes.time, "time", side_effect=lambda: 1000 + clock[0]), \
                patch.object(processes.time, "sleep", side_effect=advance), \
                patch.object(processes, "find_codex", return_value="disabled-test-executable"), \
                patch.object(processes.subprocess, "Popen", return_value=ModelProcess()), \
                patch.object(processes, "_terminate_tree") as terminate:
            result = processes.run_agent("Check the supplied local proof.", work, output,
                                         role="audit", settings=selected)
        self.assertEqual(result["elapsed_seconds"], 800)
        self.assertEqual(result["returncode"], 0)
        terminate.assert_not_called()
        state_path = next((work / "runtime" / "processes").glob("*.json"))
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertIsNone(state["total_seconds"])
        self.assertIsNone(state["work_seconds"])
        self.assertFalse(state["time_limit_enabled"])


if __name__ == "__main__":
    unittest.main()
