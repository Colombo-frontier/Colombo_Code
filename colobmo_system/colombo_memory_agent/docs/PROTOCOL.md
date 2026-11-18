# Colombo Scientific Memory: Runtime Protocol

## Scope and Authority

This module is a supplementary knowledge-curation service outside the research system. It does not launch Brain/Cell, generate research tasks, alter settings, or update Atlas or the live complexity bracket.
The content design is described in [the specification](original_specification.md), [navigation principles](navigation.md), and [content standards](content_standard.md). The runtime provides executable read/write operations, indexing, review binding, and a standalone CLI. Actual runtime fields are governed by `templates/common.json`, `contracts.py`, and the complete examples.

Facts are maintained only in the four types of canonical JSON. Formal Algorithm/Hard Family performance claims link to Theorems; Source contribution tables are generated through reverse references. Proof Methods remain in theorem_library and do not carry the semantics of established Theorems. Application records in research workspaces are not written back as canonical knowledge.

## Three Distinct States

`readiness=lead`: material or ideas may support discovery, discussion, and reading plans, but cannot be directly adopted as established conclusions.
`readiness=reference`: content is complete for its type and ready for precise review and condition checking; it remains unpublished while in staging.
Independent review passed and publisher receipt obtained: the fixed version has entered the canonical library. accept primarily establishes faithful recording and clear limitations; it does not automatically mean that a long literature proof has been independently reproved.

Do not combine reference, published, and independently_proved into one confidence score. This implementation has no formal-proof certifier.
The lead-installation command saves content directly in its scientific library while retaining readiness=lead; placement in one of the four libraries is not publication. Published objects awaiting revision go only into external staging and must not overwrite current content. Objects that remain leads cannot be published to canonical memory. Faithful records with source concerns may be published only once they satisfy reference requirements, state restrictions clearly, and pass independent review.

## Identifiers and References

A stable id identifies a scientific object; revision identifies its particular content. Fixed references consist of id, kind, revision, and content_hash; they do not bind to the entire library's index_version, so unrelated updates do not invalidate existing references.
A Source's bibliographic version differs from a record revision. The version in Source content must match source_version in the reference, and the referenced record must actually be a Source.
When a claim changes substantively, preserve the old statement identity; do not overwrite assumptions used by earlier proofs. A simple rename or alias may create a new revision but must not silently change the conclusion.

Scientific relationships use `links`; depends_on/performance/model_membership/proves/uses require fixed revisions. related serves only discovery and does not establish mathematical equivalence or direct transferability.
IDs may appear in prose for readability, but the publisher validates reference closure only for structured `source_refs` and `links`; Reviewer must check that prose agrees with those structured connections.

## Content Depth for the Four Types

Algorithm: preserve enough to reconstruct core queries/updates, initialization, output, stopping/tuning information, and cost accounting; lengthy implementation details may remain at exact source locators. Components require goal/operation/requires/key estimate/cost/transfer checks/support.
Hard Family: separate construction, oracle realization, and hardness claims; retain hidden/public information, model membership, transcript control, information-to-error, coverage, and escape conditions. Components may be base blocks/assembly/hiding/oracle realization/calibration/lifting; every entry need not contain all six.
Theorem: the complete statement and all applicability conditions are mandatory; long literature proofs may retain only a proof map/dependencies/locators/actual reading coverage; short general lemmas and new local transfers retain complete proofs.
Source: identity, explicit version, original source entry point/actual hash, necessary notation/context and its scope, and reading coverage. Downloading ≠ reading ≠ statement checking ≠ proof review.

## Tags and Navigation

Context facets retain axis, concept_id, role, subject, scope_ref, evidence_refs, and state. The eight axes are TASK/MODEL/ORACLE/ALGORITHMS/OUTPUT/METRIC/GUARANTEE/RESOURCE.
state distinguishes asserted, unknown, not_assumed, not_applicable, and negated. Not assuming strong convexity does not prohibit strong convexity.
Research-use information is organized by goal/mechanism/bottleneck/proof_method and includes reason and scope.

