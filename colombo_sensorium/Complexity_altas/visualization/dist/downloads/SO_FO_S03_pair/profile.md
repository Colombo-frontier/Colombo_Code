# Stochastic nonconvex stationarity: paired-sample mean-square smoothness; two-point gradients from one sample

**Setting ID.** `SO_FO_S03_pair`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Fully optimal

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Mean square smooth samples; stochastic model: Bounded variance

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Paired sample gradient; operation: Paired sample gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

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

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $\beta$-smooth and satisfies $f(x_0)-\inf f\le\Delta$. Convexity and a bounded query radius are not assumed. Paired-sample access is supplied by $g(x,z)$, with $\mathbb E\|g(x,z)-g(y,z)\|^2\le\beta^2\|x-y\|^2$ and a uniform centered variance bound $\sigma^2$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad {\varepsilon}^{2} \le c\,\beta\,\Delta,\quad \alpha = 2\\\beta > 0,\quad \Delta > 0,\quad \sigma \ge 0,\quad \alpha > 1\\\alpha \le 2\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta,\ \sigma$.

The unknown object is the objective $f$.

Submit both legal points $x,y\in\mathbb R^d$ before drawing a fresh sample; the oracle then returns information at both points.

$$\bigl(g(x,z),g(y,z)\bigr),\quad\mathbb{E}_zg(u,z)=\nabla f(u),\quad\mathbb{E}_z\|g(u,z)-\nabla f(u)\|_2^2\le\sigma^2\ (u=x,y)$$

Submit both points before drawing a fresh sample $z$. Samples cannot be reused across rounds; each point costs one gradient evaluation.

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

$z$: Sample generating a stochastic gradient map; the oracle specifies how two points may share a sample

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

**Definition.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Two-point access with high noise in sufficiently high dimension

**Region.** $\sigma\ge\varepsilon,\ d\ge d_{\rm pair}$

**Quantity.** Q1

**Resource.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Status.** Optimal

**Lower bound.** B1

$$
c[\beta\Delta/\varepsilon^2+\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2]
$$

**Upper bound.** B2

$$
C[\beta\Delta/\varepsilon^2+\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2]
$$

**Gap or comparison.** $O(1)$

### R2 - Two-point access with low noise in sufficiently high dimension

**Region.** $0\le\sigma\le\varepsilon,\ d\ge d_{\rm pair}$

**Quantity.** Q1

**Resource.** One gradient evaluation for one sample at one point costs one unit; a paired two-point response costs two units.

**Status.** Optimal

**Lower bound.** B1

$$
c\beta\Delta/\varepsilon^2
$$

**Upper bound.** B3

$$
C\beta\Delta/\varepsilon^2
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Mean-square-smooth lower bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[\beta\Delta/\varepsilon^2+\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2]
$$

**Sources.** [3](https://arxiv.org/pdf/1912.02365)

**Conditions.** $$d\ge d_{\rm pair}(\beta,\Delta,\sigma,\varepsilon)$$

**Dimension conditions.** $d\ge d_{\rm pair}(\beta,\Delta,\sigma,\varepsilon)$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients, stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/1912.02365) theorem: Theorem 3, Eqs.(23)–(24); PDF pp.14–15

**Source location.** [3](https://arxiv.org/pdf/1912.02365) theorem: Section 5.1, Proposition 1, Lemma 8; Theorem 3

### B2 - SPIDER online

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C(\beta\Delta\sigma/\varepsilon^3+\sigma^2/\varepsilon^2)
$$

**Sources.** [2](https://arxiv.org/pdf/1807.01695)

**Conditions.** $$\sigma\ge\varepsilon,\quad\theta\in\Theta_{\rm variance}$$

**Dimension conditions.** $\sigma\ge\varepsilon,\quad\theta\in\Theta_{\rm variance}$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [2](https://arxiv.org/pdf/1807.01695) theorem: Assumption 1(ii); Theorem 1, Eq.(3.6); PDF pp.9–11

### B3 - Use RSG without exploiting two-point access

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C[\beta\Delta/\varepsilon^2+\beta\Delta\sigma^2/\varepsilon^4]
$$

**Sources.** [1](https://arxiv.org/pdf/1309.5549)

**Conditions.** $$\alpha=2,\quad0<\varepsilon^2\le c\beta\Delta$$

**Dimension conditions.** $\alpha=2,\quad0<\varepsilon^2\le c\beta\Delta$

**Oracle correspondence.** Applicable interfaces: paired-sample two-point gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/1309.5549) theorem: Corollary 2.2, Eq.(2.14); PDF p.8

## References

[1] Saeed Ghadimi and Guanghui Lan. Stochastic First- and Zeroth-order Methods for Nonconvex Stochastic Programming. 2013; SIAM Journal on Optimization 23(4):2341–2368; Corollary 2.2, Eq.(2.14), arXiv PDF p.8.

https://arxiv.org/pdf/1309.5549

[2] Cong Fang, Chris Junchi Li, Zhouchen Lin and Tong Zhang. SPIDER: Near-Optimal Non-Convex Optimization via Stochastic Path-Integrated Differential Estimator. 2018; NeurIPS 2018; arXiv v2, Assumption 1(ii), Theorem 1, Eq.(3.6), pp.9–11.

https://arxiv.org/pdf/1807.01695

[3] Yossi Arjevani, Dylan J. Foster, Yair Carmon, Nathan Srebro, John Duchi and Blake Woodworth. Lower Bounds for Non-Convex Stochastic Optimization. 2023; Mathematical Programming 199:165–214; arXiv v2, Theorem 3, Eq.(23)–(24), Section 5.2 Proposition 2, pp.14–15,18.

https://arxiv.org/pdf/1912.02365
