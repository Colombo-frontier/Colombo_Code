# Finite-sum nonconvex-concave minimax optimization: componentwise smoothness and Moreau stationarity

**Setting ID.** `CV_S_FS_NCC_IS`

Minimax optimization

$$
\Phi(x)=\max_{y\in Y}\frac1n\sum_{i=1}^n f_i(x,y),\qquad\min_{x\in\mathbb{R}^{d_x}}\Phi(x).
$$

**Status.** Logarithmic gap present; Bounds missing

**TASK tags.** solution concept: Moreau envelope gradient; task family: Minimax

**MODEL tags.** convexity: Nonconvex concave; geometry: Compact geometry; smoothness: Individual smooth

**ORACLE tags.** feedback quality: Exact; index control: Algorithm selects; interface family: Component value gradient; operation: Component value joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N component; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

$$
\Phi(x)=\max_{y\in Y}\frac1n\sum_{i=1}^n f_i(x,y),\qquad\min_{x\in\mathbb{R}^{d_x}}\Phi(x).
$$

### Admissible model

The set $Y\subset\mathbb{R}^{d_y}$ is known, nonempty, compact, and convex, with $\operatorname{diam}(Y)\le D_Y$ and $x\in\mathbb{R}^{d_x}$. Each $f_i$ is continuously differentiable on a neighborhood of the product domain.

The objective $f=n^{-1}\sum_i f_i$ is concave in $y$ only after averaging; individual components need not be concave. Initialization satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta<\infty$ and need not be exactly dual-optimal.

$$
\|\nabla f_i(z)-\nabla f_i(w)\|_2\le\beta\|z-w\|_2\quad(\forall i,z,w).
$$

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $D_Y$, $\Delta$, $\beta$, $\varepsilon$, $n$, together with the stated initial point and feasible geometry. Hidden analytic representations are not revealed.

$$
(i,x,y)\longmapsto(f_i(x,y),\nabla_x f_i(x,y),\nabla_y f_i(x,y)).
$$

The algorithm selects $i\in\{1,\ldots,n\}$, $x\in\mathbb{R}^{d_x}$, and $y\in Y$. Component identities are fixed, repeated evaluations are charged again, and responses are exact noiseless real values.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return $\widehat x\in\mathbb R^{d_x}$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\nabla\Phi_{1/(2\beta)}(\widehat{x})\|_2
$$

$\Phi_{1/(2\beta)}(c)=\min_u\{\Phi(u)+\beta\|u-c\|_2^2\}$; $\nabla\Phi_{1/(2\beta)}(c)=2\beta(c-\operatorname{prox}_{\Phi/(2\beta)}(c))$. Neither the envelope gradient nor an inner proximal oracle is supplied.

### Resource accounting

One bundled component-value and joint-gradient response costs one $N_{\rm component}$ call. A complete average-value or average-gradient scan costs $n$ calls.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\Phi_{1/(2\beta)}(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$A$: The dimensionless scale of the initial primal objective gap. **Domain:** Positive real number.

$A=\beta\Delta/\varepsilon^2$

$A_\star$: Sufficient accuracy threshold in the source theorem; no numerical value is specified. **Domain:** Universal positive constant.

$B$: The dimensionless scale of the dual-domain diameter. **Domain:** A nonnegative real.

$B=\beta D_Y/\varepsilon$

$\overline B$: Saturation scale unifying the small- and large-diameter regimes **Domain:** At least one.

$\overline B=\max\{1,B\}$

$D_Y$: Euclidean diameter bound for the dual feasible domain **Domain:** A nonnegative real.

$\operatorname{diam}(Y)=\sup_{u,v\in Y}\|u-v\|_2\le D_Y$

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$\beta$: Common Lipschitz bound for every component joint gradient **Domain:** Positive real number.

$\|\nabla f_i(z)-\nabla f_i(w)\|_2\le\beta\|z-w\|_2\quad(1\le i\le n)$

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\ell$: A logarithmic factor in the upper bound for the large-diameter regime **Domain:** Positive real number.

$\ell=\log(2+n+A+B)$

$\varepsilon$: The Euclidean-norm tolerance for the reduced objective’s Moreau-envelope gradient. **Domain:** Positive real number.

$n$: Fixed number of finite-sum components; the full function or operator is their 1/n average **Domain:** Positive integer.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in Y}f(x,y)$

