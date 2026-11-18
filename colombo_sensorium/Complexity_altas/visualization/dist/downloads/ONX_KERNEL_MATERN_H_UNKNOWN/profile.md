# Matérn kernel bandits with an unknown RKHS variation budget

**Setting ID.** `ONX_KERNEL_MATERN_H_UNKNOWN`

Online learning and bandits

The unknown reward functions belong to the reproducing kernel Hilbert space of a public Matérn kernel. Each round reveals one value corrupted by Gaussian noise at the chosen point. The objective tracks the current maximum reward. Consecutive functions are compared in the RKHS norm, and the variation budget is not supplied to the algorithm.

**Status.** Polynomial gap present

**TASK tags.** formulation: Onx kernel matern h unknown; task family: Online bandit

**MODEL tags.** smoothness: Matern rkhs; stochastic model: Nonstationary

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; public information: Unknown variation

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Dynamic regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Time rounds; setup: Initialization included

## 1. Setting specification

### Task

The unknown reward functions belong to the reproducing kernel Hilbert space of a public Matérn kernel. Each round reveals one value corrupted by Gaussian noise at the chosen point. The objective tracks the current maximum reward. Consecutive functions are compared in the RKHS norm, and the variation budget is not supplied to the algorithm.

### Admissible model

The action domain is $[0,1]^d$. The Matérn kernel $k=k_{\nu,\ell}$ is public, with smoothness $\nu>0$, length scale $\ell>0$, and $k(x,x)=1$. The environment fixes all reward functions before interaction:

$$
f_t\in\mathcal{H}_k,\qquad \|f_t\|_{\mathcal{H}_k}\le B\quad(t=1,\ldots,T).
$$

$$
\sum_{t=2}^{T}\|f_t-f_{t-1}\|_{\mathcal{H}_k}\le V_{\mathcal{H}}.
$$

### Oracle interface

Each round first selects $x_t\in[0,1]^d$ and then receives one noisy function value there:

$$
Y_t=f_t(x_t)+Z_t,\qquad Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal{N}(0,\sigma^2).
$$

Noise is independent across rounds and independent of the algorithm. Only the current actual action point may be observed.

Causal randomized strategies are allowed; $d,T,k,B,\sigma$ is public.

The drift budget is hidden. One policy must operate without dependence on $V_{\mathcal{H}}$.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

Use the cumulative quantity in the task formula, without dividing by online rounds.

### Resource accounting

The resource is $N=T$ noisy function observations. The recorded public lower bound fixes $d,B,\sigma,\nu,\ell$ and therefore does not establish uniformly optimal polynomial dependence on those parameters.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

Every loss $f_{1:T}$ is hidden. Internal optimization has no polynomial-time restriction unless a computationally restricted variant is explicitly declared.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

$$
\inf_{\mathcal{A}}\ \sup_{f_{1:T}\ \text{\text{satisfying the stated constraints}}}\ \mathbb{E}_{\mathcal{A},Z}\!\left[\sum_{t=1}^{T}\left(\max_{x\in[0,1]^d}f_t(x)-f_t(x_t)\right)\right].
$$

The objective is expected dynamic regret relative to each round’s optimum, with expectation over algorithmic and observation randomness. The unknown-budget view requires one algorithm that does not take the drift budget as input.

## 2. Notation and parameters

$B$: The RKHS norm bound for each reward function. **Domain:** $B>0$.

$\|f_t\|_{\mathcal H_k}\le B$. The condition $k(x,x)=1$ implies $|f_t(x)|\le B$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$V_{\mathcal H}$: Total function variation measured in the RKHS norm. **Domain:** $0\le V_{\mathcal H}\le2B(T-1)$.

$\sum_{t=2}^T\|f_t-f_{t-1}\|_{\mathcal H_k}\le V_{\mathcal H}$.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\ell$: Length scale of the Matérn kernel **Domain:** $\ell>0$.

Length parameter controlling spatial correlation in the fixed kernel; it does not denote a loss vector.

$\nu$: The Matérn kernel smoothness parameter. **Domain:** Assume $\nu>0$; this comparison further requires $\nu>1/2$.

Smoothness parameter of the fixed kernel $k_{\nu,\ell}$; not a reward distribution.

$\sigma$: Standard deviation of independent Gaussian observation noise **Domain:** Assume $\sigma\ge0$; the noisy lower bound uses a fixed positive noise scale.

The quantity $Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal N(0,\sigma^2)$ is independent of the learner and the fixed function sequence.

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
\inf_{\mathcal A}\ \sup_{f_{1:T}\ \text{satisfying the stated constraints}}\ \mathbb E_{\mathcal A,Z}\!\left[\sum_{t=1}^{T}\left(\max_{x\in[0,1]^d}f_t(x)-f_t(x_t)\right)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

This is expected dynamic regret relative to each round's optimal value, averaging algorithmic and noise randomness. Unknown-budget variants require one algorithm that does not take the drift budget as input.

### R1 - SUPPORTED

**Region.** Fix d, B, sigma, nu, and ell; assume $\nu>1/2$ and the source's nondegenerate asymptotic drift window. The RKHS norm differs from the supremum norm. Lower-bound comparison additionally requires fixed positive noise $\sigma>0$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Polynomial gap

**Lower bound.** B2, B3

$$
\Omega(\max\left\{T^{(\nu+d)/(2\nu+d)},\ \begin{cases}V_{\mathcal{H}}^{\nu/(2\nu+d)}T^{(\nu+d)/(2\nu+d)},&\nu\le d,\\ V_{\mathcal{H}}^{1/3}T^{2/3},&\nu\ge d.\end{cases}\right\})
$$

**Upper bound.** B1, B4

$$
\widetilde{O}\!\left(\min\{2BT,\sqrt{T\gamma_T}+(\gamma_T V_{\mathcal{H}})^{1/3}T^{2/3}\}\right)
$$

## 4. Bounds and supporting evidence

### B1 - ADA-OPKB: optimized sampling and change detection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(\min\{2BT,\sqrt{T\gamma_T}+(\gamma_T V_{\mathcal{H}})^{1/3}T^{2/3}\}\right)
$$

**Sources.** [2](https://proceedings.mlr.press/v206/hong23b.html)

**Conditions.** Fix $d,B,\sigma,\nu,\ell$ and assume $\nu>1/2$, with horizon $T$ sufficiently large. Hidden constants may depend on these fixed kernel and noise parameters.; The algorithm requires neither a variation budget nor a switch count and uses public exact kernel operations to build a fine grid. Asymptotic thresholds are not replaced by unsupported uniform numerical thresholds.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**computation.** Finite-grid optimization may be expensive. Internal computation is unrestricted in this setting.

**native feedback.** T Gaussian-noised values

**rounds.** T

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** Appendix D.7 of the source handles Gaussian observations by sub-Gaussian truncation. Set the grid error to $1/T$; for fixed Matern kernel parameters, the logarithm of grid size is $O(\log T)$. Choosing failure probability $\delta=T^{-2}$ and using $R_T\le2BT$ yields an expectation bound. Information gain satisfies $\gamma_T=O(T^{d/(2\nu+d)}(\log T)^{2\nu/(2\nu+d)})$. The RKHS-drift variant also uses $k(x,x)\le1$ to derive $\|f-g\|_\infty\le\|f-g\|_{\mathcal H_k}$; the uniform-norm and switching variants require no such norm conversion.

**Source location.** [2](https://proceedings.mlr.press/v206/hong23b.html) theorem: Theorem3.1; Section3; AppendixD.7

Appendix D.7 of the source handles Gaussian observations by sub-Gaussian truncation. Set the grid error to $1/T$; for fixed Matern kernel parameters, the logarithm of grid size is $O(\log T)$. Choosing failure probability $\delta=T^{-2}$ and using $R_T\le2BT$ yields an expectation bound. Information gain satisfies $\gamma_T=O(T^{d/(2\nu+d)}(\log T)^{2\nu/(2\nu+d)})$. The RKHS-drift variant also uses $k(x,x)\le1$ to derive $\|f-g\|_\infty\le\|f-g\|_{\mathcal H_k}$; the uniform-norm and switching variants require no such norm conversion.

### B2 - Localized bump-block construction in the RKHS

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\begin{gathered}\begin{cases}\Omega\!\left(V_{\mathcal{H}}^{\nu/(2\nu+d)}T^{(\nu+d)/(2\nu+d)}\right),&\nu\le d,\\ \Omega\!\left(V_{\mathcal{H}}^{1/3}T^{2/3}\right),&\nu\ge d,\end{cases}\\ \text{\text{stationary subclass also has lower bound} }\Omega\!\left(T^{(\nu+d)/(2\nu+d)}\right).\end{gathered}
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf)

**Conditions.** The expression $V_{\mathcal H}$ corresponds to the data field $V_H$ and bounds $\sum_{t=2}^T\|f_t-f_{t-1}\|_{\mathcal H_k}$ from above.; The parameter $d,B,\sigma,\nu,\ell$ is fixed. The conclusion applies in the nontrivial asymptotic drift range and is capped by linear regret. The effective drift upper bound may be clipped to its feasible value $2B(T-1)$.; The source does not give a uniform numerical finite-horizon threshold. Dimension dependence in an exponent must not be interpreted as dimension-independent hidden constants. This result is registered separately from the directly verified upper bound and compared by region.; This noisy information-theoretic lower bound fixes $B>0$ and $\sigma>0$; it does not cover the zero-noise degeneracy.

**Oracle correspondence.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

**Derivation.** A lower bound in the stronger information model with public RKHS drift budget also constrains policies without that budget. Fixed kernel parameters, asymptotic windows, and linear-scale restrictions remain those of the source theorem.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf) Theorem 3 pp.4–5 Eqs.(14)–(15), paragraph immediately after theorem

### B3 - Switch-count subclass transfer

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(T)
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf)

**Conditions.** S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

**Oracle correspondence.** Same played-point scalar Gaussian feedback, oblivious functions, T actions and T observations.

**Guarantee conversion.** Same expected cumulative dynamic regret; supplying more subclass information cannot invalidate a lower bound for policies lacking that information.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**computation.** Unrestricted native computation

**native feedback.** T Gaussian-noised values; no extra queries

**rounds.** T

**Constants.** May depend on fixed d,B,sigma,nu,ell, not on T or V_H.

**Derivation.** See ONX_KERNEL_MATERN_H_UNKNOWN__main__p1. At most L-1 changes cost <=2B(L-1)<=V_H; Omega(sqrt(LT))=Omega(T).

**Local argument.** ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf) AISTATS 2025 / PMLR 258, Theorem 1 Eq.(12), pp.4-5; Section 3 model; Appendix C.1 Eq.(24), p.14. Read character ranges [11300,22000) and [43700,45900). Appendix B.2, p.13, read [42100,43800), establishes the random block construction.

Full source-to-target transfer and elementary upper-bound derivation are in ONX_KERNEL_MATERN_H_UNKNOWN__main__p1.

The source is a fixed 2025 proceedings version, before cutoff 2026-11-15. This does not certify absence of later differently titled corrections.

### B4 - Native pathwise regret cap

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** One feasible policy independent of V_H works simultaneously for every drift budget.

$$
2BT
$$

**Conditions.** The pathwise cap is valid throughout the native domain; this bound is adopted only on S in this patch.

**Oracle correspondence.** Unchanged native protocol.

**Guarantee conversion.** A pathwise cap also bounds the native expectation.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**computation.** Unrestricted native computation

**native feedback.** T Gaussian-noised values; no extra queries

**rounds.** T

**Constants.** Exact coefficient 2B; no suppressed constants or logs.

**Derivation.** From the frozen normalized-kernel/RKHS-ball premise, |f_t(x)|<=B, so each reward gap is at most 2B. Sum over T rounds; see ONX_KERNEL_MATERN_H_UNKNOWN__main__p1.

**Local argument.** ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf) AISTATS 2025 / PMLR 258, Theorem 1 Eq.(12), pp.4-5; Section 3 model; Appendix C.1 Eq.(24), p.14. Read character ranges [11300,22000) and [43700,45900). Appendix B.2, p.13, read [42100,43800), establishes the random block construction.

Full source-to-target transfer and elementary upper-bound derivation are in ONX_KERNEL_MATERN_H_UNKNOWN__main__p1.

The source is a fixed 2025 proceedings version, before cutoff 2026-11-15. This does not certify absence of later differently titled corrections.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 3b1270f44bec8683054719e54a6692c1dacbbfa32cb55cd74fb7a7cd73634218

### Native proof: ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

Native pointer: /proofs/0; canonical SHA-256: d3a5d516b9d18bbc00d766b6c2a6dcee0c08dd58d4b7759330feadc7ccc07312

#### Native field: assumptions

Native pointer: /proofs/0/assumptions; canonical SHA-256: 065f0ac3204aafd23ea6f9acf5e7d0d0897f2053fb9d6c8cc87d2528360e6399

#### Native item 1

Native pointer: /proofs/0/assumptions/0; canonical SHA-256: df5b1bffe4e1d8a097d5866aee64467bf574ec3005b97c06dd10d982ed78db19

S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

#### Native item 2

Native pointer: /proofs/0/assumptions/1; canonical SHA-256: 99ed7023b28041a86889691f2ef92c19651c13fb0ef5d831b2d2ea48bf041a61

The native oracle, view main, guarantee g1 and quantity q1 are unchanged.

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: 2ff66cc5d0e1cc9b2d0d3f5322af59c5a0a8573833260becc9ee0c651f6fddad

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: 63a30deb0e57cd5ab2668b84585d7f85e3d897b696b9c2d1cd9508054ee2bc0c

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: ae688fd93ccc1f98602dd8339f6a96037b721ef19370fc75e783caa6d8ababfe

6ce47283209950b3485f863e1998378f510981a6f6d804a9f032c739d7309fbf

#### Native field: derivation

Native pointer: /proofs/0/derivation; canonical SHA-256: a81397ae85112349ccc894343a45a2dd83ad6a46050e64fcdead0fc37ae87e3a

#### Native item 1

Native pointer: /proofs/0/derivation/0; canonical SHA-256: c0bc571bae692bc271b58a4f6ba5d89632295f84cb56f71a169e0e6148527144

For T>=4 choose the auxiliary integer L=floor(T/2). Then 1<=L<=T and L>=T/4. L is an analyst's subclass size, not information supplied to the target policy.

#### Native item 2

Native pointer: /proofs/0/derivation/1; canonical SHA-256: 41cfbd83234bd9aab87df3c71aa5cc2778dbe25f03eb137da32f421a5c76b5c5

Take the source Theorem 1 hard family with at most L-1 changes. Each reward function lies in the same normalized Matérn RKHS ball of radius B on [0,1]^d. By the triangle inequality each change has RKHS norm at most 2B. Therefore every member has total RKHS drift at most 2B(L-1)<=B(T-1)<=V_H.

#### Native item 3

Native pointer: /proofs/0/derivation/2; canonical SHA-256: 25d82399581ec44833ac20700c57da5c122129a2103f4c14bd5a4ac10f5666de

