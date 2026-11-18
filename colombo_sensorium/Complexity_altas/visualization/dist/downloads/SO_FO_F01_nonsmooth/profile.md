# Finite-sum minimization with convex components: components Lipschitz on the domain; selected component subgradients

**Setting ID.** `SO_FO_F01_nonsmooth`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; convexity: Convex components; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; structure: Finite sum

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component subgradient; operation: Component subgradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}F(x)$$

The complete objective is the finite sum $F(x)=n^{-1}\sum_{i=1}^n f_i(x)$. Component information is available only through the declared component oracle.

### Admissible model

The $n$ unknown components are convex and $L$-Lipschitz. The feasible ball is public, and $F$ is their average. Every returned subgradient satisfies $g_i\in\partial f_i(x)$ and $\|g_i\|\le L$.

Feasible geometry: $Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad \varepsilon \le c\,L\,R\\d \ge C\,{\frac{L\,R}{\varepsilon}}^{2},\quad L > 0,\quad R > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $L,\ R$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in Q$ and receives the following information about that component.

$$g_i\in\partial f_i(x),\quad\|g_i\|\le L$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

Exact Euclidean projection onto the public domain; its internal computation is free

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in Q}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One selected-component subgradient costs one call. Uniform random index selection is algorithmic randomization.

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

$f_i,F$: Unknown components and finite-sum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^n f_i(x)$$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in Q}F(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f_i(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f_i(x)=\{g:f_i(u)\ge f_i(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f_i\}$$

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One selected-component subgradient costs one call. Uniform random index selection is algorithmic randomization.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nonsmooth convex finite-sum minimization

**Region.** $0<\varepsilon\le cLR,\quad d\ge C(LR/\varepsilon)^2$

**Quantity.** Q1

**Resource.** One selected-component subgradient costs one call. Uniform random index selection is algorithmic randomization.

**Status.** Optimal

**Lower bound.** B2

$$
c L^2R^2/\varepsilon^2
$$

**Upper bound.** B1

$$
C L^2R^2/\varepsilon^2
$$

**Gap or comparison.** $O(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$0<\varepsilon\le cLR,\quad d\ge C(LR/\varepsilon)^2$$

**Dimension conditions.** $0<\varepsilon\le cLR,\quad d\ge C(LR/\varepsilon)^2$

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Stochastic subgradient descent with uniformly sampled components

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C L^2R^2/\varepsilon^2
$$

**Sources.** [1](https://www2.isye.gatech.edu/~nemirovs/SIOPT_RSA_2009.pdf)

**Oracle correspondence.** Applicable interfaces: selected component subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://www2.isye.gatech.edu/~nemirovs/SIOPT_RSA_2009.pdf) theorem: §2.2, Eqs.(2.19)–(2.21); finite sum uniform sampling

### B2 - Replication of the same hard function

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c L^2R^2/\varepsilon^2
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Oracle correspondence.** Applicable interfaces: selected component subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: TheoremV.1; replicate same component n times

## References

[1] Arkadi Nemirovski, Anatoli Juditsky, Guanghui Lan and Alexander Shapiro. Robust Stochastic Approximation Approach to Stochastic Programming. 2009; Section 2.2, equations (2.19)-(2.21), PDF p.7; uniform finite-sum sampling reduction.

https://www2.isye.gatech.edu/~nemirovs/SIOPT_RSA_2009.pdf

[2] Gábor Braun; Cristóbal Guzmán; Sebastian Pokutta. Lower Bounds on the Oracle Complexity of Nonsmooth Convex Optimization via Information Theory. 2017; arXiv v3, 2023. Theorems IV.2, V.1, and VI.5; Propositions V.5 and VI.7 and their proofs. IEEE Transactions on Information Theory 63(7):4709–4724. The dimension range in Theorem VI.3 is not adopted without its required qualifications..

https://arxiv.org/pdf/1407.5144
