# Executed small-instance checks

`exact_check` executes rational arithmetic without shell access, arbitrary code, filesystem access, or network access. A receipt proves that the stated calculation ran. It does **not** prove that its formulas faithfully represent a source algorithm, exhaust all cases, or establish a theorem. The independent reviewer remains responsible for those questions and for the full mathematical argument.

For an adopted oracle simulation or branch-dependent constructive reduction, choose small legal instances that exercise each branch and selection/tie behavior. Derive the true response from the underlying instance independently of the proposed simulation. Check every returned component and its required legality, not just the final rate or query count. Include off-domain queries or other exceptional cases when the contract permits them. A failed equality or supporting inequality is a reason to investigate and, if it applies to the adopted argument, to reject or repair that argument. Do not certify a failed calculation because its asymptotic conclusion is plausible.

Call `exact_check(label, program_json, evidence_refs)`. Include the exact formal proof being checked in `evidence_refs`; source/result refs may supplement it. All refs must already be authorized. `program_json` is an object with two arrays:

```json
{"steps":[{"name":"total","expr":["add","1/3","1/2"]}],
 "assertions":[{"id":"rational_sum","left":{"var":"total"},"relation":"eq","right":"5/6"}]}
```

Expressions are integer or rational/decimal string literals, `{"var":"previous_step_name"}`, or arrays `[operator, operands...]`. Operators: `add`, `sub`, `mul`, `div`, `pow` (integer exponent from -16 to 16), `abs`, `min`, `max`, comparisons `eq/ne/le/lt/ge/gt`, and lazy `if` with condition/true/false expressions. Comparisons return booleans for `if`; arithmetic and assertions use rational values. Variables refer only to earlier uniquely named steps. There is no implicit float conversion, external lookup, random sampling, or symbolic theorem prover. Limits: 64 steps, 64 assertions, depth 16, 4,000 evaluated nodes, 4,096-bit numerators/denominators, and 32,000 program characters.

The tool returns `check_ref`, `all_passed`, and failed assertion IDs. The full immutable result includes every intermediate value, input program, exact assertion operands, and original evidence refs. Read it with `artifact_get` or `read_batch`. Save both failing and repaired executions; never replace a failure with only the successful test. The program must test the actual submitted construction. A revised proof gets its own receipt bound to its new proof ref.

In scope contract occurrence-bound-scope, each independent proof credential declares `execution_check = {required, reason, check_refs}`. The reviewer determines applicability; genuinely nonconstructive arguments may explain why a finite rational experiment is inapplicable. When required, cite successful receipts executed by an independent reviewer and inspect the exact programs and their limits. Historical receipts may be reused only from a completed independent proof credential, with the separate unchanged-proof/context requirements still satisfied. Neither empty refs nor a model-written assertion that a check ran substitutes for an execution receipt.
