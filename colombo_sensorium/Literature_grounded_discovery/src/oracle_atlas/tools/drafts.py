"""Bounded structural navigation over one authorized, revision-pinned draft snapshot."""
from __future__ import annotations

from ..core.contracts import ProtocolError, resolve_pointer
from ..core.store import bounded, dumps

ID_KEYS = ("id", "bound_id", "view_id", "regime_id", "comparison_id", "obligation_id", "operation_id", "parameter_id", "evidence_id")


def _type(value):
    if value is None: return "null"
    if isinstance(value, bool): return "boolean"
    if isinstance(value, dict): return "object"
    if isinstance(value, list): return "array"
    if isinstance(value, str): return "string"
    return "number"


def _header(draft, revision):
    if isinstance(revision, bool) or not isinstance(revision, int) or revision != draft["revision"]:
        raise ProtocolError("Draft revision changed; obtain its current revision and reread before combining pages.")
    return {"draft_id": draft["id"], "revision": draft["revision"], "kind": draft["kind"]}


def outline(draft, pointer, offset, limit, cap):
    if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0 or isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ProtocolError("offset/limit out of range")
    value = resolve_pointer(draft["data"], pointer)
    entries = list(value.items()) if isinstance(value, dict) else list(enumerate(value)) if isinstance(value, list) else []
    out = {**_header(draft, draft["revision"]), "pointer": pointer, "type": _type(value), "items": [], "total": len(entries), "next_offset": None}
    for key, child in entries[offset:offset + min(limit, 50)]:
        path = pointer + "/" + str(key).replace("~", "~0").replace("/", "~1")
        row = {"pointer": path, "type": _type(child)}
        if isinstance(child, (dict, list, str)): row["length"] = len(child)
        if isinstance(child, dict):
            row["ids"] = {k: child[k] for k in ID_KEYS if k in child and isinstance(child[k], (str, int)) and not isinstance(child[k], bool)}
        out["items"].append(row)
        out["next_offset"] = offset + len(out["items"]) if offset + len(out["items"]) < len(entries) else None
        if len(dumps(out)) > cap:
            out["items"].pop()
            out["next_offset"] = offset + len(out["items"])
            if not out["items"]: raise ProtocolError("This structural entry exceeds the response budget; read the known pointer directly.")
            break
    return out


def read_batch(draft, revision, requests, cap):
    header = _header(draft, revision)
    if not isinstance(requests, list) or not 1 <= len(requests) <= 8:
        raise ProtocolError("Read 1 to 8 draft pointers in one batch.")
    # All values come from the same single Workspace.draft read. No further SQL
    # reads, child tool calls, or dependency expansion occur inside this batch.
    page_cap = (cap - len(dumps(header)) - 256) // len(requests) - 256
    if page_cap < 1: raise ProtocolError("The response budget cannot accommodate this draft batch.")
    items = []
    for req in requests:
        if not isinstance(req, dict) or set(req) != {"pointer", "offset", "limit"} or not isinstance(req["pointer"], str):
            raise ProtocolError("Each draft read needs only pointer, offset, and limit.")
        offset, limit = req["offset"], req["limit"]
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0 or isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ProtocolError("offset/limit out of range")
        value = resolve_pointer(draft["data"], req["pointer"])
        items.append({"pointer": req["pointer"], **bounded(value, offset, min(limit, page_cap))})
    out = {**header, "items": items, "count": len(items), "per_item_limit": page_cap}
    while len(dumps(out)) > cap:
        # Escaped JSON strings can occupy more than their source character count.
        # Re-page already selected values with a smaller cap; never archive a
        # changing draft under an implicitly authorized immutable artifact.
        if page_cap == 1: raise ProtocolError("Draft batch metadata exceeds the response budget; request fewer or shorter pointers.")
        page_cap = max(1, page_cap // 2)
        out["items"] = [{"pointer": req["pointer"], **bounded(resolve_pointer(draft["data"], req["pointer"]), req["offset"], min(req["limit"], page_cap))} for req in requests]
        out["per_item_limit"] = page_cap
    return out
