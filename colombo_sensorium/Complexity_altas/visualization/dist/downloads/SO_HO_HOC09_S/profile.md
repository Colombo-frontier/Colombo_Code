# Uniformly convex composite minimization with higher-order derivatives

**Setting ID.** `SO_HO_HOC09_S`

Single-objective optimization

Solve $\min_{x\in Q}F(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; convexity: Uniformly convex; geometry: Euclidean ball; geometry: Full space; smoothness: Kth derivative holder; structure: Composite

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Full jet; operation: Exact jet k; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in Q}F(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The full objective is $F=f+\psi$. The smooth term $f$ is convex and $C^k$ on an open convex neighborhood of $\operatorname{dom}\psi$. The term $\psi$ is proper, closed, convex, and extended-real-valued, and may include an indicator of convex constraints.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_{k,\nu}\|x-y\|_{2}^{\nu}.$$

Fix $k\ge2$ and $0<\nu\le1$, and set $s=k+\nu$.

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

The full objective $F$ additionally satisfies uniform convexity of order $r$, with $r\ge2$ and $\mu_r>0$:

$$F(y)\ge F(x)+\langle v,y-x\rangle+\frac{\mu_r}{r}\|y-x\|_2^r,\quad v\in\partial F(x),\quad x,y\in\operatorname{dom}\psi.$$

Highest-order smoothness is imposed on $f$, and uniform convexity on $F$.

### Oracle interface

Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The complete regularizer $\psi$ is known. Regularized Taylor and mirror models involving $\psi$ may be solved globally for free, with the associated subgradient or normal-cone element selected. Unknown derivatives in the models must still be obtained through paid queries.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $M_{k,\nu}$, $\nu$, $r$, $\mu_r$, $R$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

#### Deterministic

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$F(\widehat{x})-F^*\le \varepsilon_f.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[F(\widehat{x})-F^*\le \varepsilon_f\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private random seed.

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,k\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$J_{k}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x)).$$

$f,\psi,F$: Unknown smooth term, public composite term, and full objective.

$$F=f+\psi.$$

$\operatorname{dom}\psi$: Effective domain of the regularizer, which is the feasible set.

$$\operatorname{dom}\psi=\{x:\psi(x)<+\infty\}.$$

$\partial F(x)$: Set of all convex subgradients; a subgradient is obtained only through an explicitly permitted auxiliary operation.

$F^*$: Global infimum of the full objective over its effective domain.

$$F^*=\inf_{x\in\operatorname{dom}\psi}F(x).$$

$Q$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{+}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}, k\ge2$.

$M_{k,\nu}$: Global $\nu$-Hölder upper bound for the order-$k$ derivative in the specified tensor norm. **Domain:** $M_{k,\nu}\ge0$.

$\nu$: Hölder exponent of the highest derivative **Domain:** $0<\nu\le1$.

$s$: Sum of the highest derivative order and its Hölder exponent. **Domain:** $s>2$.

$$s=k+\nu.$$

$a$: Complexity exponent associated with the highest-order regularity. **Domain:** $a>0$.

$$a=\frac{2}{3\,s-(2)}.$$

$r$: Order of uniform convexity; distinct from the oracle order and norm exponent **Domain:** $r\ge2$.

$\mu_r$: Lower bound on the order-r uniform-convexity modulus of F; smoothness is imposed only on f **Domain:** $\mu_r>0$.

$R$: Radius of the known ball. **Domain:** $R\ge0$.

$\varepsilon_f$: Objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$c_{k,\nu,r}$: Sufficient window constants depending only on the fixed orders or exponents in their subscripts; existence is asserted without numerical values. **Domain:** $0<c_{k,\nu,r}<1$.

$Q_r$: Dimensionless ratio of uniform-convexity growth to highest-order regularity, used only when the localization radius is positive. **Domain:** $Q_r\ge0\quad(R>0)$.

$$Q_r=\frac{M_{k,\nu}\,((R)^{s-(r)})}{\mu_r}.$$

