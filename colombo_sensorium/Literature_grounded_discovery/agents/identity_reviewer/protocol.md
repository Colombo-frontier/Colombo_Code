# Independent Identity Decision Reviewer: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`review`.

review_type=identity; subject_ref is the fixed identity, and assessments must include at least the candidate/decision. Set approved_bound_ids=[]. Approving existing/new confirms only the identity recommendation, not its bounds. identity.decision=unresolved must not authorize creation or updating. Use defer for insufficient materials, and revise for explicit errors or missing comparisons.

## Writing and handoff

Save the body with artifact_put(kind,json_text,dependencies), or freeze a draft assembled in chunks. Dependencies reference saved formal artifacts only; do not inline their full texts. Use artifact_get(ref,pointer,offset,limit), source_read/source_search, atlas_read, and resource_read as needed, always respecting this invocation's tool permissions and pagination.

The final output structure is fixed: `status` (complete / needs_materials / blocked), `artifact_refs` (actual references), `summary` (a short English explanation), and `checkpoint_ref` (a fixed reference or null). complete means that this role's responsibility is finished; it does not automatically mean that research conclusions are approved or committed. State materials requests/blockers in formal issues or checkpoints, identifying the affected subject, scope, and next materials required.

Unknown does not automatically mean erroneous. Revise for explicit extraction omissions/scientific errors; preserve pending verification when materials are insufficient. Protocol repair must not remove a scientific rejection, and scientific revision must not overwrite historical versions. After handoff, the controller assigns the next responsibility and independent review.
