# Two Tag Systems: Shared Facts, Different Purposes

Tags support navigation and retrieval. An LLM must still read the specification to judge setting identity and theorem applicability. Machine and human tags must project the same scoped `tag_facts`; they must not independently generate contradictory semantics.

## 1. A single fact layer

Each fact follows the current TagFact schema: `concept_id,axis,value,object_ref,view_ref,operation_ref,source_pointer,status`. The axes are TASK/MODEL/ORACLE/ALGORITHMS/OUTPUT/METRIC/GUARANTEE/RESOURCE. `source_pointer` identifies an existing specification field in the candidate or profile. `status` distinguishes known/unknown/not_applicable. Absence of registration does not imply false.

First use `vocabulary_lookup` to look up exact IDs in batches, or navigate paginated results by query/axis. Read the actual definitions, registered_parents, missing_ids, and vocabulary version. Use exact concept IDs from the current controlled vocabulary. Expand parent-child, synonym, and cross-concept relations only as explicitly registered; do not infer hierarchy from string prefixes. For a new concept, preserve the original statement and scope and propose a definition, parents, and aliases. An existing approximate term must not masquerade as an exact classification. A new task not approved for the task catalog may still be retained as a proposal.

Place smoothness, geometry, convexity, and similar properties under MODEL subclasses. Separate task topics from specific formulations. If a matrix computation is a specific query task, TASK must register the corresponding formulation and the defined Matrix computation parent; an unclassified keyword alone is insufficient.

## 2. Human-facing tags

Navigation uses a small number of common parents under the eight axes, expanding to show subclasses and exact constraints. First-order interface may serve as a familiar navigation entry, while retaining exact subclasses such as value-plus-gradient and gradient-only; readers need not choose among three alternatives at the top level. A parent selection may include registered children and display additional capabilities and unknowns.

Multiple selections within one axis default to OR; selections across axes default to AND. The interface must display this logic clearly and allow stricter conditions. Concept search supports aliases and displays the match path, for example MODEL → Smoothness → Lipschitz gradient. When no results match, identify conflicts or missing registrations and suggest relaxed conditions. Do not silently filter out unknowns.

A broad human-facing match does not change the native interface. `Match the native interface` requires matching query/return/precision/cost contracts. `Find interfaces supplying at least this information` may list stronger or convertible interfaces, but must identify additional capabilities, applicability conditions, and conversion costs. The latter does not establish identity.

## 3. Machine-facing tags

Machine retrieval combines multiple OR-based recall routes, including related tasks, objects/levels, oracle operations, models, and metrics, and ranks the results. Do not join several keywords into an overly restrictive AND. Joint conditions support a scoped match only when they concern the same view/operation/object. Exact feedback at a lower level and value feedback at an upper level cannot be combined into an upper-level exact-value match.

Precision checks include every native primitive feedback operation, including operations not yet covered by the vocabulary. An unqualified Exact query is matched only when all native feedback in its current scope is confirmed exact; one unknown makes it unknown. A local `right_matvec + Exact` query only requires conditions for that same operation; unknown precision of an unrelated operation does not invalidate this local match. Register public auxiliary operations explicitly; unfamiliarity does not justify excluding them.

An exact sample value is an exact value of the sampled object, not necessarily an exact value of the population objective. Explicit null/unknown cannot inherit global Exact. Read the original field to determine whether a view override replaces or extends operations; do not silently choose one of conflicting aliases.

## 4. Conclusions tags cannot establish

A match score, identical tags, a low score, or an empty top-k result cannot establish either identity or novelty. Retain unknown candidates; expand synonyms, parents, neighboring tasks, and further pages. Read complete specifications for credible neighbors before deciding. For a large corpus, work in batches and select decisive differences; return unresolved if the budget is insufficient. Do not require the model to generate an exclusion certificate for every database entry to "guarantee no omissions."

Graph edges may represent the same concept, parent-child classes, or neighboring properties. These are retrieval relations. Equivalence, strict generalization, oracle simulation, and complexity transfer require independent evidence and direction; they cannot be inferred as mathematical relations from the tag graph.

## 5. Acceptance checks for every profile

Manually check that readers can find the profile using expected single-tag and combined searches. Machine checks verify that all eight axes contain explicit facts or unknown/not_applicable, fact pointers are valid, and parent expansion preserves scope. Pay particular attention to task parents, precision such as Exact/Noisy, and multilevel oracles. Repair projection/registration when tags are missing; do not change the mathematical specification to satisfy the interface.

## Binding a candidate to the final profile

A candidate pointer such as `/views/0/...` is local to that candidate and does not necessarily identify the first Atlas view. The host may mechanically rewrite these pointers only from a reviewed `view_mapping` and stable view IDs. If operation/object IDs or source field paths have also been explicitly normalized, provide final-profile fact bindings in `research.tag_facts` for independent profile review. Without that field, the host uses candidate facts plus the reviewed view mapping; it does not guess operation equivalence. An update inherits old facts only when their source values and original view/operation contracts are unchanged, with new facts taking precedence. It neither overwrites algorithm tags of an old view nor automatically extends old common facts to a new view.

