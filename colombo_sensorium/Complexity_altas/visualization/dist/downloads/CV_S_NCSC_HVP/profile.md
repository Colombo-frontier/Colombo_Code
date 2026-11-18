# Nonconvex-strongly-concave minimax optimization with separate gradient and Hessian-vector product resources

**Setting ID.** `CV_S_NCSC_HVP`

Minimax optimization

$$
\min_x\Phi(x),\quad\Phi(x)=\max_y f(x,y).
$$

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** task family: Minimax

**MODEL tags.** convexity: Nonconvex strongly concave; convexity: Strong concavity; initialization: Initialization; smoothness: Lipschitz Hessian

**ORACLE tags.** feedback quality: Exact; interface family: Gradient and hvp; operation: Hessian vector product; operation: Payoff value joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N hvp; measure: N payoff first order; setup: Initialization included

## 1. Setting specification

### Task

$$
\min_x\Phi(x),\quad\Phi(x)=\max_y f(x,y).
$$

### Admissible model

$f:\mathbb{R}^{d_x}\times\mathbb{R}^{d_y}\to\mathbb{R}$, with both blocks unconstrained and Euclidean norms throughout. The joint gradient satisfies $\|\nabla f(z)-\nabla f(w)\|_2\le \beta\|z-w\|_2$.

The condition $f\in C^2$ holds, and the full joint Hessian satisfies $\|\nabla^2f(z)-\nabla^2f(w)\|_{\rm op}\le\rho\|z-w\|_2$.

For every $x$, $f(x,\cdot)$ is uniformly $\mu_y$-strongly concave. Thus $y^\star(x)=\arg\max_y f(x,y)$ is unique and $\Phi(x)=f(x,y^\star(x))$ is differentiable. Neither $f(\cdot,y)$ nor $\Phi$ is assumed convex.

Assume $\inf_x\Phi(x)>-\infty$, with an initial point satisfying $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$.

The public initial point additionally satisfies $\|y_0-y^\star(x_0)\|_2\le R_y$. The condition number is $\kappa=\beta/\mu_y$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $\Delta$, $R_y$, $\beta$, $\varepsilon$, $\mu_y$, $\rho$, together with the stated initial point and feasible geometry. The analytic representation of the hidden function, operator, or matrix is not revealed.

$$
z\longmapsto(f(z),\nabla f(z))
$$

$$
(z,v)\longmapsto\nabla^2f(z)v
$$

Every direction is charged separately. Reconstructing the complete Hessian from basis directions requires $d_x+d_y$ HVP calls.

Inner optimizers, reduced gradients, and reduced Hessians are not supplied directly. Linear algebra on returned data does not reveal new information about hidden functions.

### Output

Return $\widehat x\in\mathbb R^{d_x}$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\nabla\Phi(\widehat{x})\|_2
$$

The reduced gradient is $\nabla\Phi(x)=\nabla_xf(x,y^\star(x))$. Second-order stationarity is not the target.

### Resource accounting

Retain the joint fixed budget $(N_{\rm first},N_{\rm HVP})$; without cost weights, do not combine its coordinates into one scalar optimal rate.

The fixed joint budget $(B_{\rm first},B_{\rm HVP})$ requires $N_{\rm first}\le B_{\rm first}$ and $N_{\rm HVP}\le B_{\rm HVP}$ for every instance and execution path. Each Hessian action in a specified direction is charged separately.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_y$: Distance bound from the initial dual point to the unique best response at the same initial primal point **Domain:** A nonnegative real.

$\|y_0-y^\star(x_0)\|_2\le R_y$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the population smoothness upper bound, or mean-square average smoothness for finite sums, to the dual strong-concavity lower bound **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$\rho$: Lipschitz upper bound for the complete joint Hessian in spectral norm. **Domain:** Positive real number.

$\|\nabla^2f(z)-\nabla^2f(w)\|_{\rm op}\le\rho\|z-w\|_2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\nabla^2 f$: Complete joint Hessian, including both diagonal and both mixed blocks **Domain:** The matrix $(d_x+d_y)\times(d_x+d_y)$ is real symmetric.

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in \mathbb R^{d_y}}f(x,y)$

$y^\star(x)$: The unique global dual maximizer at fixed primal x. **Domain:** $y^\star(x)\in\mathbb R^{d_y}$.

$y^\star(x)=\arg\max_{y\in\mathbb R^{d_y}}f(x,y)$

$\|\cdot\|_{\rm op}$: Matrix or multilinear tensor norm induced by the Euclidean norm **Domain:** Matrix and derivative tensors used in this profile.

$\|T\|_{\rm op}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}\|T[u_1,\ldots,u_j]\|_2$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm first}$: Number of bundled function-value and full joint-gradient queries **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm HVP}$: The number of complete Hessian–vector products along specified directions. **Domain:** Nonnegative integer count; expected work is its expectation.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$v$: Arbitrary direction for the current Hessian-vector product query **Domain:** $v\in\mathbb R^{d_x+d_y}$.

$B_{\rm first},B_{\rm HVP}$: One algorithm simultaneously meets the fixed value–gradient and HVP budgets. **Domain:** Pair of nonnegative integers.

## 3. Complexity bracket

### Compared quantities

#### Q1 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Jointly attainable budgets under the stated success guarantee

**Scope.** Achievable budgets are uniform in each public finite block dimension. The necessary sum constraint is certified only in the separately displayed large-dimension window.

**Optimization direction.** pareto_minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - The declared parameter domain.

**Region.** All parameters in the declared model with positive accuracy and positive Hessian-Lipschitz bound.

**Quantity.** Q1

**Resource.** Identity projection on the declared joint resource vector; no scalar weights are supplied.

**Status.** Joint budget unresolved

**Achievable budgets.** B1, B2, B4

**Necessary constraints.** No admitted claim in this comparison

**Comparison argument.** On Z: epsilon^2 >= 2 beta(1+kappa) Delta, the exact minimal joint budget is (0,0); all nonnegative budgets are attainable. On the complement retain the two separate achievable budget pairs (T,(d_x+d_y)T) and (F,0), F=tilde O(sqrt(kappa)(1+A1)), with their original initialization and logarithmic factors. Their upward closures form a union, not coordinatewise minima or a weighted scalar optimum. The guarded sum lower bound remains in c2 on r2; the Pareto frontier outside Z is unresolved.

### R2 - High-accuracy window for the necessary sum bound

**Region.** $\kappa\ge6$, $0<r\le1$, $A_2\ge C_0$, and both block dimensions $d_x,d_y\ge C_1 A_2^2\log(2+A_2)$, for sufficiently large universal $C_0,C_1$. $A_2=\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2}$ and $r=\rho\kappa^{3/2}\varepsilon/\beta^2$.

**Quantity.** Q1

**Resource.** Identity projection on the declared joint resource vector; no scalar weights are supplied.

**Status.** Joint budget unresolved

**Achievable budgets.** B1, B2

**Necessary constraints.** B3

**Comparison argument.** The two algorithms certify separate achievable budget pairs. The necessary half-space leaves the Pareto frontier unresolved.

### R3 - Exact joint zero-query endpoint

**Region.** Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

**Quantity.** Q1

**Resource.** Identity projection on the declared joint resource vector; no scalar weights are supplied.

**Status.** Optimal

**Achievable budgets.** B4

**Necessary constraints.** B5

**Gap or comparison.** Exact attainable region R_+^2, minimum vector(0,0). Scalar multiplicative ratio is inapplicable.

**Comparison argument.** CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

## 4. Bounds and supporting evidence

### B1 - Simulate the bundled full-Hessian method with basis HVPs.

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
(T,(d_x+d_y)T)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Dimension conditions.** Valid for every declared finite dimension.

**Oracle correspondence.** Query $(f(z),\nabla f(z))$ once and obtain every column $\nabla^2f(z)e_j$ separately.

**Guarantee conversion.** The deterministic source witness meets the fixed success probability.

**Resource conversion.** The two counts are simultaneous. Here $T=\widetilde O\!\left(I_0+\min\{A_2(1+r^{1/7}),A_1(1+r^{2/7}),\sqrt\kappa A_1\}\right)$ is a sufficient bundled-query cap. $A_1=\Delta\beta/\varepsilon^2$, $A_2=\Delta\sqrt{\rho}\,\kappa^{3/4}\varepsilon^{-3/2}$, $r=\rho\kappa^{3/2}\varepsilon/\beta^2$, $I_0=\widetilde O\!\left(1+\min\{\sqrt{\kappa},[\rho(R_y+\kappa\sqrt{\Delta/\beta})/\mu_y]^{2/7}\}\right)$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N HVP.**

$$
(d_x+d_y)T
$$

**N payoff first order.** T

**Derivation.** Reassemble the full Hessian using the $d_x+d_y$ standard basis directions. The simulated algorithm receives the exact source transcript. Charge every initialization, inner-solve, and output-certification response at the same per-bundle cost. The resulting joint cap is $(T,(d_x+d_y)T)$, where the source estimate on $T$ is given in Theorem 4.1.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) pdf pages: 4; 5; 15; 16; 17; 18; section: Sections 3–4 and Appendix E; theorem: Theorem 4.1

Deterministic exact bundled-Hessian algorithm with the stated initialization and three-branch bound.

Same smoothness, dual strong concavity, start, and true primal stationarity. Each simulated bundled call uses one value-gradient response and one HVP per coordinate.

The separate-resource conclusion is a local simulation of the cited result.

### B2 - Use first-order saddle-envelope gradient descent throughout.

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
\bigl(\widetilde O(\sqrt\kappa(1+A_1)),0\bigr)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Dimension conditions.** Valid for every declared finite dimension.

**Oracle correspondence.** Use only the gradient part of the value-gradient response. The source's analysis of reduced-dual curvature uses Hessians analytically.

**Guarantee conversion.** The deterministic terminal primal output attains true primal stationarity.

**Resource conversion.** The same algorithm uses zero HVPs. Count all first-order calls for initialization and final certification. $A_1=\Delta\beta/\varepsilon^2$, $A_2=\Delta\sqrt{\rho}\,\kappa^{3/4}\varepsilon^{-3/2}$, $r=\rho\kappa^{3/2}\varepsilon/\beta^2$, $I_0=\widetilde O\!\left(1+\min\{\sqrt{\kappa},[\rho(R_y+\kappa\sqrt{\Delta/\beta})/\mu_y]^{2/7}\}\right)$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N HVP.** 0

