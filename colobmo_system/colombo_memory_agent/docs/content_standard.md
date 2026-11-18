# Scientific Content Storage Standard

This standard specifies the content to retain for Algorithm, Hard Family, Theorem, Proof Method, and Source records. Explanations are written in Chinese, while research terminology is in English.

JSON is the maintained source; Markdown is a reading view of the same content. The Markdown templates in this directory guide completion or generation of reading pages and are not maintained independently of JSON. Tag, retrieval-card, and directory rules are specified in the retrieval documentation.

## 1. Storage Units and Lightweight Design Principles

Algorithms, Hard Families, and Theorems maintain separate stable identities; Sources preserve paper identities, versions, and original locators. A paper's reading page organizes its contributions through references without copying every entry's full content.

Use an **object or variant that can be independently understood, retrieved, and cited** as the unit. A Family aggregates and supports reuse of shared mechanisms; it need not contain dozens of variants in one entry. A few similar variants may be embedded; variants with different query protocols, initialization, applicability conditions, or costs should be independently citable, readable, and reviewable. Existing schemas may support this through stable subreferences or separate entries; immediate directory restructuring is unnecessary.

To remain lightweight, first reduce duplicated full text, repeated scopes, and research-process records. Conditions determining validity must be retained:

- Identical names do not imply identical mathematical rules; parameter windows usually belong to scopes or claims, without copying a Family for every parameter value.
- Different proofs of the same statement share a Theorem identity; clearly distinguish changes to assumptions, quantifiers, or conclusions.
- Local calculations serving only one proof in the source may remain within that proof or Source context.
- Applications, failed attempts, and unfinished derivations for the current task first remain in the research workspace; submit them to memory when they have independent reuse value.

## 2. Algorithm: Preserve Rules, Reusable Components, and Scope of Validity

An Algorithm entry should answer at least:

1. **What it is.** Family, variant, state, initialization, query sequence, update, output, and necessary tuning rules.
2. **What it requires.** Model conditions, Oracle capabilities, public parameters, and available auxiliary operations.
3. **Why it works.** Key mechanisms, invariants, or estimates, and supporting claims.
4. **What can be reused.** Components such as estimators, momentum, clipping, restart, and preconditioning.
5. **What it guarantees.** References to specific Theorems, scopes, regimes, Metrics, Guarantees, and Resources.
6. **Where its limitations lie.** Clearly distinguish proved limitations, gaps in current analysis, and unverified conjectures.

For a lengthy Algorithm, retain key mathematical rules and exact source locators; specify which details must be read in the original to execute it. Do not retain only the Algorithm name, and do not require copying implementation code and the entire convergence proof.

Use a short contract for each reusable component:

- goal: the difficulty it addresses;
- operation: the update, estimator, or information flow it changes;
- requires: conditions and permitted information on which it depends;
- produces: the estimate or structure it provides;
- cost: additional Resource;
- checks: what must be reproved during transfer;
- support: specific claims or worked proofs.

Keep components inside their parent entry initially. Assign independent stable references when there is a clear need for reuse across entries. After combining components, recheck the resulting Algorithm and Guarantee.

An Algorithm entry's scope describes the witness's rules and applicability; class-lower-bound coverage describes the entire excluded Algorithm Class. Read each from its own claim, without allowing one to inherit the other.

### Describing Bottlenecks

| Type | What it may state |
|---|---|
| Algorithm-specific limitation | Limitations of a specific variant or explicitly defined method class on certain instances |
| Class lower bound | Necessary cost for the entire declared Algorithm Class |
| Analysis limitation | A term not controlled by the current proof; this does not establish inevitable method failure |
| Empirical finding | Behavior observed in experiments, without upgrading it to a mathematical lower bound |
| Unknown | No evidence-based explanation has yet been found |

Do not invent an unsupported story merely to fill the "bottleneck explanation" field. A known performance result and its explanatory mechanism may have different evidence statuses.

## 3. Hard Family: Store Construction and Hardness Argument Separately

Core Hard Family content includes:

- Parameterized construction, hidden objects, dimension, and parameter domains;
- Properties such as Model membership, normalization, and initialization;
- Exact Oracle feedback, query domain, randomness, and sample coupling;
- The information-bottleneck mechanism;
- The argument converting the bottleneck into the target Metric;
- Covered Algorithm Class, Guarantee, Resource, and regime;
- Known escape conditions and lifting not yet established.

One construction may be used with multiple oracles. Hardness under one oracle does not automatically transfer to another. Failure of a fixed Algorithm likewise does not automatically establish a class-wide lower bound.

