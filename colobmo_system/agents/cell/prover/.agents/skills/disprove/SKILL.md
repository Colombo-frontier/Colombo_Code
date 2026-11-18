---
name: disprove
description: Actively test whether a mathematical assertion designated by the main agent is false, construct a counterexample that satisfies its assumptions but violates its conclusion, or establish an argument for its negation. Use when a conclusion may be too strong, assumptions may be insufficient, or an intermediate step may be invalid.
---

# Disprove: Seeking a Refutation

## 1. Objective

Test whether the designated assertion is false, construct a counterexample satisfying the assumptions but violating the conclusion, or establish an argument for its negation; precisely delimit how the refutation affects the original objective and route.

## 2. Inputs: What to Read Before Starting

| Material | Reading Requirements |
|---|---|
| `problem.md` and, when present, `TASK.md` | Confirm the original problem or the subcell's local objective and deliverables. |
| Current `proof_state` and relevant Attempts | Recover the objective, routes, scope of previous failures, and experimental choices awaiting reassessment. |
| Target Claim or argument step under examination | Read the fixed version and identify the conditions and quantifiers of both the assertion and its negation. |
| Relevant constructions, arguments, experiments, and dependencies | Read the necessary content and actual scope of coverage; use `retrieve` to check `current_trust` before reusing evidence. |

First verify the target's version, definitions, assumptions, quantifiers, and parameter ranges, and state its negation. If no local objective is specified, examine the original problem. Create or reuse a precise Claim for an assertion studied independently; an existing argument step can be referenced directly when checking that step. Refuting an intermediate assertion, a candidate sufficient condition, or a proof step rules out only the corresponding conclusion or route.

