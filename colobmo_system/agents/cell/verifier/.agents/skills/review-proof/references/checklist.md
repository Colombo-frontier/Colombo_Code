# Mathematical Proof Checklist

Source: user-supplied `Mathematical_Proof_Checklist.md`. The original checks and reference numbers are retained below. This material is used on demand to investigate omissions, not as required report fields; its reference numbers are unrelated to this proof's check IDs. Inapplicable methods require no records.

This is a general mathematical proof checklist addressing mathematical content only. Sections on limits, probability, and similar topics apply only when the proof uses the corresponding methods.

**First, establish exactly what must be proved and which assumptions may be used.**

| # | Check | Specific Questions |
|---|---|---|
| 1 | **Is the target statement clear?** | Are the objects, scope, and conclusion to be proved clear? Is any key formulation ambiguous? |
| 2 | **Are definitions and notation consistent?** | Is every symbol defined? Does a symbol change meaning partway through? Are similarly named definitions incorrectly treated as equivalent? |
| 3 | **Are the assumptions complete and respected?** | Does every condition used in each step follow from the original assumptions or an established result? Have stronger conditions been silently introduced? |
| 4 | **Are the quantifiers correct?** | Is “a choice exists for each object separately” confused with “one choice works for all objects”? For example, $\forall x\,\exists y$ versus $\exists y\,\forall x$. |
| 5 | **Are parameter dependencies valid?** | Which parameters may constants, thresholds, and auxiliary objects depend on? Is a constant depending on $n$ treated as independent of $n$? Is information used before it is determined? |

**Then check step by step whether the argument actually holds.**

| # | Check | Specific Questions |
|---|---|---|
| 6 | **Is the direction of inference correct?** | Is a necessary condition treated as sufficient? Is $A\Rightarrow B$ treated as $B\Rightarrow A$? When equivalence is claimed, are both directions proved? |
| 7 | **Are key steps justified?** | Is there sufficient justification between adjacent steps? Can arguments omitted as “obvious”, “easy to obtain”, or “proved similarly” actually be supplied under the current assumptions? |
| 8 | **Have intermediate conclusions been established?** | When a lemma or claim is used, has it been proved or supported by reliable external grounds? Is something still to be proved treated as an established fact? |
| 9 | **Is there circular reasoning?** | Does a lemma depend directly or indirectly on the final conclusion to be proved? Do intermediate conclusions support one another without an independent starting point? |
| 10 | **Is the proof method used correctly?** | Does induction have a base case and invoke only permitted earlier cases? Does proof by contradiction negate the correct target? Is choosing a minimal counterexample justified? |
| 11 | **Is the case analysis complete?** | Are all possible cases covered? Are equality, endpoints, zero values, the empty set, singular cases, or minimum parameter values omitted? Are conditions local to one case misapplied to another? |
| 12 | **Are reductions and “without loss of generality” valid?** | Does simplification preserve the necessary assumptions and conclusion? Can the reduced problem be connected back to the original? Does the claimed symmetry actually exist? |

**Check constructed objects and computations separately.**

| # | Check | Specific Questions |
|---|---|---|
| 13 | **Does the object exist?** | Does the object used actually exist? Can the construction be carried out? Can a recursive construction proceed at every step? |
| 14 | **Does the object have the required properties?** | Even if it exists, has it been proved to satisfy every property subsequently used, such as membership in the required set, compliance with constraints, or the required regularity? |
| 15 | **Is the construction well-defined?** | Does the definition produce a definite and meaningful result? Is the result consistent across different representatives or decompositions? If multiple choices are allowed, does the argument hold for the choices required? |
| 16 | **Are the algebra and calculations correct?** | Are expansions, rearrangements, substitutions, derivatives, and sums correct? Are any terms, coefficients, or signs missing? Is the direction of each inequality preserved correctly? |
| 17 | **Is every operation valid?** | Are denominators nonzero? Are the conditions for square roots, logarithms, and inverses satisfied? Does squaring or elimination introduce extraneous solutions that must be checked by substitution? |
| 18 | **Are conclusions of different strengths confused?** | Existence does not imply uniqueness; existence of an infimum does not imply attainment of a minimum; finding a candidate does not prove its validity; finding one solution does not characterize all solutions. |

**Pay particular attention to the following when passing from local to global or from approximate to exact statements.**

| # | Check | Specific Questions |
|---|---|---|
| 19 | **Does a local conclusion imply the global conclusion?** | Can a local property extend over the entire domain? Are different local constructions compatible? Is a stationary point or local optimum mistaken for a global optimum? |
| 20 | **Is pointwise validity mistaken for uniform validity?** | Does validity for each object separately suffice for an estimate, threshold, or error bound that holds uniformly over all objects? |
| 21 | **Is interchanging operations justified?** | Are the relevant conditions satisfied when interchanging limits, infinite sums, integrals, derivatives, expectations, suprema, or other operations? Formal similarity of expressions alone does not justify interchange. |
| 22 | **Are requirements preserved in the limit?** | Does the sequence actually converge, or does the required subsequence exist? Does the limit remain in the required set? Do the original constraints and properties pass to the limit? |
| 23 | **Does an approximate conclusion imply an exact one?** | Does arbitrary closeness actually imply equality or existence? As the error decreases, do the compared objects remain fixed, or do they change as well? |
| 24 | **Are bounds and asymptotic statements accurate?** | Are inequality directions, rates, constants, and parameter ranges correct? Are dimension dependence, logarithmic factors, or necessary thresholds omitted? |
| 25 | **Do probability statements match?** | Are expectation, high probability, almost-sure validity, and validity for every outcome confused? Are the conditions for independence, conditioning, or simultaneous control of multiple events satisfied? Are parameter-dependent exceptional sets handled? |

**Finally, verify external grounds and the final conclusion.**

| # | Check | Specific Questions |
|---|---|---|
| 26 | **Are cited results accurate?** | Does the original source actually contain the cited statement? Have hypotheses been omitted, quantifiers changed, or a conjecture treated as a proved theorem? |
| 27 | **Are cited results applicable?** | Do the definitions, objects, assumptions, and parameter ranges of the original theorem match the current setting? |
| 28 | **Is the transition from the citation to the current conclusion valid?** | Even if the theorem is cited correctly, are the specific specialization, parameter substitution, and subsequent deduction still correct? |
| 29 | **Does the evidence support the claimed conclusion?** | Are examples, numerical experiments, or finitely many checks mistaken for a general proof? When numerical computation is used, are rounding errors and computational precision controlled? |
| 30 | **Does the final conclusion match the original objective?** | Has only a special case, weaker statement, or version under additional assumptions been proved? Have all parts of the original objective been completed? |

Retain room for judgment on three points when using this checklist:

- **An unused assumption does not automatically indicate an error.** It may be redundant, or it may suggest an omitted argument.
- **An unwritten step does not automatically constitute a substantive gap.** Assess whether the step can be supplied directly from the available assumptions.
- **Failure to locate a citation does not automatically mean it is fabricated.** Distinguish “not yet verified” from “a discrepancy has been found”.
