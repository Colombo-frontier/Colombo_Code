# Nonconvex-concave minimax optimization with exact first-order information: Moreau stationarity

**Setting ID.** `CV_S_NCC_MOREAU_EXACT_GENERAL_X`

Minimax optimization

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

**Status.** Bounds missing

**TASK tags.** formulation: Nonconvex concave minimize value; solution concept: Moreau envelope gradient; task family: Minimax

**MODEL tags.** convexity: Concavity in the declared block; convexity: No convexity promise in block; convexity: Nonconvex concave; geometry: Bounded dual; geometry: Compact geometry; geometry: Dual diameter; initialization: Initialization; initialization: Value initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; interface family: Value joint gradient; operation: Payoff value joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: Zero respecting

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N bundle; measure: N payoff first order; measure: N projection; precision: Bit precision not counted; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Admissible model

Let $X\subseteq\mathbb R^{d_x}$ be a known nonempty closed convex set and $Y\subseteq\mathbb R^{d_y}$ a known nonempty compact convex set with $\operatorname{diam}(Y)\le D_y$.

The unknown payoff $f$ has a jointly $\beta$-Lipschitz gradient on $X\times Y$, and $f(x,\cdot)$ is concave for every $x$. No convexity in $x$ or positive strong-concavity modulus is assumed.

The public initial point $(x_0,y_0)\in X\times Y$ satisfies $\Phi(x_0)-\inf_{x\in X}\Phi(x)\le\Delta<\infty$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Oracle interface

The public data are $d_x,d_y,\beta,D_y,\Delta,\varepsilon$, the sets $X,Y$, and the initial point. The analytic representation of $f$ is hidden.

Each query $(x,y)\in X\times Y$ returns the exact bundle $(f(x,y),\nabla_x f(x,y),\nabla_y f(x,y))$ at unit first-order query cost.

Exact Euclidean projections onto the known sets are available. Their calls are retained as a separate resource and are uncharged in the primary query projection.

### Output

Return one primal point $\widehat x\in X$. No dual point is required.

### Loss or accuracy criterion

$$
\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2
$$

Let $\phi(x)=\Phi(x)+\iota_X(x)$, where $\iota_X$ equals $0$ on $X$ and $+\infty$ elsewhere; define $\phi_{1/(2\beta)}(c)=\min_u\{\phi(u)+\beta\|u-c\|_2^2\}$. The envelope is differentiable. Its gradient is the evaluation criterion, not a free oracle.

### Resource accounting

Each bundled value-and-joint-gradient call counts once in $N_{\rm first}$. Projection counts are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

#### Deterministic zero respecting

Deterministic adaptive zero-respecting algorithms are allowed. Feasible queries and outputs may use only coordinates exposed by the relevant gradient blocks. Projection cannot bypass the support restriction in source Definition 2.6.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2\le\varepsilon.
$$

**Output qualification.** Unqueried outputs are allowed, subject to the stated support rule.

**View qualification.** Deterministic zero-respecting algorithms; feasible queries, projected points, and outputs obey the stated coordinate-support restriction.

**Budget convention.** fixed worst-case query cap

#### Deterministic unrestricted

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2\le\varepsilon.
$$

**Output qualification.** The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

**View qualification.** Arbitrary measurable deterministic adaptive algorithms with unrestricted transcript-based output.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$D_y$: Euclidean diameter bound for the dual feasible domain **Domain:** Positive real number.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_y$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: The Euclidean-norm tolerance for the reduced objective’s Moreau-envelope gradient. **Domain:** Positive real number.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in Y}f(x,y)$

$X,Y$: The primal domain is known, nonempty, closed, and convex; the dual domain is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$N_{\rm first}$: Number of bundled function-value and full joint-gradient queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$c_1$: A small universal constant in the source accuracy window, with no numerical value specified. **Domain:** Fixed positive constant in the source theorem; its numerical value is unspecified and it is not a new instance parameter.

$\phi,\iota_X$: Reduced objective with primal feasibility constraints and the set indicator function. **Domain:** An extended-real-valued function.

$\phi=\Phi+\iota_X,\quad\iota_X(x)=0\ (x\in X),\ +\infty\ (x\notin X)$

$\phi_{1/(2\beta)}$: The Moreau envelope of the constrained reduced objective; error measures its true gradient. **Domain:** A differentiable real-valued function on $\mathbb R^{d_x}$.

$\phi_{1/(2\beta)}(c)=\min_u\{\phi(u)+\beta\|u-c\|_2^2\}$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

$A$: The dimensionless scale of the initial primal objective gap. **Domain:** Positive real number.

$A=\beta\Delta/\varepsilon^2$

$B$: The dimensionless scale of the dual-domain diameter. **Domain:** A nonnegative real.

$B=\beta D_y/\varepsilon$

$D_y$: Euclidean diameter bound for the dual feasible domain **Domain:** A nonnegative real.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_y$

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic zero respecting

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm first}(\mathcal A,I)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

#### Q2 - source scoped metric resource statement

**View.** Deterministic unrestricted

**Metric contract.** output: domain: xhat in X; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: ||grad Phi_{1/(2L)}(xhat)||; guarantee: ||grad Phi_{1/(2L)}(xhat)||<=epsilon for every legal instance

**Resource contract.** budget: fixed worst-case cap on every transcript; primary: N_payoff_first_order; unit: one declared oracle call; auxiliary: projection/internal model solves separately retained, never counted as hidden oracle

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q3 - target accuracy cost

