---
name: prune
description: Determine whether current Tasks are redundant, subsumed, or refuted_target using Verifier-confirmed mathematical Claims and an independent relation audit.
---

# Prune

After update, inspect Tasks that remain eligible for stopping. Use actual task_id/attempt_id values and pinned assignments from context; premises must be reviewed mathematical Claims, not unreviewed candidates or empirical evidence.

reason is limited to redundant / subsumed / refuted_target. Explain how the premises' scope/assumptions relate to all target deliverables while preserving independent responsibilities. An erroneous Proof does not establish that the target is false; an experimental trend does not refute a mathematical goal.

Call audit with inputs containing prune_relations and any necessary optional context. Each relation includes execution identity, reason, evidence_refs, relation_explanation, scope_check, covered_deliverables, and premises; do not fill audit_ref before the audit. Only a matching completed/pass audit may be referenced in formal prunes. The audit checks the relation under the premises and does not replace Result Verifier review of those premises.

If a long operation returns job_id, continue polling the original job_status; do not restart it because it is pending. Submit an empty array when no valid Pruning applies. There is no Scheduling stop for temporary lack of progress, resource reallocation, or an exhausted dispatch budget.

Submit prunes together with update through record_results. Controller rechecks identity/evidence, issues stops, and waits for receipts; Brain does not stop processes directly or treat a stop request as a released concurrency slot. Leave new Tasks to subsequent plan calls.
