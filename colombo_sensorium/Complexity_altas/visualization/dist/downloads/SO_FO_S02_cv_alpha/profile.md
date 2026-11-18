# Stochastic smooth convex minimization: convexity on a ball and heavy-tailed centered noise; stochastic full gradients

**Setting ID.** `SO_FO_S02_cv_alpha`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz gradient; stochastic model: Centered alpha moment noise

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic gradient; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown function $f$ is convex and $\beta$-smooth on the public ball $Q$, whose prox diameter is finite. This differs from an unrestricted unconstrained initial-distance model.

Feasible geometry: $Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{R}^{2},\quad \beta > 0\\\sigma \ge 0,\quad \alpha > 1,\quad \alpha \le 2,\quad R > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \varepsilon$.

Public upper bounds: $\beta,\ R,\ \sigma$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of stochastic full gradients:

$$\mathbb{E}_tG_t=\nabla f(x_t),\quad\mathbb{E}_t\|G_t-\nabla f(x_t)\|^\alpha\le\sigma^\alpha$$

Every observation is fresh. Same-point batches are conditionally independent, and the conditional moment bounds hold uniformly over histories. Samples cannot be reused across points.

Exact Euclidean projection onto the public domain; its internal computation is free

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Expected loss

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise. The algorithm uses no private random numbers. The instance and its admissible oracle law are fixed before randomness is averaged.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$G_t$: $t$th full stochastic gradient or subgradient observation

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$S$: Number of halving stages, $\max\{1,\lceil\log_2(2\Delta/\epsilon)\rceil\}$.

$$S=\max\{1,\lceil\log_2(2\Delta/\varepsilon)\rceil\}$$

$V$: Heavy-tailed statistical term at the final accuracy scale.

$$V={\frac{{\sigma}^{2}}{\mu\,\varepsilon}}^{\frac{\alpha}{2\,((\alpha-1))}}$$

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

**View.** Deterministic / Expected loss

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

### R1 - sufficiently high dimension

**Region.** $d\ge C\beta R^2/\varepsilon$

**Views.** Deterministic / Expected loss; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2, B7, B5, B9

$$
c_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Upper bound.** B1, B4

$$
C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Gap or comparison.** $O_\alpha(1)$

### R2 - Statistical dominance in all dimensions

**Region.** $(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}\ge \sqrt{\beta R^2/\varepsilon}$

**Views.** Deterministic / Expected loss; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2, B5

$$
c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)}
$$

**Upper bound.** B1, B4

$$
C_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)}
$$

**Gap or comparison.** $O_\alpha(1)$

### R3 - Remaining low-dimensional low-noise regime

**Region.** $\Theta_{\rm cv-alpha}\setminus(\Theta_{\rm hd}\cup\Theta_{\rm statistics})$

**Views.** Deterministic / Expected loss

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B2, B7

$$
\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}\}
$$

**Upper bound.** B1, B8

$$
\begin{cases}\min\{C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],2+\max\{0,\lceil\log_4(\beta R^2/(2\varepsilon))\rceil\}\},&d=1,\ \sigma=0,\\C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],&\text{otherwise}.\end{cases}
$$

**Gap or comparison.** $\frac{\begin{cases}\min\{C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],2+\max\{0,\lceil\log_4(\beta R^2/(2\varepsilon))\rceil\}\},&d=1,\ \sigma=0,\\C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],&\text{otherwise}.\end{cases}}{\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}\}}$

### R4 - Remaining low-dimensional low-noise regime

**Region.** $\Theta_{\rm cv-alpha}\setminus(\Theta_{\rm hd}\cup\Theta_{\rm statistics})$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B5, B9

$$
\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}\}
$$

**Upper bound.** B4, B10

$$
\begin{cases}\min\{C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],2+\max\{0,\lceil\log_4(\beta R^2/(2\varepsilon))\rceil\}\},&d=1,\ \sigma=0,\\C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],&\text{otherwise}.\end{cases}
$$

**Gap or comparison.** $\frac{\begin{cases}\min\{C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],2+\max\{0,\lceil\log_4(\beta R^2/(2\varepsilon))\rceil\}\},&d=1,\ \sigma=0,\\C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}],&\text{otherwise}.\end{cases}}{\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}\}}$

## 4. Bounds and supporting evidence

### B1 - Accelerated stochastic approximation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Sources.** [2](https://arxiv.org/pdf/2510.11676)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [2](https://arxiv.org/pdf/2510.11676) theorem: Assumption 1; Theorem 2(i), Eq.(33); PDF pp.4–5,8

### B2 - One-dimensional statistical obstruction

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874) [3](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_RARE_EVENT, FO_EXPECTATION_CONVERSION

### B3 - Exact-oracle subclass

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\max\{\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\},\log(2+\beta R^2/\varepsilon)\}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; quadratic reduction p.3; Eq.(7) dimension O(T²)

### B4 - Accelerated stochastic approximation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha[\sqrt{\beta R^2/\varepsilon}+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Sources.** [2](https://arxiv.org/pdf/2510.11676)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [2](https://arxiv.org/pdf/2510.11676) theorem: Assumption 1; Theorem 2(i), Eq.(33); PDF pp.4–5,8

### B5 - One-dimensional statistical obstruction

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874) [3](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Local argument.** FO_RARE_EVENT, FO_EXPECTATION_CONVERSION

### B6 - Exact-oracle subclass

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\max\{\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\},\log(2+\beta R^2/\varepsilon)\}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

**Conditions.** $$0<\varepsilon\le c\beta R^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta R^2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output rule.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource conversion.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

**Source location.** [1](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; quadratic reduction p.3; Eq.(7) dimension O(T²)

### B7 - Finite-dimensional exact-gradient subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

**Conditions.** Full native admissible domain, 0<epsilon<=c*beta*R^2.

**Dimension conditions.** Every d>=1, by the finite-dimensional transfer and affine bounded-m endpoint.

**Oracle correspondence.** Exact-gradient subclass admissible at every sigma; two source products per gradient.

**Guarantee conversion.** Expected loss implies relative-residual success>=3/4; unrestricted randomized scope.

**Output rule.** Minimizer inside ball; output projection to hard coordinates and <=1 source output query.

**Resource conversion.** B samples induce <=2B+1 source queries; see CV_ALPHA_DIMENSION_TRANSFER.

**Local argument.** CV_ALPHA_DIMENSION_TRANSFER

### B8 - Endpoint checks and derivative bisection

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
2+\max\{0,\lceil\log_4(\beta R^2/(2\varepsilon))\rceil\}
$$

**Conditions.** Native domain with d=1,sigma=0.

**Dimension conditions.**

$$
d=1
$$

**Oracle correspondence.** Zero centered moment gives exact derivatives almost surely.

**Guarantee conversion.** Deterministic finite cap and almost-sure epsilon error imply native expected loss.

**Output rule.** Feasible endpoint or possibly unqueried final midpoint.

**Resource conversion.** At most 2+max(0,ceil(log_4(beta R^2/(2 epsilon)))) samples.

**Local argument.** CV_ALPHA_1D_BISECTION

### B9 - Finite-dimensional exact-gradient subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{\sqrt d,\sqrt{\beta R^2/\varepsilon}\}
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

**Conditions.** Full native admissible domain, 0<epsilon<=c*beta*R^2.

**Dimension conditions.** Every d>=1, by the finite-dimensional transfer and affine bounded-m endpoint.

**Oracle correspondence.** Exact-gradient subclass admissible at every sigma; two source products per gradient.

**Guarantee conversion.** Expected loss implies relative-residual success>=3/4; unrestricted randomized scope.

**Output rule.** Minimizer inside ball; output projection to hard coordinates and <=1 source output query.

**Resource conversion.** B samples induce <=2B+1 source queries; see CV_ALPHA_DIMENSION_TRANSFER.

**Local argument.** CV_ALPHA_DIMENSION_TRANSFER

### B10 - Endpoint checks and derivative bisection

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
2+\max\{0,\lceil\log_4(\beta R^2/(2\varepsilon))\rceil\}
$$

**Conditions.** Native domain with d=1,sigma=0.

**Dimension conditions.**

$$
d=1
$$

**Oracle correspondence.** Zero centered moment gives exact derivatives almost surely.

**Guarantee conversion.** Deterministic finite cap and almost-sure epsilon error imply native expected loss.

**Output rule.** Feasible endpoint or possibly unqueried final midpoint.

**Resource conversion.** At most 2+max(0,ceil(log_4(beta R^2/(2 epsilon)))) samples.

**Local argument.** CV_ALPHA_1D_BISECTION

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: a99cba84356e2a01181d927ecc5a0855458a2ff774086c9d927a79bc3b7fb59e

### Native proof: FO_RARE_EVENT

Native pointer: /proofs/0; canonical SHA-256: ae0c9ad714558906081adc28274a1eb206ecf8145139411bf0df9c91db4cf08c

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: 0d5fbafbb82f7e02bb99b4992b954f7fcb4b689a57dc750afb848cc83e0267ee

Statistical lower bounds against arbitrary randomized algorithms; fixed confidence or expected error.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 59ec997d79d34a4701aa7d7ad629ec318911b27a6e7fcfbfb1afde545f17a504

A hidden sign determines mean $\pm a$. Return zero with probability $1-\pi$, and $\pm a/\pi$ with probability $\pi$. This is unbiased, with
$\mathbb E|Y-\mathbb EY|^\alpha\le C_\alpha a^\alpha\pi^{1-\alpha}$.
Choose $\pi$ proportional to $(a/\sigma)^{\alpha/(\alpha-1)}$ when it is below a fixed constant. If $T\pi\le c$, all observations are zero with constant probability, leaving the signs indistinguishable even for adaptive randomized algorithms.

For convex optimization on $[-R,R]$, take $f_\pm(x)=\pm ax$, $a=C\epsilon/R\le L$. On the common transcript, the two instances' average loss is $aR$, giving
$\Omega_\alpha((\sigma R/\epsilon)^{\alpha/(\alpha-1)})$.

For strong convexity, use $f_\pm(x)=\mu x^2/2\mp ax$, with response $\mu x-Y$, and $a=C\sqrt{\mu\epsilon}$. The recorded window $\epsilon\le c\mu R^2$ keeps both minimizers in the domain. On the common transcript, average loss is at least $a^2/(2\mu)$, giving
$$
\Omega_\alpha((\sigma^2/(\mu\epsilon))^{\alpha/[2(\alpha-1)]}).
$$
For the Lipschitz model, continue convexly with bounded slopes outside the query domain. For the global smooth strongly convex model the quadratics already qualify. At $\alpha=2$, these are the finite-variance terms.

The noise parameter here is centered, not a total-gradient moment. Exact function values are not part of this lower-bound interface. A statistical expression below a constant supplies no additional nontrivial query obstruction.

The noise-free subclass remains admissible for any noise upper bound. In the stated high-dimensional strong-convexity window, its imported arbitrary-randomized exact lower bound gives the optimization term $\sqrt\kappa S$; the rare-event construction gives the statistical term $V$. Their maximum is equivalent, up to constants, to $\sqrt\kappa S+V$. This supports expected loss and fixed-confidence loss at $\delta=1/4$, without changing the original dimension or accuracy conditions.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: 929d0c14c73cec6d9cf06863de5d2bd589301caf226f905069c6af2839f33cc6

Nontrivial scale and minimizer-containment restrictions are retained. The exact optimization term is imported separately.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: a9eb2e73f27ae3ef9d206d432550793a1b152c3b4dd0a49d2a5fba92eaae2931

Fresh stochastic gradients or subgradients with a centered moment bound; no exact value feedback.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 64598e5f5ac8dd470410dac4dc6be6680cf855f3dd59a38e2c84c0e545ed063c

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 19c468124d172f5b4cee7eb267e486d006acb6a073d4783e8b7242539ef36d0f

Centered-moment statistical lower bounds

### Native proof: FO_EXPECTATION_CONVERSION

Native pointer: /proofs/1; canonical SHA-256: b8a41e91e7b89db8a5dc97e12b571e198cd0a4bc66c50b23ba078fcc34c9f1e9

#### Native field: algorithm_scope

Native pointer: /proofs/1/algorithm_scope; canonical SHA-256: d4c7709352557c274e22876c9f4a78e23261874388e490846b713e09e550ea9e

Deterministic query policies remain deterministic.

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: a033d10e2d81409357b1254b6327d2b99291ba0a297752b0dff02b99e6ad5b4b

For a globally $\mu$-strongly convex, $\beta$-smooth objective with initial gap $\Delta$, set $R_0=\sqrt{2\Delta/\mu}$. Run the cited high-probability algorithm at accuracy $\epsilon/2$ and failure rate $\delta=\epsilon/(32\kappa\Delta)$. Its successful event includes output in $B(x^\star,2R_0)$.

Replace outputs outside $B(x_0,3R_0)$ by $x_0$. The success event is unchanged. Every retained output is within $4R_0$ of $x^\star$, so its gap is at most $16\kappa\Delta$. Expected gap is therefore at most
$\epsilon/2+\delta16\kappa\Delta\le\epsilon$.
The substituted failure rate creates the recorded logarithm. Deterministic query policies remain deterministic.

At $\kappa=1$, the objective is a known-curvature quadratic plus an unknown affine term. Averaging $b$ noisy gradients at a fixed point and taking the resulting quadratic minimizer gives expected gap at most $\sigma^2/(2\mu b)$. Integer rounding yields $O(1+\sigma^2/(\mu\epsilon))$ samples.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: 09d5cb7637612d59cd875d4abf961668926bf5d9a3977ca4fe205ae13eed405c

A generic probability guarantee without a bounded-loss truncation cannot be converted by this argument.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: fcb78d9046b7d1310d06db76b24480242d8f042ed14c645b182c34208366d831

The primary high-probability algorithm, its localization event, and the public strong-convexity radius.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f41e4d9e6f01925f402f6a4d8c431c5b54e04155a9283ac1e2ccf5cf86ccb53

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 7e75f30886c7472d8671742772da2d3a25a1d41087b6aa3b3a9fff032a624f81

SO_SRC_4a9caa6c975c30ce

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 181be3122fb8655d1f9f70619bf88c90e92c03cd92ed94c8ec2e1379839b2ef2

Probability-to-expectation conversion and the unit-condition endpoint

### Native proof: CV_ALPHA_DIMENSION_TRANSFER

Native pointer: /proofs/2; canonical SHA-256: bd27b30d3496f267dc6f46cf7870aab00fdadd895f1a148d070b4da20ee05af7

#### Native field: algorithm_scope

Native pointer: /proofs/2/algorithm_scope; canonical SHA-256: 5ea9315a7115546656e2e6138fd33a059fd95e7fd12fb1172d35a29e9ebb28d9

Unrestricted adaptive randomized algorithms, hence also algorithms without private randomness; pathwise sample budget.

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 9b27c613ba68f953d0cf3b03c248dac33e4fb6b6008303b19471ea05549ff829

Use Shamir, arXiv:2609.10874v1, Theorem 1 and its explicit construction (PDF pp.2-3,7-9; archived characters 3000-10000 and 14300-18100). Fix a sufficiently small universal relative-residual tolerance delta0 allowed by Theorem 1. Its proof constructs, for every sufficiently large condition parameter k and T=c0*k, hard symmetric A with singular values in [1,k], in dimension n<=D*T^2; c0,D are universal and independent of k. T can be rounded down. Success probability 2/3 requires Omega(k) products, even for fully adaptive randomized algorithms with the stated stronger source interface. Normalize the supplied nonzero right-hand side to norm R: relative residual and query count are invariant under rescaling b and the output. Set q=beta*R^2/epsilon, m=min(d,q), k^2=a*m, where a>0 is a sufficiently small universal constant. Choose a<=delta0^2/8 and small enough that the constructed n<=d for T=floor(c0*k). For large enough m, k meets the theorem threshold. Define f(z)=beta*||Az-b||^2/(2*k^2) on the hard coordinates and pad with unused coordinates if n<d. Its Hessian is beta*A^2/k^2<=beta*I; it is convex and globally beta-smooth. The minimizer A^{-1}b has norm<=R, so the ball optimum is zero. A target gradient is simulated by two source products, Ax and A(Ax-b), scaled by beta/k^2; no values, private information or extra native oracle are supplied. Restricting target queries to the ball only restricts the simulated source algorithm. Projecting a feasible target output onto the hard coordinates preserves the residual implication. Expected gap<=epsilon implies by Markov that P(||Axout-b||>delta0*R)<=2*k^2/(q*delta0^2)<=1/4. This yields success at least 3/4, exceeding the source's required 2/3. A target budget B induces at most 2B+1 source queries, conservatively including a final query at an unqueried output. If B were smaller than a universal multiple of k, this would contradict the source construction. Thus B=Omega(sqrt(min(d,q))) for sufficiently large m. For bounded m, the uniform extension follows from at least one necessary call: with zero calls, any feasible output X independent of the objective has, on the admissible affine pair f_plus/minus(x)=plus/minus M*x_1, maximum expected gap at least M*R; choose M>epsilon/R. Since bounded sqrt(m) is a universal constant, reducing the universal lower constant proves the displayed bound on the entire fixed target domain. Use the exact-gradient response law, whose centered alpha-moment is zero, for every sigma>=0. All initialization and simulation calls are counted. This derivation supplies the min(sqrt(d),sqrt(q)) term only, and supplies no log(2+q) lower bound in fixed dimension.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: 0bd3bc467341e357e4e323b506ad2f30576bb28beebe4b53404878df0bb50a11

Universal constants and the sufficiently-small native accuracy constant are not numerical thresholds. The old all-dimensional logarithmic term is excluded; this is not a disproof of a separately sourced logarithmic lower bound.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: e4139fa2679c03c06dfc569902bb6dbe6c1d5b3e7564b18c90092ea23e3462fc

Both fixed expected-loss views on the convex beta-smooth public ball; exact gradients are admissible at every noise upper bound.

#### Native field: source_hashes

Native pointer: /proofs/2/source_hashes; canonical SHA-256: dce4113471a4487522a475efe8d5d25a3ce026ce79f6907babfe20511be446ef

#### Native item 1

Native pointer: /proofs/2/source_hashes/0; canonical SHA-256: 3cb1ce90a4ee5add9aa74f6502fabca445b7310ff293fdf8384328776ee94f86

4cdec5889a00b9e7b2a81c80304f12e0d22bb3ef409eb46ce5d08112989e68a7

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 64598e5f5ac8dd470410dac4dc6be6680cf855f3dd59a38e2c84c0e545ed063c

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 9722122ceca4969860e7e34881288bea8dc0a040ac6c86b495a391b63a420f40

Finite-dimensional exact-gradient subclass transfer without an all-dimensional logarithm

### Native proof: CV_ALPHA_1D_BISECTION

Native pointer: /proofs/3; canonical SHA-256: aaa7d7a2228148241a3f4118e762f240ba7707e30bdfdcc825148c88690af5f3

#### Native field: algorithm_scope

Native pointer: /proofs/3/algorithm_scope; canonical SHA-256: de0711c03dd537ffd9ed80b2dc5ec65d79c8321611bb44eb1140998a8bc98bdf

Deterministic query and stopping policy, permitted in both views.

#### Native field: baseline_refs

Native pointer: /proofs/3/baseline_refs; canonical SHA-256: 0182b8315cfcbc5e9184e72d206c9cfc4047226e861f09a58792542aa08cc444

#### Native item 1

Native pointer: /proofs/3/baseline_refs/0; canonical SHA-256: cd75ae60bf93eea62ba4625b200095d6a4fc0118e906472ce2694c2eb29e1de6

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/0/sha256; canonical SHA-256: efc29b26d8ef5a7b20bb333efaf2fd0719cd97995278392b4d6e8bec18957755

efa4266c707cdadd2088f647f330c32588fda1250ec2b6be948840c5a3598889

#### Native item 2

Native pointer: /proofs/3/baseline_refs/1; canonical SHA-256: 3b362cd041c8c97a0d410449e344dca7c398fb7a05b9158ca1a57ce2002425f5

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/1/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/1/sha256; canonical SHA-256: 726902efb300f6c85c51da50d88541864079f904160ff51ef30c3baaae36b21d

b2851e6464f036e179cf00760a9eb03e4798cf9288f7874f96d135895538203b

#### Native item 3

Native pointer: /proofs/3/baseline_refs/2; canonical SHA-256: 7155ffec08e468b5b26851b469a615e4f34f6eaae771a1758b610e8af513af11

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/2/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/2/sha256; canonical SHA-256: 975371ddb620353a108569064c511fd8deb0a8ecc0ea441db27bd53e08813f44

7cf473f455c229e60b3c26db94b54b5fdbcb6c562fcf306871a72ba350f0c89c

#### Native item 4

Native pointer: /proofs/3/baseline_refs/3; canonical SHA-256: 0d4dca3800b745ba086cdf7a940d58517a0140f76e3f2df547497ca95ed11dd5

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/3/sha256; canonical SHA-256: 606808cdd0cb3c7746f549ecb7d86575a00055eece153a73db23df1b6de128f5

06a99636df76fc2e86d85a74378fd56f33894ef562c238fd59f095db63cf7210

#### Native item 5

Native pointer: /proofs/3/baseline_refs/4; canonical SHA-256: 2452f936a83f059cea4dbad8dc757492d5868316af10c1756ec4dc6fa0e82caf

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/4/sha256; canonical SHA-256: 5871ce6a11467f81f6de0ef7bf621a6db4c5993dc5943ca9f0c9c68815b52b77

c7d4764c051d3d51230e45717c2280e9901b8b393c6433cdb46558e56abcb77b

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: aeb26bf0643c78b309f0bdb1aa3f7f4016a0cfe01787e12adfd42ac1698e65ca

From the frozen centered conditional moment contract, sigma=0 implies every returned gradient equals f'(x) almost surely. In d=1 the public ball is [-R,R]. Query f'(-R); if nonnegative, convexity proves -R is an exact minimizer, so return it. Otherwise query f'(R); if nonpositive return R, an exact minimizer. These two branches handle unbounded affine slopes without assuming bounded initial gap or bounded gradient. Otherwise the continuous monotone derivative has a zero xstar in (-R,R). Maintain an interval containing a zero, initially [-R,R]. Query its midpoint. If its derivative is zero return that midpoint; if negative retain the right half, otherwise retain the left half. After k midpoint queries a zero lies in the retained interval of length 2R*2^(-k). Return its midpoint without another query. Its distance to some zero is at most R*2^(-k). Integrating the beta-Lipschitz derivative from that zero gives f(xout)-f(xstar)<=beta*|xout-xstar|^2/2<=beta*R^2*4^(-k)/2. Take k=max(0,ceil(log_4(beta*R^2/(2*epsilon)))). At most 2+k native gradient samples suffice. All points and the output are feasible, and no function values or certificate are used. The cap is pathwise even on zero-probability erroneous transcripts: stop after k midpoint steps and output the maintained interval midpoint. Hence the almost-sure loss guarantee implies the required expected loss for every admissible response law. Randomized algorithms may use this same deterministic algorithm. No hidden constant depends on dimension, precision, beta, R, sigma, mu or Delta.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: f36769768d5198bc5294bf53ca2e762474939740869d9fcc1e83a04b2dde9cc4

Valid only for d=1 and sigma=0; no positive-noise extension is asserted. The integer sample bound is exact, while its crossover with an O_alpha(sqrt(q)) theorem has unspecified constants.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: cc3f3ad98c83dfdc3dee15638041e8805f4dfc2680b1a648c624dd95a0e98629

Native target domain intersected with d=1 and sigma=0, with both expected-loss views and the same sample resource.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 6f1de694c389c354a93739d223507999485afe0f65d3b886813fd3ea36fbff34

Exact derivative bisection on the one-dimensional feasible ball

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: cd797b0c20de8c8b773ebd19a77a4d8dce8f627cda4d995d4ec269b4f32edd01

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 50d4451e43f0d78abf74f3e9e5306d4c4ec820ff81aed9e4f744f4993d158825

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: bb807494459b33105a9584dc1a6faab0596e4a06825f5314046d53b49e782464

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: a060ce91c71a971df3d137da22b2c03b0b4dcb002bafdc9c694322eea0ad2524

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 81001c3788c10f6fcfdf3b6c40f19abe8df92453f9027360912270a677b9fb44

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: b5df9b6ddee77bc56eb1adf016f81b05ed463e2107ba9ef22fb20a5db13b80de

D intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 89c743143afcc0142a5beea0914b095bb848b69aac9a6d7aeca04cb3f1dfa1bb

Unchanged baseline upper retained conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 4e2715e3ef838e656897f843b743084b701071243088e03710f8648777dbde91

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: b5df9b6ddee77bc56eb1adf016f81b05ed463e2107ba9ef22fb20a5db13b80de

D intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: bf06fb266882501153047fe749fa857759ea0a3f200219529601b1bdd8b2bf37

Retain statistical lower conditionally; use maximum with optimization term. Below-constant s adds no obstruction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 9a3ad19ba7e713e182fdce6dfd034c21416e1bb01956990e01b51182b226e1b8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 8fa84f5e36645bda43d123bb5d4f17a3640d8b0ae1ef3194039540434638c890

SO_FO_S02_cv_alpha__deterministic__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 7ce2ffc403011be78611456b754038629d72d908485e53c91080d7225ee69ce6

Inactive source-support quarantine: n=O(T^2) does not yield an all-dimensional logarithm. Historical claim preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 77e5df2486c30fe83e44f88e0897621c7b9c1337e0aa680640c22c4b61ebcf54

Full old package unsupported by cited dimension-dependent theorem.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 33ee30886e10042fc73d7b42e2a21a70b6537d1c9103a4dc8373bbe0924087e8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: b5df9b6ddee77bc56eb1adf016f81b05ed463e2107ba9ef22fb20a5db13b80de

D intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: d267711a304033ae5a17b008cfb90f74450d48df4f4b75ee431d7a8deca1cf6e

Finite-dimensional exact-oracle subclass transfer; affine endpoint covers bounded min(d,q).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: a4c5b830b6933d1daf603201f3d9aaaf87695684ac7c12ab20094cb4ccc368d7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 5941355c2fade8127af596912d75b144c1504aac917369fbbca3373bc50db9af

E does not intersect H or S in the native domain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: c9c2ebdd5e482baaab13df7c6df148ff8e80f643333d423eb8bcbf4f31ded6e3

E={D,d=1,sigma=0}

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: bb1d560e45393bc395eef2e1b196a03f3e219c86a59d0245acb6f89b27d3de10

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: da2627473f9fa8d36639d60b63687420bb62ea0dfb8acd3b1ba1de4ea4f31e24

q>=1/c>1; c,C are unspecified source thresholds. alpha is fixed, including alpha=2; no uniform alpha->1 limit.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 31503fd9c2ebcb546d3f1a7244b26ad399b34d7d9de825348519e6f6739e2db1

At sigma=0 the oracle is exact almost surely. Opposite arbitrary affine slopes preclude zero-query uniform accuracy.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 5fac6369692e00417d091be5a41cdf52a97e2bbf547ba2930812544a1a8c1f11

On H intersect S, sqrt(q)+s=Theta(s), so native c1/c2 overlap consistently.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 67a41560157c3059eb495b4b3b0fe30fdc2bbe46e8d958b6570375f1fb035915

O_alpha(1).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 97f9a55908e0b66932d7b531ac7f1e4bd03ab5b13fb239e1cc28b9da9638b9d3

Omega_alpha(sqrt(q)+s), from max of b2 and b4 on H.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 48ce3aa7a78134225df413c9b918e57962086eca91804fef0ecfe8446f96a309

Constant-factor closure of this retained guarded rate; not a strongest-literature certificate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 4919b11e1cae29889950af920bae0ae1668f68aacfd39f2ae81d0822705f8fd4

O_alpha(sqrt(q)+s)

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 42dac5b5fb339572ff59674d2a3766c43840714940485e1ed281bb133199f42a

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: cdc3ffb9d15dd339b1825dfc2973643ac3c39df3248299a27f5a712f3de8bf34

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 18441f7f6554959084f667a74db525f83ecbc5d7055a2353076182ed3aabe891

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: b7be15d637f5a6951ccaa374a00d4371e553161dc1c8f6fb067f84f1882287b5

D intersect S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 89c743143afcc0142a5beea0914b095bb848b69aac9a6d7aeca04cb3f1dfa1bb

Unchanged baseline upper retained conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 9b96bbba88a7be10d69c392e202a37ea0dda5bcb1f0bdb4b50102d9511a92fc0

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: b7be15d637f5a6951ccaa374a00d4371e553161dc1c8f6fb067f84f1882287b5

D intersect S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: bf06fb266882501153047fe749fa857759ea0a3f200219529601b1bdd8b2bf37

Retain statistical lower conditionally; use maximum with optimization term. Below-constant s adds no obstruction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 9a3ad19ba7e713e182fdce6dfd034c21416e1bb01956990e01b51182b226e1b8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 8fa84f5e36645bda43d123bb5d4f17a3640d8b0ae1ef3194039540434638c890

SO_FO_S02_cv_alpha__deterministic__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 7ce2ffc403011be78611456b754038629d72d908485e53c91080d7225ee69ce6

Inactive source-support quarantine: n=O(T^2) does not yield an all-dimensional logarithm. Historical claim preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 77e5df2486c30fe83e44f88e0897621c7b9c1337e0aa680640c22c4b61ebcf54

Full old package unsupported by cited dimension-dependent theorem.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 2127d0f37210bc148281d94dfcccb4eaa330dcc072869f1da83d9aa88da07eee

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 7370d5e4fd63646548ce7d4245326288014104f12f338cc64caf37a495695edc

s>=sqrt(q) dominates this new term.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: a4c5b830b6933d1daf603201f3d9aaaf87695684ac7c12ab20094cb4ccc368d7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 5941355c2fade8127af596912d75b144c1504aac917369fbbca3373bc50db9af

E does not intersect H or S in the native domain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: c9c2ebdd5e482baaab13df7c6df148ff8e80f643333d423eb8bcbf4f31ded6e3

E={D,d=1,sigma=0}

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: bb1d560e45393bc395eef2e1b196a03f3e219c86a59d0245acb6f89b27d3de10

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: da2627473f9fa8d36639d60b63687420bb62ea0dfb8acd3b1ba1de4ea4f31e24

q>=1/c>1; c,C are unspecified source thresholds. alpha is fixed, including alpha=2; no uniform alpha->1 limit.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 31503fd9c2ebcb546d3f1a7244b26ad399b34d7d9de825348519e6f6739e2db1

At sigma=0 the oracle is exact almost surely. Opposite arbitrary affine slopes preclude zero-query uniform accuracy.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 5fac6369692e00417d091be5a41cdf52a97e2bbf547ba2930812544a1a8c1f11

On H intersect S, sqrt(q)+s=Theta(s), so native c1/c2 overlap consistently.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 67a41560157c3059eb495b4b3b0fe30fdc2bbe46e8d958b6570375f1fb035915

O_alpha(1).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 17dc8585d6d8760672a142792266eb72473292f09afb02e042b86901e6050123

Omega_alpha(s)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 48ce3aa7a78134225df413c9b918e57962086eca91804fef0ecfe8446f96a309

Constant-factor closure of this retained guarded rate; not a strongest-literature certificate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: b4900b65a56c9b55c34c4e6211e03e2c368437e43c352841013aefc22be6b8ed

O_alpha(s)

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 37e74cf25e41d38aade3e3b90ae4e55cbec95295964987f0c279742a8e0158e3

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: a0b572ceaef9cdbe5fcdb0e0fd6eeab21dd7732837893101d3c9c962d6d77cf4

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: fcd68c34deb17114de72391f531f3c9cbc1de179c0bb5a09b3ca4a9e2108a8b8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 3bd4b3b790d4ada72a043bedd8d4bcbcd53a387fc171b1ecb461b92db9e67aba

D outside H union S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: d4c830b9b0a71fae446c02aeffc4c7b41c145ffbc6fb5127d1fb8e2fbf4a59b2

Retain unchanged upper and minimize with b5 on E.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 0c36c07416c8621ef13eba45eac5e1c88ff514563bcc065e8d1a95afddf237b6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 3bd4b3b790d4ada72a043bedd8d4bcbcd53a387fc171b1ecb461b92db9e67aba

D outside H union S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: bf06fb266882501153047fe749fa857759ea0a3f200219529601b1bdd8b2bf37

Retain statistical lower conditionally; use maximum with optimization term. Below-constant s adds no obstruction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 9a3ad19ba7e713e182fdce6dfd034c21416e1bb01956990e01b51182b226e1b8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 8fa84f5e36645bda43d123bb5d4f17a3640d8b0ae1ef3194039540434638c890

SO_FO_S02_cv_alpha__deterministic__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 7ce2ffc403011be78611456b754038629d72d908485e53c91080d7225ee69ce6

Inactive source-support quarantine: n=O(T^2) does not yield an all-dimensional logarithm. Historical claim preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 77e5df2486c30fe83e44f88e0897621c7b9c1337e0aa680640c22c4b61ebcf54

Full old package unsupported by cited dimension-dependent theorem.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: ff3e3eecf678e9aad0e6afc816b1b597d8e02cc7cf2c92c4d772572d694b0e30

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 3bd4b3b790d4ada72a043bedd8d4bcbcd53a387fc171b1ecb461b92db9e67aba

D outside H union S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: d267711a304033ae5a17b008cfb90f74450d48df4f4b75ee431d7a8deca1cf6e

Finite-dimensional exact-oracle subclass transfer; affine endpoint covers bounded min(d,q).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: b581342ab9da32fcbed862cdfbf29094a2367171643f062f0719f8040db33254

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 99f66691a3c3b52a9fcaefa24115a72cbea177ec88a1be546c4c0f99c6edd6c5

E within c3, in guarded minimum

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: cd9619aba8a1495abfe37e5275443ae970d11b2191bf930ceda0da81e629ed03

Endpoint checks and derivative bisection; exact integer cap K(q), no positive-noise extension.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: c9c2ebdd5e482baaab13df7c6df148ff8e80f643333d423eb8bcbf4f31ded6e3

E={D,d=1,sigma=0}

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 13a631ca91cb0027653b3cfff2415a6695b6bb7ed375bc462216314bb24e8f90

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: da2627473f9fa8d36639d60b63687420bb62ea0dfb8acd3b1ba1de4ea4f31e24

q>=1/c>1; c,C are unspecified source thresholds. alpha is fixed, including alpha=2; no uniform alpha->1 limit.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 31503fd9c2ebcb546d3f1a7244b26ad399b34d7d9de825348519e6f6739e2db1

At sigma=0 the oracle is exact almost surely. Opposite arbitrary affine slopes preclude zero-query uniform accuracy.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/boundary_checks/2; canonical SHA-256: 13c0e8599f3d88ab6b5b967532d28529fcdf070638c427a14670d85cf366954f

On E, endpoint signs handle steep affine objectives; bisection gives K(q)=2+max(0,ceil(log_4(q/2))). No finite-call saturation or logarithmic lower is assumed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/fixed_parameters/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: ae078fd4dddcb5b192c6a316baa61020ce7dab265f697a704206ca7e20e26de6

Guarded upper divided by max(c_alpha*s,c0*min(sqrt(d),sqrt(q))). O(log(2+q)) on E; otherwise O_alpha((sqrt(q)+s)/max(s,min(sqrt(d),sqrt(q)))).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: dbf3e989c5b13dc14e3fd4057159a6863fede6073119cc22b3b6a2060f5d25ed

max(c_alpha*s,c0*min(sqrt(d),sqrt(q))); on E this is Omega(1).

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 036d52bb343da2d2d60aab58b59a4ce8cef7ec709d9a0be65be547265a5fe31a

Quantified gap, including O(log(2+q)) ratio on E. Independent log lower and sharper noisy/d>1 rates remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: d8b3c112dfdc8d46119f2d690309790bf105d01d6d3ae1eb4e992575e83d6065

On E: min(C_alpha*sqrt(q),K(q)); otherwise C_alpha*(sqrt(q)+s). K(q)=2+max(0,ceil(log_4(q/2))).

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 4c73969036b2584e7a472c8cdc5db66a6054886494262d64e1d6836e3b287d19

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 04b3c3ee5315c5bd450335d1bff31e66caeb463abeef483e051e79f757bb3336

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: a3d43b2dce7e7f82d8e204d90333ea98206eca51535fabb6e203597be3c58628

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: b5df9b6ddee77bc56eb1adf016f81b05ed463e2107ba9ef22fb20a5db13b80de

D intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 89c743143afcc0142a5beea0914b095bb848b69aac9a6d7aeca04cb3f1dfa1bb

Unchanged baseline upper retained conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 1fa1ec1a457ca5ac1f18e862ff45ec983661b803e99734202bcee31c341bc96a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: b5df9b6ddee77bc56eb1adf016f81b05ed463e2107ba9ef22fb20a5db13b80de

D intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: bf06fb266882501153047fe749fa857759ea0a3f200219529601b1bdd8b2bf37

Retain statistical lower conditionally; use maximum with optimization term. Below-constant s adds no obstruction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 84aa8b145f559bbebefb524521bc63422620448be96a2f52cfc1a584864efe90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: f1986060a6cb60f42ee69d9dbcbba077dfbf06326df9f436cb0eee4bbcbea29b

SO_FO_S02_cv_alpha__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 7ce2ffc403011be78611456b754038629d72d908485e53c91080d7225ee69ce6

Inactive source-support quarantine: n=O(T^2) does not yield an all-dimensional logarithm. Historical claim preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 77e5df2486c30fe83e44f88e0897621c7b9c1337e0aa680640c22c4b61ebcf54

Full old package unsupported by cited dimension-dependent theorem.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 4f2dc53aaf25eeebd90db846a444df513087f3484e7b8b3104a7c10de31d5469

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: b5df9b6ddee77bc56eb1adf016f81b05ed463e2107ba9ef22fb20a5db13b80de

D intersect H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: d267711a304033ae5a17b008cfb90f74450d48df4f4b75ee431d7a8deca1cf6e

Finite-dimensional exact-oracle subclass transfer; affine endpoint covers bounded min(d,q).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: bff9f0f0abb600148e317b6c06cb43efa3418a02057f9ccdafabf07885595e5e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 5941355c2fade8127af596912d75b144c1504aac917369fbbca3373bc50db9af

E does not intersect H or S in the native domain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: c9c2ebdd5e482baaab13df7c6df148ff8e80f643333d423eb8bcbf4f31ded6e3

E={D,d=1,sigma=0}

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: bb1d560e45393bc395eef2e1b196a03f3e219c86a59d0245acb6f89b27d3de10

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: da2627473f9fa8d36639d60b63687420bb62ea0dfb8acd3b1ba1de4ea4f31e24

q>=1/c>1; c,C are unspecified source thresholds. alpha is fixed, including alpha=2; no uniform alpha->1 limit.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 31503fd9c2ebcb546d3f1a7244b26ad399b34d7d9de825348519e6f6739e2db1

At sigma=0 the oracle is exact almost surely. Opposite arbitrary affine slopes preclude zero-query uniform accuracy.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: 5fac6369692e00417d091be5a41cdf52a97e2bbf547ba2930812544a1a8c1f11

On H intersect S, sqrt(q)+s=Theta(s), so native c1/c2 overlap consistently.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/fixed_parameters/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 67a41560157c3059eb495b4b3b0fe30fdc2bbe46e8d958b6570375f1fb035915

O_alpha(1).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 97f9a55908e0b66932d7b531ac7f1e4bd03ab5b13fb239e1cc28b9da9638b9d3

Omega_alpha(sqrt(q)+s), from max of b2 and b4 on H.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 48ce3aa7a78134225df413c9b918e57962086eca91804fef0ecfe8446f96a309

Constant-factor closure of this retained guarded rate; not a strongest-literature certificate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 4919b11e1cae29889950af920bae0ae1668f68aacfd39f2ae81d0822705f8fd4

O_alpha(sqrt(q)+s)

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 6daaee7e942c1382d02b0f6318e7b0dc99d216c4992334c4366e1d69828b01bd

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 3f2cd7e1634bc539526e21d458959aaf5123f1d97420eee2f52d74f42c6ece9d

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 422ce653cd6cbf866a828c82ecedb40379af31c9d6042e4f260e1bca23b86ccb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: b7be15d637f5a6951ccaa374a00d4371e553161dc1c8f6fb067f84f1882287b5

D intersect S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 89c743143afcc0142a5beea0914b095bb848b69aac9a6d7aeca04cb3f1dfa1bb

Unchanged baseline upper retained conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: dd6263f6c8773ebaae7f8a6f6eb10e4ed0f1bc01e6aae80f639b615c1a5e3f94

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: b7be15d637f5a6951ccaa374a00d4371e553161dc1c8f6fb067f84f1882287b5

D intersect S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: bf06fb266882501153047fe749fa857759ea0a3f200219529601b1bdd8b2bf37

Retain statistical lower conditionally; use maximum with optimization term. Below-constant s adds no obstruction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 84aa8b145f559bbebefb524521bc63422620448be96a2f52cfc1a584864efe90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: f1986060a6cb60f42ee69d9dbcbba077dfbf06326df9f436cb0eee4bbcbea29b

SO_FO_S02_cv_alpha__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 7ce2ffc403011be78611456b754038629d72d908485e53c91080d7225ee69ce6

Inactive source-support quarantine: n=O(T^2) does not yield an all-dimensional logarithm. Historical claim preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 77e5df2486c30fe83e44f88e0897621c7b9c1337e0aa680640c22c4b61ebcf54

Full old package unsupported by cited dimension-dependent theorem.

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: f369807be7e0de158d51d8f59f67ea3b63919c7e4df115665603512120df4f3e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: 7370d5e4fd63646548ce7d4245326288014104f12f338cc64caf37a495695edc

s>=sqrt(q) dominates this new term.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: bff9f0f0abb600148e317b6c06cb43efa3418a02057f9ccdafabf07885595e5e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: 5941355c2fade8127af596912d75b144c1504aac917369fbbca3373bc50db9af

E does not intersect H or S in the native domain.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: c9c2ebdd5e482baaab13df7c6df148ff8e80f643333d423eb8bcbf4f31ded6e3

E={D,d=1,sigma=0}

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: bb1d560e45393bc395eef2e1b196a03f3e219c86a59d0245acb6f89b27d3de10

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: da2627473f9fa8d36639d60b63687420bb62ea0dfb8acd3b1ba1de4ea4f31e24

q>=1/c>1; c,C are unspecified source thresholds. alpha is fixed, including alpha=2; no uniform alpha->1 limit.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 31503fd9c2ebcb546d3f1a7244b26ad399b34d7d9de825348519e6f6739e2db1

At sigma=0 the oracle is exact almost surely. Opposite arbitrary affine slopes preclude zero-query uniform accuracy.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/boundary_checks/2; canonical SHA-256: 5fac6369692e00417d091be5a41cdf52a97e2bbf547ba2930812544a1a8c1f11

On H intersect S, sqrt(q)+s=Theta(s), so native c1/c2 overlap consistently.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/fixed_parameters/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 67a41560157c3059eb495b4b3b0fe30fdc2bbe46e8d958b6570375f1fb035915

O_alpha(1).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: 17dc8585d6d8760672a142792266eb72473292f09afb02e042b86901e6050123

Omega_alpha(s)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 48ce3aa7a78134225df413c9b918e57962086eca91804fef0ecfe8446f96a309

Constant-factor closure of this retained guarded rate; not a strongest-literature certificate.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: b4900b65a56c9b55c34c4e6211e03e2c368437e43c352841013aefc22be6b8ed

O_alpha(s)

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: 9d1dc06b4d2b05b81c404268eef1a5c32574432def795d64db8fc3afed0957db

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 31b0b4dbf2255e0d4be8c8f30e52aa1811b473c649a4e6ede60e50fe359d2b87

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: dde5a6394ddec7b0a008cbf780bf13d39faf138e9f3943cc23a123156401b1aa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: 3bd4b3b790d4ada72a043bedd8d4bcbcd53a387fc171b1ecb461b92db9e67aba

D outside H union S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: d4c830b9b0a71fae446c02aeffc4c7b41c145ffbc6fb5127d1fb8e2fbf4a59b2

Retain unchanged upper and minimize with b5 on E.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: b3c3137d0dcd48aa24407ebff9de905ff7302a29e99010c0f09c59ded38aefec

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: 3bd4b3b790d4ada72a043bedd8d4bcbcd53a387fc171b1ecb461b92db9e67aba

D outside H union S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: bf06fb266882501153047fe749fa857759ea0a3f200219529601b1bdd8b2bf37

Retain statistical lower conditionally; use maximum with optimization term. Below-constant s adds no obstruction.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 84aa8b145f559bbebefb524521bc63422620448be96a2f52cfc1a584864efe90

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: f2953d2931e36d0c55640f51865f8394ebe52194765d04e521017232558f871c

None

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: f1986060a6cb60f42ee69d9dbcbba077dfbf06326df9f436cb0eee4bbcbea29b

SO_FO_S02_cv_alpha__randomized__expected_loss__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 7ce2ffc403011be78611456b754038629d72d908485e53c91080d7225ee69ce6

Inactive source-support quarantine: n=O(T^2) does not yield an all-dimensional logarithm. Historical claim preserved.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: 77e5df2486c30fe83e44f88e0897621c7b9c1337e0aa680640c22c4b61ebcf54

Full old package unsupported by cited dimension-dependent theorem.

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: 96093e0bb252bc797a6f77f498dd3047a9a22db8420419871168c8b0c619e2c3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: 3bd4b3b790d4ada72a043bedd8d4bcbcd53a387fc171b1ecb461b92db9e67aba

D outside H union S

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: d267711a304033ae5a17b008cfb90f74450d48df4f4b75ee431d7a8deca1cf6e

Finite-dimensional exact-oracle subclass transfer; affine endpoint covers bounded min(d,q).

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 8f097023401b3d58704c1f3abea8ec2eba57c387f09d10125cd66076afd13b1e

D

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: a70e0a5dfa2376f6fc048f01228911ec96912fe4afc8b7ab1d460f47529701da

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: 99f66691a3c3b52a9fcaefa24115a72cbea177ec88a1be546c4c0f99c6edd6c5

E within c3, in guarded minimum

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: cd9619aba8a1495abfe37e5275443ae970d11b2191bf930ceda0da81e629ed03

Endpoint checks and derivative bisection; exact integer cap K(q), no positive-noise extension.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: c9c2ebdd5e482baaab13df7c6df148ff8e80f643333d423eb8bcbf4f31ded6e3

E={D,d=1,sigma=0}

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 13a631ca91cb0027653b3cfff2415a6695b6bb7ed375bc462216314bb24e8f90

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: da2627473f9fa8d36639d60b63687420bb62ea0dfb8acd3b1ba1de4ea4f31e24

q>=1/c>1; c,C are unspecified source thresholds. alpha is fixed, including alpha=2; no uniform alpha->1 limit.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: 31503fd9c2ebcb546d3f1a7244b26ad399b34d7d9de825348519e6f6739e2db1

At sigma=0 the oracle is exact almost surely. Opposite arbitrary affine slopes preclude zero-query uniform accuracy.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: 13c0e8599f3d88ab6b5b967532d28529fcdf070638c427a14670d85cf366954f

On E, endpoint signs handle steep affine objectives; bisection gives K(q)=2+max(0,ceil(log_4(q/2))). No finite-call saturation or logarithmic lower is assumed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/fixed_parameters/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: ae078fd4dddcb5b192c6a316baa61020ce7dab265f697a704206ca7e20e26de6

Guarded upper divided by max(c_alpha*s,c0*min(sqrt(d),sqrt(q))). O(log(2+q)) on E; otherwise O_alpha((sqrt(q)+s)/max(s,min(sqrt(d),sqrt(q)))).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: dbf3e989c5b13dc14e3fd4057159a6863fede6073119cc22b3b6a2060f5d25ed

max(c_alpha*s,c0*min(sqrt(d),sqrt(q))); on E this is Omega(1).

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 036d52bb343da2d2d60aab58b59a4ce8cef7ec709d9a0be65be547265a5fe31a

Quantified gap, including O(log(2+q)) ratio on E. Independent log lower and sharper noisy/d>1 rates remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: d8b3c112dfdc8d46119f2d690309790bf105d01d6d3ae1eb4e992575e83d6065

On E: min(C_alpha*sqrt(q),K(q)); otherwise C_alpha*(sqrt(q)+s). K(q)=2+max(0,ceil(log_4(q/2))).

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 8ab69d6ea0aefbc19e7a10004463c3ec467a2d8a70c85b9b20f8b479ab0446e7

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: fc560dfcfab9b61f32541c533ba6e726190aeb46eaa0613210dcaa1a7d908136

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: b8b0e81ca631d018c103e31eac9963e895c1ce1d26ff100c7d45514b38fb1bd7

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: a5b1c94a7c8628d5e1d5acda4006187a3306ac8fa6570d0fefdfd19749c948bf

hd_and_statistics

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 782a1c2278788c3ca09f58ad5eb87de8f70ea6a7454561a4c75a114e72888756

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/2; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: fbe3b63541958d56a1fabadfc446907a3129d89aa226fe73b3d4906e129954f9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/2; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/3; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: ca25512dfa8cd3497e0a8b3e2d43b4b36fe2d275e77bff87eab054bb530c0810

Overlap rates agree since sqrt(q)+s=Theta(s); H is source applicability, not an intrinsic phase transition.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 635ccf97cbd8c8151a56e5de408af92775d34f457fc7628f8b0f754728a18ef8

D intersect H intersect S, where H={d>=C*q} and S={s>=sqrt(q)} use the native universal C and native guards.

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: b63703b93a09582324922147418fb1ef3a55262c1319bb9fbd93275078a76daa

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 9b00016e6f20d39da1be1f77a5ec4596e20177c0283470fd954972c9504eaee4

hd_without_statistics

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 782a1c2278788c3ca09f58ad5eb87de8f70ea6a7454561a4c75a114e72888756

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/2; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 16a668ce8de892ca064f7323e3081a73158b8387d95ff5d8c914f23c19986c35

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 293f621e0ec9460edd4d89b8af8ee4375ce73a308d11f689049cfef52fdfa5ea

Retained b1,b2 and new b4 match in order.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 1dfc0089cd6b8179c88e6a85bc1ba7f28fe2715ba9ca04fd21003000bbb021c2

D intersect H intersect not S

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: c35c96d000c368ba6e3208536a1658c01cdea81dd901b0a53c603c0011dce744

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 24fec056ebf81c415ca769694ac16fc2d75a506fd76441fdcf4b346e2455a06d

statistics_without_hd

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: eccd3ee30a1655e71d36da4ec289959c6342e69aa9f499a2742150dc3f8234cf

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/0; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/1; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: d46312abc79efa7d5fb1fc6dddef2ae876b5a0a863efaf4e322707f84f1ebd9e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: b578ea3b996007519aaca35677027c2c2014dde65d6c99b4ada615cb03ed9421

Retained b1,b2 match; b4 is dominated.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 96b8e1868fbb70e8af6683b737517f0caa63041b96fabcd972a729cd4341ec48

D intersect not H intersect S

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: b8295644ef10113c9b6ffa09ca10e8aa201bbf0e3ea74d1a18a29a8d39c1919c

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 1fb8de03d4374c2ecbb2260e94a22c36eb1e24f9ef44da9f1564e2b418b9a238

remainder_exact_1d

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 0edbd4affac2ee8e710754153db988b1a17b66e5943220e36639da14df46a050

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/1; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: c34d3927f58546247e274942622c6ad2fe46b3dadb8b61c37145533065aa45e0

Guarded bisection upper O(log(2+q)); supported lower only Omega(1). No matching logarithmic lower adopted.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 81ec7135031f8ffc948f95c7041284458b67655d5c53e609a3a307342d9aae72

D intersect not H intersect not S intersect {d=1,sigma=0}

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: 0b1b4d84967d76934ed6500a5cfd731c74b7c2c5fa6e0a191fafb10113a221fb

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 4f4d92f362698202f46c8efc08149af92c53fda250ca82e13c55f98e930bd4ed

remaining_lowdim_lownoise

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 0edbd4affac2ee8e710754153db988b1a17b66e5943220e36639da14df46a050

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/1; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 93b8ff791765a88291c2bf45b0cb30f8d509f9162d5f5296952adadbadd43651

Recorded upper O_alpha(sqrt(q)+s), lower Omega_alpha(max(s,min(sqrt(d),sqrt(q)))); sharper results unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 146be07a695bd3733cf22933950046fb67ece0beae032a273ed7974d2af4c64e

D intersect not H intersect not S intersect not {d=1,sigma=0}

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: f60c44bb4781ec788d64cc50fdc618a6c2f873f857207996dc5ad121ae33d68b

Partition by H={d>=C*q}, S={s>=sqrt(q)} and their complements; split not H and not S by E={d=1,sigma=0}. These Boolean cells exhaust D. Native c1/c2 overlap consistently. E lies in c3 because q>=1/c>1,C>1 and s=0. No numerical value or intrinsic transition is assigned to c,C.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 2912531bb67561fcdb553a6c060aef77c9d2eee9b945f2da2b22ce03d6168c33

No residual inside D. Outside D is outside this immutable contract, including epsilon=0. Sharper-rate research remains unassessed.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 61b65b54e304f52119fdb65c7ebdc56583b987ea3833c92946f93da178c29457

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: d9b71b899606655de019e49a64241c5d01af22d860af587b356d7891ce268090

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: e021a07e697dd12c0d5fe0de83682e9b47a0d8897131e21d9d7ff7cb6a3eca10

The source spends dimension O(T^2). A new explicit ball/expected-loss transfer proves the dimension-sensitive min term, not a fixed-dimensional logarithm. Quarantine preserves history and removes active b3 references. The lower weakens where log(2+q) asymptotically exceeded both surviving terms.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 290681f6b62c6cccea0ac831830afa79acd2d0ac38239baca9ece9b2797e45db

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: cc141fda8bd04fa2110ac4b890279a3aa4c05ecc7dc24aa2677486d65dfc9cb5

cv_alpha_dimension_support_correction

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 1b8b7fe11605c23cf2551afdaa2be1166a06ae15ad10f03f6556e93d52855a57

None: this corrects lower support rather than claiming a stronger lower bound.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: ec1f34862557884ced9ee99fc1c93e493d04d2d43824d08549791a2a4423894f

Replace inactive b3 by b4=Omega(min(sqrt(d),sqrt(q))). c1 rate unchanged; c3 lower=max(c_alpha*s,c0*min(sqrt(d),sqrt(q))).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 0928362772d32b4de4926003329300c65a9a2927b6e66928417181aff6a89f2d

c1: Theta_alpha(sqrt(q)+s); c3 lower=max(c_alpha*s,c*max(min(sqrt(d),sqrt(q)),log(2+q))).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 73932469ebdaaa5407d087a49d5fb83c2a4de7e64f4a2edcdbfcd9c3e59483b9

Constant-factor main rates on H or S, and any asymptotic window where max(s,min(sqrt(d),sqrt(q))) already dominates log(2+q).

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: b4a2d98c5def90bc2ea1c4576bf7f091f413d1cf8c48a809c9ea38b88fc22075

D in each native view.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 4056840655587dfd3bdfe8d7e621b85cec5c9bba76a8f0c938d63b0362ce398c

d=1,sigma=0,q tending to infinity: the old unsupported lower grows as log(q), whereas the supported replacement lower is constant.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 9c567cfa4e0231ff95d18a73bc4d1b1cb56c3fdd4fc6ba1e0a4d111e15644587

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 9d3739fbb40d768ba176d8f342190e551b5fe5cd5016e94bce9b315a8277e1b3

CV_ALPHA_1D_BISECTION proves error<=beta*R^2*4^(-k)/2 after k midpoint samples and <=2 endpoint samples. Same native expected loss and pathwise budget. No matching lower claimed.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 0edbd4affac2ee8e710754153db988b1a17b66e5943220e36639da14df46a050

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: e526685e1d40f5cffe7e78f18ee2803df21fd846df51dcd05e22e25158fa9eeb

cv_alpha_exact_1d_bisection

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 02e50a24febf9c495a2c6e140b3fe86bd9c6453613027b0744c1adc21cbc2f4c

E as q tends to infinity, where log(q)=o(sqrt(q)); no numerical crossover against the unspecified baseline C_alpha is asserted.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: e540926c486ef1f37a3108d2091bd5168a1c36e8827ab8b1624a60ddc4c17c98

On E use min(C_alpha*sqrt(q),K(q)), K(q)=2+max(0,ceil(log_4(q/2))); elsewhere retain the old upper. Lower is independently corrected by the separate finding.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 35ec2af110e126cdd63b3cc1758950dffd65d448b724cf806b671cf08496e77a

Upper C_alpha*(sqrt(q)+s), in particular C_alpha*sqrt(q) on E.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 5ac69bfb9277708244856acc5707b154d1c2584b08626a3480e2d0bf9793a779

D outside E; inside E where the retained bound is smaller, the guarded minimum retains it.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: d8911c30207d52cb1c76618e8f4b027b4006efcd0c215eaf172a8a7f9fb3e0ce

Exactly E={D,d=1,sigma=0}.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 4a88c180e72b08b3209075c9fb41e1e3afd8a3c02e49a1cf4a59cdf3695265d2

Fix alpha,beta,R, take d=1,sigma=0 and epsilon decreasing to zero. K(q)/sqrt(q) tends to zero.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 03d93cded5abdc3713a5f7b68536456b2cfb3196839e9c6749fadb29d12ae6f1

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 41423da5fbef31b409b3dad13ef0b03268b7b1fdbf4acccb5f22c4024e9b0a8f

Presentation only, grounded in fully read exact frozen arrays. It independently changes no science.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/impact/2/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/impact/2/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/impact/2/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/impact/2/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 9b5e69cafd87137ebc29afead53e9cab70e6bfd9d795aed7bc9331fa2ed8e8f0

cv_alpha_first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 901539ea6d8e7caef2c8d39bad16f08c7005499128b598736f618924f4bac484

No independent scientific improvement is attributed to this annotation.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 34ea01a324376248b94ebed42011e8dd327475294e9195edfbb02794d2fd366b

Joint target/domain/candidate accounting; scientific changes covered by the two separate material findings.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 2657e04cc029b4aafe3d875bca60deb9b65990e6c7089883f2bbf6bd551bf590

Six native guarded comparisons without joint annotation.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: a2875152fae3cd8f6d4b17fceb7c21d117cd3e42054dc365a8a337157090c42a

All scientific content except the deltas justified by the two separate material findings.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 76cac5edcf0b74e93eea5fc6e3b5e183d62e5775b684984555d00d73d5b8dd5c

D; all six registered comparisons are considered separately by native view and quantity.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: eeace1aaf54ba590505dc4ab1413c56f5d1a205210a506fd134c4ebd80ac1375

H/S overlap, E, fixed-alpha constants and unused mu/Delta bookkeeping are explicit.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: a20809b1bdea4da3741ee678d1424d8299dfb9299056caee557a15624dd27d19

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 9d9f9174f6e6336f8b44424a45dc3378b8c57c28e1e86e1c479d8b781ae0d6e6

Terminal exact-ID search and theorem reading screen the named route; unchanged applicability is conditionally retained. No literature-exhaustion claim.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/impact/3/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 0caca01dd92da8f505bf528fe3db92972dee9cdcf5bbff7270a00f927e348b4d

cv_alpha_registered_upper_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 637ff02cbd44f30f7b8527a86c397ef74485963719a22cd6c44cf668e9594c66

None found in this named-source check.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: b3e7d9d59536a912e0324459bd6b40d3a82dd2508b527443cfa0a67586d7a340

No additional main-rate upper is adopted from the inspected Theorem 2(i).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 7920e027b3287564da3eaca1d6435c2cef6f6cf28b5a2f27dbe382b0c3b992c4

Registered b1 upper O_alpha(sqrt(q)+s).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: c47fdb6de229858fe1430e30305d4d773ddfbd4e51f20ab3d87f9f9a5fa6cb3e

All uses of unchanged b1.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 66593609e812827975625687a8175c86044ec12662b60144cdc148e65a28284b

The inspected bounded-domain heavy-tailed expected-loss theorem and its registered native intersection.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 4eb996f7ffd55ce1481df782f1a02b4ca6a1d0dc9ab5f470e169a28440a983e2

arXiv metadata identifies v2 dated 2026-09-21; inspected Algorithm 2/Theorem 2(i) at source characters 24600-28900 contains the registered smooth-plus-noise route.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 9688cc4ca194dc0599fd50194702b9de7c5fa91e45bfcbc51925e19350c0c26b

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/impact/4/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/impact/4/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 52a1c50b77737cc53ef3b3ea72ac0bd3845de55ea1ea4cfe875ab6b2779e740f

curated_feedback_SO_FO_S02_cv_alpha_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 53fd8c574a6c785ab5e9764d69975200ef72366239ac7570323a32c9a7b0c78d

For each fixed alpha in (1,2]: d integer>=1, beta,R>0, sigma>=0, 0<epsilon<=c*beta*R^2 (native sufficiently-small universal c). Separate native minimax sample counts, expected gap g1, pathwise budget, feasible output. Native metadata also tracks mu,Delta though the convex-ball contract does not use them: retain these dummy axes, impose no strong-convexity/initial-gap assumptions, and require uniformity in their positive values.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: c70042b53ceef6b9579df7446b5b3d076c48a21b31ac71cdb70939792df518e3

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/impact/5/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/impact/5/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/impact/5/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/impact/5/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: b3c0a050dba057ee9041dc14cba51c570280386b8c250c31051b53259cbc45dc

curated_feedback_SO_FO_S02_cv_alpha_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: 53fd8c574a6c785ab5e9764d69975200ef72366239ac7570323a32c9a7b0c78d

For each fixed alpha in (1,2]: d integer>=1, beta,R>0, sigma>=0, 0<epsilon<=c*beta*R^2 (native sufficiently-small universal c). Separate native minimax sample counts, expected gap g1, pathwise budget, feasible output. Native metadata also tracks mu,Delta though the convex-ball contract does not use them: retain these dummy axes, impose no strong-convexity/initial-gap assumptions, and require uniformity in their positive values.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 1860af94ca11e9d7fa6a0aa0d83c08d3d8a9d30bd42c9bede727a131a285488e

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 2fe529ec8f5489f320bec63b340c49a880b779b01e07e2bd6ffdb9f602cbe7d9

Seek independent support for an all-dimensional logarithmic lower bound on the smooth convex ball; the old source alone does not establish it, so both b3 rows remain inactive pending such evidence.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 2bde1efb57ddef6548045c109891a2c7476b98a3397ecfa0c6595bfc0fdfa6e9

Sharper positive-noise and multi-dimensional low-dimensional upper/lower envelopes were not searched beyond the two named baseline sources; present gaps are recorded bounds, not certified literature gaps.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 67f2f66534648dbfe1d27b1517d836f92a343b1b9e1cb8389bde815baf9f2026

Native tracked mu and Delta are unused by the scientific contract. They remain unchanged and all proposed rates are uniform in them; optional future metadata cleanup requires its own controlled normalization review.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 6ff18363e0610c0a0e82956ea1be93a88fd08a9e0ae5183b38dfea68b9043b27

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 9a5d88349fdb1fdfdccf326711fd5bb8b5e874703c35e8f6a561efeb5e7de518

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 1f1aff41ead58623d668199502c9eb7b3c311c3a790e4bbb6eb6ef73b281b2fc

Identity retention only; no fresh recertification or cross-quantity merge.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 340334e441e37fece19845cfdd7f78e71848b0afa54e3f1209ba66af6ddf190f

Unchanged frozen bound premises, retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: e5b323ed9b121c45947a6bbdf1be31ae959c375b761d3eb3ea9e0e11f40542b1

Frozen native e1: upper Theorem 2(i), Eq.(33).

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: daee4d141bf23a61dbbcec8e610b53347ac68f173f83222f8c6f45ee598a98ac

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 2e6846fbebd4f9c4ef0126bb71b79564ad6a196af83cd1db3794bbe20ddd9f03

SO_SRC_a73fce82d651b459

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 592c945c4377776a57a040b6f7728747634924c7a24346f57c0207653a78c7b9

D in the same native view/guarantee/quantity/resource.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 4842841514d3868d375bcfe293a6c641afbbc9b073a4609e760b4daaef647b4b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 1f1aff41ead58623d668199502c9eb7b3c311c3a790e4bbb6eb6ef73b281b2fc

Identity retention only; no fresh recertification or cross-quantity merge.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/provenance/1/proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 340334e441e37fece19845cfdd7f78e71848b0afa54e3f1209ba66af6ddf190f

Unchanged frozen bound premises, retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 393b46558ef1e68f24f145480907e5f128e8b51832b1f5b38be7b3b86eebb597

Frozen native e2 and its proof_refs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 5faaca4d5a3788ad2da4feb854c7395b3245bd3cdd11a0dc4f6f19d78a9ee825

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native item 2

Native pointer: /joint_analysis/provenance/1/source_refs/1; canonical SHA-256: 7e75f30886c7472d8671742772da2d3a25a1d41087b6aa3b3a9fff032a624f81

SO_SRC_4a9caa6c975c30ce

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 592c945c4377776a57a040b6f7728747634924c7a24346f57c0207653a78c7b9

D in the same native view/guarantee/quantity/resource.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: cad850474d8fd1c54cb5cdefe3ba6c4a5a3ec3fd5acba9bf0d5ad9ebe035bc37

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: b27b0a8d707ddf01c4aefc4373fb3ec330eac3142726bca856fb0842fb3c2e2f

Ball-contained scaled least squares, two matvecs/gradient, Markov conversion, dimension calibration, affine endpoint; complete proof in CV_ALPHA_DIMENSION_TRANSFER.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 1a03f4c889bf5dfedefbce12a85e050136cecdf5ae38046caf1e31394d89ea52

Randomized adaptive matvecs, fixed small relative residual, large condition k, n=O(T^2).

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 79f799ce8deb32e6b8a1e473863ba88900cbdda428aae29f89703bb2d40eefb4

Shamir arXiv:2609.10874v1, Thm.1/reduction pp.2-3, Eq.(7)/conclusion pp.7-9; chars 3000-10000,14300-18100. sha256:4cdec5889a00b9e7b2a81c80304f12e0d22bb3ef409eb46ce5d08112989e68a7

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 64598e5f5ac8dd470410dac4dc6be6680cf855f3dd59a38e2c84c0e545ed063c

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 5799f19eb470e833f4c6325348a2eda4b502cc91c4bd6296f875f1c73e9e3a3c

D; exact-gradient subclass allowed at every sigma.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: d793fc80434e028c0cc22b34c52dc91569b37fdd8f2ceb47d31ef99551427950

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 4a2ec336ff58703dfc0f8b6542f91dca169a4cdbdcdf92efd81114e2cb22dbac

Exact derivatives almost surely; endpoint signs then bisection; feasible possibly unqueried output, deterministic sample cap.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 58ef8ba365b3165dac1d1e3cecbf34f73e1db7e4af5b4d775311811e731f7090

Frozen contract with d=1,sigma=0.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 252401d14aa416f9c5ee370be372f72e4bfe1f0a8e9ca2af702804f51a055148

Fully read frozen premises identified in CV_ALPHA_1D_BISECTION baseline_refs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: d896926767fa3ca9feb23a5b64973d033ba02b82bc2c2edc1ab8722eb420f5f8

E, same native view/guarantee/quantity/resource.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 52705eae14c2070154a899b6de48d2ecc363c14a69d632e77a356f3b030672e4

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 1f1aff41ead58623d668199502c9eb7b3c311c3a790e4bbb6eb6ef73b281b2fc

Identity retention only; no fresh recertification or cross-quantity merge.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 340334e441e37fece19845cfdd7f78e71848b0afa54e3f1209ba66af6ddf190f

Unchanged frozen bound premises, retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: e5b323ed9b121c45947a6bbdf1be31ae959c375b761d3eb3ea9e0e11f40542b1

Frozen native e1: upper Theorem 2(i), Eq.(33).

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: daee4d141bf23a61dbbcec8e610b53347ac68f173f83222f8c6f45ee598a98ac

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: 2e6846fbebd4f9c4ef0126bb71b79564ad6a196af83cd1db3794bbe20ddd9f03

SO_SRC_a73fce82d651b459

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 592c945c4377776a57a040b6f7728747634924c7a24346f57c0207653a78c7b9

D in the same native view/guarantee/quantity/resource.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 411509256e7479c347debda1dbbd6affb011f8a0e27b066a56a7b4fba3f39d8a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 1f1aff41ead58623d668199502c9eb7b3c311c3a790e4bbb6eb6ef73b281b2fc

Identity retention only; no fresh recertification or cross-quantity merge.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 8935899cc7217d259b728ec2b149156926a09bcaa54bcf7d921ae6118f91f210

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: fe306dfb2914f1fa7fdd13c9edd709fa8ade607255ad7be06d916e118271a6e4

FO_RARE_EVENT

#### Native item 2

Native pointer: /joint_analysis/provenance/5/proof_refs/1; canonical SHA-256: 29b9306c3ae6ce4ce0a8266c6fe249d2553aa06dc0f17176893e4c9cc2fd0ec2

FO_EXPECTATION_CONVERSION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 340334e441e37fece19845cfdd7f78e71848b0afa54e3f1209ba66af6ddf190f

Unchanged frozen bound premises, retained conditionally.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 393b46558ef1e68f24f145480907e5f128e8b51832b1f5b38be7b3b86eebb597

Frozen native e2 and its proof_refs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 5faaca4d5a3788ad2da4feb854c7395b3245bd3cdd11a0dc4f6f19d78a9ee825

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native item 2

Native pointer: /joint_analysis/provenance/5/source_refs/1; canonical SHA-256: 7e75f30886c7472d8671742772da2d3a25a1d41087b6aa3b3a9fff032a624f81

SO_SRC_4a9caa6c975c30ce

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 592c945c4377776a57a040b6f7728747634924c7a24346f57c0207653a78c7b9

D in the same native view/guarantee/quantity/resource.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: 66e9f2b7a1d2bb2ea18e4e56a66e14b013fb7a0bdbb5dbf9713bf21cf60a1983

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: b27b0a8d707ddf01c4aefc4373fb3ec330eac3142726bca856fb0842fb3c2e2f

Ball-contained scaled least squares, two matvecs/gradient, Markov conversion, dimension calibration, affine endpoint; complete proof in CV_ALPHA_DIMENSION_TRANSFER.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: ef521782115a5c48b6220c60a0f09483d1c838e719af774a8e058d7b375a810d

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 8d82014b1e40371a569f845f66bfd308a0c3c6b9dc1679c2b56d8913c483d98d

CV_ALPHA_DIMENSION_TRANSFER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 1a03f4c889bf5dfedefbce12a85e050136cecdf5ae38046caf1e31394d89ea52

Randomized adaptive matvecs, fixed small relative residual, large condition k, n=O(T^2).

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 79f799ce8deb32e6b8a1e473863ba88900cbdda428aae29f89703bb2d40eefb4

Shamir arXiv:2609.10874v1, Thm.1/reduction pp.2-3, Eq.(7)/conclusion pp.7-9; chars 3000-10000,14300-18100. sha256:4cdec5889a00b9e7b2a81c80304f12e0d22bb3ef409eb46ce5d08112989e68a7

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 64598e5f5ac8dd470410dac4dc6be6680cf855f3dd59a38e2c84c0e545ed063c

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: b16d20412234a21b7d751ad148856511c79c81bf7535570d39faedcbd0ba1d21

SO_SRC_cdf1550d10cb341b

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 5799f19eb470e833f4c6325348a2eda4b502cc91c4bd6296f875f1c73e9e3a3c

D; exact-gradient subclass allowed at every sigma.

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: f4f74860a0e1f8d2b1bb5249e2236a912bf4dc95ac81c3de9269bbd9f53706ea

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 4a2ec336ff58703dfc0f8b6542f91dca169a4cdbdcdf92efd81114e2cb22dbac

Exact derivatives almost surely; endpoint signs then bisection; feasible possibly unqueried output, deterministic sample cap.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: c42dfa4462987e30d1684ee0a765e921d7034174aeff6244df1f6c57482937ac

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: 30d0429f8f6f67761fb100015d1952b47640b2bff41f1533719123357d8b9990

CV_ALPHA_1D_BISECTION

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: 58ef8ba365b3165dac1d1e3cecbf34f73e1db7e4af5b4d775311811e731f7090

Frozen contract with d=1,sigma=0.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: 252401d14aa416f9c5ee370be372f72e4bfe1f0a8e9ca2af702804f51a055148

Fully read frozen premises identified in CV_ALPHA_1D_BISECTION baseline_refs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: d896926767fa3ca9feb23a5b64973d033ba02b82bc2c2edc1ab8722eb420f5f8

E, same native view/guarantee/quantity/resource.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 71ec9d81452ab04fdae78b1ebbc168bd3aadaa733a9728bd2ffc48fce800454b

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 7bcf61ac99a2385da9a02102fdee4367e4c813c178aa87295839ca6308650c11

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 05a9b4610facbe01c33ce02e5b749d207dad2792fd721ee08e28f6c6d86ce49e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 6e53a91b602247e08f0a98c6bb9b03f1e794a86ba349619ad71facef279cd1a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 4159aeb22dfe73bc528a644941855934cac107770af2a7c1ac1266da2e9b4433

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 20b09cc3d8393051d6e5265b69084a0c71be747680e12d55412ac7428e8ec281

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 6e53a91b602247e08f0a98c6bb9b03f1e794a86ba349619ad71facef279cd1a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 32b4e339818e05c32424b89df602d9a9e0c27bfbce28c6f85b721faed469c721

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 502a1f80ad3aaf22806f380d823e40b7cecc11501b6c9c36c34cfb4c4c17ce31

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 6e53a91b602247e08f0a98c6bb9b03f1e794a86ba349619ad71facef279cd1a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 7a0517122dad393df62ebdd0b3f35b3072ede1126c9723ab1bd1eea5c461f3f1

SO_FO_S02_cv_alpha__deterministic__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 756d62e0537a8f4e461e8012f46a6d0da7ff2bdfbfad11a603296ceef8602c5e

SO_FO_S02_cv_alpha__deterministic__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: c8d9f1e164d81b815f52fccfedc91b1f3148cb5dc32d8d5bf561ab121427e505

SO_FO_S02_cv_alpha__deterministic__expected_loss__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: b798068dfad0d08501843cca64684550868bd9e8b7e6de7cf6e78cad4b3b2e5f

SO_FO_S02_cv_alpha__deterministic__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 29106c742d530994e937d0d22e163198986a71851fe895cb39465afc6dcd2252

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 94ebdcb021bcbc6fc94fa708c1e7a7f9d1afd6248b96e70935fa7df176e425ff

synthesis-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: f5be8d45d07c171314dc77c585a381ad78f0590df74c1c0e9f668dcc869d6466

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 6ddfe103aff1cf6d0774d844ef5c3bc1f1de0c08c4a3d0c78a16c960c990f2d0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 04216b61632a5c52e245c10451f85254cc50f63fc79c01bc9335499db54e8031

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 7f1a6540bd14dbb3bcfdfdfac9a64bfde09607556bb3c904bfc43adedf6ede22

synthesis-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: d876d076896f70342b213ceae85a06a1c2480e29fade021caa8275f95794ae26

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 6ddfe103aff1cf6d0774d844ef5c3bc1f1de0c08c4a3d0c78a16c960c990f2d0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: c74433f40eac6099d43096923a8e840f7536a0f7fd1212c06c302b5c96ebdf15

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: ca0bbdf769e92b6ee0fc04da5960cb413f34af9e8cc0d5eca08f2ac29f71ac8f

synthesis-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 4182a3a5d10c25366b654f62a8af429c3fa3135ed6e8585429ca52f961d8c935

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 6ddfe103aff1cf6d0774d844ef5c3bc1f1de0c08c4a3d0c78a16c960c990f2d0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: 3c9c08021e47af1659e3a1e8dff2a277695b8144eb96e1953b70fc35637f4683

SO_FO_S02_cv_alpha__randomized__expected_loss__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: ff1d787fecf8215605d9829fde356afab064a84df3edc228836d8a83c0931360

SO_FO_S02_cv_alpha__randomized__expected_loss__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: 0b788360e859d6078595db0d6062b510a350dc9a482e4c11735c5cd85625f0ef

SO_FO_S02_cv_alpha__randomized__expected_loss__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: 608d220cebd0cc3fd9cb4940bffa9fc8a0112fab8fb53971f7365af6fffa0b2c

SO_FO_S02_cv_alpha__randomized__expected_loss__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 8947e9af3d8d8b4b1513afb8cd854a38367cd50507fa69a4bb7de20be85b1a2b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 8cedb7c54fb7a3ff1b2d98263a56263d1a8afbb4fdabf8cee435054dc16d1ea3

synthesis-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: d5952caad7033a653fbc8f33d3b2e5893acbcf8962872d77e22da4e9c1506ed3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 2fe529ec8f5489f320bec63b340c49a880b779b01e07e2bd6ffdb9f602cbe7d9

Seek independent support for an all-dimensional logarithmic lower bound on the smooth convex ball; the old source alone does not establish it, so both b3 rows remain inactive pending such evidence.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 49d4778ff833f6a1bce0e753f18fd883ac169c9051f384c0a1aedacc747e14fc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 2bde1efb57ddef6548045c109891a2c7476b98a3397ecfa0c6595bfc0fdfa6e9

Sharper positive-noise and multi-dimensional low-dimensional upper/lower envelopes were not searched beyond the two named baseline sources; present gaps are recorded bounds, not certified literature gaps.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: d93d3d8770de5788530c6c2e0b402afe46c87b1513af5693e173d1e6eb1f12dc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 67f2f66534648dbfe1d27b1517d836f92a343b1b9e1cb8389bde815baf9f2026

Native tracked mu and Delta are unused by the scientific contract. They remain unchanged and all proposed rates are uniform in them; optional future metadata cleanup requires its own controlled normalization review.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 80e1d9baa81f98fe479985e2dd9398fc7eb504277eff21aded2cefa5dc3054d4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: fad282054762ef3078cacfeead288a316048c6169ef7741b0190863381ca7d72

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 098885e66c666077f0dacabaa60c252ed56cb75628885bb6a316e5e4bb349f82

SO_FO_S02_cv_alpha__deterministic__expected_loss__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 6bfe6160fdd969c89b6ee1f6c8cdf39f01926221cbb70bc420136b8f50f87665

SO_FO_S02_cv_alpha__deterministic__expected_loss__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: 5d1afb68c5aad4cf36c425c9a5da7084690194d8075fc8974751727ccf953bc9

SO_FO_S02_cv_alpha__deterministic__expected_loss__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/3; canonical SHA-256: 293504231472294147adbac47b4cc97f717455261e64179cf62d5c49a7a00adc

SO_FO_S02_cv_alpha__randomized__expected_loss__c1

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/4; canonical SHA-256: a829642e1c702a6a39953c3294c0e728bf036266999d53f8d6761147f244c739

SO_FO_S02_cv_alpha__randomized__expected_loss__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/5; canonical SHA-256: 38bd34d35e5d5d0e603a8a71eeb1ea8ecd54ecb8e3a1d9baab6ffe0a22832f51

SO_FO_S02_cv_alpha__randomized__expected_loss__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: c1accb6266e4a3cb279bdff991cc1e85dc737ab3cf3cf4c9ea14a16616eab496

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: ed0dd356b2406cacf3789f7fef324a2ade1cbb4adc652c5cd76f9af27e223562

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 4c040d64b6fcc00194d1e3a7427f28624c0ae083e7cb68695195f0a6cb9ee7bd

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 65db86bd486797ec0ab62a107d37670aa3dc8d6cd5e61c4ebbeef80e689426d5

/regimes/5

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: 26244fadf4d335759aed5dc1a813f66e19f4ae191a17c1500f4539f81bc5d450

/regimes/11

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 5a34a1fafdc78867b69352f103eeb9cc724e2a49d7c4ffd63e65793fcba7f62b

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: bba3eb2b15ac9129236304a58622aeaaa4d06b7e68a577a167a0b0fe53bb605e

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 68fca58cf80cbbafdb999d7359870b2259136e0bd4413c0adadfe450394406dc

1<alpha<=2, fixed for each theorem; constants may diverge as alpha approaches 1.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 53fd8c574a6c785ab5e9764d69975200ef72366239ac7570323a32c9a7b0c78d

For each fixed alpha in (1,2]: d integer>=1, beta,R>0, sigma>=0, 0<epsilon<=c*beta*R^2 (native sufficiently-small universal c). Separate native minimax sample counts, expected gap g1, pathwise budget, feasible output. Native metadata also tracks mu,Delta though the convex-ball contract does not use them: retain these dummy axes, impose no strong-convexity/initial-gap assumptions, and require uniformity in their positive values.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: bd23e776300adfaf5ca244c78e8c8a68cea352affd5ad0bafa3a1ba1bc926831

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: acaf8b36ef4c14cdddfdab6eaa18567e8b7cc3fa224ce72aeae4076bdbad7609

SO_FO_S02_cv_alpha_p_b4e942dc3f

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 4cb84c2cd8d680f0dd11ca731d1ffe264ac964be4efb7bea4b5198bd318b85f8

SO_FO_S02_cv_alpha_p_d360d55977

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 41fc28124d1f1cfb5b23a5829500f3b0bd06e1be3742b17ec4bb2022034aea07

SO_FO_S02_cv_alpha_p_c8d2553836

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 4adb23a4111b64ffc3d8d37b12c917f6b747915452aef3d996c7a5daa469c920

SO_FO_S02_cv_alpha_p_f622aabe5e

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 94f9603ee28865bc2622697428f407d78fb6a48311066925904f7ab64e0ad06b

SO_FO_S02_cv_alpha_p_188c06cfa3

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 3b23d19c69e9b6520bd46a6a71ccaa1a8afd39dfaede5074b9702c2c24d592e8

SO_FO_S02_cv_alpha_p_a6849cb45c

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: 4fe497f9c4775d1f39b7f7261f0767f9af6ba442c716ddb6786b3c3a432c5921

SO_FO_S02_cv_alpha_p_95775a4b65

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: f4a703577c4528c3dc0dfdeb54dd6d53a4a15afcdb79eb52d71bb163062d73e2

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 58c4ff9e4af927219247eb9a46b79c38716ac27a9470ab805bcdd0e240b02ab3

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: c3c6eef5230453852c599c1a3769e2e68ab8c188baf19019106af1ac5778145e

q=beta*R^2/epsilon; with y=x/R,F(y)=f(R*y)/epsilon, q is unit-ball smoothness. This dimensionless rescaling preserves samples.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: b78856d92a575634c457c1acf25af59789bab1b3c11ba36687efaaf519aa73d7

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 4cb84c2cd8d680f0dd11ca731d1ffe264ac964be4efb7bea4b5198bd318b85f8

SO_FO_S02_cv_alpha_p_d360d55977

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 4adb23a4111b64ffc3d8d37b12c917f6b747915452aef3d996c7a5daa469c920

SO_FO_S02_cv_alpha_p_f622aabe5e

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: 4fe497f9c4775d1f39b7f7261f0767f9af6ba442c716ddb6786b3c3a432c5921

SO_FO_S02_cv_alpha_p_95775a4b65

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 90edba1c9d0bb14ec514a96ca800a95448adb82f1adced02b66c15b4091777d2

q

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: ac331b974cde589291f7e93bc7fc3793687290fcaf91ba24779fcfce005780ce

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: 6b2e07f7b5d468e59e2c07c27520f793e3605d6c677a61368a8d3a890a314038

s=(sigma*R/epsilon)^(alpha/(alpha-1)), zero when sigma=0. Under y=x/R,F(y)=f(R*y)/epsilon, sigma*R/epsilon is normalized centered-noise scale; sample cost is unchanged.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: cf5cc8bf221aca2b3304f0e5aea47555f7791a0b8362ccc3d519b83bb594ab21

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: 3b23d19c69e9b6520bd46a6a71ccaa1a8afd39dfaede5074b9702c2c24d592e8

SO_FO_S02_cv_alpha_p_a6849cb45c

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/1; canonical SHA-256: 4adb23a4111b64ffc3d8d37b12c917f6b747915452aef3d996c7a5daa469c920

SO_FO_S02_cv_alpha_p_f622aabe5e

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/2; canonical SHA-256: 4fe497f9c4775d1f39b7f7261f0767f9af6ba442c716ddb6786b3c3a432c5921

SO_FO_S02_cv_alpha_p_95775a4b65

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/3; canonical SHA-256: 7546df35eae2d72100841de30da56d7cf1dc53f7d9a238ad07a64793f57fd8ee

SO_FO_S02_cv_alpha_p_debd1b8136

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: 0f4657778ae14ff7aeeb2c2190ede79099aa9c4e8a9e54829462f0e92af659e5

s

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: bd23e776300adfaf5ca244c78e8c8a68cea352affd5ad0bafa3a1ba1bc926831

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: acaf8b36ef4c14cdddfdab6eaa18567e8b7cc3fa224ce72aeae4076bdbad7609

SO_FO_S02_cv_alpha_p_b4e942dc3f

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 4cb84c2cd8d680f0dd11ca731d1ffe264ac964be4efb7bea4b5198bd318b85f8

SO_FO_S02_cv_alpha_p_d360d55977

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 41fc28124d1f1cfb5b23a5829500f3b0bd06e1be3742b17ec4bb2022034aea07

SO_FO_S02_cv_alpha_p_c8d2553836

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 4adb23a4111b64ffc3d8d37b12c917f6b747915452aef3d996c7a5daa469c920

SO_FO_S02_cv_alpha_p_f622aabe5e

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 94f9603ee28865bc2622697428f407d78fb6a48311066925904f7ab64e0ad06b

SO_FO_S02_cv_alpha_p_188c06cfa3

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 3b23d19c69e9b6520bd46a6a71ccaa1a8afd39dfaede5074b9702c2c24d592e8

SO_FO_S02_cv_alpha_p_a6849cb45c

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: 4fe497f9c4775d1f39b7f7261f0767f9af6ba442c716ddb6786b3c3a432c5921

SO_FO_S02_cv_alpha_p_95775a4b65

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 9 September 2026; preprint v1. Theorem 1 (PDF p. 2); strongly convex quadratic reduction (p. 3); the dimension $O(T^2)$ in equation (7) (p. 7)..

https://arxiv.org/pdf/2609.10874

[2] Chuan He, Bowen Li and Zhaosong Lu. Accelerated stochastic first-order method for convex optimization under heavy-tailed noise. 2026; arXiv:2510.11676v2, 21 September 2026; Assumption 1, Theorem 2(i), Eq.(33), pp.4–5,8.

https://arxiv.org/pdf/2510.11676

[3] Abdurakhmon Sadiev, Marina Danilova, Eduard Gorbunov, Samuel Horváth, Gauthier Gidel, Pavel Dvurechensky, Alexander Gasnikov and Peter Richtárik. High-Probability Bounds for Stochastic Optimization and Variational Inequalities: the Case of Unbounded Variance. 2023; ICML 2023, PMLR 202:29563–29648; Theorems 3.2–3.3, F.3, Eq.(189), PDF pp.7,48–50.

https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf
