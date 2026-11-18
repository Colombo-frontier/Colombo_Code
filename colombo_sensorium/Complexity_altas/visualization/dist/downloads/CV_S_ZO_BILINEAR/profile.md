# Bilinear-affine saddle problems with exact scalar values

**Setting ID.** `CV_S_ZO_BILINEAR`

Minimax optimization

$$
\min_{x\in R_xB_2^{d_x}}\max_{y\in R_yB_2^{d_y}}f(x,y),\quad f(x,y)=y^\top Ax-b^\top y.
$$

**Status.** Other quantified gap present

**TASK tags.** formulation: Bilinear affine saddle; task family: Minimax; task family: Saddle point

**MODEL tags.** geometry: Two balls; structure: Bilinear affine

**ORACLE tags.** feedback quality: Exact; interface family: Exact payoff value; operation: Payoff value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar function value (order 0)

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N value; precision: Bit precision not counted

## 1. Setting specification

### Task

$$
\min_{x\in R_xB_2^{d_x}}\max_{y\in R_yB_2^{d_y}}f(x,y),\quad f(x,y)=y^\top Ax-b^\top y.
$$

### Admissible model

Assume $A\in\mathbb{R}^{d_y\times d_x}$ and $\|A\|_{\rm op}\le C$, with no norm bound on $b\in\mathbb{R}^{d_y}$. The two balls $R_x,R_y>0$ are known, compact, and convex. The payoff is affine in each block, so a saddle point exists.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $C$, $R_x$, $R_y$, and $\varepsilon$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(x,y)\in\mathbb{R}^{d_x+d_y}\longmapsto y^\top Ax-b^\top y.
$$

Responses are exact noiseless reals, and queries may lie outside the ball. Ball projection uses public geometry and does not supply matrix-vector access.

### Output

Return $(\widehat{x},\widehat{y})\in R_xB_2^{d_x}\times R_yB_2^{d_y}$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\operatorname{Gap}(x,y)=R_y\|Ax-b\|_2+R_x\|A^\top y\|_2+b^\top y.
$$

This is the exact global saddle-gap expression; it is finite and nonnegative.

### Resource accounting

Each scalar value costs one $N_{\rm value}$ call.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\operatorname{Gap}(\widehat{x},\widehat{y})\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$C$: Spectral-norm bound on the coupling matrix $A$, a problem parameter **Domain:** Positive real number.

$\|A\|_{\rm op}\le C$

$R_x$: Radius of the primal Euclidean ball **Domain:** Positive real number.

$X=R_xB_2^{d_x}$

$R_y$: The Euclidean-ball radius for the dual variable. **Domain:** Positive real number.

$Y=R_yB_2^{d_y}$

$d$: Common block dimension in the balanced-dimension regime; used only where $d_x=d_y=d$ **Domain:** Positive integer.

$d_x=d_y=d$ in the balanced-dimension regime only

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\varepsilon$: Tolerance for the true root residual or Euclidean norm of an admissible graph element. **Domain:** Positive real number.

$r$: The smaller of the two block dimensions. **Domain:** Positive integer.

$r=\min\{d_x,d_y\}$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\|\cdot\|_{\rm op}$: Matrix or multilinear tensor norm induced by the Euclidean norm **Domain:** Matrix and derivative tensors used in this profile.

$\|T\|_{\rm op}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}\|T[u_1,\ldots,u_j]\|_2$

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm value}$: The number of exact scalar-value calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$A,b$: The hidden coupling matrix and dual affine term. No norm bound is imposed on b. **Domain:** $A\in\mathbb R^{d_y\times d_x},\ b\in\mathbb R^{d_y}$.

$f(x,y)=y^\top Ax-b^\top y$

$\operatorname{Gap}$: The displayed global saddle gap maximizes and minimizes over the output strategy domains. **Domain:** Nonnegative real number; not a gradient norm.

$B_2^k$: Closed k-dimensional Euclidean unit ball **Domain:** $k\ge1$.

$B_2^k=\{u\in\mathbb R^k:\|u\|_2\le1\}$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm value}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - The general accuracy window.

**Region.** $0<\varepsilon\le CR_xR_y/32$

**Quantity.** Q1

**Resource.** Number of scalar function-value responses

**Status.** Other quantified gap

**Lower bound.** B1

