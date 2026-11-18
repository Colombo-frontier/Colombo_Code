---
name: update
description: After Result Verifier review, record Task completion assessments and the GoalProgress Bracket, retaining unresolved responsibilities without rewriting the complete Proof.
---

# Update

First inspect the pinned Task, formal Result/Verifier review, and existing GoalProgress. Local acceptance does not replace outer review, and some confirmed Claims do not imply completion of the entire Task. After a result is returned, read the complete research archive for that attempt as needed rather than relying only on summaries.

update.admissions distinguishes actual completed parts, remaining work, completion_status, and the evidence verdict. Adopt only Claims/scopes actually confirmed by the Verifier. Errors, inconclusive outcomes, execution failures, and cancellations do not establish that the target is false.

update.progress:

- overall: describe the current overall research progress.
- status and Goal items: record overall status and individual responsibilities separately; one valid Bound does not establish completion of the entire Goal.
- bracket.bounds: each certified item's expression/scope/assumptions/direction exactly matches the review's confirmed Claim; baseline/unknown entries are not certified automatically.
- bracket.regimes: Lower/Upper references, gap, conjectural candidate rate/basis, near-optimality status, and remaining work. Preserve the assumptions of conditional comparisons in regime.assumptions, exactly as in the review. Do not compare across different views/Oracles/Guarantees/Resources or treat overlap as a partition.
- remaining: unmet requirements.

Registering a reviewed Claim does not require another review of the same Proof; new comparisons/transfers/compositions still require verification. Assign an explicit auxiliary Task, or present them at final integrate for the final Verifier. Intermediate update does not require a complete ProofDraft.

## Empirical Results

When adopting a Result with evidence_kind=empirical, use empirical Claims and fixed artifacts actually confirmed by the outer Verifier; local accepted=false does not imply failed empirical review. These findings may inform candidate-rate assessments, record Algorithm candidates, Hard Instances, mechanisms, or explicit statements for Proof Cells, and link to the original Result/review. They cannot directly certify Bracket Bounds, near-optimality, mathematical supported/refuted status, or Pruning premises.

Report outcome=inconclusive does not imply admission.verdict=inconclusive. If the Verifier confirms reliable evidence and completion_status=completed, and the report answers the original Task's question, the admission may be accepted/completed while retaining the mathematical Goal's gap. If only some responsibilities are addressed, keep completion_status=partial; retain corresponding admission uncertainty only while the report's reliability remains unresolved.

Reuse the scientific review's checks of design and data; revisit artifacts only for new, specific concerns. Choose a concrete next Proof question, improve an Algorithm / Hard Instance, extend distinguishable scales, or discontinue an unproductive direction. Substantive corrections requiring a new experiment belong in a new repair Task.

Next execute the prune Skill and submit admissions, progress, and prunes together once through record_results. Use next_action=plan when supplementary dispatch is needed, and explicitly leave substantive repair findings for plan. Controller schedules subsequent calls; do not start a Cell directly within update. Finish after receiving the receipt.
