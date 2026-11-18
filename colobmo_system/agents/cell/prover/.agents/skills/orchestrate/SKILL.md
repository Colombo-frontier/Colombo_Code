---
name: orchestrate
description: Assign distinct proof routes or independent subproblems to subcells for parallel investigation, select explicit context, stop competing routes within a group based on audit results, and collect outputs usable in the main proof.
---

# Orchestrate: Organizing Parallel Research

## 1. Objective

Use parallel work to resolve specific differences between routes or divide subproblems. Assess the completion of all tasks separately from completion of the mathematical objective. Locate material independently in the records; see the workspace [protocol.md](../../../protocol.md) for records, configuration, and parent-import rules.

## 2. Inputs: What to Read Before Starting

| Material | Reading Requirements |
|---|---|
| `problem.md` and, when present, `TASK.md` | Confirm the local research scope and deliverables that the current task may delegate. |
| Current `proof_state`, Claims, and Attempts | Locate differences between routes, independent subproblems, dependencies, and reductions not yet established. |
| Arguments, constructions, sources, and audits to be provided | Read the full evidence, assumptions, failure scope, and `current_trust`, then select the snapshots actually needed. |
| Task statuses and runtime configuration | Read existing tasks through `task_status`; query `configure` when concurrency, depth, and budget information is needed. |

## 3. Procedure: Dispatching, Collecting, and Stopping Tasks

### 3.1 Define Responsibilities and Context

Create or reuse a precise Claim for each assignment, stating its fixed target, assumptions, version, route, and completion criteria; do not use the overall objective's ID in place of distinct local propositions. Routes should differ substantively; when decomposing a problem, explain the dependencies and how subproblems connect back to the overall objective, retaining unestablished reductions as proof obligations.

Only routes with the same target, assumptions, version, and completion criteria may form a competing group. For example, three routes for A and two for B form two groups; a complete result for A affects only group A. Save the rationale for the division of work and grouping in the current Attempt, then add task IDs, outputs, and scheduling reasons later.

Use `spawn_task` to provide the target reference, task description, group identifier, and selected `context_refs`. Supply the definitions, assumptions, results, audit feedback, and relevant failure scope needed to understand and verify the task; a summary of conclusions alone is insufficient.

Determine the scale of dispatch according to current concurrency, depth, and budget, and query or adjust with `configure` when needed. Specify child settings through dispatch parameters; search is disabled for subcells by default, so offline tasks must include necessary source text and locations—a URL alone does not provide the text.

Each subcell uses its own workspace and authorized parent snapshots. No tool currently allows context to be appended to a running task; if a task returns because material is insufficient, collect its existing outputs before deciding whether to supply the missing material and dispatch it again.

If a subsequently confirmed audit revokes parent evidence that was used, snapshots and late-arriving results may be marked stale. Address affected dependencies first, stopping and redispatching when necessary; passing labels in old snapshots cannot bypass the parent library's current trust status.

### 3.2 Retrieve Complete Outputs as Needed

Use `task_status` to inspect execution status and `collect_task` to inspect output summaries and paginated references. Retain returned cursors to continue reading new pages; retrying the same cursor does not skip that page. Full audit and event records are not loaded by default; explicitly select them when needed.

Retrieve complete fixed-version records by relevance using `record_ref`, or paginate through their contents with `detail="full"`; set `include_result=True` only when the final response is needed. There is no need to wait for all tasks to finish, but mathematical conclusions cannot be accepted from summaries alone.

Verify the targets, assumptions, and dependencies addressed by the outputs, then select useful content for import into parent records, preserving full arguments, sources, and provenance. Use service-returned parent references to connect targets, constructions, properties, and evidence; do not infer correspondence from titles or identical IDs. Existing parent snapshots map back to their original identities, while propositions newly created by children receive new parent identities. Re-audit in the parent under the protocol; child passing labels cannot be adopted directly.

