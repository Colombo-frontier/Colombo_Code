---
name: lower-bound
description: Develop an optimization Resource Lower Bound through Hard Family and Proof co-design, preserving Algorithm Class, Oracle, quantifiers and output scope while tracking the actual proof obligations.
---

# Lower-bound Hard Family–Proof development

## 1. Objective

Establish the assigned Lower-bound Claim for its actual Algorithm Class and Oracle model, or complete the explicitly assigned local component. Connect an admissible construction or obstruction to the requested Guarantee and Resource. A Lower Bound is usually a positive Claim to prove; the establishing Argument uses `supports`.

## 2. Inputs

Read the assignment, current `proof_state`, relevant Attempts and fixed Claim/Example/Argument refs. Identify Function Class, Algorithm Class, Oracle query/feedback and allowed information, initialization, Output/Metric, Resource, randomness, probability convention and parameter regime. Preserve consequential unknowns instead of filling them with convenient assumptions.

Determine whether the Task fixes a Family or allows construction. Search `recollect` with relevant `hard_family`, `theorem` or `relation` kinds when useful; read precise scope, mechanisms, dependencies and source coverage. A source-backed entry or metadata match is not current-task certification. Preserve the returned library ref and actual read content through existing Source and evidence fields. Do not preload the Library or limit new constructions to its entries.

## 3. Method

### Fix the mathematical responsibility

Distinguish a Lower Bound for one Algorithm, a restricted Algorithm Class and the full admissible class. In a standard fixed-instance randomized setting, the hard instance may depend on the Algorithm's identity/distribution and public budget, but not on its realized private random seed. A distributional argument must justify its transfer to the required worst-case Guarantee. Adaptive Oracle responses require the consistency or realizability demanded by the assigned model; a changing sequence of incompatible functions is not a fixed-instance proof.

Specify the construction and Oracle together: public/hidden parameters, complete feedback, query domain and any sample coupling. Check Function Class membership and parameter normalization. A gradient-only obstruction does not automatically cover an Oracle that also reveals exact values; justify any change of interface through an appropriate information/cost simulation. Do not add noise or precision restrictions to an exact Oracle without authorization and a valid transfer Argument.

Use an existing Example for a reusable Family/variant when useful. Keep mathematical changes under the common identity rules. Put the actual target in a Claim, relevant construction in Argument `subject_refs`, genuine premises in `dependencies`, and the proved target in `conclusions` with relation `supports`. A library construction can be identified through fixed Source evidence when another local object adds no useful identity.

### Let the bottleneck guide co-design

| Evidence about the bottleneck | Possible action |
|---|---|
| Construction falls outside the assigned class or parameter regime | Repair admissibility, scaling or embedding within the allowed design scope. |
| Allowed queries or feedback reveal the hidden structure too quickly | Modify the permitted construction or revise the transcript/progress Argument. |
| Current Proof covers only restricted Algorithms | Establish the missing lifting Argument, or report the restricted result and the remaining gap. |
| Hardness is established but does not imply the requested Output error or cost | Improve reduction, error conversion, dimension/scaling calibration or Resource accounting. |

Choose chain, indistinguishability, information-theoretic, reduction or other methods when they serve the actual problem; none is mandatory. Uncertainty can motivate a focused Lemma or experiment. An Algorithm defeating the current candidate Family defeats that candidate mechanism, not automatically a class-wide Lower Bound over the full Function Class. Refuting the full Claim requires the corresponding uniform counter-Guarantee or another valid implication.

A failed proof attempt is not evidence that the target is impossible. Fixed-Family Tasks may report useful alternatives, but cannot silently substitute them for the assigned object. Record significant route changes and their reasons in the existing Attempt `route_review`; preserve valid dependencies and re-audit affected Arguments after construction or scope changes.

### Track actual obligations and compose the result

