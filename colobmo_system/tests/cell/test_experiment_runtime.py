"""Hosted execution durability and evidence tests; all HTTP/model calls are fake."""
from __future__ import annotations

from contextlib import ExitStack
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import colombo.shared.experiment_execution as ex
from colombo.cell.record_store import Store as RealStore
from colombo.cell.settings import managed_settings
from colombo.cell.recovery import caller_deadline
from colombo.cell.settings import get_settings
RealClient = ex._Client


class Clock:
    now = 1000.0

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class Memory:
    def __init__(self):
        self.records = {}

    def resolve_record_refs(self, refs):
        return refs

    def write_experiment_result(self, record_id, payload, **kwargs):
        before = self.records.get(record_id)
        revision = before["revision"] + 1 if before else 1
        result = {"id": record_id, "kind": "experiment_result", "revision": revision,
                  "payload": deepcopy(payload)}
        self.records[record_id] = result
        return result


class Remote:
    def __init__(self, root):
        self.root = root
        self.calls = []
        self.files = {}
        self.waiting = False
        self.cancel_unknown = False
        self.submit_unknown = False
        self.fail_download_once = False
        self.script_failed = False
        self.missing_receipt = False
        self.bad_path = False
        self.extra_bytes = 0
        self.deadline = None
        self.response = None
        self.settings_history = []

    def factory(self, key, settings, deadline):
        self.deadline = deadline
        self.settings_history.append(deepcopy(settings))
        return self

    def close(self):
        pass

    def json(self, method, path, body=None):
        self.calls.append((method, path, deepcopy(body)))
        if path == "/containers":
            return {"id": "cntr_one"}
        if method == "DELETE":
            return {"deleted": True}
        if path == "/responses" and method == "POST":
            if self.submit_unknown:
                raise ex._TransportError("connection_interrupted", uncertain=True)
            self.generate(body)
            return {"id": "resp_one", "status": "in_progress"} if self.waiting else self.response
        if path.endswith("/cancel"):
            if self.cancel_unknown:
                raise ex._TransportError("connection_interrupted", uncertain=True)
            self.waiting = False
            return {"id": "resp_one", "status": "cancelled"}
        if path.startswith("/responses/"):
            return {"id": "resp_one", "status": "in_progress"} if self.waiting else self.response
        if "/files" in path:
            data = [{"id": key, "path": value[0]} for key, value in self.files.items()]
            if self.bad_path:
                data.append({"id": "evil", "path": "/mnt/data/../../plan.json"})
            return {"data": data, "has_more": False}
        raise AssertionError((method, path))

    def upload(self, container_id, name, data):
        self.calls.append(("UPLOAD", name, None))
        return {"id": "cfile_input", "path": "/mnt/data/" + name}

    def download(self, container_id, file_id, maximum):
        self.calls.append(("DOWNLOAD", file_id, None))
        if self.fail_download_once:
            self.fail_download_once = False
            raise ex._TransportError("download_interrupted")
        data = self.files[file_id][1]
        if len(data) > maximum:
            raise ex._TransportError("artifact_size_limit")
        return data

    def generate(self, body):
        owned = [path for path in (self.root / "experiments").glob("exp-*/plan.json") if (path.parent / "state.json").is_file()]
        plan = json.loads(owned[-1].read_text())
        prefix = "/mnt/data/cell-" + plan["experiment_id"] + "/"
        values = {"environment.json": ex._json({"python": "3.test", "packages": {"sympy": "test"}}),
                  "stdout.txt": b"answer=0\n", "stderr.txt": b"", "answer.json": b'{"residual":0}'}
        if self.extra_bytes:
            values["large.bin"] = b"0" * self.extra_bytes
        receipt = {key: plan[key] for key in ("experiment_id", "nonce")}
        receipt.update(status="failed" if self.script_failed else "completed",
                       files=[{"name": name, "size": len(data)} for name, data in values.items()])
        if not self.missing_receipt:
            values["execution_receipt.json"] = ex._json(receipt)
        self.files = {f"cfile_{index}": (prefix + name, data) for index, (name, data) in enumerate(values.items())}
        self.response = {"id": "resp_one", "status": "completed", "usage": {"input_tokens": 1},
                         "output": [{"type": "code_interpreter_call", "status": "completed", "code": body["input"],
                                     "outputs": [{"type": "logs", "logs": "Execution receipt created"}]}]}



