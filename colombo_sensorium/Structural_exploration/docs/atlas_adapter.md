# Atlas Adaptation, Tags, and Ingestion

## Boundary

`src/oracle_atlas/atlas/` handles files, deterministic projections, preliminary filtering, and transactions. It does not determine whether two mathematical specifications are equivalent, prove upper or lower bounds, or interpret a retrieval miss as a new setting. Independent matching and review agents make those judgments.

Input retains the existing Atlas structure `data/settings/<setting_id>/`, including `profile.json`, `identity.json`, `classification.json`, `human_tags.json`, and `machine_tags.json`. The supplied root may also be the `data/` directory containing `settings/`. Native schemas reside in `data/schemas/`. Where a schema exists, writes must satisfy it; the component must not force its own format over the existing database.

## Three Modules

| Module | Responsibility |
| --- | --- |
| `tags.py` | Effective oracle operations, unified fact projection, strict source-pointer and scope validation |
| `retrieval.py` | Multichannel ranking, controlled parent expansion, three-valued scope filtering |
| `store.py` | Five-file adaptation, scientific versions, frozen snapshots, review/adoption validation, commit and recovery |

## Shared Facts and Two Tag Representations

Agents produce `tag_facts` with sources and scopes. Each fact contains `concept_id`, an `axis` from the eight axes, `value`, `object_ref`, `view_ref`, `operation_ref`, `source_pointer`, and `status`. The statuses distinguish `known`, `unknown`, and `not_applicable`. A `source_pointer` addresses a field in the current profile, not character coordinates in the paper; paper evidence is referenced separately through specification or evidence fields.

The same facts generate machine `features` and human `facets/details`. All eight axes always appear in `axis_coverage`; unclassified axes remain in `unclassified_axes`. These mechanical projections do not fill in missing scientific semantics for the LLM.

`project_tags` registers a small set of structural fields with definite semantics, such as `primary_domain`, explicit `navigation_domains`, and native-oracle precision and operations. It does not extract convexity, smoothness, or success guarantees from free text. The extraction agent must register those facts, and independent review must check them.

Parent expansion follows only registered `parent_id`, `parent_ids`, or `retrieval_parent_ids` links in the vocabulary. Under MODEL, smoothness and geometry are groups; a shared string prefix does not establish mathematical containment. Both original Atlas `concepts` vocabularies, human and machine, are readable. Unknown concepts may remain `proposed`, but cannot silently become approved vocabulary definitions.

### Mechanical Source and Scope Checks

- JSON Pointers must resolve; negative array indices and invalid escapes are forbidden.
- Facts pointing into `/views/i/...` must bind to that view and cannot be registered as shared facts.
- A specified operation must occur in that view's effective native interface.
- The object binding must agree with that operation.
- The source must belong to the same operation or to a specification statement explicitly registering that `operation_ref`.

These rules are not semantic review. An LLM reviewer must still determine whether the source field actually supports the tag.

## Normalize the Native Interface Once

`effective_native_operations(profile, view)` combines the shared specification with the view override: objects merge recursively, lists replace whole lists, and explicit null remains unknown. It returns all native operations, including those not yet covered by the vocabulary. Public auxiliary operations must be explicitly registered as `public_auxiliary`; undeclared free capabilities are not added.

The aliases `id/operation_id/operation_ref` and `object_ref/object_id/target_object` are supported, with diagnostics for conflicts. Duplicate operation IDs, invalid types, and contradictory precision declarations neither cause string/hash crashes nor produce `matched` results.

A bare `Exact` check covers every native primitive within the same view. Unknown precision, an unknown role, or explicitly exact sample values of a sampled function cannot establish that the entire fixed-object interface is Exact. A local `right_matvec + Exact` check applies to the same operation and object; precision from another independent operation is not borrowed when its precision is unknown.

The only narrow historical compatibility entry is structured `oracle.code=exact_value`. Other legacy specifications with unexpanded operations remain unknown until extraction or adaptation is revised; prose is not used to guess an interface.

### Two Interface Filters

```python
match_interface(profile, {"returns": ["value"]}, mode="native")
match_interface(profile, {"returns": ["value"]}, mode="supplies")
```

A native `returns=["value", "gradient"]` does not match the first call. It matches the second, which reports the extra `gradient` and a conversion that discards a returned component with 0 additional calls. The current deterministic adapter automatically applies only this information-discarding operation. Finite differences, randomized conversions, guarantee conversions, and similar steps require formal applicability arguments and cannot be implemented at the tag layer.

## Preliminary Retrieval and Scope Queries

`retrieve(atlas, candidate, limit=12, offset=0, broaden=False)` ranks candidates using IDs/aliases, exact concepts, registered parents, title/task terms, legacy tags, and unknown records. Each page returns only short candidate information and ranking reasons. Pagination covers the entire catalog; low scores never automatically exclude a setting.

`broaden=True` prioritizes unknown or legacy-index records so that the matcher can investigate blind spots in the first retrieval pass. It does not establish exhaustive recall. When the budget is exhausted, the matcher should report unresolved credible neighbors and the next required material, rather than fabricate a certificate excluding the whole database.

