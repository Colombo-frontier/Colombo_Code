# Smooth finite-sum composite strongly convex optimization with exact component values and a known proximal mapping

**Setting ID.** `SO_ZO_E09d`

Single-objective optimization

Minimize $H$ globally over $\operatorname{dom}\psi$ and return a point with small objective gap.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Composite strong convexity; convexity: Known convex prox; convexity: Strongly convex composite with convex components; smoothness: Component gradient lipschitz; structure: Finite sum

**ORACLE tags.** access order: Zeroth-order interface; interface family: Selected component value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $H$ globally over $\operatorname{dom}\psi$ and return a point with small objective gap.

### Admissible model

$F(x)=n^{-1}\sum_{i=1}^n f_i(x)$, with $n\in\mathbb{N}$. Each component $f_i:\mathbb{R}^d\to\mathbb{R}$ is globally convex.

Every component satisfies $\|\nabla f_i(x)-\nabla f_i(y)\|_2\le\beta\|x-y\|_2$. Component affine terms and gradients at the optimum are unrestricted, and components need not attain minima.

$\psi:\mathbb{R}^d\to(-\infty,+\infty]$ is a known proper closed convex function, and the full composite objective $H=F+\psi$ is $\mu$-strongly convex. A minimizer $x_*$ exists. The given $x_0\in\operatorname{dom}\psi$ satisfies $\|x_0-x_*\|_2\le R$ and $H(x_0)-\inf H\le\Delta_\Phi$. Distance and objective gap are separate bounds.

### Oracle interface

The algorithm may actively choose $i\in\{1,\ldots,n\}$ and $x\in\mathbb{R}^d$. The interface $(i,x)\mapsto f_i(x)$ returns one exact component value. Components may be revisited; full-average values must be computed through component calls.

The complete definition of $\psi$ is known. For every $\eta>0$, the exact proximal mapping $\operatorname{prox}_{\eta\psi}$ is available at no charge.

