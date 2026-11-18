"""Select a Cell instruction pack once; preserve its research scope on resume."""
from __future__ import annotations

import json
import shutil
import os
import re
from colombo.shared.file_io import Path
from colombo.shared.file_io import atomic_write

INSTRUCTION_VERSION = "v8.1"
MODES = ("generic", "oracle_complexity")
SPECIALIZATIONS = ("general", "upper_bound", "lower_bound", "experiment")
from colombo.project_paths import PROJECT_ROOT
ROOT = Path(PROJECT_ROOT)
REVIEW_GUIDANCE = "upper_bound_review_guidance.md"
LOWER_REVIEW_GUIDANCE = "lower_bound_review_guidance.md"
# Pack paths and review roles are installation-owned, not model-provided paths.
# Adding a new specialization does not change existing v8.1 pack identities.
PACKS = {
    "experiment": {"source": "agents/experiment_cell", "skill": None, "label": "Experiment",
                   "review_file": None, "instruction_version": INSTRUCTION_VERSION},
    "general": {"source": "agents/cell/prover", "skill": None, "label": "General",
                "review_file": None, "instruction_version": INSTRUCTION_VERSION},
    "upper_bound": {"source": "agents/cell/upper_bound", "skill": "upper-bound", "label": "Upper-bound",
                    "review_file": REVIEW_GUIDANCE, "instruction_version": INSTRUCTION_VERSION},
    "lower_bound": {"source": "agents/cell/lower_bound", "skill": "lower-bound", "label": "Lower-bound",
                    "review_file": LOWER_REVIEW_GUIDANCE, "instruction_version": INSTRUCTION_VERSION},
}


def validate_mode(research_mode="generic", specialization="general") -> dict:
    if not isinstance(research_mode, str) or research_mode not in MODES:
        raise ValueError("Cell research_mode must be generic or oracle_complexity")
    if not isinstance(specialization, str) or specialization not in PACKS:
        raise ValueError("Cell specialization must be general, upper_bound, lower_bound or experiment")
    if specialization != "general" and research_mode != "oracle_complexity":
        raise ValueError(f"{specialization} requires oracle_complexity research_mode")
    return {"research_mode": research_mode, "specialization": specialization,
            "instruction_version": PACKS[specialization]["instruction_version"]}


def pack_for_mode(mode: dict) -> dict:
    """Resolve only known frozen modes, including when rebuilding a review."""
    if not isinstance(mode, dict) or mode != validate_mode(mode.get("research_mode"), mode.get("specialization")):
        raise ValueError("Invalid or unsupported frozen Cell mode")
    return dict(PACKS[mode["specialization"]])


def read_cell_mode(root, *, research_mode=None, specialization=None) -> dict:
    root = Path(root)
    config = json.loads((root / "run.json").read_text(encoding="utf-8")) if (root / "run.json").is_file() else {}
    if config.get("cell_mode") is not None:
        mode = config["cell_mode"]
        if not isinstance(mode, dict) or set(mode) != {"research_mode", "specialization", "instruction_version"}:
            raise ValueError("Invalid frozen Cell mode")
        expected = validate_mode(mode["research_mode"], mode["specialization"])
        if mode != expected:
            raise ValueError("Unsupported Cell instruction version")
    else:
        # Legacy workspaces and isolated tests carry only the common pack.
        mode = validate_mode()
    assignment_path = root.parent / "prepare_request.json"
    if root.name == "cell" and assignment_path.is_file():
        # Brain's fixed preparation lives outside the prover's Cell workspace.
        # Editing both local copies cannot silently disable specialization.
        assigned = json.loads(assignment_path.read_text(encoding="utf-8"))
        if (assigned.get("task_id") != root.parent.name
                or Path(assigned.get("task_dir", "")).resolve() != root.parent.resolve()):
            raise ValueError("Cell preparation belongs to a different task")
        expected = validate_mode(assigned.get("research_mode", "generic"), assigned.get("specialization", "general"))
        if mode != expected:
            raise ValueError("Frozen Cell mode differs from Brain preparation")
    if research_mode is not None and mode["research_mode"] != research_mode:
        raise ValueError("Existing Cell research_mode differs from its assignment")
    if specialization is not None and mode["specialization"] != specialization:
        raise ValueError("Existing Cell specialization differs from its assignment")
    return mode


def install_cell_pack(root, mode: dict) -> None:
    """Install only selected instructions into a newly created workspace."""
    root = Path(root)
    pack = pack_for_mode(mode)
    if (root / "AGENTS.md").exists():
        raise ValueError("Cell instruction pack is already frozen")
    common = ROOT / "agents" / "cell" / "prover"
    source = ROOT / pack["source"]
    if mode["specialization"] == "experiment":
        shutil.copyfile(source / "agent.md", root / "AGENTS.md")
        shutil.copyfile(source / "protocol.md", root / "protocol.md")
        shutil.copytree(source / "skills", root / "skills")
        shutil.copytree(source / "skills", root / ".agents" / "skills")
        # The source pack uses agent.md; installed instructions use AGENTS.md.
        # Both readable skills/ and discovered .agents/skills/ resolve locally.
        for file in [root / "protocol.md", *(root / "skills").rglob("*.md"),
                     *(root / ".agents" / "skills").rglob("*.md")]:
            text = file.read_text(encoding="utf-8")
            for filename, target in (("agent.md", root / "AGENTS.md"), ("protocol.md", root / "protocol.md")):
                local = os.path.relpath(target, file.parent).replace("\\", "/")
                text = re.sub(r"\((?:\.\./)*" + re.escape(filename) + r"\)", "(" + local + ")", text)
            file.write_text(text, encoding="utf-8")
    else:
        shutil.copyfile(source / "AGENTS.md", root / "AGENTS.md")
        shutil.copyfile(common / "protocol.md", root / "protocol.md")
        shutil.copytree(common / ".agents", root / ".agents")
    if pack["skill"]:
        shutil.copytree(source / ".agents" / "skills" / pack["skill"],
                        root / ".agents" / "skills" / pack["skill"])
        shutil.copyfile(source / "review_guidance.md", root / pack["review_file"])


def review_guidance(root) -> bytes | None:
    root = Path(root)
    mode = read_cell_mode(root)
    pack = pack_for_mode(mode)
    if pack["review_file"] is None:
        return None
    # A prover can write workspace files. Never promote its local copy into
    # reviewer instructions unless it matches the trusted version's source.
    source = ROOT / pack["source"] / "review_guidance.md"
    trusted = source.read_bytes()
    local = root / pack["review_file"]
    if not trusted.strip() or not local.is_file() or local.read_bytes() != trusted:
        raise ValueError(f"Frozen {pack['label']} review guidance differs from its installed instruction version")
    return trusted


def validate_specialization(mode, specialization):
    """Validate the same fixed instruction choice for Brain and Cell."""
    validate_mode(mode, specialization)
