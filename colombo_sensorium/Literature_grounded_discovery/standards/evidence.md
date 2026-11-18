# Evidence, Atomic Results, and Independent Review

## 1. Three evidence origins

- `published_theorem`: faithfully records a locatable published result, all its conditions, and the original authors' proof status.
- `analyst_transfer`: transfers an existing result to the target contract. A separate proof object must explain the mapping and its cost.
- `analyst_derivation`: a self-contained derivation or short proof proposed by the component. It must not be attributed to the original paper as a theorem.

Search summaries, bibliographic metadata, producer notes, and unreviewed drafts are leads; they do not automatically qualify as admissible mathematical evidence. Verify publications mentioned in API search responses. Do not invent DOIs, versions, years, or theorem numbers.

## 2. Atomic result cards

Each card carries a conclusion that can be verified independently. It must include at least the complete proposition or inequality, all parameter ranges, assumptions, exact guarantee and cost quantifiers, upper/lower bound direction, an actual algorithmic witness for an upper bound or the permitted algorithm class for a lower bound, source/version/locator, current issues, and dependencies.

For comparisons, specify six keys: setting, view, guarantee, quantity, resource projection, and parameter region. A source whose setting is not yet established may initially reference a candidate; provide an explicit mapping after identity is confirmed. A free-form rate string cannot support automatic comparison.

Preserve enough conditions for readers to understand the card without rereading the entire paper. Key theorem/proof passages remain available through targeted reads of source refs. Do not embed full papers, complete page indexes, or annual bibliographies in cards.

## 3. Citations and sources

Bind the source to a ref for the actual fixed content, and separately record the URL/DOI/arXiv version, title, and locator. Theorem numbers may differ between PDF, HTML, and supplementary materials; an argument must bind the version it uses. Page, equation, and passage locators help find evidence; they do not establish that the text has been read.

If OCR or text conversion loses exponents, matrix layout, or subscripts/superscripts, check the original page or another representation of the same version. If verification is impossible, identify the unverified formula and the bounds it affects. Fetched, read, and understood/verified are three distinct states.

## 4. Issue scope

Populate issue kind/scope/subject_refs/blocks/message/evidence_refs/resolves according to the schema. `blocks` lists only the affected extraction/identity/bound/profile/publication stages or objects.

A historical issue may be partially resolved: a new revision states what was fixed and what remains uncertain, and removes resolved blockers. Preserve the issue's identity and history; an open issue need not retain every historical blocker forever. Wording changes alone cannot resolve a substantive issue.

A scoped issue names the dependent field, view, quantity, projection, theorem, or adoption claim. Unspecified implementation work may remain unresolved while source-defined task information is retained. An empty adopted-bound list is not a waiver for unresolved primary identity: explain whether the unknown changes that identity or a proposed equality. Conversely, an arithmetic-accounting gap does not block unrelated source-description or objective-query claims that do not depend on that accounting. Apply the uncertainty test in `identity.md`. Approval of a gap-disclosing document approves neither a missing computation model nor a conjectured guarantee.

Protocol errors (missing fields or invalid pointers) require protocol repair; unclear source text requires targeted material acquisition; proof errors require scientific revision. An external network failure does not establish that a setting does not exist or that a proposition is false.

## 5. Approval and quarantine

Review must take place in a fresh session without the producer's private working memory. Reviewers may read formal results/proofs, fixed sources, previously reviewed baselines, and differences. Producer self-assessment cannot replace verification.

A review binds a specific subject_ref. Each assessment identifies its subject, verdict, and actual reason. A profile review's `approved_bound_ids` lists only bounds that are genuinely admissible. Approving a document that honestly discloses gaps does not approve its quarantined results.

Unknowns do not require universal rejection: determine whether they block the responsibility under review. Faithful extraction may be approved while retaining bound uncertainties; a profile may be approved with some missing bounds. Conversely, unresolved unknowns in the core native interface prevent formal identity approval, and an unproved derivation cannot enter an active bracket.

## 6. Valid reuse

Proof credentials separate credentials for a fixed proof proposition from its application to the current bound. A proof becomes a reuse candidate only when an independent review explicitly provides proof_approvals, its complete assumptions, context_pointers, full proof, and fixed source/result dependencies are unchanged, and proof_issue_scopes records no unresolved impact. The catalog supplies verifiable fingerprints and the prior review chain only; the new final review still verifies application, domain, and scientific coverage and explicitly adopts the proof. Do not infer independent approval of every proof from bound approval, whole-document approval, or citation of a source. Fall back to full verification when older records lack explicit credentials. Reusing evidence text and reusing approval are separate actions; the former cannot replace the latter.

The first review of a new profile checks the complete scientific output. An update checks differences, new applications, and composition against a fixed baseline. The review_context validates the previous independent role, valid handoff, subject/prepared-package hashes, scientific context for each bound, and declared dependency closure. Approvals with unchanged dependencies and no bound blockers become reuse candidates; an explicitly approved individual bound in a revise review can also qualify. The new final review still explicitly lists every bound proposed for adoption and approves the current five files; the writer does not add approvals automatically. Missing formal support, missing/ambiguous dependencies, or invalid role/source/hash credentials require full review. Implicit dependencies must not be presented as verified. New counterexamples can overturn prior approval.

When assumptions, oracles, metrics, algorithm quantifiers, proof dependencies, or source versions change, recheck affected results and brackets. Unrelated annual queues need not be reread. Memory only helps locate the next step; adoption must enter the formal evidence chain.

Independent scope review distinguishes unchanged-proof reuse from independent scope revalidation. Only a controller-listed `proof_scope_revalidation_candidates` entry may use the latter: the formal proposition and mathematical dependencies remain fixed, but its profile context or contextual issues changed. The current reviewer inspects the original credential, changed context and all affected historical/current issue occurrences, determines applicability independently, and issues a new complete credential. `proof_scope_revalidations` records that work; it does not belong in `reused_proof_refs`. A stable fingerprint establishes content identity, not mathematical truth or unchanged applicability.

The optional credential scope `standalone_proposition_explicit_context` requires `/common_specification` and every mathematical definition needed by the proposition: parameters and domains, variables and blocks, norms, quantifiers, oracle and cost assumptions. Unlike legacy `standalone_proposition`, it does not implicitly include the entire profile parameters array. When switching scopes, inspect the old context and justify any excluded fields as irrelevant; a real assumption cannot be removed by changing credential metadata. Changed assumptions or sources/proofs require full review of affected mathematics. New contextual counterexamples remain blockers until independently resolved or correctly scoped, including earlier occurrences with the same issue ID. The current bound applications, synthesis, six joint checks and frozen five files still need approval.
