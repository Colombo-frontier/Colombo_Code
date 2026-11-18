# Nonconvex finite-sum optimization: global PL condition and mean-square smoothness; selected component gradients

**Setting ID.** `SO_FO_F03_pl_mean_square_G`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; growth: Global polyak lojasiewicz; smoothness: Lipschitz gradient; smoothness: Mean square smoothness; structure: Finite sum

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component gradient; operation: Component gradient; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Failure probability parameter explicitly declared; mode: Expectation; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; budget: Worst-instance expected cost; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}F(x)$$

The complete objective is the finite sum $F(x)=n^{-1}\sum_{i=1}^n f_i(x)$. Component information is available only through the declared component oracle.

### Admissible model

Let $F=n^{-1}\sum_{i=1}^n f_i$ have initial suboptimality at most $\Delta$. The components satisfy $n^{-1}\sum_i\|\nabla f_i(x)-\nabla f_i(y)\|^2\le\beta^2\|x-y\|^2$. The average satisfies a global $\mu$-PL inequality; convexity is not required.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

The global PL inequality is $\|\nabla F(x)\|_2^2\ge2\mu(F(x)-F^\star)$ for every $x\in\mathbb R^d$.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad \beta > 0\\\Delta > 0,\quad \mu > 0,\quad \mu \le \beta\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $\beta,\Delta$. Public lower bound: $\mu$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in\mathbb R^d$ and receives the following information about that component.

$$\nabla f_i(x)$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One primitive response for a selected component at one point costs one call. Computing the full average gradient requires $n$ component calls.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Resource qualification.** Cost is bounded in expectation for every instance: $\sup_{I,\mathcal O}\mathbb E N_A\le T$. This contract is not replaced by a fixed bound on every execution path.

#### Randomized / Probability guarantee

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}:\ \mathbb{P}(\ell(I,\widehat{x})>\varepsilon)\le\delta$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

**Resource qualification.** Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

**Oracle qualification.** This view additionally takes the public confidence parameter $\delta$, with $0<\delta<1/2$.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f_i,F$: Unknown components and finite-sum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^n f_i(x)$$

$\nabla F$: Full gradient of the differentiable complete objective with respect to the decision variable

$\nabla f_i$: Full gradient of differentiable component $i$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\mu$: Known lower bound on the global PL modulus **Domain:** $\mu>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\kappa$: $\beta/\mu$, where $\mu$ denotes the PL constant.

$$\kappa=\frac{\beta}{\mu}$$

$d_{\rm dense}$: Sufficient dimension for the Dense Weak Hiding construction. The worst case is over finite dimensions, and the threshold grows with the parameters or budget; no numerical threshold is supplied here. **Domain:** $d_{\rm dense}(n,\beta,\mu,\Delta,\varepsilon)$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$\delta$: Allowed failure probability; expected-error and probability contracts are kept distinct. **Domain:** $0<\delta<1/2$.

$p_0$: Universal positive failure-probability threshold in the source lower bound; no numerical value is supplied. **Domain:** $0<p_0<1$.

$\Pr,\mathbb{P}$: Event probability after the instance and admissible response law are fixed

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized / Probability guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Sufficient dimension for the small-condition-number PL regime

**Region.** $3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad\theta\in\Theta_{\rm PL}$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Status.** Optimal

**Lower bound.** B2

$$
c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Upper bound.** B1

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Gap or comparison.** $O(1)$

### R2 - Sufficient dimension for the large-condition-number PL regime

**Region.** $\kappa\ge\sqrt n,\quad d\ge d_{\rm dense},\quad\theta\in\Theta_{\rm PL}$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Status.** Optimal

**Lower bound.** B4

