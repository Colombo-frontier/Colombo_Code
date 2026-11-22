# Stochastic convex Lipschitz minimization: directional moment bounds and a composite objective; high-probability risk; stochastic full subgradients

**Setting ID.** `SO_FO_S01_direction_HP`

Single-objective optimization

Fixed-budget high-probability objective risk under separate norm and directional heavy-tail moments. Source-scoped all-budget envelopes are recorded for an explicitly fixed query-dependent fresh kernel. High-dimensional saturation and statistical regimes match; finite-budget transients remain quantified, and no matching source lower is imported below its dimension or outside its confidence window.

**Status.** Other quantified gap; Bounds missing

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; stochastic model: Directional moment noise; structure: Composite

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Failure probability parameter explicitly declared; mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}F(x)$$

The complete objective is $F=f+h$. The properties and Oracle interfaces of the two terms are specified separately.

### Admissible model

The objective is $f+h$. The function $f$ is convex and $L$-Lipschitz; $h$ is public, proximable, and $\mu$-strongly convex, with $\mu=0$ allowed. A minimizer lies within distance $R$ of $x_0$. The centered noise norm has $\alpha$th moment at most $\sigma^\alpha$, and every unit-direction projection has $\alpha$th moment at most $\sigma_{\mathrm{dir}}^\alpha$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Write $F=f+h$ and $F^\star=\inf_{x\in\mathbb R^d}F(x)$. The public proximal term $h$ is $\mu$-strongly convex; when $\mu=0$, only convexity is required. The directional centered-moment condition is $\mathbb E_t|\langle u,G_t-\mathbb E_tG_t\rangle|^\alpha\le\sigma_{\mathrm{dir}}^\alpha$ for every unit vector $u$.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad L,R>0,\quad\mu\ge0,\quad0<\sigma_{\rm dir}\le\sigma,\quad1<\alpha\le2,\quad0<\delta<1/2,\quad T\in\mathbb{N}_{\ge1}$$

The public proximal term is proper, closed and convex, and its exact proximal map is available for every positive proximal parameter. It is part of the admissible instance class; the minimax lower bound is not asserted for every arbitrarily prescribed fixed nonquadratic regularizer.

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \delta,\ T,\ x_0$.

Public upper bounds: $L,\ R,\ \sigma,\ \sigma_{\rm dir}$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$. Access to the composite term $h$, including public information and proximal operations, is specified by the interface below.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full subgradients:

$$G_t,\quad \mathbb{E}_tG_t\in\partial f(x_t),\quad\mathbb{E}_t\|G_t-\mathbb{E}_tG_t\|^\alpha\le\sigma^\alpha$$

The instance fixes a query-dependent response kernel K_x before interaction. Given the query x_t, each raw response is a fresh draw from K_{x_t}, independent of the preceding history and private randomness conditional on x_t. Repeated calls at a frozen query are independent copies of the same kernel. Its mean belongs to the subdifferential of f at that query, and both centered moment bounds hold uniformly over queries. Samples cannot be reused across points. A raw response discarded by rejection or used in a batch still costs one call.

The exact proximal map of the public function $h$ is available at zero query cost.

The fixed-kernel interpretation is made explicit for source compatibility. No equivalence to the broader class of history-dependent response kernels is asserted.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,x)=F(x)-F^\star,\qquad F=f+h$$

$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

Every raw oracle draw is counted, including rejected observations. The source algorithm may use unrestricted internal computation; no polynomial arithmetic or storage bound follows from the oracle bound.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\mathcal{R}_{T,\delta}=\inf_{A:N_A\le T}\inf\{r\ge0:\sup_{I,\mathcal{O}}\Pr(\ell(I,A^{\mathcal{O}})>r)\le\delta\}$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

The budget-to-risk curve is $\mathcal R_{T,\delta}=\inf_{A:N_A\le T}\inf\{r\ge0:\sup_{I,\mathcal O}\Pr(\ell(I,A^{\mathcal O})>r)\le\delta\}$. The budget $T$ is fixed, and the comparison concerns high-probability error. A risk rate is not a query-complexity rate.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f,h,F$: Smooth or Lipschitz term, convex proximal term, and complete objective

