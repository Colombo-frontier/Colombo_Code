# Gradient and linear-minimization access: hidden strongly convex feasible set

**Setting ID.** `SO_FO_O02_hidden_curve`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Convex body; geometry: Full space; geometry: Hidden feasible set; geometry: Strongly convex set; smoothness: Lipschitz gradient

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Gradient lmo; interface family: Mixed; operation: Gradient lmo; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The unknown compact convex set $Q$ has diameter at most $D$ and satisfies $tx+(1-t)y+B_2(0,\mu_Qt(1-t)\|x-y\|^2/2)\subseteq Q$. The objective is $\beta$-smooth and $\mu$-strongly convex. Access to $Q$ is limited to an LMO and the initial point; neither a complete domain description nor free projection is supplied.

Feasible geometry: $Q\subset\mathbb{R}^d,\quad\operatorname{diam}(Q)\le D$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Here $\beta$-smoothness means $\|\nabla f(u)-\nabla f(v)\|_2\le\beta\|u-v\|_2$ for all $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad \mu > 0,\quad \mu \le \beta\\\mu_Q > 0,\quad T \ge 1,\quad \beta > 0,\quad D > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon,\ T$.

Public upper bounds: $\beta,D$. Public lower bound on set curvature: $\mu_Q$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of gradients and linear minimization:

$$(\nabla f(x),\operatorname{LMO}_Q(v))$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

The feasible set is accessed only through an LMO. Its complete description and a free projection operation are not provided.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=f(\widehat{x})-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

Each LMO call costs one unit. After budget $T$, the criterion is worst-case expected suboptimality risk; gradient costs are recorded separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

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

$\mu_Q$: Public lower bound on the set's strong-convexity constant, with units of inverse length. **Domain:** $\mu_Q>0$.

$D$: Public upper bound on the Euclidean diameter of the feasible set. **Domain:** $D>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$T$: Integer budget in the native budget-risk theorem. **Domain:** $T\ge1$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$N_{\nabla},N_{\mathrm{LMO}}$: Gradient and linear-minimization call counts achieved by the same algorithm **Domain:** All are nonnegative integers.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - fixed budget risk

$$
R^\star_{v,\pi}(B;\theta)=\inf_{\mathcal A\in\mathfrak A_v:\ C_\pi(\mathcal A,I)\le B\ \forall I}\sup_I\mathbb E[\ell(I,\mathcal A)]
$$

**Definition.** Error risk under the prescribed fixed budget

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Native curvature window for the randomized hidden-domain lower bound

**Region.** $\mu=\beta,\quad d=64(T+1),\quad\mu_QD=\Theta(1/d)$

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Other quantified gap

**Lower bound.** B2

$$
c\beta D^2/(T+1)^2
$$

**Upper bound.** B1

$$
C[\beta D^2+\beta^2/(\mu\mu_Q^2)]/(T+2)^2
$$

**Gap or comparison.** $O(1+\beta/(\mu\mu_Q^2D^2))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Garber–Hazan risk bound

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T\le C[\beta D^2+\beta^2/(\mu\mu_Q^2)]/(T+2)^2
$$

**Sources.** [1](https://proceedings.mlr.press/v37/garbera15.pdf)

**Conditions.** $$0<\mu\le\beta,\quad\mu_Q>0,\quad T\ge1$$

**Dimension conditions.** $0<\mu\le\beta,\quad\mu_Q>0,\quad T\ge1$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://proceedings.mlr.press/v37/garbera15.pdf) theorem: Theorem2; PDF p.3

### B2 - Pokutta's hidden-domain risk bound for arbitrary randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T\ge c\beta D^2/(T+1)^2
$$

**Sources.** [2](https://arxiv.org/pdf/2610.13590v1)

**Conditions.** $$\mu=\beta,\quad d=64(T+1),\quad\mu_QD=\Theta(1/d)$$

**Dimension conditions.** $\mu=\beta,\quad d=64(T+1),\quad\mu_QD=\Theta(1/d)$

**Oracle correspondence.** Applicable interfaces: gradients and linear minimization. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/2610.13590v1) theorem: Theorem2.7; Corollary2.8; Theorem2.9; PDF pp.6–7

## References

[1] Dan Garber and Elad Hazan. Faster Rates for the Frank-Wolfe Method over Strongly-Convex Sets. 2015; Theorem 2, PDF p.3.

https://proceedings.mlr.press/v37/garbera15.pdf

[2] Sebastian Pokutta. Lower Bounds for Randomized Linear-Oracle Optimization over Strongly Convex Sets. 2026, arXiv v1 preprint; Theorem 2.7; Corollary 2.8; Theorem 2.9; pp.6-7.

https://arxiv.org/pdf/2610.13590v1
