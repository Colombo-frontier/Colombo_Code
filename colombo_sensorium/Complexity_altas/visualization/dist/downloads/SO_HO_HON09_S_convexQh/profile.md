# Strong Taylor stationarity for nonconvex composite objectives with structured derivatives: convex feasible domain and convex outer function

**Setting ID.** `SO_HO_HON09_S_convexQh`

Single-objective optimization

Find a strong approximate Taylor stationary point at every order: return a feasible point and positive radii such that, for each $1\le j\le m$, the Taylor decrease satisfies its independent tolerance $\varepsilon_j$.

**Status.** Bounds missing

**TASK tags.** task family: Single objective

**MODEL tags.** convexity: Known convex outer h; convexity: Convexity not assumed; geometry: Full space; geometry: Known convex feasible set; smoothness: Lipschitz function; smoothness: Simultaneous component derivative lipschitz; structure: Inexpensive known constraints; structure: Known subadditive h with h0 zero; structure: Strong composite taylor stationarity; structure: Structured composite

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact structured composite jet; operation: Exact structured composite jet; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point with orderwise positive radii; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a strong approximate Taylor stationary point at every order: return a feasible point and positive radii such that, for each $1\le j\le m$, the Taylor decrease satisfies its independent tolerance $\varepsilon_j$.

### Admissible model

The objective is $w=f+h\circ c$, where $f:\mathbb{R}^d\to\mathbb{R}$ and $c:\mathbb{R}^d\to\mathbb{R}^r$ are $C^k$ maps. For every $1\le j\le k$, their $D^jf,D^jc$ derivatives are respectively $M_{f,j},M_{c,j}$-Lipschitz on the relevant open convex neighborhood.

The outer function $h:\mathbb{R}^r\to\mathbb{R}$ satisfies $h(0)=0$, $h(a+b)\le h(a)+h(b)$ and $|h(a)-h(b)|\le L_h\|a-b\|_2$. The feasible set $Q$ is known, nonempty and closed, with $x_0\in Q$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $w(x_0)-\inf_{x\in Q}w(x)\le\Delta$.

Both $Q$ and $h$ are additionally convex; the full objective $w$ may remain nonconvex.

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

A query at any $x\in Q$ returns $f(x),c(x)$ and the complete exact derivatives of both functions through order $1,\ldots,k$. Exact evaluation of the outer function $h$, geometric operations on the public domain, and global solution of known composite Taylor models are free.

A description of the feasible set, feasibility tests and global minimization of known models formed from existing replies are supplied as public auxiliary operations.

The public inputs are $x_0$, the target accuracy, and $d$, $r$, $k$, $m$, $\Delta$, $(M_{f,j})_{j=1}^k$, $(M_{c,j})_{j=1}^k$, $L_h$, $(\varepsilon_j)_{j=1}^m$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $(\widehat{x},\rho_1,\ldots,\rho_m)$ with $\widehat{x}\in Q$ and each $\rho_j\in(0,1]$; all derivative orders must satisfy their error requirements simultaneously.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=\max_{1\le j\le m}\frac{j!\,\phi_{w,j}^{\rho_j}(\widehat{x})}{\varepsilon_j\rho_j^j}.$$

$$T_{f,j}(x,u)=\sum_{a=0}^{j}\frac1{a!}D^af(x)[u^a].$$

$$T_{c,j}(x,u)=\sum_{a=0}^{j}\frac1{a!}D^ac(x)[u^a],\qquad T_{w,j}(x,u)=T_{f,j}(x,u)+h(T_{c,j}(x,u)).$$

$$\phi_{w,j}^{\rho_j}(x)=w(x)-\min_{x+u\in Q,\ \|u\|_2\le\rho_j}T_{w,j}(x,u).$$

Fix $1\le m\le k$. The order-specific tolerances $\varepsilon_j>0$ are independent. Output radii must be strictly positive, and each minimum is attained on a nonempty compact set.

### Resource accounting

One complete $(f,c)$ structured derivative tuple costs one unit.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

#### Deterministic

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\max_{1\le j\le m}\frac{j!\,\phi_{w,j}^{\rho_j}(\widehat{x})}{\varepsilon_j\rho_j^j}\le 1.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[\max_{1\le j\le m}\frac{j!\,\phi_{w,j}^{\rho_j}(\widehat{x})}{\varepsilon_j\rho_j^j}\le 1\right]\ge\frac23.$$

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

$f,c,h,w$: Unknown smooth scalar function, unknown smooth vector-valued map, public outer function, and full objective.

$$w(x)=f(x)+h(c(x)).$$

