# Gradient and linear-minimization access: strongly convex objective and atomic-hull outputs

**Setting ID.** `SO_FO_O02_strong_function_joint`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Convex body; geometry: Full space; smoothness: Lipschitz gradient; structure: Linear minimization access

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Gradient lmo; interface family: Mixed; operation: Gradient lmo; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; computation: Internal arithmetic uncharged; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown function $f$ is convex and $\beta$-smooth, and the unknown compact convex set $Q$ has diameter at most $D$. No free projection onto $Q$ is available. A feasible initial atom $x_0$ is public. In addition, $f$ is $\mu$-strongly convex and the initial suboptimality is at most $\Delta$.

Feasible geometry: $Q\subset\mathbb{R}^d,\quad\operatorname{diam}(Q)\le D$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \varepsilon \le c\,\beta\,{D}^{2},\quad \mu > 0\\\mu \le \beta,\quad \varepsilon \le c\,\Delta,\quad \beta > 0,\quad D > 0\\\Delta > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta,\ D,\ \Delta$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of gradients and linear minimization:

$$(\nabla f(x),\operatorname{LMO}_Q(v))$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

No free projection

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

The pair $(N_{\nabla},N_{\rm LMO})$ must be achieved by one algorithm; its coordinates cannot be selected from different algorithms.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

The output must lie in the convex hull of the initial atom and the atoms returned by the LMO. Directions may be chosen arbitrarily and adaptively; they are not subject to a span restriction.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

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

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$D$: Public upper bound on the Euclidean diameter of the feasible set. **Domain:** $D>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\kappa$: Function condition number $\beta/\mu$; the set-curvature parameter $\mu_Q$ is separate.

$$\kappa=\frac{\beta}{\mu}$$

$N_{\nabla},N_{\mathrm{LMO}}$: Gradient and linear-minimization call counts achieved by the same algorithm **Domain:** All are nonnegative integers.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

## 3. Complexity bracket

### Compared quantities

#### Q1 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Joint resource vector

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Strongly convex function

**Region.** $0<\mu\le\beta,\quad0<\varepsilon\le c\Delta$

**Quantity.** Q1

**Resource.** Joint resource vector

**Status.** Joint budget unresolved

**Achievable budgets.** B1

**Necessary constraints.** No admitted claim in this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$0<\mu\le\beta,\quad0<\varepsilon\le c\Delta$$

**Dimension conditions.** $0<\mu\le\beta,\quad0<\varepsilon\le c\Delta$

**Oracle mapping.** Applicable interfaces: gradients and linear minimization. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee mapping.** The error bound holds separately for every admissible instance.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Joint CGS budget under strong convexity

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Deterministic witness

$$
(C\sqrt\kappa\log(C\Delta/\varepsilon),C[\beta D^2/\varepsilon+\sqrt\kappa\log(C\Delta/\varepsilon)])
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf)

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf) theorem: Corollary3 Eqs.(2.31)–(2.32); Theorem6 Eqs.(2.42)–(2.44); PDF pp.10,13

## References

[1] Guanghui Lan and Yi Zhou. Conditional Gradient Sliding for Convex Optimization. 2016; author manuscript 2014; Corollary 3 and Theorem 6, manuscript PDF pp.10 and 13.

https://optimization-online.org/wp-content/uploads/2014/10/4605.pdf