This proves inclusion in the target class without imposing a switch-count promise on the target. The source uses the same played-point Gaussian scalar observations and expected cumulative dynamic regret. Its block hard family is fixed obliviously before interaction. Causal randomized policies and their action trajectories are preserved, as are T rounds and T observations. A lower bound against policies even given the subclass parameters also holds against policies not given V_H.

#### Native item 4

Native pointer: /proofs/0/derivation/3; canonical SHA-256: 036771a0de534e3f9acb231fdbf6ed95921afdd43eeba279fb56dba8a36e4f4d

Theorem 1, Eq.(12), includes the lower bound Omega(sqrt(L*T)) for every fixed (nu,d). Since L>=T/4, sqrt(L*T)>=T/2, giving Omega(T) uniformly over V_H in S. Alternatively its main rate L^{nu/(2nu+d)}T^{(nu+d)/(2nu+d)} has the same consequence. No external theorem beyond the read source is introduced.

#### Native item 5

Native pointer: /proofs/0/derivation/4; canonical SHA-256: a09818201e3ccdb638263097dab45eba1813b1376a83bcc431af9e078c7cdb7f

The frozen native norm/kernel contract gives |f_t(x)|<=B and 0<=R_T<=2BT pathwise. Thus any fixed feasible policy independent of V_H gives expected regret <=2BT. Together with the lower bound this yields Theta(T) on S.

#### Native item 6

Native pointer: /proofs/0/derivation/5; canonical SHA-256: 1cf83f8996f4b084bd90368a5679a293759fdde964a77688508c89fc2ef6f33a

The threshold V_H>=B(T-1) is an exact sufficient inclusion inequality, not a claim about the smallest drift causing linear regret. Source asymptotic constants are retained; no numerical finite-horizon threshold is inferred.

#### Native field: evidence_refs

Native pointer: /proofs/0/evidence_refs; canonical SHA-256: 74fe140907d2dc3d4cfc15808be32092aa5e614019487e70c7769a5b1b214f1f

#### Native item 1

Native pointer: /proofs/0/evidence_refs/0; canonical SHA-256: 89fbeed841d8728e2e1dd7c2f4c0f9f929c84e9e98e32a0feb7f7d167e979f0f

ONX_KERNEL_MATERN_H_UNKNOWN__main__e3

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: b9b1cb1bb9b56669469bcd3eaf745121b51ff9f2beedd1b4ee066e91d649821e

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 819ab4e38678e9d775f96f16d78b3c773fd16600b024e2062d1bfe7f7925b1e4

ONX_SRC_RKHS2025

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 460611ecad2dad145b06f71e674dba38c058c8b1dddd271dc9760184cefcaa5b

On S, the native unknown-RKHS-budget expected dynamic regret is Theta(T), with upper bound 2BT.

### Native proof: ONX_KERNEL_MATERN_H_UNKNOWN__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/1; canonical SHA-256: 36a2b736b6bc934986b5087ad97281d77ff0b43ca5c6b9ce334bca74137a4c68

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: bcc95f4a9d9dcd1de16218eabfd251bba2026694ba8b1fb8796e40216096b0b3

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. On S, the retained positive structural constant c and bounds c*T<=R_T^*<=2*B*T match for fixed d,B,sigma,nu,ell, so this local state is optimal. The earlier witness lies in S but has no proof of membership outside symbolic W; therefore the canonical impact records explicit saturation-region registration and does not assert a proved nonempty S minus W. 

#### Native field: comparison_refs

Native pointer: /proofs/1/comparison_refs; canonical SHA-256: 54e693b0399096a9b0248fbda33af96d37c2a698b28e7fcf9bc876b67d94832a

#### Native item 1

Native pointer: /proofs/1/comparison_refs/0; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: evidence_basis

Native pointer: /proofs/1/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 0b82b0baedf5effeed2663858606a26accc7acf18f4a68d049c02962e41d5b34

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 359b6f3fa2cbb035c742be14fa7ff8e988890f4ea080589bae066aad7004e64e

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: bc421b135dfada8a29342c524f96662db1f7243fc6bc0f8bd6b37c729299e7f8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 8ee86ac9fe83d7f8bad841736f34d312de81012083ff407bf325b7aab1c0cdb4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: d2d783ebe72f621e27a2c136566578f763f4129ce58d4aab35cd5ca54d352aa5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: bf225f2e4787e165f5a245e55bb71f55793511a8a605aefe07ca2c056ccf936d

W

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 5c974e4300842fec2372948266f9eb795579ddda56935144b466d30fc7a0176b

ONX_KERNEL_MATERN_H_UNKNOWN__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 2c79a8629ad83b0d30216cd273b60bb372c46477aefe5ac8d35a5117fed31360

Retain the frozen upper envelope and conversion guards conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 68c686d8c0bfe0f66118c7575994cc76cb8d0e4e65de7f4fe884c1a047c71f5f

W = the unchanged frozen theorem window in /regimes/0 and /comparisons/0, including nu>1/2, fixed positive sigma, sufficiently large T, and the retained nondegenerate-drift/linear-scale guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: f73a4a2db449e8bec8d51fc3dc8764dafcc09cdfed49bdae62e706ef50020c9b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: bf225f2e4787e165f5a245e55bb71f55793511a8a605aefe07ca2c056ccf936d

W

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 4336171618ec49a56737a878b09646883a03a04278d7ebbf4b28399ceb74bc02

ONX_KERNEL_MATERN_H_UNKNOWN__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 49d5f27710d0ace6758bec1dcd1b73eeba43154aff5c5cb431f3b6c5d81be62b

Retain the frozen lower/stationary terms with positive-noise and linear-scale guards.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 68c686d8c0bfe0f66118c7575994cc76cb8d0e4e65de7f4fe884c1a047c71f5f

W = the unchanged frozen theorem window in /regimes/0 and /comparisons/0, including nu>1/2, fixed positive sigma, sufficiently large T, and the retained nondegenerate-drift/linear-scale guards.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 3cb0882e5af1df0c675c9eeebf7d40cf2492b7a63e89738c1b3c6aded8dcf3e9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 5511a0b33d80360690774b4528fec86cd6cb6a8e379ce4a03520ae0d81834dd1

ONX_KERNEL_MATERN_H_UNKNOWN__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: eb4768a45aae6a625b2342b1e9c9adffa8b5d0d0cde287fb772104fddbfd8a19

On S intersect W, V_H=Theta(T) for fixed B, so both old lower branches already have Omega(T) order. No new active c1 reference.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: df5b1bffe4e1d8a097d5866aee64467bf574ec3005b97c06dd10d982ed78db19

S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 7c2ca0b3d6005154d0afdd4db83ea4d54337913785daffcca4935445d1de204d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 11bfa6b9ed4ee734dd28c9be2bac3da5c33248b90cdf6bb4efabde18694c05a9

ONX_KERNEL_MATERN_H_UNKNOWN__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 456ecf92d9d2b88d53c6ad4003fc04788a7ce943a30ffea2a85ceb7c67fbeecb

The exact 2BT cap already occurs in b1's guarded min. No new active c1 reference.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: fd7a166309f5195013842f6371a9b8aaa4328150413d7c1d3ac290f609fa6dcb

Entire native domain; recorded adoption on S.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: c956ceb1f81665b87146e06f1d698754d0419717eeb54775ec6565543308d2a1

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 2937879e4e8a66f37cf35f75ec27261c8db658e287ee7d5af45bc08f6183293b

At nu=d the dynamic lower branches coincide.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: daa1ae9a12ae82da478350a56bbfc3478d58185346de2748f512199ecc574577

Keep the 2BT cap and source guards; do not extrapolate an uncapped asymptotic lower formula to arbitrary endpoints.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 77d656673baa6d8b9173c345ccb60677ae7ce7d6abf7bf21957efb7522bde861

