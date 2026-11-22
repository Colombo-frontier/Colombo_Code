# Fresh joint gradients: joint parameter dependence and expected query complexity

**Setting ID.** `BL_SPEC_joint_expected_cost`

Bilevel optimization

Fresh joint-gradient bilevel optimization with independent reduced smoothness. The effective-curvature zero region is exact; a proved source-compatible subregion restores the A.6 lower and contains an explicit noise-dominated near-optimal branch. Outside those subregions a positive lower remains unestablished.

**Status.** Other quantified gap present; Bounds missing

**Gap classes present.** Other quantified gap; Logarithmic gap

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

The derived quantity $B_\Phi=(1+L_g/\mu)^2(L_f+\rho C_f/\mu)$ is always a valid smoothness bound. Algorithms may use $\bar\Lambda_\Phi=\min\{\Lambda_\Phi,B_\Phi\}$. This does not replace or constrain the independent model input $\Lambda_\Phi$.

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

**Effective curvature.** $k=L_g/\mu$, $B_\Phi=(1+k)^2(L_f+\rho C_f/\mu)$ and $\bar\Lambda_\Phi=\min\{\Lambda_\Phi,B_\Phi\}$. The independent public $\Lambda_\Phi$ promise remains part of the model.

**Source-transfer window S.** $L_f=L_g=C_f=L>0$, $0<\Delta\le L$, $\kappa=L/\mu\ge C_s$, $C_s\le\theta=\rho/\mu\le c_s\kappa$, $0<\varepsilon\le c_s\min\{L,\kappa\sqrt{L\Delta}\}$, $\Lambda_\Phi\ge B_\Phi$, $R_0,\sigma_f,\sigma_g\ge0$. Here $c_s>0$ is a sufficiently small and $C_s>0$ a sufficiently large universal constant fixed by the normalization proof. Let $T_0=\kappa^2L\Delta/\varepsilon^2$, $K_0=T_0(1+\theta^2\kappa^6\sigma_g^2L^2/\varepsilon^4)$, $D_0=\lceil C_d(1+K_0)(1+T_0)\theta^2\log(2+K_0T_0)\rceil$ for a sufficiently large universal $C_d$. Require $d_x\ge D_0$ and $d_y\ge D_0+2$, or take the stated worst case over arbitrary finite dimensions.

**Matching subwindow N.** The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

**Cost convention.** The adopted source lower concerns worst-instance expected stopping cost for the bundled fresh first-order response. No fixed-budget conversion is being assumed.

Historical audit note: BL_SPEC_joint_expected_cost__main__p_zero_query retains its eight original premise hashes. Its exact predecessor premise snapshot has not been recovered; seven hashes differ from the current fields and four already differed in the first-observed 996c941 profile. It is ineligible for current bounds. The active effective-curvature zero-query proof is BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122; the new guarded lower has its own independent proof.

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

$k$: Primitive lower-gradient condition bound **Domain:** Real number at least one.

$k=L_g/\mu$

$B_\Phi$: A derived valid global reduced-gradient Lipschitz bound; not a new model promise **Domain:** Nonnegative real number.

$B_\Phi=(1+k)^2(L_f+\rho C_f/\mu)$

$\bar\Lambda_\Phi$: Effective smoothness usable by an algorithm while preserving the independent Lambda_Phi input **Domain:** Nonnegative real number.

$\bar\Lambda_\Phi=\min\{\Lambda_\Phi,B_\Phi\}$

$E_\rho$: Coefficient of the frozen-linear-tilt bias **Domain:** Nonnegative real number.

$E_\rho=(1+k)\rho C_f^2/(2\mu^2)$

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}\mathbb E C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\mathrm{joint}}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Zero queries from the effective smoothness bound

**Region.** All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Gap or comparison.** Exact zero; no multiplicative ratio.

**Comparison argument.** Complete effective-curvature proof; nonnegative expected query cost.

### R2 - Source-compatible window outside the matching branch

**Region.** The complete S predicate and not the complete N predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Other quantified gap

**Lower bound.** B6

$$
\Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)
$$

**Upper bound.** B5

$$
\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)
$$

**Gap or comparison.** The upper/lower ratio is the displayed U divided by the displayed positive L, up to the source logarithms. No matching dependence on arbitrary sigma_f or theta is asserted.

**Comparison argument.** Source theorem plus complete normalized transfer; all parameter dependence stays explicit.

### R3 - N: bounded variation and a noise-dominated matching branch

**Region.** The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})
$$

**Upper bound.** B7

$$
\widetilde O(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})
$$

**Gap or comparison.** Only the source upper logarithms remain; accuracy, condition-number, lower-noise and gap powers match on N.

**Comparison argument.** Complete dominance calculation; theta is bounded by fixed universal constants.

### R4 - Remaining independently curved parameter class

**Region.** All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B5

$$
\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)
$$

**Gap or comparison.** A target-compatible positive lower is missing outside E and S.

**Comparison argument.** B.2 supplies an upper bound throughout this remainder. Neither the quarantined b2 nor the new S-only lower is used here.

## 4. Bounds and supporting evidence

### B1 - frozen-tilt estimator and descent

**Admission.** Eligible evidence; not selected in the displayed bracket

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

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) theorem: Theorem B.2; section: Appendix B.2; pdf pages: 18; 19; printed pages: 18; 19; equations: (41); (42)

Theorem B.2 requires Assumption 3.1, a finite initialization certificate and any valid reduced smoothness bound; it is not restricted to the lower-bound window H.

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

**Conditions.** All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.** 0

**Constants.** Exact zero; no hidden constants.

**Derivation.** {'evidence_basis': 'analyst_derivation', 'proof_refs': ['BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122']}

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122; theorem: Global reduced smoothness and a redundant-budget transfer

Analyst-derived argument is kept separate from published/preprint evidence.

### B4 - Resource nonnegativity

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**declared scalar projection.** 0

**Constants.** Exact zero; no hidden constants.

**Derivation.** {'evidence_basis': 'analyst_derivation', 'proof_refs': ['BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122']}

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122; theorem: Global reduced smoothness and a redundant-budget transfer

Analyst-derived argument is kept separate from published/preprint evidence.

