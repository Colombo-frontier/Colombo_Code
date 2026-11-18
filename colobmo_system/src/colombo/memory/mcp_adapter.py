"""Builtin read-only Memory interface on the existing research MCP servers."""
from __future__ import annotations
import json
from pathlib import Path
from .contracts import ContractError
from .retrieval import Reader
from .store import Store

class ScopedReader:
    """Capability projection is applied before retrieval, paging and link expansion."""
    def __init__(self, root: str | Path, *, allowed_kinds: set[str] | None = None):
        self.reader = Reader(Store(root), allowed_kinds=allowed_kinds); self.allowed_kinds = allowed_kinds

    def call(self, mode: str, **kwargs):
        if mode in {"read", "expand"}:
            ref = kwargs.get("ref")
            if isinstance(ref, dict) and ("index_version" in ref or ("version" in ref and "revision" not in ref)):
                raise ContractError(
                    "legacy_ref_retired: this historical Recollect reference is not a current Memory reference. "
                    "Use its frozen research material or the hash-verified legacy archive; no automatic mapping is performed."
                )
        allowed = self.allowed_kinds
        if allowed is None:
            return self.reader.call(mode, **kwargs)
        if mode in {"search", "browse"}:
            requested = set(kwargs.pop("kinds", allowed))
            if not requested.issubset(allowed):
                raise ContractError("Kind is not authorized in this research mode")
            kwargs["kinds"] = sorted(requested)
        elif mode in {"read", "expand"}:
            # Do not trust the user-supplied ref.kind; inspect the actual record.
            record = self.reader._record(kwargs["ref"])
            if record["kind"] not in allowed:
                raise ContractError("Record kind is not authorized")
            if mode == "expand":
                # Project before pagination, rather than returning unauthorized counts/IDs.
                limit, offset = kwargs.pop("limit", 12), kwargs.pop("offset", 0)
                all_items = []; pos = 0
                while True:
                    page = self.reader.expand(**kwargs, offset=pos, limit=50)
                    for item in page["items"]:
                        if item.get("ref", {}).get("kind") in allowed:
                            all_items.append(item)
                    if page["next_offset"] is None: break
                    pos = page["next_offset"]
                if not 1 <= limit <= 50 or offset < 0: raise ContractError("Invalid expansion window")
                return {"items": all_items[offset:offset+limit], "next_offset": offset+limit if offset+limit < len(all_items) else None}
        elif mode == "overview":
            original = self.reader._cards
            # Separate view, not a mutation of shared state.
            local = Reader(self.reader.store)
            local._cards = lambda include_leads, query="": [(c,s) for c,s in original(include_leads,query) if c["ref"]["kind"] in allowed]
            return local.overview(**kwargs)
        return self.reader.call(mode, **kwargs)

def register_memory(mcp, *, memory_root: str | Path, research_mode: str = "oracle_complexity") -> None:
    # Preserve Colombo's generic-mode theorem-only permission.
    allowed = {"theorem"} if research_mode == "generic" else None
    if research_mode not in {"generic", "oracle_complexity"}:
        raise ContractError("Unknown research mode; define its capabilities explicitly")
    service = ScopedReader(memory_root, allowed_kinds=allowed)
    @mcp.tool(name="scientific_memory", annotations={"readOnlyHint": True, "idempotentHint": True, "destructiveHint": False})
    def scientific_memory(mode: str, arguments_json: str = "{}") -> dict:
        """Read-only overview/browse/search/read/expand. Search never proves applicability."""
        args = json.loads(arguments_json)
        if not isinstance(args, dict): raise ContractError("arguments_json must decode to an object")
        return service.call(mode, **args)
