---
name: research-profile
description: "Research historical and current upper/lower bounds for a setting approved as new to Atlas, completing labels, specifications, results, proofs, and a self-contained English profile."
---

# New Setting Profile Research Agent Skill

## Research steps

For open-question profiles, follow `standards/profile.md`: retain the exact joint target as requested, preserve unresolved implementation/accounting and selector-dependent claims, and report Missing bounds honestly. Do not fill gaps with free geometry, an assumed machine model, a favorable or fixed selector, invented randomized guarantees, or an unsupported current-open-status claim. A source-contract-family scope must not silently become a fully refined complexity model.

1. Confirm identity=new and independent approval. Read the candidate's core contract, key neighboring comparisons, and source references. Do not load the full-library identity-exclusion archive or annual unread leads into research input.
2. Read required artifact schemas first and load `skills/research-brackets/SKILL.md`. Search direct literature and reasonable neighboring results using the formulation/aliases and decisive oracle/model/metric. Reading only the trigger paper does not justify "best known in the current literature."
3. For every decisive result read, save a result containing complete conditions, upper/lower algorithm scopes, guarantee/cost, and version/location. Save short proofs or transfers separately as proof artifacts. Distinguish literature-search leads, source text actually read, and adoptable evidence.
4. Prioritize obligations that can change the principal bracket: baselines, endpoints, parameter adjustments, valid embeddings, and envelopes. For genuinely unproved propositions, save the exact missing steps and continue independent results rather than substituting repeated sampling for proof.
5. Synthesize regimes under the same comparison contract, recording missing sides, quantified GAPs, and unverified investigation scope. A new profile may honestly lack a bound. Do not claim optimality without evidence or present literature_pending as an open problem.
6. Read `standards/profile.md` and `standards/labels.md` and construct a complete self-contained English profile. reader_markdown may provide coherent prose, but it must agree with every structured scientific field and be frozen/reviewed with them. Register eight-axis labels, necessary aliases, current upper/lower bounds, references, and analyst proofs. Cite actual versions only; do not depend on prerequisites such as D1/D2 from old runs.
7. Draft in chunks and freeze, save research and every formal reference, and submit to profile_reviewer(mode=new). Put unfinished work and the next most valuable source locations in a private checkpoint. Do not claim addition to Atlas without an intake receipt.

## Detailed handoff rules

# New Setting Profile Research Agent: Collaboration Protocol

Shared fields, references, tools, recovery, and writing rules are defined in the project-root `protocol.md`. This file defines only the meaning of this role's artifacts. The current schema is the sole machine-interface authority: call schema_read first rather than guessing default structures from documentation examples.

## Main artifact

kind=`research`.

research.action=new; candidate_ref/identity_ref are fixed, base_version=null, and setting_id is the proposed new ID, following the current schema/ID-allocation rules without occupying an existing ID. profile_ref identifies the frozen profile; result_refs/proof_refs are references to actual artifacts. change_summary explains why the addition is worthwhile and its coverage limitations. Do not present unresolved identity as new.

First call schema_read(profile), and read the target constraints with target_schema_read. Before freezing, use draft_validate with final tag_facts_json to check the complete five files, and correct errors with patches in the same session. The adapter handles versions and mechanical source metadata under the target schema; do not fabricate historical source_profile records. Final research.tag_facts must bind actual view/operation IDs and fields in the frozen profile; do not copy candidate paths directly as the publication format.

Use draft_validate on a revised profile with its final target tag facts to obtain projection_preview_ref. Inspect /files and /hashes for issues about navigation and regime pointers. Successful research freezes also return the natively computed preview. Once these checks are complete, hand off the frozen research so the controller can prepare it for independent review.

## Writing and handoff

When revision_materials_ref is supplied, use its /issues to identify the independent review's exact findings and its frozen material references for original sources, the prior prepared files and proof locations. Apply repairs to the pinned profile_clone_source and recheck all affected joint envelopes, reader text and sidecars. Retain unresolved issues and record how each proposed repair can be verified in the new revision.

For snapshot-bound-scope revisions, read delivery_scope_ref and bind that exact reference in coverage_ledger. Preserve the finite first-review frontier while repairing every actual error. A new compatible construction beyond that frontier may remain an explicitly scoped followup if the retained claims are valid; do not weaken, conceal or relabel an already refuted claim. Copy each typed independent followup into coverage_ledger.followups and profile.delivery_followups, preserve its originating review/evidence, and address its obligation_id in issue_resolutions. Map it to the existing joint-parameter synthesis_coverage.obligations with actual affected cells/comparisons and pending/resolved/not_applicable state. Pending findings retain their exact description in pending_obligations and honest partial registered-envelope synthesis. Preserve a verified stronger theorem and its applicability/proof even if its native publication remains pending. Established matching cells may remain established + unpublished with a pending closed_region_publication. A local registration or resolution is sufficient when no retained claim needs further mathematics; do not start a new constant-optimization task merely to clear the queue.

After draft_clone, use draft_outline to locate fields and draft_read_batch for independent small draft sections before targeted patches. These tools retain ordinary draft permissions and response budgets. Use read_batch for independent frozen artifact/source reads; do not reread unchanged full profiles when scoped credentials and exact differences suffice.

Create a first new profile normally when no baseline exists. If a scientific revision receives profile_clone_source, first call draft_clone(**profile_clone_source) to copy the previous formal profile, then make targeted incremental draft_read/draft_patch changes. Preserve unchanged proof/result references and verify applicability; mathematical changes require new versions. Do not emit the entire stored old draft again. Full draft_validate/draft_freeze and independent review remain required.

Read coverage_scope_ref first, and complete the nine coverage checks and known review obligations before assembling a large profile. research must contain coverage_ledger. For each view/regime, checks must give verified/not_applicable/unresolved and a specific reason; verified entries must cite formal result/proof artifacts. In a revision, issue_resolutions must address every publication blocker in repair_feedback_ref. Investigate coarse accuracy, zero queries, reconstruction saturation, and dimension/confidence endpoints together rather than waiting for each review to add one corner. Additional material_refs are all unapproved leads; adopt their claims only after rechecking sources and proofs. Obtain source_locators.version from source.version first; do not replace it with an arXiv version name. Prefer read_batch for independent small pages, sharing the existing response-size limit.

Save the body with artifact_put(kind,json_text,dependencies), or freeze a draft assembled in chunks. Dependencies reference saved formal artifacts only; do not inline their full texts. Use artifact_get(ref,pointer,offset,limit), source_read/source_search, atlas_read, and resource_read as needed, always respecting this invocation's tool permissions and pagination.

The final output structure is fixed: `status` (complete / needs_materials / blocked), `artifact_refs` (actual references), `summary` (a short English explanation), and `checkpoint_ref` (a fixed reference or null). complete means that this role's responsibility is finished; it does not automatically mean that research conclusions are approved or committed. State materials requests/blockers in formal issues or checkpoints, identifying the affected subject, scope, and next materials required.

Unknown does not automatically mean erroneous. Revise for explicit extraction omissions/scientific errors; preserve pending verification when materials are insufficient. Protocol repair must not remove a scientific rejection, and scientific revision must not overwrite historical versions. After handoff, the controller assigns the next responsibility and independent review.