**N payoff first order.**

$$
\widetilde O(\sqrt\kappa(1+A_1))
$$

**Derivation.** Use the first-order option in Proposition D.2 at each outer center. Its approximate reduced-dual gradients use accelerated gradient solves of the known regularized primal subproblem and one evaluation of $\nabla_y f$. Thus no Hessian response is required. Appendix E.1 gives $O(1+A_1)$ outer steps with $\widetilde O(\sqrt\kappa)$ first-order work per saddle solve. Appendix E.3 preserves this count up to logarithms.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) pdf pages: 10; 14; 15; 17; 18; section: Appendices C.3, D, E.1 and E.3; theorem: Proposition D.2

First-order-only inner solve and first-order outer gradient descent on the saddle envelope.

The reduced-dual gradient can be approximated via first-order evaluations only. Use the accelerated first-order branch for initialization and every subsequent saddle solve.

The separate-resource conclusion is a local simulation of the cited result.

### B3 - Reduce each split-interface query to one bundled call.

**Admission.** Included in the bracket

**Direction.** necessary

**Witness or lower-bound scope.** All algorithm necessity: All randomized adaptive algorithms

$$
B_{\rm first}+B_{\rm HVP}\ge c\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** $\kappa\ge6$, $0<r\le1$, $A_2\ge C_0$, and both block dimensions $d_x,d_y\ge C_1 A_2^2\log(2+A_2)$, for sufficiently large universal $C_0,C_1$. $A_2=\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2}$ and $r=\rho\kappa^{3/2}\varepsilon/\beta^2$.

**Dimension conditions.** Pad both blocks of the Appendix F hard family with known separable dummy coordinates.

**Oracle correspondence.** A bundled call at $z$ answers a split value-gradient request or provides $\nabla^2 f(z)v$ by internal multiplication.

**Guarantee conversion.** The reduction preserves arbitrary adaptive randomized querying, arbitrary primal output, and instancewise success probability at least 2/3.

**Resource conversion.** The fixed pathwise bundle budget is at most the sum of the two split budgets. The inequality is necessary for a feasible pair.

**Derivation.** Suppose an algorithm attained $(B_{\rm first},B_{\rm HVP})$. An algorithm with bundled access could run it with the same seed and transcript using at most $B_{\rm first}+B_{\rm HVP}$ bundled calls. Apply Appendix F. For $\kappa\ge6$, the lift uses $b^2=(\kappa-3)/2$ and turns $\varepsilon$ primal stationarity into single-level stationarity at $3\varepsilon/(2b)$. The all-derivative lower bound has scale $\min\{A_1,A_2\}=A_2$ in the stated window. One preliminary source query for the affine offset can be absorbed for $A_2\ge C_0$. Each block is padded to its requested dimension, using an inert primal block and a known $\mu_y$-quadratic dual block. The hard instances start with exact inner maximization and therefore obey every $R_y\ge0$ promise.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) pdf pages: 5; 18; 19; section: Section 3 and Appendix F; theorem: Theorem 4.1 and Lemmas F.1–F.2

Randomized all-derivative lower bound after a quadratic lift in the high-accuracy branch.

At least order $A_2$ bundled calls are necessary in sufficiently large block dimensions even from exact dual initialization. A bundled response can answer either one value-gradient or one Hessian-vector product query.

The separate-resource conclusion is a local simulation of the cited result.

### B4 - Return x0 without any information calls.

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Algorithmic witness: Deterministic witness

$$
(0,0)
$$

**Conditions.** Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

**Dimension conditions.** Every declared positive finite block dimension.

**Oracle correspondence.** No oracle response is used; x0 is public and an x-only output is allowed.

**Guarantee conversion.** The deterministic output satisfies ||grad Phi(x0)||<=epsilon for every admissible instance; success probability is one.

**Resource conversion.** Both fixed pathwise caps are exactly zero, including initialization.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N HVP.** 0

**N payoff first order.** 0

**Derivation.** The complete exact-baseline derivation is CV_S_NCSC_HVP__main__p1_zero_query: strong concavity and beta-smoothness give Lip(y^star)<=kappa and Lip(grad Phi)<=beta(1+kappa); integrating a gradient step yields ||grad Phi(x0)||^2<=2 beta(1+kappa) Delta. Apply Z and return x0.

**Local argument.** CV_S_NCSC_HVP__main__p1_zero_query

**Source location.**  proof ref: CV_S_NCSC_HVP__main__p1_zero_query

A uniform initialization-gradient estimate gives a zero-query joint budget on the closed sufficient region Z.

Same hidden payoff class, public x0, arbitrary finite block dimensions, fixed success probability and two separate pathwise resource coordinates. The deterministic output has success probability one. See the complete elementary proof in CV_S_NCSC_HVP__main__p1_zero_query.

### B5 - Each count and its valid cap is nonnegative by definition.

**Admission.** Included in the bracket

**Direction.** necessary

**Witness or lower-bound scope.** Resource nonnegativity

$$
\mathcal B\subseteq\{(B_{\rm first},B_{\rm HVP}):B_{\rm first}\ge0,\ B_{\rm HVP}\ge0\}
$$

**Conditions.** Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

**Dimension conditions.** All declared finite positive block dimensions.

**Guarantee conversion.** Necessary for every native successful algorithm, not a success algorithm.

**Resource conversion.** No negative caps exist; necessity requires no calls or source theorem.

**Derivation.** The exact accepted p1_zero_query derives Lip(y*(x))<=kappa and Lip(gradPhi)<=L=beta(1+kappa) from the unchanged global payoff/strong-concavity contract. Integrating the population gradient along x0-gradPhi(x0)/L gives ||gradPhi(x0)||²<=2L Delta; this is proof arithmetic, not free oracle access by an algorithm. Thus on the exact closed Z:epsilon²>=2beta(1+kappa)Delta, return already public x0, without calls, and satisfy the native x-only stationarity guarantee with probability1. Both pathwise caps including initialization are (0,0). By the frozen resource definition every admissible call count and cap coordinate is nonnegative. Consequently the attainable budget region is contained in R_+² and, from this SAME no-call algorithm, contains every pair in R_+². Therefore it equals R_+² with unique componentwise least budget(0,0). This is exact joint-region closure, not a scalar ratio or coordinatewise mixing of different algorithms. All nine public parameters remain uniform; no extra rho or Ry constraint is added. Equality in Z is included; there is no converse outside Z. The old positive witnesses remain valid but are dominated on Z; no source is newly recertified. The old necessary sum lower keeps its full H guard, disjoint from Z under its sufficiently-large universal activation constants as already proved in p1_zero_query (Z gives A1<=1/[2(1+kappa)],A2<=A1 whenr<=1,kappa>=6, so A2<=1/14<C0>=1). Full c1 and high-accuracy c2 retain their unresolved Pareto status. This publication is an already-known endpoint, not a new paper or main-rate improvement.

**Local argument.** CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 63e5f42c514c845f3dfccd0df3a699e1637ee1a0675d5d8c9421ce13517f231e

### Native proof: CV_S_NCSC_HVP__main__p1_zero_query

Native pointer: /proofs/0; canonical SHA-256: 3ecbbd14b7848a7576c3c27e55fd378039b68524fee1ac24004a6eede3462e4e

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: ba8f4a3c3334754187dfb965617aeab1068e8cb917dfe9554e7c9f0b273ef0c8

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: 161397e32217ef4112d28fddbfe9fea7dda0bb6fbbc523e312f556c01958fb86

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: ab0247aad4cba85653bf0e87e7db704636eaf63ae190b22061115a56ebaf1eec

0cec417b618b92406afbfbaaa45f95610b01cd396faf14403abb22e19ca8bf30

#### Native item 2

Native pointer: /proofs/0/baseline_refs/1; canonical SHA-256: 4fa6a1cb464966ad57ddb35136d00ee142642f48c7d3cd6d91255c703032a5c2

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/1/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/1/sha256; canonical SHA-256: 2e2a6e9e030bd9f9e9e1557e045670e422c67329a38b7d4e71c77b75a39354d8

a274efff8da593546b25525a34246dc43ff6c18f4e9c3c34ee52aca6810339fe

#### Native item 3

Native pointer: /proofs/0/baseline_refs/2; canonical SHA-256: 232145904a03a8ce39510b0de0e91badc871c7e5e7c13a78c2a408c3dda466c1

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/2/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/2/sha256; canonical SHA-256: d0aa7f218cf7ce828b828d76ca415d8122b0c0e23665149dd0b851a19454d34a

84825290506f8793ed7883b175063ede38e4b27b9d21b4a17c50479b066931aa

#### Native item 4

Native pointer: /proofs/0/baseline_refs/3; canonical SHA-256: f532b3ccdef7c48b17b39c5128719536c54e821642537160c3ec088a4e332e41

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/3/sha256; canonical SHA-256: 0aed3675c0041315215ab4789a037cc0b0c8330f2d25c3556456d598fb7c76c9

cf45c9913dd0cce7b5d6f62d33d1aa50e249878064be17f8c2df879cfff5bd33

#### Native item 5

Native pointer: /proofs/0/baseline_refs/4; canonical SHA-256: 5db56ed1c5d7f159ad7d67fbf70a9b07d674210243d2ca866d3b754bee28710f

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/4/sha256; canonical SHA-256: f95d52012dd7ff5bbb521664ed7baa0381d4537441d8a5632439d4d80854bec0

8b6c9aaedcea95b807bf0ed0ab981584f59d73e96d32087739755aba9f01a48c

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof

Native pointer: /proofs/0/proof; canonical SHA-256: 491af38e9800c08943e96fce37f333f2fad6ffc023217531710572338bfe11cc

