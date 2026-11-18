# Joint-parameter synthesis standard, version 2

Apply this standard to every maintained setting. It augments the existing scientific contract; it does not change the task/oracle/model or approve an old theorem.

## 1. Define the target before comparing rates

Identify the minimax quantity, algorithm/guarantee view, resource projection and full admissible domain. State which variables vary jointly in the primary complexity question. A dimensionless accuracy variable may replace scale and precision parameters only with its definition and scaling justification.

- `joint_variables`: variables whose dependence is optimized jointly.
- `normalized_variables`: symbols, definitions and exact native parameter references.
- `fixed_parameters`: structural parameters fixed for each theorem, with their domain and native reference when present.
- `uniform_in`: parameters excluded from hidden constants; include every joint variable.
- `allowed_constant_dependencies`: declared fixed parameters permitted in hidden constants.

For native parameters, prefer their exact canonical IDs from `/parameters` in `joint_variables` and `uniform_in`. An accepted display symbol or source parameter ID must be copied exactly; do not invent ASCII transliterations, abbreviations or renamed aliases. A new coordinate must have its own `normalized_variables` entry, exact `parameter_refs`, definition and scaling justification before it is used. Keep readable notation in the explanatory text. Resolving target references does not authorize changes to native parameter identities or the quantity's scientific contract.

Recording a parameter is different from studying its joint asymptotics. “For every fixed structural value, constants may depend on that value” is weaker than uniformity over its domain. Do not hide dimension, precision, confidence, condition number or any other joint variable in an undeclared constant.

A precision-independent rate can be correct on a proved zero-query or finite-dimensional saturation region. Keep that region's full joint predicate visible; do not force every formula to contain every parameter.

## 2. Give each region its mathematical role

Regions lie inside the fixed target domain. Do not expand the contract merely to add an endpoint. Distinguish:

| Boundary or region | Meaning |
| --- | --- |
| Source applicability | Where a source theorem and its conversion are known valid. |
| Envelope crossover | Where an eligible term starts to dominate another; possibly asymptotic. |
| Saturation/endpoint | Where the task is trivial, exactly reconstructible or enters another proved branch. |
| Slice | An imposed parameter relation, useful diagnostically but lower-dimensional than the joint target. |
| Unassessed complement | Target parameters whose bounds have not been sufficiently assembled or verified. |

Do not call a source's sufficient dimension restriction an intrinsic phase transition without a separate argument. Retain guards inside min/max envelopes. Compact guarded expressions are acceptable; unnecessary splits at every source constant are not required.

`domain_map` gives cells, their comparison IDs and assessment states, plus `residual_domain` and `partition_argument`. `status: accounted` means the whole target domain is accounted for, possibly with explicitly unassessed cells. `partial` and `unknown` preserve the remainder honestly. Disjointness and coverage are mathematical assertions for review, not conclusions of a string validator.

Distinguish missing registered bounds, a quantified gap between compatible bounds, an unassessed region and an invalid/inapplicable source. A finite search does not prove universal absence of a theorem.

## 3. Keep fixed-parameter slices secondary

A row imposing a relation such as `epsilon = c * g(d)` with fixed `c` uses `role: slice`, its exact `slice` relation, local `fixed_parameters`, `constant_dependencies` and the permitted range of `c`. Keep the joint target primary.

Do not substitute a varying expression for `c` into an `O_c` statement and then treat its constant as uniform. Extending a slice requires explicit constant dependence or a uniform theorem. A gap ratio may legitimately cancel precision while the upper/lower complexities retain it; display the ratio separately from query costs.

## 4. Recompute guarded envelopes from old and new claims

For each affected comparison, account for mechanically compatible candidates from the catalogue and actual profile. In `bound_uses`, mark every candidate `included`, `dominated`, `inapplicable`, `incomparable` or `unresolved`, with `validity_region`, `adopted_region`, reason and any `mapping_proof_refs`.

Mechanical compatibility only locates candidates. Scientific inclusion requires the right model, algorithm scope, guarantee, output, quantity, resource and region. Do not merge distinct quantity/resource IDs by labels. A reviewed equivalence transfer must explain direction, cost and guard.

Write separate `upper_envelope`, `lower_envelope` and `gap`. Identify newly closed subregions when justified. For zero-cost regions, report the exact cost and an inapplicable ratio rather than division by zero. Numerical probes can expose errors but cannot certify uniform dominance or coverage. Excluded candidates must not appear in native active bracket-reference fields.

## 5. Separate provenance, validity and actual impact

Each new/changed adopted bound records an origin: `source_theorem`, `subclass_transfer`, `oracle_reduction`, `analyst_derivation` or conditional `retained_baseline`. Include source/proof IDs, theorem/version locator, source domain, target validity domain and mapping. A lower-bound subclass transfer must establish inclusion and preservation of queries, outputs, guarantees and cost; do not add subclass properties to the target assumptions.

Each material finding has an `impact` record: old/new envelopes, validity region, actual improvement region, unchanged region, witness, boundary type and argument. Classify main bound improvement, zero-query endpoint, `nontriviality_only`, domain extension, correction, synthesis-only clarification or no effect. A valid at-least-one-call statement must not be presented as advancing the main rate when it does not.

Use `boundary_type: exact` only with supporting constants and inequalities. Otherwise mark asymptotic crossover scales separately from exact source activation thresholds. A result may be valid widely, improve only in a narrower window and be dominated again at more extreme parameters. Explain each relevant window. Equal gap labels do not imply equal envelopes.

