#!/usr/bin/env python3
"""Read-only current-memory CLI wrapper. Importing this module has no side effects."""
from pathlib import Path
import sys
from _memory_bootstrap import DEFAULT_MEMORY_ROOT, SYSTEM_ROOT
from colombo.memory.cli import main
if __name__=='__main__':raise SystemExit(main())