$E_r$: Local objective-gap scale used only when $r<s$. **Domain:** $E_r>0\quad(r<s,\ M_{k,\nu}>0)$.

$$E_r=(\frac{(\mu_r)^{s}}{(M_{k,\nu})^{r}})^{\frac{1}{s-(r)}}.$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Superlinear local regime when $r<s$

**Region.** $r<s$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_{k,\nu,r}(1+Q_r^{a}+\log(1+\log(1+E_r/\varepsilon_f)))
$$

### R2 - Linear-convergence regime when $r=s$

**Region.** $r=s$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

$$
O_{k,\nu,r}([1+(M_{k,\nu}/\mu_r)^a]\log(2+M_{k,\nu}R^s/\varepsilon_f))
$$

### R3 - Polynomial high-accuracy regime when $r>s$

**Region.** $r>s,\ \varepsilon_f\le c\mu_rR^r$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
O_{k,\nu,r}(1+(M_{k,\nu}/\mu_r)^a(\mu_r/\varepsilon_f)^{a(r-s)/r}+\log(2+R(\mu_r/\varepsilon_f)^{1/r}))
$$

### R4 - The localization or feasible ball degenerates to the initial point

**Region.** $R=0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B5, B12

$$
0
$$

**Upper bound.** B4, B11

$$
0
$$

### R5 - Zero highest-order regularity modulus

**Region.** $M_{k,\nu}=0,\ R>0$

**Views.** Deterministic; Randomized

**Quantity.** Q2; Q4

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Optimal

**Lower bound.** B7, B14

$$
1
$$

**Upper bound.** B6, B13

$$
1
$$

**Gap or comparison.** $1$

### R6 - Superlinear local regime when $r<s$

**Region.** $r<s$

**Views.** Randomized

**Quantity.** Q3

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B8

$$
O_{k,\nu,r}(1+Q_r^{a}+\log(1+\log(1+E_r/\varepsilon_f)))
$$

### R7 - Linear-convergence regime when $r=s$

**Region.** $r=s$

**Views.** Randomized

**Quantity.** Q3

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B9

$$
O_{k,\nu,r}([1+(M_{k,\nu}/\mu_r)^a]\log(2+M_{k,\nu}R^s/\varepsilon_f))
$$

### R8 - Polynomial high-accuracy regime when $r>s$

**Region.** $r>s,\ \varepsilon_f\le c\mu_rR^r$

**Views.** Randomized

**Quantity.** Q3

**Resource.** Each complete jet costs one unit, under a fixed worst-case call budget. Tensor operations, linear algebra, and global solution of known regularized models are free; this is not an arithmetic-time complexity measure.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B10

$$
O_{k,\nu,r}(1+(M_{k,\nu}/\mu_r)^a(\mu_r/\varepsilon_f)^{a(r-s)/r}+\log(2+R(\mu_r/\varepsilon_f)^{1/r}))
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in Q$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Geometric-radius restarts of higher-order composite acceleration, followed by a local model when $r<s$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,r}(1+Q_r^{a}+\log(1+\log(1+E_r/\varepsilon_f)))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $r<s$

**Dimension conditions.** $r<s$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2, A3

### B2 - Geometric-radius restarts of higher-order composite acceleration, followed by a local model when $r<s$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,r}([1+(M_{k,\nu}/\mu_r)^a]\log(2+M_{k,\nu}R^s/\varepsilon_f))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $r=s$

**Dimension conditions.** $r=s$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2, A3

### B3 - Geometric-radius restarts of higher-order composite acceleration, followed by a local model when $r<s$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,r}(1+(M_{k,\nu}/\mu_r)^a(\mu_r/\varepsilon_f)^{a(r-s)/r}+\log(2+R(\mu_r/\varepsilon_f)^{1/r}))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $r>s,\ \varepsilon_f\le c\mu_rR^r$

