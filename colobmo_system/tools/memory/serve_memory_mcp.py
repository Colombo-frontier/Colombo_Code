#!/usr/bin/env python3
"""Standalone read-only MCP for the current Memory Store."""
from __future__ import annotations
import argparse,sys
from pathlib import Path
from _memory_bootstrap import DEFAULT_MEMORY_ROOT, SYSTEM_ROOT
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,default=DEFAULT_MEMORY_ROOT)
    a.add_argument('--research-mode',choices=['oracle_complexity','generic'],default='oracle_complexity');q=a.parse_args()
    try:from mcp.server.fastmcp import FastMCP
    except ImportError:raise SystemExit('Install colobmo_system/requirements.txt in this Python environment')
    from colombo.memory.integration import register_builtin_memory
    mcp=FastMCP('colombo-scientific-memory')
    register_builtin_memory(mcp,research_mode=q.research_mode,memory_root=q.root)
    mcp.run(transport='stdio')
if __name__=='__main__':main()
