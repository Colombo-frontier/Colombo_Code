# Structural_exploration Design

## 1. Role of the Component

The new entry point starts from settings already defined in the Atlas, proposes research contracts worth adding, determines whether they are already included, and then reuses the existing workflow for profile research, independent review, and five-file ingestion.

This entry point does not require a triggering paper. Candidate provenance is explicitly recorded as `atlas_expansion`, together with a frozen version of the seed setting, the transformation used, and the rationale for selection. Papers found during subsequent research still require evidence tied to their actual versions, theorems, and locations in the original text. Candidates without papers use empty `paper_refs`; bibliographic or extraction records must not be fabricated to satisfy the previous workflow.

The code uses one shared backend and two application entry points: the original `oracle-atlas` retains its paper-scanning role, while `structural-exploration` handles neighborhood expansion. Identity comparison, complexity research, profile review, tools, memory, input budgets, and Atlas transactions reuse the existing implementation. Expansion logic is concentrated in `src/oracle_atlas/expansion/`.

## 2. New and Reused Agents

Three new roles are introduced, each operating at a different level of granularity:

| Role | Inputs and responsibilities | Formal output |
|---|---|---|
| `expansion_planner` | Reads the bounded scope, seeds, and neighbor summaries; proposes concise opportunity cards and explains their ranking | `expansion_plan` |
| `setting_expander` | Completes the full eight-axis specification, tags, and mathematical consistency checks for one selected direction | `expansion`, referencing a frozen `candidate` |
| `expansion_reviewer` | Independently reviews scope, specification, nonemptiness, value, and duplication with previously reviewed candidates in the batch | `expansion_review` |

Subsequently, `matcher` and `identity_reviewer` continue to determine identity relative to the current Atlas. Confirmed new settings are passed to `profile_researcher`; updates to existing entries, when permitted, may be passed to `bound_updater`. The final stages share `profile_reviewer` and the Atlas writer.

Planning produces only concise cards; it does not require more than twenty complete specifications at the outset. Full specifications are generated only for a bounded set of selected directions. Literature and bracket research is then conducted only for candidates that pass review, have a resolved identity, and receive a research slot.

Each new role has its own `AGENTS.md`, `protocol.md`, and `SKILL.md`. Responsibilities and collaboration rules are loaded explicitly, while detailed skills are read as needed. The shared standard `standards/expansion.md` explains the expansion methodology; the eight-axis, tagging, evidence, and profile standards remain shared.

## 3. Defining the Scope of an Expansion Round

A round is a bounded, resumable request. Its scope distinguishes at least four elements:

1. **Source scope**: `source_task_ids` restricts the task families from which seeds may be selected.
2. **Target scope**: `target_task_ids` specifies the task families to which transitions are permitted.
3. **Scope of changes**: `allowed_operators` and `allowed_axes` restrict the transformations and affected axes permitted in the round.
4. **Preservation conditions**: `fixed_constraints` and `scope_description` specify mathematical or research requirements that must be preserved, to be interpreted by agents and independently reviewed.

For example, a transition from a higher-order or first-order model for single-objective optimization to a zeroth-order model may be restricted to the same task family. A transition from single-objective to bilevel optimization should explicitly add bilevel to the target scope and specify whether the transition concerns the upper level, lower level, or coupling structure. A new target task must already exist in the Atlas task taxonomy or approved catalog; expansion agents cannot enlarge the task catalog on their own.

`seed_setting_ids` can identify specific seeds; when it is empty, the component selects a bounded combination from the source scope. If target tasks are not explicitly specified, the declared task families of the seeds selected for the round are used. When task membership is unknown, a definitive classification must not be inferred from the title; an explicitly approved target task is required.

Source task tags are used for preliminary filtering. Unknown information or information in legacy formats remains pending determination and must not simply be treated as outside the scope. The model verifies free-text constraints and mathematical preservation conditions; the code does not split natural language into keywords and then claim to have completed mathematical filtering.

## 4. Neighborhood Extent: Separating Navigation Relations from Transformation Depth

The current neighborhood implementation reads a compact catalog and uses declared task, oracle, and model concepts, together with registered parent-class relationships, to recommend a small number of entries worth reading together. Entries in the target task families can also serve as references for transitions.

This is not a graph of mathematical relations in which the meaning of every edge has been proved. Catalog similarity serves only as a navigation aid; it does not imply that two settings are equivalent, that a reduction exists, or that complexity bounds transfer automatically. Any subsequent records of simulations, inclusions, or objective transformations must specify their direction, assumptions, parameters, and costs.

The default `max_mutation_steps=1` denotes one principal conceptual change; it does not restrict changes to a single JSON field or axis. For example, moving from a single-level to a bilevel structure is one hierarchical transition, but it requires coordinated definitions of the functions at both levels, inner-level selection, outputs, errors, and the oracle at each level. All dependent changes must remain within the permitted axes and be justified as necessary parts of the same transition.

If two independent changes are needed, such as changing the noise protocol and then moving to a bilevel structure, two mutation steps may be explicitly permitted. The current implementation does not immediately reuse unverified model-generated candidates as seeds for the next generation, preventing the recursive propagation of unreviewed assumptions; results formally ingested into the Atlas may participate in the next round.

**Discovery scope differs from the scope of identity deduplication.** Only a small number of neighbors are recommended for each seed to control research input. Determining whether a new candidate already exists still requires broad retrieval across the entire Atlas and LLM comparison, rather than checking only those few neighbors.

## 5. Why Use Portfolio Batches Rather Than Exhaustive Enumeration?

The default scheduling parameters are listed below. These parameters control cost; they are not theoretically sufficient thresholds.

| Parameter | Default | Meaning |
|---|---:|---|
| `max_seeds` | 8 | Maximum number of seeds in the round |
| `max_neighbors_per_seed` | 6 | Maximum number of navigation neighbor summaries per seed |
| `max_opportunities` | 24 | Maximum number of opportunity cards proposed by the Planner |
| `max_candidates` | 16 | Maximum number of directions entering the full-specification stage |
| `max_profiles` | 10 | Maximum number of candidate slots for initiating profile research |
| `max_mutation_steps` | 1 | Maximum number of principal conceptual transformations per direction |
| `max_per_seed` | 3 | Maximum uses of one seed among the directions selected for the round |
| `max_per_operator` | 5 | Maximum uses of one transformation among the directions selected for the round |

Seed selection combines usage counts from previous rounds, task and oracle diversity, and stable ordering. The LLM assigns priorities and rationales to opportunity cards; the program applies quantity and diversity constraints in that order. The purpose is to avoid persistent concentration on the first few tractable nodes and prevent one seed or transformation from dominating an entire batch.

`max_profiles` limits the number of research efforts initiated; it does not guarantee ten completed profiles. A research effort that enters a pending-verification state still consumes one of the round's initiated research slots. When updates to existing settings are enabled, those updates also consume research slots. The final result may contain fewer than ten profiles eligible for approval; the report must state the counts and reasons progress stopped, without meeting the quota by lowering standards or marking unknown results as closed.

The current implementation executes the formal stages using a bounded queue and does not claim to implement parallel scheduling across candidates. Agents may use the existing tools for batched, narrowly scoped reads; the shared runner handles tool calls, segmentation, and recovery.

## 6. Assessing Whether a Direction Is Worth Expanding

Each opportunity card must identify the source seed, the object and properties being changed, the conditions preserved, why the change produces a meaningful research contract, potentially reusable algorithms or lower-bound mechanisms, and risks that remain to be verified.

Three prioritization modes are available:

| Mode | Priorities | Claims not justified by the mode |
|---|---|---|
| `classical` | Classical foundational contracts, reusable coverage, and clear evidence pathways | Classical entries necessarily contain unresolved problems |
| `gaps` | Directions with an explicit mechanistic rationale and complexity relationships that remain to be verified | A missing bound in the Atlas proves that the problem is open in the literature |
| `balanced` | A combination of coverage value, mechanism diversity, and verification cost | All selected candidates are equally important |

Scientific review must check that the model is nonempty, the objective and outputs are well defined, oracle promises are consistent, and the assumptions do not already reveal the answer. Here, "interface realizability" refers to the internal consistency of the information model; it does not require an idealized exact oracle to have a low-cost computational implementation in practice.

Research may continue for a fully specified setting for which no lower bound has yet been found, producing a profile that accurately reports missing lower. The absence of a known bound, missing fields in a candidate definition, and an original theorem awaiting verification are distinct issues.

## 7. Preventing Duplicate Additions

The round uses two layers of independent checks:

**The first layer deduplicates candidates within the batch.** Each expansion reviewer receives references to candidates in the batch that have previously passed specification review and assigns a distinct, equivalent, or unresolved judgment to each comparison. Equivalent candidates retain a reference to the canonical candidate and their provenance, but do not trigger duplicate research. An approve decision cannot override a credible comparison that remains unresolved.

If a review was interrupted and candidates approved later are present upon resumption, the system also checks before research whether the comparisons for the current candidate pairs have been covered. Missing comparisons trigger only supplementary independent review, reusing the frozen specifications.

This layer currently addresses reviewed candidates within the same batch. Pending records from earlier batches are available as history leads to consult and avoid redundant work; this does not constitute exhaustive semantic deduplication across all historical candidates. Historical results formally ingested into the Atlas are covered by the next layer.

**The second layer compares identity across the entire Atlas.** It reuses multichannel tag/text retrieval and independent identity review. An empty top-k, identical tags, or an identical rate cannot determine whether a setting is new or already exists.

A change from deterministic to randomized computation, a new success guarantee, a new algorithm, or a parameter window may often belong to a view, witness, or regime within the original profile. Matcher should make an explicit determination rather than force the creation of a new setting simply because the task is called "expansion". With the default `allow_existing_updates=false`, such results are recorded as `redirected_existing` and the existing ID is reported; enabling this option routes them to the update branch for the existing profile.

## 8. Reusing Subsequent Research and Evidence

After specification review and identity confirmation, candidates enter the existing research pipeline: extract atomic results source by source, record algorithmic scope and costs, complete any necessary short proofs or applicability transformations, and then synthesize the bracket using the full comparison key.

A candidate derived from a neighbor does not automatically inherit the applicability of that neighbor's bounds. One-way oracle simulations, model inclusions, objective substitutions, and guarantee transformations all require explicit assumptions and costs. Full literature sources, historical proofs, and review indexes are retained by reference; stage inputs do not automatically concatenate all materials.

Old evidence IDs in a seed snapshot likewise do not automatically constitute reviewed proofs in the current workspace. Their contents may serve as historical leads, but adoption still requires a verifiable source or an independent proof.

Generated reader-facing profiles continue to use professional English. Their specification, view/regime, upper and lower bounds, status, and evidence should be self-contained, without relying on historical explanations such as "the previous round's D1/D2 audit appendix".

## 9. Human Approval and Batch Ingestion

The expansion entry point requires proposals that have completed research and independent review to stop at `ready_for_approval`, allowing a human to approve individual proposals or the entire batch. This does not change the publication policy of the original paper-scanning entry point.

After the first new setting in a batch is ingested, the Atlas-wide version changes. Subsequent proposals cannot proceed with writes merely by replacing the version number. The publication path repeats identity comparison and independent identity review against the current Atlas.

If a candidate remains a new setting and its scientific content has not changed, the component retains the original research results, rebinds the candidate to the current identity, and obtains a new independent profile review. This path does not repeat the full literature investigation, nor does it carry over approval of an older document as approval of the current document. If an equivalent existing entry is found, the status changes to `superseded_existing` and the result is reported, preventing a duplicate addition.

Human approval is bound to the content hashes of the five files reviewed. If the contents of those files change after a refresh, the new proposal must again await human review; the original approval cannot cover the changed content. A proposal counts as ingested only when an actual commit receipt has been obtained.

## 10. Recovery, Budgets, and Input Control

The same normalized request and `run_label` identify the same batch; repeated execution resumes that batch. To start another round based on a new Atlas state, change `run_label`; also persist `cutoff_date` explicitly so that execution spanning multiple calendar days does not implicitly change the request.

Recovery has three forms:

- An ordinary `resume` continues unfinished tasks; it does not resample scientific rejections or pending outcomes until they pass.
- `specification`, `identity`, and `research` revisions target their corresponding stages and require conditions permitted by the existing protocol, such as explicit revise feedback or new material.
- Low-level protocol errors, budget exhaustion, and transport uncertainty each use the corresponding job recovery operation; these operations do not change scientific conclusions.

Each candidate retains the configured run budget, while the batch adds aggregate limits on model calls, external calls, and jobs. The default batch limits are 1600 model calls, 600 external calls, and 240 jobs. These limits prevent uncontrolled execution; they are neither estimates of consumption nor an indication that every round will exhaust them.

Client inputs and tool returns continue to be segmented according to the existing budgets. Agents read and write files, drafts, formal artifacts, and concise memory records instead of waiting for a single enormous JSON request to output all profiles. The internal context of Codex or a hosted service is not fully observable, so a client-side character budget cannot be described as an absolute peak guarantee for every backend.

## 11. Code and Data Entry Points

| File or directory | Responsibility |
|---|---|
| `src/oracle_atlas/expansion/request.py` | Default scope, normalization, and request validation |
| `src/oracle_atlas/expansion/neighborhood.py` | Bounded seed combinations and navigation neighbor summaries |
| `src/oracle_atlas/expansion/selection.py` | Applying budget and diversity constraints in LLM-ranked order |
| `src/oracle_atlas/expansion/validation.py` | Consistency of references, scope, outputs, and reviews in the new stages |
| `src/oracle_atlas/expansion/engine.py` | Expansion batches, revisions, research integration, and approval and publication |
| `agents/expansion_planner/` | Opportunity-planning responsibilities and skills |
| `agents/setting_expander/` | Responsibilities and skills for constructing complete contracts |
| `agents/expansion_reviewer/` | Independent specification review and within-batch deduplication |
| `standards/expansion.md` | Expansion principles aligned with the eight-axis, identity, and evidence standards |
| `config/expansion_request.example.json` | Editable request with a bounded scope |

Backend tools, memory, results, and drafts continue to be managed in the same workspace. Atlas writes remain a five-file transaction involving `profile.json`, `identity.json`, `classification.json`, `human_tags.json`, and `machine_tags.json`.

## 12. Distinctions Required in Acceptance Evaluation

Software acceptance evaluation should cover accurate origin records for candidates without papers, resumption after specification revisions, routing to existing views, within-batch duplicates, identity retrieval across the entire Atlas, pending human approval, version refresh for the second item in a batch, and idempotence under repeated execution.

Offline scripted tests can verify these software behaviors, but cannot establish that the model has actually proposed valuable new settings or that the bracket derived from an actual publication is correct. Scientific acceptance evaluation must be performed using the user-selected model and Atlas, examining complete specifications, actual evidence, independent reviews, and actual receipts. Delivery reports must separately describe completed code tests, actual model calls, research using actual papers, and formal Atlas changes, without merging them into a single claim that "the workflow ran successfully".
