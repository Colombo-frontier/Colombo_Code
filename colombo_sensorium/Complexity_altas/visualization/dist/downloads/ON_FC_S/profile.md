# Bernoulli best-arm identification: fixed confidence and expected stopping cost

**Setting ID.** `ON_FC_S`

Online learning and bandits

The algorithm adaptively samples Bernoulli arms, chooses a stopping time, and recommends the unique best arm. It must attain the prescribed confidence for every admissible mean vector. Cost is the expected number of samples on the instance; the central comparison concerns the leading constant as confidence tends to one for a fixed instance.

**Status.** Fully optimal

**TASK tags.** formulation: Best arm fixed confidence; solution concept: Minimize expected stopping time; task family: Online bandit

**MODEL tags.** stochastic model: Parametric bernoulli; structure: Finite actions; structure: Unique best

**ORACLE tags.** feedback quality: Source-declared exact feedback (may be a random reward); interface family: Selected reward; operation: Sample selected arm; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Stopping time and arm recommendation

**METRIC tags.** criterion: Uniform fixed-confidence identification correctness

**GUARANTEE tags.** confidence: Confidence parameter explicitly declared; mode: Uniform fixed-confidence identification correctness; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Instancewise expected stopping cost (not a worst-instance supremum); measure: Samples; measure: Stopping checks

## 1. Setting specification

### Task

The algorithm adaptively samples Bernoulli arms, chooses a stopping time, and recommends the unique best arm. It must attain the prescribed confidence for every admissible mean vector. Cost is the expected number of samples on the instance; the central comparison concerns the leading constant as confidence tends to one for a fixed instance.

### Admissible model

The fixed unknown mean vector satisfies $\mu\in(0,1)^K$ and has a unique best arm. Both means and individual arm gaps are hidden.

The data-dependent stopping time $\tau_\delta$ is measurable with respect to observed history and is not a fixed horizon.

The arm $\widehat{b}$ is recommended at stopping. Correctness must hold uniformly over all admissible mean vectors.

The comparison characteristic time $T^*(\mu)$ is defined by the allocation problem using forward $\operatorname{KL}(\nu_{\mu_i}\,\|\,\nu_{\lambda_i})$. It is an analytical benchmark, not an input supplied to the algorithm.

The full characteristic time $T^*(\mu)$ is defined by $T^*(\mu)^{-1}=\sup_{w\in\Delta_K}\inf_{\lambda\in\operatorname{Alt}(\mu)}\sum_i w_i\operatorname{kl}(\mu_i,\lambda_i)$. The alternative class, Bernoulli KL divergence, and simplex are defined in the local notation table.

Require $K\ge2$ and $0<\delta<1/2$. Both round actions and the final recommendation lie in $[K]$.

Take delta to zero with the instance mu fixed. Finite-parameter conclusions in which K or mu also vary are not part of this leading-constant comparison.

### Oracle interface

Bernoulli arm sampling:

$$
a_t\in[K],\quad t\le\tau_\delta\ \longmapsto\ Y_t\in\{0,1\},\quad \mathbb{P}(Y_t=1\mid\mathcal{H}_{t-1},a_t)=\mu_{a_t}
$$

Each call returns a fresh independent Bernoulli sample.

Arm choices depend only on the history; stopping and recommendation use information already obtained.

No extra samples are taken after stopping. This task has no regret-bearing action point.

Public inputs are K, δ, and the Bernoulli family. The means μ and gaps are hidden.

### Output

Output an almost surely finite stopping time $\tau_\delta$ and recommended arm $\widehat{b}\in[K]$. A computable correctness certificate is not required. No samples may be drawn after stopping.

### Loss or accuracy criterion

$$
p_\mu(\mathcal{A}_\delta)=\Pr_\mu(\widehat{b}\ne b(\mu)),\qquad C_\mu(\mathcal{A}_\delta)=\mathbb{E}_\mu[\tau_\delta].
$$

The identification loss is an error indicator, and expected stopping time is the cost. The asymptotic efficiency quantity $\mathbb{E}_\mu[\tau_\delta]/\log(1/\delta)$ is kept distinct from fixed-budget error probability.

### Resource accounting

Each arm pull yields one charged sample. The total number of samples is the random stopping time $\tau_\delta$, and the primary resource objective is the instancewise expectation $\mathbb{E}_\mu[\tau_\delta]$.

Any causal randomized algorithm that is uniformly delta-correct is allowed.

Track-and-Stop maintains empirical means, sample counts, and likelihood ratios and numerically computes allocation proportions. Those computations are not identified with one sample at no additional accounting cost.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

Arbitrary causal randomized sampling, stopping, and recommendation rules are allowed. The algorithm must achieve the confidence guarantee uniformly over all admissible mean vectors and stop almost surely. Internal computation and storage are unrestricted.

One algorithm family $\{\mathcal{A}_\delta\}$ must satisfy $\Pr_\mu(\widehat{b}=b(\mu))\ge1-\delta$ for every admissible mean vector $\mu$ and stop almost surely. Expected-cost guarantees are instancewise. In the limit $\delta\downarrow0$, hold $K$ and the entire $\mu$ fixed. Randomness includes sampling and the algorithm.

**Budget convention.** The sample count $\tau_\delta$ is random, with primary cost $\mathbb E_\mu\tau_\delta$. There is no prespecified hard budget $T$.

## 2. Notation and parameters

$K$: The finite number of arms. **Domain:** $K\in\mathbb N,\ K\ge2$.

The arm set is $[K]=\{1,\ldots,K\}$.

$\delta$: The allowed statistical failure probability. **Domain:** $0<\delta<1/2$.

Used only for statistical correctness or high-probability performance, and distinct from the privacy relaxation parameter.

$\mu$: Unknown Bernoulli mean vector **Domain:** The vector $\mu\in(0,1)^K$ has a unique largest component.

$\mu_i=\mathbb E_{Y\sim\nu_i}Y$, where $\nu_i=\operatorname{Bernoulli}(\mu_i)$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$\mathcal M_K$: Class of Bernoulli mean vectors with a unique best arm **Domain:** $\mathcal M_K\subset(0,1)^K$.

The instance class is $\mathcal M_K=\{\mu\in(0,1)^K:\arg\max_i\mu_i\text{ contains exactly one arm}\}$.

$b(\mu)$: Unique best arm of mean vector mu **Domain:** $b(\mu)\in[K]$.

$b(\mu)=\arg\max_i\mu_i$.

$\tau_\delta$: A stopping time determined by observed data. **Domain:** A nonnegative integer-valued stopping time.

The quantity $\mu\in\mathcal M_K$ is almost surely finite on every admissible instance. Its expectation is the charged sampling cost.

$\widehat b_{\tau_\delta}$: Arm recommended upon stopping **Domain:** $\widehat b_{\tau_\delta}\in[K]$.

The guarantee $\Pr_\mu(\widehat b_{\tau_\delta}\ne b(\mu))\le\delta$ holds for every admissible mu.

$\operatorname{Alt}(\mu)$: Alternative mean vectors with a different best arm. **Domain:** The set of mean vectors.

The expression is $\{\lambda\in\mathcal M_K:b(\lambda)\ne b(\mu)\}$; taking the closure in the inner infimum gives an equivalent value.

$\operatorname{kl}(p,q)$: Forward relative entropy of Bernoulli distributions. **Domain:** $p,q\in(0,1)$.

The expression is $p\log(p/q)+(1-p)\log((1-p)/(1-q))$, with endpoints defined by continuous limits.

$\Delta_K,w$: The sampling-proportion simplex and its elements. **Domain:** $w\in\Delta_K$.

$\Delta_K=\{w\in[0,1]^K:\sum_iw_i=1\}$.

$\lambda$: Alternative means in the inner characteristic-time optimization. **Domain:** $\lambda\in\operatorname{Alt}(\mu)$.

$T^*(\mu)$: Instance characteristic time for fixed-confidence identification **Domain:** Positive real number used only in analysis of the hidden instance.

$$
T^*(\mu)^{-1}=\sup_{w\in\Delta_K}\inf_{\lambda\in\operatorname{Alt}(\mu)}\sum_iw_i\operatorname{kl}(\mu_i,\lambda_i)
$$.

$\mathcal T_\delta(\mu)$: Minimum expected sample count among all uniformly delta-correct algorithms that stop almost surely **Domain:** A nonnegative real.

$\mathcal T_\delta(\mu)=\inf_{\mathcal A\ \delta\text{correct}}\mathbb E_\mu\tau_\delta$. The algorithm must first be uniformly correct; its performance is then evaluated at the fixed instance μ.

