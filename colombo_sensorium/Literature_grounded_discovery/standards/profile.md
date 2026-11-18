# Self-Contained Setting Profiles and Publication

Use professional English for component explanations, research records, and reader-facing profile titles, paragraphs, labels, tables, and evidence descriptions. Mathematical notation and structural fields follow the native Atlas. Translation must not change quantifiers, error guarantees, or costs.

## 1. Complete information for the reader

1. The task/formulation and scope, including why it belongs to the declared oracle-based task; a topic tag alone is insufficient.
2. The common eight-axis specification. Views contain differences such as algorithm permissions/guarantees, and the concrete native operations must be recoverable.
3. Definitions of quantities, guarantees, resource projections, and parameter regimes.
4. The strongest supportable upper/lower bounds, witnesses/algorithm classes, applicability domains, and corresponding results/proofs/sources.
5. Bracket tables for comparable windows and an overall status.
6. A literature/evidence catalog, necessary short analyst proofs, scope limitations, unresolved material, and the research cutoff.
7. Human navigation tags, machine-scoped facts, and legacy-ID-to-setting_id-plus-view_id aliases.

Do not embed complete papers, a year's paper leads, the entire identity-exclusion index, or private memory in `profile`. Read evidence through stable references and locators. Necessary analyst arguments must be self-contained formal propositions, not dependent on a particular run's history.

Optional `reader_markdown` may provide coherent English prose. It is frozen and reviewed with the structured profile, not freely rewritten after publication. Its mathematical definitions, regions, bounds, and status must agree with the structured fields. Prose cannot replace required machine records.

For an open-question record, preserve the original question's exact domain, normalization, quantifiers, parameter dependence, and concurrent resource targets. Label the target as requested, not established. Separate source-time openness from a current-literature conclusion. Keep source-known primitives separate from unspecified implementation operations. The absence of a computational model must remain explicit; it is not permission to grant free exact geometry or a bit-complexity guarantee. Apply the identity uncertainty test before treating that omission as a blocker for the abstract problem.

## 2. Reader-facing status

Use these primary statuses: All optimal / Logarithmic gap / Polynomial gap / Other quantified gap / Missing bounds. Do not use “statuses differ across regions” as the primary label. When missing bounds and a quantified gap coexist, retain two short indicators and explain the basis for each view/regime in the text.

Display Joint budget, Impossibility, Infeasibility, and Coverage separately from optimality. Keep unverified sources separate from mathematical GAPs: incomplete research does not automatically establish an open problem.

The joint research target must remain visible even when one resource projection is unresolved or has no approved bound. A query-only summary must not replace a query-and-computation question. A Missing bounds profile need not invent an algorithm, lower bound, quantified gap, scalarization, or complexity cell to fill a table. State each missing side and its reason, investigated sources, cutoff, and next evidence needed. If the reviewed scope is a source-contract family rather than one fully specified refinement, say so and do not silently assign a unique refinement-dependent minimax quantity. An incompletely specified suggested variant belongs in research directions or relations until its operative guarantee is sourced.

Commonly closed windows may share a bracket row; retain separate rows when algorithms, guarantees, or regions differ. Preserve each bound's actual upper-witness type and lower-algorithm scope. A generic “randomized” label must not conceal a deterministic upper bound.

## 3. Presenting evidence

Cite actual papers, versions, and theorem/equation locations. Attribute analyst arguments as `analyst_derivation` or `analyst_transfer` and include the text and premises needed for independent checking. Do not substitute run-history labels such as “D1: endpoint proof from the old audit” or “D2: appendix of the old snapshot” for complete evidence.

Keep necessary audit provenance in machine records. Readers need verifiable mathematical content and formal literature. “Proved in the previous round” is insufficient without the argument.

## 4. Independent review of the finished profile

For a new profile, review the complete specification, both tag representations, bounds and evidence, transfers, envelopes, status, all references, English expression, and formulas. For an update, review the fixed baseline, changes, affected dependencies, and support for unchanged results. Without genuine prior approval, perform a complete review. This version does not automatically inherit bound approval; the final review lists every proposed bound for adoption.

`approved_bound_ids` explicitly identifies the bounds that may become active. Quarantined claims cannot participate in a bracket. Document approval may retain unresolved missing sides; it cannot conceal unresolved identity or an unsupported optimality claim.

Check mathematical presentation: inline/display delimiters, backslash escaping, subscripts/superscripts, brackets, vertical bars in tables, and HTML/KaTeX/export usability. JSON parsing or successful compilation does not establish correct display. Do not claim visual acceptance if actual rendering was not performed.

## 5. Commit boundary

Only the writer commits transactions. Research Agents and reviewers do not modify the production Atlas directly. Commit checks cover identity approval, approval of the exact profile version, the old `base_version`, and IDs/aliases. Prepare the complete reviewable change first, then execute the configured publication policy. Task-taxonomy extensions take effect only through the user-approved catalog.

An Atlas commit receipt exists only after a successful update. Completed research/review is not a commit. Reports separately count leads, verified bibliography, fetched full texts, read papers, candidates, identity approvals, profile reviews, and actual new/update receipts.
