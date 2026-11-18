# Finite-sum strongly convex objective accuracy with complete component second derivatives: unrestricted randomized algorithms

**Setting ID.** `SO_HO_HOF03_S_unrestricted`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}F(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; structure: Finite sum

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Incremental full second order; operation: Incremental full second order; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}F(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The full objective is $F=n^{-1}\sum_{i=1}^n f_i$. Each component is $C^2$, and every $i,x$ satisfies $\mu I_d\preceq\nabla^2f_i(x)\preceq\beta I_d$ and $0<\mu\le\beta$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $F(x_0)-\inf_{x\in \mathbb{R}^d}F(x)\le\Delta$.

Admissible parameter domain:

$$d,n\ge1,\quad0<\mu\le\beta,\quad\Delta,\varepsilon_f>0$$

### Oracle interface

Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

The public inputs are $x_0$, the target accuracy, and $d$, $n$, $\beta$, $\mu$, $\Delta$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=F(\widehat{x})-F^*.$$

Here $F^*=\inf_{x\in \mathbb{R}^d}F(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each complete component response through order $2$ costs one unit. A complete population response requires $n$ component queries.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\mathbb{E}\!\left[F(\widehat{x})-F^*\right]\le \varepsilon_f.$$

Expectation or probability is evaluated after fixing the instance; component sampling is part of the algorithm's private randomness.

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

$J_{2}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x)).$$

$f_i,F,F^*$: Unknown component functions, mean objective, and population optimal value. **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^nf_i(x),\qquad F^*=\inf_{x\in\mathbb{R}^d}F(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$I_d$: The identity matrix in dimension $d$.

$A\preceq B$: Loewner order: the symmetric matrix $B-A$ is positive semidefinite.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$n$: Number of components **Domain:** $n\in\mathbb{N}_{\ge 1}$.

$\beta$: Component-gradient Lipschitz bound **Domain:** $\beta>0$.

$\mu$: Per-component strong-convexity lower bound **Domain:** $\mu>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$\varepsilon_f$: Absolute expected objective gap **Domain:** $\varepsilon_f>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial absolute accuracy

**Region.** $0<\varepsilon_f<\Delta/4$

**Quantity.** Q1

**Resource.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Status.** Other quantified gap

**Lower bound.** B2

$$
cn
$$

**Upper bound.** B1

$$
C(n+\sqrt{n\beta/\mu})\log(2+\Delta/\varepsilon_f)
$$

**Gap or comparison.** $O((1+\sqrt{\beta/(n\mu)})\log(2+\Delta/\varepsilon_f))$

### R2 - The known initial-gap bound is sufficient

**Region.** $\varepsilon_f\ge\Delta$

**Quantity.** Q1

**Resource.** One complete componentwise second-order reply costs one call; internal linear algebra is free. A first-order algorithm may discard the Hessian information.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Submit $(i,x)$, where $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$, and receive the complete exact component tuple $(f_i(x),Df_i(x),\ldots,D^{2}f_i(x))$. Components may be queried repeatedly. Permissions for selecting component indices are specified under ALGORITHMS.

**Guarantee mapping.** Expected-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete component response through order $2$ costs one unit. A complete population response requires $n$ component queries.

### B1 - Katyusha, without using Hessian feedback

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C(n+\sqrt{n\beta/\mu})\log(2+\Delta/\varepsilon_f)
$$

**Sources.** [1](https://jmlr.org/papers/volume18/16-410/16-410.pdf)

**Conditions.** $n\ge1,\quad0<\mu\le\beta,\quad\Delta,\varepsilon_f>0$

**Dimension conditions.** $n\ge1,\quad0<\mu\le\beta,\quad\Delta,\varepsilon_f>0$

**Source location.** [1](https://jmlr.org/papers/volume18/16-410/16-410.pdf) theorem: Theorem 2.1, strongly convex composite form; pdf pages: 9

### B2 - Every Hessian equals mu I, with the linear term hidden in one component

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cn
$$

**Sources.** [2](https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf)

**Conditions.** $0<\varepsilon_f<\Delta/4$

**Dimension conditions.** $0<\varepsilon_f<\Delta/4$

**Local argument.** A1, A2

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A3

### B4 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A3

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

### A2 - Known quadratic components: exact recovery and matching initialization

**Scope.** Known quadratic components, unrestricted internal matrix computation, and exact complete component Hessians. General nonlinear components remain a separate model.

**Algorithm scope.** Known quadratic components, unrestricted internal matrix computation, and exact complete component Hessians. General nonlinear components remain a separate model.

With unrestricted complete Hessian access and known quadratic structure, the nontrivial strongly convex finite-sum complexity is $\Theta(n)$ in the stated accuracy window.

Write $f_i(x)=x^TA_i x/2+b_i^Tx+c_i$, with $\mu I\preceq A_i\preceq\beta I$. Query each component at one public point $x_0$. Its complete Hessian and gradient reveal $A_i$ and $b_i=\nabla f_i(x_0)-A_ix_0$. Then
$$x^*=-\left(\sum_iA_i\right)^{-1}\sum_i b_i$$
is computed internally at no additional query cost. Constants $c_i$ are unnecessary. Total cost is n, independent of accuracy and condition number.

For the lower bound, take $A_i=\mu I$ and place the linear term $-n\mu aZx_1$ at one uniformly hidden component, with $a^2=2\Delta/\mu$. The mean initial gap is exactly $\Delta$. Before that index is found, Z remains uniform and the smallest conditional expected gap is $\Delta$. If $\varepsilon_f<\Delta/4$, a constant hit probability is necessary, requiring $\Omega(n)$ calls under either fixed or expected resource accounting by the hidden-index argument.

AS17's restricted algorithm classes are different: Theorem 2 uses oblivious indices and a restriction on allowable matrix block structure generated from recent Hessians; Theorem 3 permits adaptive indices but retains the matrix-operation restriction. Full storage and inversion of all n Hessians need not belong to those classes. The recovery upper bound therefore explains why their restrictions cannot be dropped; it does not contradict their lower bounds.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

**Sources.** [2](https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf)

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

## References

[1] Zeyuan Allen-Zhu. Katyusha: The First Direct Acceleration of Stochastic Gradient Methods. JMLR 18(221):1-51, 2018.

https://jmlr.org/papers/volume18/16-410/16-410.pdf

[2] Yossi Arjevani; Ohad Shamir. Oracle Complexity of Second-Order Methods for Finite-Sum Problems. ICML 2017, PMLR 70 proceedings PDF.

https://proceedings.mlr.press/v70/arjevani17a/arjevani17a.pdf