The stationary term is retained, without expanding c1's active guard to V_H=0 outside W.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 0e41cab3f0d8bbc766a8d93f602534af162ba943cc983aba59c92b7757e7ce7e

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/2; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/3; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/4; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 0e41cab3f0d8bbc766a8d93f602534af162ba943cc983aba59c92b7757e7ce7e

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/2; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/3; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/4; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: a6627317004d178c6dfb2a2c0e514daa8196f1b7f88429b55ec0dc4d326bca33

Retain the native polynomial_gap classification and the ratio of these guarded envelopes. This is not a pointwise polynomial-gap claim: c2 identifies matching Theta(T) order on S intersect W.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: c16788d9d3a3156abc80d9d0a52f8063372fb761a08bf87f659ec4031f461765

\Omega(\max\left\{T^{(\nu+d)/(2\nu+d)},\ \begin{cases}V_{\mathcal H}^{\nu/(2\nu+d)}T^{(\nu+d)/(2\nu+d)},&\nu\le d,\\ V_{\mathcal H}^{1/3}T^{2/3},&\nu\ge d.\end{cases}\right\}); only on W with frozen linear-scale/noise guards.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 5c323e2acfa0233fb297ae82d430eada9fbd769b3e8c78ff2cc4a111597f922d

The non-saturation part of W retains the curated gap. Uniform structural-parameter dependence and globally strongest rates are not established.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 278f26332dbd92c6fc9ec5334bd059a68212a43c0fca34fbe4008880d69ecfba

\widetilde O\!\left(\min\{2BT,\sqrt{T\gamma_T}+(\gamma_T V_{\mathcal H})^{1/3}T^{2/3}\}\right); only on W with all frozen guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 89fe20640d29911309c8b47db4e66411175f9f3af065b2f08dbed7e5660b2c3e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 070e5e8931969f2a9e2783c336986080b7e34230d73f39af6639de6a16619550

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: dc86b99adff1e444f97653672568a5afa38d8cbc8a795adb689220449dcf425e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 5c974e4300842fec2372948266f9eb795579ddda56935144b466d30fc7a0176b

ONX_KERNEL_MATERN_H_UNKNOWN__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 993e6e29701a09ad0a3f1f09798dab46bd7aeb03a78b0535d6a245cf471bc39e

Only applicable on S intersect W; b4 already supplies its linear cap. Not adopted outside W.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 68c686d8c0bfe0f66118c7575994cc76cb8d0e4e65de7f4fe884c1a047c71f5f

W = the unchanged frozen theorem window in /regimes/0 and /comparisons/0, including nu>1/2, fixed positive sigma, sufficiently large T, and the retained nondegenerate-drift/linear-scale guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 81319126ead2a47d3e1c5e1e1a3469986bb81cd2723bcb3009cfe42ff7bd749a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 4336171618ec49a56737a878b09646883a03a04278d7ebbf4b28399ceb74bc02

ONX_KERNEL_MATERN_H_UNKNOWN__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 303ee112ac8ddd0314bd9edab2f7e00a251ec8786709e787c3d80d568b5e8d2b

Only applicable on S intersect W; either dynamic branch is Omega(T) there. Not adopted outside W.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 68c686d8c0bfe0f66118c7575994cc76cb8d0e4e65de7f4fe884c1a047c71f5f

W = the unchanged frozen theorem window in /regimes/0 and /comparisons/0, including nu>1/2, fixed positive sigma, sufficiently large T, and the retained nondegenerate-drift/linear-scale guards.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 5fe20c9e1184535610e26759d31777a12e8cf40846ea7b405857bfd80e6668da

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 5511a0b33d80360690774b4528fec86cd6cb6a8e379ce4a03520ae0d81834dd1

ONX_KERNEL_MATERN_H_UNKNOWN__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 32ea62b18a7ae7fe03edb97e33517891f3e3ca5849df2e0f3ca5616445276a98

The switching subclass with L=floor(T/2) has RKHS drift <=2B(L-1)<=V_H and forces Omega(T).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: df5b1bffe4e1d8a097d5866aee64467bf574ec3005b97c06dd10d982ed78db19

S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: e8be3ec5daa1ac92d9a4f02d43b420dd45de389660b8f193b191cda29d8e14ee

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 52bd5f3d03badf80f7ab61b0ebd226fa4b122255c1293fd4530e227c9a66a3f4

S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 11bfa6b9ed4ee734dd28c9be2bac3da5c33248b90cdf6bb4efabde18694c05a9

ONX_KERNEL_MATERN_H_UNKNOWN__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 41293e4dee4a61f555ec6225cb15a428000f0bbe24707923627449a99062bff3

Any fixed feasible budget-independent policy has pathwise regret <=2BT.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 075ef9ec3318e1ec1ed0d0ce56a67afde62e5ded5e1247f38ee70046f3e8317d

Entire native domain.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: af51de60e2dccaa4cd3937bddd9cd658653c57da87cb4931c195b7d8af737ea2

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 64180dad0b952480e4556db086dc947fa9619bade9e8983948bd5b5165dc2b8c

For T>=4, L=floor(T/2)>=T/4, 2B(L-1)<=B(T-1)<=V_H, and sqrt(LT)>=T/2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: f983a71a4df421a1d4389d41bdb8f3ead0657eb26736119e692c639c74b97b27

Both drift endpoints B(T-1) and 2B(T-1) are included. The lower endpoint is sufficient, not an optimal phase transition.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 547a90f927e7abf843ef501024eb0b6480934d8d96b2c54b54c41df0b40b94c1

The source horizon threshold remains asymptotic; T>=4 alone is not asserted to activate its lower constant.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 21a4ae97e0dbdc764ce675fff671d04b49987683158ecaf2cde9bd1dc01e0ebc

T=1 forces V_H=0 and lies outside S. There is no zero-round member of the native N=T,T>=1 protocol.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/boundary_checks/4; canonical SHA-256: 7fd2ab1b128b219191bea508ea6384fc9265da80af46479413802096c71ccb11

d=1 and nu=d require no separate transfer; sigma=0 and nu<=1/2 are not adopted here.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 0e41cab3f0d8bbc766a8d93f602534af162ba943cc983aba59c92b7757e7ce7e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/0; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/1; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/2; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/3; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/4; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 0e41cab3f0d8bbc766a8d93f602534af162ba943cc983aba59c92b7757e7ce7e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/1; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/2; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/3; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/4; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 56412f147f56b0ae5a03fdde266b4f11bc2156ad3c88498fb9c272caff8aaaab

Theta(1) for fixed structural parameters; expected regret is Theta(T). N=T remains the observation budget.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: eef0c32eeae25190fd5a92c0c9125409029f25895c4bf3a92b082c1ab3daf966

R_T^*>=c(d,B,sigma,nu,ell)T on S for the source asymptotic threshold, with c>0.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 6a371f178d8b9438f1e1069111508a6035876bdbd61fa2cd9eec90134c80e902

No asymptotic order gap on S; exact lower constants and uniform structural dependence remain unspecified.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 242a439baa0b45f4dd48c222a72d0032ec5fceadff1c78ca5a01d23c74551d9c

R_T^*<=2BT on S, exactly and without logs.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 9452f7ea5733f1363eadffee7bd7d51c4f3e8a15d5d586413ea5c13e4375cab9

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: c6524300810cd443a4407e230467373293de1a98f0bc453858f4b5722248fefc

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: f1f195d66469b6a3c73b7a36b01ee8aeb061dac1eb26efa9b20ee72940a9467b

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: ba2e01b052f165087aecbcfcd05e7385be85530a7fdca54ed0a63f8d02f264bf