Retain exactly the frozen model, public initial point, x-only output, success guarantee and nonnegative pathwise resource caps. Write y_x=y^star(x). Strong concavity implies mu_y ||y_x-y_x'|| <= ||grad_y f(x,y_x')-grad_y f(x',y_x')|| <= beta ||x-x'||, using the two zero dual gradients and strong monotonicity; the conclusion also holds when the dual points coincide. Hence ||y_x-y_x'|| <= kappa ||x-x'||. The frozen reduced-gradient identity then gives ||grad Phi(x)-grad Phi(x')|| <= beta (||x-x'||+||y_x-y_x'||) <= L ||x-x'||, L=beta(1+kappa)>0. For g=grad Phi(x0), s=-g/L, integrate the gradient along the segment: Phi(x0+s)-Phi(x0)=int_0^1 <grad Phi(x0+t s),s> dt <= <g,s>+L||s||^2/2=-||g||^2/(2L). Since inf Phi <= Phi(x0+s), ||g||^2 <= 2L(Phi(x0)-inf Phi) <= 2 beta(1+kappa) Delta. Under the closed predicate Z this is <=epsilon^2. The algorithm returns the already public x0 without calls, so it succeeds on every instance with probability one and has fixed pathwise cap (0,0). No y^star computation, reduced-gradient oracle or certificate is required by the algorithm. Resource nonnegativity makes (0,0) the exact minimal pair and every nonnegative pair attainable on Z. This is a sufficient endpoint, not a converse threshold. It is uniform in all nine native tracked parameters. It does not constrain rho or R_y beyond the contract. For consistency with the retained lower window H, Z implies A1<=1/[2(1+kappa)], and r<=1 implies A2=A1 sqrt(r)<=A1. With kappa>=6 this gives A2<=1/14<C0 for sufficiently large universal C0>=1, so Z and H are disjoint.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 49d47a0d474d63465fd3d317dd80746f91b839e11684d27b6e9a54eda2bc1331

The exact joint cap (0,0) is achievable on Z by returning x0.

#### Native field: supports

Native pointer: /proofs/0/supports; canonical SHA-256: 61f8b9e5deb8926158355b6638f87822507f28311eff0e50353b858170114b92

#### Native item 1

Native pointer: /proofs/0/supports/0; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

### Native proof: CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

Native pointer: /proofs/1; canonical SHA-256: 07dfd70b15276b7d27486d63a96e89cc2d73e6e881f805142ae3d4bd0765c9cc

#### Native field: baseline_refs

Native pointer: /proofs/1/baseline_refs; canonical SHA-256: b49320842ab01893a78c02426b32a752129bb881689eeb63d5711f65fde37aac

#### Native item 1

Native pointer: /proofs/1/baseline_refs/0; canonical SHA-256: 161397e32217ef4112d28fddbfe9fea7dda0bb6fbbc523e312f556c01958fb86

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/0/sha256; canonical SHA-256: ab0247aad4cba85653bf0e87e7db704636eaf63ae190b22061115a56ebaf1eec

0cec417b618b92406afbfbaaa45f95610b01cd396faf14403abb22e19ca8bf30

#### Native item 2

Native pointer: /proofs/1/baseline_refs/1; canonical SHA-256: 232145904a03a8ce39510b0de0e91badc871c7e5e7c13a78c2a408c3dda466c1

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/1/sha256; canonical SHA-256: d0aa7f218cf7ce828b828d76ca415d8122b0c0e23665149dd0b851a19454d34a

84825290506f8793ed7883b175063ede38e4b27b9d21b4a17c50479b066931aa

#### Native item 3

Native pointer: /proofs/1/baseline_refs/2; canonical SHA-256: 4fa6a1cb464966ad57ddb35136d00ee142642f48c7d3cd6d91255c703032a5c2

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/2/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/2/sha256; canonical SHA-256: 2e2a6e9e030bd9f9e9e1557e045670e422c67329a38b7d4e71c77b75a39354d8

a274efff8da593546b25525a34246dc43ff6c18f4e9c3c34ee52aca6810339fe

#### Native item 4

Native pointer: /proofs/1/baseline_refs/3; canonical SHA-256: f532b3ccdef7c48b17b39c5128719536c54e821642537160c3ec088a4e332e41

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/3/sha256; canonical SHA-256: 0aed3675c0041315215ab4789a037cc0b0c8330f2d25c3556456d598fb7c76c9

cf45c9913dd0cce7b5d6f62d33d1aa50e249878064be17f8c2df879cfff5bd33

#### Native item 5

Native pointer: /proofs/1/baseline_refs/4; canonical SHA-256: a4173dc37db9da0c186072e292bb7e985a907eff6b87e3a3d70a7863be569d6f

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/4/sha256; canonical SHA-256: 5cd7b1191aad01fa39560ac43bbe063bb61a7eb49d13b7e9f54e4ccf4bf5d008

7048c484ba264a5a85820b8e911535c4d4ab50c09da16639d1c8146eb8a6d9d8

#### Native item 6

Native pointer: /proofs/1/baseline_refs/5; canonical SHA-256: d698d145e4b9645bef4521e713cfc98859070251aaa33f110ba12754b734df0d

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/5/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/5/sha256; canonical SHA-256: e0ab96999437b542ba0d1b0367e8fb15bf4e2854472893d6dd653d330522f5ea

816d0adfff5c99eb0468cfdcaf5cfc1f707cf972e650004d60e11103180ac8ce

#### Native item 7

Native pointer: /proofs/1/baseline_refs/6; canonical SHA-256: 46d900b34732c00623a33f98c70115f3dcb2a0ab5275040ab6c769763ce8ce9e

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/6/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/6/sha256; canonical SHA-256: ee14c16dd8c84cac1f6b6dd98d09fc44eec57a242de42b21cfe378eff1d198c7

1962b3bcd98537c27d8c395c752f567c8a68abefbfb54343b453c8f039b6077f

#### Native item 8

Native pointer: /proofs/1/baseline_refs/7; canonical SHA-256: 90c0fc031a64c4e6173542c1330cbab9787c606d06874a36c36f7ca523d86d78

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/7/pointer; canonical SHA-256: 827389749d3001e88ba1259848cb6989c8ddd64d1399694733d555d9bbe48702

/joint_analysis

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/7/sha256; canonical SHA-256: 2a58902f1ff5649700fa80923e9627a4e14d6ee7f0f6d381da2f5a2240cf5767

be1460bb8d739bcb1c822f1a39db49f0c3b029f31a7ed1ae571cebe24db883b8

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: b0bfe34d9387c263b18e795bed3278d5aedd1edecb8d44abe23296940dc7898e

The exact accepted p1_zero_query derives Lip(y*(x))<=kappa and Lip(gradPhi)<=L=beta(1+kappa) from the unchanged global payoff/strong-concavity contract. Integrating the population gradient along x0-gradPhi(x0)/L gives ||gradPhi(x0)||²<=2L Delta; this is proof arithmetic, not free oracle access by an algorithm. Thus on the exact closed Z:epsilon²>=2beta(1+kappa)Delta, return already public x0, without calls, and satisfy the native x-only stationarity guarantee with probability1. Both pathwise caps including initialization are (0,0). By the frozen resource definition every admissible call count and cap coordinate is nonnegative. Consequently the attainable budget region is contained in R_+² and, from this SAME no-call algorithm, contains every pair in R_+². Therefore it equals R_+² with unique componentwise least budget(0,0). This is exact joint-region closure, not a scalar ratio or coordinatewise mixing of different algorithms. All nine public parameters remain uniform; no extra rho or Ry constraint is added. Equality in Z is included; there is no converse outside Z. The old positive witnesses remain valid but are dominated on Z; no source is newly recertified. The old necessary sum lower keeps its full H guard, disjoint from Z under its sufficiently-large universal activation constants as already proved in p1_zero_query (Z gives A1<=1/[2(1+kappa)],A2<=A1 whenr<=1,kappa>=6, so A2<=1/14<C0>=1). Full c1 and high-accuracy c2 retain their unresolved Pareto status. This publication is an already-known endpoint, not a new paper or main-rate improvement.

#### Native field: proof_refs

Native pointer: /proofs/1/proof_refs; canonical SHA-256: 7a20bc6903e82e915c73328b52337ef7f41cefd36676e1b46ec376a255f829ae

#### Native item 1

Native pointer: /proofs/1/proof_refs/0; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: efc9bbc87975cfe00a0f1fdea5e1c28a52562f87de599b3df680058518e8eb1f

Exact joint-budget region from the retained simultaneous witness and necessary constraints

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 0d272963710d476f0dc121923f07fc48e98968bed669339c3c9717c3d7d876ab

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 4e07f7bf12cbf1b3f1276a18c70b183f52b18576912d62ec75f156b6d8489d4a

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 4428a59b84194112650a9c9ebb3a97e7385a1fedaef19f89d267dae59b3039f7

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 954aebd7d2127e88bc7ae67b06abd989ccfd6587d5e472143be6e4f09445f75e

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: da85f8e0a4650c129726d79e79eecaa822c281808cddd0998fb357990486586b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: cc00757f11c0099072aad014d51e7cba184d61c5882b92998e60461863b02b2c

Declared full domain r1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 2bfb4272efd1d09a18ebfe1883bea479cd8da2e3a5315cfdb5f2d940ca3955f2

Retain the simultaneous pair with one first-order call and d_x+d_y HVPs per bundle. It remains valid on Z but is redundant there; outside Z its first-coordinate advantage cannot be combined coordinatewise with b2's zero HVP coordinate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: cc00757f11c0099072aad014d51e7cba184d61c5882b92998e60461863b02b2c

Declared full domain r1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 8d3e01eaf096a660e3f5369fc8f5bd9a3f37f8c0a6f5bafdf79f969f2fa947b4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: cc00757f11c0099072aad014d51e7cba184d61c5882b92998e60461863b02b2c

Declared full domain r1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: d030feee8a2178da8593666267c245a36b38846bb80442dfb377197d61f0d8ed

Retain the separate first-order-only witness (F,0), including initialization. It is redundant on Z; no uniform componentwise dominance between the two retained algorithmic certificates is claimed.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: cc00757f11c0099072aad014d51e7cba184d61c5882b92998e60461863b02b2c

Declared full domain r1.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 614637fb34fb37ce40943e914af2ab8e26a3523cc381c6d436a92d35e677a420

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 1263cbf492a0c4f8c6a7c77e93e12ec4e6903a57534b39e50a9c33779454c5fc

None as a uniform full-r1 constraint in c1; active only in c2 on H.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: ccaf0dc2396baa89a36b1f04a55faed5753c3decf89334fcfea09b2cd2e713d2

This lower constraint is not valid uniformly on c1's full regime. Its guarded use is explicitly retained in c2, not discarded on H or extrapolated outside H.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 2dbc3c937c94122a07163260d0fb484f754e17db0412ee0e561978ca61da4709

H exactly as r2.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 2721bed82dc6cf31ee366247ef3ceeb4c187dfa28f30da0fc130682f325681ba

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7a20bc6903e82e915c73328b52337ef7f41cefd36676e1b46ec376a255f829ae

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: bd26247daf3b4441e97c8e2e480f688e4ef6c2998be0b3dfb442f315234cce37

Return x0; exact minimal cap (0,0), dominating both recorded positive-cost sufficient caps on Z.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/bound_uses/4; canonical SHA-256: 5b1461fa768212ed57176647d88de0e5acb0f5280b89a3ad3a2b962eed1f75cc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/adopted_region; canonical SHA-256: 3c2afaf3d5474b8f2a5234cf68a75ee95a15829c9f5a79815ed0697bbcab9087

Not a selected nontrivial lower in this broad comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/bound_id; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/reason; canonical SHA-256: 9d71b767ec2403d47e470b08513807b16d3518b97285c1dd110f15b6f42481d3

Only the separately closed Z comparison uses this explicit vacuous nonnegativity constraint. For broad c1 it adds no meaningful frontier constraint beyond the quantity definition; old H/c2 is disjoint from Z. No positive lower or outside-Z adoption is inferred.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/4/validity_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: a45d0433e1904540551ea3a5401d5aaeca1ca6d6e473133d87d5a4cad3c85ca0

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 27714c25f3a0c1b2177a2c617e1b733d9dc7c06483001bb7eeeb3ca63cf11606

Equality epsilon^2=2 beta(1+kappa) Delta is included by the squared-gradient inequality.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 84e7a427ab52d3dda7ef57f8817060482e417685ab96450b176508bd08b6cf45

The proof covers kappa=1, d_x=d_y=1, R_y=0 and arbitrary declared rho>0; neither Delta=0 nor rho=0 is added to the contract.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: b66db99b8447bde6299d9c274dd6d4b49bc0af3e00c5eff61b879612f6ff724b

At r=1, A2=A1. The retained main-term crossover scales r=1 and r=kappa^(7/4) describe bundled-cap estimates, not a proved HVP Pareto phase diagram.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 9f7272dd4849653408739511144721e84ff7a8cafd2f7ba561093e61184c7377

No reduced derivative or inner optimizer is called to return x0.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 3990cddabbb032f2452b29b4efcbb1cb2b5754e667fb88a1e742b6edf5c72e2d

On Z the exact joint minimum is (0,0); a multiplicative ratio is inapplicable. Outside Z no scalar gap ratio is defined for this unweighted vector resource.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 34100c28213f2022f96286451fb24b91ad8075b39b19c22a1b036694c0d3c855

Intrinsic nonnegativity of both resource coordinates holds globally. On Z it matches the zero achievable pair exactly. The nontrivial guarded sum constraint is documented in c2 on H, not asserted uniformly on r1.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: a44497de01c312d149dc5cbcfef507cfdd6e9d0afa98fbd73b4c1ff74305e881

The sufficient endpoint is closed. Outside it, necessary constraints, low-dimensional branches and potentially sharper first-order/HVP pairs require further theorem-level assessment.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 2adea14ff0529419c7d1095439b5f1a1991029390ccfdcce445dba0d37802c4d

On Z, exact minimal pair (0,0), so every nonnegative budget pair is attainable. Outside Z, Union of the upward closures of (T,(d_x+d_y)T) and (F,0); T = tilde O(J + min{A2(1+r^(1/7)), A1(1+r^(2/7)), sqrt(kappa) A1}); F = tilde O(sqrt(kappa)(1+A1)). These are sufficient caps with the retained logarithmic qualifications.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: ad9544fe3243fedd591c977efc52c281ba2ef573c7090de5a0dfe78cebedeb98

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: c2c31d21ee081dd610dec08595c2d58dc5e23d9efee798615ff9e0638d0fe17a

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: bac2ec013448ea38ede83f66dff222022cb3b58a51fc4168e60b3002e31406ec

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: a0321c84a9182b5aa9def2b825c0b246d9734f9f0bce2404904f104f68792556

Retain the exact basis-HVP simulation. On H, r<=1 implies T=tilde O(J+A2); keep the simultaneous HVP multiplier d_x+d_y.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: cc00757f11c0099072aad014d51e7cba184d61c5882b92998e60461863b02b2c

Declared full domain r1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 9e8561d14c89b9573a70e6dde693abb86a3938083fae587366cce8c8802b71fa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: d9da7df363e4833c53457102af7e9e1613ccbb77480bec1dab403eee969286ca

Retain (F,0) as an alternative budget, not as the first coordinate of b1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: cc00757f11c0099072aad014d51e7cba184d61c5882b92998e60461863b02b2c

Declared full domain r1.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: bf1dc74ece66d0f9dbd92d726d86075d28750fc8a4f80e0dc4859db2ca20b858

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 8d74d7696fd3a92bb4b3ee6b7919bb9b30961d4fc623562b6fe645671c32061b

Conditionally retain the randomized all-algorithm lower constraint B_first+B_HVP>=c A2 and every accuracy, dimension and initialization guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 7499c53b80350db62e05439f0f86a5c1b9eae4c23d649cc6e0822c990d866384

H

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 3570087ed2dfea51ca25dbcc1e3235ad9075a09f1e3985d3741c54569b1734ed

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 4c9ae1d92b328f9ed899140bae5b787c54ca7b5df5aa617020bea4a47c3dfe87

Empty intersection with H.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 7a20bc6903e82e915c73328b52337ef7f41cefd36676e1b46ec376a255f829ae

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 7280810dab9f79fe0546fe506af9e8e52bfd374c45cfd42d306e9da5d8b6a0bb

The exact sufficient zero-query region and H are disjoint by A2<=1/14<C0 on a hypothetical intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/bound_uses/4; canonical SHA-256: a0725e2a844a690d9734dba1f206710abc825b5030eecbaf46abfc8d45af345b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/adopted_region; canonical SHA-256: 3c2afaf3d5474b8f2a5234cf68a75ee95a15829c9f5a79815ed0697bbcab9087

Not a selected nontrivial lower in this broad comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/bound_id; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/reason; canonical SHA-256: 9d71b767ec2403d47e470b08513807b16d3518b97285c1dd110f15b6f42481d3

Only the separately closed Z comparison uses this explicit vacuous nonnegativity constraint. For broad c1 it adds no meaningful frontier constraint beyond the quantity definition; old H/c2 is disjoint from Z. No positive lower or outside-Z adoption is inferred.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/4/validity_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: f08d555a969d9837db0745ecc76d4f936a4b13d1d52f17bf03af4a2f43851fc2

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 4d17d1dbd5d6c6d8faca3552249ad95e49bbd2674212e6e4bf2d1a55842cf777

Retain kappa>=6, 0<r<=1, A2>=C0 and each block dimension >=C1 A2^2 log(2+A2). These are source applicability guards with symbolic constants.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: f671ac313e324107942a05139373daab76655e101dc3ea7e45de30e3055c9c7f

No large-dimension guard is applied to the upper witnesses; no fixed-dimension saturation theorem follows from the lower bound.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: a041adab23c5c34ffc889b27baae134c6cf2a64dbbe33ed1f2c88a789faec0c7

Initialization J is retained even when the main rate A2 does not dominate it.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 1b13ae2673b8f46805beb8e951af7357a8085f8e02ded732bc8c5a692eb789a5

The new zero-query proof neither weakens nor contradicts the retained sum bound, since its validity region has empty intersection with H.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 7714517bf17ed96372cc7f965ac058ae444a8de2f215b2f1a4d162f480fd09f7

An unresolved Pareto region between two attainable upper orthants and a necessary half-space. A scalar sum lower bound does not provide separate coordinate lower bounds or close the frontier.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 414ddbd65e46ca9743ffc621fd77b9a2fe5b054c1e94008cda49c0be23a0dba0

B_first>=0, B_HVP>=0 and B_first+B_HVP>=c A2, only under the complete r2 guard with sufficiently large universal C0,C1.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: a2cb4e8ea1bb6b4ce90dc8ad177bb7ed44bf60b1e39383d325376d5000cb0eb4

No closure of the joint Pareto frontier or extension of the necessary half-space beyond H is proposed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 8daf37f32dfb62c60406f5cd4cc9ac4fefe014d593510c2d86c8d8f994ab2dab

Union of the upward closures of (T,(d_x+d_y)T) and (F,0); T = tilde O(J + min{A2(1+r^(1/7)), A1(1+r^(2/7)), sqrt(kappa) A1}); F = tilde O(sqrt(kappa)(1+A1)). These are sufficient caps with the retained logarithmic qualifications. On H this simplifies to the union generated by (tilde O(J+A2),(d_x+d_y)tilde O(J+A2)) and (F,0), preserving the simultaneous cap and logarithmic factors.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: f8f733445e8812a9fa84a291e5d350ebbc30c1c1b0bee517ba6594f483ff3ccc

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: b75225d7ac496cac2f0b83b85707b73ffc588ad5990f70bcece69a63b508f0b2

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 035714e5c22ff745f963c715f89ff59c74dfedc50c411ba5134256f15fcbd25b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 50dbe559f043827cd1f8e795a8df6ecc6891d58f5ff3416bf40fd2a227b13b9a

Not adopted; original guard retained.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 8eb8040ac5c89dbdb170cd8e1af4d889fc143cf95466ac8a9fbba4245281c3e6

Retained upper is no sharper on its source-valid overlap than the same-algorithm exact minimum vector; outside its original guard it is not asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 8607f4ae41a8f259d46fc2a7cd5ee3f47548255d31ee774f2f4c9cc0e1712989

Exactly the unchanged native bound guard; see applicability/region_refs.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: f4efefc7947a29bb6ff844a2f79751c4a5ff68c0851373010a64bf0c570fafd2

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 50dbe559f043827cd1f8e795a8df6ecc6891d58f5ff3416bf40fd2a227b13b9a

Not adopted; original guard retained.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 8eb8040ac5c89dbdb170cd8e1af4d889fc143cf95466ac8a9fbba4245281c3e6

Retained upper is no sharper on its source-valid overlap than the same-algorithm exact minimum vector; outside its original guard it is not asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 8607f4ae41a8f259d46fc2a7cd5ee3f47548255d31ee774f2f4c9cc0e1712989

Exactly the unchanged native bound guard; see applicability/region_refs.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: 8b1599b6a87c2d14c5e4eff5b7a351351564fa8e39239d9c3fa0372621c3076b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 50dbe559f043827cd1f8e795a8df6ecc6891d58f5ff3416bf40fd2a227b13b9a

