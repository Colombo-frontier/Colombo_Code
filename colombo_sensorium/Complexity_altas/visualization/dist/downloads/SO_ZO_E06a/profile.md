# Euclidean smooth convex optimization with a narrow localization norm ball and exact values

**Setting ID.** `SO_ZO_E06a`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Other quantified gap present

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz gradient; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$1\le p\le2$. The function $f$ is globally convex.

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

A global minimizer $x_*\in B_p(0,R)$ exists; function smoothness is still measured in the Euclidean norm.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $\beta$, $R$, $p$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

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

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$R$: Radius of the non-Euclidean minimizer-localization ball **Domain:** $R>0$.

$x_*\in B_p(0,R)$

$p$: Norm exponent of the feasible or localization ball **Domain:** $1\le p\le2$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$t$: Exponent difference between a narrow norm ball and the Euclidean ball **Domain:** $0\le t\le1/2$.

$t=1/p-1/2$

$p^*$: Hölder conjugate of the domain's norm exponent **Domain:** $1\le p^*\le\infty$.

$1/p+1/p^*=1$, with $p^*=\infty$ when $p=1$.

$a_p$: Representative logarithmic factor from the known proximal geometry **Domain:** $a_p\ge1$.

$a_p=\min\{p^*,\log(ed)\}$

$Q$: Smoothness accuracy ratio **Domain:** $Q>0$.

$Q=\beta R^2/\varepsilon$

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

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in \mathbb{R}^d}f(x)$.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$m,k$: Hard-instance dimension and algorithmic truncation dimension **Domain:** $m,k\in\{1,\ldots,d\}$.

Each maximum or minimum is over its admissible integers satisfying the displayed accuracy window; these indices provide no additional instance information.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E06a.R2

**Region.** $Q\ge\max\{32d^{2t},d^{2+2t}\}$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(d^2)
$$

**Upper bound.** B1

$$
O(d^2\log(e+Q))
$$

**Gap or comparison.** $O(\log(e+Q))$

### R2 - Parameter regime E06a.R5

**Region.** $1\le p<2,\ 32d^{2t}\le Q\le d^{2+2t}$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega(d^{1-t}\sqrt Q)
$$

**Upper bound.** B1

$$
O(\min\{d\sqrt Q,d^2\log(e+Q)\})
$$

**Gap or comparison.** $O(\min\{d^t,d^{1+t}\log(e+Q)/\sqrt Q\})$

### R3 - Parameter regime E06a.R6

**Region.** $Q\le2$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B4, B10

$$
0
$$

**Upper bound.** B3, B9

$$
0
$$

### R4 - Parameter regime E06a.R1

**Region.** $d\ge8,\ 32d^{2t}\le Q\le d^{2+2t}$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega(d^{1-t}\sqrt Q)
$$

**Upper bound.** B5

$$
O(a_p d^{1-t}\sqrt Q)
$$

**Gap or comparison.** $O(a_p)\le O(\log(ed))$

### R5 - Parameter regime E06a.R2

**Region.** $Q\ge\max\{32d^{2t},d^{2+2t}\}$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega(d^2)
$$

**Upper bound.** B7

$$
O(d^2\log(e+Q))
$$

**Gap or comparison.** $O(\log(e+Q))$

### R6 - Parameter regime E06a.R3

**Region.** Fix $1\le p<2$ in advance; $d\ge8$ and $32\le Q<32d^{2t}$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega_p(\min\{d,Q^{1/(2t)}\})
$$

**Upper bound.** B5, B6

$$
O_p(\log(ed)\min\{d,Q^{1/(2t)}\})
$$

