# Experiment Skills

Select by the current question; read only useful supporting resources. Shared execution and evidence rules are in the [protocol](../protocol.md), with the research loop in the [main agent](../agent.md).

| Skill | Use when | Optional executable example |
|---|---|---|
| [estimate-epsilon-rate](estimate-epsilon-rate/SKILL.md) | Estimate rate or parameter dependence for a fixed Algorithm, Algorithm search or empirical minimax competition; axes can include epsilon, N, d, kappa or sigma. | GD fixed instance, budget-matched family and epsilon-matched family. |
| [probe-mechanism](probe-mechanism/SKILL.md) | Investigate an intermediate quantity, inequality, construction or information mechanism and formulate a specific Proof question. | Numerical quadratic search followed by an exact rational candidate check. |
| [explore](explore/SKILL.md) | Existing results, constructions or implementation references would change the experiment design or interpretation. | Read supplied fixed materials and relevant Skill resources; use lookup for external sources. |

Examples do not constrain the candidate space. Reuse suitable implementations or adapt them in Task working files. Calibration and independent validation are proportionate to the scientific claim; fixed stage counts, parameter grids and repetitions are not required. Scenario instructions/code stay inside their Skill; actual measurements and reports stay in Task artifacts.

Experiment Cell exposes no live Memory reader: neither the retired recollect interface nor scientific_memory is available. Use the supplied fixed materials, installed Skill resources and lookup for external sources.