$Q$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$w^*$: Global infimum of the full objective over the feasible domain.

$$w^*=\inf_{x\in Q}w(x).$$

$T_{f,j}(x,u)$: The Taylor polynomial of order $j$ centered at $x$ with step $u$; the exact expression is given in the metric definition.

$D^jf(x)[u^j]$: The order-$j$ derivative applied to $j$ copies of the same step direction.

$$D^jf(x)[u^j]=D^jf(x)[u,\ldots,u].$$

$\phi_{w,j}^{\rho}(x)$: Maximum feasible Taylor-model decrease within radius $\rho$, defined by the minimization formula in the metric specification.

$\rho,\rho_j$: Positive radius returned by the algorithm. **Domain:** $0<\rho,\rho_j\le1$.

$T_{c,j},T_{w,j}$: Taylor polynomial of a vector map and the structured composite Taylor model. The latter is $T_{f,j}+h\circ T_{c,j}$ and does not require classical higher derivatives of $w$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$r$: Dimension of the range of the composite map c **Domain:** $r\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge2}$.

$m$: Order of Taylor stationarity **Domain:** $m\in\{1,\ldots,k\}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$(M_{f,j})_{j=1}^k$: Lipschitz bounds on the derivatives of f **Domain:** $(M_{f,j})_{j=1}^k\in\mathbb{R}_{>0}^k$.

$(M_{c,j})_{j=1}^k$: Lipschitz bounds on the derivatives of c **Domain:** $(M_{c,j})_{j=1}^k\in\mathbb{R}_{>0}^k$.

$L_h$: Known Lipschitz upper bound for h **Domain:** $L_h\ge0$.

$(\varepsilon_j)_{j=1}^m$: Strong Taylor-stationarity tolerances at the respective orders **Domain:** $(\varepsilon_j)_{j=1}^m\in(0,1]^m$.

$\theta$: Model parameters held fixed in the corresponding accuracy bound.

$$\theta=(r,k,m,\Delta,(M_{f,j})_{j=1}^k,(M_{c,j})_{j=1}^k,L_h).$$

$C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<C<\infty$.

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete structured jet of (f,c) costs one call, under a fixed worst-case cap. The known h, geometry, internal algebra and global minimization of known nonconvex models are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete structured jet of (f,c) costs one call, under a fixed worst-case cap. The known h, geometry, internal algebra and global minimization of known nonconvex models are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter window 1

**Region.** $m=1;0<\varepsilon_1\le 1$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete structured jet of (f,c) costs one call, under a fixed worst-case cap. The known h, geometry, internal algebra and global minimization of known nonconvex models are free.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

$$
O_\theta(1+\varepsilon_1^{-(k+1)/k})
$$

### R2 - Parameter window 2

**Region.** $1\le m\le k;0<\varepsilon_j\le 1;\theta=(k,m,\Delta,M_f,M_c,L_h,r,algorithm constants) fixed$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete structured jet of (f,c) costs one call, under a fixed worst-case cap. The known h, geometry, internal algebra and global minimization of known nonconvex models are free.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C_\theta[1+\max_{1\le j\le m}\varepsilon_j^{-(j+1)}]
$$

### R3 - Parameter window 1

**Region.** $m=1;0<\varepsilon_1\le 1$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete structured jet of (f,c) costs one call, under a fixed worst-case cap. The known h, geometry, internal algebra and global minimization of known nonconvex models are free.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B4

$$
O_\theta(1+\varepsilon_1^{-(k+1)/k})
$$

### R4 - Parameter window 2

**Region.** $1\le m\le k;0<\varepsilon_j\le 1;\theta=(k,m,\Delta,M_f,M_c,L_h,r,algorithm constants) fixed$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete structured jet of (f,c) costs one call, under a fixed worst-case cap. The known h, geometry, internal algebra and global minimization of known nonconvex models are free.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
C_\theta[1+\max_{1\le j\le m}\varepsilon_j^{-(j+1)}]
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** A query at any $x\in Q$ returns $f(x),c(x)$ and the complete exact derivatives of both functions through order $1,\ldots,k$. Exact evaluation of the outer function $h$, geometric operations on the public domain, and global solution of known composite Taylor models are free.

**Output mapping.** Return $(\widehat{x},\rho_1,\ldots,\rho_m)$ with $\widehat{x}\in Q$ and each $\rho_j\in(0,1]$; all derivative orders must satisfy their error requirements simultaneously.

**Resource mapping.** One complete $(f,c)$ structured derivative tuple costs one unit.

