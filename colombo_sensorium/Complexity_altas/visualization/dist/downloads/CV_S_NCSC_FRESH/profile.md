# Nonconvex–strongly concave optimization with fresh-sample joint gradients

**Setting ID.** `CV_S_NCSC_FRESH`

Minimax optimization

$$
\min_{x\in\mathbb{R}^{d_x}}\Phi(x),\qquad\Phi(x)=\max_{y\in\mathbb{R}^{d_y}}f(x,y).
$$

**Status.** Logarithmic gap present

**TASK tags.** formulation: Minimize value function; task family: Minimax

**MODEL tags.** convexity: No convexity promise in block; convexity: Nonconvex strongly concave; convexity: Strong concavity in the declared block; initialization: Bounded dual residual; initialization: Dual initial residual; initialization: Initial suboptimality; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Conditionally unbiased e noise 2 past query sigma 2; interface family: Fresh joint gradient; operation: Stochastic joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

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

The public initial point is $(x_0,y_0)=(0,0)$, with public dual-residual bound $\|\nabla_yf(0,0)\|_2\le G$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $\Delta$, $G$, $\beta$, $\varepsilon$, $\mu_y$, and $\sigma$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(x,y)\in\mathbb{R}^{d_x+d_y}\longmapsto G_f(x,y;\xi)=(G_x,G_y)
$$

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^{d_x+d_y}$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=\nabla f(z_t)$ and $\mathbb E[\|G_t-\nabla f(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

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

One full joint-gradient sample costs one $N_{\rm grad}$ call. Both blocks are returned together and do not count as two calls.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability includes only algorithm randomness and explicitly permitted stochastic feedback. The guarantee is not averaged over an instance distribution.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$A_{\mathrm{det}}$: Deterministic primal-progress scale **Domain:** A nonnegative real.

$A_{\mathrm{det}}=\sqrt\kappa\,\beta\Delta/\varepsilon^2$

$B_{\mathrm{noise},1}$: The statistical sampling scale across outer progress. **Domain:** A nonnegative real.

$B_{\mathrm{noise},1}=\kappa\beta\Delta\sigma^2/\varepsilon^4$

$B_{\mathrm{noise},2}$: The final statistical-refinement scale. **Domain:** A nonnegative real.

$B_{\mathrm{noise},2}=\kappa^2\sigma^2/\varepsilon^2$

$C_0$: Universal sufficient constant in the nontrivial accuracy regime; no numerical value is specified. **Domain:** Positive proof constant with no specified numerical value.

$C_{\mathrm{up}}$: The universal numerical constant in the source upper bound. **Domain:** Positive proof constant with no specified numerical value.

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(0)-\inf_x\Phi(x)\le\Delta$

$G$: Euclidean norm bound on the dual gradient at the public initial point **Domain:** A nonnegative real.

$\|\nabla_yf(x_0,y_0)\|_2\le G$

$I_G$: Logarithmic scale needed for dual initialization **Domain:** A nonnegative real.

$I_G=\sqrt\kappa\log_+\!\left(\frac{G}{\varepsilon\sqrt\kappa}\right)$

$\Lambda$: Dimensionless logarithmic overhead independent of $G$ **Domain:** Positive real number.

$\Lambda=1+\log(2+\kappa)+\log(2+\beta\Delta/\varepsilon^2)+\log(2+\kappa^2\sigma^2/\varepsilon^2)$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$c$: Universal positive constant in the source lower bound **Domain:** Positive proof constant with no specified numerical value.

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the population smoothness upper bound, or mean-square average smoothness for finite sums, to the dual strong-concavity lower bound **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\kappa_0$: Universal sufficient condition-number threshold in the lower-bound theorem; its numerical value is unspecified. **Domain:** Positive proof constant with no specified numerical value.

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** Positive real number.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

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

$G_f(z;\xi),G_t$: Random sample of the full joint gradient and the response from sample $t$ **Domain:** $\mathbb R^{d_x+d_y}$. The two blocks may be internally correlated.

$G_f=(G_x,G_y)$

$G_x,G_y$: The primal and dual blocks in one complete joint-gradient sample. **Domain:** $G_x\in\mathbb R^{d_x},\ G_y\in\mathbb R^{d_y}$.

$\xi,\mathcal H_t,z_t$: Current fresh-sample seed, complete pre-query history, and query point. **Domain:** The seed space, history-generated $\sigma$-algebra, and declared query domain.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm grad}$: Number of full joint-gradient queries using fresh samples **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm grad}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The nontrivial condition-number and accuracy region.

