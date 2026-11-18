# Cell Record and Execution Protocol

## 1. Scope and Basic Conventions

This protocol applies to the prover and subcells in the current workspace, using `storage_version=2` and research-collection `schema_version=2`. Legacy storage formats are rejected without migration. See `AGENTS.md` for role entry points and read the current skill as needed for research methods. This file defines record, tool, and state constraints; the current MCP interface is authoritative for complete parameters and return structures.

Manage records using IDs, revisions, and explicit references; normal interfaces append versions rather than overwrite history. File paths are relative to their owning workspace, and evidence is read only under explicit authorization. The system does not detect direct modification of historical files that bypasses the interfaces.

## 2. Record Objects and References

### Records and Audits

When first saving or reusing material, establish object identity from this section, then consult the [reading rules](#3-reading-and-access-rules), [tool interfaces](#4-tool-and-submission-interfaces), and [trust status](#audit-promotion-and-current-trust) as needed.

| Collection | Content Stored |
| --- | --- |
| claims | A fixed mathematical `proposition` and its sources; do not copy the proof or assign proved status yourself |
| arguments | Complete or partial derivations, conclusion directions, actual premises, and specific gaps |
| examples | Fixed constructions or parameter families, individual properties, and their computational or argumentative grounds |
| attempts | Route execution, skill and selection reasons, outputs, and failure scope; route reviews and experimental decisions when needed |
| experiment_result | Execution facts for one experiment, code and artifact references, observations, limitations, and subsequent outputs; the service maintains execution facts |
| sources | Bibliographic identifiers and versions, original-source locations, actual reading coverage, and applicability conditions |
| proof_state | Current routes, remaining obligations, relevant record references, and next steps; revisions retain the same ID |
| reviews | Local audits and confirmed corrections from full reviews, maintained by the service |
| events | Operational events, maintained by the service |

A fixed research reference is `{kind,id,revision}`; include `property_ids` when selecting Example properties. Obtain IDs and versions from save receipts or retrieval; do not guess them or substitute identically named objects. `conclusions` states the targets actually supported or refuted by an argument, `subject_refs` identifies the objects under study, and `dependencies` identifies the premises actually used.

Create or reuse a precise Claim for an independent, complete prove/disprove objective or a proposition to be delegated or studied across rounds. Its `proposition` includes definitions, assumptions, quantifiers, scope, and conclusion and cannot change after creation; any change to mathematical content, including added assumptions, changed parameter ranges, or a formula correction that changes meaning, requires a new ID. `title`, nonmathematical `notes`, sources, and provenance may be updated through revisions, but mathematical conditions must not be hidden in these fields. An old proof does not automatically prove a new proposition; a source relationship is not a proved implication or equivalence. After a metadata-only update under the same ID, old evidence still references the original version and remains discoverable when querying the same fixed proposition.

Store the full statement of an external theorem in a Claim and its source in a Source. A Claim may use `citation:{"source_refs":[fixed_Source_reference],"locator":"theorem number, section, or page"}` to identify a verifiable source; retain the bibliographic identifier or URL, applicable version, and actual reading coverage. The derived status `cited` means only that a verifiable citation exists, not that there is a local proof or completed source verification. An application Argument for the current problem should reference that theorem and any necessary sources; the audit verifies the statement, source, satisfaction of assumptions, and derivation of the conclusion, followed by independent verification by the verifier. Storing or reproving the external theorem's original proof is unnecessary; search summaries cannot replace verification against the original text.

Create or reuse an Example when a construction is specified to test an assertion, rule out a route, or enable later reuse. The construction and parameter domain are fixed; changes to formulas, key structure, or allowed ranges require a new Example, retaining variant provenance. Valid values within a declared parameter family may be specified through fixed parameters without recreating the entire family for each value. Being a positive example or counterexample is a relationship to a precise Claim, not a permanent label on the construction.

Create records according to actual outputs, without splitting ideas merely to populate every type. A one-off equality within an Argument may remain there; keep ideas that are not yet explicit in an Attempt and extract them once they become independent objectives. State gaps in the corresponding argument steps; record failed attempts in an Attempt, identifying whether a construction, method, or reduction failed and distinguishing mathematical obstacles from budget exhaustion, cancellation, and tool failures. One failed attempt does not prove a target false.

### Routes and Decisions

`proof_state` is the recovery entry point; it stores only current routes, precise targets, obligations, material references, and next steps, without copying proof contents, review history, or operation logs. Revise it when first establishing a route and whenever routes or obligations change; save the current state before a handoff. Subsequent processes follow references to full evidence rather than continuing a proof from summaries alone.

When decomposing an objective, use `routes` to save stable `route_id`, `target_claim_ref`, and `obligations` values. Each obligation uses a stable `id` to reference an exact `target_claim_ref`, and may include `owner_attempt_ref`, relevant `evidence_refs`, a `remaining_gap` explaining the obstacle, and `closing_argument_ref`. `expected_relation` defaults to `supports`; use `refutes` for tasks intended to establish the negation. When target assumptions or conclusions change, create a new Claim and obligation ID, retaining the supersession relationship rather than silently changing the meaning of the old obligation.

When a key counterexample, failed connection, or change in core assumptions occurs, or when further investment is planned despite an unchanged bottleneck, write a brief `route_review` in the relevant Attempt: triggering evidence, what was resolved, the unchanged bottleneck, reasons for continuing, switching, or deferring the route, and the next check that can distinguish routes. The same attempt may be revised, but a substantive change in objective or method requires a new Attempt; proof_state references only the current version. Use `progress_delta` to identify added or refuted propositions, discharged obligations, and precisely excluded scopes; organization, re-auditing, and execution recovery do not constitute new mathematical results. Do not mechanically cancel routes based on round counts, Argument counts, or pass counts.

Save `experiment_decision` only when a computational question has actually been considered, explicitly deferred, or its reassessment conditions have changed; not every route needs a “no experiment” entry. `run` records `target_ref`, `question`, `outcome_actions`, and `scope_and_stop`; `defer` records the target, `reason`, and `reconsider_on`; `not_useful` needs only the target and reason. Add `experiment_refs` after actual execution; explain why a run decision was not executed rather than presenting it as completed. When returning to the relevant Attempt, carry forward still-valid defer decisions and let the current agent assess whether conditions have changed; natural-language reassessment conditions are not triggers already determined to be satisfied by the program.

### Experiment Records and Evidence

The `target_ref` in `run_experiment` may link an existing Claim, Example, or saved Attempt; put the specific computational question in `question` and link the current Attempt through `attempt_ref`. For Pattern discovery and Simulation without an explicit proposition, do not force a Claim solely to satisfy the execution interface. Save actual experiment refs in `Attempt.experiment_decision.experiment_refs`.

The execution service saves the question, target reference, parameters, actual execution status, code and input copies, environment, remote identifiers, and local artifact manifest. Use `archive` to revise an existing record's `observations`, `limitations`, and `derived_refs`; these fields alone may be submitted with the ID and `expected_revision`. Do not create experiment records, rewrite execution facts, or change a service report to success. In observations, distinguish exact symbolic results, finite-enumeration results, floating-point behavior, and your own interpretation. Successful execution means only that the computation completed.

The Attempt explains why the experiment is conducted, how it is selected, and when to stop; `experiment_result` stores what that specific computation actually produced. Put conjectured conclusions arising from it in Claims, concrete constructions and properties in Examples, and rigorous derivations in Arguments; connect them using fixed-version references, while `proof_state` states only how they affect the current route. A separate local audit is not required for every experiment; Example properties and complete Arguments still undergo audit under the existing protocol.

Retain code, raw data, plots, and trajectories as experiment artifacts; extract into Examples only concrete objects worth independent study or citation, rather than creating a record for each sample. Keep patterns that are not yet explicit in observations / the Attempt; extract a Claim only when an actual proposition has formed. `experiment_result.derived_refs` links Examples, Claims, or Arguments actually produced, without requiring every experiment to produce them.

Include experiment records used as proof evidence in the `dependencies` of derived outputs, identifying the actual values, ranges, errors, or coverage arguments used. Local audits and final verification collect local files from experiment manifests through explicit dependencies or selected `record_refs`; a `target_ref`, a filename mentioned in prose, or a cloud link alone does not deliver evidence. The text must still explain why the computations support the claim; artifact paths cannot replace an argument. When experiments support the final proof, identify corresponding draft locations in the `record_refs` of `submission.json` and explicitly include any other necessary files in `evidence_files`.

Provide experiment material to subcells through authorized snapshots; a subcell may use experiment tools for its local objective. After collecting experiment results, the parent uses the returned `imported_record_ref` rather than references to child directories; imported computational facts do not automatically make parent Examples or Arguments trusted. Hosted computation and web search have separate switches; disabling search does not prohibit experiments. Retain execution errors and choose subsequent actions without silently switching to local computation; the service reads API keys, which must not be written into code, prompts, records, or handoffs.

### Markdown formula formatting

In Markdown artifacts, delimit formulas with `$...$`, `$$...$$`, `\(...\)` or `\[...\]`; use code spans for literal plain-text expressions. Bare `[expression](expression)` is a Markdown link and can be mistaken for a file dependency. Keep real local file references as Markdown links and include their evidence files. This is a formatting convention, not a change to mathematical content or verification.

## 3. Reading and Access Rules

Records reside in the current workspace's `memory/`; absence means no material has yet been saved. Use `retrieve` to locate current versions or read fixed versions, or read JSON contents as needed. Read cross-record relationships and trust status through the service rather than assembling a presumed simultaneous state from independent file reads. Historical labels in raw JSON do not include derived current trust status; before reusing evidence, use `retrieve` to check `current_trust` for the corresponding version. Do not load the entire history at once.

A subcell reads only local records and authorized `context/` snapshots. Subsequent parent modifications do not synchronize automatically; during collection, the service compares initial and current trust statuses. Known incorrect material may be explicitly selected as repair input, but cannot serve as a trusted premise. Directory and tool conventions do not provide operating-system-level isolation.

### Target-Based Reading and Incremental Omission Checks

`retrieve` supports keyword queries and fixed ID/revision reads; specify `target_ref` for related material, and use `relations` to select `supports`, `refutes`, `attempts`, `subjects`, or `uses`. Here, uses denotes only actual recorded dependencies, not relationships to objects under study. Relation receipts distinguish author declarations, audit status, and current usability. A Claim with metadata-only changes can retrieve evidence for the original version; a new Claim does not inherit it automatically.

Query current gaps with `route_id`, optionally adding `state_filter={"domain":"obligation","value":"unresolved"}`. `mathematical` filters mathematical results; `work` filters work status; `trust`, `payload`, and `execution` filter current trust, stored labels, and execution status, respectively. Different filters must all hold, while multiple values within a list are alternatives. Obligations appear in the returned `obligations`, with a fixed reference to their source proof_state.

Use `since_event={"scope":"current_workspace","stream":"memory","sequence":previous_sequence_number}` to inspect changes across rounds. This returns only direct writes or audit facts in that memory event stream; it does not include all indirectly affected evidence and is not a measure of mathematical progress. `detail="summary"` returns concise summaries and fixed references; read full contents when the argument text is needed.

Use the returned `cursor` for the next page and `page_cursor` to retry the current page; supplying only a cursor retains the original filters. Page membership is fixed, and new writes appear in the next query; current_trust is rechecked on every return, so status may no longer satisfy the original filter. Changes to authorization scope invalidate old cursors. An object with property_ids is a view of selected properties; the record reference still points to the complete fixed source version, and property_ids selects only the properties permitted for use. Use service snapshots for cross-record relationships and validity; direct JSON access is for reading contents only. Current context JSON retains the complete source record to verify the original version; property_ids restricts service responses, further authorization, and evidentiary use, but does not provide property-level file confidentiality.

## 4. Tool and Submission Interfaces

The table below describes each interface by purpose, prerequisites, inputs, returns, state effects, and failure/replay behavior; details appear in the corresponding subsections and MCP definitions. Process startup and tools with usage limits follow the existing task configuration.

| Tool | Purpose and Prerequisites | Key Inputs | Returns | State Effects | Failure and Replay |
|---|---|---|---|---|---|
| `retrieve` / `lookup` | Read authorized records; external queries require search to be enabled. | Fixed references or query conditions; URL. | Records/pagination cursors or source contents. | Reading does not confer certification. | Replay cursors within the original scope; no external request is made when search is disabled. |
| `archive` | Save candidates or revise fields you may write. | kind, payload; add ID and expected_revision for updates. | ID, revision, current trust; full may include contents. | Appends a record version. | Version conflicts are rejected; replay with request_id must preserve the original inputs. |
| `archive_result` | Save related outputs together. | records, request_id; see the format below. | A mapping from local_key to fixed references. | Atomically saves ordinary research records without certification. | Replays the same request with identical inputs; changed inputs or any conflict are rejected. |
| `audit` | A complete Argument exists, or Example properties need checking. | kind, record_id, revision; optional property_ids. | Audit findings and record receipts. | The service promotes passing records; an adverse reassessment of a certified argument enters the challenge workflow. | fail/uncertain/service_error do not promote records; repeated calls start new audits, so read existing feedback first. |
| `challenge_argument` / `resume_argument_challenge` | A specific concern about a certified Argument; resume with the original challenge ID. | Fixed record_ref, reason, optional evidence and request_id; or challenge_id. | Status, reports, and effects on trust. | Suspends evidence; revokes support after independent confirmation. | Unresolved matters are neither certified nor declared false; the same request resumes with original inputs and accumulated counts. |
| `run_experiment` / `resume_experiment` | Experiments are enabled and there is a clear computational objective. | question, target_ref, code, request_id; optional parameters and files; or experiment_id. | Execution status, experiment record, and artifact references. | Saves execution facts without upgrading mathematical certification. | Identical requests recover the original execution; do not resubmit when the submission outcome is unknown; see Section 6 for recovery rules. |
| `spawn_task` | A precise target, explicit local requirements, and authorized material. | target_ref, instructions, context_refs; optional subtask settings. | Subtask identity and status. | Creates an independent workspace and execution. | No request_id deduplication; do not redispatch because a result was not received—check status first. |
| `task_status` / `cancel_task` | Inspect an existing subtask or cancel execution that is no longer needed. | task_id; may be omitted only when task_status queries all tasks. | Current status or cancellation-request status. | Only cancel_task requests cancellation; saved research is retained. | Terminal tasks do not restart; cancel_requested does not mean the process has ended. |
| `collect_task` | Read child outputs; import requires explicit selection. | task_id, pagination/record_ref; add import_refs and request_id for imports. | Output pages, fixed records, or parent import_result. | Ordinary reads do not import; imports become parent candidates. | cursor rereads the current page, next_cursor continues; imports replay the original request. |
| `configure` | Query or adjust this task's parameters; changes require a reason. | settings_overrides/search_enabled, reason. | Changes and when they take effect. | Updates this task's configuration, not the user's root configuration. | Invalid parameters are rejected; processes do not start automatically and accumulated counts do not reset. |
| `budget_status` / `finish_handoff` | Check time, or save unfinished work and end this process. | Queries take no parameters; handoffs provide summary, pending, next_steps, and necessary references. | Budget status or a handoff receipt. | A handoff saves a recovery entry point without a mathematical verdict. | Remaining time is null when no time limit applies; handoff and recovery do not reset budgets. |

### Long-Term Memory: scientific_memory

By default, Prover and Subcell read the current Memory through the builtin `scientific_memory(mode, arguments_json)`. It supports overview/browse/search/read/expand, does not depend on the external search switch, and does not authorize browsing other Cell workspaces. No tool parameter can change the Memory root. See `.agents/skills/scientific-memory/GUIDE.md` for complete examples.

The runner freezes the current Cell's research_mode, specialization, and instruction version; generic still permits only theorem records. Search cards, match checks, and leads do not prove applicability; do not expand permissions by fabricating ref.kind. Explicitly set include_leads=true to discover candidates; an empty published-only search does not prove that no relevant method exists.

A complete Memory ref is `{id,kind,revision,content_hash,tier}` and cannot be used as a retrieve/archive record ref. In read, offset/limit are measured in characters, with a default limit=10000 and a maximum of 20000; continue with next_offset when complete=false. Freeze selected statements, scopes, source locators, and content hashes through the existing Source/Claim/Argument workflow; applications/transfers still require review. The Verifier reads only a fixed package. Old Recollect refs are retired and cannot be guessed or rewritten as new refs; historical frozen material retains its original identity.

### External Sources: lookup

In `lookup(query="", url="", limit=None)`, query uses Serper search by default and URL uses Jina Reader by default; URL takes precedence when both are supplied. `limit` controls only the number of search results and defaults to the configured value when omitted. In the outer `cell.settings.network` configuration, `search_provider` may be serper/arxiv and `reader_provider` may be jina/direct; the existing compatible theorem search service remains available through configuration. The service reads API keys; do not place them in queries, Sources, or runtime snapshots.

Search returns discovery metadata and snippets; URL reading returns retrieved contents, source, provider, reading time, and truncation or access limitations. Jina Reader's converted output does not guarantee that every formula is complete; the direct reader extracts all readable PDF pages. Neither full-text reading nor Source registration establishes that a theorem has been verified. Cell lookup does not archive automatically: follow [explore](.agents/skills/explore/SKILL.md) to save useful Sources, actual read coverage, and locators; new insights may remain in an Attempt, with assumptions and applicability checked before use as proof grounds.

When search is disabled, requests are rejected before HTTP access; timeouts, authentication failures, or no readable content return errors, not evidence that no relevant result exists. Read existing fixed Sources locally first; another lookup is a new external request and does not guarantee the same version.

### Related-Record Archiving and Explicit Imports

Save or revise through `archive`; updates require the original ID and `expected_revision`, and history is retained. Use `archive_result` below for related outputs, including only actual outputs; if any item is invalid or conflicts in version, the entire batch is rejected, and partial writes are not treated as success. The execution service creates `experiment_result`; only its interpretation fields may be supplemented or revised through `archive`, as described in [Experiment Records and Evidence](#experiment-records-and-evidence). Receipt IDs and versions support subsequent reads and audits; rereading solely to recover the contents just submitted is unnecessary.

`archive_result(records, request_id, detail="summary")` accepts a set of record operations, each with a `local_key` unique within the batch and an `op`:

| op | Other Fields |
| --- | --- |
| `create` | `kind`, `payload`; a new `record_id` may be specified |
| `update` | `kind`, `record_id`, `expected_revision`, complete `payload` |
| `reference` | `ref`, referencing an existing fixed record without revising it |

A new or updated `payload` may reference another item using `{"local_key":"key_of_another_item_in_this_batch"}`, optionally with valid `property_ids`; existing material may also be referenced directly by fixed references. Do not handwrite IDs or versions not yet assigned by the service. Returned `refs` maps local_key to official references; `records` contains receipts by default, with complete contents returned only for `detail="full"`. This entry point saves records and does not replace subsequent local audits of candidate Arguments or Example properties.

First inspect and select ordinary subtask outputs through `collect_task`, then explicitly call `collect_task(task_id, import_refs=[fixed_child_record_ref], request_id="current_import_identifier")`. `import_result` returns parent references and mappings; use those references for subsequent saving and auditing. Preserve the request identifier and selected versions when retrying the same import; ordinary pagination or reading contents does not request an import. Import only outputs actually needed by this task and their authorized dependencies, rather than copying the child library's entire history by default.

The import plan is saved in the subtask's `imports/`, and the service saves source-to-parent ID mappings in `import-map.json`. Retries replay the original plan without resetting version requirements; if parent records have been concurrently revised, explicitly report the conflict and use a new request to make a new selection. When properties from the same fixed child Example version are selected in separate imports, the parent library retains the same construction identity, appends new properties, and preserves existing parent certification. Experiment execution records and files follow the experiment service's separate import steps and are outside the cross-file atomicity guarantee for ordinary record batches.

### Runtime Parameters

`configure()` queries the current task configuration; `detail="full"` returns the complete snapshot. Only non-budget changes such as model/search are permitted, and a reason is required. All time limits, counts, concurrency, MCP/HTTP timeouts, token caps, and file caps are set only in the outer configuration. `spawn_task(settings_overrides)` likewise cannot modify budgets. The runtime reads the resolved policy; adopting a new configuration on resume does not reset consumed allowances.

Colombo has no run-wide research deadline. `budget_status` provides read-only usage, policy revision, and execution information for the current Cell; a null time remaining means unlimited time, not exhaustion. Limits on Cell-local process starts, review/Challenge/Experiment counts, and resources still apply and do not reset on resume. Infrastructure timeouts and explicit process-recovery boundaries are handled separately and must not be used to introduce a run-wide research deadline.

Long-running audit/challenge/Experiment tools may first return `status="running"` and a `job_id`. Use `job_status(job_id)` to obtain the original final result; pending must not be treated as pass. Worker interruption reports only an execution issue and provides neither a mathematical conclusion nor an automatic repeat of a paid request.

### Main Task Submission

This section defines the main prover's file-submission interface; the runner writes back results after review. See [Full Review and Acceptance](#full-review-and-acceptance) for formal acceptance conditions. Subcells use local-output collection.

The final Argument for a complete proof or disproof first undergoes a local audit; then write the full objective, necessary derivations, and sources in a self-contained `draft.md`. A disproof must negate the complete objective of the original problem; merely refuting an auxiliary proposition or a particular argument does not justify a disproved submission.

At the beginning of the draft, clearly state the mathematical proposition, assumptions, scope, and conclusion; retain an independently readable proof and its sources in the body, without copying runtime allowances, scheduling, or tool-operation instructions. After review passes, `manuscript.md` retains the reviewed draft verbatim and adds brief review information. The complete `problem.md` is still frozen unchanged so that the initial review and confirmation can check every original task responsibility.

Write `submission.json`:

```json
{"status":"ready","outcome":"proved","problem_file":"problem.md","draft_file":"draft.md","evidence_files":[],"record_refs":[]}
```

Use `outcome:"disproved"` when the original problem is false. No separate files are needed for necessary evidence already included in the draft; use paths relative to the current run directory for other evidence. After saving, end the round and let the Python runner start the verifier; a full review does not start without a ready submission.

The `run.json.required_review_files` specified at initialization is the fixed set of mandatory evidence; the runner freezes it together with the current `evidence_files`. Do not change this list through configure or ordinary resume. It is empty for independent Cells when unspecified. Missing required files are reported as an input issue before any review starts or review count is consumed. An original material catalog indicates sources only; reviewers use the current `review_input_manifest.json` to confirm files actually received.

For external theorems actually used in the final proof, state the theorem used, its conditions, specific source, and application location in the draft; these details may instead be placed in a file listed in evidence_files and referenced in the manuscript. Do not provide only internal Source/Claim IDs or leave source details in unselected memory records: the verifier receives the original problem, draft, explicitly attached evidence files, and material frozen through `record_refs`. The theorem's entire original proof need not be attached; the verifier independently checks the original text and application using the source location, accessing it online when necessary.

`record_refs` maps draft locations to fixed library-record versions actually used: each entry includes `position`, `kind`, `id`, and `revision`; add `property_ids` when using particular Example properties. The runner resolves and freezes these references for verifier checks. This enables accurate distinctions between errors in records themselves, application errors, and affected dependencies; library conclusions cannot be changed on natural-language similarity alone. The self-contained proof must still be written in the draft.

## 5. State and Relationship Constraints

### Audit Promotion and Current Trust

Save an Argument with `status:"candidate"` or `"partial"`; once complete, call `audit` for its ID and version. The audit checks declared conclusion targets, directions, and coverage individually; on passing, the service generates a new `proved` version and an `audit_id`. Proving the negation of the original target also produces a proved Argument. A Claim's `current_trust` is derived from valid, explicit evidence relations as `proved`, `refuted`, `conflicted`, or `unresolved` and cannot be declared directly by the author. When a conflict appears, retain both sides' evidence, stop treating the obligation as complete on that basis, and use the existing review channels. An Argument without an explicit conclusion relation cannot certify a Claim solely through a historical passing label.

An Example records properties individually in `properties`, for example `[{"id":"p1","statement":"...","basis":"calculation or argument","status":"pending"}]`. Use a new property ID for each new property; substantive changes to the statement or scope of an existing property also require a new property ID, retaining the old property. Claims that premises hold, a conclusion holds or fails, or a construction satisfies the quantifiers needed for a counterexample all require audits. `audit` may check all properties or selected `property_ids`; the service changes passing properties to `checked`. When extracting a new Example from an audited Argument, do not copy its audit_id to the new object; save it as pending and audit its properties as needed.

An Argument may also explicitly support specified `property_ids` of an existing Example through `conclusions`; the audit then binds each construction, property, and argument. The service displays valid support in the property's `current_trust`, without silently changing the original pending label to checked or copying the Argument's audit_id. A prior audit that does not explicitly cover that property cannot provide this certification.

Re-audit affected parts after changes to assumptions, derivations, constructions, properties, or dependencies. Read `current_trust` from receipts or `retrieve`; it reflects whether the fixed version is currently usable. Historical `status`, `checked`, and `audit_id` remain unchanged and do not establish current usability. A record whose support has been revoked must be revised into a new candidate and locally audited again after addressing objections in the confirmed report; an old audit_id or changed ID cannot restore the original evidence's authority. An affected dependency means only that current support is insufficient, not that the conclusion is false; repaired dependencies also require explicit updates to downstream fixed versions and re-auditing. When a correct lemma is misapplied in a draft, repair only the application rather than declaring the lemma itself wrong.

An audit may include suggestions about missing record registrations; a registration omission is not a mathematical error, and suggestions confer neither proof nor certification. The main agent registers necessary outputs after confirming the target and construction statements. Absence of omission-check results does not mean that checks were performed and found nothing; when budget is insufficient, save pending tasks rather than starting a new omission-check model during the closing stage.

When saving outputs not sent for audit, check whether any objectives or constructions need independent registration; do not launch a separate model every round for this purpose. Save unprocessed omission-check suggestions in the corresponding Attempt and reference them from proof_state. For omission checks across rounds, query incremental material using the memory event sequence number from the previous check; events only help locate new content and do not automatically determine mathematical omissions.

When importing subcell outputs, preserve provenance to the subtask and original version, and consistently map targets, constructions, properties, and actual dependencies. Parent-authorized snapshot references map back to the original parent records; new child propositions receive new identities rather than being merged by identical IDs or similar titles. Parent Arguments start as candidate/partial and Example properties as pending; remove child trust labels and audit_id, then audit in the parent. Summaries, renumbering, and child audits cannot upgrade the parent records' evidence status.

Example revocation is property-specific and does not automatically revoke other independent properties. Changing a title, source, or ID cannot erase the same erroneous argument; after repair, audit the substantively changed candidate again.

### Route Completion and Evidence Relations

`work_status` describes work status such as active work, deferral, or abandonment; mathematical results and satisfaction of route requirements are assessed separately. Proving a lemma false may answer the investigation of that lemma while blocking a route that requires it to hold. Nonempty `evidence_refs`, completed subtasks, or answers to all subproblems do not imply that the parent objective is proved; an Argument connecting those results to the parent objective is still required. After certification is revoked or evidence conflicts, do not retain the old completion display.

`proof_state.routes[*].obligations[*].work_status` accepts only these strings: `active`, `pending`, `paused`, `suspended`, `cancelled`, `abandoned`, `superseded`, `completed`. Omission is interpreted as `active`, but save requests do not automatically insert the field; use `active` for work in progress, not `in_progress`. These enums constrain only ProofState obligations, not extension fields of the same name in Attempts.

Minimal route example (first replace `C1` with an actual Claim reference; batch archiving may also use a same-batch `{local_key: "target"}`):

```json
{"routes":[{"route_id":"R1","target_claim_ref":{"kind":"claims","id":"C1","revision":1},"obligations":[{"id":"O1","target_claim_ref":{"kind":"claims","id":"C1","revision":1},"expected_relation":"supports","work_status":"active"}]}]}
```

`route_id` is unique within the ProofState, and an obligation's `id` is unique within its route. The service computes `mathematical_state`, `satisfaction`, `satisfied`, and `current_trust`; do not include them in obligation inputs.

### Full Review and Acceptance

The first-stage report takes effect only after confirmation by a new independent process. If confirmation rejects it or identifies new issues, revise and reconfirm findings within the verifier first. Only a finally confirmed `pass` permits acceptance; `revise` indicates a definite error or substantive gap requiring actual repair and resubmission; `inconclusive` indicates necessary evidence remains unverified and must be supplied, not that the proposition is false. Timeouts and execution failures pass to the next verifier to continue review, not to the prover to change mathematical content. Do not resubmit unchanged after mathematical rejection; during revision, read the confirmed report and current record trust statuses, repair the issues, and set ready again.

The runtime verifies submission identity, report version, and current trust status before generating accepted status and `manuscript.md`; a normal exit or file existence alone does not indicate a pass. Main-process rounds and full-review counts have separate budget limits; retain unfinished work when limits are reached. A subcell does not use this submission protocol and returns only local outputs to its parent.

The initial review and independent confirmation bind to the same `review_id + report_revision`. Revising the initial review creates a new report version, which an old confirmation cannot certify. Local challenges likewise bind findings and independent confirmation through `challenge_id + report_revision`.

## 6. Exceptions and Recovery

### Challenges and Revocation

This channel is available when a specific concern already exists; it is not a routine task. There is no requirement to search for issues or initiate a challenge every round, on every record reuse, or before submission.

When studying or using material, a specific concern about the reasoning, assumptions, or calculations in a certified Argument may be raised through `challenge_argument(record_ref, reason, evidence_refs=None, request_id=None)`. The reference includes `kind`, `id`, and `revision`; the reason identifies the concerning step and potential consequences, with saved counterexamples or other evidence when necessary. You need not first determine independently that the argument is wrong. Challenge only that version of the argument; do not equate an erroneous argument with a false proposition. Do not substitute a new candidate version for revocation of the old certification.

The service freezes the original argument, necessary dependencies, and selected evidence, and first suspends use of the challenged evidence. The first stage examines the objection; if it finds an error or substantive gap, an independent process then checks that assessment against the original argument. Support is formally revoked after both rounds confirm. If the second round disagrees, revise and recheck within the local audit workflow first, rather than treating provisional findings as instructions for the prover to revise. When a challenge is explicitly dismissed, only its suspension is lifted; other unresolved challenges or confirmed revocations remain effective.

When an unfinished state is returned, resume the original stage with `resume_argument_challenge(challenge_id)`, retaining the original inputs and consumed counts. Records whose `current_trust` indicates suspension or blocked dependencies cannot serve as proved evidence; work independent of them may continue. Timeouts, exhausted counts, or insufficient evidence leave the matter unresolved, without automatic rejection or restoration of certification. Record the challenge ID, state paths, and follow-up matters in `proof_state` or the handoff. Additional attempts require the user to change the root config, adopted at a safe resume boundary; do not rewrite workflow state.

To repair a revoked argument, save a substantively revised candidate and run a new local audit; downstream arguments using the repair must also update their fixed-version dependencies and be re-audited. Retain the original argument, original local audit, and revocation grounds. If a subtask finds an issue in read-only parent material, save a specific objection and return it to the parent task; the task owning the record initiates the challenge.

### Experiment Recovery

The `experiment_result` collection corresponds to `memory/experiment_result.json`. `run_experiment` creates a hosted execution and record; `resume_experiment` resumes that same execution or download. A repeated `request_id` recovers the original execution; use a new `request_id` when changing code or parameters or adding computation, and reference the previous result in the Attempt. Execution failures, timeouts, and failure to discover a pattern are distinct and cannot substitute for one another.

Recover remote execution using the experiment ID, nonce, and response/file ID. Retain file manifests, path authorization, size limits, and missing-artifact checks; incomplete downloading does not mean the experiment is complete, and an unknown remote submission outcome must not trigger automatic resubmission.

### Budgets and Handoff

`budget_status` queries this process's remaining working time and closing window; near the limit, save existing progress under `$handoff` and call `finish_handoff`. Closing work and one necessary read-only organization pass are included within the original time limit. The next prover reads a prover handoff; verifier handoffs remain with the next verifier in the same stage, and do not cause unconfirmed feedback to be sent to the prover. Process counts accumulate across resumes; increasing budgets requires changing the root config, and restarting alone does not reset counts.

### Requests and Failure Handling

Write and execution requests with request_id save their actual inputs and receipts; replay preserves those inputs, with necessary JSON comparisons distinguishing booleans from numbers. Do not bypass unresolved execution by changing the request ID. On error, first determine whether it concerns parameters/permissions, a version conflict, a mathematical assessment, or a process failure, then use the corresponding tool or handoff entry point. Execution failure, cancellation, timeout, and exhausted allowances cannot constitute evidence that a proposition is false.
