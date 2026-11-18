# Research Cell

This directory contains Cell instructions, protocols, and Skills; all runtime code resides in `src/colombo/cell/`. Launch a Standalone Cell through `run_cell.py` at the repository root, supplying a UTF-8 Markdown mathematical problem for natural-language research.

The Colombo Cell uses `storage_version=2` and collection `schema_version=2`. Research record references have the form `{kind,id,revision}`, with versions appended by revision; legacy storage formats are rejected without migration. Audit promotion and error revocation compare the actual arguments, and reviews are linked by `review_id + report_revision`. Cell research records retain their existing version checks; Brain's fixed Input Packages and each returned ZIP have separate file-content verification.

**All defaults come from the sole outer [config.toml](../../config.toml)**. The top-level `profile` selects standard/hard; shared values appear once, and hard specifies only differences. Colombo research has no run-wide deadline; Standalone Cell and Brain use the same resolved configuration, retaining each Cell's cumulative starts, Experiment resources, and infrastructure timeouts.

The main agent's directory and runtime role are named `prover`, parallel child agents are `subcell`, and the full-review agent is `verifier`. The draft submitted for review is `draft.md`; the accepted manuscript is `manuscript.md`.

Provers and subcells can perform read-only retrieval from shared Long-Term Memory through [Scientific Memory MCP](../../docs/MEMORY.md), obtaining Algorithms, Hard Families, Theorems, and reusable skills. It is independent of the external search switch; the Verifier still reads only authorized fixed packages.

The Verifier creates review records around the actual proof and uses the checklist to find omissions; the prover may challenge a certified Argument when a specific concern exists, with support revoked after confirmation by a local audit and independent review.

## Startup

Python 3.11+, a working Codex CLI, and a signed-in session are required. Run all commands below from the Colombo root:

```powershell
python -m pip install -r requirements.txt
python run_cell.py "your_problem_file.md" --run-dir runs/my-problem
```

Use a new empty directory for `--run-dir`; one is created automatically if omitted. Add `--model MODEL_NAME` to specify a model. If automatic CLI discovery fails, set `CELL_CODEX_BIN` to the executable path.

Resume an existing task:

```powershell
python run_cell.py --run-dir runs/my-problem --resume
```

## Parameters and Scope of Effect

Select the mode only at the top of the outer config: `profile = "standard"` uses the base configuration, and `profile = "hard"` applies differences from `[profiles.hard.*]`. Hard uses `gpt-6-astra / ultra`, with at most 15 / 20 Prover / Verifier starts and 4 report-check attempts; each Challenge allows at most 4 Challenge Reviewer starts, and the Report Checker allows at most 4 attempts per report version. Each parent allows at most 8 concurrent Subcells at depth 2, with Subcell external search enabled by default and unlimited research time. Standard disables Subcell external search by default. Colombo does not pass a run-wide research deadline to internal stages; Brain separately manages the two-hour limit for final integrate.

Hosted Experiment separately uses `cell.settings.experiment.reasoning_effort`: `medium` for Standard and `max` for Hard, without inheriting the Cell's `ultra`. Hard permits up to 12 Experiment runs. Each Experiment saves an independent model/effort snapshot; resuming an old Experiment still uses its originally fixed effort, without rewriting submitted requests or repeating execution.

`configure()` queries the current configuration; `detail="full"` reads the full execution snapshot. Changes require a reason and permit only non-budget fields such as model/search. Resource caps for time, rounds, concurrency, MCP/HTTP timeouts, files, and tokens can be changed only in the root config. `spawn_task` settings follow the same restriction.

After changing the root configuration, adopt the new policy revision at a safe resume boundary while retaining records and cumulative usage. Running child processes do not silently change configuration. Internal snapshots and compatibility aliases are not a second configuration entry point; `CELL_AGENT_TIMEOUT` no longer overrides budgets, and CLI options `--timeout` and `--max-rounds` are rejected.

`--model` and `--search` / `--no-search` remain available for non-budget behavior. Select the mode by changing the top-level profile, without overriding it again through the CLI.

## Search and Parent Material

