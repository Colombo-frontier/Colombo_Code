# Usage and Minimal Architecture

This specification is intended for Colombo's Brain, Cell, Memory Curator, and Memory Reviewer. It provides an implementable storage and agent design; it does not imply that the current runtime implements every interface described here, nor have the examples been written to the existing memory.

Core conventions: store the four types of scientific objects separately; aggregate a paper's contributions in a Paper view through references. Input setting profiles need not belong to Atlas. Memory is a reference resource to consult as needed; agents remain free to read external literature, develop their own derivations, run experiments, and propose new methods.

| Storage location | Contents | Maintenance |
| - | - | - |
| algorithm_library | Algorithm / explicit variant, core rules, components, mechanisms, result references, and limitations | Canonical JSON |
| hard_family_library | Parameterized construction, oracle realization, information bottleneck, reusable components, and lower-bound references | Canonical JSON |
| theorem_library | Complete statements, necessary conditions, and proof records; independently useful proof methods | Canonical JSON |
| sources | Source identity, version, access to the original, necessary context, and reading coverage | Canonical JSON; retain a separate copy of the original or retrieve it as needed |
| navigation | Vocabulary, overview, directories, and retrieval cards | Controlled vocabulary maintenance; other views generated from canonical records |
| staging | Current proposals, review comments, revision diffs, and publication receipts | Retain only what the current task requires |
| research workspace | Application records, derivations, and failed attempts for the current problem | Part of the research process; extract into memory when they have reusable value |

If the existing code stores Source identities in theorem_library/papers, provide a unified read interface and a sources view; there is no need to migrate all files merely to change directory names.

**The storage unit is a knowledge object that can be understood and cited independently.** One paper may yield multiple entries, and one entry may be supported by multiple papers. A Family aggregates shared mechanisms. A few closely related variants may share an entry, but each variant must be independently citable; separate them when their query protocols, core structures, uses, or lengths differ substantially. Do not allow a Family document to grow without bound.

**Maintain a single source of scientific facts.** JSON is the source of truth; the Markdown reading view, Paper view, directory cards, and search index are generated from it. Source-code adapters map to the existing schema. The field templates in this document are design contracts, not data that can be passed to an old validator without adaptation.

The following project files are recommended; alternatively, use this document as a unified specification initially:

| File | Purpose |
| - | - |
| protocol.md | Rules for object identity, references, review, updates, and publication |
| docs/navigation.md | Principles for tags, directories, and retrieval |
| docs/content_standard.md | Storage granularity for the four content types |
| docs/04_brain_cell_usage.md | Usage by Brain / Cell |
| json_templates/common.json | Shared fields |
| json_templates/algorithm_content.json | Algorithm content |
| json_templates/hard_family_content.json | Hard Family content |
| json_templates/theorem_content.json | Theorem content |
| json_templates/source_content.json | Source content |
| json_templates/proof_method_content.json | Optional proof method, still stored in theorem_library |
| agents/memory_curator/AGENTS.md | Curator responsibilities |
| agents/memory_reviewer/AGENTS.md | Reviewer responsibilities |
| instructions/extract_memory.md | Extraction workflow |
| instructions/review_memory.md | Review workflow |

AGENTS.md defines roles, responsibilities, and working methods; protocol.md defines shared interfaces and decision rules; instructions files contain detailed task prompts. Document organization does not require additional agents.

# Shared Protocol

## Identity and References

1. Every entry has a stable ID. References to specific scientific conclusions bind to a record revision; references to papers bind to a source version and an exact locator.

2. Different proofs of the same complete statement may share a Theorem identity. Substantive changes to assumptions, quantifiers, or the conclusion require a new statement identity or an explicit statement version; do not overwrite the previous meaning.

3. A new performance result for the same Algorithm usually adds a Theorem / application reference; distinguish variants when the actual query, update, permitted initialization, output, or tuning rules change.

4. Keep hardness claims for the same construction under different oracles separate. Different parameter windows may remain as scoped claims within one entry.

5. Synonymous names are aliases; similar mechanisms have a related relationship. Identical names or rates are insufficient grounds for merging.

6. Navigation links may point to the current entry. References actually used in a proof must pin versions and retain a snapshot of the content used or an accessible historical revision. If the existing store has no permanent history, at least preserve the statements used, necessary conditions, and hashes in the proof package.

## Three Reading Depths

- Overview / card: helps select material worth reading; includes its purpose, core prerequisites, limitations, and reading entry points.

- Scientific record: specifies the Algorithm, construction, or statement precisely.

- Proof / original source: supports detailed application, transfer, and verification.

These three depths derive from the same record, not three manually maintained databases. A card does not discharge proof obligations.

## Scope and Performance Links

An Algorithm / Hard Family may include a brief scope description. Complete conditions for formal performance results belong in Theorems; each performance link explicitly identifies the variant or construction, the Theorem, and the applicable regime. The union of Family-level tags is only for navigation; it must not combine the Oracle, Model, and Guarantee of different variants into one result.

A general lemma does not require an invented complete setting. Irrelevant axes may be omitted; use not_applicable when they must be represented. Record a condition that is not required as not_assumed; this does not mean that the condition is false.

## Evidence and Review

Record the following facts separately:

- Whether the record represents the source faithfully and with sufficient completeness.

- Whether the claim rests on a source statement, a local derivation, or merely an idea awaiting verification.

- Which proof sections have been read.

- Whether there has been an independent review and whether a formal artifact actually exists.

Do not collapse these facts into a vague confidence score. An entry that faithfully records concerns about a source may pass record review, but affected claims must retain usage restrictions. Bind issues to specific claims, scopes, or fields; continue with entries that do not depend on them.

## Publication and Recovery

Canonical mutations use base revisions to prevent concurrent changes from being overwritten. The program checks formats, references, revisions, review bindings, and publication permissions; mathematical judgments are delegated to LLM review.

Model outputs enter the accepted-result cache only after structural and business-rule validation. Retain diagnostics for rejected outputs to support revision; do not treat them as valid results during ordinary resume. Recovery requests include the current candidate, relevant previous candidate, latest feedback, and diff.

