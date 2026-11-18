# Short Proofs, Applicability Transfers, and Bracket Synthesis

Investigate the strongest supportable bracket as of the research cutoff, within the specified contract and region, rather than merely extracting the triggering paper. A finite investigation is not an exhaustive literature survey; record the sources covered and the scope not yet examined. Read [evidence.md](evidence.md) first and save formal work as atomic result/proof artifacts.

## 1. Short derivations to prioritize

Check zero-query bounds, exact reconstruction, simple baselines, accuracy monotonicity, coarse-accuracy clipping, parameter reselection, dimension padding/embedding, upper/lower envelopes, saturation, and degenerate cases first. Existing material may close an apparent GAP through these arguments. Prioritize obligations that change the main bracket or applicability domain and allocate a finite research budget. If a proof cannot be completed, save the precise missing step and continue with independent results.

Every proof must state the exact proposition; all premises and objects; the derivation; dependencies of parameters and constants; boundary and degenerate cases; the mapping back to target instances and probability/cost quantifiers; and its source/result dependencies. Do not replace the decisive step with “standard argument” or “it follows readily.”

A randomized adaptive exact-query lower bound cannot rely solely on having more unknowns than equations. Conditional-distribution or integration arguments must explain independent random seeds, adaptive conditioning, residual uncertainty, fixed worst-case query budgets/early stopping, and the quantifier conversion from a distributional statement to per-instance success. Check joint measurability when the argument requires it. It is not a span, continuous-update, or finite-bit restriction; the source need not contain that literal term, and the condition must not be silently added to a frozen specification.

A counterexample to an auxiliary lemma refutes that formulation alone. Assess consequences for the main theorem from its actual dependencies and any repair or alternative argument. Isolate scientific disputes at the bound level.

## 2. Applicability-transfer checklist

Every `analyst_transfer` must specify the source contract and parameter domain; target contract and parameter domain; instance map; query simulation; output/error conversion; all costs; algorithm and probability quantifiers; and valid endpoints.

- **Direction:** use the correct direction for accuracy relaxation/tightening and containment of stronger/weaker models or algorithm classes. A deterministic lower bound does not cover general randomized algorithms.
- **Metrics/guarantees:** convert distances/squared distances, expectations/fixed probabilities, high-probability/simultaneous events, and different notions of regret or gap only with a proof.
- **Dimension:** if the source theorem holds only on a lattice or accuracy-dependent sequence, explain whether padding preserves structural promises and how the remaining dimensions/parameter windows are handled.
- **Fixed public objects:** determine whether a mask, graph, or distribution is an arbitrary fixed input or part of the outer worst case. Constructing one hard mask does not prove a lower bound for every fixed mask.
- **Native capabilities/costs:** when a stronger interface simulates a weaker one, state the extra capabilities and exact call counts. Include preprocessing, reuse, parallelism, and communication costs.
- **Geometry/existence:** preserve norms, feasible domains, regularity, and solution-existence promises under the map. Do not hide dimension dependence in constants.

If a transfer requires supplementing the common specification, propose a specification revision and obtain a new review first. Do not rewrite an identity conclusion during research.

## 3. Synthesizing a bracket

For admissible results within the same setting/view/guarantee/quantity/resource projection/valid region, take the minimum upper envelope and maximum lower envelope. Prove applicability before adding a result to an envelope. Do not forcibly scalarize incomparable guarantees, multi-resource vectors, or different success probabilities.

Partition the covered regions explicitly. Check overlaps, intersections, accuracy endpoints, coarse accuracy, small dimensions, degenerate instances such as empty/full support, zero queries, reconstruction saturation, infeasibility, and impossibility. Preserve provenance separately for the source theorem's original window and every proved extension. Reader tables may merge commonly closed windows, but retain separate rows where algorithms/views differ.

Claim optimality or near-optimality only when the declared comparison variables, constant dependence, and quantifiers agree. Theta-optimality is not an exact equality. A missing side does not imply a positive GAP. Logarithmic and polynomial gaps require an actually comparable ratio scale and region; do not infer a global gap from one row's rate.

## 4. Reasons for a remaining gap

A regime may have multiple `gap_causes`: `mathematical_gap`, `literature_pending`, `proof_verification_pending`, `applicability_pending`, `specification_unresolved`, and `unassessed`. An empty list or missing legacy field does not establish optimality. `mathematical_gap` means that the currently admissible results leave a gap at the declared scale; it does not certify a recognized open problem in the field.

For every unclosed region, explain which upper/lower bounds and proofs are used, their coverage, the precise missing information, and the most valuable next step. “Endpoints checked” or “left to future research” is not an adequate explanation.

## 5. Updates and new settings

For an update, first fix the old profile's scientific version. Preserve existing IDs, aliases, evidence, and unchanged windows. Report the actual delta: no change, new evidence, a stronger/weaker applicability domain, a new view, a new regime, or a changed bracket. A stronger deterministic witness does not necessarily require a new view.

A new setting requires investigation of the direct literature and reasonable neighboring directions, producing a self-contained specification, both tag representations, the current bracket, evidence, and coverage notes. Report Missing bounds honestly when a reliable lower or upper bound is unavailable; do not invent results to fill a table. The reviewer must also ask whether existing evidence supports a stronger envelope and whether an apparent GAP merely reflects an omitted short synthesis.

## 6. Concentrated review of coverage obligations

The coverage protocol records this work in `coverage_ledger`/`coverage_audit`. List the nine checks and their formal support under the fixed contract, views, regimes, and research-cutoff scope first. A generic “endpoints checked” is insufficient. The first review must consolidate all discovered actionable obligations; revisions must respond to them individually. The second review follows the differences. New coverage blockers must identify new evidence or a first-review omission and the exact missing proof step. Any new counterexample, source error, or applicability error must still block the affected adoption.

A finite investigation cannot guarantee discovery of every potential new algorithm. Directions outside the stated scope may be explicitly marked `unassessed`/follow-up with later work retained; they cannot simultaneously be described as globally strongest or literature-exhaustive. A known short synthesis from current material that changes a claimed gap, optimality status, or envelope still requires a formal proof/result and independent review. The ledger is neither a reason to omit that work nor an automatic approval.
