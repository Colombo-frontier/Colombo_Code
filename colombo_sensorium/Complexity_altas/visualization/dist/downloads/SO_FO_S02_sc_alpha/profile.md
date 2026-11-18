# Stochastic smooth convex minimization: strong convexity and heavy-tailed centered noise; stochastic full gradients

**Setting ID.** `SO_FO_S02_sc_alpha`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; stochastic model: Centered alpha moment noise

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic gradient; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Failure probability parameter explicitly declared; mode: Expectation; mode: Probability; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The objective is globally $\beta$-smooth and $\mu$-strongly convex, with initial suboptimality at most $\Delta$. The conditional centered moment of order $\alpha$ is at most $\sigma^\alpha$, and samples at the same point are conditionally independent.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \mu > 0,\quad \kappa \ge 4\\\varepsilon \le c\,\Delta,\quad \beta > 0,\quad \sigma \ge 0,\quad \alpha > 1\\\alpha \le 2,\quad \Delta > 0,\quad \mu \le \beta\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \varepsilon$.

Public upper bounds: $\beta,\ \Delta,\ \sigma$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full gradients:

$$\mathbb{E}_tG_t=\nabla f(x_t),\quad\mathbb{E}_t\|G_t-\nabla f(x_t)\|^\alpha\le\sigma^\alpha$$

Every observation is fresh. Same-point batches are conditionally independent, and the conditional moment bounds hold uniformly over histories. Samples cannot be reused across points.

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

#### Deterministic / Probability guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}:\ \mathbb{P}(\ell(I,\widehat{x})>\varepsilon)\le\delta$$

The probability space includes observation noise. The algorithm uses no private random numbers. The instance and its admissible oracle law are fixed before randomness is averaged.

**Oracle qualification.** This view additionally takes the public confidence parameter $\delta$, with $0<\delta<1/2$.

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

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$G_t$: $t$th full stochastic gradient or subgradient observation

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$\delta$: Allowed failure probability; expected-error and probability contracts are kept distinct. **Domain:** $0<\delta<1/2$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\kappa$: Condition number $\beta/\mu$; not an independent parameter.

$$\kappa=\frac{\beta}{\mu}$$

$S$: Number of halving stages, $\max\{1,\lceil\log_2(2\Delta/\epsilon)\rceil\}$.

$$S=\max\{1,\lceil\log_2(2\Delta/\varepsilon)\rceil\}$$

$V$: Heavy-tailed statistical term at the final accuracy scale.

$$V={\frac{{\sigma}^{2}}{\mu\,\varepsilon}}^{\frac{\alpha}{2\,((\alpha-1))}}$$

$c_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<c_\alpha<\infty$.

$C_\alpha$: Positive multiplicative constant depending only on the fixed $\alpha$; uniform boundedness as $\alpha\downarrow1$ is not asserted. **Domain:** $0<C_\alpha<\infty$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$\Pr,\mathbb{P}$: Event probability after the instance and admissible response law are fixed

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Sufficiently high dimension with fixed confidence

**Region.** $d\ge C\kappa\log^2(\Delta/\varepsilon),\quad\delta=1/4$

**Views.** Deterministic / Probability guarantee

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
c_\alpha(\sqrt\kappa S+V)
$$

**Upper bound.** B1

$$
C_\alpha(\sqrt\kappa S+V)\log(2+S(\sqrt\kappa+V)/\delta)
$$

**Gap or comparison.** $\log(2+S(\sqrt\kappa+V)/\delta)$

### R2 - sufficiently high dimension

**Region.** $d\ge C\kappa\log^2(\Delta/\varepsilon)$

**Views.** Deterministic / Expected loss

**Quantity.** Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
c_\alpha(\sqrt\kappa S+V)
$$

**Upper bound.** B3

$$
C_\alpha(\sqrt\kappa S+V)\log(2+32\kappa\Delta S(\sqrt\kappa+V)/\varepsilon)
$$

**Gap or comparison.** $\log(2+32\kappa\Delta S(\sqrt\kappa+V)/\varepsilon)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - restarted clipped-SSTM

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Probability guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha(\sqrt\kappa S+V)\log(2+S(\sqrt\kappa+V)/\delta)
$$

