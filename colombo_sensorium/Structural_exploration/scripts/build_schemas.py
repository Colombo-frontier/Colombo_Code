"""Generate the single set of artifact schemas read identically by runtime and models."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from oracle_atlas.science.joint import JOINT_CHECKS
S={"type":"string"}; N={"type":["string","null"]}; R={"type":"string","pattern":"^sha256:[a-f0-9]{64}$"}; A=lambda x:{"type":"array","items":x}; O=lambda p,required=None,extra=False:{"type":"object","properties":p,"required":list(p) if required is None else required,"additionalProperties":extra}; E=lambda *x:{"type":"string","enum":list(x)}
axes=['TASK','MODEL','ORACLE','ALGORITHMS','OUTPUT','METRIC','GUARANTEE','RESOURCE']
issue=O(dict(issue_id=S,kind=E('extraction_omission','source_ambiguity','proof_gap','applicability','identity_ambiguity','coverage','protocol_error','other'),scope=S,subject_refs=A(S),blocks=A(E('extraction','identity','bound','profile','publication')),message=S,evidence_refs=A(R),resolves=A(S)))
statement=O(dict(id=S,text=S,status=E('known','unknown','not_applicable'),object_ref=N,variable_block_ref=N,norm_ref=N,domain_ref=N,view_ref=N,operation_ref=N,evidence_refs=A(R)))
axis=O(dict(summary=S,statements=A(statement)),extra=True)
spec=O({a.lower():axis for a in axes},extra=True)
fact=O(dict(concept_id=S,axis=E(*axes),value=S,object_ref=N,view_ref=N,operation_ref=N,source_pointer=S,status=E('known','unknown','not_applicable')),extra=True)
fact['properties']['view_ref']={**N,'description':'Reference a view_id declared in the current document, not a /views/N path. Preflight converts paths only when unambiguous; it must not guess identity mappings.'}
fact['properties']['operation_ref']={**N,'description':'Reference an operation ID declared in the effective native interface of this view, not an /operations/N path. Record unknown permissions explicitly as unknown and null; do not invent operations.'}
fact['properties']['source_pointer']={**S,'pattern':'^/','description':'An existing RFC 6901 path inside the final profile. A view source binds the same view; an operation source binds the same native operation or an explicit statement.operation_ref. Do not carry over an old candidate layout directly.'}
view=O(dict(view_id=S,label=S,algorithms={"type":"object"},guarantees=A({"type":"object"}),specification_overrides={"type":"object"},alias_ids=A(S)),extra=True)
key=O(dict(setting_id=S,view_id=S,guarantee_id=S,quantity_id=S,resource_projection_id=S,regime_id=S))
# The target Atlas permits free-form scientific objects; expose native-operation shapes that this component can read mechanically,
# without inferring permissions from free text or forcing changes to established scientific expressions.
precision_object=O(dict(code=N,kind=N,model=N,status={'type':['string','null'],'enum':['known','unknown','unspecified','unresolved','not_reported','not_applicable',None]}),required=[],extra=True)
precision_object['anyOf']=[{'required':[k]} for k in ('code','kind','model')]+[{'properties':{'status':{'enum':['unknown','unspecified','unresolved','not_reported','not_applicable',None]}},'required':['status']}]
quality_contract={'anyOf':[S,precision_object,{'type':'null'}],'description':'Explicit precision code: exact/inexact/stochastic or unknown/null. Objects may use code/kind/model; multiple aliases must agree. status=unknown/null preserves uncertainty, and an unknown status alone is allowed. Do not use formulas or explanations as precision codes.'}
returns_contract={'anyOf':[S,A(S),{'type':'null'}],'description':'A string or list of strings explicitly identifying return components; null is allowed when unknown. A single string is mechanically wrapped as one item without inferring equivalence to another interface.'}
native_operation=O(dict(id=S,operation_id=S,operation_ref=S,code=S,operation_code=S,object_ref=N,object_id=N,target_object=N,role=S,
    returns=returns_contract,return_components=returns_contract,feedback_quality=quality_contract,precision=quality_contract,quality=quality_contract,
    noise={'anyOf':[S,{'type':'boolean'},{'type':'object'}]},precision_scope=S,target_scope=S,response_target=S,sampled_object={'type':'boolean'},
    response=O(dict(text=S,precision=quality_contract,feedback_quality=quality_contract,quality=quality_contract,noise={'anyOf':[S,{'type':'boolean'},{'type':'object'}]},target_scope=S,precision_scope=S,response_target=S,sampled_object={'type':'boolean'}),required=[],extra=True)),required=[],extra=True)
native_operation['anyOf']=[{'required':[k]} for k in ('id','operation_id','operation_ref')]
native_operation['description']='Component structural contract/recommended shape; declare it in common_specification.oracle.operations or a view override. IDs serve only binding; source_pointer preserves the original field. Check the full operation inventory and precision/noise/sampling scope separately. Additional source descriptions may be retained.'
schemas={
'native_operation':native_operation,
'handoff':O(dict(status=E('complete','needs_materials','blocked'),artifact_refs=A(R),summary=S,checkpoint_ref={"anyOf":[R,{"type":"null"}]})),
'request':O(dict(task_ids=A(S),years=A({"type":"integer","minimum":1900}),sources=A(S),query_budget={"type":"integer","minimum":1},paper_limit={"type":"integer","minimum":1},event_kind=E('publication','preprint','any'),notes=S)),
'plan':O(dict(task_ids=A(S),years=A({"type":"integer","minimum":1900}),sources=A(S),query_budget={"type":"integer","minimum":1},paper_limit={"type":"integer","minimum":1},notes=S)),
'catalog':O(dict(tasks=A(O(dict(task_id=S,label=S,queries=A(S),approved={"type":"boolean"}),extra=True))),extra=True),
'task_proposal':O(dict(proposals=A(O(dict(task_id=S,label=S,formulation=S,queries=A(S),evidence_refs=A(R),reason=S))),report_zh=S)),
'paper':O(dict(title=S,doi=N,arxiv_id=N,urls=A(S),publication_events=A({"type":"object"}),provenance=A({"type":"object"})),extra=True),
'paper_batch':O(dict(paper_refs=A(R),coverage={"type":"object"},search_refs=A(R))),
'source':O(dict(url=S,version=S,content_hash=S,text=S,metadata={"type":"object"}),extra=True),
'candidate':O(dict(candidate_id=S,title=S,paper_refs=A(R),common_specification=spec,views=A(view),tag_facts=A(fact),issues=A(issue)),extra=True),
'extraction':O(dict(candidate_refs=A(R),paper_ref=R)),
'identity':O(dict(candidate_ref=R,decision=E('existing','new','unresolved'),setting_id=N,view_mapping=A(O(dict(candidate_view_id=S,atlas_view_id=N,reason=S))),normalization=S,comparisons=A(O(dict(setting_id=S,relation=E('same','different','related','unresolved'),reason=S,evidence_refs=A(R)))),retrieval_ref=R,recall_audit=O(dict(strategies=A(S),unresolved_ids=A(S),reason=S,inventory_version=S)),issues=A(issue))),
'review':O(dict(subject_ref=R,review_type=E('extraction','identity','profile'),verdict=E('approve','revise','defer'),assessments=A(O(dict(subject_id=S,verdict=E('approve','revise','defer'),reason=S))),issues=A(issue),approved_bound_ids=A(S),summary=S)),
'research':O(dict(candidate_ref=R,identity_ref=R,action=E('no_change','update','new'),setting_id=S,base_version=N,profile_ref={"anyOf":[R,{"type":"null"}]},result_refs=A(R),proof_refs=A(R),issues=A(issue),change_summary=S)),
'result':O(dict(result_id=S,comparison_key=key,direction=E('upper','lower','impossibility','infeasibility'),statement=S,formula_latex=S,conditions=A(S),parameter_region=S,algorithm_scope=S,witness_type=N,guarantee=S,resource_accounting=S,origin=E('published_theorem','analyst_transfer','analyst_derivation'),source_refs=A(R),source_locators=A(O(dict(source_ref=R,version=S,locator=S))),proof_refs=A(R),status=E('proposed','quarantined'),issues=A(issue))),
'proof':O(dict(proof_id=S,origin=E('analyst_transfer','analyst_derivation'),proposition=S,premises=A(S),argument=S,boundary_cases=S,quantifiers=S,resource_accounting=S,dependencies=A(R),issues=A(issue))),
'profile':O({**{k:S for k in ['schema_version','setting_id','title','primary_domain']},'common_specification':{"type":"object"},**{k:A({"type":"object"}) for k in ['views','parameters','symbols','quantities','resource_projections','regimes','bounds','comparisons','bracket_rows','proofs','evidence','references','facets','relations','aliases']},'summary_status':{"type":"object"},'provenance':{"type":"object"}},extra=True),
'retrieval':{"type":"object"},'search':{"type":"object"},'prepared':{"type":"object"},
'proposal':O(dict(research_ref=R,candidate_ref=R,identity_ref=R,profile_ref=R,prepared_ref=R,change_summary=S,base_version=N,inventory_version=S,mode=E('update','new'))),
'checkpoint':O(dict(summary=S,refs=A(R),remaining=A(S))),
'receipt':{"type":"object"},'native_record':{"type":"object"},'external_result':{"type":"object"}
}
schemas['research']['properties']['tag_facts']=A(fact)
schemas['profile']['properties']['tag_facts']=A(fact)
coverage_check=O(dict(check_id=E('zero_query','exact_reconstruction','coarse_accuracy','dimension_endpoints','confidence_endpoints','degenerate_instances','envelopes_and_monotonicity','moment_contracts','supported_transfers'),scope=S,status=E('verified','not_applicable','unresolved'),reason=S,result_refs=A(R),proof_refs=A(R)))
coverage_checks={**A(coverage_check),'minItems':9,'description':'Check nine boundary categories per view/regime. Give specific reasons for inapplicability; the template is not a proof of mathematical exhaustiveness.'}
schemas['research']['properties']['coverage_ledger']=O(dict(scope=S,checks=coverage_checks,issue_resolutions=A(O(dict(issue_id=S,status=E('resolved','remaining','not_applicable'),reason=S,result_refs=A(R),proof_refs=A(R))))))
schemas['research']['properties']['coverage_ledger']['description']='Required for new tasks with coverage_scope_ref since 1.0.2; historical artifacts remain readable. Record verified and genuinely unresolved findings; do not present new algorithm ideas as approved results.'
schemas['review']['properties']['coverage_audit']=O(dict(scope=S,checks=coverage_checks,resolved_issue_ids=A(S),carried_issue_ids=A(S),new_blocker_justifications=A(O(dict(issue_id=S,category=E('correctness','evidence','contract','coverage'),why_new=S,affected_subjects=A(S)))),followups=A(O(dict(scope=S,description=S,reason_nonblocking=S))),reuse_context_ref={'anyOf':[R,{'type':'null'}]},reused_bound_ids=A(S)))
schemas['review']['properties']['coverage_audit']['description']='A new profile review checks coverage item by item and consolidates mandatory obligations. A second review explicitly carries forward/resolves old issues; new coverage blockers explain new evidence or first-review omissions. New counterexamples or invalid dependencies may always block. Reuse is limited to per-bound candidates whose unchanged dependencies the controller has verified; the current proposal still requires approval.'
schemas['review']['properties']['proof_approvals']=A(O(dict(proof_ref=R,scope=E('standalone_proposition'),assumptions_complete={'const':True},context_pointers={**A(S),'minItems':1,'uniqueItems':True},reason=S)))
schemas['review']['properties']['proof_approvals']['description']='Explicit credentials from an independent profile review for fixed proof propositions, introduced in 1.0.3. Actually verify each proposition, its complete assumptions, original content, and dependencies. context_pointers includes /common_specification and every necessary profile definition; the controller recomputes hashes from fixed prepared content. Do not infer proof approval from approved_bound_ids. An empty array is allowed when certification is unsupported, but reuse must not then be claimed.'
schemas['review']['properties']['proof_issue_scopes']=A(O(dict(issue_id=S,affected_proof_refs={**A(R),'uniqueItems':True},scope_complete={'type':'boolean'},reason=S)))
schemas['review']['properties']['proof_issue_scopes']['description']='Cover every scientific issue in profile/research/review that blocks bound/profile/publication and specify its impact on standalone proof propositions. Unknown/omitted scope requires full review. An empty affected list is allowed only after verifying that the issue is unrelated to the proof. An unresolved blocker directly targeting that proof cannot be overridden as unaffected.'
schemas['review']['properties']['proof_reuse_context_ref']={'anyOf':[R,{'type':'null'}],'description':'When reusing proofs, bind the current input proof_context_ref; an old review or producer-reported catalog cannot replace it.'}
schemas['review']['properties']['reused_proof_refs']={**A(R),'uniqueItems':True,'description':'List only candidates verified by the controller in this run and explicitly approved by current proof_approvals. Reuse concerns standalone propositions only; current bound applicability, coverage/envelopes/reader/five files, and every active bound still require new review.'}
schemas['result']['properties']['source_locators']['items']['properties']['version']={**S,'description':'Must equal the version of the formal source object for that source_ref exactly; do not substitute the arXiv version label of a paper. Inspect the actual version first with source_read or artifact_get.'}
# comparisons are complexity comparison cells, not free-form descriptions of related settings/literature.
comparison=O(dict(comparison_id=S,id=S,comparison_key={**key,'additionalProperties':True},**key['properties']),required=[],extra=True)
comparison['description']='A complexity comparison cell. Requires the full six-part comparison_key (or equivalent legacy flat fields). Put textual relations to related settings/literature in relations; do not guess a missing view/guarantee/regime.'
comparison['allOf']=[{'anyOf':[{'required':['comparison_id']},{'required':['id']}]},{'anyOf':[{'required':['comparison_key']},{'required':list(key['properties'])}]}]
schemas['profile']['properties']['comparisons']=A(comparison)

# Current creation contracts. Scientific truth and native cross-reference checks
# still run separately against the exact frozen context and prepared five files.
status_contract=json.loads((ROOT/'standards'/'status_taxonomy.json').read_text('utf-8'))
nonempty={**S,'minLength':1}
strings=lambda values:{**A(E(*values)),'uniqueItems':True}
research_scope=O(dict(scope=nonempty,queries_complete={'type':'boolean'},
    unresolved_leads={**A(nonempty),'uniqueItems':True}))
research_scope['description']='Actual finite research scope. Completion and unresolved leads are declared explicitly; this does not certify exhaustive literature.'
schemas['research_scope']=research_scope
schemas['research']['properties']['research_scope']=research_scope
schemas['research']['required'].append('research_scope')
schemas['profile']['properties']['research_scope']=research_scope

comparison_status=O(dict(code=E(*status_contract['comparison_statuses']),label=nonempty,
    missing_sides=strings(['lower','upper','achievable_budget','necessary_resource_constraint'])),extra=True)
comparison_status['properties']['gap_causes']=strings(status_contract['gap_causes'])
comparison_status['properties']['attributes']=O(dict(exact_cost={'type':'integer','minimum':0},
    ratio_applicable={'type':'boolean'},saturation={'type':'boolean'}),required=[],extra=True)
comparison['properties']['status']=comparison_status
comparison['required']=['status']
comparison['properties']['gap_causes']=strings(status_contract['gap_causes'])
regime=O(dict(gap_causes=strings(status_contract['gap_causes'])),required=[],extra=True)
regime['not']={'required':['status']}
schemas['profile']['properties']['regimes']=A(regime)
comparison['properties']['regimes']=A(regime)
comparison['properties']['bracket']={'type':'object','not':{'required':['status']}}
schemas['profile']['properties']['comparisons']={**A(comparison),'minItems':1}
named_status=lambda codes:O(dict(code=E(*codes),label=nonempty),extra=True)
summary_status=O(dict(scope={'const':'documented_comparison_domain'},
    badges=A(named_status(status_contract['summary_badges'])),
    special_statuses=A(named_status(status_contract['special_statuses'])),
    gap_classes=strings(status_contract['gap_classes']),
    missing_sides=strings(['lower','upper','achievable_budget','necessary_resource_constraint']),
    comparison_count={'type':'integer','minimum':1},
    status_counts={'type':'object','properties':{code:{'type':'integer','minimum':1} for code in status_contract['comparison_statuses']},'additionalProperties':False}),extra=True)
summary_status['not']={'required':['code']}
schemas['profile']['properties']['summary_status']=summary_status
joint_schema=json.loads((ROOT/'schemas'/'joint_analysis.schema.json').read_text('utf-8'))
joint_schema.pop('$schema',None)
joint_schema.pop('title',None)
joint_schema['properties']['version']={'const':2}
schemas['profile']['properties']['joint_analysis']=joint_schema
schemas['profile']['required'].append('joint_analysis')

joint_check=O(dict(check_id=E(*JOINT_CHECKS),verdict=E('approve','revise','defer'),reason=nonempty))
joint_checks={**A(joint_check),'minItems':len(JOINT_CHECKS),'maxItems':len(JOINT_CHECKS),
    'allOf':[{'contains':{'type':'object','properties':{'check_id':{'const':name}},'required':['check_id']},
              'minContains':1,'maxContains':1} for name in JOINT_CHECKS]}
sha={'type':'string','pattern':'^[a-f0-9]{64}$'}
joint_review=O(dict(prepared_hash=sha,analysis_hash=sha,science_context_hash=sha,checks=joint_checks))
schemas['review']['properties']['joint_review']=joint_review
schemas['review']['allOf']=[{'if':{'properties':{'review_type':{'const':'profile'}},'required':['review_type']},
    'then':{'required':['joint_review']}}]
for kind,schema in schemas.items():
 schema={"$schema":"https://json-schema.org/draft/2020-12/schema","title":kind,**schema}
 (ROOT/'schemas'/f'{kind}.schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__': print(f'{len(schemas)} schemas written')
