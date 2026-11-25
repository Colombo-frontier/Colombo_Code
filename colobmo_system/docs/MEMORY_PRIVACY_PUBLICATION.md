# Scientific Memory and review identity

The bundled Memory contains 388 published records and 43 leads. Keep
`long_term_memory/` together with `.long_term_memory_state/`.

Mathematical statements, assumptions, proof arguments, source identities, literature
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

Removing metadata or projecting public wording changes a record's JSON digest. The manifest and
`PRIVACY_PROJECTION.json` bind the original accepted content hash to the public
projected hash. Original review scopes remain distinguishable from projected
bytes; `original_review_scope_hash` commits to the scope before removal of local
identifiers. Reader cards disclose this distinction. **No new independent review
is asserted for the projected bytes.** A lead remains a lead.

## Neutral public wording

The current release also contains an explicitly disclosed editorial projection,
`neutral-public-language-v1`. Evaluative commentary about external sources is
expressed as the precise formula convention, local calculation, evidence scope,
or application restriction used by this Memory. Mathematical examples and their
calculations remain available. A source formula that was not adopted remains
unadopted; a blocked application remains blocked. This operation neither
certifies a source statement nor upgrades a lead or a local argument.

The `editorial_projection` extension in `PRIVACY_PROJECTION.json` records each
affected input and output hash, the changed prose pointers, and any pinned
reference pointers updated as a consequence. Affected published manifest
entries carry the same extension. The existing privacy schema and its legacy
transformation identifier remain for reader compatibility; the explicit
extension identifies the additional editorial operation. Lead mappings are
listed separately and do not carry a review acceptance.

The release retains the original accepted-content, review, review-scope and
receipt hash commitments. It does not rebind a historical review to new bytes.
Only affected scientific objects and references are projected; both search
indexes are rebuilt from the current paired Store with the existing index
builder. Prior wording and private before/after audit files are not bundled.
The hashes and field pointers provide the public projection trail, while the
original review applies only to its original content identity. **No new review,
new scientific revision, or new publication is claimed for this projection.**

Artifact identifiers identify evidence but do not promise that original PDFs or
page images are bundled. Obtain the selected literature version from its public
source URL and verify the recorded original-material hash.

Published-only search is the default. Use `include_leads=true` to discover
candidates, reuse complete returned references, and finish paginated reads.
Review status does not establish applicability to a new mathematical Setting.

Future scientific changes use the independent Curator/Reviewer workflow. New
candidate content requires review of its exact prepared identity and explicit
publication through the trusted writer; release projection does not replace
this process. Runtime compatibility identities and literature editions retain
their original meanings.
