# General nonconvex–nonconcave optimization: exact local minimax points.

**Setting ID.** `CV_S_LOCAL_MINIMAX`

Minimax optimization

Find an exact local minimax point $(x^\star,y^\star)\in\mathbb R^{d_x}\times\mathbb R^{d_y}$. There must exist $r_0>0$ and a function $h:(0,r_0]\to[0,\infty)$ with $\lim_{r\downarrow0}h(r)=0$ such that every $0<r\le r_0$, $\|x-x^\star\|_2\le r$, and $\|y-y^\star\|_2\le r$ satisfies

**Status.** Infeasible task

**TASK tags.** formulation: Local sequential minimax; solution concept: Exact local minimax; task family: Minimax

**MODEL tags.** convexity: C2 nonconvex nonconcave; existence: Existence not promised

**ORACLE tags.** feedback quality: Exact; interface family: Value joint gradient; operation: Payoff value joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Local minimax exact

**GUARANTEE tags.** quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N bundle; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an exact local minimax point $(x^\star,y^\star)\in\mathbb R^{d_x}\times\mathbb R^{d_y}$. There must exist $r_0>0$ and a function $h:(0,r_0]\to[0,\infty)$ with $\lim_{r\downarrow0}h(r)=0$ such that every $0<r\le r_0$, $\|x-x^\star\|_2\le r$, and $\|y-y^\star\|_2\le r$ satisfies

$$
f(x^\star,y)\le f(x^\star,y^\star)\le\max_{\|y^\prime-y^\star\|_2\le h(r)} f(x,y^\prime).
$$

The two neighborhood radii are r and h(r). Neither h(r)=r nor proportionality to r is required, and the radii are not supplied in advance.

### Admissible model

Assume $f\in C^2(\mathbb{R}^{d_x+d_y})$; neither variable block must be convex or concave. Existence of a local minimax point is not promised, and no quantitative regularity, neighborhood radius, or approximate-solution tolerance is specified.

### Oracle interface

Public inputs are the positive integer block dimensions $d_x,d_y$. The analytic expression for $f$ is hidden. The output must be exact; there is no adjustable positive error tolerance.

$$
(x,y)\longmapsto(f(x,y),\nabla_x f(x,y),\nabla_y f(x,y)).
$$

Exact full-space queries.

### Output

Return an exact local minimax point $(\widehat x,\widehat y)\in\mathbb R^{d_x+d_y}$.

### Loss or accuracy criterion

The set $\mathcal L_f$ contains every local minimax point under the stated local definition.

$$
\mathbf 1\{(\widehat x,\widehat y)\notin\mathcal L_f\}.
$$

The indicator loss must equal zero. Here $\varepsilon=0$ denotes an exact task, not a gradient-norm tolerance.

### Resource accounting

Count bundled value-and-joint-gradient calls. Because existence is not guaranteed, no uniform finite-query upper bound results.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

A single deterministic algorithm must return a point in $\mathcal L_f$ for every admissible $f$. The model allows $\mathcal L_f=\varnothing$, so this uniform requirement is infeasible.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Fixed zero tolerance for exact decision **Domain:** Fixed at zero for exact decision.

$\varepsilon=0$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$N_{\rm first}$: Number of bundled function-value and full joint-gradient queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: This is the principal information-call budget on one instance. The resource specification determines whether it is fixed or a worst-instance expected budget. **Domain:** A nonnegative integer; expected budgets may be nonnegative real numbers.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\mathcal L_f$: The exact local minimax points under the complete local definition stated here. **Domain:** A subset of $\mathbb R^{d_x+d_y}$, possibly empty.

$x^\star,y^\star$: An arbitrary candidate point in the local definition, not an assumed global solution. **Domain:** $\mathbb R^{d_x}$ and $\mathbb R^{d_y}$.

$r_0,r,h$: The local threshold, vanishing neighborhood radius, and dual-response radius function. **Domain:** $r_0>0,\ 0<r\le r_0,\ h:(0,r_0]\to[0,\infty)$.

$\lim_{r\downarrow0}h(r)=0$

$\mathbf1\{E\}$: The indicator of proposition E: one if true and zero otherwise. **Domain:** $\{0,1\}$.

$e_1$: First coordinate unit vector in the primal-variable space **Domain:** $\mathbb R^{d_x}$.

$\mathfrak A_{\rm succ}$: Algorithms returning an exact local minimax point for every admissible function **Domain:** Empty set for the task over the full model class.

