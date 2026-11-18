"""Optional hooks for another component's NEW-profile authoring pipeline.

The maintenance entry point is already wired. These hooks do not monkey-patch
the separately distributed oracle_atlas_agents dependency or grant publication.
"""
from copy import deepcopy
import hashlib
from pathlib import Path

from .joint import validate_joint_analysis


def authoring_standard():
    text = (Path(__file__).parent / "resources" / "joint_parameter_standard.md").read_text("utf-8")
    science = text.split("## 6. Handoff", 1)[0]
    from .taxonomy import status_contract
    import json
    status_text = json.dumps(status_contract(), ensure_ascii=False, sort_keys=True, indent=2)
    return science + "\n## Canonical machine status contract\n\n" + status_text + "\n\n" + """## New-profile output

Preserve the native profile and handoff formats of the calling component. Put
the synthesis object in profile.joint_analysis, using the joint_analysis.schema.json
format. The controller supplies that schema through its existing schema/resource
route. Resolve the joint target and constant conventions, account for the full
domain including explicitly unassessed cells, and require source/transfer/analyst
provenance for every adopted claim. A new profile has no accepted scientific
baseline: do not use retained_baseline as evidence. Impacts against an old profile
are unnecessary for first creation. Independent scientific review and native
publication remain required after structural validation.
"""


def extend_authoring_instructions(text, manifest):
    """Append the actual shared text and rebind the calling instruction manifest."""
    extra = authoring_standard()
    updated = deepcopy(manifest)
    output = text + "\n\n" + extra
    updated.setdefault("loaded", []).append({"path": "oracle_atlas_maintenance:joint_parameter_standard",
        "sha256": hashlib.sha256(extra.encode()).hexdigest()})
    updated["instructions_sha256"] = hashlib.sha256(output.encode()).hexdigest()
    updated["chars"] = len(output)
    updated.pop("contract_version", None)
    from .state import digest
    updated["contract_version"] = digest(updated)
    return output, updated


def validate_new_profile(profile):
    """Structural gate for new profiles; does not replace a scientific reviewer."""
    from .taxonomy import validate_status_taxonomy
    validate_status_taxonomy(profile)
    analysis = profile.get("joint_analysis")
    if analysis is None or analysis.get("target", {}).get("resolution") != "resolved":
        raise ValueError("A newly authored profile must resolve its joint complexity target")
    empty_baseline = deepcopy(profile)
    for collection in ("bounds", "comparisons", "regimes", "proofs", "evidence", "references"):
        empty_baseline[collection] = []
    empty_baseline.pop("joint_analysis", None)
    return validate_joint_analysis(analysis, empty_baseline, profile,
                                   report={"outcome": "candidate_change", "findings": []}, require_current=True)
