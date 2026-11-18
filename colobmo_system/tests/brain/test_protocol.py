"""Single-protocol entry points: no legacy run may launch current model instructions."""
from contextlib import redirect_stderr, redirect_stdout
import copy
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from colombo.brain.model_calls import BackendError
from colombo.system_commands import main
from colombo.configuration import PROJECT_ROOT, load_config
from colombo.brain.research_store import Store
import test_backend as backend_helpers


class CurrentProtocolConfigTests(unittest.TestCase):
    def setUp(self):
        parent = PROJECT_ROOT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="v3-protocol-", dir=parent)
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)

    def test_new_run_config_accepts_only_workflow_three(self):
        self.assertEqual(load_config()["workflow"]["version"], 3)
        original = (PROJECT_ROOT / "config.toml").read_text(encoding="utf-8")
        for literal in ("1", "2", "true", '"3"'):
            with self.subTest(version=literal):
                override = self.folder / "config.toml"
                override.write_text(original.replace("[workflow]\nversion = 3", "[workflow]\nversion = " + literal, 1), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_config(override)

    def test_legacy_status_is_readable_but_resume_never_starts_controller(self):
        for version in (1, 2, None):
            with self.subTest(version=version):
                config = {**load_config(), "research_mode": "generic"}
                if version is None:
                    config.pop("workflow")
                else:
                    config["workflow"]["version"] = version
                store = Store.create(self.folder / str(version), "Historical goal", [], load_config(), [])
                # Historical files remain readable; current creation never emits this config.
                store.set_meta(config=config)
                before = {key: store.get_meta(key) for key in ("phase", "status", "round_no", "config")}
                with redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(main(["status", "--run-dir", str(store.root)]), 0)
                self.assertIn("Historical goal", output.getvalue())
                with patch("colombo.brain.controller.OracleController.run") as run, \
                     redirect_stderr(io.StringIO()) as error:
                    self.assertEqual(main(["resume", "--run-dir", str(store.root)]), 2)
                run.assert_not_called()
                self.assertIn("workflow version 3 only", error.getvalue())
                self.assertEqual(before, {key: store.get_meta(key) for key in before})

    def test_each_current_role_has_only_canonical_protocol(self):
        for role in ("brain", "verifier"):
            with self.subTest(role=role):
                folder = PROJECT_ROOT / "agents/brain" / ("verifier" if role == "verifier" else "")
                names = sorted(p.name for p in folder.glob("protocol*.md"))
                self.assertEqual(names, ["protocol.md"])


class CurrentProtocolBackendTests(unittest.TestCase):
    def setUp(self):
        backend_helpers.BackendTests.setUp(self)

    def test_legacy_brain_and_verifier_are_rejected_before_launch(self):
        original = copy.deepcopy(self.config)
        for version in (1, 2, None):
            for role, stage in (("brain", "plan"), ("brain", "process_results"), ("brain", "integrate"),
                                ("verifier", "verify-progress")):
                with self.subTest(version=version, role=role, stage=stage):
                    self.config.clear()
                    self.config.update(copy.deepcopy(original))
                    if version is None:
                        self.config.pop("workflow")
                    else:
                        self.config["workflow"]["version"] = version
                    with patch("colombo.brain.model_calls.managed_popen") as launch:
                        with self.assertRaisesRegex(BackendError, "workflow version 3 only"):
                            self.backend.invoke(role, stage, self.run_root, "legacy", "Legacy", {})
                    launch.assert_not_called()
                    self.assertFalse((self.run_root / "brain/calls/legacy").exists())

    def test_current_integrate_uses_its_skill_and_committed_receipt(self):
        expected = {"rationale": "Synthetic integration transport receipt"}

        def respond(process, *_):
            work = Path(process.command[process.command.index("-C") + 1])
            self.assertTrue((work / ".agents/skills/integrate/SKILL.md").is_file())
            backend_helpers.BackendTests.write_submission(self, process, expected)

        with backend_helpers.BackendTests.spawn(self, respond) as launch:
            actual = self.backend.invoke("brain", "integrate", self.run_root,
                                         "integrate-current", "Integrate", {})
        self.assertEqual(actual, expected)
        self.assertEqual(launch.call_count, 1)


if __name__ == "__main__":
    unittest.main()