$N_{\mathcal A}(I,\omega)$: Primary information calls accumulated by algorithm A on execution path omega of fixed instance I **Domain:** A nonnegative integer. For an almost surely terminating algorithm, use its complete stopping count.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star=\inf_{\mathcal A\in\mathfrak A_{\rm succ}}\sup_I N_{\mathcal A}(I),\qquad\inf\varnothing:=+\infty
$$

**Scope.** A successful algorithm must return an exact local minimax point for every admissible function. A linear counterexample makes the admissible algorithm set empty; this is not an ordinary finite-error query rate.

**Optimization direction.** minimize

### R1 - Full model class, which contains instances with no solution

**Region.** All declared $C^2$ nonconvex–nonconcave full-space functions, without a solution-existence promise.

**Quantity.** Q1

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Infeasible task

**Lower bound.** B1

$$
N^\star=+\infty
$$

**Comparison argument.** No algorithm succeeds on the entire class because some admissible instances have no solution. This is task infeasibility, not missing upper and lower bounds.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** For arbitrary positive integers $d_x,d_y$, let $f(x,y)=x_1$. This function is $C^\infty$ on the whole space and satisfies the stated $C^2$ assumptions. The model imposes no lower boundedness, compact primal domain, strong concavity, or existence promise. For any candidate $(x^\star,y^\star)$, any $r_0>0$, and any admissible $h$, choose $0<r\le r_0$ and $x=x^\star-(r/2)e_1$. For every $y^\prime$, $f(x,y^\prime)=x_1^\star-r/2<f(x^\star,y^\star)$, violating the second inequality in the local minimax definition. Thus an instance without a solution exists in every allowed dimension; even revealing the entire function cannot produce a valid output. The notation $N^\star=+\infty$ uses the convention that the successful-algorithm class is empty. The explanatory status is `infeasible_task`.

**Dimension conditions.** Any $d_x,d_y\ge1$ are allowed. The counterexample already holds at $d_x=d_y=1$.

**Oracle mapping.** The counterexample is independent of the information available. Exact-value and gradient interfaces satisfy the model, and additional information cannot create a nonexistent point.

**Guarantee mapping.** The requirement that one algorithm succeed on every instance fails because the class contains an admissible instance with no solution.

**Resource mapping.** No algorithm succeeds, so neither a finite nor an infinite query budget satisfies the task on the entire class.

### B1 - No-solution counterexample with a linear primal objective

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** An admissible instance has an empty solution set, so no output strategy can succeed. No span, zero-respecting, or queried-output restriction is needed.

$$
N^\star=+\infty
$$

**Sources.** [1](https://proceedings.mlr.press/v119/jin20e/jin20e.pdf)

**Constants.** This no-solution counterexample involves no asymptotic constant or accuracy threshold.

**Local argument.** A1

**Source location.** [1](https://proceedings.mlr.press/v119/jin20e/jin20e.pdf) theorem: Definition 14; section: Section 3.1; pdf pages: 5

Use the original definition’s quantifiers. The source paper supports the definition only; the counterexample f = x_1 is a separate argument, not a theorem attributed to that paper.

## 5. Local arguments

### A1 - No-solution counterexample with a linear primal objective

**Scope.** All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

For arbitrary positive integers $d_x,d_y$, let $f(x,y)=x_1$. This function is $C^\infty$ on the whole space and satisfies the stated $C^2$ assumptions. The model imposes no lower boundedness, compact primal domain, strong concavity, or existence promise. For any candidate $(x^\star,y^\star)$, any $r_0>0$, and any admissible $h$, choose $0<r\le r_0$ and $x=x^\star-(r/2)e_1$. For every $y^\prime$, $f(x,y^\prime)=x_1^\star-r/2<f(x^\star,y^\star)$, violating the second inequality in the local minimax definition. Thus an instance without a solution exists in every allowed dimension; even revealing the entire function cannot produce a valid output. The notation $N^\star=+\infty$ uses the convention that the successful-algorithm class is empty. The explanatory status is `infeasible_task`.

**Sources.** [1](https://proceedings.mlr.press/v119/jin20e/jin20e.pdf)

## References

[1] Chi Jin; Praneeth Netrapalli; Michael I. Jordan. What is Local Optimality in Nonconvex-Nonconcave Minimax Optimization?. 2020. ICML PMLR119.

https://proceedings.mlr.press/v119/jin20e/jin20e.pdf