Independently retrieve relevant constructions, arguments, and failure scopes, and read the necessary dependencies; follow the workspace [protocol.md](../../../protocol.md#records-and-audits) for records and audits.

## 3. Procedure: How to Seek a Refutation

### 3.1 Satisfy the Assumptions and Violate the Conclusion

Start with the most questionable assumption or conclusion. Existing constructions, low-dimensional or degenerate cases, and boundary or extreme parameter values may reveal the issue; choose a direction that explains the concern. An object violating the assumptions may clarify their role, but is not a counterexample to the target.

The quantifiers determine the required evidence. A single object can refute some universal assertions; refuting existence or uniformity may require a general argument or a parameterized family of constructions. State how parameters are chosen, which quantities they depend on, and why they satisfy the quantifiers of the negation.

Specify each candidate construction exactly, check every assumption, and then calculate or argue why the conclusion fails. Numerical anomalies are only leads requiring explanation; state the specific need when further experiments or literature searches are required. Constructions that do not become counterexamples but illuminate the role of assumptions, equality cases, or useful properties may also be retained.

When counterexample construction is blocked, or a related conjecture / pattern is uncertain, and batch sampling, enumeration, strategy search, or simulation could narrow the search or provide insight, the current agent may use `$experiment` as needed, design the computation, read its actual output, and then return to this skill; neither another agent nor prior exhaustion of proof routes is required. Use experiment directly when explicitly requested by the user. Record choices actually considered and next steps in the Attempt; keep simple arithmetic and a few directly calculable examples in this skill, without routine experiments for every Claim or written reasons for omitting them. For a floating-point violation, first check the domain, assumptions, and numerical error, then confirm it using exact computation or reliable error bounds; failure to find a violation does not prove the Claim.

If an error is found in the original proof, locate it and explain its consequences; unless the negation of the target has been proved, report only that this argument has not been established.

### 3.2 Record the Actual Scope of the Refutation

Store the construction in an Example and check properties such as satisfying the premises, violating the conclusion, and constituting a counterexample to the target; store the argument for negation in an Argument, with `conclusions` referencing the precise target and direction `refutes`. Constructions belong in `subject_refs`; only established premises belong in `dependencies`. An Argument's `proved` status here means that the negation has been proved, not that the original target holds. Use a new Claim for a revised statement with different assumptions or conclusion; use a new Example when formulas or the scope of the construction change.

## 4. Constraints: Limits on Permissible Conclusions

- Complete arguments for negation and properties claimed for Examples require local audits under the protocol; candidates and numerical anomalies cannot directly serve as audited refutations.
- Whether a record remains usable depends on `current_trust`, not historical `proved`, `checked`, or `audit_id` values alone.
- Handle specific concerns about certified Arguments through the challenge channel; an erroneous argument does not automatically prove the target false.
- A subcell reads only local records and authorized `context/`, and returns local results to its parent; imported results still require re-auditing by the parent.

## 5. Outputs: Scope of the Refutation and Remaining Checks

Return references to evidence, audits, and remaining checks, and distinguish an audited refutation, a candidate awaiting review, no refutation found so far, and insufficient evidence. Refuting a lemma required by one route means that the route is blocked, not that the proof obligation has been discharged; identify what remains possible for the original objective. If the same proposition has both valid supporting and refuting evidence, retain both, stop treating the objective as complete on that basis, and refer the conflict to the main agent for review through existing channels.

The Attempt summarizes the construction families actually examined, why they violated assumptions or failed to invalidate the conclusion, obstacles to the negation argument, and reusable components. When a key counterexample changes the route, briefly review exactly what it rules out and what should change next; do not generalize the failure of one construction into the impossibility of an entire method. Failure to find a counterexample does not imply that none exists, and budget exhaustion or tool failures do not constitute mathematical conclusions. The main agent maintains the overall state and final submission.

Record this use of `skill` and `decision_reason` in the Attempt. If an intermediate handoff is needed, preserve the checks completed so far using `$handoff`; do not present an unfinished search as a mathematical verdict.

## 6. Relevant Record Objects

Read and write records in the current `memory/` according to the actual outputs; obtain fixed references from tool receipts rather than assembling evidence from matching IDs.

| Object (Collection) | Use and Read/Write Behavior at This Stage | Entry Point |
|---|---|---|
| Claim `claims` | Read the precise target to be refuted; create a new Claim when assumptions or the conclusion change. | Designated target reference, current `proof_state`, or `retrieve`. |
| Example `examples` | Store candidate constructions and properties such as satisfying the premises and violating the conclusion; audit individual properties. | `archive` / `archive_result` receipts or relevant references. |
| Argument `arguments` | Store the negation argument and its `refutes` relation; audit when complete. | Fixed ID, revision, and conclusion target reference. |
| Attempt `attempts` | Store the scope of checks, reasons for failure, reusable components, and route or experiment decisions. | References in `proof_state` or `retrieve`. |
| `proof_state` | Read current objectives and obligations; the main agent maintains the overall state using the returned results. | `retrieve(kinds=["proof_state"])`. |
| `experiment_result` | When computation is involved, read the actual scope, outputs, errors, and execution status. | Experiment references in the relevant Attempt. |
| `reviews` | Read audits and confirmed objections; do not modify certification status yourself. | Audit receipts and record references. |

## 7. MCP Tools Used

Invoke tools when applicable; see `protocol.md` and tool definitions for complete parameters. Not every refutation requires every tool.

| Tool | When to Call | What It Reads or Produces |
|---|---|---|
| `retrieve` | When identifying the target, finding constructions and failure scopes, or reusing evidence. | Fixed records, complete derivations, and current trust status. |
| `archive` | When saving or revising an individual output or Attempt. | A fixed-version receipt; revisions require the original ID and `expected_revision`. |
| `archive_result` | Optionally, when related Claims, Examples, Arguments, or other records need to be saved together. | A batch receipt and mapping to official references. |
| `audit` | When a complete negation argument or Example property is ready to serve as evidence. | Local audit results; a passing negation Argument certifies the negation direction. |
| `challenge_argument` / `resume_argument_challenge` | When there is a specific concern about a certified argument in this task, or when continuing the original challenge. | Objection checks and confirmation status; concerns about read-only parent material are returned to the parent. |
| `budget_status` | When assessing remaining time or preparing to conclude. | The current time allowance; switch to `$handoff` when a handoff is needed. |
