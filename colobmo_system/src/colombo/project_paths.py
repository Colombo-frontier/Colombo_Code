"""Canonical source and instruction locations for the Colombo repository."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src"
AGENTS_ROOT = PROJECT_ROOT / "agents"
BRAIN_AGENTS_ROOT = AGENTS_ROOT / "brain"
CELL_AGENTS_ROOT = AGENTS_ROOT / "cell"
EXPERIMENT_AGENTS_ROOT = AGENTS_ROOT / "experiment_cell"
CELL_CODE_ROOT = SOURCE_ROOT / "colombo" / "cell"
EXPERIMENT_CODE_ROOT = SOURCE_ROOT / "colombo" / "experiment_cell"
