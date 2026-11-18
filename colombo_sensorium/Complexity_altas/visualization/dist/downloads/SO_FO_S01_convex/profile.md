# Stochastic convex Lipschitz minimization: centered-moment noise; stochastic full subgradients

**Setting ID.** `SO_FO_S01_convex`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; stochastic model: Centered alpha moment noise; structure: Fresh samples

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown function $f$ is globally convex and $L$-Lipschitz. The ball $Q=RB_2^d$ is public, and queries are restricted to $Q$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,L\,R,\quad L > 0\\R > 0,\quad \sigma \ge 0,\quad \alpha > 1,\quad \alpha \le 2\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \varepsilon$.

Public upper bounds: $L,\ R,\ \sigma$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of stochastic full subgradients:

$$G_t,\quad \mathbb{E}_tG_t\in\partial f(x_t),\quad\mathbb{E}_t\|G_t-\mathbb{E}_tG_t\|^\alpha\le\sigma^\alpha$$

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

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f(x)=\{g:f(u)\ge f(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f\}$$

$G_t$: $t$th full stochastic gradient or subgradient observation

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

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

$\log_+$: Truncated positive logarithm

$$\log_+u=\max\{0,\log u\}$$

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

### R1 - Statistically dominated regime in all dimensions

**Region.** $((\sigma R/\varepsilon)^{\alpha/(\alpha-1)})\ge (LR/\varepsilon)^2$

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

### R2 - Sufficiently high-dimensional regime with arbitrary noise level

**Region.** $d\ge C (LR/\varepsilon)^2$

**Views.** Deterministic / Expected loss; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2, B3, B5, B6

$$
c_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Upper bound.** B1, B4

$$
C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Gap or comparison.** $O_\alpha(1)$

### R3 - Remaining low-dimensional regime before statistical error dominates

**Region.** $\Theta_{\rm convex}\setminus(\Theta_{\rm noise}\cup\Theta_{\rm hd})$

**Views.** Deterministic / Expected loss

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B2, B3

$$
\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]\}
$$

**Upper bound.** B1

$$
C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Gap or comparison.** $\frac{C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]}{\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]\}}$

### R4 - Remaining low-dimensional regime before statistical error dominates

**Region.** $\Theta_{\rm convex}\setminus(\Theta_{\rm noise}\cup\Theta_{\rm hd})$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B5, B6

$$
\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]\}
$$

**Upper bound.** B4

$$
C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Gap or comparison.** $\frac{C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]}{\max\{c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)},c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]\}}$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Expected-error upper bound for clipped SGD

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Sources.** [1](https://arxiv.org/pdf/2303.12277)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Source location.** [1](https://arxiv.org/pdf/2303.12277) theorem: Theorems 5 and 9; PDF pp.6,9

### B2 - One-dimensional statistical lower bound under a centered-moment assumption

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - All-dimensional lower bound from the admissible noiseless subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1; Proposition V.5; Euclidean specialization and truncation

### B4 - Expected-error upper bound for clipped SGD

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha[(LR/\varepsilon)^2+(\sigma R/\varepsilon)^{\alpha/(\alpha-1)}]
$$

**Sources.** [1](https://arxiv.org/pdf/2303.12277)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the declared randomness and control the underlying error. Query policies and postprocessing use no private random numbers; all randomness comes from observations.

**Source location.** [1](https://arxiv.org/pdf/2303.12277) theorem: Theorems 5 and 9; PDF pp.6,9

### B5 - One-dimensional statistical lower bound under a centered-moment assumption

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_\alpha (\sigma R/\varepsilon)^{\alpha/(\alpha-1)}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B6 - All-dimensional lower bound from the admissible noiseless subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1; Proposition V.5; Euclidean specialization and truncation

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

**Sources.** [3](https://arxiv.org/pdf/2609.10874)

## References

[1] Zijian Liu and Zhengyuan Zhou. Stochastic Nonsmooth Convex Optimization with Heavy-Tailed Noises: High-Probability Bound, In-Expectation Rate and Initial Distance Adaptation. 2023; arXiv:2303.12277v3, 20 May 2023; Theorems 5 and 9, PDF pp.6,9.

https://arxiv.org/pdf/2303.12277

[2] Gábor Braun; Cristóbal Guzmán; Sebastian Pokutta. Lower Bounds on the Oracle Complexity of Nonsmooth Convex Optimization via Information Theory. 2017; arXiv v3, 2023. Theorems IV.2, V.1, and VI.5; Propositions V.5 and VI.7 and their proofs. IEEE Transactions on Information Theory 63(7):4709–4724. The dimension range in Theorem VI.3 is not adopted without its required qualifications..

https://arxiv.org/pdf/1407.5144

[3] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 9 September 2026; preprint v1. Theorem 1 (PDF p. 2); strongly convex quadratic reduction (p. 3); the dimension $O(T^2)$ in equation (7) (p. 7)..

https://arxiv.org/pdf/2609.10874
