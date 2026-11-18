# Gradient and linear-minimization access: atomic-hull outputs

**Setting ID.** `SO_FO_O02_atom`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present; Bounds missing; Joint budget unresolved

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Convex body; geometry: Full space; smoothness: Lipschitz gradient; structure: Linear minimization access

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Gradient lmo; interface family: Mixed; operation: Gradient lmo; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown function $f$ is convex and $\beta$-smooth, and the unknown compact convex set $Q$ has diameter at most $D$. No free projection onto $Q$ is available. A feasible initial atom $x_0$ is public.

Feasible geometry: $Q\subset\mathbb{R}^d,\quad\operatorname{diam}(Q)\le D$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{D}^{2},\quad \beta > 0\\D > 0\end{gathered}$$

### Oracle interface

The algorithm has separate access to the exact gradient of the unknown objective and to a linear minimization oracle for the compact convex feasible set.

A gradient query at $x\in Q$ returns $\nabla f(x)$. A linear minimization query with direction $v\in\mathbb R^d$ returns an atom $a\in\arg\min_{u\in Q}\langle v,u\rangle$.

No free projection oracle is supplied. The initial feasible atom is public.

Record the simultaneous call counts $(N_G,N_{\mathrm{LMO}})$. A scalar resource projection is specified by each comparison; it does not change the available information.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

The output must lie in the convex hull of the initial atom and the atoms returned by the LMO. Directions may be chosen arbitrarily and adaptively; they are not subject to a span restriction.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

**Resource qualification.** Joint resource vector $(N_\nabla,N_{\mathrm{LMO}})$, with both coordinates charged. Compare only budget pairs achieved together by one algorithm.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

The output must lie in the convex hull of the initial atom and the atoms returned by the LMO. Directions may be chosen arbitrarily and adaptively; they are not subject to a span restriction.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Resource qualification.** The selected resource is $N_{\mathrm{LMO}}$, with one unit per linear-minimization call. Gradient calls are also retained in the same algorithm's joint budget.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q\subset\mathbb{R}^d,\quad\operatorname{diam}(Q)\le D$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\operatorname{LMO}_Q$: Exact linear minimization oracle for a supplied direction

$$\operatorname{LMO}_Q(v)\in\arg\min_{u\in Q}\langle v,u\rangle$$

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$D$: Public upper bound on the Euclidean diameter of the feasible set. **Domain:** $D>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$N_{\nabla},N_{\mathrm{LMO}}$: Gradient and linear-minimization call counts achieved by the same algorithm **Domain:** All are nonnegative integers.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\lceil a\rceil$: Smallest integer greater than or equal to $a$

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Linear-minimization calls $N_{\mathrm{LMO}}$; gradient costs are recorded separately

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - achievable resource region

**View.** Deterministic / Pointwise guarantee

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Joint resource vector

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Linear-minimization calls $N_{\mathrm{LMO}}$; gradient costs are recorded separately

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - High-dimensional bottleneck for atomic LMO access

**Region.** $d\ge C\beta D^2/\varepsilon$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** Linear-minimization calls $N_{\mathrm{LMO}}$; gradient costs are recorded separately

**Status.** Optimal

**Lower bound.** B2, B6

$$
c\beta D^2/\varepsilon
$$

**Upper bound.** B1, B5

$$
C\beta D^2/\varepsilon
$$

**Gap or comparison.** $O(1)$

### R2 - Nontrivial accuracy on a compact convex domain

**Region.** $0<\varepsilon\le c\beta D^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Linear-minimization calls $N_{\mathrm{LMO}}$; gradient costs are recorded separately

**Status.** Other quantified gap

**Lower bound.** B2, B4

$$
\max\{1,\lceil\min\{d/2,\beta D^2/(4\varepsilon)\}\rceil-1\}
$$

**Upper bound.** B1

$$
C\beta D^2/\varepsilon
$$

**Gap or comparison.** $\frac{C\beta D^2/\varepsilon}{\max\{1,\lceil\min\{d/2,\beta D^2/(4\varepsilon)\}\rceil-1\}}$

### R3 - Nontrivial accuracy on a compact convex domain

**Region.** $0<\varepsilon\le c\beta D^2$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q2

**Resource.** Joint resource vector

**Status.** Joint budget unresolved

**Achievable budgets.** B3

**Necessary constraints.** No admitted claim in this comparison

### R4 - Nontrivial accuracy on a compact convex domain

