"""Select a frozen partial draft from a specific interrupted producer handoff."""
import json

from ..core.contracts import ProtocolError
from ..core.store import digest


def partial_clone_source(workspace, role, inputs):
    job_id = inputs.get("resume_producer_job_id")
    work = inputs.get("prior_unreviewed_work_refs", [])
    if not job_id or not work or role not in {"profile_researcher", "bound_updater"}:
        return None
    try:
        prior = workspace.job(job_id)
        output = prior.get("output") or {}
        if prior["role"] != role or prior["status"] != "needs_materials" or output.get("status") != "needs_materials":
            return None
        fields = ("candidate_ref", "identity_ref", "setting_id", "base_version", "budget_scope", "transfer_scope_ref")
        if any(prior["inputs"].get(k) != inputs.get(k) for k in fields):
            return None
        artifacts = workspace.artifacts
        candidates = {ref for ref in work if artifacts.get(ref)["kind"] == "research"}
        produced = {ref for ref in output["artifact_refs"] if artifacts.get(ref)["kind"] == "research"}
        if len(produced) != 1 or produced != candidates:
            return None
        research_ref = next(iter(produced))
        events = workspace.query("SELECT payload FROM events WHERE job=? AND event='validated_handoff'", (job_id,))
        if not any((event := json.loads(row["payload"])).get("status") == "needs_materials" and
                   research_ref in event.get("refs", []) for row in events):
            return None
        research = artifacts.get(research_ref)["data"]
        if not artifacts.owned(research_ref, job_id) or not research.get("profile_ref"):
            return None
        if any(research[k] != inputs.get(k) for k in ("candidate_ref", "identity_ref", "base_version")):
            return None
        if research["action"] != {"bound_updater": "update", "profile_researcher": "new"}[role]:
            return None
        sid = research["setting_id"]
        if inputs.get("setting_id") is not None and inputs["setting_id"] != sid:
            return None
        if inputs.get("previous_artifact_ref"):
            anchor = artifacts.get(inputs["previous_artifact_ref"])
            if anchor["kind"] == "research" and anchor["data"]["setting_id"] != sid:
                return None
        profile_ref = research["profile_ref"]
        profile = artifacts.get(profile_ref)
        if profile["kind"] != "profile" or profile["data"]["setting_id"] != sid or not artifacts.owned(profile_ref, job_id):
            return None
        return {"source_ref": profile_ref, "source_pointer": "", "expected_digest": digest(profile["data"])}
    except (ProtocolError, KeyError, TypeError, ValueError):
        # The established pre-revision or native clone path still applies.
        return None
