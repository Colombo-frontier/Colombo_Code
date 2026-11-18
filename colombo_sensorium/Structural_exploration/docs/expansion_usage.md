# Using Structural_exploration

The expansion frontend proposes settings from an existing Atlas and reuses the paper component's identity, research, review, tools, and transaction services. Its command is `structural-exploration`. The existing `oracle-atlas` command remains available for paper discovery and maintenance.

Expansion always stages reviewed profiles for explicit human publication. Running a batch does not itself approve or commit its profiles. A candidate without a triggering paper has an `atlas_expansion` origin and an empty `paper_refs` array; it is not wrapped in an artificial paper record.

## 1. Install and configure

From the extracted project directory, install the shared package and the desired optional providers:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[all,test]"
```

Create configuration for an Atlas copy before running acceptance on production data:

```bash
structural-exploration init \
  --config config.local.toml \
  --atlas "/absolute/path/to/atlas-copy" \
  --workspace "./work-expansion" \
  --backend codex

structural-exploration doctor --config config.local.toml
```

Use `--backend responses --model YOUR_AVAILABLE_MODEL_ID` when using the Responses provider. Configure the actual credentials/environment and supported model options according to `docs/providers.md`; neither installation nor `init` authenticates a model account. Codex uses the available configured CLI and its account/session. External read-only MCP tools use the same explicit allowlists as the paper frontend.

Paths in the TOML configuration resolve relative to that configuration file. Use a dedicated expansion workspace to make its batches easy to inspect. The Atlas may be shared with the scanner, subject to the same version checks and serialized writer.

## 2. Define one finite request

Start from `config/expansion_request.example.json`. It illustrates single-objective seeds, single-objective/bilevel targets, value/noise/model/layer changes, and explicit dimension/resource requirements. Replace the task IDs with those actually declared in your Atlas or approved task catalog. The example's date is fixed for reproducibility; update it deliberately for a later literature cutoff.

The most important fields are:

| Field | Meaning |
|---|---|
| `source_task_ids` | Task families used to screen seed settings. Unknown membership is retained for Agent review. |
| `target_task_ids` | Approved task families that may receive new candidate definitions. Empty means the declared tasks of the selected seeds. |
| `seed_setting_ids` | Optional explicit seed pool. Use real stable IDs; empty enables bounded portfolio selection. |
| `allowed_operators` | Allowed conceptual transformations, such as `oracle_substitution`, `noise_protocol`, `model_transfer`, or `layer_transfer`. |
| `allowed_axes` | Eight-axis properties that may change, including necessary dependent changes. |
| `fixed_constraints` | Scientific requirements that the planner, expander, and independent reviewer must preserve. |
| `scope_description` | Human-readable research intent; it is not treated as a closed-world keyword filter. |
| `priority` | `balanced`, `classical`, or `gaps`; this affects planning, not mathematical truth. |
| `cutoff_date` | Explicit literature cutoff in `YYYY-MM-DD` form. |
| `run_label` | Distinguishes a new discovery round from resuming the same request. |
| `allow_existing_updates` | Defaults to false. Existing matches are reported; true also allows the shared update branch. |

Supported operator IDs are `oracle_substitution`, `noise_protocol`, `model_transfer`, `layer_transfer`, `target_change`, `resource_change`, `boundary_probe`, and `algorithm_permission`. An operator is a prompt-level direction, not a built-in theorem or a command to create a new top-level setting. For example, an algorithm-permission change may be an existing profile's view.

The defaults are eight seeds, six neighbor summaries per seed, 24 opportunity cards, 16 fully specified candidates, and at most ten candidates entering profile research. The selector also caps an individual seed at three selected opportunities and an operator at five. Requests must satisfy `max_profiles <= max_candidates <= max_opportunities`.

`max_mutation_steps=1` allows one primary conceptual transformation. A layer transfer may require changes to several axes; those dependencies must be explicit and authorized. The component does not recursively expand unreviewed candidates.

Before research, the controller also checks pairwise comparison coverage among current approved peers. A late-completing review triggers only the missing independent peer review, without regenerating the specification.

The profile limit counts research starts, including a case that later remains unresolved. It is not a guarantee of ten completed profiles. Existing updates also consume this limit when enabled.

## 3. Inspect a plan or run the batch

Create a plan without launching all candidate research:

```bash
structural-exploration plan \
  --config config.local.toml \
  --request config/expansion_request.example.json
```

The result identifies the batch. Review the selected seed portfolio, opportunity cards, and deferred directions. Planning uses a real model backend when configured; it is not a free static preview.

Run the request through specification, independent review, identity verification, and the bounded research phase:

```bash
structural-exploration run \
  --config config.local.toml \
  --request config/expansion_request.example.json
```

The normalized request determines the batch ID. Reusing the exact request, including its cutoff and run label, reuses the stored plan and work. Change `run_label` to intentionally begin a new round against the current Atlas. A normal resume does not silently replace the old discovery snapshot with a new one.

The default request omits `cutoff_date` only if the caller wants it filled with the execution date at normalization. Set it explicitly for repeatable runs that may continue across midnight or on another host.

## 4. Understand outcomes

The batch report records opportunities and candidates separately. A new opportunity is not yet a full specification, and a full specification is not yet an Atlas addition.

| Outcome | Interpretation |
|---|---|
| `specified` | A candidate has been constructed. Inspect its `candidate_review_ref` before treating specification review as approved; identity/research may still be pending. |
| `expansion_revise` / `expansion_defer` / `expansion_exclude` | Independent specification review requires repair, lacks necessary information, or excludes the direction. |
| `duplicate_pending` | An independently compared candidate duplicates a supplied pending peer in this batch. Its provenance is retained. |
| `identity_unresolved` / `identity_revise` / `identity_defer` | Whole-Atlas identity is not yet approved. These do not imply a new setting. |
| `redirected_existing` | The candidate maps to an existing profile and updates are disabled for this request. |
| `research_deferred_budget` | The candidate did not receive a research-start slot in this finite batch. |
| `profile_revise` / `profile_defer` | The research proposal needs the corresponding scientific work or materials. |
| `ready_for_approval` | Independent review is complete; a person can inspect and publish the frozen proposal. |
| `superseded_existing` | A pre-publication identity refresh found an existing Atlas target. No duplicate new setting is committed. |
| `committed` | A successful transaction issued an ingestion receipt. |

Other execution states preserve job-level transport, protocol, or budget interruptions. Inspect the recorded diagnostic rather than treating every incomplete job as a scientific rejection.

Same-batch comparison covers all supplied previously approved peers. Earlier uncommitted batches are history leads, not an exhaustive semantic duplicate registry. Every final Atlas identity decision still requires full-library retrieval and independent reasoning.

## 5. Inspect and export

Use status to inspect recorded progress:

```bash
structural-exploration status --config config.local.toml
```

Export the batch report and available profile material for review:

```bash
structural-exploration export \
  --config config.local.toml \
  --batch-id BATCH_ID \
  --out ./expansion-review
```

Reader-facing profiles remain professional English. The batch explains why each setting was selected and distinguishes research gaps from missing verification. Incomplete candidates remain visible; exporting a draft does not change its approval state or issue a receipt.

## 6. Resume and revise

Continue ordinary unfinished batch work:

```bash
structural-exploration resume \
  --config config.local.toml \
  --batch-id BATCH_ID
```

Request a scoped candidate revision:

```bash
structural-exploration resume \
  --config config.local.toml \
  --case-id CASE_ID \
  --stage specification
```

The available stages are `specification`, `identity`, and `research`. A scientific revision needs an explicit revision request or new material/current-version change under the shared recovery protocol. Ordinary resume must not repeatedly sample a deferred conclusion until it becomes approval. Preserve and address each existing issue's actual remaining scope.

Job-level recovery uses `--job-id` and the shared explicit recovery flags, such as `--repair-protocol`, `--retry-transport`, or `--continue-budget`, for their respective conditions. Inspect `structural-exploration resume --help` and the recorded diagnostic before selecting one. A transport retry can incur a new provider charge; a local cached response is reconciled when available. Raising an exhausted budget is an explicit configuration decision, not an automatic infinite loop.

## 7. Publish reviewed selections

After reading the exported profile and proposal, approve named cases:

```bash
structural-exploration publish \
  --config config.local.toml \
  --batch-id BATCH_ID \
  --case-id FIRST_CASE_ID \
  --case-id SECOND_CASE_ID
```

To approve all currently ready proposals in that batch:

```bash
structural-exploration publish \
  --config config.local.toml \
  --batch-id BATCH_ID \
  --all-ready
```

Publication is serial. Each new-setting proposal must still have a valid current Atlas identity. The first commit changes the inventory for later proposals, so a later proposal may need refreshed matching, independent identity review, and final profile review. When scientific content remains unchanged, the original research artifacts are retained rather than repeating the full literature investigation.

Authorization binds the five-file content the person selected. If refreshed preparation changes that content, the case returns to approval with a note; the old authorization does not silently cover the new files. If identity refresh finds an existing target, the case is reported as superseded and is not committed as a new setting.

`publish` may therefore perform additional model work and may produce fewer receipts than selected cases. Inspect the report and actual receipt references. Re-running a successful publication does not create another copy of a committed case.

A receipt confirms the five authoritative setting files and their transaction record. The component does not rebuild an Atlas application's derived catalog, browsing indexes, or website. If the application reads those generated files, run its existing catalog and site build/release workflow after accepting the committed settings.

## 8. Budgets and practical operation

The existing `[budgets]` values bound each Agent/candidate execution scope, including input characters, tool return size, calls, jobs, segments, and bounded repairs. The expansion frontend adds finite batch ceilings:

```toml
[expansion]
max_batch_model_calls = 1600
max_batch_external_calls = 600
max_batch_jobs = 240
```

These values are ceilings, not usage estimates. A first real acceptance run can use fewer seeds, opportunities, and profile starts while keeping the same review requirements.

The current workflow runs finite candidate phases sequentially. It uses shared bounded tools and may batch selected small reads, but does not advertise a cross-candidate parallel scheduler. Large artifacts remain in the workspace and are read in pages. Only compact references and checkpoints carry across model segments.

Software acceptance and scientific acceptance are separate. Offline scripted fixtures can exercise provenance, independent stages, routing, retries, publication, and receipts. They cannot establish that a real model will find a valuable new problem or that a real paper's bounds are correct. See [testing and release boundaries](testing.md) for the software-validation scope, then perform real-model acceptance on an Atlas copy before relying on the workflow for production research.
