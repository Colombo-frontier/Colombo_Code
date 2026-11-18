# Workspace Migration and Continuation

Use Literature_grounded_discovery with the existing Atlas file structure while starting an independent runtime workspace. The component keeps `oracle-atlas` and `oracle_atlas` integration entry points.

## Prepare an Atlas copy

Preserve a recoverable copy of the target Atlas. Install the component and configure it following the [README](../README.md), then point `atlas` to the copy and `workspace` to a separate empty directory.

```bash
oracle-atlas init --config config.local.toml --atlas ./atlas-copy \
  --workspace ./work --backend responses --model YOUR_AVAILABLE_MODEL_ID
oracle-atlas doctor --config config.local.toml
oracle-atlas run-paper --config config.local.toml --url https://example.org/paper
oracle-atlas status --config config.local.toml
```

Replace the URL with a genuine paper source. These commands describe a validation procedure; they do not assert that a paper has already passed review or ingestion. Check model access, the approved task catalog, publication-event selection, budgets, and publication policy before widening the scan.

## Reuse scientific material

| Material | Treatment |
| --- | --- |
| Native five-file setting records | Read through Atlas adaptation and validate against native schemas |
| Sources, results, and proofs | Import as fixed material and independently check applicability to current claims |
| Drafts and previous reviews | Preserve as references without treating their state as current approval |
| Pending jobs, call caches, and transaction logs | Keep in their original runtime workspace |
| Browsing pages and indexes | Rebuild through existing Atlas tools |

The five setting files are `profile.json`, `identity.json`, `classification.json`, `human_tags.json`, and `machine_tags.json`. The adapter preserves unrelated extension fields and stable IDs. Similar titles or rates cannot establish mathematical identity.

Import additional source material:

```bash
oracle-atlas import-source --config config.local.toml --file ./materials/paper.pdf
oracle-atlas resume --config config.local.toml --case-id CASE_ID \
  --stage identity --material-ref ACTUAL_SOURCE_REF
```

Use the actual returned source reference. Choose `extraction` for changed core specifications and `research` for additional bounds or proofs within the confirmed identity. An affected candidate receives independent review again; sibling progress is retained.

Do not copy model outputs into runtime tables or mark jobs complete manually. Format failures require schema-guided protocol repair. Scientific revision requires new material or a specific review request. Ordinary continuation does not turn uncertainty into approval.

## Approval and baseline checks

With `publication.require_human_approval=false`, an authorized scan can commit after independent reviews and baseline checks pass. To inspect each case, enable human approval and export cases in `ready_for_approval` before using `resume --case-id CASE_ID --approve`.

Task-catalog expansion requires a task_scout proposal and explicit `approve-task`. After a workspace contains `approved_tasks.json`, that file holds its approved catalog; editing the initial configuration does not silently replace approval history.

Scientific baselines depend on native records, schemas, vocabulary definitions, and aliases. Rebuilding known derived browsing indexes does not create a scientific conflict. After `atlas_conflict` or `identity_stale`, recheck the affected work instead of replacing `base_version` manually.

An update review checks the frozen baseline, changes, applicability, and all proposed active bounds. Previous document approval does not establish adoption of every pending claim or automatic approval throughout a proof-dependency graph.

## Budget continuation and subsequent scans

After confirming the additional budget, increase the applicable configuration limits and continue:

```bash
oracle-atlas resume --config config.local.toml --job-id JOB_ID --continue-budget
oracle-atlas resume --config config.local.toml --case-id CASE_ID
```

This retains fixed records and advances the affected candidate. It does not reopen completed scientific rejections.

Identical scan requests and run labels reuse completed stages. For a separate subsequent search, choose a distinct descriptive label and replace `YEAR`:

```bash
oracle-atlas scan --config config.local.toml --task single_objective \
  --year YEAR --run-label followup
```

A run label identifies execution scope; it does not establish exhaustive coverage. Review actual sources, unfinished work, and receipts.

## Validation and rollback

Validate missing-bound updates, new views, and new settings separately. Record the model configuration, source identity, reused material, scope, and actual receipts. Engineering checks and generated reader text do not establish scientific acceptance.

Retain recoverable Atlas backups and runtime records according to the deployment's policy. Deleting a receipt is not rollback. Concurrent writers must respect the shared write lock. See [Atlas adaptation](atlas_adapter.md) for transaction recovery and [backend adapters](providers.md) for transport recovery.
