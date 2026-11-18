# Experiment Skill evaluation fixtures

`cases.json` contains neutral public assignments and input files. `rubrics.json`
is evaluator-only and must never be copied into researcher workspaces. Cases are
development/behavioral evidence, not mathematical certification. S03, S04, S07
and S08 start as held-out variants; any exposure or use to revise instructions
invalidates that designation for later runs.

The harness freezes fixtures and both instruction bundles before research starts.
It launches the existing Cell worker, hosted executor and outer Result Verifier.
It does not grade by matching words in researcher prose. The independent review
must supply criterion-level judgments with actual evidence paths. Missing grades,
unverified read traces and infrastructure errors never become held-out passes.

## Running the approved batch

From the Colombo root, after the candidate pack is final:

```powershell
python -B scripts/evaluate_experiment_skills.py --help
python -B scripts/evaluate_experiment_skills.py prepare --codex-bin C:/path/to/native/codex.exe
python -B scripts/evaluate_experiment_skills.py run --live --key candidate-S01
python -B scripts/evaluate_experiment_skills.py run --live
python -B scripts/evaluate_experiment_skills.py summarize
```

Preparation freezes 8 candidate and 4 baseline assignments, the complete code
snapshot, both instruction packs and evaluation config. The real baseline must
be the captured pre-change pack; offline unit tests use a synthetic temporary
baseline so they do not depend on excluded historical validation directories.
Each run has one fixed Task/attempt. It uses production `TaskExecution.run_job`,
Cell worker, hosted execution/recovery and archive export. The current safe
runtime is shared by baseline/candidate; only researcher instruction packs differ.
All reports use the same frozen candidate outer Verifier plus evaluator-only
criterion guidance. The researcher never receives that guidance.

S01 and S02 additionally invoke the actual Brain `process_results` stage with its
existing Store, fixed Result review, Setting, assignment and task snapshot. Its
MCP server is the existing server with `audit`, `job_status` and `lookup` removed
for this adoption-only call. It keeps `read_research`, `read_material`,
`record_results`, notes and read-only retrieval. No scheduler/plan/integrate call
is run, and no new research, nested audits or Pruning is authorized. The update
records experimental responsibility separately from the still-open mathematical
Goal. The wrapper does not modify production server behavior.

The runner never replaces a failed/unknown review or Brain update. A restart can
recover an already committed original receipt; otherwise the call stays incomplete.
The batch stops at an infrastructure/unknown error so an operator can inspect it.
Use an explicit different authorized `--key` to continue unaffected cases.

`summarize` is read-only and reports grades, usage and unfinished calls. Researcher
trace extracts are in `traces/<key>.json`; full JSONL logs stay in the Task. After
examining actual reads, a human may record `read-audits/<key>.json` with `status`
(`clean`, `contaminated` or `unknown`), `reviewer`, `reason`, and `inspected_logs`
(the exact relative-path-to-SHA256 map returned by summarize as `required_logs`).
Missing, stale or incomplete audits remain unknown. A clean audit does not
establish filesystem isolation; it records review of the observed trace. Only a
passing held-out variant with such a completed audit counts as held-out success.
