# Atlas Identity Matching Agent: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`identity`.

identity must contain candidate_ref, decision, setting_id, view_mapping, normalization, comparisons, retrieval_ref, recall_audit, and issues exactly as required. decision is existing/new/unresolved; setting_id=null for new and unresolved. If an existing profile has no corresponding view, set atlas_view_id=null in the mapping and explain the proposed new view. normalization is required and must not be hidden only in comparisons.reason. Under the schema, recall_audit must record actual strategies, unresolved credible neighbors in unresolved_ids, the coverage reason, and the actual inventory_version. Do not return new while credible neighbors remain unresolved.

## Writing and handoff

Save the body with artifact_put(kind,json_text,dependencies), or freeze a draft assembled in chunks. Dependencies reference saved formal artifacts only; do not inline their full texts. Use artifact_get(ref,pointer,offset,limit), source_read/source_search, atlas_read, and resource_read as needed, always respecting this invocation's tool permissions and pagination.

The final output structure is fixed: `status` (complete / needs_materials / blocked), `artifact_refs` (actual references), `summary` (a short English explanation), and `checkpoint_ref` (a fixed reference or null). complete means that this role's responsibility is finished; it does not automatically mean that research conclusions are approved or committed. State materials requests/blockers in formal issues or checkpoints, identifying the affected subject, scope, and next materials required.

Unknown does not automatically mean erroneous. Revise for explicit extraction omissions/scientific errors; preserve pending verification when materials are insufficient. Protocol repair must not remove a scientific rejection, and scientific revision must not overwrite historical versions. After handoff, the controller assigns the next responsibility and independent review.