**Dimension conditions.** $r>s,\ \varepsilon_f\le c\mu_rR^r$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2, A3

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A4, A5

### B5 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A4, A5

### B6 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A4, A5

### B7 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A4, A5

### B8 - Geometric-radius restarts of higher-order composite acceleration, followed by a local model when $r<s$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,r}(1+Q_r^{a}+\log(1+\log(1+E_r/\varepsilon_f)))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $r<s$

**Dimension conditions.** $r<s$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2, A3

### B9 - Geometric-radius restarts of higher-order composite acceleration, followed by a local model when $r<s$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,r}([1+(M_{k,\nu}/\mu_r)^a]\log(2+M_{k,\nu}R^s/\varepsilon_f))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $r=s$

**Dimension conditions.** $r=s$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2, A3

### B10 - Geometric-radius restarts of higher-order composite acceleration, followed by a local model when $r<s$

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O_{k,\nu,r}(1+(M_{k,\nu}/\mu_r)^a(\mu_r/\varepsilon_f)^{a(r-s)/r}+\log(2+R(\mu_r/\varepsilon_f)^{1/r}))
$$

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

**Conditions.** $r>s,\ \varepsilon_f\le c\mu_rR^r$

**Dimension conditions.** $r>s,\ \varepsilon_f\le c\mu_rR^r$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2, A3

### B11 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A4, A5

### B12 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $R=0$

**Dimension conditions.** $R=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A4, A5

### B13 - Recover a polynomial from one complete derivative reply

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A4, A5

### B14 - Two admissible instances indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_{k,\nu}=0,\ R>0$

**Dimension conditions.** $M_{k,\nu}=0,\ R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A4, A5

## 5. Local arguments

### A1 - Public convex constraints and composite terms

**Scope.** Applies only where the auxiliary operations are explicitly permitted. Does not merge distinct oracle interfaces or impose a lower bound on a publicly known singleton feasible domain.

**Algorithm scope.** Applies only where the auxiliary operations are explicitly permitted. Does not merge distinct oracle interfaces or impose a lower bound on a publicly known singleton feasible domain.

The convex high-order proximal analysis transfers to a public proper closed convex term when the declared auxiliary interface solves known composite models globally.

For $F=f+\psi$, solve the known model
$$T_k(f;x,y)+\psi(y)+CM\|y-x\|^s.$$
At a global model minimizer y, model optimality supplies a compatible $v_\psi\in\partial\psi(y)$. Then $v=\nabla f(y)+v_\psi$ is a subgradient of F, and the residual relative to the model's regularization gradient is exactly the Taylor-gradient error of f. The subgradient support inequality and Bregman three-point identity used in the convex accelerated framework therefore remain valid. Mirror subproblems also stay in the effective domain of $\psi$, and queries are convex combinations of known feasible points, preserving ball-restricted access.

This transfer requires global solution of the known high-order composite model and mirror subproblems, including a compatible subgradient or normal-cone selection. An ordinary projection, ordinary proximal map, or linear-minimization oracle alone does not automatically supply that capability. Unknown objective values or gradients requested at candidate points cost additional complete jets; at most a constant number per iteration preserves the stated order. The primary theorem's phrase 'one highest-order call per iteration' does not make other unknown-function information free.

For lower bounds on the family of permitted public regularizers, choose the subclass $\psi=0$ and use the convex resisting chain. This is a family-level inclusion argument, not a lower bound for every individually fixed special regularizer or feasible set.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://arxiv.org/pdf/2411.08987v2)

### A2 - A dimension-controlled convex high-order resisting chain

**Scope.** Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

**Algorithm scope.** Arbitrary deterministic complete-jet algorithms, including unqueried outputs. No randomized lower bound follows from the resisting-rotation argument. Constants depend only on fixed derivative order and Hölder exponent.

For fixed $s=k+\nu>2$, the construction gives deterministic lower bounds for objective accuracy and gradient norm, including arbitrary unqueried outputs.