### B1 - Adaptive regularization for strong composite Taylor stationarity

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_\theta[1+\max_{1\le j\le m}\varepsilon_j^{-(j+1)}]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf)

**Conditions.** $1\le m\le k;0<\varepsilon_j\le 1;\theta=(k,m,\Delta,M_f,M_c,L_h,r,algorithm constants) fixed$

**Dimension conditions.** $1\le m\le k;0<\varepsilon_j\le 1;\theta=(k,m,\Delta,M_f,M_c,L_h,r,algorithm constants) fixed$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf) theorem: Theorem5.6(2), eqs(5.19)–(5.20); pdf pages: 22

### B2 - First-order composite model with a convex domain and convex outer function

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_\theta[1+\varepsilon_1^{-(k+1)/k}]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf)

**Conditions.** $m=1;0<\varepsilon_1\le 1$

**Dimension conditions.** $m=1;0<\varepsilon_1\le 1$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf) theorem: Theorem5.6(1), eqs(5.17)–(5.18); pdf pages: 21

### B3 - Adaptive regularization for strong composite Taylor stationarity

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_\theta[1+\max_{1\le j\le m}\varepsilon_j^{-(j+1)}]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf)

**Conditions.** $1\le m\le k;0<\varepsilon_j\le 1;\theta=(k,m,\Delta,M_f,M_c,L_h,r,algorithm constants) fixed$

**Dimension conditions.** $1\le m\le k;0<\varepsilon_j\le 1;\theta=(k,m,\Delta,M_f,M_c,L_h,r,algorithm constants) fixed$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf) theorem: Theorem5.6(2), eqs(5.19)–(5.20); pdf pages: 22

### B4 - First-order composite model with a convex domain and convex outer function

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_\theta[1+\varepsilon_1^{-(k+1)/k}]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf)

**Conditions.** $m=1;0<\varepsilon_1\le 1$

**Dimension conditions.** $m=1;0<\varepsilon_1\le 1$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf) theorem: Theorem5.6(1), eqs(5.17)–(5.18); pdf pages: 21

## 5. Local arguments

### A1 - Independent strong Taylor tolerances and structured composite jets

**Scope.** Preserve all orderwise regularity assumptions and the structured composite interface. Do not transfer method-specific sharpness into unrestricted minimax comparisons.

**Algorithm scope.** Preserve all orderwise regularity assumptions and the structured composite interface. Do not transfer method-specific sharpness into unrestricted minimax comparisons.

The primary strong-Taylor theorems use independent orderwise tolerances and explicit algorithm-specific lower-bound scope.

For strong smooth Taylor stationarity, return radii $\rho_j\in(0,1]$ with $\phi_{f,j}^{\rho_j}(x)\le\varepsilon_j\rho_j^j/j!$ for every $j=1,\ldots,m$. Under the source's orderwise Lipschitz assumptions, CGTstrong, Theorem 5.5(1), gives complexity $O_\theta(\max_j\varepsilon_j^{-(k+1)/(k-j+1)})$ on a convex domain when $m\le2$, with all radii equal to one. The general branch, Theorem 5.5(2), equations (5.15)–(5.16), is $O_\theta(\max_j\varepsilon_j^{-j(k+1)/k})$. Its order-j step lower bound in Lemma 5.4 is $c\varepsilon_j^{j/k}$, confirming the individual exponents. The looser abstract-level worst-order exponent should not replace them.

For $w=f+h\circ c$, the interface returns structured jets of f and c. The public h is Lipschitz, subadditive, and zero at zero. Its model is $T_{f,j}+h(T_{c,j})$, not a classical Taylor jet of a potentially nonsmooth w. On a convex domain with convex h and $m=1$, Theorem 5.6(1) gives $O_{\theta}(\varepsilon_1^{-(k+1)/k})$. The general branch in Theorem 5.6(2), equations (5.19)–(5.20), gives $O_\theta(\max_j\varepsilon_j^{-(j+1)})$. Only equal tolerances reduce this to $\varepsilon^{-(m+1)}$.

The sharpness results in Theorems 6.1 and 6.4 concern the paper's adaptive regularization algorithm and its step rules. They are not lower bounds for every adaptive or randomized oracle algorithm. These direct theorem correspondences replace any need for an internal historical proof reference.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf)

## References

[1] Coralia Cartis; Nicholas I. M. Gould; Philippe L. Toint. Strong Evaluation Complexity Bounds for Arbitrary-Order Optimization of Nonconvex Nonsmooth Composite Functions. 2020-01-29 manuscript, associated arXiv:2001.10802v1.

https://optimization-online.org/wp-content/uploads/2020/01/7590.pdf