overlap

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 54e693b0399096a9b0248fbda33af96d37c2a698b28e7fcf9bc876b67d94832a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: fbf797516ed28061ea80ea0fc64191fd8b147e86557497fd56d5e202c04edff3

Both comparisons apply; the new bracket has matching linear order, without strengthening the old rates there. The recorded Theta(T) closure is conditional on the retained native proof, not a new independent verification of its source. No outside-W witness is claimed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 62d4382419a5e413af86236369d4f8168270f3b5f7820b5bf7471fa99cbad4e6

S intersect W. S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H. W = the unchanged frozen theorem window in /regimes/0 and /comparisons/0, including nu>1/2, fixed positive sigma, sufficiently large T, and the retained nondegenerate-drift/linear-scale guards.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: a2ac7c654bf74954b6a267ab63253f8fee4bcc4a8226856e3fd6f7dd6d81ff9e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: cbab71b363b34dbb8033e635b1efc9388b732259b28b8ac0139a41225cbe2d66

saturation_only_formal_cell

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 54e693b0399096a9b0248fbda33af96d37c2a698b28e7fcf9bc876b67d94832a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 05885bf94cd4db883768ddc465601ba265019e6630aa5e96f24a1202283da72c

Formal S minusW cell, possibly empty. Saturation is valid onS, but strict extra-domain coverage/nonemptiness outside symbolicW has not been proved. The recorded Theta(T) closure is conditional on the retained native proof, not a new independent verification of its source. No outside-W witness is claimed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: fb980e9bc9a464715a249495777346fd3aba46f6d0dddc8afd20cdaa5780ca3b

S minus W. S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 4970cc9359b8c62c4d05d9bdb2bac1778e9ed298aba88e8d2f564aa97071d4bb

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 36c20b3c8f1cb26e9880f32474bba6ca4042a6c069fc819f9f8bafc82aba0575

old_window

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 71e654594d969692b0b408d2ac96653c1171c43228c80c72afd5c1e80d522ce0

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 1996a7e4196038d2185b1517cc37b1c1788c2e9b7f04dadc1bec1dc9b79485c2

Conditional retention of the frozen bounds; no fresh recertification.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: c5df01b08213786e17041b0e7de4e4ebe07dda1d6f92c537b1384048a7c504fc

W minus S. W = the unchanged frozen theorem window in /regimes/0 and /comparisons/0, including nu>1/2, fixed positive sigma, sufficiently large T, and the retained nondegenerate-drift/linear-scale guards.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: a5bd58c2ec4f5031841e4cfe4f5109c903a16c9847f9e416bbe28ea0ca58e0f0

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: ef9670ac75858f70360100ba43d68692b8a287ac8864f9cf3f34c50c91bff22b

residual

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: aee2ee74ff4a40c3f3ee1156c991e513c57c97c21e9687bd1630cc9f30bf4357

Unassessed, not a claim that bounds are missing or the problem is open.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: e18d9198f1044d3fa0c32c5cbf727758a4826a5a08f382be627235a02f19923d

Native domain minus (W union S).

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: c10458b7e67805e0ce5be80c1d7382d7fd5842d469b7413a6ad09cad5dee2f20

The four cells S intersect W, S minus W, W minus S, and D minus (S union W) are disjoint and cover the native domain D by Boolean identities. W and S are intersected with D. S is feasible since B(T-1)<=2B(T-1), B>0,T>=4. The symbolic boundary of W is not converted into an invented numerical threshold. These Boolean cells do not certify nonemptiness of S minusW or a strict frontier advance.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 661b3300f78894fcd2bfbe0927ece9321682b7a665575c3cd048db247b3964bc

Outside W union S is unassessed, including uncovered finite horizons, vanishing/zero drift, zero noise and low smoothness. Source asymptotic horizon thresholds remain symbolic.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 532cad7c70919977fedac0c6161928d43bd9b6aa6a4773e0cf13fda69450c641

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: f2d158bb3d09e6178d493f14424fec4e94a5a7f2d1a504053afce355d7eba6d0

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: fd60fe726e7b35ddecf819d5c1d8af8706e832e715abafb3718ee3e13fc6586d

Retain the valid Theta(T) saturation comparison onS. This is explicit saturation registration, not a certified frontier/domain gain; onS intersectW old bounds already have the same order. Native impact, report and downstream counting must use this same qualification.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 0d54486b6165693ed7547afd83b0dd511b15092afa324a35e5b989ae1572c82b

matern_h_linear_saturation_v1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: d31067e6c7153ec07ed408a0168f577e37af70658e9cdb80d7602f87cddb3c0e

No strict improvement or strict domain extension established: W remains symbolic, so nonemptiness of S minusW is unproved.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 17acee8483f7e3cd5a0df199ecd4e48e92887f1d48a07e2417b3b7928a3a497f

Retain c1; add c2 with Omega(T)<=R_T^*<=2BT on S.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 4df3632424a86da8b5a06b66c34d43217614a54085215a15d5790db7cbce6ad4

Only c1, with its symbolic nondegenerate window W, was registered; no explicit saturation comparison independent of W.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: b5bf61fca2d23a86f9381668b40926452a94b780f815d735cdafa1c9d455fbf7

All old c1 formulas, guards and status; outside S no new bound.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: df5b1bffe4e1d8a097d5866aee64467bf574ec3005b97c06dd10d982ed78db19

S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 655d86d1494d34de6bbe05e03d0903a8fb26b5387b9b632f7db0ad238a0471c4

S itself is nonempty for sufficiently largeT,V_H=B(T-1), but this does not prove that the point is outsideW.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 58fce5e1d0df1097faaca9aee946f7e1d18e6303088b5a9a919af1fd787cb585

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: f599b480e2ec58cabc57631adb3d78da79d296daa77bed87dbc4080e61aa266a

Presentation support for retained c1 is separate from the source-backed new c2; it does not justify a changed old bound.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 71e654594d969692b0b408d2ac96653c1171c43228c80c72afd5c1e80d522ce0

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: c476ca3bbd6df1ef662249c87969824921f48362ff242cff8ccb09293314bbaa

matern_h_first_joint_annotation_v1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 713d7333c6d601b5bf8548461d5b9aea9087e69807d6b36f43cd7b7eefc12977

empty for scientific envelopes

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 46aa2d08c85c9b21b3c07eeda31120dc7ac1f75b2efecef79b19d3aee2219513

Identical scientific c1 data, with explicit parameter roles, candidate accounting and residual domain.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: fa44a45687708bb85a83ae2d430626c0ef759adf27ed2f92e0bc7f645d1a535f

Frozen c1 envelopes/guards/status.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 53b05b5ac4f8dbaa1c67ab176288323cc8b3e37969f35eb29df6301fed94fd5c

All c1 scientific data.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: cd10f8bdf6cae1d9a65c0f583dd2be71dec208851299ef067d0f9048848f8d61

Native domain for descriptive accounting; unchanged bounds adopted only on W.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: cc937ed32fcab9ba71531595b642ebda4ec326d57f0f53a67fc3ad6e72efed78

No patch modifies c1,b1,b2 or r1.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: eb8cbf14ccacabc324b3a2023aeb95984123e1ca1fe598b36621bfe27ba917db

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 0f897f8d73bd7a5a4d78841f54b2b785c7404f5afe17c4fddec688370def6612

Norm domination and the stated expectation conversion do not supply the hidden budget or prove a selector. Do not adopt its tuned rate.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: c41f7c158de60542b854cfba74ab3122bce9f393b80794969f9df69c505b9044

rperp_known_drift_rate_v1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: c85494cf3fff1dafdde3abc8b183f06a044f9a96cc8ddeb9306879994642ac73

empty under the native hidden-budget policy contract

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 35da2d84a18beebd060cc9685b0d92a689a8df450f3390d62595904491f71eaa