**Region.** Assume $\kappa\ge\kappa_0$ and $\beta\Delta\ge C_0\varepsilon^2$.

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
c(A_{\mathrm{det}}+B_{\mathrm{noise},1}+B_{\mathrm{noise},2}+I_G)
$$

**Upper bound.** B1

$$
C_{\mathrm{up}}\Lambda^{10}[A_{\mathrm{det}}+B_{\mathrm{noise},1}+B_{\mathrm{noise},2}+\sqrt\kappa\log(2+\kappa^2G^2/\varepsilon^2+\kappa^2\beta\Delta/\varepsilon^2)]
$$

**Gap or comparison.** $U/L\le C\Lambda^{11}$

**Comparison argument.** Combine four nonnegative lower bounds using max >= sum/4. The logarithm satisfies log(2+$\kappa$^3 u^2+$\kappa$^2 $\beta$$\Delta$/eps^2) <= C[log(2+$\kappa$)+log(2+$\beta$$\Delta$/eps^2)+$\log_+$u]. Under $\beta$$\Delta$/eps^2 >= C0, the additional initialization logarithm is absorbed by A and D_G.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - coarse proximal progress plus one final refinement; global truncation fixes query budget

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** Source Algorithm 1 selects a random outer index, and its subroutine also uses fresh samples and multilevel randomized corrections.

$$
C_{\mathrm{up}}\Lambda^{10}[A_{\mathrm{det}}+B_{\mathrm{noise},1}+B_{\mathrm{noise},2}+\sqrt\kappa\log(2+\kappa^2G^2/\varepsilon^2+\kappa^2\beta\Delta/\varepsilon^2)]
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00229v2)

**Conditions.** The logarithmic terms involving $G$ are additive before multiplication of the full expression by $\Lambda^{10}$. The noiseless branch is implemented by an actual deterministic solver.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
C_{\mathrm{up}}\Lambda^{10}[A_{\mathrm{det}}+B_{\mathrm{noise},1}+B_{\mathrm{noise},2}+\sqrt\kappa\log(2+\kappa^2G^2/\varepsilon^2+\kappa^2\beta\Delta/\varepsilon^2)]
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** $\Lambda=1+\log(2+\kappa)+\log(2+\beta\Delta/\varepsilon^2)+\log(2+\kappa^2\sigma^2/\varepsilon^2)$. The exact-interface special case sets $\sigma=0$.

**Source location.** [1](https://arxiv.org/pdf/2610.00229v2) Definitions3.1–3.3; Theorem3.4; Corollary3.5; Theorem3.6

Localized fresh-gradient unrestricted randomized fixed-budget complexity and no-localization obstruction.

Exact source uses a fixed Markov kernel, conditional unbiasedness/variance, all finite dimensions and no sample reuse. Source C1 is the upper constant, C is the statistical refinement scale; atlas typo merged them. New names C_up and B_noise,2 repair only notation. The unlocalized infinity theorem is dimension-uniform, not an assertion of unsolvability of every fixed finite instance.

The fixed worst-case call budget, conditional feedback law, unrestricted query domain, and inner-initialization cost have been checked.

### B2 - separate primal chain, local testing and dual-localization hard families

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
c(A_{\mathrm{det}}+B_{\mathrm{noise},1}+B_{\mathrm{noise},2}+I_G)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00229v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The finite hard-instance dimension may grow with the candidate call budget. The same-order lower bound is not claimed in fixed small dimension.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
c(A_{\mathrm{det}}+B_{\mathrm{noise},1}+B_{\mathrm{noise},2}+I_G)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.00229v2) Definitions3.1–3.3; Theorem3.4; Corollary3.5; Theorem3.6

Localized fresh-gradient unrestricted randomized fixed-budget complexity and no-localization obstruction.

Exact source uses a fixed Markov kernel, conditional unbiasedness/variance, all finite dimensions and no sample reuse. Source C1 is the upper constant, C is the statistical refinement scale; atlas typo merged them. New names C_up and B_noise,2 repair only notation. The unlocalized infinity theorem is dimension-uniform, not an assertion of unsolvability of every fixed finite instance.

The fixed worst-case call budget, conditional feedback law, unrestricted query domain, and inner-initialization cost have been checked.

## References

[1] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Sharp Fresh-Gradient Complexity of Nonconvex--Strongly-Concave Minimax Optimization. 2026. arXiv:2610.00229v2, 2026-10-19.

https://arxiv.org/pdf/2610.00229v2
