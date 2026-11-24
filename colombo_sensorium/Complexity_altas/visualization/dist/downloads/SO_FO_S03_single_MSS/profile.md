# Stochastic nonconvex stationarity: mean-square smoothness with single-point feedback; stochastic full gradients

**Setting ID.** `SO_FO_S03_single_MSS`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Other quantified gap

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Mean square smooth samples; stochastic model: Bounded variance; structure: Sample loss gradient realizable; structure: Single use sample

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic gradient; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $\beta$-smooth and satisfies $f(x_0)-\inf f\le\Delta$. Convexity and a bounded query radius are not assumed. An instance also specifies differentiable scalar losses $f_\xi$ and their distribution, with $f=\mathbb E f_\xi$ and $g=\nabla f_\xi$. Unbiasedness, a uniform full-space variance bound $\sigma^2$, and paired-sample mean-square smoothness with constant $\beta^2$ must hold simultaneously.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad {\varepsilon}^{2} \le c\,\beta\,\Delta,\quad \alpha = 2\\\beta > 0,\quad \Delta > 0,\quad \sigma \ge 0,\quad \alpha > 1\\\alpha \le 2\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta,\ \sigma$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full gradients:

$$G_t=\nabla f_{\xi_t}(x_t),\quad\mathbb{E} G_t=\nabla f(x_t)$$

Select the query point before drawing a fresh sample. Each sample may be queried only once. Mean-square smoothness is a model property and does not grant two-point access.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=\|\nabla f(\widehat{x})\|_2$$

$\varepsilon$ is a gradient-norm tolerance. Expected norm and expected squared norm are different performance requirements.

### Resource accounting

One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$G_t$: $t$th full stochastic gradient or subgradient observation

$\xi$: Random observation sample; the oracle's interaction protocol determines sample-reuse permissions

$g(x,z)$: Stochastic gradient map generated by sample $z$ at query point $x$

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$d_{\rm pair}$: The maximum of the dimension required by the mean-square-smooth construction in Arjevani et al. (2023), Theorem 3, and the exact-subclass threshold. Its order may be taken as $\widetilde O(1+(\beta\Delta/\epsilon^2)^2)$, with the logarithmic dependence on $\sigma$ retained. This is a sufficient condition, not a necessary transition. **Domain:** $d_{\rm pair}=\widetilde{O}(1+(\beta\Delta/\varepsilon^2)^2)$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - minimax metric resource quantity

$$
T^\star_\infty=\inf_A\{N:\forall d,I,\ \mathbb E\|\nabla F(\widehat x)\|_2\le\varepsilon,\ N_A\le N\text{ on every run}\}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\rm sample}$; description: Fixed pathwise cap on single-use gradient responses.

### R1 - Two-point access with low noise in sufficiently high dimension

**Region.** $0\le\sigma\le\varepsilon,\ d\ge d_{\rm pair}$

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2

$$
c\beta\Delta/\varepsilon^2
$$

**Upper bound.** B1

$$
C\beta\Delta/\varepsilon^2
$$

**Gap or comparison.** $O(1)$

### R2 - Sufficiently high-dimensional mean-square-smooth regime

**Region.** $d\ge d_{\rm pair}(\beta,\Delta,\sigma,\varepsilon)$

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B2

$$
c[\beta\Delta/\varepsilon^2+\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2]
$$

**Upper bound.** B1

$$
C[\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4]
$$

**Gap or comparison.** ${\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4\over\beta\Delta/\varepsilon^2+\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2}$

### R3 - Dimension-uniform single-query MSS complexity

**Region.** $\Delta,\beta>0$, $\sigma\ge0$, $\alpha=2$, $0<\varepsilon\le c_0\sqrt{\beta\Delta}$, where $c_0$ is the universal constant of Theorem main. The upper bound holds for every finite $d$. For a proposed cap $N$, the lower construction uses $d=(T_0+1)D_0$, where $T_0=\lfloor c_T\beta\Delta/\varepsilon^2\rfloor$, $n_0=1+\lfloor c\sigma^2/\varepsilon^2\rfloor$, and $D_0\ge2T_0+C\rho_0^{-2}[n_0+\log(24T_0(N+1))]$, enlarged for Lemma side-channel. Here $c_T,c,\rho_0>0$ are source-fixed universal constants. See equations scales, n0, dimension-choice and Theorem lower. This is not a lower bound uniform over each fixed small dimension.

**Quantity.** Q2

**Resource.** Fixed pathwise cap on single-use gradient responses.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Upper bound.** B3

$$
O\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Gap or comparison.** Upper/lower ratio is bounded by a universal constant.

## 4. Bounds and supporting evidence

### B1 - RSG with randomized output selection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C[\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4]
$$

**Sources.** [1](https://arxiv.org/pdf/1309.5549)

**Conditions.** $$\alpha=2,\quad0<\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\alpha=2,\quad0<\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/1309.5549) theorem: Corollary 2.2, Eq.(2.14); PDF p.8

