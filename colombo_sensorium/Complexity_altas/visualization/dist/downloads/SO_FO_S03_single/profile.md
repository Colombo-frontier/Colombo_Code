# Stochastic nonconvex stationarity: fresh single-point samples; stochastic full gradients

**Setting ID.** `SO_FO_S03_single`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; stochastic model: Centered alpha moment noise

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic gradient; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $\beta$-smooth and satisfies $f(x_0)-\inf f\le\Delta$. Convexity and a bounded query radius are not assumed.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad {\varepsilon}^{2} \le c\,\beta\,\Delta,\quad \beta > 0\\\Delta > 0,\quad \sigma \ge 0,\quad \alpha > 1,\quad \alpha \le 2\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta,\ \sigma$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full gradients:

$$\mathbb{E}_tG_t=\nabla f(x_t),\quad\mathbb{E}_t\|G_t-\nabla f(x_t)\|^\alpha\le\sigma^\alpha$$

Every observation is fresh. Same-point batches are conditionally independent, and the conditional moment bounds hold uniformly over histories. Samples cannot be reused across points.

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

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

#### Deterministic / Expected loss

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise. The algorithm uses no private random numbers. The instance and its admissible oracle law are fixed before randomness is averaged.

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

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$c_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<c_\alpha<\infty$.

$C_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<C_\alpha<\infty$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Finite variance with an improved dimension requirement

**Region.** $\alpha=2,\quad\theta\in\Theta_{\rm single,hd}$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B3

$$
c[\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4]
$$

**Upper bound.** B1

$$
C[\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4]
$$

**Gap or comparison.** $O(1)$

### R2 - Sufficiently high-dimensional single-point heavy-tailed regime

**Region.** $\varepsilon^2\le\beta\Delta/(96\cdot12\cdot154),\quad d\ge C_\alpha {\beta\Delta\over\varepsilon^2}\log\!\left[2+{\beta\Delta\over\varepsilon^2}(1+\sigma/\varepsilon)^{\alpha/[2(\alpha-1)]}\right]$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B3

