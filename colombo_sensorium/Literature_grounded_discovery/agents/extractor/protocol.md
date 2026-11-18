# Setting Extraction Agent: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`extraction`.

First call schema_read(candidate) and schema_read(extraction). candidate.common_specification must contain all eight axes. Fill every statement scope-binding field explicitly according to the schema, using null even when a field is not applicable. Preserve genuine algorithm-permission/guarantee differences in views, and point tag_facts to existing specification locations. extraction={candidate_refs,paper_ref}. A new candidate ID is not a formal Atlas setting ID.

Declare native operations explicitly under common_specification.oracle.operations or a view override; view_ref/operation_ref use declared IDs. Check the candidate with draft_validate first. Unique ID paths may be normalized mechanically; missing or ambiguous operation declarations must be corrected from the source or explicitly marked unknown. Do not invent permissions from operation names.

After reading the theorem and oracle model, group the source terms across axes and call vocabulary_lookup_batch once per group (up to 16 terms, axis and offset per term). Compare the returned human and machine registrations to the source and view. Follow next_offset only for ambiguous terms. Use vocabulary_lookup for the full records and registered parent edges of selected IDs in one request. An empty list leaves a concept unresolved or proposed. Do not enumerate entire axes to find a known term or infer exact feedback from an auxiliary operation.

## Writing and handoff

Save the body with artifact_put(kind,json_text,dependencies), or freeze a draft assembled in chunks. Dependencies reference saved formal artifacts only; do not inline their full texts. Use artifact_get(ref,pointer,offset,limit), source_read/source_search, atlas_read, and resource_read as needed, always respecting this invocation's tool permissions and pagination.

The final output structure is fixed: `status` (complete / needs_materials / blocked), `artifact_refs` (actual references), `summary` (a short English explanation), and `checkpoint_ref` (a fixed reference or null). complete means that this role's responsibility is finished; it does not automatically mean that research conclusions are approved or committed. State materials requests/blockers in formal issues or checkpoints, identifying the affected subject, scope, and next materials required.

Unknown does not automatically mean erroneous. Revise for explicit extraction omissions/scientific errors; preserve pending verification when materials are insufficient. Protocol repair must not remove a scientific rejection, and scientific revision must not overwrite historical versions. After handoff, the controller assigns the next responsibility and independent review.
