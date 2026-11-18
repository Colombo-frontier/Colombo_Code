"""Synthetic Cell fixtures shared by current Controller and storage tests.

These adapters exercise orchestration without starting a research model.
"""
from pathlib import Path
import json
import threading
import time
from colombo.shared.file_io import freeze_json, read_json


class FakeCell:
    def __init__(self):
        self.lock = threading.Lock()
        self.active = self.maximum = self.launches = 0
        self.inputs = []

    def prepare(self, task_dir, assignment, package_dir, **scope):
        if not (package_dir / "manifest.json").is_file():
            raise ValueError("Package must be frozen before launch")
        self.inputs.append((assignment["task_id"], package_dir))

    def run(self, task_dir, attempt_id, resume=False, cancel_event=None):
        folder = task_dir / "results" / attempt_id
        receipt = folder / "fake-receipt.json"
        if receipt.is_file():
            return json.loads(receipt.read_text())
        with self.lock:
            self.active += 1
            self.maximum = max(self.maximum, self.active)
            self.launches += 1
        try:
            time.sleep(0.04)
            folder.mkdir(parents=True, exist_ok=True)
            content = b"Synthetic output for orchestration testing. No mathematical certification.\n"
            artifact = folder / "output.md"
            artifact.write_bytes(content)
            result = {"execution_status": "finished", "accepted": True, "review_status": "synthetic",
                "scientific_outcome": "synthetic", "summary": "Synthetic Cell result", "stop_reason": "fixture",
                "run_dir": str(task_dir / "cell"), "attempt_id": attempt_id,
                "artifacts": [{'path': artifact.relative_to(task_dir).as_posix(), 'size': len(content)}]}
            receipt.write_text(json.dumps(result))
            return result
        finally:
            with self.lock:
                self.active -= 1

def event_task(title, *, retain=False):
    return {"title": title, "instructions": "Synthetic independent route " + title,
        "deliverables": ["A complete synthetic proof"], "completion_criteria": ["Justify the target"],
        "mode": "new", "resume_task_id": None,
        "package": {"background": "Equivalent routes for one test target",
            "selection_reason": "The synthetic fixture is self-contained", "items": []},
        "responsibility": {"problem_id": "G0", "claim": "Synthetic target",
            "assumptions": [], "scope": "Synthetic test only", "goal_ids": ["G0"],
            "proof_step_ids": ["P0"], "route_group": "equivalent-routes", "retain": retain}}

