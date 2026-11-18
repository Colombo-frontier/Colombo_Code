# Nonconvex–concave optimization: arbitrary randomized algorithms and Moreau stationarity.

**Setting ID.** `CV_S_NCC_RANDOM_EXACT_PRIMAL`

Minimax optimization

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

**Status.** Fully optimal

**TASK tags.** solution concept: Moreau envelope gradient; task family: Minimax

**MODEL tags.** convexity: Nonconvex concave; geometry: Bounded dual; geometry: Compact geometry; initialization: Initialization

**ORACLE tags.** feedback quality: Exact; interface family: Value joint gradient; operation: Payoff value joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N payoff first order; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Admissible model

The set $X$ is known, nonempty, closed, and convex. The set $Y$ is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$. This setting uses $X=\mathbb{R}^{d_x}$.

The function $f$ is jointly $\beta$-smooth on $X\times Y$. For every $x$, $f(x,\cdot)$ is concave. Convexity in the $x$ direction and a positive strong-concavity modulus are not required.

The public feasible initial point $(x_0,y_0)$ satisfies $\Phi(x_0)-\inf_{x\in X}\Phi(x)\le\Delta<\infty$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $D_y$, $\Delta$, $\beta$, and $\varepsilon$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(x,y)\longmapsto(f(x,y),\nabla_xf(x,y),\nabla_yf(x,y))
$$

Queries satisfy $(x,y)\in X\times Y$. The exact value and both gradient blocks form one bundled response.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return one primal point $\widehat x\in X$. No dual point is required.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

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

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\phi_{1/(2\beta)}(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$A$: The dimensionless scale of the initial primal objective gap. **Domain:** Positive real number.

$A=\beta\Delta/\varepsilon^2$

$A_\star$: Sufficient accuracy threshold in the source theorem; no numerical value is specified. **Domain:** Universal positive constant.

$B$: The dimensionless scale of the dual-domain diameter. **Domain:** A nonnegative real.

$B=\beta D_y/\varepsilon$

$D_y$: Euclidean diameter bound for the dual feasible domain **Domain:** A nonnegative real.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_y$

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\varepsilon$: The Euclidean-norm tolerance for the reduced objective’s Moreau-envelope gradient. **Domain:** Positive real number.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in Y}f(x,y)$

$X,Y$: The primal domain is known, nonempty, closed, and convex; the dual domain is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$X=\mathbb R^{d_x}$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm first}$: Number of bundled function-value and full joint-gradient queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\phi,\iota_X$: Reduced objective with primal feasibility constraints and the set indicator function. **Domain:** An extended-real-valued function.

$\phi=\Phi+\iota_X,\quad\iota_X(x)=0\ (x\in X),\ +\infty\ (x\notin X)$

$\phi_{1/(2\beta)}$: The Moreau envelope of the constrained reduced objective; error measures its true gradient. **Domain:** A differentiable real-valued function on $\mathbb R^{d_x}$.

$\phi_{1/(2\beta)}(c)=\min_u\{\phi(u)+\beta\|u-c\|_2^2\}$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm first}(\mathcal A,I,\omega)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Main theorem's applicability region

**Region.** $A=\beta\Delta/\varepsilon^2\ge A_\star$, $B=\beta D_y/\varepsilon\ge0$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(1+A\max\{1,B\})
$$

**Upper bound.** B1

$$
O((1+A)(1+B))
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** For $A\ge A_\star$, the two expressions differ by universal factors only. The randomized lower bound comes from an arbitrary-randomized result with $n=1$.

### R2 - Zero-query regime

**Region.** $\varepsilon\ge\sqrt{8\beta\Delta/3}$.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Comparison argument.** Nonnegative cost.

## 4. Bounds and supporting evidence

### B1 - Operator-splitting upper bound of Pan (2026)

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The actual algorithms in Pan (2026), Theorems 3.3–3.4, are deterministic. Specifications allowing randomization may also use the OS witness.

$$
O((1+A)(1+B))
$$

**Sources.** [2](https://arxiv.org/pdf/2609.14235v2)

**Applicability.** Restrict Pan deterministic OS upper to $X=\mathbb R^{d_x}$; stronger deterministic guarantee satisfies probability2/3.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [2](https://arxiv.org/pdf/2609.14235v2) Definitions2.1–2.5; Theorems3.1–3.4

Separate arbitrary deterministic exact-oracle Moreau OS and joint constrained GS results.

Source definition is first good queried iterate, not automatically a fixed returned output for a lower bound. Extra final query can embed arbitrary returned point with +1 call. Domains known X closed, Y compact; value+joint gradient; lower dimension supremum. Source version Oct22 predates the old atlas Oct31 cutoff; its omission is not explained by the cutoff.

### B2 - Use n = 1 in the finite-sum NC–C lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega(1+A\max\{1,B\})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** Specialize the source component value-gradient lower bound to $n=1$. Full-space primal queries, feasible dual queries, and unqueried outputs agree with this contract.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) Definitions2.1; Theorems3.1–3.3; Section2 oracle

AS upper and IS lower for fixed-cap randomized Moreau stationarity; full n,A,B phase diagram.

Only average dual concavity. Component value+joint gradient at chosen index. Known compact Y, primal Euclidean unconstrained, no component affine-gradient bound. Success2/3; AS includes IS, so lower transfer is class inclusion. Dimension supremum may require exponentially large d. No claim about a fixed prescribed Y. Not fresh samples.

### B3 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** In this region, the witness returns the public initial point or known root, deterministically and without querying.

$$
0
$$

**Sources.** [2](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** A deterministic zero-query guarantee also applies to the randomized algorithm class.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [2](https://arxiv.org/pdf/2609.14235v2) description: Definition 2.1; Theorems 3.1–3.4

0

A deterministic zero-query guarantee also applies to the randomized algorithm class.

## References

[1] Wendao Wu; Haihan Zhang; Qian Chen; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Randomized Bounds for Finite-Sum Nonconvex–Concave Optimization. 2026. arXiv:2610.16991v2, 2026-10-19.

https://arxiv.org/pdf/2610.16991v2

[2] Siyu Pan; Taoli Zheng; Jiajin Li. Optimal Deterministic First-Order Oracle Complexity for Nonconvex-Concave Minimax Optimization. 2026. arXiv:2609.14235v2, 2026-10-22.

https://arxiv.org/pdf/2609.14235v2