### B2 - Mean-square-smooth lower bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[\beta\Delta/\varepsilon^2+\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2]
$$

**Sources.** [2](https://arxiv.org/pdf/1912.02365)

**Conditions.** $$d\ge d_{\rm pair}(\beta,\Delta,\sigma,\varepsilon)$$

**Dimension conditions.** $d\ge d_{\rm pair}(\beta,\Delta,\sigma,\varepsilon)$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients, stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [2](https://arxiv.org/pdf/1912.02365) theorem: Theorem 3, Eqs.(23)–(24); PDF pp.14–15

**Source location.** [2](https://arxiv.org/pdf/1912.02365) theorem: Section 5.1, Proposition 1, Lemma 8; Theorem 3

### B3 - Stochastic gradient descent with randomized output selection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0902/manuscript.pdf)

**Conditions.** $\Delta,\beta>0$, $\sigma\ge0$, $\alpha=2$, $0<\varepsilon\le c_0\sqrt{\beta\Delta}$, where $c_0$ is the universal constant of Theorem main.; The samplewise MSS model implies population smoothness; the upper proof gives a squared-norm estimate and then the required expected norm.

**Dimension conditions.** The upper bound holds for every finite $d$. For a proposed cap $N$, the lower construction uses $d=(T_0+1)D_0$, where $T_0=\lfloor c_T\beta\Delta/\varepsilon^2\rfloor$, $n_0=1+\lfloor c\sigma^2/\varepsilon^2\rfloor$, and $D_0\ge2T_0+C\rho_0^{-2}[n_0+\log(24T_0(N+1))]$, enlarged for Lemma side-channel. Here $c_T,c,\rho_0>0$ are source-fixed universal constants. See equations scales, n0, dimension-choice and Theorem lower. This is not a lower bound uniform over each fixed small dimension.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0902/manuscript.pdf) Theorem main, equation main-rate; Section upper; verified labels: thm:main (line 408), eq:main-rate (line 414), sec:upper (line 476)

Stochastic gradient descent with randomized output selection. An unrestricted randomized algorithm with a fixed query cap.

The samplewise MSS model implies population smoothness; the upper proof gives a squared-norm estimate and then the required expected norm.

### B4 - Smooth gated scalar sample losses with additive Gaussian noise and sequential information accounting

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0902/manuscript.pdf)

**Conditions.** $\Delta,\beta>0$, $\sigma\ge0$, $\alpha=2$, $0<\varepsilon\le c_0\sqrt{\beta\Delta}$, where $c_0$ is the universal constant of Theorem main.; The hard dimension may depend on the proposed cap. The hard sample losses can be chosen individually gradient-Lipschitz with the same beta.

**Dimension conditions.** The upper bound holds for every finite $d$. For a proposed cap $N$, the lower construction uses $d=(T_0+1)D_0$, where $T_0=\lfloor c_T\beta\Delta/\varepsilon^2\rfloor$, $n_0=1+\lfloor c\sigma^2/\varepsilon^2\rfloor$, and $D_0\ge2T_0+C\rho_0^{-2}[n_0+\log(24T_0(N+1))]$, enlarged for Lemma side-channel. Here $c_T,c,\rho_0>0$ are source-fixed universal constants. See equations scales, n0, dimension-choice and Theorem lower. This is not a lower bound uniform over each fixed small dimension.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0902/manuscript.pdf) Theorems main and lower; equation lower-rate; verified labels: thm:main (line 408), sec:lower (line 1529), thm:lower (line 1571), eq:lower-rate (line 1573)

Smooth gated scalar sample losses with additive Gaussian noise and sequential information accounting. Arbitrary adaptive randomized queries and arbitrary measurable outputs.

The hard dimension may depend on the proposed cap. The hard sample losses can be chosen individually gradient-Lipschitz with the same beta.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Saeed Ghadimi and Guanghui Lan. Stochastic First- and Zeroth-order Methods for Nonconvex Stochastic Programming. 2013; SIAM Journal on Optimization 23(4):2341–2368; Corollary 2.2, Eq.(2.14), arXiv PDF p.8.

https://arxiv.org/pdf/1309.5549

[2] Yossi Arjevani, Dylan J. Foster, Yair Carmon, Nathan Srebro, John Duchi and Blake Woodworth. Lower Bounds for Non-Convex Stochastic Optimization. 2023; Mathematical Programming 199:165–214; arXiv v2, Theorem 3, Eq.(23)–(24), Section 5.2 Proposition 2, pp.14–15,18.

https://arxiv.org/pdf/1912.02365

[3] Colombo_0902. Sharp Single-Query Complexity of Nonconvex Optimization under Mean-Squared Smoothness. 0902_revised.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0902/manuscript.pdf