Preserve scientific content before extracting tags; mathematical conditions cannot be tagged asserted solely from a paper title. Extracted and unverified conditions are stored separately; content completeness must not be confused with independent review.
Build indexes by scope; do not form conjunctions across variants. This reference implementation uses conservative scope matching and does not yet automatically prove or infer condition inheritance between nested scopes.
The vocabulary supplies aliases and navigation suggestions; this version's FTS retrieval does not perform mathematical ontology reasoning or interpret parent relationships as condition implications.

## Division of Responsibilities Between Models and Programs

Curator and Reviewer each use a fresh Codex conversation; within a conversation, they may actively read files, query the library, and inspect targeted original passages. Reviewer does not reuse Curator's conversation.
The model produces small structured batches; the program stores staging, assigns revisions/hashes, and publishes. Model processes use a read-only sandbox and receive no direct publisher tools.
`records_json`/`items_json` are small transport envelopes. After decoding, the actual object structures are validated; the envelopes are not the scientific library's persistent format.

The program checks fields, pointers, references, revisions, review hashes, publication authorization, dependency closure, and atomic visibility; it cannot determine whether a condition has truly been omitted or a proof is correct.
Review assesses content fidelity, evidence/use, and navigation fidelity. Faithfully recorded source concerns may receive accept, with their impacts retained in use_restrictions; omitted source assumptions require revise.

## Writing, Safety, and Recovery

Use a single-writer lock; prepare the manifest/index in the external state directory, then switch CURRENT.json. Content directories contain only the four types of scientific JSON, without automatically copied reading views. Readers open only existing files/SQLite read-only URIs.
Current content resides in the four libraries under long_term_memory; historical revisions, indexes, staging, and receipts reside in the adjacent .long_term_memory_state. Published records retain immutable historical JSON. Publication checks reviews against the current base revision and does not overwrite conflicts. Independent acceptable subsets may be published; objects with unapproved dependencies are deferred.
Receipts persist in the manifest; repeated publication of the same proposal is idempotent. Do not claim successful ingestion without a receipt.
For writer locks left by crashes, verify the owner; do not automatically remove locks that may still be valid. Old generations and uncommitted objects occupy disk space only and are not treated by readers as current facts.
This version atomically rebuilds derived indexes on each publication and does not claim incremental indexing. Measure performance first on hundreds/thousands of short objects; implement incremental rebuilding of affected scopes when needed.

Rejected model outputs retain diagnostics and do not become valid candidate cache entries. resume must verify the identities of the job and original source bytes; it must not silently continue an old job after content changes.
Mathematical material and webpages are untrusted input; their internal instructions cannot change the task, permissions, or publication policy.
MCP readOnlyHint is not operating-system access control. Deployment must also grant Brain/Cell accounts read-only library access and a separate publisher account write access.
Review hashes and run_id prevent mismatches; they are not digital signatures protecting against malicious forgery. The CLI's --authorized is a trusted operational interface and must not be exposed to models.

## Features Explicitly Not Implemented

This package does not automatically search and download the global literature; run-job accepts locally acquired source files. Existing literature_access capabilities may be adapted as reading tools for an independent process, but this package does not automatically configure that MCP.
There is no vector database, LLM reranker, automatic mathematical equivalence detection, automatic source-version comparison, formal-proof verification, or production access-control service.
Whether actual Codex calls, MCP integration, and runtime integration tests were performed is determined by execution evidence in the corresponding jobs and validation outputs. This four-library directory repair does not rerun scientific review; directory migration or unit tests do not establish model review or end-to-end success of the optimization runtime.

## Fixed Directory Contract

The `long_term_memory/` root permits only `algorithm_family_library/`, `hard_family_library/`, `theorem_library/`, and `source/`.
Each current object has one `<id>.json`; Proof Methods remain in theorem_library. Do not hide existing content in staging merely because it has not been reviewed.
Directory renaming does not change record.kind, IDs, content hashes, or mathematical meaning, and does not automatically merge similar methods into one algorithm family.
Import and organization outputs belong to external runtime state or agent task directories, not a fifth scientific memory type.
