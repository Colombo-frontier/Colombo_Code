# Best-arm identification with bounded rewards: fixed budget and known difficulty upper bound.

**Setting ID.** `ON_FB_CAP_S`

Online learning and bandits

The algorithm knows a hardness upper bound controlling all arm gaps and identifies the best arm under a fixed sample budget. Performance is the maximum identification error over that hardness class. Constants in an error exponent and multiplicative approximation of the probability are different comparisons.

**Status.** Fully optimal

**TASK tags.** formulation: Best arm fixed budget; solution concept: Minimize error probability; task family: Online bandit

**MODEL tags.** stochastic model: Bounded iid rewards; structure: Finite actions; structure: Public complexity cap

**ORACLE tags.** feedback quality: Source-declared exact feedback (may be a random reward); interface family: Selected reward; operation: Sample selected arm; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Terminal arm recommendation

**METRIC tags.** criterion: Fixed budget error

**GUARANTEE tags.** mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

The algorithm knows a hardness upper bound controlling all arm gaps and identifies the best arm under a fixed sample budget. Performance is the maximum identification error over that hardness class. Constants in an error exponent and multiplicative approximation of the probability are different comparisons.

### Admissible model

Fixed unknown reward distributions $\nu_i$, supported on [0,1], with each sample fresh and independent.

Public $h$ bounds instance complexity through $H\le h$. Individual arm gaps remain hidden.

The recommendation $\widehat b_T$ after exhausting the fixed budget; the native error is misidentification probability.

Assume $K\ge2$, a fixed integer sample budget $N=T\ge1$, and a unique best arm. The recorded comparison requires $h\ge11K^2$; other complexity windows require their own status assessment.

The sum defining $H$ includes suboptimal arms only. The source UCB-E quantity $H_1$ repeats the minimum-gap term for the best arm; this conversion is recorded in the bound's derivation.

### Oracle interface

Sampling an arm with bounded rewards:

$$
t\in[T],\quad a_t\in[K]\ \longmapsto\ Y_t\mid\mathcal{H}_{t-1},a_t\sim\nu_{a_t}
$$

An arm is selected before one fresh reward sample is returned.

After all T calls are used, only internal computation and recommendation are allowed; no extra confirmation sample is available.

The learner may tune parameters using public h, but not hidden gaps.

Public inputs are $K,T$, complexity upper bound $h$, and reward support $[0,1]$.

### Output

After at most $T$ samples, return a recommended arm $\widehat{b}_T\in[K]$. Any postprocessing of the observed history is allowed. The arm need not have been sampled, and no additional certificate is required.

### Loss or accuracy criterion

$$
H(\nu)=\sum_{i\ne b}(\mu_b-\mu_i)^{-2}\le h,\qquad p_{\mathcal{A},\nu,T}=\mathbb{P}_{\mathcal{A},\nu}(\widehat{b}_T\ne b)
$$

### Resource accounting

Use exactly $T$ arm pulls and compare the final error probability $p_{\mathrm{error}}$. This objective does not involve a random stopping time.

All causal algorithms knowing h are allowed. UCB-E is tuned using the public upper bound h.

Sample averages, index comparisons, and recommendation are internal operations. Error-exponent comparisons retain polynomial prefactors and applicability windows.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
p^*(K,T,h)=\inf_{\mathcal{A}(K,T,h)}\sup_{\nu:\ H(\nu)\le h}\mathbb{P}_{\mathcal{A},\nu}(\widehat{b}_T\ne b(\nu))
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** Use exactly T arm pulls, then recommend one arm to minimize worst-case error probability.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$T$: The exact fixed sample budget used before the final recommendation. **Domain:** $T\in\mathbb N,\ T\ge1$.

Each pull gives one fresh sample, for a total of $N=T$ samples. Stopping is not data-dependent.

$h$: Public upper bound on instance difficulty **Domain:** $h\ge11K^2$, the currently documented window.

$H(\nu)=\sum_{i\ne b}(\mu_b-\mu_i)^{-2}\le h$. The public quantity h does not reveal individual arm gaps.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\nu_i,\mu_i$: Fixed arm-reward distribution and its mean **Domain:** $\operatorname{supp}(\nu_i)\subseteq[0,1],\ \mu_i\in[0,1]$.

$\mu_i=\mathbb E_{Y\sim\nu_i}Y$.

$b$: Arm with the unique largest mean **Domain:** $b\in[K]$.

$b=\arg\max_i\mu_i$.

$\Delta_i$: Mean gap of a suboptimal arm **Domain:** $i\ne b,\ 0<\Delta_i\le1$.

$\Delta_i=\mu_b-\mu_i$.

