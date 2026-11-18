"""Run the independent memory writer; never starts the proof scheduler."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
sys.path[:0] = [str(root.parent / "src"), str(root / "runtime")]

from colombo_memory_agent.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