The public inputs are $d$, $n$, $\beta$, $\mu$, $R$, $x_0$, $\varepsilon$, $\Delta_\Phi$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \operatorname{dom}\psi$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=H(x)-H_*$, where $H_*=\inf_{u\in \operatorname{dom}\psi}H(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One $(i,x)\mapsto f_i(x)$ costs $1$ component-value calls; recomputing the full average costs $n$ calls. Every initialization, snapshot and differencing point is charged individually.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

#### Deterministic

Only deterministic strategies are allowed. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The requirement $\ell(I,\widehat{x})\le \varepsilon$ holds deterministically for each instance.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

#### Randomized

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over the algorithm's random seed only.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

**Output qualification.** Random selection among previously queried points is permitted, subject to the declared success guarantee.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$n$: Number of finite-sum components **Domain:** $n\in\mathbb{N},\ n\ge1$.

$F=n^{-1}\sum_{i=1}^n f_i$

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$R$: Upper bound on the distance from the public initial point to a minimizer **Domain:** $R>0$.

$\|x_*-x_0\|_2\le R$

$x_0$: Known initial point **Domain:** $x_0\in\mathbb{R}^d$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa>0$; the strong-convexity modulus of the full composite objective may exceed the smoothness bound on its smooth part.

$\kappa=\beta/\mu$

$\Delta_\Phi$: Initial-gap upper bound for the composite objective **Domain:** $\Delta_\Phi\ge0$.

$H(x_0)-\inf H\le\Delta_\Phi$

$R_{\mathrm{eff}}$: Effective initial radius from distance and strongly convex composite objective-gap bounds **Domain:** $R_{\mathrm{eff}}\ge0$.

$R_{\mathrm{eff}}=\min\{R,\sqrt{2\Delta_\Phi/\mu}\}$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $\operatorname{dom}\psi$.

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

$f_i,i$: Finite-sum components and their indices **Domain:** $f_i:\mathbb{R}^d\to\mathbb{R},\ i\in\{1,\ldots,n\}$.

Components are unknown; indices may be selected actively and revisited at a cost.

$F$: Finite-sum mean objective **Domain:** $F:\mathbb{R}^d\to\mathbb{R}$.

$F=n^{-1}\sum_{i=1}^n f_i$

$H,H_*$: Composite objective and its finite optimal value **Domain:** The objective is extended-real-valued on $\mathbb{R}^d$, and its optimal value belongs to $\mathbb{R}$.

$H=F+\psi$, $H_*=\inf_{x\in\mathbb{R}^d}H(x)$.

$\operatorname{prox}_{\eta\psi}$: Proximal mapping of the known convex regularizer **Domain:** $\eta>0,\ v\in\mathbb{R}^d$.

$\operatorname{prox}_{\eta\psi}(v)=\operatorname{argmin}_u\{\psi(u)+\|u-v\|_2^2/(2\eta)\}$

$\eta$: Step size for the auxiliary proximal operation **Domain:** $\eta>0$.

Public numerical value selectable by the algorithm.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\operatorname{dom}\psi$ and $\mathcal{X}=\operatorname{dom}\psi$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact selected component scalar value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E09d.R1

**Region.** $0<\mu\le\beta$, $0<\varepsilon\le\mu R_{\mathrm{eff}}^2/512$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact selected component scalar value

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega(nd)
$$

**Upper bound.** B1

$$
O(nd(1+\sqrt\kappa)[1+\log_+(\mu R_{\rm eff}^2/\varepsilon)])
$$

**Gap or comparison.** $O((1+\sqrt{\kappa})(1+\log_+(\mu R_{\mathrm{eff}}^2/\varepsilon)))$

### R2 - Parameter regime E09d.R3

**Region.** $\varepsilon\ge\Delta_\Phi$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact selected component scalar value

**Status.** Optimal

**Lower bound.** B4, B8

$$
0
$$

**Upper bound.** B3, B7

$$
0
$$

### R3 - Parameter regime E09d.R1

**Region.** $0<\mu\le\beta$, $0<\varepsilon\le\mu R_{\mathrm{eff}}^2/512$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact selected component scalar value

**Status.** Other quantified gap

**Lower bound.** B6

$$
\Omega(nd)
$$

**Upper bound.** B5

$$
O(nd(1+\sqrt\kappa)[1+\log_+(\mu R_{\rm eff}^2/\varepsilon)])
$$

**Gap or comparison.** $O((1+\sqrt{\kappa})(1+\log_+(\mu R_{\mathrm{eff}}^2/\varepsilon)))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each source component value corresponds to one selectable component query; computing the exact mean requires accessing every component.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Variance-reduced proximal methods or proximal acceleration with complete averaging

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(nd(1+\sqrt\kappa)[1+\log_+(\mu R_{\rm eff}^2/\varepsilon)])
$$

**Sources.** [2](https://papers.neurips.cc/paper_files/paper/2011/file/8f7d807e1f53eff5f9efbe5cb81090fb-Paper.pdf) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa=\beta/\mu>0$; each phase uses $m=\max\{1,\lceil5\sqrt\kappa\rceil\}$ and a positive differencing radius $h_j=R_j/[2\sqrt d\,m(m+1)]$. The argument remains valid when only the full objective H is strongly convex.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

**Source location.** [2](https://papers.neurips.cc/paper_files/paper/2011/file/8f7d807e1f53eff5f9efbe5cb81090fb-Paper.pdf) theorem: Proposition 2, equation (6), PDF page 4; update (3), PDF page 2

### B2 - Zero-regularizer subclass and finite-sum component measurements

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(nd)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\mu\le\beta,\quad0<\varepsilon\le\mu R_{\rm eff}^2/512$. Take the hard subclass with zero regularizer and common $Hessian \mu I$. The independent initial-gap bound must be retained.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Proposition A; the $\psi=0$ subclass

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta_\Phi$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

### B4 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta_\Phi$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

### B5 - Variance-reduced proximal methods or proximal acceleration with complete averaging

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(nd(1+\sqrt\kappa)[1+\log_+(\mu R_{\rm eff}^2/\varepsilon)])
$$

**Sources.** [2](https://papers.neurips.cc/paper_files/paper/2011/file/8f7d807e1f53eff5f9efbe5cb81090fb-Paper.pdf) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\kappa=\beta/\mu>0$; each phase uses $m=\max\{1,\lceil5\sqrt\kappa\rceil\}$ and a positive differencing radius $h_j=R_j/[2\sqrt d\,m(m+1)]$. The argument remains valid when only the full objective H is strongly convex.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

**Source location.** [2](https://papers.neurips.cc/paper_files/paper/2011/file/8f7d807e1f53eff5f9efbe5cb81090fb-Paper.pdf) theorem: Proposition 2, equation (6), PDF page 4; update (3), PDF page 2

### B6 - Zero-regularizer subclass and finite-sum component measurements

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(nd)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $\mu\le\beta,\quad0<\varepsilon\le\mu R_{\rm eff}^2/512$. Take the hard subclass with zero regularizer and common $Hessian \mu I$. The independent initial-gap bound must be retained.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Proposition A; the $\psi=0$ subclass

### B7 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta_\Phi$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

### B8 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\Delta_\Phi$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

## 5. Local arguments

### A1 - An adaptive $nd$ lower bound for selected-component values

**Scope.** Fixed scalar-call cap; arbitrary measurable adaptive randomized queries, including unbounded query points; only the explicitly stated average or component localization promises.

For smooth finite sums, $T>nd/2$ is necessary at $\varepsilon\le\mu R^2/512$. For globally Lipschitz components the same conclusion holds at
$$\varepsilon\le\frac{LRd}{512n[d+\log(16n)]}.$$
The displayed constants give success probability $2/3$; an expected-error transfer uses the same statement at $3\varepsilon$.

Take independent $a_i\sim N(0,s^2I_d)$. A component query, after subtracting a known common term, reveals one linear measurement of $a_i$. Conditional on the random seed and the transcript, the components remain independent Gaussian vectors with covariance $s^2P_i$, where $P_i$ projects onto the complement of the span queried in that component. Hence the mean $\bar a$ has covariance $\Sigma=(s^2/n^2)\sum_iP_i$ and
$$\operatorname{tr}\Sigma\ge s^2(nd-T)/n^2,\qquad\Sigma\preceq(s^2/n)I.$$
For any Gaussian vector $Z$, any proposed center $b$, and $t>0$, Gaussian integration gives $\mathbb E e^{-t\|Z-b\|^2}\le(1+2t\operatorname{tr}\Sigma)^{-1/2}$. Taking $t=1/(2r^2)$ yields
$$\Pr(\|Z-b\|^2\le r^2)\le\sqrt{\frac{er^2}{r^2+\operatorname{tr}\Sigma}}.$$
In particular, $r^2\le\operatorname{tr}\Sigma/8$ makes this at most $\sqrt e/3$.

For the smooth family set $f_i(x)=\mu\|x\|^2/2-\mu\langle a_i,x\rangle$ and $s^2=nR^2/(16d)$. The mean is minimized at $\bar a$. The event $E=\{\|\bar a\|\le R\}$ has probability at least $15/16$. For $T\le nd/2$, $\operatorname{tr}\Sigma\ge R^2/32$. Objective accuracy $\varepsilon$ means squared center error at most $2\varepsilon/\mu$, which is at most $\operatorname{tr}\Sigma/8$ on the displayed window. The unconditional success probability is at most $\sqrt e/3$; conditioning on $E$ only after this calculation bounds valid-instance success by $16\sqrt e/45<2/3$. Choose $\mu=\beta$ for the merely convex smooth class, or the declared $\mu\le\beta$ for the strongly convex class. Individual component centers are not bounded in this construction.

For globally Lipschitz components define the radial Huber function
$$h_R(x)=\begin{cases}\|x\|^2/2,&\|x\|\le R,\\R\|x\|-R^2/2,&\|x\|>R,\end{cases}\quad q=L/(2R),\quad f_i=q(h_R-\langle a_i,x\rangle).$$
Choose $s^2=R^2/[8(d+\log(16n))]$. A Gaussian tail bound and union bound give $\Pr(\max_i\|a_i\|\le R)\ge15/16$. On this event each component is globally convex and $L$-Lipschitz. Inside the feasible ball the mean gap is $q\|x-\bar a\|^2/2$. The same posterior argument gives $\operatorname{tr}\Sigma\ge R^2d/[16n(d+\log(16n))]$, proving the stated window. Every unbounded query still reveals just one linear measurement because the common Huber term is known. Inside the ball this family has curvature $qI$, so it also proves the average-strongly-convex finite-sum lower for every public $\mu\le L/(2R)$.

These are joint $nd$ arguments. Separate $\Omega(n)$ and $\Omega(d)$ statements would justify only a maximum, not their product.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A2 - Explicit logarithmic lower bounds and class restrictions

**Scope.** The source theorem retains its unrestricted query/output domain, fixed query cap, and stated accuracy window.

For the smooth class, $Q\ge128^2$ gives $\Omega(d\log Q)$. This also holds in a public strongly convex class with $\kappa\ge2$. For a ball-restricted Lipschitz class, $A=LR/\varepsilon\ge6\cdot128^2$ gives $\Omega(d\log A)$.

Dorn et al., Theorem 2.5, gives
$$\frac{3d}{4000}\left[1+\frac{\log(\beta_hR_h^2/\varepsilon)}{\log((\beta_h+\mu_h)/(\beta_h-\mu_h))}\right]$$
when $\mu_h/\beta_h\in[1/2,1]$ and $\beta_hR_h^2/\varepsilon\ge128^2$. Choose $\mu_h=\beta_h/2$, so the denominator is $\log3$. A convex $\beta$-smooth class contains this subclass with $\beta_h=\beta$, $R_h=R$. A public lower curvature budget $\mu\le\beta/2$ also contains it, uniformly in the public condition number.

For the ball-restricted Lipschitz class choose $R_h=R/2$, $\beta_h=2L/(3R)$, and $\mu_h=\beta_h/2$. On $B_2(R)$, $\|\nabla f(x)\|\le\beta_h(\|x\|+\|x_*\|)\le L$, and the global minimizer remains inside the feasible ball. One source value simulates one restricted value. The stronger source oracle permits all such algorithms, and $Q_h=A/6$. The explicit window makes $\log(A/6)$ and $\log A$ uniformly comparable.

For a selected-component finite sum with all components equal to the same hard function, one component query is one source query. This transfer has cost one, not $n$. A logarithmic and a dimension-dependent lower bound may be maximized only where both respective windows hold.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

### A3 - A deterministic finite-difference restart for a strongly convex composite

**Scope.** Each component is globally convex and $\beta$-smooth; a public proper closed convex regularizer has a free exact prox; only the full composite objective must be $\mu$-strongly convex. A public initial radius $R_0$ is required.

For $H=n^{-1}\sum_i f_i+\psi$, the scalar-component cost is
$$O\!\left(nd(1+\sqrt{\beta/\mu})[1+\log_+(\mu R_0^2/\varepsilon)]\right).$$
This includes $\beta/\mu<1$.

Put $m=\max\{1,\lceil5\sqrt{\beta/\mu}\rceil\}$ and $R_j=2^{-j}R_0$. At phase $j$ reset accelerated proximal gradient and use forward differences with
$$h_j=\frac{R_j}{2\sqrt d\,m(m+1)}.$$
One approximate average gradient uses $n(d+1)$ scalar values and has norm error at most $\beta h_j\sqrt d/2=\beta R_j/[4m(m+1)]$. The inexact proximal-gradient proposition of Schmidt, Le Roux, and Bach, with exact prox and momentum $(k-1)/(k+2)$, gives after $m$ steps
$$H(x_m)-H_*\le\frac{2\beta}{(m+1)^2}\left(R_j+\frac2\beta\sum_{k=1}^m k\|e_k\|\right)^2\le\frac{25\beta R_j^2}{8(m+1)^2}\le\frac{\mu R_j^2}{8}.$$
Strong convexity then gives $\|x_m-x_*\|\le R_j/2$, justifying the next restart. After
$$K=1+\max\{0,\lceil\log_4(\mu R_0^2/(8\varepsilon))\rceil\}$$
phases, the gap is at most $\varepsilon$. The exact count is at most $n(d+1)mK$. If $R_0=0$, the initial point is already optimal. A public gap $\Delta_H$ supplies $R_0=\sqrt{2\Delta_H/\mu}$; if both a radius and a gap are supplied, use their minimum. An unspecified initial potential cannot replace this certificate.

The argument requires neither strong convexity of each component nor a known allocation of strong convexity between the smooth part and the regularizer. In the single-objective composite case take $n=1$. Lower bounds from $\psi=0$ apply only to a class that includes that regularizer; they do not automatically apply to an arbitrarily fixed nonzero regularizer. For the joint $nd$ lower use the common-quadratic family with $R_{\rm eff}=\min\{R,\sqrt{2\Delta_H/\mu}\}$ and its explicit small-error window.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://papers.neurips.cc/paper_files/paper/2011/file/8f7d807e1f53eff5f9efbe5cb81090fb-Paper.pdf) [1](https://arxiv.org/html/2610.00345v1)

### A4 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Mark Schmidt, Nicolas Le Roux and Francis Bach. Convergence Rates of Inexact Proximal-Gradient Methods for Convex Optimization. NIPS 2011.

https://papers.neurips.cc/paper_files/paper/2011/file/8f7d807e1f53eff5f9efbe5cb81090fb-Paper.pdf
