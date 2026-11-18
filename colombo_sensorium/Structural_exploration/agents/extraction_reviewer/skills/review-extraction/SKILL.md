---
name: review-extraction
description: "Independently verify candidates' extraction of paper specifications, scopes, and label facts, distinguishing extraction omissions from faithfully recorded source uncertainties."
---

# Independent Specification Extraction Reviewer Skill

## Independent verification

1. Read `standards/eight_axes.md`, `standards/labels.md`, and the issue layers in `standards/evidence.md`. Then call schema_read(review) and read the frozen extraction and each candidate. Verify actual sources through references; do not substitute the producer's summary for the original text.
2. Check completeness of tasks/native operations, especially layered objects, full-gradient/single-coordinate/subdifferential distinctions, public parameters, output spaces, metric formulas, and aggregation order. Verify online timing, sampling dependence, algorithm classes, and costs. Do not elevate one algorithm's restriction to a restriction on all admissible algorithms.
3. Verify that every identity-critical statement has a location and accurate scope. Missing fields are protocol issues; miscopied/omitted source statements are extraction issues. For OCR/readability issues, locate the original formula first; do not declare it erroneous before verification.
4. Use vocabulary_lookup to verify labels' eight-axis placement, concept definitions, parent-child relationships, source_pointer, and bindings to the same operation/view/object. Common human-facing parent classes should retrieve the candidate; machine unknown must not be disguised as false or exact.
5. Give a per-candidate judgment: critical extraction omission -> revise; inaccessible critical materials preventing a judgment of fidelity -> defer; faithful extraction with necessary unknowns recorded -> approve. Remaining bound-proof questions may use only blocks=[bound], with an explanation of why they do not block extraction. Explicitly retain an identity blocker for unknown native interfaces that affect identity.
6. When a historical issue is partly resolved, state the resolved portion and remaining uncertainty; removal of repaired extraction blockers is allowed. Do not require an open issue to retain every historical blocker permanently.
7. Save an independent review. Approval means only that extraction responsibilities are complete; it does not certify identity or the currently optimal bracket, and does not grant permission to write Atlas.
