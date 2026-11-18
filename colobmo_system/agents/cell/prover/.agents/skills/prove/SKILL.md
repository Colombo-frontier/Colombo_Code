---
name: prove
description: Advance a designated mathematical objective or proof gap through substantive derivation; when blocked, construct examples satisfying the current assumptions, extract useful mechanisms, and return to the general proof.
---

# Prove: Advancing a Proof

## 1. Objective

Establish a proof of the full problem, an auxiliary proposition, or a specific gap; when direct progress is blocked, use concrete examples to understand the obstacle and then return to the general derivation.

## 2. Inputs: What to Read Before Starting

| Material | Reading Requirements |
|---|---|
| `problem.md` and, when present, `TASK.md` | Confirm the current problem; a subcell follows its local objective and deliverables. |
| Current `proof_state` and relevant Attempts | Recover the precise objective, routes, remaining obligations, and experimental decisions awaiting reassessment; if no state exists, start from the problem. |
| Target Claim or designated argument step | Verify definitions, assumptions, quantifiers, parameter ranges, and the fixed version. |
| Relevant Arguments, Examples, and dependencies | Read the necessary full evidence; use `retrieve` to check `current_trust` before reuse. |
| Revision feedback or existing experiments | During revision, read the reports or errors referenced by `draft.md` and `submission.json`; when experiments are involved, read their conditions, coverage, and limitations. |

If no local objective is specified, address the original problem. Create or reuse a precise Claim for an independent, complete research objective; when continuing an existing route, retain its fixed target and local assumptions. An existing argument step may be referenced directly when only that step is being checked.

