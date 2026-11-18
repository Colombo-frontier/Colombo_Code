"""The outer file and its difference-only preset are the sole budget authority."""
from __future__ import annotations
from copy import deepcopy
import json
import os
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest.mock import patch

from colombo.configuration import PROJECT_ROOT, load_config
from colombo.cell import settings
from colombo.configuration import resolve_document


def toml_document(value):
    lines=[]
    def visit(node,path=""):
        if path: lines.append("["+path+"]")
        for key,item in node.items():
            if not isinstance(item,dict):
                literal=str(item).lower() if isinstance(item,bool) else json.dumps(item,ensure_ascii=False)
                lines.append(key+" = "+literal)
        lines.append("")
        for key,item in node.items():
            if isinstance(item,dict):visit(item,path+"."+key if path else key)
    visit(value)
    return "\n".join(lines)


class UnifiedConfigurationTests(unittest.TestCase):
    def setUp(self):
        env=patch.dict(os.environ);env.start();self.addCleanup(env.stop)
        for key in tuple(os.environ):
            if key.startswith("CELL_") or key.startswith("COLOMBO_BUDGET"):
                os.environ.pop(key)
        temporary_root=PROJECT_ROOT/"validation/tmp"
        temporary_root.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=temporary_root);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.document=tomllib.loads((PROJECT_ROOT/"config.toml").read_text(encoding="utf-8-sig"))

    def config_file(self,document=None):
        path=self.root/"config.toml"
        path.write_text(toml_document(document or self.document),encoding="utf-8")
        return path

    def test_one_mode_selector_and_no_duplicate_cell_config(self):
        self.assertEqual(self.document["profile"],"hard")
        self.assertNotIn("default_profile",self.document["cell"])
        self.assertNotIn("profiles",self.document["cell"])
        self.assertNotIn("standard",self.document["profiles"])
        self.assertFalse((PROJECT_ROOT/"agents/cell/config.toml").exists())
        self.assertNotIn("timeout_seconds",self.document["brain"])
        self.assertNotIn("run_timeout_seconds",self.document["cell"])

    def test_hard_has_no_research_deadline_and_keeps_cell_local_limits(self):
        config=load_config()
        self.assertEqual(config["profile"],"hard")
        self.assertNotIn("budget", config)
        self.assertEqual(config["integration"]["timeout_seconds"], 7200)
        for role in ("brain","verifier","audit"):
            self.assertEqual(config[role]["timeout_seconds"],"unlimited")
        self.assertEqual(config["cell"]["run_timeout_seconds"],"unlimited")
        for key in ("prover","subcell","verifier","report_check","audit"):
            self.assertEqual(config["cell"]["settings"]["agents"][key+"_timeout_seconds"],"unlimited")
        self.assertEqual(config["cell"]["settings"]["agents"]["prover_max_rounds"],15)
        self.assertEqual(config["cell"]["settings"]["runtime"]["mcp_tool_timeout_seconds"],120)

    def test_hard_expands_outer_allocation_and_pins_separate_model_efforts(self):
        config=load_config()
        self.assertEqual(config["limits"], {"max_rounds":8,"max_dispatches_per_wave":6,
            "max_parallel_cells":4})
        for role in ("brain","verifier","audit"):
            self.assertEqual(config[role]["model"],"gpt-6-astra")
            self.assertEqual(config[role]["reasoning_effort"],"ultra")
        cell=config["cell"]["settings"]
        self.assertEqual(cell["model"],{"name":"gpt-6-astra","reasoning_effort":"ultra"})
        self.assertEqual(cell["experiment"]["reasoning_effort"],"max")
        self.assertEqual(cell["experiment"]["max_runs"],12)
        self.assertEqual(cell["agents"]["verifier_max_rounds"],20)
        self.assertEqual(cell["agents"]["report_check_max_attempts"],4)
        self.assertEqual(cell["challenge"]["max_rounds"],4)
        self.assertEqual(cell["challenge"]["max_check_attempts"],4)
        self.assertTrue(cell["network"]["subcell_search_enabled"])
        self.assertEqual(cell["parallel"]["max_subcells"],8)
        self.assertEqual(cell["parallel"]["max_depth"],2)

    def test_research_mode_is_fixed_to_oracle_complexity(self):
        self.assertEqual(load_config()["research_mode"], "oracle_complexity")
        self.document.pop("research_mode")
        self.assertEqual(load_config(self.config_file())["research_mode"], "oracle_complexity")
        for invalid in ("auto", "generic", "upper_bound", "optimization", True, None):
            self.document["research_mode"] = invalid
            with self.assertRaisesRegex(ValueError, "research_mode"):
                resolve_document(self.document)

    def test_standard_keeps_local_counts_without_root_deadline(self):
        self.document["profile"]="standard"
        config=load_config(self.config_file())
        self.assertNotIn("budget", config)
        self.assertEqual(config["cell"]["settings"]["agents"]["prover_max_rounds"],3)
        self.assertEqual(config["cell"]["settings"]["agents"]["audit_timeout_seconds"],"unlimited")
        self.assertEqual(config["cell"]["settings"]["parallel"]["max_subcells"],4)
        self.assertEqual(config["limits"], {"max_rounds":3,"max_dispatches_per_wave":3,
            "max_parallel_cells":2})
        for role in ("brain","verifier","audit"):
            self.assertEqual(config[role]["model"],"")
            self.assertEqual(config[role]["reasoning_effort"],"")
        cell=config["cell"]["settings"]
        self.assertEqual(cell["model"],{"name":"","reasoning_effort":"medium"})
        self.assertEqual(cell["experiment"]["reasoning_effort"],"medium")
        self.assertEqual(cell["experiment"]["max_runs"],6)
        self.assertFalse(cell["network"]["subcell_search_enabled"])
        self.assertEqual(cell["agents"]["verifier_max_rounds"],3)
        self.assertEqual(cell["agents"]["report_check_max_attempts"],2)
        self.assertEqual(cell["challenge"]["max_rounds"],2)
        self.assertEqual(cell["challenge"]["max_check_attempts"],2)

    def test_presets_only_override_listed_differences(self):
        self.document["cell"]["settings"]["network"]["read_timeout_seconds"]=73
        config=load_config(self.config_file())
        self.assertEqual(config["cell"]["settings"]["network"]["read_timeout_seconds"],73)
        self.assertEqual(config["cell"]["settings"]["model"]["reasoning_effort"],"ultra")
        self.assertEqual(self.document["cell"]["settings"]["model"]["reasoning_effort"],"medium")

    def test_cell_behavior_overrides_do_not_change_experiment_effort(self):
        with patch.dict(os.environ,{"CELL_REASONING_EFFORT":"high"}):
            selected=load_config()["cell"]["settings"]
        self.assertEqual(selected["model"]["reasoning_effort"],"high")
        self.assertEqual(selected["experiment"]["reasoning_effort"],"max")
        changed=settings.merge_settings(selected,{"model":{"reasoning_effort":"low"}})
        self.assertEqual(changed["model"]["reasoning_effort"],"low")
        self.assertEqual(changed["experiment"]["reasoning_effort"],"max")

    def test_current_experiment_effort_requires_explicit_valid_string(self):
        self.document["profile"]="standard"
        for invalid in (None,True,3,""," "):
            with self.subTest(invalid=invalid),self.assertRaises(ValueError):
                document=deepcopy(self.document)
                document["cell"]["settings"]["experiment"]["reasoning_effort"]=invalid
                config=resolve_document(document)
                settings.load_defaults(document=config)
        document=deepcopy(self.document)
        del document["cell"]["settings"]["experiment"]["reasoning_effort"]
        with self.assertRaises(ValueError):
            config=resolve_document(document)
            settings.load_defaults(document=config)

    def test_historical_experiment_effort_uses_saved_cell_effort_not_new_defaults(self):
        selected=load_config()["cell"]["settings"]
        old=deepcopy(selected)
        old["model"]["reasoning_effort"]="high"
        del old["experiment"]["reasoning_effort"]
        with patch("colombo.cell.settings._read_document",side_effect=AssertionError("No live root reload")):
            migrated=settings.migrate_settings(old,defaults=selected)
        self.assertEqual(migrated["experiment"]["reasoning_effort"],"high")
        self.assertNotIn("reasoning_effort",old["experiment"])
        self.assertEqual(selected["experiment"]["reasoning_effort"],"max")
        migrated["model"]["reasoning_effort"]="ultra"
        self.assertEqual(settings.migrate_settings(migrated,defaults=selected)["experiment"]["reasoning_effort"],"high")

    def test_unknown_profile_and_misspelled_preset_paths_are_rejected(self):
        self.document["profile"]="unknown"
        with self.assertRaisesRegex(ValueError,"Unknown profile"):load_config(self.config_file())
        self.document["profile"]="hard"
        self.document["profiles"]["hard"]["limits"]["dispatches_typo"]=10
        with self.assertRaisesRegex(ValueError,"Unknown config key"):load_config(self.config_file())

    def test_no_second_research_time_authority(self):
        self.document["brain"]["timeout_seconds"]=20
        with self.assertRaisesRegex(ValueError,"research time"):load_config(self.config_file())
        self.document["brain"].pop("timeout_seconds")
        self.document["cell"]["settings"]["agents"]["audit_timeout_seconds"]=90
        with self.assertRaisesRegex(ValueError,"derived"):load_config(self.config_file())

    def test_complete_config_is_selected_not_merged(self):
        partial=self.root/"partial.toml";partial.write_text('[budget.research]\ntotal_active_seconds=12\n',encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"complete outer config"):load_config(partial)
        self.document["profile"]="standard"
        self.document["limits"]["max_dispatches_per_wave"]=12
        config=load_config(self.config_file())
        self.assertEqual(config["limits"]["max_dispatches_per_wave"],12)
        self.assertEqual(Path(config["policy_metadata"]["source"]),self.root/"config.toml")

    def test_integration_time_validation_is_shared_by_preview_and_execution(self):
        self.document["profile"]="standard"
        for invalid in (True,False,0,-1,1.5,"300","forever",None):
            with self.subTest(invalid=invalid):
                value=deepcopy(self.document);value["integration"]["timeout_seconds"]=invalid
                with self.assertRaises(ValueError):resolve_document(value)

    def test_budget_environment_override_is_ignored(self):
        baseline=load_config()
        with patch.dict(os.environ,{"CELL_AGENT_TIMEOUT":"1"}):
            self.assertEqual(load_config(),baseline)
            self.assertEqual(settings.load_defaults()[0],baseline["cell"]["settings"])

    def test_legacy_aliases_cannot_override_snapshot_budget(self):
        effective=load_config()["cell"]["settings"]
        (self.root/"run.json").write_text(json.dumps({"settings":effective,"prover_timeout":1,"max_prover_rounds":999}),encoding="utf-8")
        self.assertEqual(settings.get_settings(self.root),effective)

    def test_runtime_budget_overrides_rejected_but_behavior_allowed(self):
        for patch_data in ({"agents":{"prover_max_rounds":99}}, {"experiment":{"memory_limit":"64g"}},
                           {"runtime":{"mcp_tool_timeout_seconds":999}}, {"parallel":{"max_depth":9}}):
            with self.subTest(patch=patch_data),self.assertRaisesRegex(ValueError,"outer config"):
                settings.reject_budget_overrides(patch_data)
        settings.reject_budget_overrides({"model":{"reasoning_effort":"high"},"network":{"prover_search_enabled":False}})
        with self.assertRaisesRegex(ValueError,"CLI overrides"):
            settings.apply_overrides(load_config()["cell"]["settings"],timeout=20)

    def test_policy_adoption_preserves_nonbudget_behavior(self):
        selected=load_config()["cell"]["settings"]
        old=deepcopy(selected);old["agents"]["prover_max_rounds"]=999;old["model"]["name"]="chosen-model"
        old["network"]["prover_search_enabled"]=False
        adopted=settings.apply_budget_policy(old,selected)
        self.assertEqual(adopted["agents"]["prover_max_rounds"],15)
        self.assertEqual(adopted["model"]["name"],"chosen-model")
        self.assertFalse(adopted["network"]["prover_search_enabled"])

    def test_managed_context_replaces_old_stage_budgets_without_live_root_reload(self):
        root_policy=load_config()["cell"]["settings"]
        old=deepcopy(root_policy);old["agents"]["audit_timeout_seconds"]=1000
        old["agents"]["prover_max_rounds"]=99;old["model"]["name"]="local-model"
        del old["challenge"]
        del old["experiment"]
        (self.root/"run.json").write_text(json.dumps({"settings":old,"audit_timeout":1}),encoding="utf-8")
        with patch("colombo.shared.runtime_budget.get_budget_context",return_value={"policy_settings":root_policy}), \
             patch("colombo.cell.settings._read_document",side_effect=AssertionError("No live root reload")):
            adopted=settings.get_settings(self.root)
        self.assertEqual(adopted["agents"]["audit_timeout_seconds"],"unlimited")
        self.assertEqual(adopted["agents"]["prover_max_rounds"],15)
        self.assertEqual(adopted["model"]["name"],"local-model")
        self.assertEqual(adopted["challenge"],root_policy["challenge"])
        self.assertEqual(adopted["experiment"],root_policy["experiment"])

    def test_managed_workspace_without_task_snapshot_uses_frozen_policy(self):
        root_policy=load_config()["cell"]["settings"]
        with patch("colombo.shared.runtime_budget.get_budget_context",return_value={"policy_settings":root_policy}), \
             patch("colombo.cell.settings._read_document",side_effect=AssertionError("No live root reload")):
            self.assertEqual(settings.get_settings(self.root),root_policy)

    def test_old_managed_policy_and_task_migrate_efforts_without_reload_or_mutation(self):
        policy=load_config()["cell"]["settings"]
        policy["model"]["reasoning_effort"]="max"
        policy["agents"]["prover_max_rounds"]=10
        del policy["experiment"]["reasoning_effort"]
        task=deepcopy(policy)
        task["model"]["reasoning_effort"]="high"
        task["agents"]["prover_max_rounds"]=99
        run_path=self.root/"run.json"
        run_path.write_text(json.dumps({"settings":task,"prover_rounds":7,"verifier_rounds":6}),encoding="utf-8")
        saved=run_path.read_bytes()
        context={"policy_settings":policy,"used_seconds":417.0,"revision":"historical"}
        before=deepcopy(context)
        with patch("colombo.shared.runtime_budget.get_budget_context",return_value=context), \
             patch("colombo.cell.settings._read_document",side_effect=AssertionError("No live root reload")):
            adopted=settings.get_settings(self.root)
        self.assertEqual(adopted["model"]["reasoning_effort"],"high")
        self.assertEqual(adopted["experiment"]["reasoning_effort"],"high")
        self.assertEqual(adopted["agents"]["prover_max_rounds"],10)
        self.assertEqual(context,before)
        self.assertEqual(run_path.read_bytes(),saved)
        self.assertNotIn("reasoning_effort",task["experiment"])

    def test_old_managed_policy_without_task_migrates_its_own_pinned_effort(self):
        policy=load_config()["cell"]["settings"]
        policy["model"]["reasoning_effort"]="high"
        del policy["experiment"]["reasoning_effort"]
        before=deepcopy(policy)
        with patch("colombo.shared.runtime_budget.get_budget_context",return_value={"policy_settings":policy}), \
             patch("colombo.cell.settings._read_document",side_effect=AssertionError("No live root reload")):
            adopted=settings.get_settings(self.root)
        self.assertEqual(adopted["experiment"]["reasoning_effort"],"high")
        self.assertEqual(policy,before)

    def test_direct_budget_adoption_migrates_old_inputs_and_preserves_behavior(self):
        policy=load_config()["cell"]["settings"]
        policy["model"]["reasoning_effort"]="max"
        policy["agents"]["prover_max_rounds"]=10
        del policy["experiment"]["reasoning_effort"]
        task=deepcopy(policy)
        task["model"]["reasoning_effort"]="high"
        task["agents"]["prover_max_rounds"]=99
        before=(deepcopy(task),deepcopy(policy))
        with patch("colombo.cell.settings._read_document",side_effect=AssertionError("No live root reload")):
            adopted=settings.apply_budget_policy(task,policy)
        self.assertEqual(adopted["experiment"]["reasoning_effort"],"high")
        self.assertEqual(adopted["agents"]["prover_max_rounds"],10)
        self.assertEqual((task,policy),before)

    def test_policy_revision_changes_when_effective_budget_changes(self):
        self.document["profile"]="standard"
        first=load_config(self.config_file())
        self.document["limits"]["max_dispatches_per_wave"]=5
        second=load_config(self.config_file())
        self.assertNotEqual(first["policy_metadata"]["revision"],second["policy_metadata"]["revision"])
        self.assertEqual(first["cell"]["policy_metadata"],first["policy_metadata"])


if __name__=="__main__":unittest.main()