$$
\max\{5r/32,\ (r/8192)\min\{r,\sqrt{CR_xR_y/\varepsilon}\}\}
$$

**Upper bound.** B2, B3

$$
O(\min\{d_y(d_x+1),(d_x+d_y)(1+CR_xR_y/\varepsilon)\})
$$

**Gap or comparison.** $\frac{\min\{d_y(d_x+1),(d_x+d_y)(1+\Lambda)\}}{r\min\{r,\sqrt\Lambda\}},\quad\Lambda=CR_xR_y/\varepsilon$

**Comparison argument.** Only the certified envelopes are compared. In unbalanced blocks, $r^2$ is not a substitute for general rectangular reconstruction cost.

### R2 - Balanced-dimension high-accuracy saturation regime

**Region.** $d_x=d_y=d,\ 0<\varepsilon\le CR_xR_y/(32d^2)$

**Quantity.** Q1

**Resource.** Number of scalar function-value responses

**Status.** Optimal

**Lower bound.** B1

$$
\Omega(d^2)
$$

**Upper bound.** B2, B3

$$
O(d^2)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** This recovery regime lies within the general theorem window. The active branch of the lower-bound minimum is $d$, and coefficient recovery requires $d_y(d_x+1)\le2d^2$ calls. Higher accuracy does not increase the information-recovery cost.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - quadratic scalar-value lower via polarization

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\max\{5r/32,\ (r/8192)\min\{r,\sqrt{CR_xR_y/\varepsilon}\}\}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00345v1)

**Dimension conditions.** Within the stated applicability window, the claim holds for every $d_x,d_y\ge1$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\max\{5r/32,\ (r/8192)\min\{r,\sqrt{CR_xR_y/\varepsilon}\}\}
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.00345v1) theorem: Theorem5.1; TheoremG.1; PropositionG.2; section: Sections5,G; pdf pages: 8; 42; 43

The polarization reduction uses two source scalar-value queries per target payoff. The compact-domain gap expression and the total coefficient-recovery count $d_y(d_x+1)$ are retained explicitly.

### B2 - exact coefficient recovery

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Source Proposition G.2 explicitly gives a deterministic exact-value algorithm. Both coefficient recovery and exact finite-difference Mirror-Prox use no random choices.

$$
O(d_y(d_x+1))
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00345v1)

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N value.**

$$
O(d_y(d_x+1))
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Query all $d_y(d_x+1)$ affine-bilinear coefficients, then solve the known compact-domain bilinear game using internal computation excluded from the query count.

**Source location.** [1](https://arxiv.org/pdf/2610.00345v1) theorem: Theorem5.1; TheoremG.1; PropositionG.2; section: Sections5,G; pdf pages: 8; 42; 43

The polarization reduction uses two source scalar-value queries per target payoff. The compact-domain gap expression and the total coefficient-recovery count $d_y(d_x+1)$ are retained explicitly.

### B3 - exact finite-difference Mirror-Prox

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Source Proposition G.2 explicitly gives a deterministic exact-value algorithm. Both coefficient recovery and exact finite-difference Mirror-Prox use no random choices.

$$
O((d_x+d_y)(1+CR_xR_y/\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2610.00345v1)

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N value.**

$$
O((d_x+d_y)(1+CR_xR_y/\varepsilon))
$$

**N projection.**

$$
O(1+CR_xR_y/\varepsilon)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Coordinate finite differences are exact for affine bilinear payoffs. A joint gradient can therefore be obtained with $O(d_x+d_y)$ scalar queries over the full space, after which Mirror-Prox applies.

**Source location.** [1](https://arxiv.org/pdf/2610.00345v1) theorem: Theorem5.1; TheoremG.1; PropositionG.2; section: Sections5,G; pdf pages: 8; 42; 43

The polarization reduction uses two source scalar-value queries per target payoff. The compact-domain gap expression and the total coefficient-recovery count $d_y(d_x+1)$ are retained explicitly.

## References

[1] Yuriy Dorn; Darina Dvinskikh; Timofei Loginov; Osman Osmanov; Aleksandr Shestakov; Nazarii Tupitsa; Alexander Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. 2026. arXiv:2610.00345v1, PDF header 2026-09-29; downloaded 94-page version.

https://arxiv.org/pdf/2610.00345v1
