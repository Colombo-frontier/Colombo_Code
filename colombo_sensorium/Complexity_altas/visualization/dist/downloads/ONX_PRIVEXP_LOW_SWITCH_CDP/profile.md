# Online experts: a low-switch public-resampling mechanism under concentrated differential privacy.

**Setting ID.** `ONX_PRIVEXP_LOW_SWITCH_CDP`

Online learning and bandits

After incurring the selected expert's loss, the learner observes the full loss vector; the complete loss stream is fixed in advance. Privacy protects one round's complete loss vector, and the release is the full action sequence. Only the specified low-switching and public-resampling mechanisms are allowed.

**Status.** Bounds missing

**TASK tags.** formulation: Onx privexp low switch cdp; task family: Online bandit

**MODEL tags.** structure: Finite actions

**ORACLE tags.** interface family: Full loss vector; operation: Full loss vector; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: Concentrated differential privacy

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

After incurring the selected expert's loss, the learner observes the full loss vector; the complete loss stream is fixed in advance. Privacy protects one round's complete loss vector, and the release is the full action sequence. Only the specified low-switching and public-resampling mechanisms are allowed.

### Admissible model

Before interaction, fix $T$ loss vectors $\ell_t\in[0,1]^K$ satisfying $K\ge2$. Adjacent private inputs differ in one complete round’s loss vector.

### Oracle interface

There are $K\ge2$ experts, with losses $\ell_t:[K]\to[0,1]$ fixed before interaction. Select $I_t$, then observe the complete current loss vector. Adjacent input streams differ in one entire loss vector.

The quantity $L_\star=\min_i\sum_t\ell_t(i)$ is the unknown cumulative loss of the best fixed expert.

The quantity $K,T,\epsilon_{\mathrm{priv}}$ is public. The infimum is restricted to mechanisms satisfying source Condition 4.1, not all private expert algorithms.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

Return the action sequence and the public resampling times and selected experts. The entire record jointly satisfies the stated CDP condition. Final postprocessing cannot alter actions already taken.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^T\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i),\qquad L_\star=\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).
$$

Cumulative external regret, without division by $T$. Privacy separately constrains the designated released record.

### Resource accounting

$$
\mathbb{E}\!\left[\sum_{t=1}^{T}\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^{T}\ell_t(i)\right].
$$

Take the infimum over the stated restricted algorithms and supremum over fixed loss streams. Each round provides one full-vector feedback event, so $N=T$. Resampling records are public.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

In each round the algorithm may retain the current expert or resample the next expert from $\mu_{t+1}$ determined by past losses.

The release includes the full action sequence $I_{1:T}$, resampling rounds, and resampled experts or models. All are part of the output transcript protected by privacy.

Let $P_{\mathrm{tr}},Q_{\mathrm{tr}}$ denote the distributions of complete released transcripts induced by neighboring loss streams. Use the source normalization of $\epsilon_{\mathrm{priv}}^2$ concentrated differential privacy (CDP):

$$
D_a(P_{\mathrm{tr}}\|Q_{\mathrm{tr}})\le\epsilon_{\mathrm{priv}}^2 a\qquad(\forall a>1).
$$

The quantity $D_a$ is Rényi divergence of order $a$. Public resampling rounds and models must also be included in the inequality.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Take the infimum over the stated restricted algorithms and supremum over fixed loss streams. Each round provides one full-vector feedback event, so $N=T$. Resampling records are public.

## 2. Notation and parameters

$K$: Number of experts **Domain:** $K\in\mathbb N,\ K\ge2$.

The expert set is $[K]$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\epsilon_{\mathrm{priv}}$: Square root of the concentrated-privacy parameter **Domain:** $\epsilon_{\mathrm{priv}}>0$.

Require $D_a(P_{\mathrm{tr}}\|Q_{\mathrm{tr}})\le a\epsilon_{\mathrm{priv}}^2$ ($a>1$), with concentrated-privacy parameter $\epsilon_{\mathrm{priv}}^2$.

$\ell_t$: Hidden loss vector at round t **Domain:** $\ell_t\in[0,1]^K$.

The entire sequence is fixed before interaction; only coordinates allowed by the protocol become visible after acting.

$I_t$: Arm or expert that actually incurs loss in round $t$ **Domain:** $I_t\in[K]$.

$[K]$: Index set of K arms or experts **Domain:** A finite set.

$[K]=\{1,\ldots,K\}$.

$i$: The fixed comparator expert’s index. **Domain:** $i\in[K]$.

$\mathsf D,\mathsf D^{\prime}$: Neighboring input streams differ in one round's complete loss vector. **Domain:** A fixed sequence of loss vectors.

Privacy adjacency changes one complete round, rather than one loss coordinate.

$\mu_{t+1}$: Resampling distribution chosen from the observed loss history **Domain:** $\mu_{t+1}\in\Delta_K$.

Its information dependence is restricted by the low-switching mechanism conditions; it is not an environment reward mean.

$P_{\mathrm{tr}},Q_{\mathrm{tr}}$: Distributions of the complete public transcript induced by adjacent loss inputs. **Domain:** A probability distribution.

The public transcript includes the stated actions and resampling information.

$a,D_a$: The Rényi order and divergence. **Domain:** $a>1$.

The quantity is $D_a(P\|Q)=(a-1)^{-1}\log\int(dP/dQ)^a\,dQ$, with value infinity when absolute continuity fails.

$\Delta_K$: Probability simplex containing the resampling distribution **Domain:** A finite-dimensional probability-vector set.

$\Delta_K=\{p\in[0,1]^K:\sum_ip_i=1\}$.

$L_\star$: The best expert’s loss on the fixed loss stream. **Domain:** $0\le L_\star\le T$.

The quantity $L_\star=\min_i\sum_t\ell_t(i)$ is not public.

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

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
R_T=\sum_{t=1}^T\ell_t(I_t)-\min_{i\in[K]}\sum_{t=1}^T\ell_t(i),\qquad L_\star=\min_{i\in[K]}\sum_{t=1}^T\ell_t(i).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** The public low-switch resampling mechanism satisfies Condition 4.1, with $\epsilon_{\rm priv}^{2}-CDP$ and $\epsilon_{\rm priv}\ge 100\log(KT)^{3/2}/T$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Upper bound missing

**Lower bound.** B1

$$
\Omega\!\left(\sqrt T+\frac{T^{1/3}}{\epsilon_{\mathrm{priv}}^{2/3}}\right)
$$

**Upper bound.** Admitted envelope

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $\epsilon_{\mathrm{priv}}\ge100\log^{3/2}(KT)/T$, Condition 4.1 of the source, and $\epsilon_{\mathrm{priv}}^2$ concentrated differential privacy.; The quantifiers cover only the specified restricted mechanism class, not every $(\epsilon_{\mathrm{priv}},\delta_{\mathrm{priv}})$-differentially-private experts algorithm. This result cannot form a matching bracket for the unrestricted approximate-privacy contract.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - The lower bound for the public resampling, low-switch CDP mechanism.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

$$
\Omega\!\left(\sqrt T+\frac{T^{1/3}}{\epsilon_{\mathrm{priv}}^{2/3}}\right)
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/cb775ebc750e0454a470fc99c5accc85-Paper-Conference.pdf)

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/cb775ebc750e0454a470fc99c5accc85-Paper-Conference.pdf) Theorem 4.2, PDF p.10

## References

[1] Hilal Asi; Tomer Koren; Daogao Liu; Kunal Talwar. Private Online Learning via Lazy Algorithms. 2024. NeurIPS 2024 publisher PDF.

https://papers.nips.cc/paper_files/paper/2024/file/cb775ebc750e0454a470fc99c5accc85-Paper-Conference.pdf
