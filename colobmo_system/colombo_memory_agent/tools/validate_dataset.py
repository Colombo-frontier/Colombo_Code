#!/usr/bin/env python3
from dataset import load_dataset,report,ContractError
from _agent_bootstrap import DATASET_ROOT
from pathlib import Path
import argparse,json,sys
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Validate current four-library records or an explicit legacy snapshot without scientific certification')
    parser.add_argument('--dataset-root',type=Path,default=DATASET_ROOT)
    args=parser.parse_args()
    try: print(json.dumps(report(load_dataset(args.dataset_root)),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,TypeError,OSError,ContractError) as exc:
        print(json.dumps({'error':str(exc),'scientific_review':False},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(2)
