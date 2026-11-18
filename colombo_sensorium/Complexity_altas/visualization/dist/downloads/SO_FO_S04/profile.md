# Stochastic global PL minimization: stochastic full gradients

**Setting ID.** `SO_FO_S04`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; growth: Global polyak lojasiewicz; smoothness: Lipschitz gradient; stochastic model: Centered alpha moment noise

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic gradient; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Failure probability parameter explicitly declared; mode: Expectation; mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $\beta$-smooth and satisfies $\|\nabla f(x)\|^2\ge2\mu(f(x)-f^\star)$, with $f(x_0)-f^\star\le\Delta$. Nonconvexity is allowed; $\mu$ is the PL constant.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \mu > 0,\quad \kappa \ge 6\\\varepsilon \le c\,\Delta,\quad \beta > 0,\quad \Delta > 0,\quad \sigma \ge 0\\\alpha > 1,\quad \alpha \le 2,\quad \mu \le \beta\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ \Delta,\ \sigma$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full gradients:

$$\mathbb{E}_tG_t=\nabla f(x_t),\quad\mathbb{E}_t\|G_t-\nabla f(x_t)\|^\alpha\le\sigma^\alpha$$

Samples in a same-point batch are conditionally independent and satisfy the same history-conditional moment bound. No additional independence across adaptively chosen locations is imposed.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

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

#### Deterministic / Probability guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}:\ \mathbb{P}(\ell(I,\widehat{x})>\varepsilon)\le\delta$$

The probability space includes observation noise. The algorithm uses no private random numbers. The instance and its admissible oracle law are fixed before randomness is averaged.

**Oracle qualification.** This view additionally takes the public confidence parameter $\delta$, with $0<\delta<1/2$.

#### Randomized / Probability guarantee

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}:\ \mathbb{P}(\ell(I,\widehat{x})>\varepsilon)\le\delta$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Oracle qualification.** This view additionally takes the public confidence parameter $\delta$, with $0<\delta<1/2$.

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

$\mu$: Known lower bound on the global PL modulus **Domain:** $\mu>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\kappa$: $\beta/\mu$, where $\mu$ is the PL constant; strong convexity is not assumed.

$$\kappa=\frac{\beta}{\mu}$$

$S$: Number of halving stages, $\lceil\log_2(\Delta/\epsilon)\rceil$; not an independent parameter.

$$S=\lceil\log_2(\Delta/\varepsilon)\rceil$$

$V$: Statistical term at the final accuracy scale.

$$V={\frac{{\sigma}^{2}}{\mu\,\varepsilon}}^{\frac{\alpha}{2\,((\alpha-1))}}$$

$d_{\rm hd}$: Sufficient construction dimension in OW26, equation (166): $\widetilde O_\alpha(\kappa^2[\Delta/\epsilon+V])$. Only logarithmic factors are hidden. This is not a necessary dimension threshold. **Domain:** $d_{\rm hd}=\widetilde{O}_\alpha(\kappa^2[\Delta/\varepsilon+V])$.

$c_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<c_\alpha<\infty$.

$C_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<C_\alpha<\infty$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\delta$: Allowed failure probability; expected-error and probability contracts are kept distinct. **Domain:** $0<\delta<1/2$.

$\Pr,\mathbb{P}$: Event probability after the instance and admissible response law are fixed

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

#### Q3 - target accuracy cost

**View.** Deterministic / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q5 - target accuracy cost

**View.** Randomized / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Native high-dimensional theorem window

**Region.** $\kappa\ge\kappa_{\rm hd},\quad d\ge d_{\rm hd},\quad0<\varepsilon\le c_{0,\alpha}\Delta$

**Views.** Deterministic / Expected loss; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2, B4

$$
c_\alpha\kappa(S+V)
$$

**Upper bound.** B1, B3

$$
C_\alpha\kappa(S+V)
$$

**Gap or comparison.** $O_\alpha(1)$

### R2 - High-dimensional regime with fixed confidence

**Region.** $\theta\in\Theta_{\rm hd},\quad\delta=1/4$

**Views.** Deterministic / Probability guarantee

**Quantity.** Q3

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B6

$$
c_\alpha\kappa(S+V)
$$

**Upper bound.** B5

$$
C_\alpha\kappa(S+V)\log(64\kappa S)
$$

**Gap or comparison.** $O_\alpha(\log(64\kappa S))$

### R3 - High-dimensional regime with fixed confidence

**Region.** $\theta\in\Theta_{\rm hd},\quad\delta=1/4$

