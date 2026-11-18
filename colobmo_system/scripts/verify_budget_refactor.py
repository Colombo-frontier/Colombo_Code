"""Run local unittest suites with concise failure locations, never environment dumps."""
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback
import unittest

parser=argparse.ArgumentParser()
parser.add_argument('suite',choices=['brain','cell'])
parser.add_argument('--pattern',default='test*.py')
parser.add_argument('--shard',help='Run one disjoint test shard, numbered 1/N through N/N')
parser.add_argument('--output',required=True)
args=parser.parse_args()
project=Path(__file__).resolve().parents[1]
dest=Path(args.output)
if not dest.is_absolute():dest=project/dest
dest.parent.mkdir(parents=True,exist_ok=True)
progress=dest.with_suffix('.progress.json')
base=project/'tests'/args.suite
scratch=project/'validation'/'tmp';scratch.mkdir(parents=True,exist_ok=True)
tempfile.tempdir=str(scratch)
os.chdir(project)
sys.path.insert(0,str(base))
sys.path.insert(0,str(project/'src'))

class Result(unittest.TestResult):
    details=[]
    def startTest(self,test):
        super().startTest(test)
        progress.write_text(json.dumps({'pid':os.getpid(),'test':test.id(),
            'tests_started':self.testsRun,'updated_at':time.time()}),encoding='utf-8')
    def detail(self,test,err,kind):
        typ,value,tb=err
        self.details.append({'test':test.id(),'kind':kind,'exception':typ.__name__,
            'frames':[{'file':f.filename,'line':f.lineno,'function':f.name}
                      for f in traceback.extract_tb(tb)[-6:]]})
    def addError(self,test,err):
        self.detail(test,err,'error');super().addError(test,err)
    def addFailure(self,test,err):
        self.detail(test,err,'failure');super().addFailure(test,err)
    def addSubTest(self,test,subtest,err):
        if err is not None:
            self.detail(subtest,err,'failure' if issubclass(err[0],test.failureException) else 'error')
        super().addSubTest(test,subtest,err)

suite=unittest.defaultTestLoader.discover(str(base),pattern=args.pattern)
if args.shard:
    try:
        index,count=map(int,args.shard.split('/'))
        if not 1 <= index <= count: raise ValueError
    except ValueError:
        parser.error('--shard must be an index/count pair with 1 <= index <= count')
    def flatten(tests):
        for item in tests:
            if isinstance(item,unittest.TestSuite): yield from flatten(item)
            else: yield item
    suite=unittest.TestSuite(test for n,test in enumerate(flatten(suite)) if n%count==index-1)
result=Result()
with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    suite.run(result)
report={'suite':args.suite,'tests':result.testsRun,'errors':len(result.errors),
        'failures':len(result.failures),'skipped':len(result.skipped),'details':result.details}
dest.write_text(json.dumps(report,indent=2),encoding='utf-8')
progress.unlink(missing_ok=True)
print(json.dumps({k:v for k,v in report.items() if k!='details'}))
print('Report: '+str(dest))
raise SystemExit(0 if result.wasSuccessful() else 1)
