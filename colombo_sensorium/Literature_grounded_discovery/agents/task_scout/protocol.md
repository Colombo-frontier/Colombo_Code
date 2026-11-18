# Task Type Discovery Agent: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`task_proposal`.

Each entry in task_proposal.proposals contains task_id, label, formulation, queries, evidence_refs, and reason, accompanied by report_zh. task_id is a proposal; formal approval/normalization belongs to the user and catalog management. report_zh explains the proposed expansion, representative literature, relationships to existing classes, and unverified scope. An empty proposals array is allowed when no new task is found; describe coverage honestly.

## Writing and handoff

Save the body with artifact_put(kind,json_text,dependencies), or freeze a draft assembled in chunks. Dependencies reference saved formal artifacts only; do not inline their full texts. Use artifact_get(ref,pointer,offset,limit), source_read/source_search, atlas_read, and resource_read as needed, always respecting this invocation's tool permissions and pagination.

The final output structure is fixed: `status` (complete / needs_materials / blocked), `artifact_refs` (actual references), `summary` (a short English explanation), and `checkpoint_ref` (a fixed reference or null). complete means that this role's responsibility is finished; it does not automatically mean that research conclusions are approved or committed. State materials requests/blockers in formal issues or checkpoints, identifying the affected subject, scope, and next materials required.

Unknown does not automatically mean erroneous. Revise for explicit extraction omissions/scientific errors; preserve pending verification when materials are insufficient. Protocol repair must not remove a scientific rejection, and scientific revision must not overwrite historical versions. After handoff, the controller assigns the next responsibility and independent review.
