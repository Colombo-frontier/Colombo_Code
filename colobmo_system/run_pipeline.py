"""Optional independent downstream launcher; run.py remains the Brain entrypoint."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from colombo.downstream.launcher import main
if __name__=='__main__':
    raise SystemExit(main())
