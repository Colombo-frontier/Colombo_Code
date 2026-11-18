"""Schema-only routing stubs; never use these to approve a prepared proposal."""
from oracle_atlas.science.joint import JOINT_CHECKS


def routing_joint_review(verdict="defer"):
    """Keep unrelated routing tests schema-valid without asserting science.

    Zero hashes deliberately bind no real prepared bundle. Actual proposal and
    writer tests must use the exact snapshot's hashes and independent checks.
    """
    return {"prepared_hash": "0" * 64, "analysis_hash": "0" * 64,
            "science_context_hash": "0" * 64,
            "checks": [{"check_id": name, "verdict": verdict,
                        "reason": "Schema-only synthetic routing stub; no proposal or mathematical approval."}
                       for name in JOINT_CHECKS]}
