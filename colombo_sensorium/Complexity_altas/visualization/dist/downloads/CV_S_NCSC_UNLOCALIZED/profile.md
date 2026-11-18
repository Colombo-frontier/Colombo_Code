# Nonconvex-strongly-concave problems without control of dual initialization

**Setting ID.** `CV_S_NCSC_UNLOCALIZED`

Minimax optimization

$$
\min_{x\in\mathbb{R}^{d_x}}\Phi(x),\qquad\Phi(x)=\max_{y\in\mathbb{R}^{d_y}}f(x,y).
$$

**Status.** Infinite complexity

**TASK tags.** formulation: Minimize value function; task family: Minimax

**MODEL tags.** convexity: No convexity promise in block; convexity: Nonconvex strongly concave; convexity: Strong concavity in the declared block; initialization: Initial suboptimality; initialization: No dual localization; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; interface family: Exact joint gradient; operation: Payoff joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad; precision: Bit precision not counted

## 1. Setting specification

### Task

$$
\min_{x\in\mathbb{R}^{d_x}}\Phi(x),\qquad\Phi(x)=\max_{y\in\mathbb{R}^{d_y}}f(x,y).
$$

### Admissible model

$f:\mathbb{R}^{d_x}\times\mathbb{R}^{d_y}\to\mathbb{R}$, with both blocks unconstrained and Euclidean norms throughout. The joint gradient satisfies $\|\nabla f(z)-\nabla f(w)\|_2\le \beta\|z-w\|_2$.

For every $x$, $f(x,\cdot)$ is uniformly $\mu_y$-strongly concave. Thus $y^\star(x)=\arg\max_y f(x,y)$ is unique and $\Phi(x)=f(x,y^\star(x))$ is differentiable. Neither $f(\cdot,y)$ nor $\Phi$ is assumed convex.

Assume $\inf_x\Phi(x)>-\infty$, with an initial point satisfying $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$.

The initial point $(x_0,y_0)=(0,0)$ is public. There is no uniform upper bound on $\|\nabla_y f(0,0)\|_2$, $\|y_0-y^\star(x_0)\|_2$, or the dual gap.

The dimension $d_x,d_y$ is a finite positive integer visible to the algorithm. Complexity takes a uniform worst case over these dimensions. Candidate budgets may not depend on the hidden instance’s dual-initialization scale.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $\Delta$, $\beta$, $\varepsilon$, and $\mu_y$, together with the stated initial-point and feasible-domain information. Analytic representations of hidden functions, operators, or matrices are not revealed.

$$
(x,y)\in\mathbb{R}^{d_x+d_y}\longmapsto (\nabla_x f(x,y),\nabla_y f(x,y))
$$

Responses are exact and noiseless; neither function values nor Hessians are returned.

The interface does not directly supply $y^\star(x)$, $\Phi(x)$, or $\nabla\Phi(x)$. Every primitive gradient used for inner optimization is charged.

### Output

Return a single $\widehat x\in\mathbb R^{d_x}$. No dual point is required.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\nabla\Phi(\widehat{x})\|_2
$$

The identity $\nabla\Phi(x)=\nabla_xf(x,y^\star(x))$ specifies the evaluation target and does not supply an additional Oracle interface.

### Resource accounting

One full joint gradient costs one $N_{\mathrm{grad}}$ call. Both blocks are returned together, not charged as two calls.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Here $+\infty$ means that for every finite candidate budget $N$, some finite dimension and admissible instance prevent any $N$-call algorithm from achieving success probability $2/3$. It does not assert that every fixed finite-dimensional instance is unsolvable or requires infinitely many calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(0)-\inf_x\Phi(x)\le\Delta$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the population smoothness upper bound, or mean-square average smoothness for finite sums, to the dual strong-concavity lower bound **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in \mathbb R^{d_y}}f(x,y)$

$y^\star(x)$: The unique global dual maximizer at fixed primal x. **Domain:** $y^\star(x)\in\mathbb R^{d_y}$.

$y^\star(x)=\arg\max_{y\in\mathbb R^{d_y}}f(x,y)$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm grad}$: The number of complete exact joint-gradient calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: This is the principal information-call budget on one instance. The resource specification determines whether it is fixed or a worst-instance expected budget. **Domain:** A nonnegative integer; expected budgets may be nonnegative real numbers.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$\mathcal F_{d_x,d_y}$: Function class satisfying the stated smoothness, strong concavity, and initial-gap assumptions at the given block dimensions **Domain:** The admissible hidden-instance class fixes $\beta$, $\mu_y$, and $\Delta$.

$\mathfrak A_{\rm succ}$: Algorithm families succeeding with probability at least $2/3$ for every admissible instance in every finite dimension. **Domain:** The algorithm may read the dimension, but its fixed query budget must be uniform over all dimensions.

$N_{\mathcal A}(I,\omega)$: Primary information calls accumulated by algorithm A on execution path omega of fixed instance I **Domain:** A nonnegative integer. For an almost surely terminating algorithm, use its complete stopping count.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star=\inf_{\mathcal A\in\mathfrak A_{\rm succ}}\ \sup_{d_x,d_y\ge1}\ \sup_{I\in\mathcal F_{d_x,d_y}}\ \sup_\omega N_{\mathcal A}(I,\omega)
$$

**Scope.** The algorithm may read the finite block dimensions. A single algorithm family must succeed with probability at least $2/3$ on every admissible instance, with a budget uniform over all finite dimensions. If no successful algorithm family or uniform finite budget exists, the complexity is $+\infty$.

**Optimization direction.** minimize

The algorithm class is exactly the declared legal algorithms attaining the adjacent specification guarantee; C is the declared charged resource projection. Expected-call objectives retain E N; fixed budgets take worst-case execution cost. The instance/oracle class and dimension regime remain those in the specification.

### R1 - Regime with a proved absence of any finite uniform budget

**Region.** Assume $\beta\ge4\mu_y$ and $\Delta\ge80\varepsilon^2/\beta$. Take the worst case over all finite dimensions; the initial dual error is unrestricted.

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Infinite complexity

**Lower bound.** B1

$$
+\infty
$$

**Comparison argument.** Without dual-initialization control, every finite budget admits an admissible finite-dimensional instance on which the algorithm fails. This is an impossibility result, not a missing search result.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Assume $\beta\ge4\mu_y>0$, $\varepsilon>0$, and $\Delta\ge80\varepsilon^2/\beta$; $\|\nabla_yf(0,0)\|_2$ is unrestricted.; The noiseless hard instances in Theorem 3.6 already belong to this exact joint-gradient model. Neither stochastic oracle noise nor a linear-span restriction is needed.; The hard distribution in Appendix B is fixed before interaction and independent of the algorithmic seed. At every finite budget $N$, average success probability is at most $7/12$. Hence some fixed admissible instance has success probability below $2/3$.

**Dimension conditions.** For each $N\ge1$, choose $d_x=1$ and chain length $m=4N+4$. Equation (20) of Theorem B.2 supplies a sufficiently large finite $d_y$. Both $d_y$ and initial dual residual may grow with $N$. Infinite complexity at fixed $d_y$ is not proved.

**Oracle mapping.** Each call returns both gradient blocks exactly. The source hard construction supplies no function values, Hessians, inner solutions, or reduced gradients, matching this interface exactly.

**Guarantee mapping.** The success event is $\|\nabla\Phi(\widehat x)\|_2\le\varepsilon$, with probability over the algorithmic seed only. A distribution-average success upper bound establishes failure on at least one fixed instance.

**Output mapping.** The successful primal-output intervals for the two hidden signs are disjoint. The output argument in Theorem B.2 allows unqueried points of arbitrary norm.

**Resource mapping.** A uniform finite integer N bounds all joint-gradient calls on every instance and every execution path. It is not a worst-instance expected stopping time.

### B1 - Two-ended dual chain with exact gradients: independent fair signs and a random orthogonal frame

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Definition 3.2 and Theorem B.2 explicitly allow arbitrary randomized adaptive unbounded queries and unqueried outputs.

$$
N^\star=+\infty
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00229v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
N^\star=+\infty
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.00229v2) theorem: Definitions 3.1–3.3; Theorem 3.6; Lemma B.1; Theorem B.2; Corollary B.3; section: Section 3.4; Appendix B.1–B.3; pdf pages: 6; 7; 8; 18; 19; 20; 21; equations: (17); (18); (19); (20)

The specification retains exact joint gradients, arbitrary randomized algorithms, fixed budgets, arbitrary primal outputs, the true reduced-gradient target, and the supremum over dimensions. The lower bound does not imply that any particular fixed instance is unsolvable.

Assume $\beta\ge4\mu_y>0$, $\varepsilon>0$, and $\Delta\ge80\varepsilon^2/\beta$; $\|\nabla_yf(0,0)\|_2$ is unrestricted.

The noiseless hard instances in Theorem 3.6 already belong to this exact joint-gradient model. Neither stochastic oracle noise nor a linear-span restriction is needed.

The hard distribution in Appendix B is fixed before interaction and independent of the algorithmic seed. At every finite budget $N$, average success probability is at most $7/12$. Hence some fixed admissible instance has success probability below $2/3$.

For each $N\ge1$, choose $d_x=1$ and chain length $m=4N+4$. Equation (20) of Theorem B.2 supplies a sufficiently large finite $d_y$. Both $d_y$ and initial dual residual may grow with $N$. Infinite complexity at fixed $d_y$ is not proved.

The successful primal-output intervals for the two hidden signs are disjoint. The output argument in Theorem B.2 allows unqueried points of arbitrary norm.

## References

[1] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Sharp Fresh-Gradient Complexity of Nonconvex--Strongly-Concave Minimax Optimization. 2026. arXiv:2610.00229v2, 2026-10-19.

https://arxiv.org/pdf/2610.00229v2
