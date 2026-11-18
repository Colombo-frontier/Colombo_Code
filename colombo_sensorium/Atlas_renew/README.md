# Atlas_renew

Maintain the complexity brackets of existing Atlas settings through bounded research, explicit joint-domain reasoning and independent review. The controller freezes the native baseline, records evidence and budgets, prepares the complete proposal, and adopts it only through the native transaction writer.

The component supports finite literature checks, exact known-source lookup, bounded download recovery, concurrent settings, observable deadlines and explicit continuation. It does not establish a new autonomous profile-generation workflow. Analysis drafts, metadata matches and valid JSON are not scientific approval.

## Install

Use a Python environment that provides `tomllib`. From this directory, create and activate a dedicated virtual environment, then install the bundled native backend and this component:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install ./native_backend
python -m pip install '.[codex,pdf,test]'
atlas-renew --help
```

The bundled `Atlas_native_backend` is a compatibility dependency dedicated to this maintenance component. Keep this environment separate from sibling components: they can expose the same `oracle_atlas` import namespace with different native contracts. Do not install them together or assume their prepared profiles and approvals are interchangeable. The maintenance evidence gates and native transaction boundary remain required; this dependency does not upgrade a new-setting generation workflow.

`python -m oracle_atlas_maintenance` exposes the same CLI. Authentication and model selection belong to the configured backend; no account, credential or model choice is bundled here. Keep credentials in the backend's supported local configuration or environment, outside the repository.

## Start with a copy

1. Make a complete writable copy of an existing Atlas, including its schemas, registry and vocabulary.
2. Copy a configuration example to a local file. Set `atlas` to that copy and `workspace` to a separate private work directory. Paths resolve relative to the configuration file.
3. Select existing setting IDs in a JSON array. Use the CLI to audit, plan, run, inspect results and apply independently approved bundles.

```bash
cp config/example.toml local.toml
# Edit local.toml and create selected-ids.json with your existing setting IDs.
atlas-renew --config local.toml audit --ids selected-ids.json --output audit.json
atlas-renew --config local.toml plan --ids selected-ids.json
# Use the returned run ID.
atlas-renew --config local.toml run "$RUN_ID"
atlas-renew --config local.toml status "$RUN_ID"
atlas-renew --config local.toml apply "$RUN_ID"
```

Planning makes no research-model call. Running can incur backend usage; the default run stages approved proposals for a later explicit apply. `run --commit` permits adoption during execution only after all review and transaction gates pass. If you need a particular research cutoff, supply `--cutoff "$CUTOFF"`; otherwise the CLI chooses the current date according to the configuration.

## Evidence boundaries

- Scientific source claims require actual decisive primary-text reads. Fetches, cache hits, metadata and another role's reads are insufficient.
- Baseline references bind exact frozen objects and their canonical hashes. Prepared proposals bind the complete native five-file bundle.
- A fresh independent reviewer must perform its own required reads and all six synthesis checks. No checkpoint or imported draft carries an approval.
- Native comparison codes and derived summaries follow the supplied closed taxonomy. Zero cost and saturation are guarded properties, not invented status codes.
- Supported local work can remain partial. Unfinished necessary evidence cannot become a successful no-change check or completed-maintenance watermark.

Read [Usage](docs/USAGE.md), [Finite research](docs/FINITE_RESEARCH.md), and [Operations](docs/OPERATIONS.md) before enabling larger queues or resuming unfinished work. Keep generated workspaces, source caches, raw backend events and reports out of Git.
