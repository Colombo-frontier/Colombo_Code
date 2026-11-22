# Nonconvex first-order stationarity with ordinary value-gradient and rich full-Hessian jets: joint fixed budgets

**Setting ID.** `SO_HO_HOI08_S_joint`

Single-objective optimization

Minimize the number of ordinary calls under a prescribed rich-call cap, retaining the native joint (G,H) resource. The randomized lower and deterministic upper match in the stated logarithmic-dimension, small-rich-budget window.

**Status.** Quantified zero-rich gap in a recorded subwindow; Lower rates not registered in remaining windows; Joint frontier only partly characterized

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Ordinary rich full jets; interface family: Typed exact derivative jet; operation: Joint ordinary rich jets; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Gradient norm

**GUARANTEE tags.** mode: Probability; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Joint budget; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point with gradient norm at most the prescribed tolerance for a globally Hessian-Lipschitz, possibly nonconvex objective.

### Admissible model

The unknown objective f:R^d->R is C^2, has a finite infimum, and obeys f(x_0)-inf f<=Delta at the public initial point x_0.

For every x,y in R^d, ||H_f(x)-H_f(y)||_op<=L_2||x-y||_2. There is no bound on ||H_f(x)||, no separate gradient-Lipschitz parameter, and no convexity assumption.

The normalized class is F_d(T)={u in C^2(R^d): inf u> -infinity, u(0)-inf u<=T, Lip(H_u)<=1}. Its target is ||grad u||<=1.

The Delta=0 endpoint is included by a local argument. A positive public L_2 may bound an instance whose actual Hessian Lipschitz constant is zero; the separate parameter case L_2=0 is not part of this profile.

### Oracle interface

At any point, choose an ordinary response containing the value and full gradient, or a rich response containing the value, full gradient and full Hessian.

One rich call increments H only. Its included value and gradient do not also increment G. An ordinary call increments G only. Full Hessians are returned, not Hessian-vector products.

Queries may be arbitrary exact-real vectors with arbitrarily small positive separations. No radius, span, periodic-access rule, sampling interface, or weighted price is imposed.

### Output

Return an arbitrary point in R^d. The output may be unqueried.

### Loss or accuracy criterion

The target is the gradient norm itself; no squared-norm or expected-error conversion is implicit.

### Resource accounting

Both caps hold on every execution path, including unsuccessful runs. Initialization, repeated responses and all actual stopping checks are charged. Expected query counts are not substituted.

The principal scalar comparison minimizes the ordinary cap G subject to the prescribed rich cap H<=h. The native joint feasible region is retained as a second quantity.

Policies enforce caps even on counterfactual histories, terminating before an excess call. Internal work is uncharged but must terminate in finitely many measurable steps on every legal input; no uniform arithmetic-time bound is required.

A feasible pair must be witnessed by one algorithm. Coordinatewise upper bounds from unrelated algorithms are not combined into a joint pair.

### Algorithm views and success guarantees

Arbitrary measurable adaptive policies may use a private random seed independent of the fixed input. Queries and outputs are unrestricted exact-real points.

Finite parameter-dependent advice is allowed when independent of the unknown instance. No span, Krylov or zero-respecting condition is imposed.

Every adopted upper witness is deterministic; every cited main lower bound applies to unrestricted randomized policies.

Probability is over the algorithm seed after fixing the objective. There is no oracle noise. Deterministic witnesses succeed on every instance and therefore satisfy this view.

**Native accounting.** An ordinary response contains $(f,\nabla f)$ and costs one $G$; a rich response contains $(f,\nabla f,\nabla^2f)$ and costs one $H$ only. Both budgets are fixed pathwise caps.

**Matching window.** With $T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$, constant-factor matching is asserted for $T\ge T_0$, $d\ge C_{\rm dim}\log(2+T)$, $1\le h$ and $h+1\le aT$. The two branch rows partition this window. Other rows keep their own guards.

**Joint scope.** The joint row gives proved feasible pairs and conditional necessary inequalities. It does not identify the whole Pareto frontier, the sharp rich-only threshold, or all results in the literature.

