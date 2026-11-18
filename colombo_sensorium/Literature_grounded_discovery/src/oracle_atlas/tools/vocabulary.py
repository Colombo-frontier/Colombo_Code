"""Find registered alternatives for several source terms in one vocabulary snapshot."""
import re

from ..atlas.tags import AXES, vocabulary_index
from ..core.contracts import ProtocolError
from ..core.store import digest, dumps


def _terms(value):
    return " ".join(re.findall(r"[^\W_]+", value.casefold(), re.UNICODE))


def lookup_batch(vocabulary, queries, limit, budget):
    if not isinstance(queries, list) or not 1 <= len(queries) <= 16:
        raise ProtocolError("Provide 1 to 16 vocabulary queries")
    if type(limit) is not int or not 1 <= limit <= 12:
        raise ProtocolError("Per-query limit must be 1 to 12")
    index = vocabulary_index(vocabulary)
    sections = {section: vocabulary_index(vocabulary[section])
                for section in ("human", "machine") if section in vocabulary}
    entries = []
    for cid, row in sorted(index.items()):
        aliases = row.get("aliases") or []
        fields = [row.get("label"), row.get("value"), *aliases, cid.rsplit(":", 1)[-1]]
        names = {_terms(s) for s in fields if isinstance(s, str) and s.strip()}
        item = {"id": cid, "label": row.get("label", cid),
                "catalogs": [s for s, ids in sections.items() if cid in ids]}
        entries.append((cid, row.get("axis") or cid.split(":")[0], names, item))

    output = {"vocabulary_hash": digest(vocabulary), "results": []}
    pages = []
    for query in queries:
        term, axis, offset = query["term"], query["axis"], query["offset"]
        if not isinstance(term, str) or not term.strip() or len(term) > 160:
            raise ProtocolError("Each term must have 1 to 160 characters; use vocabulary_lookup for catalog browsing")
        if not isinstance(axis, str) or (axis and axis.upper() not in AXES):
            raise ProtocolError("Provide a known axis or an empty string")
        if type(offset) is not int or offset < 0:
            raise ProtocolError("Each offset must be a nonnegative integer")
        term = term.strip()
        axis = axis.upper()
        needle = _terms(term)
        tokens = set(needle.split())
        ranked = []
        for cid, axis_id, names, item in entries:
            if axis and axis_id != axis:
                continue
            if cid.casefold() == term.casefold():
                rank = 0
            elif ":" in term or not needle:
                continue
            elif needle in names:
                rank = 1
            elif any(tokens <= set(name.split()) for name in names):
                rank = 2
            else:
                continue
            ranked.append((rank, cid, item))
        ranked.sort(key=lambda hit: (hit[0], hit[1]))
        total = len(ranked)
        result = {"term": term, "axis": axis, "total": total, "matches": [],
                  "next_offset": offset if offset < total else None}
        output["results"].append(result)
        pages.append((result, offset, ranked[offset:offset + limit]))

    # Share the reply across terms, never return an unmarked truncated candidate list.
    for i in range(limit):
        for result, offset, hits in pages:
            if i >= len(hits) or len(result["matches"]) != i:
                continue
            result["matches"].append(hits[i][2])
            following = offset + i + 1
            result["next_offset"] = following if following < result["total"] else None
            if len(dumps(output)) > budget:
                result["matches"].pop()
                result["next_offset"] = following - 1
    if len(dumps(output)) > budget or any(hits and not row["matches"] for row, _, hits in pages):
        raise ProtocolError("Tool output budget too small for one result per term; split the batch")
    return output
