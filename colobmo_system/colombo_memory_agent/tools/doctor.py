#!/usr/bin/env python3
"""Local preflight only: never makes a model request or verifies account authentication."""
from __future__ import annotations
import argparse, importlib.util, json, shutil, sqlite3, subprocess, sys
from contextlib import closing
from pathlib import Path
from _agent_bootstrap import AGENT_ROOT,CORE_ROOT,DEFAULT_MEMORY_ROOT,DATASET_ROOT

def inspect(check_codex=False, executable='codex', root=None):
    result={'python':sys.version.split()[0], 'python_supported':sys.version_info >= (3,11),
            'mcp_importable':importlib.util.find_spec('mcp') is not None,
            'model_called':False,'authentication_verified':False}
    with closing(sqlite3.connect(':memory:')) as db:
        try: db.execute('CREATE VIRTUAL TABLE probe USING fts5(text)'); result['sqlite_fts5']=True
        except sqlite3.OperationalError: result['sqlite_fts5']=False
    binary=shutil.which(executable); result['codex_executable']=binary
    if check_codex and binary:
        for name,args in [('version',['--version']),('exec_help',['exec','--help'])]:
            p=subprocess.run([binary,*args],capture_output=True,text=True,timeout=20,check=False)
            result[name]={'returncode':p.returncode,'text':(p.stdout+p.stderr)[:24000]}
        helptext=result['exec_help']['text']
        result['required_cli_flags']={x: x in helptext for x in [
            '--output-schema','--output-last-message','--sandbox','--ignore-user-config','--ephemeral']}
        result['codex_cli_ready']=(result['version']['returncode']==0 and result['exec_help']['returncode']==0
                                   and all(result['required_cli_flags'].values()))
    elif check_codex:
        result['codex_cli_ready']=False
    if root:
        from colombo.memory.store import Store
        s=Store(root); m=s.manifest()
        result['store']={'root':str(s.root),'published_records':len(m['entries']),
                         'has_lead_snapshot':(s.state_root/'LEADS.json').is_file()}
    result['local_data_tools_ready']=result['python_supported'] and result['sqlite_fts5']
    return result

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--check-codex',action='store_true')
    a.add_argument('--codex',default='codex');a.add_argument('--root',type=Path,default=DEFAULT_MEMORY_ROOT);a.add_argument('--out',type=Path)
    q=a.parse_args();r=inspect(q.check_codex,q.codex,q.root)
    text=json.dumps(r,ensure_ascii=False,indent=2)
    if q.out:q.out.parent.mkdir(parents=True,exist_ok=True);q.out.write_text(text,encoding='utf-8')
    print(text);return 0 if r['local_data_tools_ready'] and (not q.check_codex or r['codex_cli_ready']) else 2
if __name__=='__main__':raise SystemExit(main())
