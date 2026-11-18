# Nonconvex-PL minimax optimization: fresh gradients and reduced-objective stationarity

**Setting ID.** `CV_S_NCPL_FRESH_REDUCED`

Minimax optimization

Solve $\min_x\Phi(x)$, where $\Phi(x)=\max_yf(x,y)$.

**Status.** Bounds missing

**TASK tags.** task family: Minimax

**MODEL tags.** growth: Dual pl; initialization: Initialization; smoothness: Lipschitz

**ORACLE tags.** feedback quality: Stochastic unbiased bounded variance; interface family: Fresh joint gradient; operation: Stochastic joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_x\Phi(x)$, where $\Phi(x)=\max_yf(x,y)$.

### Admissible model

The function $f:\mathbb{R}^{d_x+d_y}\to\mathbb{R}$ is continuously differentiable with $\beta$-Lipschitz joint gradient. For each $x$, the value $\Phi(x)=\max_y f(x,y)$ is finite and attained, and the dual PL condition holds:

$$
\|\nabla_y f(x,y)\|_2^2\ge2\mu_y\bigl(\Phi(x)-f(x,y)\bigr).
$$

Concavity in the $y$ direction and uniqueness of the maximizer are not required; set $\kappa=\beta/\mu_y\ge1$. Global PL and smoothness imply a differentiable value function, and $\nabla\Phi(x)$ is independent of the selected maximizer.

Assume $\inf\Phi> -\infty$ and $\Phi(x_0)-\inf\Phi\le H$. Define $h_{x_0}(x,y)=f(x,y)+\beta\|x-x_0\|_2^2$, and additionally require

$$
b_0=2\bigl[\max_yh_{x_0}(x_0,y)-\min_xh_{x_0}(x,y_0)\bigr]\le c_{\rm init}H.
$$

The quantity $c_{\rm init}$ is a fixed public constant. This initialization condition does not follow automatically from the primal gap.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $H$, $\beta$, $c_{\rm init}$, $\varepsilon$, $\mu_y$, $\sigma$, together with the stated initial point and feasible geometry. The analytic representation of the hidden function, operator, or matrix is not revealed.

$$
(x,y)\longmapsto G_f(x,y;\xi)=(G_x,G_y).
$$

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^{d_x+d_y}$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=\nabla f(z_t)$ and $\mathbb E[\|G_t-\nabla f(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

No best response, reduced gradient, or function value is supplied.

### Output

Return $\widehat x\in\mathbb R^{d_x}$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\nabla\Phi(\widehat{x})\|_2
$$

### Resource accounting

One complete joint-gradient sample at one point costs one call. Using independent samples at two points in an iteration costs two.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\|\nabla\Phi(\widehat{x})\|_2\right)^2\right]\le\varepsilon^2.
$$

Expectation is over private algorithmic randomness and the random samples actually used.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$H$: Public scale jointly controlling the initial reduced-objective gap and auxiliary initial saddle gap **Domain:** Positive real number.

$\Phi(x_0)-\inf\Phi\le H,\qquad b_0\le c_{\rm init}H$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$c_{\rm init}$: Fixed upper bound on the ratio between an auxiliary initial gap and $H$. **Domain:** A fixed positive constant.

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the joint smoothness bound to the dual PL constant **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\mu_y$: Uniform positive constant in the dual PL inequality for every fixed x **Domain:** $0<\mu_y\le\beta$.

$\|\nabla_yf(x,y)\|_2^2\ge2\mu_y(\Phi(x)-f(x,y))$

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** A nonnegative real.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in \mathbb R^{d_y}}f(x,y)$

$\operatorname{Argmax}_y f(x,y)$: The nonempty set of global dual maximizers at fixed x. It need not be a singleton. **Domain:** Nonempty closed subset of the dual-variable space.

$\{y:f(x,y)=\Phi(x)\}$

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

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$h_{x_0}$: Regularized payoff centered at the public initial primal variable **Domain:** A real-valued function on $\mathbb R^{d_x+d_y}$.

$h_{x_0}(x,y)=f(x,y)+\beta\|x-x_0\|_2^2$

$b_0$: Twice the primal–dual gap of the first regularized saddle problem at the public initial point **Domain:** A nonnegative real.

$b_0=2[\max_y h_{x_0}(x_0,y)-\min_x h_{x_0}(x,y_0)]$

$a_0$: The initial dual-value gap in the Stochastic AGDA analysis is controlled by the declared b0 bound. **Domain:** A nonnegative real.

$a_0=\Phi(x_0)-f(x_0,y_0)\le b_0/2$

$T,J$: The predetermined iteration count and independent uniform output index. **Domain:** $T\ge1,\ J\sim\operatorname{Unif}\{0,\ldots,T-1\}$.

$\mathfrak A_{\rm succ}$: Algorithms satisfying the declared mean-square reduced-gradient guarantee on every admissible instance. **Domain:** A subset of the admitted randomized adaptive algorithm class.

$C$: Sufficiently large positive constant in the source's unbalanced error expression; it may depend on fixed $c_{\rm init}$ **Domain:** A constant, not a new instance parameter.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm grad}(\mathcal A,I,\omega)
$$

**Scope.** Fixed worst-case complete joint-sample call count under this profile's per-instance mean-square reduced-gradient guarantee

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The declared parameter domain.

**Region.** Assume $H>0$, $\varepsilon>0$, $0<\mu_y\le\beta$, and $\sigma\ge0$, together with the global dual PL condition, $\Phi(x_0)-\inf\Phi\le H$, and $b_0\le c_{\rm init}H$ specified here. The parameter $c_{\rm init}$ is fixed and public.

**Quantity.** Q1

