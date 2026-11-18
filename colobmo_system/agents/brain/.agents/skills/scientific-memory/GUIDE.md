# Builtin Scientific Memory: Reading and Reuse in Research

Brain, Prover, and Subcell use the current Memory by default, with `scientific_memory(mode, arguments_json)` as the sole entry point. No additional startup script, external package, or environment variable is required; tool parameters cannot select a different library. Generic mode permits only theorem records; Verifier, Experiment, and recovery do not provide a live reader.

Reading supports discovery and reuse; it does not define a closed boundary for knowledge. If there are no hits, continue with external lookup, independent derivation, or new method design; an empty result does not prove that a problem is open. Neither search cards nor similarity certify applicability.

## Five Read-Only Operations

`arguments_json` is a string encoding a JSON object; mode is one of overview/browse/search/read/expand.

```python
scientific_memory("overview", '{"group":"mechanism","include_leads":true,"limit":12}')
scientific_memory("search", '{"query":"SPIDER conditioning history same-sample tracking error","kinds":["algorithm","theorem"],"include_leads":true,"intent":"explore","limit":10}')
```

- overview: Browse actual mechanism/goal/bottleneck/proof_method branches and continue with next_offset. Do not treat the first page as the entire library.
- browse: Set concept to an actual returned Research-use concept_id; do not invent tags or automatically traverse parent links.
- search: Combine query with facets/kinds, with intent set to explore/apply/challenge. A facet is a conflict only when it explicitly contradicts the setting; unknown means neither satisfied nor negated. exact=true excludes only registered explicit conflicts and does not check logical equivalence.
- read: Return the full ref unchanged; pointer is a JSON Pointer within this record, such as #/content/statement, #/content/complexity_scope, #/evidence, or #/source_refs. If a field is missing, read #/content rather than guessing the template.
- expand: Follow actual links as needed; performance/depends_on/model_membership/proves/uses still require review, while related serves only discovery. A Source's paper_contribution corresponds to a specific source version.

For search/browse/expand/overview, limit is 1..50 items and offset is an item position. For read, offset/limit are measured in characters, with a default limit of 10000 and a maximum of 20000; continue with next_offset when complete=false. A full ref is `{id,kind,revision,content_hash,tier}`; do not invent a hash or revision.

Candidates with readiness=lead require independent review before publication. overview includes leads by default; search defaults to published-only, so explicitly set include_leads=true during discovery. Do not conflate readiness, review_status, or publication with confidence. Leads may inspire work or be independently rederived, but cannot directly serve as accepted Theorems; published records also require checking against the current problem's conditions. FTS uses keywords, Chinese characters, and character bigrams, not vector search or an LLM reranker; when recall_exhaustive=false, change the query, mechanism, or branch to continue searching as needed.

## Use Around Research Obligations

Search as needed when beginning planning, encountering a blocked route, or meeting a new obstacle; overview is not mandatory every round. Upper may consult Hard Families, and Lower may search for Algorithms that exploit a construction. Estimators, potentials, or hiding mechanisms from other TASKs can provide transfer insights.

Read a few cards first, then fully read the statements, assumptions, scopes, evidence, sources, and Proofs that actually affect the route. Check Oracle/Metric/Guarantee/Resource, parameter mappings, dimension, and budget windows. Fresh-sample permissions cannot substitute for same-sample two-point queries; failure of a specific Algorithm cannot be upgraded into an unrestricted Lower Bound; additional primitives must be charged.

Save an application record only for material actually adopted or seriously attempted. Use existing materials/attachments and the research text to record the target obligation, fixed Setting, selected refs/content snapshots, intended use, known matches and conflicts, and remaining transfer obligations; do not blindly add fields to the existing Task schema. Distinguish direct/needs_transfer/inspiration_only/incompatible/insufficient_information; retain insufficient_information when complete material is missing. Give the Cell and Verifier a selected fixed package, not live references or the full retrieval history.

## Historical Material and Permissions

The old Recollect has been retired and no longer queries a separate library. Old `{id,version,content_hash,index_version}` refs remain as historical data; the new interface explicitly returns legacy_ref_retired. Do not guess ID mappings or silently replace contents. Do not rewrite the references or bytes of historical frozen packages.

During research, do not modify the assignment, current Memory, publication status, or Atlas bracket, and do not start Curator/Reviewer. The user separately invokes the independent Memory Agent outside the research loop. New mathematical inference, transfer, or composition still follows the existing verification workflow.
