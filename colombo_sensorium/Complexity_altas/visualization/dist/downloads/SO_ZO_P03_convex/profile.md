# Convex optimization with heavy-tailed samples: at most two values per sample

**Setting ID.** `SO_ZO_P03_convex`

Single-objective optimization

Convex population minimization from two exact values per hidden sample, under a sample Lipschitz r-moment bound. The r=3/2 slice has a logarithmic bracket for d>=2 and A>=max{d,2^17}; other documented parameter regions retain their stated dimension-accuracy gaps.

**Status.** Polynomial gap present

**Gap classes present.** Logarithmic gap; Polynomial gap

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; stochastic model: Sample function lipschitz r moment; structure: Expectation of sample functions

**ORACLE tags.** access order: Zeroth-order interface; interface family: Same sample paired value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $B_2(0,R)$ and return a point with small objective gap.

### Admissible model

Each sample function $F(\cdot;Z)$ is convex on $B_2(0,2R)$ and satisfies $\mathbb{E}|F(0;Z)|<\infty$, so $f(x)=\mathbb{E}[F(x;Z)]$ is well defined. The optimization domain is $B_2(0,R)$.

The sample Lipschitz coefficient $G(Z)$ satisfies $|F(x;Z)-F(y;Z)|\le G(Z)\|x-y\|_2$ and $\mathbb{E}[G(Z)^r]\le L^r$, with moment exponent $1<r\le2$.

### Oracle interface

A new sample handle corresponds to an independent draw of the hidden sample $Z$. Given its handle and $x\in B_2(0,2R)$, the interface returns the exact sample value $F(x;Z)$. The algorithm observes only handles and numerical values, not the underlying sample data or the complete sample function.

At most two paid evaluations are allowed per handle; the second point may depend on the first response. Distinct handles are independent.

Projection and the stated proximal operations over known geometry are free.

The public inputs are $d$, $L$, $R$, $r$, $\varepsilon$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in B_2(0,R)$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in B_2(0,R)}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One scalar sample-function value costs $1$ call; two points with the same sample handle or Markov state cost $2$ calls. Batches, initialization and repeated visits are charged per value. An empty handle supplies no free instance information.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$L$: Moment budget of the sample Lipschitz coefficient **Domain:** $L>0$.

$\mathbb{E}[G(Z)^r]\le L^r$

$R$: Feasible-ball radius **Domain:** $R>0$.

The output must belong to $B_2(0,R)$; the query radius is specified separately in the interface.

$r$: Moment exponent of the sample Lipschitz coefficient **Domain:** $1<r\le2$.

$\mathbb{E}[G(Z)^r]\le L^r$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$A$: Lipschitz accuracy ratio **Domain:** $A>0$.

$A=LR/\varepsilon$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $B_2(0,R)$.

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

$f_*=\inf_{x\in B_2(0,R)}f(x)$.

$Z,F(\cdot;Z)$: Hidden sample and its associated sample function **Domain:** Samples lie in an admissible probability space; each sample function is real-valued on the declared domain.

The population objective is the expectation under the sample distribution or stationary distribution.

$G(Z)$: Random sample Lipschitz coefficient **Domain:** $G(Z)\ge0$.

The model's difference inequality holds for each sample, with the moment budget fixed as specified here.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=B_2(0,R)$ and $\mathcal{X}=B_2(0,R)$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one paid scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime P03.R1

**Region.** Convex specification, $r=2$, $d\ge1$, $L,R>0$ and $0<\varepsilon\le LR/2^{17}$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(dL^2R^2/\varepsilon^2)
$$

**Upper bound.** B1

$$
O(dL^2R^2/\varepsilon^2)
$$

**Gap or comparison.** $O(1)$

### R2 - Other moment orders: joint dimension and accuracy gap

**Region.** Convex specification; fixed $1<r<2$, $r\ne3/2$, $d\ge2$, $L,R>0$, and $A=LR/\varepsilon\ge2^{17}$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega_r(\max\{dA^2,A^{r/(r-1)}\})
$$

**Upper bound.** B1

$$
O_r(d^{r/[2(r-1)]}A^{r/(r-1)})
$$

