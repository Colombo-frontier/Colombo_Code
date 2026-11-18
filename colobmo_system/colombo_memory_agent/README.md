# Independent Memory Agent

This folder contains the Curator, independent Reviewer, WriterStore, index
builder and trusted publication CLI. It updates the single current Store at
`../long_term_memory/`; it does not maintain another library.
It is not imported or launched by the proof scheduler.

Use the parent system's Python 3.11+ environment. The tools load its core from
source, so no companion package or editable installation is required. Run the
commands below from this `colombo_memory_agent/` directory.

## Small explicit jobs

```sh
python tools/doctor.py --check-codex
python tools/create_job.py --out jobspecs/local-note-001.json \
  --job-id local-note-001 --source examples/local_math_note.md \
  --focus 'full-space gap-to-gradient lemma and constrained-optimum limitation' \
  --objective 'Extract one Source and one Theorem with complete assumptions and local argument.' \
  --publication-policy stage_only --max-rounds 2
python tools/run_memory_job.py --job jobspecs/local-note-001.json
```

Default memory root: the parent system's `long_term_memory/`. Default execution directory:
this Agent's `jobs/<job_id>/`. Each role starts a fresh read-only Codex process;
the runner records actual source snapshots, hashes, prompts, outputs and review.
It preserves existing authentication and only whitelisted model/system-proxy
preferences, while excluding unrelated user MCP configuration.

`stage_only` performs extraction and independent review without publication.
Actual scientific papers require their selected-version original sources;
Candidate records are seeds, not original evidence. A new Source must bind registered
source bytes. New source versions, roots or focus use new job identities.
Only explicit `publish_reviewed` jobs or an authorized operator may publish.

## Operator commands

The single management entry point is `run.py`:

```sh
python run.py --help
python run.py publish ACTUAL_PROPOSAL_ID jobs/JOB_ID/validated-review.json --authorized
```

Use actual IDs and review paths from a completed job. Review decisions, hashes,
dependencies and base revisions must match. No publisher command is exposed to
Brain, Cell, Curator or Reviewer MCP tools. Partial acceptance, withholding and
bounded revisions preserve unresolved items rather than inventing acceptance.

The current scientific records are directly stored in four libraries in the parent system:
`algorithm_family_library`, `hard_family_library`, `theorem_library`, and `source`,
all under `long_term_memory`. `tools/validate_dataset.py` validates these records;
`--paper` jobs select their current contents as repair seeds. Seeds remain distinct
from actual source files. Jobs without `--paper` do not load the corpus.

Engineering state, indexes, proposals and immutable older revisions live in the parent system's
`.long_term_memory_state`, outside the four libraries. `tools/import_staging.py`
can build a new isolated four-library store but never copies an `ingest/dataset`
tree into it. Do not re-import the existing nonempty store.

For an unreviewed, zero-publication legacy layout only, inspect then explicitly apply:

```sh
python -B tools/repair_layout.py
# Stop research and curation processes before this operation.
python -B tools/repair_layout.py --apply
```

It creates a byte-verified backup of the complete old memory directory and keeps
all current record bytes and scientific statuses unchanged. The migration is
restricted to the unreviewed, zero-publication legacy layout; a store that has
since published records is refused rather than being silently flattened.

Read-only discovery, freeze and navigation tools belong to the parent system:
`../tools/memory/`. Scientific contracts and the read-only
Store are implemented once in `../src/colombo/memory/`.

The public package excludes prior local deployments, raw role prompts, model
outputs and retired handoff instructions. Current publication provenance and
pinned scientific revisions remain in the parent system's paired `.long_term_memory_state`.
Existing private jobs retain their original identities; do not rewrite their
source, job or review bytes to resume them at a different location.

## Job exit status and recovery

`run-job` returns exit status 0 for `completed` or
`completed_with_deferred_items`; the latter still requires inspection of the
per-item decisions and any publication receipt. `stage_only` can complete
successfully without publishing. `budget_exhausted` returns exit status 2 and
keeps its JSON diagnostics on stdout. Configuration and transport errors return
exit status 2 with JSON diagnostics on stderr.

After a model timeout, failed process or interrupted call, fix the transport
problem and use `--resume` with the same job, sources, Store and jobs directory.
Recovery continues the unfinished phase: an existing prepared proposal needs
only a fresh independent Reviewer; a validated review is reused after checking
its binding and hashes. Completing that phase does not allocate another
candidate revision round, even on the last allowed round. Content or protocol
errors still consume the bounded repair budget. A committed publication is
recovered through its existing receipt rather than publishing twice. Changed
source bytes or conflicting scientific revisions require explicit reconciliation.
