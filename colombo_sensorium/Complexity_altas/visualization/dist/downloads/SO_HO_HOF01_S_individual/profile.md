# Finite-sum nonconvex first-order stationarity with complete component high-order derivatives: individual component regularity

**Setting ID.** `SO_HO_HOF01_S_individual`

Single-objective optimization

Find an approximate first-order stationary point of the full objective, namely $\|\nabla F(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

**Status.** Fully optimal

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Individual highest derivative lipschitz; structure: Finite sum

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Incremental full k jet; operation: Incremental full k jet; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate first-order stationary point of the full objective, namely $\|\nabla F(\widehat{x})\|_2\le\varepsilon_g$. The interaction interface and admissible outputs are specified under ORACLE and OUTPUT, respectively.

### Admissible model

The full objective is $F(x)=n^{-1}\sum_{i=1}^n f_i(x)$, each $f_i:\mathbb{R}^d\to\mathbb{R}$ is $C^k$, and $k\ge2$ is fixed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $F(x_0)-\inf_{x\in \mathbb{R}^d}F(x)\le\Delta$.

Every component satisfies $\|D^kf_i(x)-D^kf_i(y)\|_{\mathrm{op}}\le M_k\|x-y\|_2$.

Individual components and their average may be nonconvex. No additional bound is imposed on lower-derivative magnitudes or componentwise additive offsets.

### Oracle interface

Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{k}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

The public inputs are $x_0$, the target accuracy, and $d$, $n$, $k$, $M_k$, $\Delta$, $\varepsilon_g$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\|\nabla F(\widehat{x})\|_2.$$

The criterion uses the gradient norm itself. Squared norms, expectations, and probability guarantees are recorded separately and are not substituted automatically.

### Resource accounting

Each complete component response through order $k$ costs one unit. A complete population response requires $n$ component queries.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\|\nabla F(\widehat{x})\|_2\le \varepsilon_g\right]\ge\frac23.$$

Expectation or probability is evaluated after fixing the instance; component sampling is part of the algorithm's private randomness.

The running-cost guarantee is specified separately under RESOURCE.

#### Deterministic

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\|\nabla F(\widehat{x})\|_2\le \varepsilon_g.$$

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

$f_i,F,F^*$: Unknown component functions, mean objective, and population optimal value. **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^nf_i(x),\qquad F^*=\inf_{x\in\mathbb{R}^d}F(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$n$: Number of components **Domain:** $n\in\mathbb{N}_{\ge 1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge 2}$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k\ge0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$\varepsilon_g$: Gradient tolerance **Domain:** $\varepsilon_g>0$.

$A_k$: Dimensionless leading term of the high-dimensional first-order stationarity complexity. **Domain:** $A_k\ge0$.

$$A_k=\Delta\,(M_k)^{\frac{1}{k}}\,((\varepsilon_g)^{\frac{0-(k+1)}{k}}).$$

$C_k$: Sufficient dimension constant for the lower-bound construction; it depends only on the fixed parameters specified by that bound and is not numerically given. **Domain:** $C_k>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Dimension sufficient to contain the randomized hard instances

**Region.** $d\ge C_k(1+A_kn^{-1/(2k)})\log(2+n+A_kn^{1-1/(2k)})$

**Views.** Randomized

**Quantity.** Q1

**Resource.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Status.** Optimal

**Lower bound.** B2

$$
c_k[n+A_kn^{1-1/(2k)}]
$$

**Upper bound.** B1

$$
C_k[n+A_kn^{1-1/(2k)}]
$$

**Gap or comparison.** $O_k(1)$

### R2 - Zero highest-order Lipschitz constant

**Region.** $\Delta>0,\quad M_k=0$

**Views.** Randomized; Deterministic

**Quantity.** Q2; Q4

**Resource.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Status.** Optimal

**Lower bound.** B6, B12

$$
cn
$$

**Upper bound.** B5, B11

$$
n
$$

**Gap or comparison.** $O(1)$

### R3 - Zero initial gap

**Region.** $\Delta=0$

**Views.** Randomized; Deterministic

**Quantity.** Q2; Q4

**Resource.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Status.** Optimal

**Lower bound.** B4, B10

$$
0
$$

**Upper bound.** B3, B9

$$
0
$$

### R4 - Dimension required by the deterministic hard construction

**Region.** $d\ge C_k(1+nA_k)$

**Views.** Deterministic

**Quantity.** Q3

**Resource.** Each complete component k-jet costs one call. A full scan for F and all its derivatives costs n calls. Arbitrary internal exact computation, tensor operations, and model solution are free.

**Status.** Optimal

**Lower bound.** B8

$$
c_kn(1+A_k)
$$

**Upper bound.** B7

$$
C_kn(1+A_k)
$$

**Gap or comparison.** $O_k(1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{k}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete component response through order $k$ costs one unit. A complete population response requires $n$ component queries.

### B1 - Tensor estimation with staged variance reduction

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
C_k[n+A_kn^{1-1/(2k)}]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28202v2)

**Conditions.** $n\ge1,\ k\ge2\text{ fixed},\quad\Delta,M_k,\varepsilon_g>0$

**Dimension conditions.** $n\ge1,\ k\ge2\text{ fixed},\quad\Delta,M_k,\varepsilon_g>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2609.28202v2) theorem: Theorem 3.2; Appendix D; pdf pages: 5

