---
name: upper-bound
description: Develop an optimization Upper-bound proof with its Algorithm witness, adapt Algorithm and analysis within the assigned scope, and track the actual proof obligations and total Resource bound.
---

# Upper-bound Algorithm–Proof development

## 1. Objective

Establish the assigned Upper-bound Claim by connecting a specified or newly constructed Algorithm to its Guarantee and counted total Resource. A partial Task may instead establish one explicitly scoped component. This skill supplies methods for the existing Cell workflow; it does not add an agent, record collection or automatic certification step.

## 2. Inputs

Read `problem.md`, any `TASK.md`, the current `proof_state`, relevant Attempts and fixed Claim/Argument/Example refs. Identify the Function Class, Oracle, admissible information, initialization, Output/Metric, risk convention, target rate and parameter regime from the actual assignment. Keep unspecified choices visible when they matter to the Claim.

Determine whether the Task fixes an Algorithm or allows its design. Read the exact fixed construction and selected evidence before building on it. Use `recollect` when the Algorithm Library or Theorem Library can help: search relevant candidates, then read the precise construction/statement and necessary dependencies or proof. A catalog hit is a lead, not a proof of applicability; record the actual read coverage and fixed library ref through existing Source/Claim/Argument fields. The library does not delimit the design space.

## 3. Method

### Connect the Algorithm to the Claim

Specify the details that affect the claimed result: Oracle queries, updates, sampling, initialization, tuning, stopping and output rule. Distinguish public information available to the Algorithm from hidden instance information used only in analysis. A required but unavailable parameter needs a justified estimator/adaptation or a narrower Claim, not a silent assumption.

Use an existing Example for a reusable Algorithm construction when appropriate; no new Algorithm record type is required. Keep its exact variant fixed. Bind the Guarantee Claim to that construction, put research objects in the Argument's `subject_refs`, actual premises in `dependencies`, and the target Claim in `conclusions` with relation `supports`. A source Algorithm can instead be precisely identified through its existing fixed Source and statement when a new local construction would add no useful identity.

For the Argument that establishes a complexity result, `complexity_profile` is an optional object for a compact account of the Oracle model, parameter domain, total Resource, allowed constant dependence, normalization and relevant Algorithm/Guarantee refs. It does not change Claim identity or certify anything. The complete conditions and conclusion belong in the Claim and the checked Argument; do not hide new assumptions in the profile.

### Let the bottleneck guide the next step

When the current proof falls short, use the evidence to choose a productive change. These are possible approaches, not required branches or a fixed checklist:

| Evidence about the bottleneck | Possible research action |
|---|---|
| Analysis loses a necessary factor or cannot close | Develop a better Potential/Lyapunov Function, tighter inequality, invariant, coupling or proof decomposition. |
| Algorithm mechanism cannot supply the needed property | If design is allowed, change update, sampling, batch schedule, restart or output, then revisit admissibility, Guarantee and full cost for that variant. |
| Target requires a condition the assigned scope does not provide | State the missing condition or a precise Counterexample/obstruction, preserve the scope and report what remains unresolved. |

Uncertainty about the bottleneck can itself motivate a discriminating Lemma, example or experiment. An unsuccessful proof attempt does not establish Algorithm impossibility. Fixed-Algorithm Tasks may report a promising alternative, but that alternative does not complete the original responsibility. A design Task may let proof requirements guide construction; it need not freeze the first Algorithm and only repair its analysis.

Save useful variants, derivations and unresolved questions in existing records. A mathematical change to a Claim or construction requires a new identity under the common protocol. Reuse valid dependencies explicitly; re-audit affected Arguments instead of carrying certification across a changed Algorithm. For a substantive change of route, an Attempt `route_review` records `decision` and `reason`, with the evidence, remaining bottleneck and next discriminating check as useful context.

### Track the obligations that the route actually needs

Use `proof_state.routes`, not a parallel Upper-bound state file. Typical obligations concern admissibility, a recurrence/invariant, conversion to the requested Guarantee, stopping/output validity, or total Resource accounting. Combine, omit or add obligations to fit the proof; there is no mandatory count, order or linear chain. An iteration estimate needs the correct conversion when one iteration uses several queries, an inner solve, adaptive sampling or success amplification.