## 2. Notation and parameters

$d$: Ambient dimension, retained explicitly in every rate. **Domain:** $d\in\mathbb N_{\ge1}$.

$\Delta$: Public upper bound on the initial objective gap. **Domain:** $\Delta\ge0$.

$L_2$: Public positive upper bound on the global Hessian Lipschitz constant in operator norm. **Domain:** L_2>0.

$\varepsilon$: Target Euclidean gradient norm. **Domain:** $\varepsilon>0$.

$h$: Prescribed integer cap on rich calls; rich calls include a full Hessian and do not increment the ordinary counter. **Domain:** $h\in\mathbb N_0$.

$T$: Dimensionless second-order scale. **Domain:** $T\ge0$.

$$
T=\Delta\sqrt{L_2}/\varepsilon^{3/2}
$$

$\bar T$: Enlarged normalized gap used only for global upper bounds. **Domain:** $\bar T\ge1$.

$$
\bar T=\max\{1,T\}
$$

$k(h,T)$: Legal rich cap used by the extended mixed upper witness. **Domain:** $k\in\mathbb N_0$.

$$
k(h,T)=\min\{h,\lfloor\bar T\rfloor\}
$$

$H_{\rm cub}$: A sufficient, explicit rich-only budget; not the optimal rich-only threshold. **Domain:** $H_{\rm cub}\in\mathbb N_{\ge2}$.

$$
H_{\rm cub}=\lfloor12T\rfloor+2
$$

$a$: One fixed absolute lower-theorem constant, reduced below one if necessary. **Domain:** 0<a<1.

$C_{\rm dim}$: Absolute sufficient dimension constant in the source lower theorem; no numerical value is asserted. **Domain:** $C_{\rm dim}>0$.

$T_0$: A fixed absolute threshold at least $\max\{T_*,1,2/a\}$; enlarging the source threshold permits the h=0 monotonicity consequence. **Domain:** $T_0\ge\max\{T_*,1,2/a\}$.

$G,H$: Realized numbers of ordinary and rich responses; G excludes every rich call. Caps use the same letters in joint inequalities. **Domain:** $G,H\in\mathbb N_0$.

$C_0,C_1,C_U,c_L$: Absolute upper/lower constants; no d,h,Delta,L_2,epsilon dependence is hidden. **Domain:** Positive absolute constants.

$\mathcal F_d(T),Q_g^\star,\mathcal B^\star$: Normalized instance class, cap-slice minimax complexity and joint feasible cap region. **Domain:** As defined in MODEL and QUANTITIES.

$\uparrow S$: Coordinatewise upward closure of attainable nonnegative integer budget pairs, without convexification. **Domain:** $S\subseteq\mathbb N_0^2$.

$$
\uparrow S=\{b:\exists a\in S,\ a\preceq b\}
$$

$O,\Omega,\Theta$: Uniform rate bounds using only absolute constants in their stated parameter windows. **Domain:** Each bound retains its explicit regime conditions.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{aligned}&Q_g^\star(h;d,T)=\min\{g\in\mathbb N_0:\exists A,\\[3pt]&\forall f,\omega:\ G_A(f,\omega)\le g,\ H_A(f,\omega)\le h;\\[3pt]&\forall f:\Pr_\omega[\|\nabla f(\widehat x_A)\|\le\varepsilon]\ge2/3\}\end{aligned}
$$

**Definition.** Minimum ordinary cap under a prescribed rich cap

**Scope.** documented_parameter_windows

**Optimization direction.** minimize

A single algorithm, chosen using only public inputs, must terminate on every legal instance and path. T is obtained by a one-response-for-one-response rescaling. Q_g counts ordinary calls only, excluding gradients included in rich calls.

#### Q2 - feasible resource region

$$
\begin{aligned}&\mathcal B^\star(d,T)=\{(g,h)\in\mathbb N_0^2:\exists A\text{ satisfying main/g1 with }\\[3pt]&(G_A,H_A)\preceq(g,h)\text{ on every path}\}\end{aligned}
$$

**Definition.** Joint feasible ordinary/rich budget region

**Scope.** documented_parameter_windows