**Gap or comparison.** $O_r(d^{r/[2(r-1)]}A^{r/(r-1)}/\max\{dA^2,A^{r/(r-1)}\})$

### R3 - Three-halves moment: logarithmic dimension-accuracy bracket

**Region.** $r=3/2$, $d\ge2$, $L,R>0$, and $A=LR/\varepsilon\ge\max\{d,2^{17}\}$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Logarithmic gap

**Lower bound.** B7

$$
dA^3/131072
$$

**Upper bound.** B5, B6

$$
O\!\left(dA^3\min\{\sqrt d,[\log(edA)]^{3/2}\}\right)
$$

**Gap or comparison.** $O(\min\{\sqrt d,[\log(edA)]^{3/2}\})$

### R4 - Three-halves moment outside the Haar upper window

**Region.** $r=3/2$, $d\ge2$, $L,R>0$, and $16\le A=LR/\varepsilon<\max\{d,2^{17}\}$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Polynomial gap

**Lower bound.** B7

$$
dA^3/131072
$$

**Upper bound.** B5

$$
O(d^{3/2}A^3)
$$

**Gap or comparison.** $O(\sqrt d)$

### R5 - Parameter regime P03.R4

**Region.** Convex specification, $d=1$; fixed $1<r<2$, $L,R>0$ and $0<\varepsilon\le LR/2^{17}$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_r(A^{r/(r-1)})
$$

**Upper bound.** B1

$$
O_r(A^{r/(r-1)})
$$

**Gap or comparison.** $O_r(1)$

### R6 - Parameter regime P03.R_zero

**Region.** $\varepsilon\ge LR$.

**Quantity.** Q1

**Resource.** one paid scalar function value

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

### B1 - Clipped two-point estimation with projection and restarting

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathrm{Convex}:\quad O_r((\sqrt d\,LR/\varepsilon)^{r/(r-1)})
$$

**Sources.** [1](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Conditions.** Sample rth moment; $hL\le c\varepsilon$.

**Oracle correspondence.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HEAVY_UPPER

### B2 - Finite-second-moment subclass and a rare-nonzero-sample test

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathrm{Convex}:\ \Omega_r\!\left(\max\{d(LR/\varepsilon)^2,(LR/\varepsilon)^{r/(r-1)}\}\right)
$$

**Conditions.** The first term comes from P01; the second from the probability of observing a nonzero sample. The terms are not multiplied.

**Oracle correspondence.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_HEAVY_DIMENSION, ZO_PROOF_HEAVY_SPIKE

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Oracle correspondence.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO

### B4 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge LR$.

**Oracle correspondence.** Preserve sample handles and their reuse limits. Each queried point returns one sample value; sample data and sample gradients are not available for free.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** ZO_PROOF_ZERO

### B5 - Two-point robust stochastic mirror descent in Euclidean geometry

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(1+d^{3/2}A^3)
$$

**Sources.** [2](https://arxiv.org/abs/2304.02442v3)

**Conditions.** $r=3/2$, $d\ge2$, $A=LR/\varepsilon>1$.; Theorem 3.3 uses tail parameter $\kappa=1/2$, zero adversarial error, Euclidean primal and dual norms, and $\tau=\varepsilon/(4L)<R/4$.

**Dimension conditions.** $d\ge2$; no hidden dimension dependence in constants.

**Oracle correspondence.** A fresh independent hidden sample handle supplies at most two exact values on the declared query ball. Each scalar reply is charged. Choosing each pair before either reply is an allowed subclass of the within-handle adaptive interface.

**Guarantee conversion.** The source conclusion is per-instance expectation over algorithmic and sample randomness, with the objective instance fixed before expectation.

**Output rule.** The output is a feasible average of points in the known Euclidean ball; arbitrary feasible unqueried outputs remain allowed for lower bounds.

**Resource conversion.** The iteration count is deterministic; all paired sample evaluations are charged individually under a pathwise scalar-reply cap.

**Constants.** Universal constants because the moment order is fixed at 3/2.

**Local argument.** SO_ZO_P03_convex__kimi003_20261124__published_upper_mapping

**Source location.** [2](https://arxiv.org/abs/2304.02442v3) Theorem 3.3, Algorithm 1, Lemma 2.3, Assumptions 1-3; Euclidean specialization at kappa=1/2

Expected-error robust mirror descent upper bound under a three-halves sample Lipschitz moment, specialized to the exact two-value handle contract.

### B6 - Haar coordinate secants with scalar clipping and projected averaging

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(dA^3[\log(edA)]^{3/2})
$$

**Sources.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_003/kimi_003.pdf)

**Conditions.** $r=3/2$, $d\ge2$, $L,R>0$, and $A=LR/\varepsilon\ge\max\{d,2^{17}\}$.; $T=\lceil C_TA^3s^{3/2}\rceil$, $s=C_s\log(edA)$; each iteration uses $d$ fresh handles and exactly $2d$ replies.; The implemented algorithm uses its first random basis, never tests hidden-instance goodness and never performs the ghost rejection used in the analysis.

**Dimension conditions.** $d\ge2$; no hidden dimension dependence in constants.

**Oracle correspondence.** A fresh independent hidden sample handle supplies at most two exact values on the declared query ball. Each scalar reply is charged. Choosing each pair before either reply is an allowed subclass of the within-handle adaptive interface.

**Guarantee conversion.** The source conclusion is per-instance expectation over algorithmic and sample randomness, with the objective instance fixed before expectation.

**Output rule.** The output is a feasible average of points in the known Euclidean ball; arbitrary feasible unqueried outputs remain allowed for lower bounds.

**Resource conversion.** The iteration count is deterministic; all paired sample evaluations are charged individually under a pathwise scalar-reply cap.

**Constants.** Universal constants because the moment order is fixed at 3/2.

**Logarithmic factors.** $[\log(edA)]^{3/2}$, explicitly displayed.

**Source location.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_003/kimi_003.pdf) Theorem 1 and Section 4, especially Lemma 2 and equations (U6)-(U10)

Haar coordinate secants and scalar clipping attain O(d A^3 log(edA)^(3/2)) charged replies on the stated joint dimension-accuracy window.

### B7 - Rare informative linear samples and adaptive sphere-fiber posterior energy

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
dA^3/131072
$$

**Sources.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_003/kimi_003.pdf)

