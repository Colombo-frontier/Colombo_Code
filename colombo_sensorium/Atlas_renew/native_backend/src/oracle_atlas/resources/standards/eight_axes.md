# Setting Specifications: Eight Axes and Their Scope

This standard governs extraction and specification review. It describes the mathematical contract; the concrete JSON fields and enumerations are defined by `schema_read(kind)`. Store the common specification once. Differences in algorithm permissions and guarantees normally belong in `views`. A topic name, algorithm name, or matching rate cannot replace a problem definition.

## 1. Questions that all eight axes must answer

| Axis | Required information | Boundaries that are easily confused |
|---|---|---|
| TASK | The mathematical object to solve for, estimate, or decide; objective formulas; solution concept; rounds and participants; references to the interaction protocol | Membership in a category such as “variational inequality” does not specify the operator, feasible domain, or solution condition. The same task may have different oracles. |
| MODEL | The admissible instance class; the object, variable block, norm, and domain of each regularity or structural assumption; parameter ranges, geometry, existence promises; random-distribution or environmental-strategy classes | Smoothness and geometry are MODEL subcategories. Keep local/global, joint/blockwise, and componentwise/average assumptions distinct. |
| ORACLE | For every native operation: queried object, admissible points/domain, exact return values, selection rights, precision/error/noise, random dependence and reuse, public auxiliary operations; the register of public and hidden information | Full gradients, individual coordinates, a full subgradient, the entire subdifferential, prox access, and value-plus-gradient access grant different capabilities. Do not maintain a duplicate public/hidden-information register in MODEL. |
| ALGORITHMS | Determinism/randomization, adaptivity, parallelism, communication/memory/internal-computation restrictions; random seeds and accessible information | Explicitly state the relevant permissions when no restriction is imposed. Do not automatically add span, zero-respecting, continuous-update, or finite-bit restrictions. |
| OUTPUT | Output object, space, and feasibility; whether unqueried points, averages, or convex combinations may be returned; any required function value, set, or certificate | An algorithm's trajectory or internal state need not become the problem's output. Do not omit required certificates. |
| METRIC | Exact formula for the base error, normalization, and finiteness conditions; aggregation order across multiple random sources, times, players, or instances | Distances and squared distances, gradient norms and squared norms, distinct gap functions, and different notions of regret are not automatically equivalent. |
| GUARANTEE | Quantifiers over instances, algorithms, randomness, success events, and accuracy; per-instance, expected, fixed-probability, or arbitrary-confidence guarantees; separate error and cost guarantees | High-probability error is not high-probability runtime cost. Success on each instance is not a single random event that succeeds simultaneously on every instance. |
| RESOURCE | Unit cost of each operation; oracle calls, samples, components, communication/bits, arithmetic, passes, memory; free computation and preprocessing | An exact oracle with free real arithmetic does not establish bit complexity. Do not assume that an operation on an entire matrix costs one unit. |

## 2. Bindings for every statement

Each entry of `statements[]` must contain every field required by its schema, including `object_ref`, `variable_block_ref`, `norm_ref`, `domain_ref`, `view_ref`, `operation_ref`, and `evidence_refs`. Use `null` as specified by the schema for genuinely inapplicable bindings. Distinguish unknown from inapplicable. Never invent an object, norm, or evidence reference to satisfy a required field.

Objects, variable blocks, and operation IDs must be locatable within the specification. A source locator must identify the version actually read and its theorem, equation, page, or passage. Missing protocol fields and invalid JSON Pointers are generation-protocol errors: correct the format and resubmit. They do not establish a mathematical error in the paper.

`summary` is the reader's overview; the complete applicability conditions must remain recoverable from the statements and operations. When the source omits information that determines identity, record the specific unknown and its consequences. Do not fill it in from general expectations.

## 3. Common specifications, views, and algorithmic witnesses

Identify the common task/model/native-oracle/output/metric/resource contract first, then record views for permitted algorithms and guarantees. Deterministic and randomized comparisons ordinarily belong in one profile. If an algorithm needs a known radius for tuning, determine whether that radius is common public input, a permission of one view, or an additional condition of that particular upper-bound witness. Do not redefine the entire instance class on that basis.

Record a paper algorithm's step sizes, initialization, sampling method, waiting periods, exact elimination tests, and any other conditions necessary for its theorem in the corresponding result card or witness. Promote them to the common specification only when they actually define the task or permitted protocol. “This algorithm starts at zero” does not mean “all algorithms must start at zero.”

Different native oracles, models, or targets are not automatically merged because they share a complexity rate. A new algorithm, randomized lower bound, or changed parameter window usually updates the original profile's results, views, or regimes.

## 4. Multilevel and interactive problems

For bilevel/multilevel problems, specify each level's variables, objectives/constraints, and operators. List query inputs, returned components, precision, shared samples, and unit costs separately. For example, access to a lower-level value, partial derivative, Hessian-vector product, approximate solution, optimal value, or solution map cannot be used interchangeably. Explicitly state, or retain as unknown, whether the upper level can query arbitrary lower-level points, reuse the same random sample, or solve internal subproblems for free.

For online problems, games, and noisy oracles, specify the order within each round: who selects an action first, who then chooses the environment/loss, who observes which history, when the round's randomness is generated, and the information set relative to which conditional independence holds. Do not change the source's timing, ball/sphere sampling, or regularization conditions merely to make an estimator unbiased.

## 5. Levels of source uncertainty

- An explicit source condition was omitted from the candidate: block extraction and revise the candidate.
- The source itself is unclear and the candidate records that faithfully: extraction may pass; block identity if the uncertainty affects the common native interface or quantifiers.
- A theorem's proof, parameter recurrence, or cost accounting remains unverified: quarantine the corresponding bound and continue with independent results.
- Display/OCR conversion lost a superscript or symbol: first check the original PDF/HTML formula; retain a specific unresolved issue only if it cannot be verified.

Missing material means that the component has not verified a claim; it is not evidence that the paper is wrong. A counterexample to an auxiliary lemma affects only claims that depend on that lemma and does not automatically refute the main theorem.