**Optimization direction.** coordinatewise_minimize

The set is upward closed. Its h-slice satisfies Q_g^star(h;d,T)=min{g:(g,h) in B^star}. Bounds below describe proved attainable families and conditional necessary constraints, not an exact global frontier.

### R1 - Matching dimension-dependent branch

**Region.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\quad 1\le h,\\[3pt]&h+1\le aT;\quad d\le(T/h)^{3/2}\end{aligned}
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Optimal

**Lower bound.** B5

$$
\Omega(Td^{1/3})
$$

**Upper bound.** B4

$$
O(Td^{1/3})
$$

**Gap or comparison.**

$$
\Theta(1)
$$

### R2 - Matching rich-budget-dependent branch

**Region.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\quad 1\le h,\\[3pt]&h+1\le aT;\quad d>(T/h)^{3/2}\end{aligned}
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Optimal

**Lower bound.** B5

$$
\Omega(T^{3/2}/\sqrt h)
$$

**Upper bound.** B4

$$
O(T^{3/2}/\sqrt h)
$$

**Gap or comparison.**

$$
\Theta(1)
$$

### R3 - Zero-rich matching subwindow

**Region.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\quad h=0;\\[3pt]&d\le T^{3/2}\end{aligned}
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega(Td^{1/3})
$$

**Upper bound.** B1

$$
O(Td^{1/3})
$$

**Gap or comparison.**

$$
\Theta(1)
$$

### R4 - Zero-rich dimension larger than T^(3/2)

**Region.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\quad h=0;\\[3pt]&d>T^{3/2}\end{aligned}
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Other quantified gap

**Lower bound.** B6

$$
\Omega(T^{3/2})
$$

**Upper bound.** B1

$$
O(d+Td^{1/3})=O(d)
$$

**Gap or comparison.**

$$
O((d+Td^{1/3})/T^{3/2})=O(d/T^{3/2})
$$

### R5 - Zero initial gap: no calls

**Region.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad \Delta=0$

**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Optimal

**Lower bound.** B9

$$
0
$$

**Upper bound.** B7

$$
0
$$

**Gap or comparison.** Exact equality at zero; no multiplicative division by zero.

### R6 - Sufficient rich budget: zero ordinary calls

**Region.** 

$$
d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad \Delta>0,\quad h\ge H_{\rm cub}=\lfloor12T\rfloor+2
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Optimal

**Lower bound.** B9

$$
0
$$

**Upper bound.** B8

$$
0
$$

**Gap or comparison.** Exact ordinary count zero; the sufficient rich threshold is not claimed sharp.

### R7 - Small normalized scale

**Region.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad 0<T<T_0,\quad h<H_{\rm cub}$

**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B3

$$
U(h;d,T)
$$

**Gap or comparison.** A nontrivial lower rate is not adopted in this update.

### R8 - Below the logarithmic dimension threshold

**Region.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d<C_{\rm dim}\log(2+T),\\[3pt]&h<H_{\rm cub}\end{aligned}
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B3

$$
U(h;d,T)
$$

**Gap or comparison.** A nontrivial lower rate is not adopted in this update.

### R9 - Beyond the source rich-budget window

**Region.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\\[3pt]&1\le h<H_{\rm cub},\quad h+1>aT\end{aligned}
$$



**Quantity.** Q1

**Resource.** Minimize G subject to the separate hard cap H<=h; G excludes every rich call.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B3

$$
U(h;d,T)
$$

**Gap or comparison.** The transition to zero ordinary calls is not characterized by the adopted results.

### R10 - Joint feasible region: proved pieces

**Region.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$

**Quantity.** Q2

**Resource.** Native pair of fixed caps (G,H), using coordinatewise order.

**Status.** Joint budget unresolved

**Achievable budgets.** B10

**Necessary constraints.** B11

**Gap or comparison.** No globally matching joint frontier is asserted.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Ordinary=(value, full gradient); rich=(value, full gradient, full Hessian), rich charged only to H.

**Guarantee mapping.** Per-fixed-instance success at least 2/3. Upper witnesses are deterministic; main lower source covers unrestricted randomized algorithms.