$$
c_\alpha (\beta\Delta/\varepsilon^2)[1+(\sigma/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Upper bound.** B2

$$
C_\alpha (\beta\Delta/\varepsilon^2)[1+(\sigma/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Gap or comparison.** $O_\alpha(1)$

### R3 - Sufficiently high-dimensional single-point heavy-tailed regime

**Region.** $\varepsilon^2\le\beta\Delta/(96\cdot12\cdot154),\quad d\ge C_\alpha {\beta\Delta\over\varepsilon^2}\log\!\left[2+{\beta\Delta\over\varepsilon^2}(1+\sigma/\varepsilon)^{\alpha/[2(\alpha-1)]}\right]$

**Views.** Deterministic / Expected loss

**Quantity.** Q3

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Upper bound missing

**Lower bound.** B4

$$
c_\alpha (\beta\Delta/\varepsilon^2)[1+(\sigma/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - RSG with randomized output selection

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4]
$$

**Sources.** [1](https://arxiv.org/pdf/1309.5549)

**Conditions.** $$\alpha=2,\quad0<\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\alpha=2,\quad0<\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/1309.5549) theorem: Corollary 2.2, Eq.(2.14); PDF p.8

### B2 - Robust gradient estimation and gradient descent with a randomized output

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C_\alpha (\beta\Delta/\varepsilon^2)[1+(\sigma/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Conditions.** $$0<\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $0<\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Local argument.** A1

### B3 - Heavy-tailed lower bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha (\beta\Delta/\varepsilon^2)[1+(\sigma/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Sources.** [2](https://proceedings.mlr.press/v313/liu26a.html)

**Conditions.** $$\varepsilon^2\le\beta\Delta/(96\cdot12\cdot154),\quad d\ge C_\alpha {\beta\Delta\over\varepsilon^2}\log\!\left[2+{\beta\Delta\over\varepsilon^2}(1+\sigma/\varepsilon)^{\alpha/[2(\alpha-1)]}\right]$$

**Dimension conditions.** $\varepsilon^2\le\beta\Delta/(96\cdot12\cdot154),\quad d\ge C_\alpha {\beta\Delta\over\varepsilon^2}\log\!\left[2+{\beta\Delta\over\varepsilon^2}(1+\sigma/\varepsilon)^{\alpha/[2(\alpha-1)]}\right]$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://proceedings.mlr.press/v313/liu26a.html) theorem: Final ALT2026 Theorem 10 and Remark 13; PDF pp.44–46

### B4 - Heavy-tailed lower bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha (\beta\Delta/\varepsilon^2)[1+(\sigma/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Sources.** [2](https://proceedings.mlr.press/v313/liu26a.html)

**Conditions.** $$\varepsilon^2\le\beta\Delta/(96\cdot12\cdot154),\quad d\ge C_\alpha {\beta\Delta\over\varepsilon^2}\log\!\left[2+{\beta\Delta\over\varepsilon^2}(1+\sigma/\varepsilon)^{\alpha/[2(\alpha-1)]}\right]$$

**Dimension conditions.** $\varepsilon^2\le\beta\Delta/(96\cdot12\cdot154),\quad d\ge C_\alpha {\beta\Delta\over\varepsilon^2}\log\!\left[2+{\beta\Delta\over\varepsilon^2}(1+\sigma/\varepsilon)^{\alpha/[2(\alpha-1)]}\right]$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://proceedings.mlr.press/v313/liu26a.html) theorem: Final ALT2026 Theorem 10 and Remark 13; PDF pp.44–46

## 5. Local arguments

### A1 - Heavy-tailed gradient estimation and PL stages

**Scope.** Conditionally independent fresh samples in each same-point batch, with centered norm moment of order greater than one.

**Algorithm scope.** PL upper witness has deterministic policies; nonconvex stationarity output uses private randomization.

Condition on the history at an adaptively selected point. Fresh samples are conditionally independent, have mean $g$, and obey
$\mathbb E\|G-g\|^\alpha\le\sigma^\alpha$, $1<\alpha\le2$.
Form nine block means of $b$ samples and take their geometric median with deterministic tie breaking. Symmetrization and the Hilbert-space moment inequality give
$\mathbb E\|Z_j-g\|^\alpha\le2^\alpha\sigma^\alpha b^{1-\alpha}$.
If seven blocks lie within radius $r$, median optimality gives
$5\|\widehat g-g\|\le14r$.
An error larger than $3r$ requires at least three bad blocks, so
$$
\Pr(\|\widehat g-g\|>3r)\le
84\min\{1,(2\sigma b^{-(\alpha-1)/\alpha}/r)^{3\alpha}\}.
$$
Integrating the tail, since $3\alpha>2$, yields
$$
\mathbb E[\|\widehat g-g\|^2\mid\mathcal H]
\le C_\alpha\sigma^2b^{-2(\alpha-1)/\alpha}.
$$
Individual samples need not have finite variance. Independence within a batch is essential.

The update $x^+=x-\widehat g/\beta$ satisfies
$$
f(x^+)\le f(x)-\|\nabla f(x)\|^2/(2\beta)
+\|\widehat g-\nabla f(x)\|^2/(2\beta),
$$
even if the estimate is biased. Under PL this gives conditional expected contraction with additive term
$C_\alpha\sigma^2/[2\beta b^{2(\alpha-1)/\alpha}]$.
At scale $u_s=\Delta/2^s$, choose
$$
b_s=\left\lceil\max\{1,(C_\alpha\sigma^2/(\mu u_s))^{\alpha/[2(\alpha-1)]}\}\right\rceil
$$
and $J=\lceil\kappa\log4\rceil$ steps. Starting from expected gap at most $u_s$, the next stage has gap at most $u_s/2$. Summing the charged $9Jb_s$ samples gives
$$
C_\alpha\kappa\left[\log(2+\Delta/\epsilon)
+(\sigma^2/(\mu\epsilon))^{\alpha/[2(\alpha-1)]}\right].
$$
The schedule and output require no private randomness.

For general nonconvex stationarity, choose
$b=C_\alpha[1+(\sigma/\epsilon)^{\alpha/(\alpha-1)}]$,
run $C\beta\Delta/\epsilon^2$ updates, and return a uniformly random iterate. Summing descent gives expected squared gradient norm at most $\epsilon^2$, hence expected norm at most $\epsilon$. This output rule is private randomization.

**Limits of the argument.** The proof does not apply to arbitrarily dependent samples within a batch.

## References

[1] Saeed Ghadimi and Guanghui Lan. Stochastic First- and Zeroth-order Methods for Nonconvex Stochastic Programming. 2013; SIAM Journal on Optimization 23(4):2341–2368; Corollary 2.2, Eq.(2.14), arXiv PDF p.8.

https://arxiv.org/pdf/1309.5549

[2] Zijian Liu. Online Convex Optimization with Heavy Tails: Old Algorithms, New Regrets, and Applications. 2026; ALT 2026, PMLR 313:1–47; final published PDF Theorem 10 and Remark 13, pp.44–46. PDF: https://raw.githubusercontent.com/mlresearch/v313/main/assets/liu26a/liu26a.pdf; earlier author version Theorem 11 and Remark 10, pp.35–36.

https://proceedings.mlr.press/v313/liu26a.html
