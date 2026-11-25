# Complexity Atlas

Complexity Atlas contains scientific records and offline webpages for **445 optimization and information-reconstruction settings**. Each setting describes its mathematical model, oracle access, algorithm permissions, output, error metric, guarantee and resource budget, with bounds and evidence for explicit applicability regions.

Open `index.html` to browse the library. Native records are in `data/settings/<setting_id>/`, including the profile, identity, classification, and human and machine tags. The catalog and source bindings are in `data/derived/catalog.json` and `data/derived/catalog_sources.json`. The 31 supplied Colombo manuscripts, including KIMI_001, KIMI_002, KIMI_003 and the joint stochastic bilevel complexity manuscript, and their stable source signatures are indexed in `data/sources/colombo/catalog.json`.

The `★ Colombo` contribution marker currently covers 85 settings: 49 supported by the public-paper registry and 38 supported by bundled manuscripts, with two overlaps. Two pending claims remain in the provenance registry and are excluded from adopted coverage. The 39 historical near-optimal highlight selections are a narrower subset. Current markers follow selected native support and preserve each comparison's rate status, including remaining gaps. `data/derived/colombo_contributions.json` provides the merged provenance; its 22 arXiv entries and 31 local manuscript entries are source records, not a deduplicated count of independent works.

The setting pages and profile downloads describe the current manuscript contributions of N01, A4 and U10: N01's alternative construction and measurable transfer framework, A4's alternative smooth macro-block construction, and U10's uniform bounds and boundary geometry. The corresponding known-rate acknowledgements are retained.

PDF, TeX and Markdown versions of each profile are available in `visualization/dist/downloads/<setting_id>/profile.*`.

Statuses describe the documented comparisons within their stated regions. A matching or near-matching result in one region does not establish whole-profile optimality or exhaustive literature coverage. Source attribution is separate from mathematical status, and references and applicability conditions accompany individual claims. Mathematical-font mappings in some PDFs may limit formula search or copying; the native JSON, TeX and Markdown preserve the underlying expressions.