$f_i,i$: The fixed ith real-valued component and the algorithm-selected index. **Domain:** $i\in\{1,\ldots,n\},\quad f_i:\text{the declared product domain}\to\mathbb R$.

$f=\frac1n\sum_{i=1}^n f_i$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm component}$: Number of bundled calls returning a selected component value and full joint gradient. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$\Phi_{1/(2\beta)}$: The Moreau envelope of the $\beta$-weakly convex reduced objective; its gradient is used only for evaluation. **Domain:** A differentiable real-valued function on $\mathbb R^{d_x}$.

$\Phi_{1/(2\beta)}(c)=\min_u\{\Phi(u)+\beta\|u-c\|_2^2\}$

$\operatorname{prox}_{\Phi/(2\beta)}$: The unique proximal minimizer defining the Moreau envelope; this interface is not supplied. **Domain:** $\mathbb R^{d_x}\to\mathbb R^{d_x}$.

$\operatorname{prox}_{\Phi/(2\beta)}(c)=\arg\min_u\{\Phi(u)+\beta\|u-c\|_2^2\}$

$Y$: Known nonempty compact convex dual domain with Euclidean diameter at most $D_Y$ **Domain:** $Y\subset\mathbb R^{d_y}$.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** output: domain: xhat in R^{d_x}; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: ||nabla Phi_{1/(2L)}(xhat)||; Phi_{1/(2L)}(c)=min_x {Phi(x)+L||x-c||^2}; guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: Pr(||nabla Phi_{1/(2L)}(xhat)||<=epsilon)>=2/3.

**Resource contract.** budget: fixed worst-case cap on every transcript; primary: N_component; unit: one declared oracle call; auxiliary: projection/internal model solves separately retained, never counted as hidden oracle

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q2 - source scoped metric resource statement

**Metric contract.** output: domain: xhat in R^{d_x}; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: ||nabla Phi_{1/(2L)}(xhat)||; Phi_{1/(2L)}(c)=min_x {Phi(x)+L||x-c||^2}; guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: Pr(||nabla Phi_{1/(2L)}(xhat)||<=epsilon)>=2/3.

**Resource contract.** budget: fixed worst-case cap on every transcript; primary: N_component; unit: one declared oracle call; auxiliary: projection/internal model solves separately retained, never counted as hidden oracle

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q3 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm component}(\mathcal A,I,\omega)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Small-scale regime

**Region.** Assume $n\ge1$, $A\ge A_\star$, and $0\le B\le n^{1/6}$.

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(n+A\sqrt n\,\overline B)
$$

**Upper bound.** B3

$$
O(n+A\sqrt n\,\overline B)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The three regions cover the source theorem's window $A\ge A_\star$; they do not extend to every accuracy.

### R2 - The intermediate-scale region.

**Region.** Assume $n\ge1$, $A\ge A_\star$, and $n^{1/6}<B\le n^{1/4}$.

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega(n+AB^4)
$$

**Upper bound.** B5

$$
O(n+AB^4)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The three regions cover the source theorem's window $A\ge A_\star$; they do not extend to every accuracy.

### R3 - The large-scale region.

**Region.** Assume $n\ge1$, $A\ge A_\star$, and $B>n^{1/4}$.

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega(n+An^{3/4}B)
$$

**Upper bound.** B7

$$
O\!\left((n+An^{3/4}B)\ell\right)
$$

**Gap or comparison.** $O(\ell)$

**Comparison argument.** The three regions cover the source theorem's window $A\ge A_\star$; they do not extend to every accuracy.

### R4 - The coarse-accuracy zero-query region.

**Region.** $A=\beta\Delta/\varepsilon^2\le1/4$.

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B9

$$
0
$$

**Comparison argument.** The zero upper bound and nonnegativity of cost determine the value without an additional literature lower bound.

### R5 - Remaining regime between the accuracy thresholds

**Region.** Assume $1/4<A<A_\star$; $A_\star$ is the source theorem's universal sufficient threshold, without an assigned numerical value.

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B10

$$
O\!\left(\min\{n+(1+A)(\sqrt n\,\overline B+\overline B^4),(1+A)(n+n^{3/4}B)\ell\}\right)
$$

