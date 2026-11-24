# Finite-arm lexicographic bandits without tradeoff side information

**Setting ID.** `ONX_LEX_FINITE_UNKNOWN`

Online learning and bandits

Two-objective simultaneous regret when primary ties must be distinguished from small primary improvements without a supplied tradeoff bound.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Lexicographic bandit regret; task family: Online bandit

**ORACLE tags.** feedback quality: Stochastic subgaussian; operation: Two coordinate reward vector; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; mode: Probability; quantifier: Algorithm before instance

**RESOURCE tags.** measure: N arm pull; measure: N reward coordinate

## 1. Setting specification

### Task

Minimize simultaneous coordinate regret for a two-objective lexicographic stochastic bandit without a supplied tradeoff envelope.

### Admissible model

The public action set is $[K]$, with the discrete metric $D(a,b)=\mathbf1\{a\ne b\}$ and $K\ge2$.

There are two fixed reward means $\mu^1,\mu^2$ taking values in $[0,1]$. The primary optimum set is $\mathcal X_1^*=\arg\max_x\mu^1(x)$, and a lexicographic optimum $x^*$ maximizes $\mu^2$ over that set. Primary ties are permitted.

The local tradeoff is $\lambda_* =\inf\{\lambda\ge0:\mu^2(x)-\mu^2(x^*)\le\lambda[\mu^1(x^*)-\mu^1(x)]\ \forall x\}$. No value or upper bound for $\lambda_*$ is supplied. The same policy must handle all admissible means without such side information.

### Oracle interface

At round $t$, choose an arm $X_t$ using the past and an independent random seed; then observe both coordinates $(Y_t^1,Y_t^2)$. Each coordinate is conditionally 1-sub-Gaussian around its fixed mean: $\mathbb E[\exp(\theta(Y_t^i-\mu^i(X_t)))\mid\mathcal H_{t-1},X_t]\le\exp(\theta^2/2)$. Independence between coordinates is not required. There is no feedback for unselected arms and no sample reuse interface.

The public inputs are $K,T$ and, for a probability guarantee, $\delta$. The means and primary-optimal set are hidden.

### Output

The output is the sequence of selected arms. One policy must control both objective regrets against the same lexicographic optimum.

### Loss or accuracy criterion

Define $\Delta_i(x)=\mu^i(x^*)-\mu^i(x)$ and signed coordinate regret $R_i(T)=\sum_{t=1}^T\Delta_i(X_t)$. The simultaneous expected criterion is $\max_{i\le2}\mathbb E R_i(T)$. The secondary regret can be negative, so the maximum is taken after each expectation.

For the high-probability view, use $R_i^+(T)=\sum_t[\Delta_i(X_t)]_+$ and the common threshold for $\max_iR_i^+(T)$. This is a distinct metric linked to its explicit view.

### Resource accounting

There is one arm pull and two scalar reward observations per round, so the fixed horizon is $T$, the pull count is $T$, and the number of observed reward coordinates is $2T$. Computation and storage are unrestricted.

### Algorithm views and success guarantees

#### Simultaneous expected coordinate regret

All measurable randomized nonanticipating policies are allowed. A policy may use K and T but no tradeoff envelope.

$$
\forall\nu:\quad\max_{i\le2}\mathbb E_\nu R_i(T)\le r
$$

One policy handles every instance and both coordinates; the expectation includes observation and policy randomness.

**Budget convention.** fixed_horizon

#### High-probability simultaneous positive regret

All randomized nonanticipating policies may use K,T,delta, but no tradeoff envelope.

$$
\forall\nu:\quad\Pr_\nu(\max_{i\le2}R_i^+(T)\le r)\ge1-\delta
$$

The same regret threshold must hold simultaneously for both objectives on every admissible instance.

Metric: The metric is $\max_{i\le2}R_i^+(T)$ with $R_i^+(T)=\sum_t[\Delta_i(X_t)]_+$.

**Budget convention.** fixed_horizon

## 2. Notation and parameters

$K$: Number of arms **Domain:** $K\in\mathbb N_{\ge2}$.

$T$: Horizon **Domain:** $T\in\mathbb N_{\ge2}$.

$\delta$: Failure probability for the probability view **Domain:** $0<\delta<1$.

$\lambda_*$: Instance local tradeoff; not given to the policy **Domain:** $0\le\lambda_*<\infty$ on finite arm sets.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

**View.** Simultaneous expected coordinate regret

$$
\mathfrak M_{T,K}=\inf_\pi\sup_{\nu\in\mathcal F_K}\max_{i\le2}\mathbb E_\nu R_i(T)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

#### Q2 - minimax metric resource quantity

**View.** High-probability simultaneous positive regret

$$
\mathfrak Q_{T,K}(\delta)=\inf_\pi\inf\{r:\sup_{\nu\in\mathcal F_K}\Pr_\nu(\max_iR_i^+(T)>r)\le\delta\}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

### R1 - Expected regret without tradeoff side information

**Region.** $K,T\ge2$ integers; no tradeoff envelope is supplied. Finite action count K; no ambient Euclidean dimension.

**Views.** Simultaneous expected coordinate regret

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega\!\left(\min\{T,(K-1)^{1/3}T^{2/3}\}\right)
$$

**Upper bound.** B1

$$
O\!\left(\min\{T,(K\log(4KT))^{1/3}T^{2/3}\}\right)
$$

