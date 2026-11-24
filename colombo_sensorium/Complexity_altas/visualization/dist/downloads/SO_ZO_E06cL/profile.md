# Lipschitz convex optimization in a general norm with known convex constraints and exact values

**Setting ID.** `SO_ZO_E06cL`

Single-objective optimization

Minimize a globally norm-Lipschitz convex objective over a known convex body using exact scalar values. Matched l1 geometry has an explicit randomized joint dimension-accuracy bracket; other geometries and deterministic regimes retain their own bounds.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Logarithmic gap; Other quantified gap

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Function lipschitz in declared norm; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space; operation: Function value; feedback quality: Exact

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $K$ and return a point with small objective gap.

### Admissible model

$B\subset\mathbb{R}^d$ is a known compact, centrally symmetric convex body with nonempty interior. It induces the norm $\|x\|_B=\inf\{t>0:x\in tB\}$. The set $K\subset\mathbb{R}^d$ is known, nonempty, compact and convex.

$f:\mathbb{R}^d\to\mathbb{R}$ is globally convex and satisfies $|f(x)-f(y)|\le L\|x-y\|_B$. Constrained minimization is over $K$; boundary minimizers are allowed.

Ball-geometry subregions are written as $K=B_p(0,R)$ and $B=B_q(0,1)$. The exponents $p$ and $q$ describe domain geometry and the regularity norm, respectively. General convex-body specifications do not require this ball parameterization.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $B$, $K$, $L$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in K$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in K}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$B$: Unit ball of the known norm **Domain:** $B\subset\mathbb{R}^d$; compact, convex and centrally symmetric, with nonempty interior.

$\|x\|_B=\inf\{t>0:x\in tB\}$

$K$: Known feasible body or minimizer-localization body **Domain:** $K\subset\mathbb{R}^d$; nonempty, compact and convex.

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_B$, $x,y\in\mathbb{R}^d$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$a_B$: Comparison coefficient between the specified norm and the Euclidean norm **Domain:** $a_B>0$.

$a_B=\max_{\|u\|_2=1}\|u\|_B$

$R_2(K)$: Radius of the supplied Euclidean enclosing ball **Domain:** $R_2(K)\ge0$.

$K\subseteq B_2(c_K,R_2(K))$, with known center $c_K$.

$\widehat{R}$: Combined norm and geometry scale **Domain:** $\widehat{R}\ge0$.

$\widehat{R}=a_BR_2(K)$

$r_m(B,K)$: Radius of the largest Euclidean ball inscribed in the norm-contractive linear image **Domain:** $m\in\{1,\ldots,d\},\ r_m(B,K)\ge0$.

$r_m(B,K)=\sup_{\|P\|_{B\to2}\le1}\sup\{r\ge0:\exists z\in\mathbb{R}^m,\ z+rB_2(0,1)\subseteq PK\}$; $P:\mathbb{R}^d\to\mathbb{R}^m$ is a linear map.

$m$: Dimension index of the linear image in the hard construction **Domain:** $m\in\{1,\ldots,d\}$.

Take the maximum only over integers $m$ satisfying the respective accuracy windows.

$p$: Norm exponent of the feasible or localization ball **Domain:** $1\le p\le\infty$.

$q$: Exponent of the regularity norm **Domain:** $1\le q\le\infty$.

For ball parameterizations, $B=B_q(0,1)$; independent of the domain exponent $p$.

$R$: Public radius in the explicitly stated feasible-body parameterization **Domain:** $R>0$.

$K=B_p(0,R)$ in ball-geometry regions, or $K=c+RB$ in matching-body regions.

$A_B$: Lipschitz accuracy ratio in the matching ellipsoidal subregime **Domain:** $A_B>0$.

$A_B=LR/\varepsilon$; used only in the subregime $K=c+RB$.

$s$: Proximal-norm exponent chosen by the algorithm **Domain:** $1\le s\le\infty$.

Use a public proximal function $\omega_s$ that is $1$-strongly convex with respect to the $\ell_s$ norm.

$\Theta_s$: Range of the selected proximal function over the feasible body **Domain:** $\Theta_s\ge0$.

$\Theta_s=\sup_{x\in K}\omega_s(x)-\inf_{x\in K}\omega_s(x)$; $\omega_s$ is known and $\ell_s$-strongly convex in the $1$ norm.

$m_0$: Minimum dimension for the linear-image hard construction **Domain:** $m_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$\varepsilon_Z$: Normalized accuracy threshold for the randomized exact-value lower bound **Domain:** $\varepsilon_Z>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_Z$: Positive multiplicative constant in the randomized exact-value lower bound **Domain:** $c_Z>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$C$: Upper-bound constant or universal threshold for an applicability window **Domain:** $C>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$d_0$: Universal dimension threshold required by the lower bound **Domain:** $d_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c$: Small positive constant defining the accuracy window **Domain:** $c>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_1$: Positive constant in the cube accuracy window **Domain:** $c_1>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$c_*$: Positive upper-threshold constant for the cube accuracy window **Domain:** $c_*>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $K$.

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

$f_*=\inf_{x\in K}f(x)$.

$\|\cdot\|_{B,*},\|P\|_{B\to2}$: Dual norm and induced operator norm of a linear map **Domain:** $v\in\mathbb{R}^d,\ P:\mathbb{R}^d\to\mathbb{R}^m$.

$\|v\|_{B,*}=\sup_{x\in B}\langle v,x\rangle$, $\|P\|_{B\to2}=\sup_{x\in B}\|Px\|_2$

$c_K,c,z$: Known centers of the enclosing ball, affine ellipsoid and inscribed ball in the linear image **Domain:** $c_K,c\in\mathbb{R}^d,\ z\in\mathbb{R}^m$.

Used only in the corresponding geometric formula.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=K$ and $\mathcal{X}=K$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$A_1$: Accuracy ratio for matched l1 geometry **Domain:** $A_1>0$.

$A_1=LR/\varepsilon$ when $B=B_1(0,1)$ and $K=B_1(0,R)$.

$\alpha_1$: Normalized accuracy for matched l1 geometry **Domain:** $\alpha_1>0$.

$\alpha_1=\varepsilon/(LR)=A_1^{-1}$.

$M_1$: Saturated dimension-accuracy factor **Domain:** $M_1>0$.

$M_1=\min\{d,A_1^2\}$.

$\Lambda_1$: Explicit logarithmic scale **Domain:** $\Lambda_1>0$.

$\Lambda_1=\log(ed)+\log(eA_1)$ in the small-accuracy domain.

$c_0^{(1)}$: Fixed small-accuracy endpoint **Domain:** $0<c_0^{(1)}\le1/8$.

Fixed independently of varying $d,L,R,\varepsilon$.

$c_\diamond$: Fixed normalized threshold for the penalized-support reduction **Domain:** $c_\diamond>0$.

$c_\diamond=c_{\rm err}/(8C_{\rm coh})$, where $c_{\rm err}>0$ is the fixed source-error constant and $C_{\rm coh}>0$ is the universal coordinate-coherence constant.

$\tau_d$: Boundary between the two randomized lower-bound arguments **Domain:** $\tau_d>0$.

$\tau_d=c_\diamond/\sqrt{\log(ed)}$.

$d_1^{(1)}$: Sufficient dimension threshold for the matched l1 joint theorem **Domain:** $d_1^{(1)}\in\mathbb N$.

A fixed integer large enough for Theorem 1, Theorem 2 and Corollary 1, with $d_1^{(1)}\ge\max\{3,m_0\}$ and $d^{-1/2}\le\tau_d<c_0^{(1)}$ for every $d\ge d_1^{(1)}$. No numerical threshold is asserted.

$\mathcal L_{\rm img}$: Previously available image-radius lower envelope with its admissibility guards **Domain:** $\mathcal L_{\rm img}\ge0$.

$\mathcal L_{\rm img}=\sup\left(\{0\}\cup\left\{c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})}:m_0\le m\le d,\ 0<\varepsilon\le\varepsilon_ZLr_m\right\}\right)$. An empty set of admissible image dimensions contributes zero.

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

**View.** Deterministic

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one exact scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime E06cL.R4

**Region.** $B=B_\infty(0,1)$, $K=B_\infty(0,R)$; $d\ge d_0$, $0<\varepsilon\le c_1LR/\sqrt d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B1

$$
O(d^2\log(ed)\log(e+LR\sqrt d/\varepsilon))
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+LR\sqrt d/\varepsilon))$

### R2 - Parameter regime E06cL.R1

**Region.** $B$ is an ellipsoid, $K=c+RB$, $d\ge d_0$ and $A_B\ge C$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7

$$
\Omega(d\min\{d,A_B^2\}/\log(e\min\{d,A_B^2\}))
$$

**Upper bound.** B8, B9

$$
O(\min\{dA_B^2,d^2\log(ed)\log(e+A_B)\})
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+A_B))$

### R3 - Matched l1 benchmark at fixed c

**Region.** $B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Also $d\ge d_1^{(1)}$ and $\alpha_1=c/\sqrt d\le c_0^{(1)}$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7, B19

$$
\max\{\mathcal L_{\rm img},\Omega_c(d^2/\log^2(ed))\}
$$

**Upper bound.** B5, B14

$$
O_c(d^2\log(ed))
$$

**Gap or comparison.**

$$
O_c(\log^3(ed))
$$

### R4 - Parameter regime E06cL.R3

**Region.** $B=B_\infty(0,1)$ and $K=B_\infty(0,R)$; $\varepsilon=cLR$ for a fixed $0<c\le c_*$, with $d\ge d_0$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Polynomial gap

**Lower bound.** B7

$$
\Omega_c(d)
$$

**Upper bound.** B6

$$
O_c(d^2)
$$

**Gap or comparison.** $O_c(d)$

### R5 - Parameter regime E06cL.R4

**Region.** $B=B_\infty(0,1)$, $K=B_\infty(0,R)$; $d\ge d_0$, $0<\varepsilon\le c_1LR/\sqrt d$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B4

$$
O(d^2\log(ed)\log(e+LR\sqrt d/\varepsilon))
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+LR\sqrt d/\varepsilon))$

### R6 - Matching-body zero-query endpoint

**Region.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q3

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B11, B13

$$
0
$$

**Upper bound.** B10, B12

$$
0
$$

**Gap or comparison.** Not applicable: exact zero query complexity; no multiplicative ratio is defined.

### R7 - Matched l1 benchmark outside the joint-theorem window

**Region.** $B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Outside the joint-theorem domain: $d<d_1^{(1)}$ or $\alpha_1=c/\sqrt d>c_0^{(1)}$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Other quantified gap

**Lower bound.** B7

$$
\Omega_c(d)
$$

**Upper bound.** B5

$$
O_c(d^2\log(ed))
$$

**Gap or comparison.**

$$
O_c(d\log(ed))
$$

### R8 - Matched l1: coarse accuracy within the support-transfer window

**Region.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7, B17

$$
\max\left\{\mathcal L_{\rm img},\Omega\!\left(\frac{dA_1^2}{\log(ed)\log(eA_1^2)}\right)\right\}
$$

**Upper bound.** B14, B15, B5

$$
O\!\left(\min\{dA_1^2\log(ed),d^2\log(d+1)\log(4A_1)\}\right)
$$

**Gap or comparison.**

$$
O(\log^2(ed)\log(eA_1^2))
$$

### R9 - Matched l1: coarse accuracy above the support-transfer threshold

**Region.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7, B18

$$
\max\{\mathcal L_{\rm img},d/(16384\log(ed))\}
$$

**Upper bound.** B14, B15, B5

$$
O\!\left(\min\{dA_1^2\log(ed),d^2\log(d+1)\log(4A_1)\}\right)
$$

**Gap or comparison.**

$$
O(A_1^2\log^2(ed))\le O(\log^3(ed))
$$

### R10 - Matched l1: high-accuracy dimension plateau

**Region.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

**Views.** Randomized

**Quantity.** Q3

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7, B17

$$
\max\{\mathcal L_{\rm img},\Omega(d^2/\log^2(ed))\}
$$

**Upper bound.** B14, B15, B5

$$
O\!\left(\min\{dA_1^2\log(ed),d^2\log(d+1)\log(4A_1)\}\right)
$$

**Gap or comparison.**

$$
O(\log^3(ed)\log(4A_1))
$$

### R11 - Matched l1: deterministic coarse-accuracy bracket

**Region.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le c_0^{(1)}$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Polynomial gap

**Lower bound.** B2, B21

$$
\max\{\mathcal L_{\rm img},\Omega(dA_1^2/\Lambda_1^2)\}
$$

**Upper bound.** B16

$$
O(d^2\log(d+1)\log(4A_1))
$$

**Gap or comparison.**

$$
O\!\left(\frac{d}{A_1^2}\log(d+1)\log(4A_1)\Lambda_1^2\right)
$$

### R12 - Matched l1: deterministic high-accuracy dimension plateau

**Region.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B2, B20

$$
\max\{\mathcal L_{\rm img},\Omega(d^2/\log^2(ed))\}
$$

**Upper bound.** B16

$$
O(d^2\log(d+1)\log(4A_1))
$$

**Gap or comparison.**

$$
O(\log^3(ed)\log(4A_1))
$$

## 4. Bounds and supporting evidence

### B1 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
U_{L,\det}=O(1+d^2\log(d+1)\log(e+L\widehat{R}/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $\widehat{R}=a_BR_2(K)$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Proposition 4, with a known distance-penalty reduction

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, with a known distance-penalty reduction

### B2 - Random support functions under a norm-contracting linear image

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{m_0\le m\le d:\ 0<\varepsilon\le\varepsilon_Z Lr_m}c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_IMAGE

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 5; printed pages: 5; theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: D26, Theorem 3.3, with zero known regularizer

### B3 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(ed)\log(4A_B))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ A_B>1$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12

### B4 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
U_{L,\det}=O(1+d^2\log(d+1)\log(e+L\widehat{R}/\varepsilon))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $\widehat{R}=a_BR_2(K)$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) pdf pages: 12; printed pages: 12; theorem: Proposition 4, with a known distance-penalty reduction

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, with a known distance-penalty reduction

### B5 - Non-Euclidean randomized two-point mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
U_{L,\mathrm{rand}}=O(1+L^2\Theta_s d^{1+2/\min(q,2)-2/s}/\varepsilon^2)
$$

**Sources.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [6](https://arxiv.org/abs/1802.09022) [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** $B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_RANDOM

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 4; printed pages: 4; theorem: Theorem 1; Lemmas 1, 3, 4

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 6; printed pages: 6; theorem: Theorem 1; Lemmas 1, 3, 4

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 8; printed pages: 8; theorem: Theorem 1; Lemmas 1, 3, 4

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) pdf pages: 7; printed pages: 7; theorem: Theorem 1; Lemmas 1, 3, 4

### B6 - Euclidean randomized two-point mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
U_{L,\mathrm{rand}}=O(1+dL^2\widehat{R}^2/\varepsilon^2)
$$

**Sources.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1) [6](https://arxiv.org/abs/1802.09022) [3](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf)

**Conditions.** Arbitrary B and K; Euclidean prox, with $L_2=a_BL$.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_RANDOM

**Source location.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) pdf pages: 4; printed pages: 4; theorem: S17 Theorem 1 / Corollary 2; D26 N.4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: S17 Theorem 1 / Corollary 2; D26 N.4

### B7 - Random support functions under a norm-contracting linear image

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\max_{m_0\le m\le d:\ 0<\varepsilon\le\varepsilon_Z Lr_m}c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})}
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_IMAGE

**Source location.** [1](https://arxiv.org/html/2610.00345v1) pdf pages: 5; printed pages: 5; theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: D26, Theorem 3.3, with zero known regularizer

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: D26, Theorem 3.3, with zero known regularizer

### B8 - Geometry-adapted two-point mirror descent or localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(dA_B^2)
$$

**Sources.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ A_B=LR/\varepsilon>1$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE, ZO_PROOF_PAIRED_UPPER

**Source location.** [4](https://jmlr.org/papers/volume18/16-632/16-632.pdf) pdf pages: 4; printed pages: 4; theorem: Theorem1/Corollary2

### B9 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(ed)\log(4A_B))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** $B\text{ is an ellipsoid},\ K=c+RB,\ A_B>1$

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_GEOMETRY_BASE

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12

### B10 - Return the known center without querying

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
C^\star\le0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No objective information is used.

**Guarantee conversion.** The gap is deterministically at most Lρ.

**Output rule.** The known center belongs to K.

**Resource conversion.** Exactly zero scalar objective calls on every execution path.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B11 - Nonnegativity of the charged call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
C^\star\ge0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No additional oracle assumption.

**Guarantee conversion.** Every admissible budget is nonnegative.

**Output rule.** The registered output space is retained.

**Resource conversion.** The infimum of nonnegative call budgets is nonnegative.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B12 - Return the known center without querying

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
C^\star\le0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No objective information is used.

**Guarantee conversion.** Deterministic success gives probability one, exceeding 2/3.

**Output rule.** The known center belongs to K.

**Resource conversion.** Exactly zero scalar objective calls on every execution path.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B13 - Nonnegativity of the charged call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
C^\star\ge0
$$

**Conditions.** K=c_K+ρB, ρ≥0, ε≥Lρ; fixed target domain.

**Oracle correspondence.** No additional oracle assumption.

**Guarantee conversion.** Every admissible fixed-path budget is nonnegative.

**Output rule.** The registered output space is retained.

**Resource conversion.** The infimum of nonnegative call budgets is nonnegative.

**Local argument.** ZO_PROOF_MATCHING_BODY_ZERO

### B14 - Product-Laplace smoothing and entropic mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
2\left\lceil576dA_1^2\log(2d)\right\rceil
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) Lemma 1, signed-simplex product-Laplace estimator and entropic mirror descent

Product-Laplace smoothing and entropic mirror descent

### B15 - Deterministic localization on the explicit l1 body

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(d+1)\log(4A_1))
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [8](https://arxiv.org/pdf/1706.07357)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [8](https://arxiv.org/pdf/1706.07357) Lemma 2 and Proposition 1; Protasov explicit-body value theorem, discussed in Lee--Sidford--Vempala PDF page 2

Deterministic localization on the explicit l1 body

### B16 - Deterministic localization on the explicit l1 body

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(d^2\log(d+1)\log(4A_1))
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [8](https://arxiv.org/pdf/1706.07357)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [5](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [8](https://arxiv.org/pdf/1706.07357) Lemma 2 and Proposition 1; Protasov explicit-body value theorem, discussed in Lee--Sidford--Vempala PDF page 2

Deterministic localization on the explicit l1 body

### B17 - Penalized support-function distribution with coordinate coherence

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{dM_1}{\log(ed)\log(eM_1)}\right)
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2) Theorem 2, Sections 5.1--5.4; normalized ZZQL Theorem 5 input

Penalized support-function distribution with coordinate coherence

### B18 - Full-domain hidden-spike adaptive exact linear measurements

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\frac{d}{16384\log(ed)}
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) Lemma 3 and Corollary 1; two charged validation values included

Full-domain hidden-spike adaptive exact linear measurements

### B19 - Joint small-accuracy lower envelope

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{dM_1}{\Lambda_1^2}\right)
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2) Theorem 1, composed from Theorem 2 and Corollary 1 in Section 7

Joint small-accuracy lower envelope

### B20 - Penalized support lower for the deterministic subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{dM_1}{\log(ed)\log(eM_1)}\right)
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2) Theorem 2; restriction of the unrestricted randomized lower to deterministic algorithms

Penalized support lower for the deterministic subclass

### B21 - Joint lower envelope for the deterministic subclass

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{dM_1}{\Lambda_1^2}\right)
$$

**Sources.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2)

**Conditions.** $B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

**Oracle correspondence.** Every arbitrary finite full-space query receives one exact scalar value; all smoothing, source simulation and selection queries are counted.

**Guarantee conversion.** The private-seed probability is per fixed objective. Deterministic upper witnesses have probability one; the product-Laplace witness uses expected gap at most epsilon/3 before Markov. Lower bounds cover arbitrary randomized algorithms and therefore their deterministic subclass.

**Output rule.** The point belongs to the original known l1 ball and may be unqueried; source decoding is valid for every feasible measurable output.

**Resource conversion.** One fixed cap applies to every execution path, including initialization and all auxiliary queries.

**Local argument.** SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

