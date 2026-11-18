# Higher-order convex-concave saddle-point problems: complete scalar jets and tangential residual

**Setting ID.** `CV_S_HIGH_SADDLE_tan`

Minimax optimization

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$, with $K=X\times Y$ and $z=(x,y)$. The target is the tangent residual of the associated operator.

**Status.** Fully optimal

**TASK tags.** formulation: Convex concave saddle; task family: Minimax; task family: Saddle point

**MODEL tags.** convexity: Concavity in the declared block; convexity: Convex concave; convexity: Convexity in the declared block; geometry: Diameter bound; smoothness: Highest derivative lipschitz

**ORACLE tags.** feedback quality: Exact; interface family: Complete scalar jet; operation: Payoff complete jet; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Parameterized order p (see exact operation binding)

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal dual pair; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Tangential residual

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N jet; measure: N model solve; measure: N projection; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$, with $K=X\times Y$ and $z=(x,y)$. The target is the tangent residual of the associated operator.

### Admissible model

The sets $X\subset\mathbb R^{d_x}$ and $Y\subset\mathbb R^{d_y}$ are known, nonempty, compact, and convex; $K=X\times Y\subset\mathbb R^d$, $d=d_x+d_y$, and $\operatorname{diam}(K)\le D_K$. Queries and outputs lie in $K$; differentiability holds on an open neighborhood of $K$.

Fix an integer $p\ge2$. The function $f$ is convex on $x$ and concave on $y$; assume $f\in C^p$ and $\|\nabla^p f(z)-\nabla^p f(w)\|_{\rm op}\le L_p\|z-w\|_2$.

These conditions ensure existence of a solution. Derivative tensors use the multilinear operator norm induced by the Euclidean norm.

### Oracle interface

Public inputs comprise the block dimensions $d_x,d_y$ and parameters $D_K$, $L_p$, $\varepsilon$, and $p$, together with the stated initial point and feasible-set information. Analytic descriptions of hidden functions, operators, and matrices are not supplied.

$$
z\in K\longmapsto(f(z),\nabla f(z),\ldots,\nabla^p f(z))
$$

One exact query returns the entire derivative bundle, not just tensor actions along a selected direction. Repeated queries at the same point are allowed.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return $\widehat{z}\in K$, a feasible primal–dual pair $(\widehat{x},\widehat{y})$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\operatorname{dist}(0,F_f(\widehat{z})+N_K(\widehat{z}))
$$

This nonnegative error uses the declared Euclidean geometry.

$F_f(x,y)=(\nabla_xf(x,y),-\nabla_yf(x,y))$ is a derived operator determined by the scalar feedback.

For a closed convex set $K$, define $N_K(z)=\{v:\langle v,u-z\rangle\le0,\ \forall u\in K\}$ for $z\in K$, and $\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$.

### Resource accounting

Each complete jet call counts once in $N_{\rm jet}$. Projection and known Taylor-model solution counts are recorded separately; the main comparison counts only $N_{\rm jet}$.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\operatorname{dist}(0,F_f(\widehat{z})+N_K(\widehat{z}))\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the entire feasible product domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$L_p$: Lipschitz upper bound for the scalar function's $p$th Fréchet derivative in the Euclidean induced tensor norm **Domain:** Positive real number.

$\|\nabla^p f(z)-\nabla^p f(w)\|_{\rm op}\le L_p\|z-w\|_2$

$\chi_{\mathrm{tan}}$: Dimensionless accuracy ratio expressed in the units of the specified metric **Domain:** Positive real number.

$\chi_{\mathrm{tan}}=L_pD_K^{p}/\varepsilon$

$Q_{0,p}$: Sufficient accuracy threshold for integer rounding in the lower bound at fixed $p$ **Domain:** Positive proof constant with no specified numerical value.

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: This is the tangent-residual tolerance. The mean-square guarantee uses its square $\varepsilon^2$. **Domain:** Positive real number.

$p$: Fix the derivative order. The scalar interface returns through order p, equivalently through order p − 1 for the derived operator. **Domain:** Integer at least $2$.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\nabla^j f$: The jth Fréchet derivative of a scalar function. The complete derivative bundle contains orders zero through p. **Domain:** The quantity $0\le j\le p$ is a j-linear map taking j vectors to a real scalar.

$\nabla^0f=f$

$F_f$: Monotone saddle-point operator induced by the payoff function **Domain:** $K\to\mathbb R^{d_x+d_y}$.

$F_f(x,y)=(\nabla_x f(x,y),-\nabla_y f(x,y))$

$\|\cdot\|_{\rm op}$: Matrix or multilinear tensor norm induced by the Euclidean norm **Domain:** Matrix and derivative tensors used in this profile.

$\|T\|_{\rm op}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}\|T[u_1,\ldots,u_j]\|_2$

$K$: A known nonempty compact convex feasible set. **Domain:** A subset of Euclidean space.

$K=X\times Y\subset\mathbb R^{d_x+d_y}$

$X,Y$: Both primal and dual domains are known, nonempty, compact, and convex. Their product has diameter at most $D_K$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$N_K(z)$: Use the Euclidean normal cone of the closed convex feasible set K at the feasible point z. The same definition applies blockwise to $N_X$ and $N_Y$. **Domain:** $z\in K,\quad N_K(z)\subset\mathbb R^d$.

$N_K(z)=\{v:\langle v,u-z\rangle\le0\ \forall u\in K\}$

$\operatorname{dist}(0,S)$: Infimum of the Euclidean distances from vectors in $S$ to the origin **Domain:** Nonnegative extended real value.

$\operatorname{dist}(0,S)=\inf_{v\in S}\|v\|_2$

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\widehat z$: Joint output consisting of the two variable blocks **Domain:** $\mathbb R^{d_x+d_y}$.