Not adopted; original guard retained.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 2f68ee57c4ab82342bebcf2465633468e79e589799036be226e0360e6d3a0f03

Old H source guard is disjoint from Z under its sufficiently-large activation constants; it is not used here.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 8607f4ae41a8f259d46fc2a7cd5ee3f47548255d31ee774f2f4c9cc0e1712989

Exactly the unchanged native bound guard; see applicability/region_refs.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: 771faa8c76d3d9b27cd3f78839f66df8a7c51988ca29229298fda624a4a8a333

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 7dde98e2fdb29293d361f33916e83bad8c1c6d95a8579f6962d2394a116fe41c

Exact native same-quantity witness/necessary side, fully combined in CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 8607f4ae41a8f259d46fc2a7cd5ee3f47548255d31ee774f2f4c9cc0e1712989

Exactly the unchanged native bound guard; see applicability/region_refs.

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: c0a796eae300c685100d47c272d3ddb9f7f5f9065fcf6de52cc830e287f770eb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 7dde98e2fdb29293d361f33916e83bad8c1c6d95a8579f6962d2394a116fe41c

Exact native same-quantity witness/necessary side, fully combined in CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 8607f4ae41a8f259d46fc2a7cd5ee3f47548255d31ee774f2f4c9cc0e1712989

Exactly the unchanged native bound guard; see applicability/region_refs.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: 5b241f78538400f979600ab1e135661597d59d592c210b8778ec23ab22b0608c

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: fe220f953bda9f3c5d270f91a5788e121f48eef73a41f1957d6d189790caf3cd

Equality in the sufficient activation guard is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/boundary_checks/1; canonical SHA-256: 59b82f1828abbfd200688c2fd78983a9690c004d24b46dcae55e95c24d48661d

Every cost coordinate comes from the SAME witness; no scalarization or coordinatewise combination.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: d0efc1ebe9c454cc572c72d3f85ebc15a53659af6859598abcfbefe8d6c50d85

Exact joint-region equality; scalar multiplicative ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 6fb9e52c6237f8cd05af0ac924b5f9dd133cc29b5943c05e1ec6774c8972085d

Every admissible budget is componentwise >= (0, 0).

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: eceb39ba8d1bc97239eea3e601ee208874bd7a45e0609ab86cf98c1928b4e6fa

No Pareto gap on this sufficient region. No converse/largest-region or full-domain optimality claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: c436b49629d1d0526e7e8555989ed1cec8f7b012b2eadd94139b9f1c670069e9

All componentwise budgets above (0, 0) achieved by one algorithm.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: a360080e6b5729b40d3681264c2a3f1baf75f312b79ea83b1851af0205d89b96

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 7467b9a9e7fea130e6846d814d05fcdf39d48d8552a78db6106033188f18369e

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: ad91feaf9f2fa971a7ce0a7f63ed989587820e00a7190084163ff7c64cac9c7d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: a1663bf2bfb82a8e4d0361be3a8f3151310759b4f74fa95489445a8f384dd2f0

zero_query

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 10746416a6163d03433cfcd9341f236a01c43ad5395accc818cafd992f6b7880

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/1; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 38698e991e3b0554fe55d57e0f9d631879e8745e711da03211de156eb20bc9dd

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 65d76858bc8d7afd3ceb3583079fc0256923bb741f17207c1f9c1b75327e2044

Exact joint-region equality is now published by its own optimal comparison. Only this sufficient endpoint is closed; old full-domain c1 remains unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 4ded8bc07f81a25dfe41df0ede20de3df26235764d421773e2eb936479da8b0d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: ac42ef8556602c4e95069ef430a9e3aae9f4164fd7a4fdaa49306c7d4f258737

retained_high_accuracy

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 2abe21b6d2fb8f62815635cd7f5f76db20143c2be8972f57338c203e530530ae

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 505c47841b716d34ea48891d6cdf204dcbb7acd42723e2ebc2059b543d3da06b

Two retained achievable pairs and a guarded necessary sum constraint; the Pareto frontier is unresolved. Sufficient dimension conditions are source activation guards.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: d963bb804cce8c0b9e217b17d6386916df154fcfc61e7d1cfc7981f320f7045c

not Z and H, with H exactly r2: $\kappa\ge6$, $0<r\le1$, $A_2\ge C_0$, and both block dimensions $d_x,d_y\ge C_1 A_2^2\log(2+A_2)$, for sufficiently large universal $C_0,C_1$. $A_2=\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2}$ and $r=\rho\kappa^{3/2}\varepsilon/\beta^2$.

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 2828a78c929ceb772ddb09ac637ed6bc78d59edfc55753ad52d328e63f73be03

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 7e767166fae7ad55199595f15b014cd0120df03c878b93d835e19b9b9bc8eb8f

unassessed_complement

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 47c51753756734bde602c80f37220d09062e3489bbfbfd7d8c231e1f41ccdf7f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 42a4b77206ef071b25de2849ec218b03a305925294a6fd3598d99646b0be671f

The two baseline achievable witnesses remain recorded. A matching necessary region and sharper HVP/first-order envelopes have not been assembled; this is not a claim of absence of bounds.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 38c22df79ca1284e246b8963f039f3a14ff504f3231432f77c71e4c9c9640d9a

r1 and not Z and not H

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 3f630d894f3e74894092b21960f49d92ae694cb4ed44d75d009425919888c8cc

For every point of r1 first test Z, then H; the three cells are mutually disjoint and exhaustive by Boolean partition. Moreover Z and H cannot overlap: Z gives A1<=1/[2(1+kappa)]; H gives A2=A1 sqrt(r)<=A1<=1/14<C0 for its sufficiently large universal C0>=1. No exact converse endpoint or intrinsic dimension transition is asserted.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 777226f2d951679843ea45a15acd39f008defc2c911e78956c0e39a2b5f8532a

No target point is omitted by the cells. The scientific residual is r1 outside Z and H, together with unresolved Pareto tradeoffs on H and the listed theorem-level leads.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 4c4aa53ccd72b9f166114c21e7bfae23a8099f899e13981021be701b30d5621a

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: e0264af98bd475b092809577eb465a51aca017c95d539409fa58eaa184777e1a

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: cc4eef949ea6975a67542f81bd5570c90a3ed96233ba6259a5a6db9e477b56ee

The proof gives ||grad Phi(x0)||^2<=2 beta(1+kappa) Delta. The closed displayed inequality is an exact sufficient activation threshold; no necessity or maximal zero-query region is claimed. Resource nonnegativity closes this endpoint exactly.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 47c51753756734bde602c80f37220d09062e3489bbfbfd7d8c231e1f41ccdf7f

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: c7f085767444e4963fdcddcefcb30a347a8bfa4422854e5f58a5b05258fd9c78

ncsc_hvp_zero_query_initialization

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 2adea14ff0529419c7d1095439b5f1a1991029390ccfdcce445dba0d37802c4d

On Z, exact minimal pair (0,0), so every nonnegative budget pair is attainable. Outside Z, Union of the upward closures of (T,(d_x+d_y)T) and (F,0); T = tilde O(J + min{A2(1+r^(1/7)), A1(1+r^(2/7)), sqrt(kappa) A1}); F = tilde O(sqrt(kappa)(1+A1)). These are sufficient caps with the retained logarithmic qualifications.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 4376caeb5a35a04fb6df432b6f47e5e5ca957af0315fef478d48a336814b35ff

Union of the upward closures of (T,(d_x+d_y)T) and (F,0); T = tilde O(J + min{A2(1+r^(1/7)), A1(1+r^(2/7)), sqrt(kappa) A1}); F = tilde O(sqrt(kappa)(1+A1)). These are sufficient caps with the retained logarithmic qualifications.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 9b1ef377026968f2eaa39a85e14fb464b5c17a18608c490c81890e3547ca927d

r1 outside Z; all retained claims on H, which is disjoint from Z.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: c86b50bc8a69e1f6160ac8a9eac94a18a74d7fec2cd42ec9c2e6c4f1cc0db3fc

Delta=beta=mu_y=rho=1, kappa=1, R_y=0, d_x=d_y=1, epsilon=2 lies at equality. The old displayed sufficient caps contain positive initialization work; the new certified cap is exactly (0,0). This improves the recorded certificate, not a claimed lower bound on the old algorithms.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 0322d49d2d458d338277e5efdef4470e20657f45c761b5bedaad61c8c949fc17

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: f12c698c91d0a23e1e58c7db5d424c86d7560fc1a629fb332cfbfef09839f18c

The first annotation distinguishes vector attainability, a sum necessity constraint, source guards and an unassessed complement. It conditionally retains old premises without claiming fresh certification or using presentation to justify the endpoint.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 2abe21b6d2fb8f62815635cd7f5f76db20143c2be8972f57338c203e530530ae

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: d572a9e82668e47cd8843b3647ae49817c12cfbc72395f42f3bddd759679af35

ncsc_hvp_first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: c90590b9e636917169a2f5ed10767c395c9a096160e7faa48f9ba1ed4d0feb95

No additional scientific improvement from this presentation finding.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 60bc7489cda14a0a3116db48954391b8ebb689ebcd20baf242609465f8a11776

The same retained witness and necessary-constraint statements with unchanged guards, now recorded as joint vector envelopes; the separate zero-query finding supplies the only scientific addition.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 1c68e8a3362600c32ed03192cb3cc5b677c5cf78985c238d1b410dfa55434511

Union of the upward closures of (T,(d_x+d_y)T) and (F,0); T = tilde O(J + min{A2(1+r^(1/7)), A1(1+r^(2/7)), sqrt(kappa) A1}); F = tilde O(sqrt(kappa)(1+A1)). These are sufficient caps with the retained logarithmic qualifications. Necessary sum bound only on H.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 2ed261a619a545655061971275d57c74edc42cc948b3b4cf8ac86d2860454211

Every retained bound, source guard, contract, status and comparison key.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: d9d4e8da5b2ebd7ffde77fa81bb73186ff65da14cbea15c13d6c02c51cf713a4

The declared domain, with H explicitly guarded.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 24db5f215e6ea410253566cb0e3ea08602c538bf90c8304dafb3da171838740b

