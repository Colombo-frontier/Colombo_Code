import pytest
from jsonschema import Draft202012Validator

from oracle_atlas.atlas.tags import vocabulary_index
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import Workspace, dumps
from oracle_atlas.tools.host import ToolHost
from oracle_atlas.tools.vocabulary import lookup_batch


def concept(cid, label, **extra):
    return {"concept_id": cid, "axis": cid.split(":")[0], "label": label, **extra}


def query(term, axis="", offset=0):
    return {"term": term, "axis": axis, "offset": offset}


def test_extraction_tools_find_scoped_human_and_machine_alternatives(tmp_path):
    human_id = "TASK:family:matrix_computation"
    machine_id = "TASK:task_family:matrix_computation"
    oracle_id = "ORACLE:quality:exact"
    vocab = {"human": {"concepts": [concept(human_id, "Matrix computation", aliases=["Matrix calculations"]),
                                     concept(oracle_id, "Exact")]},
             "machine": {"concepts": [concept(machine_id, "Matrix computation"),
                                       concept("MODEL:promise:exact", "Exact")]}}

    class AtlasFixture:
        reads = 0

        def vocabulary(self):
            self.reads += 1
            return vocab

    atlas, ws = AtlasFixture(), Workspace(tmp_path)
    try:
        for role in ("extractor", "extraction_reviewer"):
            host = ToolHost(ws, atlas, ws.job(ws.create_job(role, {})), {"budgets": DEFAULTS})
            spec = next(d for d in host.definitions() if d["name"] == "vocabulary_lookup_batch")
            args = {"queries": [query("matrix-computation", "task"), query("Exact", "ORACLE"),
                                query("unlisted"), query("Matrix calculations"), query("MODEL:wrong:exact")], "limit": 6}
            Draft202012Validator(spec["parameters"]).validate(args)
            result = host.call(spec["name"], args, "batch")["results"]
            assert [(v["id"], v["catalogs"]) for v in result[0]["matches"]] == [
                (human_id, ["human"]), (machine_id, ["machine"])]
            assert [v["id"] for v in result[1]["matches"]] == [oracle_id]
            assert result[2]["total"] == 0 and result[3]["matches"][0]["id"] == human_id
            assert result[4]["matches"] == []
        assert atlas.reads == 2
    finally:
        ws.close()


def test_pagination_does_not_hide_other_terms_or_join_across_axes():
    vocab = {"concepts": [concept(f"ORACLE:quality:exact_{i}", f"Exact oracle {i}") for i in range(40)]}
    args = [query("Exact", "oracle"), query("exact", "task")]
    first = lookup_batch(vocab, args, 12, 750)
    assert len(dumps(first)) <= 750
    result = first["results"][0]
    assert first["results"][1]["matches"] == [] and 0 < result["next_offset"] < 12
    seen = []
    while True:
        seen += [r["id"] for r in result["matches"]]
        if result["next_offset"] is None:
            break
        args[0]["offset"] = result["next_offset"]
        result = lookup_batch(vocab, args, 12, 750)["results"][0]
    assert seen == sorted(vocabulary_index(vocab))
    with pytest.raises(ProtocolError):
        lookup_batch(vocab, [query("exact")] * 17, 4, 12000)
    with pytest.raises(ProtocolError):
        lookup_batch(vocab, [query("exact", "alternative")], 4, 12000)
