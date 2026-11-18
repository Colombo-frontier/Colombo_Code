# Tag Extraction and Browsing Directories

## Two Types of Information for Two Retrieval Questions

**Context facets answer "under what conditions does this knowledge apply?"** using the eight axes. **Research-use tags answer "what can this help me do, and by what idea?"** to help agents discover methods they have not considered. Human-facing directories and machine indexes are generated from the same facts, without separately maintained scientific classifications.

| Axis | Information recorded here | Common pitfalls |
|---|---|---|
| TASK | Mathematical formulation, solution concept, and target object | Topic membership cannot replace the formulation |
| MODEL | Instance class, regularity, geometry, variable blocks, norm, and existence and distributional conditions | Smoothness, convexity, and geometry belong to this axis; conditions must identify their subjects and scopes |
| ORACLE | Queries, exact feedback, query domain, randomness, coupling, reuse, and auxiliary operations | Distinguish exact value, value+gradient, gradient-only, fresh-sample, and same-sample access |
| ALGORITHMS | Characteristics of a method itself, or the algorithm class covered by a lower bound | "The method is deterministic" differs from "the lower bound covers only deterministic algorithms" |
| OUTPUT | Output object, space, feasibility, query restrictions, and averaging or random selection | The last iterate, an averaged point, and a random iterate are different |
| METRIC | Error formula, norm and squaring, normalization, and order of aggregation | Proximity in a directory does not make two metrics equivalent |
| GUARANTEE | Quantifiers, expectation / probability, randomness, and cost guarantees | Distinguish expected error from expected runtime |
| RESOURCE | Accounting for oracle calls, samples, components, communication, arithmetic, and other costs | Multiple call types cannot be represented by a single unitless complexity value |

Research-use tags initially contain only four groups of concepts:

| Group | Purpose | Examples of vocabulary candidates, not a list of entries already in the library |
|---|---|---|
| goal | What I need to accomplish now | reduce_variance, control_bias, accelerate, construct_lower_bound, convert_metric |
| mechanism | How it works | momentum, clipping, preconditioning, recursive_estimation, information_hiding |
| bottleneck | What obstacle it reveals or addresses | information_leakage, noise_accumulation, coordinate_revelation, inner_accuracy |
| proof_method | How an argument can be organized | potential, coupling, change_of_measure, concentration, scaling, reduction |

There is no need to enumerate all terms in advance. Each concept stores a stable ID, a clear definition, a display label, aliases, an optional parent, and related concepts. Parent-child relationships serve only navigation and query expansion; mathematical implications require a separate Theorem / derivation. Multiple reasonable parents may be retained, but navigation ancestors must not be treated as additional proved properties.

Example vocabulary entry:

```json
{
  "id": "mechanism.variance_reduction",
  "label": "Variance reduction",
  "aliases": [
    "variance reduction",
    "variance-reduced estimator"
  ],
  "definition": "Improves usable estimates or their cumulative cost by controlling estimation error; specific guarantees are supplied by linked entries.",
  "parent": "mechanism.estimation",
  "related": [
    "proof.recursive_error_control"
  ]
}
```

## Tags Must Bind to Specific Scientific Statements

Each scientific facet retains:

- axis and normalized concept ID;
- role:describes / requires / covers / concludes / limits;
- subject: the object to which it applies, such as outer f, inner g, the x-block, or the lower-bound Algorithm Class;
- scope_ref: the entry's variant, statement, or explicit conditions section;
- evidence_refs: references to supporting content or source evidence;
- state:asserted / unknown / not_assumed / not_applicable.

These fields recover meaning; they do not require the model to create another formal logic. Norms, ranges, and other details already expanded in the scope need not be repeated in full in every tag, but must be accessible through the binding. Explicit negative conditions must state their mathematical meaning; not_assumed must not be treated as false.

