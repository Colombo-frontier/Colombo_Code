"""Actual Host navigation, bounded pages, pinned snapshots, and role isolation."""
import pytest

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.core.store import dumps
from test_draft_clone import context, host


def make(h, value):
    return h.call("draft_create", {"kind": "profile", "initial_json": dumps(value)}, "create")


def test_outline_to_batch_to_local_patch(context):
    h = host(context, {})
    draft = make(h, {"bounds": [{"bound_id": "B1", "claim": "x" * 5000}, {"bound_id": "B2", "claim": "y"}], "a/b~c": {"id": "escaped"}})
    root = h.call("draft_outline", {"draft_id": draft["draft_id"], "pointer": "", "offset": 0, "limit": 50}, "root")
    assert "/a~1b~0c" in {row["pointer"] for row in root["items"]}
    listing = h.call("draft_outline", {"draft_id": draft["draft_id"], "pointer": "/bounds", "offset": 0, "limit": 1}, "bounds")
    assert listing["items"] == [{"pointer": "/bounds/0", "type": "object", "length": 2, "ids": {"bound_id": "B1"}}]
    assert listing["next_offset"] == 1 and "claim" not in dumps(listing)
    args = {"draft_id": draft["draft_id"], "revision": listing["revision"], "requests": [
        {"pointer": "/bounds/0/claim", "offset": 10, "limit": 20},
        {"pointer": "/a~1b~0c", "offset": 0, "limit": 1000}]}
    result = h.call("draft_read_batch", args, "batch")
    assert result["items"][0]["next_offset"] == 30
    assert result["items"][1]["data"] == {"id": "escaped"}
    h.call("draft_patch", {"draft_id": draft["draft_id"], "revision": result["revision"], "patches_json": dumps([{"op":"replace", "path":"/bounds/1/claim", "value":"new"}])}, "patch")
    with pytest.raises(ProtocolError, match="revision changed"):
        h.call("draft_read_batch", args, "stale")
    assert h.ws.draft(draft["draft_id"], h.job["id"])["data"]["bounds"][0]["claim"] == "x" * 5000


def test_batch_one_snapshot_shared_budget_and_complete_scalar(context):
    h = host(context, {})
    h.cap = 1800
    draft = make(h, {"long": '\\"\n' * 10000, "tiny": True})
    requests = [{"pointer": "/long", "offset": 0, "limit": 20000}, {"pointer": "/tiny", "offset": 0, "limit": 20000}]
    original = h._draft
    calls = []
    def one_read(ident):
        calls.append(ident)
        return original(ident)
    h._draft = one_read
    result = h.call("draft_read_batch", {"draft_id": draft["draft_id"], "revision": 0, "requests": requests}, "escaped")
    assert calls == [draft["draft_id"]]
    assert len(dumps(result)) <= h.cap
    assert result["items"][1]["data"] is True
    assert result["items"][0]["next_offset"] > 0


def test_navigation_never_exposes_other_job_drafts(context):
    producer = host(context, {})
    draft = make(producer, {"private": "producer private notes"})
    reviewer = host(context, {}, "profile_reviewer")
    for name, args in [("draft_outline", {"pointer":"", "offset":0,"limit":10}),
                       ("draft_read_batch", {"revision":0, "requests":[{"pointer":"", "offset":0,"limit":1000}]})]:
        with pytest.raises(ProtocolError):
            reviewer.call(name, {"draft_id":draft["draft_id"], **args}, name)
    assert not reviewer.grants


@pytest.mark.parametrize("revision,requests", [(True, [{"pointer":"", "offset":0,"limit":10}]), (0, []),
    (0, [{"pointer":"", "offset":0,"limit":10}] * 9), (0, [{"pointer":"", "offset":False,"limit":10}]),
    (0, [{"pointer":"", "offset":0,"limit":10,"extra":"no"}])])
def test_batch_rejects_invalid_shape_before_returning_any_content(context, revision, requests):
    h = host(context, {})
    draft = make(h, {"secret": "fixture"})
    with pytest.raises(ProtocolError):
        h.call("draft_read_batch", {"draft_id":draft["draft_id"],"revision":revision,"requests":requests}, "invalid")