Publish in small batches with complete dependencies, and update derived directories. Report successful publication only after obtaining an actual receipt. When automatic publication is already authorized, follow the existing policy without adding routine human confirmation.

# Tag Extraction and Browsing Directories

## Two Types of Information for Two Retrieval Questions

**Context facets answer "under what conditions does this knowledge apply?"** using the eight axes. **Research-use tags answer "what can this help me do, and by what idea?"** to help agents discover methods they have not considered. Human-facing directories and machine indexes are generated from the same facts, without separately maintained scientific classifications.

| Axis | Information recorded here | Common pitfalls |
| - | - | - |
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
| - | - | - |
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

# Common Storage Template

The following JSON is a template to complete. Text in angle brackets and null values indicate unfinished fields; do not publish the template unchanged. Actual IDs, revisions, hashes, and review receipts are supplied or verified by the runtime. A missing value does not mean mathematical falsehood.

Each record uses this shared envelope, with content populated from the corresponding template in the next section. A Source record usually has empty source_refs; its own version entry point is stored in content. Fill only fields relevant to the same scientific statement; do not turn every optional field into an acceptance requirement.

```json
{
  "schema": "colombo-memory-proposal/1",
  "id": "<stable-entry-id>",
  "revision": null,
  "kind": "<algorithm | hard_family | theorem | proof_method | source>",
  "title": "<precise name>",
  "aliases": [],
  "summary": "<one to three sentences: what it is, what it helps accomplish, and key limitations>",
  "use_when": [
    "<a natural research question or usage trigger>"
  ],
  "content": {},
  "navigation": {
    "concept_ids": [],
    "query_aliases": [],
    "facets": []
  },
  "source_refs": [
    {
      "ref_id": "s1",
      "source_id": "<source-id>",
      "source_version": "<exact version>",
      "locator": "<section / theorem / equation / page>"
    }
  ],
  "links": []
}
```

Choose one actual value for kind. Proof Methods remain in theorem_library; do not create a fifth scientific library. revision denotes the actual published version and may be null for a new proposal awaiting assignment.

A scientific facet has the following structure. This example illustrates only the format; it must not be used to automatically impose a function-value requirement on any actual Algorithm:

```json
{
  "axis": "ORACLE",
  "concept_id": "oracle.feedback.function_value",
  "role": "requires",
  "subject": "<queried function and variable blocks>",
  "scope_ref": "#/content/variants/0/requirements",
  "evidence_refs": [
    "#/source_refs/0"
  ],
  "state": "asserted"
}
```

Reference rules:

- scope_ref uses a valid JSON Pointer within this record; the locator is stable only when the record revision is pinned.

- evidence_refs point to source / statement entries actually stored; local derivations point to the actual proofs.

- navigation.concept_ids may express broad research uses. They cannot override or replace scoped facets.

- Scientific connections in links include relation, target_id, target_revision, applicable scope, and a one-sentence explanation. A related link used only for discovery may resolve to the latest version; pin it when it enters a proof package.

- Retrieval summaries may repeat short phrases, but complete conditions are maintained only in canonical scientific content or explicit fixed references.

Do not maintain the same complexity formula separately in Algorithm, Hard Family, Theorem, and Source records. Performance summaries displayed by Algorithm / Hard Family records are generated from the corresponding Theorem; the "current best bracket" remains the responsibility of research on the specific setting and the Atlas synthesis layer.

# Algorithm Content and Template

Algorithm memory should let a Cell understand how the core method works, which component can be reused, and what its costs and prerequisites are. "Momentum + Clipping" alone is insufficient; copying the complete implementation and convergence proof is unnecessary.

Required content includes the core query / update, state and initialization, output, public parameters that affect implementation, key scope, components, and result references. For long methods, extensive implementation details may remain in precisely located source passages, but the record must specify which details must be read to execute the method fully.

Bottlenecks fall into five categories: proved limitations of a specific method, lower bounds for an entire Algorithm Class, terms not yet controlled by the analysis, empirical observations, and unknowns. Without evidence, record unknown; do not invent "why it cannot be faster" merely to fill the template.

```json
{
  "family": "<shared mechanism or family reference>",
  "variants": [
    {
      "variant_id": "v1",
      "name": "<explicit variant name>",
      "public_inputs": [
        "<information available for tuning>"
      ],
      "state_and_initialization": "<state variables, initialization, and required promises>",
      "requirements": "<key Model conditions and Oracle capabilities; required norm / domain / sample coupling>",
      "query_and_update": "<complete core mathematical rules: what is queried first, what is returned, and how updates are made>",
      "tuning_and_stopping": "<step size, batch, restart, stopping rules, and dependence on public parameters>",
      "output": "<last iterate / averaging / random selection and feasibility>",
      "cost": "<unit costs of each operation and call type; reusable or free operations>",
      "implementation_details_ref": "<exact locator for lengthy details not expanded here; leave empty if none>"
    }
  ],
  "components": [
    {
      "component_id": "c1",
      "name": "<e.g., clipping / estimator / momentum>",
      "goal": "<the difficulty it addresses>",
      "operation": "<inputs, operation, and outputs>",
      "requires": "<mathematical conditions and available information>",
      "key_estimate": "<key inequality, invariant, or Theorem reference>",
      "cost_effect": "<additional calls or computation; parameters affected>",
      "transfer_checks": [
        "<what must be reestablished after changing the task or Oracle>"
      ],
      "support_refs": [
        "<claim / proof / source references>"
      ]
    }
  ],
  "performance_links": [
    {
      "variant_id": "v1",
      "theorem_ref": "<Theorem ID and revision>",
      "scope_note": "<regime of this link; read the corresponding statement for complete conditions>"
    }
  ],
  "limitations": [
    {
      "kind": "<algorithm_specific | class_lower_bound | analysis_gap | empirical | unknown>",
      "statement": "<specific limitation or fact that remains unknown>",
      "scope": "<the particular variant / class / regime affected>",
      "support_refs": []
    }
  ]
}
```

