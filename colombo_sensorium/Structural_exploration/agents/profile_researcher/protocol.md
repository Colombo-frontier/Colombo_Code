# New Setting Profile Research Agent: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`research`.

research.action=new; candidate_ref/identity_ref are fixed, base_version=null, and setting_id is the proposed new ID, following the current schema/ID-allocation rules without occupying an existing ID. profile_ref identifies the frozen profile; result_refs/proof_refs are references to actual artifacts. change_summary explains why the addition is worthwhile and its coverage limitations. Do not present unresolved identity as new.

First call schema_read(profile), and read the target constraints with target_schema_read. Before freezing, use draft_validate with final tag_facts_json to check the complete five files, and correct errors with patches in the same session. The adapter handles versions and mechanical source metadata under the target schema; do not fabricate historical source_profile records. Final research.tag_facts must bind actual view/operation IDs and fields in the frozen profile; do not copy candidate paths directly as the publication format.

## Writing and handoff

Before freezing a finite-completion profile, declare its profile.research_scope; final research.research_scope must match exactly. The controller binds this declaration to actual search/read logs, not a self-issued completion certificate.

Use the complete mandatory loaded status and joint-parameter standards, and obtain `schema_read(joint_analysis)` before authoring `profile.joint_analysis` v2. Fill `research_scope={queries_complete,unresolved_leads,scope}` from actual work. Bind exact pending-lead strings in synthesis obligations. Classify slices, uniform constants, compatible candidates, replacements, projections, native closure publication and impact witnesses; do not inherit a seed's evidence or global completion claim. Partial supported proposals remain explicitly partial. The same existing profile reviewer independently checks the frozen analysis and all three hash bindings.

Create a first new profile normally when no baseline exists. If a scientific revision receives profile_clone_source, first call draft_clone(**profile_clone_source) to copy the previous formal profile, then make targeted incremental draft_read/draft_patch changes. Preserve unchanged proof/result references and verify applicability; mathematical changes require new versions. Do not emit the entire stored old draft again. Full draft_validate/draft_freeze and independent review remain required.

Read coverage_scope_ref first, and complete the nine coverage checks and known review obligations before assembling a large profile. research must contain coverage_ledger. For each view/regime, checks must give verified/not_applicable/unresolved and a specific reason; verified entries must cite formal result/proof artifacts. In a revision, issue_resolutions must address every publication blocker in repair_feedback_ref. Investigate coarse accuracy, zero queries, reconstruction saturation, and dimension/confidence endpoints together rather than waiting for each review to add one corner. Additional material_refs are all unapproved leads; adopt their claims only after rechecking sources and proofs. Obtain source_locators.version from source.version first; do not replace it with an arXiv version name. Prefer read_batch for independent small pages, sharing the existing response-size limit.

Use the shared protocol for incremental formal writes, the small handoff, reference grants, scoped issues and recovery. A role handoff is neither scientific approval nor a commit receipt.

## Atlas expansion origins

When origin_ref/expansion_ref are provided, the candidate is a designed research contract. Read those fixed records and the literature_cutoff. Preserve a concise source-setting relation and the declared structural changes in profile.relations/provenance where appropriate, identifying them as design provenance rather than a proved reduction. Do not treat the seed bracket as inherited evidence. Recheck any theorem transfer, with the correct algorithm range, native oracle, goal, parameter region and charged resources. A complete contract may honestly have missing bounds; do not turn incomplete literature coverage into a claim of a field-level open problem. If new evidence undermines identity, save an explicit identity issue and an executable next step rather than force a new profile.
