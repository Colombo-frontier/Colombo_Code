"""A new review contract cannot bypass either boundary by omitting its context inputs."""
from copy import deepcopy

import pytest

from oracle_atlas.core.contracts import ProtocolError
from oracle_atlas.tools.host import ToolHost
from test_pipeline_demo import DEMO


@pytest.mark.parametrize("missing,code", [("proof_context_ref", "proof_context_missing"),
                                          ("review_context_ref", "bound_context_missing")])
def test_current_contract_rejects_missing_catalog_at_host_and_engine(tmp_path, missing, code):
    engine, _, _, request = DEMO.setup_demo(tmp_path)
    try:
        run = engine.scan(request)
        case = engine.ws.case(run["cases"][0])
        assert case["state"] == "committed"
        job = deepcopy(engine.ws.job(case["jobs"]["profile_reviewer"]))
        assert job["inputs"]["issue_scope_contract_version"] == "occurrence-bound-scope"
        review = engine.artifacts.get(case["profile_review_ref"])["data"]
        # This really is a completed, otherwise valid review with actual exact
        # execution receipts. Removing one input is the only mutation.
        job["inputs"].pop(missing)
        host = ToolHost(engine.ws, engine.atlas, job, engine.config)
        _, errors, _ = host._validate_artifact("review", review)
        assert code in {row["code"] for row in errors}
        with pytest.raises(ProtocolError, match="missing catalogs cannot disable validation"):
            engine._validate_stage(job, job["output"])
    finally:
        engine.ws.close()
