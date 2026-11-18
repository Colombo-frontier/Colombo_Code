# Weakly convex composite objectives: Moreau stationarity of the original objective

**Setting ID.** `SO_ZO_C11_rand_expected`

Single-objective optimization

Find an approximate stationary point of the Moreau envelope of the composite objective $\Phi=f+\psi$, with envelope parameter fixed at $\lambda=1/(2\omega)$.

**Status.** Polynomial gap present

**TASK tags.** formulation: So moreau envelope stationarity; solution concept: Moreau envelope gradient; task family: Single objective

**MODEL tags.** convexity: Known convex regularizer; convexity: Weakly convex; initialization: Composite initial gap; stochastic model: Sample lipschitz second moment

**ORACLE tags.** access order: Zeroth-order interface; interface family: Reusable sample value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an approximate stationary point of the Moreau envelope of the composite objective $\Phi=f+\psi$, with envelope parameter fixed at $\lambda=1/(2\omega)$.

### Admissible model

$f(x)=\mathbb{E}[F(x;Z)]$. The sample value at a reference point is integrable. Sample functions satisfy $|F(x;Z)-F(y;Z)|\le G(Z)\|x-y\|_2$ and $\mathbb{E}[G(Z)^2]\le L^2$ throughout $\mathbb{R}^d$; samplewise convexity is not required.

$f$ is $\omega$-weakly convex: $x\mapsto f(x)+\frac\omega2\|x\|_2^2$ is convex, with $\omega>0$.

$\psi:\mathbb{R}^d\to(-\infty,+\infty]$ is a known proper closed convex function; $\Phi=f+\psi$ is bounded below. The given $x_0\in\operatorname{dom}\psi$ satisfies $\Phi(x_0)-\inf\Phi\le\Delta$.

### Oracle interface

A new sample handle corresponds to an independent draw of the hidden sample $Z$. Given its handle and $x\in \mathbb{R}^d$, the interface returns the exact sample value $F(x;Z)$. The algorithm observes only handles and numerical values, not the underlying sample data or the complete sample function.

Sample handles may be retained for arbitrarily many paid evaluations. Responses using the same handle come from the same function, and distinct handles are independent.

The complete definition of $\psi$ is known. For every $\eta>0$, the exact proximal mapping $\operatorname{prox}_{\eta\psi}$ is available at no charge.

The public inputs are $d$, $\omega$, $L$, $\Delta$, $\varepsilon$, $\psi$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

$\Phi_\lambda(x)=\inf_{u\in\mathbb{R}^d}\{\Phi(u)+\|u-x\|_2^2/(2\lambda)\}$, with $\lambda=1/(2\omega)$. Weak convexity makes the envelope differentiable, and $\nabla\Phi_\lambda(x)=\lambda^{-1}(x-\operatorname{prox}_{\lambda\Phi}(x))$.

The base loss is $\ell(I,x)=\|\nabla\Phi_\lambda(x)\|_2^2$ with tolerance $\varepsilon^2$. The quantity $\operatorname{prox}_{\lambda\Phi}$ defines only the performance metric and adds no Oracle interface.

### Resource accounting

One scalar sample-function value costs $1$ call; two points with the same sample handle or Markov state cost $2$ calls. Batches, initialization and repeated visits are charged per value. An empty handle supplies no free instance information.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon^2$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\omega$: Weak-convexity budget for the population objective **Domain:** $\omega>0$.

$f+\omega\|\cdot\|_2^2/2$ is convex.

$L$: Moment budget of the sample Lipschitz coefficient **Domain:** $L>0$.

$\mathbb{E}[G(Z)^2]\le L^2$

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_{x\in\mathbb{R}^d}\Phi(x)\le\Delta$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\lambda$: Moreau-envelope parameter **Domain:** $\lambda>0$.

$\lambda=1/(2\omega)$

$\psi$: Known proper closed convex regularizer **Domain:** $\psi:\mathbb{R}^d\to(-\infty,+\infty]$.

$\operatorname{dom}\psi=\{x:\psi(x)<+\infty\}\ne\varnothing$

$B$: Truncated hard-instance scale in the lower bound **Domain:** $B\ge0$.

$B=\min\{\omega\Delta,L^2\}$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $\mathbb{R}^d$.

$I$: Complete problem instance **Domain:** $I\in\mathcal{I}$.

Includes the unknown objective and its admissible feedback distribution or environment law. Public parameters are fixed before the quantifiers.

$\mathcal{I}$: Admissible instance class determined by the eight specification fields in this profile **Domain:** Instances satisfying the public parameter bounds.

$\mathcal{A}$: Algorithm or strategy **Domain:** Measurable adaptive strategies allowed in this profile.

The algorithm is selected before the hidden instance.

$\ell$: Base loss or residual **Domain:** $\ell:\mathcal{I}\times\mathcal{X}_{\mathrm{out}}\to[0,+\infty]$.

The exact formula appears in this profile's performance-criterion section.

$\mathbb{E},\Pr$: Expectation and probability **Domain:** Evaluated over the algorithmic and feedback randomness specified by this profile's guarantee.

Fix the instance first; aggregate cost and error separately.

