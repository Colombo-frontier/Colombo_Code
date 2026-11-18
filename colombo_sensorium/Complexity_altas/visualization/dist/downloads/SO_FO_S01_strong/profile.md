# Stochastic convex Lipschitz minimization: strong convexity on the domain; stochastic full subgradients

**Setting ID.** `SO_FO_S01_strong`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; stochastic model: Centered alpha moment noise; structure: Fresh samples

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

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

The unknown function $f$ is globally convex and $L$-Lipschitz and is $\mu$-strongly convex only on the public ball $Q=RB_2^d$. Global strong convexity and global Lipschitz continuity are not imposed simultaneously.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \mu\,R > 0,\quad \mu\,R \le \frac{L}{2}\\\varepsilon \le c\,\mu\,{R}^{2},\quad L > 0,\quad R > 0,\quad \sigma \ge 0\\\alpha > 1,\quad \alpha \le 2,\quad \mu > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \varepsilon$.

Public upper bounds: $L,\ R,\ \sigma$.

Public lower bounds: $\mu$.

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

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

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

**Region.** $((\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]})\ge L^2/(\mu\varepsilon)$

**Views.** Deterministic / Expected loss; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2, B5

$$
c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}
$$

**Upper bound.** B1, B4

$$
C_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}
$$

**Gap or comparison.** $O_\alpha(1)$

### R2 - Sufficiently high-dimensional regime with arbitrary noise level

**Region.** $d\ge C L^2/(\mu\varepsilon)$

**Views.** Deterministic / Expected loss; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2, B3, B5, B6

$$
c_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]
$$

**Upper bound.** B1, B4

$$
C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]
$$

**Gap or comparison.** $O_\alpha(1)$

### R3 - Remaining low-dimensional regime before statistical error dominates

**Region.** $\Theta_{\rm strong}\setminus(\Theta_{\rm noise}\cup\Theta_{\rm hd})$

**Views.** Deterministic / Expected loss

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B2, B3

$$
\max\{c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]},c d\log(1+L^2/(\mu\varepsilon d))\}
$$

**Upper bound.** B1

$$
C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]
$$

**Gap or comparison.** $\frac{C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]}{\max\{c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]},c d\log(1+L^2/(\mu\varepsilon d))\}}$

### R4 - Remaining low-dimensional regime before statistical error dominates

**Region.** $\Theta_{\rm strong}\setminus(\Theta_{\rm noise}\cup\Theta_{\rm hd})$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Other quantified gap

**Lower bound.** B5, B6

$$
\max\{c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]},c d\log(1+L^2/(\mu\varepsilon d))\}
$$

**Upper bound.** B4

$$
C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]
$$

**Gap or comparison.** $\frac{C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]}{\max\{c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]},c d\log(1+L^2/(\mu\varepsilon d))\}}$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$0<\mu R\le L/2,\quad0<\varepsilon\le c\mu R^2$$

**Dimension conditions.** $0<\mu R\le L/2,\quad0<\varepsilon\le c\mu R^2$

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Expected-error upper bound for clipped SGD

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]
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
c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - All-dimensional lower bound from the admissible noiseless subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c d\log(1+L^2/(\mu\varepsilon d))
$$

**Sources.** [3](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/1401.1792)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2

### B4 - Expected-error upper bound for clipped SGD

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_\alpha[L^2/(\mu\varepsilon)+(\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}]
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
c_\alpha (\sigma^2/(\mu\varepsilon))^{\alpha/[2(\alpha-1)]}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B6 - All-dimensional lower bound from the admissible noiseless subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c d\log(1+L^2/(\mu\varepsilon d))
$$

**Sources.** [3](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/1401.1792)

**Oracle correspondence.** Applicable interfaces: stochastic full subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A2

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