## 6. Handoff, normalization and completion

Submit `joint_analysis_json` with version, target, domain map, comparison syntheses, provenance, impacts, normalization requests and pending obligations. Exact field names and types follow the complete supplied `joint_analysis.schema.json`. In first annotation, no existing analysis or generic template is supplied; construct it from the frozen original profile and catalogues without requesting a skeleton. When an existing `joint_analysis_template` is supplied, read it completely, preserve unaffected records and revise only with justified statements. Bounded objects with `provided_complete: false` contain pointers, not a complete analysis; follow the stated artifact/pointer by pagination. Absence is not a `provided_complete: true` assertion. The proposed review copy is at `prepared` `/joint_analysis` when omitted from initial input, and its complete read remains required.

The analysis must agree with native bracket records. It cannot approve a claim, repair an inconsistent inequality through prose or merge scientific identities. A presentation-only finding can reorganize the interpretation of retained data but cannot justify changed scientific rows, guards, envelopes or statuses. Mixed batches are allowed: separate source-backed or derivation-backed findings cover every scientifically affected comparison, with auxiliary presentation findings supporting the remaining synthesis. Necessary metadata normalization is explicit and preserves stable IDs. Only the controlled quantity-metadata path can change tracked/fixed parameter roles or analysis scope; other scientific definitions stay fixed. Keep unresolved requests pending.

The reviewer checks parameter roles, guarded envelopes, domain accounting, improvement regions, provenance and display consistency on the frozen prepared analysis. The controller checks structure, references, hashes and workflow; it does not prove arbitrary symbolic inequalities.

A coherent supported partial change may proceed while unrelated work remains pending. Complete finite maintenance requires the actual search scope finished, required comparisons synthesized, necessary normalization resolved and no unresolved plausible material lead. Known gaps can remain. A completed maintenance step is not a solved setting or exhaustive literature certificate.

## 7. Structured synthesis and publication (version 2)

Every new handoff uses the complete current structured schema. A legacy baseline remains a conditional historical record with `legacy_unknown` synthesis coverage; reading or retaining it is not a new completion certificate. Add the required structured fields without silently recertifying earlier source claims.

`synthesis_coverage` separates `gap_basis: registered_envelope` from `literature.status` (`finite_scope_complete`, `partial`, or `not_assessed`) and its explicit finite `scope`. A registered-envelope gap compares recorded compatible bounds; it is not proof that literature or available derivations have been fully assembled. Its `status` is `complete`, `partial`, or `unassessed`.

Within affected `comparison_ids`, record structured obligations, with native bound/cell/proof refs, `argument`, `state` (`resolved`, `pending`, `not_applicable`) and `affects_gap`:
- `compatible_candidates`: assess every selected/eligible compatible candidate, overlaps and guarded envelopes.
- `replacement_branch`: after an old selected claim is withdrawn or excluded, assess the remaining compatible branch; do not stop at removing the bad term.
- `resource_projection`: assess an available claim on a different quantity/resource for a valid directional transfer. A sum-resource necessary inequality can follow from a component inequality only with an explicit proof; differing IDs remain distinct. Upper bounds on components achieved by different algorithms cannot be added to assert a common algorithm.
- `closed_region_publication`: make a derived closed region native, or keep publication pending.
- `material_lead`: retain each exact textual `pending_obligations`/`scope.unresolved_leads` string as its `lead`, pending with its effect on the registered gap stated. Do not erase an unprocessed GAP-changing route by calling the current envelope fully synthesized.

The controller enumerates bounded opportunities, not all possible mathematics. Identify further affected projections, replacement branches and material routes yourself. A reasoned `not_applicable` judgment must explain the contract/guard obstruction. A pending obligation must remain visible in `pending_obligations`; complete synthesis and no-change cannot contain pending obligations. Supported partial adoption is permitted when the pending route does not undermine the proposed claim, but it does not advance a successful complete-maintenance watermark.

Every domain cell states `closure`, `publication`, and `closure_proof_refs`. `publication` records publication of the claimed matching upper/lower closure, not merely the existence of a native comparison. Use `closure: established` only for a proved matching upper/lower bracket. With `publication: native_comparison`, link nonempty native `comparison_ids` whose status is optimal, plus the decisive native proof IDs. An established region without a native comparison is `publication: unpublished`, with a pending `closed_region_publication` obligation and partial synthesis. Do not say a native bracket has closed merely because prose or a domain cell derives it. `closure: not_claimed` requires `publication: unassessed` and an empty `closure_proof_refs` array, including for cells linked to existing native comparisons; textual claims must agree with these fields.

`impact.kind: domain_extension` asserts a strict extension beyond the old certified domain. Supply `extension_witness` with old/new domains, an explicit `outside_old_witness`, its membership/nonemptiness argument and native `proof_refs`. Independent review must prove these assertions and any constant uniformity. Registering a valid new regional or saturation comparison without a proved old-domain-exterior witness uses `explicit_region_registration`, with `extension_witness: null`; this does not assert strict improvement or extension. Other kinds also use null. Structural validation never solves symbolic dominance, feasibility or nonemptiness.

A full complete/no-change assessment requires complete structured synthesis, complete finite literature scope and the unchanged actual search/read gates. The six independent joint checks include these obligations and publication/witness claims; no third model role is introduced.
