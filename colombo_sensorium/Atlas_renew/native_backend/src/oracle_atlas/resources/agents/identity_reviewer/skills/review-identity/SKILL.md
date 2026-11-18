---
name: review-identity
description: "Verify the final existing/new identity recommendation, retrieval coverage, specification normalization, and view mapping to prevent duplicate settings and incorrect merges."
---

# Independent Identity Decision Reviewer Skill

## Review scope

1. Read `standards/identity.md` and the review schema. Verify that the subject candidate/Atlas version binds to the current task. Diagnose missing fixed identity materials as protocol issues; a missing normalization field is not a mathematical counterexample.
2. Actually read the candidate and closest Atlas specifications. Check agreement of the common task/model/native oracle/output/metric/resource, and whether algorithm-scope/guarantee differences belong in views. A "new" view mapping must justify a new view; do not silently change an existing view's permissions.
3. Check normalization of inputs, outputs, parameters, metrics, probabilities, and costs. Interface inclusion, model inclusion, and reduce-to relationships do not automatically imply equivalence. Check whether the argument relies only on matching rates or ignores free auxiliary computation/full-function access.
4. Inspect recall_audit's actual strategies, unresolved neighbors, inventory version, and retrieval coverage: was new based only on an empty top-k; are reasonable aliases/parents missing; do credible neighbors remain unread; was a scope mismatch mistaken for nonexistence? Use authorized Atlas search for targeted checks when needed. Defer if scale becomes unmanageable; do not require a full-library certificate.
5. Unknown core oracles/protocols must block identity. Locate the actual scope of individual algorithm-parameter, theorem-proof, or cost-accounting uncertainties; do not mechanically turn pending bound verification into an identity blocker.
6. Approve existing/new only with adequate grounds. Explicit correctable error -> revise; insufficient evidence -> defer. Preserve the history of partial resolutions. Save the review and return a small handoff. Subsequent profile research still requires independent scientific review.
