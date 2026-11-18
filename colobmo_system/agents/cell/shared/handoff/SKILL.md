---
name: handoff
description: Save a resumable handoff when budget_status reports closing time or the process must stop before completing its task.
---

# Handoff: Saving a Resumable Handoff

## 1. Objective

When the budget enters its closing window or work must end early, save completed work, unresolved matters, and the precise resumption point for the next process in the same role and stage. A handoff confers neither proof nor review certification.

## 2. Inputs: What to Read Before Starting

| Material | Reading Requirements |
|---|---|
| Current budget | Call `budget_status` to confirm the role, stage, actual remaining time, and whether the closing window has begun. |
| Current task and saved progress | prover/subcell reads the task, existing research records, and `proof_state`; verifier reads the frozen inputs specified in `review_request.json` and the notes for this stage. |
| Unfinished external operations | prover/subcell locates the actual IDs, requests, statuses, and saved evidence for experiments or Argument challenges awaiting recovery. |
| Previous handoff (when resuming) | Read the existing handoff report and distinguish completed items, checks still pending, and resumption points. |

Read files using the current workspace's access method, and research and review records using the MCP tools for this role; do not assume that all roles have the same tools.

## 3. Procedure: Saving the Handoff

### 3.1 Confirm the Conditions for Concluding

Call `budget_status` to check the running process's actual deadline. Its reserve is already part of the process budget. Once closing begins, finish saving the work in progress and call `finish_handoff`; do not start another proof route, lookup, experiment, or subagent.

With `time_limit_enabled=false`, deadline and remaining-time fields are `null`: there is no time cutoff, not zero time remaining. Do not invent a closing deadline. You may still use `finish_handoff` when an explicit handoff is needed, giving the actual stopping reason.

### 3.2 prover / subcell Saves Research Progress

For a prover or subcell, save useful partial arguments and attempts in the existing memory records, and update `proof_state` with fixed target references, the current route, unresolved obligations, and relevant evidence. A refuted required lemma blocks that route; it does not satisfy its proof obligation or refute the overall problem. Keep unfinished arguments unfinished. This is a navigation handoff, not another memory collection.

Link still-relevant deferred experiment decisions and their reconsideration conditions in the current Attempt. The next research process judges whether those conditions changed; a new round alone does not require an experiment. Preserve necessary registration or audit tasks without starting a new review or extraction process during closing time.

For an unfinished experiment, include its experiment ID, request ID, saved artifacts and unresolved execution or download state. The next prover or subcell calls `resume_experiment` for that ID before considering a new run; an unknown remote outcome is not permission to submit the same computation again.

For a pending Argument challenge, include its challenge ID, frozen input and state paths, current phase and remaining issue. Resume it with `resume_argument_challenge`; keep affected evidence suspended until the service resolves the challenge. An unconfirmed objection or a timeout is not a mathematical rejection.

### 3.3 verifier Saves Checks for the Current Stage

For a verifier, save the checks and evidence actually completed in `review_notes.json` using the review tools. In the report-check stage, call `save_confirmation_notes` to save `confirmation_notes.json` instead. Leave unexamined checks and unresolved disagreements open. Do not fill missing checks, issue a review receipt, or decide pass merely to satisfy a final-output schema. The next verifier resumes the same frozen input and stage; a timeout report is not feedback to the prover.

## 4. Constraints: Requirements During Handoff

- After entering the closing window, save only existing work; do not start new routes, searches, experiments, subtasks, or audit workflows.
- Unfinished proofs and checks remain unfinished; unconfirmed objections, timeouts, cancellations, or a single blocked route cannot become mathematical conclusions.
- Leave recovery identifiers for unknown remote execution states; do not resubmit the same computation with a new request.
- Save locations and references must actually exist. Use the existing record system rather than creating another research memory; save file contents and evidence through the existing tools.

## 5. Outputs: What to Submit and When to End

Then call `finish_handoff(summary, pending, next_steps, references, stopping_reason="budget")`. Use existing file paths and record IDs in `references`; state exactly where work stopped and what remains to be checked. The runtime adds the process ID, role, stage, input version, elapsed time, and effective budget windows. It stops this process after the handoff is committed, so save records before this call. No completed proof or review result is required for this exit.

If the process is killed first, Python writes a factual handoff and may ask a fresh, restricted process to summarize saved evidence within the remaining budget. That process cannot reconstruct unsaved reasoning or make a mathematical decision.

## 6. Relevant Record Objects

| Object or File | Use and Read/Write Behavior at This Stage | Entry Point |
|---|---|---|
| Research records: Argument, Attempt, `proof_state`, etc. | prover/subcell saves valid partial derivations, the current route, proof obligations, and fixed references. | Records returned by `retrieve` and the workspace `memory/`; write with `archive`. |
| Experiment records and execution artifacts | Record the experiment ID, request ID, saved outputs, and unfinished execution/download state; do not alter execution facts saved by the service. | Existing `experiment_result` and tool-returned status/artifact paths. |
| Argument challenge | Record the challenge ID, frozen input, state paths, current stage, and remaining objection, keeping relevant evidence suspended. | Original challenge tool receipts and saved state files. |
| First-stage checks and sources | In `stage=proof`, save completed checks and their grounds using the review tools. | `review_notes.json`; inspect with `read_review`. |
| Report-confirmation notes | In `stage=report_check`, save incomplete assessments with `save_confirmation_notes`. | `confirmation_notes.json`. |
| Handoff report | `finish_handoff` saves progress and resumption information; the runner adds the process, role, stage, input, and budget identities. | Returned `handoff_path`, located in `handoffs/`. |
| Factual handoff after forced termination | The runner generates it from saved information, adding a restricted summary when necessary; unsaved reasoning cannot be recovered. | Runner-generated handoff report and recovery summary. |

## 7. MCP Tools Used

| Tool | Role and Invocation Conditions | What It Reads or Produces |
|---|---|---|
| `budget_status` | All roles supporting this skill, before beginning a handoff. | The current process's actual budget and closing status; unlimited-time mode does not mean zero time remaining. |
| `retrieve` | prover/subcell, when locating existing research records. | Record summaries, fixed references, or required full contents; see the role's protocol for parameters. |
| `archive` | prover/subcell, when saving existing partial work. | Updates research records and `proof_state`, preserving incomplete status and correct version references. |
| `record_check`, `record_source` | The verifier's proof stage, when saving checks or source verifications actually completed. | Checks, issues, and grounds in `review_notes.json`. |
| `read_review` | The verifier's proof stage, when confirming saved progress. | Summaries or paginated contents of existing review records. |
| `save_confirmation_notes` | The verifier's report_check stage, when saving incomplete confirmation work. | `confirmation_notes.json`; it does not confirm the report. |
| `finish_handoff` | All roles supporting this skill, after necessary records have been saved. | A handoff report and exit receipt; the current process then ends. |
| `resume_experiment`, `resume_argument_challenge` | Reserved for the next prover/subcell round; state existing IDs and recovery requirements in the handoff. | Resumes the original operation, rather than starting new work during the current closing stage. |

Use this table according to role and conditions. A handoff must not call `write_report` or `write_confirmation` to fabricate a conclusion; submit a fully completed review according to its corresponding review skill.
