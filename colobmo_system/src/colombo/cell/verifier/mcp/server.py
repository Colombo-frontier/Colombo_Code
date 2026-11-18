"""Compatibility entry for frozen Colombo MCP configurations; no research logic."""
from pathlib import Path
import runpy
import sys

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    runpy.run_module("colombo.cell.verifier.mcp_server", run_name="__main__")