class AsyncCellFixture:
    """Independent background workers outlive cancelled controller waits."""
    def __init__(self):
        self.lock = threading.RLock()
        self.workers = {}
        self.release_slow = threading.Event()
        self.launches = []
        self.stop_requests = []
        self.effective_stops = set()
        self.first_stop_crash = False
        self.active = self.maximum = 0
        self.worker_errors = {}

    def prepare(self, task_dir, assignment, package_dir, *, assignment_ref, package_ref):
        assert (package_dir / "manifest.json").is_file()
        freeze_json(task_dir / "prepared.json", {"task_id": task_dir.name, "assignment_ref": assignment_ref, "package_ref": package_ref})

    def _result_path(self, task_dir, attempt_id):
        return task_dir / "results" / attempt_id / "fixture_result.json"

    def _finish(self, task_dir, attempt_id, cancelled, *, started=True):
        with self.lock:
            output = self._result_path(task_dir, attempt_id)
            if output.exists():
                return read_json(output)
            content = ("Synthetic partial draft after pruning" if cancelled else
                       "Synthetic complete proof for orchestration testing").encode()
            artifact = output.parent / "proof.md"
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_bytes(content)
            result = {"execution_status": "cancelled" if cancelled else "finished",
                "accepted": not cancelled, "review_status": "synthetic",
                "scientific_outcome": None if cancelled else "synthetic", "started": started,
                "summary": "Synthetic fixture output", "stop_reason": "pruned" if cancelled else "fixture",
                "run_dir": str(task_dir / "cell"), "attempt_id": attempt_id,
                "artifacts": [{'path': artifact.relative_to(task_dir).as_posix(), 'size': len(content)}]}
            freeze_json(output, result)
            return result

    def _work(self, task_dir, attempt_id, stop):
        try:
            if task_dir.name == "T0001":
                time.sleep(0.06)
            else:
                # Stay active until the test explicitly releases or prunes this
                # route. A busy machine must not invent a successful result.
                deadline = time.monotonic() + 60
                while not stop.is_set() and not self.release_slow.is_set() and time.monotonic() < deadline:
                    stop.wait(0.01)
                if not stop.is_set() and not self.release_slow.is_set():
                    with self.lock:
                        self.worker_errors[(str(task_dir), attempt_id)] = "Fixture timed out awaiting explicit release or stop"
                    return
            self._finish(task_dir, attempt_id, stop.is_set())
        finally:
            with self.lock:
                self.active -= 1

    def run(self, task_dir, attempt_id, resume=False, cancel_event=None):
        task_dir = Path(task_dir)
        key = (str(task_dir), attempt_id)
        with self.lock:
            result = self.reconcile(task_dir, attempt_id)
            if result is not None:
                return result
            if key not in self.workers:
                folder = task_dir / "attempts" / attempt_id
                folder.mkdir(parents=True, exist_ok=True)
                freeze_json(folder / "launch.json", {"synthetic": True})
                stop = threading.Event()
                thread = threading.Thread(target=self._work, args=(task_dir, attempt_id, stop), daemon=True)
                self.workers[key] = (stop, thread)
                self.launches.append((task_dir.name, attempt_id))
                self.active += 1
                self.maximum = max(self.maximum, self.active)
                thread.start()
        while True:
            with self.lock:
                if key in self.worker_errors:
                    raise AssertionError(self.worker_errors[key])
            if cancel_event is not None and cancel_event.is_set():
                raise InterruptedError("Controller detached; synthetic worker continues")
            result = self.reconcile(task_dir, attempt_id)
            if result is not None:
                return result
            time.sleep(0.01)

    def reconcile(self, task_dir, attempt_id):
        # The fixture publishes on a background thread under this same lock.
        # Observe only a fully published receipt, without racing its Windows
        # file replacement. Real adapter receipts have their own lifecycle.
        with self.lock:
            path = self._result_path(Path(task_dir), attempt_id)
            return read_json(path) if path.exists() else None

    def request_stop(self, task_dir, attempt_id, decision_ref, request_id):
        task_dir = Path(task_dir)
        key = (str(task_dir), attempt_id)
        with self.lock:
            self.stop_requests.append((task_dir.name, attempt_id, request_id))
            result = self.reconcile(task_dir, attempt_id)
            if result is not None:
                return {"status": "cancelled" if result["execution_status"] == "cancelled" else "already_completed"}
            folder = task_dir / "attempts" / attempt_id
            freeze_json(folder / "stop_request.json", {"decision_ref": decision_ref, "request_id": request_id})
            self.effective_stops.add(key)
            if key in self.workers:
                self.workers[key][0].set()
                status = "requested"
            else:
                self._finish(task_dir, attempt_id, True, started=False)
                status = "cancelled"
            if self.first_stop_crash:
                self.first_stop_crash = False
                raise RuntimeError("Simulated crash after durable stop request")
            return {"status": status}

    def close(self):
        self.release_slow.set()
        for stop, thread in list(self.workers.values()):
            stop.set()
            thread.join(3)


class OracleTestFixture:
    """Fresh current-workflow Store and a synthetic Cell for lifecycle tests."""
    def setUp(self):
        import tempfile
        from colombo.configuration import load_config, PROJECT_ROOT
        from colombo.brain.research_store import Store
        parent = PROJECT_ROOT / "validation/tmp"
        parent.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="controller-current-", dir=parent)
        self.root = Path(self.temp.name) / "run"
        config = load_config()
        config["limits"].update(max_rounds=1, max_dispatches_per_wave=1, max_parallel_cells=2)
        self.store = Store.create(self.root, "fixture", [], config)
        self.adapter = FakeCell()

    def tearDown(self):
        if hasattr(self.adapter, "close"):
            self.adapter.close()
        self.temp.cleanup()

    def controller(self, backend, cls=None):
        from colombo.configuration import PROJECT_ROOT
        from colombo.brain.controller import OracleController
        return (cls or OracleController)(PROJECT_ROOT, self.root, backend=backend, adapter=self.adapter)