$\inf,\sup$: Infimum and supremum **Domain:** Evaluated only over the variable sets explicitly specified in the formula.

In the risk definition, the infimum over algorithms precedes the supremum over instances or centers.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product **Domain:** $\|x\|_2=\sqrt{\langle x,x\rangle}$.

$\langle x,y\rangle=x^\top y$

$B_p(c,R)$: Closed norm ball **Domain:** $p\in[1,\infty],\ R\ge0$.

$B_p(c,R)=\{x:\|x-c\|_p\le R\}$; $B_2$ denotes the Euclidean ball.

$N,T$: Actual call count and declared budget **Domain:** $N,T\in\mathbb{N}_0$.

A fixed budget bounds every execution path; the Markov specification uses an expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching orders, and upper bounds with hidden logarithms **Domain:** Within the joint parameter window specified for each complexity regime.

Dependence of hidden constants on fixed parameters is stated separately for each bound. Tilde notation may hide logarithmic factors only in the declared variables.

$c,C,c_\alpha,C_\alpha$: Positive constant in a proof or asymptotic bound **Domain:** $0<c,C,c_\alpha,C_\alpha<\infty$.

Unsubscripted constants have the dependencies stated in the bound; constants subscripted by $\alpha$ may depend only on the fixed smoothness order.

$\log,\log_+,e$: Natural logarithm, truncated logarithm, and Euler's number **Domain:** $z>0$.

$\log_+(z)=\max\{0,\log z\}$; $e=\exp(1)$, and $\log_2$ denotes the base-two logarithm.

$f$: Population-function term in the composite objective **Domain:** $f:\mathbb{R}^d\to\mathbb{R}$.

The full composite objective is $\Phi=f+\psi$. Existence and finite-lower-bound assumptions apply only to the objects explicitly identified in the model.

$\Phi,\Phi_*$: Composite objective and its finite optimal value **Domain:** The objective is extended-real-valued on $\mathbb{R}^d$, and its optimal value belongs to $\mathbb{R}$.

$\Phi=f+\psi$, $\Phi_*=\inf_{x\in\mathbb{R}^d}\Phi(x)$.

$\operatorname{prox}_{\eta\psi}$: Proximal mapping of the known convex regularizer **Domain:** $\eta>0,\ v\in\mathbb{R}^d$.

$\operatorname{prox}_{\eta\psi}(v)=\operatorname{argmin}_u\{\psi(u)+\|u-v\|_2^2/(2\eta)\}$

$\eta$: Step size for the auxiliary proximal operation **Domain:** $\eta>0$.

Public numerical value selectable by the algorithm.

$\Phi_\lambda$: Moreau envelope of the composite objective **Domain:** $\Phi_\lambda:\mathbb{R}^d\to\mathbb{R}$.

$\Phi_\lambda(x)=\inf_u\{\Phi(u)+\|u-x\|_2^2/(2\lambda)\}$

$\operatorname{prox}_{\lambda\Phi}$: Unique proximal minimizer defining the envelope gradient **Domain:** $\lambda=1/(2\omega)$.

This is a mathematical object in the performance criterion, not a free oracle.

$Z,F(\cdot;Z)$: Hidden sample and its associated sample function **Domain:** Samples lie in an admissible probability space; each sample function is real-valued on the declared domain.

The population objective is the expectation under the sample distribution or stationary distribution.

$G(Z)$: Random sample Lipschitz coefficient **Domain:** $G(Z)\ge0$.

The model's difference inequality holds for each sample, with the moment budget fixed as specified here.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\operatorname{dom}\psi$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar sample-function value; two points using the same handle cost two calls

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime C11.R1

**Region.** $B=\min\{\omega\Delta,L^2\}$, $\varepsilon^2\le cB$, $d\ge C(B/\varepsilon^2)\log(2+BL^2/\varepsilon^4)$ and $\lambda=1/(2\omega)$. Also require $\omega\Delta\le L^2$.

**Quantity.** Q1

**Resource.** One scalar sample-function value; two points using the same handle cost two calls

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(d\omega L^2\Delta/\varepsilon^4)
$$

**Upper bound.** B1

$$
O(d\omega L^2\Delta/\varepsilon^4+\omega\Delta/\varepsilon^2)
$$

**Gap or comparison.** $O(1)$

### R2 - Parameter regime C11.R2

**Region.** $B=\min\{\omega\Delta,L^2\}$, $\varepsilon^2\le cB$, $d\ge C(B/\varepsilon^2)\log(2+BL^2/\varepsilon^4)$ and $\lambda=1/(2\omega)$. Also require $\omega\Delta> L^2$.

**Quantity.** Q1

**Resource.** One scalar sample-function value; two points using the same handle cost two calls

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(dL^4/\varepsilon^4)
$$

**Upper bound.** B1

$$
O(d\omega L^2\Delta/\varepsilon^4+\omega\Delta/\varepsilon^2)
$$

**Gap or comparison.** $O(\omega\Delta/L^2)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output may lie in $\mathbb{R}^d$ and need not also belong to $\operatorname{dom}\psi$; error is measured by the Moreau-envelope gradient of the original composite objective.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Smoothed stochastic subgradients and transfer of Moreau-envelope error

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(d\omega L^2\Delta/\varepsilon^4+\omega\Delta/\varepsilon^2\right)
$$

