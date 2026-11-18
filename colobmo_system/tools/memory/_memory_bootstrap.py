"""Use the core installed beside the ordinary system entry points."""
from pathlib import Path
import sys
SYSTEM_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MEMORY_ROOT = SYSTEM_ROOT / "long_term_memory"
sys.path.insert(0, str(SYSTEM_ROOT / "src"))
