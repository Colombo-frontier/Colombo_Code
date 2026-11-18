# Nonconvex-concave problems: arbitrary deterministic algorithms and game stationarity

**Setting ID.** `CV_S_NCC_DET_GS_UNRESTRICTED`

Minimax optimization

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

**Status.** Fully optimal

**TASK tags.** solution concept: Constrained game stationarity; task family: Minimax

**MODEL tags.** convexity: Nonconvex concave; geometry: Bounded dual; geometry: Compact geometry; initialization: Initialization

**ORACLE tags.** feedback quality: Exact; interface family: Value joint gradient; operation: Payoff value joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point pair

**METRIC tags.** criterion: Game stationarity; criterion: Tangential residual

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N payoff first order; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_{x\in X}\Phi(x)$, where $\Phi(x)=\max_{y\in Y}f(x,y)$.

### Admissible model

The set $X$ is known, nonempty, closed, and convex. The set $Y$ is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_y$.

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

Return a feasible pair $(\widehat x,\widehat y)\in X\times Y$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\max\{\operatorname{dist}(0,\nabla_xf(\widehat{x},\widehat{y})+N_X(\widehat{x})),\operatorname{dist}(0,-\nabla_yf(\widehat{x},\widehat{y})+N_Y(\widehat{y}))\}
$$

For a closed convex set $K$, define $N_K(z)=\{v:\langle v,u-z\rangle\le0,\ \forall u\in K\}$ for $z\in K$, and $\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$.

### Resource accounting

Each bundled value-and-joint-gradient call counts once in $N_{\rm first}$. Projection counts are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\max\{\operatorname{dist}(0,\nabla_xf(\widehat{x},\widehat{y})+N_X(\widehat{x})),\operatorname{dist}(0,-\nabla_yf(\widehat{x},\widehat{y})+N_Y(\widehat{y}))\}\le\varepsilon.
$$

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$A$: The dimensionless scale of the initial primal objective gap. **Domain:** Positive real number.

$A=\beta\Delta/\varepsilon^2$

$B$: The dimensionless scale of the dual-domain diameter. **Domain:** A nonnegative real.

$B=\beta D_y/\varepsilon$

$D_y$: Euclidean diameter bound for the dual feasible domain **Domain:** A nonnegative real.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_y$

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: This is the tangent-residual tolerance. The mean-square guarantee uses its square $\varepsilon^2$. **Domain:** Positive real number.

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

$N_K(z)$: Use the Euclidean normal cone of the closed convex feasible set K at the feasible point z. The same definition applies blockwise to $N_X$ and $N_Y$. **Domain:** $z\in K,\quad N_K(z)\subset\mathbb R^d$.

$N_K(z)=\{v:\langle v,u-z\rangle\le0\ \forall u\in K\}$

$\operatorname{dist}(0,S)$: Infimum of the Euclidean distances from vectors in $S$ to the origin **Domain:** Nonnegative extended real value.

$\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$N_{\rm first}$: Number of bundled function-value and full joint-gradient queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** output: domain: (xhat,yhat) in X x Y; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: max{dist(0,grad_x f(xhat,yhat)+N_X(xhat)),dist(0,-grad_y f(xhat,yhat)+N_Y(yhat))}; guarantee: max{dist(0,grad_x f(xhat,yhat)+N_X(xhat)),dist(0,-grad_y f(xhat,yhat)+N_Y(yhat))}<=epsilon for every legal instance

**Resource contract.** budget: fixed worst-case cap on every transcript; primary: N_payoff_first_order; unit: one declared oracle call; auxiliary: projection/internal model solves separately retained, never counted as hidden oracle

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q2 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm first}(\mathcal A,I)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Main theorem's applicability region

**Region.** $\beta,\Delta,D_y,\varepsilon>0$.

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(\sqrt{(1+A)(1+B)(1+A+B)})
$$

**Upper bound.** B2

$$
O(\sqrt{(1+A)(1+B)(1+A+B)})
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

### B1 - See the cited theorem

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** two_sided_statement

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The actual algorithms in Pan (2026), Theorems 3.3–3.4, are deterministic. Specifications allowing randomization may also use the OS witness.

$$
\Theta\!\left(\sqrt{(1+A)(1+B)(1+A+B)}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** The bounds are recorded individually. GS's two block tangent residuals and OS's Moreau measure are handled separately.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [1](https://arxiv.org/pdf/2609.14235v2) Definitions2.1–2.5; Theorems3.1–3.4

Separate arbitrary deterministic exact-oracle Moreau OS and joint constrained GS results.

Source definition is first good queried iterate, not automatically a fixed returned output for a lower bound. Extra final query can embed arbitrary returned point with +1 call. Domains known X closed, Y compact; value+joint gradient; lower dimension supremum. Source version Oct22 predates the old atlas Oct31 cutoff; its omission is not explained by the cutoff.

### B2 - Deterministic regularization and nested first-order method, Theorem 3.4

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The actual algorithms in Pan (2026), Theorems 3.3–3.4, are deterministic. Specifications allowing randomization may also use the OS witness.

$$
O(\sqrt{(1+A)(1+B)(1+A+B)})
$$

**Sources.** [1](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** Count every primitive value and joint-gradient call. Projection and known-model computation follow the declared specification.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2609.14235v2) description: Definition 2.1; Theorems 3.1–3.4

$$
O(\sqrt{(1+A)(1+B)(1+A+B)})
$$

Count every primitive value and joint-gradient call. Projection and known-model computation follow the declared specification.

### B3 - Adversarially rotated hard instance, Theorem 3.2

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** The source theorem covers arbitrary adaptive deterministic queries, beyond linear-span iterations. It does not thereby give an arbitrary-randomized lower bound.

$$
\Omega(\sqrt{(1+A)(1+B)(1+A+B)})
$$

**Sources.** [1](https://arxiv.org/pdf/2609.14235v2)

**Conditions.** One additional query converts the source’s queried-output convention to an arbitrary final output. Constants and the boundary requiring at least one query are treated separately. This does not extend the result to arbitrary randomized algorithms.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2609.14235v2) description: Definition 2.1; Theorems 3.1–3.4

$$
\Omega(\sqrt{(1+A)(1+B)(1+A+B)})
$$

One additional query converts the source’s queried-output convention to an arbitrary final output. Constants and the boundary requiring at least one query are treated separately. This does not extend the result to arbitrary randomized algorithms.

## References

[1] Siyu Pan; Taoli Zheng; Jiajin Li. Optimal Deterministic First-Order Oracle Complexity for Nonconvex-Concave Minimax Optimization. 2026. arXiv:2609.14235v2, 2026-10-22.

https://arxiv.org/pdf/2609.14235v2