`scope_search(atlas, filters)` returns counts and paginated entries for `matched`, `unknown`, and `conflict`. Unknown entries remain separate by default. Combined conditions must hold within the same view. Use `{"interface": {...}, "mode": "native"}` when restricting an oracle, to avoid combining conditions across operations. Matrix computation and Exact can be queried separately or together. After a tag match, the LLM must still read the complete specification to determine scope membership.

## prepare → Independent Review → commit

```python
base = atlas.version(setting_id)       # None if the setting does not exist
prepared = atlas.prepare(profile, tag_facts, expected_version=base)
# Freeze prepared.files['profile.json'] and review it in a new session.
# The controller validates reviewer origin, subject_ref, and fixed inputs,
# then adds prepared_hash.
receipt = atlas.commit(prepared, review, idempotency_key=case_revision_id)
```

`prepare` does not modify the Atlas. It preserves existing top-level profile extensions omitted from the input and unmanaged sidecar fields, so review must target the fixed profile produced by `prepare`. Existing view, bound, and alias IDs cannot disappear from arrays. Withdrawal or invalidation requires retaining the record with an explicit status instead of breaking historical references. Missing derived sidecars can be rebuilt. A missing `profile.json` must first be restored; scientific specifications cannot be reconstructed from tags.

When adding a view, one candidate's tags cannot replace the old views' tags. `prepare` inherits old facts only if every condition holds: the old machine file binds to the correct profile hash; the source Pointer value is unchanged; the old view contract is unchanged; and, for operation-bound facts, the effective interface, object, precision, and source scope are unchanged. Old shared facts are inherited by expansion over the original views and do not automatically extend to a new view. New facts take precedence for the same concept in the same scope, or for the same group at the same source, so explicit `unknown` or corrected values can replace old `known` facts. Changed sources or stale old hashes stop inheritance, and the agent must register the affected tags again. The snapshot's `tag_inheritance` reports inherited/skipped counts.

The frozen five-file bundle first normalizes object-key order and then hashes the native formatted bytes. Its pending-write snapshot therefore remains identical after storage and retrieval through the content-addressed ArtifactStore.

Before a review handoff enters the valid cache, the controller calls `atlas.validate_review(prepared, review)`. This read-only check shares its implementation with `commit`: an independent `verdict=approve` is required, and `approved_bound_ids` must cover every bound that is active, eligible, or actually referenced by comparison/bracket_rows. Bounds marked `quarantined`, `withdrawn`, `ineligible`, or explicitly `eligible_for_bracket=false` cannot appear in active references or the adoption list. Approval of a document that honestly isolates doubts does not adopt those doubts. A document may retain quarantined records that are neither adopted nor referenced. Publication blockers prevent writes. Automatic reuse of approvals for proof-dependency closures is not assumed; review must explicitly approve each bound that remains active in the current publication.

A new setting must undergo duplicate checking again after catalog changes. Updating an existing setting uses that target's five-file baseline; an independent update to another setting does not create a false conflict. Changes to schemas, controlled-vocabulary definitions, or alias registration create semantic conflicts.

## Versions and Recovery

The scientific inventory includes the five files, schemas, registry, vocabulary definitions, and top-level aliases. It excludes the explicitly derived files `browse_facets.json`, `browse_index.json`, and `catalog.json`. Regenerating browsing pages does not invalidate scientific conclusions.

For legacy Atlas compatibility, identity/classification use a hash of the profile's formatted UTF-8 bytes, whereas human/machine tags use a canonical JSON hash. The code handles these two existing bindings explicitly rather than treating them as the same hash.

All writes reuse the existing Atlas lock `data/intake/oracle_scout/write.lock`. The new component stores transactions in `data/intake/oracle_atlas_agents/`. If an unfinished pending transaction from the old component is found, execution stops so that the original component can recover first.

Commit proceeds as follows: persist all five new files → write the journal → write a pending marker → atomically replace each target file → write the receipt → clear pending. After restart, recovery rolls forward from the same journal without asking the model again. If a target matches neither the old nor the new hash, it is treated as an external modification; execution stops and retains the recovery material.

All component reads and writes obey the shared lock and therefore avoid partially completed snapshots. External programs reading the five files directly without the lock may see partial replacement during commit; they should read after the completed receipt or use this adapter.

An idempotency key applies only to the same snapshot, review, and baseline. A retry returns the existing receipt. Changed content requires a new revision/key. Test receipts establish software transaction behavior, not genuine mathematical research or successful ingestion of a real paper.

## Verified Scope

`tests/test_atlas.py` uses explicitly marked synthetic profiles and runtime-generated, explicitly synthetic legacy-format fixtures. It covers native interfaces, binding, eight-axis tags, Matrix+Exact combinations, retrieval pagination, native schemas, independent updates, version conflicts, idempotency, and interrupted recovery. These tests do not rewrite the user's production Atlas and cannot replace independent scientific review of real papers.
