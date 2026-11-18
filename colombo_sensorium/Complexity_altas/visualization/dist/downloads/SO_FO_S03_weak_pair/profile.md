# Stochastic nonconvex stationarity: weak moments and paired-sample two-point access

**Setting ID.** `SO_FO_S03_weak_pair`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Weak average smoothness; stochastic model: Centered alpha moment noise

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Paired sample gradient; operation: Paired sample gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: Zero respecting

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $\beta$-smooth and satisfies $f(x_0)-\inf f\le\Delta$. Convexity and a bounded query radius are not assumed. Paired-sample gradient differences have $\gamma$th moment at most $\beta^\gamma\|x-y\|^\gamma$, and centered noise has $\alpha$th moment at most $\sigma^\alpha$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad {\varepsilon}^{2} \le c\,\beta\,\Delta,\quad \gamma \ge 1\\\gamma \le 2,\quad \beta > 0,\quad \Delta > 0,\quad \sigma \ge 0\\\alpha > 1,\quad \alpha \le 2\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \gamma,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta,\ \sigma$.

The unknown object is the objective $f$.

Submit both legal points $x,y\in\mathbb R^d$ before drawing a fresh sample; the oracle then returns information at both points.

$$\mathbb{E}_tG_t=\nabla f(x_t),\quad\mathbb{E}_t\|G_t-\nabla f(x_t)\|^\alpha\le\sigma^\alpha,\quad\mathbb{E}\|g(x,z)-g(y,z)\|^\gamma\le\beta^\gamma\|x-y\|^\gamma$$

One fresh sample returns gradients at two points specified in advance; the two evaluations are charged separately.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=\|\nabla f(\widehat{x})\|_2$$

$\varepsilon$ is a gradient-norm tolerance. Expected norm and expected squared norm are different performance requirements.

### Resource accounting

One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

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

#### Randomized / Zero respecting / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

Every iterate is supported on the union of supports of previously returned gradients. The output obeys the corresponding historical-support restriction.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Output qualification.** The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

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

$z$: Sample generating a stochastic gradient map; the oracle specifies how two points may share a sample

$g(x,z)$: Stochastic gradient map generated by sample $z$ at query point $x$

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\gamma$: Moment order of the paired-sample gradient difference; distinct from the noise tail index. **Domain:** $1\le\gamma\le2$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$C_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<C_\alpha<\infty$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$c_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<c_\alpha<\infty$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Zero respecting / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Weak mean-smoothness model

**Region.** $1<\alpha\le2,\quad1\le\gamma\le2,\quad0<\varepsilon^2\le c\beta\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C_{\alpha,\gamma}[(\sigma/\varepsilon)^{\alpha/(\alpha-1)}+\beta\Delta/\varepsilon^2+(\beta\Delta/\varepsilon^2)(\sigma/\varepsilon)^{\alpha/[\gamma(\alpha-1)]}]
$$

### R2 - Construction window for the restricted-algorithm lower bound

**Region.** $\theta\in\Theta_{\rm weak},\quad d\ge d_{\rm Fradin}$

**Views.** Randomized / Zero respecting / Expected loss

**Quantity.** Q2

**Resource.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Status.** Optimal

**Lower bound.** B3

$$
c_{\alpha,\gamma}[(\sigma/\varepsilon)^{\alpha/(\alpha-1)}+\beta\Delta/\varepsilon^2+(\beta\Delta/\varepsilon^2)(\sigma/\varepsilon)^{\alpha/[\gamma(\alpha-1)]}]
$$

**Upper bound.** B2

$$
C_{\alpha,\gamma}[(\sigma/\varepsilon)^{\alpha/(\alpha-1)}+\beta\Delta/\varepsilon^2+(\beta\Delta/\varepsilon^2)(\sigma/\varepsilon)^{\alpha/[\gamma(\alpha-1)]}]
$$

**Gap or comparison.** $O_{\alpha,\gamma}(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - NSGD-MVR

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C_{\alpha,\gamma}[(\sigma/\varepsilon)^{\alpha/(\alpha-1)}+\beta\Delta/\varepsilon^2+(\beta\Delta/\varepsilon^2)(\sigma/\varepsilon)^{\alpha/[\gamma(\alpha-1)]}]
$$

**Sources.** [1](https://arxiv.org/pdf/2512.18713)

**Conditions.** $$1<\alpha\le2,\quad1\le\gamma\le2,\quad0<\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $1<\alpha\le2,\quad1\le\gamma\le2,\quad0<\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2512.18713) theorem: Theorems 3.1,4.1; Definition B.4; PDF pp.8,10–11

### B2 - NSGD-MVR

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Zero respecting / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C_{\alpha,\gamma}[(\sigma/\varepsilon)^{\alpha/(\alpha-1)}+\beta\Delta/\varepsilon^2+(\beta\Delta/\varepsilon^2)(\sigma/\varepsilon)^{\alpha/[\gamma(\alpha-1)]}]
$$

**Sources.** [1](https://arxiv.org/pdf/2512.18713)

**Conditions.** $$1<\alpha\le2,\quad1\le\gamma\le2,\quad0<\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $1<\alpha\le2,\quad1\le\gamma\le2,\quad0<\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2512.18713) theorem: Theorems 3.1,4.1; Definition B.4; PDF pp.8,10–11

### B3 - Zero-respecting hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Zero respecting / Expected loss

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c_{\alpha,\gamma}[(\sigma/\varepsilon)^{\alpha/(\alpha-1)}+\beta\Delta/\varepsilon^2+(\beta\Delta/\varepsilon^2)(\sigma/\varepsilon)^{\alpha/[\gamma(\alpha-1)]}]
$$

**Sources.** [1](https://arxiv.org/pdf/2512.18713)

**Conditions.** $$\theta\in\Theta_{\rm weak},\quad d\ge d_{\rm Fradin}$$

**Dimension conditions.** $\theta\in\Theta_{\rm weak},\quad d\ge d_{\rm Fradin}$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2512.18713) theorem: Theorems 3.1,4.1; Definition B.4; PDF pp.8,10–11

## References

[1] Adrien Fradin, Abdurakhmon Sadiev, Laurent Condat and Peter Richtárik. Tight Lower Bounds and Optimal Algorithms for Stochastic Nonconvex Optimization with Heavy-Tailed Noise. 2026; AISTATS 2026, PMLR 300:2548–2556; arXiv v2, 31 March 2026; Theorems 3.1–3.2,4.1–4.2 and Definition B.4.

https://arxiv.org/pdf/2512.18713
