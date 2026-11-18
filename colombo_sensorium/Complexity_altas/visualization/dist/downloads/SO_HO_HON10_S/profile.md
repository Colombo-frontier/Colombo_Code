# Objective-gap minimization under a PL condition with full higher-order derivatives

**Setting ID.** `SO_HO_HON10_S`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; growth: Global polyak lojasiewicz; smoothness: Kth derivative lipschitz

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet k; operation: Exact jet k; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is $C^k$ and bounded below; nonconvexity is allowed.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_k\|x-y\|_{2}.$$

Fix $k\ge2$; no additional lower-order regularity bound is imposed.

$$f(x)-f^*\le\frac{\|\nabla f(x)\|_2^2}{2\mu},\qquad\mu>0,\qquad x\in\mathbb{R}^d.$$

Admissible parameter domain:

$$d\ge1,\quad k\ge2;\quad\text{all other parameters satisfy their tabulated ranges}.$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $\Delta$, $M_k$, $\mu$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

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

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge2}$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta\ge0$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k\ge0$.

$\mu$: Known positive lower bound on the PL constant **Domain:** $\mu>0$.

$\varepsilon_f$: Global objective-gap tolerance **Domain:** $\varepsilon_f>0$.

$E_*$: Natural objective-gap scale for local superlinear convergence under PL and higher-order regularity **Domain:** $E_*\ge0$.

$$E_*=((\mu)^{\frac{k+1}{k-(1)}})\,((M_k)^{\frac{-2}{k-(1)}}).$$

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

**Region.** $\varepsilon_f\ge \Delta$

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Optimal

**Lower bound.** B4, B8

$$
0
$$

**Upper bound.** B2, B6

$$
0
$$

### R2 - Parameter window 2

**Region.** $M_k,\mu,\Delta>0,0<\varepsilon_f<\Delta$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_k(1+(\Delta/E_*)^{(k-1)/(2k)}+\log(1+\log(1+E_*/\varepsilon_f)))
$$

### R3 - Parameter window 3

**Region.** $M_k=0,0<\varepsilon_f<\Delta$

**Views.** Deterministic

**Quantity.** Q1

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
1
$$

### R4 - Parameter window 1

**Region.** $M_k,\mu,\Delta>0,0<\varepsilon_f<\Delta$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5

$$
O_k(1+(\Delta/E_*)^{(k-1)/(2k)}+\log(1+\log(1+E_*/\varepsilon_f)))
$$

### R5 - Parameter window 3

**Region.** $M_k=0,0<\varepsilon_f<\Delta$

**Views.** Randomized

**Quantity.** Q2

**Resource.** One complete jet costs one call, under a fixed cap on every execution path. Exact real feedback, arbitrary precision and arbitrarily small positive query displacements are permitted. Internal computation, tensor algebra and global minimization of known regularized Taylor models are free. HVP counts and arithmetic complexity are not the resource being measured.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B7

$$
1
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{k}f(x)=(f(x),Df(x),\ldots,D^{k}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Higher-order regularized Taylor iteration under a PL condition

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C_k[1+(\Delta/E_*)^{(k-1)/(2k)}+\log(1+\log(1+E_*/\varepsilon_f))]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $M_k,\mu,\Delta>0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_k,\mu,\Delta>0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1, A2, A3

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) theorem: Lemmas2.1–2.3 and Theorem2.5; pdf pages: 7

### B2 - Return the public initial point

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

**Local argument.** A1

### B3 - Free search for an epsilon_f-optimal point once all polynomial coefficients are known

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_k=0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_k=0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Deterministic-error guarantee for every instance

**Local argument.** A1

### B4 - Nonnegativity of oracle cost

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

**Local argument.** A1

### B5 - Higher-order regularized Taylor iteration under a PL condition

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C_k[1+(\Delta/E_*)^{(k-1)/(2k)}+\log(1+\log(1+E_*/\varepsilon_f))]
$$

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

**Conditions.** $M_k,\mu,\Delta>0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_k,\mu,\Delta>0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1, A2, A3

**Source location.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf) theorem: Lemmas2.1–2.3 and Theorem2.5; pdf pages: 7

### B6 - Return the public initial point

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

**Local argument.** A1

### B7 - Free search for an epsilon_f-optimal point once all polynomial coefficients are known

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Conditions.** $M_k=0,0<\varepsilon_f<\Delta$

**Dimension conditions.** $M_k=0,0<\varepsilon_f<\Delta$

