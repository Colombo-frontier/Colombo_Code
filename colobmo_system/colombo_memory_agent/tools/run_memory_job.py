#!/usr/bin/env python3
"""Convenience entrypoint for the independent Curator/Reviewer process; no Brain/Cell imports."""
from __future__ import annotations
import argparse,sys
from pathlib import Path
from _agent_bootstrap import AGENT_ROOT, DEFAULT_MEMORY_ROOT
from colombo_memory_agent.cli import main as cli

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,default=DEFAULT_MEMORY_ROOT)
    a.add_argument('--jobs-root',type=Path,help='Execution logs and snapshots; defaults to Agent/jobs')
    a.add_argument('--job',type=Path,required=True);a.add_argument('--model');a.add_argument('--reviewer-model')
    a.add_argument('--codex',default='codex');a.add_argument('--timeout',type=int,default=900);a.add_argument('--resume',action='store_true')
    q=a.parse_args()
    args=['--root',str(q.root),'run-job',str(q.job),'--package-root',str(AGENT_ROOT),'--codex',q.codex,'--timeout',str(q.timeout)]
    if q.model:args+=['--model',q.model]
    if q.reviewer_model:args+=['--reviewer-model',q.reviewer_model]
    if q.jobs_root:args+=['--jobs-root',str(q.jobs_root)]
    if q.resume:args+=['--resume']
    return cli(args)
if __name__=='__main__':raise SystemExit(main())
