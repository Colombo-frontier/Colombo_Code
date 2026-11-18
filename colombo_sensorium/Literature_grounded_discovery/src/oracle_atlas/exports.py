"""English Markdown projection of a fixed scientific profile, without historical derivation dependencies."""
from __future__ import annotations

import json


def _text(value):
    if isinstance(value,str): return value
    if value is None:return "Not specified."
    if isinstance(value,list):return "\n\n".join(_text(x) for x in value)
    if isinstance(value,dict):
        if "description_paragraphs" in value:return _text(value["description_paragraphs"])
        if "summary" in value:return _text(value["summary"])
        return "; ".join(f"{k.replace('_',' ')}: {_text(v)}" for k,v in value.items())
    return str(value)


def render_profile(profile: dict) -> str:
    if profile.get("reader_markdown"):
        # reader_markdown is reviewed within the same frozen proposal; do not alter conclusions after publication.
        return profile["reader_markdown"].rstrip()+"\n"
    lines=[f"# {profile.get('title',profile['setting_id'])}","",f"Setting ID: `{profile['setting_id']}`","",_text(profile.get("summary","")),"","## Specification",""]
    for axis in ["task","model","oracle","algorithms","output","metric","guarantee","resource"]:
        if axis in profile["common_specification"]:
            section=profile["common_specification"][axis]
            lines += [f"### {axis.upper()}","",_text(section),""]
            if isinstance(section,dict):
                for statement in section.get("statements",[]):
                    if statement.get("text") and statement["text"]!=section.get("summary"):
                        lines += [statement["text"],""]
                for field in ["formula_latex","threshold_latex","base_expression"]:
                    if section.get(field):lines += ["$$",section[field],"$$",""]
    lines += ["## Algorithm views",""]
    for view in profile.get("views",[]):
        lines += [f"### {view.get('label',view['view_id'])}","",_text(view.get("algorithms",{})),"",_text(view.get("guarantees",[])),""]
    lines += ["## Complexity brackets",""]
    for row in profile.get("bracket_rows",[]):
        lines += [_text(row),""]
    lines += ["## Bounds and applicability",""]
    for bound in profile.get("bounds",[]):
        lines += [f"### {bound.get('bound_id',bound.get('id','Bound'))}","",_text(bound),""]
    for title,key in [("Coverage and remaining questions","coverage"),("Status","summary_status"),("Self-contained arguments","proofs"),("Evidence","evidence"),("References","references")]:
        lines += [f"## {title}","",_text(profile.get(key,[])),""]
    return "\n".join(lines).rstrip()+"\n"