On H the inequality B_first+B_HVP>=c A2 leaves many incomparable budget pairs; taking coordinatewise minima of the two upper witnesses would be unjustified.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 00a72fc05e36fac6c12202fb83d58ec59c98e297d0845449cbbbb2e748ebcd77

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: b0bfe34d9387c263b18e795bed3278d5aedd1edecb8d44abe23296940dc7898e

The exact accepted p1_zero_query derives Lip(y*(x))<=kappa and Lip(gradPhi)<=L=beta(1+kappa) from the unchanged global payoff/strong-concavity contract. Integrating the population gradient along x0-gradPhi(x0)/L gives ||gradPhi(x0)||²<=2L Delta; this is proof arithmetic, not free oracle access by an algorithm. Thus on the exact closed Z:epsilon²>=2beta(1+kappa)Delta, return already public x0, without calls, and satisfy the native x-only stationarity guarantee with probability1. Both pathwise caps including initialization are (0,0). By the frozen resource definition every admissible call count and cap coordinate is nonnegative. Consequently the attainable budget region is contained in R_+² and, from this SAME no-call algorithm, contains every pair in R_+². Therefore it equals R_+² with unique componentwise least budget(0,0). This is exact joint-region closure, not a scalar ratio or coordinatewise mixing of different algorithms. All nine public parameters remain uniform; no extra rho or Ry constraint is added. Equality in Z is included; there is no converse outside Z. The old positive witnesses remain valid but are dominated on Z; no source is newly recertified. The old necessary sum lower keeps its full H guard, disjoint from Z under its sufficiently-large universal activation constants as already proved in p1_zero_query (Z gives A1<=1/[2(1+kappa)],A2<=A1 whenr<=1,kappa>=6, so A2<=1/14<C0>=1). Full c1 and high-accuracy c2 retain their unresolved Pareto status. This publication is an already-known endpoint, not a new paper or main-rate improvement.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 38698e991e3b0554fe55d57e0f9d631879e8745e711da03211de156eb20bc9dd

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: ab921904c2f74f241e0902d5318c4b237c6d4134603e057128d6401512830e12

CV_S_NCSC_HVP_native_joint_closure_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: fdefc8f8a874bdbd4583d85fb847649698ca1fb1197f07a72bf0c34fe250920b

Native publication of an already-proved local closure, not a new numeric main rate or strict extension outside the old full domain.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 0db40757c4d51f8e829588f8f813d13ca734808483bd6b44dfc7c27f37ad75e7

A separate native optimal comparison publishes exact attainable region above (0, 0).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 7d581c0075e512ebaf42ee4b04fe446bc247a399313f936fdc9d2bdb1b3201b7

Existing joint analysis already stated the exact local minimum vector but linked only broad joint_budget_unclosed c1.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 3eef3e1b9316e2cc107146014425a730f3382115503cec7048ed25555f3a40f8

Old fullc1 and all old upper/lower source guards; fine/complement/Pareto obligations remain pending.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: e7786adc40fc6aaddc2fa5091645ea183871da08b8ff3504ee282dde2598d2a9

The same fully accounted algorithm attains (0, 0) and the complete necessary constraints match it.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: dab21fd362f211e74540a90648ba92154d03a983c1795775529f812120634a19

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 56d9e66e2b9e81d38efa09f7945f6b7dcc51e209c7f0ffd714ef558bc9d54771

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/impact/3/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: bbffeffb5ef6689d726abdaf3438576ca4006b14b58540b9feac97bdbe3507bd

curated_feedback_CV_S_NCSC_HVP_20261116_ab3e5d3796

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

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 5c1c53c08b431ff539ee27a32525f3c0ce5d99299b31d78d8deeb31039c49c4f

The achievable resource region q_declared for view main, g1: instancewise success probability >=2/3 for ||grad Phi(xhat)||<=epsilon, arbitrary adaptive randomized algorithms and fixed pathwise caps (N_payoff_first_order,N_HVP), with identity resource projection. Jointly vary Delta,beta,rho,epsilon>0; R_y>=0; positive integer d_x,d_y; 0<mu_y<=beta and kappa=beta/mu_y>=1. No tracked native parameter is hidden in a constant. The normalized A1,A2,r,J are dimensionless under rescaling payoff and spatial units; they abbreviate the native parameters without changing their identities or domains. Universal theorem constants and explicit logarithmic factors remain as retained; confidence is fixed at 2/3.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: a55962c9942b98de8be3e41c137cf70683d5f2edd7523aa3f7830335159e4f75

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 39eb7722502ab986611a96c01c78e66be79f599dbc5476a27fa4553b4525bb80

Complete the native-resource mapping of arXiv:2602.14058v1 (IHSDA), source 3afa87e3843ad414cad689d39e96467e236566c4524d3cd69c9337fc994809fe: Assumption 3.1 remains unread; resolve reduced-Hessian actions, inverse-dual work, all first-order calls, accuracy constants, confidence/dimension restrictions and a fixed cap on every failure path. Read Assumption 2.1/Lemma 2.1 at characters 11900-15500 and Theorem 3.1/Remark 3.1 at 36550-40650; no budget pair adopted.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 11fd0b8f279f09c9883001de617b5d311d597a1a2f38c9802405182467ca26b2

Read primary theorems for arXiv:2304.12453v2 and 2307.00126v1: possible higher-smoothness first-order improvements require a uniform conversion from the native payoff Hessian bound, initialization accounting and the exact guarantee.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: b825b29df06d108cc9d6adf32a97b4d315f3079f18817e4fea01bd22d456a71e

Read primary theorems for arXiv:2110.04814v3, 2110.07098v5 and 2411.15769v2: possible dimension-sensitive HVP budget pairs remain unassessed.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 0106c2e6b9f394e7204f4ea0d8e0583f51770d25b58d29c892f7df20f97601b5

Assess arXiv:2610.20345v1, 2606.07003v1 and 2605.06431v1, plus the remaining broader-query leads 2601.10086v1, 2406.13041v3 and 2402.09807v1; metadata alone establishes no applicability, dominance or exclusion.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 27be6934badd884a30f44d5cd4426d55c13b6cc96334a9fd54d7398309bdabbb

Source 6bd43aa82bb739466f4594430d68f49b18e773dde79fc86fbbf96000f44b8e3c, arXiv:2610.16771v2 Theorem 4.1/Appendix F: other sum-lower regimes require explicit finite-block-dimension and simulation checks before extension beyond retained r2.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 47ed2b0fbcabddbbb196a852acad2fad1d41e2c3b6b1e7d7a09d2673b0bb04a5

Outside Z the Pareto frontier, low-dimensional improvements and other saturation regions remain unassessed by this local update; no converse to the sufficient zero-query condition is claimed.

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 61857e0d0d3e4626b627097ebe9da2e074f0fdf572afbcbf3dbf74dc6bb6054a

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: b313f0b3938b8c12d5331a38fa6cf51f050d4573165deed33773b49d5f373974

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: f29280a22cd56071e0449a3c7bb06834d8d6b8f315f142be353d03c3a5f608f5

Retain one first-order response and d_x+d_y separately charged basis HVPs for each bundled source response.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 27ba3ef832425d6f4334a037998d6d7dace3b080768b6bbddd56b350bb0cbc3b

The declared r1 domain.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 7e3aedd27d889d5a6260efbd3b54c08b57609dac3bf5f4e33b8481b1997fd960

Conditionally retained frozen /bounds/0; complete parent /bounds canonical hash c320517b28172d91d54045898e051549590890a5eae8ed49ca526f3ebc85ba67. Existing evidence CV_S_NCSC_HVP__main__e1; not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 234236a6b4a6453183e905584a21f0e7ee59af3b6678c63dd471c52253280ebf

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: dd8fcb442851f97d713428fe372ca36444edafffb1df6ad13016b77ed99019a0

CV_SRC_ncsc_hessian_2610_16771

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: f42c085cd6e6efe7643207b142c40d20456ee3475a7cc791e0cb1892d6fc3be3

r1; unchanged witness validity.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: e9fcf22d1fc8de881837f0a1469469e8bc47a9091394799443ac78fbe9b7ae15

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: ba3c15ec2136b9d1104fb50d6f4327408e81185a74ae8a8cf46e3ae45718d5ff

Retain the first-order-only source option with zero HVPs and all initialization costs.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 27ba3ef832425d6f4334a037998d6d7dace3b080768b6bbddd56b350bb0cbc3b

The declared r1 domain.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: ddb719105960019f2e1f6f32ab5e32159b928f8d113f6f11ceb75ea79b88cb69

Conditionally retained frozen /bounds/1; complete parent /bounds canonical hash c320517b28172d91d54045898e051549590890a5eae8ed49ca526f3ebc85ba67. Existing evidence CV_S_NCSC_HVP__main__e2; not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 234236a6b4a6453183e905584a21f0e7ee59af3b6678c63dd471c52253280ebf

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: dd8fcb442851f97d713428fe372ca36444edafffb1df6ad13016b77ed99019a0

CV_SRC_ncsc_hessian_2610_16771

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: f42c085cd6e6efe7643207b142c40d20456ee3475a7cc791e0cb1892d6fc3be3

r1; unchanged witness validity.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 289f6b239737029d88bc48ce9fe6857771495fa24fec10973a2f0390232acf2e

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 65cabdf0ff4d1729f327eba09dd29dccd6a6dadfd39c22d8851f073b585b5231

Retain the split-to-bundled simulation and necessary sum inequality, arbitrary randomized guarantee and block-padding guards.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 6bcda1be35286764d11d1918de11777682ac0cbceaa25a13330d547f3062d6fa

The complete r2 guard H.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 7a444e4da8043a74f0e070972e1323431308b5075981e360799a1feb20022e41

Conditionally retained frozen /bounds/2; complete parent /bounds canonical hash c320517b28172d91d54045898e051549590890a5eae8ed49ca526f3ebc85ba67. Existing evidence CV_S_NCSC_HVP__main__e3; not freshly recertified.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 234236a6b4a6453183e905584a21f0e7ee59af3b6678c63dd471c52253280ebf

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: dd8fcb442851f97d713428fe372ca36444edafffb1df6ad13016b77ed99019a0

CV_SRC_ncsc_hessian_2610_16771

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: cef8243c6957ceaea6406d7a979b8b549b644f79a7a4c124709fb50aa70e997d

H only, as retained in c2.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: d509ed4e83f66f64c008373d1433275b05cc6e6d1b2d802e6da4f192e1a607cc

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 4ccfb80aa30935ec69ca789b7f42ca6939f52da0d9c663a16dd89ec39c2628bc

