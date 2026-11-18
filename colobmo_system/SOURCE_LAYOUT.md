# Source Code Responsibilities

This table documents the current implementation. See README.md for the workflow and agents/ for role instructions. All paths below are relative to `src/colombo/`.

The root-level `run.py` calls `system_commands.py`, which starts research through the Brain Controller; Brain starts `cell/worker.py` through `cell_dispatch.py`. `run_cell.py` is a separate entry point for users to launch Standalone Cell directly; Brain need not go through that command file.

## System and Brain

| File | Responsibility |
|---|---|
| system_commands.py | Parse run/config/status/resume/mcp commands |
| configuration.py | Load configuration, expand presets, validate, and fix Oracle mode |
| project_paths.py | Define project, source, and instruction paths |
| brain/controller.py | Coordinate plan → Result Verifier → update/prune → integrate |
| brain/model_calls.py | Formal model calls, receipts, and call recovery |
| brain/task_execution.py | Task queue, concurrency, formal Result registration, and recovery |
| brain/cell_dispatch.py | Prepare and launch Cell processes; verify execution and stop receipts |
| brain/record_formats.py | Current Task/Setting/GoalProgress/ProofDraft/review formats |
| brain/submission_validation.py | Validate submissions, scope, pinned references, and Claim consistency |
| brain/mcp_server.py | MCP tools, role permissions, and parameter adaptation |
| brain/research_store.py | SQLite transactions, fixed references, and run recovery |
| brain/research_records.py | Research object layout, Task/Wave queries, and JSON/status exports |
| brain/cell_package.py | Create pinned, self-contained packages and resolve all local dependencies |
| brain/cell_evidence.py | Read a specified version of evidence from a returned attempt |
| brain/proof_draft.py | Save, resolve, and render complete ProofDrafts |
| brain/final_report.py | Submit Conclusions and export final reports |
| brain/evidence_audit.py | Independent audit requests, execution, pinned results, and recovery |
| brain/pruning.py | Check Pruning relations, premises, and target responsibilities |

`record_formats` describes formats, `submission_validation` checks submissions, and `research_store` performs authoritative transactions; mathematical correctness remains the Verifier's responsibility. The active workflow schema defines the current data contract.

## Cell and Experiment Cell

| File | Sole Responsibility |
|---|---|
| cell/controller.py | Research rounds and result-return workflow for ordinary Cells |
| cell/worker.py | Independent Cell process entry point dispatched by Brain, and Result receipts |
| cell/model_calls.py | Cell model processes, isolated home, and handoff lifecycle |
| cell/settings.py | Cell settings, validation, locking, and managed settings |
| cell/instructions.py | Specialization and instruction identity |
| cell/recovery.py | Handoff, pinned recovery materials, and resumed execution |
| cell/diagnostics.py | Read Cell diagnostics and exception information |
| cell/attempt_archive.py | Immutable ZIP/inventory for each formal return |
| cell/mcp_server.py | Prover MCP tools and role permissions |
| cell/subcell_dispatch.py | Subcell creation, concurrency, and result collection |
| cell/subcell_worker.py | Independent Subcell execution entry point |
| cell/record_store.py | Versioned writes and transactions for Cell records |
| cell/research_records.py | Claims/Arguments, dependencies, pinned references, and trust |
| cell/record_queries.py | Retrieve Cell records and relations according to permissions |
| cell/record_formats.py | Cell MCP input formats and record constants |
| cell/verifier/proof_review.py | Manuscript review, Report Checker, and authority updates |
| cell/verifier/local_audit.py | Audit local Cell records |
| cell/verifier/challenge.py | Challenge workflow for Challenge Reviewer and Report Checker |
| cell/verifier/review_validation.py | Format and reference validation for review/confirmation/conclusion |
| cell/verifier/mcp_server.py | Cell Verifier MCP tools |
| experiment_cell/controller.py | Execution, reports, and results for independent empirical Tasks |
| experiment_cell/mcp_server.py | Experiment Cell MCP tools |

Cell's former runner and prover/mcp business modules have been moved to the files above according to responsibility. settings and configure were merged; handoff and recovery were merged; records and references were merged; the two sets of review format validation were merged. Cell's Store, records, and queries have distinct responsibilities and remain separate.

## Independent downstream Agents

`run_pipeline.py` is an independent entry point that provides a one-way handoff through existing exports. Brain/Cell do not handle downstream scheduling, configuration, or state storage. See `docs/DOWNSTREAM.md` for full usage instructions.

| File | Sole Responsibility |
|---|---|
| downstream/handoff.py | Validate Brain exports in read-only mode; freeze Proof, Setting, and selected source materials |
| downstream/launcher.py | Read the separate downstream.toml and hand off sequentially to Lean Agent → Writing Agent |
| downstream/model.py | Independent native model processes and replay records shared by the two Agents |
| lean_agent/agent.py | Formalization, repair from compiler feedback, and independent statement correspondence review |
| lean_agent/compiler.py | Run the actual Lean compiler and check declarations and axioms |
| writing_agent/agent.py | Validate the Lean result and generate manuscript sources, a Claim map, and editorial gaps |

Lean/Writing each have their own instruction pack, working directory, and run records; they do not import Brain/Cell modules or call their MCP or Store. The former Brain postprocess hooks, phases, configuration, and Skills have been withdrawn; the reused compiler was moved to `lean_agent/`.

## Shared Implementations

| File | Sole Responsibility |
|---|---|
| shared/file_io.py | Path, atomic write, JSON, immutable files, and OS file locks |
| shared/process_control.py | Process identity, Windows Job, process tree termination, and receipts |
| shared/model_launcher.py | Shared preparation of CLI discovery and model cache/catalog |
| shared/runtime_budget.py | Usage ledger, deadlines, and remaining budget calculations |
| shared/tool_jobs.py | Background tool launch, polling, and result collection |
| shared/literature_access.py | External literature search and source reading |
| memory/contracts.py | Shared scientific objects, pinned references, and review format validation |
| memory/store.py | Read-only access to the current text in the four libraries and the external state directory |
| memory/retrieval.py | Execute overview/browse/search/read/expand using existing derived indexes |
| memory/mcp_adapter.py, memory/integration.py | Register builtin scientific_memory and restrict research role permissions |
| memory/cli.py | Command entry points for the five read-only retrieval operations |
| shared/experiment_execution.py | Experiment execution, quotas, deduplication, recovery, and result collection |
| shared/experiment_artifacts.py | Path and manifest validation for Experiment code/data/artifacts |

Brain and Cell retain their respective call lifecycles and share only implementations that are actually identical. Callers explicitly specify configuration precedence, lock timeouts, and file formats; the distinct return contracts for epoch and monotonic deadlines remain unchanged. Experiment execution receives an explicit ExperimentContext and does not locate other Cell workspaces on its own.

## Entry point compatibility

The Cell prover/verifier MCP executable wrappers forward to the current servers. They contain no separate research implementation. Protocol/storage versions and instruction identities remain explicit data contracts.

## Independent Memory Agent

The nested `colombo_memory_agent/` uses `src/colombo/memory/` from its parent system. It owns Curator/Reviewer execution and trusted publication tools; Brain and proof Cells only read scientific Memory. Both components share the same paired library and state directories.

The final completion modules validate exact final-review bindings and append corrected progress/conclusion records without rewriting earlier scientific records.