**Region.** $0<\varepsilon\le c\beta D^2$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** Linear-minimization calls $N_{\mathrm{LMO}}$; gradient costs are recorded separately

**Status.** Other quantified gap

**Lower bound.** B6, B7

$$
\max\{1,\lceil\min\{d/2,\beta D^2/(4\varepsilon)\}\rceil-1\}
$$

**Upper bound.** B5

$$
C\beta D^2/\varepsilon
$$

**Gap or comparison.** $\frac{C\beta D^2/\varepsilon}{\max\{1,\lceil\min\{d/2,\beta D^2/(4\varepsilon)\}\rceil-1\}}$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - LMO coordinate of the resource vector attained by CGS

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\beta D^2/\varepsilon
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf)

**Conditions.** $$0<\varepsilon\le c\beta D^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta D^2$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf) theorem: Corollary3 Eqs.(2.31)–(2.32); Theorem6 Eqs.(2.42)–(2.44); PDF pp.10,13

### B2 - Support-size argument for a quadratic on the simplex

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\lceil\min\{d/2,\beta D^2/(4\varepsilon)\}\rceil-1
$$

**Sources.** [2](https://arxiv.org/pdf/1309.5550)

**Conditions.** $$0<\varepsilon\le c\beta D^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta D^2$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1309.5550) theorem: Algorithm1 andTheorem1; PDF p.5

### B3 - Joint resource budget of CGS

**Admission.** Included in the bracket

**Direction.** achievable

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
(C\sqrt{\beta D^2/\varepsilon},C\beta D^2/\varepsilon)
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf)

**Conditions.** $$0<\varepsilon\le c\beta D^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta D^2$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** The error bound holds separately for every admissible instance.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf) theorem: Corollary3 Eqs.(2.31)–(2.32); Theorem6 Eqs.(2.42)–(2.44); PDF pp.10,13

### B4 - Atomic-hull outputs require at least one LMO call

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{D}^{2},\quad \beta > 0\\D > 0\end{gathered}$$

**Dimension conditions.** $\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{D}^{2},\quad \beta > 0\\D > 0\end{gathered}$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B5 - LMO coordinate of the resource vector attained by CGS

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\beta D^2/\varepsilon
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf)

**Conditions.** $$0<\varepsilon\le c\beta D^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta D^2$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf) theorem: Corollary3 Eqs.(2.31)–(2.32); Theorem6 Eqs.(2.42)–(2.44); PDF pp.10,13

### B6 - Support-size argument for a quadratic on the simplex

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\lceil\min\{d/2,\beta D^2/(4\varepsilon)\}\rceil-1
$$

**Sources.** [2](https://arxiv.org/pdf/1309.5550)

**Conditions.** $$0<\varepsilon\le c\beta D^2$$

**Dimension conditions.** $0<\varepsilon\le c\beta D^2$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1309.5550) theorem: Algorithm1 andTheorem1; PDF p.5

### B7 - Atomic-hull outputs require at least one LMO call

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{D}^{2},\quad \beta > 0\\D > 0\end{gathered}$$

**Dimension conditions.** $\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{D}^{2},\quad \beta > 0\\D > 0\end{gathered}$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

## 5. Local arguments

### A1 - An atomic-hull output requires an LMO call

**Scope.** Gradient and LMO access, with outputs in the hull of the initial and returned atoms.

**Algorithm scope.** Lower bound for every algorithm, randomized or deterministic.

With zero LMO calls, the convex hull of the public initial atom and returned atoms is the singleton $x_0$, on every execution path. Choose
$Q=\{te_1:0\le t\le D\}$, $x_0=0$, and $f(x)=-Mx_1$, where $MD>\epsilon$.
The function is convex and zero-smooth and therefore satisfies any positive smoothness upper bound. Its optimum is the opposite endpoint, while the initial gap is $MD$. Gradient queries do not enlarge the available atomic hull. At least one LMO call is necessary, including for randomized algorithms. This lower bound concerns the LMO coordinate of the joint budget.

**Limits of the argument.** This is a lower bound on the LMO resource only and relies on the atomic-hull output restriction.

## References

[1] Guanghui Lan and Yi Zhou. Conditional Gradient Sliding for Convex Optimization. 2016; author manuscript 2014; Corollary 3 and Theorem 6, manuscript PDF pp.10 and 13.

https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf

[2] Guanghui Lan. The Complexity of Large-scale Convex Programming under a Linear Optimization Oracle. 2013; Algorithm 1 and Theorem 1, PDF p.5.

https://arxiv.org/pdf/1309.5550