### How Hardness Can Be Reused

Reusable content may be an entire Family or a local construction method:

| Component | Common purpose | Main transfer checks |
|---|---|---|
| Base block | Supplies basic geometry or a local obstacle | Model conditions, scale, and target error |
| Assembly | Combines multiple blocks | Whether queries reveal several blocks simultaneously; whether Resource costs are additive |
| Information hiding | Hides directions, signs, indices, or other objects | Whether the Oracle leaks extra information; applicable Algorithm Class |
| Oracle realization | Implements the required noise or feedback structure | Unbiasedness, moments, coupling, history dependence |
| Calibration | Adjusts the construction to the target parameter range | All affected parameters, dimension, and constants |
| Lifting argument | Extends arguments for restricted methods to a broader Algorithm Class | Quantifiers, randomness, dimension, and budget costs |

These components are not building blocks that compose automatically. Each must retain input conditions, the precise transformation, properties proved to be preserved, additional costs, and obligations still to be established.

In particular, a direct-sum construction does not automatically yield an additive query lower bound; under exact real-valued feedback, effective concealment of the hidden information requires a separate proof.

## 4. Theorem: Complete Statements and Layered Proof Storage

### Results to Prioritize

Prioritize independently useful results:

- Principal performance claims supporting existing Algorithms or Hard Families;
- Analytic, probabilistic, and information-theoretic lemmas;
- Oracle simulations and Resource conversions;
- Normalization, scaling, Metric, or Guarantee conversions;
- Construction properties and information-to-error reductions;
- lower-bound lifting;
- Proof components actually reused in multiple arguments.

Do not mechanically create a Theorem entry for every numbered result in a paper.

### Required Statement Detail

The local record of an established Theorem should reconstruct its exact meaning:

- Objects, spaces, norms, and necessary definitions;
- All assumptions determining validity;
- Parameter domains, quantifier order, and randomness;
- An explicit conclusion;
- For complexity claims, Algorithm coverage or upper-bound witness, Oracle, Output, Metric, Guarantee, Resource, dimension, regime, and hidden-constant dependence.

Precise references to pinned definition or scope records are allowed; "satisfies the paper's conditions" is insufficient. When key assumptions remain unconfirmed, retain a literature lead rather than presenting a directly usable Theorem.

### Three Levels of Proof Storage

| Level | Local content | Suitable cases |
|---|---|---|
| Source-linked proof | Core route, key steps or dependencies, exact source locators, and actual reading coverage | Published results with long proofs; the default |
| Proof sketch | Readable main argument with omissions identified | Supports understanding and transfer, without claiming a complete derivation |
| Complete local proof | Complete argument that can be checked step by step, with necessary dependencies | Short general lemmas, local normalization, transfer, correction, or new derivation |

Do not rewrite the entire proof of every published result. Read targeted original passages when transferring methods, checking sensitive conditions, addressing concerns, or relying on a key step not yet read.

Source support, completeness of stored proofs, independent review, and formal certification are distinct facts. Reading the original or passing structural validation does not constitute an independent proof.

## 5. Proof Method: Preserve Its Identity as a Recipe

Proof Methods are stored in the Theorem Library, initially if desired as stable subrecords of a proof; create a method entry when it has independent reuse value.

Retain the goal pattern, required inputs, key choices, invariant or reduction, proof skeleton, common failure points, and worked proof references.

A method recipe helps construct proofs. It does not itself carry the semantics of an established Theorem; each specific instantiation must still discharge the corresponding obligations.

## 6. Source: Minimal Identity, Context, and Coverage

A Source retains:

- Title, authors, bibliographic identifiers, explicit version, and links;
- Access to the original; a content hash may be recorded for acquired files;
- Locators for necessary notation, definitions, and standing assumptions;
- Mappings from original locators to extracted entries;
- Actual reading coverage and important unmapped anchors;
- Verified correction or supersession relationships.

Do not claim paper-level verification without reading the full text. If a URL does not identify an explicit version, record that fact rather than guessing a version number.

The Paper view's entry list and reverse references are generated from canonical entries. Complete PDFs, HTML, or text may be cached as needed; retrieval cards do not embed full texts.

## 7. When Additional Material Is Needed

Leave explicit local tasks in the following cases:

- Algorithm execution details are insufficient for reconstruction;
- A construction's Model membership has not been verified;
- A statement's key prerequisites remain unconfirmed;
- A required proof step has not been read;
- The Source version or locator cannot be resolved reliably;
- A transfer has only intuition and no argument.

Bind tasks to the affected objects or claims. One local gap does not prevent further organization of independent, verified content.
