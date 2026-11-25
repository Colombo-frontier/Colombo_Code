# Current Long-Term Memory

The current Memory is `colobmo_system/long_term_memory/`, paired with
`.long_term_memory_state/`. It contains 388 published records and 43 leads.

This public snapshot is a privacy projection. Workstation evidence locators are
replaced with nonlocal identifiers, affected pinned hashes and indexes are
rebuilt, and the original review identity is kept separate from the projected
JSON hash. See [public snapshot and review identity](MEMORY_PRIVACY_PUBLICATION.md)
and `../.long_term_memory_state/PRIVACY_PROJECTION.json`.

The same disclosure records the release's neutral public wording projection.
It retains mathematical arguments and application restrictions while expressing
source commentary as explicit formula conventions and evidence scope. Affected
bytes and pinned references have new disclosed hashes; historical reviews still
bind their original identities, with no new review or change of publication tier.

## Ordinary system use

Install system `requirements.txt` in Python 3.11+ and use the original entry points:

```sh
python run.py config
python run.py run path/to/goal.md --run-dir runs/example --prepare-only
python run_cell.py --help
```

Brain and research Cells automatically expose read-only `scientific_memory`.
There is no optional companion installation, MEM environment variable or extra
launcher. The default root is determined by this system source location, not by cwd,
task input, inherited environment or a model-selected path. Generic Cells remain
theorem-only. Verifier, Recovery and Experiment do not get a live memory reader.

The five operations are `overview`, `browse`, `search`, `read`, and `expand`.
The MCP signature is `scientific_memory(mode, arguments_json="{}")`.
Published-only search defaults to excluding leads; explicitly include the
current candidates when discovering useful material:

```sh
python tools/memory/query_memory.py query \
  '{"mode":"search","query":"SPIDER tracking error","include_leads":true,"limit":10}'
python tools/memory/query_memory.py query \
  '{"mode":"overview","include_leads":true,"limit":12}'
```

Always reuse the returned full ref. `read` supports JSON Pointer selection and
character pagination; continue with `next_offset` until complete. `expand`
follows recorded scientific links, not inferred applicability. Scientific facets may use
scope-hash concept IDs; use actual returned identifiers rather than inventing
an ontology. Candidate cards, matching conditions and published reviews do not
prove applicability to a new Setting.

For selected material, use `tools/memory/freeze_application.py` to freeze actual
JSON/hash into a research package. A lead cannot be used as an accepted `direct`
memory citation. Preserve transfer obligations and check Oracle, Metric,
Guarantee, Resource, parameter domains and complete quantifiers.

## Storage: four scientific libraries only

```text
colobmo_system/
  long_term_memory/
    algorithm_family_library/  # one current Algorithm/variant record per ID
    hard_family_library/       # constructions, information limitations, components
    theorem_library/           # Theorem and Proof Method records
    source/                    # source identity, version, locators, reading coverage
  .long_term_memory_state/      # engineering state, not another scientific library
```

Every current scientific object is directly readable as `<library>/<id>.json`.
Review status does not choose a storage directory. The 43 retained candidates
have `readiness=lead`; placing them in their scientific libraries does not
publish or certify them. Algorithm family membership remains in the original `content.family`
and `variants`; this layout change does not merge mathematically distinct methods.

The sibling `.long_term_memory_state` contains the current indexes and pointers,
pinned scientific objects, privacy-projection mapping and original review
hash commitments. The bundled objects use digest-only names in `objects/`;
the active indexes use fixed `current` and `leads` directory names. Local task
receipts, audit history and execution timestamps are excluded. Private job directories, prompts, local source caches,
archives and unaccepted staging proposals are excluded from this public package.
The Reader requires read-only access to both directories. Keep generated reading
views and research execution output outside the scientific libraries.

For future updates use the existing independent Curator/Reviewer workflow.
`prepare` writes outside the knowledge directory; accepted publication updates
one current JSON and preserves pinned historical JSON in the state directory.
Candidate imports cannot overwrite published records or change an existing ID's
scientific kind. A pending update to a published object stays in the external
review workspace until accepted; it does not replace the visible accepted object.

The reader CLI and `scientific_memory` MCP remain read-only. Search/read interfaces,
record IDs, generic-mode permissions and proof-scheduler behavior are unchanged.
Projection hashes differ where documented; original review hashes remain in
the provenance mapping. A privacy projection is not a new scientific review.

## Paired Store and independent updates

Memory and its required state form one paired Store. The nested [Memory Agent](../colombo_memory_agent/README.md) defaults to its parent system's Store. Each new candidate still requires independent review and native publication; the writer is separate from the proof scheduler.