No added R-PERP term.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 813c944a1179cb2f3ff793effedfdb0390c6acf31be96eeb3ce578c1d3b6e6dc

Guarded c1 and proposed saturation c2.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 84c3a87a3b3ae9769aa5dde1c2f31b4c6c1e2c5f5c1fe0c1b36d060e1a4ecbfc

W union S

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 1fdb5a55585e050f19f3763b41ee7be528a67145655a0b04ee2c1767c6917e04

arXiv:2410.16052v1 Section 4 Theorem 3 and Section 5.2 Theorem 5 assume/tune to known uniform-norm drift.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: bbc835d95075a7e761c513c206321f580f457a4a66a1e24c866f54d1b75d6a81

Theorem 5 chooses H as a function of V_T; Section 4 explicitly distinguishes known from unknown V_T.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: fad5d5513e86800db4dd7c541066338c8bcd7aaab980ae750290df1f29f33922

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: fbb6d3d2e72398d6f56214e8ab7a6635aa75a117d0566e01ddd632892bc0e19b

Keep the supported fixed-structure linear saturation bracket and map its main code to optimal. Reclassify impact as explicit region registration; S minus the old symbolic W has not been proved nonempty, and the earlier witness only established membership of S. Preserve strict-domain-gain uncertainty in canonical data.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 0e34414168ccc44ceb851cec66fc33225f85b0227c022f39177b69932ef70f71

curated_feedback_ONX_KERNEL_MATERN_H_UNKNOWN_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

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

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: ef938d83fb8cbb303db3d00dbcf53fb234fafc89eb46fcfdea7834ffd3c587b7

Native q1/main/g1 is minimax expected cumulative dynamic regret of a causal randomized policy not given V_H, with oblivious functions in the normalized Matérn RKHS ball on [0,1]^d. Integer T>=1; 0<=V_H<=2B(T-1); B>0; integer d>=1; ell>0; nu>0; sigma>=0. Resource resource_6a63cfee9f has N=T played-point Gaussian observations and unrestricted computation. T,V_H vary jointly. Constants may depend on fixed d,B,sigma,nu,ell. gamma_T in the retained envelope is derived fixed-kernel information gain, not an independent coordinate.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: c263c1bf69bbe3e1ebcf10433af613c5af43f0bbd0ad2a3d0a1dcedc2351f23a

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 2dfa47e8061408644fb7c28ec53e2d0538726899f455cc50f103c8b738f25907

arXiv:2207.00908v1 interference-constrained beam alignment was exposed as metadata but its theorem/reduction remains unassessed.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: ec3766f124aa4c84354e6f74f9ab01a9baa39339aed57fa38e7fd26c898f7af8

Fixed-public-reset or budget-independent selector routes based on R-PERP Theorem 5 remain unassessed; its known-budget tuned rate is excluded.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 7d31a49a3bb5665e8bbc5320e3b73f5fd578a46d14b6fc3dee80b1adbe6f0b96

Assess the residual domain separately; this local update does not certify finite horizons, zero/vanishing drift, zero noise or nu<=1/2.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 92a99275b939fd611285ba1401e038ca5c9f39234dca1b0c69e8c814afc64e36

The retired broad query has 15 unrequested records outside the refined metadata scope; no exhaustive literature/correction search is claimed.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: fcce9d3f34c0ede66c1334f5916fcdb137fd1d4e76236821fcd72fdc0ebf5c34

Resolve the symbolic oldW and prove or refute nonemptiness of S minusW before any strict domain_extension/frontier claim. Current impact is saturation registration only.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 8b5ef7b8a055a7469386a8214227e33cc7c00abb50f1287c78d6e44a2022afb3

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 972513f697d289d25e242a54d8a76cdcf652fcd42ea73a267888df831047f982

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 5c974e4300842fec2372948266f9eb795579ddda56935144b466d30fc7a0176b

ONX_KERNEL_MATERN_H_UNKNOWN__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 2a72d77ce995a732bf77488c597e82463fb165dbeaaabc0a0ef4a5d0d4e1d002

Preserve the old Gaussian/expectation/grid/norm conversion without recertification.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: b429927951c876305a8a8030a27d2d3bef0606c2f0e5b42fc09a2d12af9a8c45

Unchanged frozen applicability conditions.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 2b426c2105b20a72061ed93efd7e67fadd826712d06e2e0fba94b69313d1dd76

Frozen /bounds/0 and /evidence/1; conditional retention.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 717130f36ff469de1fcbba750a26867afaed7493e23ebeb11d3701c583465060

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 6624bb5e735ccac999086c23bc139e0a15f39e1eb08fb1e73ee87a95d07c8a1b

ON_REV_SRC_KERNEL2023

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: bf225f2e4787e165f5a245e55bb71f55793511a8a605aefe07ca2c056ccf936d

W

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: dbb9ba149edd9c4ed0b7d649a812ebdf6981e0a4fa30ada14886ad6da1191d73

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 4336171618ec49a56737a878b09646883a03a04278d7ebbf4b28399ceb74bc02

ONX_KERNEL_MATERN_H_UNKNOWN__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 7dfca19d60b607b2d520877081513eab67f5792592dff195ae2df2b5ae0a891c

Preserve the known-to-unknown-budget lower transfer and stationary term.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: c508ee01824e0e0701d6587faf2acfefeee470e81f8299f5f73436b3993c9cdc

Unchanged positive-noise nondegenerate-drift window.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: bbd0cdd7a11716e8e23a70320d733808a06198a5f873538c070f2dab69c6b530

Frozen /bounds/1 and /evidence/0; conditional retention.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: b9b1cb1bb9b56669469bcd3eaf745121b51ff9f2beedd1b4ee066e91d649821e

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 819ab4e38678e9d775f96f16d78b3c773fd16600b024e2062d1bfe7f7925b1e4

ONX_SRC_RKHS2025

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: bf225f2e4787e165f5a245e55bb71f55793511a8a605aefe07ca2c056ccf936d

W

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 25f057fef8f41b48ed109f53dcf7290ee867814148d1306b31811b6998be15ba

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 5511a0b33d80360690774b4528fec86cd6cb6a8e379ce4a03520ae0d81834dd1

ONX_KERNEL_MATERN_H_UNKNOWN__main__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 4627bfcd4f7562a8fc100907fef00bec50605f1893915abc12f885ad552feac8

Choose L=floor(T/2); norm triangle inequality gives drift <=2B(L-1)<=V_H. Sample the block hard functions obliviously in advance. Preserve causal randomized policies, actions, outputs and T observations; no target switch promise or budget information is added.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: a0a879e1bfc9800cf84a227a436c883b1abe07b158678eb51a3b608f55c0f03b

Same Matérn RKHS ball/Gaussian observations/expected cumulative regret, with at most L-1 changes and L in {1,...,T}.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 1315b837785aa6afa75610ff7882ed0e713f0764287a9e1da8d5a8830551bb7c

SHA256 28d92cfa7793986045ce7c2f595da9c63b0d34e3fb4a6558f61d8788988374a1; PMLR 258 (2025), Theorem 1 Eq.(12), Appendix B.2/C.1 Eq.(24); read [13000,22000), [42100,43800), [43700,45900).

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: b9b1cb1bb9b56669469bcd3eaf745121b51ff9f2beedd1b4ee066e91d649821e

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: 819ab4e38678e9d775f96f16d78b3c773fd16600b024e2062d1bfe7f7925b1e4

ONX_SRC_RKHS2025

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: df5b1bffe4e1d8a097d5866aee64467bf574ec3005b97c06dd10d982ed78db19

