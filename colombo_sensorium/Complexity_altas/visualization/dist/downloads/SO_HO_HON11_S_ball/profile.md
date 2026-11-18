# Global minimization of general nonconvex functions on a compact ball with complete higher-order derivatives

**Setting ID.** `SO_HO_HON11_S_ball`

Single-objective optimization

Solve $\min_{x\in Q}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Other quantified gap present; Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Euclidean ball; geometry: Full space; geometry: Known compact optimization domain; smoothness: Holder smooth; smoothness: Kth derivative holder

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet k; operation: Exact jet k; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in Q}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The feasible set is the known closed ball $Q=\{x:\|x-x_0\|_2\le R\}$. The function $f$ is $C^k$ on an open convex neighborhood of the ball and may be nonconvex.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_{k,\nu}\|x-y\|_{2}^{\nu}.$$

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in Q}f(x)\le\Delta$.

Admissible parameter domain:

$$R>0$$

### Oracle interface

Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

A description of the feasible set, feasibility tests and global minimization of known models formed from existing replies are supplied as public auxiliary operations.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $M_{k,\nu}$, $\nu$, $R$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in Q$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in Q}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

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

$$f(\widehat{x})-f^*\le \varepsilon_f.$$

The running-cost guarantee is specified separately under RESOURCE.

#### Randomized

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\Pr\!\left[f(\widehat{x})-f^*\le \varepsilon_f\right]\ge\frac23.$$

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

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in Q}f(x).$$

$Q$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge2}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$M_{k,\nu}$: Global $\nu$-Hölder upper bound for the order-$k$ derivative in the specified tensor norm. **Domain:** $M_{k,\nu}\ge0$.

$\nu$: Hölder exponent of the highest derivative **Domain:** $0<\nu\le1$.

$R$: Radius of the known ball. **Domain:** $R>0$.

$\varepsilon_f$: Global objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$C_{k,\nu}$: A sufficiently large positive constant depending only on the fixed order $k$ and Hölder exponent $\nu$. **Domain:** $C_{k,\nu}>0$.

$s$: Sum of the highest derivative order and its Hölder exponent. **Domain:** $s\ge0$.

$$s=k+\nu.$$

$X$: Ratio of ball radius to resolution scale **Domain:** $X\ge0$.

$$X=R\,((\frac{M_{k,\nu}}{\varepsilon_f})^{\frac{1}{k+\nu}}).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter window 1

**Region.** $0<\varepsilon_f\le \Delta/2;R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}\ge C_{k,\nu}$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Other quantified gap

**Lower bound.** B2

$$
\frac23\left\lfloor[c_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d\right\rfloor-1
$$

**Upper bound.** B1

$$
[1+C_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/s}]^d
$$

**Gap or comparison.** $C_{k,\nu}^{d}$

### R2 - Parameter window 2

**Region.** $\varepsilon_f\ge \Delta$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B5, B11

$$
0
$$

**Upper bound.** B3, B9

$$
0
$$

### R3 - Parameter window 3

**Region.** $\varepsilon_f>0,M_{k,\nu}>0,R>0$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
[1+C_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d
$$

### R4 - Parameter window 4

**Region.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B6, B12

$$
1
$$

**Upper bound.** B4, B10

$$
1
$$

**Gap or comparison.** $1$

### R5 - Parameter window 1

**Region.** $0<\varepsilon_f\le \Delta/2;R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}\ge C_{k,\nu}$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Other quantified gap

**Lower bound.** B8

$$
\frac23\left\lfloor[c_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d\right\rfloor-1
$$

**Upper bound.** B7

$$
[1+C_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/s}]^d
$$

**Gap or comparison.** $C_{k,\nu}^{d}$

### R6 - Parameter window 3

**Region.** $\varepsilon_f>0,M_{k,\nu}>0,R>0$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B7

$$
[1+C_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $Q$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in Q$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Finite grid within the ball and global solution of local Taylor polynomials

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
[1+C_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d
$$

**Conditions.** $\varepsilon_f>0,M_{k,\nu}>0,R>0$

**Dimension conditions.** $\varepsilon_f>0,M_{k,\nu}>0,R>0$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

### B2 - Separated compactly supported smooth radial wells within a ball

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\frac23\left\lfloor[c_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d\right\rfloor-1
$$

**Conditions.** $0<\varepsilon_f\le \Delta/2;R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}\ge C_{k,\nu}$

**Dimension conditions.** $0<\varepsilon_f\le \Delta/2;R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}\ge C_{k,\nu}$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge \Delta$

**Dimension conditions.** $\varepsilon_f\ge \Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B4 - Full polynomial reconstruction and free global optimization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B5 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_f\ge \Delta$

**Dimension conditions.** $\varepsilon_f\ge \Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B6 - Zero-query indistinguishability of translated quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A3

### B7 - Finite grid within the ball and global solution of local Taylor polynomials

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
[1+C_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d
$$

**Conditions.** $\varepsilon_f>0,M_{k,\nu}>0,R>0$

**Dimension conditions.** $\varepsilon_f>0,M_{k,\nu}>0,R>0$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

### B8 - Separated compactly supported smooth radial wells within a ball

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\frac23\left\lfloor[c_{k,\nu}R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}]^d\right\rfloor-1
$$

**Conditions.** $0<\varepsilon_f\le \Delta/2;R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}\ge C_{k,\nu}$