**Gap or comparison.** $O_p(\log(ed))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Euclidean finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+\min\{d\sqrt Q,d^2\log(e+Q)\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [4](https://arxiv.org/html/2607.16558v2) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** A feasible deterministic upper bound, also available to randomized algorithms; a global minimizer is known to lie in the localization region.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; Appendix N.4; pdf pages: 29; printed pages: 29

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; Appendix N.4

### B2 - Euclidean linear-image hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{1\le m\le d:\ Qm^{-2t}\ge32}\Omega\!\left(m\min\{m,\sqrt Q\,m^{-t}\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Check the window separately for each $m$ before taking the maximum; $r_m\ge Rm^{-t}$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I; pdf pages: 5; printed pages: 5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I; pdf pages: 9; printed pages: 9

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B4 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B5 - Non-Euclidean random-direction acceleration or Euclidean localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(1+\min\{a_p d^{1-t}\sqrt Q,\ a_p^2d^{1-2t}Q,\ d^2\log(e+Q)\}\right)
$$

**Sources.** [3](https://arxiv.org/abs/1802.09022) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Randomized; $d\ge8$. Constants in $a_p$ are uniform over $p,d$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [3](https://arxiv.org/abs/1802.09022) theorem: GDG22 Theorems 2.2 / 2.9; D26 Appendix N.4; pdf pages: 7

**Source location.** [3](https://arxiv.org/abs/1802.09022) theorem: GDG22 Theorems 2.2 / 2.9; D26 Appendix N.4; pdf pages: 15

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: GDG22 Theorems 2.2 / 2.9; D26 Appendix N.4

### B6 - Randomized two-point estimator with coordinate truncation

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(1+\log(ed)\,Q k^{2/p^*})
$$

**Sources.** [2](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Choose the integer $k\in[1,d]$ as $k=d$ or $Qk^{-2t}\le1/12$, and take the minimum over the corresponding admissible $k$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

**Source location.** [2](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) theorem: Theorem 1 and its dual-averaging proof; Lemmas 1 and 4

**Source location.** [2](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) theorem: Theorem 1 and its dual-averaging proof; Lemmas 1 and 4

### B7 - Euclidean finite-difference acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+\min\{d\sqrt Q,d^2\log(e+Q)\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [4](https://arxiv.org/html/2607.16558v2) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** A feasible deterministic upper bound, also available to randomized algorithms; a global minimizer is known to lie in the localization region.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; Appendix N.4; pdf pages: 29; printed pages: 29

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Appendix C.2; Appendix N.4

### B8 - Euclidean linear-image hard family

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{1\le m\le d:\ Qm^{-2t}\ge32}\Omega\!\left(m\min\{m,\sqrt Q\,m^{-t}\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Check the window separately for each $m$ before taking the maximum; $r_m\ge Rm^{-t}$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I; pdf pages: 5; printed pages: 5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorem 3.1; Corollary 6.1; Appendix I; pdf pages: 9; printed pages: 9

### B9 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

### B10 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $Q\le2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

## 5. Local arguments

### A1 - Norm conversion, penalized localization, and affine equivalence

**Scope.** Globally defined objectives, the declared regularity norm, a public feasible or localization body, and the stated free geometric operations.

Let $a_B=\max_{\|u\|_2=1}\|u\|_B$ and let $R_2(K)$ be a public Euclidean enclosing radius. Then $\beta_2=a_B^2\beta$, $L_2=a_BL$, and $D_2=a_BR_2(K)$ give the deterministic smooth envelope
$$O\!\left(1+\min\{d\sqrt{\beta D_2^2/\varepsilon},d^2\log(e+\beta D_2^2/\varepsilon)\}\right)$$
and Lipschitz localization $O(1+d^2\log(d+1)\log(e+LD_2/\varepsilon))$.

The norm inequality $\|v\|_B\le a_B\|v\|_2$ and its dual give the stated Euclidean smoothness and Lipschitz constants. Apply the exact-value Euclidean acceleration or smooth localization theorem with those constants and the public radius; each transformed value remains one scalar call. The global-minimizer promise is retained for the smooth localization argument.

For a Lipschitz objective minimized over a known convex set $K$, define $g(x)=f(x)+L_2\operatorname{dist}_2(x,K)$. This is convex and $2L_2$-Lipschitz, $\min g=\min_K f$ on a ball containing $K$, and $f(\Pi_Kx)\le g(x)$. One value of $g$ uses one value of $f$ plus public geometry. The Euclidean ball localization theorem therefore returns a legal point of $K$ after projection. This is a concrete transfer to a general body, not a presumed general-body localization theorem.

If $B=UB_2(1)$ and $K=c+RB$ for a public invertible matrix $U$, set $g(y)=f(c+Uy)$. Then $\|Uv\|_B=\|v\|_2$ and $\|U^\top w\|_2=\|w\|_{B,*}$. Thus both the Lipschitz and smoothness budgets are unchanged, the feasible or localization body becomes $B_2(R)$, and one value plus the inverse output map preserves the exact gap, budget, and guarantee. No condition-number factor appears. Deterministic acceleration/localization and randomized two-point methods keep their original algorithm permissions.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [4](https://arxiv.org/html/2607.16558v2) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

### A2 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

### A3 - Using a sparse comparator in a narrow norm ball

**Scope.** Euclidean regularity on a public $B_p(R)$ with $1\le p<2$; global minimizer localization for the smooth branch; randomized two-point values.

Let $t=1/p-1/2$ and $p^*=p/(p-1)$. For an integer $k\le d$, the smooth upper is $O(1+\log(ed)Qk^{2/p^*})$ when $k=d$ or $\beta R^2k^{-2t}\le\varepsilon/12$. The Lipschitz upper is $O(1+\log(ed)A^2k^{2/p^*})$ when $k=d$ or $LRk^{-t}\le\varepsilon/6$.

Retain the largest $k$ coordinates of a minimizer to form $v_k$. Then $\|v_k\|_1\le Rk^{1/p^*}$ and $\|x_*-v_k\|_2\le Rk^{-t}$ for $k<d$; the error is exactly zero for $k=d$. The tail bound follows from $\max_{i>k}|x_i|\le Rk^{-1/p}$ and the tail $p$-power sum at most $R^p$.

For the smooth branch use the $\ell_1$-sphere estimator
$$g_h(x)=\frac d{2h}[f(x+h\zeta)-f(x-h\zeta)]\operatorname{sign}(\zeta).$$
Independent signs and Dirichlet absolute weights give $\mathbb E\langle a,\zeta\rangle^2=2\|a\|_2^2/[d(d+1)]$ and $\mathbb E\|\zeta\|_2^4=4(d+5)/[(d+1)(d+2)(d+3)]\le4/d^2$. The central-difference remainder is at most $\beta h\|\zeta\|_2^2/2$. Hence
$$\mathbb E\|g_h\|_\infty^2\le4\|\nabla f(x)\|_2^2+2\beta^2h^2\le8\beta(f(x)-f_*)+2\beta^2h^2.$$
The final inequality needs a global minimizer. The smoothing identity gives $\mathbb E g_h=\nabla f_h$ and gradient bias at most $\beta h$. Mirror descent in an $\ell_1$-strongly-convex prox at step $1/(8\beta)$ yields
$$\mathbb E[f(\bar x_N)-f_*]\le\frac{16\beta V_0(v)}N+2[f(v)-f_*]+4\beta hR+\beta h^2/4.$$
Here the bias term uses the Euclidean radius, and $V_0(v_k)=O(\log(ed)R^2k^{2/p^*})$. Smoothness gives $f(v_k)-f_*\le\beta\|v_k-x_*\|_2^2/2$. Choose $k$ from the stated public inequality and then a finite positive $h$ making the remaining bias arbitrarily small. A constant-factor tighter expectation target gives the fixed-success claim.

For the Lipschitz branch, the dual-averaging proof retains the comparator's prox value rather than the maximum prox value over the whole body. Its variance is $O(L^2)$ and its approximation loss is at most $LRk^{-t}$. Optimizing the step and using the same prox comparator gives the stated bound. The choice of $k$ needs no knowledge of the minimizer or its support. Simplified powers obtained by solving for $k$ have constants that need not be uniform as $p\uparrow2$; retain the integer formula when uniformity matters.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [1](https://arxiv.org/html/2610.00345v1)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Arya Akhavan, Evgenii Chzhen, Massimiliano Pontil and Alexandre B. Tsybakov. A gradient estimator via L1-randomization for online zero-order optimization with two point feedback. NeurIPS 2022.

https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf

[3] Gorbunov, Dvurechensky and Gasnikov. An Accelerated Method for Derivative-Free Smooth Stochastic Convex Optimization. SIAM Journal on Optimization 32(2):1210--1238, 2022.

https://arxiv.org/abs/1802.09022

[4] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[5] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper
