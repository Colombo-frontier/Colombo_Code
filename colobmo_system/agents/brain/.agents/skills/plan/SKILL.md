---
name: plan
description: Fix the Oracle Complexity Setting and assign initial, supplementary, or repair Tasks based on candidate rates, the reviewed Bracket, and Task coverage.
---

# Plan

Use the Goal, Setting, GoalProgress, Task assignments, formal reviews, and remaining current-Wave budget from context. Read evidence as needed without inspecting the internal research of running Cells.

## Initial Setting

The first submit_plan submits setting_specification={specification,provenance,unknowns,near_optimal_policy}. specification preserves the supplied profile's entries and IDs, especially common_specification={task,model,oracle,output,metric,resource}, views (Algorithm Class/Guarantee), registry, parameters, symbols, quantities, resource_projections, and regimes. Organize non-profile materials according to the same meanings without falsely attributing them to Atlas.

Fill in missing items that can be justified; provenance records entry/source/status (provided/completed/unknown). Definitions that affect the goal but cannot be determined remain unknown; do not fabricate Bounds/Proofs/citations or silently add easier assumptions. The Setting is fixed thereafter. The default near-optimal policy permits a polylog gap in natural dimensionless parameters, subject to the user's explicit requirements.

## Candidate Rates and Task Allocation

First consider the most plausible rate and its basis, then allocate work. The following are possibilities, not fixed quotas:

- If the current Upper Bound is likely near-optimal, assign one or more Lower Bound Cells to match it with a Lower Bound, allowing a polylog gap.
- If the current Lower Bound is likely near-optimal, primarily assign Upper Bound Cells.
- If the candidate rate lies between the bounds, assign Upper and Lower Bound Tasks concurrently in the corresponding scope.
- Assign regimes separately when their bottlenecks differ, and combine them when they share a mechanism. A General Cell may address the complete problem, but its goal must be near-optimal results in all assigned regimes.
- Assign Lemma, transfer, and composition Tasks with explicit local deliverables as needed. Distinguish technical suggestions from fixed conditions; a conjectured rate is not an established fact. Do not mandate all three Cell types or a whole-domain explorer.
- Consider an experiment Cell when reasoning cannot distinguish credible candidates and experiments would help; specify measurement scope, candidate questions, code/data/report, and uncertainty. No fixed number of preceding Waves is required; lack of a complete Proof alone is not a reason.

An Experiment assignment specifies the research question, referenced Setting, admissible Algorithm / construction / parameter exploration scope, available budget, and evidence sufficient to change the next decision. Distinguish fixed Algorithm evaluation, Algorithm search, empirical minimax competition, and mechanism probes; suggest the estimate-epsilon-rate or probe-mechanism Skill if appropriate, leaving methods, grids, repetitions, and stopping times to the Cell. Do not prewrite the full experiment for the Cell or require support for the original conjecture, a predetermined fitted exponent, or a claim of optimality. Completion criteria may accept a justified inconclusive outcome. responsibility.claim denotes the question to investigate, and proof_step_ids may be empty.

## Assignment and Package

specialization is general / upper_bound / lower_bound / experiment. Specify instructions, deliverables, completion_criteria, responsibility, and package. Scope, Oracle, Guarantee, Resource, and mandatory conditions must not be left for the Cell to change. Methodological suggestions are not mandatory routes unless the assignment explicitly requires them.

Select all necessary local materials and dependencies to form a self-contained package, without linking sibling workspaces or including all history. Attach summaries and intended uses to external URLs. package.items uses actual Brain record IDs and explains importance/purpose/limitations; essential library evidence must be converted into reviewable materials or complete required content. Use package.regime_ids to select necessary Bracket rows and items[].artifact_paths to explicitly select necessary attachments from a record; all required dependencies must still be included. If regime_ids is omitted, provide the current Bracket snapshot; this does not permit omission of the pinned Setting.

resume preserves the original assignment/specialization/package; new conditions or materials require a new Task. A repair Task references actual Verifier findings and aims to complete the corresponding Proof or empirical evidence, rather than having Brain repair it within an Assessment. After an Experiment returns a report, substantive corrections require a new repair Task carrying the pinned report, necessary artifacts, and review feedback; resume must not rewrite the research question of an existing report.

## Current Wave

Before dispatching an existing Task, read `resume_eligibility` and the latest Result's `stop_info` / `budget_snapshot`. `mode="resume"` reuses the remaining Cell starts; do not repeatedly resume when the next required stage has exhausted its budget. If further research is warranted, use `mode="restart"` and the original `resume_task_id` to explicitly allocate a fresh round of Prover/Verifier or Experiment starts; retain the assignment/package, existing records, historical Results, and cumulative usage. Each mode consumes one dispatch; reconnecting the same attempt does not allocate again.

Restart does not reset existing Subcell quotas, per-Challenge quotas, or Checker quotas for the same report version. When Checker quota is exhausted, choose a new repair Task; reconcile unknown executions first rather than bypassing them with Restart. Resume is permitted to synchronize confirmed results or continue a review with remaining budget, even if Prover starts are exhausted. Republishing results without new research is not research progress.

Supplementary dispatch follows Controller's completion of result processing. Use the remaining gap and the scope/direction of queued/running assignments to identify uncovered responsibilities without guessing their internal progress. The number of tasks must not exceed dispatch_remaining; an empty tasks list may indicate no supplementary dispatch for now. Each new execution/resume consumes one allocation.

Submit a separate plan through submit_plan without overwriting existing plans/assignments. Controller handles Wave transitions, stop receipts, and counters; finish after receiving the receipt.