Initially embed components within their records. Assign a component an independent knowledge identity only when other entries repeatedly reference it or when it has independent applicability conditions and a proof. Guarantees for different components cannot simply be added; new combinations still require review of oracle legality, error propagation, Metric, and Resource.

Aim for one to a few screens of reading in ordinary cases; this is a readability target, and necessary conditions must never be removed to meet a length target.

# Hard Family Content and Reuse Template

Hardness constructions contain reusable components, which are often more valuable to preserve than a final numerical lower bound. Reusable objects include basic hard blocks, assembly methods, information hiding, oracle realizations, parameter calibration, and lifting arguments.

Separate three objects: the instance construction; how it interacts with a particular oracle; and the resulting lower-bound claim for a specific Algorithm Class. A function formula alone does not identify the information access under which it is hard.

```json
{
  "construction": {
    "definition": "<formula for the parameterized instance or reconstructible construction steps>",
    "parameters": "<parameter ranges, dimension, and normalization>",
    "hidden_objects": "<unknown sign / direction / index / distribution>",
    "public_information": "<information known to the algorithm and initialization promises>",
    "model_membership_refs": [
      "<properties and their proofs or statements>"
    ]
  },
  "oracle_realizations": [
    {
      "oracle_id": "o1",
      "query_and_feedback": "<exact query domain and returned information>",
      "choices_and_history": "<oracle choices, sources of randomness, and history dependence>",
      "sampling_and_reuse": "<independence, coupling, fresh / same-sample access>",
      "cost": "<accounting unit>",
      "information_bottleneck": "<what one query / the entire transcript can and cannot reveal>",
      "information_to_error": "<how missing information yields error in the target Metric>",
      "supporting_claim_refs": []
    }
  ],
  "hardness_claims": [
    {
      "oracle_id": "o1",
      "theorem_ref": "<lower-bound Theorem ID and revision>",
      "algorithm_coverage": "<fixed / restricted / unrestricted; actual deterministic and randomized coverage>",
      "regime_note": "<budget, dimension, and parameter conditions>",
      "missing_lifting": "<extensions not yet established; write none if there are none>"
    }
  ],
  "components": [
    {
      "component_id": "h1",
      "role": "<base_block | assembly | hiding | oracle_realization | calibration | lifting>",
      "input_conditions": "<objects to which it can be applied>",
      "transformation": "<the precise transformation>",
      "preserved_model_properties": "<properties proved to be preserved>",
      "transcript_control": "<why information from the new Oracle remains restricted as required>",
      "parameter_and_cost_changes": "<changes in dimension, scale, budget, and probability>",
      "remaining_obligations": [],
      "support_refs": []
    }
  ],
  "escape_conditions": [
    {
      "statement": "<additional information or methods that can invalidate the argument>",
      "scope": "<corresponding Oracle / Algorithm Class>",
      "support_refs": [],
      "epistemic_note": "<proved fact or hypothesis awaiting verification>"
    }
  ]
}
```

Check the following questions when reusing components:

| Component | What can be reused | What must be checked again |
| - | - | - |
| Base block | Basic geometry, local difficulty, error separation | Model membership and target Metric |
| Assembly | Direct sum, embedding, methods for combining instances | Whether one query reveals all blocks at once; whether costs are additive |
| Information hiding | Hiding mechanisms based on signs, rotations, indices, etc. | Whether the new Oracle leaks hidden quantities; coverage of adaptive / randomized algorithms |
| Oracle realization | Methods for implementing feedback or noise | Unbiasedness, moments, independence, history dependence, and sample reuse |
| Calibration | Scaling, translation, and dimension adjustment | Joint changes in all parameters, normalization, and regimes |
| Lifting | Arguments extending restricted methods to broader classes | Quantifier order, dimension cost, randomness, and budget windows |

For example, a direct sum alone does not make lower bounds on oracle calls additive; one full-gradient query may return information about several blocks simultaneously. This interface issue must be proved when transferring the construction. Exact real-valued feedback likewise cannot be assigned a fixed information content merely because it returns "only one number per query."

"This construction fails against a particular algorithm" also differs from "the entire problem is easy." An escape Algorithm must bind to the relevant variant, Oracle, and scope.

# Theorem Inclusion Criteria and Level of Detail

The Theorem Library preserves mathematical conclusions that can be cited precisely, together with methods that help construct proofs. Do not copy every numbered lemma from a paper into the library unchanged.

## What to Prioritize

| Type | Reason for inclusion | Minimum local content |
| - | - | - |
| Key upper / lower bound | Supports the performance and coverage of an Algorithm or Hard Family | Complete statement, all conditions, complete complexity scope, and exact source |
| General analytic / probabilistic Lemma | Can discharge multiple proof obligations | Complete statement; preferably the complete proof when short |
| Oracle simulation / Resource conversion | Connects different information access models and cost conventions | Input/output interfaces, validity of the simulation, cost, and applicability conditions |
| Metric / Guarantee / normalization transfer | Prevents direct substitution of inequivalent targets | Exact direction, prerequisites, parameter transformation, and proof |
| Construction property / information-to-error | Connects instances to lower bounds | Properties, quantifiers, applicable construction, and proof entry point |
| Lifting result | Extends arguments for restricted algorithms to broader classes | Algorithm coverage, dimension/probability/budget conditions, and key argument |
| Local calculation used in only one proof | Usually does not warrant a separate entry | Retain within that proof's context, with the original locator |
| Proof method | Provides a route for constructing an argument | Recipe, key choices, failure points, and references to actual worked proofs |

## Statements Must Be Complete

Regardless of how the proof is stored, the local statement must be precisely understandable: objects, spaces, norms, necessary definitions, all assumptions, quantifier order, randomness, parameter domains, and conclusion.

Do not write only "Assumption 3 holds," "usual gap," or "good initialization." Expand definitions that affect the conclusion, or cite a pinned definition record that can be read precisely. A Source's notation/context helps readers navigate the original; it cannot replace a Theorem's key prerequisites.

## How to Store Proofs

