"""Generate the single set of artifact schemas read identically by runtime and models."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
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
schemas['research']['properties']['coverage_ledger']['description']='Required for new tasks with coverage_scope_ref since bound-review-context; historical artifacts remain readable. Record verified and genuinely unresolved findings; do not present new algorithm ideas as approved results.'
schemas['review']['properties']['coverage_audit']=O(dict(scope=S,checks=coverage_checks,resolved_issue_ids=A(S),carried_issue_ids=A(S),new_blocker_justifications=A(O(dict(issue_id=S,category=E('correctness','evidence','contract','coverage'),why_new=S,affected_subjects=A(S)))),followups=A(O(dict(scope=S,description=S,reason_nonblocking=S))),reuse_context_ref={'anyOf':[R,{'type':'null'}]},reused_bound_ids=A(S)))
schemas['review']['properties']['coverage_audit']['description']='A new profile review checks coverage item by item and consolidates mandatory obligations. A second review explicitly carries forward/resolves old issues; new coverage blockers explain new evidence or first-review omissions. New counterexamples or invalid dependencies may always block. Reuse is limited to per-bound candidates whose unchanged dependencies the controller has verified; the current proposal still requires approval.'
# Reuse the native joint-parameter obligation ledger rather than creating another scientific queue.
# Historical three-field followups remain readable; anchored tasks validate the typed fields.
followup=O(dict(scope=S,description=S,reason_nonblocking=S,obligation_id=S,evidence_refs={**A(R),'minItems':1,'uniqueItems':True},source_review_ref={'anyOf':[R,{'type':'null'}]},retained_claims_valid={'const':True}),required=['scope','description','reason_nonblocking'])
followup['description']='A nonblocking extension whose existing claims remain valid. In anchored tasks all fields are required. obligation_id binds the native joint-parameter synthesis obligation; persist the same record in research.coverage_ledger.followups and profile.delivery_followups. A reviewer cannot add it after signing the frozen five files.'
schemas['review']['properties']['coverage_audit']['properties']['followups']=A(followup)
schemas['research']['properties']['coverage_ledger']['properties']['followups']=A(followup)
schemas['profile']['properties']['delivery_followups']=A(followup)
for kind,field in [('research','coverage_ledger'),('review','coverage_audit')]:
 schemas[kind]['properties'][field]['properties']['delivery_scope_ref']=R
justification=schemas['review']['properties']['coverage_audit']['properties']['new_blocker_justifications']['items']['properties']
justification.update(basis=E('current_claim_invalid','frozen_obligation','first_review_omission','new_evidence_defect','new_construction'),frozen_issue_ids=A(S),affected_profile_pointers=A(S))
schemas['review']['properties']['proof_approvals']=A(O(dict(proof_ref=R,scope=E('standalone_proposition','standalone_proposition_explicit_context'),assumptions_complete={'const':True},context_pointers={**A(S),'minItems':1,'uniqueItems':True},reason=S)))
schemas['review']['properties']['proof_approvals']['items']['properties']['execution_check']=O(dict(required={'type':'boolean'},reason=S,check_refs={**A(R),'uniqueItems':True}))
schemas['review']['properties']['proof_execution_checks']=A(O(dict(proof_ref=R,execution_check=schemas['review']['properties']['proof_approvals']['items']['properties']['execution_check'])))
schemas['review']['properties']['proof_execution_checks']['description']='Execution applicability for formal proofs supporting currently adopted bounds, including when no reuse credential is issued. May instead use proof_approvals.execution_check for the same proof. If both are present they must agree; declining reusable credentials does not waive actual scientific checks.'
schemas['review']['properties']['proof_approvals']['description']='Independent credentials for fixed propositions, not current bound adoption. Verify complete assumptions, original proof and mathematical dependencies. context_pointers includes /common_specification and every necessary definition. standalone_proposition retains legacy conservative hashing; standalone_proposition_explicit_context uses the explicitly complete context without implicitly hashing the whole parameters array. The new scope requires actual review of all mathematical parameters, variables, norms and quantifiers, including excluded old-context fields; changing a scope cannot delete a real assumption. The controller computes hashes. Empty credentials do not waive scientific review.'
schemas['review']['properties']['proof_scope_revalidations']={**A(O(dict(proof_ref=R,candidate_id={**S,'minLength':1},changes_reviewed={'const':True},reason={**S,'minLength':1}))),'uniqueItems':True,'description':'Independent current scope re-review for a controller-listed proof_scope_revalidation_candidates entry whose proof and mathematical dependencies remain stable. Inspect the original credential, context_changes and all new/historical issue occurrences, then issue a current proof_approvals credential with complete assumptions and scopes. Bind the current candidate_id; do not list this proof in reused_proof_refs. This is newly reviewed applicability/context, not automatic reuse or permission to ignore changed assumptions, source/proof defects, or older issue occurrences.'}
schemas['review']['properties']['proof_issue_scopes']=A(O(dict(issue_id=S,affected_proof_refs={**A(R),'uniqueItems':True},scope_complete={'type':'boolean'},reason=S)))
schemas['review']['properties']['proof_issue_scopes']['description']='Cover every scientific issue in profile/research/review that blocks bound/profile/publication and specify its impact on standalone proof propositions. Unknown/omitted scope requires full review. An empty affected list is allowed only after verifying that the issue is unrelated to the proof. An unresolved blocker directly targeting that proof cannot be overridden as unaffected.'
schemas['review']['properties']['issue_scope_version']=E('snapshot-bound-scope','occurrence-bound-scope')
schemas['review']['properties']['bound_approvals']=A(O(dict(bound_id=S,scope=E('bound_applicability'),assumptions_complete={'const':True},context_pointers={**A(S),'minItems':1,'uniqueItems':True},reason=S)))
schemas['review']['properties']['bound_approvals']['description']='Independent per-bound applicability credentials. Include /common_specification and all necessary definitions in context_pointers; effective views, global parameters and pinned dependencies remain mandatory. This does not replace approved_bound_ids or final independent review.'
schemas['review']['properties']['bound_issue_scopes']=A(O(dict(issue_id=S,affected_bound_ids={**A(S),'uniqueItems':True},scope_complete={'type':'boolean'},reason=S)))
for field in ('bound_issue_scopes','proof_issue_scopes'):
 schemas['review']['properties'][field]['items']['properties']['occurrence_ids']={**A(S),'uniqueItems':True}
schemas['review']['properties']['projection_repairs']=A(O(dict(issue_id=S,file=E('identity.json','classification.json','human_tags.json','machine_tags.json'),pointer={**S,'pattern':'^/'},reason=S)))
schemas['review']['properties']['projection_repairs']['description']='Explicit sidecar-only protocol defects. Each row identifies an issue of kind protocol_error blocking only profile/publication and a file-relative JSON pointer. When these are all publication blockers, the controller regenerates the sidecars once and requests fresh independent review without an author rewrite. This never approves a bound or resolves a scientific issue.'
schemas['review']['properties']['bound_issue_scopes']['description']='Explicit impact of each scientific issue on registered bounds. Unknown scope remains conservative. With issue_scope_version snapshot-bound-scope, verified whole-snapshot provenance references are separated from the unchanged mathematical issue semantics; all older credentials remain conservative.'
schemas['review']['properties']['proof_reuse_context_ref']={'anyOf':[R,{'type':'null'}],'description':'When reusing proofs or independently revalidating a listed scope candidate, bind the current input proof_context_ref; an old review or producer-reported catalog cannot replace it. This binding does not turn scope revalidation into automatic reuse.'}
schemas['review']['properties']['reused_proof_refs']={**A(R),'uniqueItems':True,'description':'List only candidates verified by the controller in this run and explicitly approved by current proof_approvals. Reuse concerns standalone propositions only; current bound applicability, coverage/envelopes/reader/five files, and every active bound still require new review.'}
schemas['result']['properties']['source_locators']['items']['properties']['version']={**S,'description':'Must equal the version of the formal source object for that source_ref exactly; do not substitute the arXiv version label of a paper. Inspect the actual version first with source_read or artifact_get.'}
# comparisons are complexity comparison cells, not free-form descriptions of related settings/literature.
comparison=O(dict(comparison_id=S,id=S,comparison_key={**key,'additionalProperties':True},**key['properties']),required=[],extra=True)
comparison['description']='A complexity comparison cell. Requires the full six-part comparison_key (or equivalent legacy flat fields). Put textual relations to related settings/literature in relations; do not guess a missing view/guarantee/regime.'
comparison['allOf']=[{'anyOf':[{'required':['comparison_id']},{'required':['id']}]},{'anyOf':[{'required':['comparison_key']},{'required':list(key['properties'])}]}]
schemas['profile']['properties']['comparisons']=A(comparison)
joint_check_names = ("parameter_roles", "guarded_envelopes", "domain_accounting", "improvement_regions", "provenance", "display_consistency")
schemas["review"]["properties"]["joint_checks"] = O({name: {"type": "boolean"} for name in joint_check_names})
schemas["review"]["properties"]["prepared_hash"] = {"type": "string", "pattern": "^[0-9a-f]{64}$", "description": "For proposal approvals, copy bundle_hash from the independently inspected prepared object."}
joint_field = {"type": "object", "description": "Complete complete synthesis analysis. Read schema_read(kind=joint_analysis) for the exact schema. The host validates this field and cross-checks native references before freezing."}
schemas["profile"]["properties"]["joint_analysis"] = joint_field
schemas["research"]["properties"]["joint_analysis"] = {**joint_field, "description": "Required for no_change on the pinned existing profile; new and update store their analysis in the profile."}
schemas["research"]["properties"]["literature_scope"] = O(dict(mode=E("fixed_sources","bounded_search"), source_refs={**A(R),"minItems":1,"uniqueItems":True}, search_refs={**A(R),"uniqueItems":True}, unresolved_leads=A(S)))
schemas["profile"]["properties"]["refinement_pending"] = O(dict(reason={"type":"string","minLength":1}, next_evidence={"type":"string","minLength":1}, source_refs={**A(S), "minItems":1}))
for kind,schema in schemas.items():
 schema={"$schema":"https://json-schema.org/draft/2020-12/schema","title":kind,**schema}
 (ROOT/'schemas'/f'{kind}.schema.json').write_text(json.dumps(schema,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__': print(f'{len(schemas)} schemas written')