S = fixed d>=1, B>0, sigma>0, nu>1/2, ell>0; sufficiently large integer T>=4; B(T-1)<=V_H<=2B(T-1). Constants and the sufficiently-large-T threshold may depend on the five fixed structural parameters, never on T or V_H.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 8cda4c6ebf4dcbfb2f6665df784815271fc4326260464202ec3feb5be12bfe93

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 11bfa6b9ed4ee734dd28c9be2bac3da5c33248b90cdf6bb4efabde18694c05a9

ONX_KERNEL_MATERN_H_UNKNOWN__main__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 92cc632221f7cd2bf0960880e3fa26ea11b3ba693c4feb88d8250013e9d63f9e

The retained premise |f_t(x)|<=B gives each reward gap <=2B, so one fixed feasible policy independent of V_H has expected cumulative regret <=2BT.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: be86d639b45543708f3c580bc5947c53268e2b8cb76ec8719a01b3f81da9f937

All native feasible parameters/functions.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: fb72dfdfb4b61dfa69d61bd47f4ea13727b60a3e82d0a6a6d482d32f415e536b

Completely read /common_specification, canonical hash 6ce47283209950b3485f863e1998378f510981a6f6d804a9f032c739d7309fbf.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 06387eb51da3856d2bd6b8f7e4021497e747aa1358afb629bf22b8bfab06b0bf

Valid throughout the native domain; adopted on S.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 40a239084a2c2dab4e2b758ba1f7d37b22393bd3b70047d118d7b44e34a13b14

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: fa5e390ece55c6b8e51ee91f48b354c5e9ac4ff51b7bb79b305cd73e7af0a2bc

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 8c42041c3d721fd9a7c249e43a89935601f6430ba09523a58b00f260883449ec

User-feedback-guided curator synthesis plus the explicitly recorded new primary-source reads. Previous partial searches and retained-source recertification limits persist; neither a new exhaustive search nor a completed native approval is claimed.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 5f0b0116e8d8217208b5a3da63eefd671401a519fad77f7b9d339c58be8a5003

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: cf70238546466b1dca8e234d2f7f00b0e7280d0e6b905f53cd81c4f801fa511b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 0f16c1e71ce4014687553a2db6acc17ed54f7a8bf58093102b1e8cee87ac14b3

Retained b3/b4 give matching Theta(T) on S; b1/b2 keep W only. On S intersect W the old envelope already has linear order, so there is no proved strict gain. S minus W remains potentially empty. The correction does not alter any rate or source guard; native saturation c2 is explicitly registered optimal, with all old retention/source limitations intact. ONX_KERNEL_MATERN_H_UNKNOWN__main__b1: included — Retain the frozen upper envelope and conversion guards conditionally.; ONX_KERNEL_MATERN_H_UNKNOWN__main__b2: included — Retain the frozen lower/stationary terms with positive-noise and linear-scale guards.; ONX_KERNEL_MATERN_H_UNKNOWN__main__b3: dominated — On S intersect W, V_H=Theta(T) for fixed B, so both old lower branches already have Omega(T) order. No new active c1 reference.; ONX_KERNEL_MATERN_H_UNKNOWN__main__b4: dominated — The exact 2BT cap already occurs in b1's guarded min. No new active c1 reference.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 514f398c80631a253fc39334ea47f9973848b375b3cb56d5e97a5d615bfe700d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 5c974e4300842fec2372948266f9eb795579ddda56935144b466d30fc7a0176b

ONX_KERNEL_MATERN_H_UNKNOWN__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 4336171618ec49a56737a878b09646883a03a04278d7ebbf4b28399ceb74bc02

ONX_KERNEL_MATERN_H_UNKNOWN__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 5511a0b33d80360690774b4528fec86cd6cb6a8e379ce4a03520ae0d81834dd1

ONX_KERNEL_MATERN_H_UNKNOWN__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 11bfa6b9ed4ee734dd28c9be2bac3da5c33248b90cdf6bb4efabde18694c05a9

ONX_KERNEL_MATERN_H_UNKNOWN__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 71e654594d969692b0b408d2ac96653c1171c43228c80c72afd5c1e80d522ce0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 890f5877cbad4f519ef874c9b79fe66020f6d4496a6814816a3f3461b0ea6624

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: a1c319ea099238aa167bdb73d884f90632299dd162a2f64e5d85f216706b96d0

Retained b3/b4 give matching Theta(T) on S; b1/b2 keep W only. On S intersect W the old envelope already has linear order, so there is no proved strict gain. S minus W remains potentially empty. The correction does not alter any rate or source guard; native saturation c2 is explicitly registered optimal, with all old retention/source limitations intact. ONX_KERNEL_MATERN_H_UNKNOWN__main__b1: dominated — Only applicable on S intersect W; b4 already supplies its linear cap. Not adopted outside W.; ONX_KERNEL_MATERN_H_UNKNOWN__main__b2: dominated — Only applicable on S intersect W; either dynamic branch is Omega(T) there. Not adopted outside W.; ONX_KERNEL_MATERN_H_UNKNOWN__main__b3: included — The switching subclass with L=floor(T/2) has RKHS drift <=2B(L-1)<=V_H and forces Omega(T).; ONX_KERNEL_MATERN_H_UNKNOWN__main__b4: included — Any fixed feasible budget-independent policy has pathwise regret <=2BT.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 514f398c80631a253fc39334ea47f9973848b375b3cb56d5e97a5d615bfe700d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 5c974e4300842fec2372948266f9eb795579ddda56935144b466d30fc7a0176b

ONX_KERNEL_MATERN_H_UNKNOWN__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 4336171618ec49a56737a878b09646883a03a04278d7ebbf4b28399ceb74bc02

ONX_KERNEL_MATERN_H_UNKNOWN__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 5511a0b33d80360690774b4528fec86cd6cb6a8e379ce4a03520ae0d81834dd1

ONX_KERNEL_MATERN_H_UNKNOWN__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 11bfa6b9ed4ee734dd28c9be2bac3da5c33248b90cdf6bb4efabde18694c05a9

ONX_KERNEL_MATERN_H_UNKNOWN__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 54e693b0399096a9b0248fbda33af96d37c2a698b28e7fcf9bc876b67d94832a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 8eae3738dc29b12f676bc8d9f9c073e11dce1560aba16b8ee59c506d9c01cd8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: a5bbf6633f794b5b5cc70b4b41ff2d5461816bb0a977cfbfd335ce0dd1ab09e1

ONX_KERNEL_MATERN_H_UNKNOWN__main__p1

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 53f966e7cb13e08552fb7abce179da69e0c5f8cf8120831248d463607a564373

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: d0167f548742ead3d895787ec442b4a84beeb280ebe70d01f9a7603611e9c56f

remaining-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 2dfa47e8061408644fb7c28ec53e2d0538726899f455cc50f103c8b738f25907

arXiv:2207.00908v1 interference-constrained beam alignment was exposed as metadata but its theorem/reduction remains unassessed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: cd42dfc8bfe0349e792c632246d0674d57f98befcf1f0184576017bb0735335b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: a4b3d9806c41184784f257b17680c859184105b903c13a4dc473b5d4a38646ea

remaining-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: ec3766f124aa4c84354e6f74f9ab01a9baa39339aed57fa38e7fd26c898f7af8

Fixed-public-reset or budget-independent selector routes based on R-PERP Theorem 5 remain unassessed; its known-budget tuned rate is excluded.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 05ecaa4229ddb0c8467ba9ff93a73b6f662990482937239d763f54f28b9eeb98

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 3e14526e35b394fe370a6fc3dd84e97e336771629d764f97e1112f9be119d23a

remaining-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 7d31a49a3bb5665e8bbc5320e3b73f5fd578a46d14b6fc3dee80b1adbe6f0b96