**Conditions.** $r=3/2$, $d\ge2$, $A=LR/\varepsilon\ge16$.; The hard family is $F_\theta(x;Z)=JB_0\langle\theta,x\rangle$, with $J\sim\operatorname{Bernoulli}((16/A)^3)$ and $B_0=LA^2/256$; thus $\mathbb EG^{3/2}=L^{3/2}$ and $F_\theta(0;Z)=0$.; Revealing the status of a handle only on its first paid query strengthens the oracle. Each informative handle supplies at most two adaptive linear measurements.

**Dimension conditions.** $d\ge2$; no hidden dimension dependence in constants.

**Oracle correspondence.** The stronger lower-bound oracle reveals the independent Bernoulli status only with the first charged reply. Unqueried handles reveal nothing; within-handle adaptive second queries are permitted. A lower bound for this stronger oracle applies to the declared interface.

**Guarantee conversion.** The source conclusion is per-instance expectation over algorithmic and sample randomness, with the objective instance fixed before expectation.

**Output rule.** The output is a feasible average of points in the known Euclidean ball; arbitrary feasible unqueried outputs remain allowed for lower bounds.

**Resource conversion.** The argument assumes a deterministic cap N on all scalar replies, counts at most N first paid handle accesses, and uses E K <= pN. No expected-work substitution is made.

**Constants.** Universal constants because the moment order is fixed at 3/2.

**Source location.** [3](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_003/kimi_003.pdf) Section 5, Lemma 3, and equations (L1)-(L9); final lower bound on page 11

The rare-direction lower construction is valid for every d>=2 and A>=16, and permits arbitrary within-handle adaptive second queries and arbitrary feasible outputs.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 266c9102891b4c3fa39a8b514cd38d2186f2355694d29fafc258e3e52a9cc678

### Native proof: ZO_PROOF_PAIRED_MOMENT

Native pointer: /proofs/0; canonical SHA-256: 1590ade2e6787fe33d10f650f8ab64ef46bf6350869f6f4f185dad60be780bd6

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 293f2ab735f268a2ffbfdb19ec489b03f31469acbe264107320d5061ad83ae63