### B2 - Random hidden chains and hidden components under complete higher-order information

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_k[n+A_kn^{1-1/(2k)}]
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28202v2)

**Conditions.** $d\ge C_k(1+A_kn^{-1/(2k)})\log(2+n+A_kn^{1-1/(2k)})$

**Dimension conditions.** $d\ge C_k(1+A_kn^{-1/(2k)})\log(2+n+A_kn^{1-1/(2k)})$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2609.28202v2) theorem: Theorems 3.2,3.4; Appendix E.1-E.2; pdf pages: 5

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

### B4 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

### B5 - Recover the global polynomial after one complete jet per component at a single point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
n
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28202v2)

**Conditions.** $\Delta>0,\quad M_k=0$

**Dimension conditions.** $\Delta>0,\quad M_k=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2609.28202v2) theorem: Discussion following Theorem 3.2; Appendix E.1; pdf pages: 5

### B6 - One hidden component contains the unknown linear term

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cn
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28202v2)

**Conditions.** $\Delta>0,\quad M_k=0$

**Dimension conditions.** $\Delta>0,\quad M_k=0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Source location.** [1](https://arxiv.org/pdf/2609.28202v2) theorem: Appendix E.1; pdf pages: 23

### B7 - Each complete population k-jet is implemented using n component queries

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_k n(1+A_k)
$$

**Sources.** [2](https://proceedings.mlr.press/v151/emmenegger22a/emmenegger22a.pdf)

**Conditions.** $n\ge1,\ k\ge2\text{ fixed},\quad\Delta,M_k,\varepsilon_g>0$

**Dimension conditions.** $n\ge1,\ k\ge2\text{ fixed},\quad\Delta,M_k,\varepsilon_g>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A2

### B8 - Deterministic finite-sum resisting oracle

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
c_k n(1+A_k)
$$

**Sources.** [2](https://proceedings.mlr.press/v151/emmenegger22a/emmenegger22a.pdf)

**Conditions.** $d\ge C_k(1+nA_k)$

**Dimension conditions.** $d\ge C_k(1+nA_k)$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [2](https://proceedings.mlr.press/v151/emmenegger22a/emmenegger22a.pdf) theorem: Theorem 3.5; combine FSM26 Appendix E.1 for n term; pdf pages: 6

### B9 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

### B10 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\Delta=0$

**Dimension conditions.** $\Delta=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

### B11 - Recover the global polynomial after one complete jet per component at a single point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
n
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28202v2)

**Conditions.** $\Delta>0,\quad M_k=0$

**Dimension conditions.** $\Delta>0,\quad M_k=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2609.28202v2) theorem: Discussion following Theorem 3.2; Appendix E.1; pdf pages: 5

### B12 - One hidden component contains the unknown linear term

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cn
$$

**Sources.** [1](https://arxiv.org/pdf/2609.28202v2)

**Conditions.** $\Delta>0,\quad M_k=0$

**Dimension conditions.** $\Delta>0,\quad M_k=0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Source location.** [1](https://arxiv.org/pdf/2609.28202v2) theorem: Appendix E.1; pdf pages: 23

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

### A2 - Deterministic finite-sum upper bound by complete scans

**Scope.** Deterministic complete component jets with individual regularity. Does not automatically apply to mean-square-only component regularity or certify a randomized lower bound.

**Algorithm scope.** Deterministic complete component jets with individual regularity. Does not automatically apply to mean-square-only component regularity or certify a randomized lower bound.

With individual component kth-derivative Lipschitz bound $M_k$, a deterministic full-scan method uses $O_k(n(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k}))$ component jets.

For $F=n^{-1}\sum_i f_i$, one population k-jet uses n complete component responses, and the population kth-derivative Lipschitz modulus is at most $M_k$. Globally minimize
$$m_x(s)=T_k(F;x,s)+\frac{2M_k}{(k+1)!}\|s\|^{k+1}.$$
The positive leading regularizer makes the model coercive. Comparing with $s=0$ and applying Taylor remainders gives
$$F(x)-F(x+s)\ge\frac{M_k}{(k+1)!}\|s\|^{k+1},\qquad
\|\nabla F(x+s)\|\le\frac{3M_k}{k!}\|s\|^k.$$
Every step whose successor fails the gradient target therefore decreases F by at least $c_kM_k^{-1/k}\varepsilon_g^{(k+1)/k}$. Total gap $\Delta$ bounds the number of population calls by $O_k(1+A_k)$, and multiplication by n gives the component count. Initial and final complete scans are included.

The lower comparison uses EKZ22, Theorem 3.5 for the deterministic $nA_k$ term and a separate hidden-component argument for n. Constants depend on fixed k, not on a varying derivative order. At $\Delta=0$ the zero-query endpoint takes priority over an n startup term.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://proceedings.mlr.press/v151/emmenegger22a/emmenegger22a.pdf)

## References

[1] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Upper and Lower Bounds for Higher-Order Nonconvex Finite-Sum Optimization. arXiv:2609.28202v2 (2026-10-19); latest history checked 2026-10-29.

https://arxiv.org/pdf/2609.28202v2

[2] Nicolas Emmenegger; Rasmus Kyng; Ahad N. Zehmakan. On the Oracle Complexity of Higher-Order Smooth Non-Convex Finite-Sum Optimization. AISTATS 2022, PMLR 151 proceedings PDF.

https://proceedings.mlr.press/v151/emmenegger22a/emmenegger22a.pdf
