---
name: verify-progress
description: Check returned Results before Brain update, or independently review the complete integrated ProofDraft, confirming precise Claims and scope while distinguishing empirical evidence from mathematical proof.
---

# Verify Result or ProofDraft

Call read_review_package using review_package_ref from context and read all required_records. Use actual required_checked_refs/allowed_refs; complete pinned content already read need not be retrieved again, but key attachments must still be inspected.

## Result

Compare the actual results with the pinned Setting and Task assignment/package, checking definitions, quantifiers, Oracle, Algorithm Class, Guarantee, Resource accounting, and regime scope. Read the Proofs and dependencies supporting the conclusions rather than relying only on summaries or local acceptance.

Confirm each Claim that actually holds: id, statement, assumptions, scope, kind, expression, and evidence_paths. kind is upper_bound/lower_bound/lemma/comparison/empirical; Bound expressions and comparison gaps must be accurate, and paths must come from that Result. Do not fill in a confirmed Claim without evidence. Retain remaining findings even when some Claims hold; assess completion_status against all responsibilities in the original assignment.

For a comparison, check that both scopes concern the same problem, polylog factors fall within the allowed policy, and constants/exponents are independent of tracked parameters. Do not mix Guarantees or Resources, or substitute counts of overlapping rows for coverage. kind=comparison requires comparison_bounds, recording each compared direction/expression/scope/assumptions and including both Lower and Upper Bounds; do not confirm only a gap string without binding the actual Bounds. Preserve conditional comparison assumptions in the regime; do not remove conditions and then claim near-optimality.

For a Result with evidence_kind=empirical, read the [empirical review reference](references/empirical-review.md) and confirm only empirical Claims. Check code/data/receipts, measurements, Oracle cost, validation, and uncertainty for the current question. Experiments support conjectures but do not prove asymptotic Bounds or near-optimality.

## ProofDraft

Read the complete integrated manuscript and check self-contained definitions, assumptions, Lemmas, every Proof step, composition, regime coverage, and unresolved parts. Compare the actual scope with the original Goal and verify new comparisons rather than merely counting approved sources. Pinned source versions may be reused, but new applications and combinations still require checking.

A partial report may pass if it accurately distinguishes proved results, unresolved gaps, and conjectures; failure to solve the entire Goal must not force a false claim of completeness. Distinguish a known error explicitly withdrawn and retained as a gap from one still used as a conclusion.

Empirical motivation is not certifying evidence for a checked step. An exact computation or certificate supplied by a Proof Cell may form part of a mathematical argument, subject to checks of assumptions, complete coverage, numerical or exact guarantees, and derivation. Do not reject evidence merely because it cites computation, or substitute successful execution for Proof.

## Output

write_review uses verdict pass/revise/inconclusive; findings contain subject/reason/result_refs. checked_refs records references actually checked and authorized by the package, covering all required refs.

repair_kind=none/presentation/research: formatting, reference, and wording revisions are presentation; missing key arguments, incorrect mathematical derivations, or the need for new experiments or theory are research. pass must leave no findings and requires repair_kind=none. Submit Proof reviews according to the schema's confirmed_claims convention; do not use a review to alter the original Proof. Finish after receiving the receipt.
