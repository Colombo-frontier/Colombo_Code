# Lower-bound review supplement

Apply this supplement within the assigned proof/audit scope and during independent report confirmation. The runner authenticates the workspace copy against the installation-owned pack and freezes it with review evidence. Reviewers receive `input/lower_bound_review_guidance.md`; local auditors and challenge reviewers receive `lower_bound_review_guidance.md`.

## Check the Claim and quantifiers

A proved Lower-bound Claim is normally supported, not refuted. Identify whether the actual Claim concerns a fixed Algorithm, restricted Algorithm Class or the full admissible class. Compare the actual conclusion with the assigned responsibility; a narrower result may be valid partial progress without completing the original Task.

Check the order of Algorithm, instance, Oracle and randomness quantifiers. In a standard fixed-instance randomized setting, the instance may depend on the Algorithm's distribution and public parameters but must not be chosen after observing its realized private randomness. Check any distributional-to-worst-case transfer. For adaptive constructions or resisting Oracles, verify the model's required consistency/realizability; do not assume an arbitrary adaptive answer sequence comes from an admissible fixed function. Apply the actual Task's adversary model rather than imposing a stronger one.

## Check construction, information and output scope

Check Family membership, initialization, normalization, dimension and parameter regime. For a fixed-Family Task, follow that construction; for a design Task, trace the actual final variant through the Proof and all dependencies. A fixed-Algorithm bad instance or a raw zero-chain property does not establish an unrestricted randomized Lower Bound by itself.

Check the full Oracle interface, query domain, feedback, sample coupling and cost convention. A proof that omits informative values, assumes unrequested noise/finite precision, or restricts allowed adaptive queries needs a valid transfer Argument. Inspect any claimed lift beyond zero-respecting/span/deterministic restrictions, including control of queries outside the region where the mechanism was proved.

Verify that the obstruction implies error for the permitted Output, including an arbitrary unqueried output when allowed. Check the conversion from information/progress to the requested Metric and then to the counted Resource; expectation and high-probability guarantees are different. Retain necessary dependence on dimension, accuracy and other parameters. Do not multiply independent Lower Bounds without a joint Argument.

## Check closure and evidence

Inspect the actual composition to the parent Claim. Completed work, a constructed Family, nonempty evidence refs or child certification do not replace correctly scoped closing Arguments and parent audit after import. Missing lifting or output conversion remains a gap even if all available local properties are proved. An Algorithm beating one candidate Family does not alone refute a class-wide Lower Bound over a larger Function Class.

Use authorized fixed source content and its actual scope. Library status is not current-task certification; a live ref is not missing proof content. Do not demand re-proving every properly cited external Theorem, but check the statement, conditions and application needed here. Empirical failures and unsuccessful proof attempts do not prove impossibility.

Report the precise unsupported step and its effect on the assigned conclusion. In report confirmation, check the alleged error against the same frozen Claim, construction and evidence rather than repeating the review's labels. Preserve the existing verdict, confirmation, challenge and handoff semantics; this supplement adds no review stage or automatic mathematical verdict.