| Situation | Local level of detail |
| - | - |
| Existing long proof in the literature | By default, retain a proof map of a few steps, key dependencies, exact locators, and actual reading coverage; read the complete proof in the source as needed |
| Short general lemma | Preserve the complete proof where possible so a Cell can reuse it immediately |
| Locally introduced normalization, transfer, correction, or new derivation | Preserve the complete local argument and dependencies, then obtain independent review |
| Only the main idea is understood | Mark it as a sketch and identify omissions; do not claim the proof is complete |
| Only a methodological idea is available | Store it as a proof method / candidate, not as an established Theorem |

Do not copy an entire paper merely for "detail," or remove applicability conditions merely to remain "lightweight." A proof map supports navigation and understanding; it does not establish omitted steps.

A literature Theorem with complete conditions and no relevant concerns need not be reproved in full on every use. Expand the relevant proof passages when adapting applicability, relying on a key unread step, encountering boundary conditions, or investigating source concerns.

```json
{
  "claim_type": "<performance | lemma | construction_property | transfer | limitation>",
  "intended_use": "<type of proof obligation it can discharge>",
  "statement": {
    "objects_and_definitions": "<spaces, norms, functions, random variables, and necessary definitions>",
    "assumptions": [
      "<all conditions determining validity; identify objects, variable blocks, and scope>"
    ],
    "quantifiers_and_randomness": "<order of for every / exists; randomness and conditioning history>",
    "parameter_domains": "<dimension, accuracy, constants, and parameter ranges>",
    "conclusion": "<complete mathematical conclusion>"
  },
  "complexity_scope": null,
  "proofs": [
    {
      "proof_id": "p1",
      "kind": "<source_linked | sketch | local_complete>",
      "source_ref": "<ref_id in source_refs; null for a local proof without a source>",
      "locator": "<actual proof locator>",
      "map": [
        "<key steps and their dependencies>"
      ],
      "full_local_argument": null,
      "dependencies": [],
      "omitted_details": "<details not expanded locally>",
      "reading_coverage": "<what has actually been read; do not report planned reading>"
    }
  ],
  "evidence": {
    "basis": "<source_statement | local_argument | conjectural>",
    "statement_check": "<actual scope of verification>",
    "issues": []
  },
  "application_guidance": {
    "input_pattern": "<how to recognize a potentially useful application>",
    "sensitive_conditions": [],
    "read_original_when": [
      "<transfer, unclear key conditions, or a particular proof step requiring expansion>"
    ]
  }
}
```

For complexity / performance claims, populate complexity_scope with the following object. A general lemma may retain null because it need not describe an oracle setting:

```json
{
  "upper_witness_or_lower_coverage": "<actual Algorithm variant or covered algorithm class>",
  "oracle": "<native interface, information access, and stochastic model>",
  "output_and_metric": "<precise output, base loss, and order of aggregation>",
  "guarantee": "<quantifiers for error and runtime cost separately>",
  "resource": "<unit cost of each operation and free computation>",
  "regime": "<accuracy window, dimension, and parameter relationships>",
  "hidden_constants": "<parameters on which hidden constants may depend>"
}
```

The Theorem statement is the canonical source of truth; tags and summaries are derived from it. Different proofs of the same statement may coexist, each marked as source-linked, a sketch, or a complete local argument. A longer stored proof is not automatically more trustworthy.

# Lightweight Source Template

A Source organizes identity and access to the original material. The original PDF / HTML may be stored once, cached on demand, or retained as an accessible remote reference. Do not copy the same full text into every Algorithm, Theorem, or review request.

```json
{
  "bibliographic_identity": {
    "title": "<title>",
    "authors": [],
    "identifiers": {
      "doi": null,
      "arxiv": null
    },
    "version": "<explicit version; state honestly if it cannot be determined>",
    "canonical_url": "<entry point to the original source>",
    "related_versions": []
  },
  "original_material": [
    {
      "format": "<PDF | HTML | text>",
      "artifact_ref": "<actual local file or remote reference to the original source>",
      "content_hash": null,
      "locator_scheme": "<printed pages / PDF pages / anchors / equations>",
      "extraction_notes": "<parsing issues actually observed>"
    }
  ],
  "necessary_context": [
    {
      "name": "<notation / definition / standing assumption>",
      "content": "<only explanations necessary for understanding>",
      "locator": "<location in the original source>",
      "applies_to": "<applicable results or sections>"
    }
  ],
  "coverage": {
    "acquired": [],
    "inspected_anchors": [],
    "extracted_anchors": [],
    "unmapped_relevant_anchors": []
  },
  "corrections_and_supersession": []
}
```

Generate the following from reference relationships rather than maintaining them manually again in Source records:

- The Algorithms, Hard Families, and Theorems extracted from the paper;

- The memory entries corresponding to original Algorithms / Theorems / Equations;

- Current reading links and revisions for each entry;

- The contribution list in the Paper view.

Reading coverage must distinguish bibliographic information recorded, original material acquired, a passage actually read, a result extracted, its statement checked, and a proof passage reviewed. A successful download does not establish that "the entire paper has been verified."

Record version differences, corrections, retractions, or supersession only after actual verification. Content hashes must come from bytes actually acquired, not from model generation.

# Proof Method Template

Proof Methods belong in theorem_library and may initially appear as subsections of proofs; create separate entries only after repeated reuse or when independently valuable for retrieval. A Proof Method describes "how to attempt a proof" and does not carry the semantics of an established Theorem.

```json
{
  "goal_pattern": "<type of proof obligation for which this method is worth trying>",
  "required_inputs": "<required objects, conditions, or primitives>",
  "key_choice": "<choice of potential / coupling / prior / reduction, etc.>",
  "key_relation": "<invariant or estimate to establish>",
  "proof_skeleton": [
    "<what to establish>",
    "<what to control>",
    "<how to obtain the target conclusion>"
  ],
  "transfer_obligations": [],
  "failure_modes": [],
  "worked_proof_refs": [],
  "evidence_note": "<whether actual worked proofs exist or this is a proposed recipe>"
}
```

For example, an entry on the potential method should explain how to choose a potential, which one-step inequality to establish, how to handle residuals, how to convert to the target quantity, and where to find at least one actual worked proof. Recording only the word "Lyapunov" still does not tell a Cell how to use it.