**Source location.** [7](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf) [2](https://arxiv.org/html/2607.16558v2) Theorem 1; restriction of the unrestricted randomized lower to deterministic algorithms

Joint lower envelope for the deterministic subclass

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 428384526cfd2cb9d509784b218794ef4a0e8fba3ef1ef364c1a05010cd3098c

### Native proof: ZO_PROOF_GEOMETRY_BASE

Native pointer: /proofs/0; canonical SHA-256: d6b8eb7b837b547d07112f9065a4fff7b241625efffba7e56094a8b8f9d6c4fd

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 4468fc6d9bbf4a1ea74651e295f99626443555521dac386c650e090b3f22dbb9

Let $a_B=\max_{\|u\|_2=1}\|u\|_B$ and let $R_2(K)$ be a public Euclidean enclosing radius. Then $\beta_2=a_B^2\beta$, $L_2=a_BL$, and $D_2=a_BR_2(K)$ give the deterministic smooth envelope
$$O\!\left(1+\min\{d\sqrt{\beta D_2^2/\varepsilon},d^2\log(e+\beta D_2^2/\varepsilon)\}\right)$$
and Lipschitz localization $O(1+d^2\log(d+1)\log(e+LD_2/\varepsilon))$.

The norm inequality $\|v\|_B\le a_B\|v\|_2$ and its dual give the stated Euclidean smoothness and Lipschitz constants. Apply the exact-value Euclidean acceleration or smooth localization theorem with those constants and the public radius; each transformed value remains one scalar call. The global-minimizer promise is retained for the smooth localization argument.

For a Lipschitz objective minimized over a known convex set $K$, define $g(x)=f(x)+L_2\operatorname{dist}_2(x,K)$. This is convex and $2L_2$-Lipschitz, $\min g=\min_K f$ on a ball containing $K$, and $f(\Pi_Kx)\le g(x)$. One value of $g$ uses one value of $f$ plus public geometry. The Euclidean ball localization theorem therefore returns a legal point of $K$ after projection. This is a concrete transfer to a general body, not a presumed general-body localization theorem.

If $B=UB_2(1)$ and $K=c+RB$ for a public invertible matrix $U$, set $g(y)=f(c+Uy)$. Then $\|Uv\|_B=\|v\|_2$ and $\|U^\top w\|_2=\|w\|_{B,*}$. Thus both the Lipschitz and smoothness budgets are unchanged, the feasible or localization body becomes $B_2(R)$, and one value plus the inverse output map preserves the exact gap, budget, and guarantee. No condition-number factor appears. Deterministic acceleration/localization and randomized two-point methods keep their original algorithm permissions.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: e5bf34af7950d8ee2664d09b259b1849e4fa3ae1ee7a4405a616ac92a8ff6664

Globally defined objectives, the declared regularity norm, a public feasible or localization body, and the stated free geometric operations.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: a1795be38e4c9c395f3571ba8859982c16974469de33e616917508807f2842b6

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /proofs/0/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 3

Native pointer: /proofs/0/source_refs/2; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 1ab0b833ad81901c161d28bf8c7db1cfbea162415c9eb514997fbae0a1895d3c

Norm conversion, penalized localization, and affine equivalence

### Native proof: ZO_PROOF_GEOMETRY_IMAGE

Native pointer: /proofs/1; canonical SHA-256: 892f66944e9f468111ef70e7b7e06565157e901138bd73bb2fc0740687d59f45

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 1cd2fd44286245db2e01d3873cb88247d0b94a6bed8634b453e4d8636e20dcf0

For an $m$-dimensional Euclidean image radius $r_m(B,K)>0$, smooth and Lipschitz lower bounds may be maximized over the integers $m$ for which their source windows hold.

Define $r_m(B,K)$ as the largest radius of a Euclidean ball contained in $AK$, maximized over maps with $\|A\|_{B\to2}\le1$. Dorn et al., Theorem 3.1, gives
$$T\ge\max\left\{5m/16,\ (m/4096)\min\{m,\sqrt{\beta r_m^2/\varepsilon}\}\right\},\quad0<\varepsilon\le\beta r_m^2/32.$$
Theorem 3.3, with its regularization parameter zero, gives
$$T\ge c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})},\quad m\ge m_Z^\circ,\quad0<\varepsilon\le\varepsilon_ZLr_m.$$
The all-space nonsmooth transfer uses the source's radial penalty for its homogeneous support-function hard family: a target query is simulated by one bounded source query and known arithmetic, and radial decoding preserves the output comparison. This permits the stronger all-space target queries without silently importing a bounded-query lower bound.

For $B=B_q$ and $K=B_p(R)$, put $\theta=(1/2-1/q)_++(1/p-1/2)_+$ and $\gamma=(1/q-1/p)_+$. The source's block certificate is
$$r_m\ge R\lfloor d/m\rfloor^\gamma m^{-\theta},\qquad r_d=Rd^{-\theta}.$$
Insert this certificate into each theorem before maximizing over legal $m$. For $q=2$ and $p\le2$, this is $r_m\ge Rm^{-t}$, $t=1/p-1/2$. Other source certificates, such as constant-radius quotient images, may be added only with their own operator-norm and dimension conditions. An exact geometric radius does not itself prove a matching optimization upper bound.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: effd57adbd4f2e6b8ac74ca034d0dcd07578cf89617bb46746e94c5feb0022bf

Exact values; the original all-space query/output reduction and all source dimension and accuracy windows are retained.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: b1a6d19e45f290a3e0020b31af423a2cf8268018186490ebf54856d1c7c72f45

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 2

Native pointer: /proofs/1/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 0dcb91b1df938d63c713d0645344dd76864094d407e54d2a7a1e71c8b334132e

Image-radius lower bounds and their admissible windows

### Native proof: ZO_PROOF_GEOMETRY_RANDOM

Native pointer: /proofs/2; canonical SHA-256: 9681ed890272028cd769f4d3e770d3cf82f4b4a2854794e610be0370676ef829

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 3bea1b77967e9979bba854eff9460c14cc442bdb4d30f8ed47a2c86424b0cb99

The applicable randomized upper bounds are
$$O(1+d\sqrt{\eta_{d,s}\beta_2\Theta_s/\varepsilon}),\quad O(1+d\eta_{d,s}\beta_2\Theta_s/\varepsilon),$$
$$O(1+L^2\Theta_s d^{1+2/\min(q,2)-2/s}/\varepsilon^2),\quad O(1+dv_H L_2^2\Theta_H/\varepsilon^2).$$

For the smooth directional methods take $d\ge8$, $1\le s\le2$, $s^*=s/(s-1)$, and $\eta_{d,s}=\min\{s^*-1,16\log d-8\}d^{2/s^*-1}$. Gorbunov, Dvurechensky, and Gasnikov's theorems apply to Euclidean smoothness $\beta_2$ and a prox divergence bounded by $\Theta_s$. Exact noiseless values use batch size one and two scalar values per direction; a finite positive difference scale can be chosen small enough for the fixed budget.

For the Lipschitz method of Akhavan et al., $q$ is the regularity norm and $s$ is the prox norm. Their theorem gives expected gap at most $11.9L\sqrt{\Theta_s d^{1+2/\min(q,2)-2/s}/T}$, with two values per round. Tightening the target by a factor three and applying Markov's inequality gives success probability $2/3$. A usable prox is
$$t_s=\max\{s,1+1/\log(ed)\},\quad a_{s,d}=\frac{d^{2(1/s-1/t_s)}}{t_s-1},\quad\omega_s(x)=a_{s,d}\|x\|_{t_s}^2/2.$$
It is 1-strongly convex in $\ell_s$ and on $B_p(R)$ has range at most $a_{s,d}R^2d^{2(1/t_s-1/p)_+}/2$. In particular, $q=2$, $s=p\le2$ gives the advertised $a_{p,d}d^{2/p^*}(LR/\varepsilon)^2$ term.

For Shamir's general-prox bound let $v_H=(\mathbb E\|U\|_{H,*}^4)^{1/2}$ for a uniform Euclidean sphere direction. Use ball convolution as the smoothed function, with sphere directions in its gradient estimator. The divergence identity belongs to the ball average; this formulation preserves convexity, Lipschitzness, the $O(hL_2)$ smoothing bias, and the source variance proof. All these witnesses are randomized, even when their value oracle is exact and deterministic.

For $B=K=B_1(R)$, Euclidean conversion gives $\beta_2=d\beta$, while the $\ell_1$ prox and directional factor contribute $\Theta_1=O(R^2\log(ed))$ and $\eta_{d,1}=O(\log(ed)/d)$. Substitution yields $O(1+d\log(ed)\sqrt{\beta R^2/\varepsilon})$.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 2dd7012e5a43034d8ab19de233e91264d77e296614beac9b70498741bec105aa

The direction distribution, prox norm, regularity norm, query domain, and randomness are distinct parts of the statement.

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 69e4cc09709afd15b575374fa42764c6d97311a36d4726f2c038a2d3fc2d8dc0

#### Native item 1

Native pointer: /proofs/2/source_refs/0; canonical SHA-256: 2cee8e21b7bc875b704141e0743e94f8f2584df042a10ecb2affee2b910dddf2

SO_SRC_2939e2a45af80e71

#### Native item 2

Native pointer: /proofs/2/source_refs/1; canonical SHA-256: 96834bf80f3bf3ec0a22adf5e62a559ee9bba0f6bbeca157c6b91e15f8b21e04

SO_SRC_72ac6a8c2c1738e3

#### Native item 3

Native pointer: /proofs/2/source_refs/2; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

#### Native item 4

Native pointer: /proofs/2/source_refs/3; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 5fbacee4c7b340daf764f6a06cd9843993375f5a86b58d10ff50483795d22e87

Randomized directional methods with explicit norm budgets

### Native proof: ZO_PROOF_PAIRED_MOMENT

Native pointer: /proofs/3; canonical SHA-256: 1590ade2e6787fe33d10f650f8ab64ef46bf6350869f6f4f185dad60be780bd6

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: 3ad958d5da6f01b544d353454c3372bc69148946dc23d87a9f02d9c83e87957c

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 8b49ec7dca2985f462ed168dfff1ed752288e50486b8b7133d5d5ea0e91edc18

A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: 2b913a5fb0aabb726f77d1aae7fd6ffc8d2d2a43974d8a9a576b6ed5f74e86bc

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 293f2ab735f268a2ffbfdb19ec489b03f31469acbe264107320d5061ad83ae63

Ball smoothing and the same-sample directional moment

### Native proof: ZO_PROOF_PAIRED_UPPER

Native pointer: /proofs/4; canonical SHA-256: 2e0e54fd584fc5d48d0ce8a9dba241d65ebbaa7375747bcc8134ff73f2fcfc4e

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 685be49a225f461c5aad1c8f1a5c7d6be838d104f66a8c19ee8e9caada27dac4

For a $\mu$-strongly-convex mean with $\mathbb E G^2\le L^2$, $K$ rounds and $T=2K$ scalar calls give
$$\mathbb E[f(\bar x_K)-f_*]\le\frac{4dL^2}{\mu(K+1)}+2hL.$$
The merely convex branch uses $O(d(LR/\varepsilon)^2)$ values.

Run the paired estimator on $K_h=B_2(R-h)$ and let $x_{h,*}$ minimize $f_h$ there. The shrinkage comparator $y=(1-h/R)x_*$ gives $f_h(y)\le f_*+2hL$. Set $V=2dL^2$, $\eta_t=2/[\mu(t+1)]$, and $D_t=\mathbb E\|x_t-x_{h,*}\|^2$. Projection and strong convexity yield
$$\mathbb E[f_h(x_t)-f_h(x_{h,*})]\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{V}{\mu(t+1)}.$$
Multiply by $t$, telescope, and average with weights $2t/[K(K+1)]$. The initial distance coefficient is zero and the last is nonpositive, giving $2V/[\mu(K+1)]$. Add the comparator error. For expected accuracy choose, for example, $h=\varepsilon/(8L)$ and $K+1\ge8dL^2/(\mu\varepsilon)$. For success probability $2/3$, use $h=\varepsilon/(12L)$ and $K+1\ge24dL^2/(\mu\varepsilon)$, making the expected nonnegative gap at most $\varepsilon/3$ before Markov.

For convex objectives, the projected averaging recursion with step $R/\sqrt{VK}$ gives expected optimization error at most $R\sqrt{V/K}$, plus the same smoothing/shrinkage error. Uniform component sampling makes the estimator unbiased for the finite-sum mean and costs exactly two selected-component values per round. Neither the oracle nor the components need be stochastic in that case; the algorithm supplies the randomness. These bounds also hold under an almost-sure Lipschitz promise, since it implies the required second moment. The Gaussian lower construction in the separate lower lemma does not acquire that stronger promise.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/4/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: module_dependencies

Native pointer: /proofs/4/module_dependencies; canonical SHA-256: 0f93027dd13c1fc76f53eafc5f7af337161f3e067e9523895d0587c084c781f1

#### Native item 1

Native pointer: /proofs/4/module_dependencies/0; canonical SHA-256: 89f132536e860e550967b3b720a81cd0588e96be63dd5faf8219129f756df13e

ZO_PROOF_PAIRED_MOMENT

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 1cee90c0ade7a1c76974664107d84323ced5a0094233ab2475673590acf69a2f

Optimization/output in $B_2(R)$; all two-point queries remain in the prescribed ball; mean strong convexity suffices. A uniformly sampled finite-sum component is also a valid fresh sample.

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: e508c27dccb22eb6891bf8af030dc2253349aaf59b1ef7a90b2a3177a1b6408f

Projected optimization with same-sample two-point values

### Native proof: ZO_PROOF_MATCHING_BODY_ZERO

Native pointer: /proofs/5; canonical SHA-256: 4ec2d74319ed348757fa098a0ac1805e2a065d4d36c1795c70295f0f1dd44ef6

#### Native field: baseline_refs

Native pointer: /proofs/5/baseline_refs; canonical SHA-256: 8354be7a3fcdd63335222e734e9b94ba784ba153d64d8584e23a44ccc6305d31

#### Native item 1

Native pointer: /proofs/5/baseline_refs/0; canonical SHA-256: cc81e3798ebc32618496a90480d46151c7b2611cdcb4b0c6aa4ca677ffaf64c4

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/0/sha256; canonical SHA-256: abf1fae15085ad1b3179311d9de64543b05a1f28041dfa986f2483be9e447da1

eb76338084545e3bb4e6499f5de20533d5e758c77e11e1e2c3a80e2a576e90e4

#### Native item 2

Native pointer: /proofs/5/baseline_refs/1; canonical SHA-256: 16e16a91d81ac90006d9de623596fd03825cc127779514310184e9f2f32dbd46

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/1/sha256; canonical SHA-256: 38f974c942511a34d341344c7159095331598aaab36cbd85f1183200916a36f2

583552b3be7cc093f09579c96c8e736b59b3543dcdc921a3dff35916cc233f17

#### Native item 3

Native pointer: /proofs/5/baseline_refs/2; canonical SHA-256: 713042387dabea829b64781565e893cd51bd15e2d130de7281e038eba11701a2

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/2/sha256; canonical SHA-256: 29b1e254dca764e049b7026212d2dec590ebe7f006854f4cdd10eb0951ddef33

0e6d148192001eff47d2806160019a01d78c8d738539b0e4dd10cc0c879b7fe7

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: 1c436f29f6c136a8144171f723bf998d0273e311dc33aeb46b329916be3b6d5f

Retained premises: the frozen common specification gives global L-Lipschitzness in the B norm, known B,K, output in K, and charges scalar objective values. Both views permit deterministic algorithms; randomized g1 requires success at least 2/3. The q1 quantities minimize a nonnegative call budget. For u∈K=c_K+ρB, ||u-c_K||_B≤ρ, hence f(c_K)-f(u)≤Lρ. Taking the infimum over u proves gap≤Lρ. Returning the known center without objective information therefore succeeds deterministically whenever ε≥Lρ, including equality. If ρ=0, K is a singleton and the gap is zero. Nonnegative costs give C*≥0, proving C*=0 in both views. No global-minimizer promise or extra oracle is used. Sharpness for ρ>0: choose a nonzero vector a and normalize it by max_{b∈B}a·b, positive by compactness, symmetry and nonempty interior. Then max_{b∈B}a·b=1 and |a·v|≤||v||_B by the gauge definition. The global convex functions f_±(x)=±La·(x-c_K) are admissible and have minimum -Lρ on K. Their ε-good sets respectively require a·(x-c_K)≤ε/L-ρ and a·(x-c_K)≥ρ-ε/L. These sets are disjoint for ε<Lρ. A zero-call algorithm has the same output distribution on both objectives, so one success probability is at most 1/2. It cannot satisfy deterministic g1 or randomized success 2/3. This last argument proves only nontriviality below the endpoint, not a main-rate lower bound.

#### Native field: limitations

Native pointer: /proofs/5/limitations; canonical SHA-256: 6b0f1f0a1869fb8936df0e4ed0393b75fa9bae575c903bbce424ee73f83a889f

#### Native item 1

Native pointer: /proofs/5/limitations/0; canonical SHA-256: c281d159b627016d8b56f7be27eaec0b11e8af037ea9808a795baf32cbe2e444

Below Lρ the proof establishes only that zero queries are insufficient.

#### Native item 2

Native pointer: /proofs/5/limitations/1; canonical SHA-256: 1a757e0c1265dcb5c6a832599a3e35dc791c395dd8da355ac554be60cbba8d84

Unchanged external baseline theorems are retained conditionally.

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: fa7ce2cf28e484bebc3932c1d8246851f0ade793d2bcf311d0f8b9e74c934b34

Both registered g1 views; known K=c_K+ρB, ρ≥0; fixed-path scalar-value budgets.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: 860938997582bb095dd828732c4f4a8b357c97b816d9443cdf273306ca066580

Exact zero-query threshold for a matching norm body

### Native proof: SO_ZO_E06cL__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/6; canonical SHA-256: 5ba99f5a0e75db27657e999519bd94ab5f69a5829e445ce09cbdd727e02ab0cc

#### Native field: body

Native pointer: /proofs/6/body; canonical SHA-256: 684c665b3c4a236b79d382a25b94eb03fc9570c5fe4b721f3a0d02e3cd7a093a

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature.

#### Native field: comparison_refs

Native pointer: /proofs/6/comparison_refs; canonical SHA-256: a8ea6921a245a2ba99dcb8aaf7b5ec5181288ea28c8116e82c7bc676962c4621

#### Native item 1

Native pointer: /proofs/6/comparison_refs/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 2

Native pointer: /proofs/6/comparison_refs/1; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: evidence_basis

Native pointer: /proofs/6/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

### Native proof: SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

Native pointer: /proofs/7; canonical SHA-256: 144aa3d30b3afc667e04beefbc224742e5ce968c682b92276ad16a412924e972

#### Native field: title

Native pointer: /proofs/7/title; canonical SHA-256: f9bfdebab1d3054f72e881bd45809423f47cdaaf09da46e4fbac4ed4f806b7ed

Matched l1 normalization, admissible envelopes and algorithm scopes

#### Native field: scope

Native pointer: /proofs/7/scope; canonical SHA-256: 58ac828e0cecd0b1054843dc044d9e6545eaa69eac464be6c3933d24b12fe1d3

$B=B_1(0,1)$, $K=B_1(0,R)$, exact full-space values and feasible arbitrary outputs.

#### Native field: source_refs

Native pointer: /proofs/7/source_refs; canonical SHA-256: 345de25e948b57d310d8102c39c87c455a59609f1ddae121f1ad38cc5f4fc901

#### Native item 1

Native pointer: /proofs/7/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /proofs/7/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native item 3

Native pointer: /proofs/7/source_refs/2; canonical SHA-256: 74ca633bf39c086deed99631293bb2ed5e84f8d20b7758d8448b19d09d96e9c9

SO_SRC_9557f7498abe575b

#### Native item 4

Native pointer: /proofs/7/source_refs/3; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native item 5

Native pointer: /proofs/7/source_refs/4; canonical SHA-256: 3870a660e3630920141416411901519b55e702fccd2d42b40fd802fefe8f62ee

SO_SRC_LSV_1706_07357_PROTASOV

#### Native field: body

Native pointer: /proofs/7/body; canonical SHA-256: 29a75cafc0b169b01fc51ddca3f7e33d40543c08270e795734e3aaaf352a0f6d

For $g(z)=f(Rz)/(LR)$, convexity and global l1 Lipschitzness give $|g(z)-g(w)|\le\|z-w\|_1$. A value of $g$ is computed by one value of $f$, and $z\in B_1(1)$ decodes to $Rz\in K$ with the same normalized gap $\alpha_1$. This preserves every pathwise budget and the per-instance seed probability.

Lemma 1 of Colombo_KIMI_001 uses exactly $2\lceil576dA_1^2\log(2d)\rceil$ scalar queries and yields expected feasible error at most $\varepsilon/3$. Nonnegativity of the gap and Markov's inequality give success probability at least $2/3$. Its witness is randomized. The public-body value-only theorem in Lemma 2 instead gives a deterministic witness with $O(d^2\log(d+1)\log(4A_1))$ calls; the cited Protasov ingredient is for an explicit known body, with free auxiliary geometric computation.

