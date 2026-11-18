# Matérn kernel bandits with a known upper bound on the number of stationary segments

**Setting ID.** `ONX_KERNEL_MATERN_SWITCH`

Online learning and bandits

The unknown reward functions belong to the reproducing kernel Hilbert space of a public Matérn kernel. Each round reveals one value corrupted by Gaussian noise at the chosen point. The objective tracks the current maximum reward. An upper bound on the number of stationary segments is known, but the change times are not.

**Status.** Polynomial gap present

**TASK tags.** formulation: Onx kernel matern switch; task family: Online bandit

**MODEL tags.** smoothness: Matern rkhs; stochastic model: Nonstationary

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

The unknown reward functions belong to the reproducing kernel Hilbert space of a public Matérn kernel. Each round reveals one value corrupted by Gaussian noise at the chosen point. The objective tracks the current maximum reward. An upper bound on the number of stationary segments is known, but the change times are not.

### Admissible model

The action domain is $[0,1]^d$. The Matérn kernel $k_{\nu,\ell}$ and its RKHS are public, with $\nu,\ell>0$ and $k(x,x)=1$. The function sequence is fixed before interaction and satisfies:

$$
\|f_t\|_{\mathcal{H}_k}\le B,\qquad \sum_{t=2}^{T}\mathbf 1\{f_t\ne f_{t-1}\}\le S_{\mathrm{seg}}-1,\qquad 1\le S_{\mathrm{seg}}\le T.
$$

### Oracle interface

Choose $x_t$, then observe $Y_t=f_t(x_t)+Z_t$ with $Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal{N}(0,\sigma^2)$. Only one action-point observation is available each round.

Causal strategies are allowed. The quantity $T,S_{\mathrm{seg}},k,B,\sigma$ is public; switching times and reward functions are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

Use the cumulative quantity in the task formula, without dividing by online rounds.

### Resource accounting

The budget is $N=T$ noisy function values. The registered lower bound fixes $d,B,\sigma,\nu,\ell$ and concerns the corresponding horizon and segment-count dependence.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

$$
\inf_{\mathcal{A}}\ \sup_{f_{1:T}\ \text{\text{has at most} }S_{\mathrm{seg}}\text{ \text{stationary segments}}}\ \mathbb{E}\!\left[\sum_{t=1}^{T}\left(\max_{x\in[0,1]^d}f_t(x)-f_t(x_t)\right)\right].
$$

Expectation includes algorithmic and Gaussian-noise randomness. The worst case ranges only over fixed function sequences satisfying the RKHS norm bound.

## 2. Notation and parameters

$B$: The RKHS norm bound for each reward function. **Domain:** $B>0$.

$\|f_t\|_{\mathcal H_k}\le B$. The condition $k(x,x)=1$ implies $|f_t(x)|\le B$.

$S_{\mathrm{seg}}$: A public upper bound on stationary segments. **Domain:** $S_{\mathrm{seg}}\in\mathbb N,\ 1\le S_{\mathrm{seg}}\le T$.

Assume $1+\sum_{t=2}^T\mathbf1\{f_t\ne f_{t-1}\}\le S_{\mathrm{seg}}$; change-point locations are not disclosed.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\sigma$: Standard deviation of independent Gaussian observation noise **Domain:** Assume $\sigma\ge0$; the noisy lower bound uses a fixed positive noise scale.

The quantity $Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal N(0,\sigma^2)$ is independent of the learner and the fixed function sequence.

$\nu$: The Matérn kernel smoothness parameter. **Domain:** Assume $\nu>0$; this comparison further requires $\nu>1/2$.

Smoothness parameter of the fixed kernel $k_{\nu,\ell}$; not a reward distribution.

$\ell$: Length scale of the Matérn kernel **Domain:** $\ell>0$.

Length parameter controlling spatial correlation in the fixed kernel; it does not denote a loss vector.

$k_{\nu,\ell}$: Variance-normalized Matérn kernel **Domain:** Public positive definite kernel.

Assume $k_{\nu,\ell}(x,y)=2^{1-\nu}z^\nu\mathrm K_\nu(z)/\Gamma(\nu)$ and $z=\sqrt{2\nu}\|x-y\|_2/\ell$. When $z=0$, define the value as one by continuity.

$\mathcal H_k$: Reproducing kernel Hilbert space of kernel $k$. **Domain:** The Hilbert space of functions.

The evaluation identity is $f(x)=\langle f,k(x,\cdot)\rangle_{\mathcal H_k}$; the norm is that of the RKHS.

$f_t,x_t$: Current hidden reward function and selected action **Domain:** $f_t\in\mathcal H_k,\ x_t\in[0,1]^d$.

The function sequence is fixed before interaction, with $\|f_t\|_{\mathcal H_k}\le B$.

$Y_t,Z_t$: Noisy reward observation and added noise **Domain:** $Y_t,Z_t\in\mathbb R$.

Assume $Y_t=f_t(x_t)+Z_t$ and $Z_t\sim\mathcal N(0,\sigma^2)$; only one point is observed per round.

$\|g\|_\infty$: The uniform norm over the complete action domain. **Domain:** A nonnegative real.

Assume $\|g\|_\infty=\sup_{x\in[0,1]^d}|g(x)|$; kernel normalization implies $\|g\|_\infty\le\|g\|_{\mathcal H_k}$.

$\gamma_T$: Maximum kernel information gain from $T$ action points **Domain:** A nonnegative real.

$\gamma_T=\frac12\sup_{x_1,\ldots,x_T\in[0,1]^d}\log\det(I_T+\lambda_{\mathrm{ker}}^{-1}K_T)$, where $(K_T)_{ij}=k(x_i,x_j)$.

