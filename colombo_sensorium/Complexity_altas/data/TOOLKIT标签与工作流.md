# Toolkit Tags and Research Workflows

`data/settings/<setting_id>/profile.json` stores the mathematical specification. Toolkit provides two tagging layers that can be rebuilt. Each record is linked to the original specification through the setting ID, view ID, and profile hash.

| Tagging layer | Files | Purpose |
| --- | --- | --- |
| Human navigation | `data/vocabulary/human_tags.json` and the `human_tags.json` for each setting | Filter by common concepts and inspect matching views and expandable native-interface descriptions. Options within a group are combined with OR; different groups must be satisfied by the same view. |
| Machine tags | `data/vocabulary/machine_tags.json` and the `machine_tags.json` for each setting | Find candidates using exact concepts and inspect source fields, objects, operations, variable blocks, norms, domains, and applicable views. Unparsed fields remain unknown. |

Both layers use the eight axes TASK, MODEL, ORACLE, ALGORITHMS, OUTPUT, METRIC, GUARANTEE, and RESOURCE. Human tags group related concepts, while machine tags preserve distinctions. For example, native reduced-objective gradients, partial gradients of the upper-level function, and lower-level Hessian-vector products retain their respective query, response, object, coupling, and cost-accounting conventions.

## Offline Exact Queries

Run the following command from the Atlas root directory. This example finds views in `CV_S_HIGH_VI` that have both the complete operator jet operation tag and the exact feedback tag.

```bash
python3 data/tools/query_machine_tags.py \
  --setting CV_S_HIGH_VI --axis ORACLE \
  --concept ORACLE:operation:operator_complete_jet \
  --concept ORACLE:feedback_quality:exact
```

Select concept IDs from `concepts` in `data/vocabulary/machine_tags.json`. Passing `--concept` multiple times requires the same view to have every specified exact tag. Omit `--setting` to query all current settings. `--axis` requires all selected concepts to belong to the specified axis. `--data-dir` can point to the `data/` directory of another compatible release.

The JSON results provide `matching_view_ids`, `matched_features` with their original bindings, and `operation_bindings` for the matching views. The latter supplies the complete oracle-operation context for each view. To determine whether multiple tags refer to the same operation or object, inspect the individual bindings. Unknown concept IDs, unknown setting IDs, and missing or outdated tag records produce errors. A known ID returning zero results means only that the current records contain no match within the same view; unknown fields still require investigation. Exact-tag queries provide candidates and provenance; mathematical identity, scope membership, reductions, and theorem applicability require independent review.

## Toolkit Research Entry Points

Use the following entry points in a separate Toolkit working directory. The toolkit requires Python 3.10 or later and SQLite FTS5. Online research requires access to the relevant paper sources and configured models and credentials. Detailed parameters are documented in `docs/WORKFLOWS.md`, `docs/PROVIDERS.md`, and `docs/CODEX_IMPLEMENTATION_GUIDE.md` in that directory.

| Entry point | Research objects and outputs |
| --- | --- |
| `venue`, `scan` | First confirm the journal ISSN, then enumerate Crossref metadata by year and the chosen date convention. `--screen` retains entries with missing abstracts or uncertain relevance. `--ingest` sends candidates to theorem extraction and review. The scan year limits the discovery scope; subsequent upper- and lower-bound research uses a separately specified `literature_cutoff`. |
| `extract`, `ingest`, `research` | Read versioned paper source texts with precise locations, extract theorem-level contracts, and retrieve candidates; then investigate upper bounds, lower bounds, and corrections separately. Improvements sharing the same specification are incorporated into the existing profile or added as a new view. When proposing a new setting, extend identity review to the entire current library. |
| `discover` | Make explicit changes to the task, model, or oracle of an existing setting to generate research hypotheses and search leads. `--investigate` sends the identified literature through the same review pipeline. |
| `scope` | Review scope membership for Atlas candidates individually, optionally incorporating external literature and leads from neighboring contracts. `classical_first` prioritizes classical problems, while `unresolved_gap_first` prioritizes unresolved gaps. Missing upper and lower bounds are separate statuses. Result counts, candidate counts, paper budgets, and new-setting budgets are accounted for separately. `--atlas-only` still uses the scope-review model. |
| `review`, `publish` | After identity, applicability, and publication review, plus scope review where applicable, staged proposals are submitted with bindings to the current release version and source evidence. Re-review is required if the version changes. |

The active Toolkit release is specified by `data/state/active.json`, which points to an immutable release manifest and content-addressed objects. `data/settings/` is the working mirror of that release. When applying reviewed changes to Atlas pages, rebuild tags, indexes, and pages from the same release version, and retain the Atlas's complete profile export format.