Create independent Claims only when the statements are meaningful research targets or shared dependencies. A route has its stable `route_id` and `target_claim_ref`; each obligation has a stable `id` and exact `target_claim_ref`, with `owner_attempt_ref`, `evidence_refs`, `remaining_gap` and `closing_argument_ref` when useful. Use `expected_relation="supports"` for a required positive Lemma. `work_status="active"` records ongoing work; `completed` describes work, not mathematical validity. Never write derived `satisfaction`, `mathematical_state` or `current_trust` into an obligation.

The service reports an obligation as `satisfied` only when its closing Argument is currently supported, its audit certifies the same target Claim in the expected direction, and that Claim has the corresponding current status. A refuted required Lemma blocks that route. Nonempty `evidence_refs`, child completion or an unrelated proved Claim cannot close the obligation.

Parallelize only useful independent work through the common Orchestrate skill. `spawn_task` creates a general subcell in this version; provide the exact local Claim, Algorithm construction and necessary conditions in `context_refs` and instructions. Read returned fixed records, explicitly import selected results with `collect_task(import_refs=..., request_id=...)`, and use the returned parent refs. Imported Arguments are candidates requiring parent audit. After component obligations are satisfied, write and check the composition Argument to the parent Upper-bound Claim; all components being satisfied is not itself the parent proof.

## 4. Constraints

- Do not replace a full-class, uniform Guarantee with performance on sampled instances, a conditional special case, or a Guarantee for a different Algorithm.
- Respect the declared Resource and risk convention. Account for actual calls, inner work or repetition where counted; do not silently equate iterations and Oracle queries.
- Preserve unresolved conditions, gaps and conflicts. Library provenance, stored labels and subcell acceptance do not replace current applicability and audit evidence.
- Keep the common permissions, budget, identity and review contract. This skill does not dispatch a dedicated Lower-bound/Experiment Cell or modify Programme mode.

## 5. Output

Leave the exact Algorithm/Claim relationship, useful Arguments, their actual audit refs, and remaining gaps in the existing records. Update `proof_state` when the route or obligations change. Record the chosen skill, decision reason and useful output refs in the relevant Attempt; no per-turn form is required.

For a complete candidate, prepare a self-contained draft connecting the Algorithm to the assigned Guarantee and full cost, then use the common main-task submission workflow. The runner's independent verifier and report confirmation still determine completion. For partial work, distinguish proved components, conditional progress, candidate constructions and the concrete missing composition; preserve them through the normal handoff.

## 6. Records involved

| Object | Use and reference |
|---|---|
| Claim `claims` | Fixed Guarantee and meaningful component statements; refs from archive/retrieve. |
| Example `examples` | Reusable Algorithm construction/variant and separately checked properties when needed. |
| Argument `arguments` | Actual derivation, composition, scope and cost; optional `complexity_profile`, explicit conclusions and dependencies. |
| Source `sources` | Library or external provenance, exact source locator, relevant fixed content and read coverage. |
| Attempt `attempts` | Method choice, bottleneck, useful variants, result refs and substantive route review. |
| `proof_state` | Current route, obligation targets and closing evidence; computed validity comes from the service. |
| `reviews`, subcell import results | Audit evidence and provenance; use fixed parent refs after import, not child trust labels. |

## 7. MCP tools

| Tool | When used |
|---|---|
| `retrieve` | Restore exact records, inspect obligations and current trust before reuse. |
| `recollect` | Search/read the shared Algorithm/Theorem libraries or follow relevant relations on demand; never a new Algorithm-only MCP. |
| `archive` / `archive_result` | Save actual constructions, Claims, derivations, Attempts or state; batch refs via `local_key` when helpful. |
| `audit` | Check a complete local Argument or claimed Example property before relying on its certification. |
| `spawn_task`, `task_status`, `collect_task` | Delegate a precise component, inspect its result and explicitly import chosen fixed records; follow Orchestrate. |
| `job_status` | Recover the original asynchronous tool result before dependent work. |
| `budget_status`, `finish_handoff` | Save useful progress within the existing budget and hand off unfinished work. |

Other common skills retain their tools and permissions; exact signatures and record constraints are in the installed `protocol.md` and current MCP schema.
