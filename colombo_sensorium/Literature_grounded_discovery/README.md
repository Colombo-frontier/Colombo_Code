# Literature_grounded_discovery

Literature_grounded_discovery discovers papers, extracts mathematical settings, matches them to an oracle-complexity Atlas, researches upper and lower bounds, and submits independently reviewed updates through transactional ingestion. LLM agents make scientific judgments; Python manages records, tools, budgets, recovery, and writes.

The component retains the `oracle-atlas` command and `oracle_atlas` Python import for integration compatibility. Its role definitions follow the `AGENTS.md → protocol.md → skills` structure. Project skills are loaded resources and do not need installation in a personal skills directory.

Authorized scans write to the configured Atlas after independent review passes. Set `publication.require_human_approval=true` to inspect each case before ingestion. Expanding the task catalog requires a separate task proposal and explicit approval.

## Install and configure

From this component directory, create a Python environment and install the desired optional dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[all,test]'
```

For Responses, the relevant extras are `openai,pdf`; for Codex, use `mcp,pdf`. Tests and the offline demonstration require no API key. PDF extraction can lose mathematical layout, so decisive formulas still require checking against the original source.

Start with a copy of the Atlas:

```bash
oracle-atlas init --config config.local.toml --atlas ./atlas-copy \
  --workspace ./work --backend responses --model YOUR_AVAILABLE_MODEL_ID
oracle-atlas doctor --config config.local.toml
```

Set the environment variable named by `api_key_env`, normally `OPENAI_API_KEY`. Select a model actually available to the account. `doctor` inspects configuration and component resources; it does not call a model or establish scientific acceptance.

To use an independently configured Codex CLI:

```bash
oracle-atlas init --config config.codex.toml --atlas ./atlas-copy \
  --workspace ./work-codex --backend codex
```

For that backend, an empty `[model] model` inherits Codex configuration. See [backend and source adapters](docs/providers.md) for transport, MCP configuration, recovery, and measurement limits.

The task catalog in [config/example.toml](config/example.toml) is an editable starting point. Review task IDs, formulations, search terms, approval flags, budgets, and publication policy before scanning. Relative Atlas and workspace paths resolve against the configuration directory.

## Scan or process a paper

Replace `YEAR` with the publication year to search:

```bash
oracle-atlas scan --config config.local.toml \
  --task single_objective --task matrix_computation \
  --year YEAR --event-kind publication --query-budget 12 --paper-limit 10
```

Task, year, and source options may be repeated. The built-in discovery sources are arXiv, Crossref, and OpenAlex. Search results are leads until publication events and provenance are verified. Selecting `preprint`, `revision`, or `any` changes event attribution; a submission event does not establish journal publication.

To process a supplied paper, replace the example URL with the original source:

```bash
oracle-atlas run-paper --config config.local.toml --url https://example.org/paper
oracle-atlas status --config config.local.toml
```

`run-paper` also accepts `--paper-json ./paper.json` conforming to the [paper schema](schemas/paper.schema.json), or `--paper-ref` for an existing workspace record. These inputs are mutually exclusive. Optional research notes can be supplied through `--research-material-file ./materials/notes.txt` or a workspace `--research-material-ref`. Notes inform research and review; they do not establish approval.

The workflow branches to update an existing setting or research a new setting after independent identity review. An asserted `no_change` also requires independent scientific review. Atlas ingestion is established by a successful commit receipt, not by completed research, test results, or a review alone.

## Task proposals and recovery

```bash
oracle-atlas scout-tasks --config config.local.toml \
  --notes "Check whether the approved catalog omits important oracle tasks"
oracle-atlas approve-task --config config.local.toml \
  --proposal-ref ACTUAL_PROPOSAL_REF --task-id proposed_task_id