Explicitly import ordinary outputs through `collect_task(task_id, import_refs=[fixed_child_record_ref], request_id="current_import_identifier")`, and use the parent references returned in `import_result`. Reading summaries or contents is not importing; keep the request identifier and inputs unchanged on retries. See the [protocol](../../../protocol.md#related-record-archiving-and-explicit-imports) for related-record archiving and import formats.

Collect saved derivations, examples, and obstacles even from tasks that were blocked, exhausted their budgets, or were canceled. Explicitly mark anything that could not be retrieved as uncollected; do not infer its contents.

### 3.3 Stop Other Routes in the Same Group After Auditing

When a route returns a proof or refutation, first assess whether it meets the group's complete completion criteria. A local lemma, a result under additional assumptions, or a counterexample to a sufficient condition may advance only part of the work.

Only after the Arguments and Example properties needed to judge completion pass audit in the parent should `cancel_task` stop the remaining routes in the same group; then collect their saved material. Cancellation does not mean those routes failed mathematically; other independent groups continue running.

If a result changes another group's dependencies, explain the effect and let the main agent decide scheduling. Refuting a lemma required by this route blocks the route; it does not discharge that obligation. If supporting and refuting evidence conflict, retain and recheck both; do not select a conclusion or declare completion based on arrival order.

## 4. Constraints: Scheduling and Certification Boundaries

- Do not infer completion of a mathematical objective from task exits, completion counts, or child passing labels; re-audit imported candidates in the parent.
- Do not place work with different targets, assumptions, versions, or completion criteria in the same competing group; stopping one group does not automatically terminate other independent groups.
- A subcell uses only its own workspace and authorized `context/`; it does not read ancestor or sibling directories. Snapshots do not automatically update when parent material changes later.
- Save, import, and cancel through tools; do not directly modify shared records, task statuses, or service reports.

## 5. Outputs: Connecting Back to the Main Proof

Place useful derivations, constructions, sources, and assertions to be proved in the corresponding records, reusing service-confirmed references to the same objects; do not merge different mathematical content merely because it appears similar. Save current routes and outstanding connection obligations under the protocol; even after all local results pass, an Argument connecting them to the overall objective is still required. Importing or compression cannot upgrade evidence status.

Update each task's outputs, status, audits, cancellation reasons, and uncollected work in the Attempt. Distinguish inadequate decomposition or reduction, mathematical obstacles, insufficient context, audit failure, and execution causes; all routes in a group being blocked does not imply that the target is unprovable.

Return a concise summary and expandable record references, identifying solved objectives, objectives with only candidates or partial progress, and what the overall proof still lacks. The main agent updates the overall state accordingly; copying the full logs is unnecessary.

Retain this use of `skill`, `decision_reason`, and task IDs still requiring attention in the Attempt. When a handoff is needed, use `$handoff` to record dispatched tasks, collected evidence, and subsequent actions; a handoff does not imply cancellation of children.

## 6. Relevant Record Objects

Read parent and child records through their respective local services and task tools; after import, use the fixed parent references returned by the service.

| Object (Collection or Runtime Object) | Use and Read/Write Behavior at This Stage | Entry Point |
|---|---|---|
| Claim `claims` | Register or reuse the precise fixed target of each subtask. | References from the current objective or `proof_state`, and archiving receipts. |
| Attempt `attempts` | Store the division of work, competing groups, skill selection, task IDs, scheduling reasons, and collection status. | Current Attempt reference or `retrieve`. |
| `proof_state` | Read routes and obligations; the main agent maintains the overall state using collected results. | `retrieve(kinds=["proof_state"])`. |
| Subtasks and authorized context snapshots | The service creates execution tasks and selected versions in `context/`; read statuses through task tools. | Task ID returned by `spawn_task`, and `task_status`. |
| Child outputs and parent import mappings | Select fixed child versions and explicitly import the required records and dependencies, preserving provenance. | Paginated references, `record_ref`, and `import_result` from `collect_task`. |
| Argument `arguments`, Example `examples`, Source `sources` | Import or save useful outputs; parent Arguments begin as candidate/partial and Example properties as pending, and are re-audited. | Parent references returned by `collect_task` or archiving receipts. |
| `experiment_result` and experiment files | When relevant, collect facts and evidence through the experiment service's separate import workflow; do not present this as an atomic cross-file write within an ordinary batch. | `imported_record_ref` and artifact references in collection receipts. |
| `reviews` | Read parent local-audit results and current certification grounds; maintained by the service. | `audit` receipts and fixed record references. |

## 7. MCP Tools Used

Invoke tools according to scheduling needs; see tool definitions and `protocol.md` for complete dispatch, pagination, and import parameters.

| Tool | When to Call | What It Reads or Produces |
|---|---|---|
| `retrieve` | When locating parent targets, evidence, and current trust status. | Local records and authorized context; it does not traverse child directories. |
| `archive` / `archive_result` | When saving targets, an Attempt describing the division of work, connecting arguments, or the main agent's proof_state. | Fixed individual or related-batch records and reference mappings. |
| `configure` | When querying or necessarily adjusting the current task's configuration. | Settings such as concurrency, depth, and allowances, plus an explanation of their effects; child settings are specified through dispatch parameters. |
| `spawn_task` | After the local target, deliverables, and authorized material are specified. | A new subcell, task ID, and selected context snapshots. |
| `task_status` | When determining which tasks are still running or have returned. | Execution status; it does not automatically accept outputs or prune routes. |
| `collect_task` | When reading summaries, fixed contents, or subsequent pages, or explicitly importing selected outputs. | Child output references; with `import_refs` and a stable `request_id`, it produces parent import results. |
| `audit` | When a complete Argument or Example property imported by the parent must serve as evidence. | Parent local audits and certification status, used to judge completion and stop routes in the same group. |
| `cancel_task` | After the group's full criteria are met and the required evidence passes audit in the parent. | A cancellation request for the specified task; collect saved material afterward. |
| `budget_status` | When assessing time for collection, auditing, and handoff. | The current time allowance; use `$handoff` when a handoff is needed. |
