# Current comparisons and historical audit records

The `comparisons` array contains current envelopes only. A complete
`comparison_key` identifies at most one current row: setting, view, guarantee,
quantity, resource projection and regime. An improved envelope replaces the
weaker row on that contract; its source bounds can still contribute to the
new minimum upper envelope. Summary counts and research tasks use current rows.

Retired comparisons are preserved in `provenance.comparison_history`. Each
entry retains the complete original comparison, its canonical JSON SHA-256,
the current `superseded_by` IDs and the replacement relation. Legacy aliases
are routed through `data/registry/aliases.json`. A split routes to the view and
its complete replacement row set; it does not claim a one-to-one identity.

## Remaining research regions

A broad gap label must not be used to reopen a certified closed subregion.
For the normalized `d >= 3` target in `SO_FO_N01_L1_G`, let D be the original
target, H the existing high-dimensional closed region, and S the region
`d/log(2+d) >= epsilon^(-2)` where the recorded lower envelope saturates.
The current rows cover D intersect H, D outside H intersect S, and
`D \ (H union S)`. Only the last row is the remaining quantified-gap target.
Its `research_target` records the target regime, excluded closed comparison
IDs, remaining regime and explicit predicate AST. Equality belongs to the
closed branch. The original high-dimensional row is preserved without
assuming H is contained in S.

These are constant-factor rate closures. No exact query count or necessary
dimension threshold is asserted. A quantified remaining envelope can still
have a bounded ratio on some parameter slices. Before assigning a narrower
task, subtract any additional certified closures at the requested precision.

## Proof premise bindings

By default, `premises` entries with `pointer` and `sha256` bind to the current
profile. Hashes use UTF-8 JSON with sorted keys, compact separators and
`ensure_ascii=False`. Missing pointers and mismatches fail validation.

A proof with `lifecycle.state = historical` is excluded from current bound
support. Its original text and premise hashes remain intact. When the exact
predecessor snapshot has not been recovered, the explicit
`historical_unresolved` binding is reported as unresolved, rather than being
silently rehashed against current fields. `first_observed` identifies where
the audit record was found; it does not certify that this was its original
premise snapshot. The historical BL zero-query audit has four premise hashes
that already differ at that first-observed snapshot. Current zero-query and
guarded lower results have separate proofs.

The validator checks current-key uniqueness, history hashes and replacement
links, research-target contracts, current premise hashes, and rejection of
historical proofs as active bound support. These integrity checks do not
independently certify the cited research theorems.
