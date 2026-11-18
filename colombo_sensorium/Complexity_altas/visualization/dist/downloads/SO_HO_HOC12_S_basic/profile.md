# Quasi-self-concordant convex composite objectives: exact second derivatives with sublevel-set control

**Setting ID.** `SO_HO_HOC12_S_basic`

Single-objective optimization

Solve $\min_{x\in Q}F(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Full space; smoothness: Quasi self concordant; structure: Composite

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet 2; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in Q}F(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The full objective is $F=f+\psi$, where $f$ is convex and $C^3$, and $\psi$ is proper, closed, and convex. For all relevant points and directions,

$$|D^3f(x)[u,u,v]|\le M_{\mathrm{qsc}}D^2f(x)[u,u]\|v\|_2.$$

The objective has a finite infimum, and the public initial point $x_0$ satisfies $F(x_0)-\inf_{x\in \operatorname{dom}\psi}F(x)\le\Delta$.

The initial sublevel set $\{x:F(x)\le F(x_0)\}$ has Euclidean diameter at most $D$. A norm bound $G_0$ is given for the selected initial composite subgradient $g_0\in\partial F(x_0)$.

### Oracle interface

Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The complete regularizer $\psi$ is known. Regularized Taylor and mirror models involving $\psi$ may be solved globally for free, with the associated subgradient or normal-cone element selected. Unknown derivatives in the models must still be obtained through paid queries.

The public inputs are $x_0$, the target accuracy, and $d$, $M_{\rm qsc}$, $\Delta$, $\varepsilon_f$, $D$, $G_0$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in Q$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=F(\widehat{x})-F^*.$$

Here $F^*=\inf_{x\in Q}F(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$F(\widehat{x})-F^*\le \varepsilon_f.$$

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,3\}$ and $D^0f=f$.

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

$f,\psi,F$: Unknown smooth term, public composite term, and full objective.

$$F=f+\psi.$$

$\operatorname{dom}\psi$: Effective domain of the regularizer, which is the feasible set.

$$\operatorname{dom}\psi=\{x:\psi(x)<+\infty\}.$$

$\partial F(x)$: Set of all convex subgradients; a subgradient is obtained only through an explicitly permitted auxiliary operation.

$F^*$: Global infimum of the full objective over its effective domain.

$$F^*=\inf_{x\in\operatorname{dom}\psi}F(x).$$

$Q$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$M_{\rm qsc}$: Quasi-self-concordance constant in the fixed Euclidean norm **Domain:** $M_{\rm qsc}\ge0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$D$: Upper bound on the Euclidean diameter of the initial composite-objective sublevel set **Domain:** $D>0$.

$G_0$: Upper bound on the norm of a selected initial composite subgradient; it may be obtained from the first query **Domain:** $G_0\ge0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Bounded level set and initial subgradient

**Region.** $D>0,\ G_0\ge0$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(1+M_{\rm qsc}D\log(2\Delta/\varepsilon_f)+\log(2+DG_0/\varepsilon_f))
$$

### R2 - The known initial-gap bound already satisfies the target accuracy

**Region.** $\varepsilon_f\ge\Delta$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B3

$$
0
$$

**Upper bound.** B2

$$
0
$$

### R3 - Zero quasi-self-concordance endpoint of the basic specification

**Region.** $M_{\rm qsc}=0,\ 0<\varepsilon_f<\Delta$

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B4

$$
1
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in Q$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Gradient-regularized Newton method

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+M_{\rm qsc}D\log(2\Delta/\varepsilon_f)+\log(2+DG_0/\varepsilon_f))
$$

**Sources.** [1](https://arxiv.org/pdf/2308.14742v1)

**Conditions.** $D>0,\ G_0\ge0$

**Dimension conditions.** $D>0,\ G_0\ge0$

**Source location.** [1](https://arxiv.org/pdf/2308.14742v1) theorem: Corollary 3.4, Eq.(46); pdf pages: 16

### B2 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A1

### B3 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A1

### B4 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{\rm qsc}=0,\ 0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_{\rm qsc}=0,\ 0<\varepsilon_f<\Delta$

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

[1] Nikita Doikov. Minimizing Quasi-Self-Concordant Functions by Gradient Regularization of Newton Method. arXiv:2308.14742v1; Mathematical Programming219 (2026), DOI10.1007/s10107-025-02270-9.

https://arxiv.org/pdf/2308.14742v1