### B5 - Frozen-tilt method with effective curvature

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Conditions.** Assumption 3.1 and finite initialization; outside the effective zero region barLambda_Phi>0.

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Logarithmic factors.** The accuracy and initialization logarithms in source Theorem B.2 are retained.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122; theorem: Global reduced smoothness and a redundant-budget transfer

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) theorem: Theorem B.2; section: Appendix B.2; pdf pages: 18; 19; printed pages: 18; 19; equations: (41); (42)

Theorem B.2 requires Assumption 3.1, a finite initialization certificate and any valid reduced smoothness bound; it is not restricted to the lower-bound window H.

### B6 - Theorem A.6 under the proved normalized guard

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Conditions.** $L_f=L_g=C_f=L>0$, $0<\Delta\le L$, $\kappa=L/\mu\ge C_s$, $C_s\le\theta=\rho/\mu\le c_s\kappa$, $0<\varepsilon\le c_s\min\{L,\kappa\sqrt{L\Delta}\}$, $\Lambda_\Phi\ge B_\Phi$, $R_0,\sigma_f,\sigma_g\ge0$. Here $c_s>0$ is a sufficiently small and $C_s>0$ a sufficiently large universal constant fixed by the normalization proof. Let $T_0=\kappa^2L\Delta/\varepsilon^2$, $K_0=T_0(1+\theta^2\kappa^6\sigma_g^2L^2/\varepsilon^4)$, $D_0=\lceil C_d(1+K_0)(1+T_0)\theta^2\log(2+K_0T_0)\rceil$ for a sufficiently large universal $C_d$. Require $d_x\ge D_0$ and $d_y\ge D_0+2$, or take the stated worst case over arbitrary finite dimensions.

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122; theorem: A sufficient normalized guard for Theorem A.6

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) equations: (30); (31); pdf pages: 16; section: Appendix A; theorem: Theorem A.6

### B7 - Frozen-tilt upper bound on N

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\widetilde O(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Conditions.** The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122, BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122; theorem: Comparison on the bounded-variation noise branch

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122; theorem: Global reduced smoothness and a redundant-budget transfer

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) theorem: Theorem B.2; section: Appendix B.2; pdf pages: 18; 19; printed pages: 18; 19; equations: (41); (42)

Theorem B.2 requires Assumption 3.1, a finite initialization certificate and any valid reduced smoothness bound; it is not restricted to the lower-bound window H.

### B8 - Guarded A.6 lower restricted to N

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Conditions.** The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122, BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122; theorem: Comparison on the bounded-variation noise branch

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122; theorem: A sufficient normalized guard for Theorem A.6

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) equations: (30); (31); pdf pages: 16; section: Appendix A; theorem: Theorem A.6

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 44fff7d4e897fdde6c27a13bc0ebbda5e82ec19dbe2bcd1fa4df88f629706653

### Native proof: BL_SPEC_joint_expected_cost__main__p_zero_query

Native pointer: /proofs/0; canonical SHA-256: b3d937fd6594d7f147ff4fdda32d744963f3b9618a994cfcefa6cb06785006fb

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

#### Native field: lifecycle

Native pointer: /proofs/0/lifecycle; canonical SHA-256: 566fa22ae9c73735b1bce7381314da1c11411bc13a2de43b97ac8c1ae72ae102

#### Native field: state

Native pointer: /proofs/0/lifecycle/state; canonical SHA-256: 1e573cd09004872234c556146aab838ddb563a9476581b94921aae207b306203

historical

#### Native field: eligible_for_current_bounds

Native pointer: /proofs/0/lifecycle/eligible_for_current_bounds; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: premise_binding

Native pointer: /proofs/0/lifecycle/premise_binding; canonical SHA-256: 0d336514218b13b6a43bc512d674a9be5a082badb3c8fd48bc57b9b0fce34d53

#### Native field: mode

Native pointer: /proofs/0/lifecycle/premise_binding/mode; canonical SHA-256: f381f36dd47fc3a354dbd3b788b7918c8e82c6dc210d3135f1850692475ccba3

historical_unresolved

#### Native field: verification_status

Native pointer: /proofs/0/lifecycle/premise_binding/verification_status; canonical SHA-256: e349b8ef487eaef6ceaf2efd8d99b5746b4bca5809cc23df2870e65c6f816cad

unresolved_snapshot

#### Native field: first_observed

Native pointer: /proofs/0/lifecycle/premise_binding/first_observed; canonical SHA-256: 086f09b3eda693e4836a33f229d8fcd71369e0b598f68a65c33faa32a2f0da45

#### Native field: git_commit

Native pointer: /proofs/0/lifecycle/premise_binding/first_observed/git_commit; canonical SHA-256: 27d7234fdf542252d893c65fa7c58f39f3e15c475ce0a958d67bead1791b8747

996c941748d9d2c998dfeadba41766d463357b1d

#### Native field: profile_sha256

Native pointer: /proofs/0/lifecycle/premise_binding/first_observed/profile_sha256; canonical SHA-256: a8af4286457b0d3f1bc5bf567c347bf31efbd6d47d1132db52a45f84482009ed

e7d304cc4e6f3035a9c31d64e8a4957d693bb7b502e107c35faf6f699f207d85

#### Native field: note

Native pointer: /proofs/0/lifecycle/premise_binding/note; canonical SHA-256: c02b900be06ade143f71ef6de51c955fdf28b09801922fe92817ca35da2cec00

The eight original premise hashes are frozen audit claims, not current-field bindings. Seven differ from the current profile; four already differ in the cited first-observed profile. That profile is evidence of the record, not a recovered premise snapshot. The exact predecessor snapshot is unresolved; no hashes were refreshed and no historical proof certification is claimed.

#### Native field: matched_first_observed_pointers

Native pointer: /proofs/0/lifecycle/premise_binding/matched_first_observed_pointers; canonical SHA-256: 14fe47571a6451eb23a88b273943c893323c594787272dc177e08041be41a4f0

#### Native item 1

Native pointer: /proofs/0/lifecycle/premise_binding/matched_first_observed_pointers/0; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 2

Native pointer: /proofs/0/lifecycle/premise_binding/matched_first_observed_pointers/1; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 3

Native pointer: /proofs/0/lifecycle/premise_binding/matched_first_observed_pointers/2; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 4

Native pointer: /proofs/0/lifecycle/premise_binding/matched_first_observed_pointers/3; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: unresolved_first_observed_pointers

Native pointer: /proofs/0/lifecycle/premise_binding/unresolved_first_observed_pointers; canonical SHA-256: 2a31f899bf96a274bd7c79bfba4c340ff18901c1fe04c212a584d7578687e82c

#### Native item 1

Native pointer: /proofs/0/lifecycle/premise_binding/unresolved_first_observed_pointers/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /proofs/0/lifecycle/premise_binding/unresolved_first_observed_pointers/1; canonical SHA-256: d6039afddf27bddb8de5dba6560d032afc09d8a78c6a685d9519ce1cea90d703

/bounds/1

#### Native item 3

Native pointer: /proofs/0/lifecycle/premise_binding/unresolved_first_observed_pointers/2; canonical SHA-256: 093a9ad2f779c83c2483d0b2930a00cfedd078d5514a96b1e08bc8c92c96a35b

/comparisons/0

#### Native item 4

Native pointer: /proofs/0/lifecycle/premise_binding/unresolved_first_observed_pointers/3; canonical SHA-256: 0f08bfcf119ae0e9a290ad2d12da66c4f20c5c71100f28c664e523ab0cd3b9d9

/regimes

#### Native field: superseded_by

Native pointer: /proofs/0/lifecycle/superseded_by; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /proofs/0/lifecycle/superseded_by/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /proofs/0/lifecycle/reason; canonical SHA-256: 773ab05bbbdc7727412a106ce85b543c5302d1850f95606bc85c9d3cce4ea674

Historical audit of the former independent-curvature zero region and invalid overbroad lower transfer; current endpoint support uses the separately proved effective-curvature result.

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

### Native proof: BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

Native pointer: /proofs/3; canonical SHA-256: a97473908161d2b020e61d532c786afd3d0aa38adb9097c9616c8d2929309a67

#### Native field: kind

Native pointer: /proofs/3/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/3/title; canonical SHA-256: 1092b11fb61d0734a071ca6c2a99bd816644ad5d9c9209234dcdf1f56b5ab091

Global reduced smoothness and a redundant-budget transfer

#### Native field: statement

Native pointer: /proofs/3/statement; canonical SHA-256: efaadcfe6ccca4f4455072767093a0e7381c22bba9bacf7bf83ebf5b91ebefc2

Lip(grad Phi)<=B_Phi; the independent Lambda_Phi promise is redundant when Lambda_Phi>=B_Phi. Effective curvature is min(Lambda_Phi,B_Phi).

#### Native field: proof

Native pointer: /proofs/3/proof; canonical SHA-256: ffc8811702012eaca5ff283180bb1aced87ee7d1a7017eb0ebd6563ce927e269