**Output mapping.** Arbitrary point in R^d, possibly unqueried.

**Resource mapping.** Fixed caps on every path, including all initialization and actual checks; no weighted cost or periodic oracle restriction.

### B1 - Proposition A.1(ii), applied at enlarged gap max{1,T}, with H=0

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
Q_g^\star(h;d,T)\le C_0\bigl(d+\bar T d^{1/3}\bigr)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A2

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(ii), finite-difference ordinary-only implementation

Retains O(d+T d^(1/3)); dropping the additive d requires the separate absorption proof.

### B2 - Proposition A.1(i) with k=min{h,floor(max{1,T})}; H<=k<=h

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
Q_g^\star(h;d,T)\le C_1\bar T^{3/2}/\sqrt{k(h,T)}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad h\ge1$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A2

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(i), prescribed-rich-cap translation of NALEN

Includes a deterministic witness with at most h rich calls, and explicit ordinary initialization/stopping accounting.

### B3 - Choose the better legal deterministic witness from the public parameters

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\begin{gathered}Q_g^\star(h;d,T)\le U(h;d,T),\\[5pt]U(h;d,T)=\begin{cases}C_0(d+\bar T d^{1/3}),&h=0,\\\min\{C_0(d+\bar T d^{1/3}),C_1\bar T^{3/2}/\sqrt{k(h,T)}\},&h\ge1.\end{cases}\end{gathered}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A2

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(ii), finite-difference ordinary-only implementation

Retains O(d+T d^(1/3)); dropping the additive d requires the separate absorption proof.

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(i), prescribed-rich-cap translation of NALEN

Includes a deterministic witness with at most h rich calls, and explicit ordinary initialization/stopping accounting.

### B4 - NALEN adaptations with explicit absorption of the ordinary initialization cost

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
Q_g^\star(h;d,T)\le C_U\min\{Td^{1/3},T^{3/2}/\sqrt h\}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge1,\quad 1\le h\le T$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A2

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(ii), finite-difference ordinary-only implementation

Retains O(d+T d^(1/3)); dropping the additive d requires the separate absorption proof.

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(i), prescribed-rich-cap translation of NALEN

Includes a deterministic witness with at most h rich calls, and explicit ordinary initialization/stopping accounting.

### B5 - Theorem 3.1: fixed-input randomized lower tradeoff

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
Q_g^\star(h;d,T)\ge c_L\min\{Td^{1/3},T^{3/2}/\sqrt{h+1}\}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** 

$$
\begin{aligned}&d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\quad 1\le h,\\[3pt]&h+1\le aT\end{aligned}
$$



**Dimension conditions.**

$$
d\ge C_{\rm dim}\log(2+T)
$$

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 5; 6; 28; 29; theorem: Theorem 3.1; Section 15 parameter optimization

Only the displayed T,d,h window is adopted. The main construction was not independently re-proved.

### B6 - Monotonicity in the allowed rich cap, using Theorem 3.1 at h=1

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
Q_g^\star(0;d,T)\ge Q_g^\star(1;d,T)\ge c_L\min\{Td^{1/3},T^{3/2}/\sqrt2\}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** 

$$
d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad T\ge T_0,\quad d\ge C_{\rm dim}\log(2+T),\quad h=0
$$



**Dimension conditions.**

$$
d\ge C_{\rm dim}\log(2+T)
$$

**Local argument.** A1, A3

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 5; 6; 28; 29; theorem: Theorem 3.1; Section 15 parameter optimization

Only the displayed T,d,h window is adopted. The main construction was not independently re-proved.

### B7 - Return the public initial global minimizer

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
Q_g^\star(h;d,0)=0\quad\text{with }(G,H)=(0,0)
$$

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad \Delta=0$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A4

### B8 - Explicit cubic-regularization argument with all rich checks counted

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
Q_g^\star(h;d,T)=0\quad\text{if }h\ge H_{\rm cub}=\lfloor12T\rfloor+2;\quad(G,H)\preceq(0,H_{\rm cub})
$$