For example, if a method "does not require strong convexity," record the absence of that requirement; do not turn it into "applies only to functions that are not strongly convex." Lower-bound coverage must use covers, so it cannot be misread as the construction itself employing a deterministic algorithm.

The exact oracle of variant A and the convexity of variant B in a Family must not be combined across scopes into an established Exact + Convex match. The union of Family tags may retrieve it as a candidate, but the result card must identify the matching variant or state that the conditions have not been verified within the same scope.

## Extraction Steps

1. Read the source first and preserve scientific content that can be reconstructed.
2. Extract the formulation, conditions, interfaces, and claim coverage from the actual content, without guessing from the paper title.
3. Normalize using the existing vocabulary and aliases; propose a new term only for a genuinely new concept, with its definition and neighboring concepts.
4. Add use_when, mechanism, bottleneck, and proof goals to express uses worth considering.
5. Generate short cards, directory entries, and retrieval indexes from the same record.
6. An independent Reviewer checks both content and navigation: tags must not broaden conclusions, and necessary conditions must not be omitted in a way that makes the record undiscoverable.

Provide at least one realistic usage query for each record; add a neighboring query when confusion is a clear risk. This is a small-scale retrieval check, not a reason to write implementation-mirroring unit tests for every tag.

## Directories for Brain and Cell

The overview begins with a one-page map of methods, optionally without any setting filter. For each direction, provide a one-sentence purpose, common prerequisites, a few actual entries, and an expansion entry point. Suggested initial directories:

- Construct or improve an Algorithm: estimation, momentum, restart, clipping, preconditioning.
- Manage multilevel or nested errors: inner accuracy, tracking, bias propagation.
- Design a Hard Family: base blocks, assembly, hiding, oracle realization.
- Establish a lower bound: information-to-error, hypothesis testing, lifting.
- Complete an analytic proof: potential, recursion, concentration, coupling.
- Transfer results: scaling, oracle simulation, Metric / Guarantee / Resource conversion.
- Challenge research routes: known failure examples, escape Algorithms, limitations.

These directories overlap and need not be mutually exclusive. A component may appear under both Algorithm design and proof techniques. Official directories list only entries that are actually readable; empty branches or unverified literature must not masquerade as existing knowledge.

## Avoiding Omissions in Machine Retrieval

Initial screening serves recall and ranking, not applicability decisions.

- Retrieve in parallel using names and aliases, body keywords, context facets, research uses, and mechanisms; supplement with a semantic index when available.
- Treat the current TASK as an important clue only; allow removal of the TASK filter when searching for a mechanism or proof obligation.
- Exclude records outright only when the user explicitly requests an exact match and the evidence clearly conflicts. Records with unknown conditions, missing tags, or a required adapter may be retained with an explanation.
- Identify "directly relevant candidates," "transferable leads," and "challenge material," together with missing conditions. These are reading recommendations, not automatically established applicability conclusions.
- Rerank using variant / claim bindings; remove duplicate cards while retaining substantive differences between variants.
- The initial response may contain roughly a dozen cards, with further pages as needed. This number is a working budget, not a guarantee of exhaustiveness.

An agent's actual use of a result depends on the complete statement, variable mapping, and necessary derivation. A failed search means only that this retrieval found nothing; it does not establish that a result does not exist or that a problem is open.

## Organization as the Collection Grows

Index cards, condition summaries, use_when, components, mechanisms, and limitations, not just titles. Search and read full proofs as needed, without including them in every startup context. Cache original sources separately and reuse locator indexes.

Rebuild only affected records, cards, and links on update. Use stable record IDs / revisions so unrelated updates do not invalidate old references. Decide whether to add lexical search, facet retrieval, or semantic retrieval based on observed query recall; a large graph database need not be built first.

Minimum acceptance checks should include: natural-language queries retrieve known relevant items; Exact / Model combinations do not combine conditions across variants; profiles outside Atlas are searchable; methods across TASK boundaries are discoverable; nearby records with unmet conditions show the differences; unknown items are not silently filtered out.