Write z=(x,y*(x)) and z'=(x',y*(x')). Strong convexity and the L_g-Lipschitz full gradient imply ||y*(x)-y*(x')||<=k||x-x'||, hence ||z-z'||<=sqrt(1+k^2)||x-x'||. Put B=g_xy, H=g_yy, u=f_x and a=f_y at z, with primed symbols at z'. The model gives ||B||,||B'||<=L_g, ||H^{-1}||,||H'^{-1}||<=1/mu, ||a||,||a'||<=C_f, and ||H^{-1}-H'^{-1}||<=rho||z-z'||/mu^2. Using grad Phi=u-BH^{-1}a and adding/subtracting terms yields
||grad Phi(x)-grad Phi(x')|| <= [(1+k)L_f+(1+k)rho C_f/mu] ||z-z'|| <= (1+k)^2(L_f+rho C_f/mu)||x-x'||.
This is a whole-class bound, with no assumption on g_xx variation. Consequently, for fixed primitive budgets, initialization, dimensions, oracle laws and guarantees, the class with Lambda_Phi>=B_Phi is exactly the class before imposing the Lambda_Phi promise. The identity map preserves every query and expected stopping cost. A source hard family already satisfying the primitive budgets therefore also satisfies this independent promise. Merely excluding 2 Lambda_Phi Delta<=epsilon^2 would not prove this transfer. For every budget tuple the same derivation and the independent promise imply the usable bound barLambda=min(Lambda_Phi,B_Phi). If barLambda=0, grad Phi is constant; finite inf Phi on the full Euclidean space forces grad Phi=0. Otherwise the descent inequality gives ||grad Phi(x0)||^2<=2 barLambda Delta. Thus returning x0 costs zero whenever 2 barLambda Delta<=epsilon^2, including equality and Delta=0. Outside this region barLambda>0, so Theorem B.2 may be run with barLambda as its public valid bound. This improves its displayed polynomial factor without modifying the model.

#### Native field: source_refs

Native pointer: /proofs/3/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /proofs/3/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: evidence_refs

Native pointer: /proofs/3/evidence_refs; canonical SHA-256: 49ec1b65739bd2251401ba42f00dd82d9a09db228770205b15cd35e1f6b8325f

#### Native item 1

Native pointer: /proofs/3/evidence_refs/0; canonical SHA-256: 026ea3e58189207ae8c3f9960312af72f71682c03385890c7f91fa87a3865f92

BL_SPEC_joint_expected_cost__main__e_universal_curvature_20261122

#### Native field: verification_scope

Native pointer: /proofs/3/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

Native pointer: /proofs/4; canonical SHA-256: 5840768135d8ac298305837e2a9781ca0807124003979686792f96431f2e37bf

#### Native field: kind

Native pointer: /proofs/4/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 7959980b22b72a47328bd2e1665460434ba3948a40b839bd9bc141209526292a

A sufficient normalized guard for Theorem A.6

#### Native field: statement

Native pointer: /proofs/4/statement; canonical SHA-256: 4ade97fbf0357a6309b897b2a52da57672fa1a1ddff39e9a3232d11389f99424

On S, the source Theorem A.6 gives Omega(kappa^2 L Delta epsilon^-2 + theta^2 kappa^8 sigma_g^2 L^3 Delta epsilon^-6) for the exact target expected-cost quantity.

#### Native field: proof

Native pointer: /proofs/4/proof; canonical SHA-256: 0a23e864b5fc1b922708fdcc975547f74bce2d155342e3241f5fd4768b4a60d9

Use the source Theorems A.4 and A.6, equations (14), (20)--(23), (29)--(31), as cited preprint premises. Let C_A bound their fixed global-regularity constants. Choose a fixed a>0 so small that C_A(a+sqrt(a))<=1 and C_A a<=1. Use internal scale ell=aL and internal lower curvature mu_int=2mu. Choose a fixed b>0 with 2 C_A b<=1 and set vartheta_int=b theta. Choose universal C_s large and c_s small so that kappa_int=ell/mu_int=a kappa/2>=2, 1<=vartheta_int<=kappa_int, beta vartheta_int lies in A.4's small window, and the target accuracy window implies A.6's internal one. Such choices are possible, for example by enforcing C_s>=max(4/a,1/b) and c_s below the finite source constants times a^(3/2) and a/b.
A.4 gives strong convexity at least mu_int/2=mu, first-order Lipschitz budgets at most C_A ell<=L, and Hessian variation at most C_A mu_int vartheta_int<=rho. Its full upper-gradient bound is C_A(ell+sqrt(ell Delta))<=C_A(a+sqrt(a))L<=C_f because Delta<=L and C_f=L. Thus every primitive target budget, including the sometimes omitted f_y budget, is respected. The source upper gradient is exact and hence fits any sigma_f>=0; the source lower-gradient variance fits sigma_g^2.
At x0=0 the exact lower solution is (0,R(0)/ell,0): U^T b(0)=0, so R(0) does not depend on the hidden frame. Translating the scalar lower coordinate by this public number gives the common initialization y0=0=y*(0), preserves all global derivative/variance bounds and preserves query count under a known affine query/reply transformation. Thus every R0>=0 is admissible; unknown exact initialization is not granted as extra oracle information. Padding unused outer coordinates by zero dependence and unused inner coordinates by mu-quadratics preserves the construction and budgets.
The source primitive class automatically satisfies Lip(grad Phi)<=B_Phi by the complete preceding curvature proof. Lambda_Phi>=B_Phi therefore supplies a rigorous target admissibility check. No assertion is made when this guard fails. Under the fixed internal rescaling, kappa_int^2 ell Delta and vartheta_int^2 kappa_int^8 ell^3 sigma_g^2 Delta are fixed positive universal multiples of kappa^2 L Delta and theta^2 kappa^8 L^3 sigma_g^2 Delta. The source dimension condition (29), with M of order the claimed lower query budget and failure probability 1/8, is bounded by D0 displayed in S after increasing universal C_d; the dimension dependence is polynomial, not hidden in constants. The source lower variable has dimension d+2. Its A.6 explicitly treats worst-instance expected stopping cost using a fixed-horizon truncation argument. Thus its joint oracle, arbitrary randomized algorithms, expected norm target and resource order all agree with this profile. The resulting lower is a new guarded transfer record; the old overbroad b2 remains quarantined. This proof establishes target applicability of the cited theorem; it does not claim an independent reproof of its adaptive information lemma.

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /proofs/4/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: evidence_refs

Native pointer: /proofs/4/evidence_refs; canonical SHA-256: a199ff572036d4e81c6560da5a7f4ec6685c5b4e681312358c90d7ab0a111e4e

#### Native item 1

Native pointer: /proofs/4/evidence_refs/0; canonical SHA-256: 6ac96130f34b6fcb77fc7b1b436d48a150b11c1695244d4aba0d85bb18417951

BL_SPEC_joint_expected_cost__main__e_source_normalization_20261122

#### Native field: verification_scope

Native pointer: /proofs/4/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

### Native proof: BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

Native pointer: /proofs/5; canonical SHA-256: 756208022400364c59f64ccb0e0df56dc1df51c88925ba9ba12b7246f8784bab

#### Native field: kind

Native pointer: /proofs/5/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: ebedbd8f0722babd7d887868e9ccc186c64eb90c7b62bc481c2ddd302ff0e506

Comparison on the bounded-variation noise branch

#### Native field: statement

Native pointer: /proofs/5/statement; canonical SHA-256: 5e4bb44bee39dc6942b2be525bec275691148726387410fa401ef7d6f98386f9

On N, Q*=tildeTheta(theta^2 kappa^8 sigma_g^2 L^3 Delta epsilon^-6), with universal constants apart from the displayed logarithms.

#### Native field: proof

Native pointer: /proofs/5/proof; canonical SHA-256: 99a5ff096212b6f158e0741a745128d5aa7958755664ec62cdc8c156849f2362

On S, k=kappa, E_rho=theta kappa(1+kappa)L/2 and B_Phi=(1+kappa)^2 L(1+theta); the effective bound equals B_Phi. Put D_sigma=(1+kappa)^2 E_rho^2 sigma_g^2/epsilon^4. The N inequalities bound each of the deterministic inner cost, the upper-noise cost and the remaining lower-noise cost by a universal multiple of D_sigma. They also give 1+B_Phi Delta/epsilon^2<=2 B_Phi Delta/epsilon^2. Thus the B.2 polynomial upper expression is at most a universal multiple of
(B_Phi Delta/epsilon^2)D_sigma=(1+theta)theta^2 kappa^2(1+kappa)^6 L^3 Delta sigma_g^2/(4epsilon^6).
Since kappa>=1, (1+kappa)^6<=64 kappa^6. The guarded source lower contains theta^2 kappa^8 L^3 Delta sigma_g^2/epsilon^6. The ratio is therefore at most a universal multiple of 1+theta. On N, C_s<=theta<=2C_s and C_s is fixed universally; the ratio is universal. All source upper logarithms remain displayed through tilde notation; no condition-number or dimension polynomial is suppressed. The source deterministic lower term remains valid as well. These explicit dominance conditions replace an unquantified appeal to a sufficiently small epsilon while other parameters may vary.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /proofs/5/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: evidence_refs

Native pointer: /proofs/5/evidence_refs; canonical SHA-256: 41b51073a4d6d71137315ea5516bef4af840db95beb33befc675146300c0eca4

#### Native item 1

Native pointer: /proofs/5/evidence_refs/0; canonical SHA-256: 2ed43d19279387ffad0180efa604f1201fca26fbdbbb945434a0da296062565a

BL_SPEC_joint_expected_cost__main__e_matching_noise_20261122

#### Native field: verification_scope

Native pointer: /proofs/5/verification_scope; canonical SHA-256: 1350e56715be218d79afee65f34c86d25295364f8783734a58733c7ab14251ec

Complete proof of the stated local endpoint or transfer only; external source theorems are cited premises, not independently re-proved.

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 3682a86c51da1af89fed0dd8d5f62d79cdddc9f5e8e9c4079e0288d3773dd1cf

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 2ce6757ba51e5fd0b90bbe8359af6b0df9e808e08d197c58d221cd4a541c3317

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

#### Native field: setting_id

Native pointer: /joint_analysis/target/setting_id; canonical SHA-256: 6288ab13c9690a1007108a5d8daa26ca8b493f993577c13ed9907447ed130fe9

BL_SPEC_joint_expected_cost

#### Native field: contract_policy

Native pointer: /joint_analysis/target/contract_policy; canonical SHA-256: d4543a64b2bd7b127c223768269eb08c7418c637909f6a10de4ec875e4531c2d

Original common specification and view guarantees retained.

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 9eb6b0b59dd8e9b96245cbe33fdf3b7cecc2fbe157145be4a060249bc3e7bf99

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: ce74b1ba4f12b7545c340dd525329a748d45fd1c95ae99d1b63412d7921edf28

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 2a332a69ebd42ac868eeba1b9c376fbe56e467d631f7555a90b335070625a621

Exact zero; no multiplicative ratio.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 2a332a69ebd42ac868eeba1b9c376fbe56e467d631f7555a90b335070625a621

Exact zero; no multiplicative ratio.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 622dedba0803eaa1c3d981e7573d17e269df70c6bf748f2bdb87026968b46139

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 97c1025e719b93505f7f1c4395df4ba28dc68d42b24e6a21edcffee21e5b6c8a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 5e5bb8095408578c1bbf27fa2c5d3468fbeaee3ab4f0219164445470b76d034f

BL_SPEC_joint_expected_cost__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: b3a81a39bbac271ffa94679366316e5ec6032134654420e2b37140620bc87820

All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: b3a81a39bbac271ffa94679366316e5ec6032134654420e2b37140620bc87820

All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 43df56f8ca1875661be0bec027ff455116ae4ddefa7db64fca8845a8dbaf49aa

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 713f63d69b0f7adce84630c8c53066c5dd3998a068eafd0dd649c6bff2cf9f1c

BL_SPEC_joint_expected_cost__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: b3a81a39bbac271ffa94679366316e5ec6032134654420e2b37140620bc87820

All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: b3a81a39bbac271ffa94679366316e5ec6032134654420e2b37140620bc87820

All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 1cf18f1e99a70e43bca4d4ba1f4a5fd474349954f7c31e83d82de5a0537fce15

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 10fb29dcc6f63dbf6cdba8e16ac2e873415fa393fbb69838bc77bff84f549f82

\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: bcf9d2a363caf2637deb47edf04eaa166837042b50df812c471b1eafe77ac197

\Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 87a349df326e07173f7c3caec2a06bb0bd04fbb0d5946ed8d77a7cea1d9d3b97

The upper/lower ratio is the displayed U divided by the displayed positive L, up to the source logarithms. No matching dependence on arbitrary sigma_f or theta is asserted.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 87a349df326e07173f7c3caec2a06bb0bd04fbb0d5946ed8d77a7cea1d9d3b97

The upper/lower ratio is the displayed U divided by the displayed positive L, up to the source logarithms. No matching dependence on arbitrary sigma_f or theta is asserted.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: e00c99b1a8efbe59d84b5feca612aa642cc22bf36e0f66116f94ad8c944cce3e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 782c304e50fb55ed9deb5949c5e4b59726fab846c609a7476bb7e53818788bff

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 8fd0ba1bfe62db0a1fc287eabc43f1ec77ce7eb0e3e5d6abb7cd1705192d408c

The complete S predicate and not the complete N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 8fd0ba1bfe62db0a1fc287eabc43f1ec77ce7eb0e3e5d6abb7cd1705192d408c

The complete S predicate and not the complete N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 95637fff552c42ecac03abf8a7714f64ba29236cc549fd421661a4c60c4e9f5a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 8fd0ba1bfe62db0a1fc287eabc43f1ec77ce7eb0e3e5d6abb7cd1705192d408c

The complete S predicate and not the complete N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 8fd0ba1bfe62db0a1fc287eabc43f1ec77ce7eb0e3e5d6abb7cd1705192d408c

The complete S predicate and not the complete N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 48e6b31a60b2939f4e436397d643b16b993c839eaf2b32172524993eabcfaf29

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 1dfc749e064f199de5e43fd5d1f0f7000e99dfeec2054539bcd2a8ecfead2247

BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 2cc6c6427e6d9789e1a24265c6c3f7aa81b926409d8a7e5c79218fa463d353a1

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: c7fcc261a27ba0aa6091e2d05e004635e7985109123be9794a8a6e95c6cddc36

\widetilde O(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: bbe63ee0a72fd99b885d66c18650b9ed4f11794bbb7e41ce7055bf0010e1b3b2

\Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 0bea534dc53df6284033496cb8cc349ff8cda59bb74e42783003a1b30bc16857

Only the source upper logarithms remain; accuracy, condition-number, lower-noise and gap powers match on N.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 0bea534dc53df6284033496cb8cc349ff8cda59bb74e42783003a1b30bc16857

Only the source upper logarithms remain; accuracy, condition-number, lower-noise and gap powers match on N.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 7bef9bed7435b96a9f0c1339bc7c45bea4b5fe731ceb276fc39264f9234da4a7

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: 30e009ce475155f6279f60b9892bbe53bb5a2eb1c446ff6401cc6554085f9ba8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: c40402aa1a3425761a7b3e9d0a103e7674761f5429e25d6ff377e08fcc8878a8

BL_SPEC_joint_expected_cost__main__b_matching_noise_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 20681456a0777796bb2d3640970998631f90ba7aaaf4f79cd23b85002f1773a6

The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 20681456a0777796bb2d3640970998631f90ba7aaaf4f79cd23b85002f1773a6

The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6f84a64a2620e51e082cc992c58e3814c6541d079e8e1cab7ba38dcc90798935

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: bd96cf5f3776dc90e71e8a65cfbc21b4abe93cfc39f61ae3f086f7a7769d8d97

BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/1; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 3135b9bb31d124cf5f20679f0a09c50744b5931163850624bdb940a6afade2b0

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: c66acb120133c44f01bd9d82ef1ae8bdd967e827da50c4973288c428545d99da

BL_SPEC_joint_expected_cost__main__b_matching_noise_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 20681456a0777796bb2d3640970998631f90ba7aaaf4f79cd23b85002f1773a6

The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 20681456a0777796bb2d3640970998631f90ba7aaaf4f79cd23b85002f1773a6

The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: ff52ab9bd593cce3178c83a3eb8f6e78cc94df19dedb580140d169f6889567af

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: bd96cf5f3776dc90e71e8a65cfbc21b4abe93cfc39f61ae3f086f7a7769d8d97

BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 1dfc749e064f199de5e43fd5d1f0f7000e99dfeec2054539bcd2a8ecfead2247

BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: ccf1bf876035be292ca301fb10f410332dda72240db19e9dd49bf3db3364c6d8

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 10fb29dcc6f63dbf6cdba8e16ac2e873415fa393fbb69838bc77bff84f549f82

\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: 12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126

Native value (string): ""

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: d2b89510a639dd9d3292bdfe0cd11b4b30830e75943b44aaa22b40a7118504c5

A target-compatible positive lower is missing outside E and S.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: d2b89510a639dd9d3292bdfe0cd11b4b30830e75943b44aaa22b40a7118504c5

A target-compatible positive lower is missing outside E and S.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: a9040a5b21f1702ed88acbbc08cdccc4b9bec3aac49ed0f43f6a37b199f7b7bb

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: e7bf87897de9f7265480a5971cc03e43133cf6fee47d6a19223cf756d2bdadaf

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 8e12661506ef5e3177d9f0b2ff2a60811b6ba4fb5150fb717edbf87e4e8a6259

All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 8e12661506ef5e3177d9f0b2ff2a60811b6ba4fb5150fb717edbf87e4e8a6259

All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 85010076d3911b8f8b71cc875601d12caf6ac94da83015e272f4a5ccf15475f2

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: a3576cad498d0dbcd78fda17df1bf6bc2c10d104b39e7f34870cbfc1687d72fa

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 0bb8bc62a5ac77d5bae0b4aeeead4ca9739a33e07da246ecfcc6a4ce1526194e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: b3a81a39bbac271ffa94679366316e5ec6032134654420e2b37140620bc87820

All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: b4d65ebaddff150b85afc3cc8ce33112bf5b7856f25369b0c105a86247964946

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 470d477f98f7ab37d0d4f418b6b3c98e982ff4690de44473b4be41ee9d49ad11

Complete effective-curvature proof; nonnegative expected query cost.

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 8cc8654b24a50c323aab5f91b213011141abbb97a45f9801b6a3e0270ec4b88a

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 8fd0ba1bfe62db0a1fc287eabc43f1ec77ce7eb0e3e5d6abb7cd1705192d408c

The complete S predicate and not the complete N predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 683a8e49f9f96b39117fb1a8bcffc20de0fc76044dce9134f69ccca07e1eaad1

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: f1754846d6edcb176fe741ec32fc26165666c329b8e42f5357c927e47592e30b

Source theorem plus complete normalized transfer; all parameter dependence stays explicit.

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 59d70f7b93101225cc5c4e5083bf37787b8b3efa35b34008db3db5fbe7c84361

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 20681456a0777796bb2d3640970998631f90ba7aaaf4f79cd23b85002f1773a6

The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: c57e77e59274953c8654e6aa4d84f418b74405e5a960ed9fdb23aa0a64e7d201

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 51add160ea8da9879029145ca5d7e3382b097e936e182bfd6201eb6480d0266d

Complete dominance calculation; theta is bounded by fixed universal constants.

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 2c867606ee80c4ba994ddc5cb6a4103cee3f8764f43b9faff4804916341be26c

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 8e12661506ef5e3177d9f0b2ff2a60811b6ba4fb5150fb717edbf87e4e8a6259

All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 5436e82d2b7b61ec4aaa61aa3495b935a3ae2dbabd839f45afcb63a7707d09b9

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 3edd8c8fdbed3b2a195bb2acd0b89e19cffbff594ad1be058bcc2d24ed55e736

B.2 supplies an upper bound throughout this remainder. Neither the quarantined b2 nor the new S-only lower is used here.

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 1619dcf9c1ab5aa4e8773eb62b4c24882595cd123ca1f771d6f0c70c7a2cd6be

Let E be 2 barLambda_Phi Delta<=epsilon^2. S is the explicit normalized source-compatible guard and is disjoint from E for the fixed sufficiently small c_s; N is a subset of S. The four cells E, N, S minus N, and D minus (E union S) are disjoint and cover the native parameter domain.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 972ea8a41362086708909ce378df98205a855f46924d80e1b28c5836b554c444

See explicitly marked missing-lower or retained deterministic residual cells.

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: d79a3a017e435b35c53ecc2be2d24aa4f2e63d29375b3c913e1b45a051d1fafa

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: e89350a8d6b5fbdf29aaedd92ab607b64f4fe2b0b8091c0c38acf4796d212185

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 911bb6230de947eadbbbb08a416e1159ac14d9597548a0f504c518fa92566c0b

BL_SPEC_joint_expected_cost_mathematical_update_20261122

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 44a4c8f689f0395b2d8c685edbc01191a70adaff7e754afd9110a18ff77691b1

Preserve the independent Lambda_Phi model, prove the global bound B_Phi, and strengthen the upper bound and zero-query region using min(Lambda_Phi,B_Phi). Add the A.6 lower bound within the explicit S window, retaining all primitive budgets, initialization, dimension and expected-cost requirements; keep the invalid old b2 excluded. Add the near-optimal N branch with its explicit noise-domination condition and fixed range of theta, without claiming closure elsewhere. Correct the resource-projection description: one joint response in the original interface contains both full gradients and is charged once.

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 92b0703e340009dfe95f68b61749a08e1a2a29c30ae42719be0cc7ad89b26ad6

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 84b9079d0998e636de533a1a2d2213812c1796e1287ade0531ac3af35dea0daa

Establish stronger target-compatible lower bounds for independent Lambda_Phi<B_Phi or primitive budgets outside S.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 4db624ca7355c74b5aa24bcfd7887fa4edf7f9edb6666970b479116e562ad3b1

Verify any larger source-transfer window, especially variable C_f/Delta, rather than deleting its constraints.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 79a884b8378db74890ea979b8ffbe5612a9a8047bd3e19e6c78147885c848062

Independently audit the source adaptive lower-bound proof before claiming a source-proof certification.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: c7fded90be696fe8bdd2a6dfafe7c3771db94cecd78b191cebb475b253a9e7b1

Assess source arXiv:2610.03633v2 Corollary C.6 and Theorem C.5 for the accuracy-dependent small-gap slice, preserving its fixed multiplier, primitive-budget ratios, Lambda_Phi compatibility and source high-accuracy restrictions; no such bound is adopted here.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: e791f8c0b187550c6727bec79a76e00b3bf2603f9a308c5e79133ae4e3482daa

Read the remaining zero-variation branch in Section D of arXiv:2610.03633v2 and map the initialization/noise/dominance restrictions before any adoption.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 72637d133339608635afda450cef4b482f80accd97a68dda2b53cf958c755b29

Read primary theorems of arXiv:2610.03638v2 and arXiv:2610.01843v1 if pursuing the nearby main-rate routes; metadata alone does not settle fixed-budget versus expected-cost applicability or uniform structural dependence.

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: e88a251e7db28f98adb3c93c7e1da546bce42a640b687a00dfbc6d19331127d9

Investigate the upper-level-noise lower route and any finite-dimensional saturation or guarantee-containment refinements outside this local correction; they are not certified absent.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 0e6af2903437641daba172bf21425c19eb5295aca82052a379bf7dd44cb2d0a3

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: c55d3bf8e166968932e27c21a26f703cfe11a47fa8a650bf864fb829b49d99a4

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: 732d644c9a4910bc79c46406734ebdc342be508a168e6d85b2ba9497049e2722

Targeted checks of the named primary versions and complete local proofs; no exhaustive literature claim.

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 1dee0d4f1045cb40fa1b597adcab02c90213d8a4ec6f07c65dcce160169e9f00

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 5a73376781a5f896e5d148e49e51ea1e5268f21fd5a0bf7d885f2135aef91fc0

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: 56faeda9bb894418ff9945a53fbcabbc9c4d62e4e2a5e17f6ce8e0b16051e82d

pending-20261122-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 84b9079d0998e636de533a1a2d2213812c1796e1287ade0531ac3af35dea0daa

Establish stronger target-compatible lower bounds for independent Lambda_Phi<B_Phi or primitive budgets outside S.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 2bce339b219a592b6e72519095e93615501bc2ca6b44cbc6c9a80bc8ed037b9c

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: 116cc72611b7d9bbc01357f04524c3a2e8c10665ec909c36222d1aad26e7983c

pending-20261122-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 4db624ca7355c74b5aa24bcfd7887fa4edf7f9edb6666970b479116e562ad3b1

Verify any larger source-transfer window, especially variable C_f/Delta, rather than deleting its constraints.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: e50f153319060eea806dcb4b05884ed18bda82fc6fc21e295ffd6303ace87dc5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 6c54e37233d5eaf6c35bbacbc94f2ca42aeb635e29e3d5660dd601dc9781188f

pending-20261122-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 79a884b8378db74890ea979b8ffbe5612a9a8047bd3e19e6c78147885c848062

Independently audit the source adaptive lower-bound proof before claiming a source-proof certification.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 8053ed1efe154313975f568ad59adbae97c1f0eecc5bffd623ab6803f9aa3788

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 76133c8a4f70db7cde2f1df965265ee46901a1c240d1aab474ac03fcccb3bc14

pending-20261122-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: c7fded90be696fe8bdd2a6dfafe7c3771db94cecd78b191cebb475b253a9e7b1

Assess source arXiv:2610.03633v2 Corollary C.6 and Theorem C.5 for the accuracy-dependent small-gap slice, preserving its fixed multiplier, primitive-budget ratios, Lambda_Phi compatibility and source high-accuracy restrictions; no such bound is adopted here.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 3348f6ccd8115b790dda9cd44328acea920b05e7ac74786c3d8818f3a84cae93

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: c96b9a83311385aff7047c91b3a6443135f0b4f349c602a377449aef6eed6f38

pending-20261122-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: e791f8c0b187550c6727bec79a76e00b3bf2603f9a308c5e79133ae4e3482daa

Read the remaining zero-variation branch in Section D of arXiv:2610.03633v2 and map the initialization/noise/dominance restrictions before any adoption.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 4cd0f912b601f95308e2e869a86997e78d545c67d7dd54e3ae69833b7e3d86f7

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 628db5951a1f2f9656525d5519cf5518a562dbf2ac06fdf405a5d3afb919857b

pending-20261122-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 72637d133339608635afda450cef4b482f80accd97a68dda2b53cf958c755b29

Read primary theorems of arXiv:2610.03638v2 and arXiv:2610.01843v1 if pursuing the nearby main-rate routes; metadata alone does not settle fixed-budget versus expected-cost applicability or uniform structural dependence.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: ec41df71eb37b85ccc2ec7d3f5dd56f96ce22a3b00b4695b1561a7bafe2bd9b6

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: a9ccdac122fd4c1583db8dd0be80f265ee5dd5cf17f14c61a4935488de7fd6b2

pending-20261122-6

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: e88a251e7db28f98adb3c93c7e1da546bce42a640b687a00dfbc6d19331127d9

Investigate the upper-level-noise lower route and any finite-dimensional saturation or guarantee-containment refinements outside this local correction; they are not certified absent.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: 0d20e987967139ce219043faef79d2ae6887e55504a8ea35d85892f2181c9cbb

Remaining work is explicitly unproved; a missing Atlas bound is not itself a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 22bbe7126f073164c3de902779d9d961058c601929c374e468ddb988f790506d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 2f22786af1455ea6b93ff0b04aef4ad522bb3a3d6959b898cd4c38cdb27418c5

BL_SPEC_joint_expected_cost__main__c_source_remaining_20261122

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/2; canonical SHA-256: 063fb9342ea345e5a2af8b6f95a2e3c1fb9e72cc483415573a18d2e06580b4a1

BL_SPEC_joint_expected_cost__main__c_matching_noise_20261122

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/3; canonical SHA-256: aedc7c7c5ce7a3de706700ae8d1479fd64ce8ceac267e0439a5db3111a2a4021

BL_SPEC_joint_expected_cost__main__c_residual_20261122

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: c97c4f34e0cb36abb137cc070a1d1f26ba2cd7bb3ae5c235f0ab19328903c112

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 05bdc9e60ae26b4e2ee0481b3050a1ff726669429767944e679e48100cb15ef4

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: f7a61f49ae5e60151d293133b29642f789e81e3d59dc194e683d14af3fdbef2b

source_theorem_with_analyst_transfer

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: d5f3b004de201f241d45b677a117b4092f660edc2907a9528bbbc08e18a05ba4

#### Native item 1

Native pointer: /joint_analysis/provenance/0/target_domain/0; canonical SHA-256: 0a5cb13165e7d68a4bd9fe4e5ff71259653efad1c97aabc052fb988dfe60585a

BL_SPEC_joint_expected_cost__main__r2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 286a8e1ebd5542ff0e47562257ceee137a7b20a881e8925c360c5839f57de133

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: f7a61f49ae5e60151d293133b29642f789e81e3d59dc194e683d14af3fdbef2b

source_theorem_with_analyst_transfer

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 48e6b31a60b2939f4e436397d643b16b993c839eaf2b32172524993eabcfaf29

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 1dfc749e064f199de5e43fd5d1f0f7000e99dfeec2054539bcd2a8ecfead2247

BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 769b944645f8b53ae77d7897b8766f8ffa069cdd57d19520c8218697e2def5c8

#### Native item 1

Native pointer: /joint_analysis/provenance/1/target_domain/0; canonical SHA-256: 834bc3ddd67b355d467aed3101acf4f0dbd3e8f078a0ee41cbff45dd0bd427ba

BL_SPEC_joint_expected_cost__main__r_source_compatible_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 9a3fe54023c12a56f064e832530949395041eb583efbd699fb342b82a08b351a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: c40402aa1a3425761a7b3e9d0a103e7674761f5429e25d6ff377e08fcc8878a8

BL_SPEC_joint_expected_cost__main__b_matching_noise_upper_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: f7a61f49ae5e60151d293133b29642f789e81e3d59dc194e683d14af3fdbef2b

source_theorem_with_analyst_transfer

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 6f84a64a2620e51e082cc992c58e3814c6541d079e8e1cab7ba38dcc90798935

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: bd96cf5f3776dc90e71e8a65cfbc21b4abe93cfc39f61ae3f086f7a7769d8d97

BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

#### Native item 2

Native pointer: /joint_analysis/provenance/2/proof_refs/1; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 19d2f52c0f10ec7bf94133b00d5d665c87e6db9c24176c051a54225898218ce0

#### Native item 1

Native pointer: /joint_analysis/provenance/2/target_domain/0; canonical SHA-256: c9adb3314e51120309898403308df6ac3b13e7fddf4e0a030bae4cb34de542da

BL_SPEC_joint_expected_cost__main__r_bounded_variation_noise_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 578c2a7a3763f2d73d237307175489c956f91be8720a627882cb7a2389167615

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: c66acb120133c44f01bd9d82ef1ae8bdd967e827da50c4973288c428545d99da

BL_SPEC_joint_expected_cost__main__b_matching_noise_lower_20261122

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: f7a61f49ae5e60151d293133b29642f789e81e3d59dc194e683d14af3fdbef2b

source_theorem_with_analyst_transfer

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: d9cfd9eed1653c28ad200db21d0a9d6bd6a26b330d258ef5705699b9f01b02fc

#### Native item 1

Native pointer: /joint_analysis/provenance/3/source_refs/0; canonical SHA-256: 1bcea262a4977047d2be580dd33d8cb9f263d852a69182aba19d1b973150fe27

BL_SRC_zhang2026

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: ff52ab9bd593cce3178c83a3eb8f6e78cc94df19dedb580140d169f6889567af

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: bd96cf5f3776dc90e71e8a65cfbc21b4abe93cfc39f61ae3f086f7a7769d8d97

BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

#### Native item 2

Native pointer: /joint_analysis/provenance/3/proof_refs/1; canonical SHA-256: 1dfc749e064f199de5e43fd5d1f0f7000e99dfeec2054539bcd2a8ecfead2247

BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 0af78bd3881e6adf6d0815068b0b027ddcb1a0f64ecee145fc5cd31fece3fe48

The source premise or native class explicitly stated in the complete local proof.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 19d2f52c0f10ec7bf94133b00d5d665c87e6db9c24176c051a54225898218ce0

#### Native item 1

Native pointer: /joint_analysis/provenance/3/target_domain/0; canonical SHA-256: c9adb3314e51120309898403308df6ac3b13e7fddf4e0a030bae4cb34de542da

BL_SPEC_joint_expected_cost__main__r_bounded_variation_noise_20261122

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: f16f6afeb9badfdbb8084c70cbd647a38fc3049edf788757420b7d573a1da0aa

Exact target view, guarantee, output and resource scope as recorded in this bound.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 5b6b0188d72504f8b2617c136ee4b012bd5491a0d78fc44303e8ea511a2cbe8f

See this bound's evidence and complete local proof records.

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Closing the Accuracy Gap in Stochastic First-Order Bilevel Optimization. 2026. arXiv:2610.03633v2, 2026-10-19.

https://arxiv.org/pdf/2610.03633v2