**Guarantee conversion.** Success probability at least 2/3 for every instance

**Local argument.** A1

### B8 - Nonnegativity of oracle cost

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

### A2 - Global objective accuracy under a PL condition

**Scope.** Full-space PL objectives, complete jets, positive highest-order modulus, and the linked accuracy window. Treat constant-function and zero-gap degeneracies separately.

**Algorithm scope.** Full-space PL objectives, complete jets, positive highest-order modulus, and the linked accuracy window. Treat constant-function and zero-gap degeneracies separately.

High-order descent and a global PL inequality yield an explicit upper bound with a polynomial global phase and double-logarithmic local phase.

Assume $f(x)-f_*\le\|\nabla f(x)\|^2/(2\mu)$ and let $e_t=f(x_t)-f^*$. High-order regularized descent implies
$$e_t-e_{t+1}\ge c_kM_k^{-1/k}\mu^{(k+1)/(2k)}e_{t+1}^{(k+1)/(2k)}.$$
Put $a=(k+1)/(2k)\in(0,1)$, $E_* =\mu^{(k+1)/(k-1)}M_k^{-2/(k-1)}$, and $z=e/E_*$. Then $z_t-z_{t+1}\ge c_kz_{t+1}^a$.

Above a fixed constant, a step either halves z or reduces the potential $z^{1-a}$ by a fixed k-dependent amount. Thus the global phase takes $O_k(1+(\Delta/E_*)^{1-a})$ steps. In a sufficiently small fixed local region, $z_{t+1}\le C_kz_t^{1/a}$, whose exponent exceeds one. The local phase costs $O_k(1+\log(1+\log(1+E_*/\varepsilon_f)))$. Together,
$$O_k\left[1+(\Delta/E_*)^{(k-1)/(2k)}+\log(1+\log(1+E_*/\varepsilon_f))\right].$$
The execution budget depends only on public parameters; knowing $f^*$ is unnecessary. This is a safe upper bound rather than a claim of sharp constants at every near-trivial endpoint.

If an explicit $\beta$-smoothness assumption is also present, gradient descent and PL give the alternative $O(1+(\beta/\mu)\log(\Delta/\varepsilon_f))$ bound on its nontrivial gap window. Choose between complete applicable algorithms using public budgets. The extra $\beta$ assumption is a specification distinction, not an implicit condition inserted into a regime. No joint-parameter minimax lower bound follows from this argument.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

### A3 - High-order regularized descent with full parameter dependence

**Scope.** Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

**Algorithm scope.** Fixed derivative order, complete exact jets, full-space queries, bounded initial gap, and free global known-model solution. Zero modulus is treated by polynomial recovery.

With a Lipschitz kth derivative and fixed $k\ge2$, first-order stationarity uses $O_k(1+\Delta M_k^{1/k}\varepsilon_g^{-(k+1)/k})$ complete jets.

At x, form $m_x(s)=T_k(f;x,s)+a_kM_k\|s\|^{k+1}$, choosing $a_k$ sufficiently large, depending only on k, to dominate the Taylor remainder with slack. For $M_k>0$ the model is coercive, so it has a global minimizer, available under the declared free internal computation. Comparing the model at s and zero and applying the value remainder gives
$$f(x)-f(x+s)\ge c_kM_k\|s\|^{k+1}.$$
Model first-order optimality and the gradient remainder give
$$\|\nabla f(x+s)\|\le C_kM_k\|s\|^k.$$
If the next point is not $\varepsilon_g$-stationary, the decrease is at least $c_kM_k^{-1/k}\varepsilon_g^{(k+1)/k}$. The total decrease is at most $\Delta$, so after the displayed number of calls, including initialization and final verification, stationarity is reached.

This is the parameter restoration of the regularized-model argument in BGMST17, Lemmas 2.1–2.3 and Theorem 2.5. Its normalization is $(k-1)!L=M_k$. Separate function and derivative evaluations in the source cost only a fixed multiple when complete jets are charged as one. The argument is about information calls and does not assert an inexpensive arithmetic implementation of global nonconvex model minimization.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [1](https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf)

## References

[1] E. G. Birgin; J. L. Gardenghi; J. M. Martínez; S. A. Santos; Ph. L. Toint. Worst-case evaluation complexity for unconstrained nonlinear optimization using high-order regularized models. NAXYS-05-2015, 2015-07-10; Mathematical Programming 163 (2017), 359–368.

https://optimization-online.org/wp-content/uploads/2015/06/4970.pdf