Use existing `proof_state.routes`. Useful obligations may concern Family/Oracle admissibility, transcript information or progress obstruction, output-error conversion and the target Resource Lower Bound. Add randomized or unrestricted-query lifting, dimension or normalization Claims only when the route needs them. This is not a fixed number or linear checklist.

Each route has `route_id` and `target_claim_ref`; obligations have `id` and exact `target_claim_ref`, with `owner_attempt_ref`, `evidence_refs`, `remaining_gap` and `closing_argument_ref` as useful. A required positive Lower-bound Claim or Lemma uses `expected_relation="supports"`. `work_status="active"` or `completed` tracks work, not correctness. Never write computed `satisfaction`, `mathematical_state` or `current_trust` fields.

An obligation is satisfied only through current, correctly scoped certification of the target and its closing Argument. Construction alone, a completed work label or an unrelated proved Claim cannot close it. Component obligations still need a composition Argument establishing the parent Lower-bound Claim.

Delegate independent useful components through Orchestrate. Current subcells use the General pack; give exact local scope and selected construction evidence in their authorized `context_refs`. Read returned fixed records and explicitly import chosen results with `collect_task(import_refs=..., request_id=...)`. Use the returned parent refs and audit imported Arguments at the parent before relying on them.

## 4. Constraints

- Do not promote fixed-Algorithm, zero-respecting, span-restricted or deterministic results to a broader Algorithm Class without a valid bridge.
- Cover the Output actually allowed by the Task, including an unqueried output when allowed; failure of queried iterates alone may be insufficient.
- Keep Oracle feedback, adaptivity, sample coupling, Resource and expectation/probability conventions explicit. Preserve dimension and parameter restrictions needed by the Argument.
- Empirical failure, catalog status and source provenance do not certify a class-wide Lower Bound. Neither several difficult examples nor separate parameter bounds automatically compose into the target rate.
- Follow the shared evidence, budget and review contract; this skill does not alter Programme mode or directly dispatch other specializations.

## 5. Output

Save the exact construction/Claim relationship, Arguments, actual audit refs and remaining gaps in existing records. An optional Argument `complexity_profile` may summarize Algorithm/Oracle scope, Resource, regime and relevant refs; it cannot hide assumptions or replace the complete Claim and Proof.

For a complete candidate, prepare the normal self-contained main-task draft and submission, including the full composition and actual scope. For partial work, distinguish construction properties, restricted-class Lower Bounds and the missing lifting or conversion. Preserve them for Brain's next Task rather than declaring the original responsibility completed. Independent verification and report confirmation still determine acceptance.

## 6. Records involved

| Object | Use |
|---|---|
| Claim `claims` | Fixed Lower-bound target, scoped component statements and required bridging Claims. |
| Example `examples` | Reusable Hard Instance/Family/distribution construction with separately checked properties. |
| Argument `arguments` | Admissibility, hardness, transfer, error conversion and final composition with exact conclusions/dependencies. |
| Source `sources` | Library/external provenance, fixed locator and actual read coverage. |
| Attempt `attempts` | Method choice, bottleneck, useful variants, result refs and substantive route review. |
| `proof_state` | Routes, obligations and closing refs; validity is computed by the service. |
| `reviews`, import results | Scoped audit evidence and provenance; imported child trust is not parent certification. |

## 7. MCP tools

| Tool | When used |
|---|---|
| `retrieve` | Read exact records, current trust and obligation state. |
| `recollect` | Search/read relevant Hard Family, Theorem and Relation entries on demand. |
| `archive` / `archive_result` | Save actual constructions, Claims, Arguments, Attempts and state under the common schema. |
| `audit` | Check a complete scoped Argument or a claimed Example property. |
| `spawn_task`, `task_status`, `collect_task` | Delegate a precise component and explicitly import selected fixed results. |
| `job_status` | Recover the original asynchronous result before dependent work. |
| `budget_status`, `finish_handoff` | Preserve useful incomplete work at the existing budget boundary. |

Other common skills retain their tools. Exact signatures, permissions and record constraints come from installed `protocol.md` and the current MCP schema.