$\lambda_{\mathrm{ker}}$: Fixed regularization scale in the definition of information gain **Domain:** Fixed positive real number.

May be fixed at one. Changing this fixed positive number changes only constants under fixed kernel and noise scales and reveals no hidden-function information.

$K_T,I_T$: Kernel Gram matrix and the identity matrix of order $T$ **Domain:** $K_T,I_T\in\mathbb R^{T\times T}$.

The quantity is $K_T=(k(x_i,x_j))_{i,j=1}^T$; it is not the finite arm count K.

$\delta_{\mathrm{conf}}$: Internal failure probability used to convert a probability bound to an expectation bound **Domain:** Used only in the proof of the corresponding upper bound.

The adaptive branch uses $T^{-2}$ and the known-budget restart branch uses $T^{-1}$; both are ultimately converted to expected dynamic pseudo-regret.

$\mathrm K_\nu,\Gamma$: The modified Bessel and Gamma functions in the Matérn kernel formula. **Domain:** Standard special functions.

The function $\mathrm K_\nu$ is the modified Bessel function of the second kind; $\Gamma(\nu)=\int_0^\infty t^{\nu-1}e^{-t}\,dt$, where $\nu>0$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t[\max_{x\in[0,1]^d}f_t(x)-f_t(x_t)]$. Realized observation noise is excluded from the loss difference; probability or expectation aggregation is specified separately by the guarantee.

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
\inf_{\mathcal A}\ \sup_{f_{1:T}\ \text{has at most }S_{\mathrm{seg}}\text{ stationary segments}}\ \mathbb E\!\left[\sum_{t=1}^{T}\left(\max_{x\in[0,1]^d}f_t(x)-f_t(x_t)\right)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

Expectation covers the algorithm and Gaussian noise. The worst case ranges only over fixed function sequences satisfying the RKHS-norm constraint.

### R1 - SUPPORTED

**Region.** Fix $d,B,\sigma,\nu,\ell$ and assume $\nu>1/2$ and $1\le S_{\rm seg}\le T$ within the source asymptotic lower-bound window. The comparison additionally requires fixed positive noise $\sigma>0$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Polynomial gap

**Lower bound.** B1

$$
\Omega(S_{\rm seg}^{\nu/(2\nu+d)}T^{(\nu+d)/(2\nu+d)})
$$

**Upper bound.** B2

$$
\widetilde{O}\!\left(\min\{2BT,\sqrt{S_{\rm seg}T\gamma_T}\}\right)
$$

## 4. Bounds and supporting evidence

### B1 - Hard instances with bumps in independent stationary segments

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(S_{\mathrm{seg}}^{\nu/(2\nu+d)}T^{(\nu+d)/(2\nu+d)}\right)
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf)

**Conditions.** $1\le S_{\mathrm{seg}}\le T$, where $S_{\mathrm{seg}}$ bounds the number of stationary segments and $d,B,\sigma,\nu,\ell$ is fixed.; This noisy information-theoretic lower bound fixes $B>0$ and $\sigma>0$; it does not cover the zero-noise degeneracy.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf) Theorem 1 p.4 Eq.(12)

### B2 - ADA-OPKB: optimized sampling and change detection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(\min\{2BT,\sqrt{S_{\rm seg}T\gamma_T}\}\right)
$$

**Sources.** [2](https://proceedings.mlr.press/v206/hong23b.html)

**Conditions.** Fix $d,B,\sigma,\nu,\ell$ and assume $\nu>1/2$, with horizon $T$ sufficiently large. Hidden constants may depend on these fixed kernel and noise parameters.; The algorithm requires neither a variation budget nor a switch count and uses public exact kernel operations to build a fine grid. Asymptotic thresholds are not replaced by unsupported uniform numerical thresholds.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T Gaussian-noised values

**computation.** Finite-grid optimization may be expensive. Internal computation is unrestricted in this setting.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** Appendix D.7 of the source handles Gaussian observations by sub-Gaussian truncation. Set the grid error to $1/T$; for fixed Matern kernel parameters, the logarithm of grid size is $O(\log T)$. Choosing failure probability $\delta=T^{-2}$ and using $R_T\le2BT$ yields an expectation bound. Information gain satisfies $\gamma_T=O(T^{d/(2\nu+d)}(\log T)^{2\nu/(2\nu+d)})$. The RKHS-drift variant also uses $k(x,x)\le1$ to derive $\|f-g\|_\infty\le\|f-g\|_{\mathcal H_k}$; the uniform-norm and switching variants require no such norm conversion.

**Source location.** [2](https://proceedings.mlr.press/v206/hong23b.html) theorem: Theorem3.1; Section3; AppendixD.7

Appendix D.7 of the source handles Gaussian observations by sub-Gaussian truncation. Set the grid error to $1/T$; for fixed Matern kernel parameters, the logarithm of grid size is $O(\log T)$. Choosing failure probability $\delta=T^{-2}$ and using $R_T\le2BT$ yields an expectation bound. Information gain satisfies $\gamma_T=O(T^{d/(2\nu+d)}(\log T)^{2\nu/(2\nu+d)})$. The RKHS-drift variant also uses $k(x,x)\le1$ to derive $\|f-g\|_\infty\le\|f-g\|_{\mathcal H_k}$; the uniform-norm and switching variants require no such norm conversion.

## References

[1] Xu Cai; Jonathan Scarlett. Lower Bounds for Time-Varying Kernelized Bandits. 2025. AISTATS 2025, PMLR 258.

https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf

[2] Kihyuk Hong; Yuhang Li; Ambuj Tewari. An Optimization-based Algorithm for Non-stationary Kernel Bandits without Prior Knowledge. 2023. AISTATS2023, PMLR206:3048–3085.

https://proceedings.mlr.press/v206/hong23b.html
