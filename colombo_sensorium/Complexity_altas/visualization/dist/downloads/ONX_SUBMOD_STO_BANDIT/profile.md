# Stochastic submodular minimization with single-set feedback and a positive gap.

**Setting ID.** `ONX_SUBMOD_STO_BANDIT`

Online learning and bandits

Each round selects a subset under i.i.d. submodular losses. The mean loss has a unique optimal subset and a positive gap. Only the chosen subset's loss is observed. The target is cumulative excess mean loss, and the gap is not revealed to the algorithm.

**Status.** Polynomial gap present

**TASK tags.** formulation: Onx submod sto bandit; task family: Online bandit

**MODEL tags.** structure: Submodular

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round selects a subset under i.i.d. submodular losses. The mean loss has a unique optimal subset and a positive gap. Only the chosen subset's loss is observed. The target is cumulative excess mean loss, and the gap is not revealed to the algorithm.

### Admissible model

An action is any subset of the ground set $[d]$. Random loss functions $f_t:2^{[d]}\to[0,1]$ are drawn independently from an unknown distribution $\mathcal{D}$, and every sample function is submodular. The mean function has a unique minimizing subset:

$$
\bar f(X)=\mathbb{E}_{f\sim\mathcal{D}}f(X),\qquad X^\star=\operatorname*{arg\,min}_{X\subseteq[d]}\bar f(X),
$$

$$
\Delta=\min_{X\ne X^\star}\bigl(\bar f(X)-\bar f(X^\star)\bigr)>0.
$$

### Oracle interface

The current function is sampled independently. The algorithm chooses $X_t$ and incurs $f_t(X_t)$ before receiving the round's feedback.

Only one scalar $f_t(X_t)$ for the selected subset is returned; other subsets cannot be queried additionally.

Randomness comes from function sampling; no additional value-query noise is added.

Causal policies are allowed; $d$ and $T$ are public.

The distribution $\mathcal{D}$, gap $\Delta$, and optimal subset $X^\star$ are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

In each round output a subset $X_t\subseteq[d]$. Final postprocessing cannot change losses already incurred. No separate optimal-subset recommendation or certificate is required.

### Loss or accuracy criterion

$$
\sum_{t=1}^{T}\mathbb{E}\bigl[\bar f(X_t)-\bar f(X^\star)\bigr].
$$

### Resource accounting

Exactly one value is observed per round; the total query count is $N=T$.

$$
\text{\text{computation per round}}=O\!\left(d\log d+\mathsf{EO}\right).
$$

The quantity $\mathsf{EO}$ is the cost of one set-function value evaluation. This computational notation retains the original accounting convention.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Minimize worst-case expected regret over i.i.d. loss classes whose mean has a unique optimal subset with the stated positive gap. Expectation includes random sample functions and algorithmic randomness.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ground-set size of the submodular function. **Domain:** $d\in\mathbb N,\ d\ge1$.

An action is any subset of $[d]=\{1,\ldots,d\}$.

$\Delta$: Smallest mean-loss gap between the unique optimal subset and every other subset **Domain:** $0<\Delta\le1$.

The quantity $\Delta=\min_{X\ne X^\star}[\bar f(X)-\bar f(X^\star)]$ is not supplied to the algorithm.

$[d],2^{[d]}$: Ground set and the action space consisting of all its subsets **Domain:** A finite set and its power set.

$[d]=\{1,\ldots,d\}$. Every subset is an admissible action.

$\mathcal D,f_t$: Unknown sample-function distribution and an independent sample in each round **Domain:** Distribution over submodular functions taking values in $[0,1]$.

$f_t\overset{\mathrm{i.i.d.}}\sim\mathcal D$. Submodularity means $f(A)+f(B)\ge f(A\cup B)+f(A\cap B)$.

$\bar f$: Mean loss function **Domain:** Real-valued submodular set function.

$\bar f(X)=\mathbb E_{f\sim\mathcal D}f(X)$.

$X_t,X^\star$: Current action subset and the unique subset with optimal mean **Domain:** $X_t,X^\star\subseteq[d]$.

$X^\star=\arg\min_X\bar f(X)$.

$\mathsf{EO}$: Arithmetic cost of one set-function evaluation **Domain:** The unit of computation cost.

Only one $f_t(X_t)$ is supplied per round. Other sets cannot be evaluated for free.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_t[\bar f(X_t)-\bar f(X^\star)]$ Realized observation noise is excluded from the loss difference. Probability or expectation aggregation is specified separately by the guarantee.

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

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
\sum_{t=1}^{T}\mathbb E\bigl[\bar f(X_t)-\bar f(X^\star)\bigr].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Assume $d\ge 4,T\ge d^{2},0<\Delta<1/(4d)$; when $T\ge (1/\Delta)^{2}$, the lower bound is d/Delta.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(\min\{d/\Delta,d\sqrt T\})
$$

**Upper bound.** B1

$$
O(d^3\log(T)/\Delta^2)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Stochastic submodular minimization with single-set feedback

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{d^3\log T}{\Delta^2}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v162/ito22a/ito22a.pdf)

**Conditions.** The mean function has a unique optimal subset with gap $\Delta>0$, unknown to the algorithm. Each round reveals only the value at the selected subset.

**Source location.** [1](https://proceedings.mlr.press/v162/ito22a/ito22a.pdf) Theorem 4.7, PDF p.7

### B2 - Stochastic submodular hard instances for arbitrary randomized algorithms.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\min\!\left\{\frac d\Delta,d\sqrt T\right\}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v162/ito22a/ito22a.pdf)

**Conditions.** Require $d\ge4$, $T\ge d^2$, and $0<\Delta<1/(4d)$.; This is a partial-feedback lower bound. The catalog comparison between $1/\Delta$ and $d/\Delta$ concerns full feedback and cannot be combined across feedback modes.

**Source location.** [1](https://proceedings.mlr.press/v162/ito22a/ito22a.pdf) Theorem 5.1, PDF p.8 with C=0

## References

[1] Shinji Ito. Revisiting Online Submodular Minimization: Gap-Dependent Regret Bounds, Best of Both Worlds and Adversarial Robustness. 2022. ICML 2022, PMLR 162.

https://proceedings.mlr.press/v162/ito22a/ito22a.pdf