**Views.** Randomized / Probability guarantee

**Quantity.** Q4

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B8

$$
c_\alpha\kappa(S+V)
$$

**Upper bound.** B7

$$
C_\alpha\kappa(S+V)\log(64\kappa S)
$$

**Gap or comparison.** $O_\alpha(\log(64\kappa S))$

### R4 - Fixed-dimensional branch d=1

**Region.** $d=1,\quad\theta\in\Theta_{\rm fixed}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B10, B7

$$
\widetilde{O}_{\alpha,d}(\min\{\kappa(S+V),S+V\})
$$

**Gap or comparison.** $\operatorname{polylog}(\kappa,\Delta/\varepsilon)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d1. In one dimension the gap is logarithmic. In other dimensions, retain the explicit interaction between $\kappa$ and the statistical term. Constants allowed to depend on fixed $d$ cannot establish joint optimality in $d$.

### R5 - Fixed-dimensional branch d=2

**Region.** $d=2,\quad\theta\in\Theta_{\rm fixed}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B11, B7

$$
\widetilde{O}_{\alpha,d}(\min\{\kappa(S+V),\kappa^{2/3}S+V\})
$$

**Gap or comparison.** $\widetilde{O}_{\alpha,d}\!\left({\min\{\kappa(S+V),\kappa^{2/3}S+V\}\over S+V}\right)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d2. In one dimension the gap is logarithmic. In other dimensions, retain the explicit interaction between $\kappa$ and the statistical term. Constants allowed to depend on fixed $d$ cannot establish joint optimality in $d$.

### R6 - Fixed-dimensional statistically dominated regime

**Region.** $V\ge \kappa^{2/3}S$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
c_\alpha V
$$

**Upper bound.** B11, B7

$$
\widetilde{O}_{\alpha,d}(V)
$$

**Gap or comparison.** $\operatorname{polylog}(\kappa,\Delta/\varepsilon)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d2-statistics. Statistical dominance allows $V$ to absorb the optimization term. Constants retain the stated fixed-dimension convention.

### R7 - Fixed-dimensional branch d=3

**Region.** $d=3,\quad\theta\in\Theta_{\rm fixed}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B12, B7

$$
\widetilde{O}_{\alpha,d}(\min\{\kappa(S+V),\kappa S+V\})
$$

**Gap or comparison.** $\widetilde{O}_{\alpha,d}\!\left({\min\{\kappa(S+V),\kappa S+V\}\over S+V}\right)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d3. In one dimension the gap is logarithmic. In other dimensions, retain the explicit interaction between $\kappa$ and the statistical term. Constants allowed to depend on fixed $d$ cannot establish joint optimality in $d$.

### R8 - Fixed-dimensional statistically dominated regime

**Region.** $V\ge \kappa S$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
c_\alpha V
$$

**Upper bound.** B12, B7

$$
\widetilde{O}_{\alpha,d}(V)
$$

**Gap or comparison.** $\operatorname{polylog}(\kappa,\Delta/\varepsilon)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d3-statistics. Statistical dominance allows $V$ to absorb the optimization term. Constants retain the stated fixed-dimension convention.

### R9 - Fixed-dimensional branch $d>3,\ \alpha/(\alpha-1)\ge d-1$

**Region.** $d>3,\ \alpha/(\alpha-1)\ge d-1,\quad\theta\in\Theta_{\rm fixed}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B13, B7

$$
\widetilde{O}_{\alpha,d}(\min\{\kappa(S+V),\kappa^{(d-1)/2}S+V\})
$$

**Gap or comparison.** $\widetilde{O}_{\alpha,d}\!\left({\min\{\kappa(S+V),\kappa^{(d-1)/2}S+V\}\over S+V}\right)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.dplus-heavy. In one dimension the gap is logarithmic. In other dimensions, retain the explicit interaction between $\kappa$ and the statistical term. Constants allowed to depend on fixed $d$ cannot establish joint optimality in $d$.

### R10 - Fixed-dimensional statistically dominated regime

**Region.** $V\ge \kappa^{(d-1)/2}S$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
c_\alpha V
$$

**Upper bound.** B13, B7

$$
\widetilde{O}_{\alpha,d}(V)
$$

**Gap or comparison.** $\operatorname{polylog}(\kappa,\Delta/\varepsilon)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.dplus-heavy-statistics. Statistical dominance allows $V$ to absorb the optimization term. Constants retain the stated fixed-dimension convention.

### R11 - Fixed-dimensional branch $d>3,\ \alpha/(\alpha-1)<d-1$