Ball smoothing and the same-sample directional moment

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 3ad958d5da6f01b544d353454c3372bc69148946dc23d87a9f02d9c83e87957c

With ball smoothing $f_h(x)=\mathbb E_{U\sim\operatorname{Unif}(B_2)}f(x+hU)$ and a sphere direction $u$,
$$g_h(x)=\frac d{2h}[F(x+hu;Z)-F(x-hu;Z)]u,\quad\mathbb E g_h=\nabla f_h,\quad\mathbb E\|g_h\|^r\le(\sqrt{2d}L)^r.$$
For $r=2$, the bound is $2dL^2$.

For each fixed sample, the scalar difference $a(u)=F(x+hu;Z)-F(x-hu;Z)$ is odd on the sphere, hence has mean zero, and has Lipschitz constant at most $2hG$. Sphere Poincare gives $\mathbb E_u a(u)^2\le4h^2G^2/(d-1)$ for $d\ge2$. Thus $\mathbb E_u\|g_h\|^2\le d^2G^2/(d-1)\le2dG^2$; for $d=1$ the difference quotient is directly bounded by $G$. Apply Jensen only to the direction expectation and then integrate over the sample:
$$\mathbb E_{Z,u}\|g_h\|^r\le\mathbb E_Z(\mathbb E_u\|g_h\|^2)^{r/2}\le(2d)^{r/2}\mathbb E G^r.$$
No second moment of $G$ is needed when $r<2$. The divergence theorem for ball convolution gives the unbiasedness identity. Integrability follows from the Lipschitz difference bound. Convexity gives $f_h\ge f$, and $|f_h-f|\le hL$; mean strong convexity is preserved on the region where every translated point satisfies it. All statements hold conditionally on the past when the next sample and direction are fresh. Reusing an old adaptively explored sample does not automatically preserve this conditional moment calculation.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8b49ec7dca2985f462ed168dfff1ed752288e50486b8b7133d5d5ea0e91edc18

A fresh sample each round; the same sample supplies both values; sample Lipschitz modulus $G$ on the stated query neighborhood; $\mathbb E G^r\le L^r$, $1<r\le2$.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/0/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 2b913a5fb0aabb726f77d1aae7fd6ffc8d2d2a43974d8a9a576b6ed5f74e86bc

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 7ec8d4ed8f91c132a1de87534a55d39252f47d06682b98ca5b170368ee0a8388

SO_SRC_072506cc03b2f8a7

### Native proof: ZO_PROOF_HEAVY_UPPER

Native pointer: /proofs/1; canonical SHA-256: 49461dadc4f72d597d91cd48446ffe6bdb72a7b46c1d893c9bef5c98d1ede88f

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 843b2530c2a21f3276e95d7ae08cc6dceee00aafb8db7976dd5a60a522a6bb0f

Clipped projected methods with a local $r$-moment budget

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 4cc9c4b79d0891946e8457e09a93adbc5fb0e65bc9b3490343d19b31b00c21a8

Put $q=(r-1)/r$ and $M=\sqrt{2d}L$. The convex upper is $O_r((\sqrt d\,LR/\varepsilon)^{1/q})$ and the strongly convex upper is $O_r((dL^2/(\mu\varepsilon))^{1/(2q)})$.

Run the projected algorithm on $K_h=B_2(R-h)$. Every smoothing translate then lies in $B_2(R)$, where mean strong convexity is promised. The shrinkage comparator $(1-h/R)x_*$ and smoothing together cost at most $2hL$. The paired-moment lemma gives $\mathbb E[\|g_t\|^r\mid\mathcal F_t]\le M^r$. For $v_t=g_t\min\{1,b_t/\|g_t\|\}$, its conditional bias and total second moment obey
$$B_t\le M^rb_t^{1-r},\qquad V_t\le M^rb_t^{2-r}.$$
For the convex case take $b=MT^{1/r}$ and $\eta=R/(MT^{1/r})$. Projection and convexity yield
$$2\eta\mathbb E\delta_t\le\mathbb ED_t-\mathbb ED_{t+1}+4\eta RB+\eta^2V.$$
Since $D_1\le R^2$, averaging gives $\mathbb E[f_h(\bar x_T)-\min_Kf_h]\le3RMT^{-q}$. Adding at most $2hL$ for smoothing and comparator shrinkage, choose $h=\min\{R/2,\varepsilon/(4L)\}$ and $T\ge(6RM/\varepsilon)^{1/q}$. Each round costs two values.

For the strongly convex case take $b_t=M(t+1)^{1/r}$ and $\eta_t=4/[\mu(t+1)]$, starting at $t=1$. The inequality $2B_t\sqrt{D_t}\le(\mu/2)D_t+2B_t^2/\mu$ gives
$$\mathbb ED_{t+1}\le(1-\mu\eta_t/2)\mathbb ED_t-2\eta_t\mathbb E\delta_t+\eta_t^2V_t+(2\eta_t/\mu)B_t^2.$$
Divide by $2\eta_t$ and multiply by $t$. The distance terms are $\mu[t(t-1)D_t-t(t+1)D_{t+1}]/8$, and the remainder is at most $(3M^2/\mu)t(t+1)^{-2q}$. They telescope from a zero initial coefficient. As $0<q\le1/2$, $\sum_{t=1}^Tt(t+1)^{-2q}\le T^{2-2q}$. Weighted averaging therefore gives gap at most $6M^2/(\mu T^{2q})+2hL$. Choose $T\ge(12M^2/(\mu\varepsilon))^{1/(2q)}$ and the same $h$.

The feasible minimizer can lie on the boundary; no stationary unconstrained minimizer or additional gradient self-bounding assumption is used. Fixed success follows from a constant-factor tighter expectation target and Markov. Constants may depend on fixed $r$ and are not asserted uniform as $r\downarrow1$.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 8ea00a83fe8321454ca16027ad2bedbf396179f9c8c05b01fab169bf57147cef

Sample/query domain $B_2(2R)$; optimization/output domain $B_2(R)$; fresh paired samples; $1<r\le2$ fixed. Mean strong convexity is sufficient for the strongly convex branch.

#### Native field: limitations

Native pointer: /proofs/1/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/1/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: module_dependencies

Native pointer: /proofs/1/module_dependencies; canonical SHA-256: 0f93027dd13c1fc76f53eafc5f7af337161f3e067e9523895d0587c084c781f1

#### Native item 1

Native pointer: /proofs/1/module_dependencies/0; canonical SHA-256: 89f132536e860e550967b3b720a81cd0588e96be63dd5faf8219129f756df13e

ZO_PROOF_PAIRED_MOMENT

### Native proof: ZO_PROOF_PAIRED_LOWER

Native pointer: /proofs/2; canonical SHA-256: 23e8b6ab205035010c77798f8526fe66fab436df338037cbbd95ec8445415922

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: f942cbbe7824686be5c800748b33cb9610ebd0b97d2396148811f8630bb932f8

A joint dimension and accuracy lower bound under a second-moment sample budget

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: 7a017c193ac5644f7fea8baedd68fd4f269a73651796938a9640f4bedcecb322

For $L\ge2\mu R$,
$$\mathfrak R_T\ge\left[\frac{16\mu T}{dL^2}+\frac{8\pi^2}{\mu R^2}\right]^{-1}.$$
In particular, $0<\varepsilon\le\mu R^2/(16\pi^2)$ requires $T\ge dL^2/(32\mu\varepsilon)$.

Use $F_\theta(x;Z)=\mu\|x\|^2/2+\langle Z,x\rangle$, with $Z\sim N(\theta,(v^2/d)I)$, $v^2=L^2/8$, and $\|\theta\|\le a=\mu R/2$. The mean minimizer is $-\theta/\mu\in B_2(R/2)$, and objective loss is $\|\widehat\theta-\theta\|^2/(2\mu)$ for $\widehat\theta=-\mu\widehat x$. On the query ball a sample Lipschitz modulus is $\mu R+\|Z\|$, whose second moment is at most $2\mu^2R^2+2a^2+2v^2\le7L^2/8$ under the stated slack. Every sample is itself $\mu$-smooth and $\mu$-strongly convex.

Subtracting the known quadratic leaves linear observations of $Z$. Within one sample, project a new query vector onto the complement of its previously observed span. Its conditional innovation has variance $(v^2/d)\|x_\perp\|^2$ and Fisher trace $d/v^2$ if nonzero; a dependent query gives no new information. The adaptive query rule is fixed once the previous transcript is conditioned on and contributes no extra Fisher term. Thus $T$ charged scalars contribute total trace at most $Td/v^2$, even with unlimited paid reuse.

