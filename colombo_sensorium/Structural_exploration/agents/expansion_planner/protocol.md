# Expansion Planner: Collaboration Protocol

The project protocol governs references, tools, bounded input, persistence, and recovery. The current schema defines all fields and types; read it before producing a formal artifact.

## Inputs and main artifact

The controller supplies `request_ref` and `neighborhood_ref`, with any explicitly authorized formal history. Read the request's scope and limits. Read the neighborhood's inventory version and seed/neighbor identifiers. Its retrieval relations are navigational leads, not certified mathematical reductions.

The main kind is `expansion_plan`. Bind the exact input references. Each opportunity has a stable local `opportunity_id`, title, source seed and neighbor identifiers, operators, changed axes, target tasks, mutation steps, a concrete transformation, selection reason, expected value, transfer leads, risks, and priority score. Follow the schema for the exact representations. Do not invent source IDs or present proposed targets as existing Atlas IDs.

`transfer_leads` describe statements or mechanisms that should be investigated. They do not adopt any theorem. `not_pursued` and `coverage_note` state what this finite plan leaves aside and why. An empty plan is valid when no defensible opportunity fits the request; explain the limitation.

## Handoff

Store the plan using `artifact_put` or a frozen incremental draft. Return only the shared handoff fields: `status`, `artifact_refs`, `summary`, and `checkpoint_ref`. `complete` means that planning is complete, not that any setting is novel, reviewed, researched, or committed.

Preserve the same frozen request during recovery. A new round or changed scope requires its own request. Private memory may help planning but is not an independent review or proof. All later scientific decisions remain with their assigned agents.