**Sources.** [2](https://arxiv.org/pdf/2609.10874)

### A2 - Strongly convex information-theoretic reductions

**Scope.** Exact value and one full subgradient; original query domain and public regularizer.

**Algorithm scope.** Lower bounds against arbitrary randomized adaptive algorithms.

The imported ingredients are Braun–Guzmán–Pokutta's string-guessing simulation (Lemma V.4), recursive boxes (Section IV and Lemma IV.7), and Proposition III.3. Their arbitrary-randomized local-information scope includes values and subgradients.

For $\mu R\le L/2$, put $a=L/2$ and
$$
F_s(x)=a\max_{i\le m}s_ix_i+\mu\|x\|^2/2.
$$
At $x_i=-s_i\min\{R/\sqrt m,a/(\mu m)\}$, its value is at most
$-\tfrac a2\min\{R/\sqrt m,a/(\mu m)\}$.
Whenever

$$m\le c\min\{d,(LR/\epsilon)^2,L^2/(\mu\epsilon)\},$$

any sufficiently accurate output identifies all signs. Subtracting the public quadratic leaves the imported string simulation and proves the dimension-truncated power term.

For the logarithmic term, set $R_{\rm loc}=\min\{R,\sqrt{\epsilon/\mu}\}$, $b=R_{\rm loc}/\sqrt d$, and
$$
h_s(x)=ab\max_{i\le d}\phi_{s_i}(x_i/b),\qquad
F_s=h_s+\mu\|x\|^2/2.
$$
The recursive convex one-Lipschitz functions $\phi_s$ have equal minima and continue as $|u|$ outside $[-1,1]$. A minimizer $y$ of $h_s$ lies in the small box. An $O(\epsilon)$-solution of $F_s$ is an $O(\epsilon)$-solution of $h_s$, because only the comparison term $\mu\|y\|^2/2$ enters the bound. Outside the box, a public absolute-value tail attains the maximum and supplies feedback without revealing bits. Inside, Lemma IV.7 applies. The resulting lower term is
$$
\Omega\!\left(d\log_+\!\left[{L\over\epsilon\sqrt d}
\min\{R,\sqrt{\epsilon/\mu}\}\right]\right).
$$
Combining it with the power term gives the displayed $d\log(1+H_\epsilon/d)$ rate. Markov's inequality converts expected error to constant-probability accuracy. Near the compatibility boundary, replace $a$ by $L_{\rm rem}/2$ and retain $\epsilon\le cL_{\rm rem}^2/\mu$. A globally convex Lipschitz extension is the supremum of the supporting affine functions on the compact query domain.

For matching $1\le p\le2$, use a public prox $\psi_p$ that is one-strongly convex in $\ell_p$, satisfies $\psi_p(x)\le C\Gamma_p(d)\|x\|_p^2$, and has Lipschitz constant at most $CR\Gamma_p(d)$ on $RB_p^d$. A construction is
$$
u=\max\{p,\min\{2,1+1/\log(2d)\}\},\quad
\psi_p(x)={\|x\|_u^2\over2(u-1)d^{2(1/u-1/p)}}.
$$
The squared-norm fact is supplied by Juditsky–Nesterov. In $m$ coordinates use a normalized Hadamard basis $v_i$ and
$h_s=a m^{1/p-1/2}\max_i s_i\langle v_i,x\rangle$.
The point $y=-R_{\rm loc}m^{-1/p}\sum_i s_iv_i$ has
$\|y\|_p\le R_{\rm loc}$, $h_s(y)=-aR_{\rm loc}/\sqrt m$, and
$\psi_p(y)\le C\Gamma_p(d)R_{\rm loc}^2$.
Optimizing $R_{\rm loc}\le R$ gives
$\min\{d,(LR/\epsilon)^2,L^2/[\mu\Gamma_p(d)\epsilon]\}$.
Subtract the public prox before the information simulation. Restricting $m$ to powers of two changes only constants.

For $p>2$, standard coordinate signs and $\psi_p=\|\cdot\|_2^2/2$ give
$\min\{d,(LR/\epsilon)^p,L^2/(\mu\epsilon)\}$.
Recursive boxes of half-width $R_{\rm loc}d^{-1/p}$ give the companion logarithmic term. The declared compatibility slack reserves a constant share of the Lipschitz budget for the hidden function.

For general $(p,q,r)$, set $\mu_{\rm quad}=\mu d^{2(1/r-1/2)_+}$. The public quadratic is $\mu$-strongly convex in $\ell_r$, and its gradient norm on $RB_p^d$ is at most
$\mu_{\rm quad}R d^{(1-1/p-1/q)_+}$ in $\ell_{q^\star}$.
Under the stated slack condition, a hidden single-coordinate slope of size $L/2$ is legal. The same sign and box arguments give the general formulas, with constants inside variable powers retained.

The $p>2$ upper term $(L^2/(\mu\epsilon))^{p/2}$ follows by restarting a convex $C_p(LR/u)^p$ method at error scale $u$, using radius $O(\sqrt{u/\mu})$. The geometrically decreasing stages are dominated by the final stage. These reductions do not assert uniform optimality across geometries.

**Limits of the argument.** Uses identified primary information-theoretic lemmas. Retain compatibility slack, norm dependence, and the accuracy windows.

**Sources.** [3](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/1401.1792)

## References

[1] Zijian Liu and Zhengyuan Zhou. Stochastic Nonsmooth Convex Optimization with Heavy-Tailed Noises: High-Probability Bound, In-Expectation Rate and Initial Distance Adaptation. 2023; arXiv:2303.12277v3, 20 May 2023; Theorems 5 and 9, PDF pp.6,9.

https://arxiv.org/pdf/2303.12277

[2] Ohad Shamir. A Simple Complexity Lower Bound for Solving Ax=b. 9 September 2026; preprint v1. Theorem 1 (PDF p. 2); strongly convex quadratic reduction (p. 3); the dimension $O(T^2)$ in equation (7) (p. 7)..

https://arxiv.org/pdf/2609.10874

[3] Gábor Braun; Cristóbal Guzmán; Sebastian Pokutta. Lower Bounds on the Oracle Complexity of Nonsmooth Convex Optimization via Information Theory. 2017; arXiv v3 2023.

https://arxiv.org/pdf/1407.5144

[4] Anatoli Juditsky; Yuri Nesterov. Primal-dual subgradient methods for minimizing uniformly convex functions; journal version: Deterministic and Stochastic Primal-Dual Subgradient Algorithms for Uniformly Convex Minimization. 2014.

https://arxiv.org/pdf/1401.1792
