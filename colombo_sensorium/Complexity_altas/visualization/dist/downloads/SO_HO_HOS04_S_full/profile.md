# Stochastic nonconvex first-order stationarity with independent fresh samples: complete Hessians

**Setting ID.** `SO_HO_HOS04_S_full`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Fully optimal

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Stochastic; interface family: Fresh gradient full hessian; operation: Fresh gradient full hessian; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the full objective, namely $\|\nabla f(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is bounded below.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

The objective is $C^2$, with an $\beta$-Lipschitz gradient and an $M_2$-Lipschitz Hessian.

The derivative estimates need not arise from one scalar sample loss. Conditional moments and independence are specified by the oracle.

### Oracle interface

At any $x\in\mathbb{R}^d$, draw a fresh sample and return the complete $(g_j(x))_{j=1}^{2}$. Conditional on the history and query, every derivative estimate is unbiased and satisfies

$$\mathbb{E}[g_j(x)\mid\mathcal{H}]=D^jf(x),\qquad\mathbb{E}[\|g_j(x)-D^jf(x)\|_{\mathrm{op}}^2\mid\mathcal{H}]\le\sigma_j^2.$$

Each call uses a sample independent of the previous history. Sample identities are hidden and cannot be reused, and no function value is returned. Estimates of different derivative orders need not arise from the same scalar sample loss.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $\beta$, $M_2$, $\varepsilon_g$, $\sigma_1$, $\sigma_2$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\|\nabla f(\widehat{x})\|_2.$$

The criterion uses the gradient norm itself. Squared norms, expectations, and probability guarantees are recorded separately and are not substituted automatically.

### Resource accounting

Each complete stochastic response specified under ORACLE costs one unit; each fresh-sample response within a batch is charged separately.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\|\nabla f(\widehat{x})\|_2\le \varepsilon_g\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private seed and oracle sampling.

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,2\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$\mathcal{H}$: The complete history before the current query. Conditional unbiasedness and moment bounds are evaluated after the query is selected and before the fresh sample is drawn.

$g_j(x)$: Full tensor estimate of the derivative of order $j$ returned from one fresh sample. **Domain:** $1\le j\le 2$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$k$: The highest derivative order in this specification is fixed at two. **Domain:** $k=2$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$\beta$: Gradient Lipschitz budget **Domain:** $\beta>0$.

$M_2$: Hessian Lipschitz bound **Domain:** $M_2>0$.

$\varepsilon_g$: Gradient tolerance **Domain:** $\varepsilon_g>0$.

$\sigma_1$: Root-mean-square gradient error **Domain:** $\sigma_1>0$.

$\sigma_2$: Root mean-square error of the Hessian estimate **Domain:** $\sigma_2>0$.

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(k,\Delta,\beta,M_2,\sigma_1,\sigma_2).$$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete (g,H) response costs one call and can simulate one HVP. Internal computation is free. If the original algorithm has random cost, budget truncation and the joint-event constants in its proof yield a fixed cap.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete (g,H) response costs one call and can simulate one HVP. Internal computation is free. If the original algorithm has random cost, budget truncation and the joint-event constants in its proof yield a fixed cap.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete (g,H) response costs one call and can simulate one HVP. Internal computation is free. If the original algorithm has random cost, budget truncation and the joint-event constants in its proof yield a fixed cap.

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Fixed positive second-order scales and sufficient dimension

**Region.** $k=2,\ \theta=(\Delta,\beta,M_2,\sigma_1,\sigma_2)>0\ {\rm fixed},\quad0<\varepsilon_g\le c(\theta),\quad d\ge C D_g\Delta/\varepsilon_g$

**Quantity.** Q1

**Resource.** Each complete (g,H) response costs one call and can simulate one HVP. Internal computation is free. If the original algorithm has random cost, budget truncation and the joint-event constants in its proof yield a fixed cap.

**Status.** Optimal

**Lower bound.** B3

$$
c(\theta)\varepsilon_g^{-3}
$$

**Upper bound.** B1

$$
C(\theta)\varepsilon_g^{-3}
$$

**Gap or comparison.** $O_\theta(1)$

### R2 - The gradient requirement holds automatically

**Region.** $\varepsilon_g^2\ge2\beta\Delta$

**Quantity.** Q2

**Resource.** Each complete (g,H) response costs one call and can simulate one HVP. Internal computation is free. If the original algorithm has random cost, budget truncation and the joint-event constants in its proof yield a fixed cap.

**Status.** Optimal

**Lower bound.** B5

$$
0
$$

**Upper bound.** B4

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** At any $x\in\mathbb{R}^d$, draw a fresh sample and return the complete $(g_j(x))_{j=1}^{2}$. Conditional on the history and query, every derivative estimate is unbiased and satisfies

**Guarantee mapping.** Success probability at least 2/3 for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete stochastic response specified under ORACLE costs one unit; each fresh-sample response within a batch is charged separately.

### B1 - Stochastic gradient method with recursive HVP variance reduction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C[\Delta\sigma_1\sigma_2/\varepsilon_g^3+\Delta\sqrt{M_2}\sigma_1/\varepsilon_g^{5/2}+\Delta\beta/\varepsilon_g^2]
$$

**Sources.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf)

**Conditions.** $0<\varepsilon_g<\min\{\sigma_1,\sqrt{\Delta\beta}\},\quad k=2$

**Dimension conditions.** $0<\varepsilon_g<\min\{\sigma_1,\sqrt{\Delta\beta}\},\quad k=2$

**Source location.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) theorem: Theorem 2; pdf pages: 8

