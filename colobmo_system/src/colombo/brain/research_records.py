"""Domain storage: fixed bodies live in Task/Wave nodes, never in a record bag."""
from __future__ import annotations

import copy
import json
import uuid
from colombo.shared.file_io import json_equal


def initial_documents():
    return {"research": {"goal": {}, "materials": {}, "tasks": {}, "waves": {},
                         "audits": {}, "conclusion": {}},
            "proof_draft": {"current_ref": None, "versions": {}},
            "working_notes": {"entries": {}}}


def identity(ref):
    return ref["id"] if isinstance(ref, dict) else ref


def at(documents, document, pointer):
    value = documents[document]
    for key in json.loads(pointer):
        value = value[key]
    return value


def task_node(research, tid):
    return research["tasks"].setdefault(tid, {"task_id": tid, "definition": None,
        "inputs": None, "attempts": {}, "runtime": {"task_id": tid}})


def wave_node(research, number):
    wid = f"W{number:04d}"
    return research["waves"].setdefault(wid, {"wave_id": wid, "round_no": number,
        "rationale": "", "members": [], "status": "running", "updates": {}})


def insert(store, db, documents, kind, payload, meta):
    """Insert one immutable version; return an index reference without its body."""
    from colombo.brain.research_store import StoreError, now
    value = copy.deepcopy(payload)
    research = documents["research"]
    rid = kind + "-" + uuid.uuid4().hex
    revision = 1
    document = "research"
    event = meta.get("event_data") or {}

    def register(pointer, body, *, node_kind=kind, identifier=rid, rev=revision, doc=document):
        parent = documents[doc]
        for part in pointer[:-1]:
            parent = parent.setdefault(part, {})
        if pointer[-1] in parent and parent[pointer[-1]] is not None:
            raise StoreError("Fixed domain node already exists")
        parent[pointer[-1]] = body
        db.execute("INSERT INTO refs VALUES(?,?,?,?,?,?)",
                   (identifier, doc, json.dumps(pointer), rev, node_kind, now()))
        return {"id": identifier, "revision": rev}

    def assessment_owner(assessment_ref=None):
        if assessment_ref:
            row = store._row(db, assessment_ref)
            pointer = json.loads(row["pointer"])
            if row["node_type"] != "assessment":
                raise StoreError("Expected an assessment reference")
            return pointer[:-1]
        number = meta.get("round_no", 0)
        wave = wave_node(research, number)
        eid = event.get("id") or "E" + uuid.uuid4().hex
        ver = str(event.get("version", 1))
        update = wave["updates"].setdefault(eid, {"event_id": eid, "versions": {}})
        update["versions"].setdefault(ver, {"event_id": eid, "version": int(ver)})
        return ["waves", wave["wave_id"], "updates", eid, "versions", ver]

    if kind == "goal":
        return register(["goal", "definition"], value)
    if kind == "setting":
        return register(["goal", "setting_specification"], value)
    if kind == "review_package" and value.get("review_kind") == "result":
        result = store._read_row(store._row(db, value["result_ref"]), documents)
        return register(["tasks", result["task_id"], "attempts", result["attempt_id"], "review_packages", rid], value)
    if kind == "review" and value.get("review_kind") == "result":
        result = store._read_row(store._row(db, value["result_ref"]), documents)
        return register(["tasks", result["task_id"], "attempts", result["attempt_id"], "reviews", rid], value)
    if kind == "review_package" and value.get("review_kind") == "proof":
        return register(["versions", identity(value["proof_ref"]), "review_packages", rid], value, doc="proof_draft")
    if kind == "review" and value.get("review_kind") == "proof":
        context = (meta.get("pending_call") or {}).get("context", {})
        proof_ref = context.get("proof_ref", meta.get("integration", {}).get("proof_ref"))
        return register(["versions", identity(proof_ref), "reviews", rid], value, doc="proof_draft")
    if kind == "goal_progress":
        return register(["goal_progress", "versions", rid], value)
    if kind == "material":
        return register(["materials", rid], value)
    if kind == "note":
        previous = value.get("supersedes")
        revision = store._row(db, previous)["revision"] + 1 if previous else 1
        return register(["entries", rid], value, rev=revision, doc="working_notes")
    if kind == "audit":
        # The complete model input, including source text, is an external file.
        if "input" in value:
            relative = "audits/" + value.get("audit_id", rid) + "/input.json"
            from colombo.shared.file_io import atomic_write, json_bytes
            atomic_write(store.safe_path(relative), json_bytes(value.pop("input")))
            value["input_path"] = relative
        return register(["audits", rid], value)
    if kind == "conclusion":
        return register(["conclusion", rid], value)
    if kind == "proof_draft":
        revision = len(documents["proof_draft"]["versions"]) + 1
        return register(["versions", rid], value, rev=revision, doc="proof_draft")
    if kind == "plan":
        number = meta.get("planning_wave", meta.get("round_no", 0) + 1)
        wave = wave_node(research, number)
        next_id = meta.get("task_counter", 0)
        members = []
        for spec in value["tasks"]:
            if spec["mode"] == "new":
                next_id += 1
                tid, attempt = f"T{next_id:04d}", 1
                task = task_node(research, tid)
                definition = {k: v for k, v in spec.items() if k != "package"}
                dref = register(["tasks", tid, "definition"], definition,
                    node_kind="assignment", identifier="assignment-" + uuid.uuid4().hex)
                task.update(assignment_ref=dref, round_no=number, goal_ref=meta.get("goal_ref"), plan_ref={"id": rid, "revision": 1})
                task["research_mode"] = (meta.get("research_routing") or {}).get("research_mode", "generic")
                task["inputs"] = {"selection": copy.deepcopy(spec["package"]), "artifacts": []}
            else:
                tid = spec["resume_task_id"]
                task = task_node(research, tid)
                attempt = task["runtime"].get("attempt_no", 0) + 1
            aid = f"A{attempt:04d}"
            task["attempts"].setdefault(aid, {"attempt_id": aid, "wave_id": wave["wave_id"]})
            members.append({"task_id": tid, "attempt_id": aid, "attempt_no": attempt,
                            "resume": spec["mode"] != "new",
                            **({"restart": True} if spec["mode"] == "restart" else {}),
                            **({"specialization": spec["specialization"]} if "specialization" in spec else {})})
        wave["status"] = "running"
        wave["members"].extend(members)
        wave.setdefault("plans", {})[rid] = {"round_no": number, "members": members,
            "rationale": value["rationale"], **({"setting_specification": value["setting_specification"]} if "setting_specification" in value else {})}
        wave["dispatch_used"] = len(wave["members"])
        wave["rationale"] = value["rationale"]
        wave.setdefault("plan_ref", {"id": rid, "revision": 1})
        db.execute("INSERT INTO meta VALUES('task_counter',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (json.dumps(next_id),))
        # Index the structural plan, which contains task identities, not copies.
        db.execute("INSERT INTO refs VALUES(?,?,?,?,?,?)", (rid, "research",
            json.dumps(["waves", wave["wave_id"], "plans", rid]), 1, "plan", now()))
        return {"id": rid, "revision": 1}
    if kind == "assignment":
        tid = value["task_id"]
        task = task_node(research, tid)
        if task.get("assignment_ref"):
            if not json_equal(store._read_row(store._row(db, task["assignment_ref"]), documents), value):
                raise StoreError("Cannot replace a task definition")
            return task["assignment_ref"]
        spec = value["spec"]
        task.update({k: v for k, v in value.items() if k != "spec"})
        task["inputs"] = {"selection": copy.deepcopy(spec.get("package", {})), "artifacts": []}
        ref = register(["tasks", tid, "definition"], {k: v for k, v in spec.items() if k != "package"})
        task["assignment_ref"] = ref
        return ref
    if kind == "context_package":
        tid = value["task_id"]
        task = task_node(research, tid)
        old = task.get("inputs")
        if task.get("package_ref"):
            raise StoreError("Task inputs are already fixed")
        if old and not json_equal(old.get("selection"), value.get("selection")):
            raise StoreError("Package selection differs from its plan")
        task["inputs"] = None
        ref = register(["tasks", tid, "inputs"], {k: v for k, v in value.items() if k != "task_id"})
        task["package_ref"] = ref
        return ref
    if kind in {"result", "execution_fault"}:
        tid = value.get("task_id") or "source-" + rid
        aid = value.get("attempt_id") or "A0001"
        task = task_node(research, tid)
        attempt = task["attempts"].setdefault(aid, {"attempt_id": aid})
        if kind == "result":
            ref = register(["tasks", tid, "attempts", aid, "result"], value)
            attempt["result_ref"] = ref
        else:
            ref = register(["tasks", tid, "attempts", aid, "faults", rid], value)
        return ref
    if kind == "assessment":
        owner = assessment_owner()
        node = at(documents, "research", json.dumps(owner))
        if "assessment" in node:
            # Direct test callers may build multiple independent candidates.
            eid = "E" + uuid.uuid4().hex
            wave = research["waves"][owner[1]]
            wave["updates"][eid] = {"event_id": eid, "versions": {"1": {"event_id": eid, "version": 1}}}
            owner = ["waves", owner[1], "updates", eid, "versions", "1"]
            node = at(documents, "research", json.dumps(owner))
        if value.get("update", {}).get("proof_draft") is not None:
            proof = value["update"].pop("proof_draft")
            if "body_source" in proof:
                from colombo.brain.proof_draft import resolve_proof_source
                proof = resolve_proof_source(store, proof)
            proof_ref = insert(store, db, documents, "proof_draft", {"proof_draft": proof,
                "previous_ref": event.get("previous_proof_ref", meta.get("proof_ref")),
                "assessment_ref": {"id": rid, "revision": int(owner[-1])},
                "review_ref": None, "artifacts": [], "summary": proof.get("title", "")}, meta)
            value["update"]["proof_ref"] = proof_ref
            node["proof_candidate_ref"] = proof_ref
        ref = register(owner + ["assessment"], value, rev=int(owner[-1]))
        node.update(assessment_ref=ref, adoption_status="candidate")
        return ref
    if kind == "prune_decision":
        owner = assessment_owner(value.get("assessment_ref") or event.get("assessment_ref"))
        node = at(documents, "research", json.dumps(owner))
        if node.get("assessment", {}).get("prunes"):
            if "prune_index" in value:
                idx = value["prune_index"]
                matches = [(idx, node["assessment"]["prunes"][idx])] if type(idx) is int and 0 <= idx < len(node["assessment"]["prunes"]) else []
            else:
                matches = [(i, p) for i, p in enumerate(node["assessment"]["prunes"]) if p["task_id"] == value.get("task_id")]
            if len(matches) != 1:
                raise StoreError("Prune decision must identify exactly one candidate item")
            index, prune = matches[0]
            value = {k: v for k, v in value.items() if k not in prune}
            value["prune_index"] = index
        return register(owner + ["prune_decisions", rid], value)
    raise StoreError(f"Unsupported domain node: {kind}")


def read_node(store, row, documents, *, expand=True, replay=False):
    value = copy.deepcopy(at(documents, row["document"], row["pointer"]))
    pointer = json.loads(row["pointer"])
    kind = row["node_type"]
    research = documents["research"]
    if kind == "plan":
        tasks = []
        for member in value["members"]:
            task = research["tasks"][member["task_id"]]
            spec = {**copy.deepcopy(task["definition"]), "package": copy.deepcopy(task["inputs"]["selection"])}
            # A resume may explicitly spell the optional general default. Keep
            # that submission's JSON shape for idempotent receipt replay.
            if "specialization" in member:
                spec["specialization"] = member["specialization"]
            else:
                spec.pop("specialization", None)
            spec.update(mode="restart" if member.get("restart") else "resume" if member["resume"] else "new",
                        resume_task_id=member["task_id"] if member["resume"] else None)
            tasks.append(spec)
        return {"rationale": value["rationale"], "tasks": tasks,
                **({"setting_specification": value["setting_specification"]} if "setting_specification" in value else {})}
    if kind == "assignment":
        task = research["tasks"][pointer[1]]
        return {**{k: task[k] for k in ("task_id", "round_no", "goal_ref", "plan_ref", "research_mode") if k in task},
                "spec": {**value, "package": copy.deepcopy(task["inputs"]["selection"])}}
    if kind == "context_package":
        return {"task_id": pointer[1], **value}
    if kind == "assessment" and expand and value.get("update", {}).get("proof_ref"):
        proof_ref = value["update"].pop("proof_ref")
        proof = documents["proof_draft"]["versions"][identity(proof_ref)]
        value["update"]["proof_draft"] = copy.deepcopy(proof["proof_draft"])
        if replay and "body_source" in value["update"]["proof_draft"]:
            value["update"]["proof_draft"].pop("body")
    if kind == "goal_progress" and "progress" not in value and pointer[0] != "goal_progress":
        owner = at(documents, "research", json.dumps(pointer[:-2]))
        source = owner["assessment"].get("update", owner["assessment"])
        value["progress"] = copy.deepcopy(source["progress"])
    if kind in {"task_relation", "prune_decision"} and "prune_index" in value and not replay:
        owner = at(documents, "research", json.dumps(pointer[:-2]))
        prune = copy.deepcopy(owner["assessment"]["prunes"][value.pop("prune_index")])
        if kind == "prune_decision":
            value = {**prune, **value}
        else:
            value = {"target_task_id": prune["task_id"], "relation": prune["reason"],
                     "evidence_refs": prune["evidence_refs"], "explanation": prune["relation_explanation"],
                     "scope_check": prune["scope_check"], **value,
                     **({"audit_ref": prune["audit_ref"], "premises": prune["premises"],
                         "relation_review": "audit"} if prune.get("audit_ref") else {})}
    if kind == "proof_draft" and expand and value.get("assessment_ref") and not replay:
        # Adoption provenance lives on the candidate, keeping this proof body fixed.
        for wave in research["waves"].values():
            for update in wave["updates"].values():
                for version in update["versions"].values():
                    if (version.get("assessment_ref") == value["assessment_ref"]
                            and version.get("adoption_status") == "adopted"):
                        value["review_ref"] = version.get("review_ref")
    return value


def wave_history(research):
    return {wid: {"wave_id": wid, "round_no": w["round_no"], "plan_ref": w.get("plan_ref"),
        "task_runs": [{"task_id": m["task_id"], "attempt_id": m["attempt_id"]} for m in w["members"]],
        "status": w["status"], "assessments": [
            {key: copy.deepcopy(value) for key, value in version.items() if key in {
                "event_id", "version", "assessment_ref", "proof_candidate_ref", "review_package_ref", "review_ref",
                "review_verdict", "adoption_status", "progress_ref", "proof_ref", "processing_scope"}}
            for update in w["updates"].values() for version in update["versions"].values()
            if version.get("assessment_ref")]}
        for wid, w in research["waves"].items() if w.get("plan_ref")}


def apply_control(documents, meta, changes):
    """Apply lifecycle pointers beside immutable bodies in the writer transaction."""
    merged = {**meta, **changes}
    research = documents["research"]
    data = merged.get("round_data") or {}
    wid = f"W{data.get('round_no', 0):04d}"
    wave = research["waves"].get(wid)
    event = merged.get("event_data") or {}
    if wave and event.get("wave_id") == wid and event.get("assessment_ref"):
        for update in wave["updates"].values():
            for version in update["versions"].values():
                if (version.get("assessment_ref") == event["assessment_ref"]
                        and version["version"] == event["version"]):
                    for name in ("proof_candidate_ref", "review_package_ref", "review_ref", "review_verdict",
                                 "adoption_status", "progress_ref", "proof_ref", "processing_scope"):
                        if name in event:
                            version[name] = copy.deepcopy(event[name])
    if wave:
        phase = changes.get("phase")
        if phase == "planning":
            wave["status"] = "running" if merged.get("planning_wave") == wave["round_no"] else "finished"
        elif phase in {"integrating", "concluding", "done"}:
            wave["status"] = "finished"
        elif phase in {"preparing", "running"}:
            wave["status"] = "running"
    if "progress_ref" in changes:
        research["goal"]["current_progress_ref"] = changes["progress_ref"]
        research.setdefault("goal_progress", {})["current_ref"] = changes["progress_ref"]
    if "result_reviews" in changes:
        for rid, ref in changes["result_reviews"].items():
            for task in research["tasks"].values():
                for attempt in task["attempts"].values():
                    if identity(attempt.get("result_ref", "")) == rid:
                        attempt["review_ref"] = ref
    if "final_review_ref" in changes and merged.get("proof_ref"):
        documents["proof_draft"]["versions"][identity(merged["proof_ref"])]["review_ref"] = changes["final_review_ref"]
    if "proof_ref" in changes:
        documents["proof_draft"]["current_ref"] = changes["proof_ref"]


def wave_entries(meta):
    waves = meta.get("wave_history", {})
    ordered = sorted(waves.values(), key=lambda w: w["round_no"])
    active = [w for w in ordered if w["status"] == "running"]
    closed = [w for w in ordered if w["status"] == "finished"]
    return {"current_wave_id": active[-1]["wave_id"] if active else None,
            "previous_wave_id": closed[-1]["wave_id"] if closed else None,
            "latest_wave_id": ordered[-1]["wave_id"] if ordered else None,
            "waves": [{"wave_id": w["wave_id"], "round_no": w["round_no"],
                       "status": w["status"], "plan_ref": w["plan_ref"],
                       "task_runs": w["task_runs"]} for w in ordered]}



def unresolved_reviews(meta, read):
    """Expose existing review feedback until its returned results are resolved.

    This is a read projection, not another stored assessment or a retry queue.
    Keep feedback visible while a new result is being considered with old ones.
    """
    pending = [e for e in meta.get("result_events", [])
               if e["state"] in {"unconfirmed", "processing", "unreviewed_budget"}]
    if not pending:
        return []
    pending_refs = {identity(e["result_ref"]) for e in pending}
    latest = {}
    for wave in sorted(meta.get("wave_history", {}).values(), key=lambda w: w["round_no"]):
        for entry in wave["assessments"]:
            if not entry.get("review_ref") or entry.get("review_verdict") not in {"revise", "inconclusive"}:
                continue
            assessment = read(entry["assessment_ref"])
            for ref in assessment["result_refs"]:
                if identity(ref) in pending_refs:
                    # History is append-only. The latest failed review of each
                    # return stays relevant until a new judgment is adopted;
                    # even a later stale pass must not erase these findings.
                    latest[identity(ref)] = {**entry, "wave_id": wave["wave_id"]}
    groups = {}
    for event in pending:
        entry = latest.get(identity(event["result_ref"]))
        if entry:
            group = groups.setdefault(identity(entry["review_ref"]), {"entry": entry, "events": []})
            group["events"].append(event)
    feedback = []
    for group in groups.values():
        entry, events = group["entry"], group["events"]
        report = read(entry["review_ref"])
        feedback.append({"event_id": entry["event_id"], "wave_id": entry["wave_id"],
            "event_ids": [e["id"] for e in events],
            "result_refs": [e["result_ref"] for e in events],
            "task_runs": [{"task_id": e["task_id"], "attempt_id": e["attempt_id"]} for e in events],
            "assessment_ref": entry["assessment_ref"], "review_ref": entry["review_ref"],
            "review": report})
    return feedback


def state_view(store):
    from colombo.shared.runtime_budget import context as budget_context
    from colombo.brain.resume_eligibility import task_resume_eligibility
    goal = store.read_record(store.get_meta("goal_ref"))
    progress = store.get_meta("progress_ref")
    view = {"goal": goal, "goal_ref": store.get_meta("goal_ref"), "budget": budget_context(store.root),
            "research_mode_request": store.get_meta("research_mode_request", "generic"),
            "research_routing": store.get_meta("research_routing"),
            "confirmed_progress": store.read_record(progress) if progress else None,
            "progress_ref": progress, "round_no": store.get_meta("round_no", 0),
            "phase": store.get_meta("phase"), "status": store.get_meta("status"),
            "stop_reason": store.get_meta("stop_reason", ""),
            "tasks": store.list_tasks(), "limits": store.get_meta("config")["limits"],
            "dispatch_count": store.get_meta("dispatch_count", 0),
            "model_call_count": store.get_meta("model_call_count", 0),
            "unresolved_review_ref": store.get_meta("unresolved_review_ref"),
            "notes": store.note_directory(status="open")[:20],
            "notes_next_read": {"section": "notes", "offset": 0, "limit": 20}}
    for task in view["tasks"]:
        if task.get("state") in {"returned", "failed", "cancelled"}:
            task["resume_eligibility"] = task_resume_eligibility(store, task)
    if store.get_meta("config").get("workflow", {}).get("version", 1) in (2, 3):
        proof_ref = store.get_meta("proof_ref")
        proof_record = store.read_record(proof_ref) if proof_ref else None
        draft = proof_record["proof_draft"] if proof_record else None
        view.update(workflow_version=store.get_meta("config")["workflow"]["version"], proof_ref=proof_ref,
                    audit_call_count=store.get_meta("audit_call_count", 0),
                    proof_draft={key: value for key, value in draft.items() if key != "body"} if draft else None,
                    proof_revision_reviewed=bool(proof_record and proof_record.get("review_ref")),
                    result_events=store.get_meta("result_events", []),
                    prune_commands=store.get_meta("prune_commands", []),
                    execution_faults=[{"ref": task["execution_fault_ref"],
                                       "payload": store.read_record(task["execution_fault_ref"])}
                                      for task in view["tasks"] if task.get("execution_fault_ref")],
                    event_data=store.get_meta("event_data"))
        history = store.get_meta("wave_history", {})
        view.update(wave_entries({"wave_history": history}))
        view["unresolved_reviews"] = unresolved_reviews({"wave_history": history,
            "result_events": view["result_events"]}, store.read_record)
    if store.get_meta("config", {}).get("workflow", {}).get("version") == 3:
        view.update(setting_ref=store.get_meta("setting_ref"), result_reviews=store.get_meta("result_reviews", {}),
                    integration=store.get_meta("integration"), final_review_ref=store.get_meta("final_review_ref"))
        view["unresolved_reviews"] = [{"result_ref": rid, "review_ref": ref,
            "review": store.read_record(ref)} for rid, ref in view["result_reviews"].items()
            if store.read_record(ref).get("findings")]
    return view


def export_research(store):
    """Rebuild the current authoritative documents without a second state view."""
    store.export_documents()
    return store.read_document("research")


def research_page(store, section="overview", id=None, offset=0, limit=20):
    """Project authorized Brain navigation from current formal documents."""
    sections = {"overview", "goal", "tasks", "waves", "proof", "notes", "materials", "audits", "conclusion"}
    if section not in sections:
        raise ValueError("Unknown research section")
    if id is not None and (not isinstance(id, str) or not id):
        raise ValueError("id must be a nonempty string")

    def page(items, **extra):
        total = len(items)
        next_offset = offset + limit if offset + limit < total else None
        return {**extra, "items": items[offset:offset + limit], "offset": offset,
                "total": total, "next_offset": next_offset,
                "next": {"section": section, **({"id": id} if id else {}),
                         "offset": next_offset, "limit": limit} if next_offset is not None else None}

    if section == "overview":
        if id is not None:
            raise ValueError("overview does not accept an id")
        state = state_view(store)
        keys = ("goal", "goal_ref", "progress_ref", "phase", "status", "stop_reason", "round_no",
                "research_mode_request", "research_routing",
                "proof_ref", "proof_revision_reviewed", "limits", "dispatch_count", "model_call_count",
                "audit_call_count", "current_wave_id", "previous_wave_id", "latest_wave_id",
                "unresolved_reviews")
        overview = {key: state.get(key) for key in keys}
        progress = state.get("confirmed_progress")
        overview["confirmed_progress"] = progress.get("progress") if progress else None
        overview["proof_index"] = state.get("proof_draft")
        overview["notes"] = state.get("notes", [])
        overview["notes_next_read"] = state["notes_next_read"]
        overview["pending_returns"] = [e for e in state.get("result_events", [])
                                       if e.get("state") not in {"processed", "processed_cancellation"}]
        overview["prune_commands"] = [{k: command[k] for k in
            ("id", "state", "task_id", "attempt_id", "decision_ref") if k in command}
            for command in state.get("prune_commands", [])]
        overview["execution_faults"] = [{"ref": fault["ref"], **{k: fault["payload"][k] for k in
            ("task_id", "attempt_id", "kind", "error_type", "summary", "termination_confirmed")
            if k in fault["payload"]}} for fault in state.get("execution_faults", [])]
        task_keys = ("task_id", "title", "state", "active_attempt", "assignment_ref", "package_ref",
                     "latest_result_ref", "execution_fault_ref", "resume_eligibility")
        tasks = [{k: t[k] for k in task_keys if k in t} for t in state["tasks"]]
        return page(tasks, section=section, **overview)
    if section == "goal":
        if id is not None:
            raise ValueError("goal uses its returned fixed ref, not id navigation")
        record = store.get_meta("goal_ref")
        return {"section": section, "ref": record, "payload": store.public_read(record),
                "progress_ref": store.get_meta("progress_ref"),
                "setting_ref": store.get_meta("setting_ref")}
    if section in {"tasks", "waves"}:
        nodes = store.read_document("research")[section]
        if id is None:
            return page([{"id": key, **({"runtime": node["runtime"], "assignment_ref": node.get("assignment_ref")}
                if section == "tasks" else {k: node[k] for k in ("wave_id", "round_no", "status", "dispatch_used") if k in node})}
                for key, node in nodes.items()], section=section)
        if id not in nodes:
            raise ValueError("Unknown research identity")
        node = nodes[id]
        if section == "tasks":
            return page(list(node["attempts"].values()), section=section,
                task={k: v for k, v in node.items() if k != "attempts"})
        return page(list(node.get("plans", {}).values()), section=section,
            wave={k: v for k, v in node.items() if k != "plans"})
    if section == "notes" and id is None:
        return page(store.note_directory(), section=section)
    kinds = {"proof": "proof_draft", "notes": "note", "materials": "material",
             "audits": "audit", "conclusion": "conclusion"}
    kind = kinds[section]
    if id is not None:
        record = store.record_ref(id)
        if store.record_kind(record) != kind:
            raise ValueError("Reference does not belong to this research section")
        return {"section": section, "ref": record, "payload": store.public_read(record)}
    refs = store.retrieve(kind, limit=limit + 1, offset=offset)
    more = len(refs) > limit
    result = {"section": section, "items": refs[:limit], "offset": offset,
              "total": store.reference_count(kind),
              "next_offset": offset + limit if more else None,
              "next": {"section": section, "offset": offset + limit, "limit": limit} if more else None}
    if section == "proof":
        current = store.get_meta("proof_ref")
        result.update(ref=current, payload=store.public_read(current) if current else None)
    elif section == "conclusion":
        current = store.get_meta("conclusion_ref")
        result.update(ref=current, payload=store.public_read(current) if current else None)
    return result
