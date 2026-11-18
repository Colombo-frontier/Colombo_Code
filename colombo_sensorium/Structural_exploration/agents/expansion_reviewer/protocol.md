# Expansion Reviewer: Collaboration Protocol

The main kind is `expansion_review`. Read its schema and the frozen assignment before saving any review. The schema is authoritative for exact field representations.

## Fixed subject and decision

Bind `subject_ref` to the assigned expansion and `candidate_ref` to its exact frozen candidate. Provide `scope_assessment`, `well_posedness_assessment`, `value_assessment`, `reason`, scoped `issues`, and actionable `required_changes`.

- `approve`: the defined candidate is suitable for identity verification and subsequent research; no unresolved issue blocks its specification.
- `revise`: a concrete omission, inconsistency, or unsupported defining assertion can be repaired within this opportunity's authorized scope.
- `defer`: necessary information or a credible peer comparison remains unresolved; state exactly what would resolve it.
- `exclude`: the direction is invalid, outside the approved scope, already represented by a supplied pending candidate, or has no justified independent value in this batch. Preserve the reason in the batch ledger.

Do not use missing bounds as an automatic specification blocker. An unknown native protocol that determines the candidate's identity is a real blocker even if the proposed title is plausible. Keep publication/bound-only concerns in their actual scope.

## Pending-candidate comparisons

For each pending candidate supplied by the controller, return exactly one `pending_comparisons` entry binding its actual reference, with relation `distinct`, `equivalent`, or `unresolved` and a substantive reason. Normalize representations and check common specifications, views, and regimes. A shared theme or one-way reduction is not equivalence.

Set `duplicate_of_ref` only to a supplied candidate for which the comparison is equivalent. Use `exclude` for that redundant candidate so the controller can retain its provenance without launching duplicate research. Do not approve while a credible pending peer remains unresolved. These comparisons do not replace whole-Atlas matching.

## Completion

Save the independent review with formal dependencies, then return the common small handoff. A complete review may have any of the verdicts above. Do not equate handoff completion with approval. On revision, check the changed candidate and every prior issue's actual remaining scope; do not require a partly resolved issue to retain obsolete blockers.

## Parameter scope and later closure obligations

Preserve the full authorized parameter domain and explain joint variables, fixed structural parameters, uniform constants and any diagnostic slice in the existing candidate model/view fields. Do not replace the full request by a convenient accuracy-versus-dimension slice or hide a new oracle solve/cost. Endpoint or zero-query cases are guarded regimes, not new primary status codes. A designed complete contract can pass specification review with missing bounds; it is not an optimality or complete-literature certificate.

Later research must create joint-analysis v2, assess compatible/replacement/resource-projection routes, and publish proved closed regions natively or keep publication pending. Seed/neighbor labels and historical proofs grant no current approval. Use standards/joint_parameter_standard.md for a concrete scope question, without adding profile-only analysis fields to the candidate or doing the final profile review in this stage.
