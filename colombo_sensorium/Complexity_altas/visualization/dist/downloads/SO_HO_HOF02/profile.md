# Finite-sum convex objective accuracy under mean-Hessian regularity

**Setting ID.** `SO_HO_HOF02`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}F(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Other quantified gap present; Bounds missing

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Mean squared hessian lipschitz; structure: Finite sum

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Incremental full second order; operation: Incremental full second order; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; adaptivity: Explicit restriction; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Worst-instance expected cost; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}F(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The full objective $F=n^{-1}\sum_{i=1}^n f_i$ is convex. Each $f_i:\mathbb{R}^d\to\mathbb{R}$ is $C^2$ and may be nonconvex.

$$\left(\frac1n\sum_{i=1}^n\|\nabla^2f_i(x)-\nabla^2f_i(y)\|_{\mathrm{op}}^2\right)^{1/2}\le M_2\|x-y\|_2.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

### Oracle interface

Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

The public inputs are $x_0$, the target accuracy, and $d$, $n$, $R$, $M_2$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=F(\widehat{x})-F^*.$$

Here $F^*=\inf_{x\in \mathbb{R}^d}F(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each complete component second-order response costs one unit, and a full scan for population second-order information costs $n$ calls. The resource guarantee is the per-instance expected call count $\mathbb{E}N\le B$, not a fixed cap on every execution path.

### Algorithm views and success guarantees

#### Unrestricted

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\mathbb{E}\!\left[F(\widehat{x})-F^*\right]\le \varepsilon_f.$$

Expectation or probability is evaluated after fixing the instance; component sampling is part of the algorithm's private randomness.

The running-cost guarantee is specified separately under RESOURCE.

**Output qualification.** The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

**Resource qualification.** Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

#### Restricted uniform index

Use the algorithm class in TK26, Assumption 2: indices are drawn independently and uniformly from $\{1,\ldots,n\}$, and each new iterate belongs to the sum of previously generated spaces. A local space may be extended only by linear combinations of available vectors and solutions of linear systems formed from queried component gradients and Hessians.

The source protocol permits the update form $h=a\nabla f_i(x)+b\nabla^2f_i(x)h$; query points and final iterates must satisfy its subspace restrictions. This original protocol is retained and does not represent arbitrary adaptive-index strategies or unrestricted matrix operations.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\mathbb{E}\!\left[F(\widehat{x})-F^*\right]\le \varepsilon_f.$$

Expectation or probability is evaluated after fixing the instance; component sampling is part of the algorithm's private randomness.

The running-cost guarantee is specified separately under RESOURCE.

**Output qualification.** Unqueried outputs are permitted but must still satisfy the spatial or support restrictions of the algorithm class.

**Resource qualification.** Internal computation consistent with the algorithm-class restrictions is free; free computation does not remove the stated linear-algebra or index-selection restrictions.

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

$J_{2}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x)).$$