By default, the main agent enables builtin web search and `lookup`, while subcells disable both search entry points. Defaults are specified by `prover_search_enabled` and `subcell_search_enabled` in `[cell.settings.network]` and are merely user-configured initial values. `lookup(query=...)` uses Serper search by default, and `lookup(url=...)` uses Jina Reader to read originals; `search_provider` / `reader_provider` in the same configuration still permit arXiv / direct, with the compatible theorem search service retained. See the [outer documentation](../../README.md#configuration) for credential locations and shared configuration. After obtaining useful material, a Cell still saves Sources through archive; lookup does not automatically write to Cell memory.

A parent agent may call `spawn_task(..., search_enabled=True, settings_overrides={...})` to enable search or configure other parameters for that subcell individually. If `search_enabled` is omitted, the subcell role default applies; the parent's own enabled search state is not automatically inherited. The tool still provides `lookup` to the subcell, but returns an explanation before making network requests when disabled; a subcell may call `configure(search_enabled=True, reason="Need to verify the original theorem")` when necessary and then use `lookup`. Builtin web search retains its value from the current process startup until the next startup.

Cells and subcells independently decide when to use [explore](prover/.agents/skills/explore/SKILL.md), what directions to pursue, how deeply to read, and when to return, based on the current Task and budget, to understand background, discover new methods, or compare routes. New insights may remain in an Attempt, linked to Sources through references.

When search is disabled, parent material in `retrieve` and `context/` remains readable. The parent agent selects records through `target_ref` and `context_refs`; the system expands dependencies according to configuration and copies fixed versions. Snapshots do not automatically track parent-library updates. When supplying literature to an offline subcell, save necessary text and locations in source records; providing a URL alone does not automatically download the original.

The search switch governs search entry points supplied by the program; it is not operating-system-level network isolation and does not affect model-service connections. Independent workspaces, MCP scopes, and read-only snapshot conventions likewise do not provide operating-system-level directory isolation.

## Numerical and Symbolic Experiments

Load [experiment](prover/.agents/skills/experiment/SKILL.md) as needed when a proof or counterexample construction is blocked, or an intermediate conjecture / pattern is uncertain, and computation is likely to provide insight into the next step. Keep a few directly calculable examples within the current skill; the current agent designs, calls tools for, and interprets batch sampling, enumeration, strategy search, and simulation, without requiring another agent or prior exhaustion of proof routes. Use experiment directly when the user explicitly requests it; do not run it routinely for every Claim or record a reason for omitting it on every route.

The information flow is: Attempt stores the question and design → `run_experiment` produces an `experiment_result` → save Examples / Claims / Arguments according to actual outputs → link results and next steps in the Attempt and `proof_state`. Code, data, plots, and related outputs remain artifacts; pattern discovery without an explicit proposition may link existing research records rather than requiring a Claim to be manufactured first. Observations do not automatically certify any mathematical conclusion.

`run_experiment(question, target_ref, code, request_id, parameters, input_files, attempt_ref)` executes Python through the OpenAI Responses API's Code Interpreter, saving the actual code, inputs, outputs, environment information, and file manifest. It requires a separate `OPENAI_API_KEY` environment variable; the program requests only the official API and does not write the key into configuration, prompts, or records. Experiment API usage is billed separately. Local mathematical libraries need not be installed for experiments, and cloud execution failure does not silently fall back to local execution.

`[cell.settings.experiment]` centralizes the enablement switch, API model, cumulative run count, container memory, and file limits; execution is constrained by the calling process's effective deadline and Experiment resource limits. Search and experiment switches are independent, so a subcell with search disabled may still run authorized experiments. Budget and resource limits can be adjusted only in the root config; new runs obtain a configuration snapshot. Each task executes experiments serially, with cumulative counts preserved across resumes and counted separately for each subcell. Experiments are also constrained by the calling process's remaining working time.

The same inputs and `request_id` identify the same execution; after interruption, recover the original result using `resume_experiment(experiment_id)` without resubmitting or resetting the execution deadline. Record unknown remote states, incomplete downloads, execution failures, and failure to discover new patterns separately. Expanding the scope or changing parameters defines a new experiment and requires a new request ID. `experiments/<experiment_ID>/state.json`, `plan.json`, and local evidence support recovery; containers have limited lifetimes, so download promptly.

The record type and filename are consistently **`experiment_result`** and `memory/experiment_result.json`. Tools write execution facts; agents may only supplement `observations`, `limitations`, and `derived_refs`. Attempts store selection reasons and route assessments, Claims store conjectures, Examples store constructions and properties, and Arguments store rigorous reasoning. A successful experiment does not itself generate `proved` / `checked`, and passing samples does not prove universal validity.

Arguments reference experiments through fixed-version `dependencies`; local audits and the verifier follow explicit dependencies to collect and copy code and artifacts, checking file authorization, paths, size limits, and existence. Textual summaries alone cannot replace required artifacts; manual changes to historical files are not checked. Subcells receive only experiment material explicitly authorized by the parent; full parent collection creates a local import record and `imported_record_ref`, while mathematical conclusions still require normal auditing.

New tasks automatically receive the experiment skill; existing tasks in the same format retain their instruction snapshots, without automatically overwriting custom AGENTS and research skills.

## Research Records and Routes

Save independent research objectives as Claims, whose mathematical core `proposition` is fixed after creation; changing assumptions, quantifiers, or conclusions requires a new ID. Changing a title or nonmathematical description produces only a metadata version under the same ID, and old audits remain bound to the original content. An Example stores a fixed construction or parameter family and stable property IDs; changing the construction requires a new Example, and changing a property's meaning requires a new property ID. A one-step equality or unformed idea need not be split into an independent object.

An Argument's `conclusions` identifies the targets it actually supports or refutes; `subject_refs` identifies objects under study, while `dependencies` identifies established premises used. Local audits verify targets and directions; Claim evidence status is derived from valid relationships and cannot be declared proved by the author. An external theorem may be saved with an accurate statement, source, and location and verified when applied, without storing or reproving its original proof; `cited` indicates only a verifiable citation, not a theorem proved locally.

Save related outputs together through `archive_result`, with temporary batch keys replaced by official references by the service. Failure leaves no partially valid batch, and retrying the same request does not duplicate objects. Read cross-record consistency and current trust status through Store/MCP; direct JSON reads are for contents only. See the [prover protocol](prover/protocol.md#records-and-audits) for specific record and invocation conventions.

`proof_state` stores current routes and precise proof obligations, while Attempts store research decisions. Refuting a required lemma blocks the route rather than satisfying a proof condition. After local lemmas pass, an argument connecting them to the overall objective is still necessary; revoked or conflicting evidence affects current completion judgments. When a key counterexample, failed connection, or changed assumption occurs, or when further investment is planned with an unchanged bottleneck, the main agent conducts a brief route review without automatically adding a review process or judging mathematical progress by output counts.

New tasks receive the current protocol and skills. Instruction snapshots, original records, and audits in runs of the same format are not automatically rewritten; new relationships cannot acquire certification solely from historical passing labels. Legacy storage formats cannot be resumed; existing runs in the current format retain records and cumulative usage and adopt the outer budget policy at safe resume boundaries. To study incompatible historical material, explicitly select it in a new run, save new records with clear provenance, and re-audit them.

## Files

The following paths are relative to the Colombo root:

```text
config.toml                         Defaults shared by Brain and Cell
requirements.txt                    Unified Python dependencies
run_cell.py                         Standalone Cell entry point
agents/cell/
├── prover/                         AGENTS.md, protocol.md, research Skills
├── upper_bound/                    Upper Bound instructions
├── lower_bound/                    Lower Bound instructions
├── verifier/                       Proof review and Report Checker instructions
└── shared/handoff/SKILL.md          Shared handoff guidance
src/colombo/cell/
├── controller.py                   Cell execution and research rounds
├── model_calls.py                  Model processes and isolated configuration
├── settings.py, recovery.py         Settings, handoff, and recovery
├── record_store.py, research_records.py, record_queries.py
├── mcp_server.py                    Prover MCP tools
├── subcell_dispatch.py, subcell_worker.py
└── verifier/
    ├── proof_review.py             Independent review and Report Checker
    ├── local_audit.py、challenge.py
    ├── mcp_server.py、review_validation.py
    └── schemas/                    Report and receipt JSON schemas
src/colombo/shared/                 File, process, budget, Experiment, and retrieval tools
tests/cell/                         Cell regression tests
```

Files in `agents/cell/` are guidance copied into task workspaces; MCP entry points and tool implementations reside in `src/colombo/cell/`. Full review is exposed through a local Python interface in `src/colombo/cell/verifier/proof_review.py`. Shared process-launch code is in `src/colombo/cell/model_calls.py`, with temporary configurations generated in `.runtime/cell/` at the repository root.

On Windows, file reading, writing, copying, and atomic saving handle extended-length paths through `src/colombo/shared/file_io.py`, while records still display ordinary paths. Atomic replacement uses short temporary filenames in the same directory rather than repeating the final filename; no registry modification is required. Read, directory-creation, copy, or write failures during audit preparation are saved as `service_error` with `error_stage` and `error_type`, and cannot promote or revoke mathematical certification. If the research library itself is unwritable, save errors are explicitly returned to the caller.

Call sequence:

1. `src/colombo/cell/controller.py` creates the task directory and copies the problem, AGENTS.md, protocol.md, and skills.
2. `src/colombo/cell/model_calls.py` generates an isolated Codex configuration and starts the main agent; research processes use `src/colombo/cell/mcp_server.py`, while verifier processes use `src/colombo/cell/verifier/mcp_server.py`.
3. The main agent selects skills independently and calls tool implementations in Cell and shared through the Prover MCP entry point.
4. The Prover's `src/colombo/cell/verifier/local_audit.py` starts new processes for local checks, and `src/colombo/cell/subcell_dispatch.py → subcell.py` starts new processes for parallel tasks. All model processes are launched through `src/colombo/cell/model_calls.py`.
5. The main agent writes `draft.md` and a ready `submission.json`, then exits. The submission contains `draft_file:"draft.md"`, `outcome:"proved"` or `"disproved"`, and optional `evidence_files`. `src/colombo/cell/controller.py` freezes current inputs through `src/colombo/cell/verifier/proof_review.py` and starts an independent verifier; saved submissions are checked even after an abnormal main-process exit or timeout, and no full review starts without a ready submission.
6. The first verifier uses `review-proof` to check actual proof steps and explain coverage; a new independent process uses `check-report` against the same frozen inputs to verify passing grounds, check coverage, and blocking findings. Disagreement returns to the first stage for report revision, followed by independent confirmation again; this process does not start the prover.
7. A confirmed report first synchronizes current record trust statuses, then determines whether to generate the final manuscript or return the work to the next prover round for revision. Each round resumes from files rather than continuing the preceding process's conversation. A verifier timeout passes work to the next verifier in the same stage; a prover timeout passes work to the next prover.

The Python runner handles overall scheduling; no Stop hook is registered. An ordinary exit means only that the process ended. Local audits generate historical `proved` / `checked` labels; reads must also check the current `current_trust`. The program returns 0, sets `accepted`, and supplies `manuscript.md` only after full review and independent confirmation pass, record synchronization succeeds, and submission identity, initial report version, and independent confirmation agree. Incomplete work or exhausted budgets return 2.

## Full Review

The verifier's instructions, skills, MCP tools, and report protocol follow this project's requirements and the user-supplied Mathematical Proof Checklist. It first identifies the complete objective, then checks proof dependencies and saves checks around actual assertions, key transitions, and citations. The original 30-item checklist helps identify omissions; it is no longer a form to complete item by item, and unused methods need no not-applicable records. Check numbers are assigned within each review as positive integers, without a continuity requirement or restriction to 1–30; reports must contain actual checks and explicit coverage explanations. An unused assumption is not automatically an error, a directly fillable omission is not automatically a gap, and failure to locate a citation does not automatically imply fabrication.

External theorems do not require storing their original proofs. The prover saves the statement used, conditions, locatable source, and application argument for the current problem; final citation information must appear in the draft or accompanying `evidence_files`, rather than remain only in prover memory. The verifier uses this to check the original statement, assumptions, and application; absence of a copied original proof is not itself a gap, but necessary grounds that cannot be verified remain unresolved.

Review tools are `record_check`, `record_source`, `read_review`, `lookup_sources`, and `write_report`. Each review has an independent workspace and stores checks, findings, and citation evidence in `review_notes.json`. Each check states `subject`, `location`, status, and grounds; source records link to actual checks through `check_id`. `write_report(verdict, summary, target_alignment, coverage)` assembles the complete `review_report.json` from saved records, without inventing assessments or omitting findings; `coverage` explains how those checks cover the original objective, key dependencies, and methods actually used. Tools and the final response transmit only a `review_id`, `report_revision`, and `verdict` receipt. Python reads the full report from its fixed location and verifies the receipt, record consistency, and frozen inputs; a receipt alone cannot establish acceptance.

By default, `read_review()` returns a summary of existing checks and IDs with findings; it does not infer unregistered mathematical obligations. Use `detail="full"` for reasons and source contents, optionally filtered by `check_id` and paginated with `offset` and `limit`; reread after records change during pagination. Independent confirmation must cover all actual check IDs submitted in the first stage and independently check for omitted key steps. This version accepts only new runs with storage_version=2; resuming the same run does not reset cumulative budgets.

Independent confirmation uses a separate workspace and `confirmation_notes.json`. It checks the first-stage conclusion, each blocking finding, and possible omissions, explicitly examining the original proof rather than only report format or wording. Disagreement with the first stage or discovery of a new error first produces internal findings, followed by first-stage report revision and renewed confirmation. Overturning an incorrect criticism in the second stage does not directly establish the original proof. Only confirmed `report.json` and `confirmation.json` become reports effective for the prover.

A submission may use `record_refs` to bind a draft `position` to a library `kind/id/revision`, with `property_ids` for Examples. The runner freezes the actual records, and audit findings distinguish record, application, and draft scopes. Only confirmed record errors revoke support from the corresponding evidence; merely misapplying a lemma does not revoke a correct lemma. Original records and local audits are retained, while `current_trust` dynamically reflects revocation, property scope, and blocked dependencies. Repairs require a new candidate, resolution of objections, another local audit, and explicit updates to downstream dependencies. Child snapshots and late-arriving results are also checked for invalidated parent evidence.

`reviews/index.json` stores the current stage and cumulative starts. `reports/pNNNN.json` stores first-stage report versions, and `checks/pNNNN/` stores their corresponding confirmations; timeouts retain the stage, partial checks, and handoff references. Resume prioritizes unfinished reviews and does not skip them even when prover starts are exhausted. Status is `pending_review` when review can continue within budget, and `review_incomplete` when counts are exhausted, frozen material is abnormal, or trust synchronization fails. Neither status sends provisional feedback to the prover for revision.

## Local Challenges to Arguments

A challenge is available when a specific concern arises during research; agents need not proactively traverse certified arguments to search for issues, and challenges are not mandatory every round, on each citation, or before submission.

The prover calls `challenge_argument(record_ref, reason, evidence_refs=None, request_id=None)` with the exact version of a certified Argument, a specific objection, and necessary evidence. The service first freezes the original argument and relevant material, setting the current status of affected evidence to `suspended`; historical `proved` labels and local-audit reports are retained. Downstream uses of old versions are also blocked; merely appending a candidate version cannot bypass this issue.

The first stage checks whether the objection holds; explicitly dismissing it lifts this suspension. If an error or substantive gap is found, a second independent process checks both the original argument and first-stage report, and support is formally revoked only after confirmation. If the second stage disagrees, revise and reconfirm within the local workflow before issuing any confirmed error judgment to the prover. Dismissing one challenge does not clear other unresolved challenges or confirmed revocations; revocation concerns argumentative support and does not mean that the proposition is false.

The local workflow is stored in `challenges/<challenge_ID>/`. Call `resume_argument_challenge(challenge_id)` to resume the original stage without resetting counts. Timeouts, insufficient material, or exhausted counts leave it unresolved and suspended; research independent of that evidence may continue. `[cell.settings.challenge]` limits cumulative starts per Challenge and Checker attempts per report version according to the current profile and config, without inheriting a run-wide research deadline. Increasing counts requires changing the root config and adopting it at a safe resume boundary; task-local configure cannot expand them.

An adverse local-audit result for a certified Argument also enters this workflow; ordinary unproved candidates retain the existing local-audit procedure. Challenges to read-only parent material in a subtask are returned to the parent task owning the records. Suspension/revocation affects parent assessments of snapshots and late-arriving outputs, but does not rewrite the contexts of all running child processes in real time.

## Time and Handoff

`budget_status` reports the current process's execution information, cumulative usage, policy revision, and configuration source. Neither Colombo Standard nor Hard imposes a run-wide research deadline; null remaining time means unlimited time, closing is false, and voluntary handoff remains available. Cell-local starts, review, Challenge, Experiment, and resource limits continue to apply.

The runtime still handles explicit process deadlines and legacy finite ledgers, but these do not define default Colombo research limits. Colombo descendants do not inherit stale run-wide deadlines left in old environments. Counts and usage persist on resume; infrastructure startup, locks, and network waits retain finite timeouts.

Long-running audit, challenge, and Experiment tools start jobs through MCP and return promptly. On `status="running"`, retrieve the original result with `job_status(job_id)`; do not treat pending as pass or resubmit the same experiment under another request ID. Uncollected work remains incomplete when the agent exits and cannot be submitted automatically for review. A disconnected worker may continue executing or be cleaned up with its process tree; interruption is reported explicitly without automatic repeated execution.

When a handoff is needed, save records under the shared Skill. Explicitly time-limited process recovery cannot extend its own deadline; with no available window, save the facts and record skipped status. Recovery packages are constrained by input/source byte and record limits without truncating original research archives. Brain's final integrate two-hour limit applies to a separate stage and is not a total countdown for Cell research.

## On-Demand Reading and Result Collection

By default, `archive` returns an ID, version, and trust status; complete contents remain in the library and can be read through `retrieve` at a fixed version, or explicitly requested with `archive(detail="full")`. Local audits still return findings without echoing the full audited proof again by default. Records append versions by ID and revision, and legacy storage formats are no longer compatible.

By default, `collect_task(task_id)` returns status, paginated output references, and counts without echoing the full history or final text. Use the returned `cursor` with `detail="full"` to reread that page, and `next_cursor` to advance or poll for new outputs; no server-side acknowledgment of consumed records is needed. Use `record_ref={kind,id,revision}` to read any complete evidence record, including historical dependencies, at any time. Add `include_result=True` when the final response is needed; its text appears only once. Reviews/events are omitted by default and may be explicitly selected through `kinds`. After selecting ordinary research outputs, explicitly request import with `import_refs=[fixed_child_record_ref]` and a stable `request_id`; `import_result` returns parent references, while ordinary pagination does not import the outputs automatically. The parent must re-audit imported outputs.

AGENTS retains only persistent constraints; current skills are loaded on demand, and shared conventions reside in `protocol.md`. `proof_state` stores routes, gaps, evidence references, and next steps; the handoff adds only the current stopping reason and resumption point. Operation logs are saved to files and not injected into model context by default. Both main tasks and subtasks receive the protocol file; it is added to old tasks when missing, existing custom instructions are retained, and the runner supplements the shared handoff skill. Pagination sizes follow the central retrieval parameters.

| Verdict | Meaning | Follow-Up |
| --- | --- | --- |
| `pass` | Applicable checks are complete, with no issues blocking acceptance | The runner generates the manuscript and saves version credentials |
| `revise` | A definite error, substantive gap, or source mismatch exists | Revise the draft or evidence and submit for review again |
| `inconclusive` | Necessary evidence or citations remain unverified | Supply evidence, restore source access, or continue verification without claiming that the proposition has been refuted |

Formatting errors, process failures, and inconsistencies between reports and records are execution failures and cannot become `pass`. Review attempts and original material are saved in `reviews/`; `verifier_max_rounds` limits the cumulative count of first-stage reviews, continuations, and revisions. Modifying the draft invalidates old manuscript credentials. Initial-review changes produce a new `report_revision`, and an old independent confirmation cannot apply to the new report.

In Jina Reader mode, `lookup` returns text extracted by the service; direct mode extracts HTML / text / PDF itself, traversing all PDF pages. `limit` controls only the number of search results, not text length or PDF page counts; individual downloads remain subject to the central limit, 12 MiB by default, and hitting it reports truncation or an error. Read coverage and warnings in reading results do not indicate that a theorem has passed applicability checks.

`tests/cell/` contains regression tests for configuration and the Proof—review loop, not runtime dependencies. Running the system generates `runs/`, `.runtime/`, and Python caches as needed; these are also not preinstalled runtime dependencies.

Regression tests (no real model or external network calls; MCP communication uses actual child processes, and HTTP reading uses a local test service):

```powershell
python -B -X utf8 scripts/run_validation.py --suite cell
```