Use Lipschitzness of the best response and reduced gradient solely in the proof. Return public x0 without oracle calls; probability one implies g1, and both pathwise resource caps equal zero.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: 7a20bc6903e82e915c73328b52337ef7f41cefd36676e1b46ec376a255f829ae

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 8e5dbe2b74a824b64d290dd5f97a537026dfa2278ae1a95fc877c4e9a792efe4

The fixed native model and public initialization promise.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 616d92ba1fed60edc2769aca9881fca76b24fad706092ab6cb8ce2ba3109173c

Complete proof CV_S_NCSC_HVP__main__p1_zero_query from exactly cited frozen contract/view/quantity/parameter/resource premises.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 3fdabd1bff49a1f5192897ad961c62d61aa0f592ba1eda4caf4f7e3272df5252

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: a26d299514c4769a260bec168a78d0516b49d7ec16d4b32822c90f8924152a9d

Nonnegativity gives the complete necessary orthant; pair(0,0) supplies the matching achievable orthant onZ only.

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: 411b3a2f29190b1d1c4f1b2eede53a198a27d40aac8f39fab2ec3b03cf768b4b

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 3005048a83e8a9778d46fe4390ba09c542e23c7e2f98cc4e823cc24431541b08

Unchanged entire native nonnegative resource model.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 282655b1d8bc426d0298a706780778b366d8e84d2af6f163cb38e09d10546df6

Native nonnegative resource-cap definition and complete joint closure proof CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: d83a7b897bcfbd1a2219000b512c888d397686344c77a1bc2aa1c3948a9a0b6a

Declared domain and epsilon^2 >= 2 beta(1+kappa) Delta, where kappa=beta/mu_y.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: b61c8611c24591a96e02a53f7dbc0639ef01ab9578c8eeb25d3e1eac4e7fd65a

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 8e02bedba66430ec1ce32639809efc0649cf54ff8a74794749387c11114cb781

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: f1722eb83c9694617a8c85a77abc005cc28b165dcc110c7da663b9e7be09aeb5

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b16a19adaa35707c32738ee1ff6bdc0b5c6d27206513eab7473b0623ec695dbd

All same-contract candidates are explicitly judged in the native comparison bound-use ledger. The newly published local closure follows from matching same-algorithm achievable/necessary regions in CV_S_NCSC_HVP__main__p_native_joint_closure_20261116. Retained broad/fine entries keep their original guards and unresolved status; no new theorem or old-source recertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: dcb4f3bea4aeea95fe673de502c2c547dfc50f3981626d2a79d5eb9158564bcb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/4; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 47c51753756734bde602c80f37220d09062e3489bbfbfd7d8c231e1f41ccdf7f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 10746416a6163d03433cfcd9341f236a01c43ad5395accc818cafd992f6b7880

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: ee602d277249540d1a394f4680dc76b73fb8db34cfd162612a4f4e96d20d5c0e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b16a19adaa35707c32738ee1ff6bdc0b5c6d27206513eab7473b0623ec695dbd

All same-contract candidates are explicitly judged in the native comparison bound-use ledger. The newly published local closure follows from matching same-algorithm achievable/necessary regions in CV_S_NCSC_HVP__main__p_native_joint_closure_20261116. Retained broad/fine entries keep their original guards and unresolved status; no new theorem or old-source recertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: dcb4f3bea4aeea95fe673de502c2c547dfc50f3981626d2a79d5eb9158564bcb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/4; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 1a0469b32c60297870d50c534ed3c19cfbdc14298b5ef0dad61b6f3350adf843

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 10746416a6163d03433cfcd9341f236a01c43ad5395accc818cafd992f6b7880

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 8a44fc69f718760aac5343d0a8f63c7ee7c0afb61c3820562ad5ec69c5eb2886

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: b16a19adaa35707c32738ee1ff6bdc0b5c6d27206513eab7473b0623ec695dbd

All same-contract candidates are explicitly judged in the native comparison bound-use ledger. The newly published local closure follows from matching same-algorithm achievable/necessary regions in CV_S_NCSC_HVP__main__p_native_joint_closure_20261116. Retained broad/fine entries keep their original guards and unresolved status; no new theorem or old-source recertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: dcb4f3bea4aeea95fe673de502c2c547dfc50f3981626d2a79d5eb9158564bcb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/0; canonical SHA-256: d071446455abba96a61e5fa7df40db93f838272ea6ec5a1bbd0bd211834a50da

CV_S_NCSC_HVP__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/1; canonical SHA-256: dfe73778632c4512cce66625ef5ce3d153e308101e7339172820b5fc9e205eef

CV_S_NCSC_HVP__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/2; canonical SHA-256: 483499425b57bb02f95c0b3692f00699b707e5b53c94d7fbdaddd247524fe9cc

CV_S_NCSC_HVP__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/3; canonical SHA-256: 945412e7c7a16ac3cfa47ee7896e815ce27720592eee22ee7a07ff9cbabec393

CV_S_NCSC_HVP__main__b4_zero_query

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs/4; canonical SHA-256: 520109be091febc0cdafea7c5fe639266eaf0dc2fba43b4f387554dcb780f7f1

CV_S_NCSC_HVP__main__b5_nonnegative

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 38698e991e3b0554fe55d57e0f9d631879e8745e711da03211de156eb20bc9dd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 10746416a6163d03433cfcd9341f236a01c43ad5395accc818cafd992f6b7880

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/0; canonical SHA-256: 4ff8dbe2922dcecd5e7f8a49ee5c5ed2148013fc7961ccfc8284d033af8bae38

CV_S_NCSC_HVP__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs/1; canonical SHA-256: 8f6a5ca1ea901620adf0bbb90acd281fc940e229f7770326c58c972fb0bff404

CV_S_NCSC_HVP__main__p1_zero_query

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 50d3f91033724caefb8213d8c2c65a224dc23c09226113076238db3d6e477d15

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 39eb7722502ab986611a96c01c78e66be79f599dbc5476a27fa4553b4525bb80

Complete the native-resource mapping of arXiv:2602.14058v1 (IHSDA), source 3afa87e3843ad414cad689d39e96467e236566c4524d3cd69c9337fc994809fe: Assumption 3.1 remains unread; resolve reduced-Hessian actions, inverse-dual work, all first-order calls, accuracy constants, confidence/dimension restrictions and a fixed cap on every failure path. Read Assumption 2.1/Lemma 2.1 at characters 11900-15500 and Theorem 3.1/Remark 3.1 at 36550-40650; no budget pair adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 06e2d667ce3e5ec3ae236b54b9fc653620cc1b68f316135ee19a9bc8a5a03094

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 11fd0b8f279f09c9883001de617b5d311d597a1a2f38c9802405182467ca26b2

Read primary theorems for arXiv:2304.12453v2 and 2307.00126v1: possible higher-smoothness first-order improvements require a uniform conversion from the native payoff Hessian bound, initialization accounting and the exact guarantee.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: b03ebc3dbbd7e9f2c5e1470f567a153d4429c54ebbdc0502e3482232eb408d03

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: b825b29df06d108cc9d6adf32a97b4d315f3079f18817e4fea01bd22d456a71e

Read primary theorems for arXiv:2110.04814v3, 2110.07098v5 and 2411.15769v2: possible dimension-sensitive HVP budget pairs remain unassessed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: c4d1deae40692d2138cb2bbe37d8cb5b64bb557b9e6e320a3d3779338f803890

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 0106c2e6b9f394e7204f4ea0d8e0583f51770d25b58d29c892f7df20f97601b5

Assess arXiv:2610.20345v1, 2606.07003v1 and 2605.06431v1, plus the remaining broader-query leads 2601.10086v1, 2406.13041v3 and 2402.09807v1; metadata alone establishes no applicability, dominance or exclusion.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 4b4a8c7bcd3861c1cbcbb3247df20465d2750daa12bf903277a424871aaf4125

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 27be6934badd884a30f44d5cd4426d55c13b6cc96334a9fd54d7398309bdabbb

Source 6bd43aa82bb739466f4594430d68f49b18e773dde79fc86fbbf96000f44b8e3c, arXiv:2610.16771v2 Theorem 4.1/Appendix F: other sum-lower regimes require explicit finite-block-dimension and simulation checks before extension beyond retained r2.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 28094ce45b450e93626e6d90e7392ecacbf295ccdabfde290c82b248207ae3d0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 816e64d45ab01655b0cdb3174cc88338b9552319d4504b2ed46ed2504883fbc8

retained-material-lead-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 47ed2b0fbcabddbbb196a852acad2fad1d41e2c3b6b1e7d7a09d2673b0bb04a5

Outside Z the Pareto frontier, low-dimensional improvements and other saturation regions remain unassessed by this local update; no converse to the sufficient zero-query condition is claimed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: edd91bc796d09a887410ed90a61bb2fd3268d13066421cac93e7438e31f2680d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 32031bbfee8ebd1328a1aed8882bd60d4abeec527eb705e6e42a022ef963bb52

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: e2357562311f8418a68c1c7b696e35d39f0f0a796c2a6acd48398c460b927d3d

CV_S_NCSC_HVP__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 1633ab1fcddf06f99cbde5b89bca7f2b13bbb766cff12112ff2b4818c205e814

CV_S_NCSC_HVP__main__c2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/2; canonical SHA-256: d6dac124f5f80982d6a39a3965a883f8888c1984f22828128bbf6443ff99421d

CV_S_NCSC_HVP__main__c3_zero_budget

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 39db3a595dcbc9f7067df9b13e1c2baaeb45d73aeccd1bbaf635d557970911ed

curated-scope-limit-ab3e5d3796

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 51918ac5ed3021da4b58c01faece14351ca84016b2ca56ef8c27c4bc83e7469e

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 72ec088c5014357a06da7816fb2c2b96941d93467b3c8eb7bd33404afe9cdd04

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 5c1c53c08b431ff539ee27a32525f3c0ce5d99299b31d78d8deeb31039c49c4f

