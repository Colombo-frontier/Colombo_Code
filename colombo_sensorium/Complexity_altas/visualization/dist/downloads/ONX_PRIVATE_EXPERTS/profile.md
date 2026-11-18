# Online experts: pure differential privacy for the entire action sequence

**Setting ID.** `ONX_PRIVATE_EXPERTS`

Online learning and bandits

After incurring the selected expert's loss, the learner observes the full loss vector; the entire loss stream is fixed in advance. Privacy protects one round's complete loss vector, and the released object is the full action sequence. All causal randomized strategies satisfying the specified privacy condition are allowed.

**Status.** Bounds missing

**TASK tags.** formulation: Onx privexp oblivious approx; formulation: Onx privexp oblivious pure; task family: Online bandit

**MODEL tags.** structure: Finite actions

**ORACLE tags.** interface family: Full loss vector; operation: Full loss vector; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

After incurring the selected expert's loss, the learner observes the full loss vector; the entire loss stream is fixed in advance. Privacy protects one round's complete loss vector, and the released object is the full action sequence. All causal randomized strategies satisfying the specified privacy condition are allowed.

### Admissible model

There are $K\ge2$ experts. The entire sequence of loss vectors $\ell_t\in[0,1]^K$, $t=1,\ldots,T$, is fixed before interaction. The hindsight loss $L_\star=\min_{i\in[K]}\sum_{t=1}^T\ell_t(i)$ is unknown.

### Oracle interface

At round t, choose an expert $I_t\in[K]$ before observing the complete current loss vector $\ell_t$. Feedback is exact. Observed loss vectors may be stored and reused; future loss vectors are unavailable.

The horizon T and number of experts K are public. Privacy parameters are supplied according to the selected algorithm view.

### Output

The released record is the entire action sequence $I_{1:T}$. Neighboring input streams differ in one complete loss vector. Past actions cannot be changed by terminal postprocessing.

### Loss or accuracy criterion

Performance is expected cumulative external regret, with $R_T=\sum_{t=1}^{T}\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^{T}\ell_t(i)$. The worst case ranges over fixed loss streams; expectation is over algorithmic randomness.

### Resource accounting

There are $N=T$ complete-vector feedback events, reading $KT$ loss coordinates in total. The privacy budget applies to the entire release sequence, rather than allocating an identical full budget to each round.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

#### Pure differential privacy

Adjacent input streams differ in the entire loss vector of one round. The released object is the full action sequence $I_{1:T}$. For any adjacent fixed streams $\mathsf D,\mathsf D^{\prime}$ and measurable event $E$, require:

$$
\Pr(\mathcal{A}(\mathsf D)\in E)\le e^{\epsilon_{\mathrm{priv}}}\Pr(\mathcal{A}(\mathsf D^{\prime})\in E).
$$

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

$$
\inf_{\mathcal{A}\ \text{\text{private}}}\ \sup_{\ell_{1:T}\in([0,1]^K)^T}\ \mathbb{E}_{\mathcal{A}}\!\left[\sum_{t=1}^{T}\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^{T}\ell_t(i)\right].
$$

The target is expected external regret, worst-case over fixed loss streams; expectation includes only algorithmic randomness.

**View qualification.** The public privacy budget is $\epsilon_{\rm priv}$. For every neighboring pair of fixed streams $\mathsf D,\mathsf D^{\prime}$ and measurable E, $\Pr(\mathcal A(\mathsf D)\in E)\le e^{\epsilon_{\rm priv}}\Pr(\mathcal A(\mathsf D^{\prime})\in E)$.

#### Approximate differential privacy

Adjacent input streams differ in the entire loss vector of one round. The released object is the full action sequence $I_{1:T}$. For any adjacent fixed streams $\mathsf D,\mathsf D^{\prime}$ and measurable event $E$, require:

$$
\Pr(\mathcal{A}(\mathsf D)\in E)\le e^{\epsilon_{\mathrm{priv}}}\Pr(\mathcal{A}(\mathsf D^{\prime})\in E)+\delta_{\mathrm{priv}}.
$$

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

$$
\inf_{\mathcal{A}\ \text{\text{private}}}\ \sup_{\ell_{1:T}\in([0,1]^K)^T}\ \mathbb{E}_{\mathcal{A}}\!\left[\sum_{t=1}^{T}\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^{T}\ell_t(i)\right].
$$

The target is expected external regret, worst-case over fixed loss streams; expectation includes only algorithmic randomness.