**Comparison argument.** An upper bound is available; the main phase diagram's lower-bound accuracy threshold does not extend automatically.

### R6 - The bound’s native applicability window.

**Region.** Assume $n\ge1$, $A\ge A_\star$, and $B\ge0$, with the remaining specification conditions.

**Quantity.** Q2

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

### R7 - The bound’s native applicability window.

**Region.** Require $n\ge1$, $A\ge A_\star$, and $B\ge0$. The worst case ranges over all admissible finite dimensions and dual domains; the lower bound is not asserted for every fixed small dimension or every fixed domain.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Upper bound missing

**Lower bound.** B2

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

### B1 - See the cited theorem

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The finite-sum variance-reduction algorithms in source Theorems 3.1–3.2 use randomized component and output selection.

$$
O\!\left([n+A\min\{\sqrt n\,\overline B+\overline B^4,n^{3/4}\overline B\}]\ell\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** Every IS instance is also AS, so the same AS algorithm gives this upper bound. In the relevant $B\le n^{1/4}$ branches, use the tighter expression without logarithmic factors.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) Definitions2.1; Theorems3.1–3.3; Section2 oracle

AS upper and IS lower for fixed-cap randomized Moreau stationarity; full n,A,B phase diagram.

Only average dual concavity. Component value+joint gradient at chosen index. Known compact Y, primal Euclidean unconstrained, no component affine-gradient bound. Success2/3; AS includes IS, so lower transfer is class inclusion. Dimension supremum may require exponentially large d. No claim about a fixed prescribed Y. Not fresh samples.

### B2 - See the cited theorem

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega\!\left(n+A\min\{\sqrt n\,\overline B+\overline B^4,n^{3/4}\overline B\}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The hard instances of source Theorem 3.3 satisfy individual smoothness. Indices, feasible query points, and final outputs may all be selected by arbitrary adaptive randomized algorithms.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) Definitions2.1; Theorems3.1–3.3; Section2 oracle

AS upper and IS lower for fixed-cap randomized Moreau stationarity; full n,A,B phase diagram.

Only average dual concavity. Component value+joint gradient at chosen index. Known compact Y, primal Euclidean unconstrained, no component affine-gradient bound. Success2/3; AS includes IS, so lower transfer is class inclusion. Dimension supremum may require exponentially large d. No claim about a fixed prescribed Y. Not fresh samples.

### B3 - Randomized variance reduction with regularization-based acceleration, Theorems 3.1–3.2.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Use the randomized variance-reduction algorithms in source Theorems 3.1–3.2, retaining the conversion to a fixed budget and success probability 2/3.

$$
O(n+A\sqrt n\,\overline B)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The AS algorithm also applies to the smaller IS class. Assume $\ell=\log(2+n+A+B)$. Every component value or gradient call and every complete pass is charged.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
O(n+A\sqrt n\,\overline B)
$$

The AS algorithm also applies to the smaller IS class. Assume $\ell=\log(2+n+A+B)$. Every component value or gradient call and every complete pass is charged.

### B4 - Random rotations and hard component instances, Theorem 3.3

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Source Theorem 3.3 allows arbitrary randomized queries and unqueried outputs. Its IS hard instances are also AS.

$$
\Omega(n+A\sqrt n\,\overline B)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The hard construction is IS and therefore also AS. The lower bound allows arbitrary randomization, adaptive component selection, full values and gradients, and unqueried outputs. Dimension may be sufficiently large.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
\Omega(n+A\sqrt n\,\overline B)
$$

The hard construction is IS and therefore also AS. The lower bound allows arbitrary randomization, adaptive component selection, full values and gradients, and unqueried outputs. Dimension may be sufficiently large.

### B5 - Randomized variance reduction with regularization-based acceleration, Theorems 3.1–3.2.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Use the randomized variance-reduction algorithms in source Theorems 3.1–3.2, retaining the conversion to a fixed budget and success probability 2/3.

$$
O(n+AB^4)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The AS algorithm also applies to the smaller IS class. Assume $\ell=\log(2+n+A+B)$. Every component value or gradient call and every complete pass is charged.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
O(n+AB^4)
$$

The AS algorithm also applies to the smaller IS class. Assume $\ell=\log(2+n+A+B)$. Every component value or gradient call and every complete pass is charged.

### B6 - Random rotations and hard component instances, Theorem 3.3

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Source Theorem 3.3 allows arbitrary randomized queries and unqueried outputs. Its IS hard instances are also AS.

$$
\Omega(n+AB^4)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The hard construction is IS and therefore also AS. The lower bound allows arbitrary randomization, adaptive component selection, full values and gradients, and unqueried outputs. Dimension may be sufficiently large.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
\Omega(n+AB^4)
$$

The hard construction is IS and therefore also AS. The lower bound allows arbitrary randomization, adaptive component selection, full values and gradients, and unqueried outputs. Dimension may be sufficiently large.

### B7 - Randomized variance reduction with regularization-based acceleration, Theorems 3.1–3.2.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Use the randomized variance-reduction algorithms in source Theorems 3.1–3.2, retaining the conversion to a fixed budget and success probability 2/3.

$$
O\!\left((n+An^{3/4}B)\ell\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The AS algorithm also applies to the smaller IS class. Assume $\ell=\log(2+n+A+B)$. Every component value or gradient call and every complete pass is charged.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Logarithmic factors.** log(2+n+A+B)

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
O\!\left((n+An^{3/4}B)\ell\right)
$$

The AS algorithm also applies to the smaller IS class. Assume $\ell=\log(2+n+A+B)$. Every component value or gradient call and every complete pass is charged.

### B8 - Random rotations and hard component instances, Theorem 3.3

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Source Theorem 3.3 allows arbitrary randomized queries and unqueried outputs. Its IS hard instances are also AS.

$$
\Omega(n+An^{3/4}B)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The hard construction is IS and therefore also AS. The lower bound allows arbitrary randomization, adaptive component selection, full values and gradients, and unqueried outputs. Dimension may be sufficiently large.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
\Omega(n+An^{3/4}B)
$$

The hard construction is IS and therefore also AS. The lower bound allows arbitrary randomization, adaptive component selection, full values and gradients, and unqueried outputs. Dimension may be sufficiently large.

### B9 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** In this region, the witness returns the public initial point or known root, deterministically and without querying.

$$
0
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** The source weak-convexity envelope bound gives $\|\nabla\Phi_{1/(2\beta)}(x_0)\|^2\le4\beta\Delta$. Nonnegativity of the query count then makes the optimum exactly zero.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

0

The source weak-convexity envelope bound gives $\|\nabla\Phi_{1/(2\beta)}(x_0)\|^2\le4\beta\Delta$. Nonnegativity of the query count then makes the optimum exactly zero.

### B10 - Instancewise choice between two complete algorithm budgets (Theorem 3.2).

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Public parameters select one of two complete randomized algorithms; the selected algorithm remains randomized internally.

$$
O\!\left(\min\{n+(1+A)(\sqrt n\,\overline B+\overline B^4),(1+A)(n+n^{3/4}B)\ell\}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16991v2)

**Conditions.** Public parameters determine the algorithm choice. A uniformly matching lower bound for this upper envelope is not established in the region.

**Dimension conditions.** Subject to the stated regime predicate; optimality in fixed small dimension is not asserted.

**Oracle correspondence.** All primitive information operations are charged; see the specification and method description.

**Guarantee conversion.** The guarantee matches the specification. Any reduction is recorded in conditions.

**Resource conversion.** Complete query budget of a single algorithm

**Constants.** Constants are universal except for the stated fixed structural parameters; unknown thresholds retain symbolic values.

**Logarithmic factors.** Only the second branch contains ell

**Source location.** [1](https://arxiv.org/pdf/2610.16991v2) description: Definition 2.1; Theorems 3.1–3.3; Section 2

$$
O\!\left(\min\{n+(1+A)(\sqrt n\,\overline B+\overline B^4),(1+A)(n+n^{3/4}B)\ell\}\right)
$$

Public parameters determine the algorithm choice. A uniformly matching lower bound for this upper envelope is not established in the region.

## References

[1] Wendao Wu; Haihan Zhang; Qian Chen; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Randomized Bounds for Finite-Sum Nonconvex–Concave Optimization. 2026. arXiv:2610.16991v2, 2026-10-19.

https://arxiv.org/pdf/2610.16991v2