Independently use `retrieve` or record files to find relevant arguments, examples, and attempts, and read the required full evidence and dependencies; the main agent need not preselect material. Follow the workspace [protocol.md](../../../protocol.md#records-and-audits) for records and audits.

## 3. Procedure: How to Advance a Proof

### 3.1 Turn Assumptions into Usable Derivations

Expand definitions, derive immediate consequences, complete the necessary calculations, or apply established results. When transferring a method, explain why its required assumptions and structure hold here. A method or theorem name cannot replace an actual derivation.

Cells and subcells may use [explore](../explore/SKILL.md) as needed to understand the background, generate ideas, compare routes, or find external results, then bring useful insights back to the current proof.

You may also work backward from the conclusion to sufficient conditions and connect them to the assumptions. State the direction of the reduction: what remains to be proved, and how it would imply the original objective. Failure to prove a sufficient condition means only that this route is incomplete.

Save derivations with substantive progress as Arguments, and state missing justification in the corresponding steps. Set `conclusions` to the Claim actually being proved, with direction `supports`; place objects under study in `subject_refs` and only established premises in `dependencies`. Extract an assertion into a Claim when it becomes an independent objective, will be delegated, or will be studied across rounds; a one-off equality may remain within the derivation. Create a new Claim when the target's assumptions or conclusion change; do not overwrite the old proposition.

### 3.2 Use Examples to Understand Obstacles, Then Return to the General Case

When direct progress is blocked, identify the obstacle before choosing a concrete object that can reveal it. Low-dimensional or low-order cases, boundary cases, equality cases, and special constructions may all be useful, but retain the structure responsible for the difficulty wherever possible; if a simplification removes the difficulty, explain what it can still illuminate.

Check every condition of the current objective for the example, identify any additional special properties, and calculate or prove properties relevant to the obstacle. Call it a positive example for the target only after checking the target conclusion as well; save its construction, target relationship, and property justifications as an Example, and audit the claims according to the protocol.

Look for generalizable identities, estimates, invariants, constructions, or intermediate propositions in the examples. Distinguish proved properties of an example from the general conjectures it inspires, and check whether the observed behavior relies on special structure. Compare different types of examples when necessary, reformulate the insights as explicit steps to be proved, and try to close the original gap; accumulating positive examples cannot replace a general proof.

If a suspected violation appears unexpectedly, preserve the construction and completed checks and return them to the main agent for assessment. Use `disprove` to actively expand a counterexample search; arrange computational experiments or parallel routes according to the relevant skills and role permissions.

When a proof is blocked at a particular step, or an intermediate conjecture / pattern is uncertain, and batch sampling, enumeration, strategy search, or simulation could provide insight, the current agent may use `$experiment` as needed, design the computation, read its actual output, and return to this skill; neither another agent nor prior exhaustion of proof routes is required. Use experiment directly when the user explicitly requests it. Keep simple arithmetic and a few directly calculable examples within this skill, without routine experiments for every Claim or written reasons for omitting them. Record choices actually considered and next steps in the Attempt; when an `experiment_result` already exists, read its assumptions, scope, and limitations before trying to turn observations into a general argument.

## 4. Constraints: Limits on Permissible Conclusions

- Complete Arguments and properties claimed for Examples require local audits under the protocol; saving a candidate does not automatically confer certification, and historical passing labels cannot replace the current `current_trust`.
- Recheck affected parts when assumptions, derivations, or dependencies change; handle specific concerns about certified arguments through the protocol's challenge channel rather than substituting a label change for revocation.
- A subcell reads only local records and authorized `context/` snapshots; it returns local outputs and does not perform a main-task submission.
- The runner generates the main task's `accepted` status and `manuscript.md`; this skill must not write them itself.

## 5. Outputs: Results That Support Further Progress

When changing methods or ending the round, preserve derivations that remain valid and the most specific remaining obligations and obstacles. The Attempt explains why this route was blocked and the scope of the failure, to prevent identical repetition; unorganized ideas may temporarily remain there. When a key counterexample, a failed connection, or a change in assumptions occurs, or when further investment is planned despite an unchanged bottleneck, perform a brief `route_review` under the protocol and identify the next check that can distinguish the routes; a repeated review every round is unnecessary.

Return references to the target, Attempt, key outputs, and audits, distinguishing a complete candidate, partial progress, and stagnation. A complete candidate should have an Argument that can be checked continuously; if unfinished, state what must be resolved next. The main agent handles final submission under the protocol.

For every use of this skill, save `skill`, `decision_reason`, outputs, and obstacles in the Attempt. Update `proof_state` when the route changes or the round ends; when a handoff is needed, save the work using `$handoff` and end the round.

## 6. Relevant Record Objects

Objects reside in the current workspace's `memory/`; locate them using fixed references in tool receipts. Save records according to the actual outputs; not every type is required every round.

| Object (Collection) | Use and Read/Write Behavior at This Stage | Entry Point |
|---|---|---|
| Claim `claims` | Read or register the precise objective; create a new identity when the mathematical content changes. | Current target reference, `proof_state`, or `retrieve`. |
| Argument `arguments` | Store a complete candidate or partial derivation, its `supports` conclusion relation, and actual dependencies; run a local audit when complete. | `archive` / `archive_result` receipts; read by ID and revision. |
| Example `examples` | Store constructions used to understand obstacles, their properties, and target relationships; audit properties as needed. | Relevant fixed references, or `retrieve` by target. |
| Attempt `attempts` | Record skill selection, obstacles, failure scope, and any necessary route review or experimental decisions. | Current `proof_state` references, or `retrieve`. |
| `proof_state` | Store current routes, obligations, evidence references, and next steps; revise under the same ID. | `retrieve(kinds=["proof_state"])`. |
| `experiment_result`, Source `sources` | When computation or external theorems are involved, read conditions and original evidence and follow references back to the argument. | Argument dependencies or references in the relevant Attempt. |
| `reviews` | Read audit conclusions and issues; maintained by the service. | `audit` receipts or audit references in records. |

## 7. MCP Tools Used

Invoke the tools below as needed; see `protocol.md` and tool definitions for complete parameters and record structures.

| Tool | When to Call | What It Reads or Produces |
|---|---|---|
| `retrieve` | Before recovering a route, locating evidence, or reusing a fixed version. | Relevant record contents, relationships, and derived `current_trust`; continue pagination using the cursor. |
| `archive` | When saving or revising an individual output, Attempt, or proof_state. | A fixed-version receipt; revisions use the original ID and `expected_revision`. |
| `archive_result` | Optionally, when multiple related outputs need to be saved together. | A batch of records and a mapping from `local_key` to official references; no certification is conferred. |
| `audit` | When a complete Argument has been saved or Example properties need verification. | Local audit results and a service-generated certified version or failure feedback. |
| `challenge_argument` / `resume_argument_challenge` | When a specific concern arises about a certified argument in this task, or when continuing an unfinished challenge. | Checks and confirmation status for the frozen objection; suspend use of affected evidence under the protocol. |
| `budget_status` | When assessing remaining time and when to conclude. | This process's allowance; switch to `$handoff` upon entering the closing window. |
