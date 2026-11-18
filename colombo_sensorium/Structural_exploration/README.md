# Structural_exploration

The component provides bounded neighborhood discovery, native status contracts and joint-parameter analysis for profile authoring, independent review and transactional Atlas publication.

A standalone neighborhood-discovery command sharing the Oracle Atlas research pipeline. The Python distribution is **structural-exploration**. Its primary command is `structural-exploration`; the shared `oracle_atlas` Python namespace and legacy commands remain compatible. Use a fresh dedicated environment: do not co-install this distribution with `oracle-atlas-agents` or Maintenance packages that require it, because they provide the same Python files.

**[Design Specification](docs/expansion_design.md)** · **[Usage](docs/expansion_usage.md)** · **[Migration guide](docs/migration.md)**

## What changes

The frontend reads a finite Atlas seed portfolio and produces short, motivated opportunity cards. Only selected opportunities receive full eight-axis specifications. Independent review checks the proposed contract, value and pending peers; the existing Matcher and Identity Reviewer then compare it with the entire Atlas. Confirmed new settings reuse the existing profile research and review chain. Existing profiles may be reported or updated according to the request.

Three new project roles are registered: `expansion_planner`, `setting_expander`, and `expansion_reviewer`. Each has an `AGENTS.md`, `protocol.md`, and on-demand skill. Shared tools, MCP, private memory, immutable records, incremental drafts, coverage checks, proof credentials and Atlas transactions are retained.

New definitions have `origin.kind=atlas_expansion`. They may have `paper_refs=[]`. No artificial triggering papers or extraction reviews are created.

## Install and try the offline example

Python 3.11 or later is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[all,test]"
python examples/offline_expansion_demo.py --output ./demo_expansion
```

This repository tracks source only. To create an optional local wheel, install a build frontend and run `python -m build`; then install the generated wheel from `dist/` with the desired extras. The offline example does not call a model or the network. Its toy settings and scripted decisions test software integration only. The scripted demos explicitly use at most 16 context segments and 90 turns per job, with the 60000-character input cap retained; production defaults are unchanged.

New profile writes require canonical comparison statuses, an exact aggregate summary, a resolved version-2 `joint_analysis`, native source/proof bindings, explicit research scope, and six independent joint-review assessments bound to the prepared bundle, analysis and frozen science context. Existing profiles remain readable; incomplete historical analysis must be explicitly researched and reviewed before a new write. The validator does not invent parameter roles, infer mathematical statuses, or silently repair publication input.

## Use your Atlas

```bash
structural-exploration init \
  --config expansion.local.toml \
  --atlas "/absolute/path/to/atlas-copy" \
  --workspace "./expansion_work" \
  --backend codex

structural-exploration doctor --config expansion.local.toml

structural-exploration run \
  --config expansion.local.toml \
  --request config/expansion_request.example.json
```

Edit the example request's task IDs, permitted transformations, fixed constraints and run label. An omitted cutoff date defaults to the day the request is normalized; set `cutoff_date` explicitly when a fixed literature boundary is required. A Responses backend is also available. Model authentication and availability are not configured by `init`; see [providers](docs/providers.md).

The default caps are 8 seeds, 6 neighbor summaries per seed, 24 opportunity cards, 16 full candidates, and 10 profile-research starts. A coherent primary transformation may touch multiple axes. Pending candidates are not recursively promoted to seeds. The profile cap is not a promise that ten valuable or finished profiles will be found.

## Inspect and publish

Expansion produces reviewed proposals awaiting human approval. It never treats `run` as publication authorization.

```bash
structural-exploration export --config expansion.local.toml --batch-id BATCH_ID --out ./review_batch
structural-exploration publish --config expansion.local.toml --batch-id BATCH_ID --all-ready
```

Publishing one profile changes the Atlas inventory. Later profiles receive current identity checks and a new independent final review. Exact scientific objects can be reused when unchanged. Human approval binds the selected five-file content; changed content waits for new approval. Only a receipt demonstrates ingestion.

## Compatibility

The legacy `oracle-atlas-expand` command invokes the same expansion workflow; `oracle-atlas` retains the paper workflow. Mathematical setting/view IDs, module imports and existing configuration shapes are preserved. The branded command changes product presentation, not scientific approval or publication policy.

## Source layout

| Location | Responsibility |
|---|---|
| `src/oracle_atlas/expansion/` | Request, neighborhood, portfolio selection, frontend validation, workflow and CLI |
| `agents/expansion_planner/` | Compact opportunity planning |
| `agents/setting_expander/` | Complete proposed contracts and provenance |
| `agents/expansion_reviewer/` | Independent specification/value/scope and pending-peer review |
| `standards/expansion.md` | Scientific expansion principles and current eight-axis/view granularity |
| `src/oracle_atlas/workflow/` | Shared identity, bracket research, proof reuse and adoption workflow |
| `src/oracle_atlas/science/` | Shared status and joint-analysis structure, reference and publication contracts |
| `src/oracle_atlas/runtime/`, `tools/`, `providers/` | Bounded tool sessions, memory, MCP and model adapters |
| `examples/`, `tests/` | Synthetic fixtures and reproducible offline exercises |

## Verification and limitations

See [testing and release boundaries](docs/testing.md). Run `python -m pytest`, `python scripts/check_resources.py`, and both offline examples after interface changes. `scripts/build_schemas.py` regenerates the base schemas; run `scripts/build_expansion_schemas.py` afterward for the extension contracts. The release includes the current generated schemas.

The test suite uses synthetic decisions for autonomous workflows, plus actual local MCP transport and installation checks. It does **not** establish real-model scientific performance, literature completeness, or the value of a discovered research problem. No production Atlas is modified by building or testing this package.

Discovery is a bounded sequential portfolio workflow. Same-batch pending peers are checked, including pairs appearing after interrupted reviews. Historical pending batches remain leads rather than an exhaustive cross-batch semantic registry. Formal identity checks still query the entire current Atlas before new-setting ingestion. Missing Atlas evidence does not prove a literature gap.

Runtime resources, scientific profiles, and design and delivery explanations are in professional English. Project skills are ordinary packaged runtime resources; they do not need installation into a personal skills directory.

This public source tree contains no production Atlas records, source papers, private acceptance workspaces, credentials or historical run archives. Legacy compatibility tests generate clearly marked synthetic records in temporary directories; the shipped fixture directory contains schemas only.
