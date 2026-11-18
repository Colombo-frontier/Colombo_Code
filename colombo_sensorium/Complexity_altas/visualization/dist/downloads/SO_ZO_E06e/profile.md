# Euclidean Lipschitz convex optimization on a broad norm ball with exact values

**Setting ID.** `SO_ZO_E06e`

Single-objective optimization

Minimize $f$ globally over $B_p(0,R)$ and return a point with small objective gap.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz function; structure: No additional structure

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $B_p(0,R)$ and return a point with small objective gap.

### Admissible model

$2\le p\le\infty$. The function $f:\mathbb{R}^d\to\mathbb{R}$ is globally convex.

For every $x,y\in\mathbb{R}^d$, $|f(x)-f(y)|\le L\|x-y\|_2$.

The optimization domain is $B_p(0,R)$, and boundary minimizers are allowed. The ball is not assumed to contain an unconstrained minimizer.

### Oracle interface

At any finite query point $x$ in $\mathbb{R}^d$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $L$, $R$, $p$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_p(0,R)$. The output may be an unqueried point, an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in B_p(0,R)}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

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

$L$: Public upper bound on the objective Lipschitz constant **Domain:** $L>0$.

$|f(x)-f(y)|\le L\|x-y\|_2$ throughout the function domain specified in this profile.

$R$: Radius of the non-Euclidean feasible ball **Domain:** $R>0$.

The feasible set is $B_p(0,R)$.

$p$: Norm exponent of the feasible or localization ball **Domain:** $2\le p\le\infty$.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$R_E$: Euclidean circumradius of the norm ball **Domain:** $R_E>0$.

$R_E=Rd^{1/2-1/p}$, $2\le p\le\infty$.

$A_E$: Lipschitz accuracy normalized by the Euclidean circumradius **Domain:** $A_E>0$.

$A_E=LR_E/\varepsilon$

$d_0$: Universal dimension threshold required by the lower bound **Domain:** $d_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$C_0$: Universal threshold for the linear-image construction or accuracy window **Domain:** $C_0>0$.

Determined by the applicable theorem conditions; retain a symbolic threshold when no numerical value is supplied.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $B_p(0,R)$.

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

$f_*=\inf_{x\in B_p(0,R)}f(x)$.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=B_p(0,R)$ and $\mathcal{X}=B_p(0,R)$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

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

### R1 - Parameter regime E06e.R1

**Region.** $d\ge d_0,\ C_0\le A_E^2\le d,\ C_0\ge64$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega(dA_E^2/\log(eA_E^2))
$$

**Upper bound.** B1, B2

$$
\ O(dA_E^2\log(edA_E))
$$

**Gap or comparison.** $O(\log(edA_E)\log(eA_E^2))$

### R2 - Parameter regime E06e.R2

**Region.** $d\ge d_0,\ A_E^2\ge\max\{C_0,d\},\ C_0\ge64$.

**Views.** Deterministic

**Quantity.** Q1

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B3

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B1, B2

$$
O(d^2\log(ed)\log(e+A_E))
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+A_E))$

### R3 - Parameter regime E06e.R5

**Region.** $A_E\le1$.

**Views.** Deterministic; Randomized

**Quantity.** Q1; Q2

**Resource.** one exact scalar function value

**Status.** Optimal

**Lower bound.** B5, B11

$$
0
$$

**Upper bound.** B4, B10

$$
0
$$

### R4 - Parameter regime E06e.R1

**Region.** $d\ge d_0,\ C_0\le A_E^2\le d,\ C_0\ge64$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B9

$$
\Omega(dA_E^2/\log(eA_E^2))
$$

**Upper bound.** B6, B7, B8

$$
\ O(dA_E^2)
$$

**Gap or comparison.** $O(\log(eA_E^2))$

### R5 - Parameter regime E06e.R2

**Region.** $d\ge d_0,\ A_E^2\ge\max\{C_0,d\},\ C_0\ge64$.

**Views.** Randomized

**Quantity.** Q2

**Resource.** one exact scalar function value

**Status.** Logarithmic gap

**Lower bound.** B9

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B6, B7, B8

$$
O(d^2\log(ed)\log(e+A_E))
$$

**Gap or comparison.** $O(\log^2(ed)\log(e+A_E))$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+d^2\log(d+1)\log(e+A_E))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; the minimum with the randomized two-point upper bound may also be used.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Protasov normalization in Proposition 4, with a known distance penalty; pdf pages: 12; printed pages: 12

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Protasov normalization in Proposition 4, with a known distance penalty