**View.** Deterministic unrestricted

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm first}(\mathcal A,I)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The source theorem’s applicability window.

**Region.** $0<\varepsilon\le c_1\min\{\sqrt{\beta\Delta},\beta D_y\}$

**Views.** Deterministic zero respecting

**Quantity.** Q1

**Resource.** Number of joint responses explicitly allowed by this profile

**Status.** Upper bound missing

**Lower bound.** B1

$$
\Omega(\beta^2D_y\Delta\varepsilon^{-3})
$$

**Upper bound.** No admitted bound for this comparison

**Comparison argument.** The retained upper belongs to a different algorithm/guarantee/initialization specification.

### R2 - Main theorem's applicability region

**Region.** The quantity is $0<\varepsilon<\sqrt{8\beta\Delta/3}$, equivalently $A>3/8$.

**Views.** Deterministic unrestricted

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(A(1+B))
$$

**Upper bound.** B3

$$
O(A(1+B))
$$

**Gap or comparison.** $O(1)$

### R3 - Zero-query regime

**Region.** $\varepsilon\ge\sqrt{8\beta\Delta/3}$.

**Views.** Deterministic unrestricted

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B5

$$
0
$$

**Comparison argument.** Query cost is nonnegative. This is the exact OS threshold and is not used for GS.

## 4. Bounds and supporting evidence

### B1 - deterministic dual lattice plus masked stochastic chain

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic zero respecting

**Witness or lower-bound scope.** The stated restricted deterministic class

**Algorithm-scope qualification.** The lower bound relies on zero-respecting or block-memory linear-span restrictions. This view requires only deterministic algorithms.

$$
\Omega(\beta^2D_y\Delta\varepsilon^{-3})
$$

**Sources.** [1](https://arxiv.org/pdf/2609.14233v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\beta^2D_y\Delta\varepsilon^{-3})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2609.14233v1) theorem: Theorem4.1; section: Section4; pdf pages: 14; 15

Source Definition 2.6 constrains the support of feasible queries and projected points by previous feedback. The lower bound here covers only deterministic zero-respecting algorithms.

### B2 - See the cited theorem

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** two_sided_statement

**View.** Deterministic unrestricted

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The actual algorithms in Pan (2026), Theorems 3.3–3.4, are deterministic. Specifications allowing randomization may also use the OS witness.

$$
\Theta(A(1+B))
$$

**Sources.** [2](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** The upper and lower bounds are recorded individually. Converting a source's queried-point output convention to an arbitrary final output requires one additional query, which is included in those records.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [2](https://arxiv.org/pdf/2609.14235v2) Definitions2.1–2.5; Theorems3.1–3.4

Separate arbitrary deterministic exact-oracle Moreau OS and joint constrained GS results.

Source definition is first good queried iterate, not automatically a fixed returned output for a lower bound. Extra final query can embed arbitrary returned point with +1 call. Domains known X closed, Y compact; value+joint gradient; lower dimension supremum. Source version Oct22 predates the old atlas Oct31 cutoff; its omission is not explained by the cutoff.

### B3 - Deterministic regularization and nested first-order methods, Theorem 3.3.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic unrestricted

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The actual algorithms in Pan (2026), Theorems 3.3–3.4, are deterministic. Specifications allowing randomization may also use the OS witness.

$$
O(A(1+B))
$$

**Sources.** [2](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** Count every primitive value and joint-gradient call. Projection and known-model computation follow the declared specification.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [2](https://arxiv.org/pdf/2609.14235v2) description: Definition 2.1; Theorems 3.1–3.4

O(A(1+B))

Count every primitive value and joint-gradient call. Projection and known-model computation follow the declared specification.

### B4 - Adversarially rotated hard instances, Theorem 3.1.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic unrestricted

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** The source theorem covers arbitrary adaptive deterministic queries, beyond linear-span iterations. It does not thereby give an arbitrary-randomized lower bound.

$$
\Omega(A(1+B))
$$

**Sources.** [2](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** One additional query converts the source’s queried-output convention to an arbitrary final output. Constants and the boundary requiring at least one query are treated separately. This does not extend the result to arbitrary randomized algorithms.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [2](https://arxiv.org/pdf/2609.14235v2) description: Definition 2.1; Theorems 3.1–3.4

$$
\Omega(A(1+B))
$$

One additional query converts the source’s queried-output convention to an arbitrary final output. Constants and the boundary requiring at least one query are treated separately. This does not extend the result to arbitrary randomized algorithms.

### B5 - Return the initial point; sharp initial bound for the weakly convex envelope

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic unrestricted

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** In this region, the witness returns the public initial point or known root, deterministically and without querying.

$$
0
$$

**Sources.** [2](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** The zero-query branch of Theorem 3.3.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [2](https://arxiv.org/pdf/2609.14235v2) description: Definition 2.1; Theorems 3.1–3.4

0

The zero-query branch of Theorem 3.3.

## References

[1] Qilong Wu; Zhihao Gu; Junchi Yang. Lower Bounds for Nonconvex-Concave Minimax Optimization. 2026. arXiv:2609.14233v1, 2026-09-13.

https://arxiv.org/pdf/2609.14233v1

[2] Siyu Pan; Taoli Zheng; Jiajin Li. Optimal Deterministic First-Order Oracle Complexity for Nonconvex-Concave Minimax Optimization. 2026. arXiv:2609.14235v2, 2026-10-22.

https://arxiv.org/pdf/2609.14235v2
