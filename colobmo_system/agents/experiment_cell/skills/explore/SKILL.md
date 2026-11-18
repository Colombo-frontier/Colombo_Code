---
name: explore
description: Find existing results, Algorithms, Hard Instances, calibration cases, or experimental methods for the Experiment Cell's current question; read supplied fixed materials and Skill resources as needed, use lookup to search and read external sources, and check how they apply to the current experiment.
---

# Explore for experiments

## Objectives and Triggers

Use when existing knowledge can help construct candidates, calibrate measurements, explain phenomena, select the next batch of experiments, or determine whether a rate conjecture is already resolved. Consult it before, during, or after developing your own construction; the Library does not restrict the candidate space, and a complete literature review is not required for every Task.

Start from the assignment, Setting, current question, and material already read. Retrieve only the information currently needed: for example, whether there is a known rate under the same Oracle, a transferable hard construction, a reliable calibration case, or an explanation of an observed crossover.

The current method Skill's `references/` and `scripts/` may provide scenario instructions, analytic references, and executable examples. Read the resources needed for the current problem and check scope, parameter path, Oracle, and Metric; do not load all cases. For actual execution, upload fixed script input according to the [protocol](../../protocol.md) and execute through the `INPUT_FILES` mapping. Copy resources to Task working files when modifications are needed; reference code and expected curves are not evidence from the current execution.

## Using Fixed Materials

Read the needed content from fixed materials already supplied with the assignment and installed Skill resources. When material comes from Memory, use the supplied fixed copy, retaining its source, version, and provided content hash; do not access the live store through a Library path or a ref alone. Metadata matches cannot replace applicability checks; explicitly record missing contents or Proof as unresolved.

The Experiment Cell has no live Memory reader: neither the retired `recollect` nor `scientific_memory` is provided. When external sources are missing, use `lookup` as described below; read immutable research records within the Task through the protocol's `retrieve`, which is not a shared Memory reader.

Focus on extracting currently useful constructions, complete assumptions, the bound's regime / quantifiers, source / proof locators, and conditions still requiring verification. Existing theorems may provide calibration or a theoretical bracket; a Relation does not imply that the complete Setting has a minimax characterization.

## Using lookup

Use `lookup(query=..., limit=...)` for external search and `lookup(url=...)` to read selected originals. First locate material using titles / snippets, then read the statements, definitions, and necessary proof / implementation details supporting the intended assessment. Record search results, abstracts, and full texts separately; retain limitations when reading fails.

Prioritize verification against original papers, author versions, official documentation, and locatable source code. When tool capabilities are needed, inspect the actual schema of the current session; do not bypass MCP to read credentials or create an unauthorized backend. External search is governed by the current configuration; retain any limitation when reading fails or is unavailable. See the [protocol](../../protocol.md) for tools and return conventions.

## Converting Sources into Usable Experiment Information

Match the source to the current Setting item by item: Function Family, Algorithm Class, Oracle, Metric, Resource, risk, normalization, and regime. Mark results requiring additional assumptions as conditional; a deterministic lower bound does not directly cover a randomized Algorithm Class, and a stochastic Oracle result cannot be transferred merely because its name is similar.

Choose the next step according to the current purpose:

- **Calibration**: Select a known result and its regime, then identify the testable behavior expected from the implementation; an asymptotic bound does not automatically predict constants over a finite range.
- **Construction / implementation**: Extract reusable mechanisms and justifications for their properties, and verify that the required Oracle is authorized; a paper formula or library entry does not constitute an existing executable implementation.
- **Interpretation / conjecture**: Explain which interpretation the source supports or constrains, distinguishing established theorems, inferences made here, and hypotheses awaiting testing.

If a source already resolves the current theoretical question, inform the main agent and assess whether calibration, reproduction, or a new regime still merits an experiment; do not continue running experiments merely to fill out the workflow. Not finding an answer reflects only the coverage of this search.

## Outputs and Return

Leave concise findings relevant to the current decision, fixed content or authorized artifact references, original source locations, actual reading coverage, applicability, and recommended next steps. When delivering to another agent / Verifier, also provide fixed snapshots of the content used; a potentially changing Library ref alone is insufficient.

Save obtained material as source notes within this Task, retaining location information; link the local material actually used in the empirical report. Retain the fixed ref of a tool-generated experiment_result rather than inventing an archive type or status. Reading itself does not upgrade evidence status or automatically write new entries to Long-Term Memory.

Return to the main workflow when the information is sufficient or further retrieval cannot improve the current experimental decision. For unresolved questions, state the specific obstacle and the hypothesis most worth testing, rather than leaving a generic literature list.