# Browsing and Retrieval by Brain and Cell

## Five Operations Are Sufficient

The following logical capabilities must be provided or adapted by the runtime; this does not imply that MCP tools with these names already exist.

| Operation | When to use it | Returned information |
| - | - | - |
| overview | Available methods are not yet known | A short method directory readable without a scope |
| browse | Comparing approaches for a mechanism or goal | Concept cards, subbranches, and a few actual entry cards |
| search | The knowledge need can already be described | Ranked cards, matching scopes, differences, and unknowns |
| read | Precise understanding or application is needed | Selected record / statement / component / proof, with pagination |
| expand | Inspecting dependencies or related methods | Typed links and corresponding cards, with further expansion as needed |

There is no mandatory overview-before-search sequence. Search directly when the need is clear; browse when exploring a new route. External search is always available, without first exhausting this library.

Retrieval cards are generated from canonical records and may use the following display fields:

```json
{
  "id": "<entry-id>",
  "revision": "<actual revision>",
  "kind": "<type>",
  "title": "<name>",
  "purpose": "<what it helps accomplish>",
  "mechanism": "<core idea>",
  "prerequisites": "<key prerequisites affecting selection>",
  "limitations": "<limitations requiring the most attention>",
  "evidence_note": "<source statement / local argument / outstanding verification items>",
  "matching_scopes": [
    "<variant / claim references>"
  ],
  "why_returned": "<reason for retrieval in this query>",
  "read_refs": [
    "<entry points to the complete record and source>"
  ]
}
```

why_returned belongs to the current query result and must not be written back to the scientific record as a fact.

## Brain Workflow

When starting research, planning the next round, or encountering a blocked route, Brain may, as needed:

1. Extract the research objective and main obstacles from the current profile / assignment; an Atlas ID is not required.

2. Read a short overview or pose a few research questions directly, such as "how can inner error be controlled?" or "what information-hiding mechanism could challenge this upper bound?"

3. Consider directly applicable results, transferable mechanisms, and material that challenges the current route. Entries across TASK boundaries may be consulted.

4. Read the full content of the few entries that materially affect route selection to assess key prerequisites and missing obligations.

5. Give Cell specific proof obligations, pinned references, and necessary material, without forwarding the entire search history or library directory.

Brain need not query the library every round, nor meet a fixed quota such as "select three routes." It may directly organize derivations when it has a new idea.

## Cell Workflow

Cell searches around its current obligation, usually at a finer granularity than Brain:

| Cell | Common search targets | Complementary material also worth consulting |
| - | - | - |
| Upper-bound | Algorithm components, estimators, potentials, analytic Lemmas, cost accounting | Hard Families and proved method limitations |
| Lower-bound | Constructions, oracle realizations, information-to-error, lifting | Algorithms and additional feedback capabilities that defeat the construction |
| Supporting / general | Precise lemmas, conversions, proof methods, definitions | Counterexamples and sensitive boundary conditions |

These are working priorities, not access restrictions. Cell may browse directories and propose new mechanisms, but must not silently change the assignment's objective or information access.

## Save a Short Application Record Before Actual Use

Create records only for material actually adopted or seriously attempted, not for every search card. The record belongs in the current research workspace:

```json
{
  "target_obligation": "<the specific step currently to be proved>",
  "memory_ref": {
    "id": "<entry-id>",
    "revision": "<actual revision>",
    "content_hash": "<provided by tools>"
  },
  "use": "<direct | needs_transfer | inspiration_only | incompatible | insufficient_information>",
  "variable_mapping": "<mapping from the original statement to the current objects>",
  "assumption_checks": [
    {
      "condition": "<key prerequisite>",
      "status": "<established | unknown | contradicted>",
      "evidence": "<current proof or known conditions>"
    }
  ],
  "conversion_obligations": [
    "<necessary Oracle / Metric / Guarantee / Resource conversions>"
  ],
  "retained_material": "<pinned statement, conditions, source locator, and proof entry point>"
}
```

Direct application still requires verification of all conditions. Needs_transfer indicates an outstanding new proof obligation. Inspiration_only may support design but cannot be cited as an established Theorem.

For lower bounds, check the direction of transfer: a lower bound for a large Function Class does not automatically apply to an arbitrary smaller subclass; failure of a fixed Algorithm does not establish an unrestricted lower bound. For upper bounds, establish that the complete algorithm and required primitives are legal and available under the target Oracle, and account for their costs.

Statements, conditions, and sources actually used by Brain / Cell enter a fixed proof package; Verifier must not receive only a hit ID that can change with the next search.

## A Concrete Retrieval Example

Suppose the current research concerns "a noisy bilevel problem not previously in Atlas," with inner-error propagation as the current obstacle:

- Brain may first browse "managing nested errors" and "controlling bias / variance," without restricting search to bilevel problems.

- Transferable components may appear among estimators or tracking methods for single-objective optimization.

- Cell queries a specific obligation, such as "an estimation-error recursion conditional on history," and reads candidate lemmas' exact assumptions.

- If a method requires reuse of the same random sample at two points, while the current Oracle supplies only independent fresh samples, mark the conversion as unestablished.

- Cell may seek alternatives for fresh samples, prove an adapter, or design its own estimator. Semantic similarity does not justify directly applying the original rate.

- A lower-bound Cell may conversely investigate which additional feedback would defeat the proposed construction.

This process first exposes available methods and then assesses applicability progressively; it does not require reading every paper at each start.

# Extraction and Review Agent Instructions

Only two scientific roles are recommended. Curator processes a small batch of contributions from one source version at a time, and Reviewer checks the increment in an independent conversation. The same underlying model may play both roles, but the review context must include the original material and actual proposal, not just Curator's self-summary.

The following two texts may be placed in agents/memory_curator/AGENTS.md and agents/memory_reviewer/AGENTS.md, respectively. Relative paths are resolved from the actual launch directory.

## Memory Curator