**Dimension conditions.** $0<\varepsilon_f\le \Delta/2;R(M_{k,\nu}/\varepsilon_f)^{1/(k+\nu)}\ge C_{k,\nu}$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2

### B9 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge \Delta$

**Dimension conditions.** $\varepsilon_f\ge \Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B10 - Full polynomial reconstruction and free global optimization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B11 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_f\ge \Delta$

**Dimension conditions.** $\varepsilon_f\ge \Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

### B12 - Zero-query indistinguishability of translated quadratics

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
1
$$

**Conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_{k,\nu}=0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A3

## 5. Local arguments

### A1 - Global optimization on a known ball: Taylor covering and hidden wells

**Scope.** Queries and outputs restricted to the public ball, including boundary optima. This is distinct from unrestricted queries with a merely localized global minimizer.

**Algorithm scope.** Queries and outputs restricted to the public ball, including boundary optima. This is distinct from unrestricted queries with a merely localized global minimizer.

On a known ball, upper and lower bounds have accuracy exponent $d/(k+\nu)$ at fixed dimension, with explicit dimension-dependent covering and packing constants.

Let $Q=B_2(x_0,R)$, $s=k+\nu$, and require every query and output to lie in Q. Taylor error is at most $C_{k,\nu}M\|u\|^s$. Choose h of order $(\varepsilon_f/M)^{1/s}$ so the error within distance h is at most $\varepsilon_f/2$. An h-net of Q has at most
$$[1+C_{k,\nu}R(M/\varepsilon_f)^{1/s}]^d$$
nodes. Query one complete jet per node and minimize its known Taylor model on Q intersected with the radius-h ball. Return the candidate with smallest model value. The cell containing a true constrained minimizer supplies model value at most $f^*+\varepsilon_f/2$; the selected candidate's true value is at most another $\varepsilon_f/2$ above its model value. No final unknown-function evaluation is required.

For the lower bound, in the linked small-accuracy region $\varepsilon_f\le\Delta/2$, use smooth wells of depth $2\varepsilon_f$, with a slightly larger constant if strict separation is needed, and width $h=C_{k,\nu}(\varepsilon_f/M)^{1/s}$. Pack at least $(cR/h)^d$ disjoint supports in Q and remove at most one containing $x_0$. A radial bump $\psi(\|x-c\|^2/h^2)$ has derivative operator bounds with constants depending only on fixed order, because the number of inner-product contractions depends only on that order. Hölder continuity follows by interpolation between bounded and Lipschitz derivatives.

With one uniformly hidden well, the all-zero-transcript counting argument gives
$$T\ge\frac23\left\lfloor[c_{k,\nu}R(M/\varepsilon_f)^{1/s}]^d\right\rfloor-1,$$
after absorbing finitely many removed supports into a smaller c. This argument covers randomized adaptive queries and unqueried outputs.

At fixed d the accuracy powers match. When d varies, differing base constants yield exponential-in-d factors; hiding those constants as $O_d$ or $\Omega_d$ does not establish dimension-uniform constant-factor closure. Retain the explicit powers and a quantified-gap status.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A2 - Global optimization without localization has no finite uniform budget

**Scope.** Unlocalized full-space global objective accuracy. Requires positive bump regularity budget; zero modulus instead permits polynomial recovery. No claim that each fixed instance needs infinitely many queries.

**Algorithm scope.** Unlocalized full-space global objective accuracy. Requires positive bump regularity budget; zero modulus instead permits polynomial recovery. No claim that each fixed instance needs infinitely many queries.

With $0<\varepsilon_f<\Delta$ and positive high-order regularity budget, no finite number of complete-jet queries guarantees global objective accuracy without a localization promise.

Choose well depth $D=(\varepsilon_f+\Delta)/2$, so $\varepsilon_f<D\le\Delta$. Scale a compactly supported smooth bump to width $h\asymp_{k,\nu}(D/M_{k,\nu})^{1/(k+\nu)}$, giving the required regularity. Place N disjoint candidate supports arbitrarily far apart, none containing $x_0$. Each of N instances contains exactly one negative well. Outside its support every complete jet is zero; the initial gap is D and the global minimum is -D.

Fix a private random seed and examine the common all-zero transcript. T adaptive queries can meet at most T supports, and the final possibly unqueried output can meet at most one more. With a uniformly hidden well, success probability is at most $(T+1)/N$. Integrating over the private seed preserves this inequality. To achieve success at least 2/3 on every instance would require $T+1\ge2N/3$. Since N is arbitrary, no finite uniform budget exists.

Arbitrarily distant queries and unqueried outputs are explicitly included. This is a mathematical information impossibility, not a missing upper bound. When $\varepsilon_f\ge\Delta$, returning $x_0$ instead gives the separate zero-query endpoint.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A3 - Zero-query and polynomial-recovery endpoints

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