$$
c[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Upper bound.** B3

$$
C[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Gap or comparison.** $O(1)$

### R3 - Zero-query accuracy

**Region.** $\varepsilon\ge\Delta$

**Views.** Randomized / Expected loss

**Quantity.** Q1

**Resource.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B5

$$
0
$$

### R4 - Lower-bound branch at fixed confidence

**Region.** $0<\delta<p_0,\quad\delta\text{fixed in advance},\quad d\ge d_{\rm dense}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q2

**Resource.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Status.** Optimal

**Lower bound.** B7

$$
c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Upper bound.** B6

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Gap or comparison.** $O(1)$

### R5 - Lower-bound branch at fixed confidence

**Region.** $0<\delta<p_0,\quad\delta\text{fixed in advance},\quad d\ge d_{\rm dense}$

**Views.** Randomized / Probability guarantee

**Quantity.** Q2

**Resource.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Status.** Optimal

**Lower bound.** B9

$$
c[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Upper bound.** B8

$$
C[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Gap or comparison.** $O(1)$

### R6 - Zero-query accuracy

**Region.** $\varepsilon\ge\Delta$

**Views.** Randomized / Probability guarantee

**Quantity.** Q3

**Resource.** Evaluating a specified component at one point costs one call; a full gradient costs $n$. If stopping times are allowed, cost is evaluated using the declared budget mode.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B10

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - restarted PAGE

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$\theta\in\Theta_{\rm PL},\quad\kappa\le\sqrt n$$

**Dimension conditions.** $\theta\in\Theta_{\rm PL},\quad\kappa\le\sqrt n$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Section7, PropositionE.2; AppendixF

### B2 - Dense weak hiding against arbitrary randomized IFO-FG algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad\theta\in\Theta_{\rm PL}$$

**Dimension conditions.** $3\le\kappa\le\sqrt n,\quad d\ge d_{\rm dense},\quad\theta\in\Theta_{\rm PL}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Theorem3.1, Corollary3.2, Theorem3.3; AppendixF; AppendixG.1 n₀=1024

### B3 - restarted PAGE

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Randomized witness

$$
C[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$\theta\in\Theta_{\rm PL},\quad\kappa\ge\sqrt n$$

**Dimension conditions.** $\theta\in\Theta_{\rm PL},\quad\kappa\ge\sqrt n$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Section7, PropositionE.2; AppendixF

### B4 - Dense weak hiding against arbitrary randomized IFO-FG algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$\kappa\ge\sqrt n,\quad d\ge d_{\rm dense},\quad\theta\in\Theta_{\rm PL}$$

**Dimension conditions.** $\kappa\ge\sqrt n,\quad d\ge d_{\rm dense},\quad\theta\in\Theta_{\rm PL}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Theorem3.1, Corollary3.2, Theorem3.3; AppendixF; AppendixG.1 n₀=1024

### B5 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [3](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2

### B6 - restarted PAGE

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
C[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$0<\delta<p_0,\quad\delta\text{fixed in advance}$$

**Dimension conditions.** $0<\delta<p_0,\quad\delta\text{fixed in advance}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Section7, PropositionE.2; AppendixF

### B7 - Dense weak hiding against arbitrary randomized IFO-FG algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[n+n\log(\Delta/\varepsilon)/(1+\log(\sqrt n/\kappa))]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$0<\delta<p_0,\quad\delta\text{fixed in advance},\quad d\ge d_{\rm dense}$$

**Dimension conditions.** $0<\delta<p_0,\quad\delta\text{fixed in advance},\quad d\ge d_{\rm dense}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Theorem3.1, Corollary3.2, Theorem3.3; AppendixF; AppendixG.1 n₀=1024

### B8 - restarted PAGE

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Randomized witness

$$
C[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$0<\delta<p_0,\quad\delta\text{fixed in advance}$$

**Dimension conditions.** $0<\delta<p_0,\quad\delta\text{fixed in advance}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, require the declared success probability for the specified residual event. The failure-probability parameter remains subject to the stated validity region.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Section7, PropositionE.2; AppendixF

### B9 - Dense weak hiding against arbitrary randomized IFO-FG algorithms

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c[n+\kappa\sqrt n\log(\Delta/\varepsilon)]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** $$0<\delta<p_0,\quad\delta\text{fixed in advance},\quad d\ge d_{\rm dense}$$

**Dimension conditions.** $0<\delta<p_0,\quad\delta\text{fixed in advance},\quad d\ge d_{\rm dense}$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2609.00045v3) theorem: Theorem3.1, Corollary3.2, Theorem3.3; AppendixF; AppendixG.1 n₀=1024

### B10 - Return the initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Probability guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [3](https://arxiv.org/pdf/1405.4980)

**Conditions.** $$\varepsilon\ge\Delta$$

**Dimension conditions.** $\varepsilon\ge\Delta$

**Oracle correspondence.** Applicable interfaces: selected component values and gradients, selected component gradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1, A2

## 5. Local arguments

### A1 - Finite-sum simulation and hidden components

**Scope.** Exact component gradients; the declared average objective and component regularity.

**Algorithm scope.** Deterministic full-gradient upper witnesses; lower constructions preserve their source algorithm scopes.

A full gradient of $F=n^{-1}\sum_i f_i$ costs $n$ component calls. Mean-square smoothness implies
$$
\|\nabla F(x)-\nabla F(y)\|
\le(n^{-1}\sum_i\|\nabla f_i(x)-\nabla f_i(y)\|^2)^{1/2}
\le\beta\|x-y\|.
$$
Individual smoothness also implies this. Full-gradient convex, strongly convex, PL, stationarity, and certificate algorithms therefore transfer with an $n$ multiplier. A zero-query endpoint remains zero. Convexity or PL of the average must be stated separately.

For an unrestricted smooth finite-sum $\Omega(n)$ baseline, hide an index $J$. All components have public quadratic curvature $\beta$; only component $J$ has an unknown linear term $\mp n\beta R x_1$. Their average is
$\beta\|x\|^2/2\mp\beta Rx_1$, with minimizer distance $R$. Until $J$ is queried, its sign is hidden. A budget much smaller than $n$ misses it with constant probability, giving loss of order $\beta R^2$. This construction requires a model allowing the component linear offsets.

For an expected-budget lower-bound conversion, truncate after a sufficiently large constant multiple of the expected budget. Markov's inequality makes truncation unlikely enough to preserve a constant-probability hard-instance lower bound. This does not convert an expected-budget upper bound to a pathwise budget.

Replicating the same hard function in every component preserves its one-function lower bound without multiplying by $n$. This covers nonsmooth strongly convex and one-dimensional logarithmic subclasses.

In the cited span-restricted construction, individual smoothness is $\sqrt n$ times the native mean-square parameter. Substitute native parameter $\beta/\sqrt n$ to obtain the recorded individual-smoothness lower bound. Keep the original span, dimension, and accuracy restrictions. Rescaling does not expand the lower algorithm class.

**Limits of the argument.** Replication gives no extra factor n. The rescaled lower theorem remains span-restricted.

**Sources.** [2](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [3](https://arxiv.org/pdf/1405.4980)

### A2 - Descent, PL contraction, and zero-query endpoints

**Scope.** The exact smooth, PL, Clarke, Moreau, or composite residual specified in the associated bound.

**Algorithm scope.** Deterministic upper witnesses and elementary indistinguishability lower bounds.

Global $\beta$-smoothness and boundedness below imply
$$
f(x-\nabla f(x)/\beta)\le f(x)-\|\nabla f(x)\|^2/(2\beta).
$$
Thus $\|\nabla f(x_0)\|^2\le2\beta\Delta$. Summing the decrease and returning the queried point with least gradient norm gives $O(1+\beta\Delta/\epsilon^2)$ calls; values are unnecessary. If the initial gradient bound already meets the tolerance, output $x_0$ without querying.

A globally $\beta$-Lipschitz gradient gives Hessian norm at most $\beta$, so the second-order zero-query regime additionally requires permitted negative curvature at least $\beta$.

For a global $\mu$-PL objective,
$\mathrm{gap}_{t+1}\le(1-1/\kappa)\mathrm{gap}_t$.
This proves the exact ceiling formula for $1<\kappa$. At $\kappa=1$, one step is exact, and opposite translated quadratics exclude zero calls at nontrivial accuracy. At $\epsilon\ge\Delta$, the initial point suffices.

In one dimension, PL excludes nonoptimal stationary points. The minimizer set is an interval. Integrating
$|f'|\ge\sqrt{2\mu(f-f^\star)}$
along the decreasing side shows that a minimizer lies within $\sqrt{2\Delta/\mu}$ of $x_0$. Derivative-sign bisection and smoothness therefore give $O(\log(2+\kappa\Delta/\epsilon))$ calls.

Clarke subgradients of a globally $L$-Lipschitz function have norm at most $L$, so Goldstein residuals are at most $L$, also at radius zero. For a $\rho$-weakly convex function, proximal optimality gives
$\|\nabla f_{1/(2\rho)}(x_0)\|\le L$; the proximal objective inequality gives its square at most $4\rho\Delta$.
For a smooth composite objective, proximal-gradient descent gives
$F(y)\le F(x)-\|\mathcal G_\beta(x)\|^2/(2\beta)$,
so $\|\mathcal G_\beta(x_0)\|^2\le2\beta\Delta$.
These bounds certify the corresponding zero-query outputs; the output contract does not require computing the residual.

**Limits of the argument.** Each endpoint uses its own residual and model; the metrics are not interchangeable.

## References

[1] Yuxing Peng, Zhiqing Tang and Weijia Jia. Dense Weak Hiding: Closing Complexity Gaps in Nonconvex and PL Finite-Sum Optimization under Individual Smoothness. 2026, arXiv v3 preprint; Theorems 3.1 and 3.3; Corollary 3.2; Proposition E.2; Appendices F and G.1.

https://arxiv.org/pdf/2609.00045v3

[2] Dongruo Zhou and Quanquan Gu. Lower Bounds for Smooth Nonconvex Finite-Sum Optimization. 2019; Definition 3.3; Theorem 4.2; Section 4.3 and Proposition 4.9.

https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf

[3] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980