Assess the residual domain separately; this local update does not certify finite horizons, zero/vanishing drift, zero noise or nu<=1/2.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: e0ff2f4fdd0a59a6389eedf9870d1ab7488673794cc9ab7d835ccd5d105a5e21

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 2ad76a816cfedf1ea354b21e9948710836a980becdf5124dd84ab11a1a2b3afe

remaining-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 92a99275b939fd611285ba1401e038ca5c9f39234dca1b0c69e8c814afc64e36

The retired broad query has 15 unrequested records outside the refined metadata scope; no exhaustive literature/correction search is claimed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 6ef34d0ec7074b55bba2554141d63b6ef70a2d4b05ed1ded12a53ed564c71ac5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b911f50d8b73b3d7f08b74d550e9f8050c353f01c4f9f7621905110a4d9b0067

Retained unresolved obligation. This candidate does not claim that registered-envelope closure finishes discovery, source recertification or all target regimes.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 8a1018ad75fb3da4cc08ea1e079513debdaa4af5b56952b5988e43572540acde

remaining-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: fcce9d3f34c0ede66c1334f5916fcdb137fd1d4e76236821fcd72fdc0ebf5c34

Resolve the symbolic oldW and prove or refute nonemptiness of S minusW before any strict domain_extension/frontier claim. Current impact is saturation registration only.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 1b2a8b398c4d157d61f81ca6193e1ba3a63c211e9112f4813c032e73c6c08fb8

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: e81b277648323ab1d94ebccc6c2bb35fd8f0a7ba3d68e34daab0f46054f6cdb8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: aa6f52e24f33b1e7c782131bf6a0ae42a3a8815c63f0a462cc45f5ecd4effff5

ONX_KERNEL_MATERN_H_UNKNOWN__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 8044820adcf9a73ae90c4b6165883f8ab0b480f18fc0fa766861e1ba0c35b848

ONX_KERNEL_MATERN_H_UNKNOWN__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: ca2e122318f1822d9839c4f859f80a5adbb93ec5ac45b1ae392da1a7f6973fb0

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 0e41cab3f0d8bbc766a8d93f602534af162ba943cc983aba59c92b7757e7ce7e

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native item 4

Native pointer: /joint_analysis/target/allowed_constant_dependencies/3; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native item 5

Native pointer: /joint_analysis/target/allowed_constant_dependencies/4; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 0f312fb9ed196ecd3d74c17c74179c1db54e67f48131f2f2a8af1a4d3508beef

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 15dd24a7978859271fb001237c07a1f13bc0e4f3f2e6e1c7067cb4ee24f6b0af

/views/0/guarantees/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 46e5c7866bd3a78de40a01f2bc8e126870f3a87a36039493bc32dc77ea786768

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 337c03f86ec7045090718e95eb9330322db25a49e3cbe26bc084fc63954bfedd

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 84ac196dc797779d6c0bb8d682a0e7adf0cf72f0007ace96310042f98bdb671a

Integer d>=1, fixed.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 600e680374dc51460ebcbc9f1883e7fa5828dac0369a5af3337ca4d2126c47c9

ONX_KERNEL_MATERN_H_UNKNOWN_p_6e898943e7

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: 364d82635da85b91f30dd9bd8975995fcec49ed4689b71c574c0a13feef62651

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 8cdae5a97b04395627a6da9f252a003b1c9b040fe5102c8cf6c8dfbee1335a0f

B>0, fixed.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: 858d90449beb6bf858cc9ca351aafed257c68e4e05593e25fbd9028060d4b6de

ONX_KERNEL_MATERN_H_UNKNOWN_p_56ede73029

#### Native item 3

Native pointer: /joint_analysis/target/fixed_parameters/2; canonical SHA-256: b75b47ae14402dd2a5d2babe44ff9fc0fadea902aed83207db8260e0742da764

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/2/domain; canonical SHA-256: 16a27348a695638bbf3a5e8d7d08c79b3a16e0789530eaa7d432a773c0a69fad

sigma>=0 natively; W and S require fixed sigma>0.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/2/parameter_ref; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/2/symbol; canonical SHA-256: 6ca1e3308c6a5d68e9a05414fb874287f284e2020a256bff1ed0cfd98e1f93ef

ONX_KERNEL_MATERN_H_UNKNOWN_p_242d5d68ef

#### Native item 4

Native pointer: /joint_analysis/target/fixed_parameters/3; canonical SHA-256: e86f30f643ade4801a6980349205bd22cbca5134c2fcbad2bf02fd308a26e703

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/3/domain; canonical SHA-256: 011b50dd8a1432845cf4a45fd743be47bffaa26eb03e47f60dbbc9fb51c56177

nu>0 natively; W and S require fixed nu>1/2.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/3/parameter_ref; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/3/symbol; canonical SHA-256: a558053ecdb9d17b968e9b5448be1f91ca0eb10422731f41f56c9fef682782ca

ONX_KERNEL_MATERN_H_UNKNOWN_p_6c53b3d62c

#### Native item 5

Native pointer: /joint_analysis/target/fixed_parameters/4; canonical SHA-256: 112b1cf434ec6dd82b8993629c84a8c1fe882a2087511e5df61f7c9f0937d1ac

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/4/domain; canonical SHA-256: cdc132e20e4f759f767a81905a0856b87b12301e141666e1daa2786f80708671

ell>0, fixed.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/4/parameter_ref; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/4/symbol; canonical SHA-256: c03689ee2585a1442a94596900d0bc5545fec09b43e2749cb19f55d286e042ad

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c740b7b6a

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: ef938d83fb8cbb303db3d00dbcf53fb234fafc89eb46fcfdea7834ffd3c587b7

Native q1/main/g1 is minimax expected cumulative dynamic regret of a causal randomized policy not given V_H, with oblivious functions in the normalized Matérn RKHS ball on [0,1]^d. Integer T>=1; 0<=V_H<=2B(T-1); B>0; integer d>=1; ell>0; nu>0; sigma>=0. Resource resource_6a63cfee9f has N=T played-point Gaussian observations and unrestricted computation. T,V_H vary jointly. Constants may depend on fixed d,B,sigma,nu,ell. gamma_T in the retained envelope is derived fixed-kernel information gain, not an independent coordinate.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: fe58483b3d1d013ac8d273fc4a9a432074f63babe3aedd4924278f170539b095

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: d505e7a82ea05afacc4ca667b614623afd9652305e08984958c84e9b659a218c

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c093224ff

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: a98418062bac84e8c131466586db121240e1efa0905c1e9d9daf1f42338b66a6

ONX_KERNEL_MATERN_H_UNKNOWN_p_4ba56f91f5

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: fe58483b3d1d013ac8d273fc4a9a432074f63babe3aedd4924278f170539b095

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: d505e7a82ea05afacc4ca667b614623afd9652305e08984958c84e9b659a218c

ONX_KERNEL_MATERN_H_UNKNOWN_p_0c093224ff

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: a98418062bac84e8c131466586db121240e1efa0905c1e9d9daf1f42338b66a6

ONX_KERNEL_MATERN_H_UNKNOWN_p_4ba56f91f5

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Xu Cai; Jonathan Scarlett. Lower Bounds for Time-Varying Kernelized Bandits. 2025. AISTATS 2025, PMLR 258.

https://raw.githubusercontent.com/mlresearch/v258/main/assets/cai25a/cai25a.pdf

[2] Kihyuk Hong; Yuhang Li; Ambuj Tewari. An Optimization-based Algorithm for Non-stationary Kernel Bandits without Prior Knowledge. 2023. AISTATS2023, PMLR206:3048–3085.

https://proceedings.mlr.press/v206/hong23b.html
