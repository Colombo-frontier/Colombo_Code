# Global minimization of Lipschitz nonconvex functions on a bounded domain: one full subgradient

**Setting ID.** `SO_FO_N06_SG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Subgradient; operation: Subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The public feasible set is $Q=RB_2^d$. The unknown function $f:\mathbb R^d\to\mathbb R$ is globally $L$-Lipschitz, without convexity or other structural assumptions. Global minimization is required only over $Q$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad L>0,\quad R>0,\quad \varepsilon>0$$

### Oracle interface

Public numerical inputs: $d,\ \varepsilon$.

Public upper bounds: $L,\ R$.

The unknown object is the objective $f$.

Query points lie in $Q$; the response is one full subgradient:

$$g\in\partial_C f(x)$$

All responses are consistent with one fixed function instance. If several subgradients are admissible, the oracle selects one; the algorithm receives only that vector.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$f(\widehat{x})-\min_{x\in Q}f(x)$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I,\forall\text{admissible oracle responses},\quad\mathbb{E}[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial_C f(x)$: Clarke subdifferential: the closed convex hull of limits of gradients at nearby differentiability points. Global Lipschitz continuity ensures that it is nonempty, compact, and convex.

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$d$: Dimension; a public positive integer **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $0<c<1$.

$C$: Sufficiently large absolute positive constant, potentially different between theorems. The source does not give a numerical value, and it must not be set to one by the interface. **Domain:** $C>1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Return the center without querying

**Region.** $\varepsilon\ge LR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Optimal

**Lower bound.** B2, B5

$$
0
$$

**Upper bound.** B1, B4

$$
0
$$

### R2 - Nontrivial high-accuracy regime

**Region.** $0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Upper bound missing

**Lower bound.** B3

$$
c(cLR/\varepsilon)^d-1
$$

**Upper bound.** No admitted bound for this comparison

### R3 - Nontrivial high-accuracy regime

**Region.** $0<\varepsilon\le cLR$

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** Each primitive oracle query costs one call. Every query used in a finite-difference computation is charged separately.

**Status.** Upper bound missing

**Lower bound.** B6

$$
c(cLR/\varepsilon)^d-1
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon\ge LR$$

**Dimension conditions.** $\varepsilon\ge LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B2 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge LR$$

**Dimension conditions.** $\varepsilon\ge LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B3 - Hidden Lipschitz bump against arbitrary randomized local feedback

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(cLR/\varepsilon)^d-1
$$

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B4 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $$\varepsilon\ge LR$$

**Dimension conditions.** $\varepsilon\ge LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B5 - Nonnegative resource budgets

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $$\varepsilon\ge LR$$

**Dimension conditions.** $\varepsilon\ge LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

### B6 - Hidden Lipschitz bump against arbitrary randomized local feedback

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(cLR/\varepsilon)^d-1
$$

**Conditions.** $$0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1

## 5. Local arguments

### A1 - Covering and hidden-bump bounds

**Scope.** Value-subgradient access on a known bounded ball for the upper bound; local feedback for the lower bound.

**Algorithm scope.** Deterministic net upper witness; arbitrary randomized hidden-bump lower bound.

An $\epsilon/L$-net of $RB_2^d$ has at most $(1+2LR/\epsilon)^d$ points. Query all their values and return the least; Lipschitz continuity bounds the error by $\epsilon$. This upper bound requires values. At $\epsilon\ge LR$, the center suffices.

For a lower bound, pack $N\ge(cLR/\epsilon)^d$ centers $a_j$ with disjoint radius-$2\epsilon/L$ balls. Define
$$
f_j(x)=-\max\{0,2\epsilon-L\|x-a_j\|\}.
$$
Outside the hidden ball, zero value and zero subgradient are admissible. With a uniformly hidden center, each adaptive query can hit at most one previously untested support. Count the final output as one extra opportunity. If $T+1\le cN$, a constant fraction of runs miss the support and incur gap $2\epsilon$. Adjusting constants proves the expected-error lower bound for arbitrary randomized local feedback.

Constants inside the $d$th powers cannot become dimension-independent multiplicative constants. The matching conclusion concerns $\log(1+T)$, not a constant-factor formula for $T$. A bounded feasible or localization region is essential to the covering upper bound.

**Limits of the argument.** The lower and upper exponential bases need not agree by a dimension-independent factor.
