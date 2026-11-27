# Strongly convex–strongly concave saddle points: exact joint gradients and squared distance.

**Setting ID.** `CV_S_SCSC`

Minimax optimization

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$, with $z=(x,y)$.

**Status.** Polynomial gap present; Bounds missing

**TASK tags.** formulation: Strongly convex strongly concave saddle; solution concept: Joint squared distance; task family: Minimax

**MODEL tags.** convexity: Strong concavity in the declared block; convexity: Strong convexity in the declared block; convexity: Strongly convex strongly concave; initialization: Initial distance; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; interface family: Exact joint gradient; operation: Payoff joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Squared distance

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$, with $z=(x,y)$.

### Admissible model

The spaces are $X=\mathbb R^{d_x}$ and $Y=\mathbb R^{d_y}$.

The function $f$ is jointly $\beta$-smooth, uniformly $\mu_x$-strongly convex in $x$, and uniformly $\mu_y$-strongly concave in $y$; $\beta\ge\max\{\mu_x,\mu_y\}>0$.

A unique saddle point $z^\star$ exists, and the public initial point satisfies $\|z_0-z^\star\|_2\le R$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $R^2$, $\beta$, $\varepsilon$, $\mu_x$, and $\mu_y$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
z\in X\times Y\longmapsto \nabla f(z)
$$

Return the exact complete joint gradient, without function values or a Hessian.

### Output

Return a feasible pair $\widehat{z}=(\widehat{x},\widehat{y})\in X\times Y$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\widehat{z}-z^\star\|_2^2
$$

Do not use a global gap that may be infinite on an unbounded domain.

### Resource accounting

Each joint-gradient response increments $N_{\rm grad}$ by one.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Any measurable sequential adaptive deterministic algorithm is allowed. Queries and outputs may use the complete history, with no additional span, zero-support, communication, or memory restriction.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
\|\widehat{z}-z^\star\|_2^2\le\varepsilon.
$$

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$R^2$: Public squared Euclidean distance bound from the initial point to the unique saddle point **Domain:** Positive real number.

$\|z_0-z^\star\|_2^2\le R^2$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Squared Euclidean distance tolerance to the unique saddle point. **Domain:** Positive real number.

$\|\widehat z-z^\star\|_2^2\le\varepsilon$

$\mu$: Smaller curvature constant of the two variable blocks **Domain:** Positive real number.

$\min\{\mu_x,\mu_y\}$

$\mu_x$: Uniform strong-convexity lower bound for $f(\cdot,y)$ at every fixed $y$ **Domain:** $0<\mu_x\le\beta$.

$f(u,y)\ge f(x,y)+\langle\nabla_xf(x,y),u-x\rangle+\frac{\mu_x}{2}\|u-x\|_2^2$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$X,Y$: Full space of the two unconstrained variable blocks **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$X=\mathbb R^{d_x},\ Y=\mathbb R^{d_y}$

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\widehat z$: Joint output consisting of the two variable blocks **Domain:** $\mathbb R^{d_x+d_y}$.

$\widehat z=(\widehat x,\widehat y)$

$N_{\rm grad}$: The number of complete exact joint-gradient calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$R$: Initial-distance radius, the nonnegative square root of parameter $R^2$. **Domain:** A nonnegative real.

$R=\sqrt{R^2}$

$F$: Saddle operator induced by the payoff function **Domain:** $X\times Y\to\mathbb R^{d_x+d_y}$.

$F(x,y)=(\nabla_xf(x,y),-\nabla_yf(x,y))$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I N_{\rm grad}(\mathcal A,I)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The nontrivial accuracy region.

**Region.** $0<\varepsilon<R^2$

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Polynomial gap

**Lower bound.** B5

$$
1
$$

**Upper bound.** B1, B6, B7

$$
\begin{cases}1,&(1-\mu^2/\beta^2)R^2\le\varepsilon<R^2,\\ O\!\left(\min\!\left\{\frac{\beta}{\mu}\left(1+\log\frac{R^2}{\varepsilon}\right),\frac{\beta}{\sqrt{\mu_x\mu_y}}\log\frac{2\beta^2R^2}{\mu_x\mu_y\varepsilon}\right\}\right),&0<\varepsilon<(1-\mu^2/\beta^2)R^2,\end{cases}\quad\mu=\min\{\mu_x,\mu_y\}.
$$

**Gap or comparison.** Exact N*=1 and ratio 1 on r4. Outside r4 retain lower bound 1 versus the displayed old upper minimum; matching joint curvature and accuracy dependence remains unresolved.

**Comparison argument.** Conditionally retain accepted b1, b6 and b5 with their original contracts and guards. New proof CV_S_SCSC__proof__one_call_window gives a one-call upper bound on r4 from the exact frozen strong-monotonicity and Lipschitz premises. The unchanged b5 lower bound applies to all r1, so the bracket closes exactly on r4. Outside r4 choose the smaller retained public sufficient cap. ε=R² belongs only to the separate zero-query comparison. No necessary one-call boundary, global strongest-bound result or resource transfer involving c3 is asserted.

### R2 - Zero-query regime

**Region.** $\varepsilon\ge R^2$

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Comparison argument.** Zero-query region is exact and separate from asymptotic positive-cost regions.

### R3 - Nontrivial accuracy regime for the accelerated upper bound

**Region.** $0<\varepsilon<R^2$, $0<\mu_x,\mu_y\le\beta$.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

## 4. Bounds and supporting evidence

### B1 - unconstrained extragradient with two joint-gradient calls per step

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Exact extragradient and FOAM updates and outputs require no randomized choices.

$$
O((\beta/\min\{\mu_x,\mu_y\})(1+\log(R^2/\varepsilon)))
$$

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
O((\beta/\min\{\mu_x,\mu_y\})(1+\log(R^2/\varepsilon)))
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Let $F(z)=(\nabla_x f(z),-\nabla_y f(z))$, with strong-monotonicity modulus $\mu=\min\{\mu_x,\mu_y\}$ and Lipschitz constant at most $\beta$. Two-call extragradient with step size $1/(2\beta)$ contracts squared distance to the unique zero by at most $1-3\mu/(8\beta)$ per iteration. Starting from squared-distance bound $R^2$, iterate to tolerance $\varepsilon$ and charge both joint-gradient calls per step.

**Local argument.** SIX_PROOF_395ee6ec1cc4

### B2 - FOAM: accelerated proximal outer iterations with extra-anchored gradient inner iterations.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Exact extragradient and FOAM updates and outputs require no randomized choices.

$$
\widetilde{O}\!\left(\frac{\beta}{\sqrt{\mu_x\mu_y}}\left[1+\log\frac{R^2}{\varepsilon}\right]\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2205.05653v1)

**Conditions.** Apply Kovalev–Gasnikov (2022), Theorem 3, with both known nonsmooth terms set to zero, so their proximal maps are identities.; The initial Lyapunov constant is controlled by $R^2$ and a polynomial in the condition numbers. Their logarithmic initialization dependence is retained; these terms are not claimed to vanish.

**Dimension conditions.** upper is dimension independent; lower dimension only as explicitly stated

**Oracle correspondence.** Only joint gradients are supplied. Unknown proximal saddle subproblems are solved approximately using charged gradient calls.

**Guarantee conversion.** The source Definition 1 criterion is joint squared distance at most $\varepsilon$. The tolerance is not a distance tolerance.

**Output rule.** exact metric and output specified above

**Resource conversion.** cost vector belongs to the single cited algorithm or hard family

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
O(\beta/\sqrt{\mu_x\mu_y}\log(1/\varepsilon))
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Converting the initial Lyapunov quantity to Euclidean distance introduces a logarithm involving $\beta/\min\{\mu_x,\mu_y\}$. The shorthand $\log(1/\varepsilon)$ is not a complete scale-independent formula.

**Source location.** [1](https://arxiv.org/pdf/2205.05653v1) pdf pages: 9; section: Section4; theorem: Theorem3 and Corollary1

Use the unconstrained FOAM branch without extra proximal terms, whose proximal operations are identities. Retain the initial Lyapunov scale and condition-number logarithms. The upper bound is $\widetilde O(\beta/\sqrt{\mu_x\mu_y})$ times the stated accuracy logarithm, rather than a shorthand omitting initialization.

### B3 - return public z0

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The witnesses return either the public initial point or one exact resolvent query at a fixed step size. Neither uses private or oracle randomness.

$$
0
$$

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.** 0

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** When $\varepsilon\ge R^2$, the public initial point's squared-distance guarantee already meets the target, so return it directly.

**Local argument.** SIX_PROOF_cea15d68accf

### B4 - nonnegativity of query cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** Nonnegative query cost for every algorithm in this deterministic setting.

$$
0
$$

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.** 0

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Every admissible algorithm has nonnegative query cost, so a zero-query upper bound is already minimal.

**Local argument.** SIX_PROOF_c5f449dbde2c

### B5 - Zero-query indistinguishability

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

**Algorithm-scope qualification.** No restriction on linear spans, supports or postprocessing is used.

$$
1
$$

**Conditions.** The fixed contract and 0<epsilon<R^2.

**Dimension conditions.** Every admissible finite dimension; choose any unit vector in the nonzero joint space.

**Oracle correspondence.** Only the fixed complete joint-gradient interface exists; zero calls reveal no information about the shifted center.

**Guarantee conversion.** For every deterministic zero-call algorithm one of two fixed admissible hidden instances fails the required for-all-instance guarantee.

**Output rule.** The identical arbitrary output is evaluated in the target squared Euclidean distance.

**Resource conversion.** The nonnegative integer fixed worst-case count of complete joint-gradient responses must be at least one.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.** 1

**Constants.** Exact lower bound N_grad>=1, with no asymptotic constants.

**Logarithmic factors.** None.

**Derivation.** The explicit two-instance proof in CV_S_SCSC__proof__zero_query_necessity shows that every deterministic zero-call output has squared error at least R^2 on one admissible shifted quadratic. Thus the fixed worst-case count is at least 1 on r1.

**Local argument.** CV_S_SCSC__proof__zero_query_necessity

### B6 - Fixed-parameter predictor–corrector extragradient with damped momentum

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** All updates use public parameters, exact gradients and deterministic arithmetic.

$$
O\!\left(\frac{\beta}{\sqrt{\mu_x\mu_y}}\log\frac{2\beta^2R^2}{\mu_x\mu_y\varepsilon}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/2609.20327v2)

**Conditions.** The fixed contract, beta>=max(mu_x,mu_y)>0 and 0<epsilon<R^2.; If mu_y>mu_x, swap the blocks and negate the payoff before applying the source algorithm.

**Dimension conditions.** Every admissible finite dimension; no additional dimension window.

**Oracle correspondence.** One source full-gradient call is exactly one target complete joint-gradient call, up to a known block permutation and sign change.

**Guarantee conversion.** Definition 3.2 uses squared Euclidean distance. Source relative tolerance delta=epsilon/R^2 and the radius promise imply absolute error <=epsilon for every instance.

**Output rule.** Return the last corrected pair, transformed back if blocks were swapped.

**Resource conversion.** At most 1+2T complete joint-gradient calls, including one initialization call and both predictor/corrected-point calls per iteration; cache corrected gradients.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
O\!\left(\frac{\beta}{\sqrt{\mu_x\mu_y}}\log\frac{2\beta^2R^2}{\mu_x\mu_y\varepsilon}\right)
$$

**Constants.** Universal constants; an explicit sufficient cap is 1+2 ceil[(240 beta/sqrt(mu_x mu_y)) log(32 beta^2 R^2/(min(mu_x,mu_y) sqrt(mu_x mu_y) epsilon))].

**Logarithmic factors.** None omitted; the condition-number and accuracy logarithms are displayed.

**Derivation.** Apply Theorem 3.7 of arXiv:2609.20327v2 with L=beta, oriented curvatures, and relative tolerance epsilon/R^2. The explicit transfer and full 1+2T accounting are in CV_S_SCSC__proof__pce_dm_transfer; Remark 3.8 gives the displayed rate. The existing extragradient branch remains available separately.

**Local argument.** CV_S_SCSC__proof__pce_dm_transfer

**Source location.** [2](https://arxiv.org/pdf/2609.20327v2) character ranges: 9759; 15359; 23700; 26327; equations: 3; 4; 5; 6; 24; 25; pdf pages: 5; 6; 7; 12; 13; section: Sections 2–3; theorem: Algorithm 1, Assumption 3.1, Definition 3.2, Theorem 3.7 and Remark 3.8

Primary PDF version dated 2026-09-28, before the cutoff. General nonlinear coupling is allowed. Algorithm and guarantee mapping are explicit in the transfer proof; exact decisive formulas were cross-checked in the archived HTML evidence e5.

**Source location.** [2](https://arxiv.org/pdf/2609.20327v2) character ranges: 16450; 18250; 37720; 43920; equations: 6; 24; 25; section: Section 3; theorem: Definition 3.2, Theorem 3.7 and Remark 3.8

HTML of the same arXiv:2609.20327v2 preserves mathematical alttext. Direct reads verify h<=2/(15L), the alpha interval, the exact distance prefactor and sufficient iteration count, and the displayed condition-number logarithm.

### B7 - One explicit saddle-operator gradient step

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** One fixed query and deterministic exact-real postprocessing.

$$
1
$$

**Conditions.** All fixed CV_S_SCSC contract conditions.; ε>0 and (1-min{μx,μy}²/β²)R²≤ε<R².

**Dimension conditions.** Every admissible finite block dimension; no additional dimension restriction.

**Oracle correspondence.** Use exactly one native complete joint-gradient response; the dual sign change is known arithmetic.

**Guarantee conversion.** Deterministic squared Euclidean distance at most ε on every admissible instance, with no norm/squared-norm or probability conversion.

**Output rule.** Return the explicit full-space pair, permitted as an arbitrary unqueried output.

**Resource conversion.** Exactly one N_grad call, including initialization; all remaining operations are uncharged exact-real arithmetic.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.** 1

**Constants.** Exact cap of one complete joint-gradient response; no hidden constants.

**Logarithmic factors.** None.

**Derivation.** The new proof expands the squared error and uses the retained μ-strong monotonicity and β-Lipschitz premises to obtain error≤(1-μ²/β²)R². This meets the target on r4.

**Local argument.** CV_S_SCSC__proof__one_call_window

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 5f1f30c9d884f0b02ade896662942f2a53a127d385b6b54ef9931db1510beaa5

### Native proof: SIX_PROOF_395ee6ec1cc4

Native pointer: /proofs/0; canonical SHA-256: ed25d4da4dc5609ff265ec3c0024b1f61acc06fe9502942c4aeee8d5bd12a394

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 328c300fb079e29e18f86c0d0b75280ab6d471eb9e62d99e8f21782cd18d8044

Write $F(z)=(\nabla_xf(z),-\nabla_yf(z))$ and $\mu=\min\{\mu_x,\mu_y\}$. This operator is $\mu$-strongly monotone and $\beta$-Lipschitz, and its zero is the unique saddle point $z^\star$. With $\eta=1/(2\beta)$, let $w=z-\eta F(z)$ and $z^+=z-\eta F(w)$. Expanding the square, using strong monotonicity at $w$, and bounding $\|F(z)-F(w)\|$ by $\beta\|z-w\|$ gives
$$\|z^+-z^\star\|^2\le\|z-z^\star\|^2-\frac\mu\beta\|w-z^\star\|^2-\frac34\|z-w\|^2.$$
Since $\mu\le\beta$ and $\|z-z^\star\|^2\le2\|w-z^\star\|^2+2\|z-w\|^2$, the right side is at most $(1-3\mu/(8\beta))\|z-z^\star\|^2$. Starting from squared distance at most $R^2$, geometric contraction reaches the squared-distance tolerance $\varepsilon$ in $O((\beta/\mu)(1+\log(R^2/\varepsilon)))$ iterations. Every iteration uses two exact joint-gradient calls. This proof uses the full-space model of this bound.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 5412d660786d79ccc7a08d04aa4b5d6f1edb62a4ad99f02f0a646cdeb91c5e3d

unconstrained extragradient with two joint-gradient calls per step

### Native proof: SIX_PROOF_cea15d68accf

Native pointer: /proofs/1; canonical SHA-256: b4829ff3ac83d8225d7d02d12c4cce6159fcd52458326cdfbbd29304903bf822

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: ea5dc2bc754c6adb143b37cab98c6021c76d0a5d62d64ff55e2a2d18d3e1c125

When $\varepsilon\ge R^2$, the public initial point's squared-distance guarantee already meets the target, so return it directly.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 60087ec2a9de5dfda7ddedfc316f9225c4b3a74b7ee90ac16d8d723d2c9d5c5e

return public z0

### Native proof: SIX_PROOF_c5f449dbde2c

Native pointer: /proofs/2; canonical SHA-256: 6e3e78f436127db0839eb94890477c0ee7521207e10a21ae0f0b912ddee1ec2e

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: e6da1876656a73b87a1f0cb21f30d7d717e2084cfbd8bc23fba8ca8b09b1f9cd

Every admissible algorithm has nonnegative query cost, so a zero-query upper bound is already minimal.

#### Native field: scope

Native pointer: /proofs/2/scope; canonical SHA-256: 8e7cd37b3ccc4354c1e06fa177d57119b0f24cc6b076f3eb19796ced52b490e5

All model, oracle, algorithm, guarantee, quantity, resource-projection, and region conditions attached to the mapped bounds remain in force.

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 680a9bc3fede03595e525ae2c845f3976cf6c55c144f99c06dfd3b40398671f8

nonnegativity of query cost

### Native proof: CV_S_SCSC__proof__zero_query_necessity

Native pointer: /proofs/3; canonical SHA-256: acc1ca97d87d617054c8d4d41913e819efaebd5f8386ca4c193a68a90c272ee2

#### Native field: body

Native pointer: /proofs/3/body; canonical SHA-256: a539d35e3cb4413394996108c676e0d3503c7dde5c8d469e46a6ea6d848e9e54

Fix all public inputs and any unit vector e in the joint space. Set a_plus=z0+R e and a_minus=z0-R e, and define f_a(x,y)=(mu_x/2)||x-a_x||^2-(mu_y/2)||y-a_y||^2. Each function is uniformly mu_x-strongly convex and mu_y-strongly concave, has unique saddle a, and has joint gradient Lipschitz constant max(mu_x,mu_y)<=beta. Each saddle is exactly distance R from the public z0. With no oracle calls, any permitted deterministic algorithm has the same history and arbitrary output w on both hidden instances. The parallelogram identity gives (||w-a_plus||^2+||w-a_minus||^2)/2=||w-z0||^2+R^2>=R^2. Thus one admissible instance has squared error at least R^2, contradicting epsilon<R^2. Every successful fixed worst-case query cap is therefore at least 1. This covers arbitrary measurable computation and unqueried outputs, with no span restriction, in every admissible dimension. At epsilon=R^2 the accepted return-z0 upper bound succeeds, so the strict endpoint is sharp.

#### Native field: scope

Native pointer: /proofs/3/scope; canonical SHA-256: 8966a0dbad03c7002145d068093d83a56c67df66994e539d6c15defcca06a90c

Fixed CV_S_SCSC main/g1/q1/N_grad contract on r1; unrestricted deterministic algorithms.

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 1a9eeb79527fe860179531d83ee445ae827f7c981fac8878336d700bc33eb103

One query is necessary below the sharp zero-query threshold

### Native proof: CV_S_SCSC__proof__pce_dm_transfer

Native pointer: /proofs/4; canonical SHA-256: 48726b830a5f9c0724788f2e4ba5c6687caa7e01ddfb08de4e6dde24ee012545

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 32266fa8bc90bc7aabe55d1562ca4bcc79721d17f89f544e663cfa30f97fe9a0

Use Zhang–Xu, arXiv:2609.20327v2 (2026-09-28), Algorithm 1, Assumption 3.1 and Definition 3.2 (PDF SHA256 bbeab4b027f21e83c4b21b23194d338fd92b8c7054b404a015f2711b5700f07b, pp.5–7, characters 9759–15359), and equation (6), Theorem 3.7 equations (24)–(25), Remark 3.8 (HTML SHA256 50562b606c5999850b25390aa23ee10f7757be388a7365502f34a6559222d19e, characters 16450–18250 and 37720–43920; corresponding PDF pp.12–13, characters 23700–26327). These are the unconstrained general SCSC assumptions with full-gradient Euclidean Lipschitz constant L. Set L=beta. Orient blocks so M=max(mu_x,mu_y) is the convex curvature and m=min(mu_x,mu_y) the concave curvature; when needed use g(xi,eta)=-f(eta,xi), whose complete gradient is a known permutation/sign change of one original joint-gradient response. This is an isometry and preserves the squared-distance metric. Write s=sqrt(mu_x*mu_y), choose h=2/(15 beta), rho=h M/8 and alpha=8/(8+h s), satisfying (6), and initialize v0=0 at the public z0. Theorem 3.7 gives D_T<=(32 beta^2/(m s))(1+h s/16)^(-T)D0. Set delta=epsilon/R^2 in (0,1), and T=ceil[(240 beta/s) log(32 beta^2 R^2/(m s epsilon))]. Equation (25) gives D_T<=delta D0<=epsilon; D0 itself need not be known. The algorithm uses only gradients and explicit exact-real arithmetic: query once at z0, then query the predictor and corrected point each iteration, caching the corrected joint gradient for the next predictor. Hence the fixed cap, including initialization, is 1+2T. No function values, hidden prox operators, Hessians, inner solves or certificates are supplied. If K=beta^2/(mu_x*mu_y)>=1, then 32 beta^2/(m s)<=32 K^(3/2), so this cap is O((beta/s) log(2 K R^2/epsilon)), with all logarithms displayed and universal constants. The source holds in every finite dimension, for the deterministic last iterate. For c1, retain b1 conditionally with accepted proof SIX_PROOF_395ee6ec1cc4: its squared-distance contraction factor 1-3m/(8 beta) gives the explicit cap Q_EG=2 ceil[(8 beta/(3m)) log(R^2/epsilon)]. Choose between that algorithm and PCE-DM using their public sufficient caps before making any queries. This proves the compatible upper minimum. For equal curvatures and fixed relative accuracy the new displayed branch carries an additional condition logarithm, so b1 must remain. The lower bound b5 and both upper branches have identical view, guarantee, quantity, resource and r1 domain; r2 is disjoint at epsilon=R^2. No claim is transferred from or into c3's unassessed resource projection.

#### Native field: scope

Native pointer: /proofs/4/scope; canonical SHA-256: 189c4759e43a55db7a05d4c2a0281fa03cfeb836ae14e5ab5dc972d5d133f9a2

Fixed CV_S_SCSC main/g1/q1/N_grad contract on r1; conditional retention of b1 and no change to c3.

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 4a65b6579072d53dedd19c1098b668be383e23f05aca01b9d46b24a4bae82488

PCE-DM initialization, absolute-error transfer and compatible upper minimum

### Native proof: CV_S_SCSC__proof__one_call_window

Native pointer: /proofs/5; canonical SHA-256: 6431ad292435f4bc7418a55cfcda8dd9967a669f3284dae61dde6c463b069075

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: 6b51a02cb7ddaf205f3762b1045e4b103c9274b89c65d313af0a377c5390f949

Conditionally retain the operator premises explicitly stated in frozen /proofs/0 (SIX_PROOF_395ee6ec1cc4), canonical SHA256 ed25d4da4dc5609ff265ec3c0024b1f61acc06fe9502942c4aeee8d5bd12a394: F(z)=(grad_x f(z),-grad_y f(z)) is μ-strongly monotone, β-Lipschitz, and F(z*)=0, where μ=min{μx,μy}. These are retained premises, not a fresh recertification of the unrelated extragradient proof. The fixed contract supplies ||z0-z*||²≤R², public β and μ, complete exact gradients, deterministic adaptive algorithms, arbitrary feasible outputs, and uncharged exact-real arithmetic. Query once at z0 and output z1=z0-(μ/β²)F(z0). Writing e=z0-z*, expand: ||z1-z*||²=||e||²-2(μ/β²)<F(z0)-F(z*),e>+(μ²/β⁴)||F(z0)-F(z*)||² ≤ [1-2μ²/β²+μ²/β²]||e||²=(1-μ²/β²)||e||²≤(1-μ²/β²)R². Since 0<μ≤β, the factor is in [0,1). Thus whenever ε>0 and (1-μ²/β²)R²≤ε<R² this deterministic output satisfies the exact native squared-distance guarantee after exactly one complete joint-gradient response, including all initialization. Negating the returned dual-gradient block is known arithmetic and costs no information call. No value, Hessian, prox oracle, hidden inner solution or certificate is required. For the lower side, conditionally retain b5 at frozen /bounds/4, hash 8c2f091c42c592c0f9f463dbed24a3628fe9fe9950799751c6591553bf2b7791, and /proofs/3, hash acc1ca97d87d617054c8d4d41913e819efaebd5f8386ca4c193a68a90c272ee2. Their shifted separable quadratics remain admissible after restricting public parameters to r4, so every zero-call deterministic algorithm still fails on one instance when ε<R². Consequently N*=1 on r4. At μ=β, both block curvatures equal β and the error bound is zero, so one call exactly recovers the saddle for every positive accuracy below R². At ε=R², the unchanged return-z0 algorithm instead has exact cost zero. The r4 activation inequality is sufficient for this one-step algorithm; no converse or characterization of the largest possible one-call region is asserted. Outside r4 retain the old b1/b6 upper minimum and b5 lower side. No scientific claim is transferred to c3's unassessed resource projection.

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: 7028f03ceee0b8cdea1fa7360fc0ca19ffe5ae09f098a5da012defe20aafdab0

Fixed CV_S_SCSC main/g1/CV_S_SCSC__main__q1/N_grad contract, all admissible finite dimensions; new r4 is a subset of r1.

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: 0f80b4b8de71b3e29f743759a7f02896914a3558dcd9c61bf2f8c5e49b0f9fd0

Exact one-call bracket on a sufficient joint accuracy window

### Native proof: CV_S_SCSC__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/6; canonical SHA-256: 1e71792eaf852197eeadcea23df63967366c315cf862ae61ed21793ecee93e72

#### Native field: body

Native pointer: /proofs/6/body; canonical SHA-256: d9a378e18f21b06362d6ebba80c93730c93502bbfe1645dc25b00fc97f6f29d4

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. On r4, accepted b7 has actual gradient-call cost one and accepted b5 gives the integer lower bound one throughout r1 containing r4. Thus the new native c_one_call has cost exactly one under the same q1/resource. Outside that sufficient window, the retained upper/lower ratio is bounded by the displayed minimum of beta/mu and beta/sqrt(mu_x*mu_y) times accuracy logarithms; with curvature parameters varying jointly this is a registered polynomial gap, without claiming it is a mature literature-open gap or a maximal one-call characterization.

#### Native field: comparison_refs

Native pointer: /proofs/6/comparison_refs; canonical SHA-256: 37c79196b09809b6a20170ea8b5d104efafd634b0ffe12be0c8656f34cbc07c4

#### Native item 1

Native pointer: /proofs/6/comparison_refs/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /proofs/6/comparison_refs/1; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: evidence_basis

Native pointer: /proofs/6/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 0b7b3379f2d9f9ff56a2886e0b1b51afdf08ef8cd6c64c0922e5dbe2c9e71ca5

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: cf61a7ada20f10658cbbfdd10123b58d384ae7f28ca907543d30b76ac34fcf89

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 67646353e19d529448bbe2ae8f5aee242e64f9be482aa4229718fc9846590ec5

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 94eb9a737416d75c08df1a1849bbd2f0dafef16d4b5c94173cbdfb161bd5cf2d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 98e8e7389605deb4f2cb23df99a8516de71e8233e5fe6b678c843b1b37fdf574

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 64bc2b63749433855c4e095c54964b8c60d7bc0b719f50007adfd20995bd49b3

0<ε<(1-μ²/β²)R²; retained as one branch of the old upper minimum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: a664266e2c6e42daf73382674580b8a2eb378d8613be39971ba7212f7e880eaf

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: b9e6da6b1707e7a0a80a9b67c5b206cf27e74daa147063084849197187e8d309

SIX_PROOF_395ee6ec1cc4

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/1; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: e14b772a2b1cad006e49513e8693f0a48f1d570a3c0f7ea14803cdf1a342e815

Outside the new one-call window retain its original applicability and compare public sufficient caps with b6. Within the new window an exact one-call successful algorithm is minimal by b5, so this branch cannot improve that cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 40ccebc945797bf32a53c57b1258ae4bf64944c11fef669f5d4e5e84819de097

Fixed contract and 0<ε<R², conditionally retained.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 1fa869d0c46afe5794925249d30ac3897797cffe9fd59681dabb04a96192a52a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 76d342120b04b4d2378e20a9f4f59f88c0683ef04a98db4c2a22e2e50a7a16de

None in c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 01a0c95c790fcc6841b4c402d6f476a3b1226b5da858378bb2b4886cb6a9dd03

Its native resource accounting is N and its registered comparison uses resource_cc7c360256 with no assessed expression. No reviewed transfer into N_grad is supplied in this proposal. Similar labels and theorem rates do not merge these identities.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 1c671b3451c78274a0edba4f04d8398806eb625c3a3806577608b85b67b35add

Legacy r3: 0<ε<R² and 0<μx,μy≤β, with frozen initialization qualifications.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 4c5ea6a1cb2c3a7ac35d5601a7c621cd34f0b4207e2d171c1a4d33e99803c62e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 6c27f9340fb173650c5d7bb438a4ef1a9a606a829ce988167decf43872dce16f

Empty intersection with c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 31347106dc2d3f1350b05cee03f4d37740a6a1aaa17ca83cdb275c919671c811

The zero-query upper bound has a disjoint accuracy guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: c3f46332eea8094bc7d4c173c4313d0e0012506f207ad782d0a6ecd66c0c20c2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 6c27f9340fb173650c5d7bb438a4ef1a9a606a829ce988167decf43872dce16f

Empty intersection with c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: f571d42b9d91e83474c0979d469e696d1894c7a5f245b9aa7557f0adf55a9664

Its recorded guard is disjoint; the stronger retained b5 already supplies the positive-region lower side.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: f5fdf7a96073e4bcf75625e7de9fac0b8dc10875b1a776a308a2422cf7420f8a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 939486854d71a31bbb1c1f0e8eb32f0ef14a2291e5065bf1a68c875cf8b379ed

All of c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 6d731cd49602aa0eea12de02d4dd041007827801ddcd24d007250b76a0cddff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 602acaf4e7bfd37b67840d2142d804b3ae2442513d580ee13f1466695067a2c1

CV_S_SCSC__proof__zero_query_necessity

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 74c054c7180d9cdf5eb1daa3379c961a4f9577147ec10ff5d535e27bd6e64f9e

Conditionally retain the exact unrestricted deterministic lower bound 1. Restricting public parameters to the new window preserves the two admissible shifted quadratic instances.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: 919cf5f19fbe0e19577973088a7a08b7807522b4649ef995668dd2eb89fc9141

Fixed contract and 0<ε<R² in every admissible finite dimension.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/bound_uses/5; canonical SHA-256: 9c7c6e5463a4974a6af29458979f025788ff16421052c1efa4231c3e780a74ec

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/adopted_region; canonical SHA-256: 64bc2b63749433855c4e095c54964b8c60d7bc0b719f50007adfd20995bd49b3

0<ε<(1-μ²/β²)R²; retained as one branch of the old upper minimum.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/bound_id; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs; canonical SHA-256: 9c8914ac75be6f4c64055d114fabbe6cf1cf54acd33b4b898ff6e4c3df62a4d9

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 638f4cbda063d9d629664524c0ff149cfcd2614e4b57a142827ada82b9c4e520

CV_S_SCSC__proof__pce_dm_transfer

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/mapping_proof_refs/1; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/reason; canonical SHA-256: 6d36b6f0c73f4f738333cfd5838f28ebd88c18c820dac6a86a2ad403cb885c34

Retain this accepted N_grad branch conditionally. It is unnecessary on the new exact one-call window. No fresh external premise from this theorem is used to prove b7.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/5/validity_region; canonical SHA-256: 3d89c3309676c2fd72ca695ee3753d811b5d5b5fa426bf61fcac2501ff351de1

Fixed contract and 0<ε<R², with the frozen block-orientation and initialization mapping.

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/bound_uses/6; canonical SHA-256: a274509c1c9c51893d9f77184cfddc8fc5ab3fae75288876c2275ea38fad7305

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/adopted_region; canonical SHA-256: 96f5e590c590ce3b36c695d2a53f6313d2925fbda96477eb0ff56a642c7c2485

Its full validity region inside c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/bound_id; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs; canonical SHA-256: f10fd2c9b089a1c6a5dc05938891827d49d280d8d625c3c83fb7866d8db1c5e8

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/reason; canonical SHA-256: 529d4d40ff7a22ed38015b9976a60182bd2e72845bc969f9725f8de3b77dc5d7

The explicit one-gradient output has squared error at most the displayed threshold. Together with b5 it gives exact cost 1, uniformly over all joint variables and dimensions.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/6/validity_region; canonical SHA-256: 524a9e05014eee519bf55681d45a6ab0339ab858688a295098f937ae09b64b3a

Fixed contract and (1-μ²/β²)R²≤ε<R², with ε>0 and μ=min{μx,μy}.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 0402c8d79cf4459d95c19345575db869d6551dcd0a142c9eecc9438cda10e299

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 068a1681237a5d8add57c6d96ac3aed3a4d2e1db3dd4ce1750df4a928844107a

The new lower activation threshold is included because the error inequality is non-strict; ε=R² is excluded and belongs to c2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: a140c90249fdb15887d359b354e8276f236cc2825aafa361e683ec6bd9fe59cb

When μ=β, both block curvatures equal β, the new squared-error bound is zero, and every 0<ε<R² has exact cost 1.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 4955e3fcba063efa348cd16d0080af7bd4b4ca417ad8d42ad8e06e9b6cee198f

As μ/β tends to zero, the sufficient one-call window narrows toward ε=R²; no statement that one call is impossible below this threshold is made.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 657114ee68e8d4eeb83f50e0a1865e93e59916d71ae1a845695f41f352c4be92

All statements hold in every admissible finite dimension, including d=2; no unsupported finite-dimensional saturation or reconstruction claim is introduced.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 1ce0881f2e31e0784a2b1acd8eb486991bdcc22e7bbb3825d964cdcbd9e40010

The retained b1/b6 envelope uses public sufficient query caps. Hidden constants do not establish an exact crossover or uniform dominance between their displayed asymptotic rates.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: eefca476ed3adbe8b314903d3e50a435103ffc3719e1d885580c39ceea947ffb

Ratio 1 and exact N*=1 on the new one-call window. On its complement the retained upper minimum is compared with lower bound 1; matching joint dependence remains unresolved.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: e203371f2ac58d24f5399b3b843e6b39abd5bbaf300b3d62226aeea4ae5eb73c

1 throughout 0<ε<R².

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 96ebbb02f9c33677d13eac68b6d7146952ad857d892d9994506a245823268c74

Outside the sufficient one-call window only the accepted upper minimum and lower bound 1 are retained. Sharper lower bounds, a larger one-call region, and a complete FOAM-to-N_grad transfer remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 523d9a52044dad33ccf1b0ad061dbe0d0bdaf2ff4bc3e654a79480ffd9f954ec

Exactly 1 on (1-μ²/β²)R²≤ε<R². On 0<ε<(1-μ²/β²)R² retain O(min{(β/μ)(1+log(R²/ε)), (β/sqrt(μx μy)) log(2β²R²/(μx μy ε))}). Guards remain part of this piecewise envelope.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 5491da74aa001efb9cd5326ad87ea28466d39285530cf450a54d086c9dccd3cb

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 0047bca53a62002b09a07ed3d5b1e33e520b5b36957f7a5c52b50d89b6749d49

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: f32cc116e15a0d6a16f43943a0ecaf395b4e7d2ed8d391ea203989f8e27e9ff3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: a662c75f4a54a8df8a3afb90f64a5c24927a1f3f91680dfa7ad9ec095b866841

Disjoint recorded guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 8582f549b4bae55e2c6f197f3112c06fe8c7f7a02ab17a2566e1304a45fab58a

0<ε<R².

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 100b8331aafdcf35eb056063c7e5f362d673c175c7a92beaf449253578c86240

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: abb4fc6880d33a1591495b142f158735e0e541d70b48e30c211e6afc0454a722

Disjoint accuracy guard; no resource transfer is needed here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: bcd0c6107c54a630744c084c4d7120974f29c2b95df42ce7a9bc9cd5852e518a

0<ε<R² with its legacy resource qualifications.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: c91e9460414e2057f4f8c72d3146210b2e7d68efa540b079e4f821fd60631e7a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 9b4dd8d2b73096fa63299bce2c9108f4c44217409971901eeb9c43520fd4a4ef

All of c2.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 5a465e81c4ef3b3d5846d2a9e13ec75708f723b117e8aca6e2d179a45d417db1

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: fee73030872b486f7d1c69de7df115f7c666accc94505f385dc9f80ae889e1b3

SIX_PROOF_cea15d68accf

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: a672563442e850c04e479d61a6eb285b6194be05e495f20f74070e14c97f0281

Conditionally retain return of the public initial point with zero queries.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: ff8c410f65517ecb03455c04e898629590769786dd9089a86d165d3c5d675e06

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 9b4dd8d2b73096fa63299bce2c9108f4c44217409971901eeb9c43520fd4a4ef

All of c2.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 49189535c92347f104367dff5bb261fc84e98f01214dcf2873329f7c4d9de56e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: ecb5b0cf10816f69a1ebcfeeb9d874992f97a629912a236df2939838ef498137

SIX_PROOF_c5f449dbde2c

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 8c87e706bc87e43d19fe238af22c02040e41612becee761ea7f2142567bafd42

Conditionally retain nonnegative query cost, matching the zero upper bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: ececab3f08fe22847eb5b6cef18ed2cf74ec171437f8379a3d97c6e7ff946e26

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 8d248db2b004cfaa1bd10b9d5b510d8e6e111fcaeb7bdd59e075bd40d5bd4409

The strict lower-bound guard excludes ε=R² and the rest of c2.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: 8582f549b4bae55e2c6f197f3112c06fe8c7f7a02ab17a2566e1304a45fab58a

0<ε<R².

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/bound_uses/5; canonical SHA-256: 3380a020f00d488b3a6d6cc9a8dddc972072b2834969b95158126f3303afad38

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/bound_id; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/reason; canonical SHA-256: a662c75f4a54a8df8a3afb90f64a5c24927a1f3f91680dfa7ad9ec095b866841

Disjoint recorded guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/5/validity_region; canonical SHA-256: 8582f549b4bae55e2c6f197f3112c06fe8c7f7a02ab17a2566e1304a45fab58a

0<ε<R².

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/bound_uses/6; canonical SHA-256: f3d0d888e2720f05e5601de6c474e09c09c05d7d6ef886ff20c5730f7fff3c2b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/bound_id; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/reason; canonical SHA-256: fbf0e253bbab19ad87ac37cbbcf55a9580a946a33799e63c1b164e93a8a22235

The new claim deliberately excludes the exact zero-query endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/6/validity_region; canonical SHA-256: 12f829fc29dc72bcf49e41ea4dd578470a8d4a817488e28d5f4b1f2d68bbfbdf

(1-μ²/β²)R²≤ε<R² with ε>0.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: b619d140720a1d631c76eb251072309c1176b8a0c2ca83abcd196d2662944131

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 3fb7b00113cd291e068410718e21a34a740d5e264d32925c694dfc4f86a9aa6a

At ε=R² the public initial point meets the non-strict squared-distance guarantee.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 0e1364fc0de4c607f081528cf6f1a1b6b819f6dafa839bd0e29b6f13508a87d9

No division by the zero lower bound is used.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 7929bf04b6ebd51e7768eacae891bbaf58f0022761c7b67575dc6ece6574dbaf

Exact cost 0; a multiplicative upper/lower ratio is inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 5adfd0ef96b9e53e9f96f16eba47d74204308058496992967a53ba2cc7ab4e20

0 exactly.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 016f8b6f90b4db4ef6713c9c30a8b5b604578c83880ae4918424e911903a684e

None for the retained zero-query claim. This does not certify other regions or literature coverage.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 5adfd0ef96b9e53e9f96f16eba47d74204308058496992967a53ba2cc7ab4e20

0 exactly.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: af46dde70812bb66273fd58a24b76ffe7c9a4594584e0e824fa2a70016a501b2

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: ce1f68e6e7cc8a4da0d987a39d13af9efad4526c523b3956799eb06b497aa6c0

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 45ec3396f109c17c9bbdd3d4d3fab835896fc9051fd841dbc820ad3224cae73b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 0dfacf21a72bcf55c7ca7d7fbc1becb8009fa47fc040f1d4661629aa3ac45c2f

None in c3.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: e4fba5af8e5a9dcd25b780429e5bd0c09fcccf40fb2e49e167cda9424a665eb0

c3 has a distinct unassessed native resource projection; no identity or transfer is adopted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 1bedd57ed1e367e8fa8f4dfe6ff8c9d379bfb1ef4e5def3788e4a531cd9a7f08

0<ε<R² under its N_grad accounting.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 3cb664066b42a08ec9b2b01121f8fba6e69ba4231eeed107c411cf3997380ec1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: d46e166ff8d10388f0ffbc477516dcb3db52230ea3b66da076f95c6789a525bc

The same legacy claim position in c3 as in the frozen baseline.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: bd183a7f91a6852123d3891075a681284e939f6b880c925e1025d489d508b142

Conditional retention of the existing FOAM record only. Its inclusion in the unchanged native claim list does not produce an assessed scalar resource envelope or identify its N accounting with N_grad.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 50c28a2bdd8c5810d4ca861e6bd97fa47f1fb2ac1c1f68a05f18d5fae00d9c19

Frozen r3 and the unchanged b2 initialization and zero-regularizer qualifications.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: b11a4ce12955de5293b22081c91e9afc33ef88662956fd271a938e68642b3574

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 8375c8af8f63e9f3986e7c0472d958706f9e521769bdb57a2d1f0df986102eda

Disjoint accuracy guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 7432f8ddd0cc899da350d04e28280be6aa37b7d139ac586caa43e9a6e9479af5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 3bc472ac9d1996a3c56f6b71040d755923fdb418e20481428989143fa40e0f6d

Empty.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 8375c8af8f63e9f3986e7c0472d958706f9e521769bdb57a2d1f0df986102eda

Disjoint accuracy guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 4db2b6de40d819a6dde8fb7adbe5858c78aa0f612f6b67f0b4054749b514ff00

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 0dfacf21a72bcf55c7ca7d7fbc1becb8009fa47fc040f1d4661629aa3ac45c2f

None in c3.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: f2fec18994a3e02061bd426cc822e721d4ddad3555f46c38801b419de12da532

No lower bound is transferred into the distinct unassessed resource projection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 6963de6b9a9915833870a3dd9e67c82b683411e9b26f02d374d2577e7718cc2d

0<ε<R² for the N_grad quantity projection.

#### Native item 6

Native pointer: /joint_analysis/comparisons/2/bound_uses/5; canonical SHA-256: f36c5605d282735489b5a760faa17b3f04938a068860ad2267f2f11114ac692d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/adopted_region; canonical SHA-256: 0dfacf21a72bcf55c7ca7d7fbc1becb8009fa47fc040f1d4661629aa3ac45c2f

None in c3.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/bound_id; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/reason; canonical SHA-256: 552e0b31d1eba5c4ef96b2ae90604f04bcf7bc3464a5c210e9eec02d168ccb2d

No resource equivalence is assumed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/5/validity_region; canonical SHA-256: c61cfbf9118143e9b49bd1893dd0a7ca785a20209785fde568fc784c6d6a78a0

0<ε<R² for the N_grad projection.

#### Native item 7

Native pointer: /joint_analysis/comparisons/2/bound_uses/6; canonical SHA-256: cfc4b94f360732b0fe90afa7685fd0a9240c7d05632323478f28ed8dc8cd5972

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/adopted_region; canonical SHA-256: 0dfacf21a72bcf55c7ca7d7fbc1becb8009fa47fc040f1d4661629aa3ac45c2f

None in c3.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/bound_id; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/reason; canonical SHA-256: 9a92b7eed5ba3d1b17833ccce83c06b8942b962905b39d3812aae29ff2ba22cd

The new proof counts N_grad only and supplies no transfer to resource_cc7c360256.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/6/validity_region; canonical SHA-256: 69fe0cfda074cfd2bab1c12828873c37e232e77412d3d70ecfc27264deea408d

The new one-call window for complete joint-gradient responses.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 914d7703b9d2516204b7f97b55f8d11c40a8ae799265f5219d1a316c5e321803

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: eb204bfba4cc7cb2c392c7c4015cb05a849094f9b311f309a40fd0ca233180fa

Within the fixed contract r3 is coextensive in parameter space with r1, but its resource ID remains distinct.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: f720f0bca23655dd42bc8b54bc9c124d8aa9c04e4b22c9310d45b0ddfc855262

Neither the zero-query nor the new one-query conclusion is silently transferred into this projection.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 43195f67b2ce7054a1447215c98f082cf4bcf2b2dd447bab10e2538dda797b77

Unassessed; no numerical ratio is justified.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 1bb7592d1c13ce033b1206df7856963c798822d69ffa7438650bcd4dca90d40a

No recorded lower side for this unassessed projection.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 25daf55ee202e317309179f701eb3a6a0c6f1dd2ac65334c82503d7883f04439

The legacy missing-lower status and resource interpretation remain unresolved. This is not a proved absence of a lower theorem.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: a73356b1c3ff4f7ec5cdad81efff68ab6c105e97bb0b81a62d96a2f1f51bb75e

No assessed scalar envelope for resource_cc7c360256; retain the legacy b2 claim without changing its scientific record.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: d40bb768188d2d4fe70fd1b08ce8638c3792cb61bf4ccf4a02d9e7cc811324d2

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 7d5ec6f84d304f4415840e639ed875003898cf62fa8e79aff93de0c997bf7e8d

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: 883a87cef2b954795937d8768ffc9f726532d88310082d0ad85d72b0fb007033

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: cc322124fdd592e1e34325730f2b6b75b9e627303337ef71e6a0f24ea2f22708

Not selected in the exact-one comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: a664266e2c6e42daf73382674580b8a2eb378d8613be39971ba7212f7e880eaf

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: b9e6da6b1707e7a0a80a9b67c5b206cf27e74daa147063084849197187e8d309

SIX_PROOF_395ee6ec1cc4

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/1; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 76000210fdf014f7fc70b1dde4b2c234009fc662526cce27ce8f2c49d30b50fd

The accepted one-call witness and positive integer lower bound give exact cost one on r4; alternative retained positive-cost algorithms are unnecessary here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 40ccebc945797bf32a53c57b1258ae4bf64944c11fef669f5d4e5e84819de097

Fixed contract and 0<ε<R², conditionally retained.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 1fa869d0c46afe5794925249d30ac3897797cffe9fd59681dabb04a96192a52a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 76d342120b04b4d2378e20a9f4f59f88c0683ef04a98db4c2a22e2e50a7a16de

None in c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 09ca16e3af36ba84075b616f538c97fa42ea196b458b556981ca0dbe2571d0ac

incomparable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 01a0c95c790fcc6841b4c402d6f476a3b1226b5da858378bb2b4886cb6a9dd03

Its native resource accounting is N and its registered comparison uses resource_cc7c360256 with no assessed expression. No reviewed transfer into N_grad is supplied in this proposal. Similar labels and theorem rates do not merge these identities.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 1c671b3451c78274a0edba4f04d8398806eb625c3a3806577608b85b67b35add

Legacy r3: 0<ε<R² and 0<μx,μy≤β, with frozen initialization qualifications.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 4c5ea6a1cb2c3a7ac35d5601a7c621cd34f0b4207e2d171c1a4d33e99803c62e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 6c27f9340fb173650c5d7bb438a4ef1a9a606a829ce988167decf43872dce16f

Empty intersection with c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 31347106dc2d3f1350b05cee03f4d37740a6a1aaa17ca83cdb275c919671c811

The zero-query upper bound has a disjoint accuracy guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: c3f46332eea8094bc7d4c173c4313d0e0012506f207ad782d0a6ecd66c0c20c2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 6c27f9340fb173650c5d7bb438a4ef1a9a606a829ce988167decf43872dce16f

Empty intersection with c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: f571d42b9d91e83474c0979d469e696d1894c7a5f245b9aa7557f0adf55a9664

Its recorded guard is disjoint; the stronger retained b5 already supplies the positive-region lower side.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/bound_uses/4; canonical SHA-256: f5fdf7a96073e4bcf75625e7de9fac0b8dc10875b1a776a308a2422cf7420f8a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/adopted_region; canonical SHA-256: 939486854d71a31bbb1c1f0e8eb32f0ef14a2291e5065bf1a68c875cf8b379ed

All of c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/bound_id; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs; canonical SHA-256: 6d731cd49602aa0eea12de02d4dd041007827801ddcd24d007250b76a0cddff9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 602acaf4e7bfd37b67840d2142d804b3ae2442513d580ee13f1466695067a2c1

CV_S_SCSC__proof__zero_query_necessity

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/reason; canonical SHA-256: 74c054c7180d9cdf5eb1daa3379c961a4f9577147ec10ff5d535e27bd6e64f9e

Conditionally retain the exact unrestricted deterministic lower bound 1. Restricting public parameters to the new window preserves the two admissible shifted quadratic instances.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/4/validity_region; canonical SHA-256: 919cf5f19fbe0e19577973088a7a08b7807522b4649ef995668dd2eb89fc9141

Fixed contract and 0<ε<R² in every admissible finite dimension.

#### Native item 6

Native pointer: /joint_analysis/comparisons/3/bound_uses/5; canonical SHA-256: dd9e2c92ab1dd9c71f5893b9894637c1e706b53033e454e8af850fc22c98511b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/adopted_region; canonical SHA-256: cc322124fdd592e1e34325730f2b6b75b9e627303337ef71e6a0f24ea2f22708

Not selected in the exact-one comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/bound_id; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs; canonical SHA-256: 9c8914ac75be6f4c64055d114fabbe6cf1cf54acd33b4b898ff6e4c3df62a4d9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs/0; canonical SHA-256: 638f4cbda063d9d629664524c0ff149cfcd2614e4b57a142827ada82b9c4e520

CV_S_SCSC__proof__pce_dm_transfer

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/mapping_proof_refs/1; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/reason; canonical SHA-256: 76000210fdf014f7fc70b1dde4b2c234009fc662526cce27ce8f2c49d30b50fd

The accepted one-call witness and positive integer lower bound give exact cost one on r4; alternative retained positive-cost algorithms are unnecessary here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/5/validity_region; canonical SHA-256: 3d89c3309676c2fd72ca695ee3753d811b5d5b5fa426bf61fcac2501ff351de1

Fixed contract and 0<ε<R², with the frozen block-orientation and initialization mapping.

#### Native item 7

Native pointer: /joint_analysis/comparisons/3/bound_uses/6; canonical SHA-256: a274509c1c9c51893d9f77184cfddc8fc5ab3fae75288876c2275ea38fad7305

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/adopted_region; canonical SHA-256: 96f5e590c590ce3b36c695d2a53f6313d2925fbda96477eb0ff56a642c7c2485

Its full validity region inside c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/bound_id; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs; canonical SHA-256: f10fd2c9b089a1c6a5dc05938891827d49d280d8d625c3c83fb7866d8db1c5e8

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/mapping_proof_refs/0; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/reason; canonical SHA-256: 529d4d40ff7a22ed38015b9976a60182bd2e72845bc969f9725f8de3b77dc5d7

The explicit one-gradient output has squared error at most the displayed threshold. Together with b5 it gives exact cost 1, uniformly over all joint variables and dimensions.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/6/validity_region; canonical SHA-256: 524a9e05014eee519bf55681d45a6ab0339ab858688a295098f937ae09b64b3a

Fixed contract and (1-μ²/β²)R²≤ε<R², with ε>0 and μ=min{μx,μy}.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: 0402c8d79cf4459d95c19345575db869d6551dcd0a142c9eecc9438cda10e299

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 068a1681237a5d8add57c6d96ac3aed3a4d2e1db3dd4ce1750df4a928844107a

The new lower activation threshold is included because the error inequality is non-strict; ε=R² is excluded and belongs to c2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/boundary_checks/1; canonical SHA-256: a140c90249fdb15887d359b354e8276f236cc2825aafa361e683ec6bd9fe59cb

When μ=β, both block curvatures equal β, the new squared-error bound is zero, and every 0<ε<R² has exact cost 1.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/boundary_checks/2; canonical SHA-256: 4955e3fcba063efa348cd16d0080af7bd4b4ca417ad8d42ad8e06e9b6cee198f

As μ/β tends to zero, the sufficient one-call window narrows toward ε=R²; no statement that one call is impossible below this threshold is made.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/boundary_checks/3; canonical SHA-256: 657114ee68e8d4eeb83f50e0a1865e93e59916d71ae1a845695f41f352c4be92

All statements hold in every admissible finite dimension, including d=2; no unsupported finite-dimensional saturation or reconstruction claim is introduced.

#### Native item 5

Native pointer: /joint_analysis/comparisons/3/boundary_checks/4; canonical SHA-256: 1ce0881f2e31e0784a2b1acd8eb486991bdcc22e7bbb3825d964cdcbd9e40010

The retained b1/b6 envelope uses public sufficient query caps. Hidden constants do not establish an exact crossover or uniform dominance between their displayed asymptotic rates.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 8a6cda175637f1705692d51a7e1fb885cdac63d2ade799458e11ce212c0a9298

1; exact complexity one

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 551e408e582c401a38236cb9ea81a950ac0370f2e4d6de136e9b903ec981a6da

1 on r4

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: ce920de32e95c44fdaae4d2c31832e652f43f7e3f8e1fbc88afab4c76f6ae2f9

No gap on r4. This is a sufficient one-call window, not a maximal one-call characterization.

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 551e408e582c401a38236cb9ea81a950ac0370f2e4d6de136e9b903ec981a6da

1 on r4

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 82156ac210400f62c44cc8a8112d5a520becf5d501a26978fcb23079ede2f8a3

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: f5283c49c2b38f474d03b7c600d32d9811566ee24f46ac1a2202016f101ca7af

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 0908225394e545bdc5d776a07297e85b9bba3a34b869e0517fedb8a9eeae08f3

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: d6dbfbffac319d629978bf8a526372cabc23b309e9526bd6e5380e9086815d0d

zero_calls

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 53f4be8e00cdc9b65da6ac2d985df6c7ead803bac67c26f023b1bcfea62847dd

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: ecb5b0cf10816f69a1ebcfeeb9d874992f97a629912a236df2939838ef498137

SIX_PROOF_c5f449dbde2c

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/1; canonical SHA-256: fee73030872b486f7d1c69de7df115f7c666accc94505f385dc9f80ae889e1b3

SIX_PROOF_cea15d68accf

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 8486deef2272c561397c694142920e0a15508cee77cfd5064b57d2e51b3ebbf1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 68f8ff586e805bce7ac5f5db2bf50623aeb41e85081a464425825cf5f44c8649

Exact cost 0, conditionally retained. The equality ε=R² belongs here.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 075c8cba0b7c9f339c691e0a74568cec3a9e878b5b441c7637e7ae15a38cfda0

ε≥R² within the fixed parameter domain

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: b7b0f1391745122045eee0dfba13f5197c1f96a16829a1636d0cf57151d2e90e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 36c0adc24a0089cb7f6ec1bb3c45f306afe4933c257f68b85d29ede58c5b4ae2

one_call_window

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 14f512193f3bbbcc5d1feb805884f0cbf5b908d9d03cebcc21db50aa9d2f6e6d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/1; canonical SHA-256: 602acaf4e7bfd37b67840d2142d804b3ae2442513d580ee13f1466695067a2c1

CV_S_SCSC__proof__zero_query_necessity

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: a64b4b265f46a4619126e01ff8ff1eda35d121a3605caed15b0a21f36f151c42

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: f59881046206b73e195490dbcd0ae225799abc77420f62b29b916f05e0a79d99

Primary N_grad cost is exactly 1 by new b7 and retained b5. c3 overlaps in parameter space but retains its distinct unassessed resource projection; no envelope is transferred into it. The primary q1 exact-one consequence now has its own native comparison; the distinct secondary resource remains unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: ff883c67d2383d99072037a22faff54bf1939b07bb3888af9107cfd57a90e238

0<ε<R² and (1-min{μx,μy}²/β²)R²≤ε

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 8b3eb48225b8583b96084313adabf58b5ba817eb519bad1a9c5116f87c732366

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 5903c7f7845460a20c408a8feb02ce19dacece07decc77c54a63b24cff229081

remaining_positive_region

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 487420b0d78176f1111f17728559b3fbea0f8f4ef9c5a4757f98a71c7368428c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/1; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 954fa84b901992d2648e93c6a55ae108d8d529884c407e18a938bc5e9c305d9b

Retain the old N_grad upper minimum and lower bound 1. Matching rates and the extent of any larger one-call region remain unassessed. The c3 resource interpretation remains separately unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: d1714c5661e858a53d24d42e19d395785c39bfa70c269c805fdd4c4ef413e4fc

0<ε<(1-min{μx,μy}²/β²)R²

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: f4894de2f18ff57f677594455e08616ef1e3c63a01e760da8b41123fea362612

Because 0<μ=min{μx,μy}≤β, the threshold (1-μ²/β²)R² lies in [0,R²). For ε>0, exactly one of ε≥R², threshold≤ε<R², or 0<ε<threshold holds. The last cell is empty when μ=β. Thus the three parameter cells are disjoint and cover the primary target. Listing c3 on the positive cells records a coextensive parameter overlay with a distinct native resource ID, not an identification of its resource with N_grad. The primary q1 one-call cell selects c_one_call; secondary-resource coverage remains conditionally unassessed, not jointly closed.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 002000eb2d865eaecbefa9f7ff438dccb7cf7ab9c820ed5cf29444bb0d2dec18

No uncovered parameter tuples for the primary N_grad target. Scientific assessment remains incomplete for sharper rates on the remaining positive region and for c3's unassessed resource projection; coverage is not a claim of optimality or absence of other bounds.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 22cceea16919b9407d60a0550227997613436713d3c20d8fc3ae164926c1112a

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: b15845990001410fc65afe0c08c612d342b5f9357baf4e9de7388ca403f90122

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: eb6eeacee3722c01401df8c637be7f6aec481b3b7adfba95b663bb709938a2fe

The expansion gives error≤(1-μ²/β²)R² with exact constants and includes equality. The retained zero-query impossibility gives the matching lower bound. The threshold is an exact sufficient activation inequality for this branch, not a necessary phase boundary for the task.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: d20a94a66fbedada76b74b161d6e1207573d85238cd283ab94e6ad03f9f39417

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 9e561832403dc390ad4ee28d37f25bedeaf6642cbce01f04de46af1a9c362722

CV_S_SCSC__finding__one_call_window

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 301c3c0ffde8aac7e837b2d9ece99f8401ee51923c1f559eeae603c68c5a9385

The new window receives an exact matching one-call bracket. A strict asymptotic improvement of the recorded accuracy rate occurs along μx=μy=β with ε/R² tending to zero. No claim of strict asymptotic improvement at every parameter tuple is made.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: f1293b27df98e33abd3b4f4b878531b937e484632e01fe7710b43646b70a60ac

Lower 1 throughout r1; exact upper 1 on (1-μ²/β²)R²≤ε<R², and the old upper minimum on the remaining positive region.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 80cdcd72f4d9a1569e7463d413944f39f03a8acfdeb38a706cf8f68e1ff89adb

Lower 1; upper O(min{(β/μ)(1+log(R²/ε)), (β/sqrt(μx μy))log(2β²R²/(μx μy ε))}) throughout r1.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: c74f6fa9fd9771044709dd493cdb0918bea26be4e859e64f3ea440b7716e2a5a

The native envelopes outside the new window, all of c2, and the scientific records of c3 remain unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 9a274d7073a1e212f0141f49eb16ed38df0dfb5713e468ea094de32b5f0523db

Fixed contract and (1-μ²/β²)R²≤ε<R², ε>0.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: a0826300143eea6c5a9ad7fa4ef8d18cf5d2650b5c7eeffbee1277a4a9bc068f

Take β=μx=μy=1, R²=1 and ε tending to zero. The former recorded upper expression grows as 1+log(1/ε); the new exact cost is 1 for every 0<ε<1.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: c002bc0290f564e621f4c851d1eabce93102ede6844b09e569e41b1034c6d6ae

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 7a81c774d36a5d7a89a998fba1b422e34260d1e0a73ca1a640c470b029afaa4f

The quantity already declares worst case over finite dimensions and tracks all independent scale, curvature and precision parameters. Consequently no controlled metadata normalization is needed. This annotation makes no new external theorem assertion.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 49c7e064789e21872f75696b6f112b5e7f273996ed349c99bfdf284441c8999b

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 474b8b3f7132416a8e5272dc6cbe6a1d126d356b8858be05cd5d190a74321048

CV_S_SCSC__finding__joint_accounting

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 5a2f1d3d83e628bbb95a57e7066f9f216d1f76d4ca7ad8cd41955dccb4da3f7d

None from presentation restructuring.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 5bfbb48742c06829e00d2e659d00f792338867f118bfe78b3b40d1e555c574c0

All old scientific statements are retained conditionally. Their parameter roles, guards, excluded cross-resource uses and assessment limits are explicit; the separately supported b7 change is not justified by this presentation finding.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: a790bb463f74f0db72e0ed82fb29c2ec39216272e2fddac9b6fc0d55377c0972

The frozen scientific rows: c1's old positive-cost branches and lower 1, c2's exact zero envelope, and c3's unassessed resource record.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: cfc104c323eb5238551032ecd6c3e25eb3297301b3b26b674f474d4984d6103e

All scientific rows and statuses except the independently justified c1 upper-envelope addition.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 703d47d8151f0b023399d1bdaf02cc493d0b56cf330b59ca0179cdc5153034bc

The complete fixed primary parameter domain and the registered c3 overlay.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 957bc7a41aa98831424605557ff4b837b02abece1f3e127496ddb17ad5cefe6a

The three domain predicates form a partition; c3 remains a distinct resource overlay rather than another primary parameter phase.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: d357ea17d13ef1538ddc6bd6109310624d1f6651c6f23703675384cbad51c1b7

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: c54fa6ee0b1b151fb18018c455f99c23b2f9356a251c2bbf89956056e5ee2c71

This publishes the existing proved matching one-call bracket on precisely one_call_window. The c1 taxonomy correction is a separate display correction; it is not evidence of a new scientific rate or domain extension.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: a64b4b265f46a4619126e01ff8ff1eda35d121a3605caed15b0a21f36f151c42

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 34e9595b40cb1d578f284b90911255f39a1f58043a2ee091eef436267b309022

CV_S_SCSC__finding__register_existing_one_call_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 309c9ca8e4dcc215bac8343dd91f1045e0dfafa802abf85f5157530299de51e5

Registration of the already proved sufficient region only; no new inequality, larger one-call domain or strict old-domain-exterior gain is asserted.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: e787771a4662ea7dcac55aa0bd87b91c1f99f5e81ba5f050a5f1d814ad66a648

The dedicated c_one_call comparison registers upper=lower=1 using unchanged b7/b5 and their exact guards.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 0b9b65448ae166e75c39ad9e17c15e41cab27f3211dd343bb35353f765d37707

The exact one-call consequence of b7 and b5 was already proved inside the positive primary comparison; it lacked a separate native optimal comparison.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: d8bd254f5b6297a4d2cc64cc51ea413ae28fb608d8f242312bc3dfa47a249414

All native inequalities, b7 validity, broad c1 rate, c2 and the distinct c3 resource.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: ff883c67d2383d99072037a22faff54bf1939b07bb3888af9107cfd57a90e238

0<ε<R² and (1-min{μx,μy}²/β²)R²≤ε

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 0fe240d7e23f7882296014bb534f582ba18fc20159b43a46b71c798380935ea2

Native c_one_call selects b7/b5 with proofs CV_S_SCSC__proof__one_call_window and CV_S_SCSC__proof__zero_query_necessity.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: bb9434e2d9cabf64aac68860bfa3672d509adf55570cf6b85dfd769e6af9e354

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 7dde4805df431bd381074646b18edc7ff36f80c9ded074b94e7ea9402ef9a04e

Classify the existing broad registered gap using the canonical polynomial_gap code with joint curvature dependence, keeping its formulas. Publish the accepted b7 one-call witness and b5 positive lower on r4 as a separate native optimal comparison; no maximal one-call domain or global curvature closure is asserted. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/impact/3/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: ab8b8829be75d448bb9729095b6d1fe7527c5da3aeddba127aeef2aa3a8637a7

curated_feedback_CV_S_SCSC_20261116_2a144b4edf

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

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

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: b0e2de1a6219912bb3d1828d414f9fb5f4efe61bde4dec1784e2591a0ac7c950

Primary target: CV_S_SCSC__main__q1 under main/g1 and resource_f845d741ab, minimizing the fixed worst-case number of complete exact joint-gradient responses for deterministic algorithms with arbitrary adaptive queries and measurable outputs. R²>0, ε>0, β≥max{μx,μy}>0; μ=min{μx,μy} is the native derived parameter CV_S_SCSC_p_98f870ad39. The quantity takes the worst case over all admissible finite block dimensions with d=dx+dy≥2, as already stated in its analysis_scope; it is not a fixed-dimensional complexity function. No dimension dependence is hidden in constants. The separate registered resource_cc7c360256 comparison remains unassessed as a resource interpretation.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 55c7d3b6c773648cbe2b6f15f44db716542b38c09e62ebff79d9fe63abdfc252

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: f9abdc6930db991e6ef4438392c294cc88a23b1b10dcc00e92dde547ade1151a

Complete a reviewed FOAM-to-N_grad transfer, including the full initialization-dependent accuracy cap and all charged inner calls, before adding any new bound from arXiv:2205.05653v1 or identifying resource costs.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 5a1d703d9a9465283c424809fbcf6e3d58212236f835edcd1851608ffba351b3

Read the original Zhang et al. (2021) and Ibrahim et al. (2020) lower-bound theorems and verify unrestricted deterministic algorithm coverage, dimension windows, accuracy scaling and subclass/oracle transfers before proposing a sharper lower side. Only their secondary citations were read here.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: bcd6d8e785da977173037e8fb468212cdb98e83e20752fe8ee1b93fc2973da58

Assess sharper rates and any larger one-call region outside the sufficient new window; this proposal does not characterize the necessary one-call boundary.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 957149f7358451681cf723be9dca502a4614b98456d5b6e3fbc3e6e7cf204ce7

The finite research map is only partially completed. The exact-id bibliography query was terminal and fully exposed, but the broader main-rate routes remain pending; no exhaustive literature or global strongest-bound claim is made.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 5ccec26afe03d02b9f161e5961cb38009eab1d0bd4cc1e2fd85700bd424720e0

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 20b9d8825149f92343da4947e040d5b1774fc3a3444cb1c8a38e64cc1dd4c5a4

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: b1d8018e673d141d1d4e5ed487c1e4c03ff719829000a552458a64f3b9135805

Conditionally retain the old two-call extragradient upper bound; no fresh recertification of its full proof is asserted.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 9f78ccdcee62fc7d43316da0d6656f4713ada948b1c587043d6b69e5529961e0

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: b9e6da6b1707e7a0a80a9b67c5b206cf27e74daa147063084849197187e8d309

SIX_PROOF_395ee6ec1cc4

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: c9154bf4e1778733ce9c48ba92d5f14839231df9bca113e3fdb63b732c0a7126

Accepted full-space μ-strongly monotone, β-Lipschitz saddle-operator argument.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 57685cb603d15fef1d5d21e45b7dbf13a287ce63391b1dbf659afd7d8402f70a

Frozen /proofs/0; canonical hash ed25d4da4dc5609ff265ec3c0024b1f61acc06fe9502942c4aeee8d5bd12a394.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 9111286a9f4ce53f6fbd73b620a932dcb90e7757a9cc811f0f688f1ab9424fac

Fixed contract and r1.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 9fe63e88253a3de8138e70e2a932e42bdeb1386e8c362b01e52fddf200bab17c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 838604048ec56697aad1661b610178b25815332ec75515a72db844dd6c436f9e

Retain the legacy claim only. No new scalar resource mapping or new source-backed adoption is made.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: bb0fd83ca093ae92a8106a428fed7ef8805524589da3ed9cde0e954eedcf67cd

The frozen zero-regularizer FOAM branch, retaining its initialization qualifications.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 776b472c87b512ba0e5a0f58fe4183ad16a0d2c08555465be55da829d890cf4e

Frozen /bounds/1 and /evidence/1; source theorem is arXiv:2205.05653v1, Theorem 3 and Corollary 1.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: c49c5791ab63d4d6231a4317e09a8390071496aff74ba9f7f840dd7f9d0d10b9

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 3955644ea31830023ddc491d217405d880bb335277207c99c20ce790a53eef45

CV_SRC_scsc_optimal2022

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: a38175c94787cb53922f2ba3426b91b116f506415b0587531fc9ade0425b1592

Unchanged r3 and resource_cc7c360256 comparison.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 0d5d7b781e3a2cec0f2821f3f8136afe18d9e15ae797802379633ce23a8fcff5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: b85cb91fb395cf9dcf80030a7d30cc4ea5bf6df29bcc5aaafa4dbc8cf09f521f

Unchanged return-z0 algorithm and exact zero cost.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 5a465e81c4ef3b3d5846d2a9e13ec75708f723b117e8aca6e2d179a45d417db1

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: fee73030872b486f7d1c69de7df115f7c666accc94505f385dc9f80ae889e1b3

SIX_PROOF_cea15d68accf

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: da7619f6a314672b6a83fa2cb60c8df8cfde82eac0aafaa60efbdab7006ea913

The fixed initial squared-distance promise.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 28e7e34326f56d0f6717e0c0afd1a3acd00e780ac490a76b7cc468679b1dcf3d

Frozen /proofs/1, read as part of complete /proofs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 9b8cf127e8e600f1037078e23563d65038bcc867718a589dd1593b58f065f36e

ε≥R².

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: d5648926f6899330fd749348aa88f9664a848fff369137c8983608696e92f8cd

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 90b468db557524f11d05c90135fc6dbb5d279bdaffe60bb9d2d054e8162727d8

Unchanged zero lower bound matching b3.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 49189535c92347f104367dff5bb261fc84e98f01214dcf2873329f7c4d9de56e

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: ecb5b0cf10816f69a1ebcfeeb9d874992f97a629912a236df2939838ef498137

SIX_PROOF_c5f449dbde2c

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 96953c28c44769e7c0817a79bd25253ec72ac8ace40b87dd69da9f9843854377

Nonnegative query cost in the fixed resource contract.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: d416701bf2e18baed7e2107da2bebf847c2ff69059838e9b408de5f9cbb7360f

Frozen /proofs/2, read as part of complete /proofs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 0fa8b7a24561c2e77872393cfdf81fc117e09e3e0fca650721da88e7408b0f09

Unchanged r2.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: bcd111db5d45a387df8c557641da7898596d2f6553880ba2a5049133a1815c20

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: c5d361126e87f94de154836393f169ed2c2bac56d2c51679348977701d6cb5f1

Conditionally retain the unrestricted deterministic lower bound 1. Restriction to the new parameter window preserves the hard instances and all query/output rules.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 6d731cd49602aa0eea12de02d4dd041007827801ddcd24d007250b76a0cddff9

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 602acaf4e7bfd37b67840d2142d804b3ae2442513d580ee13f1466695067a2c1

CV_S_SCSC__proof__zero_query_necessity

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: b1d23d0b43a8eb1e823f1167b4c9838eee989f4ac5f2eaa031710433f9043687

Two shifted separable quadratic saddles under all fixed public parameters.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 27c6436a5f10209fba202c00bc50ee7b3337f69bfcc80ca4d7a814d87d8f8a90

Frozen /proofs/3, canonical hash acc1ca97d87d617054c8d4d41913e819efaebd5f8386ca4c193a68a90c272ee2; /bounds/4, hash 8c2f091c42c592c0f9f463dbed24a3628fe9fe9950799751c6591553bf2b7791.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 10a6e11eb03e0d62231a1d5da8cd10642ab98bbef846169e9c4b2aff65c7fd90

All r1, including the new one-call window.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 3c47a5d130da32e757cff09e3875dabbe0465a1db9ca0e20394e98ebe7fc4258

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 17840e2fadebaa7c661364d742341b10545db8de3713364e40e2b4e45d40f2a5

Retain the existing N_grad upper branch conditionally, without reopening or newly certifying its external theorem.

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: 9baf1eac75b9479d30f1b230056008e8abcffb6522446681e7013cca3f6d37e2

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 638f4cbda063d9d629664524c0ff149cfcd2614e4b57a142827ada82b9c4e520

CV_S_SCSC__proof__pce_dm_transfer

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 69d71879e335cbd33dab0f14ede08d93dd3681c7935522c019eea0ff03654d72

The accepted oriented PCE-DM theorem and initialization mapping recorded in the baseline.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: f2795bfee20aaf403c2d88210e9b797df25abfce344f03ef8eb6911bcac3d251

Frozen /bounds/5 and /proofs/4, read completely; original source/version locators remain unchanged.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 72d6903c1fb67854d78b4d62143211fd3d0e868a931fc1bf4d9af6313f40a862

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: 42f124d2bfb4805039fd1a1e75593d5f9c5c5afc92b961541fd22dd08e552a25

CV_SRC_pce_dm2026_v2

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 9111286a9f4ce53f6fbd73b620a932dcb90e7757a9cc811f0f688f1ab9424fac

Fixed contract and r1.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: daaa9b8dcc0eebc3d5669076d9e82aa4c358811111805f7e8396d26f005070c7

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 501e80569cdcd979e228d4ed032e9993ee4e84663d4473c5d9a2ab1a50154c77

Query the complete gradient once at z0, apply the known sign change to its dual block, and return z0-(μ/β²)F(z0). Exact arithmetic is uncharged; no other interface, function value, Hessian, inner solve or certificate is used. The squared-distance expansion proves the target guarantee uniformly.

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: f10fd2c9b089a1c6a5dc05938891827d49d280d8d625c3c83fb7866d8db1c5e8

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: a5179815c27155338e6207801cba86420bf375f5c5e7a7064ca401c2a7db6213

μ-strong monotonicity, β-Lipschitz continuity, F(z*)=0 and initial squared distance at most R².

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 4007ba295b6ed903ab7d7f851798ba52e504beb5db69fd783bda0f587743bd13

New proof from exact frozen /proofs/0 operator premises, hash ed25d4da4dc5609ff265ec3c0024b1f61acc06fe9502942c4aeee8d5bd12a394, and the fixed contract.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 291aac486670eae4cbca32b1a63aba007ea53c86259d27bbab1a44819d1afd5b

Fixed main/g1/q1/N_grad contract with (1-μ²/β²)R²≤ε<R² and ε>0.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 15e2c9d3aa529eb78ec30e3d320f0fa44e395a2eb8bed3ac50fe79e6824731f9

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: be380108237389c8bc46013a26f746a23a770b7f7b6955e678202835b82f447e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 0e6d49517a5b4011258a25604aac30348d0ec096d5f25317806fe14d22a624f3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: da341add53de3c2f3dc58942bd4a4a26953eb21018823bd5d551e98136b0b264

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/5; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/6; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: d20a94a66fbedada76b74b161d6e1207573d85238cd283ab94e6ad03f9f39417

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 4158d1ffade2dfba7f186c05a67cf75d5bfab63cca809896c54ace87536b35ca

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: da341add53de3c2f3dc58942bd4a4a26953eb21018823bd5d551e98136b0b264

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/5; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/6; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 8486deef2272c561397c694142920e0a15508cee77cfd5064b57d2e51b3ebbf1

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 35eb67b1a2814bc8019354230c6c9572b2f58456dd575638e8a20dc623699ec3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: da341add53de3c2f3dc58942bd4a4a26953eb21018823bd5d551e98136b0b264

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/5; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/6; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 895cbf8290c4c4653d82964aecb7d77bba7035af2b81f2a1f65cc9bd82035d0f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: b40db94fd8ac2b311d48b68b414b0372acc2ea109748f194b723ea06676c6583

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: da341add53de3c2f3dc58942bd4a4a26953eb21018823bd5d551e98136b0b264

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/0; canonical SHA-256: 22308e2c9704a53c1b9a040555bdf5ea59e4b46f09f039daf2d6ee64aa72e984

CV_S_SCSC__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/1; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/2; canonical SHA-256: 7d6048110f74c97a50a54a497148eea9787f7feaebdd72ae4d3dd54d1bf9afe8

CV_S_SCSC__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/3; canonical SHA-256: dea82ef92e69b7abeed0545e10226cba80c698a35e17541e300e292ceb20f3d7

CV_S_SCSC__main__b4

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/4; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/5; canonical SHA-256: 03c6c4e9b18bf28252218650786a3609132cb16e8fa525d699f1670fb1e64876

CV_S_SCSC__main__b6

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs/6; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: a64b4b265f46a4619126e01ff8ff1eda35d121a3605caed15b0a21f36f151c42

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: ec07d3f108f4f9989afec3b905e27e63d33ad2664c0756a775f1463d473c4e5b

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: f9abdc6930db991e6ef4438392c294cc88a23b1b10dcc00e92dde547ade1151a

Complete a reviewed FOAM-to-N_grad transfer, including the full initialization-dependent accuracy cap and all charged inner calls, before adding any new bound from arXiv:2205.05653v1 or identifying resource costs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: bc7939b4ab59b9e280dcdd761c0480c69de71ba0ab14444ce3aa72762e45addc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 5a1d703d9a9465283c424809fbcf6e3d58212236f835edcd1851608ffba351b3

Read the original Zhang et al. (2021) and Ibrahim et al. (2020) lower-bound theorems and verify unrestricted deterministic algorithm coverage, dimension windows, accuracy scaling and subclass/oracle transfers before proposing a sharper lower side. Only their secondary citations were read here.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 343e246c2860809b269c0e39985982ad31032b13ce75e52c3280728c980ce72c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: bcd6d8e785da977173037e8fb468212cdb98e83e20752fe8ee1b93fc2973da58

Assess sharper rates and any larger one-call region outside the sufficient new window; this proposal does not characterize the necessary one-call boundary.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 1ffd2ccb61fec732e6b8df8cc84fe541037f6f73478b6d051617fbe5c84aeb41

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 957149f7358451681cf723be9dca502a4614b98456d5b6e3fbc3e6e7cf204ce7

The finite research map is only partially completed. The exact-id bibliography query was terminal and fully exposed, but the broader main-rate routes remain pending; no exhaustive literature or global strongest-bound claim is made.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: e5829c6163b86662d7c3dfa81bdb55052fa0b37d46a2fb86920b6e9868ef99c1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: 1eed4581c148b3c58dc3cb6f152f8949b7ffda6bed41530cf78e87ae272b643c

Directed pending route: convert the FOAM/b2 native/source resource interpretation (including the unassessed resource_cc7c360256 overlay c3) into the primary N_grad resource_f845d741ab of c1. Full initialization-dependent accuracy restrictions and all charged inner-gradient calls must be proved before using this route. The two IDs are not identified, no cost bound is inferred in the reverse direction, and no new bound is adopted.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 928e57ed9286c1a6d10d84a8cef88b448e1d72935996eb32dd6c5a74735a9e4f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: 22c92a2bcb9f1fadc066c15d08ac906a81be01912442b6a4296a1927862923aa

CV_S_SCSC__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: aafb8db2458363e03a3e95afa04f08333f76a18fe2087c841c42357ef59a262c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/0; canonical SHA-256: 5903c7f7845460a20c408a8feb02ce19dacece07decc77c54a63b24cff229081

remaining_positive_region

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 487420b0d78176f1111f17728559b3fbea0f8f4ef9c5a4757f98a71c7368428c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 41a7bbefee082f6b636ce232214c0aceda2aaea65589a0efec3fa7a3b2e6d0bd

typed-foam-to-gradient-cost

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: 98597b09cb9d7213d92c4bfee40d01abd339cd97712bcb287fe9f17bac42f24f

resource_projection

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: f9abdc6930db991e6ef4438392c294cc88a23b1b10dcc00e92dde547ade1151a

Complete a reviewed FOAM-to-N_grad transfer, including the full initialization-dependent accuracy cap and all charged inner calls, before adding any new bound from arXiv:2205.05653v1 or identifying resource costs.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 14852128120cdee7b653585d030681830973332abcdccf2175902599ca428a8f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: 846489ec303f47bbd43561bfab2119c9cd8ddba354dacac468088385957a0614

The native optimal c_one_call comparison already in this candidate selects precisely b7 upper=1 and b5 lower=1 on the sufficient one_call_window, with the two native proofs. This resolves publication of that established region only; no transfer into c3 or larger exact-one characterization is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 1b8c0ee5fc7deeb5d24e27317f2f073994b3a8f950c4d2a40b98f2214431fc09

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/0; canonical SHA-256: 61310f16ecdf018672a410e98f725c6384dbe6f1a22da152dbb43035d2518a90

CV_S_SCSC__main__b5

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs/1; canonical SHA-256: 1dcbaf4eda1c6fed572929202726a6b73e1bb6a0d2263a35a763bcd7b78243ae

CV_S_SCSC__main__b7

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 251c7dab4b70cecb1889e0e82af105ef7e981ee65e54fa75e2f0ac1ab25d1b1a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids/0; canonical SHA-256: 36c0adc24a0089cb7f6ec1bb3c45f306afe4933c257f68b85d29ede58c5b4ae2

one_call_window

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: a64b4b265f46a4619126e01ff8ff1eda35d121a3605caed15b0a21f36f151c42

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 899f697d7231064818d3a4609c2a1f38c6147dc7707ee03dad1b368d00946e84

typed-publish-existing-one-call

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: 50133df05f664fa7a089f5165d8e064594aa92d2dedff6eb73c481199b11b5cd

closed_region_publication

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 14f512193f3bbbcc5d1feb805884f0cbf5b908d9d03cebcc21db50aa9d2f6e6d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs/0; canonical SHA-256: 4c2e5662038f95dea3b5a1d81e0203e2ef1f854b1e6ad29bde2f18f9512c3c6d

CV_S_SCSC__proof__one_call_window

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs/1; canonical SHA-256: 602acaf4e7bfd37b67840d2142d804b3ae2442513d580ee13f1466695067a2c1

CV_S_SCSC__proof__zero_query_necessity

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/obligations/10; canonical SHA-256: 41e6424e71baad3c8fa571eb8050b3a8c4c32fb294108ea1694b20fd185b4d4d

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids; canonical SHA-256: 1b8d095219e5ef4bfe2de6319977f6952e3f362737b034a99362e1217f8b24a7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/0; canonical SHA-256: 02f6ca78c922362ddc39d7bf87073090b4e0e69f255c74c95ca8beef1f3ab09d

CV_S_SCSC__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/1; canonical SHA-256: 46ae16d980aa9b27e96424a3c619773c60fd79ce8f58ce64e64aea6aa0a79079

CV_S_SCSC__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/2; canonical SHA-256: aafe79454845d196f304e99faeb7b2322ef089103ea3ecf0c87d2c85e4117f75

CV_S_SCSC__main__c3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/comparison_ids/3; canonical SHA-256: 7c9fbecc240fecf199752b69bca4b14544cd0a178cb14f39d62eebaf7334f2ec

CV_S_SCSC__main__c_one_call

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/10/id; canonical SHA-256: 7b66618750ce506ccf40819cef50f764846b4ebf660cc36789c8ef551ca05dfe

curated-scope-limit-2a144b4edf

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

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 691747d9010c929b820a72a580597f29c730e78aacee714db1588ba28ebb9466

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: bf42410298325d95003ef6397a31db343a461e0f2a265c8eca83e8fa2898bf63

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: b0e2de1a6219912bb3d1828d414f9fb5f4efe61bde4dec1784e2591a0ac7c950

Primary target: CV_S_SCSC__main__q1 under main/g1 and resource_f845d741ab, minimizing the fixed worst-case number of complete exact joint-gradient responses for deterministic algorithms with arbitrary adaptive queries and measurable outputs. R²>0, ε>0, β≥max{μx,μy}>0; μ=min{μx,μy} is the native derived parameter CV_S_SCSC_p_98f870ad39. The quantity takes the worst case over all admissible finite block dimensions with d=dx+dy≥2, as already stated in its analysis_scope; it is not a fixed-dimensional complexity function. No dimension dependence is hidden in constants. The separate registered resource_cc7c360256 comparison remains unassessed as a resource interpretation.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 87cdb90b420e57739e7e3ffcd4616256f1261a90d443b70f61f5904cc71da20c

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 5f32476a7e06259e3ec526e809326075fb1d74b902f718bad400e01f27bedf37

CV_S_SCSC_p_a14d6028b2

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: d101200f4f705024e3192c8e5e13e66d70b87da898d421ed4f3b0a4576f7acd7

CV_S_SCSC_p_6490ff790f

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 3b94cc61292912e2dbde4a37ce4420c6b81ce6f366ec9c18c41684b4a3c98a80

CV_S_SCSC_p_a46dbb5c50

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 7d52fa6578acc10a11e2013894ae92c10e917e76bafcb1c527c046787b4f6139

CV_S_SCSC_p_e5b1bf8e9c

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: d717b05bc083c1563357040aa3afe8df9830f87d8640bed9839e879e4ab2476b

CV_S_SCSC_p_a8f9f9941d

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: bed3fe79f76912d4cc4a2b69a24fa96b1c526f51d957fd381dda3bcd9addadbe

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 5f32476a7e06259e3ec526e809326075fb1d74b902f718bad400e01f27bedf37

CV_S_SCSC_p_a14d6028b2

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: d101200f4f705024e3192c8e5e13e66d70b87da898d421ed4f3b0a4576f7acd7

CV_S_SCSC_p_6490ff790f

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 3b94cc61292912e2dbde4a37ce4420c6b81ce6f366ec9c18c41684b4a3c98a80

CV_S_SCSC_p_a46dbb5c50

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 7d52fa6578acc10a11e2013894ae92c10e917e76bafcb1c527c046787b4f6139

CV_S_SCSC_p_e5b1bf8e9c

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: d717b05bc083c1563357040aa3afe8df9830f87d8640bed9839e879e4ab2476b

CV_S_SCSC_p_a8f9f9941d

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 56c1e07dbf3a13ab3d98234e7257265aab936d7ba3c675e737782331ba96148b

CV_S_SCSC_p_cffd0f6f5a

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Dmitry Kovalev; Alexander Gasnikov. The First Optimal Algorithm for Smooth and Strongly-Convex-Strongly-Concave Minimax Optimization. 2022. arXiv:2205.05653v1, 2022-05-11.

https://arxiv.org/pdf/2205.05653v1

[2] Minhao Zhang; Zi Xu. Near-Optimal Single-Loop Predictor–Corrector Extragradient Method for Strongly Convex–Strongly Concave Minimax Optimization. 2026. arXiv:2609.20327v2, 2026-09-28.

https://arxiv.org/pdf/2609.20327v2
