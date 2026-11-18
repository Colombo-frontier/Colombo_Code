"""Oracle Complexity execution: Result verification precedes every Brain update.

One durable Controller coordinates asynchronous Cells within a single Wave.
Only returned attempt snapshots enter model context. Research counts and the
independent integration clock survive restart without replenishment.
"""
import json
import time

from colombo.brain.model_calls import CodexBackend, ModelCalls, NeedsAttention, find_codex
from colombo.brain.task_execution import TaskExecution
from colombo.brain.cell_dispatch import CellAdapter
from colombo.brain.proof_draft import initial_proof, write_proof, export_current
from colombo.brain.final_report import conclude
from colombo.brain.research_store import Store
from colombo.shared.file_io import Path
from colombo.shared import runtime_budget as shared_budget
from colombo.shared.file_io import atomic_write, json_bytes
from colombo.brain.research_records import state_view
from colombo.brain.submission_validation import validate_progress, integration_structure_issues


class OracleController:
    def __init__(self, project_root, run_root, backend=None, adapter=None):
        self.project = Path(project_root).resolve()
        self.store = Store(Path(run_root))
        self.root = self.store.root
        self.config = self.store.get_meta("config")
        self.process_poll_seconds = shared_budget.cell_operational(self.config, "process_poll_seconds", 0.05)
        backend = backend or CodexBackend(self.project, self.config)
        if adapter is None:
            config = json.loads(json.dumps(self.config))
            config["cell"]["codex_bin"] = find_codex(config.get("runtime"))
            if config.get("runtime", {}).get("auth_home"):
                config["cell"]["auth_home"] = config["runtime"]["auth_home"]
            if config.get("runtime", {}).get("model_catalog_json"):
                config["cell"]["model_catalog_json"] = config["runtime"]["model_catalog_json"]
            adapter = CellAdapter(self.project, config)

        self.calls = ModelCalls(self.store, backend)
        self.tasks = TaskExecution(self.store, adapter, self.config, self._transition)

    def _transition(self, phase, **values):
        self.store.set_meta(phase=phase, pending_call=None, **values)
        self.store.event("phase", phase=phase)
        self._export_state()

    def _start_budget(self):
        if self.store.get_meta("phase") != "done":
            shared_budget.start(self.root, self.config)

    def _pause_budget(self):
        # A detached Cell supervisor can still be doing work. Its shared clock
        # must keep running until it exits or a later controller reconciles it.
        from colombo.shared.tool_jobs import pending_jobs
        if (not any(t.get("state") in {"running", "stopping"} for t in self.store.list_tasks())
                and not pending_jobs(self.root)):
            pending = self.store.get_meta("pending_call")
            if pending:
                path = self.root / "brain/calls" / pending["call_id"] / "call.json"
                if path.is_file():
                    manifest = json.loads(path.read_text(encoding="utf-8"))
                    # An unsuccessful teardown must not release the deadline
                    # while the model or its owned tools could still be alive.
                    if (manifest.get("process_tree_terminated") is False
                            or manifest.get("status") in {"running", "launch_intent"}):
                        return
            shared_budget.pause(self.root, self.config)

    def _export_state(self):
        view = state_view(self.store)
        text = "# Brain state\n\n" + "This file is a rebuildable view; the authoritative state is stored in the research records in state.sqlite.\n\n"
        text += "```json\n" + json.dumps(view, ensure_ascii=False, indent=2) + "\n```\n"
        atomic_write(self.root / "memory/brain_state.md", text.encode("utf-8"))
        self.store.export_documents()

    def _initialize_proof(self):
        if not self.store.get_meta("proof_ref"):
            ref = write_proof(self.store, initial_proof(self.store), "proof:initial")
            self.store.set_meta(proof_ref=ref, result_events=[], admitted_results={},
                                prune_commands=[], event_counter=0)
        export_current(self.store)

    def _call(self, role, stage, prompt, context):
        return self.calls.invoke(role, stage, prompt, context)

    def _conclude(self):
        self._validate_confirmed_progress()
        conclude(self.store)
        self._export_state()

    def _integration_expired(self):
        stage = self.store.get_meta("integration")
        return (self.store.get_meta("phase") in {"integrating", "final_reviewing"}
                and stage and time.time() >= stage["deadline_unix"])

    def _integration_call_settled(self):
        """A deadline cannot release a model invocation whose exit is unknown."""
        if self.store.unresolved_audits():
            return False
        pending = self.store.get_meta("pending_call")
        if not pending:
            return True
        path = self.root / "brain/calls" / pending["call_id"] / "call.json"
        try:
            if path.is_file():
                call = json.loads(path.read_text(encoding="utf-8"))
                if call.get("call_id") != pending["call_id"]:
                    return False
                if call.get("process_tree_terminated") is False:
                    return False
                if (call.get("process_exit_confirmed") is True
                        and call.get("process_tree_terminated") is True):
                    return True
                return (call.get("status") == "not_started" or
                        call.get("lifecycle_version") == 2 and call.get("status") == "preparing")
            # Alternate backends may provide an explicit non-running receipt.
            if hasattr(self.calls.backend, "reconcile_call"):
                return self.calls.backend.reconcile_call(self.root, pending["call_id"])["state"] in {"failed", "not_started"}
        except (OSError, ValueError, KeyError, TypeError, RuntimeError):
            pass
        return False

    def _reconcile_pending(self):
        if self._integration_expired() and not self._integration_call_settled():
            raise NeedsAttention("Integration deadline expired, but the pending model call or audit has no confirmed exit")
        return self.calls.reconcile()


    def _wave_used(self):
        return len(self.tasks.jobs())

    def _remaining_dispatch(self):
        return max(0, self.config["limits"]["max_dispatches_per_wave"] - self._wave_used())

    def _has_research_budget(self):
        return self._remaining_dispatch() > 0 or self.store.get_meta("round_no", 0) < self.config["limits"]["max_rounds"]

    def _plan(self):
        current = self.store.get_meta("round_no", 0)
        wave = self.store.get_meta("planning_wave", current + 1)
        if wave > self.config["limits"]["max_rounds"]:
            self._begin_integrate("wave_allocation_exhausted")
            return
        supplement = wave == current
        remaining = self._remaining_dispatch() if supplement else self.config["limits"]["max_dispatches_per_wave"]
        self.store.set_meta(planning_wave=wave)
        proposal = self._call("brain", "plan",
            "Use plan Skill. Complete Setting Specification on the first call from the selected input files; "
            "retain unknowns and provenance. Fix Oracle, Algorithm Class, Guarantee, Resource and regimes. "
            "Reason about candidate rates before choosing scoped near-optimal Tasks. A supplemental plan "
            "may return no tasks if no useful uncovered responsibility can be assigned. "
            "Read all unresolved Result/final reviews; substantive errors require research Tasks. "
            "Do not alter existing assignments when resuming or restarting. Resume retains remaining Cell starts; "
            "use mode=restart with resume_task_id to explicitly allocate a fresh cycle of Cell starts when useful. "
            "Both cost one dispatch. Never repeat an exhausted resume; read resume_eligibility and returned "
            "stop_info/budget_snapshot. Restart retains records and cumulative usage; it does not reset "
            "per-report Checker or per-Challenge limits. Do not inspect running Cell research.",
            {"state": state_view(self.store), "round_no": wave, "supplemental": supplement,
             "dispatch_remaining": remaining, "setting_ref": self.store.get_meta("setting_ref"),
             "final_review_ref": self.store.get_meta("unresolved_review_ref")})
        ref = self.store.get_meta("pending_call")["response_ref"]
        if not self.store.get_meta("setting_ref"):
            setting = proposal["setting_specification"]
            setting_ref = self.store.write_record("setting", setting, request_id="setting:initial")
            atomic_write(self.root / "input/setting.json", json_bytes(setting))
            self.store.set_meta(setting_ref=setting_ref)
        jobs = self.store.plan_jobs(ref)
        previous = self.store.get_meta("round_data", {}) if supplement else {}
        all_jobs = [*previous.get("jobs", []), *jobs]
        data = {"round_no": wave, "plan_ref": ref, "jobs": all_jobs,
                "prepare_jobs": jobs, "result_refs": previous.get("result_refs", [])}
        self._transition("preparing" if jobs else "running", round_no=wave, round_data=data,
            dispatch_count=self.store.get_meta("dispatch_count", 0) + len(jobs),
            plan_declined_wave=wave if not jobs else None, integration_requested=not jobs)

    def _prepare(self):
        data = self.store.get_meta("round_data")
        jobs = data.get("prepare_jobs", [])
        all_jobs = data.get("all_jobs", data["jobs"])
        if jobs:
            # Current execution facts must not describe the preceding attempt.
            # Fixed Results and latest_result_ref/finished_attempt retain history.
            for job in jobs:
                task = self.store.get_task(job["task_id"])
                if task and task.get("active_attempt") != job["attempt_id"]:
                    task.update(execution_status=None, accepted=None, review_status=None,
                        result_summary=None, failure=None, outcome_attempt_id=None, execution_fault_ref=None)
                    self.store.save_task(task)
            self.store.set_meta(round_data={**data, "jobs": jobs, "all_jobs": all_jobs})
            self.tasks.prepare()
        data.pop("all_jobs", None)
        self.store.set_meta(round_data={**data, "jobs": all_jobs, "prepare_jobs": []}, phase="running")

    def _pending_results(self):
        processed = set(self.store.get_meta("processed_results", []))
        return [e for e in self.store.get_meta("result_events", []) if e["result_ref"]["id"] not in processed]

    def _review_package(self, *, result_ref=None, proof_ref=None, assessment_ref=None):
        refs = [self.store.get_meta("goal_ref"), self.store.get_meta("setting_ref")]
        refs += self.store.get_meta("material_refs", [])
        if result_ref:
            result = self.store.read_record(result_ref)
            refs += [result_ref, result.get("assignment_ref"), result.get("package_ref")]
        else:
            refs += [proof_ref, assessment_ref]
            refs += [self.store.record_ref(rid) for rid in self.store.get_meta("result_reviews", {})]
            refs += list(self.store.get_meta("result_reviews", {}).values())
        for ref in list(refs):
            if ref and self.store.record_kind(ref) == "assignment":
                refs += [self.store.record_ref(i["ref"]) for i in self.store.read_record(ref)["spec"]["package"]["items"]]
        refs = list({r["id"]: r for r in refs if r}.values())
        for ref in refs:
            self.tasks.validate_artifacts(ref)
        return {"review_kind": "result" if result_ref else "proof",
            "result_ref": result_ref["id"] if result_ref else None,
            "proof_ref": proof_ref, "proposal_ref": assessment_ref,
            "references": refs, "required_checked_refs": [r["id"] for r in refs],
            "allowed_refs": [r["id"] for r in refs]}

    def _tick(self):
        self.tasks.poll_workers()
        self.tasks.apply_stops()
        pending = self._pending_results()
        if pending:
            event = pending[0]
            rid = event["result_ref"]["id"]
            if rid in self.store.get_meta("result_reviews", {}):
                self._transition("processing_results", processing_result=event)
            else:
                package = self._review_package(result_ref=event["result_ref"])
                pref = self.store.write_record("review_package", package, request_id="result-package:" + rid)
                self._transition("result_reviewing", processing_result=event, result_review_package=pref)
            return
        if any(c["state"] not in {"confirmed", "already_completed"} for c in self.store.get_meta("prune_commands", [])):
            self.tasks.start_available()
            time.sleep(self.process_poll_seconds)
            return
        if self.store.get_meta("supplement_requested") and self._remaining_dispatch():
            self._transition("planning", planning_wave=self.store.get_meta("round_no"), supplement_requested=False)
            return
        self.tasks.start_available()
        if self.tasks.has_workers() or any(not self.tasks.terminal(j) for j in self.tasks.jobs()):
            time.sleep(self.process_poll_seconds)
            return
        progress_ref = self.store.get_meta("progress_ref")
        progress = self.store.read_record(progress_ref)["progress"] if progress_ref else None
        if (progress and progress["status"] == "completed") or self.store.get_meta("integration_requested"):
            self.store.set_meta(integration_requested=False)
            self._begin_integrate("goal_ready")
        elif self._remaining_dispatch() and self.store.get_meta("plan_declined_wave") != self.store.get_meta("round_no"):
            self._transition("planning", planning_wave=self.store.get_meta("round_no"))
        elif self.store.get_meta("round_no", 0) < self.config["limits"]["max_rounds"]:
            self._transition("planning", planning_wave=self.store.get_meta("round_no", 0) + 1)
        else:
            self._begin_integrate("research_allocation_exhausted")

    def _result_review(self):
        event = self.store.get_meta("processing_result")
        rid = event["result_ref"]["id"]
        report = self._call("verifier", "verify-progress",
            "Verify the returned Result before Brain update. Read the fixed assignment, Setting and all necessary "
            "frozen artifacts. Identify individually confirmed Claims with exact scope, assumptions, expressions "
            "and evidence paths, even if the overall Task is incomplete or local accepted=false. "
            "For empirical Results confirm empirical reliability only; never certify mathematical Bounds. "
            "Review near-optimal comparisons explicitly as comparison Claims when proved. "
            "Report mathematical defects with repair_kind=research, not presentation.",
            {"review_package_ref": self.store.get_meta("result_review_package"), "review_kind": "result"})
        ref = self.store.get_meta("pending_call")["response_ref"]
        reviews = self.store.get_meta("result_reviews", {})
        reviews[rid] = ref
        self._transition("processing_results", result_reviews=reviews,
            unresolved_review_ref=ref if report["findings"] else self.store.get_meta("unresolved_review_ref"))

    def _process_results(self):
        event = self.store.get_meta("processing_result")
        rid = event["result_ref"]["id"]
        counter = self.store.get_meta("event_counter", 0) + 1
        if not self.store.get_meta("pending_call"):
            self.store.set_meta(event_counter=counter, event_data={"id": f"E{counter:05d}", "version": 1,
                "wave_id": f"W{self.store.get_meta('round_no'):04d}", "previous_progress_ref": self.store.get_meta("progress_ref"),
                "previous_proof_ref": self.store.get_meta("proof_ref"), "processing_scope": "result"})
        proposal = self._call("brain", "process_results",
            "The Result has already been independently verified. Apply update using only individually confirmed "
            "Claims and their exact expressions/scopes; preserve unresolved Goal responsibilities. "
            "Do not repair mathematics inside Assessment. New mathematical gaps require new Tasks. "
            "Use prune only for audited mathematical relations with verified premises. "
            "next_action=plan requests optional supplementation after stop coordination; conclude requests "
            "integration after all executions settle. No full ProofDraft is required in this update.",
            {"processing_scope": "result", "state": state_view(self.store), "result_refs": [event["result_ref"]],
             "result_review_ref": self.store.get_meta("result_reviews")[rid],
             "task_snapshot": self.store.list_tasks()})
        aref = self.store.get_meta("pending_call")["response_ref"]
        pref = self.store.write_record("goal_progress", {"progress": proposal["update"]["progress"],
            "result_refs": proposal["result_refs"], "assessment_ref": aref,
            "review_refs": list(self.store.get_meta("result_reviews", {}).values()),
            "previous_ref": self.store.get_meta("progress_ref")}, request_id="progress:" + aref["id"])
        commands = self.store.get_meta("prune_commands", [])
        for i, prune in enumerate(proposal["prunes"]):
            dref = self.store.write_record("prune_decision", {**prune, "assessment_ref": aref,
                "prune_index": i}, request_id=f"prune:{aref['id']}:{i}")
            commands.append({"id": f"stop-{aref['id']}-{i}", "state": "pending", "decision_ref": dref,
                "task_id": prune["task_id"], "attempt_id": prune["attempt_id"],
                "assignment_ref": self.store.get_task(prune["task_id"])["assignment_ref"]})
        data = self.store.get_meta("event_data")
        data.update(assessment_ref=aref, progress_ref=pref, adoption_status="adopted")
        events = self.store.get_meta("result_events", [])
        for returned in events:
            if returned["result_ref"]["id"] == rid:
                returned["state"] = "processed"
        self._transition("running", progress_ref=pref, event_data=data,
            processed_results=[*self.store.get_meta("processed_results", []), rid],
            result_events=events, prune_commands=commands, supplement_requested=proposal["next_action"] == "plan",
            integration_requested=proposal["next_action"] == "conclude")


    def _begin_integrate(self, reason):
        stage = self.store.get_meta("integration")
        tokens = set()
        for rid in self.store.get_meta("processed_results", []):
            result = self.store.read_record(rid)
            activity = result.get("research_activity", {})
            if activity.get("started") is True:
                tokens.update(result["task_id"] + ":" + pid for pid in activity.get("process_ids", [])
                              if isinstance(pid, str) and pid)
        tokens = sorted(tokens)
        if stage and "research_tokens" not in stage:
            # Adopting this marker format must not replenish an existing clock.
            stage = {**stage, "research_tokens": tokens}
        elif not stage or set(tokens) - set(stage["research_tokens"]):
            started = time.time()
            stage = {"started_at": started, "deadline_unix": started + self.config["integration"]["timeout_seconds"],
                "research_generation": stage.get("research_generation", 0) + 1 if stage else 0,
                "research_tokens": tokens, "revision": 0}
        self._transition("integrating", integration=stage, stop_reason=reason)

    def _integration_context(self):
        stage = self.store.get_meta("integration")
        if time.time() >= stage["deadline_unix"]:
            if not self._integration_call_settled():
                raise NeedsAttention("Integration deadline expired before the pending model call or audit was reconciled")
            self._transition("concluding", stop_reason="integration_timeout")
            return None
        return {"integration_deadline_unix": stage["deadline_unix"],
                "state": state_view(self.store), "previous_review_ref": self.store.get_meta("unresolved_review_ref"),
                "publication_feedback": self.store.get_meta("publication_feedback")}

    def _integrate(self):
        context = self._integration_context()
        if context is None:
            return
        if not self.store.get_meta("pending_call"):
            stage = self.store.get_meta("integration")
            stage["revision"] += 1
            self.store.set_meta(integration=stage, event_data={"id": "I" + str(stage["research_generation"]),
                "version": stage["revision"], "wave_id": f"W{self.store.get_meta('round_no'):04d}",
                "previous_proof_ref": self.store.get_meta("proof_ref"), "processing_scope": "integrate"})
        self._call("brain", "integrate",
            "Use integrate Skill to compose the original top-level ProofDraft: a complete self-contained "
            "report/Proof from all relevant returned Cell process artifacts. Include definitions, assumptions, "
            "Lemmas, complete derivations, composition, regime coverage and unresolved gaps. "
            "Use only verified Claims as established results. Address previous final review. "
            "Address any publication_feedback structural issues in a new candidate; they are runtime feedback, "
            "not mathematical verification. Mark a step checked only after rechecking its argument, "
            "and retain in_progress if any mathematical work remains. The revised draft needs final Verifier again. "
            "If research allocation is exhausted, explicitly withdraw unsupported completion claims and "
            "produce a reviewed partial report. Submit with record_results; no Pruning here.", context)
        aref = self.store.get_meta("pending_call")["response_ref"]
        proof = self.store.assessment_proof(aref)
        package = self._review_package(proof_ref=proof, assessment_ref=aref)
        pref = self.store.write_record("review_package", package, request_id="proof-package:" + aref["id"])
        stage = self.store.get_meta("integration")
        stage.update(assessment_ref=aref, proof_ref=proof, review_package_ref=pref)
        self._transition("final_reviewing", integration=stage, integration_draft_ref=proof)

    def _revise_incomplete_integration(self, stage, review_ref=None):
        proposal = self.store.read_record(stage["assessment_ref"])
        issues = integration_structure_issues(proposal["update"]["proof_draft"])
        if review_ref:
            from colombo.brain.final_completion import proof_steps_complete, review_completes_goal
            if (review_completes_goal(self.store.read_record(review_ref))
                    and proof_steps_complete(proposal["update"]["proof_draft"])):
                # Only the exact completed final review can classify retained
                # questions as outside the Goal; pre-review checks stay strict.
                issues = []
        if proposal["update"]["progress"]["status"] != "completed" or not issues:
            return False
        # Historical candidates may predate submission-time validation. This
        # is runtime feedback; only Brain can submit a new candidate for review.
        feedback = {"kind": "incomplete_proof_structure", "assessment_ref": stage["assessment_ref"],
            "proof_ref": stage["proof_ref"], "review_ref": review_ref, "issues": issues,
            "instruction": "Recheck these step declarations in a new integration candidate; do not treat this runtime feedback as mathematical review. The new draft will be independently reviewed."}
        self.store.event("publication_structure_revision_required", **feedback)
        self._transition("integrating", publication_feedback=feedback)
        return True

    def _final_review(self):
        context = self._integration_context()
        if context is None:
            return
        stage = self.store.get_meta("integration")
        # Do not discard a pending invocation or a submitted genuine review.
        # With no pending call, avoid starting Verifier just to find malformed
        # completion declarations on a candidate submitted by older code.
        if not self.store.get_meta("pending_call") and self._revise_incomplete_integration(stage):
            return
        report = self._call("verifier", "verify-progress",
            "Independently verify this complete self-contained ProofDraft and its GoalProgress. "
            "Check exact Setting, uniform Oracle/resource accounting, all regimes, composition and actual "
            "polylog factors. Partial results also require a correct self-contained report. "
            "Use repair_kind=research for mathematical gaps requiring new work; presentation only for "
            "correctable exposition/reference errors. confirmed_claims=[] for this final Proof review.",
            {**context, "review_package_ref": stage["review_package_ref"], "proof_ref": stage["proof_ref"]})
        ref = self.store.get_meta("pending_call")["response_ref"]
        self.store.set_meta(integration_review_ref=ref)
        if time.time() >= stage["deadline_unix"]:
            if not self._integration_call_settled():
                raise NeedsAttention("Final review deadline expired before its process exit was confirmed")
            self._transition("concluding", stop_reason="integration_timeout", unresolved_review_ref=ref)
            return
        if report["verdict"] == "pass":
            if self._revise_incomplete_integration(stage, ref):
                return
            from colombo.brain.final_completion import final_progress_payload
            payload = final_progress_payload(self.store, stage, ref, self.store.get_meta("progress_ref"))
            pref = self.store.write_record("goal_progress", payload,
                request_id="final-progress:" + ref["id"])
            self._transition("concluding", progress_ref=pref, proof_ref=stage["proof_ref"],
                final_review_ref=ref, unresolved_review_ref=None, publication_feedback=None)
            export_current(self.store)
        elif report["repair_kind"] == "research" and self._has_research_budget():
            wave = self.store.get_meta("round_no") + (0 if self._remaining_dispatch() else 1)
            self._transition("planning", planning_wave=wave, unresolved_review_ref=ref,
                integration={**stage, "awaiting_research": True})
        else:
            self._transition("integrating", unresolved_review_ref=ref)

    def _validate_confirmed_progress(self):
        ref = self.store.get_meta("progress_ref")
        if ref:
            validate_progress(self.store, self.store.read_record(ref)["progress"])

    def run(self):
        with self.store.exclusive():
            self.tasks.start()
            try:
                self._start_budget()
                self._initialize_proof()
                self.store.set_meta(research_routing={"research_mode": "oracle_complexity", "source": "fixed", "reason": "Colombo Oracle Complexity"})
                if self.store.get_meta("phase") == "done":
                    self._conclude()
                    return state_view(self.store)
                self._reconcile_pending()
                self.tasks.recover_events()
                self.tasks.reattach_running()
                self.store.set_meta(status="running")
                handlers = {"planning": self._plan, "preparing": self._prepare, "running": self._tick,
                    "result_reviewing": self._result_review, "processing_results": self._process_results,
                    "integrating": self._integrate, "final_reviewing": self._final_review, "concluding": self._conclude}
                while self.store.get_meta("phase") != "done":
                    handlers[self.store.get_meta("phase")]()
                return state_view(self.store)
            except (KeyboardInterrupt, Exception) as exc:
                if self._integration_expired() and self._integration_call_settled():
                    self._transition("concluding", stop_reason="integration_timeout")
                    self._conclude()
                    return state_view(self.store)
                self.store.set_meta(status="needs_attention", stop_reason=f"{type(exc).__name__}: {exc}")
                self.store.event("controller_stopped", error_type=type(exc).__name__, reason=str(exc))
                raise
            finally:
                self.tasks.close()
                self._pause_budget()
                self._export_state()