```markdown
# Memory Curator

## Responsibilities
Extract reusable Algorithm, Hard Family, Theorem, Proof Method, and Source records from source versions actually read or authorized research results; create tags, use cases, and browsing entry points consistent with the scientific content.

Input profiles need not be in Atlas. Memory is a reference resource and does not restrict Brain / Cell from using external knowledge or creating new methods.

## Read First
- protocol.md: rules for objects, references, review, and publication.
- docs/navigation.md: tags and directories.
- docs/content_standard.md: scientific content granularity.
- instructions/extract_memory.md: the extraction procedure for this task.
- Read only templates required for the current object; do not load the entire library.

## Workflow
1. Verify source identity/version and the actual scope of accessible material.
2. Read the target contribution and its definitions / standing assumptions.
3. Select objects with independent reuse value, rather than mechanically extracting every numbered lemma.
4. Retrieve neighboring entries and decide whether to add a source, add a guarantee, add a variant, add a proof, or create an entry.
5. Write accurate scientific content first, then generate scoped facets, use_when, and mechanism tags.
6. Save a small staging proposal and submit it to an independent Memory Reviewer.
7. Revise affected content using specific feedback; do not reprocess unchanged objects.
8. Complete programmatic validation and publication under existing authorization; otherwise deliver a reviewable proposal.

## Scientific Requirements
- Separate Algorithm rules, constructions, and performance claims.
- Bind performance links to specific variants / constructions and Theorems.
- Do not broaden the lower-bound Algorithm Class or add span or zero-respecting restrictions by default.
- Distinguish method limitations, class lower bounds, analysis gaps, and empirical findings.
- Include all key conditions in Theorem statements; long source proofs may be read as needed.
- Preserve complete local arguments for new normalizations, adapters, or transfers; do not present them as original source conclusions.
- Bind faithfully recorded source concerns to affected claims, without implicating unrelated objects.
- General lemmas need not invent an eight-axis setting.

## Tools and Material
Use the files, sources, memory retrieval, search, and staging tools actually authorized. Tool names and schemas are determined by the runtime. Read as needed; do not supply every source, directory, unread lead, and historical review at once.

Modify only the current staging area. Do not invent source versions, hashes, review IDs, reading coverage, or publication receipts.

## Output
Deliver canonical record increments, source coverage, tag / vocabulary increments, review targets, specific verification items, and actual publication results. Do not claim successful ingestion without a receipt.
```

## Memory Reviewer

```markdown
# Memory Reviewer

## Responsibilities
Review the current proposal's scientific content, evidence descriptions, and navigation in an independent conversation. By default, review the accuracy of extraction and citation; re-proving the entire paper is not required. Do not directly modify the canonical library.

Read protocol.md, instructions/review_memory.md, the actual current proposal, necessary source sections, and dependencies first.

## Assess Separately
1. Content fidelity: whether statements, constructions, conditions, and references are faithful and sufficiently understandable.
2. Evidence and use: what evidence currently exists, and which claims retain specific concerns or transfer gaps.
3. Navigation fidelity: whether tags, cards, and links are accurate, omit important entry points, or broaden scope.

"Faithfully recording a source ambiguity" may pass fidelity review, but affected claims retain usage restrictions. This is distinct from independently proving the claim.

## Review Priorities
- Algorithm core queries / updates, initialization, output, permitted parameter information, and actual variant.
- Hard Family model membership, oracle transcript, information-to-error, algorithm coverage, dimension, and regime.
- Theorem definitions, assumptions, quantifier order, conclusion, and complexity accounting.
- Actual arguments, dependencies, direction, and cost of new local derivations / transfers.
- Tag axis, role, subject, scope, and evidence; do not combine conditions across variants.
- Source identity, version, locator, and actual reading coverage.

## Output
Assign accept / revise / defer to each independent object and describe actual review coverage.
For every issue, provide target, reason, impact, repair, and evidence. An independent subset of objects may be accepted.
Missing JSON fields or invalid pointers require protocol repair; they are not mathematical problems in the paper.

## Revision
Read the current candidate, relevant previous candidate, feedback, and diff.
An earlier issue may be partially resolved; update its remaining impact rather than requiring resolved blockers to remain permanently.
Re-review only changed content and content affected through dependencies. Pure alias / formatting changes do not require reviewing the entire proof again.

## Boundaries
Do not fabricate independent review or formal certification, elevate evidence status merely to pass review, or treat a proof sketch as a complete proof. Publication is handled by deterministic code under existing authorization.
```

Separate agents are not needed for tags, formatting, citations, or each axis. Invoke a specialist proof Cell temporarily only when a difficult and important local proof obligation actually arises; save the result through the ordinary memory proposal process afterward.

# Extraction Workflow and Independent Review

## Workflow

A task proceeds through "locate source → read contributions → select entries → check for duplicates → write content and tags → independent review → local revision → deterministic publication."

Curator may call tools, read originals, query memory, and save results within one conversation before continuing to the next object. Reviewer uses an independent conversation and can also read targeted source passages. The workflow does not rely on one enormous request that generates a complete paper dossier.

## instructions/extract_memory.md

```markdown
# Extract New Memory

## Input
The task should provide source identity/version, an accessible original source entry point, the extraction scope, already completed anchors, publication policy, and the actual output schema.
If only an abstract or search snippets are available, record a reading lead; do not generate a Theorem claiming that all conditions have been verified.

## Steps
1. Read the contribution structure: formulation, main assumptions, Algorithm/construction, principal statements, and proof ideas.
2. Select knowledge objects: prioritize independently usable rules, components, conclusions, transfers, and hardness mechanisms. Do not extract every numbered lemma by default.
3. Add necessary context: definitions, standing assumptions, Oracle timing/feedback, norm, parameter regime, and Metric/Guarantee/Resource.
4. Check for duplicates: screen source+locator, names/aliases, mechanisms, and neighboring statements in parallel; submit a small candidate set to the LLM for judgment.
5. Decide among add/update/variant/proof/application; if equivalence is uncertain, use related rather than forcing a merge.
6. Populate canonical scientific content. Use map+locator for long proofs; store complete arguments for new local derivations.
7. Extract scoped facets, use tags, and mechanism tags. Start with the existing vocabulary; provide definitions and neighboring concepts when extension is necessary.
8. Write a small staging proposal. The program supplies and checks the complete schema, IDs, pointers, versions, and references.
9. Obtain independent Reviewer assessment; revise using local feedback while distinguishing source concerns from extraction errors.
10. Publish small batches with complete dependencies under existing authorization, generate indexes and reading views, and save actual receipts and coverage progress.

## Output Must Enable the Next Stage to Continue
- Added/modified objects and their base revisions.
- Source versions, locators, and actual reading coverage.
- Required dependencies and missing content.
- Tag / alias / vocabulary increments.
- Objects awaiting review and specific issues.
- A natural usage query for every proposed item; add a neighboring query when confusion is a risk.
- A recoverable checkpoint: completed anchors, current object, latest feedback, and next step.

## Special Handling
When PDF superscripts, formulas, quantifiers, or page numbers appear unreliable, verify them against the original page; do not fill gaps from model expectations.
An existing condition was omitted from a candidate: revise the extraction.
The source itself is ambiguous and has been faithfully recorded: mark the local issue unresolved and continue with other independent content.
A transfer is unproved: retain it as a proposed obligation, without upgrading it to an established Theorem.
Missing fields or invalid JSON Pointers: regenerate as a protocol correction, without reporting a flaw in the paper.
Recovery must include the relevant previous candidate and repair feedback; do not repeatedly read rejected outputs as valid cached results.
```

## instructions/review_memory.md

```markdown
# Review Memory Increments

## Input
The current proposal, actual revision/hash, necessary base records, exact source sections, and local proofs/dependencies.
For revisions, include the previous candidate, earlier issues, and latest diff. If material is missing, identify the specific gap instead of guessing.

## Review Content
1. Object identity: whether creating an entry, variant, proof, application, or additional source link is appropriate.
2. Scientific fidelity: accuracy of rules/constructions/statements, conditions, quantifiers, Oracle, Algorithm coverage, Metric, Guarantee, and Resource.
3. Reuse explanation: components must specify inputs, transformations, outputs, prerequisites, costs, and outstanding obligations; attribute inferred mechanisms explicitly.
4. Evidence depth: checking a statement does not mean reading the entire proof; reading a proof is not formal certification. Inspect the actual argument for a new derivation.
5. Navigation: consistency of tag roles, subjects, and scopes; unknown/not_assumed must not become false; do not combine scopes across variants; ensure key uses can be found through directories.
6. References: accessibility of the actual source version, locator, record revision, and dependencies.

## Results
Return accept / revise / defer for each item.
State which statements/proofs/source sections were actually checked.
For each issue, provide target, reason, impact, repair, and evidence.
Independent subsets may be accepted; confine unresolved items to the affected claims/scopes/uses.

## Review Principles
- Do not require rewriting every proof in the literature.
- A record that faithfully documents source concerns may be accepted while restricting use of the affected claims.
- Resolved omissions and unresolved source ambiguities may be updated separately.
- Formatting failures must not be interpreted as mathematical failures.
- Changes only to aliases or display text do not require re-review of all scientific content.
- Do not publish directly or modify canonical records on Curator's behalf.
- Do not substitute "check everything again" for an actionable repair target.
```

Review results may use the following compact format. Open issues are compatible with accepting a record; use impact to identify what they affect:

```json
{
  "proposal_id": "<actual proposal-id>",
  "reviewed_revision": "<actual revision/hash>",
  "items": [
    {
      "target": "<entry-id or specific field>",
      "disposition": "<accept | revise | defer>",
      "content_fidelity": "<verified assessment>",
      "evidence_scope": "<actual scope of checking a statement / partial proof / complete local argument>",
      "navigation_fidelity": "<whether consistent>",
      "issues": [
        {
          "target": "<local scope>",
          "reason": "<specific issue>",
          "impact": "<affected claim/use>",
          "repair": "<minimal repair>",
          "evidence": "<source / argument locator>"
        }
      ]
    }
  ]
}
```

The program checks only whether these outputs connect correctly; it cannot replace LLM judgments about equivalence, applicability, or proof validity. Review also must not automatically mark every claim as independently proved.

# Required Tools and Scalable Operation

## One Shared Set of Tool Capabilities Is Sufficient

| Capability | Purpose |
| - | - |
| Literature discovery and original source acquisition | Web / scholarly search, paper pages, original PDF/HTML material, and versions |
| Targeted Source reading | Read specified sections / theorems / pages; inspect original formula pages when necessary |
| Memory overview / browse / search / read / expand | Discover and read knowledge progressively |
| File and staging read/write | Save small batches of records, local proofs, checkpoints, and revisions |
| Programmatic validation and index construction | JSON, pointers, references, revisions, atomic publication, and derived views |
| Optional computation / proof tools | Support algebra, numerical counterexamples, or formal checks; support only conclusions actually covered |

MCP is one integration mechanism. A separate MCP is not needed for every agent; agents may share tools while having different write permissions. Only Curator writes staging; Reviewer writes reviews; the publisher updates canonical memory using deterministic rules.

Generation requests should include the templates and output schema actually used by the task. Do not merely say "use the same format as before," and do not repeatedly include schemas for unrelated types.

## Avoiding Input Growth

Each model request contains only the current objective, necessary specifications, current entry or diff, a few candidate cards, source fragments actually needed, and the latest unresolved issues. Store other material as readable references.

Do not pass original texts, bibliographic leads, the full-library index, historical identity-exclusion records, or all reviews downstream as a general payload. Keep unread leads in the queue and completed reviews in audit storage; downstream stages receive only actual dependencies.

read must support selection / pagination and report completeness and continuation entry points. If the token budget is insufficient, split contributions or proof obligations; do not truncate necessary conditions and then claim the Theorem is complete.

## Organizing Thousands of Papers

1. Extract a source registry from Atlas evidence references, deduplicating by stable bibliographic identity while retaining actual source versions.

2. Track read, extracted, and unprocessed anchors for each source version. Work by source rather than rereading the same paper for every profile.