$$F=f+h$$

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f(x)=\{g:f(u)\ge f(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f\}$$

$\operatorname{prox}_{\eta h}$: Proximal map of $h$, either public or obtained through the declared interface **Domain:** $\eta>0,\ v\in\mathbb{R}^d$.

$$\operatorname{prox}_{\eta h}(v)=\arg\min_u\{h(u)+\|u-v\|_2^2/(2\eta)\}$$

$\operatorname{dom}h$: Effective domain of $h$

$$\operatorname{dom}h=\{x:h(x)<+\infty\}$$

$G_t$: $t$th full stochastic gradient or subgradient observation

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$\mathcal{R}_{T,\delta}$: Minimax quantile risk at budget $T$ and failure probability $\delta$; defined in the guarantee

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\mu$: Lower bound on the strong-convexity modulus of the public proximal term $h$; zero permits a merely convex proximal term **Domain:** $\mu\ge0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\sigma_{\rm dir}$: Centered-moment scale in an arbitrary unit direction. **Domain:** $0<\sigma_{\rm dir}\le\sigma$.

$\delta$: Allowed failure probability; expected-error and probability contracts are kept distinct. **Domain:** $0<\delta<1/2$.

$T$: Integer budget in the native budget-risk theorem. **Domain:** $T\ge1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$\Pr,\mathbb{P}$: Event probability after the instance and admissible response law are fixed

$q$: Heavy-tail statistical exponent.

$$q=1-1/\alpha$$

$e$: Ratio of norm and directional moment scales; e need not equal d.

$$e=\sigma^2/\sigma_{\rm dir}^2$$

$\ell$: Confidence logarithm, kept explicitly.

$$\ell=\log(3/\delta)$$

$A$: Heavy-tail amplitude without the confidence term.

$$A=\sigma_{\rm dir}e^q$$

$u_T$: Pure heavy-tail amplitude.

$$u_T=\sigma_{\rm dir}((e+\ell)/T)^q$$

$w_T$: Statistical amplitude, retaining the finite-variance term.

$$w_T=\sigma/\sqrt T+u_T$$

$a_T$: Deterministic and confidence transients in the upper amplitude.

$$a_T=L/\sqrt T+L\ell/T$$

$v_T$: Full upper amplitude.

$$v_T=a_T+w_T$$

$v_T^{(0)}$: Upper amplitude at source failure probability delta_0=1/20.

$$v_T^{(0)}=L/\sqrt T+L\log(60)/T+\sigma/\sqrt T+\sigma_{\rm dir}((e+\log(60))/T)^q$$

$\mathcal H_{\mu,R}(z)$: Curvature and initialization envelope. **Domain:** $z\ge0$.

$$\mathcal H_{\mu,R}(z)=\max_{0\le r\le R}(zr-\mu r^2/2)=\begin{cases}Rz,&\mu=0,\\z^2/(2\mu),&\mu>0,\ z\le\mu R,\\Rz-\mu R^2/2,&\mu>0,\ z\ge\mu R.\end{cases}$$

$c_\alpha,C_\alpha,C_{\alpha,C_0}$: Positive constants depending only on the displayed subscripts. No uniformity as alpha tends to one is asserted. **Domain:** Positive.

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget risk

$$
\mathcal R_{T,\delta}=\inf_{\mathcal A:\,N_{\mathcal A}\le T\ {\rm a.s.}}\inf\{r\ge0:\sup_{I,\mathcal O}\Pr(F_I(\widehat x_{\mathcal A}^{\mathcal O})-F_I^\star>r)\le\delta\}
$$

**Definition.** Error risk under the prescribed fixed budget

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Fixed-budget high-probability risk: the smallest loss threshold whose failure probability is at most delta uniformly over admissible instances and the fixed query-dependent kernels. The probability includes private and oracle randomness. The budget is an almost-sure cap on raw calls. This quantity is not expected loss.

### R1 - Native confidence values outside the adopted source lower range

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $1/10\le\delta<1/2$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
C_\alpha\mathcal H_{\mu,R}(\min\{L,v_T^{(0)}\})
$$

**Gap or comparison.** Upper follows by running at delta_0=1/20. No target lower for delta>=1/10 is imported here.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R2 - Upper bound below the source lower-bound dimension threshold

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$ and $d<\lceil e\rceil$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C_\alpha\mathcal H_{\mu,R}(\min\{L,v_T\})
$$

**Gap or comparison.** The cited lower requires d>=ceil(e); no dimension-uniform matching claim is made.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R3 - Saturated statistical amplitude

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T\ge L$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B5

$$
\Omega_{\alpha}\!\left(\mathcal H_{\mu,R}(L)\right)
$$

**Upper bound.** B4

$$
O_{\alpha}\!\left(\mathcal H_{\mu,R}(L)\right)
$$

**Gap or comparison.** $\Theta_\alpha(1)$ multiplicative ratio; this is a nonzero saturated risk, not zero query complexity.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R4 - General convex pure heavy-tail regime

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu=0$ and $a_T+\sigma/\sqrt T\le C_0u_T$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B7

$$
\Omega_{\alpha,C_0}\!\left(R(A+\sigma_{\rm dir}\ell^q)/T^q\right)
$$

**Upper bound.** B6

$$
O_{\alpha,C_0}\!\left(R(A+\sigma_{\rm dir}\ell^q)/T^q\right)
$$

**Gap or comparison.** $\Theta_{\alpha,C_0}(1)$ multiplicative ratio.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R5 - Strongly convex pure heavy-tail quadratic regime

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T+\sigma/\sqrt T\le C_0u_T$, and $u_T\le\mu R$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B9

$$
\Omega_{\alpha,C_0}\!\left((A^2+\sigma_{\rm dir}^2\ell^{2q})/(\mu T^{2q})\right)
$$

**Upper bound.** B8

$$
O_{\alpha,C_0}\!\left((A^2+\sigma_{\rm dir}^2\ell^{2q})/(\mu T^{2q})\right)
$$

**Gap or comparison.** $\Theta_{\alpha,C_0}(1)$ multiplicative ratio.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R6 - General convex full statistical regime

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu=0$, $a_T\le C_0w_T$, and not $a_T+\sigma/\sqrt T\le C_0u_T$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B11

$$
\Omega_{\alpha,C_0}\!\left(Rw_T\right)
$$

**Upper bound.** B10

$$
O_{\alpha,C_0}\!\left(Rw_T\right)
$$

**Gap or comparison.** $\Theta_{\alpha,C_0}(1)$ multiplicative ratio.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R7 - Strongly convex full statistical quadratic regime

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T\le C_0w_T$, $w_T\le\mu R$, and the complete pure heavy-tail quadratic predicate is false.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B13

$$
\Omega_{\alpha,C_0}\!\left(w_T^2/\mu\right)
$$

**Upper bound.** B12

$$
O_{\alpha,C_0}\!\left(w_T^2/\mu\right)
$$

**Gap or comparison.** $\Theta_{\alpha,C_0}(1)$ multiplicative ratio.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R8 - Strongly convex statistical transition regime

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T\le C_0w_T$, $w_T>\mu R$, and the complete pure heavy-tail quadratic predicate is false.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Optimal

**Lower bound.** B15

$$
\Omega_{\alpha,C_0}\!\left(\mathcal H_{\mu,R}(w_T)\right)
$$

**Upper bound.** B14

$$
O_{\alpha,C_0}\!\left(\mathcal H_{\mu,R}(w_T)\right)
$$

**Gap or comparison.** $\Theta_{\alpha,C_0}(1)$ multiplicative ratio.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

### R9 - Unclosed finite-budget transient dependence

**Region.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $a_T>C_0w_T$.

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Other quantified gap

**Lower bound.** B2

$$
c_\alpha\mathcal H_{\mu,R}(\min\{L,w_T\})
$$

**Upper bound.** B1

$$
C_\alpha\mathcal H_{\mu,R}(\min\{L,v_T\})
$$

**Gap or comparison.** The recorded ratio is $O_\alpha(\mathcal H_{\mu,R}(\min\{L,v_T\})/\mathcal H_{\mu,R}(w_T))$, at most $O_\alpha((1+a_T/w_T)^2)$. This row does not assert matching deterministic transients, a uniform polynomial gap, or a full-literature optimum.

**Comparison argument.** The cited source statement, the explicit target-class transfer and local envelope algebra support exactly this row; no blanket theorem-proof certification is asserted.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Whole-space specialization with the explicitly fixed query-dependent fresh kernel and public exact prox; no function values or reusable samples.

**Guarantee mapping.** Identical high-probability loss threshold under the fixed raw-call cap; no expectation-to-probability conversion.

**Resource mapping.** Every raw sample is one call, including rejected observations, initialization, batches and localization.

### B1 - Source mixed-moment optimization and localization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
C_\alpha\mathcal H_{\mu,R}(\min\{L,v_T\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$.

**Constants.** Only alpha; no dependence on d, L, R, mu, sigma, sigma_dir, delta or T is hidden.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Theorem 2.2

All-budget upper envelope and a high-dimensional lower envelope, with explicit deterministic transients.

Upper holds in every finite dimension. Lower requires d>=ceil(e); its whole-space quadratic-regularizer hard instances are admitted here. Delta is below 1/10.

This record does not claim an independent verification of the full paper proof.

### B2 - Source adaptive testing lower construction

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha\mathcal H_{\mu,R}(\min\{L,w_T\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$ and $d\ge\lceil e\rceil$.

**Constants.** Only alpha; no dependence on d, L, R, mu, sigma, sigma_dir, delta or T is hidden.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Theorem 2.2

All-budget upper envelope and a high-dimensional lower envelope, with explicit deterministic transients.

Upper holds in every finite dimension. Lower requires d>=ceil(e); its whole-space quadratic-regularizer hard instances are admitted here. Delta is below 1/10.

This record does not claim an independent verification of the full paper proof.

### B3 - Source upper at delta_0=1/20

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
C_\alpha\mathcal H_{\mu,R}(\min\{L,v_T^{(0)}\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $1/10\le\delta<1/2$.

**Constants.** Only alpha; no dependence on d, L, R, mu, sigma, sigma_dir, delta or T is hidden.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_confidence_transfer_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Theorem 2.2

All-budget upper envelope and a high-dimensional lower envelope, with explicit deterministic transients.

Upper holds in every finite dimension. Lower requires d>=ceil(e); its whole-space quadratic-regularizer hard instances are admitted here. Delta is below 1/10.

This record does not claim an independent verification of the full paper proof.

### B4 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
O_{\alpha}\!\left(\mathcal H_{\mu,R}(L)\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T\ge L$.

**Constants.** Only alpha; no dependence on d, L, R, mu, sigma, sigma_dir, delta or T is hidden.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Theorem 2.2

All-budget upper envelope and a high-dimensional lower envelope, with explicit deterministic transients.

Upper holds in every finite dimension. Lower requires d>=ceil(e); its whole-space quadratic-regularizer hard instances are admitted here. Delta is below 1/10.

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B5 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\alpha}\!\left(\mathcal H_{\mu,R}(L)\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T\ge L$.

**Constants.** Only alpha; no dependence on d, L, R, mu, sigma, sigma_dir, delta or T is hidden.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Theorem 2.2

All-budget upper envelope and a high-dimensional lower envelope, with explicit deterministic transients.

Upper holds in every finite dimension. Lower requires d>=ceil(e); its whole-space quadratic-regularizer hard instances are admitted here. Delta is below 1/10.

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B6 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
O_{\alpha,C_0}\!\left(R(A+\sigma_{\rm dir}\ell^q)/T^q\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu=0$ and $a_T+\sigma/\sqrt T\le C_0u_T$.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.2; Theorem 2.1

Pure heavy-tail rates under nonsaturation, domination and, for strong convexity, the quadratic-branch guard.

Keep a_T+sigma/sqrt(T)<=C0*u_T and u_T<=L. The strong branch also requires u_T<=mu*R. Our disjoint displayed rows use the sufficient restriction w_T<L.

This record does not claim an independent verification of the full paper proof.

### B7 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\alpha,C_0}\!\left(R(A+\sigma_{\rm dir}\ell^q)/T^q\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu=0$ and $a_T+\sigma/\sqrt T\le C_0u_T$.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.2; Theorem 2.1

Pure heavy-tail rates under nonsaturation, domination and, for strong convexity, the quadratic-branch guard.

Keep a_T+sigma/sqrt(T)<=C0*u_T and u_T<=L. The strong branch also requires u_T<=mu*R. Our disjoint displayed rows use the sufficient restriction w_T<L.

This record does not claim an independent verification of the full paper proof.

### B8 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
O_{\alpha,C_0}\!\left((A^2+\sigma_{\rm dir}^2\ell^{2q})/(\mu T^{2q})\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T+\sigma/\sqrt T\le C_0u_T$, and $u_T\le\mu R$.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.2; Theorem 2.1

Pure heavy-tail rates under nonsaturation, domination and, for strong convexity, the quadratic-branch guard.

Keep a_T+sigma/sqrt(T)<=C0*u_T and u_T<=L. The strong branch also requires u_T<=mu*R. Our disjoint displayed rows use the sufficient restriction w_T<L.

This record does not claim an independent verification of the full paper proof.

### B9 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\alpha,C_0}\!\left((A^2+\sigma_{\rm dir}^2\ell^{2q})/(\mu T^{2q})\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T+\sigma/\sqrt T\le C_0u_T$, and $u_T\le\mu R$.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.2; Theorem 2.1

Pure heavy-tail rates under nonsaturation, domination and, for strong convexity, the quadratic-branch guard.

Keep a_T+sigma/sqrt(T)<=C0*u_T and u_T<=L. The strong branch also requires u_T<=mu*R. Our disjoint displayed rows use the sufficient restriction w_T<L.

This record does not claim an independent verification of the full paper proof.

### B10 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
O_{\alpha,C_0}\!\left(Rw_T\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu=0$, $a_T\le C_0w_T$, and not $a_T+\sigma/\sqrt T\le C_0u_T$.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B11 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\alpha,C_0}\!\left(Rw_T\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu=0$, $a_T\le C_0w_T$, and not $a_T+\sigma/\sqrt T\le C_0u_T$.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B12 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
O_{\alpha,C_0}\!\left(w_T^2/\mu\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T\le C_0w_T$, $w_T\le\mu R$, and the complete pure heavy-tail quadratic predicate is false.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B13 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\alpha,C_0}\!\left(w_T^2/\mu\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T\le C_0w_T$, $w_T\le\mu R$, and the complete pure heavy-tail quadratic predicate is false.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B14 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Deterministic adaptive policy given the observed oracle samples: Appendix A.3 uses known-density means and deterministic internal optimization; proximal conversion, rejection decisions and localization use returned data. Oracle observations remain stochastic. This witness is admissible in the randomized-allowed target view.

$$
O_{\alpha,C_0}\!\left(\mathcal H_{\mu,R}(w_T)\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T\le C_0w_T$, $w_T>\mu R$, and the complete pure heavy-tail quadratic predicate is false.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

### B15 - Source theorem plus explicit target specialization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_{\alpha,C_0}\!\left(\mathcal H_{\mu,R}(w_T)\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00260v2)

**Conditions.** All native parameters: $d\in\mathbb N_{\ge1}$, $L,R>0$, $\mu\ge0$, $0<\sigma_{\rm dir}\le\sigma$, $1<\alpha\le2$, $T\in\mathbb N_{\ge1}$, $0<\delta<1/2$; $C_0>0$ is fixed independently of them. Additionally $0<\delta<1/10$, $d\ge\lceil e\rceil$, and $w_T<L$. Also $\mu>0$, $a_T\le C_0w_T$, $w_T>\mu R$, and the complete pure heavy-tail quadratic predicate is false.

**Constants.** Only alpha and the fixed C0.

**Local argument.** SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122, SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.1; Model and minimax risk definition

Fixed-kernel fresh subgradients; two centered moment bounds; public exact prox; high-probability fixed-budget objective risk.

Use X=R^d. Symbols map as source (G,D,L,s,p)=(target L,R,sigma,sigma_dir,alpha).

This record does not claim an independent verification of the full paper proof.

**Source location.** [1](https://arxiv.org/html/2610.00260v2) Section 2.3; Corollary 2.3 and following quadratic specialization

Matching saturation and statistical-envelope regimes; finite-variance term is retained.

Keep d>=ceil(e) and either w_T>=L or a_T<=C0*w_T. Strong quadratic formula additionally uses w_T<=mu*R.

This record does not claim an independent verification of the full paper proof.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 919f1babb27880b7791ced63c6aef9769b39444af84f2e84b1568ab75f449b9a

### Native proof: SO_FO_S01_direction_HP__randomized__probability__proof_source_transfer_20261122

Native pointer: /proofs/0; canonical SHA-256: 9e3948394cc2645b1cd3c9513ffdc12296dfb49d08f111c74429e1a80d90ae84

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: ca2a64450797a9084e45ab3ebba2b1fff403b256de86bc83092f32f79488be4c

local_applicability_derivation

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: c4f25f1790dd9f12e784d3607e501fad969ba32f87bed8e8e274885477be630b

Source-to-target class and symbol map

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 32a43d815202b7f6933e4f61b648fd36275c9b527ba02495683a71422c0a8ed4

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 10666aff4da11b0d19e83140a77e83d1bc6672d83f46e3f28322c8f5e7268888

SO_SRC_2610_00260v2

#### Native field: evidence_refs

Native pointer: /proofs/0/evidence_refs; canonical SHA-256: b2a330ea4a42cea6c270f60a6c44ef9aa13581a99d7fbb4545fbb96fad7dd7d1

#### Native item 1

Native pointer: /proofs/0/evidence_refs/0; canonical SHA-256: b19fb7c8c803db8f032fec84a224b28942fde97dde018ab224388a03db0aa9cc

SO_FO_S01_direction_HP__randomized__probability__e_model_20261122

#### Native item 2

Native pointer: /proofs/0/evidence_refs/1; canonical SHA-256: c8aa54094e1b8d3b967a5033f828dd3d3a9f3cbb0363ad3c796edfd297bb499b

SO_FO_S01_direction_HP__randomized__probability__e_all_budget_20261122

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: bb6bc647a1eb02ffc745e57268d0acf089bf9a75dfb4c0cc3fac9f1ff946352b

Set source X=R^d and source r=h, and rename (G,D,L,s,p) as (L,R,sigma,sigma_dir,alpha). The target f is globally Lipschitz on this X, and the target exact prox is exactly the source auxiliary interface. The explicitly fixed query-dependent kernels coincide with the source oracle. Both quantities minimize a uniform failure-probability threshold under an almost-sure raw-call cap. Thus the source upper theorem applies to every target instance. For the lower direction, source Theorem 2.2 uses X=R^d and h(x)=mu*||x||^2/2, including h=0 at mu=0. The source hard functions are globally convex and Lipschitz and obey the same initial-distance and moment budgets; hence they lie in the target class. This argument imports the cited theorem statement, not a reproof of it. To meet the Atlas cap on every execution path, stop before any (T+1)st call and return the last feasible point (or the public initial point). The source already uses at most T calls almost surely on every legal instance, so this change affects only a null event per instance and leaves its success probability unchanged. It does not cover history-adaptive response kernels or claim a lower bound for each individually prescribed public regularizer.

#### Native field: premises

Native pointer: /proofs/0/premises; canonical SHA-256: cb30d0947cec5bef581e52ad5c58a6bc618daaf0d550d6f3cfbdb3f9e54afa5d

#### Native item 1

Native pointer: /proofs/0/premises/0; canonical SHA-256: 46cb2254391b935eb24e08004ce1dbd4a7e371cb9f95363909c9f3be4b3d3ef2

#### Native field: pointer

Native pointer: /proofs/0/premises/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/premises/0/sha256; canonical SHA-256: e31332cc0faf2ec3ca0f20a5071800ddc9745fa0d58b6335e20f2ff164b1f2d6

700bd90b73aae523641be265d92b758639af38c0f3ab91a41b73be9c0696e319

#### Native item 2

Native pointer: /proofs/0/premises/1; canonical SHA-256: ebf4cb2bbd3345ea933032e67b9f97c2db872c7bf9a34cb745f58a2357755879

#### Native field: pointer

Native pointer: /proofs/0/premises/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/premises/1/sha256; canonical SHA-256: 75319f538c3512935f3279c34724877438fbaa3a60baf90e56895be375c047b1

bb50e5030ecbde798536c88857215054350ba80b99416078c95d4674686a53d5

#### Native item 3

Native pointer: /proofs/0/premises/2; canonical SHA-256: 0110df50cc57c83742e7645ae27ec861f676e3ad9af33e49fa02861e8a7a4426

#### Native field: pointer

Native pointer: /proofs/0/premises/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/0/premises/2/sha256; canonical SHA-256: 9ae44cc00f0c8085c1f5d2a4e9819f8e8235b84fcf152ef9f02fc5159c5f4d35

ed1d654804b32ed6936d7ad85c02a9b6f19411df17bfa03c74892de6016af71a

#### Native item 4

Native pointer: /proofs/0/premises/3; canonical SHA-256: cc637cc25951dfabf75009cf06b44b02c8a5315fcc63287f4e2fcb5b59d23199

#### Native field: pointer

Native pointer: /proofs/0/premises/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/premises/3/sha256; canonical SHA-256: 9290d87d7c3f00bf03c981ebc43c2e0fedebc9895ae68f5f7a42ee2a3c6b5233

cd5493a70bf42c3f19c57eabbb643253f46a0907d32647cdcfa4fdadb66a9c3d

#### Native item 5

Native pointer: /proofs/0/premises/4; canonical SHA-256: 3ad32a5face845be19671b72435b1780fd5a4d5c60f51164eb47d30918437984

#### Native field: pointer

Native pointer: /proofs/0/premises/4/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/0/premises/4/sha256; canonical SHA-256: 8ba38e07f929a7f3cd07defabb08b440103940cc4536d2c39f678ba5a84716ed

be501633904312c65f31f875c37820ef10ba742556a111cfef82335ffd108aa3

### Native proof: SO_FO_S01_direction_HP__randomized__probability__proof_envelope_algebra_20261122

Native pointer: /proofs/1; canonical SHA-256: 0e92737b9ec0c062a2cf7be6adaa24698f30e745f7bc9c667b9b34f1265c7bfc

#### Native field: kind

Native pointer: /proofs/1/kind; canonical SHA-256: 1a85a7722b6bb2f2ed77a2e901981deee18dc6c4549753af7b864e5870d96105

local_algebraic_derivation

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 2be50891b3abe0ea67ff3c8ecd3ddc77bf9d8596a3b610573dcc6c24bb5cfcf7

Envelope comparison, sharp subregions and exhaustive row routing

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 32a43d815202b7f6933e4f61b648fd36275c9b527ba02495683a71422c0a8ed4

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 10666aff4da11b0d19e83140a77e83d1bc6672d83f46e3f28322c8f5e7268888

SO_SRC_2610_00260v2

#### Native field: evidence_refs

Native pointer: /proofs/1/evidence_refs; canonical SHA-256: 7893769652639988313c12cd63de169ce62886dd933df85ee0c12047c28b1758

#### Native item 1

Native pointer: /proofs/1/evidence_refs/0; canonical SHA-256: c8aa54094e1b8d3b967a5033f828dd3d3a9f3cbb0363ad3c796edfd297bb499b

SO_FO_S01_direction_HP__randomized__probability__e_all_budget_20261122

#### Native item 2

Native pointer: /proofs/1/evidence_refs/1; canonical SHA-256: 36c466cb07c06ad239c0baf03cf43dc7a4f6a67a823cc36987ad34ab53669613

SO_FO_S01_direction_HP__randomized__probability__e_heavy_20261122

#### Native item 3

Native pointer: /proofs/1/evidence_refs/2; canonical SHA-256: 885d94652d02238d22b5e8d8848d2d5d794a6c8180bdb701e430332667bd0467

SO_FO_S01_direction_HP__randomized__probability__e_statistical_20261122

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 02c288dddafcb32fda7318d4306a4a98ac74f6feddce3f8ef07268a467d7f7a8

Write H(z)=max_{0<=r<=R}(zr-mu*r^2/2). Maximizing the concave quadratic gives the displayed three branches. H is increasing. For k>=1, H(kz)<=k^2 H(z): substituting r=k*s and enlarging the allowed interval bounds the maximization by k^2 times H(z); the reverse scaling inequality for 0<=k<=1 follows by restricting to r=k*s. If w>=L, both source envelopes are H(L). If a<=C0*w, min(L,v)<= (1+C0)*min(L,w), so the ratio of source envelopes is at most (1+C0)^2. At mu=0 this gives R*w in the nonsaturated region. At mu>0, w<=mu*R gives w^2/(2*mu), and w>mu*R gives R*w-mu*R^2/2. The pure heavy-tail rows use Theorem 2.1 with its complete domination predicate and u<=L (implied by w<L). Their strong row also retains u<=mu*R. The other statistical rows explicitly exclude the pure-heavy rows. A pure-heavy predicate implies a<=C0*w, so it cannot intersect the remaining row a>C0*w. Confidence and dimension are split first, then w>=L versus w<L, then the stated curvature and domination predicates. These nine active rows partition the original native parameter domain for each fixed C0>0. They say nothing about an independent proof verification of the source theorem.

#### Native field: premises

Native pointer: /proofs/1/premises; canonical SHA-256: cb30d0947cec5bef581e52ad5c58a6bc618daaf0d550d6f3cfbdb3f9e54afa5d

#### Native item 1

Native pointer: /proofs/1/premises/0; canonical SHA-256: 46cb2254391b935eb24e08004ce1dbd4a7e371cb9f95363909c9f3be4b3d3ef2

#### Native field: pointer

Native pointer: /proofs/1/premises/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/1/premises/0/sha256; canonical SHA-256: e31332cc0faf2ec3ca0f20a5071800ddc9745fa0d58b6335e20f2ff164b1f2d6

700bd90b73aae523641be265d92b758639af38c0f3ab91a41b73be9c0696e319

#### Native item 2

Native pointer: /proofs/1/premises/1; canonical SHA-256: ebf4cb2bbd3345ea933032e67b9f97c2db872c7bf9a34cb745f58a2357755879

#### Native field: pointer

Native pointer: /proofs/1/premises/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/1/premises/1/sha256; canonical SHA-256: 75319f538c3512935f3279c34724877438fbaa3a60baf90e56895be375c047b1

bb50e5030ecbde798536c88857215054350ba80b99416078c95d4674686a53d5

#### Native item 3

Native pointer: /proofs/1/premises/2; canonical SHA-256: 0110df50cc57c83742e7645ae27ec861f676e3ad9af33e49fa02861e8a7a4426

#### Native field: pointer

Native pointer: /proofs/1/premises/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/1/premises/2/sha256; canonical SHA-256: 9ae44cc00f0c8085c1f5d2a4e9819f8e8235b84fcf152ef9f02fc5159c5f4d35

ed1d654804b32ed6936d7ad85c02a9b6f19411df17bfa03c74892de6016af71a

#### Native item 4

Native pointer: /proofs/1/premises/3; canonical SHA-256: cc637cc25951dfabf75009cf06b44b02c8a5315fcc63287f4e2fcb5b59d23199

#### Native field: pointer

Native pointer: /proofs/1/premises/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/1/premises/3/sha256; canonical SHA-256: 9290d87d7c3f00bf03c981ebc43c2e0fedebc9895ae68f5f7a42ee2a3c6b5233

cd5493a70bf42c3f19c57eabbb643253f46a0907d32647cdcfa4fdadb66a9c3d

#### Native item 5

Native pointer: /proofs/1/premises/4; canonical SHA-256: 3ad32a5face845be19671b72435b1780fd5a4d5c60f51164eb47d30918437984

#### Native field: pointer

Native pointer: /proofs/1/premises/4/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/1/premises/4/sha256; canonical SHA-256: 8ba38e07f929a7f3cd07defabb08b440103940cc4536d2c39f678ba5a84716ed

be501633904312c65f31f875c37820ef10ba742556a111cfef82335ffd108aa3

### Native proof: SO_FO_S01_direction_HP__randomized__probability__proof_confidence_transfer_20261122

Native pointer: /proofs/2; canonical SHA-256: 3efaf6d264742a3bded91f3de95932b7102dc008974a45895ecabb8abcb33c1f

#### Native field: kind

Native pointer: /proofs/2/kind; canonical SHA-256: 8c8b991744407f2546efd215bc75436b90dd5f5070854ccda8f7459c535f15c1

local_guarantee_derivation

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 954de1a388bf964cac03ae7c46a90873344f27b6fb76f36d4b320a8e7d8b089c

Upper transfer to the remaining native confidence range

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 32a43d815202b7f6933e4f61b648fd36275c9b527ba02495683a71422c0a8ed4

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: 10666aff4da11b0d19e83140a77e83d1bc6672d83f46e3f28322c8f5e7268888

SO_SRC_2610_00260v2

#### Native field: evidence_refs

Native pointer: /proofs/2/evidence_refs; canonical SHA-256: 568c091e32385913310f8e6654337f31400ddb8b0b881ed73217dfbda233b020

#### Native item 1

Native pointer: /proofs/2/evidence_refs/0; canonical SHA-256: c8aa54094e1b8d3b967a5033f828dd3d3a9f3cbb0363ad3c796edfd297bb499b

SO_FO_S01_direction_HP__randomized__probability__e_all_budget_20261122

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: dd91d3868d6d65a8a0ca05a3b328f79ec7deffa439f29d808150c186b4235083

For 1/10<=delta<1/2, run the source upper algorithm with delta0=1/20. Its failure probability is at most delta0<=delta and its raw-call cap is still T. Substituting ell0=log(3/delta0)=log(60) into the upper amplitude gives v0 and proves the recorded upper bound in all finite dimensions. A lower bound for the stricter delta0 guarantee would not imply a lower bound for the weaker target delta, so none is imported.

#### Native field: premises

Native pointer: /proofs/2/premises; canonical SHA-256: cb30d0947cec5bef581e52ad5c58a6bc618daaf0d550d6f3cfbdb3f9e54afa5d

#### Native item 1

Native pointer: /proofs/2/premises/0; canonical SHA-256: 46cb2254391b935eb24e08004ce1dbd4a7e371cb9f95363909c9f3be4b3d3ef2

#### Native field: pointer

Native pointer: /proofs/2/premises/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/2/premises/0/sha256; canonical SHA-256: e31332cc0faf2ec3ca0f20a5071800ddc9745fa0d58b6335e20f2ff164b1f2d6

700bd90b73aae523641be265d92b758639af38c0f3ab91a41b73be9c0696e319

#### Native item 2

Native pointer: /proofs/2/premises/1; canonical SHA-256: ebf4cb2bbd3345ea933032e67b9f97c2db872c7bf9a34cb745f58a2357755879

#### Native field: pointer

Native pointer: /proofs/2/premises/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/2/premises/1/sha256; canonical SHA-256: 75319f538c3512935f3279c34724877438fbaa3a60baf90e56895be375c047b1

bb50e5030ecbde798536c88857215054350ba80b99416078c95d4674686a53d5

#### Native item 3

Native pointer: /proofs/2/premises/2; canonical SHA-256: 0110df50cc57c83742e7645ae27ec861f676e3ad9af33e49fa02861e8a7a4426

#### Native field: pointer

Native pointer: /proofs/2/premises/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/2/premises/2/sha256; canonical SHA-256: 9ae44cc00f0c8085c1f5d2a4e9819f8e8235b84fcf152ef9f02fc5159c5f4d35

ed1d654804b32ed6936d7ad85c02a9b6f19411df17bfa03c74892de6016af71a

#### Native item 4

Native pointer: /proofs/2/premises/3; canonical SHA-256: cc637cc25951dfabf75009cf06b44b02c8a5315fcc63287f4e2fcb5b59d23199

#### Native field: pointer

Native pointer: /proofs/2/premises/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/2/premises/3/sha256; canonical SHA-256: 9290d87d7c3f00bf03c981ebc43c2e0fedebc9895ae68f5f7a42ee2a3c6b5233

cd5493a70bf42c3f19c57eabbb643253f46a0907d32647cdcfa4fdadb66a9c3d

#### Native item 5

Native pointer: /proofs/2/premises/4; canonical SHA-256: 3ad32a5face845be19671b72435b1780fd5a4d5c60f51164eb47d30918437984

#### Native field: pointer

Native pointer: /proofs/2/premises/4/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/2/premises/4/sha256; canonical SHA-256: 8ba38e07f929a7f3cd07defabb08b440103940cc4536d2c39f678ba5a84716ed

be501633904312c65f31f875c37820ef10ba742556a111cfef82335ffd108aa3

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Sharp High-Probability Statistical Rates for Heavy-Tailed Nonsmooth Convex Optimization. 2026. arXiv:2610.00260v2, 2026-10-19.

https://arxiv.org/html/2610.00260v2