**View qualification.** The public budgets are $\epsilon_{\rm priv},\delta_{\rm priv}$. For every neighboring pair of fixed streams and measurable E, $\Pr(\mathcal A(\mathsf D)\in E)\le e^{\epsilon_{\rm priv}}\Pr(\mathcal A(\mathsf D^{\prime})\in E)+\delta_{\rm priv}$.

## 2. Notation and parameters

$K$: Number of experts **Domain:** $K\in\mathbb N,\ K\ge2$.

The expert set is $[K]$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\epsilon_{\mathrm{priv}}$: The multiplicative differential-privacy parameter. **Domain:** $\epsilon_{\mathrm{priv}}>0$.

Use the factor $e^{\epsilon_{\mathrm{priv}}}$ when comparing probabilities of output events under adjacent data inputs.

$L_\star$: Cumulative loss of the best fixed expert in hindsight **Domain:** $0\le L_\star\le T$.

$L_\star=\min_{i\in[K]}\sum_{t=1}^T\ell_t(i)$ is an instance-dependent analytical quantity and is not supplied to the algorithm.

$\ell_t$: Hidden loss vector at round t **Domain:** $\ell_t\in[0,1]^K$.

The entire sequence is fixed before interaction; only coordinates allowed by the protocol become visible after acting.

$I_t$: Arm or expert that actually incurs loss in round $t$ **Domain:** $I_t\in[K]$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$i$: The fixed comparator expert’s index. **Domain:** $i\in[K]$.

$\mathsf D,\mathsf D^{\prime}$: Neighboring input streams differ in one round's complete loss vector. **Domain:** A fixed sequence of loss vectors.

Privacy adjacency changes one complete round, rather than one loss coordinate.

$E$: A measurable event of action sequences in the pure-DP definition. **Domain:** A measurable subset of action-sequence space.

Require $\Pr(\mathcal A(\mathsf D)\in E)\le e^{\epsilon_{\mathrm{priv}}}\Pr(\mathcal A(\mathsf D^{\prime})\in E)$.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_t\ell_t(I_t)-\min_{i\in[K]}\sum_t\ell_t(i)$.

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes the learner's private randomness and, when allowed, the environment strategy's randomness. A fixed loss sequence introduces no additional observation noise.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts complete loss-vector feedback events; the corresponding scalar-coordinate count is KT.

$\delta_{\mathrm{priv}}$: Additive allowance in approximate differential privacy **Domain:** $0\le\delta_{\mathrm{priv}}<1$.

Additive allowance in the output-event probability inequality for adjacent inputs; not statistical confidence.

$E$: Measurable event in the action-sequence space used in the definition of approximate differential privacy **Domain:** A measurable subset of action-sequence space.

Comparisons of event probabilities on adjacent inputs permit the additive term $\delta_{\mathrm{priv}}$.

$\iota_2$: Additive privacy cost in the small-loss upper bound **Domain:** Nonnegative quantity in this upper bound.

$\iota_2=O((\log^{3/2}K\sqrt{\log\min\{1/\delta_{\mathrm{priv}},K\}}+\log K\log T)/\epsilon_{\mathrm{priv}})$ This term remains even on zero-loss instances.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

**View.** Pure differential privacy

$$
R_T=\sum_{t=1}^T\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i),\qquad L_\star=\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

#### Q2 - native performance

**View.** Approximate differential privacy

$$
R_T=\sum_{t=1}^T\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i),\qquad L_\star=\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Assume $0<\epsilon_{\rm priv}\le 1$; L_star is hidden. Retain the additional small-loss and zero-loss terms.

**Views.** Pure differential privacy

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\begin{aligned}[c]&O\!\left((\sqrt{\log K\log T}+\log K)\sqrt{\frac{L_\star}{\epsilon_{\mathrm{priv}}}}\right)\\ &\quad+\bigl(1+\log(1+L_\star)\bigr)\,O\!\left(\frac{\log^2K+\log K\log T}{\epsilon_{\mathrm{priv}}}\right).\end{aligned}
$$

### R2 - SUPPORTED

**Region.** Assume $0<\epsilon_{\rm priv}\le 1$ and $0<\delta_{\rm priv}\le 1/2$; L_star is unknown.

**Views.** Approximate differential privacy

**Quantity.** Q2

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B2

