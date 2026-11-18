---
name: experiment
description: When a proof lacks a promising direction or a related conjecture or pattern needs exploration, use sampling, enumeration, strategy testing, or simulation to seek counterexamples and proof insights; preserve actual computational results, then return to research. Also use when the user explicitly requests an experiment.
---

# Experiment

Use concrete examples to examine conjectures, test strategies, observe evolution, or discover patterns that inform the next proof step. The current agent designs and interprets the experiment; keep simple examples within the current reasoning, without routinely checking every Claim or requiring all proof routes to be exhausted first.

## Inputs and Objectives

Read `problem.md`, `TASK.md` when present, the current `proof_state`, and relevant Attempts; read the target Claim / Example, relevant Arguments, and existing `experiment_result` records as needed. Use `retrieve` to locate relevant current records and fixed versions, avoiding duplication of coverage already obtained.

Specify the question, the assumptions that must be retained, the inputs that may vary, and what you hope to observe. Exploration is allowed before a complete conjecture exists; do not force the creation of a Claim. `target_ref` links an existing Claim, Example, or saved Attempt; all record refs use `{kind, id, revision}` from actual receipts.

## Available Methods

The following uses can be combined; completing every item is not required.

| Purpose | Main Approach |
|---|---|
| Equality | Evaluate both sides on the same admissible input, observe the residual, and retain discrepancies. |
| Inequality | Sample or search inputs satisfying the assumptions to find violations and examine cases close to equality. |
| Geometry | Retain the construction in the problem, vary free points, and check properties such as collinearity, concyclicity, and concurrency; plots may assist inspection. |
| Strategy | Execute the strategy across different instances, initial states, or opponent responses, and observe successes, failures, and their trajectories. |
| Simulation | Given an initial state and evolution rules, observe behavior such as trajectories, terminal states, and cycles. |
| Pattern discovery | Use counting, classification, plotting, and parameter sweeps to explore patterns in structure, scaling, thresholds, distributions, and symmetry / invariance. |
| Construction | Search for or adjust candidate objects. Retain this entry point; specialized construction methods for Hard Instances and Algorithms will be added later. |

## Design and Execution

Start with a small-scale experiment to check that generated examples satisfy the assumptions and that the computation corresponds to the original problem. Specify the sampling / enumeration method, parameters, precision, applicable seeds, and results to preserve. Expand or adjust the scope only when further computation is valuable; also consider different scales, boundary cases, and special configurations.

Check a discovered pattern against new examples or parameter ranges; when a suspected violation appears, verify assumptions, implementation, and numerical error. For Strategy and Simulation, retain trajectories that explain the results as needed. Use `recollect` / Explore as needed when existing knowledge can assist design or calibration; adopt only material whose applicability has been checked.

Save `skill`, `decision_reason`, and `experiment_decision` in the Attempt. When choosing to execute, set `decision="run"` in `experiment_decision` and include `target_ref`, `question`, `outcome_actions`, and `scope_and_stop`. `outcome_actions` describes how results will affect subsequent research; it need not predict what will be discovered. For an explicit deferral, use `defer` and record `target_ref`, `reason`, and `reconsider_on`; when judged unhelpful, use `not_useful` and record `target_ref` and `reason`. Do not document a rejection reason for every route.

Execute through the existing tool:

```text
run_experiment(question, target_ref, code, request_id,
               parameters=None, input_files=None, attempt_ref=None)
```

`attempt_ref` links the current Attempt; `input_files` uses only relative paths authorized for the current Task. The Python script may read `PARAMETERS` and `INPUT_FILES` and write outputs to be retained into `OUTPUT_DIR`. Check `budget_status` before execution; permissions and resource limits follow [protocol.md](../../../protocol.md#experiment-records-and-evidence).

When `running` and a `job_id` are returned, use `job_status(job_id)` to collect the original result. Use `resume_experiment(experiment_id)` when remote execution or downloading associated with an existing `experiment_id` needs recovery. Retain the same `request_id` and inputs for the same request; changing the code or parameters defines a new experiment. Do not silently switch to local execution after an execution failure.

## Results and Information Flow

Interpret results only after reading the actual code, output, and execution status. Clearly distinguish execution failure, no violation found, a pattern discovered, and an inconclusive result.

| Object | Content to Save |
|---|---|
| Attempt (`attempts`) | Why the experiment is being conducted, its design, scope and stopping conditions, effects on the research, and subsequent actions. |
| `experiment_result` | Execution facts, references to code / inputs / artifacts, and `observations`, `limitations`, and `derived_refs`. |
| Example (`examples`) | A concrete construction, parameter family, special configuration, or counterexample candidate worth further study or reuse, together with its properties. |
| Claim (`claims`) | A conjecture with an explicit `proposition`, retaining all assumptions, quantifiers, and scope. |
| Argument (`arguments`) | A complete or partial derivation actually obtained, the evidence used, and remaining gaps. |
| `proof_state` | The current route, remaining questions, fixed references to relevant records, and next steps. |

The execution service creates `experiment_result`. The agent only supplements or revises `observations`, `limitations`, and `derived_refs` through `archive`, using the actual ID and `expected_revision`; it does not rewrite execution facts.

Keep code, raw data, plots, and trajectories in the experiment artifacts. Do not create an Example for every sample; extract only research objects worth referencing independently. Keep patterns that are not yet explicit in `observations` / the Attempt, and create a Claim once an explicit `proposition` is formed. Save only Examples, Claims, and Arguments actually produced, link their sources using fixed refs, and link derived outputs in `experiment_result.derived_refs`. When changing a Claim's mathematical content or an Example's construction, create a new object under the protocol; do not overwrite the original target to accommodate samples.

Computations actually used as proof evidence should appear in the `dependencies` of the corresponding Argument or Example property, with an explanation of the numerical values, errors, and coverage used. Passing samples does not prove a universal Claim; a counterexample candidate requires verification of every assumption and confirmation through exact computation or reliable error bounds. Complete finite enumeration or computation with rigorously controlled errors can provide proof material, but its coverage and logical justification must still be stated. Example properties requiring certification and complete Arguments undergo `audit` under the protocol; the service maintains `reviews` and trust status.

## Returning to Research

Add the actual fixed `experiment_result` reference to `Attempt.experiment_decision.experiment_refs`, and explain what was found, which conjecture / strategy it affects, and what should next be proved, revised, or abandoned.

Update the relevant references, remaining gaps, and next steps in `proof_state`, without copying the experiment contents. Return to proof work once useful insights have been obtained or further computation has no informational value; an inconclusive result is an acceptable endpoint.

When execution or downloading remains incomplete, save the `job_id` / `experiment_id`, existing artifacts, and pending state, and use the handoff to resume the original execution. A subcell uses its own authorized material; after collection, the parent uses the service-returned `imported_record_ref`, and importing does not automatically certify mathematical conclusions. See [protocol.md](../../../protocol.md#experiment-records-and-evidence) for complete record, recovery, verification, and delivery rules.