Give each coordinate of $\theta$ the density $(\sqrt d/a)\cos^2(\pi\sqrt d\,u/(2a))$ on $[-a/\sqrt d,a/\sqrt d]$. It is supported in the legal parameter ball and has total prior Fisher information $\pi^2d^2/a^2$. The vector van Trees inequality gives
$$\mathbb E\|\widehat\theta-\theta\|^2\ge\frac{d^2}{Td/v^2+\pi^2d^2/a^2}.$$
Divide by $2\mu$ and substitute $v,a$. Gaussian Lipschitz moduli are unbounded random variables; this construction proves a second-moment-model lower bound, including its sample-smooth and paid-reuse variants, but not a uniform almost-sure Lipschitz lower bound.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: adbb67937b1cae57cce62e36d7422d818327a44b97c2c19d7023d1802efd9e9d

Independent Gaussian sample functions; arbitrary adaptive scalar queries and even paid unlimited reuse of each sample; expected objective error under a fixed call cap.

#### Native field: limitations

Native pointer: /proofs/2/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/2/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

### Native proof: ZO_PROOF_HEAVY_DIMENSION

Native pointer: /proofs/3; canonical SHA-256: dbb7a6c3f5f582c3bf96b424fe2cb44a1445caab29901179d3d9de553aa748f1

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: b7d253db45eb886400bf2f5a57349c18e234ad73546e0217ec30eb5ba890d58d

The second-moment subclass supplies the heavy-tail dimension lower bound

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: fcc8d890d984f5da74b22123ef6559a98b681f367ba4d8578e4bdbc343b749ba

For $L\ge8\mu R$ and $\varepsilon\le\mu R^2/4096$, fixed success $2/3$ requires $T>dL^2/(256\mu\varepsilon)$. The expected-error version uses $768$ and the window $\varepsilon\le\mu R^2/12288$. The convex class inherits $\Omega(dL^2R^2/\varepsilon^2)$ on a sufficiently small explicit window.

Use the Gaussian linear-quadratic samples from the paired lower lemma, now with $v^2=L^2/4$ and $\|\theta\|\le a\le\mu R/2$. Their Lipschitz modulus on $B_2(2R)$ is $2\mu R+\|Z\|$. Minkowski and $L\ge8\mu R$ give $(\mathbb EG^2)^{1/2}<L$, hence $\mathbb EG^r\le L^r$.

For a fixed-success argument take the untruncated analysis prior $\theta\sim N(0,s^2I)$. Every new scalar innovation adds rank-one precision with trace at most $d/v^2$, including adaptively reused labels. Conditional posterior covariance satisfies
$$S=\operatorname{tr}\Sigma\ge\frac{ds^2}{1+Ts^2/v^2}.$$
For any transcript-measurable estimator, Gaussian integration and Markov give $\Pr(\|\theta-\widehat\theta\|^2\le b\mid\text{transcript})\le\sqrt{eb/S}$. Choose $a^2=1024\mu\varepsilon$ and $s^2=a^2/(16d)$. The legal event $\|\theta\|\le a$ has probability at least $15/16$. If $T\le v^2/s^2=dL^2/(256\mu\varepsilon)$, then $S\ge32\mu\varepsilon$. Objective success implies squared error at most $b=2\mu\varepsilon$, giving unconditional probability at most $\sqrt e/4<1/2$. But success $2/3$ on every legal instance would imply unconditional probability at least $(15/16)(2/3)=5/8$, a contradiction. The radius condition follows from $\varepsilon\le\mu R^2/4096$.

Expected gap at most $\varepsilon$ implies $2/3$ success at error $3\varepsilon$ by Markov, giving the stated expected lower. For the convex class choose the hard subclass curvature $\mu_0=12288\varepsilon/R^2$. When $\varepsilon\le LR/98304$, the slack condition holds and the expected lower becomes a universal constant times $dL^2R^2/\varepsilon^2$. This curvature is a choice inside the proof, not a new public parameter of the convex model.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: fed5d4b4990c7672518cc8ec4896f2bf1359abb278c930edb917f800a69b8a90

The local $r$-moment class on $B_2(2R)$, $1<r\le2$; fixed-success and expected-error variants are distinguished.

#### Native field: limitations

Native pointer: /proofs/3/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/3/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

#### Native field: module_dependencies

Native pointer: /proofs/3/module_dependencies; canonical SHA-256: 348b00944b32d6e8ee8513d4bda976456e091eb962495a1d0c76c16dbdcf98a7

#### Native item 1

Native pointer: /proofs/3/module_dependencies/0; canonical SHA-256: 8f998de2e5d6e6728b2c2615547cb53961f27f8f79f09b2509382d0d9483e76b

ZO_PROOF_PAIRED_LOWER

### Native proof: ZO_PROOF_HEAVY_SPIKE

Native pointer: /proofs/4; canonical SHA-256: 7aa18d3d5597d9e715702b5fd31cddbdb0b03ab5d372be5b9298fffb84d8974c

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 8834da127b8e4e8ccd6e46d887d1579999b5b43e42a4faa05f4cbf452203dde4

Rare-spike testing supplies a separate heavy-tail accuracy lower bound

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: e81016d3ff3bc5c4902cda7a69e71aa9ecc0983896b6dd24b3d4111a02b8cf08

With $q=(r-1)/r$, the convex lower is $\Omega_r((LR/\varepsilon)^{1/q})$ and the strongly convex lower is $\Omega_r((L^2/(\mu\varepsilon))^{1/(2q)})$. Combine these with dimension lower bounds by a maximum, never a product.

For a sign $s\in\{-1,1\}$, let a fresh label give $Z_s=0$ with probability $1-\pi$ and $Z_s=sB$ with probability $\pi$. For the convex family set $F_s(x;Z)=Z_sx_1$, $B=L\pi^{-1/r}$, and mean slope $m=L\pi^q=4\varepsilon/R$. Thus $\pi=(4\varepsilon/(LR))^{1/q}\le1/2$ when $\varepsilon\le LR/8$, and $\mathbb E\operatorname{Lip}(F)^r=L^r$. Even reveal the full $Z$ at each charged fresh-label query. With probability $(1-\pi)^T$ the first $T$ labels are all zero and the two transcripts agree. At a common output, the average gap of the two signs is exactly $mR=4\varepsilon$. Expected error at most $\varepsilon$ therefore requires $T\ge\log4/[2\pi]$. The two success sets are disjoint, so the fixed-success version follows from failure probability at least $(1-\pi)^T/2$.

For strong convexity add the common term $\mu\|x\|^2/2$. Use noise budget $L_0=L/2$ and $m=L_0\pi^q=4\sqrt{\mu\varepsilon}$, so $\pi=(8\sqrt{\mu\varepsilon}/L)^{1/q}$. Under $L\ge8\mu R$ and $\varepsilon\le\mu R^2/64$, both minimizers lie in $B_2(R/2)$ and $\pi\le1/2$. On $B_2(2R)$, Minkowski gives $(\mathbb E(2\mu R+|Z|)^r)^{1/r}\le3L/4$. On the all-zero transcript the average gap is at least $m^2/(2\mu)=8\varepsilon$. The same testing argument yields $T\ge\log8/(2\pi)$, and disjoint success balls give the fixed-success form. The full sample function is random; this is not an independent additive-value-noise model.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 1e97c81f3a3e7e6b97db617819b14e6ffaa923ecc71cffd494f885be0ef713c4

Any paid scalar query can access at most one new sample label; repeated access to a zero label is uninformative. Both expected-error and fixed-success guarantees are covered.

#### Native field: limitations

Native pointer: /proofs/4/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/4/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

### Native proof: ZO_PROOF_ZERO

Native pointer: /proofs/5; canonical SHA-256: 1d6580814630c8e2805d1bef988f17262747efcfe8580ea0d6eaace3086f220c

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: a1c4db43e97db238b9e152f2d0f29dccb6ee901b91806fdf8840d239abdee28f

Zero-query certificates

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: e337fe1bbdc7a8471c27bff8578ac9695fda39f5bd738324501658aee12cbc83

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: 1415baad26ae3bdb7a7f19af0ab941587cafa672fc7447677224c888ab47c12b

