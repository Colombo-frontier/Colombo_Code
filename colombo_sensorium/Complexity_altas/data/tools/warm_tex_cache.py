"""Fill the task cache using already generated, untrusted-mode TeX sources."""
from pathlib import Path
import json
import os
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
selected=json.loads((ROOT/'tmp/pdfs/cache_warm_selection.json').read_text())
environment=os.environ.copy()
environment['TECTONIC_CACHE_DIR']=os.environ.get('TECTONIC_CACHE_DIR', str(ROOT/'tmp/tectonic-cache'))
out=ROOT/'tmp/pdfs/cache_warm'
for sid in selected:
    work=out/sid
    work.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'visualization/dist/downloads'/sid/'profile.tex',work/'profile.tex')
    result=subprocess.run([shutil.which('tectonic') or 'tectonic','--untrusted','--keep-logs','-o',str(work),str(work/'profile.tex')],env=environment,capture_output=True,text=True,timeout=180)
    print(sid,result.returncode,flush=True)
    for line in (result.stdout+result.stderr).splitlines():
        if 'downloading' in line or line.startswith('error:'):print(line,flush=True)