$$
\begin{aligned}[c]&O\!\Bigg(\sqrt{\frac{L_\star\log K\log T}{\epsilon_{\mathrm{priv}}}}\\ &\qquad+\log K\min\!\left\{\frac{(L_\star\log(1/\delta_{\mathrm{priv}}))^{1/3}}{\epsilon_{\mathrm{priv}}^{2/3}},\sqrt{\frac{L_\star}{\epsilon_{\mathrm{priv}}}}\right\}\Bigg)\\ &\quad+\bigl(1+\log(1+L_\star)\bigr)\iota_2,\\ &\iota_2=O\!\left(\frac{\log^{3/2}K\sqrt{\log\min\{1/\delta_{\mathrm{priv}},K\}}+\log K\log T}{\epsilon_{\mathrm{priv}}}\right).\end{aligned}
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - A pure-DP expert algorithm adaptive to small loss.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Pure differential privacy

**Witness or lower-bound scope.** Randomized witness

$$
\begin{aligned}[c]&O\!\left((\sqrt{\log K\log T}+\log K)\sqrt{\frac{L_\star}{\epsilon_{\mathrm{priv}}}}\right)\\ &\quad+\bigl(1+\log(1+L_\star)\bigr)\,O\!\left(\frac{\log^2K+\log K\log T}{\epsilon_{\mathrm{priv}}}\right).\end{aligned}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.29575v2)

**Conditions.** Assume $0<\epsilon_{\mathrm{priv}}\le1$. Losses are fixed before interaction, and $L_\star=\min_i\sum_t\ell_t(i)$ is unknown.; This is a small-loss upper bound. When $L_\star$ and $T$ have the same order, it is not necessarily the best worst-case bound.

**Source location.** [1](https://arxiv.org/pdf/2610.29575v2) Theorem 1.1, PDF p.2

### B2 - An approximate-DP expert algorithm adaptive to small loss.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Approximate differential privacy

**Witness or lower-bound scope.** Randomized witness

$$
\begin{aligned}[c]&O\!\Bigg(\sqrt{\frac{L_\star\log K\log T}{\epsilon_{\mathrm{priv}}}}\\ &\qquad+\log K\min\!\left\{\frac{(L_\star\log(1/\delta_{\mathrm{priv}}))^{1/3}}{\epsilon_{\mathrm{priv}}^{2/3}},\sqrt{\frac{L_\star}{\epsilon_{\mathrm{priv}}}}\right\}\Bigg)\\ &\quad+\bigl(1+\log(1+L_\star)\bigr)\iota_2,\\ &\iota_2=O\!\left(\frac{\log^{3/2}K\sqrt{\log\min\{1/\delta_{\mathrm{priv}},K\}}+\log K\log T}{\epsilon_{\mathrm{priv}}}\right).\end{aligned}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.29575v2)

**Conditions.** Require $0<\epsilon_{\mathrm{priv}}\le1$ and $0<\delta_{\mathrm{priv}}\le1/2$.; The quantity $L_\star$ is the unknown cumulative loss of the best expert, and $\iota_2$ is the additive privacy term defined in the displayed expression. This term must be retained even when $L_\star=0$.

**Source location.** [1](https://arxiv.org/pdf/2610.29575v2) Theorem 1.2, PDF p.2

### B3 - Lazy-to-Private; parameter correspondence remains unverified.

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**View.** Approximate differential privacy

**Witness or lower-bound scope.** Witness type not certified

$$
\widetilde{O}\!\left(\sqrt{T\log K}+\frac{T^{1/3}\log K}{\epsilon_{\mathrm{priv}}^{2/3}}\right)
$$

**Sources.** [2](https://papers.nips.cc/paper_files/paper/2024/file/cb775ebc750e0454a470fc99c5accc85-Paper-Conference.pdf)

**Conditions.** Losses are fixed before interaction and obey the L2P parameter, rounding, and probability-tuning conditions in source Theorem 3.2.; The exact $\delta_{\mathrm{priv}}$ dependence and the stated conditions have not been independently reconciled in this review; retain the asymptotic statement as reported by the source.; This upper bound comes from one construction. The same paper's lower bound for restricted mechanisms does not cover all private strategies and cannot establish minimax closure for the general class.

**Source location.** [2](https://papers.nips.cc/paper_files/paper/2024/file/cb775ebc750e0454a470fc99c5accc85-Paper-Conference.pdf) Theorem 3.10 pp.8–9

## References

[1] Bo Li; Peng Ye. Private Online Prediction from Experts with Small Losses. 2026. 2610.29575v2.

https://arxiv.org/pdf/2610.29575v2

[2] Hilal Asi; Tomer Koren; Daogao Liu; Kunal Talwar. Private Online Learning via Lazy Algorithms. 2024. NeurIPS 2024 publisher PDF.

https://papers.nips.cc/paper_files/paper/2024/file/cb775ebc750e0454a470fc99c5accc85-Paper-Conference.pdf
