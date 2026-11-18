# Fresh joint gradients: joint parameter dependence and expected query complexity

**Setting ID.** `BL_SPEC_joint_expected_cost`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; smoothness: Bounded partial gradient; smoothness: Hessian or cross derivative lipschitz; smoothness: Lipschitz gradient; structure: Normalized common scale

**ORACLE tags.** feedback quality: Fresh; interface family: Fresh gradient; operation: Joint primitive gradient response; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** measure: N joint sample; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The full population gradient $\nabla f$ is globally $L_f$-Lipschitz in $(x,y)$; convexity is not required.

The full population gradient $\nabla g$ is globally $L_g$-Lipschitz in $(x,y)$.

For every $(x,y)$, $\|\nabla_y f(x,y)\|\le C_f$. Equivalently, for fixed $x$ the function $f(x,\cdot)$ is $C_f$-Lipschitz. This does not assert that $f$ is globally Lipschitz in value with respect to $x$.

The derivatives $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$ exist and are each $\rho$-Lipschitz jointly in $(x,y)$. No Lipschitz budget for $g_{xx}$ is assumed.

The objective $\Phi$ has a finite lower bound. A point $x_0$ is given and satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$. Convexity or existence of a global minimizer of $\Phi$ is not required.

The initial point $(x_0,y_0)$ and bound $\|y_0-y^*(x_0)\|\le R_0$ are given. This is an initialization budget, not a requirement that the oracle return $y^*$.

The common-scale summary uses $C_f,L_f,L_g\le C L$ with a universal constant $C$, subject to $\kappa=L/\mu$, $\theta=\rho/\mu$, and $\chi=1+\theta$. The full upper bound retains the individual primitive budgets.

The independent public parameter $\Lambda_\Phi$ in the native parameter table is a whole-class admissibility promise: for every legal instance and all $x,x\prime\in\mathbb R^{d_x}$, $\|\nabla\Phi(x)-\nabla\Phi(x\prime)\|\le\Lambda_\Phi\|x-x\prime\|$. Its declared bound must be satisfied together with the initialization-gap budget and every primitive and oracle condition. This is the existing independent parameter definition made explicit in MODEL, rather than a derived estimate obtained by substituting primitive budgets; it introduces no new parameter relation or model assumption.

### Oracle interface

Query $(x,y)$ returns $(G_{f,x},G_{f,y},G_{g,x},G_{g,y})$. Conditional on the transcript and query point, both full layer-gradient estimates are unbiased. Their conditional variance budgets are $\sigma_f^2$ and $\sigma_g^2$, respectively, and need not be equal.

$(x,y)\longmapsto (G_{f,x},G_{f,y},G_{g,x},G_{g,y})$ Conditional on history and query, both full-gradient estimates are unbiased. Their conditional variances are bounded separately by sigma_f^2 and sigma_g^2; the budgets need not coincide.

Each call uses fresh randomness; the $f$ and $g$ blocks of one response may be correlated. The source upper bound uses different fresh samples for lower-level differences at different points.

Every internal strongly convex solve, tilt-direction estimate, and final gradient batch in Theorem B.2 is charged. The ideal y*(x) is used only in the analysis and is not returned by the interface.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2$, with $\varepsilon$ always specified on the gradient-norm scale. Gradient norm and squared gradient norm remain distinct.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

A joint response containing both full layer gradients costs one call, denoted $Q=N_{\rm joint}$. Compare the worst-instance expected call count $\sup_{I}\mathbb{E}[N_A(I)]$, where $I$ is an admissible instance and $N_A(I)$ is the random total number of calls. Do not replace it by a pathwise fixed budget.

Initialization oracle calls count toward the total. A finite initialization bound is an instance-class assumption, not free access to an inner solver.

Use worst-instance expected calls. Random stopping is allowed; this is not a uniform pathwise cap.

Internal processing of available information is free. Comparisons use the explicitly specified scalarization or resource vector. Different resources without given weights cannot be assembled coordinatewise from separate algorithms.

### Algorithm views and success guarantees

Algorithms may use private randomness. Queries, stopping, and postprocessing may be arbitrary measurable functions of the transcript. The output may be unqueried, a random selection of a past point, or an admissible average. No linear-span or zero-respecting restriction is imposed. Queries are sequential; each actual response in a parallel batch is charged separately. Arithmetic, linear algebra, and storage using received data are uncharged. Internal operations, memory, and communication are not tracked by this quantity.

Choose an algorithm from public parameters, then require $\mathbb{E}\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon$ for every admissible instance and legal oracle law. Expectation covers all algorithmic and feedback randomness after fixing the instance.

**Budget convention.** worst-case over instances of expected stopping/query cost E N_A; not a fixed per-run horizon

## 2. Notation and parameters

$x,y$: The upper- and lower-level variables. **Domain:** $x\in\mathbb R^{d_x},y\in\mathbb R^{d_y}$.

$f,g$: The original upper- and lower-level real-valued functions. **Domain:** $f,g:\mathbb R^{d_x}\times\mathbb R^{d_y}\to\mathbb R$.

$\widehat x,x_0,y_0$: Output outer point, public outer initial point, and public lower-level initial point **Domain:** Each lies in its corresponding variable space.

$\Phi$: The reduced objective. **Domain:** Defined in the task specification.

$y^*$: Mapping to the unique lower-level global minimizer **Domain:** Constraints specified under TASK.

$\nabla,\|\cdot\|$: Euclidean gradient and vector norm; matrix and higher-derivative norms are the induced Euclidean operator norms

$\mathbb E,\Pr,\inf,\sup$: Expectation, probability, infimum, and supremum, with aggregation order and randomness specified by the guarantee.

$\mathcal O,\Omega,\Theta,\widetilde{\mathcal O}$: Asymptotic upper, lower, matching-order, and declared-logarithm upper bounds; fixed parameters are specified in each evidence record

$c,C$: Positive absolute constants or functions of fixed budgets, with dependencies specified by the corresponding result **Domain:** $0<c,C<\infty$.

$\varepsilon$: Target accuracy. Whether error is squared is determined by the metric and guarantee formulas. **Domain:** $\varepsilon>0$.

$d_x$: Upper-level dimension **Domain:** Positive integer.

$d_y$: Lower-level dimension **Domain:** Positive integer.

$C_f$: A uniform norm bound on the population upper function’s lower-variable gradient block. **Domain:** $C_f\ge0$.

$\|\nabla_yf(x,y)\|\le C_f$

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu>0$.

$L_f$: Joint-variable Lipschitz upper bound for the complete population upper-level gradient **Domain:** $L_f\ge0$.

$L_g$: A joint-variable Lipschitz bound on the population lower-level full gradient. **Domain:** $L_g\ge\mu>0$.

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: Common joint Lipschitz upper bound for the lower function's cross-Hessian block and lower-variable Hessian block **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: Public initial lower-level distance bound **Domain:** $R_0\ge0$.

$\|y_0-y^*(x_0)\|\le R_0$

$\kappa$: Lower-level condition number **Domain:** $\kappa\ge1$.

$\kappa=L/\mu$

$\theta$: The ratio of the Hessian-variation budget to lower-level curvature. **Domain:** $\theta\ge0$.

$\theta=\rho/\mu$

$\chi$: Variation scale including a constant term **Domain:** $\chi\ge1$.

$\chi=1+\theta$

$\Lambda_\Phi$: An effective Lipschitz bound on the reduced gradient. **Domain:** $\Lambda_\Phi>0$.

$\|\nabla\Phi(x)-\nabla\Phi(x\prime)\|\le\Lambda_\Phi\|x-x\prime\|$

$\sigma_f$: Conditional standard-deviation bound for the full stochastic upper-level gradient **Domain:** $\sigma_f\ge0$.

$\sigma_g$: Conditional standard-deviation bound for the full stochastic lower-level gradient **Domain:** $\sigma_g\ge0$.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$G_f,G_g,\mathcal H$: Upper- and lower-level stochastic full-gradient responses and the pre-draw history. **Domain:** $G_f,G_g\in\mathbb R^{d_x+d_y}$.

$G_{f,x},G_{f,y},G_{g,x},G_{g,y}$: Outer and lower blocks of the corresponding full stochastic gradient **Domain:** Outer-block dimension d_x and lower-block dimension d_y.

$k$: The condition number defined using the primitive lower-level smoothness constant. **Domain:** $k=L_g/\mu$.

$E_\rho$: Hessian-variation error scale in the hypergradient finite difference

$E_\rho=(1+k)\rho C_f^2/(2\mu^2)$

$N_{\rm joint}$: The number of joint full-gradient sample responses for both levels. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}\mathbb E C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\mathrm{joint}}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Original model with a common scale

**Region.** Assume $L,\Delta>0$, $\kappa\ge2$, $1\le\theta\lesssim\kappa$, and $0<\varepsilon\le c\min\{L,\kappa\sqrt{L\Delta}\}$. The lower bound requires sufficiently large hard-instance dimension. The query budget is worst-instance expected cost.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Lower bound missing

**Lower bound.** B4

$$
0
$$

**Upper bound.** B1, B3

$$
\begin{cases}0,&2\Lambda_\Phi\Delta\le\varepsilon^2,\\\widetilde O((1+\Lambda _\Phi \Delta /\varepsilon ^2)[1+k+(1+k)^2 \varepsilon ^{-2} {\sigma _f^2+(L_f^2/\mu ^2+1+E_\rho ^2/\varepsilon ^2)\sigma _g^2}]), k=L_g/\mu , E_\rho =(1+k)\rho  C_f^2/(2\mu ^2),&2\Lambda_\Phi\Delta>\varepsilon^2.\end{cases}
$$

**Gap or comparison.** On H intersect E, Q*=0 and a multiplicative ratio is inapplicable (0/0). On H outside E no verified positive lower envelope is retained; the old factor-chi gap is suspended pending a valid hard-family mapping.

**Comparison argument.** The endpoint and transfer counterexample are proved in BL_SPEC_joint_expected_cost__main__p_zero_query. The original b1 upper statement is retained conditionally; b2 has no active bracket reference. Missing positive lower support outside E is explicit.