For $N\ge2$, define
$$h_N(z)=\frac1s\left(\sum_{i=1}^{N-1}|z_i-z_{i+1}|^s+|z_N|^s\right)-z_1.$$
Let $A$ be the forward-difference matrix with a terminal row. Its Euclidean operator norm is at most two. The first $k$ derivatives of $|u|^s/s$ vanish at zero, and its kth derivative has a $\nu$-Hölder modulus depending only on $k,\nu$. Applying Hölder's inequality with exponents $s/\nu,s,\ldots,s$ gives
$$|[D^kh_N(z)-D^kh_N(w)][u_1,\ldots,u_k]|
\le H_{k,\nu}\|z-w\|_2^\nu\prod_j\|u_j\|_2,$$
with $H_{k,\nu}$ independent of $N$.

The minimizer is $z^*=(N,N-1,\ldots,1)$, with
$$h_N(0)-h_N(z^*)=(s-1)N/s,\qquad
\|z^*\|^2=N(N+1)(2N+1)/6.$$
If $z_{t+1}=\cdots=z_N=0$, then the remaining chain gives
$$h_N(z)-h_N(z^*)\ge(s-1)(N-t)/s,\qquad
\|\nabla h_N(z)\|\ge1/\sqrt{t+1}.$$
For the gradient inequality, the first $t+1$ gradient coordinates sum to $-1$, and Cauchy–Schwarz applies.

For any deterministic adaptive algorithm making $T$ queries, select orthonormal chain directions successively, orthogonal to previous directions and the query displacements seen so far. Vanishing derivatives of unrevealed terms ensure that each complete jet exposes at most the next direction. After the output is determined, choose the remaining hidden directions orthogonal to that output too. The sufficient dimension $d\ge N+T+1$ leaves room for these choices. The final function
$$f(x)=\alpha h_N(V^\top(x-x_0)/b)$$
is one fixed admissible instance consistent with the entire transcript. This construction does not select a separate instance after seeing a randomized algorithm's private seed.

For a radius promise, take $b=R/\|z^*\|$ and $\alpha=M_{k,\nu}b^s/H_{k,\nu}$. Choosing $N=2T+2$ for objective gap or $N=T+2$ for gradient norm gives
$$\operatorname{gap}(T)\ge\frac{c_{k,\nu}M_{k,\nu}R^s}{(T+1)^{(3s-2)/2}},\qquad
\operatorname{grad}_R(T)\ge\frac{c_{k,\nu}M_{k,\nu}R^{s-1}}{(T+1)^{(3s-2)/2}}.$$
For an initial-gap promise, set $\alpha=\Delta s/((s-1)N)$ and $b=(\alpha H_{k,\nu}/M_{k,\nu})^{1/s}$. Then
$$\operatorname{grad}_\Delta(T)\ge\frac{c_{k,\nu}M_{k,\nu}^{1/s}\Delta^{(s-1)/s}}{(T+1)^{(3s-2)/(2s)}}.$$
Inverting these inequalities yields the linked bounds with a sufficient dimension proportional to one plus the complexity scale. The minimizer lies in the localization ball, so the same hard subclass is admissible for ball-restricted optimization.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A3 - Uniformly convex composite objectives

**Scope.** Family of composite objectives with the stated global growth and known-model operations; constants depend on fixed orders. No minimax closure is inferred from these restart estimates.

**Algorithm scope.** Family of composite objectives with the stated global growth and known-model operations; constants depend on fixed orders. No minimax closure is inferred from these restart estimates.

Let $F(x)-F^*\ge(\mu_r/r)\|x-x^*\|^r$, while only the smooth component has order $s=k+\nu$ regularity. Restart costs have distinct forms for $r<s$, $r=s$, and $r>s$.