**Sources.** [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

**Conditions.** $$\kappa=\beta/\mu\ge4,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa=\beta/\mu\ge4,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Source location.** [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf) theorem: Theorem 3.3; Theorem F.3, Eq.(189); PDF pp.7,48–50

### B2 - Exact-information and centered-moment statistical lower bounds

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The exact-noise subclass invokes an arbitrary-randomized lower bound; the centered-moment rare-event construction is also valid against arbitrary randomized adaptive algorithms. Their maximum gives the sum up to constants, in the unchanged dimension and accuracy window. The deterministic query-policy view does not narrow the actual theorem scope.

$$
c_\alpha(\sqrt\kappa S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874) [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

**Conditions.** $$d\ge C\kappa\log^2(\Delta/\varepsilon),\quad\delta=1/4$$

**Dimension conditions.** $d\ge C\kappa\log^2(\Delta/\varepsilon),\quad\delta=1/4$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1, A2

**Source location.** [1](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; quadratic reduction p.3; Eq.(7) dimension O(T²)

### B3 - Restarted clipped SSTM and the truncation conversion

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha(\sqrt\kappa S+V)\log(2+32\kappa\Delta S(\sqrt\kappa+V)/\varepsilon)
$$

**Sources.** [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

**Conditions.** $$\kappa=\beta/\mu\ge4,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $\kappa=\beta/\mu\ge4,\quad0<\varepsilon\le c\Delta$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Local argument.** A2

**Source location.** [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf) theorem: Theorem 3.3; Theorem F.3, Eq.(189); PDF pp.7,48–50

### B4 - Exact-information and centered-moment statistical lower bounds

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The exact-noise subclass invokes an arbitrary-randomized lower bound; the centered-moment rare-event construction is also valid against arbitrary randomized adaptive algorithms. Their maximum gives the sum up to constants, in the unchanged dimension and accuracy window. The deterministic query-policy view does not narrow the actual theorem scope.

$$
c_\alpha(\sqrt\kappa S+V)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.10874) [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

**Conditions.** $$d\ge C\kappa\log^2(\Delta/\varepsilon)$$

**Dimension conditions.** $d\ge C\kappa\log^2(\Delta/\varepsilon)$

**Oracle correspondence.** Applicable interfaces: stochastic full gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1, A2

**Source location.** [1](https://arxiv.org/pdf/2609.10874) theorem: Theorem 1; quadratic reduction p.3; Eq.(7) dimension O(T²)

## 5. Local arguments

### A1 - Centered-moment statistical lower bounds

**Scope.** Fresh stochastic gradients or subgradients with a centered moment bound; no exact value feedback.

**Algorithm scope.** Statistical lower bounds against arbitrary randomized algorithms; fixed confidence or expected error.

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

**Limits of the argument.** Nontrivial scale and minimizer-containment restrictions are retained. The exact optimization term is imported separately.

**Sources.** [1](https://arxiv.org/pdf/2609.10874)

### A2 - Probability-to-expectation conversion and the unit-condition endpoint

**Scope.** The primary high-probability algorithm, its localization event, and the public strong-convexity radius.

**Algorithm scope.** Deterministic query policies remain deterministic.

For a globally $\mu$-strongly convex, $\beta$-smooth objective with initial gap $\Delta$, set $R_0=\sqrt{2\Delta/\mu}$. Run the cited high-probability algorithm at accuracy $\epsilon/2$ and failure rate $\delta=\epsilon/(32\kappa\Delta)$. Its successful event includes output in $B(x^\star,2R_0)$.

Replace outputs outside $B(x_0,3R_0)$ by $x_0$. The success event is unchanged. Every retained output is within $4R_0$ of $x^\star$, so its gap is at most $16\kappa\Delta$. Expected gap is therefore at most
$\epsilon/2+\delta16\kappa\Delta\le\epsilon$.
The substituted failure rate creates the recorded logarithm. Deterministic query policies remain deterministic.

At $\kappa=1$, the objective is a known-curvature quadratic plus an unknown affine term. Averaging $b$ noisy gradients at a fixed point and taking the resulting quadratic minimizer gives expected gap at most $\sigma^2/(2\mu b)$. Integer rounding yields $O(1+\sigma^2/(\mu\epsilon))$ samples.

**Limits of the argument.** A generic probability guarantee without a bounded-loss truncation cannot be converted by this argument.

**Sources.** [2](https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf)

## References

[1] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 9 September 2026; preprint v1. Theorem 1 (PDF p. 2); strongly convex quadratic reduction (p. 3); the dimension $O(T^2)$ in equation (7) (p. 7)..

https://arxiv.org/pdf/2609.10874

[2] Abdurakhmon Sadiev, Marina Danilova, Eduard Gorbunov, Samuel Horváth, Gauthier Gidel, Pavel Dvurechensky, Alexander Gasnikov and Peter Richtárik. High-Probability Bounds for Stochastic Optimization and Variational Inequalities: the Case of Unbounded Variance. 2023; ICML 2023, PMLR 202:29563–29648; Theorems 3.2–3.3, F.3, Eq.(189), PDF pp.7,48–50.

https://proceedings.mlr.press/v202/sadiev23a/sadiev23a.pdf