## 4. Bounds and supporting evidence

### B1 - frozen-tilt estimator and descent

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\begin{gathered}\widetilde{\mathcal{O}}\!\left(\left(1+\frac{\Lambda_\Phi\Delta}{\varepsilon^2}\right)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right),\\k=\frac{L_g}{\mu},\qquad E_\rho=\frac{(1+k)\rho C_f^2}{2\mu^2}.\end{gathered}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Oracle correspondence.** One joint call returns full gradients of $f$ and $g$ and costs one unit. Fresh responses are conditionally unbiased with separately specified variance budgets $\sigma_f$ and $\sigma_g$. The stopping-time call count may be random; complexity takes expectation before the worst case over instances.

**Guarantee conversion.** The native objective is $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon$; an expected norm is not strengthened to a root-mean-square criterion.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** The charged resource is $N_{\rm joint}$. Cost is sup_instance E N_joint, distinct from a fixed execution cap. The expression E_rho retains polynomial dependence on C_f; arbitrary C_f cannot be suppressed to claim dependence only on L and kappa.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\widetilde O((1+\Lambda _\Phi \Delta /\varepsilon ^2)[1+k+(1+k)^2 \varepsilon ^{-2} {\sigma _f^2+(L_f^2/\mu ^2+1+E_\rho ^2/\varepsilon ^2)\sigma _g^2}]), k=L_g/\mu , E_\rho =(1+k)\rho  C_f^2/(2\mu ^2)
$$

**Constants.** Only universal constants and logarithms of regularity, initialization, and accuracy are hidden. Every polynomial factor is explicit.

**Logarithmic factors.** Inner-contraction and initialization logarithms.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) equations: (41); (42); (43); pdf pages: 18; 19; section: Appendix B; theorem: Theorem B.2

### B2 - multiscale conservative hard family

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\chi^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Conditions.** Original scalar-function-gradient subclass already supports lower.; Dimension sufficiently large as Lemma A.5.

**Dimension conditions.** Arbitrary finite dimensions; lower hard family may require dimensions growing with the budget.

**Oracle correspondence.** One joint call returns full gradients of $f$ and $g$ and costs one unit. Fresh responses are conditionally unbiased with separately specified variance budgets $\sigma_f$ and $\sigma_g$. The stopping-time call count may be random; complexity takes expectation before the worst case over instances.

**Guarantee conversion.** The native objective is $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon$; an expected norm is not strengthened to a root-mean-square criterion.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** The charged resource is $N_{\mathrm{joint}}$, with cost $\sup_{\mathrm{instance}}\mathbb E N_{\mathrm{joint}}$. This differs from a fixed execution budget.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.**

$$
\Omega (\kappa ^2 L\Delta  \varepsilon ^{-2}+\chi ^2 \kappa ^8 \sigma _g^2 L^3\Delta  \varepsilon ^{-6})
$$

**Constants.** Universal constants; the source window additionally requires $\rho\gtrsim\mu$ and $\chi\lesssim\kappa$. No matching lower bound for the upper-level noise term is asserted.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) equations: (30); (31); pdf pages: 16; section: Appendix A; theorem: Theorem A.6

### B3 - Return x0 without queries

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** All frozen model and native parameter-domain constraints.; 2 Lambda_Phi Delta <= epsilon^2.

**Dimension conditions.** Uniformly in every admissible finite dimension; dimensions are still included in the minimax supremum.

**Oracle correspondence.** No response from any interface is requested. The claim holds for every legal fresh-gradient oracle law.

**Guarantee conversion.** Returning x0 deterministically has ||grad Phi(x0)||<=epsilon, hence satisfies the same expected-norm guarantee g1 without a mean-square-to-norm ambiguity.

**Output rule.** Return the supplied outer point x0; unqueried outputs are permitted.

**Resource conversion.** N_joint_sample=0 almost surely, hence worst-instance E N_joint_sample=0. Counts are nonnegative.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.** 0

**Constants.** Exact zero; no hidden constants.

**Derivation.** {'evidence_basis': 'retained_baseline_derivation', 'proof_refs': ['BL_SPEC_joint_expected_cost__main__p_zero_query']}

**Source location.**  section: Complete analyst derivation in BL_SPEC_joint_expected_cost__main__p_zero_query; theorem: Smoothness descent and an explicit joint-parameter counterexample

No external theorem is introduced. Existing source support for the original theorem is preserved as history.

### B4 - Resource nonnegativity

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** All frozen model and native parameter-domain constraints.; 2 Lambda_Phi Delta <= epsilon^2.

**Dimension conditions.** Uniformly in every admissible finite dimension; dimensions are still included in the minimax supremum.

**Oracle correspondence.** No response from any interface is requested. The claim holds for every legal fresh-gradient oracle law.

**Guarantee conversion.** For every admissible algorithm meeting g1, its expected response count is nonnegative. Together with the independently proved zero upper algorithm on E, this gives the exact endpoint lower side.

**Output rule.** All permitted outputs and randomized stopping rules remain allowed.

**Resource conversion.** For every algorithm N_joint_sample>=0 almost surely, hence its expected count and the minimax infimum are nonnegative. The matching zero upper algorithm is a separate proof step.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.** 0

**Constants.** Exact zero; no hidden constants.

**Derivation.** {'evidence_basis': 'retained_baseline_derivation', 'proof_refs': ['BL_SPEC_joint_expected_cost__main__p_zero_query']}

**Source location.**  section: Complete analyst derivation in BL_SPEC_joint_expected_cost__main__p_zero_query; theorem: Smoothness descent and an explicit joint-parameter counterexample

No external theorem is introduced. Existing source support for the original theorem is preserved as history.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 6eef3ddd6004d8cc93b7ca36df39fbd0c0e2e42a42b293f331266d0abfe84a11

### Native proof: BL_SPEC_joint_expected_cost__main__p_zero_query

Native pointer: /proofs/0; canonical SHA-256: d0259d865423a4fb88b612bc5b00f26ff2157bc7585447cf7c3809be48356bce

#### Native field: evidence_refs

Native pointer: /proofs/0/evidence_refs; canonical SHA-256: 9b83cff8b1a42c5346392e201d9cec290464e9e4a64a4a960260d3f13173612f

#### Native item 1

Native pointer: /proofs/0/evidence_refs/0; canonical SHA-256: 8b707fea8a66733c080cbeff5f52f33137e742f83e934d97de5dceba65706f6f

BL_SPEC_joint_expected_cost__main__e3

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: premises

Native pointer: /proofs/0/premises; canonical SHA-256: fe9b76bb1c6d5cb21e3960ae2783206f87b69e451b582045936e7c3dc9f2b8fe

#### Native item 1

Native pointer: /proofs/0/premises/0; canonical SHA-256: f0dfacda982e884d4ec39b782ccf523db23705214725630e99739cc8d2358e14

#### Native field: pointer

Native pointer: /proofs/0/premises/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/premises/0/sha256; canonical SHA-256: 964086511f3018e4e7abd91174ce5b92ce43aaffe2fc4d873dd0e62bdc0dca6d

ceca4e7c6ec43934abd8aad69c1dc4ce7a250f35e14a5835efc6ac1e1a04705f

#### Native item 2

Native pointer: /proofs/0/premises/1; canonical SHA-256: 18c097dc382c96be37b9b22cf1c78589c87233c50c96e631ede1ac02fafd61c4

#### Native field: pointer

Native pointer: /proofs/0/premises/1/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/premises/1/sha256; canonical SHA-256: 3e8b68c9eba407fbd17d730b90f2e8040ac03e836d6b748a82a1ed2d6c786480

6bd2eebfbb8e22955d1cb7d4f8c0c254d7b6bf1d37babcd44050b9feb6762e3c

#### Native item 3

Native pointer: /proofs/0/premises/2; canonical SHA-256: f890e6b9c77fd1638bf3d36bd5333da9fc823c7935908c848d29f248c42150eb

#### Native field: pointer

Native pointer: /proofs/0/premises/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/0/premises/2/sha256; canonical SHA-256: a90647f1ccfd354219dea3b3a673136d058540206fbcdf10938cfce890b206af

4d8fd29b92a3bf0092ebb4fecb0fd15deb2ca05a0dbe355fff32934843c8e0c2

#### Native item 4

Native pointer: /proofs/0/premises/3; canonical SHA-256: d6710e2895bff04216ffa3ffa8a3c61a163c9636a2c8072ac5597839178df7bc

#### Native field: pointer

Native pointer: /proofs/0/premises/3/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/premises/3/sha256; canonical SHA-256: 57f76ce346e15a37fcac3fe83031350f37cc2a81127e80a630403dfe96504224

369bfdfba279f845c0805be2ec40d8770d10503770c5399b0c2116dd86757a7d

#### Native item 5

Native pointer: /proofs/0/premises/4; canonical SHA-256: bca927000bff7e6e35101fe1faee841f4b28f832c2054a85b44d69ee4341f6a3

#### Native field: pointer

Native pointer: /proofs/0/premises/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/0/premises/4/sha256; canonical SHA-256: 55dffa2e1f5b152dff137dcb38bac47a0b04002ca8af65474d2040838fbf6ea7

fd19c50dc5cbe6d31f7b8408a3fe9b0866f63f570e249a91326a5b72eb7b18ed

#### Native item 6

Native pointer: /proofs/0/premises/5; canonical SHA-256: ac5d25d6c14cefcbb328a935c094349f3568b69a19cffded2559b56026da5ce4

#### Native field: pointer

Native pointer: /proofs/0/premises/5/pointer; canonical SHA-256: d6039afddf27bddb8de5dba6560d032afc09d8a78c6a685d9519ce1cea90d703

/bounds/1

#### Native field: sha256

Native pointer: /proofs/0/premises/5/sha256; canonical SHA-256: 97ef2455b90411f95bb195ed630aa7a278c5592bf51ea53d5f0427a280c439fc

40bba78e2aefee06fb788a9fa40c046a8af71108d2018f1d3f2425119cc96e88

#### Native item 7

Native pointer: /proofs/0/premises/6; canonical SHA-256: 51a958da2c1ac1a08ec85bdfda9a073b3d77a81ea2b00000bda4519a75cc0f1b

#### Native field: pointer

Native pointer: /proofs/0/premises/6/pointer; canonical SHA-256: 093a9ad2f779c83c2483d0b2930a00cfedd078d5514a96b1e08bc8c92c96a35b

/comparisons/0

#### Native field: sha256

Native pointer: /proofs/0/premises/6/sha256; canonical SHA-256: b93e9b7b28f6392fc91448f9ae13a63ce992e22bb3daf8c9f4e65aa1c1e7ceaa

3cc36dd53a1b28b7ec361c916a618d99b2a146810a43c242b9c0ca520e5d57dc

#### Native item 8

Native pointer: /proofs/0/premises/7; canonical SHA-256: 32ee4f12ad7eab4525880a19a11afc7c030ce23bf5fcc67f4ef24981eed8e963

#### Native field: pointer

Native pointer: /proofs/0/premises/7/pointer; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: sha256

Native pointer: /proofs/0/premises/7/sha256; canonical SHA-256: cb58214364128e7fa64b91fa3ed42b74cdf44f73c7e3bbef0b121f37e62cb465

08e51bb1f0fba5279523f61420bf98323829aa188915d03823a6b597a8834009

#### Native field: proof

Native pointer: /proofs/0/proof; canonical SHA-256: 3265425944410504304314582b2310e0346ca9d058202532ac2a8d4024049e30

H is exactly the frozen regime BL_SPEC_joint_expected_cost__main__r1 (including its symbolic universal constants and dimension qualification). Let D denote the frozen model and all native parameter domains. The independent public parameter Lambda_Phi is a valid global Lipschitz bound for the reduced gradient. For any admissible instance, put v=grad Phi(x0). Smoothness at z=x0-v/Lambda_Phi gives inf Phi <= Phi(z) <= Phi(x0)-||v||^2/(2 Lambda_Phi). Thus ||grad Phi(x0)||^2 <= 2 Lambda_Phi Delta. No oracle is used to compute z; it is only a proof point. On E={D:2 Lambda_Phi Delta<=epsilon^2}, the permitted algorithm that returns the supplied x0 without queries meets the expected-norm guarantee for every legal instance and oracle law. Its worst-instance expected count is 0, and resource nonnegativity gives Q*=0. Equality and Delta=0 are included; this is a sufficient zero-query region, not a converse threshold. To test the old lower transfer uniformly, fix L=Delta=1,kappa=2,mu=1/2,theta=1,rho=1/2,chi=2,L_f=L_g=C_f=1,R0=0,sigma_f=0,sigma_g=1, and let epsilon tend to zero while Lambda_Phi=epsilon^2/4. These values satisfy H for all sufficiently small epsilon and E for every epsilon. The class is nonempty in every finite dimension: f=0,g(x,y)=mu*||y||^2/2,x0=y0=0 and exact gradients satisfy all stated upper budgets and the initialization certificate. More importantly, the same return-x0 algorithm works on the entire admissible class at these budgets, not only that example. Hence Q*=0 whereas the old b2 expression is strictly positive and grows as epsilon^-6. The transfer into a quantity that varies Lambda_Phi independently is therefore invalid as recorded. This does not disprove the source theorem for its original primitive-budget class. Quarantine b2's current target formulation pending a separately proved guard ensuring that its hard family meets all public budgets, including Lambda_Phi. No positive lower bound is retained outside E merely by weakening the old formula.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: d64c24ef22edf86ad95684d182d2cbacaab771cd485ccc075424ec4cb550ff11

Q*=0 on E; the active b2 target transfer on H is not valid uniformly in the native independent Lambda_Phi budget.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 480be0c97ad3abed357c3deaf2124bd97118f991f83f26ad95e11a3c34a83f82

Exact sufficient zero-query region and counterexample to the recorded uniform lower transfer

### Native proof: BL_SPEC_joint_expected_cost__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/1; canonical SHA-256: 917f634e2447b6efd163477b03323ad54f58a8e15dd7d1090af5ecbc6dc758ce

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 684c665b3c4a236b79d382a25b94eb03fc9570c5fe4b721f3a0d02e3cd7a093a

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. 

#### Native field: comparison_refs

Native pointer: /proofs/1/comparison_refs; canonical SHA-256: c2fae5c3e77d355b847e3b46b5c6fba1a15b537601f4f646168a5ceebcc86dd5

#### Native item 1

Native pointer: /proofs/1/comparison_refs/0; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: evidence_basis

Native pointer: /proofs/1/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

### Native proof: BL_SPEC_joint_expected_cost__proof__model_lambda_phi_identity_20261116

Native pointer: /proofs/2; canonical SHA-256: 00722ecf7e9aa0d2739e714da6548197e23d7391fbfbd84537b43dbb19f40144

#### Native field: baseline_refs

Native pointer: /proofs/2/baseline_refs; canonical SHA-256: 0ec42937556bec7ae4b4f94d2495688ddb758286c565849d6f28e61f2ddfe755

#### Native item 1

Native pointer: /proofs/2/baseline_refs/0; canonical SHA-256: a554789485c3f11d5b2d82a3e5302276c413af1c79cd097a5f2a6e2a65f9204a

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/0/pointer; canonical SHA-256: c33f2326ad2bc3d67f99ab6a2f05b7c92c4a4e8ab5e28421b8b12dda042c0ecd

/parameters/14

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/0/sha256; canonical SHA-256: 5d8be73a378a6338d2ba1f2de7fcd2f9737ce231ea265a70b8fa6d3642410375

e6b59b34d41c170ce93591ceb0197e151cabbc55406992df338d2e94eb2b08f6

#### Native item 2

Native pointer: /proofs/2/baseline_refs/1; canonical SHA-256: f0dfacda982e884d4ec39b782ccf523db23705214725630e99739cc8d2358e14

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/1/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/1/sha256; canonical SHA-256: 964086511f3018e4e7abd91174ce5b92ce43aaffe2fc4d873dd0e62bdc0dca6d

ceca4e7c6ec43934abd8aad69c1dc4ce7a250f35e14a5835efc6ac1e1a04705f

#### Native item 3

Native pointer: /proofs/2/baseline_refs/2; canonical SHA-256: 44c9330699ee931f4086aa47d9d50cf4d816086f1192c2a529020001a5ad0f48

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/2/sha256; canonical SHA-256: 2c413a908496578634085de90ff1ba2e20be7bc9a6948fab621bb07be5cfbb30

82d1f71c5a80a8c731ea55aaf0059b0b300ca60e8ce50936c2c206a524da63d1

#### Native item 4

Native pointer: /proofs/2/baseline_refs/3; canonical SHA-256: d6710e2895bff04216ffa3ffa8a3c61a163c9636a2c8072ac5597839178df7bc

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/3/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/3/sha256; canonical SHA-256: 57f76ce346e15a37fcac3fe83031350f37cc2a81127e80a630403dfe96504224

369bfdfba279f845c0805be2ec40d8770d10503770c5399b0c2116dd86757a7d

#### Native item 5

Native pointer: /proofs/2/baseline_refs/4; canonical SHA-256: 49857c571fe3df8b3404e47846db78b291bbf571e3f2bf86bb11e7465190ac49

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/4/sha256; canonical SHA-256: 30e6f78a927c56588651f1b8e1c5b61a626385dfc12feb759229570f28ea0fbc

b3839b6290917d6311f231580e1d71f63debb88a875ae2c4737de0d0f217fac2

#### Native item 6

Native pointer: /proofs/2/baseline_refs/5; canonical SHA-256: 20a9df497f4fd6de14698343b03dcbeb22ca77a34dfba9756e81eb3de7a61523

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/5/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/5/sha256; canonical SHA-256: b43a0ece240c6799e0f4e730b76749c963e9091a7d581cc481e28dc42cc4728b

bfbcd699eab7a0ef8a15586f77beed2e9ad6f45b2eb0536a8c4b671129355b63

#### Native item 7

Native pointer: /proofs/2/baseline_refs/6; canonical SHA-256: 40ae26f11578857f0d4811a4e79efeb08a17c8640e755561ae72276ca0402bde

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/6/pointer; canonical SHA-256: 710d9e6bcc130379a8bad365103ceedd68708a0b078f97fda36e184171d24280

/comparisons

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/6/sha256; canonical SHA-256: 8b1cfd685bf25868d761da7f4d431d5934ff73d6deea083b6df8358bf5e123d4

1243b228f788bebf866a7a645c279c118eb8bdf4ff33b1ccfbdd1675e8bb6a70

#### Native item 8

Native pointer: /proofs/2/baseline_refs/7; canonical SHA-256: 121d6ebeddd74d621faf123cb4f723f767f2fd86eec7b6195bce2cc96014365a

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/7/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/7/sha256; canonical SHA-256: fd616c5ed35b8ce9cca0eca1870a0515587a17b402ba7849e7f5a07cef9bb557

a899686cb864ea495f69f3a71f336d8011047da6b6e070e37af68ddcafed6c0f

#### Native field: body

Native pointer: /proofs/2/body; canonical SHA-256: e7bbd63259a61b623c9ac5b73fb22eb2fb08cb634fc10973ed54586543867e08

The frozen parameter at /parameters/14 has stable ID BL_SPEC_joint_expected_cost_p_5ffc729833; it is public, kind independent, has no dependencies, positive domain, and defines the Lipschitz upper bound for the reduced gradient on the declared full upper-level domain. A legal instance of the original native profile must satisfy its public parameter definitions/budgets as well as common_specification. Let C_old be that class for a fixed admissible public parameter tuple. Let P be exactly the displayed inequality in that parameter definition, quantified over all upper-level points. Hence C_old is a subset of P. The appended MODEL paragraph states P and its already-declared independent role, leaving every previous definition and condition in force; thus C_new=C_old intersect P=C_old. Conversely every new instance satisfies every old condition since none is removed or weakened. The instance/oracle-law map in either direction is the identity. It preserves dimensions, f and g, initialization and gap, norm bounds, lower-level curvature, noise/primitive budgets, output, probability/expectation quantifiers, and every charged gradient/Hessian/vector call. Therefore every unchanged native statement retains exactly its original applicability, conditional on the same accepted premises; no withdrawn lower bound is reinstated and no external theorem is recertified. Independence means Lambda_Phi is not silently replaced by a formula in primitive budgets. This proof does not assert that arbitrary contradictory budget tuples admit an instance; feasibility and all original compatibility conditions are unchanged. In particular any hard-family transfer had to satisfy the public Lambda_Phi promise before and after the prose clarification. This is equality of the already-defined classes, not adoption of a new smoothness hypothesis or a new complexity inequality.

#### Native field: kind

Native pointer: /proofs/2/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_refs

Native pointer: /proofs/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/2/statement; canonical SHA-256: a645c98dade67a1e7b1fdf80883b1eb0ae1e8008a7cd3cf10b87d0a4d3fdb24c

Appending the MODEL paragraph makes the existing parameter-14 promise explicit and preserves the complete native admissible class and complexity statements.

#### Native field: title

Native pointer: /proofs/2/title; canonical SHA-256: 2fc1cf08bd034c5c9d342baedf60407bc9460146ebeb86ce94e67f4dba4330c7

Same-class interpretation of the already-declared independent Lambda_Phi budget

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 3d1b97a6352f449ca3864afd237241839b6628078a67669d51d65f48d5e62908

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 1865ba304969f17eb1d408d49ec6d797744ab4d21eabeaf0aa86cbba899717e1

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: fd5eb25920aeaa5aa11bdba4b42c068d6edd839be45907e9955e2b85a53aea02

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 0f27a8ea5244bbbe43fc41c67501c79d071319af07e890808264f3b11de5e4c2

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: ebbe956cd0a273b431ba768f975958e7316b556847f7904cc1461b26aea75337

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 685a3367ec58e179d14c513cb1d7d2a27beed943c941b29815713c0dec48c8dc

H outside E

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 32eaa07a755bb491c3e652dd441382e86d21198560f26c8ca57ed164323fdfef

BL_SPEC_joint_expected_cost__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 9f86235fa6714f2a7aa97cd24e152473767161f01df6528ed516e4be145eea40

Its original positive upper formula remains valid on H; the exact-zero algorithm dominates it on H intersect E.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 535111743a4bc0220b557dd5653fdfbd6221741c3a1b58c78627c6622954cbf3

The frozen H guard, conditionally retained unchanged.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 1e369d5477f1a795d09f3af55a22c98bf30b25896348fd78d01104fc83afcbb4

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 52e5791b4f00667f9a2e992dc924d663409010eec195f6b2ba165886bb57c54a

BL_SPEC_joint_expected_cost__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 7c525a6bac636cb42a86ff37c2d15da98e2ce6f5803e4c94c334bf6bd16dfcd5

Quarantined in full until a corrected hard-family applicability guard is verified. The source theorem itself is not declared false.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 8ae9cd2540becf8ed95bbf0500d8c0d125f7d6bb32fe8bf1ad85f1c913537011

The recorded target guard H is disproved as a uniform transfer to the independently Lambda_Phi-indexed quantity.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 20305c85f205e71fc545b64ecb94e47a9a3f709a942459d622979aded0055960

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 11953802b4ed54891966fb480e1b6635b9391e749840570528454e5d48c41e83

H intersect E

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 5e5bb8095408578c1bbf27fa2c5d3468fbeaee3ab4f0219164445470b76d034f

BL_SPEC_joint_expected_cost__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 1376e40812f228484205d5e5994406255dc1f0cabf9cb675adf2a88819fb1415

Exact zero-response upper bound supersedes b1 on the adopted intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 9c4b09aedb1d9aca503d0a9444b1143f4d93ebc516d1d6dd574fe9aeb4e21325

D and 2*Lambda_Phi*Delta <= epsilon^2, where D is the complete declared parameter/model domain

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: 9222e76fcc675cb0de09edd6f8f59a40af4876099ba5176e0a284e5e47f3dc57

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 11953802b4ed54891966fb480e1b6635b9391e749840570528454e5d48c41e83

H intersect E

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 713f63d69b0f7adce84630c8c53066c5dd3998a068eafd0dd649c6bff2cf9f1c

BL_SPEC_joint_expected_cost__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 81772080326fc4a6175f69bfdd228dee30c8508dd9ae7d40705e2dc96d8add6f

Resource nonnegativity matches the zero upper bound. It provides no positive lower envelope outside E.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 9c4b09aedb1d9aca503d0a9444b1143f4d93ebc516d1d6dd574fe9aeb4e21325

D and 2*Lambda_Phi*Delta <= epsilon^2, where D is the complete declared parameter/model domain

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: a44820e5a15cf8322132e07219e33a06babe4e0022cff3d267ed6893abf69b8c

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 035dadfb7f00a99e07e8d479cc81b8d088d6fcbbb2c4809cbbb97490e9c6a14e

Equality 2 Lambda_Phi Delta=epsilon^2 belongs to E and is solved with zero queries.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: c381b71a63839b193c333511d2fd810f38e73a5d8e0dc6b7fa12aed9f8481695

Delta=0 is outside H but belongs to the new endpoint comparison.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: e82c1ae59c5aeae302ab4f17f7dc2fad7295ac865b19eecef08cace4bae1daec

The sequence L=Delta=1,kappa=2,theta=1,chi=2,Lambda_Phi=epsilon^2/4 and epsilon->0 lies in H intersect E and disproves the former uniform positive lower transfer.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: a6403d5c997bf9e7204e759d4cebddc53b83bfa0c5651d85e4fb0c161f897f7e

The original sufficient large-hard-instance-dimension condition is not an intrinsic phase transition; zero-query validity is dimension-independent.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: b0d203435deb47b4fcc81a9cc37d98c47ff8439c22b30673773cce0b9571deaa

No one-query, positive lower, or fixed-dimensional saturation claim is inferred outside E.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: ce03a6f2bdf1b5c3f61f0948089e6a8db097e90433170fc458a072a6c44c681b

On H intersect E both envelopes are zero and the ratio is inapplicable. On H outside E there is no verified positive lower rate, so the old factor-chi gap cannot be asserted.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 5feddd0b6157e4ff41105a8e602c2548edd225c2214aa72f04028dfa6fa526fa

Exact 0 on H intersect E. On H outside E only cost nonnegativity is known in this update; the old positive lower transfer is quarantined.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 96b1b27abcd890f3ae105d90b1be7de40e596f669d97b11be521c287a3ef461f

A valid positive lower side and corresponding joint gap on H outside E must be re-established with all public budget restrictions. The retained upper statement is not freshly recertified.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 906ad814133a2fd86eb3b3b96ed0bad27e6d60fc532ab8647f0845c33cf94c93

0 on H intersect E; O-tilde(U) on H outside E. U=(1+Lambda_Phi*Delta/epsilon^2)*(1+k+(1+k)^2/epsilon^2*(sigma_f^2+(L_f^2/mu^2+1+E_rho^2/epsilon^2)*sigma_g^2)), k=L_g/mu, E_rho=(1+k)*rho*C_f^2/(2*mu^2); upper cost is O-tilde(U) with the unchanged initialization/accuracy logarithms

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: f339ad9eab1e14f7c440fb15219577726cea60c7f5a55687d6a310fae414d6f6

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 1264c8c74bf0bd2aa4db7af28a977c3c92890dedd1deec2fec4ee75d303bf00f

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 7dd0df080f4b792eedf9b377b09ae7af08e77ef5ce5e6b50889ac9107f91a25a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 32eaa07a755bb491c3e652dd441382e86d21198560f26c8ca57ed164323fdfef

BL_SPEC_joint_expected_cost__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: cbecbe78c22d652177eb6e51862cf64e909e45bd55acfb79393252f7f7bcab3d

On E intersect H its positive upper formula is dominated by exact zero; outside H it has no adopted extension.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 5816c1a47f83329e89611c80e697305c4a1bdd5fa87cd33df07a47c3166a67f3

Only H is conditionally retained.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 47678f6f2d832b998b1cec218da95407b1e85341cc788eb7f7398372968116bb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 52e5791b4f00667f9a2e992dc924d663409010eec195f6b2ba165886bb57c54a

BL_SPEC_joint_expected_cost__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 2ab5a4855f30aa4fdae72b077bca344aa0a2773353cd25529169c63d7c32ad66

A positive lower cost cannot apply anywhere in the exact-zero comparison. No restoration guard has been inferred.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 11b8633a274e40df56e94520741a5c34f539da3c2f03e011aa909a7c93c0528b

Invalid recorded target transfer on H; inactive.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 7a43cce14b26113c7568c6001058ae01cd4e89c52e06e0ee630efa59f412005b

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 43e6e2bebb3774311cf0c867d2fae5da733792224e8bac1d455eff172ff6af27

E

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 5e5bb8095408578c1bbf27fa2c5d3468fbeaee3ab4f0219164445470b76d034f

BL_SPEC_joint_expected_cost__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 86f57d3c94ff2611a25a20c0a5a8fbb957a7597294ea00e9f7abbabc619fc2f1

Return the public x0.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 9c4b09aedb1d9aca503d0a9444b1143f4d93ebc516d1d6dd574fe9aeb4e21325

D and 2*Lambda_Phi*Delta <= epsilon^2, where D is the complete declared parameter/model domain

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: a32c6097f88ee5d96e58164ef5e43e76551d502d23076144c7dba6556f5a01aa

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 43e6e2bebb3774311cf0c867d2fae5da733792224e8bac1d455eff172ff6af27

E

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 713f63d69b0f7adce84630c8c53066c5dd3998a068eafd0dd649c6bff2cf9f1c

BL_SPEC_joint_expected_cost__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 50f309807fdc27808f84ca313ee749942e3936e4d4c97b158f6f8e0f97fb40b2

The expected response count is nonnegative.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 9c4b09aedb1d9aca503d0a9444b1143f4d93ebc516d1d6dd574fe9aeb4e21325

D and 2*Lambda_Phi*Delta <= epsilon^2, where D is the complete declared parameter/model domain

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 636d932e60650c5f1076cd3dd1ff9f100b7a222f389dd2c6568a13c12fbed6f1

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 103dc92b3a018a59b138f0aca965136e3ac5c3165b7f635fe711665b580ef296

The sufficient activation inequality is exact, with equality included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 6a8a3f4e72be4b0d305342355002b1380cc4fbb98ad126c56c972ef6e3683f02

For Delta=0 the bound holds for every epsilon>0 and every Lambda_Phi>0.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: f5ba5544df1cecd49bbceac1a4a378b250c78f49211160e9d650bb3315e1065b

The step x0-grad Phi(x0)/Lambda_Phi occurs only in the proof and requires no query or implementation.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 4dd3bad369160b69e0a4b333883bfee12c0ee6949323c868e64373eed93e6a10

No converse or maximal zero-query threshold is claimed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 232d382a43492b00abc4265ee584dfc9748f8eb0cb65d898b45c38674fea10ee

Q*=0; a multiplicative ratio is inapplicable (0/0).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 65f68fae58b5e7fe242615ab6cd62969e9ea05d190e081d2867b9001044691be

0 exactly on E by nonnegative resource cost.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 383383ff559160a39d7dbe60968707fee4369da5eef905952166791e17a555cd

None inside E. The complement is addressed only where a retained upper comparison exists and is otherwise unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 96628edb1599607df3e6a75c7475d229eb07b8764acf0b563a8fa5a9cfe75aa7

0 exactly on E.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 958438453a7fc95a9fff3b29025b31b8acb46c8cac9a59752f8d2fdcb3a5e9c0

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: c8e98bb3095c9d7cb12ae40e04753f824fedf569f45be787ea302ac5cbe0b7c9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 643e3802d257305990fafa4c9b39b458fb36d1c8c2639c9e745c59f9c62b7c92

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: b197ebc2b058323bfc4015476172a8235f37d1442ba970c400a89c8c7f71f070

zero_inside_H

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: c2fae5c3e77d355b847e3b46b5c6fba1a15b537601f4f646168a5ceebcc86dd5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 271c5d2a74a5b3be999bfdd65d48f737fd49373c885356212ab804519f190098

Exact Q*=0. The formerly positive b2 transfer is contradicted here and is quarantined.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 5c21db2e03343d8bee563185f3a85071bf5eb39d7efa20c744cf2694c110aa69

D intersect E intersect H

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 696f1270522df48cdb4c092807f8a195e52a53ec4206285b1947c250d4aad2e8

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: a8153731c0762d63a5f88885f35ae8aa9d36d91c0e149363f4d8b9d1c4493dbe

zero_outside_H

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: c2fae5c3e77d355b847e3b46b5c6fba1a15b537601f4f646168a5ceebcc86dd5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 9fb3ebfcbf6f7b58667d309b770404973e8f0454e62e0e3e7c9d3aacc4ae0c75

Exact Q*=0, including all Delta=0 cases; the old upper bound is not extended outside H.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 40d0249df699ce739289e4ffa02c92cdd47723fb302bcddfb25fd7fa08f6cd58

D intersect E outside H

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: ae828dfafec8ed3ef84650ef88498ece8f4c161aa0167f5b5a678d7fcfd0a438

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 0e7a6d0299d4d053c3e424b456139e369be9689694c710cefe19782a9a7502e5

H_nonzero_unresolved_lower

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: e322498d3f9b5ca7b756ef907658474206fdcc5339d9dcfd2e81bc06016aeb08

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 8d1020c4a89f995da09d84773a343437e5362e299c19f80033ebaa5615781927

Retained b1 upper only; no verified positive lower rate remains after quarantining b2. This is a missing supported bracket side, not a theorem asserting universal absence of a lower bound.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 1f5a4e72691088591abefbb9025b21ca9811f316ee2d3c799b2023592e539821

D intersect H outside E

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: e263d42be6b93b829cfc1b1ec38c2d3e91ac9e51018ed1e89e3e26315f7b7530

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 9b540bde6a9b006dd1c8728a35fa95fd45a474dd62a7693fe0180e94ea2fcaf2

residual_unassessed

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: a972e19b6abffe34aa3358b73b44dbc3b03580099c2ca0915cd3e8ac3eb23fcc

Includes parameter and accuracy regimes not covered by the retained window or sufficient zero endpoint. Nearby source results require additional mapping.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 83337bb92a7c9d49f5544183f18df422f85312844275af9c58e57e0b8f1b2af3

D outside (E union H)

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: c112b040378c8f1bab31a38522e867c6356e79baf8235df095175640d783bd8d

Within D, first split E versus its complement, then H versus its complement. The four Boolean cells are disjoint and cover D. E denotes exactly 2 Lambda_Phi Delta<=epsilon^2; H is the unchanged symbolic frozen theorem-window predicate. No source constant is converted to a numerical transition, and E is only a sufficient zero-query condition.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: c14d385134a2ee96a41ef3e8c205978c219df30981c58cc9dea628c9393940d8

The entire domain is accounted for set-theoretically; the cell D outside (E union H) remains scientifically unassessed. Positive lower support on H outside E is also pending.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 6f3365d6ac2990c8b5901db3055f8eaabafb201840b841224909a5e89842c98b

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 6017f15203fb16ff7a696327907657b9358f22d158da3ca9db19958a551d4c05

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 572981f29ea36cdbccc450862fe775a6c8133de64a051c17a2d7355525172cdf

The proof BL_SPEC_joint_expected_cost__main__p_zero_query establishes the exact zero-query bound and gives a nonempty-class witness. A single shared algorithm solves the entire budget-indexed class, so this contradicts a uniform minimax lower bound, rather than merely displaying an easy individual instance. No replacement source guard is invented.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: e322498d3f9b5ca7b756ef907658474206fdcc5339d9dcfd2e81bc06016aeb08

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 61b68289279d9ffd6f8c840249e80a091e3dd739e5c67d7019247973bab94c62

fixed_curvature_transfer_correction

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 66d2cd06ecef081d1ed4ea41e3e0545f82d891e4ef4267ed505ede03fea96fb0

No lower-bound tightening is claimed. Scientific correction applies to the active b2 transfer and every former active reference.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 42c946dfe17695e52884e017769b965fd6e185131895bc537fe1d13d861d1186

The positive lower transfer is quarantined throughout H; exact zero remains on H intersect E and positive lower support is missing on H outside E.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 4aaa7322e176e46af19bbec014e154a522c4f00c1e2c7f66fa60fe9c3858abb0

Omega(kappa^2*L*Delta/epsilon^2+chi^2*kappa^8*sigma_g^2*L^3*Delta/epsilon^6) on all H, paired with O-tilde(U).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: c6cccb7cd16b2ac964867da535fc59966ed0963f52f02bf3add8e7d57e47a0e7

The source theorem's history and formula remain stored. The b1 upper statement on H is retained conditionally.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 08ce26ba02d4931834de7c70ccbf69d385b305243d7113323b49d155507d5704

The logical counterexample is on H intersect E; it disproves the recorded uniform statement on H.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 395671362c75d6d29425dea4e02931397cffc26d9a2b22f5ceaffa7c3f4f44be

Fix L=Delta=1,kappa=2,mu=1/2,theta=1,rho=1/2,chi=2,L_f=L_g=C_f=1,R0=0,sigma_f=0,sigma_g=1,Lambda_Phi=epsilon^2/4 and let epsilon->0. All sufficiently small epsilon satisfy H; all admissible instances are solved with zero calls although b2 is positive.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 2c31fa8beb4749762a0b582f5d23a23e5dc98aa28556319749b4dea6910bd2f5

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 869a3ecad933e96e24b0b935a14a922b14b2583d2bee277f16494903072504f0

No queries, inner solves, output certificates or source/oracle changes are required. Nonnegative cost supplies the matching lower side. The threshold is sufficient and includes equality, not claimed necessary.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 37cc3ecafa7a1918ef0c86f701efe2db210f0378cc073583118a5eede3428856

initial_point_zero_query

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: cd484085dc5a0e7385e7f3729b12672883cef3a0f8c258a4f2cc079a3d59f929

H intersect E: exact zero replaces the positive registered upper expression; E outside H: fills the previously unrepresented endpoint region.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: ddb8196ed4c48718aa81dc4d24ac1e4292db0871cb6b6fac73248f2373d751b5

Q*=0 on E; elsewhere the existing upper is retained only on H.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: d6e4561d5dee5c4f331c5a1fa002727d11daf4dc6228fee2daf8fc0e56219824

Only O-tilde(U) was registered on H; there was no endpoint comparison outside H. The registered positive lower transfer conflicts with part of E.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 467976f1a54b686407c18f9b8ef63983ad5c4e162667e17905dfd0283939fc98

D outside E: no new upper algorithm or lower rate is asserted. The invalid lower transfer is separately corrected.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 9c4b09aedb1d9aca503d0a9444b1143f4d93ebc516d1d6dd574fe9aeb4e21325

D and 2*Lambda_Phi*Delta <= epsilon^2, where D is the complete declared parameter/model domain

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: ce51f25e97ef899230dd1d0b19758aa0dd60d2b3d9aea651dcf678a6f2fc2304

Return the supplied x0. The descent inequality gives ||grad Phi(x0)||^2<=2 Lambda_Phi Delta<=epsilon^2.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: a35f34cc653834bff537617f0463d8fc2816447fe7fc268d0e12ac52bd05e139

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 9ef6d9c5d242016ac742fa9c09e631d055d4cf211188c35445e26097950f39bb

This auxiliary presentation finding records the first joint analysis without supplying source support for unchanged science or recertifying retained premises.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 3320f476416ea48b4d8e49ff91dbd704eacac39097901db5c1a2061447af9371

first_joint_synthesis

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 79f60c6158253c36d1e8ecf0bad4b613db14f88883f4d688a9d37514510f8f09

No independent scientific improvement is attributed to presentation.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: fa81fc8fd71e3c64b64b116e8aab69021148d0868dd1fbfe37f774032da09ad6

Explicit four-cell domain accounting, candidate dispositions, conditional retention of b1, independently justified correction of b2 and exact endpoint.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: f2022746ef68c66f7ef27e76c9405aaf6e47b57c68e297c0550df409be42a828

