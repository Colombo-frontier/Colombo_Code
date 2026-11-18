# Usage

## Isolate the native dependency

Follow the README installation in a dedicated virtual environment: install `./native_backend`, then `.[codex,pdf,test]`. The bundled backend is specific to this component's maintenance contract. Sibling components may share its Python import namespace while enforcing different native contracts, so do not mix their installations or transfer prepared bundles and approvals between them. This setup preserves the maintenance evidence gates; it is not a general native-contract migration or a new-setting generation upgrade.

## Configure the existing Atlas

Use `config/example.toml` for an initial bounded run. The large-profile example provides preview and own-read settings for substantial profiles; the parallel example allows more independent settings in flight. Configure the existing backend and command without changing the user's intended model implicitly.

`atlas` must point to a complete Atlas copy. `workspace` stores the queue, cache, journals, immutable proposals and cumulative accounting, and must remain separate from native setting directories. Copy all native support files with the data; a collection of profile JSON files alone is not a complete acceptance workspace. Do not commit local configuration, credentials or runtime evidence to this repository.

Create `selected-ids.json` as a JSON array of actual registered IDs. IDs in documentation are placeholders, never a supplied research answer.

## Inspect and plan

```bash
atlas-renew --config local.toml audit --ids selected-ids.json --output audit.json
atlas-renew --config local.toml plan --ids selected-ids.json
```

The audit checks existing target and joint-analysis structure without a model call or native write. A plan freezes the ordered selection, current baseline fingerprints, cutoff, semantics and policy. Add `--cutoff "$CUTOFF"` for a chosen cutoff. `--force` permits rechecking recently completed settings; it does not relax evidence or reset an existing cumulative budget cycle.

## Run, inspect and apply

```bash
atlas-renew --config local.toml run "$RUN_ID" --jobs "$JOBS" --limit "$LIMIT"
atlas-renew --config local.toml status "$RUN_ID"
atlas-renew --config local.toml apply "$RUN_ID"
```

Choose positive `JOBS` and `LIMIT` within the configuration. Settings can run concurrently, while each setting's research and independent review remain ordered. Running without `--commit` stages eligible approved bundles. Apply uses the frozen prepared bundle and reviewer evidence, not an edited profile. It repeats publication checks and invokes the native five-file transaction. `apply --setting "$SETTING_ID"` selects one staged item.

An outcome may be a complete finite no-change check, a staged proposal, a committed proposal, a committed partial proposal, an incomplete study or an error. A native comparison's mathematical status is a separate concept. Partial adoption does not certify the unassessed complement or advance a successful complete-maintenance watermark.

## Resume deliberately

Inspect a stopped attempt before starting another paid-capable attempt:

```bash
atlas-renew --config local.toml checkpoint "$RUN_ID" --setting "$SETTING_ID"
atlas-renew --config local.toml continue "$RUN_ID" --setting "$SETTING_ID"
```

Continuation requires matching baseline, cutoff, policy, semantics, backend/model configuration and archived audit bindings. It carries only unapproved working notes, mechanical diagnostics and verified source handles. The new role must perform its own required reads. It never inherits an approval or another role's reading credit. Ordinary `run` does not silently invoke checkpoint continuation. `run --retry-incomplete` is a separate explicit retry and may perform new research.

If a completed original scout already produced an unapproved prepared candidate, avoid repeating research by explicitly planning a new independent review in the same workspace:

```bash
atlas-renew --config local-review.toml plan-review --source-run "$SOURCE_RUN" --ids selected-ids.json
atlas-renew --config local-review.toml run "$REVIEW_RUN"
atlas-renew --config local-review.toml apply "$REVIEW_RUN"
```

The source baseline, cutoff, model and original native journal remain pinned. Current scientific and native preparation checks run again. Only a fresh reviewer is called; original scout usage is provenance, not a new research session. An eligible closed partial candidate retains every failure and unresolved obligation, and still needs a new clean reviewer. Budget-exhausted or unstable sources, modified evidence, already approved/published sources and known reviewer rejections cannot be bypassed through this route. A revised candidate must use the appropriate new research path.

Create a new plan after changing code, instructions, schemas, budgets or strategy. Do not edit old plans, prepared hashes or approval files. Reuse the bound workspace for the same cumulative cycle rather than moving files to reset accounting.

## Drafts and offline checks

```bash
atlas-renew --config local.toml draft-analysis --setting "$SETTING_ID" --out draft-analysis.json
atlas-renew --config local.toml validate-analysis --profile profile.json --analysis draft-analysis.json
python scripts/check_resources.py
python examples/offline_demo.py --output demo-output
```

Draft output is outside the Atlas and remains unreviewed. Validation checks structure and references, not theorem validity. The offline demo uses synthetic fixtures and temporary native transactions; it is not live literature research, scientific approval or an extension of profile generation. Use a fresh demo output directory.