$f_i,F,F^*$: Unknown component functions, mean objective, and population optimal value. **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^nf_i(x),\qquad F^*=\inf_{x\in\mathbb{R}^d}F(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$n$: Number of components **Domain:** $n\in\mathbb{N}_{\ge 1}$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$M_2$: Mean-square Hessian Lipschitz budget **Domain:** $M_2>0$.

$\varepsilon_f$: Expected objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$h,a,b$: Vectors and arbitrary real coefficients in the restricted algorithm's generation rule; $h$ does not denote a composite outer function here.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Unrestricted

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete component second-order response costs one call; a full batch costs n. The randomized loop is measured by its expected call count, not an unstated fixed worst-case cap. Internal proximal and model computations are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Restricted uniform index

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete component second-order response costs one call; a full batch costs n. The randomized loop is measured by its expected call count, not an unstated fixed worst-case cap. Internal proximal and model computations are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Principal validity domain

**Region.** $n\ge1,\quad M_2,R,\varepsilon_f>0$

**Views.** Unrestricted

**Quantity.** Q1

**Resource.** Each complete component second-order response costs one call; a full batch costs n. The randomized loop is measured by its expected call count, not an unstated fixed worst-case cap. Internal proximal and model computations are free.

**Status.** Other quantified gap

**Lower bound.** B2

$$
cn
$$

**Upper bound.** B1

$$
C[n\log(n+1)+n^{6/7}(M_2R^3/\varepsilon_f)^{2/7}]
$$

**Gap or comparison.** $O(\log(n+1)+n^{-1/7}(M_2R^3/\varepsilon_f)^{2/7})$

### R2 - The initialization term dominates

**Region.** $(M_2R^3/\varepsilon_f)^{2/7}\le n^{1/7}\log(n+1)$

**Views.** Unrestricted

**Quantity.** Q1

**Resource.** Each complete component second-order response costs one call; a full batch costs n. The randomized loop is measured by its expected call count, not an unstated fixed worst-case cap. Internal proximal and model computations are free.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
cn
$$

**Upper bound.** B1

$$
Cn\log(n+1)
$$

**Gap or comparison.** $O(\log(n+1))$

### R3 - Dimension window for the restricted lower bound in TK26

**Region.** $d\ge2\lfloor(M_2R^3/(300\sqrt n\,\varepsilon_f))^{2/7}\rfloor,\quad\text{nontrivial accuracy range of Thm 2}$

**Views.** Restricted uniform index

**Quantity.** Q2

**Resource.** Each complete component second-order response costs one call; a full batch costs n. The randomized loop is measured by its expected call count, not an unstated fixed worst-case cap. Internal proximal and model computations are free.

**Status.** Upper bound missing

**Lower bound.** B3

$$
c[n+n^{6/7}(M_2R^3/\varepsilon_f)^{2/7}]
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

**Guarantee mapping.** Expected-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete component second-order response costs one unit, and a full scan for population second-order information costs $n$ calls. The resource guarantee is the per-instance expected call count $\mathbb{E}N\le B$, not a fixed cap on every execution path.

### B1 - Randomized accelerated regularized Newton method with complete scans

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted

**Witness or lower-bound scope.** Randomized witness

$$
C[n\log(n+1)+n^{6/7}(M_2R^3/\varepsilon_f)^{2/7}]
$$

**Sources.** [1](https://arxiv.org/pdf/2610.10495v1)

**Conditions.** $n\ge1,\quad M_2,R,\varepsilon_f>0$

**Dimension conditions.** $n\ge1,\quad M_2,R,\varepsilon_f>0$

**Source location.** [1](https://arxiv.org/pdf/2610.10495v1) theorem: Theorem 1; Corollary 1; pdf pages: 7

### B2 - Hide an unknown linear term in one component; all other Hessians are identical

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cn
$$

**Conditions.** $n\ge1,\quad M_2,R,\varepsilon_f>0$

**Dimension conditions.** $n\ge1,\quad M_2,R,\varepsilon_f>0$

**Local argument.** A1

### B3 - Randomized zero-chain for restricted algorithms with uniform indices

**Admission.** Included in the bracket

**Direction.** lower

**View.** Restricted uniform index

**Witness or lower-bound scope.** The stated restricted randomized class

$$
c[n+n^{6/7}(M_2R^3/\varepsilon_f)^{2/7}]
$$

**Sources.** [1](https://arxiv.org/pdf/2610.10495v1)

**Conditions.** $d\ge2\lfloor(M_2R^3/(300\sqrt n\,\varepsilon_f))^{2/7}\rfloor,\quad\text{nontrivial accuracy range of Thm 2}$

**Dimension conditions.** $d\ge2\lfloor(M_2R^3/(300\sqrt n\,\varepsilon_f))^{2/7}\rfloor,\quad\text{nontrivial accuracy range of Thm 2}$

**Source location.** [1](https://arxiv.org/pdf/2610.10495v1) theorem: Assumption 2; Theorem 2; Appendix B.3; pdf pages: 7

## 5. Local arguments

### A1 - Hidden-component lower bound under expected call cost

**Scope.** Selectable component full jets, expected objective gap, and expected or fixed work. No curvature cap limiting the chosen $\lambda$ unless separately checked.

**Algorithm scope.** Selectable component full jets, expected objective gap, and expected or fixed work. No curvature cap limiting the chosen $\lambda$ unless separately checked.

An unqueried hidden linear term yields an $\Omega(n)$ initialization lower bound for convex finite sums, including expected-resource specifications.

Let I be uniform on $\{1,\ldots,n\}$, independent of a uniform sign Z, and set $x_0=0$. For $\lambda=8\varepsilon_f/R^2$, define
$$f_i(x)=\lambda x^2/2-n\lambda R Z\,\mathbf1\{i=I\}x.$$
The mean minimizer is $RZ$, every component Hessian is the same constant $\lambda$, and all Hessian-Lipschitz budgets are zero. Until I is queried, values, gradients, and Hessians reveal no Z. Conditional on any no-hit transcript, the sign remains uniform and every output has expected gap at least $\lambda R^2/2=4\varepsilon_f$. To have expected gap at most $\varepsilon_f$ on each instance, the prior-averaged hit probability must be at least 3/4.

Before a hit, index choices cannot exploit information about I. Comparing with the first $\lfloor n/2\rfloor$ distinct indices on the no-hit path gives hit probability at most $1/2+\Pr(\tau\ge n/2)$, where $\tau$ is total calls. Markov gives $\Pr(\tau\ge n/2)\le2\mathbb E\tau/n$. Hence $\mathbb E\tau\ge n/8$, with an adjusted universal constant for small n. This directly matches expected-resource accounting; it does not require converting a fixed-budget theorem.

The argument certifies an initialization term only. It does not prove a high-accuracy $n^{6/7}$ term or remove linear-algebra restrictions from a primary theorem.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] Artem Tsedenov; Dmitry Kovalev. An Optimal Second-Order Algorithm for Finite-Sum Optimization under Average Smoothness and Convexity. arXiv:2610.10495v1 (2026-10-07); latest history checked 2026-10-29.

https://arxiv.org/pdf/2610.10495v1
