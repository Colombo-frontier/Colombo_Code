"""The embedded Cell resolves the same outer, difference-only profiles."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import colombo.cell.settings as settings

PROJECT=Path(__file__).resolve().parents[2]

class ProfileTests(unittest.TestCase):
    def setUp(self):
        env=patch.dict(os.environ);env.start();self.addCleanup(env.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_"):os.environ.pop(key)
        temporary_root=PROJECT/"validation/tmp";temporary_root.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=temporary_root);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.source=(PROJECT/"config.toml").read_text(encoding="utf-8-sig")

    def select(self,profile):
        path=self.root/"config.toml"
        path.write_text(self.source.replace('profile = "hard"',f'profile = "{profile}"',1),encoding="utf-8")
        return path

    def test_hard_is_resolved_from_outer_file(self):
        effective,profile=settings.load_defaults()
        self.assertEqual(profile,"hard")
        self.assertEqual(effective["model"]["reasoning_effort"],"ultra")
        self.assertEqual(effective["experiment"]["reasoning_effort"],"max")
        self.assertEqual(effective["agents"]["prover_max_rounds"],15)
        self.assertEqual(effective["parallel"]["max_subcells"],8)
        self.assertFalse((PROJECT/"agents/cell/config.toml").exists())

    def test_standard_has_no_research_deadline(self):
        with patch.object(settings,"CONFIG_PATH",self.select("standard")):
            effective,profile=settings.load_defaults()
            policy=settings.load_policy()
        self.assertEqual(profile,"standard")
        self.assertNotIn("budget",policy)
        self.assertEqual(policy["limits"]["max_dispatches_per_wave"],3)
        self.assertEqual(effective["agents"]["prover_max_rounds"],3)
        self.assertEqual(effective["agents"]["audit_timeout_seconds"],"unlimited")
        self.assertEqual(effective["model"]["reasoning_effort"],"medium")
        self.assertEqual(effective["experiment"]["reasoning_effort"],"medium")

    def test_common_fields_apply_to_both_profiles(self):
        for profile in ("standard","hard"):
            path=self.select(profile)
            path.write_text(path.read_text(encoding="utf-8").replace('read_timeout_seconds = 25','read_timeout_seconds = 77'),encoding="utf-8")
            with patch.object(settings,"CONFIG_PATH",path):effective,_=settings.load_defaults()
            self.assertEqual(effective["network"]["read_timeout_seconds"],77)

    def test_environment_cannot_override_budget(self):
        with patch.dict(os.environ,{"CELL_AGENT_TIMEOUT":"1","CELL_REASONING_EFFORT":"high"}):
            effective,_=settings.load_defaults()
        self.assertEqual(effective["agents"]["audit_timeout_seconds"],"unlimited")
        self.assertEqual(effective["model"]["reasoning_effort"],"high")

    def test_invalid_profile_is_rejected(self):
        with patch.object(settings,"CONFIG_PATH",self.select("typo")),self.assertRaisesRegex(ValueError,"Unknown profile"):
            settings.load_defaults()

    def test_budget_fields_reject_runtime_overrides(self):
        effective,_=settings.load_defaults()
        for section,values in effective.items():
            for key,value in values.items():
                if key in settings._NON_BUDGET_OVERRIDES.get(section,set()):continue
                with self.subTest(section=section,key=key),self.assertRaisesRegex(ValueError,"outer config"):
                    settings.reject_budget_overrides({section:{key:value}})

if __name__=="__main__":unittest.main()
