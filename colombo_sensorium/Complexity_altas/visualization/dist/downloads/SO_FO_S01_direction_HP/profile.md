# Stochastic convex Lipschitz minimization: directional moment bounds and a composite objective; high-probability risk; stochastic full subgradients

**Setting ID.** `SO_FO_S01_direction_HP`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; stochastic model: Directional moment noise; structure: Composite

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Stochastic subgradient; operation: Stochastic subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Failure probability parameter explicitly declared; mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Samples; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \mathbb{R}^d}F(x)$$

The complete objective is $F=f+h$. The properties and Oracle interfaces of the two terms are specified separately.

### Admissible model

The objective is $f+h$. The function $f$ is convex and $L$-Lipschitz; $h$ is public, proximable, and $\mu$-strongly convex, with $\mu=0$ allowed. A minimizer lies within distance $R$ of $x_0$. The centered noise norm has $\alpha$th moment at most $\sigma^\alpha$, and every unit-direction projection has $\alpha$th moment at most $\sigma_{\mathrm{dir}}^\alpha$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Write $F=f+h$ and $F^\star=\inf_{x\in\mathbb R^d}F(x)$. The public proximal term $h$ is $\mu$-strongly convex; when $\mu=0$, only convexity is required. The directional centered-moment condition is $\mathbb E_t|\langle u,G_t-\mathbb E_tG_t\rangle|^\alpha\le\sigma_{\mathrm{dir}}^\alpha$ for every unit vector $u$.

Admissible parameter domain:

$$d\in\mathbb{N}_{\ge1},\quad L,R>0,\quad\mu\ge0,\quad0<\sigma_{\rm dir}\le\sigma,\quad1<\alpha\le2,\quad0<\delta<1/2,\quad T\in\mathbb{N}_{\ge1}$$

### Oracle interface

Public numerical inputs: $d,\ \alpha,\ \delta,\ T,\ x_0$.

Public upper bounds: $L,\ R,\ \sigma,\ \sigma_{\rm dir}$.

Public lower bounds: $\mu$.

The unknown object is the objective $f$. Access to the composite term $h$, including public information and proximal operations, is specified by the interface below.

Query points lie in $\mathbb{R}^d$; feedback consists of stochastic full subgradients:

$$G_t,\quad \mathbb{E}_tG_t\in\partial f(x_t),\quad\mathbb{E}_t\|G_t-\mathbb{E}_tG_t\|^\alpha\le\sigma^\alpha$$

Every observation is fresh. Same-point batches are conditionally independent, and the conditional moment bounds hold uniformly over histories. Samples cannot be reused across points.

The exact proximal map of the public function $h$ is available at zero query cost.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,x)=F(x)-F^\star,\qquad F=f+h$$

$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\mathcal{R}_{T,\delta}=\inf_{A:N_A\le T}\inf\{r\ge0:\sup_{I,\mathcal{O}}\Pr(\ell(I,A^{\mathcal{O}})>r)\le\delta\}$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

The budget-to-risk curve is $\mathcal R_{T,\delta}=\inf_{A:N_A\le T}\inf\{r\ge0:\sup_{I,\mathcal O}\Pr(\ell(I,A^{\mathcal O})>r)\le\delta\}$. The budget $T$ is fixed, and the comparison concerns high-probability error. A risk rate is not a query-complexity rate.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f,h,F$: Smooth or Lipschitz term, convex proximal term, and complete objective

$$F=f+h$$

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f(x)=\{g:f(u)\ge f(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f\}$$

$\operatorname{prox}_{\eta h}$: Proximal map of $h$, either public or obtained through the declared interface **Domain:** $\eta>0,\ v\in\mathbb{R}^d$.

$$\operatorname{prox}_{\eta h}(v)=\arg\min_u\{h(u)+\|u-v\|_2^2/(2\eta)\}$$

$\operatorname{dom}h$: Effective domain of $h$

$$\operatorname{dom}h=\{x:h(x)<+\infty\}$$

$G_t$: $t$th full stochastic gradient or subgradient observation

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$\mathcal{R}_{T,\delta}$: Minimax quantile risk at budget $T$ and failure probability $\delta$; defined in the guarantee

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\mu$: Lower bound on the strong-convexity modulus of the public proximal term $h$; zero permits a merely convex proximal term **Domain:** $\mu\ge0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\alpha$: Order of the centered noise moment. Every bound with a subscripted constant treats this order as fixed; uniformity as it approaches one is not asserted. **Domain:** $1<\alpha\le2$.

$\sigma_{\rm dir}$: Centered-moment scale in an arbitrary unit direction. **Domain:** $0<\sigma_{\rm dir}\le\sigma$.

$\delta$: Allowed failure probability; expected-error and probability contracts are kept distinct. **Domain:** $0<\delta<1/2$.

$T$: Integer budget in the native budget-risk theorem. **Domain:** $T\ge1$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$\Pr,\mathbb{P}$: Event probability after the instance and admissible response law are fixed

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

### R1 - High-probability contract under directional moment bounds

**Region.** $0<\sigma_{\rm dir}\le\sigma,\ 0<\delta<1/2,\ T\ge1,\ \mu\ge0$

**Quantity.** Q1

**Resource.** Error risk under the prescribed fixed budget

**Status.** Both bounds missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence
