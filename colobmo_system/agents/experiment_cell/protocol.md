# Experiment Cell — execution and evidence contract

The [main agent](agent.md) selects methods from [Skills](skills/README.md). This contract defines shared information, execution and submission boundaries; scenario details belong in their Skill.

## Fixed research contract

Reuse the assignment's Setting. Record only necessary experimental additions: the estimand and quantifiers, admissible Function Family/Algorithm Class/Oracle, allowed public inputs and Output, Metric and risk, Resource accounting, parameter path and actual coverage. Disclose conditional branches instead of silently changing the question.

Randomized Algorithms, stochastic Oracles and instance generation have distinct randomness. For a fixed-budget expected-error target, estimate each fixed Algorithm–instance pair's risk before taking the specified max/min. Choose the instance before private Algorithm/Oracle randomness is realized. An adaptive adversary requires explicit permission in the Setting. Simultaneously restricting Algorithm and instance pools generally gives neither a certified Upper nor a certified Lower Bound for the full minimax problem.

Expected norm, expected squared norm, high-probability accuracy, expected stopping cost and deterministic query cap are different targets. Evaluator information may measure the result but cannot become extra Algorithm feedback. Separate Algorithm cost from evaluator/search compute.

## Tools and recovery

The independent Experiment MCP exposes lookup, run_experiment, resume_experiment, retrieve, budget_status, job_status and submit_report. Follow their actual schemas. In Colombo, src/colombo/experiment_cell/controller.py manages the empirical lifecycle and mcp_server.py exposes these tools; agents need not read installation source.

Experiment Cell exposes no live Memory reader: neither the retired recollect interface nor scientific_memory is available. Use the supplied fixed materials, installed Skill resources and lookup for external sources. The retrieve tool reads immutable local research records; it is not a live Memory reader.

- run_experiment binds the real fixed target_ref automatically. Supply a recoverable request_id; do not invent or change the Task target.
- Check available budget before execution. Separate native research starts from hosted experiment runs and Algorithm query budgets.
- A running result with job_id is collected through job_status. An existing remote execution or incomplete download is recovered with resume_experiment(experiment_id).
- Repeated request IDs retain identical code, parameters and input bytes. Resume reuses the original execution and does not replenish its quota. Changed inputs require a new request.
- Use service records for execution facts and artifact locations. Failed or unknown execution cannot be replaced by an expected curve or an unreported local fallback.

## Skill code and artifacts

Skill instructions, references and scripts are installed into the Task's skills/ and .agents/skills/ from one source. Use skills/<name>/scripts/... for example execution; do not maintain two edited copies. To adapt an example, copy it to Task working files and execute the changed file as a new input.

Pass each required script or dependency through run_experiment(input_files=[...]). Uploaded names may end in .bin; use the INPUT_FILES mapping, not assumed remote filenames or package directories. The self-contained examples export run(parameters, output_dir):

```python
import runpy
module = runpy.run_path(INPUT_FILES["skills/estimate-epsilon-rate/scripts/gd_family_calibration.py"])
module["run"](PARAMETERS, OUTPUT_DIR)
```

Do not set run_name="__main__" for this invocation: the scripts' main blocks provide a development CLI. Explicitly upload any extra dependency if adapting them. Production research uses the existing hosted executor; local deterministic execution is for development tests.

Preserve code/input snapshots, dependency versions, actual parameters, seeds where applicable, query counts, raw measurements, failures and analysis. Keep run-specific outputs in Task artifacts, not Skill source. Read downloaded outputs through the actual receipt/artifact mapping; their local names may also differ from logical output names.

Label analytic reference values, actual Algorithm rollouts, numerical searches and exact/interval checks separately. A source formula is not proof that a rollout occurred. A high-precision approximation alone is not an error certificate. Relevant plots must reflect preserved measurements.

## Submission and adoption

Use submit_report(report, body) for Markdown report.md and empirical_report.json. The report contains text summary, actual_scope, method, uncertainty; lists measurements, candidate_rates, limitations, failures; fixed experiment_refs with {kind,id,revision}; and permitted local artifact_paths.

outcome is observations or inconclusive, never proved. Observations require an actually completed execution, measurements and artifacts. Inconclusive reports explain the limitations and whether the original Task's completion criteria are met. Collect pending jobs before submission. The Markdown report explains the finding, evidence, actual scope and next useful research action; a mechanism Task can leave candidate_rates empty.

The submission receipt and returned Result have evidence_kind=empirical, accepted=false: this preserves their distinction from local Proof acceptance. The existing outer Result Verifier evaluates scientific reliability and Task completion. A reliable inconclusive finding may receive review pass; that does not solve the mathematical Goal.

Review pass, Task completion, execution success and mathematical certification are separate. Empirical findings can motivate candidate rates, constructions or Proof tasks, but do not certify Bounds, mathematical refutations or checked Proof steps. Computations may later support a Proof Cell's explicit argument with appropriate certificates and the existing mathematical review.