**Resource.** Fixed worst-case number of complete joint gradients from fresh samples

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O\!\left(1+\frac{\beta\kappa^2 H}{\varepsilon^2}+\frac{\beta\kappa^4 H\sigma^2}{\varepsilon^4}\right)
$$

**Comparison argument.** The direct mean-square reduced-gradient upper bound of Theorem 3.1 applies after mapping the declared initialization conditions. No lower bound under the same contract is included.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The source Theorem 3.1 directly controls $T^{-1}\sum_{t=0}^{T-1}\mathbb E\|\nabla\Phi(x_t)\|_2^2$. Let $a_0=\Phi(x_0)-f(x_0,y_0)$. From $\min_u h_{x_0}(u,y_0)\le h_{x_0}(x_0,y_0)=f(x_0,y_0)$ we obtain $a_0\le b_0/2\le c_{\rm init}H/2$, and also $\Phi(x_0)-\inf\Phi\le H$. Use the unbalanced bound following equation (18) of the source proof, choosing a fixed step size and fixed T from the public H. This gives $C(\beta\kappa^2H/T+\kappa^2\sigma\sqrt{\beta H/T})$, with constants depending only on fixed $c_{\rm init}$. Thus the fixed choice $T=O(1+\beta\kappa^2H/\varepsilon^2+\beta\kappa^4H\sigma^2/\varepsilon^4)$ suffices for the stated mean-square guarantee.

**Dimension conditions.** The upper bound holds for arbitrary finite positive block dimensions $d_x,d_y$.

**Oracle mapping.** Algorithm 1 of the source uses two independent fresh samples per step: a primal gradient at $(x_t,y_t)$, then a dual gradient at $(x_{t+1},y_t)$. Simulate each block sample with one complete joint-gradient query and discard the unused block. The joint variance bound implies the same bound for either block. Independent fresh calls respect the stated protocol.

**Guarantee mapping.** Uniform output selection gives $\mathbb E\|\nabla\Phi(\widehat x)\|_2^2=T^{-1}\sum_t\mathbb E\|\nabla\Phi(x_t)\|_2^2\le\varepsilon^2$. This does not infer a mean-square guarantee from an expected-norm guarantee.

**Output mapping.** Select $J$ independently and uniformly from $\{0,\ldots,T-1\}$ and return $\widehat x=x_J$. A dual point is not required, and output selection does not require evaluating the true reduced gradient.

**Resource mapping.** Every execution uses exactly $2T$ fresh full joint-gradient calls. Public constants and target accuracy determine $T$ and both step sizes in advance. There is no random stopping or expected-budget conversion.

### B1 - Stochastic AGDA with a uniformly random primal iterate as output.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(1+\frac{\beta\kappa^2 H}{\varepsilon^2}+\frac{\beta\kappa^4 H\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v151/yang22b/yang22b.pdf)

**Constants.** Universal constants may be multiplied by a function of the fixed public initialization ratio $c_{\rm init}$; no other polynomial instance dependence is hidden.

**Derivation.** The source Theorem 3.1 directly controls $T^{-1}\sum_{t=0}^{T-1}\mathbb E\|\nabla\Phi(x_t)\|_2^2$. Let $a_0=\Phi(x_0)-f(x_0,y_0)$. From $\min_u h_{x_0}(u,y_0)\le h_{x_0}(x_0,y_0)=f(x_0,y_0)$ we obtain $a_0\le b_0/2\le c_{\rm init}H/2$, and also $\Phi(x_0)-\inf\Phi\le H$. Use the unbalanced bound following equation (18) of the source proof, choosing a fixed step size and fixed T from the public H. This gives $C(\beta\kappa^2H/T+\kappa^2\sigma\sqrt{\beta H/T})$, with constants depending only on fixed $c_{\rm init}$. Thus the fixed choice $T=O(1+\beta\kappa^2H/\varepsilon^2+\beta\kappa^4H\sigma^2/\varepsilon^4)$ suffices for the stated mean-square guarantee.

**Source location.** [1](https://proceedings.mlr.press/v151/yang22b/yang22b.pdf) theorem: Assumptions 2.1–2.3; Algorithm 1; Theorem 3.1; section: Sections 2–3; Appendix B; pdf pages: 4; 5; 18; 19; 20; equations: (18); telescoping inequality following (18)

The source Theorem 3.1 directly controls $T^{-1}\sum_{t=0}^{T-1}\mathbb E\|\nabla\Phi(x_t)\|_2^2$. Let $a_0=\Phi(x_0)-f(x_0,y_0)$. From $\min_u h_{x_0}(u,y_0)\le h_{x_0}(x_0,y_0)=f(x_0,y_0)$ we obtain $a_0\le b_0/2\le c_{\rm init}H/2$, and also $\Phi(x_0)-\inf\Phi\le H$. Use the unbalanced bound following equation (18) of the source proof, choosing a fixed step size and fixed T from the public H. This gives $C(\beta\kappa^2H/T+\kappa^2\sigma\sqrt{\beta H/T})$, with constants depending only on fixed $c_{\rm init}$. Thus the fixed choice $T=O(1+\beta\kappa^2H/\varepsilon^2+\beta\kappa^4H\sigma^2/\varepsilon^4)$ suffices for the stated mean-square guarantee.

A fixed T iterations, with two independent joint-gradient samples each, gives total budget 2T.

Uniformly random output gives a mean-square guarantee for the true reduced gradient.

## References

[1] Junchi Yang; Antonio Orvieto; Aurelien Lucchi; Niao He. Faster Single-loop Algorithms for Minimax Optimization without Strong Concavity. 2022. AISTATS2022 PMLR151.

https://proceedings.mlr.press/v151/yang22b/yang22b.pdf
