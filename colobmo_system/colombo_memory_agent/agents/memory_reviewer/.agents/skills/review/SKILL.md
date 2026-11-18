# Incremental Review

Check six aspects: object identity/variant selection; scientific rules and statements; all necessary conditions and quantifiers; actual conditions for component reuse; evidence depth; and tags, locators, and versions.
Key distinctions: fresh/same-sample; value/gradient/value+gradient; fixed worst-case budget/expected budget; E||g||, E||g||², RMS; general randomized algorithms/span/zero-respecting; single-resource/joint budgets; and dimension requirements as a function of accuracy.

Check the direction of lower-bound transfer: a lower bound for a larger function class does not automatically apply to a subclass; hardness for a weaker oracle does not automatically apply to a stronger oracle; failure of a fixed method is not a lower bound for arbitrary algorithms.
Check upper bounds: all primitives must be implemented and charged under the target oracle; proximal operations/Hessian inverses cannot be assumed free.
Navigation must not combine conditions across variants, treat not_assumed as false, or silently remove unknown items.

Output for each item: id, actual record_hash, decision, content_fidelity, navigation_fidelity, proof_review, and issues.
issue fields: category, severity, target, reason, impact, repair, and evidence.
severity is blocker/usage_restriction/info. target is a valid JSON Pointer into the current record.
When a complete local proof passes review, proof_review is complete_local_argument_checked.
A standard literature statement may receive statement_and_source_checked; explicitly mark proofs not independently checked as not_checked.
Revision requests must be actionable, such as "add the condition allowing the same sample to be queried at two points," rather than "check everything again."