For the source lower bound, ZZQL Theorem 5 applies to a fixed distribution of max-support objectives. Its original Lipschitz constant is 2; divide the functions and their errors by 2. The resulting rows are truncated Gaussian vectors divided by $2\sqrt d$. Their coordinate-coherence event has constant probability uniformly over the legal numbers of rows. Colombo_KIMI_001 Theorem 2 uses the known penalty $\lambda\operatorname{dist}_1(x,B_2(d^{-1/2}))$, with $\lambda=C_{\rm coh}\sqrt{\log(ed)}$. Its decoder sends every feasible output to that inner ball; positive homogeneity answers every finite full-space target query with at most one feasible Euclidean source query. Conditioning costs only the fixed prior probability. Thus its lower bound retains the same all-space oracle, arbitrary output and unrestricted randomized algorithm scope.

Set $M_1=\min\{d,A_1^2\}$. For $\alpha_1\le\tau_d$, Theorem 2 yields $c dM_1/[\log(ed)\log(eM_1)]$. Above $\tau_d$, Corollary 1 gives $d/[16384\log(ed)]$. There $A_1^2<\log(ed)/c_\diamond^2$, so the ratio of the two-point upper to the latter lower is $O(A_1^2\log^2(ed))=O(\log^3(ed))$ for fixed source constants. For $\alpha_1\le d^{-1/2}\le\tau_d$, $M_1=d$ and the regional lower is $\Omega(d^2/\log^2(ed))$, independent of any further accuracy refinement. Theorem 1 also gives the weaker but uniform expression $a dM_1/\Lambda_1^2$ over the complete stated small-accuracy domain.

Every admissible image-radius lower inequality remains valid. Taking its supremum with zero gives $\mathcal L_{\rm img}$, and taking its maximum with the new applicable lower cannot weaken the bracket. In particular, a previously available finer-accuracy image lower is not discarded. The upper envelope is the minimum of applicable algorithms under the same guarantee. On the fixed-$c$ slice $\alpha_1=c/\sqrt d$, with $c>0$ fixed, $dM_1=d^2\min\{1,c^{-2}\}$ and $\Lambda_1=O_c(\log(ed))$, giving a new $\Omega_c(d^2/\log^2(ed))$ lower while retaining the existing $O_c(d^2\log(ed))$ randomized upper.

A lower bound for all randomized algorithms also holds for deterministic algorithms. The deterministic upper is only the deterministic known-body method; the randomized two-point witness is not used in that view. Consequently the deterministic fine-accuracy region is near optimal, whereas its coarse-accuracy bracket retains the explicitly displayed polynomial factor.

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 64bcf4da532f44b11880870b0b495181d0940b7565426a9368f2a882c078bfd9

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 4600808a9f6a83573950edc0da23c72fd27d55646bd9fe43f3a46b265a4c344a

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 149569bbc26cbea242c7d2c383a104ac84c9cf671c25c96cdfa3151d3e514c3a

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 7dc362bd2ec232f744946a1343beac9e90c65f7c3c16b235276f92132c540764

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 6c25379fda6da55a7f741ac0bdb980a5a25cd384ed9c4e7e00b64903e531d7a1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: b1edb5b715f24b7d603487b943ba2d651141174d2f05b8a98744d133cd7a2dc2

Native comparison predicate with original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: bfa764e809800152e2a95de9e5ceb91b5b743bcaef6d32af0ffa0d384885cfe3

Conditional accepted-baseline retention; external premises not recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 9cafd9bef64911132434dc616bc51e63185d4b1cf2e1537ffa6bf012fa151fd5

All B,K; Rhat=a_BR_2(K); retained constrained localization transfer.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 9edece33cfbac61bada6807e1224f1bf4ea87bc81cc46a91784bf20bbdf76af7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: b1edb5b715f24b7d603487b943ba2d651141174d2f05b8a98744d133cd7a2dc2

Native comparison predicate with original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 101619bfbaa31e52ac3e1f1928fc9f373cdacdb0ec99ba50958cf0e2a47fcfc4

m_0≤m≤d, r_m>0, 0<ε≤ε_ZLr_m; maximize only over admissible integers.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 80babb135f537486642340e3741fdbe05be6e47fc468165faa477e37e39f58d6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: ad365ff5cda2c951ff747cb4ec78953c9d7a84c48513e7ac38ee3ce956bff017

Distinct q2 identity; no transfer or merge.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 817f1ac02b3cf5d14425740fdd3d0a2d5f6a693c651160f8978483418c4db37b

Matching ellipsoid, A_B>1; deterministic q2.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: c55dc435510b11321d68f13b06b2a940c1c12ccf0e586f6d02ec094d370903b9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 56fd5232e1d63b8e0c0f7cfc52e8500749c1ef8f6eb2b3918214689fc5eaab69

Z is disjoint from the adopted positive lower window: r_m≤ρ and ε_Z<1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: c0f89055ac4df70103351c91840089d46d4c0ad53240c5e4b5977dbefe089eff

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: b44d7c5dd08d59b6f59c6ae95825d38ef43694fe67b90e0ce9e7c13a70dccef1

The zero-endpoint guard is outside this adopted comparison region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: d37b1fc91551b268169e083af18f2cc7e5b909a77a7753ba361138c441c34758

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: a83bf89100d8a6105fe70ad23922a38240a63eef4b20e32c3558b9382761c529

Preserve all source dimension and accuracy guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 4abab667faa5a061849ef5cec587fb26f82e107ab257bf3dcf34b5483c38c97a

Precision-independent lower saturation does not establish finite-query exact reconstruction; the upper cost retains logarithmic accuracy dependence.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 9a5e03541de6895f29acfc987c68421d862bdd15c004f682eddc529a70a9beb0

O(log²(ed)log(e+LR√d/ε))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: feb0dedda3cd4ee5f52cea8ea60a8020007e469b165a9614ee82d57ed83ba31c

Ω(d²/log(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: b5acfb54cafba5da601768bddcb1ee63dd29c6c68681efb54d3835516958ff72

Native logarithmic gap retained conditionally; other regions remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: bc83b13ad72b7de2c3530f2fc3e728c813c125088a7c3051c559df0280779bd5

O(d²log(ed)log(e+LR√d/ε))

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 8c24d97c4fb115f155dc8e95646696d4ac63e333fceb2276141dce4b928d5b7d

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 37e89ae5ceda2adb0441364e69fa2d57ecb769961e6b9ff845367ec299c3673b

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 2b0543a16bb3e5a116dc838098a044a69700b6e262db49e9092a3ae197388a16

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 72d7884fbdeea7db55f8dc4cbed4fba15fa2929e4493f95f96287f53c5f169ec

a_BR_2(K)≥R; affine-invariant b6 is no worse up to universal constants.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: ed0a0e94328f0b5afb51852f40314aaf13d8305f697d5132308165d7d24a324e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 7a0a7f5ca975573a0b26ab380d4a409aa8d5a5e81107ce42c7ce7b7236e3b961

On the applicable B_2 subcase its optimized retained scale is dA_B², covered by b5. Other ellipsoids fail the native B=B_q condition.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: b487970aa1a009b70c411b29209c6942962c247290101b0d3ddd3e902034943f

B=B_q, d≥3; public ℓ_s prox with known range Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 88a99857e1f522cb5435426be748dab83ced42f105c1745115714704a0faec39

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: b86eb3a4d716cb7efc2cb6995ce62d9ce4df7bee98724db08973ee1494a86bf3

a_BR_2(K)≥R, so this conversion cannot improve b5.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 54a1b58fb872422b81da77fa20136daa3a3e02a1e860b40ec4548f53edff325a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: d87c039c7117adba0214e0aa6067b9420575317880b529d4bc069262d93a2cc8

Native ellipsoidal comparison and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: a50a3b19e057ea8666735da06aee519412a76c03e228c1ae523f1600191602f6

m_0≤m≤d, r_m>0, 0<ε≤ε_ZLr_m; admissible-integer maximum.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: 463c32743cba5809e83f96f3cdc9e6600e50bf921b9e0cc5bcba684c146fc1e9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 4b69bec2ba778e83f5d62b14341ea213b348bc27c5f9f882f1ff86f8380732a9

Native comparison with original guard; retain inside the minimum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: d6397c3d74ea4928760aba95ad19f5760e62d8231cc62b1cf3d08d50744297de

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/1; canonical SHA-256: 35d31d90801dd65b1e9e1658ed7d97bf28b7829088e44457c220c190834be5c0

ZO_PROOF_PAIRED_UPPER

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 8e3df867e9deb0af8cb7be0501b3dd48dd3b34273752f7300916b5861cbc74fc

Conditional retained two-point upper branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: f4af8248a9001cc322c513322302ceb6a7d73ae9ff9538b45bed99d3af5e7af3

Matching ellipsoid K=c+RB; A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 0afccedbf593c4ac6572fad5412f59dbbfa21fcefeee66fc773973d23f736efe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 4b69bec2ba778e83f5d62b14341ea213b348bc27c5f9f882f1ff86f8380732a9

Native comparison with original guard; retain inside the minimum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: 7c07f23f2e8d3d5465ac43d84d6a5ee5cdc9847ffec26d31763abc5a1c616d81

Conditional retained localization branch.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: f4af8248a9001cc322c513322302ceb6a7d73ae9ff9538b45bed99d3af5e7af3

Matching ellipsoid K=c+RB; A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: 55be14db1ce557984a6925d260a29d0714ab2ce06153ebd39da4a7f52c6e7c35

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: 12db5694bf56c21875c0ff358dead3a9f92e6b7dc9845162ac728ffd240ec28c

The adopted nontrivial source window has ε<Lρ.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/bound_uses/7; canonical SHA-256: cce564b2a5179aa773d70b35fd2242efd601cff74cf2f6a35956e67ceb090530

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/reason; canonical SHA-256: c7fcf15c08594a03768f08619ecd1879ba3f9784e10eeb41a19ac32f088f9d4b

Outside this adopted nontrivial region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: e778807e771d1fa74a67422f3000eca259a906960082388d72f3dac8df767bb7

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: d78bea4e7a9bed5b8ec36aa56e01dde76584c7079e36e99cc95a2534f83c9f6e

Lower saturation has asymptotic scale A_B²≈d.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 595f9b90472ea4c908a90e733c7066bf347d61cb201f3fcbc098f28f57b5a4e6

The upper crossover instead solves A_B²≈d log(ed)log(e+A_B); this is not an exact activation threshold.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 95102c00e525358114cca9b5bea654c6d0d08150d8ca69950abc8da48d75adb0

A_B≤1 is covered by the new endpoint, outside the adopted nontrivial source window.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: b3b520fd51f18666f50d7c61a036ce88943bc42b8492b9745f1d92d0cca526b7

Retain native O(log²(ed)log(e+A_B)).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: ded3a4df66e2559098f19f6f9acddaa7d2a147a1065900122a428f72f673c814

Ω(d min{d,A_B²}/log(e min{d,A_B²}))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: e1276bd548be8e0acb27bf3177431d18c31d11e8564a29c18afed07db1e3c56c

Native logarithmic gap retained; broader geometry refinements remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: e45bcf5b7b74b4615daa334f5280884ea0f1e7adfe81f4040fa5e56557dea7f2

O(min{dA_B²,d²log(ed)log(e+A_B)})

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 1a2aadf50b3828d1d4e7071e9a5762be7622758b7a2671638e1a318584aa1552

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 1d79a8edf705f2937e1cf23195e82927b33d556ce355387a4ab593768f5bbd2b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 092472081e34ee24f457569be673d2bebbfaf6514079abe91898afb4467dd16f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 41497e49974ed35c8eb39dbe5d293652264c3b608ca0b3aaaed1f4e3c9347fca

Localization is O_c(d²log²(ed)), worse than recorded b3.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: d77648171ff2c4499c05131c860348420347fbcd589bdc4289c4685a18a52358

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: af1a5b236dcbbe4b3330f697cf86e38ce4f66a0a7d58ace0759bcf653a93dd21

On the cube its best retained prox scale is d²(LR/ε)², already supplied by b3.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: b497ae2364fecdd3a34b4f9e7c464b0ad551adda517a144861a1a0780316f309

B=B_q, d≥3; public ℓ_s prox with known Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 3bd0b91bb4f75a996cf39db4312f6ba596773c5782f5263cd177b5fbe6ec14b2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 78a2ea64ce53f5cecdfc0cea52adcbcc40e5f1e314407f614eafcaaff627bb71

Native fixed-c cube slice and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 5bb2ce1e1fa9f4646f64adb5dd16a543bcf8d7b973094f1cb2e182a23311d9da

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 2929ae4baac4726f86a06ce0c46bd4e2703449eecdab49f1af829af540bfb3f7

Native fixed-c slice with original admissible-integer maximum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 1572abac21bef7208051475d3a040151e63a99f8a023f5937ba2642e8de9fac9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: b0204cd117ebd4d8ebf795c205ca29a33d122e9b156814db76f76166c271bde5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: 55be14db1ce557984a6925d260a29d0714ab2ce06153ebd39da4a7f52c6e7c35

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: 12db5694bf56c21875c0ff358dead3a9f92e6b7dc9845162ac728ffd240ec28c

The adopted nontrivial source window has ε<Lρ.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/2/bound_uses/7; canonical SHA-256: cf2a2ac58f27c67c519002a4b5a81f2c22c5c1c1e4fe019dd970b7ea888c5c59

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/reason; canonical SHA-256: 04fce2c337b76961477c1bcd1e2ffebbe015dcca08d0ad3963400fa432108ede

Outside this adopted nontrivial slice.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: fef95c0620815cae43ab12f4a7a1680f60d56fd2676d359d6c6bc9f11c59ef9c

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: 9cffd20d2d5c0c6acb85330ddd66012b252386ad3d8c49690801a03f9dcce253

Keep c fixed with 0<c≤c_*; constants may depend on c.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: e6f1fc90df4ead0027730361090066464428c70d52526e467c8e95bbe57a297d

Any overlap with the high-accuracy comparison retains both original theorem guards; it does not make O_c uniform in ε.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: fd2079a3096d5abb9bdf54cc5c80262e7b58bac10d524846455474beff760be9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/constant_dependencies/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: fd2079a3096d5abb9bdf54cc5c80262e7b58bac10d524846455474beff760be9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/fixed_parameters/0; canonical SHA-256: 879923da020d1533f4d8e921ea7bac61e8ba41d3c89d17a4d14e3a89c6780d5d

c

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: dcbdf3b13781daddd6c9a07ea313664a7b314dc779caeb397a029adf5d962500

O_c(d)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 14f5da8af882bab21f491b3d1542445aab83b51915ceda0c623b676bcd4d8697

Ω_c(d)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 27ee20d56ee1b1b8c8eb759a83cdf22f976aa9d2aec5664cdb610a1c91d8b5ce

Native polynomial gap on this fixed-c slice; other accuracy regions remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 62b449dbc13ed6b7bb2fbdfffb22ccc371fba1f0a7bc724657906774a3c8cbee

ε=cLR, fixed 0<c≤c_*

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: a1140e5ec2f68bba2b31bbdb0bb583057108ed570279cfde962555b6672a7e10

O_c(d²)

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 2c8e6e8110b67ef60544cf984b50de5adf5b2bb9035205b71dd4cff07b067d5c

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: a70b71eda4153733f064699a404a501be31424d081e8d23d69e76fc7c86ef030

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: a041ea37b0c3ecf714fe76a09a5c7dbc682386e3e9e7ba9d92b3017a95b02ace

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 013df455f4eb22c3aa8793d037ab2d6c2b09b6bcdbfa7487655961a8f13ed9ef

Native high-accuracy cube region and original guards.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 8ddf9ae3988394c6f34c015449d72718bad98d0e553b0e872c0025b1a6df6957

All B,K; Rhat=a_BR_2(K).

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: c75cf132ffdc5058da2407004fc57a196d135f2f7b450fbc0cac1629384a75b4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: e95815f6205c3cacba8a3b9023eaf13eb3c46069e94dd05465f34d45ae50b318

The retained cube estimate d²(LR/ε)² is asymptotically larger than localization on this small-error region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: b497ae2364fecdd3a34b4f9e7c464b0ad551adda517a144861a1a0780316f309

B=B_q, d≥3; public ℓ_s prox with known Θ_s.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 9fe15bba2f3e899e327f74570216abbad6564dfe166a7f689c4b4feda03578d1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: c2004c6ba7dd6855e7dba779db0784144445b88245112b8ecb74f61d0910cc02

Its cube estimate d²(LR/ε)² is asymptotically larger than localization here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 677ffa90bdc86e59b23608d1cc6356c42aa3d4970de1db5196c0c732d4dfe636

All B,K; Euclidean prox, L_2=a_BL.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: 18a2b926694ff441644c68b4abd8d45f508b4e1d5a781f3fe29be2d9c9f42b97

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 9ac0e1e801709a007b7903c43eaf7365482510017b8f64267e1ecbc4d8c50a4f

Native region with original admissible-integer maximum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 63835ec004c57d571b8729ff71d8b718934d763bcdcca4e41ded685638329dae

Conditional accepted-baseline retention.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: 1572abac21bef7208051475d3a040151e63a99f8a023f5937ba2642e8de9fac9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: b0204cd117ebd4d8ebf795c205ca29a33d122e9b156814db76f76166c271bde5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 716a2f3396413ec0015b749ae63e421f0e28093690689e7456e6b2625292b56a

The adopted high-dimensional cube is not ellipsoidal.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: 872e54ac303ceb7c942c5b1203fe9aee8df815b65b77535760e7ec85a50d9f14

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 60dec7cd9df1d9d46b4dfaa2de81fc3babdf1ea18807dea2b3a81483a82b8f9b

r_m≤ρ and ε_Z<1 separate Z from the adopted source window.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/3/bound_uses/7; canonical SHA-256: cce564b2a5179aa773d70b35fd2242efd601cff74cf2f6a35956e67ceb090530

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/reason; canonical SHA-256: c7fcf15c08594a03768f08619ecd1879ba3f9784e10eeb41a19ac32f088f9d4b

Outside this adopted nontrivial region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: c76f1a0aec399322a3e1f1244099111fff0bbe307c89530f2da17d4011d31b8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: e0633ac8da714cd58f8bdc2ba16b9ba5fe9fd10d0d76f933ef993ea754f38384

Keep all original source guards and universal thresholds.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: 5579055a222d99c424b32ae6c960bd4a43807fa1e28f66b3d7714f6f8c81b4f4

Precision-independent lower saturation does not certify finite-query exact reconstruction.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: f9d801bee09418ccaa7f69e9639d58453c10db7a021c4111aa2002f5723d9906

No fixed-c slice statement is substituted into a varying-accuracy bound.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 9a5e03541de6895f29acfc987c68421d862bdd15c004f682eddc529a70a9beb0

O(log²(ed)log(e+LR√d/ε))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: feb0dedda3cd4ee5f52cea8ea60a8020007e469b165a9614ee82d57ed83ba31c

Ω(d²/log(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 53d50fac9792a123524eb234e5d9e857cc0b78f30c959d88830a59871cc6c5c2

Native logarithmic gap retained; remaining accuracy and geometry regions are unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: bc83b13ad72b7de2c3530f2fc3e728c813c125088a7c3051c559df0280779bd5

O(d²log(ed)log(e+LR√d/ε))

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: c5a35c992233b98c32543db7ca54022190760bde8ffe77c2ec3dceff47ab1f38

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: 10d5068897dff07f4aaa322cd293af4571f886fa702ffe4123974ce73a27e9c0

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: c3a258faf247a9312d6589d1f1f5747cee7870db4ce5427daa4b350c93ab487e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 3efa30015f124631c7172e46648f5bf2c8f27127f1bbba876ea77595719b4eb1

Its positive upper estimate is superseded by zero calls on Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 21182f6ea2d30f63ba75be8eac7ad88fc5fa3ac1451958791520395d32001edf

All B,K; retained localization transfer.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: ee8509857a59dccae97876c9b6ffe8b75fb4b80597365a832eb1247f2600463f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 017663b113fafa50b91ab77f8715cca538f4d51e4db9586b71996af266560977

r_m≤ρ and ε_Z≤1/√8<1 make the source window disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 0f586c8519246e7ba0ee37415ba82e8094109a83ebac48f02bbd762cd8a743a7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 0aecda2c4cc618ff46dd162c93955171dcf91db02b4a84e374c715c0420bf50d

Separate q2 identity; no transfer.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: b8943b5d8f982801c3678505d4bda728676bad2c958363b2c10d537125d85d4c

Matching ellipsoid, A_B>1; q2.

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/bound_uses/3; canonical SHA-256: bbf3d7026e8c5625e183f895dcb47788d1d0eef0d9278fd77a8250fe3260ecc2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/bound_id; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/reason; canonical SHA-256: 506aa74189375b9ac386663e45a2bef9e224ea0d285ed97885624d5448112367

Return c_K; gap≤Lρ with zero calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/3/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 5

Native pointer: /joint_analysis/comparisons/4/bound_uses/4; canonical SHA-256: 498ce31dc997ed4f1c764fda67e6ddf8fae5df15becac8c374ac15714b395591

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/bound_id; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/reason; canonical SHA-256: 64a6ab15c6bc5268e643e197d8ce404cf28205bc78c2e61fc5e7405b3ec9be25

The charged call budget is nonnegative.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/4/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: 552b9f73d332a35ec5b9b295044b03bc7d520576d93b906f5b48cfeb8da2cd46

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 7417ea1ff959726c312a30d2087735604ffccee190c834e657a30a0fd9b9c389

Equality ε=Lρ is included for ρ>0.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/boundary_checks/1; canonical SHA-256: 1f4258f7b041d2a89c7b08f19027453692a4257b4faab824e561f51ac44bda4a

For ρ=0 the feasible set is a singleton and all ε>0 have zero cost.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/boundary_checks/2; canonical SHA-256: cfa652ad3931918b78b2ffb747d3ecbeeb6761564e21a6006aa53dc4ff0236d7

Below Lρ, the opposing affine pair proves only nontriviality, not a main-rate lower bound.

#### Native item 4

Native pointer: /joint_analysis/comparisons/4/boundary_checks/3; canonical SHA-256: 5fc916f3e50b3633080bc27c8505f0858ed41b8774430ba949307e1b20265d04

2610.00345v1 K.3, characters 226890–233390, defines ε_Z≤1/√8.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 394db0f20e65821b7005ea06d8b181f49203a8099c7813485869fbd2308f0201

Not applicable: exact zero cost.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 7115dbfebb87564046d0b500c2c266ab04dbe48b4858433b80c8c832860d417f

No gap on Z; the positive-cost complement is only partly assessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: 23252e7742dbd410996bb7168ecfd1c6cf47c42a1684b4780eb4798a7d30e7a8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 1082cbb76f8debd246fcdcfed0732cf198b55ecf391158e982f13916af35c7d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: cd69e8b12870dcc54da99e7d0ffc382583b8555bec026fa93ff6c87f0520bc7e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: e257638519d726914b602049b368936d7d93d25b832566b30ce5f3249d4f3830

Zero calls supersede the positive upper estimate on Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: 21182f6ea2d30f63ba75be8eac7ad88fc5fa3ac1451958791520395d32001edf

All B,K; retained localization transfer.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: 45051cf9d52798170d29629174e7dbcd4d77bb6e61cd6e9e92cc642d441eb307

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: adaaa69e59c1ac18479a1efbf8ca9a789ba0fdcb5d1635f932e8b0d87b5273ba

Where applicable, its positive upper estimate is superseded by zero calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: 7d74c54a4a319b79aad075ca4d3383885253c0dbc6a872038f2f04f2620fc1d0

B=B_q, d≥3; known public ℓ_s prox.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: f4f48f1fadb8186c5697e06f14f8e91e9aac6700556342b72aa5afbcaeb5f8b7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 24f782a0eaa4342e459920613b87abf8fcfa06498fdc320ab5b79682b70be6b2

Zero calls supersede the positive upper estimate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: b570add08de74bfb54022ad8b247ed7ac022b9b77b048d7e3ac65d93e669afd7

All B,K; retained Euclidean two-point upper.

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: ffcd287a33eae98cdaf57b84703dd6f8462e7a8177b74a7863dbdd2a30d8232d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: 017663b113fafa50b91ab77f8715cca538f4d51e4db9586b71996af266560977

r_m≤ρ and ε_Z≤1/√8<1 make the source window disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: 151b249f2cc7209feccab45294547850bae556a6ace570d286ef3f57c5690835

m_0≤m≤d, r_m>0, ε≤ε_ZLr_m.

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: 8d54f234bb6e8ad31e1a8f66dfcedd88083f473e6c6bd1f9848a7127972d3112

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: 9fe99be676608ad94faf9b76e23aea9b81004d0b3091d88e50ce831dc6b47e4a

On matching ellipsoids Z has A_B≤1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 6

Native pointer: /joint_analysis/comparisons/5/bound_uses/5; canonical SHA-256: 5c5ea7273b28ad3b979a6e597da67933608b1e27d32c217912c3e25eec8660e3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/reason; canonical SHA-256: 9fe99be676608ad94faf9b76e23aea9b81004d0b3091d88e50ce831dc6b47e4a

On matching ellipsoids Z has A_B≤1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/5/validity_region; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 7

Native pointer: /joint_analysis/comparisons/5/bound_uses/6; canonical SHA-256: fee5f6d3dfc6756530117e14ca1717f1cff7f2efae278c25f5ebe12dab2f5ae3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/reason; canonical SHA-256: 5a40ed40497ce66d958c0bd86c0d57cc08f18b911dcf5e6c2d5af561855c5eb1

The deterministic center algorithm succeeds with probability one and uses zero calls.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/6/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 8

Native pointer: /joint_analysis/comparisons/5/bound_uses/7; canonical SHA-256: d0514e63bf044bdc28d1617719136a06970480e18681fc230443ac8b6c7c36e6

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/adopted_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/mapping_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/reason; canonical SHA-256: 7ff29e6c2a43d607760ee6513f8ddab014711494f9f30acab6e2874dfabbfd1d

The fixed-path call budget is nonnegative.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/7/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: 409d698c722ed6163dd8bb1d3b6e9a6a5f475581d20936c8f5069de1d8326338

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: 05216749f3146bd5c427d388889800e11b53cff47f5bc4729c630b5b568aa946

Equality ε=Lρ is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/boundary_checks/1; canonical SHA-256: dec1f1cd2bc3ac2992fb374fa1b75d86d0cde3842c8576df8d0d834918c31dd9

Singleton K has zero cost throughout ε>0.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/boundary_checks/2; canonical SHA-256: 363804c5e7a67631ced3b1b1a15f018bca3db3bd466d48f940108f0da38b2b47

For ρ>0 and ε<Lρ, a zero-call output law has success at most 1/2 on one of two opposing affine objectives, below the required 2/3.

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/boundary_checks/3; canonical SHA-256: 518fd025a9b331d894c2bd0433ddab072084fedc3a4f092c1c3bda7f717a6cd9

The positive lower-bound source windows are disjoint from Z.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: 394db0f20e65821b7005ea06d8b181f49203a8099c7813485869fbd2308f0201

Not applicable: exact zero cost.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 7115dbfebb87564046d0b500c2c266ab04dbe48b4858433b80c8c832860d417f

No gap on Z; the positive-cost complement is only partly assessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: de38ac07aef2e5f500cd72ed0ea743e0194634309cf7ef0871a9fa949225525f

0 exactly

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: 2dfcb28b1f792e52dfc6ef11915df7d055dd1f84cbecbb4b9be937cdf820aea4

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 7b4579c64ad1c8cac678bc35d94e6a90bd375141d7bfb5c6fde0e5f960c87e5a

#### Native field: fixed_parameter_refs

Native pointer: /joint_analysis/comparisons/6/slice/fixed_parameter_refs; canonical SHA-256: 5924b1bed993884a78c76017060b5caca195321a07803d1cd69dd6aca7795733

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/slice/fixed_parameter_refs/0; canonical SHA-256: 192dd0a06e4082deea0d7a782beaf459b583ad240f088aaa0f0fa6f79f52088f

SO_ZO_E06cL_p_b34cdb433a

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 5924b1bed993884a78c76017060b5caca195321a07803d1cd69dd6aca7795733

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/fixed_parameters/0; canonical SHA-256: 192dd0a06e4082deea0d7a782beaf459b583ad240f088aaa0f0fa6f79f52088f

SO_ZO_E06cL_p_b34cdb433a

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: 36a03a2dd75e7c2da9c608cec3396149b2182c13d763ad4ea10f9d9394de3ca5

O_c(d^2\log(ed))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 0bbd71e91f3a16d815da5af16c54677c15955584f3c382b9ed7e9c7a2735c719

\max\{\mathcal L_{\rm img},\Omega_c(d^2/\log^2(ed))\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 0fbee1fdba3000b7cb39a421698985b561223717c47ba4f40e1d0bb4ceea52cc

O_c(\log^3(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: ce9e8a2eb08963e31274ba372dab4096c4aab30e88dfdf0e37bd7115c5c17f22

Logarithmic gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: a9398c8a767cffad60ee6ca123cffbd0bd6f56a649df71f9c4fa0681816d41c6

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 1103818fefa0e38bd1c17d6291fd8a5771d554a6c2d89cb852385c899b841f69

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: c582a002e97a450044c982706300a21148a583d9c6eefa44f14910b9bf9a5419

$B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: 25962b0425a9bd3f01f79c6a0cb8fbbce79bba08c5bcae0f564bee3704ed6155

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Also $d\ge d_1^{(1)}$ and $\alpha_1=c/\sqrt d\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 81506bb94fe2f3bca9f2eac5b08891caf07431da175b2fcca98a86342c5d0831

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 5d3069258aca6ab5ab624907f0b90a8eca3edcdfa69a4f7550bd4f1ec920badb

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: 25962b0425a9bd3f01f79c6a0cb8fbbce79bba08c5bcae0f564bee3704ed6155

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Also $d\ge d_1^{(1)}$ and $\alpha_1=c/\sqrt d\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: ee109c6c32fed38a67bf3595798a3de11c1160f8b042738942161138eac0bd6c

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: 25962b0425a9bd3f01f79c6a0cb8fbbce79bba08c5bcae0f564bee3704ed6155

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Also $d\ge d_1^{(1)}$ and $\alpha_1=c/\sqrt d\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: 7180c041a8e37eed9f800b2d42d740666ac3232bcb082cad3d6b7c7205520f59

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 927de04778e5034294e17889f81571b78b805189703593dac798632f5fc22a4f

SO_ZO_E06cL__kimi001_20261124__rand_joint_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: 25962b0425a9bd3f01f79c6a0cb8fbbce79bba08c5bcae0f564bee3704ed6155

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Also $d\ge d_1^{(1)}$ and $\alpha_1=c/\sqrt d\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: d94c8b816c72abe07da0b57b46a2e897f580dc11131a65d77e46ffcf100bddfd

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 7b4579c64ad1c8cac678bc35d94e6a90bd375141d7bfb5c6fde0e5f960c87e5a

#### Native field: fixed_parameter_refs

Native pointer: /joint_analysis/comparisons/7/slice/fixed_parameter_refs; canonical SHA-256: 5924b1bed993884a78c76017060b5caca195321a07803d1cd69dd6aca7795733

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/slice/fixed_parameter_refs/0; canonical SHA-256: 192dd0a06e4082deea0d7a782beaf459b583ad240f088aaa0f0fa6f79f52088f

SO_ZO_E06cL_p_b34cdb433a

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: 5924b1bed993884a78c76017060b5caca195321a07803d1cd69dd6aca7795733

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/fixed_parameters/0; canonical SHA-256: 192dd0a06e4082deea0d7a782beaf459b583ad240f088aaa0f0fa6f79f52088f

SO_ZO_E06cL_p_b34cdb433a

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: 36a03a2dd75e7c2da9c608cec3396149b2182c13d763ad4ea10f9d9394de3ca5

O_c(d^2\log(ed))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 428c2d23f7021e8d7cc2458ce4886a8d4536de8ae768aed51f365ae6f2c04d72

\Omega_c(d)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: e5579735eb448375b357e7361c51133666e68297f5cb11df37cd0d0dd6ac0b42

O_c(d\log(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: 17df2b3f1844e61e3d77e03c4c1d0cf092514940a375bad63d813a86b4d5a419

Other quantified gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: d2368deadbf7713b472a7cf1d7f3378334aef8e9d0c7aa05fac17ffd96e6bbad

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: af045f200826f02126401c0b68dc385fcca068da7df9c61440264257592e3fcd

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: c582a002e97a450044c982706300a21148a583d9c6eefa44f14910b9bf9a5419

$B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: 6b891265365fe0a30d5fc9c359a77a7f9cad212427bcf73c6260f0fd829a36d1

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Outside the joint-theorem domain: $d<d_1^{(1)}$ or $\alpha_1=c/\sqrt d>c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: cded1e601dad2e66928fcad1241095f5f4db0aa65cd6d1ef87d0cb573d349542

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: 6b891265365fe0a30d5fc9c359a77a7f9cad212427bcf73c6260f0fd829a36d1

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Outside the joint-theorem domain: $d<d_1^{(1)}$ or $\alpha_1=c/\sqrt d>c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/7/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native item 9

Native pointer: /joint_analysis/comparisons/8; canonical SHA-256: e6f6309c0ff3fc2bea82abf3cb1dd8b359f4436dad79f147a306ca6607843cad

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/8/comparison_id; canonical SHA-256: 58575a18baa8bb7e0b89cc90b11afc8b5bfb5e976af112df243b056ad22ce76d

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/8/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/8/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/8/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/8/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/8/upper_envelope; canonical SHA-256: 98281732b6c573907ac0f963cb5c9f1c4649c8069213f2fbf7a5321715026e7b

O\!\left(\min\{dA_1^2\log(ed),d^2\log(d+1)\log(4A_1)\}\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/8/lower_envelope; canonical SHA-256: 796b8d4c35c9e0a47b3f3508fea7e641563e7776a863a0b7ef10b00f68e45df5

\max\left\{\mathcal L_{\rm img},\Omega\!\left(\frac{dA_1^2}{\log(ed)\log(eA_1^2)}\right)\right\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/8/gap; canonical SHA-256: 9e34e85a1599db47a94f811563951b37684d4b9b4bb7ad585550dc4a06c5708b

O(\log^2(ed)\log(eA_1^2))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/8/remaining_gap; canonical SHA-256: ce9e8a2eb08963e31274ba372dab4096c4aab30e88dfdf0e37bd7115c5c17f22

Logarithmic gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/8/bound_uses; canonical SHA-256: bbf5ff7ab86f4596fa2ba5bc6b61f236a69bb61347353e23469bd3f1cf96357b

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/0; canonical SHA-256: 75a6bb9ce671194c820ce4da9accad5f07226bd5d4417254b7a41db11e3b3180

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/bound_id; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/validity_region; canonical SHA-256: 5d3069258aca6ab5ab624907f0b90a8eca3edcdfa69a4f7550bd4f1ec920badb

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/adopted_region; canonical SHA-256: 1eeb289cfd5ec4ad1b4bf89c082bdee62a50a52031f21a183435781d7b80958d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/bound_uses/1; canonical SHA-256: a964e1eb8839ef1baf58c8e922efde50e9d9d0123a19d46a185cee0c1391ffd3

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/bound_id; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/adopted_region; canonical SHA-256: 1eeb289cfd5ec4ad1b4bf89c082bdee62a50a52031f21a183435781d7b80958d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/bound_uses/2; canonical SHA-256: d4ddf787952751bc44f7214433afdf06699aa8abfe507cf4f33786cfa8f3259f

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/validity_region; canonical SHA-256: c582a002e97a450044c982706300a21148a583d9c6eefa44f14910b9bf9a5419

$B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/adopted_region; canonical SHA-256: 1eeb289cfd5ec4ad1b4bf89c082bdee62a50a52031f21a183435781d7b80958d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native item 4

Native pointer: /joint_analysis/comparisons/8/bound_uses/3; canonical SHA-256: 938b04dadb80196d72011a3d169d664c2e2df55d42b386a82486b96f40a13f23

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/adopted_region; canonical SHA-256: 1eeb289cfd5ec4ad1b4bf89c082bdee62a50a52031f21a183435781d7b80958d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native item 5

Native pointer: /joint_analysis/comparisons/8/bound_uses/4; canonical SHA-256: b00ab28492b393e5469bc85d43389c8a7522b64000785f17ca58cac86bbdf602

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/bound_id; canonical SHA-256: e5f1138a0999967d98b33bc0462d246bc2e3b7e35ad69972c97d0d4cbfcc52bc

SO_ZO_E06cL__kimi001_20261124__rand_regional_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/validity_region; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/adopted_region; canonical SHA-256: 1eeb289cfd5ec4ad1b4bf89c082bdee62a50a52031f21a183435781d7b80958d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/8/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/8/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native item 10

Native pointer: /joint_analysis/comparisons/9; canonical SHA-256: 60ee6d022d3de961788200514687206ce2eb38d8c740197ec341e2277a58527e

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/9/comparison_id; canonical SHA-256: 87351f4d697ec66c57b348213040afa9701f9eeaa5e228320edc9c1997951fea

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/9/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/9/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/9/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/9/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/9/upper_envelope; canonical SHA-256: 98281732b6c573907ac0f963cb5c9f1c4649c8069213f2fbf7a5321715026e7b

O\!\left(\min\{dA_1^2\log(ed),d^2\log(d+1)\log(4A_1)\}\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/9/lower_envelope; canonical SHA-256: 572112eb8ecbc5832450dab559497b5ea5a6f409ce732ba26ae490d2d0151029

\max\{\mathcal L_{\rm img},d/(16384\log(ed))\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/9/gap; canonical SHA-256: b4c375970c35449e7533595f3def6903c7c6450a231b020a46b343992b72c69c

O(A_1^2\log^2(ed))\le O(\log^3(ed))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/9/remaining_gap; canonical SHA-256: ce9e8a2eb08963e31274ba372dab4096c4aab30e88dfdf0e37bd7115c5c17f22

Logarithmic gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/9/bound_uses; canonical SHA-256: 2a8a04be00a68e2e8623f8dc7cdbb460accdf8c640533a57bf920d153e50492a

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/0; canonical SHA-256: b5ec031e8567daaa6e9e78a67d41002c68353a7ea14338daacc9260b5d7c8689

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/bound_id; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/validity_region; canonical SHA-256: 5d3069258aca6ab5ab624907f0b90a8eca3edcdfa69a4f7550bd4f1ec920badb

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/adopted_region; canonical SHA-256: 4c27f283d7d429ee6f2b585d7d0a7f859e4dea9510583a65a4779d402d06903c

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/bound_uses/1; canonical SHA-256: 5813e674420203e837cfa1269556f88192b7fdad8afff961cfc836e61ac8a2f6

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/bound_id; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/adopted_region; canonical SHA-256: 4c27f283d7d429ee6f2b585d7d0a7f859e4dea9510583a65a4779d402d06903c

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/bound_uses/2; canonical SHA-256: 61bdf36a15569f91393fc7804cc8f1c6392cf65ee57b6f04f5e49ddcb81b4d9b

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/validity_region; canonical SHA-256: c582a002e97a450044c982706300a21148a583d9c6eefa44f14910b9bf9a5419

$B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/adopted_region; canonical SHA-256: 4c27f283d7d429ee6f2b585d7d0a7f859e4dea9510583a65a4779d402d06903c

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native item 4

Native pointer: /joint_analysis/comparisons/9/bound_uses/3; canonical SHA-256: 0f4bf91d57a98c440fde341754593bbfdc4fc0dfc9853d85e21886a4b7176c4a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/adopted_region; canonical SHA-256: 4c27f283d7d429ee6f2b585d7d0a7f859e4dea9510583a65a4779d402d06903c

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native item 5

Native pointer: /joint_analysis/comparisons/9/bound_uses/4; canonical SHA-256: abea9541a641075f7e36c76e425ba519caccd8c021e011eaa91bdecd8e0c8c29

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/bound_id; canonical SHA-256: de837cab36cfe8cf2a8d74bf11f21980fc6858ad83846ae9d7bcb44b3c006b35

SO_ZO_E06cL__kimi001_20261124__rand_spike_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/adopted_region; canonical SHA-256: 4c27f283d7d429ee6f2b585d7d0a7f859e4dea9510583a65a4779d402d06903c

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/9/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/9/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/9/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native item 11

Native pointer: /joint_analysis/comparisons/10; canonical SHA-256: da08c02edf3aed8931574aee7549b2e77a5f43a0d40d743ac3533e46427443fc

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/10/comparison_id; canonical SHA-256: 7de0d0f1333f3f6d078f560a80b1fea057c1e834dcee16e848e7ea94eb72c791

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/10/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/10/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/10/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/10/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/10/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/10/upper_envelope; canonical SHA-256: 98281732b6c573907ac0f963cb5c9f1c4649c8069213f2fbf7a5321715026e7b

O\!\left(\min\{dA_1^2\log(ed),d^2\log(d+1)\log(4A_1)\}\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/10/lower_envelope; canonical SHA-256: cfae28c76eea73c1d99267cb93804d9c9d4698054bf70483fe2b6c9112b534f2

\max\{\mathcal L_{\rm img},\Omega(d^2/\log^2(ed))\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/10/gap; canonical SHA-256: 5276f7afb4367ff2f2128061cf6a99699db5d5fb8225fc90661f5ca96aed2cd8

O(\log^3(ed)\log(4A_1))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/10/remaining_gap; canonical SHA-256: ce9e8a2eb08963e31274ba372dab4096c4aab30e88dfdf0e37bd7115c5c17f22

Logarithmic gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/10/bound_uses; canonical SHA-256: 1f9f42bdea181a016228d278836149759d06065287e90a2215f13d6038d77ebe

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/0; canonical SHA-256: b35c110d44c1dd2e647df96de9e575aa3a9fe0d4ea701c7acbaf13ab761f9461

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/bound_id; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/validity_region; canonical SHA-256: 5d3069258aca6ab5ab624907f0b90a8eca3edcdfa69a4f7550bd4f1ec920badb

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/bound_uses/1; canonical SHA-256: ff7b0ca7105654fd7827849df85cb1cae218777ca652bd2f7af36621d016cf7c

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/bound_id; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 3

Native pointer: /joint_analysis/comparisons/10/bound_uses/2; canonical SHA-256: 54f12ea968ecf94b5b0486683c2ee1f751ab5ef7c64a7e3cb9e4b891bdc44824

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/validity_region; canonical SHA-256: c582a002e97a450044c982706300a21148a583d9c6eefa44f14910b9bf9a5419

$B=B_q$ and $d\ge3$. The auxiliary prox function is 1-strongly convex in the $\ell _s$ norm, with known range $\Theta_s$. The index s is chosen by the algorithm and need not equal q.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/mapping_proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native item 4

Native pointer: /joint_analysis/comparisons/10/bound_uses/3; canonical SHA-256: 72d5ae0d1c343fe0465ced7c69132a03a31f8e7cdee3d7b33e0ac73d87d99cd4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native item 5

Native pointer: /joint_analysis/comparisons/10/bound_uses/4; canonical SHA-256: 92b8a2f838fcbe7232ff3fa86c6f471a1e9aafb2529d0434a60f8f8fd65c8d12

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/bound_id; canonical SHA-256: e5f1138a0999967d98b33bc0462d246bc2e3b7e35ad69972c97d0d4cbfcc52bc

SO_ZO_E06cL__kimi001_20261124__rand_regional_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/validity_region; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/10/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/10/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/10/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native item 12

Native pointer: /joint_analysis/comparisons/11; canonical SHA-256: 6f7d19f707a6eeaf1bdfab09c8ca4f82fdaf74de8db10cb83dc77676346d2f86

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/11/comparison_id; canonical SHA-256: 96fee94beab4740b775925d6f467799a17f0164c697a48b7d93927ef6567150d

SO_ZO_E06cL__kimi001_20261124__det_coarse__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/11/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/11/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/11/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/11/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/11/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/11/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/11/upper_envelope; canonical SHA-256: 44707b69f3af1a968ff074dea03ea6b77a4948f40608ff175022d5a72e5a9c36

O(d^2\log(d+1)\log(4A_1))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/11/lower_envelope; canonical SHA-256: 7d702ce574c49744e62d3bd242231484bb98f46947fcac280ffeb308c90277b3

\max\{\mathcal L_{\rm img},\Omega(dA_1^2/\Lambda_1^2)\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/11/gap; canonical SHA-256: 66a40455443cbe47c5c9254af76774f2843e40069ff56414e8670f519ff000b0

O\!\left(\frac{d}{A_1^2}\log(d+1)\log(4A_1)\Lambda_1^2\right)

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/11/remaining_gap; canonical SHA-256: 97ba2f17a3b1ca0774b6da6554c515f3aa58c4e51d5967ccd6011e87542ff141

Polynomial gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/11/bound_uses; canonical SHA-256: b23754a81e3b383d37f0762529cb30f01aa52ab1966ebd3a188f7edbaf19fa77

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/0; canonical SHA-256: fd27b48b5fb9da7da2d92b602689cc26487f5079956b83e138bffe79115b3526

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/bound_id; canonical SHA-256: dfe217b8ce51c20ef77e003371d9b4f11b72fdc09a9e930f4cce315b0055a1ca

SO_ZO_E06cL__kimi001_20261124__det_body_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/adopted_region; canonical SHA-256: e0042ae5b59c8d7130834c80759395a24fb20586fa40809603625cc22dbe2d3d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 2

Native pointer: /joint_analysis/comparisons/11/bound_uses/1; canonical SHA-256: c8f5b7e6dc9500b985b3d288d46f3f4f07b8b0363f86992884a16aed5ddecaf1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/adopted_region; canonical SHA-256: e0042ae5b59c8d7130834c80759395a24fb20586fa40809603625cc22dbe2d3d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native item 3

Native pointer: /joint_analysis/comparisons/11/bound_uses/2; canonical SHA-256: 841a3d199ff5b317d8d3a050123d9d236620d5c86b20e63bcc517c6ba6d3f63d

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/bound_id; canonical SHA-256: a26f8b529b40e7120dd294e5e025d7866e408227ee65efba01933f41e0c30c4a

SO_ZO_E06cL__kimi001_20261124__det_joint_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/adopted_region; canonical SHA-256: e0042ae5b59c8d7130834c80759395a24fb20586fa40809603625cc22dbe2d3d

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le c_0^{(1)}$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/11/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/11/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/11/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/11/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native item 13

Native pointer: /joint_analysis/comparisons/12; canonical SHA-256: 1b8f7d7c2cf2560539c84b9d59a411ce93850ab18aef65b4d825b4dd038c3824

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/12/comparison_id; canonical SHA-256: f1d3e287a12fecdc7cc868341d491466d5f87c194950ca698c4cc94c94cebcc3

SO_ZO_E06cL__kimi001_20261124__det_plateau__c

#### Native field: role

Native pointer: /joint_analysis/comparisons/12/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/12/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/12/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/12/constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/comparisons/12/constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/comparisons/12/constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/12/upper_envelope; canonical SHA-256: 44707b69f3af1a968ff074dea03ea6b77a4948f40608ff175022d5a72e5a9c36

O(d^2\log(d+1)\log(4A_1))

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/12/lower_envelope; canonical SHA-256: cfae28c76eea73c1d99267cb93804d9c9d4698054bf70483fe2b6c9112b534f2

\max\{\mathcal L_{\rm img},\Omega(d^2/\log^2(ed))\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/12/gap; canonical SHA-256: 5276f7afb4367ff2f2128061cf6a99699db5d5fb8225fc90661f5ca96aed2cd8

O(\log^3(ed)\log(4A_1))

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/12/remaining_gap; canonical SHA-256: ce9e8a2eb08963e31274ba372dab4096c4aab30e88dfdf0e37bd7115c5c17f22

Logarithmic gap

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/12/bound_uses; canonical SHA-256: 4319c00f53db0a1f4595a0d629e6480b19670b66e97df82b0bf1a2ec38020917

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/bound_uses/0; canonical SHA-256: ebcd379dd6627fdfb5d35de038a8bd9bcace6e070a5628c632cea438d84fc018

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/bound_id; canonical SHA-256: dfe217b8ce51c20ef77e003371d9b4f11b72fdc09a9e930f4cce315b0055a1ca

SO_ZO_E06cL__kimi001_20261124__det_body_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 2

Native pointer: /joint_analysis/comparisons/12/bound_uses/1; canonical SHA-256: 34ecaf88df120c37071de3fec5574d15f21ee4dc4eef3c7e0f9d57ae40e6e8ca

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/validity_region; canonical SHA-256: d02ca0166b361e874c0b52affc8b9b42121776caea88eb1116ae56ea16a2f84f

Arbitrary randomized adaptive algorithms. Retain the source's universal constant $m_0,\varepsilon_Z,c_Z$; take the maximum only over integers m in the displayed window.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/mapping_proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native item 3

Native pointer: /joint_analysis/comparisons/12/bound_uses/2; canonical SHA-256: 56a77a8752eebd12acc91c57195b145c0122438c11a4b9efbb1e6a40d511be53

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/bound_id; canonical SHA-256: e9f655f0f146dde6794e09684fc8e89116b5fd8589de02402e10f9de84688500

SO_ZO_E06cL__kimi001_20261124__det_regional_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/validity_region; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/adopted_region; canonical SHA-256: e772033d2cc3767a978ca3db0da14316b28d4a2ea04104758cf7375657cde5d3

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$.

#### Native field: reason

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/reason; canonical SHA-256: f887dea5a93fab42a6108a590f571c33ffb66a3dd2d7994afe166ca113a5863f

Applicable under the displayed source guard; take the minimum of attainable upper bounds and maximum of necessary lower bounds.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/mapping_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/12/boundary_checks; canonical SHA-256: 5138fc733aef1df5f35fd44d5ea531a00a1b7d607630ce84d2cd0e9a5307481a

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/boundary_checks/0; canonical SHA-256: ecee5a117c808becd2c36666df733854b784b464848b2454501df87420cd4f82

The full-space scalar oracle and feasible arbitrary output are fixed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/12/boundary_checks/1; canonical SHA-256: eae85b742d9280462ade337445b1e319d85e47c226f70d2806791862e02757da

The lower theorem retains its sufficient dimension threshold and fixed small-accuracy endpoint.

#### Native item 3

Native pointer: /joint_analysis/comparisons/12/boundary_checks/2; canonical SHA-256: 7d895820d8fe4139dc13b925d491fa5b01325fd6d76d73d16b8033b776ebaa16

Randomized upper witnesses remain in the randomized view.

#### Native item 4

Native pointer: /joint_analysis/comparisons/12/boundary_checks/3; canonical SHA-256: 603f1b047512a46cf204b8298ed1d685d943b4b668930d87bf1d0c5564c853fe

Existing applicable image lower bounds remain inside the lower maximum.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: f2f011fce3d908055bace7338e5bfec4cfbc0d45d2eea980a6ff740cd2fe4fd7

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 3e47152ec28e5f96fdd90d6a137e771ac4045b527988e6cf069977d7de3b0982

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 761df97af49117b7076f1fe7f5aec73b93c2da679ca26e4fed90383f12b846ba

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: c217c43a05e328dc38c22e59f500245b6cbe31264f74aa596d751b40023d9b97

zero-endpoint

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: a8ea6921a245a2ba99dcb8aaf7b5ec5181288ea28c8116e82c7bc676962c4621

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/1; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 37e061736cb711c56f86110470f69a030f8f78f34b97452744ad194f614214b1

Exact zero cost; the two view/quantity fibers remain separate.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 87be437e4d8e8c0a1668b6bba3e31184088f9902c713c2c222340799a43b50fb

Z, separately in each registered q1 view.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 67aa351cb6ee3fa2944866ced1a931f558f0daa8ac3a5d4bfdbd232a5034ad0e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 377e1cefae4f2a57400e1e013212249579ea89d84470f98731d63804f804fa72

retained-det-c1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: e04b768e78dceb8a470bf05e02937c00e17c02051e2b8c10ed9d555ac0d84084

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: e4b5647d8b226a162d649c5b351ac040bd3eda77bfdef669c357cbab65d4b97f

Native bracket retained conditionally.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 6990e89d8c093f7986797756a43a911717997791b51e50dce2c3deeec81d514b

Deterministic q1; B=B_∞(0,1), K=B_∞(0,R), d≥d_0, 0<ε≤c_1LR/√d; retain source guards; subtract Z.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 85fc7782cc82c3c1879e956c6ab1feda7c7e09d32c932dd1fb14e3732c778411

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: dff74ce4a99746c0d996eb5bec6017789adacd61cba78f22be07487f29cb5a73

retained-rand-c1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 5595ae958132d137164fe0cd5dbaddaa271f923224a5dc609ae105638d0c4211

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: c2cc0736f6b07a4d6564270d845c03d0f802e9b30d79d8ae4f2fe17472012f8a

Source activation and envelope crossover are distinct.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 64cbb3af92873bb41861963d60e137ef70f6950a308cb3b67e0234c46d53f18c

Randomized q1; matching ellipsoid, d≥d_0, A_B≥C; retain source guards; subtract Z.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: d7b992fe01684652f8079a4f233068c552e23ad9ed51a4e9d6644d98e3b22516

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 81aa456a4ac522f15963d0ee465603e7c84f16fcd3b63200eb8a82e3f799e6eb

retained-rand-c4

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: ac42228087c861bf7b8a9ed6f028f9874a3c97d9a009b65404d66c5adc2e75f0

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: e4b5647d8b226a162d649c5b351ac040bd3eda77bfdef669c357cbab65d4b97f

Native bracket retained conditionally.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 8f98904511cbfc6f1d7ccaa061add35bfbea20228d911904e4bccb07a967126c

Randomized q1; B=B_∞(0,1), K=B_∞(0,R), d≥d_0, 0<ε≤c_1LR/√d; retain source guards; subtract earlier same-view cells.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: a16e7e87c0d45df2466fbfebb7f4fe4c1f00e5731551a6b6f4bf75fa49e2db01

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 779f7b929b03c068a8ebe645ebda94097462b70a9e0a8098cf4df74e5036ea11

retained-rand-c3

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 17bda35342cb4ec62b598f61baae03ca9e75c52625b72b95969167cf743ec255

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 85f3c11330650936bbda0b93cec140b933992c10d43843744f7f9de8a86f37c7

Secondary fixed-c slice; its original comparison remains available on overlaps.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: e0611d8e0a7094928b283c55458ed807e44b5294b8761d4c334e34119d034431

Randomized q1; B=B_∞(0,1), K=B_∞(0,R), fixed 0<c≤c_*, ε=cLR, d≥d_0; retain source guards; subtract earlier same-view cells.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 249ee469e990a00721fd50dd8fed57afe5a0b8070057dff2af294d06197b9173

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: 5e5745f9f19cd8cf3090b6c3ae51e59f644d8027c76e3d8f9cd4c3cdda24ae61

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: ac28f5f2259643c5b9cd05b7ac8e3a7a742471551cb416ffe3ecc60224475b77

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: 0d0c3c9057649cc6ae744f6a4ac23abfcb13edf6a1ba32e4033e42bb01b53f26

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Also $d\ge d_1^{(1)}$ and $\alpha_1=c/\sqrt d\le c_0^{(1)}$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: 323f87b56c3ca881a15768d5c15fc44779fc3ba2a3a2ec83f400ac6dbb8d862e

near_optimal

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: 0a5cb8d6bafb8ebbd29615702791557ef22e319b270aa65e0a070df376dab3c6

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 510a80386e7411ddb956e998f19cde94e6517ac59d13ca51ffe58d9c28192799

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: edabe0eae9707f759db8ae735ebc5c3a6958cfe47b358f823235cf2492f9418a

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: eca18de33e18f5c6f1003d0762c7d30c45b3721d0dc716e587bec61b3f7e66a4

$B=B_1(0,1)$ and $K=B_1(0,R)$; fix $0<c\le\varepsilon_Z$, with $\varepsilon=cLR/\sqrt d$ and $d\ge\max\{3,m_0\}$. Outside the joint-theorem domain: $d<d_1^{(1)}$ or $\alpha_1=c/\sqrt d>c_0^{(1)}$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 76d65c66ecee5e5adc4ce6c31085e0c483b11152f565cef9578183f452083fb1

slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: 1a98a380dbc468a41643b4ca35f755ecec6587cf86c2c7f15fc79c3ace7e21d9

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: f205425701a5acaa05bc6e0992f181c88224e636cd1c1a56069f188d37da6032

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: a69bcfe83b40f83cc000b55f2bcbce69dc821a08b544fb382990623a51a167f9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: 58575a18baa8bb7e0b89cc90b11afc8b5bfb5e976af112df243b056ad22ce76d

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: d4091fdab6a3bead479f25864ea4a8e36c2a389cce20af4cd4163e78af559a9c

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le\tau_d$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: 323f87b56c3ca881a15768d5c15fc44779fc3ba2a3a2ec83f400ac6dbb8d862e

near_optimal

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 9

Native pointer: /joint_analysis/domain_map/cells/8; canonical SHA-256: 33b85238af377c364dd8304bedfc235999d771df804075a8a8e207fb89eb9bf9

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/8/cell_id; canonical SHA-256: 3e285bca2f520f18515ad67ec7272c1e2a6ef2468676d6e32b597c8e0df81c5b

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids; canonical SHA-256: 8adc9bb1b250674511b0e5c1f1ad7b5e810bae67be6dfd21326005ff07eab74d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids/0; canonical SHA-256: 87351f4d697ec66c57b348213040afa9701f9eeaa5e228320edc9c1997951fea

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/8/predicate; canonical SHA-256: d53d4aee620c4b5a511eda428c79ad9d4e08b8e9f7ede2ddd70c86bd73740a96

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\tau_d<\alpha_1\le c_0^{(1)}$; hence $A_1^2<\log(ed)/c_\diamond^2$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/8/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/8/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/8/closure; canonical SHA-256: 323f87b56c3ca881a15768d5c15fc44779fc3ba2a3a2ec83f400ac6dbb8d862e

near_optimal

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/8/closure_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/8/closure_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/8/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/8/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 10

Native pointer: /joint_analysis/domain_map/cells/9; canonical SHA-256: 43a798c94b5699099bf314aea5e595c1f0916c2d5fa8a1b8fc3925cb654b6372

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/9/cell_id; canonical SHA-256: 18de03dedac4b234d033446ce0ff178e0d524f00356f636319141a6b4d87bd0a

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids; canonical SHA-256: 3e5644f562d10161b892c01c13f270811760276f40ee405952ec657b2bce4ad3

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids/0; canonical SHA-256: 7de0d0f1333f3f6d078f560a80b1fea057c1e834dcee16e848e7ea94eb72c791

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/9/predicate; canonical SHA-256: 0b4cadbd6554fad47bec176b32e6c6bc8d94d74df36ee4b49f3a080335f99ece

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/9/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/9/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/9/closure; canonical SHA-256: 323f87b56c3ca881a15768d5c15fc44779fc3ba2a3a2ec83f400ac6dbb8d862e

near_optimal

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/9/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/9/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 11

Native pointer: /joint_analysis/domain_map/cells/10; canonical SHA-256: 3783f169c9a911ec3f78f2690dce867e96a6c242ce8af279ba4650d0d72f01f8

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/10/cell_id; canonical SHA-256: 5eb20159bb09b2b0a17ccb67f0ef66ea6867013a180b208a1144144eac32abee

SO_ZO_E06cL__kimi001_20261124__det_coarse__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/10/comparison_ids; canonical SHA-256: 46acd4abd51d28c4e8c44fa10e712e6302e37b52cef721af10d6f55c0665674f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/10/comparison_ids/0; canonical SHA-256: 96fee94beab4740b775925d6f467799a17f0164c697a48b7d93927ef6567150d

SO_ZO_E06cL__kimi001_20261124__det_coarse__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/10/predicate; canonical SHA-256: 60c9e849b3cdd3452411dd4c1cd1b198ad37972fd4354c2ed13e9ecda0905058

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $d^{-1/2}<\alpha_1\le c_0^{(1)}$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/10/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/10/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/10/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/10/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/10/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/10/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 12

Native pointer: /joint_analysis/domain_map/cells/11; canonical SHA-256: 1f70d7c00d8eb700407616f9e540b6bd5709c61d0c54341a5ba31f1362456ad4

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/11/cell_id; canonical SHA-256: c8e0d98beacc57a6635a6ad44deac5818d8652fc2310c0fa0d40a8c4b43578e8

SO_ZO_E06cL__kimi001_20261124__det_plateau__c__cell

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/11/comparison_ids; canonical SHA-256: 6203d90f4d5cc72c272f30a461169fb53cd7096f9c1fce176b1fbaa3263627c9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/11/comparison_ids/0; canonical SHA-256: f1d3e287a12fecdc7cc868341d491466d5f87c194950ca698c4cc94c94cebcc3

SO_ZO_E06cL__kimi001_20261124__det_plateau__c

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/11/predicate; canonical SHA-256: 0b4cadbd6554fad47bec176b32e6c6bc8d94d74df36ee4b49f3a080335f99ece

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $0<\alpha_1\le d^{-1/2}\le\tau_d$. Subtract preceding cells in the same view and quantity fiber.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/11/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/11/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/11/closure; canonical SHA-256: 323f87b56c3ca881a15768d5c15fc44779fc3ba2a3a2ec83f400ac6dbb8d862e

near_optimal

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/11/closure_proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/11/closure_proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/11/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/11/note; canonical SHA-256: c1b097cd8c0a334797e3881e937100c06324cdd6c0841677268613ca6c50537f

Constants may depend on fixed c on benchmark slices; joint regions track dimension and normalized accuracy.

#### Native item 13

Native pointer: /joint_analysis/domain_map/cells/12; canonical SHA-256: 88c7935500f5f2fb0ff1f62cb601a25025985dae7581337ed84781c5cfe96c35

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/12/cell_id; canonical SHA-256: 394e431a775aa5d3b64866a7227fc91b622fd686eadf02007931f06dab50bd9a

unassessed-complement

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/12/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/12/predicate; canonical SHA-256: 6e8f75e2ffcfb7ebf86df42131ac31dbae94944a783cd1a932e99b9f9ea1ac14

The primary q1 target outside all preceding cells.

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/12/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/12/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/12/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/12/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/12/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/12/note; canonical SHA-256: b169248a3d96fb057a406e2cb218f6c505dfeaec4084e5b926e5c2c073191000

Contains other geometries and parameters outside the registered source windows.

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 4df8084fa1e705cf5d8d7d0d22b606edeed2ef4e4c49e2eb64b745202ff4497e

Split by view and q1 quantity. Assign the listed cells successively after subtracting preceding cells in the same fiber, then take the complement. This priority construction is disjoint and exhaustive without extending any native theorem guard. Benchmark rows remain available as separately identified slices on overlaps.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: f585170ad9d926957272e4d1e057307457675a35c6513995ac45a2675acb1fa9

Exactly the unassessed-complement cell. The separately stored q2 quantity is not transferred into this synthesis.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 97eb102941ed898a1195adc8c1ae574d9c98e980175e4bdec3cbab8abde75fd1

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 71f121310a06ed659d9718a8209c18b5b0a6a998afede26badf8037e0a39fd82

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 2bce5cfe27ed84cb82ffc4e83e66933aab95792442a2504e67ced02746de6d3e

The center gap is at most Lρ; query costs are nonnegative. Opposing affine objectives establish failure of zero queries below Lρ for success 2/3. This closes an endpoint, not the positive-cost main rate.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: a8ea6921a245a2ba99dcb8aaf7b5ec5181288ea28c8116e82c7bc676962c4621

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 67aea45085b728d392fd02a44d0e8ac51236dc036f43d1ef99b656827913908a

endpoint-zero

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 997c6c502f9b389426a249678915bd05c3ea57dbd90e6a213c0fd54349abf72a

Z: a missing exact endpoint bracket is filled.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: cf73dd6ab0b5872b058e942b0d6a9120ef1d8127aef6334cb4fdebbc5fc37737

C*det=C*rand=0 on Z.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 7ce3fcc1b1adcfc78ad3877dfced2944d55ba292048491acf63822aa5c60b671

No registered endpoint comparison; generic retained upper estimates are positive.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 48728d15d603110d21bdd8bd3a42aed07f2e6acb3e842b1b510766c86851c096

All five pre-existing brackets and every point outside Z.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 6de3d23b72ab0c41335ffbbc0a7b22e671b032986c5a759585cc088fe64239c9

For any ρ>0 take ε=Lρ and return c_K without querying. For ρ=0 return the sole feasible point.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: bd95f20b20c00c7fe254fa26ce2fe13c36aa6b6a46f2ccb32032dc31bbd80dda

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: d74c561910718775b35f999dc9969bff25400d7f5ee65eb5bf8bf172b91484dd

The read versions predate cutoff and reproduce retained evidence. The smooth-only quadratic route needs a further globally Lipschitz reduction and is not adopted.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/1/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/impact/1/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/impact/1/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 584ffb4babd6ea3c218549b6e73c4f766b1e75124d2256809618a6e1350ae311

named-route-check

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 740677a4a07032324273908b90af97aac47d471991d5a56747e12df2e5271cc2

Same main-rate lower envelope; its source activation constants are explicit in the candidate audit.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 9fd9ad2aad01e3ac9533cb841ef4a888ccf3047b4a7cf4e7fb909fbf7c5ef6d3

Retained recent nonsmooth lower envelope.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: f2c0c32145d8ee88ae7b213fede7e5b07d200864183871c007c155ac33986968

All retained main-rate brackets.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 3f5e8d1b75bbb78bdf5e1235d49b0e1c8547a38b2b5c3c38ff629f173a4d260a

2610.00345v1 Theorem 3.3/K.3 windows and the 2607.16558v2 Theorem 5 input.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 56dc80394eeee51dd8a549f9256be11e269394d02f28c7814be179046a524f44

K.3 defines ε_Z=√(a_Z/2), a_Z≤1/4; Theorem 3.3 at λ=0 reproduces the stored image-radius lower bound.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 8496dbb2081aeb81013efc4a9cf6a35aa2d7018c0bdc23241e8e43eee89e7ddf

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/2/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/2/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/2/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/impact/2/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/impact/2/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 4400ec8a3b9113373ed0200553bd60fe06a5de3b35d1673dd1e7e01b5ade2e46

curated_feedback_SO_ZO_E06cL_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 8ac3b850aefa1115a150e653472c5f992cf22de042ffec1212c0c25096dc1d16

For each registered deterministic/randomized g1 q1 quantity: d∈N, d≥1; known compact centrally symmetric convex B with nonempty interior; known nonempty compact convex K; L>0, ε>0; globally convex L-Lipschitz objectives on R^d; unrestricted exact scalar queries, output in K, and the registered fixed-path budget. Geometry varies jointly and its dependence remains explicit. Native p,q,R are conditional ball coordinates. The historical R metadata about a global minimizer cannot override the fixed constrained contract; the new endpoint uses derived ρ. Deterministic q2 remains separate and untransferred. Write Z for K=c_K+ρB, ρ≥0, ε≥Lρ within this domain.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 2b3a2803badd9459caa71d1be80c9f6039f7526e6483566987238a415f0cd5bd

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 7ac9866301b2a5a6fa31e55e6c6015a53bfd139945ab925b04cf770d47a023b4

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: 417540c374c7a5ea02abc2b156a7e13501e25a28289d352f38a8ed5bd7098a6d

SO_ZO_E06cL__randomized__c2

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 5

Native pointer: /joint_analysis/impact/3/comparison_ids/4; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 6

Native pointer: /joint_analysis/impact/3/comparison_ids/5; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 7

Native pointer: /joint_analysis/impact/3/comparison_ids/6; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: ed65e644f9380ee8e946bfc20e6a2462315e1bc4b35029e62ab6d14fe68723bd

curated_feedback_SO_ZO_E06cL_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 8ac3b850aefa1115a150e653472c5f992cf22de042ffec1212c0c25096dc1d16

For each registered deterministic/randomized g1 q1 quantity: d∈N, d≥1; known compact centrally symmetric convex B with nonempty interior; known nonempty compact convex K; L>0, ε>0; globally convex L-Lipschitz objectives on R^d; unrestricted exact scalar queries, output in K, and the registered fixed-path budget. Geometry varies jointly and its dependence remains explicit. Native p,q,R are conditional ball coordinates. The historical R metadata about a global minimizer cannot override the fixed constrained contract; the new endpoint uses derived ρ. Deterministic q2 remains separate and untransferred. Write Z for K=c_K+ρB, ρ≥0, ε≥Lρ within this domain.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: a5bb280d72888508c94edbe32c09cbafc2703c6b4e7fa64e5175c671baf0c117

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 7bab3634aa276ededb592ec1d42cc0c351e612cea26f1a8cc1d5979d877ae8fa

matched-l1-joint

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: dcc6a578b375ad3655cdda35273d8635dc7a2ef33fd02262a94eed0f4dba8d31

joint_rate_refinement

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: b0c9c78fc1a38e85b318d32335480f0101ec91e8e898cd8350a94d31377b34d9

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 58575a18baa8bb7e0b89cc90b11afc8b5bfb5e976af112df243b056ad22ce76d

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c

#### Native item 3

Native pointer: /joint_analysis/impact/4/comparison_ids/2; canonical SHA-256: 87351f4d697ec66c57b348213040afa9701f9eeaa5e228320edc9c1997951fea

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c

#### Native item 4

Native pointer: /joint_analysis/impact/4/comparison_ids/3; canonical SHA-256: 7de0d0f1333f3f6d078f560a80b1fea057c1e834dcee16e848e7ea94eb72c791

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c

#### Native item 5

Native pointer: /joint_analysis/impact/4/comparison_ids/4; canonical SHA-256: 96fee94beab4740b775925d6f467799a17f0164c697a48b7d93927ef6567150d

SO_ZO_E06cL__kimi001_20261124__det_coarse__c

#### Native item 6

Native pointer: /joint_analysis/impact/4/comparison_ids/5; canonical SHA-256: f1d3e287a12fecdc7cc868341d491466d5f87c194950ca698c4cc94c94cebcc3

SO_ZO_E06cL__kimi001_20261124__det_plateau__c

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: b42e55491dabf251680b1417f2936241352a71e9967dd9c57e63e97f05e70ee5

Matched l1 geometry in the displayed sufficient-dimension and small-normalized-accuracy domain.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: b0590e8d6cd3549bd57d1012f47d6e47dba0030c87a9497a04ed2373d4559f2f

At fixed $\varepsilon=cLR/\sqrt d$, the registered randomized bracket was $\Omega_c(d)$ to $O_c(d^2\log(ed))$.

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 77bbd1badc31803087816e529012b58bd1e69130e43b76a7dcc0da6945555e11

The randomized joint polynomial rate is $d\min\{d,A_1^2\}$ up to explicitly displayed logarithmic factors; the benchmark has lower $\Omega_c(d^2/\log^2(ed))$.

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 37619d20bef327540582297cb14f37499cb7a272dd4c235bc3c45735e875986b

Penalized support functions and hidden-spike sensing supply complementary randomized lower bounds; the applicable two-point and deterministic localization algorithms form the upper minimum.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 98cd6b4cd08c1c885c17fbd6f7a4b3c48faf39ed47d2c6cc10fa229c34cbbe75

asymptotic_with_explicit_source_conditions

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 408e83e89da604c1d10ebb543265ec15601b22b22b8686eb6d7cedb65c881a19

The slice alpha_1=c/sqrt(d) for fixed c and sufficiently large d.

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: dc163ae85eac0f0b7b17cb6a2d0d29cd5f6e63a09986af61b55fbd47cefff9cd

Other norm bodies, the exact zero-query endpoint, and the benchmark residual retain their separate bounds and guarantees.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 176c473f7d15902e5b0800aa40bd7fbb985fcb849500493a1aed221c8e0f9470

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: ebfd5b79d4099b8c4413bee3322daf4934ccbeca3157fd2ea0e4a6398f5e9333

Complete any desired broader literature search beyond the terminal exact-ID query; this is a supported local update, not exhaustive coverage.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 07bfc0847ea79a80fde426bbc94add0d321d556062cb0a9466e288b23d485b74

Assess 2610.00345v1 Appendix K.4 constant-distortion certificates and further image-radius refinements in other geometry/accuracy regions.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 92f73a35e5110867713a07f6115ace06d941b0b1b53c920762bb335bccc2c73c

Assemble low-dimensional positive-cost branches and the unassessed complement. The affine pair establishes only nontriviality below the matching-body threshold.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: b5873d05c45132dd91af49da8f0c6cd49f6ccfc2e14e888a394e734f8097ffc8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E06cL__deterministic__b3 to SO_ZO_E06cL__deterministic__c1, SO_ZO_E06cL__deterministic__c2; no transfer is adopted by this metadata inventory.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: b66f6ae4dc5b756fdf8c9478357ec6951b4945ceac998a0e1cc51680fb9951b6

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 50a5c44c01e9c88236b5af962ea7d53d16d17ac046d208a592a02fa5a00ae00f

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 87d28495d02917dcdc6a5463a612ede21119ca21f500b030822f9806ef31520a

Unchanged native claim and guards; no fresh recertification.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 48135db74000fdaf5f443b77680e2f4db060a4e8535562a3f844a4e53398fd2a

Frozen /bounds/0 and its original evidence/source dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: cacec765a24d4171d024d12ad6857763441318aa9764334467be1aec98800d91

Original constrained localization validity.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: ebe3e068a90033eb7bc7048c6a18d6b0ec6953a15137ddedeb4862a25d30009b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 6ca3b0e8e89e178a2e9d03691aaab16642caa3ab5ceca470269f98c2cf78634b

Frozen /bounds/1 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 5638e777c4cdab300f65ee653a8977c963a9dedb2a65ecf059cf929f237093bf

Original admissible image-dimension and accuracy windows.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 5db21b31727bd260d4ec7be41b3f5040da35ea5b200b0b3f20354e8d258b8ba1

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: a2aadf6207b5186b850effbfa5d79eda2b3ea7519e9a71e93b5d6faf846ba8c4

Frozen /bounds/3 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 6b515870705506274bd619d92256f8828652284d6f74ab47cf5f2c5a2631e741

Original localization validity.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 65bfc2467aa17fcc1021f4cf21fd50f1116e6ad80927d6017e0ef5dfdfe842df

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 1b61307dfd1cac4d3cc2370d155a4f71dde64f2b012c2f7868795e171b8870fe

Frozen /bounds/4 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: d05b0b7dc6b8a3897591b5233afcc16d9932005d89bf08f393fee99a0a368cec

Original B_q, dimension and prox guards.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: bc4bdecb75bfc799ccb1238496b1896b546f03d0f5f63fe85de3391a740a3702

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 8b6af275dfdcb5e06eca32f09258923197501ad3aea0ea6139a15c839fa90416

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: ae25a2deb5a8c46284c6cc5bbcf760cabac7bfb75b16c13385f160dfa72b5607

ZO_PROOF_GEOMETRY_RANDOM

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: d8ee906375e403584989a838e82a6215db2e604fc64ddc8cba10465d78be8a6a

Frozen /bounds/5 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 62429442f9324822993bd4d7ddd015fd5a225087aedcf81406e2ee9430378bd3

Original Euclidean conversion validity.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: fb072e3397879241171e3711cc0199f7c1af67eb83fc0b44ebeea2a53032f2b0

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 7bde60a13b373e32c58f901759e2cda8ca96a993c9e9365af89ed90651757532

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 0103c02eea6aa9949a37aba4756e64489181b6dd6773b79ca803d80802269528

ZO_PROOF_GEOMETRY_IMAGE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: ae47d47a7856ca13a2b1fdb40a8dfd9224b0936b41ec1afe0c86c09c905f006d

Frozen /bounds/6 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 5638e777c4cdab300f65ee653a8977c963a9dedb2a65ecf059cf929f237093bf

Original admissible image-dimension and accuracy windows.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: eb116405bb8b65c92f23b875983bba520c405051f325639a7276fdd1073906db

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: d6397c3d74ea4928760aba95ad19f5760e62d8231cc62b1cf3d08d50744297de

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native item 2

Native pointer: /joint_analysis/provenance/6/proof_refs/1; canonical SHA-256: 35d31d90801dd65b1e9e1658ed7d97bf28b7829088e44457c220c190834be5c0

ZO_PROOF_PAIRED_UPPER

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 2da1c1a88697fd1330b04ef265b60ad408a0940e542c7762dc005ec56b2d86eb

Frozen /bounds/7 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 92aa64d151a4114885b8c24414bc488e7f724896ff4c2339ba93501331e288ab

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 58cc405349cbf13faec0617b632695f83f4e4aba198543e3e509b5dfd0d80219

Unchanged native claim and guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 642ecb3c8038144b780e7c34f800555700c5909bb34d5e8e7de949fdb8a535f0

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: 6f7410689eef4d8115c8120981de9a4d9c8ec6a3e8665ae59dc447f15d95fc2a

ZO_PROOF_GEOMETRY_BASE

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: 2f64f30301cb193a570d66eade820041355bad0e6ed07aaf36f5f0d75a346176

Conditionally retained baseline premises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: c62994c25939867ec5e26143124f230dac5918f2fb4cd4525c44e78fa12fb977

Frozen /bounds/8 and its original dependencies.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 9c8f7cef181674f6949b4481d3c1758e8bce68db7b9c0a6894c6ec8ca91223e1

Matching ellipsoid, A_B>1.

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: 05d565b3ea3635b3945b04f7fcc28e9c611ce798f2f690a7662a4eeacddd0878

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: d3d95785f570ec146e04944481f96a85598ed9dfa1cc381448e576e87252df83

Direct center algorithm; no oracle or quantity transfer.

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: 2efc2daf450fa24b3c430b4fdb5fca461eb3b0a27fb364025ac336c9223492f8

Global Lipschitz constrained contract.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 46e32ab1a600c2830c4b312dabb26933743776cf27f02ec93d4dc138d29d8ce1

Frozen contract/views/quantities hashes in endpoint-zero.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: 4e6b277f6fa5dfedd94c0d796048dc329f19495d043d94c66a8eabde4223bdac

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 4a83e5803ed0ea0ee405f78652892629a4a0ccb652759adb7d5f720e6c84ee9f

Budget nonnegativity.

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/9/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: 2952b7b5ce38f388e3d2447adf3935fbf7c9759e9435d4d803df110c26abcd40

Nonnegative charged call budgets.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: 3ccfc4dd7e2ee5fb196c28af90d1a85cc19b5d06a71b81b982ee8ae3624a77c3

Frozen quantity and resource definitions.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: 3e3ee72256c35220e3dd0b454424154b7f7eaa2d34242e142d4935929475cbf6

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 8acab4617a9863764a3b110ef85b40c6386d756e186c8804ac13c0ca09652294

Deterministic center algorithm meets randomized g1 with probability one.

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/10/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: 2efc2daf450fa24b3c430b4fdb5fca461eb3b0a27fb364025ac336c9223492f8

Global Lipschitz constrained contract.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 46e32ab1a600c2830c4b312dabb26933743776cf27f02ec93d4dc138d29d8ce1

Frozen contract/views/quantities hashes in endpoint-zero.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 1749726df0a25f6938abff3319d7225d72772805589cb5b0ccd891108c7f8f34

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 4a83e5803ed0ea0ee405f78652892629a4a0ccb652759adb7d5f720e6c84ee9f

Budget nonnegativity.

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: c1ef726cdcb00573a62d5972cf8336587e5c55db2dcd18b133234845796010f4

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: f1cedb46adb7b52db33175e9a135101451a9fec85808bf292e9120766e4c512a

ZO_PROOF_MATCHING_BODY_ZERO

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: f0e6a7ccfa32bc96ad9314486b437e66a251647064533430aa98429858f1c82a

Nonnegative fixed-path call budgets.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 3ccfc4dd7e2ee5fb196c28af90d1a85cc19b5d06a71b81b982ee8ae3624a77c3

Frozen quantity and resource definitions.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 13

Native pointer: /joint_analysis/provenance/12; canonical SHA-256: bb35b79a349a63bad02691c0adf64fc3a7484a9ab0fbbcd6a510e3450144c2d4

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/12/bound_id; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native field: origin

Native pointer: /joint_analysis/provenance/12/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/12/source_refs; canonical SHA-256: 5f71b5bc26f2e41836f41708c54c75a2e78767aa9850f2c48e182f677b8f4484

#### Native item 1

Native pointer: /joint_analysis/provenance/12/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/12/source_locator; canonical SHA-256: 5320ea591240574b074a21ab8ff12be20e967bf3f0513a43942eaadaeeec18e6

Lemma 1, signed-simplex product-Laplace estimator and entropic mirror descent

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/12/source_domain; canonical SHA-256: 5d3069258aca6ab5ab624907f0b90a8eca3edcdfa69a4f7550bd4f1ec920badb

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/12/target_domain; canonical SHA-256: 5d3069258aca6ab5ab624907f0b90a8eca3edcdfa69a4f7550bd4f1ec920badb

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge1$ and $\alpha_1>0$.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/12/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/12/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/12/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 14

Native pointer: /joint_analysis/provenance/13; canonical SHA-256: 763837be53c28eaeaa5263473a56258fd0518684b1c8677550ce1d034a41ae8b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/13/bound_id; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native field: origin

Native pointer: /joint_analysis/provenance/13/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/13/source_refs; canonical SHA-256: 201b811da2c394c39f7297032a470c5856e6c0d8aeaa50dca51b2654fd36138a

#### Native item 1

Native pointer: /joint_analysis/provenance/13/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /joint_analysis/provenance/13/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native item 3

Native pointer: /joint_analysis/provenance/13/source_refs/2; canonical SHA-256: 3870a660e3630920141416411901519b55e702fccd2d42b40fd802fefe8f62ee

SO_SRC_LSV_1706_07357_PROTASOV

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/13/source_locator; canonical SHA-256: 2fe0e364b4adf909366446cb8f6a3cba2237f6cf521d01d3e4e56ea86b2a58f7

Lemma 2 and Proposition 1; Protasov explicit-body value theorem, discussed in Lee--Sidford--Vempala PDF page 2

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/13/source_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/13/target_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/13/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/13/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/13/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 15

Native pointer: /joint_analysis/provenance/14; canonical SHA-256: 050c20446fd95b43bb78615e505d21f813241ca160c25caf89a2a40dcc49f9fa

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/14/bound_id; canonical SHA-256: dfe217b8ce51c20ef77e003371d9b4f11b72fdc09a9e930f4cce315b0055a1ca

SO_ZO_E06cL__kimi001_20261124__det_body_upper

#### Native field: origin

Native pointer: /joint_analysis/provenance/14/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/14/source_refs; canonical SHA-256: 201b811da2c394c39f7297032a470c5856e6c0d8aeaa50dca51b2654fd36138a

#### Native item 1

Native pointer: /joint_analysis/provenance/14/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /joint_analysis/provenance/14/source_refs/1; canonical SHA-256: 5cc5a4e23e9fe4e1da65b0023dcdf67e4094dafafdb9e941785ab6101731747c

SO_SRC_77682e60a35290df

#### Native item 3

Native pointer: /joint_analysis/provenance/14/source_refs/2; canonical SHA-256: 3870a660e3630920141416411901519b55e702fccd2d42b40fd802fefe8f62ee

SO_SRC_LSV_1706_07357_PROTASOV

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/14/source_locator; canonical SHA-256: 2fe0e364b4adf909366446cb8f6a3cba2237f6cf521d01d3e4e56ea86b2a58f7

Lemma 2 and Proposition 1; Protasov explicit-body value theorem, discussed in Lee--Sidford--Vempala PDF page 2

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/14/source_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/14/target_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/14/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/14/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/14/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 16

Native pointer: /joint_analysis/provenance/15; canonical SHA-256: 133757d6cd7fb7583d5fc3ca5000769b094fe9476151513eb224d587ddc40168

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/15/bound_id; canonical SHA-256: e5f1138a0999967d98b33bc0462d246bc2e3b7e35ad69972c97d0d4cbfcc52bc

SO_ZO_E06cL__kimi001_20261124__rand_regional_lower

#### Native field: origin

Native pointer: /joint_analysis/provenance/15/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/15/source_refs; canonical SHA-256: ff20253ffa788f981f632d92b9ba4abed6fa3331aa72ff997f4d965b0866f79e

#### Native item 1

Native pointer: /joint_analysis/provenance/15/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /joint_analysis/provenance/15/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/15/source_locator; canonical SHA-256: 246c14bafec77579eb1e0308c6fe74b6d0bd704e3fd5dd345a5e95f507d336d8

Theorem 2, Sections 5.1--5.4; normalized ZZQL Theorem 5 input

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/15/source_domain; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/15/target_domain; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/15/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/15/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/15/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 17

Native pointer: /joint_analysis/provenance/16; canonical SHA-256: fc6dc589fad36bf13970f1d11881523248f60576917ac388b52eba0aa502cb17

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/16/bound_id; canonical SHA-256: de837cab36cfe8cf2a8d74bf11f21980fc6858ad83846ae9d7bcb44b3c006b35

SO_ZO_E06cL__kimi001_20261124__rand_spike_lower

#### Native field: origin

Native pointer: /joint_analysis/provenance/16/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/16/source_refs; canonical SHA-256: 5f71b5bc26f2e41836f41708c54c75a2e78767aa9850f2c48e182f677b8f4484

#### Native item 1

Native pointer: /joint_analysis/provenance/16/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/16/source_locator; canonical SHA-256: 2867b2826f5000da2e2b18e38ef97641520dd3e7e3a026f37d5d0f2572fd336f

Lemma 3 and Corollary 1; two charged validation values included

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/16/source_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/16/target_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/16/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/16/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/16/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 18

Native pointer: /joint_analysis/provenance/17; canonical SHA-256: 3f48e9ff14f0fdd67bf7fdbd08727096f9b45dbe10fe0fdb2ec500888e0d7d91

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/17/bound_id; canonical SHA-256: 927de04778e5034294e17889f81571b78b805189703593dac798632f5fc22a4f

SO_ZO_E06cL__kimi001_20261124__rand_joint_lower

#### Native field: origin

Native pointer: /joint_analysis/provenance/17/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/17/source_refs; canonical SHA-256: ff20253ffa788f981f632d92b9ba4abed6fa3331aa72ff997f4d965b0866f79e

#### Native item 1

Native pointer: /joint_analysis/provenance/17/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /joint_analysis/provenance/17/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/17/source_locator; canonical SHA-256: f74236a3fa06ce685eac2ec0cb375316f4209627a65fbbf5d85c39bf491b9469

Theorem 1, composed from Theorem 2 and Corollary 1 in Section 7

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/17/source_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/17/target_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/17/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/17/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/17/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 19

Native pointer: /joint_analysis/provenance/18; canonical SHA-256: 3cc6cdb273905a5106e2a39652165ca08f6b704879a5d9ab6a1080e95fc8dc78

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/18/bound_id; canonical SHA-256: e9f655f0f146dde6794e09684fc8e89116b5fd8589de02402e10f9de84688500

SO_ZO_E06cL__kimi001_20261124__det_regional_lower

#### Native field: origin

Native pointer: /joint_analysis/provenance/18/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/18/source_refs; canonical SHA-256: ff20253ffa788f981f632d92b9ba4abed6fa3331aa72ff997f4d965b0866f79e

#### Native item 1

Native pointer: /joint_analysis/provenance/18/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /joint_analysis/provenance/18/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/18/source_locator; canonical SHA-256: 64cce6275b141323b0753353f48e159d7ab13042a96acd57da0a0010b3cf6a3c

Theorem 2; restriction of the unrestricted randomized lower to deterministic algorithms

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/18/source_domain; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/18/target_domain; canonical SHA-256: 783b7179391f5ae12ac6f6a4fecb657ea5b8bb02f52de26ad6fb1ead65980aa8

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed. $\alpha_1\le\tau_d$.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/18/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/18/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/18/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native item 20

Native pointer: /joint_analysis/provenance/19; canonical SHA-256: daba9c1ea9e78bfde91b1e490a5f76275e275dba42a7064b281ca1053cd9ecab

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/19/bound_id; canonical SHA-256: a26f8b529b40e7120dd294e5e025d7866e408227ee65efba01933f41e0c30c4a

SO_ZO_E06cL__kimi001_20261124__det_joint_lower

#### Native field: origin

Native pointer: /joint_analysis/provenance/19/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/19/source_refs; canonical SHA-256: ff20253ffa788f981f632d92b9ba4abed6fa3331aa72ff997f4d965b0866f79e

#### Native item 1

Native pointer: /joint_analysis/provenance/19/source_refs/0; canonical SHA-256: bc5f3ca7694dd1cb7fd60cf601d1c8d89c07103d03d379a48dd201a73227b481

COLOMBO_KIMI_001

#### Native item 2

Native pointer: /joint_analysis/provenance/19/source_refs/1; canonical SHA-256: 5d3a21acbc96f86af54cdb21c87600b772611ef8808f1128555236a2c6c69dd0

SO_SRC_8baf287e5cfc8672

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/19/source_locator; canonical SHA-256: 9c20a1396dc17c6d5cc099a89e3c4f8f228ddf6f3b3c1d4aaf3191cc269470e2

Theorem 1; restriction of the unrestricted randomized lower to deterministic algorithms

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/19/source_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/19/target_domain; canonical SHA-256: 9aef8d95601be526872dfff6a17002a5eb69edbce5843f847a3086da738bdec6

$B=B_1(0,1)$, $K=B_1(0,R)$, $L,R>0$. $d\ge d_1^{(1)}$ and $0<\alpha_1\le c_0^{(1)}\le1/8$; $c_0^{(1)}$ and source constants are fixed.

#### Native field: mapping

Native pointer: /joint_analysis/provenance/19/mapping; canonical SHA-256: c8b5785f3887f41dd160ceffa648c4c07b52c85fe720779ff075b07559eb4a94

Matched-l1 normalization and the displayed guarantee, oracle, output and budget mappings.

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/19/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/provenance/19/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 6da32335bcf23cf5e076d485dc05e602e4b31bc0a6e9d29ffb4600b8184ee83f

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 60b39403baf7b477c0d66dfcc50ececdee544087ba078e1cc5e6ef957390acfa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/8; canonical SHA-256: 58575a18baa8bb7e0b89cc90b11afc8b5bfb5e976af112df243b056ad22ce76d

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/9; canonical SHA-256: 87351f4d697ec66c57b348213040afa9701f9eeaa5e228320edc9c1997951fea

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/10; canonical SHA-256: 7de0d0f1333f3f6d078f560a80b1fea057c1e834dcee16e848e7ea94eb72c791

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/11; canonical SHA-256: 96fee94beab4740b775925d6f467799a17f0164c697a48b7d93927ef6567150d

SO_ZO_E06cL__kimi001_20261124__det_coarse__c

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/12; canonical SHA-256: f1d3e287a12fecdc7cc868341d491466d5f87c194950ca698c4cc94c94cebcc3

SO_ZO_E06cL__kimi001_20261124__det_plateau__c

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: 81546000e158d9da2c68c316aceac05c0648414385355f5f10ad472c722cfe40

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 59baaf45c3ddd8d93b3158082325823381f9a9473aa501e731c04aff88f921ce

Colombo_KIMI_001 and the cited source ingredients are assessed for the displayed matched-l1 regimes. Other native claims and their finite historical scope are retained. The unassessed complement and unresolved prior material leads remain outside this source assessment.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: fecf35fcdeee5f3bda17cea4e11070f1c223c13bfa819d4ca3ba3c36d129b0c7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: abb6cf587973e4b85068b31e20d77b516f64ba7348bdff9bc9fd010c1e08d19d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 3c0fef27e7705ea9dc20997f75f0474ca7df6f780f8adb867dca12723a391486

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: e04b768e78dceb8a470bf05e02937c00e17c02051e2b8c10ed9d555ac0d84084

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 7977aaad05402497a0ba67383d64b8f7e0108da535cdaad2a7ba9b6e0a06f52e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 3c0fef27e7705ea9dc20997f75f0474ca7df6f780f8adb867dca12723a391486

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 3463fbe7607634c3917f1ec97ad50dbdf3ec350e49940b6bcc85ecc311a21c9c

SO_ZO_E06cL__deterministic__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: e62e4fc604b40589a1fb1615f96ea16e1d38981f53efaa905147134281cbfb3d

SO_ZO_E06cL__deterministic__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 3b82935387bf36964e8b641d18b3acc03efe8cb04af9ab1ad54b2c5b85fdc924

SO_ZO_E06cL__deterministic__b5

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 1ca3b819c4a540efeb55df39458dc0b7d1af02bf24f7f93f4578d26bbd3ea913

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 8a02f06c64b6955c12c0ed1c24c4310841da3c65c46574b2e3330b41092c0a94

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 5595ae958132d137164fe0cd5dbaddaa271f923224a5dc609ae105638d0c4211

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 94ebdcb021bcbc6fc94fa708c1e7a7f9d1afd6248b96e70935fa7df176e425ff

synthesis-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 0c0e592eb2292fd0cf2226c9ac25e312479da17c5390613a39f4ab11d26c73ef

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 8d6e376bac368f54053646a9603e3523de64e25fbe4d9561bcc58a78fb07d1e3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 7f1a6540bd14dbb3bcfdfdfac9a64bfde09607556bb3c904bfc43adedf6ede22

synthesis-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 770ed6278f18bbe6ed3d68c3bd1d758aeeab6e82a571a87ad8bc34bc0961a03c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 17bda35342cb4ec62b598f61baae03ca9e75c52625b72b95969167cf743ec255

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: ca0bbdf769e92b6ee0fc04da5960cb413f34af9e8cc0d5eca08f2ac29f71ac8f

synthesis-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 069a1c02fde261f6bc9882d66c3a20d44c6bb72312e90144febb6c3e634b0bf6

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: ac42228087c861bf7b8a9ed6f028f9874a3c97d9a009b65404d66c5adc2e75f0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 8cedb7c54fb7a3ff1b2d98263a56263d1a8afbb4fdabf8cee435054dc16d1ea3

synthesis-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 13e96797fad7158a4ac28671aaf3b2f7d0da737f74557f5771d9ad198fdd2801

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 1c163815a3606320ba2975c04f550e45ba5564c47dc7807d2ad91b27a4f63bf4

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/0; canonical SHA-256: b365c3c91aba3882e47966ccc756e18a6e7ddfeaec7ff2aef9db5f1ce89064fc

SO_ZO_E06cL__randomized__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/1; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/2; canonical SHA-256: e93f533ccc43f3023e907edef55baf41415aef9a62652fad37056b4db93c690e

SO_ZO_E06cL__randomized__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/4; canonical SHA-256: fdd9cc14a34b1e8f4fdb5869e7fca233863fb9d5a91b162724461a5ec3a60e52

SO_ZO_E06cL__randomized__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/5; canonical SHA-256: 08b710e65b42f66d9246d4def156a64caae672f60cdc5e503b696be6c37fd310

SO_ZO_E06cL__randomized__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/6; canonical SHA-256: 8fff8bc669e548124986abafdfdb428d3c568f0f4fb994f6491a9b8d4485da8a

SO_ZO_E06cL__randomized__b7

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs/7; canonical SHA-256: 804d5f449654effd8cdaac7626f7462a5cdfe698862093ee48960b2e0c59848b

SO_ZO_E06cL__randomized__b8

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: edf74a5372a7b6da3c1c6aad7a9fe617f6f7179312b96693eaccf00fd68a91ac

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 5fa33983f32a4c1027a92106c478a51fb23e76f63df8884a2a111e3319f68669

synthesis-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 123bb7b9622ed4dc39c0539a3512757609723ae60226a2f36136cf0e191cf47f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 573b1ff385913d0694cbad1931fa4489097adcf6ee14276bfb5112d539f7d460

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/4; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/5; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/6; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/7; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: ebfd5b79d4099b8c4413bee3322daf4934ccbeca3157fd2ea0e4a6398f5e9333

Complete any desired broader literature search beyond the terminal exact-ID query; this is a supported local update, not exhaustive coverage.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 8d49c9e9d244c0b28db859f5f7f64722bbc9e79a60b70f6f965306d1e0f6fd95

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 573b1ff385913d0694cbad1931fa4489097adcf6ee14276bfb5112d539f7d460

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/3; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/4; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/5; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/6; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/7; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 07bfc0847ea79a80fde426bbc94add0d321d556062cb0a9466e288b23d485b74

Assess 2610.00345v1 Appendix K.4 constant-distortion certificates and further image-radius refinements in other geometry/accuracy regions.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 8981f964608db030517ddf66d00a6bbeea76f69d36bd7b28b6ecfa68472ca21c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 573b1ff385913d0694cbad1931fa4489097adcf6ee14276bfb5112d539f7d460

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/3; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/4; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/5; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/6; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/7; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 92f73a35e5110867713a07f6115ace06d941b0b1b53c920762bb335bccc2c73c

Assemble low-dimensional positive-cost branches and the unassessed complement. The affine pair establishes only nontriviality below the matching-body threshold.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 8d1bff1411713758410af9b3defc20e0751362ad7563ac60d6ba7179ecdd6f1f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 573b1ff385913d0694cbad1931fa4489097adcf6ee14276bfb5112d539f7d460

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: 183442b127be22b9995ffd2369a31872743014f2adc97dd07b7d81aa19b48d69

SO_ZO_E06cL__randomized__c1

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/4; canonical SHA-256: b3bd28de42430e33970fb68ffc04da1e629ffc8098a0e52cde80cbd19b40c400

SO_ZO_E06cL__randomized__c3

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/5; canonical SHA-256: b43113655349fbb875a550bc451c50481da0ecb434e9d33b3668d7e45a7fd7a7

SO_ZO_E06cL__randomized__c4

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/6; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/7; canonical SHA-256: c4bf7706f0a9014dfe772babbf4c7341a7f8a12e0e4b456c3d3450547e6bbb44

SO_ZO_E06cL__randomized__c5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/obligations/11; canonical SHA-256: e36473a72f7e5a47aa561c467755b5a12e6b74ea5aada1753ab74f45e577da83

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/argument; canonical SHA-256: 1d6253baa7434e9481a44524a988c18a44657675fc2c2c418d93992e68454c9f

Mechanical same-view/guarantee candidate opportunity only. Distinct IDs remain distinct; validity, direction, actual dominance and any proof are explicitly unassessed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs; canonical SHA-256: cea5e89e9c80db181f33dfd893f68205bb696429eab4016255f6d4fd8852750f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/bound_refs/0; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids; canonical SHA-256: 206654a4e3e7eb59e0a47f85d69c7b21465de5ccc61082110216839cef5ffc48

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/comparison_ids/1; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/id; canonical SHA-256: d41735e638c9de1fe43fcad7600c2a277f6e3a71428b42f4a9c4fe04652e0aaa

possible-projection-455ddb5d1dae

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/lead; canonical SHA-256: b5873d05c45132dd91af49da8f0c6cd49f6ccfc2e14e888a394e734f8097ffc8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E06cL__deterministic__b3 to SO_ZO_E06cL__deterministic__c1, SO_ZO_E06cL__deterministic__c2; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/11/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/obligations/12; canonical SHA-256: f136d13747854ba3e6d576e26341bbdcf93f65ec7fee494c792ac6750d157ee1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/argument; canonical SHA-256: aaa743eaa494b44a39afd3bf614b3849a8ecba7f0e1285a8719656aeabc522c9

Explicit pending opportunity, not a proved bound, equivalence or mature open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs; canonical SHA-256: cea5e89e9c80db181f33dfd893f68205bb696429eab4016255f6d4fd8852750f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/bound_refs/0; canonical SHA-256: d1f58b650ca50fca6d3871c771d913e028c65460d4886722572076b5350e7634

SO_ZO_E06cL__deterministic__b3

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids; canonical SHA-256: 206654a4e3e7eb59e0a47f85d69c7b21465de5ccc61082110216839cef5ffc48

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/0; canonical SHA-256: 80f36278ce44c9ebaae0e5f0af157977c43fc12cda2c44bf3778106fb47c7ba6

SO_ZO_E06cL__deterministic__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/comparison_ids/1; canonical SHA-256: d98fd3c079f27b42332a9e6bbc1982bed426f1c80b83b7b2362c2cfaec570440

SO_ZO_E06cL__deterministic__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/id; canonical SHA-256: c1190c998c57c9c3af21b675846c348e2a77873c4893b05d7c760c796c7a422b

possible-projection-455ddb5d1dae-lead

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/lead; canonical SHA-256: b5873d05c45132dd91af49da8f0c6cd49f6ccfc2e14e888a394e734f8097ffc8

Assess the guard-, cost- and guarantee-preserving directed resource/quantity mapping from SO_ZO_E06cL__deterministic__b3 to SO_ZO_E06cL__deterministic__c1, SO_ZO_E06cL__deterministic__c2; no transfer is adopted by this metadata inventory.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/12/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/obligations/13; canonical SHA-256: 4ca4fe695e3e8cb8210cdee70b3a558f4a679698da1c31c5e849f35f9636cc5c

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/id; canonical SHA-256: 80e8b75eb41d2f403fb8a7735163ddcfe4dd7401b9759054cadbb068ccd92016

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids; canonical SHA-256: ac28f5f2259643c5b9cd05b7ac8e3a7a742471551cb416ffe3ecc60224475b77

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/comparison_ids/0; canonical SHA-256: d9c65b61753c1fbee9079512c1a18e4ecdf1e6d7a4045c449f240686d6815b02

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs; canonical SHA-256: 4f0322a58eaa65912ff40c0a4b39fe5f66195886abb3231d9391ab452e76df8e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/0; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/1; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/2; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/bound_refs/3; canonical SHA-256: 927de04778e5034294e17889f81571b78b805189703593dac798632f5fc22a4f

SO_ZO_E06cL__kimi001_20261124__rand_joint_lower

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids; canonical SHA-256: e485a20ecdaa654fbd15588e0f7880f622d6f21ac9a9169edd4ba89b5a2859c0

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/cell_ids/0; canonical SHA-256: 5e5745f9f19cd8cf3090b6c3ae51e59f644d8027c76e3d8f9cd4c3cdda24ae61

SO_ZO_E06cL__kimi001_20261124__l1_benchmark__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/13/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native item 15

Native pointer: /joint_analysis/synthesis_coverage/obligations/14; canonical SHA-256: 1c2ee89ece67963a2b20d3d0e1b8b93de61a2c274ea2be7a9dc8710a7ab6645e

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/id; canonical SHA-256: d8a62eb84c20617e7460cd23588f1d27b9a6fe53de39392153db36c122ef42ed

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids; canonical SHA-256: edabe0eae9707f759db8ae735ebc5c3a6958cfe47b358f823235cf2492f9418a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/comparison_ids/0; canonical SHA-256: e9c62fd11df6d983fe899839036f4861cdd9317cae49c3619a1d773338de0fe3

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs; canonical SHA-256: f0251b4b3b3b372657789201ffe7c728ac934d9b6f7c43db0f023cf233079fb2

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/0; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/bound_refs/1; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids; canonical SHA-256: 46bac8100402cc464705712ab9d98536d440906c107ce22f8730c86a684bd5b5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/cell_ids/0; canonical SHA-256: 510a80386e7411ddb956e998f19cde94e6517ac59d13ca51ffe58d9c28192799

SO_ZO_E06cL__kimi001_20261124__l1_benchmark_residual__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/14/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native item 16

Native pointer: /joint_analysis/synthesis_coverage/obligations/15; canonical SHA-256: 80c08b6c0837e0cf3ce85f592e6874ec1a10322ab3f03668d980c88ffbd1277b

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/id; canonical SHA-256: 455f3e1cbdd918cdaa722e125c67e5ac092150c11ceab2b77f4a3349e628b444

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids; canonical SHA-256: a69bcfe83b40f83cc000b55f2bcbce69dc821a08b544fb382990623a51a167f9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/comparison_ids/0; canonical SHA-256: 58575a18baa8bb7e0b89cc90b11afc8b5bfb5e976af112df243b056ad22ce76d

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs; canonical SHA-256: 51bc661d4e4a3683ede0ca00b476c3af652e27e4ae101bae3c1f1a3550352319

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/0; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/1; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/2; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/bound_refs/4; canonical SHA-256: e5f1138a0999967d98b33bc0462d246bc2e3b7e35ad69972c97d0d4cbfcc52bc

SO_ZO_E06cL__kimi001_20261124__rand_regional_lower

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids; canonical SHA-256: f1b260c30a03835f034bc062f667a73cfb5d4a40c06187bafc5aeff4e0fa2f1e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/cell_ids/0; canonical SHA-256: f205425701a5acaa05bc6e0992f181c88224e636cd1c1a56069f188d37da6032

SO_ZO_E06cL__kimi001_20261124__rand_coarse_regional__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/15/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native item 17

Native pointer: /joint_analysis/synthesis_coverage/obligations/16; canonical SHA-256: 7934b4e34ee208e3bccc72438ac652212e3d211705f60d77a6cc936812ac90c6

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/id; canonical SHA-256: 9c89265279981c7243a2965ce6ce223c6702553ad46d35d9b726de76afbaf076

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids; canonical SHA-256: 8adc9bb1b250674511b0e5c1f1ad7b5e810bae67be6dfd21326005ff07eab74d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/comparison_ids/0; canonical SHA-256: 87351f4d697ec66c57b348213040afa9701f9eeaa5e228320edc9c1997951fea

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs; canonical SHA-256: 46422a67d0d7e213e6701171adb9f4c403258615253938e5d15686ad81d59a43

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/0; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/1; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/2; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/bound_refs/4; canonical SHA-256: de837cab36cfe8cf2a8d74bf11f21980fc6858ad83846ae9d7bcb44b3c006b35

SO_ZO_E06cL__kimi001_20261124__rand_spike_lower

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids; canonical SHA-256: 5f0a562d022ebdf2a3253523565f13999f6fa0325fe6acc3f50fe5e132163d29

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/cell_ids/0; canonical SHA-256: 3e285bca2f520f18515ad67ec7272c1e2a6ef2468676d6e32b597c8e0df81c5b

SO_ZO_E06cL__kimi001_20261124__rand_coarse_spike__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/16/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native item 18

Native pointer: /joint_analysis/synthesis_coverage/obligations/17; canonical SHA-256: 6e0c9813cc3ca83d6a79487a6deeb02808b82a6ce4b38f7ea4ef0c0448d7f6d2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/id; canonical SHA-256: 94a3a2fae2a51cddc515f83423f54ebb414f21b38fa9aaad4dac66e4d5eac54d

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids; canonical SHA-256: 3e5644f562d10161b892c01c13f270811760276f40ee405952ec657b2bce4ad3

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/comparison_ids/0; canonical SHA-256: 7de0d0f1333f3f6d078f560a80b1fea057c1e834dcee16e848e7ea94eb72c791

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs; canonical SHA-256: 51bc661d4e4a3683ede0ca00b476c3af652e27e4ae101bae3c1f1a3550352319

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/0; canonical SHA-256: 4468403223031497e2f714b19747a62e8b096562fdc08752661431aeab28bf31

SO_ZO_E06cL__kimi001_20261124__rand_laplace_upper

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/1; canonical SHA-256: 6af36bca59808a19d8fd13d3c46abf532dcbe5ac9b1470e801891ab9e8ddf188

SO_ZO_E06cL__kimi001_20261124__rand_body_upper

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/2; canonical SHA-256: 96f07051775da2bb30ba4b098a75e9d7e6463db2c4d6d87da05ddf7e4a6f248c

SO_ZO_E06cL__randomized__b2

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/3; canonical SHA-256: 5a9c1f3c852365964b266330dbbea8dcd7cb46c0e47bdbdfc06909cae5465528

SO_ZO_E06cL__randomized__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/bound_refs/4; canonical SHA-256: e5f1138a0999967d98b33bc0462d246bc2e3b7e35ad69972c97d0d4cbfcc52bc

SO_ZO_E06cL__kimi001_20261124__rand_regional_lower

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids; canonical SHA-256: a9dc2f574b9583e8b47e8e324c5916aa23aaee8015ce39a6996a8778a5640de7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/cell_ids/0; canonical SHA-256: 18de03dedac4b234d033446ce0ff178e0d524f00356f636319141a6b4d87bd0a

SO_ZO_E06cL__kimi001_20261124__rand_plateau__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/17/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native item 19

Native pointer: /joint_analysis/synthesis_coverage/obligations/18; canonical SHA-256: 4e2d0467d0db64d40c3abbb2b05ea53e71eb5436637be6b51ee085d51280e525

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/id; canonical SHA-256: d398f0a86ca2cfc34af40a9e4ffd589e9aa7f85175db328d20157e71579f6b56

SO_ZO_E06cL__kimi001_20261124__det_coarse__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids; canonical SHA-256: 46acd4abd51d28c4e8c44fa10e712e6302e37b52cef721af10d6f55c0665674f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/comparison_ids/0; canonical SHA-256: 96fee94beab4740b775925d6f467799a17f0164c697a48b7d93927ef6567150d

SO_ZO_E06cL__kimi001_20261124__det_coarse__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs; canonical SHA-256: d5fc191777bbc6f22649412328e119e2df212b84218c5e37a93b0a5542cf2dfc

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs/0; canonical SHA-256: dfe217b8ce51c20ef77e003371d9b4f11b72fdc09a9e930f4cce315b0055a1ca

SO_ZO_E06cL__kimi001_20261124__det_body_upper

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs/1; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/bound_refs/2; canonical SHA-256: a26f8b529b40e7120dd294e5e025d7866e408227ee65efba01933f41e0c30c4a

SO_ZO_E06cL__kimi001_20261124__det_joint_lower

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/cell_ids; canonical SHA-256: 4144462f872663c62db27a73171afa4289080b383c74c7553d9eee2e26ba7397

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/cell_ids/0; canonical SHA-256: 5eb20159bb09b2b0a17ccb67f0ef66ea6867013a180b208a1144144eac32abee

SO_ZO_E06cL__kimi001_20261124__det_coarse__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/18/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native item 20

Native pointer: /joint_analysis/synthesis_coverage/obligations/19; canonical SHA-256: 78a85cf5b676fb07d7960d19690d5eafc17c74709584c324b69f1f2c11ae9455

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/id; canonical SHA-256: 8ee40bbd8c62bcf7cc978b55a8c6d97465f532b701022f3d30252ae7ce5b9cb1

SO_ZO_E06cL__kimi001_20261124__det_plateau__c__synthesis

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/argument; canonical SHA-256: 9926db1eefd7e48ed7cb3710ddc368deddba8b2cec804f8581c81518c16b7f41

The displayed upper minimum and lower maximum retain the original applicable image and two-point bounds and add the source bounds only under their dimension, accuracy, geometry and algorithm guards. Normalization and envelope compatibility are recorded in the cited proof.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids; canonical SHA-256: 6203d90f4d5cc72c272f30a461169fb53cd7096f9c1fce176b1fbaa3263627c9

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/comparison_ids/0; canonical SHA-256: f1d3e287a12fecdc7cc868341d491466d5f87c194950ca698c4cc94c94cebcc3

SO_ZO_E06cL__kimi001_20261124__det_plateau__c

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs; canonical SHA-256: b53313c5baf5ee9b56c371cade32d2115401b8a9055812cb57f98eedcc43ba1f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs/0; canonical SHA-256: dfe217b8ce51c20ef77e003371d9b4f11b72fdc09a9e930f4cce315b0055a1ca

SO_ZO_E06cL__kimi001_20261124__det_body_upper

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs/1; canonical SHA-256: c478086476803e2505d780b93fe13ba05e5561b362b82c65faab56da2e54cb07

SO_ZO_E06cL__deterministic__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/bound_refs/2; canonical SHA-256: e9f655f0f146dde6794e09684fc8e89116b5fd8589de02402e10f9de84688500

SO_ZO_E06cL__kimi001_20261124__det_regional_lower

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/cell_ids; canonical SHA-256: 5b88f45c7bfa844cde43ae6eaffd90d2a898f09609f011c3485e7600a08c3752

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/cell_ids/0; canonical SHA-256: c8e0d98beacc57a6635a6ad44deac5818d8652fc2310c0fa0d40a8c4b43578e8

SO_ZO_E06cL__kimi001_20261124__det_plateau__c__cell

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs; canonical SHA-256: 570b0948260bc7d7b1dd7ee77831eb5b1d0190585c3086555d62d9a2750d365d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/proof_refs/0; canonical SHA-256: 622dd10bfcc4240718419cb35138ae433b0b54c1d4c0e539a7c19e0e82828b81

SO_ZO_E06cL__kimi001_20261124__p_scaling_and_envelopes

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/19/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 9e0f57f9cbd36524afe1118c2476b39e2d4106e1683bcc6fceeb041729cdb6af

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: c2ac502657ee972767193d1d9b8653d5a0de4706c583b9f26129cc3b0e3914a2

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: e7dbd62e2517d9db3e659879a56251bc1d1ee0279c24ecc3b1974b01fe5f58f7

SO_ZO_E06cL__kimi001_20261124__p_c0

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 253a484b15dedcca470f2288066c904193c2da81da1126e148c3dec4cc85a0a5

SO_ZO_E06cL__kimi001_20261124__p_cdiamond

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: 04d7e7dcad9bc2370dcde8e69ef7fe7b3897daf9e3f54da865228db3874e6020

SO_ZO_E06cL__kimi001_20261124__p_d1

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: d84419e2c49b554448ee9a1f2df3cdbaeaa46b29f6e3bdca005f96d33a20b57c

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 4b81cab280b1e31c2ea7afa9a416577b7c9c22795698d5d642e0394c36a90edd

/quantities/2

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 3f4d2fca87d63c4fb83a0e0750a141c20e6c1a0bc6edebfefc0f4d9bdff3e644

For each registered deterministic/randomized g1 q1 quantity: d∈N, d≥1; known compact centrally symmetric convex B with nonempty interior; known nonempty compact convex K; L>0, ε>0; globally convex L-Lipschitz objectives on R^d; unrestricted exact scalar queries, output in K, and the registered fixed-path budget. Geometry varies jointly and its dependence remains explicit. Native p,q,R are conditional ball coordinates. R is the public radius only in an explicit feasible-body parameterization; the matching-body endpoint uses derived ρ. Deterministic q2 remains separate and untransferred. Write Z for K=c_K+ρB, ρ≥0, ε≥Lρ within this domain.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: a6af48a092bc0ea9e1d1a2ca1e8a9a80c14982ada4e5098d2d4e60ff7eeb2be5

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 87d22f5899dba09d228f9a2ee4c52c4620fde18e6da59a7030fca371918f56a5

SO_ZO_E06cL_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 14c926c9d28b13570cc6649c35a25bcca11749a5e701b7107d22f70c3db13c49

SO_ZO_E06cL_p_4729bcfd1c

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 984ad179be4dd155621ff8b9f27d12e918e3e4681c1c37d59b82622207ad9b0e

SO_ZO_E06cL_p_73a0c205b0

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 3e8a6aa7f2792d7437470daff2dad637353c60e95f4b4b9ab8a99630041006b0

SO_ZO_E06cL_p_5530ee35cd

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: 1a7c8e01a0c47200e802891f35b6ac47cb3e6089dfab6a77d8a93232ded5c055

SO_ZO_E06cL_p_16b7e5563d

#### Native item 8

Native pointer: /joint_analysis/target/joint_variables/7; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: a91720faaeefc8fbcf003a9937b5569baae73cf7c3def3dc5b1ad13e81735f43

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: b19e86d22aadd8d449bf802dc411ee67f7758c0bfa8ad27a9a17e203ee45a6bc

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: c9d11b84453f62d8fdb37e7174f0a30adb32e8aa64733504864d027ca24e6005

On matching bodies K=c_K+ρB, ρ≥0 is the unique homothety scale derived from B,K; c_K is the known symmetry center, or the sole point when ρ=0. For ρ>0, g(u)=f(c_K+ρu)/(Lρ) is 1-Lipschitz, so ε/(Lρ) is dimensionless accuracy. No global-minimizer promise is used.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: dfb6a76147c56882a49e51a5aa535d081adb406ed4faf0ff7e7b8bedfd58d4b0

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 14c926c9d28b13570cc6649c35a25bcca11749a5e701b7107d22f70c3db13c49

SO_ZO_E06cL_p_4729bcfd1c

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 984ad179be4dd155621ff8b9f27d12e918e3e4681c1c37d59b82622207ad9b0e

SO_ZO_E06cL_p_73a0c205b0

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 5d499343e09566f397417cb372cc43b2de03f43a5be8446a059f17f6e681818b

ρ

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: efbb2e34ffb833da2e2d148e038443f627dd8426273f75c744219f1cc8668d49

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: d3096427570ff87542cab18e02c769a8c39ed6bec95fc1910e7097b4ca682c69

Retain native A_B=LR/ε only on the existing matching ellipsoidal regime, where R is its stated body radius. Rescaling f(c+Ru)/(LR) justifies this coordinate; it is not defined for arbitrary K.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: 87622ffd1b7c57e4dca2ff1998a750f15784269323bfd117275e43e274326062

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/1; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/2; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: ee342de3ddaa6ddbf5e1a9daac41fa2b4b30d17a9c965e236c324ff9f956e0af

A_B

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/2; canonical SHA-256: db8665168852eb04a3fd5abbc78795cdd85a07b55debd9941f3517af9d0f6edd

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/2/symbol; canonical SHA-256: 6b78f8f35767357a7845073c83159cbd491668f488d43f5c6474edd7aaf446d7

\alpha_1

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/2/expression; canonical SHA-256: b093a0827982f8e6adf08c99c1d986e66d2d5c9bd57d20d9fff8c91ea4a21edf

On $B=B_1(0,1)$ and $K=B_1(0,R)$ with $L,R>0$, $\alpha_1=\varepsilon/(LR)$; $g(z)=f(Rz)/(LR)$ preserves the exact scalar-query budget, feasible output and per-instance seed guarantee.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs; canonical SHA-256: 8ca449b9f123bc0a86b6236ce00004cd031cb574db5b260b442fa0d92a915034

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/0; canonical SHA-256: 0b211755ce5d30b4d7d003b934f91ce9297d9ff5385ec2519ca9e2e8f58268e3

SO_ZO_E06cL__kimi001_20261124__p_alpha1

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/1; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/2; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/3; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/3; canonical SHA-256: aeff400713d8676cf86150bb4cbbc69a401abf1d0dfa8f48f09e17fc989edb86

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/3/symbol; canonical SHA-256: b5ab9b4623c8973607c2f07f07c78c0c8bbd3f0b610f53ae3443f8a02087b46b

A_1

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/3/expression; canonical SHA-256: 1471eb8fac1665cd5d470fb7dabb0ce903c8e26aaeb3246b91e0abd4d47a22b3

$A_1=1/\alpha_1$, $M_1=\min\{d,A_1^2\}$ and $\Lambda_1=\log(ed)+\log(eA_1)$ in the stated matched-l1 small-accuracy regions.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs; canonical SHA-256: 953c9d9e34ea7f1d05fc9d12a41dd4fea04630872223aad2669dec295d331492

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/0; canonical SHA-256: 28169715b67e0ddc981f7eac49c48859ae5723c5eed3a4e596b309cf5fb69abb

SO_ZO_E06cL__kimi001_20261124__p_A1

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/1; canonical SHA-256: 0b211755ce5d30b4d7d003b934f91ce9297d9ff5385ec2519ca9e2e8f58268e3

SO_ZO_E06cL__kimi001_20261124__p_alpha1

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/2; canonical SHA-256: f8e9fed04064b6ea5f17948fc50040eb14e1cc9c3de7d66a71791f290bf8b820

SO_ZO_E06cL__kimi001_20261124__p_M1

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/3; canonical SHA-256: 2567098c17b5a194642c4c881656f5b06d5504ac196f6b309b89429e3b659db7

SO_ZO_E06cL__kimi001_20261124__p_Lambda1

#### Native item 5

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/4; canonical SHA-256: 87d22f5899dba09d228f9a2ee4c52c4620fde18e6da59a7030fca371918f56a5

SO_ZO_E06cL_p_bb728db2b9

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: a6af48a092bc0ea9e1d1a2ca1e8a9a80c14982ada4e5098d2d4e60ff7eeb2be5

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 87d22f5899dba09d228f9a2ee4c52c4620fde18e6da59a7030fca371918f56a5

SO_ZO_E06cL_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 14c926c9d28b13570cc6649c35a25bcca11749a5e701b7107d22f70c3db13c49

SO_ZO_E06cL_p_4729bcfd1c

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 984ad179be4dd155621ff8b9f27d12e918e3e4681c1c37d59b82622207ad9b0e

SO_ZO_E06cL_p_73a0c205b0

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: d57e31d119d7067bc51944d2672f31f9f59b887f71088772300cf27efdbe3528

SO_ZO_E06cL_p_daa4cf7d79

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 4e935b9b80575efb7da0fd7e2bc527fe87ceb76bcabc0fc12d806e654d6ed8a1

SO_ZO_E06cL_p_5c322c6737

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 3e8a6aa7f2792d7437470daff2dad637353c60e95f4b4b9ab8a99630041006b0

SO_ZO_E06cL_p_5530ee35cd

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: 1a7c8e01a0c47200e802891f35b6ac47cb3e6089dfab6a77d8a93232ded5c055

SO_ZO_E06cL_p_16b7e5563d

#### Native item 8

Native pointer: /joint_analysis/target/uniform_in/7; canonical SHA-256: a873f1739d43a0722fb91b46c8e56859fa58fcc063e0cd719a75ccbe5d7c34a9

SO_ZO_E06cL_p_15881069d1

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[3] Arya Akhavan, Evgenii Chzhen, Massimiliano Pontil and Alexandre B. Tsybakov. A gradient estimator via L1-randomization for online zero-order optimization with two point feedback. NeurIPS 2022.

https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf

[4] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf

[5] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper

[6] Gorbunov, Dvurechensky and Gasnikov. An Accelerated Method for Derivative-Free Smooth Stochastic Convex Optimization. SIAM Journal on Optimization 32(2):1210--1238, 2022.

https://arxiv.org/abs/1802.09022

[7] Colombo_KIMI_001. Joint Dimension–Accuracy Complexity of Exact-Value Convex Optimization in Matched ℓ1 Geometry. Uploaded manuscript, Kimi K3.1 Pro, 2026-11-24.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_001/kimi_001.pdf

[8] Yin Tat Lee; Aaron Sidford; Santosh S. Vempala. Efficient Convex Optimization with Membership Oracles. arXiv:1706.07357v1, 22 June 2017.

https://arxiv.org/pdf/1706.07357