No frozen joint_analysis existed; the old comparison displayed the b1/b2 bracket on H.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 140a08ae784f63e71863ac6f778d74aff2a1103b25b3537e63c0a45a90946ec5

Every scientific edit is separately supported by fixed_curvature_transfer_correction or initial_point_zero_query.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 931e72431a7125980cb6bbd372f2a3f54e056e1a8a4d13e723b52ea730388a61

The entire frozen target D is accounted for, including explicitly unassessed cells.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 0c4ce6f80de5df2445cc87a092c7fda3ab0d81a3173076fd55eec34fe7ce5def

All four old/new mechanically compatible bound IDs have explicit dispositions in both affected syntheses.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 039bbafddb26eb74ca88a41af7411768e72d28185cbaf2e74a3d4e0d0edea036

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 2d07554438fd5eb14d146f1f8ee5997d4a022e3f37b5594967d86e2e6a1c4e4e

curated_feedback_BL_SPEC_joint_expected_cost_20261116

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

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 58f5ba8c843e35283e5a35a60b78b65b66926206d2d65f34863752563d27cebe

D: the frozen common specification and all native parameter domains, epsilon>0, L>=mu>0, L_g>=mu, L_f,C_f,rho,Delta,R0,sigma_f,sigma_g>=0, Lambda_Phi>0 with Lip(grad Phi)<=Lambda_Phi, kappa=L/mu, theta=rho/mu, chi=1+theta and the declared common-scale budget constraints. Dimensions are arbitrary positive finite integers and remain under the minimax supremum, not hidden in constants. Q*=inf_A sup_(I,O) E N_joint_sample subject to sup_(I,O) E||grad Phi(xhat)||<=epsilon, view main, guarantee g1, resource resource_559cd958ed. The dimension-free bounds are uniform across dimensions. The tracked list in q1 is not used to suppress dependence on other public budgets; all primitive budgets and derived relations above remain visible. Existing upper logarithms in initialization/accuracy are retained explicitly as logarithmic qualifications.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 3ae2951fea9a9ad90ee2af2cd839fd6940c6a0836c3527c679542dc662a87da8

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 64c430584a49810027a384411a63cd0a4627b8b250b1a9eabe3a75bc73c30f57

curated_feedback_BL_SPEC_joint_expected_cost_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 58f5ba8c843e35283e5a35a60b78b65b66926206d2d65f34863752563d27cebe

D: the frozen common specification and all native parameter domains, epsilon>0, L>=mu>0, L_g>=mu, L_f,C_f,rho,Delta,R0,sigma_f,sigma_g>=0, Lambda_Phi>0 with Lip(grad Phi)<=Lambda_Phi, kappa=L/mu, theta=rho/mu, chi=1+theta and the declared common-scale budget constraints. Dimensions are arbitrary positive finite integers and remain under the minimax supremum, not hidden in constants. Q*=inf_A sup_(I,O) E N_joint_sample subject to sup_(I,O) E||grad Phi(xhat)||<=epsilon, view main, guarantee g1, resource resource_559cd958ed. The dimension-free bounds are uniform across dimensions. The tracked list in q1 is not used to suppress dependence on other public budgets; all primitive budgets and derived relations above remain visible. Existing upper logarithms in initialization/accuracy are retained explicitly as logarithmic qualifications.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: 3bcdfe5f58aae4a21ab929e8a8a46d102c22be9cd3a4037109f8fe1dc3f8f464

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: e7bbd63259a61b623c9ac5b73fb22eb2fb08cb634fc10973ed54586543867e08

The frozen parameter at /parameters/14 has stable ID BL_SPEC_joint_expected_cost_p_5ffc729833; it is public, kind independent, has no dependencies, positive domain, and defines the Lipschitz upper bound for the reduced gradient on the declared full upper-level domain. A legal instance of the original native profile must satisfy its public parameter definitions/budgets as well as common_specification. Let C_old be that class for a fixed admissible public parameter tuple. Let P be exactly the displayed inequality in that parameter definition, quantified over all upper-level points. Hence C_old is a subset of P. The appended MODEL paragraph states P and its already-declared independent role, leaving every previous definition and condition in force; thus C_new=C_old intersect P=C_old. Conversely every new instance satisfies every old condition since none is removed or weakened. The instance/oracle-law map in either direction is the identity. It preserves dimensions, f and g, initialization and gap, norm bounds, lower-level curvature, noise/primitive budgets, output, probability/expectation quantifiers, and every charged gradient/Hessian/vector call. Therefore every unchanged native statement retains exactly its original applicability, conditional on the same accepted premises; no withdrawn lower bound is reinstated and no external theorem is recertified. Independence means Lambda_Phi is not silently replaced by a formula in primitive budgets. This proof does not assert that arbitrary contradictory budget tuples admit an instance; feasibility and all original compatibility conditions are unchanged. In particular any hard-family transfer had to satisfy the public Lambda_Phi promise before and after the prose clarification. This is equality of the already-defined classes, not adoption of a new smoothness hypothesis or a new complexity inequality.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: ef16e1a6dbdd42159b67465c2b83f53d5fc45ff57b78fecd4d58ea0e94679c5d

BL_SPEC_joint_expected_cost__finding__model_lambda_phi_identity_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: ccf76e922c7ac1ca94c8476acf306c2915c68c0d5e10b9d42198c669d694b4eb

No new rate, assumption, region or scientific inequality.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 5cf059fbb4a67e535d3d158fd10c460a0f3bd5d86bfff23acdde750cdbf23717

Identical mathematical and scientific payload; MODEL explicitly states the existing public parameter-14 promise.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: bb9b2dd8b774918ce23f1637972f4126da37d7e40b0d6dfc694616af7bed0020

All exact baseline native envelopes, guards, statuses and quarantines.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 840326a9238338c70c8819feb7a7cba2c5aa732fcfa2038d6afc32ef0c5d68ac

The complete previously admissible class and all original scientific records.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: 58f5ba8c843e35283e5a35a60b78b65b66926206d2d65f34863752563d27cebe

D: the frozen common specification and all native parameter domains, epsilon>0, L>=mu>0, L_g>=mu, L_f,C_f,rho,Delta,R0,sigma_f,sigma_g>=0, Lambda_Phi>0 with Lip(grad Phi)<=Lambda_Phi, kappa=L/mu, theta=rho/mu, chi=1+theta and the declared common-scale budget constraints. Dimensions are arbitrary positive finite integers and remain under the minimax supremum, not hidden in constants. Q*=inf_A sup_(I,O) E N_joint_sample subject to sup_(I,O) E||grad Phi(xhat)||<=epsilon, view main, guarantee g1, resource resource_559cd958ed. The dimension-free bounds are uniform across dimensions. The tracked list in q1 is not used to suppress dependence on other public budgets; all primitive budgets and derived relations above remain visible. Existing upper logarithms in initialization/accuracy are retained explicitly as logarithmic qualifications.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 02ca96c41c1a88fd7a04957b0f1ded1c40d6625e74cf7029f126d4840576caa4

The identity instance/oracle map in both directions, proved in BL_SPEC_joint_expected_cost__proof__model_lambda_phi_identity_20261116

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 36a7959efa24bf44c4683fa7d448b81181f53454c0fd98c1934f5dd9fdd17102

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: a20f576dabc41010e82c828b54e9986334734e278ca0fccff8e146ae94e88d16

Restore a positive lower bound only after independently verifying a hard-family mapping satisfying every public primitive budget and the independent Lambda_Phi budget; do not infer a sufficient guard merely by negating E.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: c7fded90be696fe8bdd2a6dfafe7c3771db94cecd78b191cebb475b253a9e7b1

Assess source arXiv:2610.03633v2 Corollary C.6 and Theorem C.5 for the accuracy-dependent small-gap slice, preserving its fixed multiplier, primitive-budget ratios, Lambda_Phi compatibility and source high-accuracy restrictions; no such bound is adopted here.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: e791f8c0b187550c6727bec79a76e00b3bf2603f9a308c5e79133ae4e3482daa

Read the remaining zero-variation branch in Section D of arXiv:2610.03633v2 and map the initialization/noise/dominance restrictions before any adoption.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 72637d133339608635afda450cef4b482f80accd97a68dda2b53cf958c755b29

Read primary theorems of arXiv:2610.03638v2 and arXiv:2610.01843v1 if pursuing the nearby main-rate routes; metadata alone does not settle fixed-budget versus expected-cost applicability or uniform structural dependence.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: e88a251e7db28f98adb3c93c7e1da546bce42a640b687a00dfbc6d19331127d9

Investigate the upper-level-noise lower route and any finite-dimensional saturation or guarantee-containment refinements outside this local correction; they are not certified absent.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 9d49713ac83c2cfb7267ea87b8ace5e469d74517fc65009f4ccc7e9f14b5b137

Assemble bounds on D outside (E union H); this complement is unassessed rather than a proved gap or open problem.

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native item 8

Native pointer: /joint_analysis/pending_obligations/7; canonical SHA-256: d25402e5c765c44bad065c04bd8c756b5c1af412d772f096ab7bcf7854fb9098

This explicitly authorized same-class MODEL prose authoring performs no new literature survey; all pre-existing scientific limitations remain.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 372ffca5e00f4042b0adb9abe553f66b597fa94472c55b4c3f577ca097a2fa3c

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: f370efc63ebaf8dfeadad31ae91902d55b82c4ca568a582fed88f0fe3b19a871

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 32eaa07a755bb491c3e652dd441382e86d21198560f26c8ca57ed164323fdfef

BL_SPEC_joint_expected_cost__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: d038832cef7e1a057ecbe46e44bbb9e6be7cc04b0f1fa19aae2aa9fef6f7ebcb

No change to the view, expected-norm guarantee, oracle, expected stopping-cost metric, quantity identity, primitive polynomial factors or historical statement.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 91542daa86919e0c75bde752fd3bce983dad5cd23dcfdd24efbf8a5296e6668e

The exact frozen applicability and logarithmic qualifications are retained conditionally, not freshly certified.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 92a797192bc150ddf1a7f9ff91d5509bddd3db50eddefd236720bba23b927ce6

Frozen /bounds/0, canonical hash 3475a98d4456f5428e4b601cf49e6134ff9c17bcb1762f9893a8aa18bcf64302; historical evidence e2 locates Theorem B.2, equations (41)-(43), arXiv:2610.03633v2.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 7c81411072d725b1d12d8ef0c421d21a4ec12be476cc003573821552e0d97a04

H only; scientifically selected on H outside E after the endpoint update.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 65c3ce57668ca62ad4b4cdc86e5c9ba0c782517711cabeec282cd03400db83a5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 5e5bb8095408578c1bbf27fa2c5d3468fbeaee3ab4f0219164445470b76d034f

BL_SPEC_joint_expected_cost__main__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 2a2f84227f0c3d41131056601abfe1acce686cf26e34353b4be3e99120242fad

The public x0 is an allowed unqueried output; its deterministic gradient norm is at most epsilon. Count 0 for all oracle laws, so worst-instance expected cost is 0.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 9dceec4943655e40efaed9e328fe97c2028cb7132cd1d64c162cf298c074d20b

D with lower-bounded Lambda_Phi-smooth reduced objective and gap at most Delta.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: d8a7ce7ca5c05915762a83fc9d927febf37fa12b9080553203ffea112c314934

Complete proof BL_SPEC_joint_expected_cost__main__p_zero_query from exact frozen baseline pointers and hashes recorded there.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: b927d68eb3e7d1c85fc288f97d4d08d3387e3c058e74e0eeda537a1eb51819f4

E, including equality, Delta=0 and every admissible finite dimension.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: c484b3dcb49393f76ec92d2cdff7c5f452e081800ed07e7dd03543b6377e483d

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 713f63d69b0f7adce84630c8c53066c5dd3998a068eafd0dd649c6bff2cf9f1c

BL_SPEC_joint_expected_cost__main__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: eda19fb4bbd1a90f41e208d90eb86a7b9b9c4477eb225b1ff62ca493ac69a1ab

Nonnegative expected cost lower-bounds Q* by 0 without a hard-family or oracle conversion.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: cf73fad22328ce3883c2bc052ab4c6f530352fb2b08717096a153194cc947ad1

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: a9e4b6ef5bbaa5a6419f6b0a4e41de97a8f2f6124956871363546aa643cef3e3

BL_SPEC_joint_expected_cost__main__p_zero_query

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 1b40ba2ba3e9e606db8125d709d7fa72268857bdd9c4e9d895d5936fec98043e

The declared nonnegative oracle-response count.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 9b8dd471fb3b239ca48060ccea47b796a8e1e67fe3e62b0fc24fb03fdf9468c8

Nonnegativity step of BL_SPEC_joint_expected_cost__main__p_zero_query.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: d8917d6ccafa7f915ed71cdf8494b5f94cfe3b64a1ab00f4a18ac91912dd58a3

E; adopted as the matching endpoint lower side.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 2e4cc019ca7cf59a83fcc1801eec0294fb32f34b38b9c71564d1888d6cb72ea4

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 9eb07d4834302fbbcbbc091f0a894547a5de908d329495fff44ce1eea660fc8c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: f73a7d84db516873ca10d5bffe5ab7ff354b9a6b33c98b5928c1a67850012441

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: a7eb8a80a41fe419b576ba46d583f28c0c9dbc3e7f82870be42fb3b1f209ae0f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 32eaa07a755bb491c3e652dd441382e86d21198560f26c8ca57ed164323fdfef

BL_SPEC_joint_expected_cost__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 5e5bb8095408578c1bbf27fa2c5d3468fbeaee3ab4f0219164445470b76d034f

BL_SPEC_joint_expected_cost__main__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 713f63d69b0f7adce84630c8c53066c5dd3998a068eafd0dd649c6bff2cf9f1c

BL_SPEC_joint_expected_cost__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: e322498d3f9b5ca7b756ef907658474206fdcc5339d9dcfd2e81bc06016aeb08

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: bb43e3ddecbf6690a9b4be3a1511b582c0a2a61cbb79f623535096a04d97d1dc

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: a7eb8a80a41fe419b576ba46d583f28c0c9dbc3e7f82870be42fb3b1f209ae0f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 32eaa07a755bb491c3e652dd441382e86d21198560f26c8ca57ed164323fdfef

BL_SPEC_joint_expected_cost__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 5e5bb8095408578c1bbf27fa2c5d3468fbeaee3ab4f0219164445470b76d034f

BL_SPEC_joint_expected_cost__main__b3

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 713f63d69b0f7adce84630c8c53066c5dd3998a068eafd0dd649c6bff2cf9f1c

BL_SPEC_joint_expected_cost__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: c2fae5c3e77d355b847e3b46b5c6fba1a15b537601f4f646168a5ceebcc86dd5

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: e96a17e79ac2060c1d08c453267cc28111c32f09042edd1463853c1912646486

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: a20f576dabc41010e82c828b54e9986334734e278ca0fccff8e146ae94e88d16

Restore a positive lower bound only after independently verifying a hard-family mapping satisfying every public primitive budget and the independent Lambda_Phi budget; do not infer a sufficient guard merely by negating E.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 9a5f6ec44f1da738c3aa81053a40ba38273ba56aad6bebee8763703f02fc8a72

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: c7fded90be696fe8bdd2a6dfafe7c3771db94cecd78b191cebb475b253a9e7b1

Assess source arXiv:2610.03633v2 Corollary C.6 and Theorem C.5 for the accuracy-dependent small-gap slice, preserving its fixed multiplier, primitive-budget ratios, Lambda_Phi compatibility and source high-accuracy restrictions; no such bound is adopted here.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 7c2a507fcffaf7b8d65b6963fe2201bbb176569ffaa66d3ecc331de09c08f50a

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: e791f8c0b187550c6727bec79a76e00b3bf2603f9a308c5e79133ae4e3482daa

Read the remaining zero-variation branch in Section D of arXiv:2610.03633v2 and map the initialization/noise/dominance restrictions before any adoption.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 446fddcdc55cbf4330ab20ce1e2c581844dd9766bad3ffb133e37101ded6ef43

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 72637d133339608635afda450cef4b482f80accd97a68dda2b53cf958c755b29

Read primary theorems of arXiv:2610.03638v2 and arXiv:2610.01843v1 if pursuing the nearby main-rate routes; metadata alone does not settle fixed-budget versus expected-cost applicability or uniform structural dependence.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: dcbc9d2cbb45558d46d66bc91e2de7f3e292cc8a596f441f2c5da8f7af2a35af

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: e88a251e7db28f98adb3c93c7e1da546bce42a640b687a00dfbc6d19331127d9

Investigate the upper-level-noise lower route and any finite-dimensional saturation or guarantee-containment refinements outside this local correction; they are not certified absent.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: 4421ec63e4f22391a9a7c84a43c406a8ee2d34b111c05ee3442210a3d7809139

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 816e64d45ab01655b0cdb3174cc88338b9552319d4504b2ed46ed2504883fbc8

retained-material-lead-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 9d49713ac83c2cfb7267ea87b8ace5e469d74517fc65009f4ccc7e9f14b5b137

Assemble bounds on D outside (E union H); this complement is unassessed rather than a proved gap or open problem.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 43c71ea1c960d5678232137b375a278246c4c647c267777b85884f299d90846a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: 3a5596f47228cee2df693dc42e3187d81a385b398cb9929ba8882d9d426ace9a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: f42a165a1243769bae88f121be3fc4c02d6cb5d8c418c6d410330027a3a05336

No new research or theorem certification is claimed by this authoring operation.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 029f069670404c8e6fa9e49c13ff64e0304d42527d302fc25918c4c39876d481

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: b143dc3e4f3dc1eda63e4a2c5e1c9e96844c471102339836f920f3701a88f455

BL_SPEC_joint_expected_cost__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 936fbae03363b2a220ee35ad1111289d232a8c4d1ab813d98e9e8f45210bda61

BL_SPEC_joint_expected_cost__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: d1a6ba9b8e2cb3d89d251f0a1e3ca18c2811c896452bd7e06555741fcb35bf15

model-prose-finite-scope

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: d25402e5c765c44bad065c04bd8c756b5c1af412d772f096ab7bcf7854fb9098

This explicitly authorized same-class MODEL prose authoring performs no new literature survey; all pre-existing scientific limitations remain.

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

Native pointer: /joint_analysis/target; canonical SHA-256: 6538a68fc087c7a1071a6027136285efb0edc7fc4027da64dc28ee6123ae38be

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: f04cc07d3ec18cebcc80a4bdb252862a7679d7785d60363d90b2d392f7b39099

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

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 58f5ba8c843e35283e5a35a60b78b65b66926206d2d65f34863752563d27cebe

D: the frozen common specification and all native parameter domains, epsilon>0, L>=mu>0, L_g>=mu, L_f,C_f,rho,Delta,R0,sigma_f,sigma_g>=0, Lambda_Phi>0 with Lip(grad Phi)<=Lambda_Phi, kappa=L/mu, theta=rho/mu, chi=1+theta and the declared common-scale budget constraints. Dimensions are arbitrary positive finite integers and remain under the minimax supremum, not hidden in constants. Q*=inf_A sup_(I,O) E N_joint_sample subject to sup_(I,O) E||grad Phi(xhat)||<=epsilon, view main, guarantee g1, resource resource_559cd958ed. The dimension-free bounds are uniform across dimensions. The tracked list in q1 is not used to suppress dependence on other public budgets; all primitive budgets and derived relations above remain visible. Existing upper logarithms in initialization/accuracy are retained explicitly as logarithmic qualifications.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 09b5db513c75dafaeafc91b20b229a344c0b6a84a9d87c5b1231dfffe4d872e8

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 62b84edcbaf6d11cb01da00fc2034884f205b1c056e3824f1a23c4d2e1beea6f

BL_SPEC_joint_expected_cost_p_0d1c5067b5

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 8e5f1b3fc6aa9e24cf1a791bd988b39f2832c8fd1302500a69229a01caa78ed8

