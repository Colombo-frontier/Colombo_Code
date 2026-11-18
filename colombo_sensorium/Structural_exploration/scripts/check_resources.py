"""Validate actually loaded resources, all artifact schemas, and skill entry points; do not assess mathematical truth."""
from pathlib import Path
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from jsonschema import Draft202012Validator
from oracle_atlas.core.config import resources_root
from oracle_atlas.core.contracts import MAIN_KINDS
from oracle_atlas.runtime.instructions import load_instructions

root=resources_root(); result={"agents":[],"schemas":0,"skills":0}
for role in MAIN_KINDS:
    _,manifest=load_instructions(role)
    assert manifest["skills"],role
    result["agents"].append({"role":role,"instructions_chars":manifest["chars"],"hash":manifest["instructions_sha256"]})
for p in (root/"schemas").glob("*.json"):
    Draft202012Validator.check_schema(json.loads(p.read_text()))
    result["schemas"]+=1
for p in list((root/"agents").glob("*/skills/*/SKILL.md"))+list((root/"skills").glob("*/SKILL.md")):
    text=p.read_text();assert text.startswith("---\n") and "\ndescription:" in text and "\nname:" in text,p
    assert "name: "+p.parent.name in text,p
    result["skills"]+=1
print(json.dumps(result,ensure_ascii=False,indent=2))