```

Use actual returned references. The task scout proposes formulations and search terms but cannot approve its own catalog expansion.

Inspect `status` before recovery. Each command below also requires `--config config.local.toml`:

| Situation | Command | Effect |
| --- | --- | --- |
| An unfinished case | `oracle-atlas resume --case-id CASE_ID` | Continues existing valid work |
| Uncertain transport outcome | `oracle-atlas resume --job-id JOB_ID --retry-transport` | Reconciles saved results before permitting another call |
| Invalid output structure | `oracle-atlas resume --job-id JOB_ID --repair-protocol` | Repairs format and bindings using schema diagnostics |
| Clarified identity | `oracle-atlas resume --case-id CASE_ID --stage identity --material-file ./materials/source.pdf` | Revises affected identity and downstream work |
| Additional bounds or proofs | `oracle-atlas resume --case-id CASE_ID --stage research --material-ref ACTUAL_SOURCE_REF` | Revises research within the confirmed identity |

Use `--stage extraction` for corrected extraction. Import a source separately with `oracle-atlas import-source --config config.local.toml --file ./materials/source.pdf`. Ordinary resume cannot resample a scientific uncertainty into approval. Recovery retains accumulated budget use.

If human approval is enabled, export and inspect a case in `ready_for_approval`, then use `oracle-atlas resume --config config.local.toml --case-id CASE_ID --approve`.

## Research and review boundaries

The ten roles are coordinator, task_scout, paper_scanner, extractor, extraction_reviewer, matcher, identity_reviewer, bound_updater, profile_researcher, and profile_reviewer. Independent reviewers receive frozen formal artifacts and necessary sources rather than a producer's private working memory.

Scientific work follows decisive sources → atomic results → short proofs and transfers → bracket synthesis → targeted gap checks. Matching compares the complete mathematical specification. Labels support preliminary retrieval, and an empty retrieval page cannot establish that a setting is new.

Research and review distinguish core identity uncertainty, individual unproved bounds, contextual applicability, and source defects. A document can preserve quarantined claims while the final reviewer explicitly approves only admissible active bounds. Proof reuse, independent scope revalidation, and full proof review have separate requirements; see [review scope](docs/review_scope.md).

The writer freezes and independently checks the native five-file bundle: `profile.json`, `identity.json`, `classification.json`, `human_tags.json`, and `machine_tags.json`. Baseline checks and a shared write lock protect concurrent work. A transaction journal and receipt support recovery.

## Bounded inputs and code layout

Initial prompts contain goals, references, short catalogs, and relevant issues. Full papers and Atlas artifacts remain in content-addressed storage. Source tools read passages; `artifact_get` uses JSON Pointers and pagination; draft tools write large profiles incrementally. Unread leads remain queued rather than being silently treated as reviewed literature.

Default budgets bound input characters, tool results, turns, context segments, model calls, external calls, candidates, and jobs. These are engineering limits, not exact token counts or scientific completeness guarantees. Codex runs an internal tool loop whose peak context this component cannot fully observe.

| Directory | Purpose |
| --- | --- |
| `agents/`, `skills/`, `standards/` | Responsibilities, protocols, and scientific methods |
| `schemas/` | Record and handoff contracts |
| `src/oracle_atlas/runtime/` | Instructions, bounded sessions, and recovery |
| `src/oracle_atlas/workflow/` | Stage dependencies, review, and adoption |
| `src/oracle_atlas/tools/` | Registered tools, role permissions, and MCP service |
| `src/oracle_atlas/providers/`, `src/oracle_atlas/discovery/` | Execution backends and literature sources |
| `src/oracle_atlas/atlas/`, `src/oracle_atlas/core/` | Atlas adaptation, transactions, artifacts, drafts, and memory |
| `tests/`, `scripts/`, `examples/` | Engineering checks and synthetic demonstration |

See [architecture](docs/architecture.md), [Atlas adaptation](docs/atlas_adapter.md), and [workspace migration](docs/migration.md) for details.

## Export and engineering checks

```bash
oracle-atlas export --config config.local.toml --case-id CASE_ID --out ./exports/case-review
python -m pytest
python scripts/check_resources.py
python examples/offline_demo.py --output ./demo-output
```

An export includes fixed case material, profile files, reader text, and an available receipt. Uncommitted cases can also be exported, so inspect the actual case state and receipt. Optional `reader_markdown` is frozen and reviewed with the structured profile; it cannot replace scientific records.

The offline demonstration uses synthetic sources and predetermined model conclusions while exercising orchestration, tools, schemas, drafts, review jobs, and transactions. It establishes software behavior within that scope. Real-model connectivity, source interpretation, independent mathematical review, and actual Atlas ingestion require separate validation in the deployment environment.