The achievable resource region q_declared for view main, g1: instancewise success probability >=2/3 for ||grad Phi(xhat)||<=epsilon, arbitrary adaptive randomized algorithms and fixed pathwise caps (N_payoff_first_order,N_HVP), with identity resource projection. Jointly vary Delta,beta,rho,epsilon>0; R_y>=0; positive integer d_x,d_y; 0<mu_y<=beta and kappa=beta/mu_y>=1. No tracked native parameter is hidden in a constant. The normalized A1,A2,r,J are dimensionless under rescaling payoff and spatial units; they abbreviate the native parameters without changing their identities or domains. Universal theorem constants and explicit logarithmic factors remain as retained; confidence is fixed at 2/3.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: ade0ea011aa640b0e5755067ebe78c9583efe552d82bbe4735ee55c96cbfe53a

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 4c73b9b8c81d1f555c57b247bd3db3a72a1f2f23e7ad4b3dc1664d03f440b0f7

CV_S_NCSC_HVP_p_321ee4d0e4

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: e8a03b5b2e5b418665b84d86cd55b90db0b49d8530d80c064bb4fb92d6f77aea

CV_S_NCSC_HVP_p_09dc7c3402

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: c1fde264102864e97be79788019e524a20d521384f829dc92d6e29acc598dc65

CV_S_NCSC_HVP_p_6490ff790f

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: a136e0cd3b19cb9544c1e7a0ae1fd4f4cfb4258f238d6979c025a4fcdc319af3

CV_S_NCSC_HVP_p_34f4aff3ed

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 65c5122a0beb36dc25985c9acd1223550e549ad49e07af75870d1f00ad427796

CV_S_NCSC_HVP_p_30736752f1

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 3f311e36ec1159240d55be45d92cec24db287b448e912bda2bf432b7da40e9ae

CV_S_NCSC_HVP_p_5f588572bc

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: 995f717be69b8e019dc1df76af0038c65ab9fe9609b83bec5c5c723de8e30d20

CV_S_NCSC_HVP_p_668775585d

#### Native item 8

Native pointer: /joint_analysis/target/joint_variables/7; canonical SHA-256: 2af46b10fe72fa7b914c6ae47fa6f7f88353ba49547d5d7d46b4ff5be270127c

CV_S_NCSC_HVP_p_e5b1bf8e9c

#### Native item 9

Native pointer: /joint_analysis/target/joint_variables/8; canonical SHA-256: 27de92a53531bf2211bb3827c4125c9ed0d27c08017dd4519dc8c9e26eeeddb1

CV_S_NCSC_HVP_p_b849970ba6

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: b2877d15839194d073fd4a0e3b0437b0fec042f1ef1b47f3d2a15b04bb2ddb07

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 01470e2f6bd478f37fa1f35d295529b5429fa1a4b97fb9eb6cc85ef93048f9a4

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: de029be4de79d22d39edf779fcb3955640c7adb545efed1943a3d7c0dacb557e

Delta beta / epsilon^2; dimensionless initial-gap to accuracy scale.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 3db1ded320eaa64b10a87875b3cd0c0f2376e0fb4d6f50e7bf87002995696c0e

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 4c73b9b8c81d1f555c57b247bd3db3a72a1f2f23e7ad4b3dc1664d03f440b0f7

CV_S_NCSC_HVP_p_321ee4d0e4

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: c1fde264102864e97be79788019e524a20d521384f829dc92d6e29acc598dc65

CV_S_NCSC_HVP_p_6490ff790f

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: 3f311e36ec1159240d55be45d92cec24db287b448e912bda2bf432b7da40e9ae

CV_S_NCSC_HVP_p_5f588572bc

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 961ea6171fe18f8c510fc30a17ba90b2dc0cca62fd36a1b8749aad14fe357483

A1

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: 72abbb2596887e3da172484b8d1dc5b7ffd9dcf5c6b75057d88447e550d26148

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: ff00acc2d3c8caf3bf4bf00038db57f828297bd6584aa417abb74bba85b6b19f

Delta sqrt(rho) kappa^(3/4) epsilon^(-3/2) = A1 sqrt(r); dimensionless second-order scale.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: 978e98f1fb77c9a6260b129cf1fccc7d6d6ff4d2bf996ae8902e921b173c4400

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: 4c73b9b8c81d1f555c57b247bd3db3a72a1f2f23e7ad4b3dc1664d03f440b0f7

CV_S_NCSC_HVP_p_321ee4d0e4

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/1; canonical SHA-256: 27de92a53531bf2211bb3827c4125c9ed0d27c08017dd4519dc8c9e26eeeddb1

CV_S_NCSC_HVP_p_b849970ba6

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/2; canonical SHA-256: 995f717be69b8e019dc1df76af0038c65ab9fe9609b83bec5c5c723de8e30d20

CV_S_NCSC_HVP_p_668775585d

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/3; canonical SHA-256: 3f311e36ec1159240d55be45d92cec24db287b448e912bda2bf432b7da40e9ae

CV_S_NCSC_HVP_p_5f588572bc

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: fc032765194b27a7af6e61472671edd9a55cae4019c6f63ee6a1bc4307b1f653

A2

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/2; canonical SHA-256: 6976dff6dbbf569b1179320970f111d01c955f4ffb9a209600ff3e2087b64bd1

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/2/expression; canonical SHA-256: e55d506107f19cdc2323302f9ab9078f98c9ad677ee9c0c7473d4abf33c0dff8

rho kappa^(3/2) epsilon / beta^2; dimensionless relative Hessian-smoothness scale.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs; canonical SHA-256: f6fab0d564b6ac90c174bcd1dfb8a819655a60a446635906416a30d58aeb08ee

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/0; canonical SHA-256: 27de92a53531bf2211bb3827c4125c9ed0d27c08017dd4519dc8c9e26eeeddb1

CV_S_NCSC_HVP_p_b849970ba6

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/1; canonical SHA-256: 995f717be69b8e019dc1df76af0038c65ab9fe9609b83bec5c5c723de8e30d20

CV_S_NCSC_HVP_p_668775585d

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/2; canonical SHA-256: 3f311e36ec1159240d55be45d92cec24db287b448e912bda2bf432b7da40e9ae

CV_S_NCSC_HVP_p_5f588572bc

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/2/parameter_refs/3; canonical SHA-256: c1fde264102864e97be79788019e524a20d521384f829dc92d6e29acc598dc65

CV_S_NCSC_HVP_p_6490ff790f

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/2/symbol; canonical SHA-256: 2659efe5502f101c13c3d4f2b330ba7bc6969f33ce5aee8377560e7470bf30b4

r

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/3; canonical SHA-256: 5885955952cb65e5486d226fad3eb41be5c82e62a9c8fe025673a7b858926f8e

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/3/expression; canonical SHA-256: 8c96422e9bb2ea61670b65a048e49eab8bae79013d7663d284c61a43c2201f74

1+min{sqrt(kappa),[rho(R_y+kappa sqrt(Delta/beta))/mu_y]^(2/7)}; dimensionless initialization scale; the retained I0 is tilde O(J).

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs; canonical SHA-256: 2bf4f3b93c91a77bebc5f117d8b968a9397465c4677458047d068122c1634a58

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/0; canonical SHA-256: 995f717be69b8e019dc1df76af0038c65ab9fe9609b83bec5c5c723de8e30d20

CV_S_NCSC_HVP_p_668775585d

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/1; canonical SHA-256: 27de92a53531bf2211bb3827c4125c9ed0d27c08017dd4519dc8c9e26eeeddb1

CV_S_NCSC_HVP_p_b849970ba6

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/2; canonical SHA-256: e8a03b5b2e5b418665b84d86cd55b90db0b49d8530d80c064bb4fb92d6f77aea

CV_S_NCSC_HVP_p_09dc7c3402

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/3; canonical SHA-256: 4c73b9b8c81d1f555c57b247bd3db3a72a1f2f23e7ad4b3dc1664d03f440b0f7

CV_S_NCSC_HVP_p_321ee4d0e4

#### Native item 5

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/4; canonical SHA-256: c1fde264102864e97be79788019e524a20d521384f829dc92d6e29acc598dc65

CV_S_NCSC_HVP_p_6490ff790f

#### Native item 6

Native pointer: /joint_analysis/target/normalized_variables/3/parameter_refs/5; canonical SHA-256: 2af46b10fe72fa7b914c6ae47fa6f7f88353ba49547d5d7d46b4ff5be270127c

CV_S_NCSC_HVP_p_e5b1bf8e9c

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/3/symbol; canonical SHA-256: cd045dd9c71bc81511b2fa015c942988122e9ac918912150ac19faa3a0058fc6

J

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: ade0ea011aa640b0e5755067ebe78c9583efe552d82bbe4735ee55c96cbfe53a

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 4c73b9b8c81d1f555c57b247bd3db3a72a1f2f23e7ad4b3dc1664d03f440b0f7

CV_S_NCSC_HVP_p_321ee4d0e4

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: e8a03b5b2e5b418665b84d86cd55b90db0b49d8530d80c064bb4fb92d6f77aea

CV_S_NCSC_HVP_p_09dc7c3402

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: c1fde264102864e97be79788019e524a20d521384f829dc92d6e29acc598dc65

CV_S_NCSC_HVP_p_6490ff790f

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: a136e0cd3b19cb9544c1e7a0ae1fd4f4cfb4258f238d6979c025a4fcdc319af3

CV_S_NCSC_HVP_p_34f4aff3ed

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 65c5122a0beb36dc25985c9acd1223550e549ad49e07af75870d1f00ad427796

CV_S_NCSC_HVP_p_30736752f1

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: 3f311e36ec1159240d55be45d92cec24db287b448e912bda2bf432b7da40e9ae

CV_S_NCSC_HVP_p_5f588572bc

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: 995f717be69b8e019dc1df76af0038c65ab9fe9609b83bec5c5c723de8e30d20

CV_S_NCSC_HVP_p_668775585d

#### Native item 8

Native pointer: /joint_analysis/target/uniform_in/7; canonical SHA-256: 2af46b10fe72fa7b914c6ae47fa6f7f88353ba49547d5d7d46b4ff5be270127c

CV_S_NCSC_HVP_p_e5b1bf8e9c

#### Native item 9

Native pointer: /joint_analysis/target/uniform_in/8; canonical SHA-256: 27de92a53531bf2211bb3827c4125c9ed0d27c08017dd4519dc8c9e26eeeddb1

CV_S_NCSC_HVP_p_b849970ba6

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Fangqing Zhang; Haihan Zhang; Wendao Wu; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Full-Hessian Oracle Complexity for Nonconvex–Strongly-Concave Minimax Optimization. 2026. arXiv:2610.16771v2, 2026-10-19.

https://arxiv.org/pdf/2610.16771v2