def execution_context(root, settings, memory):
    return ex.ExperimentContext(
        read_settings=lambda: settings,
        resolve_refs=memory.resolve_record_refs,
        write_result=memory.write_experiment_result,
        restore_settings=lambda snapshot: managed_settings(root, snapshot, partial=True),
        deadline=lambda phase: caller_deadline(root, phase=phase),
    )


class ExperimentRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix=".experiment-", dir=ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.config = get_settings()
        self.config["experiment"]["timeout_seconds"] = 10
        self.config["experiment"]["download_reserve_seconds"] = 2
        self.clock = Clock()
        self.memory = Memory()
        self.remote = Remote(self.root)
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-private-key"}))
        os.environ.pop("CELL_PROCESS_ID", None)
        self.stack.enter_context(patch.object(ex, "_Client", side_effect=self.remote.factory))
        self.stack.enter_context(patch.object(ex.time, "time", self.clock.time))
        # Deadline conversion and elapsed-budget checks share this simulated clock.
        self.stack.enter_context(patch.object(ex.time, "monotonic", self.clock.time))
        self.stack.enter_context(patch.object(ex.time, "sleep", self.clock.sleep))
        self.ref = {"kind": "claims", "id": "claim-a", "revision": 1}

    def run_exp(self, **kwargs):
        args = {"question": "Is the sampled residual zero?", "target_ref": self.ref,
                "code": "print(0)", "request_id": "request-1"}
        args.update(kwargs)
        return ex.run_experiment(self.root, context=execution_context(self.root, self.config, self.memory), **args)

    def resume_exp(self, experiment_id):
        return ex.resume_experiment(self.root, experiment_id,
            context=execution_context(self.root, self.config, self.memory))

    def state(self, receipt):
        return json.loads((self.root / receipt["state_file"]).read_text())

    def post_count(self):
        return sum(method == "POST" and path == "/responses" for method, path, _ in self.remote.calls)

    def test_completed_has_local_artifacts_actual_code_and_environment(self):
        result = self.run_exp()
        self.assertEqual("completed", result["status"])
        state = self.state(result)
        self.assertTrue(state["execution"]["container_deleted"])
        self.assertEqual("3.test", state["execution"]["environment"]["python"])
        self.assertTrue(any(item["path"].endswith("executed_code_0.py") for item in state["artifacts"]))
        for item in state["artifacts"]:
            content = (self.root / item["path"]).read_bytes()
            self.assertEqual(item["size"], len(content))
        self.assertNotIn("proved", json.dumps(self.memory.records))

    def test_experiment_request_uses_own_effort_instead_of_cell_ultra(self):
        self.config["model"]["reasoning_effort"] = "ultra"
        self.config["experiment"]["reasoning_effort"] = "max"
        result = self.run_exp()
        self.assertEqual(result["status"], "completed")
        payload = next(body for method, path, body in self.remote.calls
                       if method == "POST" and path == "/responses")
        self.assertEqual(payload["reasoning"], {"effort": "max"})
        plan = json.loads((self.root / result["plan_file"]).read_text())
        self.assertEqual(plan["settings_snapshot"]["experiment"]["reasoning_effort"], "max")
        self.assertNotIn("model", plan["settings_snapshot"])
        request = self.root / "experiments" / result["experiment_id"] / "transport/request.json"
        self.assertEqual(json.loads(request.read_text())["reasoning"], {"effort": "max"})
        self.assertEqual(self.config["model"]["reasoning_effort"], "ultra")

    def test_managed_resume_keeps_pinned_experiment_effort_and_original_request(self):
        from colombo.shared.runtime_budget import start_budget
        from colombo.cell.settings import load_policy
        self.config["model"]["reasoning_effort"] = "ultra"
        self.config["experiment"]["reasoning_effort"] = "max"
        self.remote.fail_download_once = True
        first = self.run_exp()
        self.assertEqual(first["status"], "download_pending")
        plan_path = self.root / first["plan_file"]
        request_path = plan_path.parent / "transport/request.json"
        plan_bytes, request_bytes = plan_path.read_bytes(), request_path.read_bytes()
        self.config["model"]["reasoning_effort"] = "low"
        self.config["experiment"]["reasoning_effort"] = "low"
        policy = load_policy(profile="hard")
        policy["cell"]["settings"]["experiment"]["reasoning_effort"] = "low"
        start_budget(self.root, policy)
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual(second["status"], "completed")
        self.assertEqual(self.remote.settings_history[-1]["experiment"]["reasoning_effort"], "max")
        self.assertEqual(plan_path.read_bytes(), plan_bytes)
        self.assertEqual(request_path.read_bytes(), request_bytes)
        self.assertEqual(self.post_count(), 1)

    def test_legacy_plan_uses_its_saved_effort_before_merging_current_policy(self):
        from colombo.shared.runtime_budget import start_budget
        from colombo.cell.settings import load_policy
        self.config["model"]["reasoning_effort"] = "high"
        self.config["experiment"]["reasoning_effort"] = "high"
        self.remote.fail_download_once = True
        first = self.run_exp()
        self.assertEqual(first["status"], "download_pending")
        plan_path = self.root / first["plan_file"]
        plan = json.loads(plan_path.read_text())
        # Construct a pre-split fixture whose original request used the pinned
        # Cell effort. Its plan and artifact length must match the old format.
        plan["settings_snapshot"]["experiment"].pop("reasoning_effort")
        plan["settings_snapshot"]["model"] = {"reasoning_effort": "high"}
        ex._save(plan_path, plan)
        state = self.state(first)
        next(item for item in state["artifacts"] if item["path"] == first["plan_file"])["size"] = plan_path.stat().st_size
        ex._save(self.root / first["state_file"], state)
        plan_bytes = plan_path.read_bytes()
        request_path = plan_path.parent / "transport/request.json"
        request_bytes = request_path.read_bytes()
        self.config["model"]["reasoning_effort"] = "ultra"
        self.config["experiment"]["reasoning_effort"] = "low"
        policy = load_policy(profile="hard")
        policy["cell"]["settings"]["experiment"]["reasoning_effort"] = "low"
        start_budget(self.root, policy)
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual(second["status"], "completed")
        self.assertEqual(self.remote.settings_history[-1]["experiment"]["reasoning_effort"], "high")
        self.assertEqual(plan_path.read_bytes(), plan_bytes)
        self.assertEqual(request_path.read_bytes(), request_bytes)
        self.assertEqual(self.post_count(), 1)

    def test_managed_execution_shares_root_windows_without_another_download_reserve(self):
        from colombo.shared.runtime_budget import start_budget
        from colombo.cell.settings import load_policy
        policy = load_policy(profile="standard")
        # Explicit historical shared-deadline fixture. Current Colombo has no root cap.
        policy["workflow"] = {"version": 2}
        policy.pop("integration", None)
        policy["budget"] = {"research": {"total_active_seconds": 1000}}
        context = start_budget(self.root, policy)
        result = self.run_exp()
        execution = self.state(result)["execution"]
        self.assertEqual(result["status"], "completed")
        self.assertAlmostEqual(execution["deadline_at"], context["work_deadline_unix"], places=2)
        self.assertAlmostEqual(execution["total_deadline_at"], context["hard_deadline_unix"], places=2)

    def test_managed_resume_replaces_legacy_local_deadline_and_preserves_remote_request(self):
        from colombo.shared.runtime_budget import start_budget
        from colombo.cell.settings import load_policy
        self.remote.fail_download_once = True
        first = self.run_exp()
        self.assertIsNotNone(self.state(first)["execution"]["deadline_at"])
        self.clock.now += 100
        start_budget(self.root, load_policy(profile="hard"))
        resumed = self.resume_exp(first["experiment_id"])
        execution = self.state(resumed)["execution"]
        self.assertEqual(resumed["status"], "completed")
        self.assertIsNone(execution["deadline_at"])
        self.assertIsNone(execution["total_deadline_at"])
        self.assertEqual(self.post_count(), 1)

    def test_same_request_recovers_and_changed_request_is_rejected(self):
        first = self.run_exp()
        deadline = self.state(first)["execution"]["deadline_at"]
        self.clock.now += 100
        self.config["experiment"]["enabled"] = False
        second = self.run_exp()
        self.assertEqual(first["experiment_id"], second["experiment_id"])
        self.assertEqual(deadline, self.state(second)["execution"]["deadline_at"])
        self.assertEqual(1, self.post_count())
        with self.assertRaisesRegex(ex.ExperimentError, "different inputs"):
            self.run_exp(code="print(1)")

    def test_replay_distinguishes_boolean_and_numeric_parameters(self):
        self.assertEqual(self.run_exp(parameters={"flag": True})["status"], "completed")
        with self.assertRaisesRegex(ex.ExperimentError, "different inputs"):
            self.run_exp(parameters={"flag": 1})
        self.assertEqual(self.post_count(), 1)

    def test_retry_download_only_preserves_deadline(self):
        self.remote.fail_download_once = True
        first = self.run_exp()
        self.assertEqual("download_pending", first["status"])
        deadline = self.state(first)["execution"]["deadline_at"]
        self.clock.now += 100
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual("completed", second["status"])
        self.assertEqual(deadline, self.state(second)["execution"]["deadline_at"])
        self.assertEqual(1, self.post_count())

    def test_submission_disconnect_never_resubmits(self):
        self.remote.submit_unknown = True
        first = self.run_exp()
        self.assertEqual("remote_unknown", first["status"])
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual("remote_unknown", second["status"])
        self.assertEqual(1, self.post_count())
        with self.assertRaisesRegex(ex.ExperimentError, "unfinished"):
            self.run_exp(request_id="another")

    def test_deadline_cancels_and_unknown_cancellation_remains_unknown(self):
        self.remote.waiting = True
        self.remote.cancel_unknown = True
        first = self.run_exp()
        self.assertEqual("remote_unknown", first["status"])
        self.assertEqual(1008, self.clock.now)
        self.assertTrue(any(path.endswith("/cancel") for _, path, _ in self.remote.calls))
        self.remote.cancel_unknown = False
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual("timed_out", second["status"])
        self.assertEqual(1, self.post_count())

    def test_task_quota_persists_after_resume(self):
        self.config["experiment"]["max_runs"] = 1
        first = self.run_exp()
        self.resume_exp(first["experiment_id"])
        with self.assertRaisesRegex(ex.ExperimentError, "max_runs"):
            self.run_exp(request_id="another")

    def test_missing_key_disabled_or_low_budget_never_calls_network(self):
        os.environ.pop("OPENAI_API_KEY")
        with self.assertRaisesRegex(ex.ExperimentError, "OPENAI_API_KEY"):
            self.run_exp()
        os.environ["OPENAI_API_KEY"] = "test-only-private-key"
        self.config["experiment"]["enabled"] = False
        with self.assertRaisesRegex(ex.ExperimentError, "disabled"):
            self.run_exp()
        self.config["experiment"]["enabled"] = True
        os.environ["CELL_PROCESS_ID"] = "a" * 32
        with patch("colombo.cell.recovery.budget_status", return_value={"work_remaining_seconds": 1, "hard_deadline": 1010}):
            with self.assertRaisesRegex(ex.ExperimentError, "Insufficient"):
                self.run_exp()
        self.assertEqual([], self.remote.calls)

    def test_parent_budget_shortens_execution_but_keeps_reserve(self):
        os.environ["CELL_PROCESS_ID"] = "a" * 32
        with patch("colombo.cell.recovery.budget_status", return_value={"work_remaining_seconds": 5, "hard_deadline": 1010}):
            result = self.run_exp()
        self.assertEqual(1003, self.state(result)["execution"]["deadline_at"])
        self.assertEqual(1005, self.remote.deadline)

    def test_remote_traversal_and_input_parent_are_rejected(self):
        with self.assertRaises(ex.ExperimentError):
            self.run_exp(input_files=["../secret.txt"])
        self.remote.bad_path = True
        result = self.run_exp()
        self.assertEqual("download_pending", result["status"])
        self.assertEqual("invalid_remote_file_path", result["reason"])
        self.assertEqual("request-1", json.loads((self.root / result["plan_file"]).read_text())["request_id"])

    def test_required_receipt_missing_cannot_complete(self):
        self.remote.missing_receipt = True
        result = self.run_exp()
        self.assertEqual("download_pending", result["status"])
        self.assertEqual("required_artifacts_missing", result["reason"])

    def test_script_failure_is_not_completed(self):
        self.remote.script_failed = True
        result = self.run_exp()
        self.assertEqual("failed", result["status"])
        self.assertEqual("script_error", result["reason"])

    def test_input_copies_and_parameters_are_immutable(self):
        (self.root / "data.json").write_text('{"x":2}')
        result = self.run_exp(parameters={"seed": 3}, input_files=["data.json"])
        (self.root / "data.json").write_text('{"x":3}')
        self.resume_exp(result["experiment_id"])
        state = self.state(result)
        copy = next(item for item in state["artifacts"] if "inputs/input_0" in item["path"])
        self.assertEqual('{"x":2}', (self.root / copy["path"]).read_text())
        with self.assertRaisesRegex(ex.ExperimentError, "different inputs"):
            self.run_exp(parameters={"seed": 3}, input_files=["data.json"])

    def test_skill_resource_bytes_are_frozen_across_replay_and_resume(self):
        relative = "skills/estimate-epsilon-rate/scripts/gd_family_calibration.py"
        resource = self.root / relative
        resource.parent.mkdir(parents=True)
        original = (ROOT / "agents/experiment_cell" / relative).read_bytes()
        resource.write_bytes(original)
        self.remote.fail_download_once = True
        first = self.run_exp(input_files=[relative])
        self.assertEqual(first["status"], "download_pending")
        resource.write_bytes(b"#" + original[1:])  # Same size; identity includes content.
        with self.assertRaisesRegex(ex.ExperimentError, "different inputs"):
            self.run_exp(input_files=[relative])
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual(second["status"], "completed")
        plan = json.loads((self.root / second["plan_file"]).read_text())
        self.assertEqual((self.root / plan["input_files"][0]["saved_path"]).read_bytes(), original)
        self.assertEqual(self.post_count(), 1)

    def test_per_file_and_total_limits_do_not_mark_complete(self):
        self.remote.extra_bytes = self.config["experiment"]["artifact_max_bytes"] + 1
        first = self.run_exp()
        self.assertEqual("download_pending", first["status"])
        self.assertEqual("artifact_size_limit", first["reason"])

    def test_file_count_limit_covers_local_and_remote_artifacts(self):
        self.config["experiment"]["max_files"] = 4
        result = self.run_exp()
        self.assertNotEqual("completed", result["status"])
        self.assertEqual("artifact_budget_limit", result["reason"])

    def test_credentials_not_persisted_or_accepted_as_inputs(self):
        with self.assertRaisesRegex(ex.ExperimentError, "credentials"):
            self.run_exp(question="test-only-private-key")
        self.run_exp()
        for file in self.root.rglob("*"):
            if file.is_file():
                self.assertNotIn(b"test-only-private-key", file.read_bytes())

    def test_only_completed_tool_with_wrapper_invocation_is_evidence(self):
        original = self.remote.generate
        def no_tool(body):
            original(body)
            self.remote.response["output"] = [{"type": "message", "content": "I executed it"}]
        self.remote.generate = no_tool
        result = self.run_exp()
        self.assertEqual("failed", result["status"])
        self.assertEqual("execution_evidence_missing", result["reason"])

    def test_resume_uses_original_configuration(self):
        self.remote.fail_download_once = True
        first = self.run_exp()
        self.config["experiment"]["artifact_max_bytes"] = 1
        self.config["experiment"]["max_files"] = 1
        self.config["experiment"]["enabled"] = False
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual("completed", second["status"])
        self.assertEqual(1, self.post_count())

    def test_expired_container_is_terminal_with_partial_evidence(self):
        self.remote.fail_download_once = True
        first = self.run_exp()
        original = self.remote.json
        def expired(method, path, body=None):
            if "/files" in path:
                raise ex._TransportError("api_http_error", details={"http_status": 404})
            return original(method, path, body)
        self.remote.json = expired
        second = self.resume_exp(first["experiment_id"])
        self.assertEqual("expired", second["status"])
        self.assertGreater(second["artifact_count"], 0)
        self.assertEqual(1, self.post_count())

    def test_sensitive_input_files_never_upload(self):
        for name in ("auth.json", ".env", ".env.production", "secret.key"):
            (self.root / name).write_text("sensitive")
            with self.assertRaisesRegex(ex.ExperimentError, "Credential"):
                self.run_exp(input_files=[name])
        self.assertEqual([], self.remote.calls)

    def test_total_bytes_limit_before_dispatch(self):
        self.config["experiment"]["max_total_artifact_bytes"] = 10
        result = self.run_exp()
        self.assertEqual("failed", result["status"])
        self.assertEqual("artifact_budget_limit", result["reason"])
        self.assertEqual(0, self.post_count())

    def test_runtime_updates_real_store_and_preserves_interpretation(self):
        store = RealStore(self.root / "memory")
        claim = store.archive("claims", {"statement": "For all integers n, n(n+1) is even."})
        self.ref = {key: claim[key] for key in ("kind", "id", "revision")}
        self.remote.fail_download_once = True
        with patch.object(self, "memory", store):
            first = self.run_exp()
            saved = store.get("experiment_result", first["experiment_id"])
            payload = deepcopy(saved["payload"])
            payload["observations"] = "Finite samples; general proof remains open."
            store.archive("experiment_result", payload, record_id=first["experiment_id"], expected_revision=saved["revision"])
            second = self.resume_exp(first["experiment_id"])
            self.assertEqual("completed", second["status"])
            final = store.get("experiment_result", first["experiment_id"])
            self.assertEqual(payload["observations"], final["payload"]["observations"])
            again = self.resume_exp(first["experiment_id"])
            self.assertEqual(final["revision"], again["record_ref"]["revision"])
        self.assertEqual(1, self.post_count())

    def test_parent_granted_plan_is_not_own_run_or_quota(self):
        inherited = self.root / "experiments" / ("exp-" + "a" * 24)
        inherited.mkdir(parents=True)
        (inherited / "plan.json").write_text('{"request_id":"request-1"}')
        self.config["experiment"]["max_runs"] = 1
        result = self.run_exp()
        self.assertEqual("completed", result["status"])
        self.assertNotEqual(inherited.name, result["experiment_id"])
        with self.assertRaisesRegex(ex.ExperimentError, "read-only"):
            self.resume_exp(inherited.name)

    def test_http_errors_do_not_read_secret_body_or_headers(self):
        class Response:
            def __init__(self, status): self.status_code = status
            def close(self): pass
            def iter_content(self, amount): raise AssertionError("Error body must not be read")
        with patch.object(ex.requests, "Session") as session:
            for status in (401, 403, 404, 429, 500):
                session.return_value.request.return_value = Response(status)
                client = RealClient("test-only-private-key", self.config, 1010)
                with self.assertRaises(ex._TransportError) as caught:
                    client.json("POST", "/responses", {"model": "unavailable"})
                self.assertEqual({"http_status": status}, caught.exception.details)
                self.assertNotIn("test-only-private-key", str(caught.exception))
                self.assertEqual(status >= 500, caught.exception.uncertain)

    def test_http_response_containing_credentials_is_rejected(self):
        class Response:
            status_code = 200
            def close(self): pass
            def iter_content(self, amount): yield b'{"id":"test-only-private-key"}'
        with patch.object(ex.requests, "Session") as session:
            session.return_value.request.return_value = Response()
            client = RealClient("test-only-private-key", self.config, 1010)
            with self.assertRaisesRegex(ex._TransportError, "credential_in_response") as caught:
                client.json("POST", "/responses", {})
            self.assertTrue(caught.exception.uncertain)

    def test_operation_lock_prevents_parallel_dispatch(self):
        with ex._operation(self.root):
            with self.assertRaisesRegex(ex.ExperimentError, "Another experiment"):
                self.run_exp()
        self.assertEqual([], self.remote.calls)

    def test_generated_wrapper_executes_exact_code_once_and_receipts_inputs(self):
        # Only the generated wrapper is executed here, in a mapped temporary
        # directory. Production run_experiment never executes code locally.
        data = self.root / "sample.txt"
        data.write_text("7")
        code = b"from pathlib import Path\nassert PARAMETERS['seed'] == 3\nassert Path(INPUT_FILES['sample.txt']).read_text() == '7'\nPath('result.txt').write_text('computed')\nprint('sample 7')\n"
        plan = {"experiment_id": "wrapper-unit", "nonce": "nonce",
                "parameters": {"seed": 3}, "input_files": [{"path": "sample.txt"}]}
        script = ex._wrapper(plan, code, {"sample.txt": str(data)}).decode()
        script = script.replace('pathlib.Path("/mnt/data")', "pathlib.Path(" + repr(str(self.root)) + ")")
        previous = Path.cwd()
        try:
            with redirect_stdout(io.StringIO()):
                exec(compile(script, "runner.py", "exec"), {})
            output = self.root / "cell-wrapper-unit"
            receipt = json.loads((output / "execution_receipt.json").read_text())
            self.assertEqual("completed", receipt["status"])
            self.assertEqual(plan["nonce"], receipt["nonce"])
            self.assertEqual("sample 7\n", (output / "stdout.txt").read_text())
            (output / "result.txt").write_text("marker")
            with redirect_stdout(io.StringIO()):
                exec(compile(script, "runner.py", "exec"), {})
            self.assertEqual("marker", (output / "result.txt").read_text())
        finally:
            os.chdir(previous)

    def test_generated_wrapper_executes_uploaded_skill_bin_through_input_files(self):
        # Real local execution of the production wrapper with a mapped container
        # directory; fake HTTP output elsewhere in this suite is not rollout evidence.
        examples = (
            ("estimate-epsilon-rate/scripts/gd_family_calibration.py",
             {"mode": "all", "budgets": [0, 1, 4], "epsilons": [0.1], "max_steps": 100}, "measurements.json"),
            ("probe-mechanism/scripts/quadratic_inequality_probe.py", {}, "exact_witness.json"),
        )
        for index, (name, parameters, output_name) in enumerate(examples):
            with self.subTest(resource=name):
                relative = "skills/" + name
                uploaded = self.root / f"uploaded-input-{index}.bin"
                uploaded.write_bytes((ROOT / "agents/experiment_cell" / relative).read_bytes())
                code = ("import runpy\nmodule = runpy.run_path(INPUT_FILES[" + repr(relative) + "])\n"
                        "module['run'](PARAMETERS, OUTPUT_DIR)\n").encode()
                plan = {"experiment_id": f"skill-wrapper-{index}", "nonce": "skill-wrapper-nonce",
                        "parameters": parameters, "input_files": [{"path": relative}]}
                script = ex._wrapper(plan, code, {relative: str(uploaded)}).decode()
                script = script.replace('pathlib.Path("/mnt/data")', "pathlib.Path(" + repr(str(self.root)) + ")")
                previous = Path.cwd()
                try:
                    with redirect_stdout(io.StringIO()):
                        exec(compile(script, "runner.py", "exec"), {})
                finally:
                    os.chdir(previous)
                output = self.root / ("cell-" + plan["experiment_id"])
                receipt = json.loads((output / "execution_receipt.json").read_text())
                self.assertEqual(receipt["status"], "completed", (output / "stderr.txt").read_text())
                self.assertIn(output_name, {row["name"] for row in receipt["files"]})
                data = json.loads((output / output_name).read_text())
                if index == 0:
                    self.assertEqual(data["source"], "actual_gd_rollout")
                    self.assertTrue(any(case["gradient_calls"] > 0 for case in data["cases"]))
                else:
                    self.assertTrue(data["witness"]["violation"])

    def test_wrapper_missing_explicit_dependency_is_a_script_failure(self):
        code = b"from pathlib import Path\nPath(INPUT_FILES['required-data.json']).read_text()\n"
        plan = {"experiment_id": "missing-dependency", "nonce": "missing", "parameters": {}, "input_files": []}
        script = ex._wrapper(plan, code, {}).decode()
        script = script.replace('pathlib.Path("/mnt/data")', "pathlib.Path(" + repr(str(self.root)) + ")")
        previous = Path.cwd()
        try:
            with redirect_stdout(io.StringIO()):
                exec(compile(script, "runner.py", "exec"), {})
        finally:
            os.chdir(previous)
        output = self.root / "cell-missing-dependency"
        receipt = json.loads((output / "execution_receipt.json").read_text())
        self.assertEqual(receipt["status"], "failed")
        self.assertEqual(receipt["error_type"], "KeyError")
        self.assertIn("required-data.json", (output / "stderr.txt").read_text())


if __name__ == "__main__":
    unittest.main()