**Gap or comparison.** At most an $O(\log^{1/3}(4KT))$ factor remains.

### R2 - General finite-arm confidence dependence

**Region.** $K\ge3$, $T\ge C$ for the source universal threshold, and $0<\delta\le1/16$. Finite arm count K.

**Views.** High-probability simultaneous positive regret

**Quantity.** Q2

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega\!\left(\min\{T,((K-1)\log(1/\delta))^{1/3}T^{2/3}\}\right)
$$

**Upper bound.** B3

$$
O\!\left(\min\{T,(K\log(4K/\delta))^{1/3}T^{2/3}\}\right)
$$

**Gap or comparison.** The general-K upper bound has an additional factor of at most order $[\log(4K/\delta)/\log(1/\delta)]^{1/3}$.

### R3 - Two-arm sharp confidence rate

**Region.** $K=2$, $T\ge C$ for the source universal threshold, and $0<\delta\le1/16$. Exactly two arms.

**Views.** High-probability simultaneous positive regret

**Quantity.** Q2

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega\!\left(\min\{T,T^{2/3}\log^{1/3}(1/\delta)\}\right)
$$

**Upper bound.** B5

$$
O\!\left(\min\{T,T^{2/3}\log^{1/3}(8/\delta)\}\right)
$$

**Gap or comparison.** The displayed logarithms differ by only constant factors throughout the stated delta range.

## 4. Bounds and supporting evidence

### B1 - LexETC: explore, filter by the primary objective, and commit by the secondary objective.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Simultaneous expected coordinate regret

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\min\{T,(K\log(4KT))^{1/3}T^{2/3}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K,T\ge2$ integers; no tradeoff envelope is supplied.

**Dimension conditions.** Finite action count K; no ambient Euclidean dimension.

**Constants.** Universal constants.

**Logarithmic factors.** Only the displayed logarithm; no power of K or T is suppressed.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:finite-upper; Corollary cor:finite-matching

LexETC: explore, filter by the primary objective, and commit by the secondary objective.. One envelope-free policy for every finite-arm instance.

### B2 - Anchor-plus-candidate primary ties with a hidden primary improvement.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Simultaneous expected coordinate regret

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(\min\{T,(K-1)^{1/3}T^{2/3}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K,T\ge2$ integers; no tradeoff envelope is supplied.

**Dimension conditions.** Finite action count K; no ambient Euclidean dimension.

**Constants.** Universal constants.

**Logarithmic factors.** Only the displayed logarithm; no power of K or T is suppressed.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:finite-lower; Corollary cor:finite-matching

Anchor-plus-candidate primary ties with a hidden primary improvement.. Every randomized causal policy lacking tradeoff side information.

### B3 - Finite-arm explore-filter-commit with a simultaneous confidence event.

**Admission.** Included in the bracket

**Direction.** upper

**View.** High-probability simultaneous positive regret

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\min\{T,(K\log(4K/\delta))^{1/3}T^{2/3}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K\ge3$, $T\ge C$ for the source universal threshold, and $0<\delta\le1/16$.

**Dimension conditions.** Finite arm count K.

**Constants.** Universal constants.

**Logarithmic factors.** Logarithms in K and 1/delta are retained explicitly.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Proposition prop:k-hp

Finite-arm explore-filter-commit with a simultaneous confidence event.. Randomized causal policies using delta but no tradeoff envelope.

### B4 - Stopped-history KL with primary ties and a hidden candidate.

**Admission.** Included in the bracket

**Direction.** lower

**View.** High-probability simultaneous positive regret

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(\min\{T,((K-1)\log(1/\delta))^{1/3}T^{2/3}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K\ge3$, $T\ge C$ for the source universal threshold, and $0<\delta\le1/16$.

**Dimension conditions.** Finite arm count K.

**Constants.** Universal constants.

**Logarithmic factors.** Logarithms in K and 1/delta are retained explicitly.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:hp-lower; Proposition prop:k-hp

Stopped-history KL with primary ties and a hidden candidate.. Every randomized causal policy under the positive-regret probability metric.

### B5 - Two-arm confidence-tuned filtering.

**Admission.** Included in the bracket

**Direction.** upper

**View.** High-probability simultaneous positive regret

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\min\{T,T^{2/3}\log^{1/3}(8/\delta)\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K=2$, $T\ge C$ for the source universal threshold, and $0<\delta\le1/16$.

**Dimension conditions.** Exactly two arms.

**Constants.** Universal constants.

**Logarithmic factors.** The confidence dependence is part of the rate and is not suppressed.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:two-hp

Two-arm confidence-tuned filtering.. Envelope-free causal policy.

### B6 - Stopped-history binary testing lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**View.** High-probability simultaneous positive regret

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(\min\{T,T^{2/3}\log^{1/3}(1/\delta)\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $K=2$, $T\ge C$ for the source universal threshold, and $0<\delta\le1/16$.

**Dimension conditions.** Exactly two arms.

**Constants.** Universal constants.

**Logarithmic factors.** The confidence dependence is part of the rate and is not suppressed.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:two-hp

Stopped-history binary testing lower bound.. Every randomized causal policy.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U07. Primary Ties and the Price of Unknown Trade-offs in Lexicographic Bandits. primary_ties_unknown_tradeoffs.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf
