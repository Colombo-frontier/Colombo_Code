# Colombo Brain protocol

This protocol applies to Oracle Complexity workflow 3. Models operate on formal records through MCP; current tools define the schema. References must come from actual tool outputs; do not invent IDs, paths, or versions.

## Files and Records

state.sqlite is the program's internal store; research.json / proof_draft.json / working_notes.json are readable exports and must not be edited directly. research contains Goal, GoalProgress, Tasks, Waves, materials, and audits. Goal stores the input index and pinned Setting; the first plan supplies the Setting, exported as input/setting.json. Copies of user materials reside in input/materials and need not originate from Atlas; there is no run input/manifest.json.

A Task stores the assignment, package, and each attempt's Result, Verifier review, confirmed Claims/scope, and unresolved findings. A Wave stores initial and supplementary plans, member executions, budget, updates, and Pruning, referencing Task reviews without overwriting the original plan. The complete ProofDraft remains the existing top-level object, and the final review is bound to a specific version.

For each model call, context.json is the input, prompt.txt contains stage instructions, call.json records identity/status/timing, and submission.json is the submission receipt; formal research text resides in records and is not replaced by the receipt.

A Brain ref is {id,revision}; MCP ref parameters generally take an ID. An internal Cell record_ref is {kind,id,revision}, where kind uses the collection names claims/arguments/examples/attempts/sources/proof_state/experiment_result/reviews/events. Do not conflate the two reference types.

## Reading

read_research(section="overview",id=None,ref=None,offset=0,limit=20): navigation sections are goal/tasks/waves/proof/notes/materials/audits/conclusion; a pinned read supplies only ref, without navigation parameters. Use full text already provided in overview/context directly. Page through catalogs using next.

read_material(ref,path=None,offset=0,limit=12000,record_ref=None): read attachments authorized by that record. Specify path when there are multiple attachments, and continue paging when truncated=true. For a specific Cell record, use the pinned memory_snapshot attachment and record_ref; locator is not a structured version identity. Read only actually authorized sources.

Controller does not expose a running Cell's internal research to Brain. After a formal return, the complete research archive for that attempt may be read, including notes/drafts/subcells/experiments/reviews. The archive and inventory are pinned; subsequent resume creates a new attempt without replacing the original references. Permission to read everything does not require automatically loading everything.

## Supporting Tools

- lookup(query/url): find external sources as needed; a URL's text receives a pinned material_ref only after being saved as a material. Search snippets are not theorem evidence. Respect the search switch and do not write credentials.
- scientific_memory(mode, arguments_json): read the current Memory in read-only mode by default, supporting overview/browse/search/read/expand; see `.agents/skills/scientific-memory/GUIDE.md` for parameters and pinned refs. Preserve the complete `{id,kind,revision,content_hash,tier}` and do not use it as a Brain record ID in a package. Explicitly set include_leads=true to discover candidates. Before actual use, read the complete statement/scope/evidence/source; necessary materials supplied to a Cell must be self-contained. Old Recollect refs are retired and are not automatically mapped; read historical materials through their existing frozen packages.
- save_note: save a free-form WorkingNote, optionally linking actual related_refs; do not duplicate existing long texts. A note does not certify a Bound.
- format_package_literal(ref,path,literal_text,reason): available only to Brain plan. First read the pinned source and confirm that a unique single-line fragment is a literal formula rather than an actual file reference. The tool only adds code-span delimiters to a future unpublished package copy, without changing characters inside the fragment. Original Results, reviews, and published packages are retained; source SHA256, position, reason, call identity, and copy SHA256 are recorded. Actual missing dependencies must be supplied normally. This operation does not certify a Claim. A failed package preflight in `submit_plan` returns source/path/link information without committing a plan or consuming dispatch budget; correct the issue and resubmit within the same call.
- audit(goal,inputs,record_refs,materials,request_id): perform an independent local check. Pruning uses inputs.prune_relations, and audit_ref may be filled only for a matching completed/pass audit. An audit does not replace Result Verifier. A long operation returns job_id; use job_status to continue retrieving the original result, and do not restart requests whose outcomes are unknown.

## Model Calls and Formal Order

1. plan / submit_plan: complete the Setting on the first call and select Tasks based on candidate rates and specific gaps. Supplementary plans may be issued within the current Wave; tasks must not exceed dispatch_remaining. Pin assignment/package; resume does not alter their content.
2. After a Cell returns, Controller first calls the Verifier and saves the Task attempt review. Brain must not update/prune unreviewed mathematical conclusions beforehand.
3. process_results / record_results: update={admissions,progress}; progress is independent of the complete ProofDraft. Then prune using only reviewed premises and a matching relation audit. next_action may be continue/plan/conclude; Controller coordinates stops before deciding on supplementary dispatch.
4. integrate / record_results: update additionally includes the complete proof_draft and rechecked_step_ids, prunes=[], and usually next_action=conclude. The final Verifier then checks that complete version; the program exports the report only after adoption.

A submitted proof_draft uses body or the mutually exclusive body_source={result_ref,path}; reading may expose a pinned version through proof_ref, but the read projection must not be treated as the submission schema. Proof evidence={result_ref,path,locator,record_ref?}.

## GoalProgress and Verification

progress={overall,status,items,bracket:{bounds,regimes},remaining}. overall only describes current overall research progress; status is separate.

A Bound stores id/direction/expression/scope/assumptions/source/evidence_state/result_ref/review_ref/claim_id. A certified item must exactly match a confirmed Claim in the review; baseline/unknown items are not certified. A Regime stores scope, lower_bound_ids/upper_bound_ids, gap, candidate_rate/candidate_basis, status, comparison_review_ref/comparison_claim_id, and remaining. A candidate is conjectural; a comparison requires review. New compositions at final integrate may be submitted as candidates and adopted after final Verifier approval.

Do not mix comparisons across different views, Oracles, Guarantees, quantities, Resources, or scopes; overlap is not a partition. Preserve the initial baseline's evidence status. Obtain runtime Task status from Tasks rather than storing it again in the Bracket.

admissions records the original Task's completion_status/completed_parts/remaining separately from local accepted status. Use Claims actually confirmed by the outer Verifier; an empirical Result does not certify a mathematical Bound. plan assigns a repair Task for an erroneous Proof; do not repeatedly repair Proofs within an Assessment.

## Budgets and Recovery

Research stages are governed by the Wave limit, per-Wave dispatch limit, top-level concurrency, and existing Cell-local limits, without a run-wide research deadline, dispatch cap, model-call cap, or Assessment revisions cap. Each new execution/resume/restart consumes one dispatch; reconnecting the same execution is not charged again, and failures/Pruning do not refund budget. Exhausting dispatch budget does not stop existing Cells.

`resume` retains remaining Cell starts; before Plan, check whether the next required stage can proceed. An explicit `restart` uses the original `resume_task_id` and fixed assignment/package to allocate a new cycle of top-level Prover/Verifier and Experiment native/hosted starts; record baselines idempotently per attempt, without resetting cumulative counters or existing Results. Retain existing Subcell, per-report Checker, and per-Challenge limits; unknown executions must first be reconciled and must not be relaunched blindly. Completed publication/sync does not require additional Prover starts.

integrate and the final Verifier share a two-hour limit for a single stage. revision/retry/resume does not reset it; a new stage requires genuinely new research results. It consumes no Wave/dispatch allocation and reserves no research budget. Return substantive Proof failures to plan when budget remains; otherwise retain verified partial results and unresolved Claims. Timeout means an incomplete run, not mathematical disproof.

Finish after a stage submission returns a submitted receipt. Replaying the same call must be identical; committed data must not be overwritten. Controller manages stop receipts, adoption, concurrency, and recovery; models must not directly alter processes or counters.
