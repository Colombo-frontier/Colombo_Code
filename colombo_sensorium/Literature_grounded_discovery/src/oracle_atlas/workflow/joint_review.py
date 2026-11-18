"""Bind current scientific assessments to the exact archived subject and baseline."""
import json

from ..core.contracts import ProtocolError, schema
from ..core.store import digest


def delivered_pages(workspace, job_id):
    """Only count pages delivered to this job. An archived-result pointer is not a read."""
    for entry in workspace.query(
        "SELECT name,args,result FROM tool_calls WHERE job=? AND status='done' "
        "AND name IN ('artifact_get','source_read','read_batch')", (job_id,)
    ):
        args, result = json.loads(entry["args"]), json.loads(entry["result"])
        if entry["name"] == "read_batch":
            for operation, row in zip(args["requests"], result.get("items", [])):
                if "result" in row:
                    yield operation["tool"], operation["arguments"], row["result"]
        else:
            yield entry["name"], args, result


def require_frozen_analysis_read(workspace, job_id, subject):
    """Accept whole-object reads and contiguous pages, including reads of enclosing objects."""
    if subject["kind"] == "proposal":
        proposal = subject["data"]
        prepared = workspace.artifacts.get(proposal["prepared_ref"])["data"]
        analysis = prepared["files"]["profile.json"]["joint_analysis"]
        targets = {proposal["prepared_ref"]: "/files/profile.json/joint_analysis"}
        authored = workspace.artifacts.get(proposal["profile_ref"])["data"]
        if digest(authored.get("joint_analysis")) == digest(analysis):
            targets[proposal["profile_ref"]] = "/joint_analysis"
    else:
        targets = {subject["ref"]: "/joint_analysis"}
    intervals = {}
    complete = set()
    for name, args, page in delivered_pages(workspace, job_id):
        ref, pointer = args.get("ref"), args.get("pointer", "")
        if name != "artifact_get" or ref not in targets or "total_chars" not in page:
            continue
        key = (ref, pointer)
        end = page["next_offset"] if page["next_offset"] is not None else page["total_chars"]
        intervals.setdefault(key, []).append((page["offset"], end, page["total_chars"]))
    for (ref, pointer), segments in intervals.items():
        cursor = 0
        for begin, end, total in sorted(segments):
            if begin > cursor:
                break
            cursor = max(cursor, end)
            if cursor == total:
                complete.add((ref, pointer))
    def covered(value, ref, path):
        if any(r == ref and (p == path or path.startswith(p + "/")) for r, p in complete):
            return True
        if isinstance(value, (dict, list)) and value:
            items = value.items() if isinstance(value, dict) else enumerate(value)
            return all(covered(child, ref, path + "/" + str(k).replace("~","~0").replace("/","~1")) for k, child in items)
        return False
    if subject["kind"] != "proposal":
        analysis = subject["data"]["joint_analysis"]
    if not any(covered(analysis, ref, path) for ref, path in targets.items()):
        raise ProtocolError("Read the frozen joint_analysis in full before approval. Use artifact_get on the prepared profile or the identical frozen profile, following next_offset through the last page.")


def require_finite_literature(workspace, job_id, research):
    analysis = research.get("joint_analysis") if research["action"] == "no_change" else workspace.artifacts.get(research["profile_ref"])["data"].get("joint_analysis")
    if not analysis or analysis["synthesis_coverage"]["literature"]["status"] != "finite_scope_complete":
        return
    scope = research.get("literature_scope")
    if not scope or not scope["source_refs"] or scope["unresolved_leads"]:
        raise ProtocolError("A completed finite literature scope requires pinned sources and no outstanding leads within that scope.")
    if scope["mode"] == "bounded_search" and not scope["search_refs"]:
        raise ProtocolError("A completed bibliographic search must cite its archived searches.")
    for ref in scope["search_refs"]:
        if workspace.artifacts.get(ref)["kind"] != "search":
            raise ProtocolError("literature_scope.search_refs must be actual search records.")
    seen = set()
    for name, args, page in delivered_pages(workspace, job_id):
        if (name == "source_read" or (name == "artifact_get" and args.get("pointer") in ("", "/text"))) and page.get("total_chars", 0) and ("data" in page or page.get("text")):
            seen.add(args["ref"])
    if any(workspace.artifacts.get(ref)["kind"] != "source" or ref not in seen for ref in scope["source_refs"]):
        raise ProtocolError("Each completed-scope source needs a pinned original source and an actual read in this research job.")


def require_joint_checks(review):
    checks = review.get("joint_checks")
    required = schema("review")["properties"]["joint_checks"]["required"]
    if not isinstance(checks, dict) or set(checks) != set(required):
        raise ProtocolError("An independent scientific approval requires all six joint_checks.")
    if any(checks[name] is not True for name in required):
        raise ProtocolError("A failed independent joint check requires revise or defer.")


def validate_no_change(atlas, research):
    from ..atlas.scientific import validate_profile_science

    sid = research["setting_id"]
    version = research["base_version"]
    if version is None or atlas.version(sid) != version:
        raise ProtocolError("A no_change assessment requires the current pinned existing baseline.")
    baseline = atlas.read(sid)
    if atlas.version(sid) != version:
        raise ProtocolError("The no_change baseline changed while it was read.")
    validate_profile_science({**baseline, "joint_analysis": research.get("joint_analysis")},
                             baseline, no_change=True)
