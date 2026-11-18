# Scientific Memory and review identity

The bundled Memory contains 388 published records and 43 leads. Keep
`long_term_memory/` together with `.long_term_memory_state/`.

Scientific statements, assumptions, proofs, source identities, literature
versions, material hashes, evidence limitations, and publication tiers are
retained. Local task identities, audit logs, execution receipts, caches from
prior jobs, workstation locators, and operational timestamps are excluded.
Local snapshot suffixes are removed from record identifiers and all affected
scientific references are updated together.

The paired state holds current search indexes and immutable scientific objects
needed by pinned references. Bundled objects are named by content hash in
`objects/`; these are scientific evidence, rather than execution history.
Original review and receipt hash commitments remain as provenance without the
local jobs that produced them.

Removing metadata changes a record's JSON digest. The manifest and
`PRIVACY_PROJECTION.json` bind the original accepted content hash to the public
projected hash. Original review scopes remain distinguishable from projected
bytes; `original_review_scope_hash` commits to the scope before removal of local
identifiers. Reader cards disclose this distinction. **No new independent review
is asserted for the projected bytes.** A lead remains a lead.

Artifact identifiers identify evidence but do not promise that original PDFs or
page images are bundled. Obtain the selected literature version from its public
source URL and verify the recorded original-material hash.

Published-only search is the default. Use `include_leads=true` to discover
candidates, reuse complete returned references, and finish paginated reads.
Review status does not establish applicability to a new mathematical Setting.

Future scientific changes use the independent Curator/Reviewer workflow. New
candidate content requires review of its exact prepared identity and explicit
publication through the trusted writer; metadata projection does not replace
this process. Runtime compatibility identities and literature editions retain
their original meanings.