$H$: True instance difficulty **Domain:** A positive real unknown to the algorithm.

$H=\sum_{i\ne b}\Delta_i^{-2}\le h$.

$H_1$: Instance difficulty used in the source UCB-E result **Domain:** A positive real used only in the source-theorem transfer.

$H_1=H+(\min_{i\ne b}\Delta_i)^{-2}\le2H$.

$\widehat b_T$: Recommended arm after T samples **Domain:** $\widehat b_T\in[K]$.

$p^*(K,T,h)$: Minimax error probability over instances of difficulty at most $h$. **Domain:** $p^*\in[0,1]$.

$$
\inf_{\mathcal A(K,T,h)}\sup_{\nu:H(\nu)\le h}\Pr_{\mathcal A,\nu}(\widehat b_T\ne b)
$$.

$\alpha$: The exploration parameter of UCB-E. **Domain:** A nonnegative real.

Use $\alpha=25(T-K)/(72h)$ in the stated window $T\ge2K$.

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

#### Q1 - minimax fixed budget error

$$
\begin{aligned} p^*(K,T,h)&=\inf_{\mathcal A(K,T,h)}\sup_{\nu\in\mathcal I_h}\mathbb P_{\nu,\mathcal A}(\widehat b_T\ne b(\nu)),\\ \mathcal I_h&=\{\nu:\ \operatorname{supp}(\nu_i)\subset[0,1],\ b(\nu)\text{ is unique},\ H(\nu)\le h\},\\ H(\nu)&=\sum_{i\ne b(\nu)}(\mu_{b(\nu)}-\mu_i)^{-2}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - LARGE_BUDGET

**Region.** $K\ge 2, h\ge 11K^2; T\ge 2K; T\ge h^2 \log(6TK)/900; T\ge 144h \log(2TK)$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
(1/6) \exp[-120T/h]
$$

**Upper bound.** B1

$$
2TK \exp[-(T-K)/(36h)]
$$

**Gap or comparison.** Within the stated regime, -log p* and T/h have the same order. This does not imply a constant ratio between the two error probabilities.

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $K\ge2$, $h\ge11K^2$, and $T\ge2K$, with instance complexity $H\le h$.; The budgets must additionally satisfy both $T\ge h^2\log(6TK)/900$ and $T\ge144h\log(2TK)$.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - UCB-E with cap-tuned exploration

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
p^*(K,T,h)\le\min\left\{1,\ 2TK\exp\left(-\frac{T-K}{36h}\right)\right\}
$$

**Sources.** [1](https://www.learningtheory.org/colt2010/papers/59Audibert.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** The source complexity $H_1$ duplicates the smallest suboptimal gap at the optimal-arm position, so $H_1\le2H\le2h$. Exploration parameter $\alpha=25(T-K)/(72h)$ meets the source condition $\alpha\le25(T-K)/(36H_1)$. Substituting into the UCB-E error bound and using this region's budget condition gives $-\log p^\star\ge T/(144h)$, where $p^\star$ is minimax error over the class with complexity at most $h$.

**Source location.** [1](https://www.learningtheory.org/colt2010/papers/59Audibert.pdf) theorem: Theorem 1; pdf pages: 4

UCB-E has error probability at most $2TK\exp(-2\alpha/25)$, provided $\alpha\le25(T-K)/(36H_1)$. In $H_1$, the best-arm coordinate duplicates the inverse squared smallest suboptimality gap.

### B2 - Carpentier–Locatelli finite-bandit lower family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
p^*(K,T,h)\ge\frac16\exp\left(-\frac{120T}{h}\right)
$$

**Sources.** [2](https://proceedings.mlr.press/v49/carpentier16.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [2](https://proceedings.mlr.press/v49/carpentier16.pdf) theorem: Theorem 1; pdf pages: 6

Complexity is $H=\sum_{i\ne i^\star}\Delta_i^{-2}$. Over instances with complexity at most $h$, worst-case error is at least $(1/6)\exp(-120T/h)$ when $T\ge h^2\log(6TK)/900$. A separate source result for instance-adaptive policies contains $\log K$ and is not mixed with this class-budget target.

## References

[1] Jean-Yves Audibert; Sébastien Bubeck; Rémi Munos. Best Arm Identification in Multi-Armed Bandits. 2010. COLT 2010.

https://www.learningtheory.org/colt2010/papers/59Audibert.pdf

[2] Alexandra Carpentier; Andrea Locatelli. Tight (Lower) Bounds for the Fixed Budget Best Arm Identification Bandit Problem. 2016. COLT / PMLR 49:590–604.

https://proceedings.mlr.press/v49/carpentier16.pdf