3. In the first pass, prioritize claims used in existing brackets, core Algorithms / Hard Families, and broadly reusable lemmas; do not first extract every lemma from every paper.

4. Add new source / theorem links for the same method; add a variant only for a new rule; add proofs for the same statement.

5. Actual Brain / Cell needs may trigger a second, closer reading. Material with an existing Source but no extraction should be shown honestly in directories as a reading entry point.

6. Review small batches and give item-level decisions. Start with a few independent knowledge objects per paper and process long papers in further batches; this is a working budget, not a reason to omit other contributions.

7. Preserve reusable query examples and assess navigation quality using actual retrieval and misuse cases, rather than checking field completeness alone.

8. When a new version, correction, or claim issue appears, mark affected records along explicit dependencies while retaining the versions used by earlier proof packages.

This design does not require a large graph database or many microservices upfront. First connect canonical records, cards, the controlled vocabulary, the five read operations, and the two agents; replace the underlying index only when performance bottlenecks arise.

# Complete Example: From Function Gap to Gradient Norm

This example illustrates why complete conditions, use tags, and Oracle tags must remain separate. It is an educational example, not a claim of novelty or published memory; no literature references or review IDs have been fabricated.

## Statement

Let f be continuously differentiable on the entire Euclidean space, with a globally L-Lipschitz gradient, L > 0, and a finite global infimum. For every x:

```math
\|\nabla f(x)\|_2^2\le 2L\bigl(f(x)-f_*\bigr),\qquad f_*:=\inf_{z\in\mathbb R^d} f(z)>-\infty.
```

Neither convexity nor attainment of the infimum is required.

## Complete local proof

Let g be the gradient at x and d = -g/L. The integral representation and Lipschitz condition give:

```math
\begin{aligned}
f(x+d)-f(x)
&=\int_0^1\langle\nabla f(x+td),d\rangle\,dt\\
&\le\langle g,d\rangle+\int_0^1 Lt\|d\|_2^2\,dt\\
&=-\frac{\|g\|_2^2}{2L}.
\end{aligned}
```

The statement follows by observing that the global infimum is no greater than f(x+d).

Thus, if epsilon is nonnegative and the function gap is at most epsilon squared divided by 2L, the gradient norm is at most epsilon. This is a pointwise implication; changing only the Guarantee tag cannot convert it into another aggregation form.

## Storage and Retrieval

| Content | Correct record |
| - | - |
| kind | theorem / analytic Lemma |
| Purpose | Function-gap to gradient-norm conversion |
| MODEL | Global gradient Lipschitzness, Euclidean geometry, unconstrained full space, finite global infimum |
| Convexity | not_assumed; this does not mean "the function must be nonconvex" |
| METRIC | Function gap, squared gradient norm, and the proved direction of conversion |
| ORACLE | Not applicable to this analytic statement; the appearance of a gradient does not require a gradient Oracle |
| Proof | Short complete local argument |
| Usage restrictions | No universal reverse conversion follows under these assumptions; a global gap cannot be replaced arbitrarily by a constrained gap |

## An Example That Helps Cell Detect Misuse

Take f(x) = (x+1) squared divided by 2 and the constraint set D = [0,∞). The function has L = 1 and is globally lower bounded on the full real line, but at x = 0 its constrained gap is 0 and its gradient norm is 1.

Replacing the global infimum with the constrained infimum therefore invalidates the conclusion. Explicitly recording the full-space assumption in the Source / Theorem directly prevents this misuse.

A Cell with only a value Oracle may still use this lemma for mathematical analysis. Whether it can implement a particular Algorithm, estimate the gradient, or attain the required function gap must be proved separately for the specific Algorithm and Resource.

# Launching an Extraction Task

Curator may be launched directly by the existing scheduler, Brain, or a human. The scheduler supplies the task, tools, and working directory without replacing scientific judgment. The following request skeleton and two ready-to-use task prompts use fields subject to the actual runtime.

## Job Template

```json
{
  "source_ref": "<source ID, explicit version, and original source entry point>",
  "objective": "Extract knowledge objects worth retaining for long-term reuse, and add source or result references to existing objects.",
  "focus_anchors": [],
  "already_completed_anchors": [],
  "memory_access": "<retrieval and reading tools actually callable>",
  "staging_target": "<storage location for this proposal>",
  "publication_policy": "<actual existing authorization for this task; the model must not elevate it>",
  "required_outputs": [
    "canonical_records",
    "navigation_changes",
    "source_coverage",
    "review_targets"
  ],
  "output_schema_ref": "<actual schema for this task; provide the required content during generation>"
}
```

## Curator Launch Prompt

```text
Work as Memory Curator.
Read the specified AGENTS.md, protocol.md, extraction instructions, and current object template.
Use the source version specified in the job; the source need not correspond to an Atlas setting.
Read the main contributions first, then select independently reusable objects; continue reading the original as needed for each object.
Use memory tools to check for duplicates and decide how to update; a failed retrieval is not proof of novelty.
Preserve accurate scientific content first, then extract tags and browsing cards; save staging in batches.
After completing a batch, invoke an independent Reviewer and revise using local feedback.
Invoke publication tools when existing authorization and validation conditions permit; otherwise return a reviewable proposal.
Report work actually completed, unfinished anchors, and receipts; do not describe planned actions as completed.
```

## Independent Reviewer Launch Prompt

```text
Review this proposal as an independent Memory Reviewer.
Read Reviewer AGENTS.md, protocol.md, review instructions, the actual proposal, and necessary source sections.
Assess content fidelity, evidence/use scope, and navigation fidelity separately.
Do not read only Curator's explanation; read the original material and dependencies directly when needed.
Assign accept/revise/defer item by item, reporting local issues, impacts, and minimal repair targets.
Faithfully recorded source concerns may coexist with accepting a record, but the corresponding claims must not be upgraded to proved status.
Do not publish or modify canonical records; return a review of the actual current version.
```

A run may pause after any saved object without waiting for extraction of the entire paper. To continue, read existing coverage, the current proposal, and the latest diagnostics; the full historical material need not be supplied again.