### B2 - Deterministic approximate subgradient extraction

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(dA_E^2\log(edA_E)\right)
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $\varepsilon\le LR_E/8$; projection onto the public domain; exact full-space values, or queries within the shrunken body justified by the accompanying argument.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

### B3 - Random support-function hard family on a broad norm ball

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{d\min\{d,A_E^2\}}{\log(e\min\{d,A_E^2\})}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [5](https://arxiv.org/abs/1802.09022) [6](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [3](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [7](https://arxiv.org/pdf/1707.08486v2)

**Conditions.** $d\ge d_0,\ A_E^2\ge C_0$; the universal threshold ensures $m\ge m0$ and $\varepsilon \le \varepsilon _Z Lr_m$, uniformly over $p\ge 2$.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Local argument.** A5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Theorem 5, PDF/printed page 12: nonsmooth hard family ; Proposition 4, PDF/printed page 12

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

### B4 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $A_E\le1$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B5 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $A_E\le1$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B6 - Two-point descent or localization on the Euclidean circumscribed ball

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Randomized witness

$$
O(1+dA_E^2)
$$

**Sources.** [3](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [5](https://arxiv.org/abs/1802.09022) [6](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [1](https://arxiv.org/html/2610.00345v1)

**Conditions.** Randomized; a known Euclidean proximal function on K has range $\le R_E^2/2$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A4

**Source location.** [3](https://jmlr.org/papers/volume18/16-632/16-632.pdf) theorem: Theorem 1 and Corollary 2, specialized to a fixed objective; pdf pages: 4; printed pages: 4

**Source location.** [3](https://jmlr.org/papers/volume18/16-632/16-632.pdf) theorem: Theorem 1 and Corollary 2, specialized to a fixed objective

### B7 - Deterministic convex localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O(1+d^2\log(d+1)\log(e+A_E))
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [1](https://arxiv.org/html/2610.00345v1) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; the minimum with the randomized two-point upper bound may also be used.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Protasov normalization in Proposition 4, with a known distance penalty; pdf pages: 12; printed pages: 12

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Protasov normalization in Proposition 4, with a known distance penalty

### B8 - Deterministic approximate subgradient extraction

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(dA_E^2\log(edA_E)\right)
$$

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

**Conditions.** Deterministic; $\varepsilon\le LR_E/8$; projection onto the public domain; exact full-space values, or queries within the shrunken body justified by the accompanying argument.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A2

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Proposition 4, PDF/printed page 12: deterministic value localization

### B9 - Random support-function hard family on a broad norm ball

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{d\min\{d,A_E^2\}}{\log(e\min\{d,A_E^2\})}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper) [5](https://arxiv.org/abs/1802.09022) [6](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [3](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [7](https://arxiv.org/pdf/1707.08486v2)

**Conditions.** $d\ge d_0,\ A_E^2\ge C_0$; the universal threshold ensures $m\ge m0$ and $\varepsilon \le \varepsilon _Z Lr_m$, uniformly over $p\ge 2$.

**Guarantee conversion.** The source gives a necessary query count at constant success probability for arbitrary adaptive randomized algorithms. A higher fixed success requirement inherits the same lower bound.

**Local argument.** A5

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

**Source location.** [2](https://arxiv.org/html/2607.16558v2) theorem: Theorem 5, PDF/printed page 12: nonsmooth hard family ; Proposition 4, PDF/printed page 12

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Theorems 3.1 and 3.3, PDF page 5; Propositions I.1 and J.8; Lemma K.5 and Appendix M ; Appendix C.2; Appendix N.4, PDF pages 81–82 ; Lemma K.13, PDF page 70 ; Theorems 3.1 and 3.3; geometric transfer definitions

### B10 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $A_E\le1$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

### B11 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $A_E\le1$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A6

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

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

### A2 - Deterministic extraction of an approximate subgradient

**Scope.** Exact real scalar values; finite positive probe scales; free real arithmetic and no bit-precision charge. Ball-restricted variants keep all probes inside the ball; global variants allow all-space probes.

A deterministic procedure obtains an $\eta$-accurate subgradient at a point within distance $\zeta$ of the requested point using at most $7d\lceil\log_2(2L\sqrt d/\eta)\rceil$ values. It yields the convex upper $O(dA^2\log(edA))$ and the strongly convex upper $O(dL^2\log(edA)/(\mu\varepsilon))$, with $A=LR/\varepsilon$.

For a convex one-dimensional restriction, maintain an active interval whose every subderivative lies in $[\ell,u]$. Divide it into six equal pieces and query its seven grid points. Their secant slopes satisfy $s_0\le\cdots\le s_5$. The intervals $[q_1,q_2]$ and $[q_4,q_5]$ have protected subgradient envelopes $[s_0,s_2]$ and $[s_3,s_5]$. Since $(s_2-s_0)+(s_5-s_3)\le u-\ell$, selecting the narrower one halves the envelope width and divides the interval length by six.

Set $\tau=\eta/\sqrt d$, $k=\lceil\log_2(2L/\tau)\rceil$, and $r_1=\zeta/2$. At coordinate $j$, run $k$ subdivisions from half-width $r_j$, move to the final midpoint, and retain the two protected secants of denominator $h_j=2r_j6^{-k}$. Set $r_{j+1}=\tau h_j/(16L)$. Then $r_{j+1}/r_j\le1/8$, and all later displacement is at most $\tau h_j/(8L)$. Translating a protected secant by this displacement changes its slope by at most $\tau/4$. Thus every subgradient of the final common point $y$ has coordinate $j$ in $[\ell_j-\tau/4,u_j+\tau/4]$. The midpoint vector differs from every such subgradient by at most $3\eta/4$ in Euclidean norm. All probe and protection points lie within $\zeta$ of the original point. The scales may be very small, but are positive and require the same finite number of queries.

For a globally Lipschitz convex function and a public projected set $K\subseteq B_2(R)$ containing zero, the extracted vector satisfies
$$f(z)\ge f(x)+\langle\widehat g,z-x\rangle-2L\zeta-2R\eta\quad(z\in K).$$
Choose $\zeta=\varepsilon/(16L)$, $\eta=\varepsilon/(16R)$, so the model error is $\varepsilon/4$ and $\|\widehat g\|\le2L$ in the stated nontrivial range. Projected subgradient descent with step $R/(2L\sqrt N)$ gives averaged gap at most $2LR/\sqrt N+\varepsilon/4$. Taking $N\ge64A^2$ proves the convex rate. The probes may leave $K$ only in the all-space variant.

For a function defined on the ball, keep iterates in $B_2(R-2\delta)$. For strong convexity, apply extraction to $h(x)=f(x)-\mu\|x\|^2/2$, which is convex and at most $2L$-Lipschitz because $\mu R\le L$. Choose $\delta=\gamma/(16L)$, vector error $\eta=\gamma/(8R)$, and add $\mu x$ back. Then $\|\widehat g\|\le4L$ and
$$f(z)\ge f(x)+\langle\widehat g,z-x\rangle+\mu\|z-x\|^2/2-\gamma.$$
With $a_t=2/[\mu(t+1)]$, projection, and $D_t=\|x_t-x_*\|^2$,
$$f(x_t)-f(x_*)-\gamma\le\frac{\mu(t-1)}4D_t-\frac{\mu(t+1)}4D_{t+1}+\frac{16L^2}{\mu(t+1)}.$$
Multiply by $t$ and sum. The initial distance coefficient is zero, and the remaining distance terms telescope. The weighted average has gap at most $32L^2/[\mu(T+1)]+\gamma$. Taking $\gamma=\varepsilon/8$ and $T+1\ge128L^2/(\mu\varepsilon)$, including shrinkage loss at most $2L\delta$, proves the result. Ordinary convex projected descent gives the $A^2$ branch. Deterministic value localization supplies the separate $d^2\log(ed)\log(4A)$ branch; take the minimum only among applicable branches.

For a known body $B_2(r_{\rm in})\subseteq K\subseteq B_2(R_{\rm out})$, the identity $(1-a)K+aB_2(r_{\rm in})\subseteq K$ supplies feasible probe room. Choose $a=\gamma/(16LR_{\rm out})$ and probe radius at most $ar_{\rm in}/2$. Shrinkage costs at most $LaR_{\rm out}$. The query count is independent of the probe radius and uses $R_{\rm out}$ in place of $R$. A finite-sum mean value costs $n$ component values, multiplying these deterministic bounds by $n$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://arxiv.org/html/2607.16558v2) [4](https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper)

### A3 - Image-radius lower bounds and their admissible windows

**Scope.** Exact values; the original all-space query/output reduction and all source dimension and accuracy windows are retained.

For an $m$-dimensional Euclidean image radius $r_m(B,K)>0$, smooth and Lipschitz lower bounds may be maximized over the integers $m$ for which their source windows hold.

Define $r_m(B,K)$ as the largest radius of a Euclidean ball contained in $AK$, maximized over maps with $\|A\|_{B\to2}\le1$. Dorn et al., Theorem 3.1, gives
$$T\ge\max\left\{5m/16,\ (m/4096)\min\{m,\sqrt{\beta r_m^2/\varepsilon}\}\right\},\quad0<\varepsilon\le\beta r_m^2/32.$$
Theorem 3.3, with its regularization parameter zero, gives
$$T\ge c_Z\frac{m\min\{m,(Lr_m/\varepsilon)^2\}}{\log(e\min\{m,(Lr_m/\varepsilon)^2\})},\quad m\ge m_Z^\circ,\quad0<\varepsilon\le\varepsilon_ZLr_m.$$
The all-space nonsmooth transfer uses the source's radial penalty for its homogeneous support-function hard family: a target query is simulated by one bounded source query and known arithmetic, and radial decoding preserves the output comparison. This permits the stronger all-space target queries without silently importing a bounded-query lower bound.

For $B=B_q$ and $K=B_p(R)$, put $\theta=(1/2-1/q)_++(1/p-1/2)_+$ and $\gamma=(1/q-1/p)_+$. The source's block certificate is
$$r_m\ge R\lfloor d/m\rfloor^\gamma m^{-\theta},\qquad r_d=Rd^{-\theta}.$$
Insert this certificate into each theorem before maximizing over legal $m$. For $q=2$ and $p\le2$, this is $r_m\ge Rm^{-t}$, $t=1/p-1/2$. Other source certificates, such as constant-radius quotient images, may be added only with their own operator-norm and dimension conditions. An exact geometric radius does not itself prove a matching optimization upper bound.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [2](https://arxiv.org/html/2607.16558v2)

### A4 - Randomized directional methods with explicit norm budgets

**Scope.** The direction distribution, prox norm, regularity norm, query domain, and randomness are distinct parts of the statement.

The applicable randomized upper bounds are
$$O(1+d\sqrt{\eta_{d,s}\beta_2\Theta_s/\varepsilon}),\quad O(1+d\eta_{d,s}\beta_2\Theta_s/\varepsilon),$$
$$O(1+L^2\Theta_s d^{1+2/\min(q,2)-2/s}/\varepsilon^2),\quad O(1+dv_H L_2^2\Theta_H/\varepsilon^2).$$

For the smooth directional methods take $d\ge8$, $1\le s\le2$, $s^*=s/(s-1)$, and $\eta_{d,s}=\min\{s^*-1,16\log d-8\}d^{2/s^*-1}$. Gorbunov, Dvurechensky, and Gasnikov's theorems apply to Euclidean smoothness $\beta_2$ and a prox divergence bounded by $\Theta_s$. Exact noiseless values use batch size one and two scalar values per direction; a finite positive difference scale can be chosen small enough for the fixed budget.

For the Lipschitz method of Akhavan et al., $q$ is the regularity norm and $s$ is the prox norm. Their theorem gives expected gap at most $11.9L\sqrt{\Theta_s d^{1+2/\min(q,2)-2/s}/T}$, with two values per round. Tightening the target by a factor three and applying Markov's inequality gives success probability $2/3$. A usable prox is
$$t_s=\max\{s,1+1/\log(ed)\},\quad a_{s,d}=\frac{d^{2(1/s-1/t_s)}}{t_s-1},\quad\omega_s(x)=a_{s,d}\|x\|_{t_s}^2/2.$$
It is 1-strongly convex in $\ell_s$ and on $B_p(R)$ has range at most $a_{s,d}R^2d^{2(1/t_s-1/p)_+}/2$. In particular, $q=2$, $s=p\le2$ gives the advertised $a_{p,d}d^{2/p^*}(LR/\varepsilon)^2$ term.

For Shamir's general-prox bound let $v_H=(\mathbb E\|U\|_{H,*}^4)^{1/2}$ for a uniform Euclidean sphere direction. Use ball convolution as the smoothed function, with sphere directions in its gradient estimator. The divergence identity belongs to the ball average; this formulation preserves convexity, Lipschitzness, the $O(hL_2)$ smoothing bias, and the source variance proof. All these witnesses are randomized, even when their value oracle is exact and deterministic.

For $B=K=B_1(R)$, Euclidean conversion gives $\beta_2=d\beta$, while the $\ell_1$ prox and directional factor contribute $\Theta_1=O(R^2\log(ed))$ and $\eta_{d,1}=O(\log(ed)/d)$. Substitution yields $O(1+d\log(ed)\sqrt{\beta R^2/\varepsilon})$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [5](https://arxiv.org/abs/1802.09022) [6](https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf) [3](https://jmlr.org/papers/volume18/16-632/16-632.pdf) [1](https://arxiv.org/html/2610.00345v1)

### A5 - Wide balls and the smooth $2\le q\le p$ region

**Scope.** A public $\ell_p$ localization ball; global smooth or Lipschitz regularity as declared; all-source accuracy and dimension windows remain explicit.

For Euclidean regularity and $p\ge2$, an image dimension $m\asymp d$ has radius $r_m\gtrsim R_E=Rd^{1/2-1/p}$. For smooth regularity $2\le q\le p$, the corresponding radius is $R_q=Rd^{1/q-1/p}$, and a randomized upper is $O(1+d\sqrt{\beta R_q^2/\varepsilon})$.

Let $s=p^*\in[1,2]$ and take a $d\times m$ Gaussian matrix $G$. For each fixed unit vector $u$, $Gu$ is standard Gaussian, $\mathbb E\|Gu\|_s\asymp d^{1/s}$ uniformly in $s$, and its Euclidean Lipschitz constant is $d^{1/s-1/2}$. Gaussian concentration gives a lower-tail probability $\exp(-cd)$. On the event $\|G\|_{2\to2}\le C\sqrt d$, a sufficiently fine fixed net in $\mathbb R^m$, followed by the bound $\|G\|_{2\to s}\le d^{1/s-1/2}\|G\|_{2\to2}$, extends the estimate to all unit vectors when $m\le c_0d$. Thus some $G$ satisfies both bounds. Put $A=G^\top/(C\sqrt d)$. Then $\|A\|_{2\to2}\le1$ and
$$h_{AB_p(R)}(u)=R\|A^\top u\|_{p^*}\ge cRd^{1/2-1/p}\|u\|_2.$$
Support-function separation gives the claimed ball inclusion. Dividing $A$ by $d^{1/2-1/q}$ makes it an $\ell_q\to\ell_2$ contraction and changes the radius to $cR_q$. Insert the resulting certificate into the image-radius lower theorems.

For the smooth upper choose a public real orthogonal matrix $U$ with $|U_{ij}|\le\sqrt{2/d}$ and set $g(y)=f(Uy)$. Coordinate smoothness satisfies $\beta_i\le2\beta d^{2/q-1}$. Also $f(0)-f_*\le\beta R_q^2/2$ and $\|U^\top x_*\|_2^2\le R^2d^{1-2/p}$. The initial potential in the accelerated randomized coordinate theorem is at most $3\beta R_q^2/2$, so its rate is $O(d\sqrt{\beta R_q^2/\varepsilon})$ rounds, two exact values per round. Declare an arbitrarily small positive error upper bound for the exact oracle and use the source's positive finite-difference scale; this avoids a zero-scale substitution. The perturbation budget can be chosen from the public potential bound to keep accumulated error below $\varepsilon/3$ at the fixed cap.

This coordinate witness is randomized. The Euclidean norm-converted deterministic upper remains a separate bound. For the Lipschitz wide-ball upper, use the Euclidean two-point estimator with radius $R_E$, or deterministic localization; only the compatible minimum is taken.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [7](https://arxiv.org/pdf/1707.08486v2) [1](https://arxiv.org/html/2610.00345v1)

### A6 - Zero-query certificates

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

[2] Haihan Zhang, Chenheng Zhang, Zhiquan Qi and Zhouchen Lin. Near-Optimal Lower Bounds for Randomized Algorithms in Exact Value Zeroth-Order Convex Optimization. arXiv:2607.16558v2, 2026-07-30.

https://arxiv.org/html/2607.16558v2

[3] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf

[4] V. Yu. Protasov. Algorithms for approximate calculation of the minimum of a convex function from its values. Mathematical Notes 59(1):69--74, 1996.

https://www.mathnet.ru/php/archive.phtml?jrnid=mzm&option_lang=eng&paperid=1697&wshow=paper

[5] Gorbunov, Dvurechensky and Gasnikov. An Accelerated Method for Derivative-Free Smooth Stochastic Convex Optimization. SIAM Journal on Optimization 32(2):1210--1238, 2022.

https://arxiv.org/abs/1802.09022

[6] Arya Akhavan, Evgenii Chzhen, Massimiliano Pontil and Alexandre B. Tsybakov. A gradient estimator via L1-randomization for online zero-order optimization with two point feedback. NeurIPS 2022.

https://proceedings.neurips.cc/paper_files/paper/2022/file/329ef22fd8cb68223d5df09a037f7dd9-Paper-Conference.pdf

[7] Pavel Dvurechensky, Alexander Gasnikov, Alexander Tyurin and Vladimir Zholobov. Unifying Framework for Accelerated Randomized Methods in Convex Optimization. arXiv:1707.08486v2, 2020-12-16; locators refer to version 2.

https://arxiv.org/pdf/1707.08486v2