**Sources.** [4](https://doi.org/10.1007/s10107-006-0706-8)

**Conditions.** 

$$
d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2};\quad \Delta>0,\quad h\ge H_{\rm cub}=\lfloor12T\rfloor+2
$$



**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A4

### B9 - Query caps are nonnegative integers

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
Q_g^\star(h;d,T)\ge0
$$

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A4

### B10 - Same-algorithm witnesses and upward closure

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\begin{aligned}&\uparrow\mathcal A(d,T)\subseteq\mathcal B^\star(d,T),\\[4pt]&\mathcal A(d,T)=\{(\lceil C_0(d+\bar Td^{1/3})\rceil,0),(0,H_{\rm cub})\}\\[4pt]&\quad\cup\{(\lceil C_1\bar T^{3/2}/\sqrt j\rceil,j):1\le j\le\lfloor\bar T\rfloor\};\\[4pt]&T=0\Rightarrow(0,0)\in\mathcal B^\star\end{aligned}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2) [4](https://doi.org/10.1007/s10107-006-0706-8)

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A2, A4, A5

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(ii), finite-difference ordinary-only implementation

Retains O(d+T d^(1/3)); dropping the additive d requires the separate absorption proof.

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 31; 32; theorem: Appendix A, Proposition A.1(i), prescribed-rich-cap translation of NALEN

Includes a deterministic witness with at most h rich calls, and explicit ordinary initialization/stopping accounting.

### B11 - Conditional slice lower bounds as necessary constraints on the same joint budget pair

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\begin{gathered}(G,H)\in\mathcal B^\star(d,T),\ T\ge T_0,\ d\ge C_{\rm dim}\log(2+T)\\[5pt]\Longrightarrow\ \begin{cases}G\ge c_L\min\{Td^{1/3},T^{3/2}/\sqrt{H+1}\},&1\le H,\ H+1\le aT,\\G\ge c_L\min\{Td^{1/3},T^{3/2}/\sqrt2\},&H=0.\end{cases}\end{gathered}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

**Conditions.** $d\in\mathbb N_{\ge1},\ \Delta\ge0,\ L_2>0,\ \varepsilon>0,\ h\in\mathbb N_0;\quad T=\Delta\sqrt{L_2}/\varepsilon^{3/2}$; the positive necessary inequalities are conditional on $T\ge T_0$ and $d\ge C_{\rm dim}\log(2+T)$, with their respective H guards.

**Dimension conditions.** $d\in\mathbb N_{\ge1}$; any additional conditional dimension guard is retained in the formula.

**Local argument.** A1, A3, A5

**Source location.** [1](https://arxiv.org/pdf/2610.22208v2) pdf pages: 5; 6; 28; 29; theorem: Theorem 3.1; Section 15 parameter optimization

Only the displayed T,d,h window is adopted. The main construction was not independently re-proved.

## 5. Local arguments

### A1 - Exact rescaling without an extra initial value query

The physical and normalized models have identical achievable pairs of query caps.

1. Set s=sqrt(epsilon/L\_2) and u(z)=f(x\_0+s z)/(epsilon s). A vertical constant is deliberately not subtracted, so no query for f(x\_0) is needed.

2. grad u(z)=grad f(x\_0+s z)/epsilon and H\_u(z)=(s/epsilon)H\_f(x\_0+s z). Thus Lip(H\_u)<=s^2 L\_2/epsilon=1; u(0)-inf u<=Delta/(epsilon s)=T. Also ||grad u||<=1 is equivalent to ||grad f||<=epsilon.

3. One native ordinary or rich response gives exactly the corresponding normalized response by known scalar multiplication, preserving its type. The inverse mapping f(x)=epsilon s u((x-x\_0)/s) gives the converse simulation. Outputs, per-instance success, pathwise caps and finite measurable termination are preserved.

4. This applies for L\_2>0 and epsilon>0, including Delta=0. It establishes source-model transfer; it does not impose a Hessian-norm bound.

**Limits of the argument.** Local argument for this exact oracle, guarantee and resource contract; source-dependent premises retain their stated parameter conditions.

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

### A2 - Literal rich caps, upper-envelope extension, and additive-d absorption

The generic upper and the two matching branches follow from the two explicitly translated NALEN implementations.

1. Proposition A.1(ii) gives H=0 and G<=C\_0(d+T d^(1/3)) for T>=1; A.1(i) gives H<=h and G<=C\_1 T^(3/2)/sqrt(h) for every integer 1<=h<=T.

2. For any T>=0 the normalized class with gap T is a subclass of the class with gap Tbar=max{1,T}. The pure-ordinary witness therefore gives the global ordinary upper. If h>=1, k=min{h,floor(Tbar)} is an integer in [1,Tbar], and the mixed witness obeys H<=k<=h. Selecting by public upper bounds yields U(h;d,T).

3. If T>=1, 1<=h<=T and d<=(T/h)^(3/2), then d^(2/3)<=T/h<=T and hence d<=T d^(1/3). The pure-ordinary upper is at most a constant times T d^(1/3).

4. If d>(T/h)^(3/2), the mixed upper is at most a constant times T^(3/2)/sqrt(h). Thus the minimum-form upper holds for all 1<=h<=T, without a lower-dimension requirement.

5. On the source lower window, h<=h+1<=2h. If A=T d^(1/3) and B=T^(3/2)/sqrt(h), then min{A,B/sqrt(1+1/h)}>=min{A,B}/sqrt(2). This matches both branches by absolute constants; no logarithm in d or h is discarded.

6. Strict cap detail from Appendix A: choose m=ceil(A\_0(T/h)^(3/2)) and N=hm, with snapshots at 0,m,...,(h-1)m. The number of rich snapshots is at most h; ordinary initialization and stationarity tests are included in the bound <=3N+1. For the zero-rich version, symmetrized coordinate differences approximate each Hessian with d+1 ordinary queries; m=d gives total O(d+T d^(1/3)). The small finite-difference steps are legal because exact-real precision is uncharged.

**Limits of the argument.** Local argument for this exact oracle, guarantee and resource contract; source-dependent premises retain their stated parameter conditions.

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

### A3 - A guarded zero-rich lower consequence

At h=0, the adopted lower is Omega(min{T d^(1/3),T^(3/2)}) when T>=T\_0 and d>=C\_dim log(2+T).

1. Any algorithm with rich cap zero is admissible under rich cap one with the same ordinary cap. Hence Q\_g^star(0)>=Q\_g^star(1).

2. Because T\_0>=2/a, the source condition h+1<=aT holds at h=1. The other lower-theorem conditions are exactly the h0\_lower regime. Substituting h=1 yields c\_L min{T d^(1/3), T^(3/2)/sqrt(2)}.

3. For d<=T^(3/2), the ordinary upper has d<=T d^(1/3), and the lower is at least c\_L T d^(1/3)/sqrt(2); this establishes a constant-factor bracket.

4. For d>T^(3/2), the adopted lower is c\_L T^(3/2)/sqrt(2), whereas the available pure-ordinary upper is O(d+T d^(1/3))=O(d). The recorded gap is O(d/T^(3/2)); no optimality claim follows.

5. This consequence does not claim that the explicit h=0 parameter theorem has been fully optimized, or that these are all existing zero-rich results.

**Limits of the argument.** Local argument for this exact oracle, guarantee and resource contract; source-dependent premises retain their stated parameter conditions.

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

### A4 - Zero-gap endpoint and an explicit rich-only sufficient cap

Delta=0 allows no calls; for any Delta>0, G=0 and H<=floor(12T)+2 suffice.

1. If Delta=0 then the differentiable objective attains its global infimum at the public x\_0. Its gradient is zero, so return x\_0 with no response. Nonnegativity of caps proves exact ordinary complexity zero.

2. For Delta>0, at the current point request one rich jet (f,g,H). If ||g||<=epsilon, return. Otherwise select a global minimizer s of the known coercive cubic model m(s)=g^T s+(1/2)s^T Hs+(L\_2/3)||s||^3, and move to x+s. A measurable global-minimizer choice is an allowed uncharged internal operation.

3. Hessian Lipschitz continuity gives f(x+s)<=f(x)+g^T s+(1/2)s^T Hs+(L\_2/6)||s||^3. Since m(s)<=m(0)=0, f(x)-f(x+s)>=(L\_2/6)||s||^3.

4. Model stationarity gives g+Hs+L\_2||s||s=0. The gradient Taylor remainder has norm at most (L\_2/2)||s||^2, so ||grad f(x+s)||<=(3L\_2/2)||s||^2.

5. If the next point fails the target, then ||s||>(2epsilon/(3L\_2))^(1/2); its objective decrease is greater than [(1/6)(2/3)^(3/2)]epsilon^(3/2)/sqrt(L\_2) and hence greater than epsilon^(3/2)/(12sqrt(L\_2)). There can be at most floor(12T) such failing next points.

6. One initial rich check and the final successful rich check therefore give H<=floor(12T)+2, while G=0 throughout. All intermediate checks are included. The gap bounds the number of iterations and the model solve is finite under the permitted abstract measurable-operation convention.

7. This explicit proof is supplied for the present contract. Nesterov-Polyak is a background reference for cubic regularization, not a claim that its theorem uses the displayed constant 12. No optimality is asserted for H\_cub itself.

**Limits of the argument.** Local argument for this exact oracle, guarantee and resource contract; source-dependent premises retain their stated parameter conditions.

**Sources.** [4](https://doi.org/10.1007/s10107-006-0706-8)

### A5 - Direction-preserving transfer from cap slices to joint budgets

The joint record retains attainable pairs and conditional necessary constraints without inventing a global Pareto curve.

1. The ordinary-only algorithm has a single fixed pair (ceil(C\_0(d+Tbar d^(1/3))),0). For each integer j in [1,floor(Tbar)], the mixed algorithm has the single pair (ceil(C\_1 Tbar^(3/2)/sqrt(j)),j). The cubic algorithm has (0,H\_cub). At T=0 return x\_0 for (0,0).

2. Increasing either cap preserves feasibility for the same algorithm, proving upward closure of these attainable pairs. Randomly mixing algorithms, taking convex hulls of budgets, or merging their separate coordinate minima is neither needed nor justified.

3. If one algorithm witnesses a feasible pair (G,H), then by definition G>=Q\_g^star(H;d,T). Applying the main lower at this same H yields the joint conditional inequality when 1<=H and H+1<=aT. For H=0 use the separate monotonicity proof. Both require the displayed scale and dimension conditions.

4. No necessary constraint is inferred in a region where these premises are absent. Thus the paired record does not certify the full feasible region, the smallest zero-ordinary threshold, or an exact large-rich transition.

**Limits of the argument.** Local argument for this exact oracle, guarantee and resource contract; source-dependent premises retain their stated parameter conditions.

**Sources.** [1](https://arxiv.org/pdf/2610.22208v2)

## References

[1] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Gradient-Hessian Query Tradeoffs: Matching Lower Bounds in Logarithmic Dimension. arXiv:2610.22208v2; PDF version dated 2026-10-19; inspected 2026-11-22.

https://arxiv.org/pdf/2610.22208v2

[2] Lesi Chen; Chengchang Liu; Luo Luo; Jingzhao Zhang. Faster Newton Methods for Convex and Nonconvex Optimization in Gradient Complexity. Official proceedings record inspected 2026-11-22; related arXiv:2501.17488.

https://proceedings.mlr.press/v336/chen26a.html

[3] Deeksha Adil; Brian Bullins; Aaron Sidford; Chenyi Zhang. Balancing Gradient and Hessian Queries in Non-Convex Optimization. Official proceedings PDF inspected 2026-11-22; related arXiv:2510.20786.

https://proceedings.neurips.cc/paper_files/paper/2025/hash/3dc910c921507a5d51d3dac0202b2618-Abstract-Conference.html

[4] Yurii Nesterov; Boris T. Polyak. Cubic regularization of Newton method and its global performance. Bibliographic identity checked against GH26 references; direct DOI content not retrieved in this session..

https://doi.org/10.1007/s10107-006-0706-8
