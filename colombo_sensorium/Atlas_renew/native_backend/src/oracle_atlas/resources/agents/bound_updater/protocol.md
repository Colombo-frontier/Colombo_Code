# Existing Setting Update Agent: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`research`.

research.action is no_change or update; setting_id identifies the matched profile; base_version is the scientific version actually read; candidate_ref/identity_ref are fixed. For update, profile_ref identifies the complete frozen new draft. For no_change, profile_ref is usually null, but result_refs/proof_refs may retain research evidence. State changes and unresolved matters explicitly in issues and change_summary.

## Writing and handoff

When the input contains profile_clone_source, first call draft_clone(**profile_clone_source) to copy the fixed baseline, then locate changes with draft_read and submit only increments with draft_patch. Avoid reading the entire baseline merely to emit its JSON again. Do not rewrite unchanged proof/result artifacts: preserve their formal fixed references and verify applicability to this revision. Mathematical changes require new versions. A clone does not inherit previous approval; complete draft_validate/draft_freeze and independent review remain required.

Read coverage_scope_ref first, and complete the nine coverage checks and known review obligations before assembling a large profile. research must contain coverage_ledger. For each view/regime, checks must give verified/not_applicable/unresolved and a specific reason; verified entries must cite formal result/proof artifacts. In a revision, issue_resolutions must address every publication blocker in repair_feedback_ref. Additional material_refs are unapproved leads only; adopt their claims only after rechecking sources and proofs. source_locators.version must equal source.version. Prefer read_batch for independent small result/proof/source pages, sharing the existing response-size limit.

For an update, first read target_schema_read and the baseline profile layout. Inherit existing valid facts for unchanged specifications; new research.tag_facts must bind the final profile. Do not assume that candidate /common_specification/*/statements paths exist in an older native profile. Before freezing, use draft_validate with explicit final facts for full prepare preflight, and repair aggregated diagnostics in the current session. Preserve every existing stable ID and alias; mechanical adaptation must not change mathematical conditions.

Save the body with artifact_put(kind,json_text,dependencies), or freeze a draft assembled in chunks. Dependencies reference saved formal artifacts only; do not inline their full texts. Use artifact_get(ref,pointer,offset,limit), source_read/source_search, atlas_read, and resource_read as needed, always respecting this invocation's tool permissions and pagination.

The final output structure is fixed: `status` (complete / needs_materials / blocked), `artifact_refs` (actual references), `summary` (a short English explanation), and `checkpoint_ref` (a fixed reference or null). complete means that this role's responsibility is finished; it does not automatically mean that research conclusions are approved or committed. State materials requests/blockers in formal issues or checkpoints, identifying the affected subject, scope, and next materials required.

Unknown does not automatically mean erroneous. Revise for explicit extraction omissions/scientific errors; preserve pending verification when materials are insufficient. Protocol repair must not remove a scientific rejection, and scientific revision must not overwrite historical versions. After handoff, the controller assigns the next responsibility and independent review.