$\beta(t,\delta)$: Public threshold in the Chernoff stopping rule **Domain:** Real number.

$\beta(t,\delta)=\log(2(K-1)t/\delta)$.

$\widehat\mu,w^*(\widehat\mu)$: Empirical arm means and their characteristic-time-optimal allocation. **Domain:** Algorithm's internal statistic.

The vector $w^*$ is an optimal sampling proportion in the outer maximization defining characteristic time. It cannot be computed using the hidden true mu as an input.

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\mathbb N,\ t\ge1$.

Sampling time. The data-dependent stopping time $\tau_\delta$ has no prespecified horizon $T$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes learner randomness and the explicitly specified reward or sample randomness. Conditional expectations retain their stated history conditioning.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=\tau_\delta$ is the cumulative number of scalar reward samples before stopping.

## 3. Complexity bracket

### Compared quantities

#### Q1 - asymptotic expected sample constant

$$
\begin{aligned} C_{\rm FC}(\mu)&=\lim_{\delta\downarrow0}\inf_{\mathcal A\in\mathfrak A_\delta}\frac{\mathbb E_{\mu,\mathcal A}[\tau_\delta]}{\log(1/\delta)},\qquad \mu,K\ \text{fixed},\\ \mathfrak A_\delta&=\{\mathcal A:\ \forall\lambda\in\mathcal M_K,\ \mathbb P_{\lambda,\mathcal A}(\tau_\delta<\infty)=1,\\ &\hspace{5em}\mathbb P_{\lambda,\mathcal A}(\widehat b_{\tau_\delta}\ne b(\lambda))\le\delta\},\\ \mathcal M_K&=\{\mu\in(0,1)^K:\ b(\mu)\text{ is unique}\}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - ASYMPTOTIC

**Region.** Fix a mean vector mu with a unique best arm and arm count K, then take delta to zero.

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
T*(\mu )
$$

**Upper bound.** B1

$$
T*(\mu )
$$

**Gap or comparison.** The same leading asymptotic constant when $\mu$ and $K$ are fixed.

**Comparison argument.** Only individually audited compatible claims enter. No inversion into fixed-budget exponent; its KL orientation and quantifiers differ.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Fix the arm count $K$ and mean vector $\mu$ with a unique best arm, and consider $\delta\to0$. The confidence requirement holds on every admissible instance, not merely one known instance.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Track-and-Stop with C-/D-tracking and Bernoulli Chernoff threshold

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\limsup_{\delta\downarrow0}\frac{\mathbb{E}_\mu[\tau_\delta]}{\log(1/\delta)}\le T^*(\mu)
$$