BL_SPEC_joint_expected_cost_p_eb3546e82c

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 98052bdf00117818069da4e54908c109e3c75ad3f5bbe2bc1c9eafd1faa9361e

BL_SPEC_joint_expected_cost_p_1cc24df773

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: b75377a8b2b8ca078b6876bb0999fb158cf48d202aa1fb5a96a43bd62e1914e7

BL_SPEC_joint_expected_cost_p_256ee43d4f

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: d12efcbf9e8d431283f73fc82cee54cec0f845ba33bb051a11e58c47c430dfc3

BL_SPEC_joint_expected_cost_p_4e3f70b140

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: 72a15a9e50588ab80028e00e029fd8e92866980d365482e4fda7efd8a6906341

BL_SPEC_joint_expected_cost_p_efcabfd5ff

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: b063ea127ca0e8cb3eecfbb35fde2628cf76e54c6636672bc47b00d2fe4c7005

BL_SPEC_joint_expected_cost_p_850094ef78

#### Native item 8

Native pointer: /joint_analysis/target/joint_variables/7; canonical SHA-256: c51edaf441dec5d639d48164db9eac8f57292b0981fd597e32ba83f16f6b4894

BL_SPEC_joint_expected_cost_p_25c351f23c

#### Native item 9

Native pointer: /joint_analysis/target/joint_variables/8; canonical SHA-256: cfdb094375bddaef1ad66f985409e1551a6a4b4a7d7de537c578b9bfaa620771

BL_SPEC_joint_expected_cost_p_d1944ba8d6

#### Native item 10

Native pointer: /joint_analysis/target/joint_variables/9; canonical SHA-256: dfc65cf7c5f19a21fff71f80793743d38a5e433f159679fbd4e6d02f5ddb85c9

BL_SPEC_joint_expected_cost_p_37583d6939

#### Native item 11

Native pointer: /joint_analysis/target/joint_variables/10; canonical SHA-256: 4c37a0c611be4a5dcdf140b771500af7a456b9ccafdec2495b360e2fae2c5d0a

BL_SPEC_joint_expected_cost_p_4ec23e4709

#### Native item 12

Native pointer: /joint_analysis/target/joint_variables/11; canonical SHA-256: 8bee0d64a1f27eb2d1602857b7a6a82c649e5853a8f03afc64169bc0b3ef71b4

BL_SPEC_joint_expected_cost_p_6f321ee5c4

#### Native item 13

Native pointer: /joint_analysis/target/joint_variables/12; canonical SHA-256: 9a6660f40156809c755d8536ceb7328fb89687cf3e61434ebc039c5b244d1910

BL_SPEC_joint_expected_cost_p_5ffc729833

#### Native item 14

Native pointer: /joint_analysis/target/joint_variables/13; canonical SHA-256: 8bedb2fc40c87837135e13024e3884dfc53e9ab6450e0d838a034e2140ccb947

BL_SPEC_joint_expected_cost_p_a17bdd1bfb

#### Native item 15

Native pointer: /joint_analysis/target/joint_variables/14; canonical SHA-256: cd8c4b47ffa7965164e6a78e1901af101a57e719c701091230c39f127f683f9f

BL_SPEC_joint_expected_cost_p_9d0f22c488

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: c3d4abd6a1d0995789a4edab6908080b9dc0b7bb42e49e59251bbc91bd5c21af

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 70a10cf3bc4b702c08cadcaf1dce3c290812babd4b6c6c5fc27f6eef2dba3bd7

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: ec3f496647ee1a4c6a32c54ee7caa22aa5f2b8b960d73918ede01eb035e353fe

L_g/mu; an algebraic abbreviation, with no change of the native parameter identities or the accuracy scale.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 415313832f67840ad5862c931ae0501511c49776d38c36c8c7db3574f009a259

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: d12efcbf9e8d431283f73fc82cee54cec0f845ba33bb051a11e58c47c430dfc3

BL_SPEC_joint_expected_cost_p_4e3f70b140

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 72a15a9e50588ab80028e00e029fd8e92866980d365482e4fda7efd8a6906341

BL_SPEC_joint_expected_cost_p_efcabfd5ff

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 37664d5895f78758ec8e94e440b30c9a2cfc68873c28306301b40d6a2f3fefa3

k

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1; canonical SHA-256: 0b66be84e44608d593877a3929708f691af502b2988a26c25431dd379f2465a0

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/1/expression; canonical SHA-256: f6241de656485b005208d8163ae4153f5bc8efa7700c1967514323f7f3b28244

(1+L_g/mu)*rho*C_f^2/(2*mu^2); the source bias coefficient, an algebraic abbreviation with its full dimensional scale retained.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs; canonical SHA-256: c705fd4a0224089e4169ac4c953ffa86b90f1b8b869809a1531f83ecf3ef378c

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/0; canonical SHA-256: d12efcbf9e8d431283f73fc82cee54cec0f845ba33bb051a11e58c47c430dfc3

BL_SPEC_joint_expected_cost_p_4e3f70b140

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/1; canonical SHA-256: 72a15a9e50588ab80028e00e029fd8e92866980d365482e4fda7efd8a6906341

BL_SPEC_joint_expected_cost_p_efcabfd5ff

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/2; canonical SHA-256: b063ea127ca0e8cb3eecfbb35fde2628cf76e54c6636672bc47b00d2fe4c7005

BL_SPEC_joint_expected_cost_p_850094ef78

#### Native item 4

Native pointer: /joint_analysis/target/normalized_variables/1/parameter_refs/3; canonical SHA-256: 8e5f1b3fc6aa9e24cf1a791bd988b39f2832c8fd1302500a69229a01caa78ed8

BL_SPEC_joint_expected_cost_p_eb3546e82c

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/1/symbol; canonical SHA-256: 44a58cbf1edfbcfe49d345e8d31d923ca570efe5c979a068120113466cdf9af6

E_rho

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: b06dcc8b7579d1f90f83eb02aeceee24a8c1d0d9f242ca8a783dea5d41d39cf5

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 62b84edcbaf6d11cb01da00fc2034884f205b1c056e3824f1a23c4d2e1beea6f

BL_SPEC_joint_expected_cost_p_0d1c5067b5

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 49775c02e02db09c140fa2bc2647e97f195d06040d699395ad527d81b1e3f88a

BL_SPEC_joint_expected_cost_p_a136776370

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 9381083e1a51ef433255f557d03b88b5353c6e6cba48ea892a509608f38739f5

BL_SPEC_joint_expected_cost_p_dc5f6d3bad

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 8e5f1b3fc6aa9e24cf1a791bd988b39f2832c8fd1302500a69229a01caa78ed8

BL_SPEC_joint_expected_cost_p_eb3546e82c

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 98052bdf00117818069da4e54908c109e3c75ad3f5bbe2bc1c9eafd1faa9361e

BL_SPEC_joint_expected_cost_p_1cc24df773

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: b75377a8b2b8ca078b6876bb0999fb158cf48d202aa1fb5a96a43bd62e1914e7

BL_SPEC_joint_expected_cost_p_256ee43d4f

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: d12efcbf9e8d431283f73fc82cee54cec0f845ba33bb051a11e58c47c430dfc3

BL_SPEC_joint_expected_cost_p_4e3f70b140

#### Native item 8

Native pointer: /joint_analysis/target/uniform_in/7; canonical SHA-256: 72a15a9e50588ab80028e00e029fd8e92866980d365482e4fda7efd8a6906341

BL_SPEC_joint_expected_cost_p_efcabfd5ff

#### Native item 9

Native pointer: /joint_analysis/target/uniform_in/8; canonical SHA-256: b063ea127ca0e8cb3eecfbb35fde2628cf76e54c6636672bc47b00d2fe4c7005

BL_SPEC_joint_expected_cost_p_850094ef78

#### Native item 10

Native pointer: /joint_analysis/target/uniform_in/9; canonical SHA-256: c51edaf441dec5d639d48164db9eac8f57292b0981fd597e32ba83f16f6b4894

BL_SPEC_joint_expected_cost_p_25c351f23c

#### Native item 11

Native pointer: /joint_analysis/target/uniform_in/10; canonical SHA-256: cfdb094375bddaef1ad66f985409e1551a6a4b4a7d7de537c578b9bfaa620771

BL_SPEC_joint_expected_cost_p_d1944ba8d6

#### Native item 12

Native pointer: /joint_analysis/target/uniform_in/11; canonical SHA-256: dfc65cf7c5f19a21fff71f80793743d38a5e433f159679fbd4e6d02f5ddb85c9

BL_SPEC_joint_expected_cost_p_37583d6939

#### Native item 13

Native pointer: /joint_analysis/target/uniform_in/12; canonical SHA-256: 4c37a0c611be4a5dcdf140b771500af7a456b9ccafdec2495b360e2fae2c5d0a

BL_SPEC_joint_expected_cost_p_4ec23e4709

#### Native item 14

Native pointer: /joint_analysis/target/uniform_in/13; canonical SHA-256: 8bee0d64a1f27eb2d1602857b7a6a82c649e5853a8f03afc64169bc0b3ef71b4

BL_SPEC_joint_expected_cost_p_6f321ee5c4

#### Native item 15

Native pointer: /joint_analysis/target/uniform_in/14; canonical SHA-256: 9a6660f40156809c755d8536ceb7328fb89687cf3e61434ebc039c5b244d1910

BL_SPEC_joint_expected_cost_p_5ffc729833

#### Native item 16

Native pointer: /joint_analysis/target/uniform_in/15; canonical SHA-256: 8bedb2fc40c87837135e13024e3884dfc53e9ab6450e0d838a034e2140ccb947

BL_SPEC_joint_expected_cost_p_a17bdd1bfb

#### Native item 17

Native pointer: /joint_analysis/target/uniform_in/16; canonical SHA-256: cd8c4b47ffa7965164e6a78e1901af101a57e719c701091230c39f127f683f9f

BL_SPEC_joint_expected_cost_p_9d0f22c488

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Closing the Accuracy Gap in Stochastic First-Order Bilevel Optimization. 2026. arXiv:2610.03633v2, 2026-10-19.

https://arxiv.org/pdf/2610.03633v2