Use the composite base bound at radius t and target gap $\mu_rt^r/C$. Each radius-halving stage costs
$$C[1+(Mt^{s-r}/\mu_r)^a],\qquad a=2/(3s-2).$$
If $r<s$, the geometric sum is dominated by its first stage. With $E_r=(\mu_r^s/M^r)^{1/(s-r)}$, a local majorizing-model step gives $e_+\le CM(re/\mu_r)^{s/r}$, whose exponent is greater than one. The total upper bound is
$$C\left[1+(MR^{s-r}/\mu_r)^a+\log\left(1+\log(1+E_r/\varepsilon_f)\right)\right].$$
If $r=s$, stages have equal order and their number is logarithmic, giving
$$C[1+(M/\mu_r)^a]\log(2+MR^s/\varepsilon_f).$$
If $r>s$, stop at radius of order $(\varepsilon_f/\mu_r)^{1/r}$. The final stage dominates the regularity-dependent sum, while the unit cost per stage contributes a separate logarithm:
$$C\left[1+(M/\mu_r)^a(\mu_r/\varepsilon_f)^{a(r-s)/r}+\log\left(2+R(\mu_r/\varepsilon_f)^{1/r}\right)\right],$$
within the linked window $\varepsilon_f\le c\mu_rR^r$.

These are upper bounds. They do not prove joint-parameter lower bounds for all $(R,M,\mu_r)$. For $r>s$, the public composite term carries the faster growth; one must retain the decomposition F=f+$\psi$ instead of assuming a globally order-s smooth F with incompatible faster uniform growth.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A4 - One-query lower bound with a shared uniformly convex regularizer

**Scope.** Uniformly convex composite family with $R>0$ and positive accuracy. Retain the smooth-plus-public-term decomposition; a globally quadratic objective would not be r-uniformly convex for r>2.

**Algorithm scope.** Uniformly convex composite family with $R>0$ and positive accuracy. Retain the smooth-plus-public-term decomposition; a globally quadratic objective would not be r-uniformly convex for r>2.

A public uniformly convex term can preserve nontrivial one-query complexity even when the unknown smooth term has zero highest-order modulus.

Fix $r\ge2$ and $\mu_r>0$. Define $\varphi_r(x)=\|x\|^r/r$, $\kappa_r=8^{r-1}\mu_r/r$, and the shared public regularizer $\psi=\kappa_r\varphi_r$. For $h=y-x$ and $a=\langle x,h\rangle/\|h\|^2$, the Hessian integral remainder gives
$$D_{\varphi_r}(y,x)\ge\|h\|^r\int_0^1(1-t)|a+t|^{r-2}\,dt.$$
Within $[0,1/2]$, the set where $|a+t|\ge1/8$ has measure at least 1/4. The integral is therefore at least $8^{1-r}$, and $D_\psi(y,x)\ge(\mu_r/r)\|y-x\|^r$.

Set $x_0=0$, $a=R/2>0$, choose $A>2\varepsilon_f/a^2$, and put $L=Aa+\kappa_ra^{r-1}$. Let the unknown smooth terms be $f_\pm(x)=A\|x\|^2/2\mp Lx_1$. They are convex quadratics with zero highest-order modulus. The two full objectives share exactly the same public $\psi$ and budgets, have minimizers at $\pm a e_1$, and remain r-uniformly convex. Since they are also A-strongly convex, their $\varepsilon_f$-success sets lie in disjoint balls of radius $\sqrt{2\varepsilon_f/A}<a$. Zero-query randomization cannot achieve 2/3 success on both.

One complete jet recovers f, after which the declared free solution of the known composite model gives an upper bound of one. For the ordinary composite family, use shared $\psi$=0 and two translated quadratics. These are family-level lower bounds; a particular known singleton domain may be solvable without queries.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A5 - Zero-query and polynomial-recovery endpoints

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

[1] Juan Pablo Contreras; Cristóbal Guzmán; David Martínez-Rubio. Non-Euclidean High-Order Smooth Convex Optimization. arXiv:2411.08987v2 (2025-02-06); COLT 2025 extended abstract.

https://arxiv.org/pdf/2411.08987v2
