# Setting Identity: High-Recall Retrieval, Semantic Verification, and One Independent Review

The formal comparison is between a frozen candidate and the current scientific version of the Atlas. `existing` means that the candidate should be integrated into an existing profile; it does not mean that every view or bracket already exists. `new` means only that the same setting is absent from the Atlas, not that it is a first discovery in the literature.

## 1. Comparison sequence

1. Check that extraction faithfully represents the source, and list the remaining core unknowns that affect identity. An unverified non-core bound must not block identity.
2. Query Atlas retrieval and record the retrieval ref and inventory version. Use clues from task/formulation, oracle/objects, metric/model, legacy IDs/aliases, and textual synonyms in parallel. Tags support initial filtering; retain unknowns.
3. Read the common specifications, views, and native operations of a small number of relevant neighbors in batches. Broaden retrieval or paginate while credible unexamined neighbors remain. Do not write exclusion reports for every low-relevance entry.
4. Compare the eight axes and quantifiers of the neighbors. Identify decisive differences first, then explain normalization. Verify actual mappings for symbol substitutions, dimension notation, and equivalent constant normalizations; “obviously equivalent” is insufficient.
5. If core definitions remain unclear, read the relevant paper version, appendix, original definition, or erratum within the same matcher task. Do not resample without new evidence. When the budget is exhausted, retain a specific unresolved decision.
6. Submit one identity proposal. An independent `identity_reviewer` must verify it before it reaches the research branch.

## 2. Equality, difference, and convertibility

When the common task/model/native-oracle/output/metric/resource contract is unchanged and only algorithm permissions or guarantees differ, the decision is normally `existing`, with mappings to existing or additional views. Use `atlas_view_id=null` and explain a new view if no corresponding view exists. A new algorithmic witness need not create a new view.

Changes in public information, admissible oracle queries or returns, dependence on random history, the cost model, output space, core error, or aggregation quantifiers can define a new setting. First rule out differences of representation or already-covered views/regimes. Do not merge settings solely because their rates agree.

An interface supplying the needed information, a reduction between problems, or containment of one instance class in another does not establish setting equality. Record the direction of the relation, differences, and prerequisites for conversion. A short transfer proof may support a related bound during research. Treating full-function access as gradient-only access, or noisy queries as exact queries, changes the meaning of the complexity claim.

### Classifying uncertainty before blocking identity

Name the missing field, the semantic claim that depends on it, and how the remaining uncertainty could change the primary task, instance class, native information/reply relation, feasible output, base error, operative guarantee, or resource convention used in the identity comparison. Do not invent alternative contracts merely to justify a blocker. A genuine uncertainty in that primary contract still blocks identity. An unresolved implementation, encoding, numerical precision, or secondary resource-accounting detail does not automatically block comparison of an otherwise source-defined abstract mathematical problem. Preserve it visibly and block every theorem, simulation, projection, or implementation claim that depends on it. Do not resolve it by granting free geometry or choosing a machine model.

A source-defined open target is not an algorithmic witness or an adopted upper bound. The absence of a method achieving it is not an identity ambiguity. Preserve the full target, including concurrent resource requirements and parameter dependence, separately from proved results. A Missing bounds profile still requires independent approval of its mathematical identity and the precise limits of its representation. If only a source-contract family is supported, label that scope explicitly; do not silently select a refinement, assign a unique refinement-dependent minimax quantity, or equate the family with a fully specified native model.

When the source defines f only on D, objective replies are defined on D; generic ambient-space wording does not grant an extension or outside-D reply. A primitive that supplies one valid subgradient grants neither the entire subdifferential nor the right to choose a favorable element. Preserve the source's valid-reply relation without inventing a fixed selector, history law, or coupling convention. Read the cited definition when finer distinctions matter. If an identity, operative guarantee, or primary quantity requires an unresolved refinement of that relation, retain the corresponding identity blocker; otherwise scope the uncertainty to the dependent claims rather than automatically rejecting the abstract question.

## 3. Required identity evidence

The `identity` artifact must satisfy its schema and explicitly provide at least: `candidate_ref`; `decision`; `setting_id` or null; `view_mapping`; `normalization`; neighbors actually compared and their evidence; `retrieval_ref`; `recall_audit`; and scoped issues.

For normalization, list the actual mappings, preserved quantifiers/costs, and conditions that are not preserved. Even when no normalization is needed, explicitly state that the native specifications are compared directly and give the symbol mapping. Do not leave required fields implicit in prose explanations.

`recall_audit` records the retrieval strategies actually used, unresolved credible neighbors, the coverage rationale, and `inventory_version`. A `new` rationale must cover reasonable retrieval scope and the decisive differences from the nearest settings; it is not a proof that the entire Atlas cannot contain an overlooked match. Set `decision=unresolved` when material is insufficient or credible neighbors remain beyond the budget. Such a decision must not create and commit a new profile downstream.

## 4. Review and continuation

The reviewer reads the frozen candidate, retrieval, key Atlas specifications, actual comparison reasons, and sources requiring verification. Check for missed neighbors, views incorrectly split into settings, capability containment mistaken for equivalence, invalid normalization, and core unknowns incorrectly downgraded.

An inadmissible theorem within the same setting blocks only the corresponding bound. First determine whether an initialization parameter belongs to common information or to a particular witness. Do not indiscriminately promote proof or cost uncertainties into identity blockers.

Approval must bind the candidate and current Atlas version. When the scientific version changes, check the affected material; rebuilding a browsing index is not a specification change. New material or candidate revisions retain the old decision, create a new version, and trigger review of affected downstream work. Sibling candidates from the same paper must not be reset as a side effect.