$\widehat z=(\widehat x,\widehat y)$

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm jet}$: Number of complete derivative-bundle queries up to the declared scalar derivative order **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Number of exact Euclidean projections onto the known feasible domain, recorded separately from primary information queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm model_solve}$: exact known tensor-model solves uncharged; no unknown best-response oracle **Domain:** Nonnegative integer count; expected work is its expectation.

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm jet}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Main higher-order theorem regime

**Region.** Fix an integer $p\ge2$ and assume $\chi_{\rm tan}\ge Q_{0,p}$. Take the worst case over all admissible finite block dimensions.

**Quantity.** Q1

**Resource.** The number of complete jet responses.

**Status.** Optimal

**Lower bound.** B2

$$
c_p\chi_{\mathrm{tan}}^{2/(3p-1)}
$$

**Upper bound.** B1

$$
C_p(1+\chi_{\mathrm{tan}}^{2/(3p-1)})
$$

**Gap or comparison.** $O_p(1)$

**Comparison argument.** This is a synthesis across sources. Keep the scalar lower bound and the new VI upper bound as independent references; a source's near-optimality summary does not replace its native theorem statement.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - scalar-to-operator jet simulation plus log-free high-order VI upper

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** Accelerated Halpern and known-model subroutines with complete jets use no random selection. Scalar-jet simulation preserves this determinism.

$$
O_p(1+\chi_{\mathrm{tan}}^{2/(3p-1)})
$$

**Sources.** [1](https://arxiv.org/pdf/2609.23557v1) [2](https://arxiv.org/pdf/2609.28246v2)

**Conditions.** The operator $F_f=(\nabla_xf,-\nabla_yf)$ is monotone and its derivative $\mathrm D^{p-1}F_f$ has Lipschitz bound $L_p$. One full scalar jet of order p yields the complete operator jet through order p-1 without extra calls.; Use the actual monotone-VI algorithm and its output certificate. Proposition 3.6 of the scalar saddle-point source provides the structural map for the derived operator.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N jet.**

$$
O_p(1+\chi_{\mathrm{tan}}^{2/(3p-1)})
$$

**N projection.** $O_p\!\left(1+\chi_{\mathrm{tan}}^{2/(3p-1)}\right)$. Use the objective-specific $\chi_{\mathrm{tan}}$ and retain the dependence on the fixed order $p$.

**N model solve.** $O_p\!\left(1+\chi_{\mathrm{tan}}^{2/(3p-1)}\right)$. Exact internal solves use only models whose coefficients have already been returned. Internal arithmetic is not charged as an oracle query.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Derivation.** Let $S=\operatorname{diag}(I,-I)$ and $F=S\nabla f$. One scalar jet of order $p$ constructs $(F,\mathrm DF,\ldots,\mathrm D^{p-1}F)$ with the same $L_p$. Tangent residual transfers directly; by $\operatorname{Gap}\le D_K r_{\rm tan}$, a gap target uses residual tolerance $\varepsilon/D_K$. Combine the reduction in Proposition 3.6 with Theorem 3.1 of arXiv:2609.23557. This supplies no additional free oracle access to the unknown object.

**Source location.** [1](https://arxiv.org/pdf/2609.23557v1) Assumptions2.1–2.4; Definition2.1/2.2; Theorems3.1,5.1; Lemma5.4

Log-free O_p((L_p R_0^p/epsilon)^{2/(3p-1)}) operator-jet upper.

Source R_0=||x0-x*|| <= $D_K$, not a new diameter assumption. Full operator jet through p-1; same-point tangent certificate. All nested F calls counted. Exact known Taylor-model solves are internal. Fixed p. Deterministic upper satisfies randomized success2/3. Source does not itself supply unrestricted randomized lower.

Let $T$ denote the outer iteration count. Lemma 5.4 and (22)-(23) sum all inner-solver calls to obtain total inner cost $O(T)$. The counted object is a full jet call, so outer iterations alone are insufficient. Bound the source initial distance to a solution by the domain diameter $D_K$.

**Source location.** [2](https://arxiv.org/pdf/2609.28246v2) theorem: Theorem3.5; Lemma3.4; Proposition3.6; pdf pages: 6; 7; 8

The source scalar-payoff hard family directly covers arbitrary randomized algorithms. A general vector-VI lower bound is not converted backward to a saddle lower bound without a construction.

### B2 - scalar flat-gate convex-concave chain

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega_p(\chi_{\mathrm{tan}}^{2/(3p-1)})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.28246v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The deterministic hard construction requires $d_x=d_y=2N+2$. For randomized algorithms, dimension $d_x,d_y\le C_p(N+1)^3\log(N+2)$ suffices, where $C_p$ may depend on the fixed order $p$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega_p(\chi_{\mathrm{tan}}^{2/(3p-1)})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [2](https://arxiv.org/pdf/2609.28246v2) theorem: Theorem3.5; Lemma3.4; Proposition3.6; pdf pages: 6; 7; 8

The source scalar-payoff hard family directly covers arbitrary randomized algorithms. A general vector-VI lower bound is not converted backward to a saddle lower bound without a construction.

## References

[1] Xinliang Zhang; Lesi Chen; Linxuan Pan; Chengchang Liu; Junchi Yang; Jingzhao Zhang. Optimal High-Order Methods for Solving Monotone Variational Inequalities. 2026. arXiv:2609.23557v1, 2026-09-20.

https://arxiv.org/pdf/2609.23557v1

[2] Yanyi Li; Haihan Zhang; Chenheng Zhang; Wendao Wu; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Near-Optimal Higher-Order Oracle Complexity for Convex--Concave Minimax Optimization. 2026. arXiv:2609.28246v2, 2026-10-19.

https://arxiv.org/pdf/2609.28246v2