**Sources.** [1](https://proceedings.mlr.press/v49/garivier16a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**samples.**

$$
E_mu \tau
$$

**stopping checks.**

$$
\le \tau
$$

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://proceedings.mlr.press/v49/garivier16a.pdf) pdf pages: 10; 13; theorem: Theorems 10 and 14

For Bernoulli rewards, use Chernoff stopping threshold $\log(2(K-1)t/\delta)$ with C- or D-tracking. The source choice $\alpha=1$ yields asymptotic expected-sample constant $T^\star(\mu)$.

### B2 - Change of measure across Alt(μ)

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\begin{aligned}[c]\mathbb{E}_\mu[\tau_\delta]&\ge T^*(\mu)\operatorname{kl}(\delta,1-\delta),\\ \liminf_{\delta\downarrow0}\frac{\mathbb{E}_\mu[\tau_\delta]}{\log(1/\delta)}&\ge T^*(\mu),\\ T^*(\mu)^{-1}&=\sup_{w\in\Delta_K}\inf_{\lambda\in\operatorname{Alt}(\mu)}\sum_{i=1}^K w_i\operatorname{kl}(\mu_i,\lambda_i).\end{aligned}
$$

**Sources.** [1](https://proceedings.mlr.press/v49/garivier16a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**samples.**

$$
E_mu \tau
$$

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Fix the number of arms and a mean vector with a unique best arm, and let $\delta\to0$. The binary relative entropy satisfies $\operatorname{kl}(\delta,1-\delta)/\log(1/\delta)\to1$, giving the asymptotic sample constant. No uniform statement is made when arm gaps shrink simultaneously.

**Source location.** [1](https://proceedings.mlr.press/v49/garivier16a.pdf) pdf pages: 3; 4; theorem: Theorem 1

Every policy that is $\delta$-PAC on the entire admissible instance class satisfies $\mathbb E_\mu\tau\ge T^\star(\mu)\operatorname{kl}(\delta,1-\delta)$. The characteristic time uses the forward divergence $\operatorname{KL}(\mu_i,\lambda_i)$.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 0ced878efd60acd4d210dae9ea3a11a334e7803e272afd7b3e6c384dbedf5250

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 39c1c3af88e8e395d942d8492e97be5422aedebd0cfa90a76b479f1bdbe52362

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 281764c14e2ff9febc07d69b867bda757144880fcb185f7a15cd570d3b06073e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: b9060dc2b21a4de32cbda4fc76a39dfe437acd8609f7bc4741f8d1b651e9e8ee

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 4a43477754b9f78bd4e3e0510c5459422822980c2b30c33e83f409f854dd2b74

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: afebc9ca67d4df5153efffb1f5a968ab3c6d5922d9e22b9109ad91713df922ac

ON_FC_S__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: f4114c9c6fb61d6fa57c225d00634405570c866498bcbf220a14bdcd66268a21

Retain the Bernoulli Track-and-Stop expected-cost limsup bound with the threshold log(2(K-1)t/delta). It is an admissible uniformly delta-correct algorithm, not an algorithm given the hidden instance. No finite-parameter uniformity follows.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: ad29789bb77c4c30687263a40703bbb0564cf801f205b7c6e509c21ef0034601

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 3bcea0ae6698f89ee64beb75653c0a9a0422536f433bfe8d9c81c7c1985b9bae

ON_FC_S__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: dd68f216b5f297853c35c43390debfa22206cec02eda2ad78e1ffd270e0456b8

Retain the change-of-measure lower bound for all admissible causal randomized procedures. Taking kl(delta,1-delta)/log(1/delta) to 1 gives the lower constant. Both mechanical candidates are accounted for; the catalogue contains no unused compatible native bounds.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 9fd58573df1e93893112f95722cc6e7ca7271d59e92a8b4d0d5a61dc21c03556

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2. Its recorded finite-delta inequality holds on the native interval 0<delta<1/2.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: f27dfe923843285a96d9c77e0297de96b46fc9a146b812160b2805e1985a7ec5

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: be8a537e07af7146cf835b1f8b6643d2ff650c9a4d53b55448c79db5cc341e6b

K=2 is included: the source explicitly gives its two-arm specialization; no large-K activation guard is needed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 4c634c8ae94e7870de58a87a8a14b79cf0edb53090704784a08db1760eb34a1a

The means remain strictly between 0 and 1 and the best arm is unique. Ties and Bernoulli endpoints are outside the immutable domain.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: b4becb3dfc64ec8aad14253abc8b17d3bc8c3f228c9a52025265451665dd0132

delta=0 is only a limiting direction; delta=1/2 is excluded. Neither endpoint is inserted as an admissible finite-confidence branch.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 5f5cca24c97e93228c93c9c5089188a6bc41ce6cc5acfbc2e706cdbc402cc9ae

For every fixed admissible instance the characteristic time is positive and finite, as in the source's allocation characterization. Thus the retained lower bound diverges with log(1/delta); a zero-query or bounded-query saturation branch cannot replace this limit.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 10f9e0df4970bc0f1be70b7252a5fe4349dd7a9dd2a7ae7357dc1e06966b8440

Optimality and correctness have different quantifiers: correctness holds for every instance, while convergence of normalized expected cost is pointwise in the fixed instance.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 5178c4cb60520eaf8d6a3d1339394f26800d2a39ad618674697a9d2e4022ca9b

The quantity lists mu among tracked parameters and also fixes it in the limit. Its explicit expression and fixed_parameters resolve the roles: mu is the argument of the limiting function, not an additional asymptotic variable. No metadata normalization is proposed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 736998c0b26e22ec52bb8b13d9374a2856bfdb2cdf3e8de1e22720c00aa4f6d9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 8f9202e72d60e2684c29ef437ba11efc1fb50e7c0ee4824c7f5c69d2c96b2f92

ON_FC_S_p_585fcb7010

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: 19e02389706214ed7d32db77f93d2a69760e81c866381eb3a95049b4503ecd37

ON_FC_S_p_3c4ea41351

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 736998c0b26e22ec52bb8b13d9374a2856bfdb2cdf3e8de1e22720c00aa4f6d9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 8f9202e72d60e2684c29ef437ba11efc1fb50e7c0ee4824c7f5c69d2c96b2f92

ON_FC_S_p_585fcb7010

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: 19e02389706214ed7d32db77f93d2a69760e81c866381eb3a95049b4503ecd37

ON_FC_S_p_3c4ea41351

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 0c820ed3694cca73acb7af4298753ec761fc6c6ab377c1ff9f859148b3f84bdd

Upper/lower leading-constant ratio 1: C_FC(mu)=T*(mu). This ratio is for samples per nat of confidence, not a ratio of finite-delta stopping costs.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 432c1d08c780d1d468689453f5f3ee99143ffe63bfff66fa99eefb91b4de245d

C_FC(mu) >= T*(mu), for each fixed admissible K,mu; the stronger recorded finite-confidence statement is E_mu[tau_delta] >= T*(mu) kl(delta,1-delta), without a matching finite-confidence upper envelope asserted here.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 9aaed67f4b23b7069102a3adf3a6adcaa09dd45b7ef9bf6a1481854428146bf8

No leading-constant gap in the registered pointwise limit, conditional on retained premises. Uniform finite-confidence bounds, coupled parameter limits, and sharper lower-order terms are unassessed and are not certified open problems.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: a8297ed4f9245380271525b63bf188bf14ec37c429849e65e19cf00cc8f1ee6e

C_FC(mu) <= T*(mu), for each fixed admissible K,mu; achieved by the retained Bernoulli Track-and-Stop family.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: edbaf8af4fe88c37243d6ddb5fa6fc0f3e666f0f65f1f2f4d4248d52598e62dd

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 15e911751f2c99b127c78164e3a324236f9e2cc1b60c6c5f60538b02471f61ed

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 85e139edc9b8d1605ce8af2fa120b45ed5043155f1ee4b1d93b7f1ffc43b1216

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 3066de202469eedd07eb2b0d1279fe976c1a35de97a3a4526ae8d64a462d67a9

ON_FC_S_pointwise_confidence_limit

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: ee23cca2b12b81324a2a7099cb84f7cbd83b7d449d7ac6e27962238860c32a89

This single cell covers every admissible fixed instance for the native limiting quantity. It does not assert simultaneous asymptotics in K, mu and delta. Existing optimal comparison states are conditionally retained; this metadata migration issues no new native-proof closure certificate for historical source-only records.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 8ad3a3726dca812d8c457712285cccfb4279b9a2b652579d6aff734022a9b337

For every admissible K and mu the contract specifies exactly the same one-variable confidence limit and the one registered regime. Its applicability predicate is the cell predicate. No relation between varying native parameters is imposed, so this is the primary domain rather than a secondary slice. Excluded boundary instances are not extra cells.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: b231fd9c434135e56781ff4550ff933e486f8ace3cb5daadf59bb406dd56d0dc

Empty within the defined limiting quantity and registered comparison. Finite-confidence cost envelopes and paths with varying K or shrinking gaps are not assessed here; the immutable contract excludes them from this leading-constant comparison.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: a3cdc1f25cc875add5fb2c95968d47add825a323f73eadd3aaa02597b2886935

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: a325a422dcd7960f77940525945cb0ca49df4ee879c49599b7121c1f4dab72ae

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 1bee3cab03613fd1da00a840832b762953893dba3131f395187f4ce007a5a5bf

Presentation restructuring of completely read frozen records; it adds no bound, widens no applicability region and changes no inequality or status.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 125538e8af63071c18c6b4a1a6ea500ffe83f57f49ac48a54145df0708522f4d

ON_FC_S_first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: e864b25287332828f784ee72ee63f54344af0dae6de9bd27b0c8879589b9f24b

None in sample cost; the change is the first explicit synthesis annotation.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: ae3034cd961be9daf418857868d9542f50a2358795923332ccd67beca7a86994

The same two guarded constants T*(mu), now with explicit parameter roles, domain accounting and candidate dispositions.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 5fa1f392ada9e87fbd3648811e9156442da67bb2b653e780f30998c6157a2aa5

Registered pointwise lower and upper constants both T*(mu). No root joint analysis existed.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 33fcaf421d40db4a5d1032c7e1a2d11b817d3381d21bf2b3132d3ce7fbb4c7f3

The entire registered pointwise asymptotic domain.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 9d5219baaca1162acefe0d553a9713a58748131de3818fbcdf14b1810eab20a5

Both native claim IDs, guards, active bracket references and the optimal status are preserved.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 00b648dc2c24e17fbe078530776057207792ec6c1478a722f1fbc264fa7eba2d

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 2cd92e19ed61948c7889fe7a532e707d8448b1de56790b669ab6578379b3b4ea

The decisive published theorem text matches the retained expected-sample statements and quantifiers. No main-rate correction, stronger compatible leading constant or extra endpoint branch was established.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: fb3d98bdd00db02e58c891c8cb570bc0799008d63cde17a3321616178d4218be

ON_FC_S_pmlr_theorem_check

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 286db01a4470d0ad21351e54154146775671c9b1187945797fdfbac94dfa3b23

T*(mu) <= C_FC(mu) <= T*(mu).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 286db01a4470d0ad21351e54154146775671c9b1187945797fdfbac94dfa3b23

T*(mu) <= C_FC(mu) <= T*(mu).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 33fcaf421d40db4a5d1032c7e1a2d11b817d3381d21bf2b3132d3ce7fbb4c7f3

The entire registered pointwise asymptotic domain.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: e179a2c6286cb3d089d540792450a67d6f42e76b87462ca85639d389f811a20c

Theorems 1, 10 and 14; alpha=1 is explicitly permitted for the Bernoulli threshold.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 5ce918c355cf2132d00353aab0362f20ff5db972e7ae6905b42ad3c10f35fe3d

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: b2e928d8486efc3abd3ef6c26e66b0cae7593e747ce70c2aeafdd905fced9687

With M=1, the alternative class and max-min allocation become the retained unique-optimum formula, as Remark 6 also states. This paper uses base-2 logs: d_bits=d_nats/ln(2) and T_bits=ln(2) T_nats, so T_bits*kl_bits=T_nats*kl_nats. It yields no stronger lower envelope. No claim from the tied-arm model is transferred.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 88031f0be92b0ce65ade50ed20f3809e0396152802107e48e379f83445576419

ON_FC_S_multi_optima_v2_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: be81cc82434e277f87da77bf71c8ccb1e008681cfcb8e3dee9521b1465378337

Lower leading constant T*(mu).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: be81cc82434e277f87da77bf71c8ccb1e008681cfcb8e3dee9521b1465378337

Lower leading constant T*(mu).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 33fcaf421d40db4a5d1032c7e1a2d11b817d3381d21bf2b3132d3ce7fbb4c7f3

The entire registered pointwise asymptotic domain.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: dff3de0fcfa48e7b173a9edbfb442d55172b819c0d149d4cfca328f5acea954c

The paper's M=1 specialization intersects the native unique-best-arm model. Its M>1 claims are outside the fixed contract.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 669c39074002b268d1c65d7c56db5bc684b86a079a1d5c87d9ecc5b46bca7cde

arXiv:2505.15643v2, Sections III-IV, Theorem 5 equations (14)-(20), Remark 6; source 3f1586c5da0bd27b1e0b5a3e184b799e4d6856ac5dbac5c328996a397ead3b9c, chars 10000:20000.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 98e086f44c14f6ea3a1c759bbbf402c9e72167a39444e3f347eb8950443187e5

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 9080af474c4c7e207e57197578a6f85fa801d1616e6cd01bfdd8b63c429d3087

curated_feedback_ON_FC_S_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: fe4fd20b84e18bf53db16741dbb48145a3f30835519641974818806d338a9a3b

The native quantity ON_FC_S__main__q1 is the pointwise limit of infimum expected samples over all causal algorithms that are delta-correct and stop almost surely on every admissible instance, divided by natural log(1/delta). For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2. There is no worst-case-over-mu operation. K and mu index pointwise problems; they are not joint asymptotic variables. Dependence of non-leading convergence thresholds on these fixed parameters is permitted; the retained leading coefficient is exactly T*(mu), with no hidden multiplier. No uniform convergence in K or mu is asserted.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 31f7d58b764c74bfcd2d5591271e412932900d0810e0563598137680da06d2b5

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 1d01f3d3da2745492f174cc9b3a94929bdc7190a336b89027272f447b0914abf

curated_feedback_ON_FC_S_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: fe4fd20b84e18bf53db16741dbb48145a3f30835519641974818806d338a9a3b

The native quantity ON_FC_S__main__q1 is the pointwise limit of infimum expected samples over all causal algorithms that are delta-correct and stop almost surely on every admissible instance, divided by natural log(1/delta). For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2. There is no worst-case-over-mu operation. K and mu index pointwise problems; they are not joint asymptotic variables. Dependence of non-leading convergence thresholds on these fixed parameters is permitted; the retained leading coefficient is exactly T*(mu), with no hidden multiplier. No uniform convergence in K or mu is asserted.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 7e4d1f254e33e95b0ae9090c93264cb8ad5729eebebebc3e940dd60368b28b0e

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 391752a321a7ec804e6a9fb7e019cdd3ec21c7d245e4eef248ef5d21f2ba05db

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 5d5f7b2e01e45d27a5e2e0d35b5ddabc610487b5eb6af38371cd1185edd41b1a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: afebc9ca67d4df5153efffb1f5a968ab3c6d5922d9e22b9109ad91713df922ac

ON_FC_S__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: cd0e208b6352ce9fd8f51d52f3e2e37c4c8be94f56a031984d9e2eb68220c276

Conditional retention of the unchanged native claim. One fresh selected-arm Bernoulli observation costs one sample; empirical means and allocation computations use no extra oracle. Theorem 10 supplies uniform error control, Proposition 13 almost-sure stopping, and Theorem 14 the expected-cost coefficient. Internal arithmetic is not identified with sample complexity.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: f2753be0bb869cce0969618448acd19bc75671a23464be51795564b8fdfac349

Bernoulli bandits with a unique best arm; Chernoff stopping plus C- or D-tracking, alpha=1 and r(t)=2(K-1)t.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 93d690b09f3f31470cb64865cb55608338d8608a82bec44a2a7d0951c7a0f78c

Frozen /bounds/0 and ON_FC_S__main__e2; Garivier--Kaufmann, COLT/PMLR 49 (2016), Theorems 10 and 14, Proposition 13. Independently reread archived source 6ad45d19aa4867fe21f5dcb223ad647bbed3748491afe3197c5ddd9ef21f5bdd, chars 22400:30900, PDF pp.9-13.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 9aa7f0254c0425363a9b0d4f03527910cef66849e3edabb8fb970d4b33aa1516

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 7854d10becf5322c035de14248e52572469e908b27326e1f07659efd4e1ae50b

ON_SRC_FC

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 71306bc229693e33bcf6a394d3e88691c923ddfa8933f671866ed87c9173957c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 3bcea0ae6698f89ee64beb75653c0a9a0422536f433bfe8d9c81c7c1985b9bae

ON_FC_S__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 75d29872d14e8b1868f56fc96b06b2ab2d798c446c0c7660f133d150042562a0

Conditional retention of the unchanged native claim. The source's universal correctness and almost-sure stopping match main/g1; expected counts sum to the stopping cost. Forward Bernoulli KL and the full alternative class are preserved. No fixed-budget error exponent is inferred.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: da771b87b26aa6daeeb4f2de5ee1617c1ee6dc45c50cb03a0a672774c0d69f9f

All delta-PAC strategies on the unique-best-arm exponential-family class, specialized to Bernoulli distributions and native delta<1/2.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: c5dd674a348df0d6de5f8719da7da7e4a0b615784689d34ab2b8c10b020e5b0e

Frozen /bounds/1 and ON_FC_S__main__e1; Garivier--Kaufmann, COLT/PMLR 49 (2016), Theorem 1 and Remark 2. Independently reread source 6ad45d19aa4867fe21f5dcb223ad647bbed3748491afe3197c5ddd9ef21f5bdd, chars 7800:13200, PDF pp.3-5; allocation and two-arm discussion chars 13200:17300, pp.5-7.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 9aa7f0254c0425363a9b0d4f03527910cef66849e3edabb8fb970d4b33aa1516

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 7854d10becf5322c035de14248e52572469e908b27326e1f07659efd4e1ae50b

ON_SRC_FC

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 4843e7aa04287c6760c9654d26f01b7046b115ed8600a58ac02428eae0d5e8e3

For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 9f18bdca893057951acbc6045903b3a9d829f028bc5be2fb32141f1b15c53f6a

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 353a4be156187b9c69d547d7bd30e96df68f731889bbc7b1c5e0269ae89b2a28

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 702e9a72444300376281195b7934833043e70f19b293fe5c0bca6e0990e4e79f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 7ea78a41f6f353cf044cae5099302c3f1e635f8d791924c4e8efa2ba38f5fc80

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: afebc9ca67d4df5153efffb1f5a968ab3c6d5922d9e22b9109ad91713df922ac

ON_FC_S__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 3bcea0ae6698f89ee64beb75653c0a9a0422536f433bfe8d9c81c7c1985b9bae

ON_FC_S__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 9659e813601c72bdf41946230a491a4c71839d8529fbb28ac953f06db82b8c0d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 1b79c2f8e558a05a62b8f00617badff4fe3bea7c5ed5bee10fa90f38715d4b36

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 3f7c7cdad55a60d9fe94c9e9aa4a2391a0a9a330afda0ac08654eb19f9b24f35

ON_FC_S__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 00fba149fc3ed337cd1b5f3d97801271f33fec78a9165a003df64def33857be0

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 736998c0b26e22ec52bb8b13d9374a2856bfdb2cdf3e8de1e22720c00aa4f6d9

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 8f9202e72d60e2684c29ef437ba11efc1fb50e7c0ee4824c7f5c69d2c96b2f92

ON_FC_S_p_585fcb7010

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 19e02389706214ed7d32db77f93d2a69760e81c866381eb3a95049b4503ecd37

ON_FC_S_p_3c4ea41351

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: f039c018213abff211d96900d7187110d3b83d1d6615e54cea16f0860d0e8a3d

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: a81f0883e496ac5b7392c427a3d8c14df3a7692724c4cd7ac93e6370cd363ebf

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 051a679315401c14f2436de1eb9a7fdf899cac11e88cf87b5f1e63409cb1e8c8

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: a7119a9501a8bf5005d2c1de0c27a99cd0726892416df266bded3ba8bae46d32

Each fixed integer K>=2.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 8f9202e72d60e2684c29ef437ba11efc1fb50e7c0ee4824c7f5c69d2c96b2f92

ON_FC_S_p_585fcb7010

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 8f9202e72d60e2684c29ef437ba11efc1fb50e7c0ee4824c7f5c69d2c96b2f92

ON_FC_S_p_585fcb7010

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: 5af3d8a154093f18cf5dbd053b265721babfb7d321eb717ace4b7d6449787556

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 0d24ce2132333e5d620d76fe06cb2d8dbadc7a71ba8a887e8d22caa038d63164

Each fixed mu in (0,1)^K with a unique largest coordinate.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 19e02389706214ed7d32db77f93d2a69760e81c866381eb3a95049b4503ecd37

ON_FC_S_p_3c4ea41351

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: 19e02389706214ed7d32db77f93d2a69760e81c866381eb3a95049b4503ecd37

ON_FC_S_p_3c4ea41351

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: fe4fd20b84e18bf53db16741dbb48145a3f30835519641974818806d338a9a3b

The native quantity ON_FC_S__main__q1 is the pointwise limit of infimum expected samples over all causal algorithms that are delta-correct and stop almost surely on every admissible instance, divided by natural log(1/delta). For each fixed finite K>=2 and fixed mu in (0,1)^K with a unique largest coordinate, take delta down to 0 through 0<delta<1/2. There is no worst-case-over-mu operation. K and mu index pointwise problems; they are not joint asymptotic variables. Dependence of non-leading convergence thresholds on these fixed parameters is permitted; the retained leading coefficient is exactly T*(mu), with no hidden multiplier. No uniform convergence in K or mu is asserted.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 8d80514474847d61c209aae25ee9126b75133e90fb3a14f8b43f2a96767e4f7f

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 412d9bf5c9168c7387cf0ec32de334a352ae23a20a7ea9077b957ac96fcadbd8

ON_FC_S_p_e0e6d54b5e

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 8d80514474847d61c209aae25ee9126b75133e90fb3a14f8b43f2a96767e4f7f

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 412d9bf5c9168c7387cf0ec32de334a352ae23a20a7ea9077b957ac96fcadbd8

ON_FC_S_p_e0e6d54b5e

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Aurélien Garivier; Emilie Kaufmann. Optimal Best Arm Identification with Fixed Confidence. 2016. COLT / PMLR 49:998–1027.

https://proceedings.mlr.press/v49/garivier16a.pdf
