---
name: integrate
description: Integrate materials returned by Cells and Waves into the existing top-level self-contained ProofDraft, undergo final Verifier review, and distinguish report revisions from mathematical repairs requiring new Tasks.
---

# Integrate

Controller invokes this Skill when the Goal appears complete or research budget is exhausted. Read the pinned Setting, GoalProgress, relevant Task reviews, existing ProofDraft, and unresolved findings; consult the complete research archives of returned Cells as needed, including intermediate Lemmas, notes, Subcells, experiments, and reviews.

Submit the integration payload through record_results: summary/result_refs/update/prunes/next_action/rationale. update contains admissions, the complete proof_draft, rechecked_step_ids, and progress; prunes is empty. Use body for the text; the mutually exclusive body_source may be used only when a single pinned result already covers the Goal completely. Do not submit only references or a Bracket table.

Reuse the existing ProofDraft object. Its body must be self-contained, with definitions, assumptions, Claims, Lemmas, complete Proofs, composition, and regime coverage. Substantive dependencies cannot be replaced by “see another Cell”; provenance still uses pinned Result/path/locator references. State actual polylog factors and unresolved parts. Preserve existing step IDs; explain retired steps and retain gaps for unresolved dependencies.

New comparisons/compositions may be developed here, but they must be checked by this final Verifier and cannot be described as certified before approval. Partial progress must also be presented as a complete, reviewable report, distinguishing confirmed, pending-review, and empirical/conjectural content.

An empirical Result may support motivation, candidate bases, and open/draft steps in the body. A checked step's evidence list contains certifying sources and must not directly reference an empirical Result; body_source must not come from an empirical Result either. To use a computational finding in a mathematical Claim, a Proof Cell may reuse the pinned code/data, supply the complete argument for an exact computation or certificate, and then use it within the scope of its confirmed mathematical Claim. Partial Proof Results containing confirmed mathematical Claims remain admissible sources and must not be discarded categorically because local accepted=false; the final Verifier still assesses the present derivation and composition.

After final Verifier approval, the program formally adopts and exports the result. Presentation/reference findings may be revised within this stage; substantive mathematical findings return to plan for a repair Task using the remaining Wave/dispatch budget, rather than conducting unlimited Cell research here. If budget is insufficient, retain verified partial results and unresolved Claims.

This stage lasts at most two hours, with no revision-round limit; retry/resume does not reset the timer. Controller may start a new integrate stage only after genuinely new research returns, not through renaming or duplicate manuscripts. Finish after receiving the stage receipt.
