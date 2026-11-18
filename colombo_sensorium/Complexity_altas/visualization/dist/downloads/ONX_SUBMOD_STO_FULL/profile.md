# Stochastic submodular minimization with full value feedback and a positive gap.

**Setting ID.** `ONX_SUBMOD_STO_FULL`

Online learning and bandits

The learner chooses a subset each round against i.i.d. submodular losses whose mean has a unique optimal subset and a positive gap. After acting, the learner may query the current loss function at any subset. The objective is cumulative excess mean loss, and the gap is not disclosed.

**Status.** Bounds missing

**TASK tags.** formulation: Onx submod sto full; task family: Online bandit

**MODEL tags.** structure: Submodular

**ORACLE tags.** interface family: Full current function; operation: Full current function; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

The learner chooses a subset each round against i.i.d. submodular losses whose mean has a unique optimal subset and a positive gap. After acting, the learner may query the current loss function at any subset. The objective is cumulative excess mean loss, and the gap is not disclosed.

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

After acting, the learner may query the same $f_t(X)$ at any subset $X$. This is full value-query access.

Randomness comes from function sampling; no additional value-query noise is added.

The distribution $\mathcal{D}$, gap $\Delta$, and optimal subset $X^\star$ are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

In each round output a subset $X_t\subseteq[d]$. Final postprocessing cannot change losses already incurred. No separate optimal-subset recommendation or certificate is required.

### Loss or accuracy criterion

$$
\sum_{t=1}^{T}\mathbb{E}\bigl[\bar f(X_t)-\bar f(X^\star)\bigr].
$$

### Resource accounting

The source algorithm evaluates $d+1$ subsets per round, so its total value-query count is $N=(d+1)T$. Full-feedback permissions and the witness algorithm's actual query count are recorded separately.

$$\text{Computation per round}=O(d\,\mathsf{EO}\log d).$$

The quantity $\mathsf{EO}$ is the cost of one set-function value evaluation. This computational notation retains the original accounting convention.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

Causal policies are allowed. Only ground-set size $d$ is required as a public tuning input; the horizon need not be supplied.

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

The full-function interface permits evaluating multiple subsets of the revealed $f_t$, with each evaluation charged separately.

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

The recorded upper-bound algorithm uses $N=(d+1)T$ set-function evaluations. Full-function feedback does not imply unlimited free computation.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
\sum_{t=1}^{T}\mathbb E\bigl[\bar f(X_t)-\bar f(X^\star)\bigr].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** A unique optimal subset, with $\Delta>0$ hidden; full-function value interface.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
O(d/\Delta)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The mean function has a unique optimal subset and gap $\Delta>0$, which the algorithm need not know. This contract uses full value-query feedback.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Stochastic submodular minimization with full-function feedback.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac d\Delta\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v162/ito22a/ito22a.pdf)

**Source location.** [1](https://proceedings.mlr.press/v162/ito22a/ito22a.pdf) Theorem 4.3, PDF p.6 Eq.(14)

## References

[1] Shinji Ito. Revisiting Online Submodular Minimization: Gap-Dependent Regret Bounds, Best of Both Worlds and Adversarial Robustness. 2022. ICML 2022, PMLR 162.

https://proceedings.mlr.press/v162/ito22a/ito22a.pdf
