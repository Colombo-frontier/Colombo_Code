# Linear bandits with parameter noise, known covariance, and a p-norm ball

**Setting ID.** `ONX_PARAMNOISE_LP_KNOWNCOV`

Online learning and bandits

Each round draws a fresh random parameter vector, and the learner observes only its exact projection along the selected action. Actions lie in the unit p-norm ball. Noise variance depends jointly on the direction and the public covariance matrix.

**Status.** Bounds missing

**TASK tags.** formulation: Onx paramnoise lp knowncov; task family: Online bandit

**MODEL tags.** structure: Linear

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Known covariance; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round draws a fresh random parameter vector, and the learner observes only its exact projection along the selected action. Actions lie in the unit p-norm ball. Noise variance depends jointly on the direction and the public covariance matrix.

### Admissible model

$$
\mathcal{A}=\{a\in\mathbb{R}^d:\|a\|_p\le1\},\qquad 1<p\le2,\qquad q=\frac{p}{p-1}.
$$

$$
\theta_t\overset{\mathrm{i.i.d.}}\sim\nu,\qquad \mathbb{E}\theta_t=\theta_*,\qquad \operatorname{Cov}(\theta_t)=\Sigma,\qquad |\langle a,\theta_t\rangle|\le1\quad\text{\text{almost everywhere},\quad \text{for every} }a\in\mathcal{A}.
$$

Randomness comes from a new parameter vector each round. Selected-action feedback is not a linear-regression model with additional homoscedastic scalar noise.

$$
N=T,\qquad \sigma_q^2=\left(\sum_{i=1}^{d}\Sigma_{ii}^{q/2}\right)^{2/q}.
$$

The quantity $N$ counts scalar observations. The quantity $\sigma_q^2$ is defined by the covariance diagonal and cannot be replaced by the maximum action variance.

### Oracle interface

$$
Y_t=\langle a_t,\theta_t\rangle,\qquad \operatorname{Var}(Y_t\mid a_t)=a_t^{\mathsf T}\Sigma a_t.
$$

The algorithm chooses $a_t$ before a fresh $\theta_t$ is drawn and observes only one scalar projection. The same $\theta_t$ defines rewards for all counterfactual actions that round, but the other projections remain hidden.

Causal policies are allowed. Public inputs are $d,p,q,T,\delta_{\mathrm{conf}}$ and covariance matrix $\Sigma$.

The distribution $\nu$ and mean parameter $\theta_*$ are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
a^*\in\operatorname*{arg\,max}_{a\in\mathcal{A}}\langle a,\theta_*\rangle,\qquad R_T=\sum_{t=1}^{T}\langle a^*-a_t,\theta_*\rangle.
$$

### Resource accounting

$$
N=T,\qquad \sigma_q^2=\left(\sum_{i=1}^{d}\Sigma_{ii}^{q/2}\right)^{2/q}.
$$

The quantity $N$ counts scalar observations. The quantity $\sigma_q^2$ is defined by the covariance diagonal and cannot be replaced by the maximum action variance.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

For every $\nu$ satisfying the stated support constraint, static pseudo-regret is controlled with probability at least $1-\delta_{\mathrm{conf}}$. This notation results from setting the source failure parameter to $\delta_{\mathrm{conf}}/2$.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\delta_{\mathrm{conf}}$: The allowed statistical failure probability. **Domain:** $0<\delta_{\mathrm{conf}}<1$.

Used only for statistical correctness or high-probability performance, and distinct from the privacy relaxation parameter.

$p$: Norm exponent of the action domain **Domain:** $1<p\le2$.

$\mathcal A=\{a:\|a\|_p\le1\}$.

$q$: The exponent conjugate to the action-norm exponent p. **Domain:** $q=p/(p-1)\in[2,\infty)$.

The relation is $1/p+1/q=1$, with finite real $q$, distinct from a recommendation distribution.

$\Sigma$: Covariance matrix of the parameter vector **Domain:** $\Sigma\in\mathbb R^{d\times d},\ \Sigma\succeq0$.

$\Sigma=\mathbb E_{\theta\sim\nu}[(\theta-\theta_*)(\theta-\theta_*)^{\mathsf T}]$.

$\sigma_q^2$: Aggregate scale formed from the $q/2$ powers of the covariance diagonal entries **Domain:** $\sigma_q^2\ge0$.

The quantity $\sigma_q^2=(\sum_{j=1}^d\Sigma_{jj}^{q/2})^{2/q}$ is not the maximum action variance.

$\mathcal A$: The fixed unit p-norm ball action set. **Domain:** $\mathcal A\subset\mathbb R^d$.

The action set is $\mathcal A=\{a:\|a\|_p\le1\}$; here $\mathcal A$ does not denote a learning algorithm.

$\nu$: Hidden distribution of the parameter vector **Domain:** Probability distribution on $\mathbb R^d$.

For every admissible action, $\theta_t\overset{\mathrm{i.i.d.}}\sim\nu$ and $|\langle a,\theta_t\rangle|\le1$ hold almost surely.

$\theta_t,\theta_*$: The current fresh parameter vector and its mean. **Domain:** $\theta_t,\theta_*\in\mathbb R^d$.

The hidden mean parameter is $\theta_*=\mathbb E_{\theta\sim\nu}\theta$ and does not vary with $t$.

$a_t,a^*$: Actual action and an action with optimal mean reward **Domain:** $a_t,a^*\in\mathcal A$.

$a^*\in\arg\max_{a\in\mathcal A}\langle a,\theta_*\rangle$.

$Y_t$: Exact projection of the random parameter onto the selected direction **Domain:** $Y_t\in[-1,1]$.

The observation is $Y_t=\langle a_t,\theta_t\rangle$ with conditional variance $a_t^{\mathsf T}\Sigma a_t$. There is no additional homoscedastic scalar noise.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t\langle a^*-a_t,\theta_*\rangle$. Realized observation noise is excluded from the loss difference; probability or expectation aggregation is specified separately by the guarantee.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes learner randomness and the explicitly specified reward or sample randomness. Conditional expectations retain their stated history conditioning.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
a^*\in\operatorname*{arg\,max}_{a\in\mathcal A}\langle a,\theta_*\rangle,\qquad R_T=\sum_{t=1}^{T}\langle a^*-a_t,\theta_*\rangle.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Assume $1<p\le2$, bounded realized rewards, known $\Sigma$, and a high-probability guarantee.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\widetilde{O}\!\left(d+\sqrt{dTq\log\!\left(\frac2{\delta_{\mathrm{conf}}}\right)\sigma_q^2}\right)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Assume $1<p\le2$ and $q=p/(p-1)$, with known covariance $\Sigma$; $\sigma_q^2=(\sum_{i=1}^d\Sigma_{ii}^{q/2})^{2/q}$.; Retain the additive $d$ term. The dimension dependence of this parameter-noise model cannot be transferred to an additive scalar Gaussian-noise model.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - A stochastic linear-bandit algorithm with known covariance.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(d+\sqrt{dTq\log\!\left(\frac2{\delta_{\mathrm{conf}}}\right)\sigma_q^2}\right)
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v306/main/assets/ezer26a/ezer26a.pdf)

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v306/main/assets/ezer26a/ezer26a.pdf) Theorem 3.7, PDF p.6

## References

[1] Daniel Ezer; Alon Peled-Cohen; Yishay Mansour. Stochastic Linear Bandits with Parameter Noise. 2026. ICML / PMLR 306:28463–28491.

https://raw.githubusercontent.com/mlresearch/v306/main/assets/ezer26a/ezer26a.pdf
