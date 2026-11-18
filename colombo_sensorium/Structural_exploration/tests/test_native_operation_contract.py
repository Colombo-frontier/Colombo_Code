"""Actual tools can read the native-operation structural contract; field shapes do not prove mathematical capabilities."""
import json
from jsonschema import Draft202012Validator
from oracle_atlas.core.contracts import schema
from oracle_atlas.core.config import DEFAULTS
from oracle_atlas.core.store import Workspace
from oracle_atlas.atlas.store import Atlas
from oracle_atlas.tools.host import ToolHost


def test_schema_exposes_supported_scalar_and_nested_precision_forms(tmp_path):
    op={"operation_id":"right_matvec","object_ref":"A","returns":"Av in R^n",
        "response":{"precision":{"model":"exact","status":"known"},"noise":"none"}}
    validator=Draft202012Validator(schema("native_operation"))
    assert not list(validator.iter_errors(op))
    for unknown in [None,{'status':'unknown'},{'model':None,'status':'known'}]:
        assert not list(validator.iter_errors({**op,'response':{'precision':unknown}}))
    bad={**op,"returns":{"vector":True}}
    assert list(validator.iter_errors(bad))
    bad={**op,"response":{"precision":{"description":"exact response"}}}
    assert list(validator.iter_errors(bad))
    ws=Workspace(tmp_path/'work');atlas=Atlas(tmp_path/'atlas')
    jid=ws.create_job('extractor',{})
    host=ToolHost(ws,atlas,ws.job(jid),{'budgets':dict(DEFAULTS),'model':{}})
    for kind in ['candidate','profile']:
        result=host.call('schema_read',{'kind':kind},kind)
        assert result['native_operation_schema']['kind']=='native_operation'
    result=host.call('schema_read',{'kind':'native_operation'},'operation-contract')
    assert result.get('data',json.loads(result.get('text','{}')))['title']=='native_operation'
    assert op['returns']=='Av in R^n'  # Exposure/validation does not rewrite the original scientific specification
    ws.close()
