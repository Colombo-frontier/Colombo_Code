# Smooth convex-concave saddle-point problems: deterministic joint gradients

**Setting ID.** `CV_S_CC_FIRST_DET`

Minimax optimization

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$.

**Status.** Fully optimal

**TASK tags.** formulation: Convex concave saddle; task family: Minimax; task family: Saddle point

**MODEL tags.** convexity: Convex concave; geometry: Diameter bound; geometry: Known compact; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; interface family: Exact joint gradient; operation: Payoff joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad; measure: N projection; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$.

### Admissible model

The set $K\subset\mathbb{R}^d$ is known, nonempty, compact, and convex, with $\operatorname{diam}(K)\le D_K$. The conditions $K=X\times Y$ and $d=d_x+d_y$ also hold.

The function $f$ is convex in $x$, concave in $y$, and has a jointly $\beta$-Lipschitz gradient.

These assumptions ensure the relevant solutions exist; all vector norms are Euclidean.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $D_K$, $\beta$, and $\varepsilon$, together with the stated initial-point and feasible-domain information. Analytic representations of hidden functions, operators, or matrices are not revealed.

$$
z\in K\longmapsto (\nabla_x f(z),\nabla_y f(z))
$$

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

Exact noiseless response, without an additional function value

### Output

Return $(\widehat{x},\widehat{y})\in X\times Y$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\max_{v\in Y}f(\widehat{x},v)-\min_{u\in X}f(u,\widehat{y})
$$

This gap is finite and nonnegative on the compact domain.

### Resource accounting

One exact joint gradient costs one $N_{\mathrm{grad}}$ call. Projection costs are recorded separately.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\max_{v\in Y}f(\widehat{x},v)-\min_{u\in X}f(u,\widehat{y})\le\varepsilon.
$$

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the entire feasible product domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$K$: A known nonempty compact convex feasible set. **Domain:** A subset of Euclidean space.

$K=X\times Y\subset\mathbb R^{d_x+d_y}$

$X,Y$: Both primal and dual domains are known, nonempty, compact, and convex. Their product has diameter at most $D_K$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$N_{\rm grad}$: The number of complete exact joint-gradient calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm grad}(\mathcal A,I)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Sufficiently high-dimensional regime

**Region.** $\beta D_K^2/\varepsilon\ge C;\ d_x,d_y\ge C\beta D_K^2/\varepsilon$

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\beta D_K^2/\varepsilon)
$$

**Upper bound.** B1

$$
O(\beta D_K^2/\varepsilon)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The result is restricted to deterministic algorithms and sufficiently large dimension. Low-dimensional exact recovery and randomized lower bounds require separate evidence.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - Euclidean Mirror-Prox

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Mirror-Prox uses exact operator responses, fixed step sizes, and deterministic proximal updates. Its averaged output is also deterministic.

$$
O(1+\beta D_K^2/\varepsilon)
$$

**Sources.** [1](https://www2.isye.gatech.edu/~nemirovs/SIOPT_MP_2004.pdf)

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
O(1+\beta D_K^2/\varepsilon)
$$

**N projection.**

$$
O(1+\beta D_K^2/\varepsilon)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://www2.isye.gatech.edu/~nemirovs/SIOPT_MP_2004.pdf) theorem: Theorem3.2, equations(3.9)--(3.10); section: Section3; pdf pages: 11

Running $T$ steps requires $2T$ joint-gradient calls and $2T$ proximal operations on known geometry. The saddle-gap guarantee comes from the source saddle-point analysis; a weak VI gap is not substituted for the saddle gap.

### B2 - smooth convex term plus bilinear hidden chain

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** The source theorem covers arbitrary adaptive deterministic queries, beyond linear-span iterations. It does not thereby give an arbitrary-randomized lower bound.

$$
\Omega(\beta D_K^2/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/1808.02901)

**Dimension conditions.** The source requires $8<m\le n$ and $t<m/4-2$. Both balanced block dimensions are sufficiently large, at scale $C\beta D_K^2/\varepsilon$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\beta D_K^2/\varepsilon)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Scale both the source primal smoothness constant and bilinear coupling norm to $\beta/c$, and choose block radii $R_x=R_y=D_K/(2\sqrt2)$ with sufficiently large universal $c$. The joint-gradient Lipschitz constant is at most $\beta$ and product-domain diameter at most $D_K$. The coupling term in the source lower bound gives gap at least $c_0\beta D_K^2/(t+1)$ after $t$ calls, for universal $c_0>0$. The source dimension and iteration conditions remain in force.

**Source location.** [2](https://arxiv.org/pdf/1808.02901) theorem: Theorem9; section: Section4; pdf pages: 29

Use the unrestricted deterministic first-order algorithm model in source equation (8), retaining conditions $L_f\ge L_A$ and $t<m/4-2$. The constants $L_f$ and $L_A$ control the smooth and coupling terms; $m$ is the hard-instance dimension and $t$ the query count. Scale with comparable smoothness constants and balanced block radii.

## References

[1] Arkadi Nemirovski. Prox-Method with Rate of Convergence O(1/t) for Variational Inequalities with Lipschitz Continuous Monotone Operators and Smooth Convex-Concave Saddle Point Problems. 2004. SIAM J. Optim. 15(1):229--251.

https://www2.isye.gatech.edu/~nemirovs/SIOPT_MP_2004.pdf

[2] Yuyuan Ouyang; Yangyang Xu. Lower complexity bounds of first-order methods for convex-concave bilinear saddle-point problems. 2021. author arXiv:1808.02901 version downloaded; Mathematical Programming 185.

https://arxiv.org/pdf/1808.02901
