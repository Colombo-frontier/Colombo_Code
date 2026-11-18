"""Source-only entry points share the parent system core."""
from pathlib import Path
import sys
AGENT_ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = AGENT_ROOT.parent
DEFAULT_MEMORY_ROOT = CORE_ROOT / "long_term_memory"
DATASET_ROOT = DEFAULT_MEMORY_ROOT  # current records, not a second dataset snapshot
sys.path[:0] = [str(CORE_ROOT / "src"), str(AGENT_ROOT / "runtime")]