### B2 - Stochastic cubic trust-region method with complete-matrix averaging

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C[\Delta\sigma_1\sigma_2\sqrt{\log(2+d)}/\varepsilon_g^3+\Delta\sqrt{M_2}\sigma_1/\varepsilon_g^{5/2}]
$$

**Sources.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf)

**Conditions.** $0<\varepsilon_g<\sigma_1,\quad k=2$

**Dimension conditions.** $0<\varepsilon_g<\sigma_1,\quad k=2$

**Source location.** [1](https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf) theorem: Theorem 3; pdf pages: 9

### B3 - Joint information lower bound for a common scalar sample loss

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(\theta)\varepsilon_g^{-3}
$$

**Sources.** [2](https://arxiv.org/pdf/2609.28238v2)

**Conditions.** $k=2,\ \theta=(\Delta,\beta,M_2,\sigma_1,\sigma_2)>0\ {\rm fixed},\quad0<\varepsilon_g\le c(\theta),\quad d\ge C D_g\Delta/\varepsilon_g$

**Dimension conditions.** $k=2,\ \theta=(\Delta,\beta,M_2,\sigma_1,\sigma_2)>0\ {\rm fixed},\quad0<\varepsilon_g\le c(\theta),\quad d\ge C D_g\Delta/\varepsilon_g$

**Source location.** [2](https://arxiv.org/pdf/2609.28238v2) theorem: Theorem F.3; (F.14)-(F.16); pdf pages: 35

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_g^2\ge2\beta\Delta$

**Dimension conditions.** $\varepsilon_g^2\ge2\beta\Delta$

**Local argument.** A1

### B5 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_g^2\ge2\beta\Delta$

**Dimension conditions.** $\varepsilon_g^2\ge2\beta\Delta$

**Local argument.** A1

## 5. Local arguments

### A1 - Zero-query and polynomial-recovery endpoints

**Scope.** Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

**Algorithm scope.** Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

Zero-query guarantees follow from a public initial-error bound. A zero highest-order regularity modulus permits exact polynomial recovery from one complete jet.

For a full-space differentiable objective with $f(x_0)-\inf f\le\Delta$, the condition $\Delta=0$ makes $x_0$ a global minimizer. Its gradient is zero, and its Hessian is positive semidefinite whenever it exists. Thus first-order and spectral second-order stationarity require no query. An objective-gap target also requires no query when $\varepsilon_f\ge\Delta$. Nonnegative query cost proves exact optimality of these zero bounds.

If a public gradient-Lipschitz bound $\beta$ is part of the specification, the descent lemma gives $\|\nabla f(x_0)\|^2\le2\beta\Delta$. For convex full-space objectives with a minimizer within distance $R$, it also gives $f(x_0)-f^*\le\beta R^2/2$ and $\|\nabla f(x_0)\|\le\beta R$. These sufficient zero-query regions require that explicit first-order regularity assumption. If only the highest derivative is controlled, positive quadratics can have arbitrary curvature and arbitrarily large initial gap despite zero highest-order modulus.

On a connected Euclidean domain, $M_k=0$ or $M_{k,\nu}=0$ makes $D^kf$ constant, so $f$ is a polynomial of degree at most $k$. One complete jet determines all coefficients. Under the specified free internal computation, a known polynomial can then be optimized on a compact public domain, or combined with a public regularizer and solved through the declared known-model interface.

A bounded-below polynomial on the full space need not attain its infimum. For approximate spectral stationarity, shift $x_0$ to zero and minimize $f(x)+\eta\|x\|^2/2$. This function is coercive, and its minimizer $x_\eta$ satisfies $\eta\|x_\eta\|^2/2\le\Delta$, $\|\nabla f(x_\eta)\|\le\sqrt{2\eta\Delta}$, and $\nabla^2f(x_\eta)\succeq-\eta I$. Choosing $\eta\le\min\{\varepsilon_H,\varepsilon_g^2/(2\Delta)\}$ meets both targets. For global objective accuracy, exact polynomial coefficients permit arbitrary-accuracy internal global optimization; no additional unknown-function query is needed.

To exclude zero queries in a nontrivial region, choose two positive quadratics centered on opposite sides of $x_0$, with the same public budgets and disjoint acceptable-output sets. A zero-query algorithm has the same output distribution on both instances, so their success probabilities sum to at most one. It cannot succeed with probability at least $2/3$ on each. With only highest-order regularity, curvature can be increased until the acceptable sets are disjoint at any prescribed positive accuracy and positive localization radius. In an initial-gap model with additional curvature restrictions, retain the bound's explicit accuracy and compatibility window.

If both a global PL constant $\mu$ and a gradient-Lipschitz upper bound $\beta$ are supplied, then $2\mu(f-f_*)\le\|\nabla f\|^2\le2\beta(f-f_*)$. When $\mu>\beta>0$, every gap is zero and the class contains only constant objectives. This degeneracy does not apply without the extra $\beta$ assumption.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] Yossi Arjevani; Yair Carmon; John C. Duchi; Dylan J. Foster; Ayush Sekhari; Karthik Sridharan. Second-Order Information in Non-Convex Stochastic Optimization: Power and Limitations. COLT 2020, PMLR 125:242-299, proceedings PDF.

https://proceedings.mlr.press/v125/arjevani20a/arjevani20a.pdf

[2] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Second-Order Stationarity with Common Random Losses: Matching Tolerance Bounds. arXiv:2609.28238v2 (2026-10-19); latest history checked 2026-10-29.

https://arxiv.org/pdf/2609.28238v2