**Region.** $d>3,\ \alpha/(\alpha-1)<d-1,\quad\theta\in\Theta_{\rm fixed}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B14, B7

$$
\widetilde{O}_{\alpha,d}(\min\{\kappa(S+V),\kappa^{(d-1)/2}S+\kappa^{[d-1-\alpha/(\alpha-1)]/2}V\})
$$

**Gap or comparison.** $\widetilde{O}_{\alpha,d}\!\left({\min\{\kappa(S+V),\kappa^{(d-1)/2}S+\kappa^{[d-1-\alpha/(\alpha-1)]/2}V\}\over S+V}\right)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.dplus-light. In one dimension the gap is logarithmic. In other dimensions, retain the explicit interaction between $\kappa$ and the statistical term. Constants allowed to depend on fixed $d$ cannot establish joint optimality in $d$.

### R12 - Fixed dimension four, $1<\alpha\le3/2$

**Region.** $d=4,\quad 1<\alpha\le3/2$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B15, B7

$$
\widetilde{O}_\alpha(\min\{\kappa(S+V),\kappa^{3/2}S+V\})
$$

**Gap or comparison.** $\widetilde{O}_\alpha\!\left({\min\{\kappa(S+V),\kappa^{3/2}S+V\}\over S+V}\right)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d4-heavy. Retain the complete ratio of the two bounds. For fixed $\kappa$, the leading accuracy and noise dependence differs only logarithmically; this does not imply closure when $\kappa$ grows jointly.

### R13 - Fixed dimension four, $3/2<\alpha\le2$

**Region.** $d=4,\quad 3/2<\alpha\le2$

**Views.** Randomized / Probability guarantee

**Quantity.** Q5

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B9

$$
c_\alpha(S+V)
$$

**Upper bound.** B16, B7

$$
\widetilde{O}_\alpha(\min\{\kappa(S+V),\kappa^{3/2}S+\kappa^{[3-\alpha/(\alpha-1)]/2}V\})
$$

**Gap or comparison.** $\widetilde{O}_\alpha\!\left({\min\{\kappa(S+V),\kappa^{3/2}S+\kappa^{[3-\alpha/(\alpha-1)]/2}V\}\over S+V}\right)$

**Comparison argument.** Compare on the intersection of S04.probability-R.parameter-domain and S04.d4-light. Retain the complete ratio of the two bounds. For fixed $\kappa$, the leading accuracy and noise dependence differs only logarithmically; this does not imply closure when $\kappa$ grows jointly.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Deterministic multistage gradient descent with robust batches

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha\kappa(S+V)
$$

**Conditions.** $$\mu>0,\quad\kappa\ge6,\quad0<\varepsilon\le c_\alpha\Delta$$

**Dimension conditions.** $\mu>0,\quad\kappa\ge6,\quad0<\varepsilon\le c_\alpha\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Local argument.** A1

### B2 - OW26 high-dimensional lower bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha\kappa(S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\kappa\ge\kappa_{\rm hd},\quad d\ge d_{\rm hd},\quad0<\varepsilon\le c_{0,\alpha}\Delta$$

**Dimension conditions.** $\kappa\ge\kappa_{\rm hd},\quad d\ge d_{\rm hd},\quad0<\varepsilon\le c_{0,\alpha}\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: arXiv2609.03990v2 (26 September 2026), Thm3.1, Eq.(166); PDF p.7, AppendixB.5

### B3 - Deterministic multistage gradient descent with robust batches

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha\kappa(S+V)
$$

**Conditions.** $$\mu>0,\quad\kappa\ge6,\quad0<\varepsilon\le c_\alpha\Delta$$

**Dimension conditions.** $\mu>0,\quad\kappa\ge6,\quad0<\varepsilon\le c_\alpha\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Local argument.** A1

### B4 - OW26 high-dimensional lower bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha\kappa(S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\kappa\ge\kappa_{\rm hd},\quad d\ge d_{\rm hd},\quad0<\varepsilon\le c_{0,\alpha}\Delta$$

**Dimension conditions.** $\kappa\ge\kappa_{\rm hd},\quad d\ge d_{\rm hd},\quad0<\varepsilon\le c_{0,\alpha}\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: arXiv2609.03990v2 (26 September 2026), Thm3.1, Eq.(166); PDF p.7, AppendixB.5

### B5 - High-probability CC-MD guarantee

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Probability guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha\kappa(S+V)\log(16\kappa S/\delta)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\theta\in\Theta_{\rm regular},\quad0<\delta<1/2$$

**Dimension conditions.** $\theta\in\Theta_{\rm regular},\quad0<\delta<1/2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorem4.3; AppendixC.2, Eq.(192); PDF pp.9,46

### B6 - High-dimensional regime with constant failure probability

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha\kappa(S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\theta\in\Theta_{\rm hd},\quad\delta=1/4$$

**Dimension conditions.** $\theta\in\Theta_{\rm hd},\quad\delta=1/4$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: arXiv2609.03990v2 (26 September 2026), Thm3.1, Eq.(166); PDF p.7, AppendixB.5

### B7 - High-probability CC-MD guarantee

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha\kappa(S+V)\log(16\kappa S/\delta)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\theta\in\Theta_{\rm regular},\quad0<\delta<1/2$$

**Dimension conditions.** $\theta\in\Theta_{\rm regular},\quad0<\delta<1/2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorem4.3; AppendixC.2, Eq.(192); PDF pp.9,46

### B8 - High-dimensional regime with constant failure probability

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha\kappa(S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\theta\in\Theta_{\rm hd},\quad\delta=1/4$$

**Dimension conditions.** $\theta\in\Theta_{\rm hd},\quad\delta=1/4$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: arXiv2609.03990v2 (26 September 2026), Thm3.1, Eq.(166); PDF p.7, AppendixB.5

### B9 - One-dimensional embedded lower bound for fixed $d$

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha(S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$\kappa\ge6,\quad\delta=1/4,\quad0<\varepsilon\le c_\alpha\Delta$$

**Dimension conditions.** $\kappa\ge6,\quad\delta=1/4,\quad0<\varepsilon\le c_\alpha\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B10 - Robust stochastic bisection

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_{\alpha,d}(S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=1,\quad\theta\in\Theta_{\rm fixed}$$

**Dimension conditions.** $d=1,\quad\theta\in\Theta_{\rm fixed}$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B11 - Two-dimensional gradient-flow traps

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_{\alpha,d}(\kappa^{2/3}S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=2,\quad\theta\in\Theta_{\rm fixed}$$

**Dimension conditions.** $d=2,\quad\theta\in\Theta_{\rm fixed}$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B12 - Three-dimensional gradient-flow traps

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_{\alpha,d}(\kappa S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=3,\quad\theta\in\Theta_{\rm fixed}$$

**Dimension conditions.** $d=3,\quad\theta\in\Theta_{\rm fixed}$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B13 - Surface reconstruction at fixed $d$ without an additional power of $\kappa$ in the heavy-tailed statistical term

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_{\alpha,d}(\kappa^{(d-1)/2}S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d>3,\ \alpha/(\alpha-1)\ge d-1,\quad\theta\in\Theta_{\rm fixed}$$

**Dimension conditions.** $d>3,\ \alpha/(\alpha-1)\ge d-1,\quad\theta\in\Theta_{\rm fixed}$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B14 - Additional surface-entropy factor at fixed $d$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_{\alpha,d}(\kappa^{(d-1)/2}S+\kappa^{[d-1-\alpha/(\alpha-1)]/2}V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d>3,\ \alpha/(\alpha-1)<d-1,\quad\theta\in\Theta_{\rm fixed}$$

**Dimension conditions.** $d>3,\ \alpha/(\alpha-1)<d-1,\quad\theta\in\Theta_{\rm fixed}$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B15 - OW26 fixed-dimensional result evaluated at $d=4$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_\alpha(\kappa^{3/2}S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=4,\quad 1<\alpha\le3/2$$

**Dimension conditions.** $d=4,\quad 1<\alpha\le3/2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

### B16 - OW26 fixed-dimensional result evaluated at $d=4$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}_\alpha(\kappa^{3/2}S+\kappa^{[3-\alpha/(\alpha-1)]/2}V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.03990)

**Conditions.** $$d=4,\quad 3/2<\alpha\le2$$

**Dimension conditions.** $d=4,\quad 3/2<\alpha\le2$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.03990) theorem: Theorems5.1,5.3; AppendixD.2,D.5; CorollaryD.13, Eq.(260); PDF pp.10–12,53–65

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

[1] Weiming Ou; Xiao Wang. Tight Heavy-Tailed Complexity Bounds for Optimizing Polyak–Łojasiewicz Objectives. 2026-09-26; preprintv2; Theorem 3.1; Theorems 4.3,5.1,5.3; Appendix B Lemmas B.13–B.15; Eq.(166),(192)..

https://arxiv.org/pdf/2609.03990
