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
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}\mathbb E C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\\[3pt]\forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\mathrm{joint}}.\end{gathered}
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
\begin{aligned}&\widetilde O\!\bigl((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\bigl[1+k\\[4pt]&+\frac{(1+k)^2}{\varepsilon^2}\bigl\{\sigma_f^2+\bigl(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\bigr)\sigma_g^2\bigr\}\bigr]\bigr)\end{aligned}
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
\begin{aligned}&\widetilde O\!\bigl((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\bigl[1+k\\[4pt]&+\frac{(1+k)^2}{\varepsilon^2}\bigl\{\sigma_f^2+\bigl(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\bigr)\sigma_g^2\bigr\}\bigr]\bigr)\end{aligned}
$$

**Gap or comparison.** A target-compatible positive lower is missing outside E and S.

**Comparison argument.** B.2 supplies an upper bound throughout this remainder. Neither the quarantined b2 nor the new S-only lower is used here.

## 4. Bounds and supporting evidence

### B1 - frozen-tilt estimator and descent

**Admission.** Eligible evidence; not selected in the displayed bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\begin{gathered}\begin{aligned}&\widetilde{\mathcal{O}}\!\bigl(\bigl(1+\frac{\Lambda_\Phi\Delta}{\varepsilon^2}\bigr)\bigl[1+k\\[4pt]&+\frac{(1+k)^2}{\varepsilon^2}\bigl\{\sigma_f^2+\bigl(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\bigr)\sigma_g^2\bigr\}\bigr]\bigr),\end{aligned}\\[5pt]k=\frac{L_g}{\mu},\qquad E_\rho=\frac{(1+k)\rho C_f^2}{2\mu^2}.\end{gathered}
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
\begin{aligned}&\widetilde O((1+\Lambda _\Phi \Delta /\varepsilon ^2)[1+k+(1+k)^2 \varepsilon ^{-2} {\sigma _f^2+(L_f^2/\mu ^2+1+E_\rho ^2/\varepsilon ^2)\sigma _g^2}]), k=L_g/\mu ,\\[3pt]&E_\rho =(1+k)\rho  C_f^2/(2\mu ^2)\end{aligned}
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

**Local argument.** A4

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

**Local argument.** A4

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122; theorem: Global reduced smoothness and a redundant-budget transfer

Analyst-derived argument is kept separate from published/preprint evidence.

### B5 - Frozen-tilt method with effective curvature

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\begin{aligned}&\widetilde O\!\bigl((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\bigl[1+k\\[4pt]&+\frac{(1+k)^2}{\varepsilon^2}\bigl\{\sigma_f^2+\bigl(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\bigr)\sigma_g^2\bigr\}\bigr]\bigr)\end{aligned}
$$

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

**Conditions.** Assumption 3.1 and finite initialization; outside the effective zero region barLambda_Phi>0.

**Guarantee conversion.** Exactly the target view guarantee; no expectation/probability or budget conversion is implicit.

**Resource conversion.** Every actual bundled oracle response is counted once under the target resource definition.

**Constants.** None for exact endpoints; otherwise only the explicitly stated universal source constants.

**Logarithmic factors.** The accuracy and initialization logarithms in source Theorem B.2 are retained.

**Local argument.** A4

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

**Local argument.** A5

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

**Local argument.** A6, A4

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

**Local argument.** A6, A5

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122; theorem: Comparison on the bounded-variation noise branch

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) section: Complete local proof BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122; theorem: A sufficient normalized guard for Theorem A.6

Analyst-derived argument is kept separate from published/preprint evidence.

**Source location.** [1](https://arxiv.org/pdf/2610.03633v2) equations: (30); (31); pdf pages: 16; section: Appendix A; theorem: Theorem A.6

## 5. Local arguments

### A1 - Exact sufficient zero-query region and counterexample to the recorded uniform lower transfer

Q\*=0 on E; the active b2 target transfer on H is not valid uniformly in the native independent Lambda\_Phi budget.

H is exactly the frozen regime BL\_SPEC\_joint\_expected\_cost\_\_main\_\_r1 (including its symbolic universal constants and dimension qualification). Let D denote the frozen model and all native parameter domains. The independent public parameter Lambda\_Phi is a valid global Lipschitz bound for the reduced gradient. For any admissible instance, put v=grad Phi(x0). Smoothness at z=x0-v/Lambda\_Phi gives inf Phi <= Phi(z) <= Phi(x0)-||v||^2/(2 Lambda\_Phi). Thus ||grad Phi(x0)||^2 <= 2 Lambda\_Phi Delta. No oracle is used to compute z; it is only a proof point. On E={D:2 Lambda\_Phi Delta<=epsilon^2}, the permitted algorithm that returns the supplied x0 without queries meets the expected-norm guarantee for every legal instance and oracle law. Its worst-instance expected count is 0, and resource nonnegativity gives Q\*=0. Equality and Delta=0 are included; this is a sufficient zero-query region, not a converse threshold. To test the old lower transfer uniformly, fix L=Delta=1,kappa=2,mu=1/2,theta=1,rho=1/2,chi=2,L\_f=L\_g=C\_f=1,R0=0,sigma\_f=0,sigma\_g=1, and let epsilon tend to zero while Lambda\_Phi=epsilon^2/4. These values satisfy H for all sufficiently small epsilon and E for every epsilon. The class is nonempty in every finite dimension: f=0,g(x,y)=mu\*||y||^2/2,x0=y0=0 and exact gradients satisfy all stated upper budgets and the initialization certificate. More importantly, the same return-x0 algorithm works on the entire admissible class at these budgets, not only that example. Hence Q\*=0 whereas the old b2 expression is strictly positive and grows as epsilon^-6. The transfer into a quantity that varies Lambda\_Phi independently is therefore invalid as recorded. This does not disprove the source theorem for its original primitive-budget class. Quarantine b2's current target formulation pending a separately proved guard ensuring that its hard family meets all public budgets, including Lambda\_Phi. No positive lower bound is retained outside E merely by weakening the old formula.

### A2 - Canonical state and previously proved region publication

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline\_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic\_gap, polynomial\_gap and other\_quantified\_gap belong to gap\_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. 

### A3 - Same-class interpretation of the already-declared independent Lambda_Phi budget

Appending the MODEL paragraph makes the existing parameter-14 promise explicit and preserves the complete native admissible class and complexity statements.

The frozen parameter at /parameters/14 has stable ID BL\_SPEC\_joint\_expected\_cost\_p\_5ffc729833; it is public, kind independent, has no dependencies, positive domain, and defines the Lipschitz upper bound for the reduced gradient on the declared full upper-level domain. A legal instance of the original native profile must satisfy its public parameter definitions/budgets as well as common\_specification. Let C\_old be that class for a fixed admissible public parameter tuple. Let P be exactly the displayed inequality in that parameter definition, quantified over all upper-level points. Hence C\_old is a subset of P. The appended MODEL paragraph states P and its already-declared independent role, leaving every previous definition and condition in force; thus C\_new=C\_old intersect P=C\_old. Conversely every new instance satisfies every old condition since none is removed or weakened. The instance/oracle-law map in either direction is the identity. It preserves dimensions, f and g, initialization and gap, norm bounds, lower-level curvature, noise/primitive budgets, output, probability/expectation quantifiers, and every charged gradient/Hessian/vector call. Therefore every unchanged native statement retains exactly its original applicability, conditional on the same accepted premises; no withdrawn lower bound is reinstated and no external theorem is recertified. Independence means Lambda\_Phi is not silently replaced by a formula in primitive budgets. This proof does not assert that arbitrary contradictory budget tuples admit an instance; feasibility and all original compatibility conditions are unchanged. In particular any hard-family transfer had to satisfy the public Lambda\_Phi promise before and after the prose clarification. This is equality of the already-defined classes, not adoption of a new smoothness hypothesis or a new complexity inequality.

### A4 - Global reduced smoothness and a redundant-budget transfer

Lip(grad Phi)<=B\_Phi; the independent Lambda\_Phi promise is redundant when Lambda\_Phi>=B\_Phi. Effective curvature is min(Lambda\_Phi,B\_Phi).

Write z=(x,y\*(x)) and z'=(x',y\*(x')). Strong convexity and the L\_g-Lipschitz full gradient imply ||y\*(x)-y\*(x')||<=k||x-x'||, hence ||z-z'||<=sqrt(1+k^2)||x-x'||. Put B=g\_xy, H=g\_yy, u=f\_x and a=f\_y at z, with primed symbols at z'. The model gives ||B||,||B'||<=L\_g, ||H^{-1}||,||H'^{-1}||<=1/mu, ||a||,||a'||<=C\_f, and ||H^{-1}-H'^{-1}||<=rho||z-z'||/mu^2. Using grad Phi=u-BH^{-1}a and adding/subtracting terms yields
||grad Phi(x)-grad Phi(x')|| <= [(1+k)L\_f+(1+k)rho C\_f/mu] ||z-z'|| <= (1+k)^2(L\_f+rho C\_f/mu)||x-x'||.
This is a whole-class bound, with no assumption on g\_xx variation. Consequently, for fixed primitive budgets, initialization, dimensions, oracle laws and guarantees, the class with Lambda\_Phi>=B\_Phi is exactly the class before imposing the Lambda\_Phi promise. The identity map preserves every query and expected stopping cost. A source hard family already satisfying the primitive budgets therefore also satisfies this independent promise. Merely excluding 2 Lambda\_Phi Delta<=epsilon^2 would not prove this transfer. For every budget tuple the same derivation and the independent promise imply the usable bound barLambda=min(Lambda\_Phi,B\_Phi). If barLambda=0, grad Phi is constant; finite inf Phi on the full Euclidean space forces grad Phi=0. Otherwise the descent inequality gives ||grad Phi(x0)||^2<=2 barLambda Delta. Thus returning x0 costs zero whenever 2 barLambda Delta<=epsilon^2, including equality and Delta=0. Outside this region barLambda>0, so Theorem B.2 may be run with barLambda as its public valid bound. This improves its displayed polynomial factor without modifying the model.

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

### A5 - A sufficient normalized guard for Theorem A.6

On S, the source Theorem A.6 gives Omega(kappa^2 L Delta epsilon^-2 + theta^2 kappa^8 sigma\_g^2 L^3 Delta epsilon^-6) for the exact target expected-cost quantity.

Use the source Theorems A.4 and A.6, equations (14), (20)--(23), (29)--(31), as cited preprint premises. Let C\_A bound their fixed global-regularity constants. Choose a fixed a>0 so small that C\_A(a+sqrt(a))<=1 and C\_A a<=1. Use internal scale ell=aL and internal lower curvature mu\_int=2mu. Choose a fixed b>0 with 2 C\_A b<=1 and set vartheta\_int=b theta. Choose universal C\_s large and c\_s small so that kappa\_int=ell/mu\_int=a kappa/2>=2, 1<=vartheta\_int<=kappa\_int, beta vartheta\_int lies in A.4's small window, and the target accuracy window implies A.6's internal one. Such choices are possible, for example by enforcing C\_s>=max(4/a,1/b) and c\_s below the finite source constants times a^(3/2) and a/b.
A.4 gives strong convexity at least mu\_int/2=mu, first-order Lipschitz budgets at most C\_A ell<=L, and Hessian variation at most C\_A mu\_int vartheta\_int<=rho. Its full upper-gradient bound is C\_A(ell+sqrt(ell Delta))<=C\_A(a+sqrt(a))L<=C\_f because Delta<=L and C\_f=L. Thus every primitive target budget, including the sometimes omitted f\_y budget, is respected. The source upper gradient is exact and hence fits any sigma\_f>=0; the source lower-gradient variance fits sigma\_g^2.
At x0=0 the exact lower solution is (0,R(0)/ell,0): U^T b(0)=0, so R(0) does not depend on the hidden frame. Translating the scalar lower coordinate by this public number gives the common initialization y0=0=y\*(0), preserves all global derivative/variance bounds and preserves query count under a known affine query/reply transformation. Thus every R0>=0 is admissible; unknown exact initialization is not granted as extra oracle information. Padding unused outer coordinates by zero dependence and unused inner coordinates by mu-quadratics preserves the construction and budgets.
The source primitive class automatically satisfies Lip(grad Phi)<=B\_Phi by the complete preceding curvature proof. Lambda\_Phi>=B\_Phi therefore supplies a rigorous target admissibility check. No assertion is made when this guard fails. Under the fixed internal rescaling, kappa\_int^2 ell Delta and vartheta\_int^2 kappa\_int^8 ell^3 sigma\_g^2 Delta are fixed positive universal multiples of kappa^2 L Delta and theta^2 kappa^8 L^3 sigma\_g^2 Delta. The source dimension condition (29), with M of order the claimed lower query budget and failure probability 1/8, is bounded by D0 displayed in S after increasing universal C\_d; the dimension dependence is polynomial, not hidden in constants. The source lower variable has dimension d+2. Its A.6 explicitly treats worst-instance expected stopping cost using a fixed-horizon truncation argument. Thus its joint oracle, arbitrary randomized algorithms, expected norm target and resource order all agree with this profile. The resulting lower is a new guarded transfer record; the old overbroad b2 remains quarantined. This proof establishes target applicability of the cited theorem; it does not claim an independent reproof of its adaptive information lemma.

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

### A6 - Comparison on the bounded-variation noise branch

On N, Q\*=tildeTheta(theta^2 kappa^8 sigma\_g^2 L^3 Delta epsilon^-6), with universal constants apart from the displayed logarithms.

On S, k=kappa, E\_rho=theta kappa(1+kappa)L/2 and B\_Phi=(1+kappa)^2 L(1+theta); the effective bound equals B\_Phi. Put D\_sigma=(1+kappa)^2 E\_rho^2 sigma\_g^2/epsilon^4. The N inequalities bound each of the deterministic inner cost, the upper-noise cost and the remaining lower-noise cost by a universal multiple of D\_sigma. They also give 1+B\_Phi Delta/epsilon^2<=2 B\_Phi Delta/epsilon^2. Thus the B.2 polynomial upper expression is at most a universal multiple of
(B\_Phi Delta/epsilon^2)D\_sigma=(1+theta)theta^2 kappa^2(1+kappa)^6 L^3 Delta sigma\_g^2/(4epsilon^6).
Since kappa>=1, (1+kappa)^6<=64 kappa^6. The guarded source lower contains theta^2 kappa^8 L^3 Delta sigma\_g^2/epsilon^6. The ratio is therefore at most a universal multiple of 1+theta. On N, C\_s<=theta<=2C\_s and C\_s is fixed universally; the ratio is universal. All source upper logarithms remain displayed through tilde notation; no condition-number or dimension polynomial is suppressed. The source deterministic lower term remains valid as well. These explicit dominance conditions replace an unquantified appeal to a sufficiently small epsilon while other parameters may vary.

**Sources.** [1](https://arxiv.org/pdf/2610.03633v2)

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Closing the Accuracy Gap in Stochastic First-Order Bilevel Optimization. 2026. arXiv:2610.03633v2, 2026-10-19.

https://arxiv.org/pdf/2610.03633v2