The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

#### Native field: limitations

Native pointer: /proofs/5/limitations; canonical SHA-256: d1bbc07ef50fae6de1ba167edc51c87b2aa1290f00e732d359785af5f606d21c

#### Native item 1

Native pointer: /proofs/5/limitations/0; canonical SHA-256: e9d58ffd13d1e57cf0514abf00beb521f4079e5d6034541c0bf100c0037e9afc

Local argument and specification transfer; cited external theorems remain primary dependencies.

### Native proof: SO_ZO_P03_convex__kimi003_20261124__published_upper_mapping

Native pointer: /proofs/6; canonical SHA-256: d9cbe2c430a024d1d11848be7495dec7872b37b6650f93f1a9a5c04ea8ff859f

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: 1a0ae1f37d8c5e99db17954de2d8b2051b206d3b994c1984a1d07e83d5a726d8

Euclidean three-halves-moment specialization of two-point robust mirror descent

#### Native field: scope

Native pointer: /proofs/6/scope; canonical SHA-256: 23d21b609d0997a24c50d081eb735a18cddf1c03e13190011b910b9aacc2d81a

$r=3/2$, $d\ge2$, $A>1$; sample/query domain $B_2(0,2R)$ and optimization/output domain $B_2(0,R)$.

#### Native field: body

Native pointer: /proofs/6/body; canonical SHA-256: c25bae52560bdea5964c6960954c442b746e7892ef264e3e722346be7294bd93

Apply Theorem 3.3 of Kornilov, Gasnikov, Dvurechensky and Dvinskikh (2023) with $\kappa=1/2$, zero adversarial value perturbation, and Euclidean primal and dual norms. Their sample assumptions are exactly convexity and a bounded $(1+\kappa)$-moment of the sample Lipschitz coefficient on the smoothing neighborhood. The theorem's Lemma 2.3 gives $\sigma_2\le C\sqrt d\,L$ at this fixed moment order. The Euclidean cubic uniformly convex prox has distance parameter $R_0\le C'R$ with universal constants, so Theorem 3.3 gives
$$\mathbb E[f(\bar x_T)-f_*]\le2L\tau+C''R\sqrt d\,L\,T^{-1/3}.$$
Choose $\tau=\varepsilon/(4L)=R/(4A)$ and $T=\lceil(2C''\sqrt d\,A)^3\rceil$. For $A>1$, a feasible iterate and either smoothing perturbation lie in $B_2(0,R+\tau)\subset B_2(0,2R)$. The paired evaluations use one fresh sample per iteration and no more than two values from it. Pair locations are selected before observing either value, which is permitted by the larger adaptive-two-query algorithm class. The deterministic count is exactly $2T$ scalar replies, and the averaged output lies in $B_2(0,R)$. This yields $O(1+d^{3/2}A^3)$ replies with the profile's per-instance expected-error guarantee. For $A\ge16$ the additive constant is absorbed in $O(d^{3/2}A^3)$.

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: cfeeb47cb5866564599574eeef2a6804fa44945d7b7740c7672c1aa60ae7746a

#### Native item 1

Native pointer: /proofs/6/source_refs/0; canonical SHA-256: ac57fceda22253974aef0a19f3819efa0235bf77da993cf3029ae649d3ccaa5a

KORNILOV_GASNIKOV_DVURECHENSKY_DVINSKIKH_2023

## References

[1] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. JMLR 18(52):1--11, 2017.

https://jmlr.org/papers/volume18/16-632/16-632.pdf

[2] Nikita Kornilov; Alexander Gasnikov; Pavel Dvurechensky; Darina Dvinskikh. Gradient-Free Methods for Non-Smooth Convex Stochastic Optimization with Heavy-Tailed Noise on Convex Compact. 2023. arXiv:2304.02442v3, 24 August 2023.

https://arxiv.org/abs/2304.02442v3

[3] Colombo_KIMI_003. Near-Optimal Dimension–Accuracy Complexity for Two-Point Stochastic Convex Optimization with Heavy Tails. Uploaded manuscript, Kimi K3.1 Pro, 2026-11-24.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/COLOMBO_KIMI_003/kimi_003.pdf