**Sources.** [1](https://arxiv.org/pdf/1802.02988) [2](https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf) [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [3](https://arxiv.org/html/2610.19652v1)

**Conditions.** Ball-averaging radius $h\le\min\{\varepsilon^2/(C\omega L),\Delta/(CL)\}$; two values per iteration.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/pdf/1802.02988) theorem: Theorem 2.5, PDF page 8; proof, pages 8–9

**Source location.** [2](https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf) theorem: DD18, Theorem 2.5; KS24, Lemma 7; the spherical-moment argument and Moreau-envelope conversion

### B2 - Smooth weakly convex hard subclass with zero regularizer

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(dL^2\min\{\omega\Delta,L^2\}/\varepsilon^4)
$$

**Sources.** [3](https://arxiv.org/html/2610.19652v1) [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/pdf/1802.02988)

**Conditions.** Retain the high-dimensional and small-accuracy restrictions of C02; $r=0$ and $\|\nabla f(x)\|\le\tfrac32\|\nabla f_{1/(2\omega)}(x)\|$.

**Local argument.** A2

**Source location.** [3](https://arxiv.org/html/2610.19652v1) theorem: Transfer to the $\beta =\omega$-smooth subclass in Theorem 10.1

**Source location.** [3](https://arxiv.org/html/2610.19652v1) theorem: Transfer to the $\beta =\omega$-smooth subclass in Theorem 10.1; pdf pages: 22; printed pages: 22

## 5. Local arguments

### A1 - Ball smoothing and the same-sample directional moment

**Scope.** A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

### A2 - A same-sample upper for the original Moreau envelope

**Scope.** Global mean weak convexity $\omega$, sample Lipschitz second moment at most $L^2$, public convex regularizer with a free prox, initial composite gap $\Delta$, and same-sample value pairs.

For $\lambda=1/(2\omega)$, the original-objective target $\mathbb E\|\nabla\Phi_\lambda(\widehat x)\|^2\le\varepsilon^2$ has upper
$$O(d\omega L^2\Delta/\varepsilon^4+\omega\Delta/\varepsilon^2).$$

Ball smoothing preserves $\omega$-weak convexity and satisfies $|f_h-f|\le hL$. The paired estimator has mean $\nabla f_h$ and second moment at most $2dL^2$, by the odd-difference Poincare argument, which does not require sample convexity. Apply Davis and Drusvyatskiy's proximal stochastic-subgradient theorem to $\Phi_h=f_h+\psi$, with its parameters $\rho=\omega$, $\widehat\rho=2\omega$, and a constant step $\eta\le1/(2\omega)$. The source bound gives
$$\mathbb E\|\nabla(\Phi_h)_\lambda(\widehat x)\|^2\le2\Delta_h/(\eta T)+8\omega dL^2\eta,\qquad\Delta_h\le\Delta+2hL.$$
Choose $h\le\min\{\varepsilon^2/(64\omega L),\Delta/(2L)\}$ and $\eta\le\min\{1/(2\omega),\varepsilon^2/(64\omega dL^2)\}$. A sufficiently large universal multiple of the displayed budget makes this term small enough.

To transfer back, if $\sup|\Phi_h-\Phi|\le a$, add the two strongly-convex prox-subproblem optimality inequalities to get
$$(\lambda^{-1}-\omega)\|\operatorname{prox}_{\lambda\Phi}(x)-\operatorname{prox}_{\lambda\Phi_h}(x)\|^2\le2a.$$
Hence $\|\nabla\Phi_\lambda-\nabla(\Phi_h)_\lambda\|^2\le8\omega a$. Set $a=hL$ and use $\|u+v\|^2\le2\|u\|^2+2\|v\|^2$. Each round costs two values.

For the lower, take the smooth subclass with $\beta=\omega$ and $\psi=0$. If $y=\operatorname{prox}_{\lambda f}(x)$, then $\nabla f(y)=\nabla f_\lambda(x)$ and $\|\nabla f(x)\|\le(1+\beta\lambda)\|\nabla f_\lambda(x)\|=3\|\nabla f_\lambda(x)\|/2$. The source gradient-stationarity lower therefore transfers with a constant-factor accuracy change and its original cap $\min\{\omega\Delta,L^2\}$ and dimension window. It does not give closure when $\omega\Delta$ exceeds that cap by an unbounded factor.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/pdf/1802.02988) [3](https://arxiv.org/html/2610.19652v1)

## References

[1] Damek Davis and Dmitriy Drusvyatskiy. Stochastic subgradient method converges at the rate O(k^{-1/4}) on weakly convex functions. arXiv:1802.02988, 2018.

https://arxiv.org/pdf/1802.02988

[2] Kornowski and Shamir. An Algorithm with Optimal Dimension-Dependence for Zero-Order Nonsmooth Nonconvex Stochastic Optimization. JMLR 25(122):1--14, 2024.

https://www.jmlr.org/papers/volume25/23-1159/23-1159.pdf

[3] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1

[4] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
