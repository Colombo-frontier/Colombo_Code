# Fresh joint gradients: joint parameter dependence and expected query complexity

**Setting ID.** `BL_SPEC_joint_expected_cost`

Bilevel optimization

Fresh joint-gradient bilevel optimization with independent reduced smoothness. General common-budget and prescribed-curvature regions have source-reported brackets matching up to logarithms, with separate upper- and lower-noise terms. Exact zero-call regions and an exact-initialization affine branch are scoped separately. A sixth-power accuracy law fixes all structural budgets; independent-budget and initialization remainders persist.

**Status.** Other quantified gap present; Bounds missing

**Gap classes present.** Logarithmic gap; Other quantified gap

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

$c_0$: Numerical fine-accuracy cutoff; it may be reduced to a common constant for the cited theorems. **Domain:** $0<c_0\le1/4$.

$0<c_0\le1/4$ is a fixed sufficiently small source constant.

$C_F$: Numerical multiplier specifying the source prescribed-curvature class, rather than a variable structural budget. **Domain:** $C_F\ge C_*\ge1$, fixed numerically.

$\Lambda_\Phi=C_F L\kappa^2$ on C, with fixed $C_F\ge C_*$.

$C_*$: Fixed source threshold for the numerical prescribed-curvature multiplier. **Domain:** $C_*\ge1$.

$C_*\ge1$ is the numerical curvature threshold in Corollary 8.5.

$p_{\log}$: Fixed source lower logarithm power; its value is not replaced by zero. **Domain:** $p_{\log}\ge0$.

$p_{\log}\ge0$ is the numerical power in Theorem 8.1.

$\varepsilon_P$: Accuracy cutoff with allowed dependence on the explicitly fixed structural budgets; not a uniform joint cutoff. **Domain:** $\varepsilon_P>0$, with fixed-tuple dependence.

$\varepsilon_P>0$ is the cutoff of Theorem 5.1 for fixed structural tuple $P$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O}\mathbb E C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|\le\varepsilon\}.\\C=N_{\mathrm{joint}}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

#### Q2 - target accuracy cost

$$
Q_P^*(\varepsilon)=Q^*(\varepsilon;P),\qquad P\ \mathrm{fixed},\ \varepsilon\downarrow0
$$

**Scope.** Accuracy asymptotics with every primitive structural budget fixed and arbitrary finite dimensions under the minimax supremum.

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

### R2 - Additional affine or perfectly conditioned zero-query region

**Region.** The complete Z guard, and not E.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Optimal

**Lower bound.** B16

$$
0
$$

**Upper bound.** B15

$$
0
$$

**Gap or comparison.** Exact zero cost.

**Comparison argument.** Return x0. Source threshold upper statements pass to every curvature subclass; expected cost is nonnegative.

### R3 - Prescribed curvature within the prior noise-dominated window

**Region.** The complete C guard; not E; not Z; the complete old N predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B12, B6, B8

$$
\max\left\{\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right),\ \Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})\right\}
$$

**Upper bound.** B11, B5

$$
\min\left\{\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** The source bracket holds on the complete C guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

### R4 - Prescribed curvature within the remaining prior source window

**Region.** The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B12, B6

$$
\max\left\{\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)\right\}
$$

**Upper bound.** B11, B5

$$
\min\left\{\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** The source bracket holds on the complete C guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

### R5 - Prescribed curvature outside the prior source window

**Region.** The complete C guard; not E; not Z; not the complete old S predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B12

$$
\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right)
$$

**Upper bound.** B11, B5

$$
\min\left\{\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** The source bracket holds on the complete C guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

### R6 - General joint bounds within the prior noise-dominated window

**Region.** The complete J guard; not E; not Z; not C; the complete old N predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B10, B6, B8

$$
\max\left\{\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right),\ \Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})\right\}
$$

**Upper bound.** B9, B5

$$
\min\left\{\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** The source bracket holds on the complete J guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

### R7 - General joint bounds within the remaining prior source window

**Region.** The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B10, B6

$$
\max\left\{\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)\right\}
$$

**Upper bound.** B9, B5

$$
\min\left\{\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** The source bracket holds on the complete J guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

### R8 - General joint bounds outside the prior source window

**Region.** The complete J guard; not E; not Z; not C; not the complete old S predicate.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B10

$$
\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right)
$$

**Upper bound.** B9, B5

$$
\min\left\{\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** The source bracket holds on the complete J guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

### R9 - Constant lower blocks with exact initialization

**Region.** The complete K guard; not E; not Z; not C; not J.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Logarithmic gap

**Lower bound.** B14

$$
\Omega\!\left(\frac{L\kappa^2\Delta}{\varepsilon^2}\left[\sqrt\kappa+\frac{\kappa^2\sigma_f^2}{\varepsilon^2}\right]\right)
$$

**Upper bound.** B13, B5

$$
\min\left\{O\!\left(\frac{L\kappa^2\Delta}{\varepsilon^2}\left[\sqrt\kappa\left(1+\log\left(2+\frac{L\kappa^2\Delta}{\varepsilon^2}+\frac{\kappa L}{\varepsilon}\right)\right)+\frac{\kappa^2\sigma_f^2}{\varepsilon^2}\right]\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}
$$

**Gap or comparison.** Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

**Comparison argument.** Theorem 7.1 uses exact initialization, global variance bounds and unbounded finite queries. All charged fresh calls and the single displayed logarithm are retained.

### R10 - Positive fractional expected cost below the affine zero threshold

**Region.** The complete A guard; not E; not Z; not C; not J; not K.

**Quantity.** Q1

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Other quantified gap

**Lower bound.** B17

$$
\left(1-\frac{\varepsilon}{S_0}\right)\left(1+\frac{\sigma_f^2}{16S_0^2}\right)
$$

**Upper bound.** B5

$$
\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)
$$

**Gap or comparison.** The displayed minimum upper and maximum lower are retained; no matching joint rate is claimed.

**Comparison argument.** Theorem 3.2 supplies a positive fractional expected-cost lower bound, not a unit-call floor. Its lower witness obeys Lambda_Phi>=L kappa^2. The universal native upper remains selected.

### R11 - N: bounded variation and a noise-dominated matching branch: remaining domain

**Region.** (The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.) and not E; not Z; not C; not J; not K; not A.

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

### R12 - Source-compatible window outside the matching branch: remaining domain

**Region.** (The complete S predicate and not the complete N predicate.) and not E; not Z; not C; not J; not K; not A.

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

### R13 - Remaining independently curved parameter class: remaining domain

**Region.** (All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.) and not E; not Z; not C; not J; not K; not A.

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

### R14 - Sixth-power accuracy law at a fixed interior tuple

**Region.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

**Quantity.** Q2

**Resource.** Worst-instance expected number of joint responses: Q=sup_(I,O) E[N_joint]. One response returns both full layer-gradient estimates and costs one; requests at two points cost two joint calls.

**Status.** Optimal

**Lower bound.** B19

$$
c_P\varepsilon^{-6}
$$

**Upper bound.** B18

$$
C_P\varepsilon^{-6}
$$

**Gap or comparison.** Matching sixth-power accuracy dependence with all listed structural budgets fixed.

**Comparison argument.** Theorem 5.1 has tuple-dependent positive constants and cutoff. This comparison concerns epsilon only; it certifies no joint structural-budget exponents.

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

### B9 - Common-budget joint bracket and contract transfer

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

$$
\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa^2$, and $\Lambda_\Phi\ge B_\Phi=(1+\kappa)^2L(1+\theta)$.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Logarithmic factors.** Source accuracy, conditioning and initialization logarithms; finite R0 is not treated as a universally constant factor.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 8; theorem: Theorem 8.1; Corollary 4.6 and Theorem 4.5 for the upper algorithm; pdf pages: 12; 13; 14; 15; 16; 33; 34; 35; printed pages: 12; 13; 14; 15; 16; 33; 34; 35; equations: 8.1; 8.2; 8.3

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

Theorem 8.1 does not give matching lower bounds for theta>kappa^2, for fixed dimensions, or for arbitrary independent tighter Lambda_Phi.

Initialization logarithms cannot be treated as constant when R0 grows exponentially with inverse accuracy.

### B10 - Common-budget joint bracket and contract transfer

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa^2$, and $\Lambda_\Phi\ge B_\Phi=(1+\kappa)^2L(1+\theta)$.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Logarithmic factors.** The displayed denominator [log(2+theta)]^p_log is retained; p_log is a fixed numerical constant.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 8; theorem: Theorem 8.1; Corollary 4.6 and Theorem 4.5 for the upper algorithm; pdf pages: 12; 13; 14; 15; 16; 33; 34; 35; printed pages: 12; 13; 14; 15; 16; 33; 34; 35; equations: 8.1; 8.2; 8.3

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

Theorem 8.1 does not give matching lower bounds for theta>kappa^2, for fixed dimensions, or for arbitrary independent tighter Lambda_Phi.

Initialization logarithms cannot be treated as constant when R0 grows exponentially with inverse accuracy.

### B11 - Prescribed-curvature bracket and independent budget transfer

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

$$
\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa$, and $\Lambda_\Phi=C_F L\kappa^2$, where $C_F\ge C_*$ is a fixed sufficiently large numerical constant. $C_F$ does not vary as a joint asymptotic parameter.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Logarithmic factors.** Source accuracy, conditioning and initialization logarithms.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 8; theorem: Corollary 8.5; Corollary 4.6; pdf pages: 15; 16; 37; printed pages: 15; 16; 37; equations: 8.6

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

The C_F dependence is fixed-numerical, not an omitted joint structural power.

### B12 - Prescribed-curvature bracket and independent budget transfer

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa$, and $\Lambda_\Phi=C_F L\kappa^2$, where $C_F\ge C_*$ is a fixed sufficiently large numerical constant. $C_F$ does not vary as a joint asymptotic parameter.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 8; theorem: Corollary 8.5; Corollary 4.6; pdf pages: 15; 16; 37; printed pages: 15; 16; 37; equations: 8.6

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

The C_F dependence is fixed-numerical, not an omitted joint structural power.

### B13 - Constant lower-block fine-accuracy bracket

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

$$
O\!\left(\frac{L\kappa^2\Delta}{\varepsilon^2}\left[\sqrt\kappa\left(1+\log\left(2+\frac{L\kappa^2\Delta}{\varepsilon^2}+\frac{\kappa L}{\varepsilon}\right)\right)+\frac{\kappa^2\sigma_f^2}{\varepsilon^2}\right]\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\rho=0$, $R_0=0$, $L>\mu>0$, and $\Lambda_\Phi\ge L\kappa^2$. The oracle has a global uniform conditional variance bound and permits arbitrarily large finite query displacements; every difference uses two fresh calls.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Logarithmic factors.** The displayed factor $\Lambda_{\log}=1+\log(2+Q_{\rm aff}+\kappa L/\varepsilon)$ only multiplies the deterministic term.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 7; theorem: Theorem 7.1; Lemmas 7.2 and 7.3; pdf pages: 29; 30; 31; 32; printed pages: 29; 30; 31; 32; equations: 7.1; 7.2; 7.3

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

Lambda_log is a local algorithmic logarithm, distinct from the model budget Lambda_Phi.

### B14 - Constant lower-block fine-accuracy bracket

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{L\kappa^2\Delta}{\varepsilon^2}\left[\sqrt\kappa+\frac{\kappa^2\sigma_f^2}{\varepsilon^2}\right]\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\rho=0$, $R_0=0$, $L>\mu>0$, and $\Lambda_\Phi\ge L\kappa^2$. The oracle has a global uniform conditional variance bound and permits arbitrarily large finite query displacements; every difference uses two fresh calls.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 7; theorem: Theorem 7.1; Lemmas 7.2 and 7.3; pdf pages: 29; 30; 31; 32; printed pages: 29; 30; 31; 32; equations: 7.1; 7.2; 7.3

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

Lambda_log is a local algorithmic logarithm, distinct from the model budget Lambda_Phi.

### B15 - Affine and perfectly conditioned zero-call boundaries

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

$$
0
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. At least one of: (i) $\rho=0$, $\kappa>1$ and $\varepsilon\ge S_0$; (ii) $\kappa=1$ and $\varepsilon\ge S=\sqrt{2L\Delta}$. Here $q_{\rm geom}=\sqrt{\kappa^2-1}$, $G_{\rm geom}=\sqrt{2L\Delta}$, $t_0=\min\{q_{\rm geom}G_{\rm geom}/\kappa,2L\}$, and $S_0=\sqrt{G_{\rm geom}^2-t_0^2}+q_{\rm geom}t_0$. No lower bound on $\Lambda_\Phi$ is needed for this sufficient zero-cost statement.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 3 and 9; theorem: Theorem 3.2; Proposition 9.1; pdf pages: 7; 8; 37; 38; printed pages: 7; 8; 37; 38; equations: 3.6; 3.7; 9.1

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

All finite R0 and lower-noise budgets are allowed in the affine zero-call and activation statements.

### B16 - Affine and perfectly conditioned zero-call boundaries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. At least one of: (i) $\rho=0$, $\kappa>1$ and $\varepsilon\ge S_0$; (ii) $\kappa=1$ and $\varepsilon\ge S=\sqrt{2L\Delta}$. Here $q_{\rm geom}=\sqrt{\kappa^2-1}$, $G_{\rm geom}=\sqrt{2L\Delta}$, $t_0=\min\{q_{\rm geom}G_{\rm geom}/\kappa,2L\}$, and $S_0=\sqrt{G_{\rm geom}^2-t_0^2}+q_{\rm geom}t_0$. No lower bound on $\Lambda_\Phi$ is needed for this sufficient zero-cost statement.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 3 and 9; theorem: Theorem 3.2; Proposition 9.1; pdf pages: 7; 8; 37; 38; printed pages: 7; 8; 37; 38; equations: 3.6; 3.7; 9.1

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

All finite R0 and lower-noise budgets are allowed in the affine zero-call and activation statements.

### B17 - Affine and perfectly conditioned zero-call boundaries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\left(1-\frac{\varepsilon}{S_0}\right)\left(1+\frac{\sigma_f^2}{16S_0^2}\right)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\rho=0$, $\kappa>1$, $\Lambda_\Phi\ge L\kappa^2$, and $0<\varepsilon<S_0$, with $S_0$ defined in Z. The strict inequality entails $S_0>0$.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 3 and 9; theorem: Theorem 3.2; Proposition 9.1; pdf pages: 7; 8; 37; 38; printed pages: 7; 8; 37; 38; equations: 3.6; 3.7; 9.1

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

All finite R0 and lower-noise budgets are allowed in the affine zero-call and activation statements.

### B18 - Sixth-power accuracy law with all structural budgets fixed

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

$$
C_P\varepsilon^{-6}
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 5; theorem: Theorem 5.1; Corollary 5.7; pdf pages: 16; 17; 24; printed pages: 16; 17; 24

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

The fixed-parameter epsilon^-6 law has cited prior work; it is distinct from the manuscript joint-parameter contribution.

### B19 - Sixth-power accuracy law with all structural budgets fixed

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_P\varepsilon^{-6}
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf)

**Conditions.** All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

**Guarantee conversion.** The native expected gradient-norm guarantee, with no squared-norm or confidence conversion.

**Resource conversion.** One fresh joint response contains both complete gradients and is charged once; initialization and random stopping are included.

**Constants.** Universal source constants unless explicitly allowed to depend on fixed C_F or the fixed tuple P.

**Local argument.** BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf) section: 5; theorem: Theorem 5.1; Corollary 5.7; pdf pages: 16; 17; 24; printed pages: 16; 17; 24

All dimensions are arbitrary finite dimensions under the minimax supremum; no fixed-dimension or polynomial-dimension lower bound is asserted. Algorithms may be adaptive and randomized, may stop at a random time, and may output any finite point, including an unqueried point. The guarantee is expected gradient norm, and every actual fresh bundled response, including initialization and unsuccessful histories, is charged once. Fractional expected costs are permitted.

Source PDF SHA-256: 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a

The stated theorem is source-reported; no full-proof or formal-verification certification is implied.

The fixed-parameter epsilon^-6 law has cited prior work; it is distinct from the manuscript joint-parameter contribution.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 2d303debfdc8a6af13c20088c691c33bc67492f0e7bbbe692708b21c7c5ca381

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

### Native proof: BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

Native pointer: /proofs/6; canonical SHA-256: 3fa194fa72e92ca6163b5a39ac2a0485087059fa2f0e9c81921f9ac2b961aa20

#### Native field: kind

Native pointer: /proofs/6/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/6/title; canonical SHA-256: d3c5ff11fb36c96ddd01ff32444ce9849a0552705fb4554f073bd7f14c23676c

Common-budget joint bracket and contract transfer

#### Native field: statement

Native pointer: /proofs/6/statement; canonical SHA-256: 82c88e7f246a580254ce8c61def8cebf76b68bf5195f1eaa1b5c07ebaea3cee1

On J, $c[U+(D+G)/\log^{p_{\log}}(2+\theta)]\le Q^*\le\widetilde O(D+U+G)$, $D=L\chi\kappa^{5/2}\Delta\varepsilon^{-2}$, $U=L\kappa^4\sigma_f^2\Delta\varepsilon^{-4}$, $G=L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}$.

#### Native field: proof

Native pointer: /proofs/6/proof; canonical SHA-256: e46ac7fe26e0b254feacd3164c5e9eb47434148755172ca8b5d39383f7050ddb

Set the source F equal to the native Phi and its variation ratio to native theta. The common-gradient and vertical-cap budgets coincide only on L_f=L_g=C_f=L. The existing universal-curvature proof gives Lip(grad Phi)<=B_Phi on this common-budget class. Therefore Lambda_Phi>=B_Phi leaves the source class unchanged, so both upper and lower statements transfer, with no dimension restriction. The source oracle is the same fresh complete joint-gradient response, with no sample reuse; upper-gradient reuse means stored numerical values, not repeated calls to a hidden sample. The source expected norm and worst expected stopping-cost quantifiers match q1. Finite R0 occurs in upper initialization logarithms; no matching dependence on R0 follows. The source lower construction can have exponential finite hard dimension in the prescribed deterministic horizon. The source logarithmic lower loss is retained. Active C takes precedence over J because the two validity guards can overlap; each active J/C cell is further intersected with N, S minus N, or outside S. The old universal upper remains a candidate in every new cell; each eligible old S/N lower also remains selected under its exact intersection guard.

#### Native field: source_refs

Native pointer: /proofs/6/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/6/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: evidence_refs

Native pointer: /proofs/6/evidence_refs; canonical SHA-256: 811223b116b6ccf4c715e0c0f46308ed97d2eda50709f7ba7e76ab8d93fdf07a

#### Native item 1

Native pointer: /proofs/6/evidence_refs/0; canonical SHA-256: 9ea935e9f9514b3e86b0839148d69e6786d022269b3704101b080b90d4cf0a9e

BL_SPEC_joint_expected_cost__main__e_joint_20261126

#### Native field: verification_scope

Native pointer: /proofs/6/verification_scope; canonical SHA-256: adfd4e85cfa3144875bb360d8a3c38de8b56a0b629e1e3694ea3232adebf20b0

Source-statement and target-contract mapping only. The manuscript theorem is a cited premise, not an independently re-proved or Lean-verified theorem.

#### Native field: evidence_status

Native pointer: /proofs/6/evidence_status; canonical SHA-256: 1578f14f82bb0083a1ecc7fd9b03327d36593f19dd602231105ef79da610c4ca

source_reported_contract_reviewed

### Native proof: BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

Native pointer: /proofs/7; canonical SHA-256: 35d36d0d3b12ed4951f9e79d16c94df612f4545cf4c141309a782102723237d6

#### Native field: kind

Native pointer: /proofs/7/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/7/title; canonical SHA-256: 7d7c67fb94dca60b1d7325afa0d918dbaefef5b8149d47bc1bedeb4a1ad3106c

Prescribed-curvature bracket and independent budget transfer

#### Native field: statement

Native pointer: /proofs/7/statement; canonical SHA-256: 4e2b2cf860dd89ae4fbdbf8f6e8adbeb8781f2588beabd8943433f5dd2908c43

On C, $c(D_{\rm curv}+U+G_{\rm curv})\le Q^*\le\widetilde O(D_{\rm curv}+U+G_{\rm curv})$, $D_{\rm curv}=L\kappa^{5/2}\Delta\varepsilon^{-2}$, $G_{\rm curv}=L^3\theta^2\kappa^8\sigma_g^2\Delta\varepsilon^{-6}$.

#### Native field: proof

Native pointer: /proofs/7/proof; canonical SHA-256: c6ad36fa5fd56695328484f257ea2a79f38a36cc0b62605dab3eb0c78486e543

The native independent curvature budget is retained and set equal to C_F L kappa^2 only in this region. This is the exact public promise of the source subclass; it is not replaced globally by a theorem-implied curvature estimate. C_F is a fixed sufficiently large numerical constant; only the upper implicit constant may depend on it. The source lower witnesses have curvature at most C_* L kappa^2, exact initialization, and admissible fresh conservative samples, which are a subset of the native fresh oracle class. Both statements thus transfer on C. All oracle, cost, guarantee and dimension quantifiers are the same as in the joint contract mapping. C is given precedence in C intersect J. No matching claim is made for arbitrary smaller Lambda_Phi.

#### Native field: source_refs

Native pointer: /proofs/7/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/7/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: evidence_refs

Native pointer: /proofs/7/evidence_refs; canonical SHA-256: 62d4b154c20961aa605ae1d59fe995a9974c036afef9750449de026fce16a341

#### Native item 1

Native pointer: /proofs/7/evidence_refs/0; canonical SHA-256: 87446bbe0bdf9087b36126d3ea578bede7afafc7b20580bde8f8aa1dcee97c4c

BL_SPEC_joint_expected_cost__main__e_curvature_20261126

#### Native field: verification_scope

Native pointer: /proofs/7/verification_scope; canonical SHA-256: adfd4e85cfa3144875bb360d8a3c38de8b56a0b629e1e3694ea3232adebf20b0

Source-statement and target-contract mapping only. The manuscript theorem is a cited premise, not an independently re-proved or Lean-verified theorem.

#### Native field: evidence_status

Native pointer: /proofs/7/evidence_status; canonical SHA-256: 1578f14f82bb0083a1ecc7fd9b03327d36593f19dd602231105ef79da610c4ca

source_reported_contract_reviewed

### Native proof: BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

Native pointer: /proofs/8; canonical SHA-256: 7920fff765f54976539154ade0045c374b72c9307cb775d3255da3149d7ae876

#### Native field: kind

Native pointer: /proofs/8/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/8/title; canonical SHA-256: 84918eb8f272c76e657b7f663ec3b52663a50146bbafe297b5e4d202d75a33c6

Constant lower-block fine-accuracy bracket

#### Native field: statement

Native pointer: /proofs/8/statement; canonical SHA-256: 2e8bbaf2491f62eb55d7d1c868156ea7b8f32ddddf2e5217fdd6bd3df1abe922

On K, $cQ_{\rm aff}(\sqrt\kappa+V)\le Q^*\le CQ_{\rm aff}(\sqrt\kappa\Lambda_{\log}+V)$, $Q_{\rm aff}=L\kappa^2\Delta/\varepsilon^2$, $V=\kappa^2\sigma_f^2/\varepsilon^2$, $\Lambda_{\log}=1+\log(2+Q_{\rm aff}+\kappa L/\varepsilon)$.

#### Native field: proof

Native pointer: /proofs/8/proof; canonical SHA-256: e3d193326b91f7854eec0a3299cfacede6f48e05490dcf3f7ce59da1cb9d94f7

At rho=0 the lower Hessian blocks are constant, y*(x) is affine, and its graph has operator norm at most kappa. With L_f=L this gives Lip(grad Phi)<=L kappa^2. Consequently Lambda_Phi>=L kappa^2 leaves the full source affine class unchanged. Theorem 7.1 additionally requires exact public initialization R0=0. Its upper uses two separately charged fresh calls for each matrix product, with displacement max{1,sqrt(2)sigma_g/r}; these displacements are finite for every fixed finite noise budget and precision. Native global variance and unrestricted finite queries allow this operation, so no hidden sigma_g-dependent cost or common sample is introduced. The lower construction respects the same curvature promise. The source constants are uniform in all public budgets and finite dimensions; the displayed single dimensionless logarithm is retained. There is no extension to R0>0 or to the intermediate-accuracy range.

#### Native field: source_refs

Native pointer: /proofs/8/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/8/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: evidence_refs

Native pointer: /proofs/8/evidence_refs; canonical SHA-256: 750372ba1e883ca556d15c71dfc281303ae4619bf1ecb856a2834d9dc0a1edf5

#### Native item 1

Native pointer: /proofs/8/evidence_refs/0; canonical SHA-256: 48d85f8396cae11b3b9eddf0c73991bb8b691d168171df3020cd1282c580bdb9

BL_SPEC_joint_expected_cost__main__e_constant_blocks_20261126

#### Native field: verification_scope

Native pointer: /proofs/8/verification_scope; canonical SHA-256: adfd4e85cfa3144875bb360d8a3c38de8b56a0b629e1e3694ea3232adebf20b0

Source-statement and target-contract mapping only. The manuscript theorem is a cited premise, not an independently re-proved or Lean-verified theorem.

#### Native field: evidence_status

Native pointer: /proofs/8/evidence_status; canonical SHA-256: 1578f14f82bb0083a1ecc7fd9b03327d36593f19dd602231105ef79da610c4ca

source_reported_contract_reviewed

### Native proof: BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

Native pointer: /proofs/9; canonical SHA-256: 8d8d7a8b7246a18a894b84b4142607cd1c18f4e2c196aaf2a670d051741afdd4

#### Native field: kind

Native pointer: /proofs/9/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/9/title; canonical SHA-256: 1e3bebab9cc7e0a64437e1978a2289dbdafc0c0abda6a0603b12d59a1958c463

Affine and perfectly conditioned zero-call boundaries

#### Native field: statement

Native pointer: /proofs/9/statement; canonical SHA-256: 358c4a4aa737d8c53a000d140c84aa9621517c86c6cf57a5fc28afb3c4b3f17e

On Z, $Q^*=0$. On A, $Q^*\ge(1-\varepsilon/S_0)(1+\sigma_f^2/(16S_0^2))>0$.

#### Native field: proof

Native pointer: /proofs/9/proof; canonical SHA-256: 8c7229c008574b68953328d0dcb15e7224f0ea697242ce2590ba2837614fd99a

The source zero-call algorithm returns the public x0 and is feasible for every independent curvature subclass when epsilon is at least the displayed source risk threshold. Nonnegativity of expected cost proves Q*=0 on Z, without any reverse class inclusion. For necessity at rho=0, the source witnesses have L-smooth f and an affine graph of norm at most kappa, hence reduced smoothness at most L kappa^2; they are admissible in the target when Lambda_Phi>=L kappa^2. This proves both the exact threshold and the fractional expected-cost activation lower bound only under that nonbinding guard. At kappa=1 the lower response is constant, the reduced objective is L-smooth, and the source exact threshold is sqrt(2LDelta); its necessity transfers under Lambda_Phi>=L. Tighter curvature subclasses retain the sufficient zero statement but not an unproved exact necessity. Old effective-curvature zero region E remains unchanged and has precedence.

#### Native field: source_refs

Native pointer: /proofs/9/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/9/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: evidence_refs

Native pointer: /proofs/9/evidence_refs; canonical SHA-256: dd9205534ee44d9edfdd6f8c9fd9ffb59f5e9fe650e0c4615053ee8f90d84d48

#### Native item 1

Native pointer: /proofs/9/evidence_refs/0; canonical SHA-256: ae92ed5872921e48f71af79d8a3b4f1292394c431b1b6bf7811152488d1a2b13

BL_SPEC_joint_expected_cost__main__e_zero_activation_20261126

#### Native field: verification_scope

Native pointer: /proofs/9/verification_scope; canonical SHA-256: adfd4e85cfa3144875bb360d8a3c38de8b56a0b629e1e3694ea3232adebf20b0

Source-statement and target-contract mapping only. The manuscript theorem is a cited premise, not an independently re-proved or Lean-verified theorem.

#### Native field: evidence_status

Native pointer: /proofs/9/evidence_status; canonical SHA-256: 1578f14f82bb0083a1ecc7fd9b03327d36593f19dd602231105ef79da610c4ca

source_reported_contract_reviewed

### Native proof: BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

Native pointer: /proofs/10; canonical SHA-256: b8717e585458b473416f32705bbf003374aad1fd577cde2f9ae353a1385a6e55

#### Native field: kind

Native pointer: /proofs/10/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/10/title; canonical SHA-256: 31d7ff73b264906944bfafd2f570538867d4466e73d42ea5e25d00daeaf8c032

Sixth-power accuracy law with all structural budgets fixed

#### Native field: statement

Native pointer: /proofs/10/statement; canonical SHA-256: 35403bf5198ee6930f65340a5c2b5fad823cde760be7f8e0ae048ac449bded87

For a fixed admissible interior tuple $P$, $c_P\varepsilon^{-6}\le Q^*(\varepsilon;P)\le C_P\varepsilon^{-6}$ for $0<\varepsilon<\varepsilon_P$.

#### Native field: proof

Native pointer: /proofs/10/proof; canonical SHA-256: e121f3cad7fba20e84ec60e5e9264e3f0a1f3e4bea12dc7577530b9447304ebb

Take L_f=L_g=C_f=L, L>mu>0, rho>0, Delta>0 and sigma_g>0. Fix every primitive structural budget, including the independent Lambda_Phi, with Lambda_Phi>=B_Phi. The universal-curvature proof then makes the source class identical to the target class on this slice. The source expected-norm guarantee and expected stopping-cost convention match the native model. The native fixed-accuracy quantity varies epsilon only; dimensions remain under the arbitrary finite-dimensional supremum, not inside the fixed tuple. Constants and the cutoff may depend on the fixed tuple. The lower witness uses one inner variable and outer dimension O_P(epsilon^-2 log(1/epsilon)), exact upper gradients and exact initialization, all allowed by larger public noise and initialization budgets. This is an accuracy-only law and does not determine the powers of structural budgets in the joint quantity.

#### Native field: source_refs

Native pointer: /proofs/10/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/10/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: evidence_refs

Native pointer: /proofs/10/evidence_refs; canonical SHA-256: 61fe3cb1cc7123df789b4b9732d997115636483758dbe1ee372fc32e314a9377

#### Native item 1

Native pointer: /proofs/10/evidence_refs/0; canonical SHA-256: 596076297956919b4a0b448e4473279eb4a2f9aaa640d329f660470f8260f004

BL_SPEC_joint_expected_cost__main__e_fixed_accuracy_20261126

#### Native field: verification_scope

Native pointer: /proofs/10/verification_scope; canonical SHA-256: adfd4e85cfa3144875bb360d8a3c38de8b56a0b629e1e3694ea3232adebf20b0

Source-statement and target-contract mapping only. The manuscript theorem is a cited premise, not an independently re-proved or Lean-verified theorem.

#### Native field: evidence_status

Native pointer: /proofs/10/evidence_status; canonical SHA-256: 1578f14f82bb0083a1ecc7fd9b03327d36593f19dd602231105ef79da610c4ca

source_reported_contract_reviewed

### Native proof: BL_SPEC_joint_expected_cost__main__proof_endpoint_structure_contract_20261126

Native pointer: /proofs/11; canonical SHA-256: f9a4a487e4545c2b218a40c84cb1c61e443bb3310f5e8dddaace7c4c786a841c

#### Native field: kind

Native pointer: /proofs/11/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: title

Native pointer: /proofs/11/title; canonical SHA-256: d6807771c7fb73efebd61f748cc83ac16fcba57fd24817268c942d615532406d

Perfect-conditioning equivalence and uniform-noise initialization classification

#### Native field: statement

Native pointer: /proofs/11/statement; canonical SHA-256: b50455f798a1641b5cbba5522db11be12cf5468594d37f8423ad3fcc7dada021

Perfect conditioning gives a constant lower response and a charged offset-shrinkage risk upper bound. A separate supremum over all finite lower-noise budgets has the regional initialization finiteness transition in Theorem 10.4.

#### Native field: proof

Native pointer: /proofs/11/proof; canonical SHA-256: a449161297d8c3d6e5bb24d5ddf91153c6ba1cb3d95c59c84616263f5145547a

For kappa=1 and common budgets, the graph is constant and the reduced objective is L-smooth. With R0=0, the source constructs oracle simulations in both directions preserving expected risk and expected calls for ordinary L-smooth nonconvex stochastic first-order optimization. The reverse embedding satisfies the target independent curvature promise when Lambda_Phi>=L. The charged shrinkage algorithm is an upper statement for every subclass without this extra lower guard. In the rho=0 initialization transition, source lower witnesses again have an affine graph of norm at most kappa and L-smooth f, so Lambda_Phi>=L kappa^2 suffices for their inclusion. The quantity N_infty has an additional outer supremum over all finite sigma_g. Its divergence does not assert an infinite complexity at any one fixed finite sigma_g. All branch equality conditions are retained in the structural record.

#### Native field: source_refs

Native pointer: /proofs/11/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /proofs/11/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: evidence_refs

Native pointer: /proofs/11/evidence_refs; canonical SHA-256: 286c31cff248207d42b5db7c53fe1531600bbd02611eb222fb71cb410f3b1308

#### Native item 1

Native pointer: /proofs/11/evidence_refs/0; canonical SHA-256: ffa4b3bcafd3c5e175fec72f2f0ec96a7e23c61eebb22cd7372388e4bf71d995

BL_SPEC_joint_expected_cost__main__e_endpoint_structure_20261126

#### Native field: verification_scope

Native pointer: /proofs/11/verification_scope; canonical SHA-256: adfd4e85cfa3144875bb360d8a3c38de8b56a0b629e1e3694ea3232adebf20b0

Source-statement and target-contract mapping only. The manuscript theorem is a cited premise, not an independently re-proved or Lean-verified theorem.

#### Native field: evidence_status

Native pointer: /proofs/11/evidence_status; canonical SHA-256: 1578f14f82bb0083a1ecc7fd9b03327d36593f19dd602231105ef79da610c4ca

source_reported_contract_reviewed

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: a4e3669985eb31b772b6469a0b35cf6ec63b2ab894114af3efb9f8fb7cb46ac2

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: 4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce

Native value (number): 3

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

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 000bbfdbeb98f3b94116fa5d554c4cd58d97379d0ebc8928954f39eb18b1b1af

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

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 2a2589ce003b79b82877dc1d8b1edf567528430d4c235d71b4c35104df8afd00

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 9765327f001cddfac6794b74d8bfb40906c25dfcb81acc559a82869d0163d3cd

BL_SPEC_joint_expected_cost__main__c_source_zero_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 98089e6d36f78e9766c9ea34d5acb3611f3a92cd81c5eb102095d924ffc7d08b

0

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 4679eead843c698bd20e6275d845c40e4aaa9599abc9eaa543d16690972d9ff2

Exact zero cost.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 4679eead843c698bd20e6275d845c40e4aaa9599abc9eaa543d16690972d9ff2

Exact zero cost.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: c5318ba0416dd9e6c57f346e6d3e1b03f43c2880391576abc1543dc1a22cf8dd

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 33d57e523ac50e11451fb58d46f5320ad6227c190a2e8bea6a832de71e394495

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: ed83cdf798d05b5c416ce9ca1b546ecf5c3ee2a576ab561a9c6ce4c8ce679547

BL_SPEC_joint_expected_cost__main__b_source_zero_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: f864796276d2399f3e4f00df46df19d0d361e5280819cd21bfabd09c2878b2d2

The complete Z guard, and not E.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: f864796276d2399f3e4f00df46df19d0d361e5280819cd21bfabd09c2878b2d2

The complete Z guard, and not E.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 4730ea76decbce810a3d5481581b10258efd1a950eebd55a5c7a8f8f327135f9

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 8920b10739b1ae8e2876aae0c57c07ab2ec89a1e20133ab1da0b36b70c9f88f0

BL_SPEC_joint_expected_cost__main__b_source_zero_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: f864796276d2399f3e4f00df46df19d0d361e5280819cd21bfabd09c2878b2d2

The complete Z guard, and not E.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: f864796276d2399f3e4f00df46df19d0d361e5280819cd21bfabd09c2878b2d2

The complete Z guard, and not E.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 3

Native pointer: /joint_analysis/comparisons/2; canonical SHA-256: 4c998584f5b91de17c73cd3e7698cb1bb81eaac5806b1cb4dd251bed1ebec550

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/2/comparison_id; canonical SHA-256: 5790a340058e7b9b2b200d448f4947ee6f1506771c1c1309070d3f1ea171bb34

BL_SPEC_joint_expected_cost__main__c_curvature_old_n_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/2/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/2/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/2/upper_envelope; canonical SHA-256: 48e8450c2d07e850ab8abddfeb53224cfd61dbeac3cbbc1d1ddd0928156687ab

\min\left\{\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/2/lower_envelope; canonical SHA-256: 6b78769385766c770316379cb4df947bb0901e08b657050308044835be40f783

\max\left\{\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right),\ \Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})\right\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/2/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/2/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/2/bound_uses; canonical SHA-256: 7263a6c5d2bb3848ff187c7c89b9b63631401374beb7d8aca93c1f3d10698b7a

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0; canonical SHA-256: b08a857a8dacfce58ca6ce1478c9049d06098e77c5747388b3a2792c483fcc0b

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/bound_id; canonical SHA-256: 4d7eaae3609ea1b1d252fa370369e3335a79801b315bce335b820ea13634c7ea

BL_SPEC_joint_expected_cost__main__b_curvature_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/adopted_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/validity_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/2/bound_uses/1; canonical SHA-256: 80735de52d6ab5f80abe4696a8a86a4fa87551da1a814d4618557ebbfb7431ef

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/adopted_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/validity_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/2/bound_uses/2; canonical SHA-256: a7b03cfd37d88e5e65aec8bfafcde10df8ff9ecb64d60b3763ef65ea86f31014

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/bound_id; canonical SHA-256: 48026746550b83fccffc0a6712faf50fcb925dada190809d2833b0a40793c9b8

BL_SPEC_joint_expected_cost__main__b_curvature_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/adopted_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/validity_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 4

Native pointer: /joint_analysis/comparisons/2/bound_uses/3; canonical SHA-256: bbfc410b471ba718b3dd96db5030e7af2a9711b4bef7ad6a5892a4d4cd30d2dd

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/adopted_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/validity_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/3/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 5

Native pointer: /joint_analysis/comparisons/2/bound_uses/4; canonical SHA-256: 577d2ea64927cda74eef32cf51c9f994108385c05758061331ddbdc899562092

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/bound_id; canonical SHA-256: c66acb120133c44f01bd9d82ef1ae8bdd967e827da50c4973288c428545d99da

BL_SPEC_joint_expected_cost__main__b_matching_noise_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/adopted_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/validity_region; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/2/bound_uses/4/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/2/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/2/constant_dependencies; canonical SHA-256: 271dbef466528e5e7f6fb9f9d0ec1b04ec9d01c0f1f9891e6561f45488c5b8e2

#### Native item 1

Native pointer: /joint_analysis/comparisons/2/constant_dependencies/0; canonical SHA-256: 6129a6981d3bddce47336e6fb2311600146a78937a31496496a8c6b5d82a863a

BL_SPEC_joint_expected_cost_p_fixed_curvature_multiplier_20261126

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/2/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 4

Native pointer: /joint_analysis/comparisons/3; canonical SHA-256: 20d941da81caeaceb1a77a27bea9020c1864541de7ba7cd2c555948614f2c948

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/3/comparison_id; canonical SHA-256: 95f8b1e32b721fad23cce5f72e863a595c416b48589a91b44a23bad341800910

BL_SPEC_joint_expected_cost__main__c_curvature_old_s_remaining_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/3/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/3/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/3/upper_envelope; canonical SHA-256: 48e8450c2d07e850ab8abddfeb53224cfd61dbeac3cbbc1d1ddd0928156687ab

\min\left\{\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/3/lower_envelope; canonical SHA-256: d73f0673028b92344d8b69e2ae8514cd8bf9b38936dfeb2da7cf1fa4a6a022c7

\max\left\{\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)\right\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/3/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/3/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/3/bound_uses; canonical SHA-256: 75e5e7f8c3200c9a371170b2a64c8f18953692536b0e891285b3ee39a9066aa4

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0; canonical SHA-256: b3327f9f94d270c2a514c67c0c40d5ee00866758fcb6cb33fa80674e1aaf2f0f

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/bound_id; canonical SHA-256: 4d7eaae3609ea1b1d252fa370369e3335a79801b315bce335b820ea13634c7ea

BL_SPEC_joint_expected_cost__main__b_curvature_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/adopted_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/validity_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/3/bound_uses/1; canonical SHA-256: 61acf30f03efb0ed6a640a91d799a7763e6918e4f5811aa2a48c8e55ed837e7a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/adopted_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/validity_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/3/bound_uses/2; canonical SHA-256: 90194578fbf587a6e7d6eccc0f002d7a8cb48cf968e6a553dfc8448703714010

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/bound_id; canonical SHA-256: 48026746550b83fccffc0a6712faf50fcb925dada190809d2833b0a40793c9b8

BL_SPEC_joint_expected_cost__main__b_curvature_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/adopted_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/validity_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 4

Native pointer: /joint_analysis/comparisons/3/bound_uses/3; canonical SHA-256: fdc168c4e2cec015d43d330540001481b6d5c6cee765c70fd02c44e8f796b956

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/adopted_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/validity_region; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/3/bound_uses/3/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/3/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/3/constant_dependencies; canonical SHA-256: 271dbef466528e5e7f6fb9f9d0ec1b04ec9d01c0f1f9891e6561f45488c5b8e2

#### Native item 1

Native pointer: /joint_analysis/comparisons/3/constant_dependencies/0; canonical SHA-256: 6129a6981d3bddce47336e6fb2311600146a78937a31496496a8c6b5d82a863a

BL_SPEC_joint_expected_cost_p_fixed_curvature_multiplier_20261126

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/3/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 5

Native pointer: /joint_analysis/comparisons/4; canonical SHA-256: 045c64cdd1787f74aa4d93c8dd61a33ce594e376f51a372ec26e4758964e0bc1

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/4/comparison_id; canonical SHA-256: 6c1c58c1253ec3c9f6144a7e5eeaea76ce053c986171ef9f361a51f0154a5cfd

BL_SPEC_joint_expected_cost__main__c_curvature_outside_old_s_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/4/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/4/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/4/upper_envelope; canonical SHA-256: 48e8450c2d07e850ab8abddfeb53224cfd61dbeac3cbbc1d1ddd0928156687ab

\min\left\{\widetilde O\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/4/lower_envelope; canonical SHA-256: fe11e590b4a1f0d70788d74258762f0804e75800df3cd13884a00950053ab479

\Omega\!\left(\frac{L\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/4/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/4/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/4/bound_uses; canonical SHA-256: f0653d9a0851a886bc7e8bfa377c48cf6bfe0925e6c888ff594252749dccbefd

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0; canonical SHA-256: 5aadcbb3d53ba1d2a150ee5105b53f598827149170afd6493372d6320327fda4

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/bound_id; canonical SHA-256: 4d7eaae3609ea1b1d252fa370369e3335a79801b315bce335b820ea13634c7ea

BL_SPEC_joint_expected_cost__main__b_curvature_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/adopted_region; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/validity_region; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/4/bound_uses/1; canonical SHA-256: 82c9c60b111fb059806528de34ac826a50a55efbaecda7c9499954cbfe154e49

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/adopted_region; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/validity_region; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/4/bound_uses/2; canonical SHA-256: 0b47f62d5326d6b4dea83eed0deeaaf31796b9eee11662f9385790ecf5e6cb5a

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/bound_id; canonical SHA-256: 48026746550b83fccffc0a6712faf50fcb925dada190809d2833b0a40793c9b8

BL_SPEC_joint_expected_cost__main__b_curvature_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/adopted_region; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/validity_region; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/4/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/4/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/4/constant_dependencies; canonical SHA-256: 271dbef466528e5e7f6fb9f9d0ec1b04ec9d01c0f1f9891e6561f45488c5b8e2

#### Native item 1

Native pointer: /joint_analysis/comparisons/4/constant_dependencies/0; canonical SHA-256: 6129a6981d3bddce47336e6fb2311600146a78937a31496496a8c6b5d82a863a

BL_SPEC_joint_expected_cost_p_fixed_curvature_multiplier_20261126

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/4/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 6

Native pointer: /joint_analysis/comparisons/5; canonical SHA-256: a5c133bee5740eb79c46d241bcf8b40137ef47782113572db3124ca7e8aa1e6c

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/5/comparison_id; canonical SHA-256: fc5b4ad329b6bb4e06961fbdb76bfe3cf9c15f1be2ed16c6530d9db641601666

BL_SPEC_joint_expected_cost__main__c_joint_old_n_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/5/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/5/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/5/upper_envelope; canonical SHA-256: c3a264a21c7a8df3e2717ffdf5ad29108d14f1ce8c6c4ba11fae5da9b8162cfa

\min\left\{\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/5/lower_envelope; canonical SHA-256: 832ca114f8cc1e2f3d085b404c30857bb833f21e9c0fcb8b1c856422571aed80

\max\left\{\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right),\ \Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})\right\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/5/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/5/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/5/bound_uses; canonical SHA-256: 8745d98d4bab39f5fca8f3205433e015501bc02bf24fc331f705b63c0dfaca20

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0; canonical SHA-256: 1e1723b9263d8e367781a237f86f0b928422d0c52541edbaf795d63a087373e9

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/bound_id; canonical SHA-256: 0dbf1f8df1b8103aaa4fbd571ba8fcc4424a8894a202b3117bc56ecbffa489e8

BL_SPEC_joint_expected_cost__main__b_joint_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/adopted_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/validity_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/5/bound_uses/1; canonical SHA-256: 7d8e92bd1d362dde5e3e4a50b7a10a84942c7e0d6c3a80929410c5ea655ba203

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/adopted_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/validity_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/5/bound_uses/2; canonical SHA-256: 4e881678f9fd2488ba4c3dda484516dff7c2fd726e592da9013df0ba25745b75

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/bound_id; canonical SHA-256: 81a2e38f18361a22f545e5d196c3706082517f1eec3155c02b432d002a8a8b3b

BL_SPEC_joint_expected_cost__main__b_joint_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/adopted_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/validity_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 4

Native pointer: /joint_analysis/comparisons/5/bound_uses/3; canonical SHA-256: 27050d37d8530b24f1332617b0c350a7ab423996067024f2c301dba874dfc592

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/adopted_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/validity_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/3/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 5

Native pointer: /joint_analysis/comparisons/5/bound_uses/4; canonical SHA-256: f11cc7b8894c7e3039f2e03674671c9a5955807305a18a00cee59487fd159c89

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/bound_id; canonical SHA-256: c66acb120133c44f01bd9d82ef1ae8bdd967e827da50c4973288c428545d99da

BL_SPEC_joint_expected_cost__main__b_matching_noise_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/adopted_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/validity_region; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/5/bound_uses/4/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/5/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/5/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/5/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/5/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 7

Native pointer: /joint_analysis/comparisons/6; canonical SHA-256: db4cb58e71f296dc54ed1efb2eef67ba76ea4ca7e8c795e59bf104aea4ea2a18

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/6/comparison_id; canonical SHA-256: 3fd04f216821f990a836079ddbe29196b9f2cfb92b2cc20d2d5404e540285af6

BL_SPEC_joint_expected_cost__main__c_joint_old_s_remaining_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/6/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/6/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/6/upper_envelope; canonical SHA-256: c3a264a21c7a8df3e2717ffdf5ad29108d14f1ce8c6c4ba11fae5da9b8162cfa

\min\left\{\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/6/lower_envelope; canonical SHA-256: 4afada079a816b5abca0a68742df90ce3ca0e83a2edd55adef606c13db610a44

\max\left\{\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right),\ \Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)\right\}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/6/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/6/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/6/bound_uses; canonical SHA-256: bdbf141081d9d43a04a92360eede525767afc20bdd7232e359f3413cf449e782

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0; canonical SHA-256: 7cd0697253708ee8cf6afd41c5fa17765bd8fa6d6b933624008529870108d8b8

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/bound_id; canonical SHA-256: 0dbf1f8df1b8103aaa4fbd571ba8fcc4424a8894a202b3117bc56ecbffa489e8

BL_SPEC_joint_expected_cost__main__b_joint_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/adopted_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/validity_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/6/bound_uses/1; canonical SHA-256: 8ca4228c85929e1b841721cf6d6b13a9f413b16fdb38af9d78e5174567eeb631

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/adopted_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/validity_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/6/bound_uses/2; canonical SHA-256: 07f6e8852f0b439a9aeb952839209863b2ed6bb020e6b72f1d37418e184bd8ec

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/bound_id; canonical SHA-256: 81a2e38f18361a22f545e5d196c3706082517f1eec3155c02b432d002a8a8b3b

BL_SPEC_joint_expected_cost__main__b_joint_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/adopted_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/validity_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 4

Native pointer: /joint_analysis/comparisons/6/bound_uses/3; canonical SHA-256: 622b3b82e24c0672dac935e45c5cd2ef0d4853ee12df0e39ce351e1b05488b31

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/adopted_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/validity_region; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/6/bound_uses/3/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/6/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/6/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/6/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/6/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 8

Native pointer: /joint_analysis/comparisons/7; canonical SHA-256: 745c2d17eb21bb67440167642db3528e2381705da720c09f122365c017601b89

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/7/comparison_id; canonical SHA-256: 68d0fea9da35c8f77d4a163d1dae56860165b099d3370bf8ec644cdfd3d37f94

BL_SPEC_joint_expected_cost__main__c_joint_outside_old_s_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/7/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/7/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/7/upper_envelope; canonical SHA-256: c3a264a21c7a8df3e2717ffdf5ad29108d14f1ce8c6c4ba11fae5da9b8162cfa

\min\left\{\widetilde O\!\left(\frac{L\chi\kappa^{5/2}\Delta}{\varepsilon^2}+\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L^3\theta^2\chi\kappa^8\sigma_g^2\Delta}{\varepsilon^6}\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/7/lower_envelope; canonical SHA-256: 495200fd1c2d9675e8734df7aed528b1af0917cbe6bcb07746e2dc65934c8c96

\Omega\!\left(\frac{L\kappa^4\sigma_f^2\Delta}{\varepsilon^4}+\frac{L\chi\kappa^{5/2}\Delta\varepsilon^{-2}+L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}}{[\log(2+\theta)]^{p_{\log}}}\right)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/7/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/7/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/7/bound_uses; canonical SHA-256: a47eed156bf310cafe21f9e60cfffdfbd391eccf06014dcf76ccc01f627dfdaf

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0; canonical SHA-256: 6ac1101128995b0caaacbb1174fac7a5eeebc96216185d30c4781e347228d2d3

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/bound_id; canonical SHA-256: 0dbf1f8df1b8103aaa4fbd571ba8fcc4424a8894a202b3117bc56ecbffa489e8

BL_SPEC_joint_expected_cost__main__b_joint_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/adopted_region; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/validity_region; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/7/bound_uses/1; canonical SHA-256: 44b01c9c1e8ccb981eb3c81dcc99d07094273ffedcc243ede4d8e9b88c45524d

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/adopted_region; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/validity_region; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/7/bound_uses/2; canonical SHA-256: f766b07d135669486deb31800a5e66ee3c35babab91f9c64ecca9b0cbb9680f1

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/bound_id; canonical SHA-256: 81a2e38f18361a22f545e5d196c3706082517f1eec3155c02b432d002a8a8b3b

BL_SPEC_joint_expected_cost__main__b_joint_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/adopted_region; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/validity_region; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/mapping_proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/7/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/7/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/7/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/7/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/7/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 9

Native pointer: /joint_analysis/comparisons/8; canonical SHA-256: 5ec541acdf5bf7cd70e9ed30fcfe7c4808e8d57ff113869719ca71a4de0a8ed3

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/8/comparison_id; canonical SHA-256: 3483eda65f1a0bb74dd035dede167e74629ad7761f22a00b4632e0166d4a0f44

BL_SPEC_joint_expected_cost__main__c_constant_blocks_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/8/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/8/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/8/upper_envelope; canonical SHA-256: 94964236a140a4235afb00acbd9b428d602d523c03626a888019c8483b2c533f

\min\left\{O\!\left(\frac{L\kappa^2\Delta}{\varepsilon^2}\left[\sqrt\kappa\left(1+\log\left(2+\frac{L\kappa^2\Delta}{\varepsilon^2}+\frac{\kappa L}{\varepsilon}\right)\right)+\frac{\kappa^2\sigma_f^2}{\varepsilon^2}\right]\right),\ \widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)\right\}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/8/lower_envelope; canonical SHA-256: e35efba15417c85dca240107d743c749d09174c265dd85b2c968f34138c98793

\Omega\!\left(\frac{L\kappa^2\Delta}{\varepsilon^2}\left[\sqrt\kappa+\frac{\kappa^2\sigma_f^2}{\varepsilon^2}\right]\right)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/8/gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/8/remaining_gap; canonical SHA-256: 3bee4e51cf8b5bd8aa969b034094f51a97a90996838cb60dd53c3a359749d4a9

Only the stated source logarithmic factors remain; no matching R0 dependence is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/8/bound_uses; canonical SHA-256: 0946f1087b96563c92b6073986de8d880f76149ffa162f7beab43fe0122d0250

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/0; canonical SHA-256: d3fc460fa192b83ec6ccb5a05087dcc1551052ad7c5d4692b789fc2708d976e7

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/bound_id; canonical SHA-256: 4df34e14d8aa539a488a08f035f0e108107220b393a67c33eeb1647b0864f958

BL_SPEC_joint_expected_cost__main__b_constant_blocks_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/adopted_region; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/validity_region; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6b331f2c681d05194a80b1067879f9112282e7a4b3de8eacdc2808ad900f5c69

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: e3be7dde89be4039356e7db3ae038bd2124a4b6174e7e75b1f56a5a43a54379a

BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/8/bound_uses/1; canonical SHA-256: 71c0b2ad3922f83f37f519300ca89a3222bc8008bbaf352a31d02d8b0d5fd01d

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/adopted_region; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/validity_region; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6b331f2c681d05194a80b1067879f9112282e7a4b3de8eacdc2808ad900f5c69

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: e3be7dde89be4039356e7db3ae038bd2124a4b6174e7e75b1f56a5a43a54379a

BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 3

Native pointer: /joint_analysis/comparisons/8/bound_uses/2; canonical SHA-256: be4300ece11615aee358b700a2ce9163274aa35e7929d733fef4166a0d9e981d

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/bound_id; canonical SHA-256: 50173b8587a50f608a8a075aeeb0747b5d52bca4631926f133a98a964bafdf4e

BL_SPEC_joint_expected_cost__main__b_constant_blocks_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/adopted_region; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/validity_region; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/mapping_proof_refs; canonical SHA-256: 6b331f2c681d05194a80b1067879f9112282e7a4b3de8eacdc2808ad900f5c69

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: e3be7dde89be4039356e7db3ae038bd2124a4b6174e7e75b1f56a5a43a54379a

BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/8/bound_uses/2/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/8/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/8/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/8/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/8/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 10

Native pointer: /joint_analysis/comparisons/9; canonical SHA-256: f7de24cb24223db2b65843ff87c0ce25bb0e6e36408be30d6d00c52839d09623

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/9/comparison_id; canonical SHA-256: 9558f1762a0daeaa51abc9891154f8a18ce5ac9fd7e3bb681e7e1367a015ce7e

BL_SPEC_joint_expected_cost__main__c_affine_activation_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/9/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/9/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/9/upper_envelope; canonical SHA-256: 10fb29dcc6f63dbf6cdba8e16ac2e873415fa393fbb69838bc77bff84f549f82

\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/9/lower_envelope; canonical SHA-256: f6de9aac3d4fde7b2296933e8371624d34b456d7c500569e69ad28c99c248edf

\left(1-\frac{\varepsilon}{S_0}\right)\left(1+\frac{\sigma_f^2}{16S_0^2}\right)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/9/gap; canonical SHA-256: 7f154e61944254d3a809f042dcc58e09a17079db170e7b86500a795c7b442f6b

The displayed minimum upper and maximum lower are retained; no matching joint rate is claimed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/9/remaining_gap; canonical SHA-256: 7f154e61944254d3a809f042dcc58e09a17079db170e7b86500a795c7b442f6b

The displayed minimum upper and maximum lower are retained; no matching joint rate is claimed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/9/bound_uses; canonical SHA-256: 401f9e23a09e7740e33e59de0621cb0626deea218a5cb8f917dd93f9e8d9a5a0

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/0; canonical SHA-256: d8a45f0fbfd10dba20d7dd3431d634ead1d1fa67f0bf8775cfc9bc4f8dbabadc

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/adopted_region; canonical SHA-256: 9076ef64ebd35f00b2d02914c6fadb33a669316629ebce96a04e4493a724ecc8

The complete A guard; not E; not Z; not C; not J; not K.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/validity_region; canonical SHA-256: 9076ef64ebd35f00b2d02914c6fadb33a669316629ebce96a04e4493a724ecc8

The complete A guard; not E; not Z; not C; not J; not K.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/9/bound_uses/1; canonical SHA-256: 60ff4655e1ce2a11796ccbc27bf2f5b5f5dba7e14da346ca7e09a75007fe9c54

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/bound_id; canonical SHA-256: 6706fab5abc9e126df2b3423af4eeb158dd0f545784bec459360ebe9e1ef7b12

BL_SPEC_joint_expected_cost__main__b_affine_activation_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/adopted_region; canonical SHA-256: 9076ef64ebd35f00b2d02914c6fadb33a669316629ebce96a04e4493a724ecc8

The complete A guard; not E; not Z; not C; not J; not K.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/validity_region; canonical SHA-256: 9076ef64ebd35f00b2d02914c6fadb33a669316629ebce96a04e4493a724ecc8

The complete A guard; not E; not Z; not C; not J; not K.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/mapping_proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/9/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/9/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/9/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/9/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/9/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 11

Native pointer: /joint_analysis/comparisons/10; canonical SHA-256: 8a7c14a68a81cb7fafb0b8f701276fbce4afe1f4fa665edc8c62cd1273e00d2c

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/10/comparison_id; canonical SHA-256: 2d7df47383a40ba4eba5e63c606b8d011ae809c160ec7b5c4638e9c6bafebd53

BL_SPEC_joint_expected_cost__main__c_old_noise_remainder_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/10/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/10/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/10/upper_envelope; canonical SHA-256: c7fcc261a27ba0aa6091e2d05e004635e7985109123be9794a8a6e95c6cddc36

\widetilde O(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/10/lower_envelope; canonical SHA-256: bbe63ee0a72fd99b885d66c18650b9ed4f11794bbb7e41ce7055bf0010e1b3b2

\Omega(\theta^2\kappa^8\sigma_g^2L^3\Delta\varepsilon^{-6})

#### Native field: gap

Native pointer: /joint_analysis/comparisons/10/gap; canonical SHA-256: 0bea534dc53df6284033496cb8cc349ff8cda59bb74e42783003a1b30bc16857

Only the source upper logarithms remain; accuracy, condition-number, lower-noise and gap powers match on N.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/10/remaining_gap; canonical SHA-256: 0bea534dc53df6284033496cb8cc349ff8cda59bb74e42783003a1b30bc16857

Only the source upper logarithms remain; accuracy, condition-number, lower-noise and gap powers match on N.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/10/bound_uses; canonical SHA-256: 81ffc6810fa0fc8ed8e6a630f5e50f3d6cd880aa0da2da14e1974888aa4dc1f9

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/0; canonical SHA-256: 458aca484aef6f8680906d448dd4e4b4a9c06f544e45afae2f61902cdd2bbbef

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/bound_id; canonical SHA-256: c40402aa1a3425761a7b3e9d0a103e7674761f5429e25d6ff377e08fcc8878a8

BL_SPEC_joint_expected_cost__main__b_matching_noise_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/adopted_region; canonical SHA-256: 47c5685a34425a429b169c6ec2d2f26ef78ff13212810627e15206de8be483b5

(The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.) and not E; not Z; not C; not J; not K; not A.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/validity_region; canonical SHA-256: 47c5685a34425a429b169c6ec2d2f26ef78ff13212810627e15206de8be483b5

(The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.) and not E; not Z; not C; not J; not K; not A.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs; canonical SHA-256: 6f84a64a2620e51e082cc992c58e3814c6541d079e8e1cab7ba38dcc90798935

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: bd96cf5f3776dc90e71e8a65cfbc21b4abe93cfc39f61ae3f086f7a7769d8d97

BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/mapping_proof_refs/1; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/bound_uses/1; canonical SHA-256: 26adbd87b15f20ba65d609f0345a29ce802943f7c2f3aae6a999d26dec15d705

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/bound_id; canonical SHA-256: c66acb120133c44f01bd9d82ef1ae8bdd967e827da50c4973288c428545d99da

BL_SPEC_joint_expected_cost__main__b_matching_noise_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/adopted_region; canonical SHA-256: 47c5685a34425a429b169c6ec2d2f26ef78ff13212810627e15206de8be483b5

(The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.) and not E; not Z; not C; not J; not K; not A.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/validity_region; canonical SHA-256: 47c5685a34425a429b169c6ec2d2f26ef78ff13212810627e15206de8be483b5

(The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.) and not E; not Z; not C; not J; not K; not A.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/mapping_proof_refs; canonical SHA-256: ff52ab9bd593cce3178c83a3eb8f6e78cc94df19dedb580140d169f6889567af

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: bd96cf5f3776dc90e71e8a65cfbc21b4abe93cfc39f61ae3f086f7a7769d8d97

BL_SPEC_joint_expected_cost__main__proof_matching_noise_20261122

#### Native item 2

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: 1dfc749e064f199de5e43fd5d1f0f7000e99dfeec2054539bcd2a8ecfead2247

BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/10/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/10/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/10/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/10/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/10/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 12

Native pointer: /joint_analysis/comparisons/11; canonical SHA-256: 2165c4d858c30e31117103fd981ae3df54b34890d15bdd503aac44a26f75bd86

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/11/comparison_id; canonical SHA-256: f5d62daf845061dd38b10aa2dc5f5544717ec7f2ffaa8cbc580802868c665f8e

BL_SPEC_joint_expected_cost__main__c_old_source_remainder_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/11/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/11/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/11/upper_envelope; canonical SHA-256: 10fb29dcc6f63dbf6cdba8e16ac2e873415fa393fbb69838bc77bff84f549f82

\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/11/lower_envelope; canonical SHA-256: bcf9d2a363caf2637deb47edf04eaa166837042b50df812c471b1eafe77ac197

\Omega\!\left(\frac{\kappa^2L\Delta}{\varepsilon^2}+\frac{\theta^2\kappa^8\sigma_g^2L^3\Delta}{\varepsilon^6}\right)

#### Native field: gap

Native pointer: /joint_analysis/comparisons/11/gap; canonical SHA-256: 87a349df326e07173f7c3caec2a06bb0bd04fbb0d5946ed8d77a7cea1d9d3b97

The upper/lower ratio is the displayed U divided by the displayed positive L, up to the source logarithms. No matching dependence on arbitrary sigma_f or theta is asserted.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/11/remaining_gap; canonical SHA-256: 87a349df326e07173f7c3caec2a06bb0bd04fbb0d5946ed8d77a7cea1d9d3b97

The upper/lower ratio is the displayed U divided by the displayed positive L, up to the source logarithms. No matching dependence on arbitrary sigma_f or theta is asserted.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/11/bound_uses; canonical SHA-256: 9acf503534a6bfaa08080ca85846e14647c62f94df435a35929bf03fe206b687

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/0; canonical SHA-256: f0f90675de60e25ed7c6173711d96114f2f2e92e96d9800b1d9cbb4e94cc4f53

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/adopted_region; canonical SHA-256: 4084db588ce3c3af906cc929861ef3b141677f038342280978946ca744ec6380

(The complete S predicate and not the complete N predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/validity_region; canonical SHA-256: 4084db588ce3c3af906cc929861ef3b141677f038342280978946ca744ec6380

(The complete S predicate and not the complete N predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/mapping_proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/11/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native item 2

Native pointer: /joint_analysis/comparisons/11/bound_uses/1; canonical SHA-256: f48e6af2b61a09f743fb896f034149935e9c2b070dcc9f40399a8ce313e005eb

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/bound_id; canonical SHA-256: 2417de16c8f6943f16f5435854280a55cb5f28bd14f8d48c748f5558931911d9

BL_SPEC_joint_expected_cost__main__b_guarded_source_lower_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/adopted_region; canonical SHA-256: 4084db588ce3c3af906cc929861ef3b141677f038342280978946ca744ec6380

(The complete S predicate and not the complete N predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/validity_region; canonical SHA-256: 4084db588ce3c3af906cc929861ef3b141677f038342280978946ca744ec6380

(The complete S predicate and not the complete N predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/mapping_proof_refs; canonical SHA-256: 48e6b31a60b2939f4e436397d643b16b993c839eaf2b32172524993eabcfaf29

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 1dfc749e064f199de5e43fd5d1f0f7000e99dfeec2054539bcd2a8ecfead2247

BL_SPEC_joint_expected_cost__main__proof_source_normalization_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/11/bound_uses/1/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/11/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/11/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/11/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/11/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 13

Native pointer: /joint_analysis/comparisons/12; canonical SHA-256: 067034a2bdc0924eb954865310ef476e5755d78f37e4a9d6b675bcb99412dc8f

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/12/comparison_id; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/12/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/12/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/12/upper_envelope; canonical SHA-256: 10fb29dcc6f63dbf6cdba8e16ac2e873415fa393fbb69838bc77bff84f549f82

\widetilde O\!\left((1+\bar\Lambda_\Phi\Delta/\varepsilon^2)\left[1+k+\frac{(1+k)^2}{\varepsilon^2}\left\{\sigma_f^2+\left(\frac{L_f^2}{\mu^2}+1+\frac{E_\rho^2}{\varepsilon^2}\right)\sigma_g^2\right\}\right]\right)

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/12/lower_envelope; canonical SHA-256: 12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126

Native value (string): ""

#### Native field: gap

Native pointer: /joint_analysis/comparisons/12/gap; canonical SHA-256: d2b89510a639dd9d3292bdfe0cd11b4b30830e75943b44aaa22b40a7118504c5

A target-compatible positive lower is missing outside E and S.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/12/remaining_gap; canonical SHA-256: d2b89510a639dd9d3292bdfe0cd11b4b30830e75943b44aaa22b40a7118504c5

A target-compatible positive lower is missing outside E and S.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/12/bound_uses; canonical SHA-256: 719c4c03efc840309619abaaa39891dc7a466889d64abb63db0fc343a059fbd7

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/bound_uses/0; canonical SHA-256: 26a132ee927db10f67533d0b3df993255a7f884abf4c19331363adf5c112f667

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/bound_id; canonical SHA-256: 6230d29b8330b9420a191b2f6a0fa728da6cdf19ba75e955650ab78fac23eeb5

BL_SPEC_joint_expected_cost__main__b_effective_upper_20261122

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/adopted_region; canonical SHA-256: 14284e905b17881e748285ba93b417b68718668d4b99bd9092acc10d9b78ea51

(All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/validity_region; canonical SHA-256: 14284e905b17881e748285ba93b417b68718668d4b99bd9092acc10d9b78ea51

(All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/mapping_proof_refs; canonical SHA-256: 63795fc3c8bf703d69ac73fe380f1b83e2361fe96a6c661a4e53e0a4f2916989

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: d6cb9deb9a5e2b17b47540887010be4ba0dcd389d898192cad75f9e1b814d413

BL_SPEC_joint_expected_cost__main__proof_universal_curvature_20261122

#### Native field: reason

Native pointer: /joint_analysis/comparisons/12/bound_uses/0/reason; canonical SHA-256: 27dcb2aadff18f8c2908e44eaee7473bde3ca6cfc962857acb8deb3746c3f514

Selected under the displayed target quantity, view and regime.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/12/boundary_checks; canonical SHA-256: de1234f6d16ecab59a9fa6785c22490a2b3aa5a54db3d1468182dc4232e08088

#### Native item 1

Native pointer: /joint_analysis/comparisons/12/boundary_checks/0; canonical SHA-256: a3ae00c8e9bd27995bc3e27785febc3d753dd939b0eb1b85b6a9c5497ddc73d1

Strict and closed tolerance endpoints are recorded in the regime predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/12/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/12/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native item 14

Native pointer: /joint_analysis/comparisons/13; canonical SHA-256: e54aed0e1ffeff50a8cec996d14e3e4185c08f68cd1b94586327fae962e9df7f

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/13/comparison_id; canonical SHA-256: 9268e84fc236c55916cc11e8fac6b93c8551fbaccc922bef391235dc78ad4f59

BL_SPEC_joint_expected_cost__main__c_fixed_structural_accuracy_20261126

#### Native field: role

Native pointer: /joint_analysis/comparisons/13/role; canonical SHA-256: 4e02f13b83c6632faeff714398656a0043fda9e574b1da32be418d8428c99511

fixed_parameter_slice

#### Native field: slice

Native pointer: /joint_analysis/comparisons/13/slice; canonical SHA-256: fc64a8a9e2b342501cfcb7f4f13763859fe6c4ad25a2e74ba5d79b973c6653a4

All structural parameters fixed

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/13/upper_envelope; canonical SHA-256: b5e3946c09cc04cdc3e46cf45463a9bc1a7586f26a969f103d43f5f379f990d4

C_P\varepsilon^{-6}

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/13/lower_envelope; canonical SHA-256: eefdb3fc68e1b6ff6b8c6b0bca1477c80bd9d301136df58592b91a9b23185c9d

c_P\varepsilon^{-6}

#### Native field: gap

Native pointer: /joint_analysis/comparisons/13/gap; canonical SHA-256: 1f24bd78b41fd5df544020939beb9ee88c949aeaec8ba747728c89bfd5b4323a

Matching sixth-power accuracy dependence with all listed structural budgets fixed.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/13/remaining_gap; canonical SHA-256: 1f24bd78b41fd5df544020939beb9ee88c949aeaec8ba747728c89bfd5b4323a

Matching sixth-power accuracy dependence with all listed structural budgets fixed.

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/13/bound_uses; canonical SHA-256: b511419f2b271c42a3d1d4ccaeab4bf1739d4f10d101c90b3ae25bd456fe8df6

#### Native item 1

Native pointer: /joint_analysis/comparisons/13/bound_uses/0; canonical SHA-256: 6fc54b6c5f99ba9d2d19261bd23b3e7cad001a16c4c170215122092b45ba21bc

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/bound_id; canonical SHA-256: 513ed8684c9f999fd43305784ab68031f32555559ca4115fde4bc8216135cdc7

BL_SPEC_joint_expected_cost__main__b_fixed_structural_accuracy_upper_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/adopted_region; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/validity_region; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/mapping_proof_refs; canonical SHA-256: 147cb940899e99c868787aee4f90641ed242e241fd672f4c67f07c3ecd979566

#### Native item 1

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: aabbbcc3bfba9fe929a403008b10496460982efc68d28064b26c986649a3c20b

BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/13/bound_uses/0/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native item 2

Native pointer: /joint_analysis/comparisons/13/bound_uses/1; canonical SHA-256: d0cd43c9f2a177db0a5e547af2aec86dafa929199172e586028e7b0633e6917b

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/bound_id; canonical SHA-256: d6b154774f132dc82521645f92791b0ccbde46aec4ee7696a78f871bd49e6666

BL_SPEC_joint_expected_cost__main__b_fixed_structural_accuracy_lower_20261126

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/adopted_region; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/validity_region; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/mapping_proof_refs; canonical SHA-256: 147cb940899e99c868787aee4f90641ed242e241fd672f4c67f07c3ecd979566

#### Native item 1

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: aabbbcc3bfba9fe929a403008b10496460982efc68d28064b26c986649a3c20b

BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

#### Native field: reason

Native pointer: /joint_analysis/comparisons/13/bound_uses/1/reason; canonical SHA-256: 5fb07be875eca2b4c0f1be879d8cfe687c348ff549e593b20a2a91ea43b3303c

Selected only under the complete displayed comparison predicate.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/13/boundary_checks; canonical SHA-256: e595a70a0dd8fbc06967492632b5e71766f30f5e9b808b6e7afbb28d40ad78fe

#### Native item 1

Native pointer: /joint_analysis/comparisons/13/boundary_checks/0; canonical SHA-256: 80df2b6ee753ce45bf037caea5b6972a858708863de8f519a69f144567ac881a

All strict, inclusive and excluded boundaries occur explicitly in the predicate.

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/13/constant_dependencies; canonical SHA-256: c55754a5c07b1d3cdac6b311111024b204f69fbff4a04631847234df5b14f22c

#### Native item 1

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/0; canonical SHA-256: 98052bdf00117818069da4e54908c109e3c75ad3f5bbe2bc1c9eafd1faa9361e

BL_SPEC_joint_expected_cost_p_1cc24df773

#### Native item 2

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/1; canonical SHA-256: 72a15a9e50588ab80028e00e029fd8e92866980d365482e4fda7efd8a6906341

BL_SPEC_joint_expected_cost_p_efcabfd5ff

#### Native item 3

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/2; canonical SHA-256: b063ea127ca0e8cb3eecfbb35fde2628cf76e54c6636672bc47b00d2fe4c7005

BL_SPEC_joint_expected_cost_p_850094ef78

#### Native item 4

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/3; canonical SHA-256: c51edaf441dec5d639d48164db9eac8f57292b0981fd597e32ba83f16f6b4894

BL_SPEC_joint_expected_cost_p_25c351f23c

#### Native item 5

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/4; canonical SHA-256: 8bedb2fc40c87837135e13024e3884dfc53e9ab6450e0d838a034e2140ccb947

BL_SPEC_joint_expected_cost_p_a17bdd1bfb

#### Native item 6

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/5; canonical SHA-256: cd8c4b47ffa7965164e6a78e1901af101a57e719c701091230c39f127f683f9f

BL_SPEC_joint_expected_cost_p_9d0f22c488

#### Native item 7

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/6; canonical SHA-256: cfdb094375bddaef1ad66f985409e1551a6a4b4a7d7de537c578b9bfaa620771

BL_SPEC_joint_expected_cost_p_d1944ba8d6

#### Native item 8

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/7; canonical SHA-256: b75377a8b2b8ca078b6876bb0999fb158cf48d202aa1fb5a96a43bd62e1914e7

BL_SPEC_joint_expected_cost_p_256ee43d4f

#### Native item 9

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/8; canonical SHA-256: d12efcbf9e8d431283f73fc82cee54cec0f845ba33bb051a11e58c47c430dfc3

BL_SPEC_joint_expected_cost_p_4e3f70b140

#### Native item 10

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/9; canonical SHA-256: 8e5f1b3fc6aa9e24cf1a791bd988b39f2832c8fd1302500a69229a01caa78ed8

BL_SPEC_joint_expected_cost_p_eb3546e82c

#### Native item 11

Native pointer: /joint_analysis/comparisons/13/constant_dependencies/10; canonical SHA-256: 9a6660f40156809c755d8536ceb7328fb89687cf3e61434ebc039c5b244d1910

BL_SPEC_joint_expected_cost_p_5ffc729833

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/13/fixed_parameters; canonical SHA-256: c55754a5c07b1d3cdac6b311111024b204f69fbff4a04631847234df5b14f22c

#### Native item 1

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/0; canonical SHA-256: 98052bdf00117818069da4e54908c109e3c75ad3f5bbe2bc1c9eafd1faa9361e

BL_SPEC_joint_expected_cost_p_1cc24df773

#### Native item 2

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/1; canonical SHA-256: 72a15a9e50588ab80028e00e029fd8e92866980d365482e4fda7efd8a6906341

BL_SPEC_joint_expected_cost_p_efcabfd5ff

#### Native item 3

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/2; canonical SHA-256: b063ea127ca0e8cb3eecfbb35fde2628cf76e54c6636672bc47b00d2fe4c7005

BL_SPEC_joint_expected_cost_p_850094ef78

#### Native item 4

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/3; canonical SHA-256: c51edaf441dec5d639d48164db9eac8f57292b0981fd597e32ba83f16f6b4894

BL_SPEC_joint_expected_cost_p_25c351f23c

#### Native item 5

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/4; canonical SHA-256: 8bedb2fc40c87837135e13024e3884dfc53e9ab6450e0d838a034e2140ccb947

BL_SPEC_joint_expected_cost_p_a17bdd1bfb

#### Native item 6

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/5; canonical SHA-256: cd8c4b47ffa7965164e6a78e1901af101a57e719c701091230c39f127f683f9f

BL_SPEC_joint_expected_cost_p_9d0f22c488

#### Native item 7

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/6; canonical SHA-256: cfdb094375bddaef1ad66f985409e1551a6a4b4a7d7de537c578b9bfaa620771

BL_SPEC_joint_expected_cost_p_d1944ba8d6

#### Native item 8

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/7; canonical SHA-256: b75377a8b2b8ca078b6876bb0999fb158cf48d202aa1fb5a96a43bd62e1914e7

BL_SPEC_joint_expected_cost_p_256ee43d4f

#### Native item 9

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/8; canonical SHA-256: d12efcbf9e8d431283f73fc82cee54cec0f845ba33bb051a11e58c47c430dfc3

BL_SPEC_joint_expected_cost_p_4e3f70b140

#### Native item 10

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/9; canonical SHA-256: 8e5f1b3fc6aa9e24cf1a791bd988b39f2832c8fd1302500a69229a01caa78ed8

BL_SPEC_joint_expected_cost_p_eb3546e82c

#### Native item 11

Native pointer: /joint_analysis/comparisons/13/fixed_parameters/10; canonical SHA-256: 9a6660f40156809c755d8536ceb7328fb89687cf3e61434ebc039c5b244d1910

BL_SPEC_joint_expected_cost_p_5ffc729833

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 14ca0cae8b9a959ab57ef94a4c0a314e931f5f340d0a45d73ffd6cbd1ad9d7f8

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 8695885c202544cbd1a818caf4ca18ba6393d763952de38aa5a8a2bdab2b17ee

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 282fd52f767bcf1a08804f7a9ed8a23b9941cb9c17f8755d11a73c310b67515c

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 9765327f001cddfac6794b74d8bfb40906c25dfcb81acc559a82869d0163d3cd

BL_SPEC_joint_expected_cost__main__c_source_zero_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: f864796276d2399f3e4f00df46df19d0d361e5280819cd21bfabd09c2878b2d2

The complete Z guard, and not E.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: c81f2dd0758f3abe625c1a7d9a7fc2648d53b220d5a4325ff0a1ff82aeec2231

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 9765327f001cddfac6794b74d8bfb40906c25dfcb81acc559a82869d0163d3cd

BL_SPEC_joint_expected_cost__main__c_source_zero_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: e091dbbbff7942edcbaf6c990da9dbeac2c6a4f80a130be81a85195f822b3c7c

Return x0. Source threshold upper statements pass to every curvature subclass; expected cost is nonnegative.

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: dfcaa232e4c34d29c2e6691f31916a3880e1a761ae4eb3f6fe8a724f8fed78da

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 5790a340058e7b9b2b200d448f4947ee6f1506771c1c1309070d3f1ea171bb34

BL_SPEC_joint_expected_cost__main__c_curvature_old_n_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 93551024a2b3e1a363e60560659efa50addfca6ecf0551b760e54aaf4d44b474

The complete C guard; not E; not Z; the complete old N predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: c106c2fdbf8a47c745ebb98508cd3677403c666648f9fd9e307bea77c0a487cf

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 5790a340058e7b9b2b200d448f4947ee6f1506771c1c1309070d3f1ea171bb34

BL_SPEC_joint_expected_cost__main__c_curvature_old_n_20261126

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

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 0c58d30e6604f85506147bf95804a028d0d3810250fedcc0adb000e6d50f3c88

The source bracket holds on the complete C guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: 1647874069b2f5b5dec8694b803671fb16bcf6311da679f87d346205296334af

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 95f8b1e32b721fad23cce5f72e863a595c416b48589a91b44a23bad341800910

BL_SPEC_joint_expected_cost__main__c_curvature_old_s_remaining_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 671d73bb410517d53bf08bf331c5d7ae0b13624400e1718635c4d3b0e707c39e

The complete C guard; not E; not Z; the complete old S predicate and not the complete old N predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 28e64b09defed39a652450d433759555351e75049310df13a1df06942f4ee00c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids/0; canonical SHA-256: 95f8b1e32b721fad23cce5f72e863a595c416b48589a91b44a23bad341800910

BL_SPEC_joint_expected_cost__main__c_curvature_old_s_remaining_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

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

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 0c58d30e6604f85506147bf95804a028d0d3810250fedcc0adb000e6d50f3c88

The source bracket holds on the complete C guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

#### Native item 5

Native pointer: /joint_analysis/domain_map/cells/4; canonical SHA-256: edc17644c0e0cf382c9048955046e16d303f41661f6cb4f0c108c59d153aecab

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/4/cell_id; canonical SHA-256: 6c1c58c1253ec3c9f6144a7e5eeaea76ce053c986171ef9f361a51f0154a5cfd

BL_SPEC_joint_expected_cost__main__c_curvature_outside_old_s_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/4/predicate; canonical SHA-256: 0642a8243e2d6ad4684ec3f8b18326d03f02c02be45b2a494eef3da74086320f

The complete C guard; not E; not Z; not the complete old S predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids; canonical SHA-256: 6e9da59d92f73fa59a0918aaa3206bafba7404f794a8d4a9ba99d5a6737fd6a6

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/4/comparison_ids/0; canonical SHA-256: 6c1c58c1253ec3c9f6144a7e5eeaea76ce053c986171ef9f361a51f0154a5cfd

BL_SPEC_joint_expected_cost__main__c_curvature_outside_old_s_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/4/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/4/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/4/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/4/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/4/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/4/note; canonical SHA-256: 0c58d30e6604f85506147bf95804a028d0d3810250fedcc0adb000e6d50f3c88

The source bracket holds on the complete C guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

#### Native item 6

Native pointer: /joint_analysis/domain_map/cells/5; canonical SHA-256: 54c52f31fcb02a9ff043ae0956e98123e531c7f773e6e00f46c221ec539edc7e

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/5/cell_id; canonical SHA-256: fc5b4ad329b6bb4e06961fbdb76bfe3cf9c15f1be2ed16c6530d9db641601666

BL_SPEC_joint_expected_cost__main__c_joint_old_n_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/5/predicate; canonical SHA-256: abbd0e2b29af2c4836862dd74f6d6f2aecdb28c724a3759046a7e4032e8ed0de

The complete J guard; not E; not Z; not C; the complete old N predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids; canonical SHA-256: 28c11b340f3369c6bff058d4caffb687f0ecfba416b5652bfa6ac76de84986de

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/5/comparison_ids/0; canonical SHA-256: fc5b4ad329b6bb4e06961fbdb76bfe3cf9c15f1be2ed16c6530d9db641601666

BL_SPEC_joint_expected_cost__main__c_joint_old_n_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/5/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/5/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/5/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/5/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/5/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/5/note; canonical SHA-256: 2116820fe06cd8c32d803ec3ece5d3e6e00989c659c9f2480c6a2c1946374ccf

The source bracket holds on the complete J guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

#### Native item 7

Native pointer: /joint_analysis/domain_map/cells/6; canonical SHA-256: c4142a4dbf69a8f0bee51836b2b937d3715d51fa3332cb25e609a73ea9f1ff9f

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/6/cell_id; canonical SHA-256: 3fd04f216821f990a836079ddbe29196b9f2cfb92b2cc20d2d5404e540285af6

BL_SPEC_joint_expected_cost__main__c_joint_old_s_remaining_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/6/predicate; canonical SHA-256: 70e6b3d4eaddc6c5513adf72828c9f14c762d2c0abbd4098189d127210b147df

The complete J guard; not E; not Z; not C; the complete old S predicate and not the complete old N predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids; canonical SHA-256: 03de4f24241bf7541eea8d6026e63a9c6689757033dff19b361d160b33d0f253

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/6/comparison_ids/0; canonical SHA-256: 3fd04f216821f990a836079ddbe29196b9f2cfb92b2cc20d2d5404e540285af6

BL_SPEC_joint_expected_cost__main__c_joint_old_s_remaining_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/6/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/6/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/6/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/6/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/6/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/6/note; canonical SHA-256: 2116820fe06cd8c32d803ec3ece5d3e6e00989c659c9f2480c6a2c1946374ccf

The source bracket holds on the complete J guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

#### Native item 8

Native pointer: /joint_analysis/domain_map/cells/7; canonical SHA-256: fb55bf5b93ccf16314ec4d53095aa38fac85152eb2601b4720f07a57c00b826c

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/7/cell_id; canonical SHA-256: 68d0fea9da35c8f77d4a163d1dae56860165b099d3370bf8ec644cdfd3d37f94

BL_SPEC_joint_expected_cost__main__c_joint_outside_old_s_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/7/predicate; canonical SHA-256: 00d90d3ea29296f913f127e6655d86d2573f265d496a55fac07e93dde824fff7

The complete J guard; not E; not Z; not C; not the complete old S predicate.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids; canonical SHA-256: 39f7be580e42878f4f925d7872da82dbffc0cec58dfd3d127ec68676e8919357

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/7/comparison_ids/0; canonical SHA-256: 68d0fea9da35c8f77d4a163d1dae56860165b099d3370bf8ec644cdfd3d37f94

BL_SPEC_joint_expected_cost__main__c_joint_outside_old_s_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/7/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/7/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/7/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/7/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/7/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/7/note; canonical SHA-256: 2116820fe06cd8c32d803ec3ece5d3e6e00989c659c9f2480c6a2c1946374ccf

The source bracket holds on the complete J guard. Minimum of eligible upper bounds and maximum of eligible lower bounds preserve both source records. Old S/N lower claims are selected only on their displayed intersections. C has precedence over J in their overlap; old zero E has first precedence.

#### Native item 9

Native pointer: /joint_analysis/domain_map/cells/8; canonical SHA-256: 3359077f602534abcaea629f8c6d41a557a667fdcd824f3de89c92c177ef739a

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/8/cell_id; canonical SHA-256: 3483eda65f1a0bb74dd035dede167e74629ad7761f22a00b4632e0166d4a0f44

BL_SPEC_joint_expected_cost__main__c_constant_blocks_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/8/predicate; canonical SHA-256: 718979941efc93e3bef0794a21a59e41972f46568141c3deab0fb9c13927bacc

The complete K guard; not E; not Z; not C; not J.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids; canonical SHA-256: 00736d3f959bff4367b80f2c56a7713fa91badaa2a250e3fe786882ce85ce0ec

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/8/comparison_ids/0; canonical SHA-256: 3483eda65f1a0bb74dd035dede167e74629ad7761f22a00b4632e0166d4a0f44

BL_SPEC_joint_expected_cost__main__c_constant_blocks_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/8/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/8/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/8/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/8/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/8/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/8/note; canonical SHA-256: 3bc4a0e1510e357540ecb576eb8d593476124e03f50f6460bb9579b7cb3430a4

Theorem 7.1 uses exact initialization, global variance bounds and unbounded finite queries. All charged fresh calls and the single displayed logarithm are retained.

#### Native item 10

Native pointer: /joint_analysis/domain_map/cells/9; canonical SHA-256: cfeb08c5d83a98d5e51b250c69e8dfcd070bd1074cbf469e753b64094ae202b2

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/9/cell_id; canonical SHA-256: 9558f1762a0daeaa51abc9891154f8a18ce5ac9fd7e3bb681e7e1367a015ce7e

BL_SPEC_joint_expected_cost__main__c_affine_activation_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/9/predicate; canonical SHA-256: 9076ef64ebd35f00b2d02914c6fadb33a669316629ebce96a04e4493a724ecc8

The complete A guard; not E; not Z; not C; not J; not K.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids; canonical SHA-256: d5338ce2ab3a3a39fba82eb359c0c72d7ad0115bc6e21b6e423fa670a5beae3b

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/9/comparison_ids/0; canonical SHA-256: 9558f1762a0daeaa51abc9891154f8a18ce5ac9fd7e3bb681e7e1367a015ce7e

BL_SPEC_joint_expected_cost__main__c_affine_activation_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/9/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/9/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/9/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/9/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/9/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/9/note; canonical SHA-256: fe752b52250c4b3fbdf2f56abc4ee16a89f6f9634f385b023e81d2ee40ce3b31

Theorem 3.2 supplies a positive fractional expected-cost lower bound, not a unit-call floor. Its lower witness obeys Lambda_Phi>=L kappa^2. The universal native upper remains selected.

#### Native item 11

Native pointer: /joint_analysis/domain_map/cells/10; canonical SHA-256: 4bd4f3fe060c24c5276a0d34b54be09a218202f6ed1333b43c05936112e8af87

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/10/cell_id; canonical SHA-256: 2d7df47383a40ba4eba5e63c606b8d011ae809c160ec7b5c4638e9c6bafebd53

BL_SPEC_joint_expected_cost__main__c_old_noise_remainder_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/10/predicate; canonical SHA-256: 47c5685a34425a429b169c6ec2d2f26ef78ff13212810627e15206de8be483b5

(The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.) and not E; not Z; not C; not J; not K; not A.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/10/comparison_ids; canonical SHA-256: 8e05a135d6bf79301bbcc67fd926ad5586f792f7ad6d445d8b12406a41cb0cd2

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/10/comparison_ids/0; canonical SHA-256: 2d7df47383a40ba4eba5e63c606b8d011ae809c160ec7b5c4638e9c6bafebd53

BL_SPEC_joint_expected_cost__main__c_old_noise_remainder_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/10/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/10/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/10/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/10/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/10/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/10/note; canonical SHA-256: 51add160ea8da9879029145ca5d7e3382b097e936e182bfd6201eb6480d0266d

Complete dominance calculation; theta is bounded by fixed universal constants.

#### Native item 12

Native pointer: /joint_analysis/domain_map/cells/11; canonical SHA-256: ee0edb6094ba063877512ecfdc7a773bbc722043463cd067396284e92670bf57

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/11/cell_id; canonical SHA-256: f5d62daf845061dd38b10aa2dc5f5544717ec7f2ffaa8cbc580802868c665f8e

BL_SPEC_joint_expected_cost__main__c_old_source_remainder_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/11/predicate; canonical SHA-256: 4084db588ce3c3af906cc929861ef3b141677f038342280978946ca744ec6380

(The complete S predicate and not the complete N predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/11/comparison_ids; canonical SHA-256: 6754ffce6eee125ca460b0455bc046c02088ee9aa4ba66716767acbce1f77688

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/11/comparison_ids/0; canonical SHA-256: f5d62daf845061dd38b10aa2dc5f5544717ec7f2ffaa8cbc580802868c665f8e

BL_SPEC_joint_expected_cost__main__c_old_source_remainder_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/11/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/11/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/11/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/11/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/11/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/11/note; canonical SHA-256: f1754846d6edcb176fe741ec32fc26165666c329b8e42f5357c927e47592e30b

Source theorem plus complete normalized transfer; all parameter dependence stays explicit.

#### Native item 13

Native pointer: /joint_analysis/domain_map/cells/12; canonical SHA-256: 2f6b7ed4ebea396792e568fa54441d46ca5e713d07dc6c8784c31dd7f9d6c466

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/12/cell_id; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/12/predicate; canonical SHA-256: 14284e905b17881e748285ba93b417b68718668d4b99bd9092acc10d9b78ea51

(All native parameter/model constraints, $2\bar\Lambda_\Phi\Delta>\varepsilon^2$, and not the complete S predicate.) and not E; not Z; not C; not J; not K; not A.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/12/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/12/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/12/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/12/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/12/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/12/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/12/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/12/note; canonical SHA-256: 3edd8c8fdbed3b2a195bb2acd0b89e19cffbff594ad1be058bcc2d24ed55e736

B.2 supplies an upper bound throughout this remainder. Neither the quarantined b2 nor the new S-only lower is used here.

#### Native item 14

Native pointer: /joint_analysis/domain_map/cells/13; canonical SHA-256: 7a9922e082229c70a8c8d7ab5625d91ad21c8df5793e719e88169f7aa3fc86e4

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/13/cell_id; canonical SHA-256: 9268e84fc236c55916cc11e8fac6b93c8551fbaccc922bef391235dc78ad4f59

BL_SPEC_joint_expected_cost__main__c_fixed_structural_accuracy_20261126

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/13/predicate; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/13/comparison_ids; canonical SHA-256: ed4f2764f881be78c64b5884381f5ecbbc0174e3d85c41a294be4d00ad50e32b

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/13/comparison_ids/0; canonical SHA-256: 9268e84fc236c55916cc11e8fac6b93c8551fbaccc922bef391235dc78ad4f59

BL_SPEC_joint_expected_cost__main__c_fixed_structural_accuracy_20261126

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/13/role; canonical SHA-256: 4e02f13b83c6632faeff714398656a0043fda9e574b1da32be418d8428c99511

fixed_parameter_slice

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/13/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/13/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/13/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/13/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/13/note; canonical SHA-256: 4760a66f044dc1a354bb95650d365f5fe7622bb22f3efb78098f7997a848a044

Accuracy-only fixed-structural result; overlaps in parameters do not change the joint quantity.

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 121e074c9d295033eabfff3fc7dc8687096bab456dad4a72faadb77c70abeb83

Within the native q1 domain, keep E first, then Z minus E; then C minus E and Z, then J minus E, Z and C. Split each C/J region by old N, old S minus N and outside old S. Then K and A apply outside the preceding guards. Finally intersect each of the three original nonzero cells with the complement of E,Z,C,J,K,A. The original four cells covered the native domain; these intersections and complements preserve that coverage. The separate fixed-structural quantity is an overlapping accuracy-only slice, not another q1 partition cell.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 2aed9e934581f9303a2b9b69c2b764504772448f309e8bb42d265934f7f0e8da

The explicit independent-budget remainder still has a missing positive lower; old guarded S/N rates persist on their exact complementary cells.

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 9d3795db17290eec6d0834eef5df5a95c42b6f30306bae0c27b2647d0706c6f2

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: a8eb757f9a73a3906b159b943a2837b700e8847a172abb9d8ba9d2c2270102cf

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

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: ae2a2660fd6138641ac78d2ea88081476eb59575dd6f6d9932221cb1bcecd6a5

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: f5d62daf845061dd38b10aa2dc5f5544717ec7f2ffaa8cbc580802868c665f8e

BL_SPEC_joint_expected_cost__main__c_old_source_remainder_20261126

#### Native item 3

Native pointer: /joint_analysis/impact/0/comparison_ids/2; canonical SHA-256: 2d7df47383a40ba4eba5e63c606b8d011ae809c160ec7b5c4638e9c6bafebd53

BL_SPEC_joint_expected_cost__main__c_old_noise_remainder_20261126

#### Native item 4

Native pointer: /joint_analysis/impact/0/comparison_ids/3; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 411ede5d80f9087a69f9b469aa5072f5f2afa15a643f9a065dcefb67d5e14221

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: b22fdaaff6b60df7f7f7d99730cf782f63d6fc395ccf4f497e4273d745e36543

BL_SPEC_joint_expected_cost_source_brackets_20261126

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0c6fd61494f00d681ec17bee6e9406191af8e3b1369e4c3263030168b139fd23

bound_strengthening

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 895f39696cab655eca44830f43ead6653acc9df1aa872d1efbf32d5bb0249cae

Separate general and prescribed-curvature source brackets retain both noise budgets and initialization logarithms. Old upper and lower claims remain selected on eligible intersections; exact source-zero and constant-block rows have their own predicates. Fixed-structural accuracy and uniform-noise finiteness use separate quantifiers.

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 773a402543fba1dae9946fb81abf55aaeaedecd5fc0cacfbdc78a1d05e734d15

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 9765327f001cddfac6794b74d8bfb40906c25dfcb81acc559a82869d0163d3cd

BL_SPEC_joint_expected_cost__main__c_source_zero_20261126

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: 5790a340058e7b9b2b200d448f4947ee6f1506771c1c1309070d3f1ea171bb34

BL_SPEC_joint_expected_cost__main__c_curvature_old_n_20261126

#### Native item 3

Native pointer: /joint_analysis/impact/1/comparison_ids/2; canonical SHA-256: 95f8b1e32b721fad23cce5f72e863a595c416b48589a91b44a23bad341800910

BL_SPEC_joint_expected_cost__main__c_curvature_old_s_remaining_20261126

#### Native item 4

Native pointer: /joint_analysis/impact/1/comparison_ids/3; canonical SHA-256: 6c1c58c1253ec3c9f6144a7e5eeaea76ce053c986171ef9f361a51f0154a5cfd

BL_SPEC_joint_expected_cost__main__c_curvature_outside_old_s_20261126

#### Native item 5

Native pointer: /joint_analysis/impact/1/comparison_ids/4; canonical SHA-256: fc5b4ad329b6bb4e06961fbdb76bfe3cf9c15f1be2ed16c6530d9db641601666

BL_SPEC_joint_expected_cost__main__c_joint_old_n_20261126

#### Native item 6

Native pointer: /joint_analysis/impact/1/comparison_ids/5; canonical SHA-256: 3fd04f216821f990a836079ddbe29196b9f2cfb92b2cc20d2d5404e540285af6

BL_SPEC_joint_expected_cost__main__c_joint_old_s_remaining_20261126

#### Native item 7

Native pointer: /joint_analysis/impact/1/comparison_ids/6; canonical SHA-256: 68d0fea9da35c8f77d4a163d1dae56860165b099d3370bf8ec644cdfd3d37f94

BL_SPEC_joint_expected_cost__main__c_joint_outside_old_s_20261126

#### Native item 8

Native pointer: /joint_analysis/impact/1/comparison_ids/7; canonical SHA-256: 3483eda65f1a0bb74dd035dede167e74629ad7761f22a00b4632e0166d4a0f44

BL_SPEC_joint_expected_cost__main__c_constant_blocks_20261126

#### Native item 9

Native pointer: /joint_analysis/impact/1/comparison_ids/8; canonical SHA-256: 9558f1762a0daeaa51abc9891154f8a18ce5ac9fd7e3bb681e7e1367a015ce7e

BL_SPEC_joint_expected_cost__main__c_affine_activation_20261126

#### Native item 10

Native pointer: /joint_analysis/impact/1/comparison_ids/9; canonical SHA-256: 2d7df47383a40ba4eba5e63c606b8d011ae809c160ec7b5c4638e9c6bafebd53

BL_SPEC_joint_expected_cost__main__c_old_noise_remainder_20261126

#### Native item 11

Native pointer: /joint_analysis/impact/1/comparison_ids/10; canonical SHA-256: f5d62daf845061dd38b10aa2dc5f5544717ec7f2ffaa8cbc580802868c665f8e

BL_SPEC_joint_expected_cost__main__c_old_source_remainder_20261126

#### Native item 12

Native pointer: /joint_analysis/impact/1/comparison_ids/11; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native item 13

Native pointer: /joint_analysis/impact/1/comparison_ids/12; canonical SHA-256: 9268e84fc236c55916cc11e8fac6b93c8551fbaccc922bef391235dc78ad4f59

BL_SPEC_joint_expected_cost__main__c_fixed_structural_accuracy_20261126

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: b63b43f8e912872a354ecba5e249dd9897a472191e74894990427c2a5a8a97a4

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: f387d2cb9d38839500c845ddb8110636c3b753fa56732d6f4651996c8bc674cb

Joint structural-budget rates outside the registered common-budget J/C regions remain unclassified, including arbitrary tighter independent curvature budgets.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 495f8cab5f6c0e3a75e1f03d4ef51c144b7a9d762c4cbd9cd5a62362f4155506

Matching deterministic or lower-noise dependence for theta>kappa^2 and matching fixed- or polynomial-dimension lower bounds are not supplied by Theorem 8.1.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: c2e115edd309746f1047a25901bf6d9d15cad773c2a49fcaafd01b3201db3dbb

Initialization logarithms in R0 are retained; matching R0 dependence is not established.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 79711f4edef37993aa30a70b772f0cb0f949d79fcbdfef27f77f1a5f5b1a6a96

The remaining affine initialization regimes and matching finite-noise critical rates outside Theorem 10.4 are not classified.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 0da82b6c86fe814f12ae7da7d9607f5a83336c4780680674457efe41dd44588b

The registered source theorems are reported with contract checks; independent full-proof and formal-verification certification are not asserted.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 311102a76f7eb1bbb82cac0e8b555881a2f797e7ebd937615e996e0393bfff7b

The prior small-gap source slices and neighboring oracle models remain outside the adopted comparisons.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 3005aa378b13fd28161a6965635f3e4ee98008b57ec2eedf883850a7bfddfcd8

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 4f71bdac7761d3aa9555486184564b009fc7c80c56f3cae86bfb7f9bff254b92

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: c6f24a90bfc277f44aab85136023fbb75a66c22285c8d95fe3cd8d6513192822

BL_SPEC_joint_expected_cost__main__c_effective_zero_20261122

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 9765327f001cddfac6794b74d8bfb40906c25dfcb81acc559a82869d0163d3cd

BL_SPEC_joint_expected_cost__main__c_source_zero_20261126

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/2; canonical SHA-256: 5790a340058e7b9b2b200d448f4947ee6f1506771c1c1309070d3f1ea171bb34

BL_SPEC_joint_expected_cost__main__c_curvature_old_n_20261126

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/3; canonical SHA-256: 95f8b1e32b721fad23cce5f72e863a595c416b48589a91b44a23bad341800910

BL_SPEC_joint_expected_cost__main__c_curvature_old_s_remaining_20261126

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/4; canonical SHA-256: 6c1c58c1253ec3c9f6144a7e5eeaea76ce053c986171ef9f361a51f0154a5cfd

BL_SPEC_joint_expected_cost__main__c_curvature_outside_old_s_20261126

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/5; canonical SHA-256: fc5b4ad329b6bb4e06961fbdb76bfe3cf9c15f1be2ed16c6530d9db641601666

BL_SPEC_joint_expected_cost__main__c_joint_old_n_20261126

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/6; canonical SHA-256: 3fd04f216821f990a836079ddbe29196b9f2cfb92b2cc20d2d5404e540285af6

BL_SPEC_joint_expected_cost__main__c_joint_old_s_remaining_20261126

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/7; canonical SHA-256: 68d0fea9da35c8f77d4a163d1dae56860165b099d3370bf8ec644cdfd3d37f94

BL_SPEC_joint_expected_cost__main__c_joint_outside_old_s_20261126

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/8; canonical SHA-256: 3483eda65f1a0bb74dd035dede167e74629ad7761f22a00b4632e0166d4a0f44

BL_SPEC_joint_expected_cost__main__c_constant_blocks_20261126

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/9; canonical SHA-256: 9558f1762a0daeaa51abc9891154f8a18ce5ac9fd7e3bb681e7e1367a015ce7e

BL_SPEC_joint_expected_cost__main__c_affine_activation_20261126

#### Native item 11

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/10; canonical SHA-256: 2d7df47383a40ba4eba5e63c606b8d011ae809c160ec7b5c4638e9c6bafebd53

BL_SPEC_joint_expected_cost__main__c_old_noise_remainder_20261126

#### Native item 12

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/11; canonical SHA-256: f5d62daf845061dd38b10aa2dc5f5544717ec7f2ffaa8cbc580802868c665f8e

BL_SPEC_joint_expected_cost__main__c_old_source_remainder_20261126

#### Native item 13

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/12; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native item 14

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/13; canonical SHA-256: 9268e84fc236c55916cc11e8fac6b93c8551fbaccc922bef391235dc78ad4f59

BL_SPEC_joint_expected_cost__main__c_fixed_structural_accuracy_20261126

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: d9e4060443d5e1a00e98b9820f4fa780f0d47a2720012958e4e1d02e0fbedc00

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 3490fef23510b1cc92f2c89a7dbe2290d7a84085ea225cbdf39d11b28ba53d92

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: efb8d48296becee64872fa01b9304a4d303052bd9f0cecc97aa04d11c68077da

scope-20261126-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: f387d2cb9d38839500c845ddb8110636c3b753fa56732d6f4651996c8bc674cb

Joint structural-budget rates outside the registered common-budget J/C regions remain unclassified, including arbitrary tighter independent curvature budgets.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: e7c26b90c7edddf00013f06b5a1cdf172c48578579a9bf6ce6669c6f47bf6dd8

The stated limitation is retained; a missing Atlas bound is not a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: dee1f48e421d270e2ef36bbe3576a8f7181eac935197d995e762dbf0aa2661e5

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: b598a2d0bdc796e669d56b3e252b03ca367803e762bfc1161e262836cb92ef03

scope-20261126-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 495f8cab5f6c0e3a75e1f03d4ef51c144b7a9d762c4cbd9cd5a62362f4155506

Matching deterministic or lower-noise dependence for theta>kappa^2 and matching fixed- or polynomial-dimension lower bounds are not supplied by Theorem 8.1.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: e7c26b90c7edddf00013f06b5a1cdf172c48578579a9bf6ce6669c6f47bf6dd8

The stated limitation is retained; a missing Atlas bound is not a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 28f0407b23e6799c5a8019cc72f41bc67a713ebcfdd71811fd6afee269794911

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 94c4814d30037e08ba812e70f8b5a51b4b54a96481e7b1f97edfc20286e173fd

scope-20261126-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: c2e115edd309746f1047a25901bf6d9d15cad773c2a49fcaafd01b3201db3dbb

Initialization logarithms in R0 are retained; matching R0 dependence is not established.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: e7c26b90c7edddf00013f06b5a1cdf172c48578579a9bf6ce6669c6f47bf6dd8

The stated limitation is retained; a missing Atlas bound is not a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: b0614f81c38fefa39e8d30207c921385eb225b625de86345e83bef13a0f7a1c9

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: af89e3528d9f03ca4ec7959e63135f5e05b7724b2e7cfafd7ee9e65d219a178d

scope-20261126-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 79711f4edef37993aa30a70b772f0cb0f949d79fcbdfef27f77f1a5f5b1a6a96

The remaining affine initialization regimes and matching finite-noise critical rates outside Theorem 10.4 are not classified.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: e7c26b90c7edddf00013f06b5a1cdf172c48578579a9bf6ce6669c6f47bf6dd8

The stated limitation is retained; a missing Atlas bound is not a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 1dd05ae16657e812e92abe02d8524f5fd637270ac10f5434407867098520a364

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 5344d62cfbbcf746b59ddde8005529edcf2e15f53a22964d15e2dbb1701f02f7

scope-20261126-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 0da82b6c86fe814f12ae7da7d9607f5a83336c4780680674457efe41dd44588b

The registered source theorems are reported with contract checks; independent full-proof and formal-verification certification are not asserted.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: e7c26b90c7edddf00013f06b5a1cdf172c48578579a9bf6ce6669c6f47bf6dd8

The stated limitation is retained; a missing Atlas bound is not a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: ffe83b9552c5c2d71ef20045a943f66900ba36137c6e62144529ad1c71f8cfe8

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 256fb35bbcc62ca2849c26640e6d226e557f086e94a4313df3b058b694c6388e

scope-20261126-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 311102a76f7eb1bbb82cac0e8b555881a2f797e7ebd937615e996e0393bfff7b

The prior small-gap source slices and neighboring oracle models remain outside the adopted comparisons.

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: e7c26b90c7edddf00013f06b5a1cdf172c48578579a9bf6ce6669c6f47bf6dd8

The stated limitation is retained; a missing Atlas bound is not a theorem that the literature is open.

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 92a8bda0bfc9f0d7635cf6df44401d7980fa256125f46b009e8180f91a4cf9da

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 94cdb19bcfbdeeb2ff42b79d08dd96c789923527cf3bdc6376380b0191dad060

BL_SPEC_joint_expected_cost__main__c_independent_budget_remainder_20261126

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: df2e77c17b9986aeca401697d110121edf844441ec220a979c9cae8abba310af

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

#### Native item 5

Native pointer: /joint_analysis/provenance/4; canonical SHA-256: 5551a35e86d4be7db790f7f68caf04f2bfcfd3126b4d3bc449705bb9d43aede7

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/4/bound_id; canonical SHA-256: 0dbf1f8df1b8103aaa4fbd571ba8fcc4424a8894a202b3117bc56ecbffa489e8

BL_SPEC_joint_expected_cost__main__b_joint_upper_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/4/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/4/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/4/proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/provenance/4/proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/4/source_domain; canonical SHA-256: 2146486fbb364a0a9e98e710933a434cf94f5ea7696b1357dc417693350ed465

#### Native item 1

Native pointer: /joint_analysis/provenance/4/source_domain/0; canonical SHA-256: b9b6264f58b58c426442387dfe1e643d1b0bd1217a111ab8f6f5965d5056ed7a

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa^2$, and $\Lambda_\Phi\ge B_\Phi=(1+\kappa)^2L(1+\theta)$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/4/target_domain; canonical SHA-256: 6bae23cf0d6cda00d829e2afeab40aede0eccff7cb5428411da099a4589a776a

#### Native item 1

Native pointer: /joint_analysis/provenance/4/target_domain/0; canonical SHA-256: e6ab815bee315072b537e5ed5d5daeda80d9047ca7d6f1143930cee8f1fc53fe

BL_SPEC_joint_expected_cost__main__r_source_j_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/4/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/4/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 6

Native pointer: /joint_analysis/provenance/5; canonical SHA-256: 0f6efc16e7d9fcc7869ce8a73ac758aad13253736d10536a66bf067dbe1381e9

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/5/bound_id; canonical SHA-256: 81a2e38f18361a22f545e5d196c3706082517f1eec3155c02b432d002a8a8b3b

BL_SPEC_joint_expected_cost__main__b_joint_lower_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/5/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/5/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/5/proof_refs; canonical SHA-256: ba6a46e461564ee2037c7dc8ff639bdce4caf23676ed4c8056a5a7f5053d74d8

#### Native item 1

Native pointer: /joint_analysis/provenance/5/proof_refs/0; canonical SHA-256: 728ae8137adaa1f8be56505f06ced0a03339545effe970737fb3550652ee2cdd

BL_SPEC_joint_expected_cost__main__proof_joint_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/5/source_domain; canonical SHA-256: 2146486fbb364a0a9e98e710933a434cf94f5ea7696b1357dc417693350ed465

#### Native item 1

Native pointer: /joint_analysis/provenance/5/source_domain/0; canonical SHA-256: b9b6264f58b58c426442387dfe1e643d1b0bd1217a111ab8f6f5965d5056ed7a

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa^2$, and $\Lambda_\Phi\ge B_\Phi=(1+\kappa)^2L(1+\theta)$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/5/target_domain; canonical SHA-256: 6bae23cf0d6cda00d829e2afeab40aede0eccff7cb5428411da099a4589a776a

#### Native item 1

Native pointer: /joint_analysis/provenance/5/target_domain/0; canonical SHA-256: e6ab815bee315072b537e5ed5d5daeda80d9047ca7d6f1143930cee8f1fc53fe

BL_SPEC_joint_expected_cost__main__r_source_j_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/5/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/5/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 7

Native pointer: /joint_analysis/provenance/6; canonical SHA-256: e756a3d3d64dc102150e1c23ca1ba5e544b01827bc82a645cc06a9cf013152f6

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/6/bound_id; canonical SHA-256: 4d7eaae3609ea1b1d252fa370369e3335a79801b315bce335b820ea13634c7ea

BL_SPEC_joint_expected_cost__main__b_curvature_upper_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/6/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/6/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/6/proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/provenance/6/proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/6/source_domain; canonical SHA-256: 7dbe0390c401f541cf45ac31e7b633341d7459a5da7d153b59d6931e5e6c06dd

#### Native item 1

Native pointer: /joint_analysis/provenance/6/source_domain/0; canonical SHA-256: 304b387f8224c034a1a9b2d3cb98a4ca194f16dc6ea0bccd7fab1c7e4850dc4e

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa$, and $\Lambda_\Phi=C_F L\kappa^2$, where $C_F\ge C_*$ is a fixed sufficiently large numerical constant. $C_F$ does not vary as a joint asymptotic parameter.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/6/target_domain; canonical SHA-256: 3719ebe1497a86db849b3e44e66bde19ab32fd58bb582ade6004c52c4e5c9cb3

#### Native item 1

Native pointer: /joint_analysis/provenance/6/target_domain/0; canonical SHA-256: 98f79d330a6d9f493eab452e42d942ea688ac69d293b6a070ed5b6de165c2158

BL_SPEC_joint_expected_cost__main__r_source_c_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/6/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/6/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 8

Native pointer: /joint_analysis/provenance/7; canonical SHA-256: 9a3bd618cd334ac257c0c52a6205c39e29791cbe2c10a3e3a1e26534ef7e4068

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/7/bound_id; canonical SHA-256: 48026746550b83fccffc0a6712faf50fcb925dada190809d2833b0a40793c9b8

BL_SPEC_joint_expected_cost__main__b_curvature_lower_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/7/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/7/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/7/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/7/proof_refs; canonical SHA-256: 6514402e8d6ff3bd1ef74ad2b47c294c22ec196d89ca3bfabbcc9e222b7f20a9

#### Native item 1

Native pointer: /joint_analysis/provenance/7/proof_refs/0; canonical SHA-256: 0b38b45392e401d88784b8d7d56011383ea515bb875014801427c28ccdf990d8

BL_SPEC_joint_expected_cost__main__proof_curvature_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/7/source_domain; canonical SHA-256: 7dbe0390c401f541cf45ac31e7b633341d7459a5da7d153b59d6931e5e6c06dd

#### Native item 1

Native pointer: /joint_analysis/provenance/7/source_domain/0; canonical SHA-256: 304b387f8224c034a1a9b2d3cb98a4ca194f16dc6ea0bccd7fab1c7e4850dc4e

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa$, and $\Lambda_\Phi=C_F L\kappa^2$, where $C_F\ge C_*$ is a fixed sufficiently large numerical constant. $C_F$ does not vary as a joint asymptotic parameter.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/7/target_domain; canonical SHA-256: 3719ebe1497a86db849b3e44e66bde19ab32fd58bb582ade6004c52c4e5c9cb3

#### Native item 1

Native pointer: /joint_analysis/provenance/7/target_domain/0; canonical SHA-256: 98f79d330a6d9f493eab452e42d942ea688ac69d293b6a070ed5b6de165c2158

BL_SPEC_joint_expected_cost__main__r_source_c_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/7/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/7/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 9

Native pointer: /joint_analysis/provenance/8; canonical SHA-256: 14611fcdc8c71f42842a9cb69bf959b1b90b1e072c1fed3c105b844d1ae29547

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/8/bound_id; canonical SHA-256: 4df34e14d8aa539a488a08f035f0e108107220b393a67c33eeb1647b0864f958

BL_SPEC_joint_expected_cost__main__b_constant_blocks_upper_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/8/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/8/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/8/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/8/proof_refs; canonical SHA-256: 6b331f2c681d05194a80b1067879f9112282e7a4b3de8eacdc2808ad900f5c69

#### Native item 1

Native pointer: /joint_analysis/provenance/8/proof_refs/0; canonical SHA-256: e3be7dde89be4039356e7db3ae038bd2124a4b6174e7e75b1f56a5a43a54379a

BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/8/source_domain; canonical SHA-256: ebc238beba88b7e419f33ed891a279ecae779c629c85bcb5f15d185d748f12c1

#### Native item 1

Native pointer: /joint_analysis/provenance/8/source_domain/0; canonical SHA-256: 7407a3a188b44b3db0a73c518ad72d3db480d812fd8e51bb0e4338057e40e577

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\rho=0$, $R_0=0$, $L>\mu>0$, and $\Lambda_\Phi\ge L\kappa^2$. The oracle has a global uniform conditional variance bound and permits arbitrarily large finite query displacements; every difference uses two fresh calls.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/8/target_domain; canonical SHA-256: b6b90bd59ec2cce5f33e3478de57832c7d8809f7d19c55674e71694425694c9c

#### Native item 1

Native pointer: /joint_analysis/provenance/8/target_domain/0; canonical SHA-256: 1dacb08574d7ecf406cb02c96a202e7c1c4989e2786ca6fa9ea11e5765a1e575

BL_SPEC_joint_expected_cost__main__r_source_k_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/8/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/8/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 10

Native pointer: /joint_analysis/provenance/9; canonical SHA-256: 9a249aa79acde922c47859ad9ce8f9ab0cebb1e74e06cdc8eb0a15850fe99496

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/9/bound_id; canonical SHA-256: 50173b8587a50f608a8a075aeeb0747b5d52bca4631926f133a98a964bafdf4e

BL_SPEC_joint_expected_cost__main__b_constant_blocks_lower_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/9/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/9/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/9/proof_refs; canonical SHA-256: 6b331f2c681d05194a80b1067879f9112282e7a4b3de8eacdc2808ad900f5c69

#### Native item 1

Native pointer: /joint_analysis/provenance/9/proof_refs/0; canonical SHA-256: e3be7dde89be4039356e7db3ae038bd2124a4b6174e7e75b1f56a5a43a54379a

BL_SPEC_joint_expected_cost__main__proof_constant_blocks_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/9/source_domain; canonical SHA-256: ebc238beba88b7e419f33ed891a279ecae779c629c85bcb5f15d185d748f12c1

#### Native item 1

Native pointer: /joint_analysis/provenance/9/source_domain/0; canonical SHA-256: 7407a3a188b44b3db0a73c518ad72d3db480d812fd8e51bb0e4338057e40e577

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\rho=0$, $R_0=0$, $L>\mu>0$, and $\Lambda_\Phi\ge L\kappa^2$. The oracle has a global uniform conditional variance bound and permits arbitrarily large finite query displacements; every difference uses two fresh calls.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/9/target_domain; canonical SHA-256: b6b90bd59ec2cce5f33e3478de57832c7d8809f7d19c55674e71694425694c9c

#### Native item 1

Native pointer: /joint_analysis/provenance/9/target_domain/0; canonical SHA-256: 1dacb08574d7ecf406cb02c96a202e7c1c4989e2786ca6fa9ea11e5765a1e575

BL_SPEC_joint_expected_cost__main__r_source_k_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/9/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/9/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 11

Native pointer: /joint_analysis/provenance/10; canonical SHA-256: 85d8b8b2ba4a9f51e078e6dc5feac8331dfb3cf072924d623c4f48d3d25977d8

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/10/bound_id; canonical SHA-256: ed83cdf798d05b5c416ce9ca1b546ecf5c3ee2a576ab561a9c6ce4c8ce679547

BL_SPEC_joint_expected_cost__main__b_source_zero_upper_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/10/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/10/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/10/proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/provenance/10/proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/10/source_domain; canonical SHA-256: 61be9e5576a1011316cd7fc6ba8a79dbd9d5b5f05118ed5a587cb4f170fd7d34

#### Native item 1

Native pointer: /joint_analysis/provenance/10/source_domain/0; canonical SHA-256: e1b594b6ad523c483c859b3e83787ec4adcb708e1b8055bf9b00f3ebf39d6968

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. At least one of: (i) $\rho=0$, $\kappa>1$ and $\varepsilon\ge S_0$; (ii) $\kappa=1$ and $\varepsilon\ge S=\sqrt{2L\Delta}$. Here $q_{\rm geom}=\sqrt{\kappa^2-1}$, $G_{\rm geom}=\sqrt{2L\Delta}$, $t_0=\min\{q_{\rm geom}G_{\rm geom}/\kappa,2L\}$, and $S_0=\sqrt{G_{\rm geom}^2-t_0^2}+q_{\rm geom}t_0$. No lower bound on $\Lambda_\Phi$ is needed for this sufficient zero-cost statement.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/10/target_domain; canonical SHA-256: 63fd452e055da983b7f9846802e5d543530a3674e4b0335d39e429f7a7daa8ac

#### Native item 1

Native pointer: /joint_analysis/provenance/10/target_domain/0; canonical SHA-256: 31169ed56bf35653e2a1bceddc61630c0db4ec6dd63de8334fcfe948f12e553f

BL_SPEC_joint_expected_cost__main__r_source_z_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/10/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/10/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 12

Native pointer: /joint_analysis/provenance/11; canonical SHA-256: 2c5fe1ecc08c43c40d192bc577ef22f7d46ab5d14d8cb27deb7aaebab83be9d7

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/11/bound_id; canonical SHA-256: 8920b10739b1ae8e2876aae0c57c07ab2ec89a1e20133ab1da0b36b70c9f88f0

BL_SPEC_joint_expected_cost__main__b_source_zero_lower_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/11/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/11/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/11/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/11/proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/provenance/11/proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/11/source_domain; canonical SHA-256: 61be9e5576a1011316cd7fc6ba8a79dbd9d5b5f05118ed5a587cb4f170fd7d34

#### Native item 1

Native pointer: /joint_analysis/provenance/11/source_domain/0; canonical SHA-256: e1b594b6ad523c483c859b3e83787ec4adcb708e1b8055bf9b00f3ebf39d6968

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. At least one of: (i) $\rho=0$, $\kappa>1$ and $\varepsilon\ge S_0$; (ii) $\kappa=1$ and $\varepsilon\ge S=\sqrt{2L\Delta}$. Here $q_{\rm geom}=\sqrt{\kappa^2-1}$, $G_{\rm geom}=\sqrt{2L\Delta}$, $t_0=\min\{q_{\rm geom}G_{\rm geom}/\kappa,2L\}$, and $S_0=\sqrt{G_{\rm geom}^2-t_0^2}+q_{\rm geom}t_0$. No lower bound on $\Lambda_\Phi$ is needed for this sufficient zero-cost statement.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/11/target_domain; canonical SHA-256: 63fd452e055da983b7f9846802e5d543530a3674e4b0335d39e429f7a7daa8ac

#### Native item 1

Native pointer: /joint_analysis/provenance/11/target_domain/0; canonical SHA-256: 31169ed56bf35653e2a1bceddc61630c0db4ec6dd63de8334fcfe948f12e553f

BL_SPEC_joint_expected_cost__main__r_source_z_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/11/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/11/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 13

Native pointer: /joint_analysis/provenance/12; canonical SHA-256: 9edba3f71ae63b4c2c32afc6e6d21ae00c683052023c3c966ca48ce20a33103c

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/12/bound_id; canonical SHA-256: 6706fab5abc9e126df2b3423af4eeb158dd0f545784bec459360ebe9e1ef7b12

BL_SPEC_joint_expected_cost__main__b_affine_activation_lower_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/12/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/12/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/12/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/12/proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/provenance/12/proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/12/source_domain; canonical SHA-256: 72271c92ef07f273ecb977a7a6cc049d2d1bdb36733b170ea912028962da036d

#### Native item 1

Native pointer: /joint_analysis/provenance/12/source_domain/0; canonical SHA-256: f1eb31df719d650fbb6651121e0f86f78ae1a376729ce28dd950e8ff42ceb034

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\rho=0$, $\kappa>1$, $\Lambda_\Phi\ge L\kappa^2$, and $0<\varepsilon<S_0$, with $S_0$ defined in Z. The strict inequality entails $S_0>0$.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/12/target_domain; canonical SHA-256: 3fecda59dc564f40bc42cb406a6f7fd0bb0730e9661d3661d4ae43bd94a385a4

#### Native item 1

Native pointer: /joint_analysis/provenance/12/target_domain/0; canonical SHA-256: ea0d351363e3f91c44a99367b84cedd7037299618a761947d290fbb17b2e330d

BL_SPEC_joint_expected_cost__main__r_source_a_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/12/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/12/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 14

Native pointer: /joint_analysis/provenance/13; canonical SHA-256: fddc0fc19fcc99ba0e10c53f08314bb89fb9ba32f77a5ccd592f6450365f40c8

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/13/bound_id; canonical SHA-256: 513ed8684c9f999fd43305784ab68031f32555559ca4115fde4bc8216135cdc7

BL_SPEC_joint_expected_cost__main__b_fixed_structural_accuracy_upper_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/13/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/13/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/13/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/13/proof_refs; canonical SHA-256: 147cb940899e99c868787aee4f90641ed242e241fd672f4c67f07c3ecd979566

#### Native item 1

Native pointer: /joint_analysis/provenance/13/proof_refs/0; canonical SHA-256: aabbbcc3bfba9fe929a403008b10496460982efc68d28064b26c986649a3c20b

BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/13/source_domain; canonical SHA-256: 91a6e417dceef5af13ea8c1df7f77d8a86910f9efa4cdadef0d0b394893fd217

#### Native item 1

Native pointer: /joint_analysis/provenance/13/source_domain/0; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/13/target_domain; canonical SHA-256: 6bdcc8f0590e885d10c8bdeb1374c38e9e6e650cca3e22aef361155c152c0c22

#### Native item 1

Native pointer: /joint_analysis/provenance/13/target_domain/0; canonical SHA-256: 8e9ec20cfdbc2c52c7b5317e8145b9f1f3209e46339d09dc8c63527d1935b7fd

BL_SPEC_joint_expected_cost__main__r_fixed_structural_accuracy_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/13/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/13/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native item 15

Native pointer: /joint_analysis/provenance/14; canonical SHA-256: 0a4666847c816d7894142f40dd8816cc85538d04d86bb19392a67177ddd244a5

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/14/bound_id; canonical SHA-256: d6b154774f132dc82521645f92791b0ccbde46aec4ee7696a78f871bd49e6666

BL_SPEC_joint_expected_cost__main__b_fixed_structural_accuracy_lower_20261126

#### Native field: origin

Native pointer: /joint_analysis/provenance/14/origin; canonical SHA-256: 1922c68a1f2df25b887438036cf7860d0789d22d54129c91400d3abe4444707a

source_statement_with_contract_mapping

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/14/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/provenance/14/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/14/proof_refs; canonical SHA-256: 147cb940899e99c868787aee4f90641ed242e241fd672f4c67f07c3ecd979566

#### Native item 1

Native pointer: /joint_analysis/provenance/14/proof_refs/0; canonical SHA-256: aabbbcc3bfba9fe929a403008b10496460982efc68d28064b26c986649a3c20b

BL_SPEC_joint_expected_cost__main__proof_fixed_accuracy_contract_20261126

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/14/source_domain; canonical SHA-256: 91a6e417dceef5af13ea8c1df7f77d8a86910f9efa4cdadef0d0b394893fd217

#### Native item 1

Native pointer: /joint_analysis/provenance/14/source_domain/0; canonical SHA-256: b4c9184a21b7172f79193a744ecb0ab8df1515d84e89d9da2383d53100a5107c

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. Fix all primitive structural budgets $P=(L,\mu,\rho,\Delta,\sigma_f,\sigma_g,R_0)$ and $L_f,L_g,C_f,\Lambda_\Phi$, with $L>\mu>0$, $\rho>0$, $\Delta>0$, $\sigma_g>0$, and $\Lambda_\Phi\ge B_\Phi$. Only $\varepsilon$ varies, with $0<\varepsilon<\varepsilon_P$. Dimensions remain under the arbitrary finite-dimensional supremum.

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/14/target_domain; canonical SHA-256: 6bdcc8f0590e885d10c8bdeb1374c38e9e6e650cca3e22aef361155c152c0c22

#### Native item 1

Native pointer: /joint_analysis/provenance/14/target_domain/0; canonical SHA-256: 8e9ec20cfdbc2c52c7b5317e8145b9f1f3209e46339d09dc8c63527d1935b7fd

BL_SPEC_joint_expected_cost__main__r_fixed_structural_accuracy_guard_20261126

#### Native field: mapping

Native pointer: /joint_analysis/provenance/14/mapping; canonical SHA-256: 7b7f844c0b1baa2338272d0793813556d7f3bfddcf117f762861d84e69e136bf

Exact stated native guard; source-reported theorem with target-contract checks.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/14/source_locator; canonical SHA-256: 5082e1fe6dc4f45bc28e108ced287881ae6ec3601996138f1430c16ca158c072

See the bound evidence record and PDF page locators.

#### Native field: source_regions_20261126

Native pointer: /joint_analysis/source_regions_20261126; canonical SHA-256: da2c18c0e5cf5792048c02ad48542373b28b585100420fb19567538a9bd7acd7

#### Native field: definitions

Native pointer: /joint_analysis/source_regions_20261126/definitions; canonical SHA-256: 6cf9a29cb23fd41e024d12f0bd99c81ee1f90208606eb2d3d0a7508ae16165a6

#### Native field: J

Native pointer: /joint_analysis/source_regions_20261126/definitions/J; canonical SHA-256: b9b6264f58b58c426442387dfe1e643d1b0bd1217a111ab8f6f5965d5056ed7a

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa^2$, and $\Lambda_\Phi\ge B_\Phi=(1+\kappa)^2L(1+\theta)$.

#### Native field: C

Native pointer: /joint_analysis/source_regions_20261126/definitions/C; canonical SHA-256: 304b387f8224c034a1a9b2d3cb98a4ca194f16dc6ea0bccd7fab1c7e4850dc4e

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\kappa\ge2$, $1\le\theta\le\kappa$, and $\Lambda_\Phi=C_F L\kappa^2$, where $C_F\ge C_*$ is a fixed sufficiently large numerical constant. $C_F$ does not vary as a joint asymptotic parameter.

#### Native field: K

Native pointer: /joint_analysis/source_regions_20261126/definitions/K; canonical SHA-256: 7407a3a188b44b3db0a73c518ad72d3db480d812fd8e51bb0e4338057e40e577

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\Delta>0$ and $0<\varepsilon\le c_0\min\{L,\sqrt{L\Delta}\}$, where $0<c_0\le1/4$ is a fixed sufficiently small numerical constant common to the cited finite collection of source theorems. $\rho=0$, $R_0=0$, $L>\mu>0$, and $\Lambda_\Phi\ge L\kappa^2$. The oracle has a global uniform conditional variance bound and permits arbitrarily large finite query displacements; every difference uses two fresh calls.

#### Native field: Z

Native pointer: /joint_analysis/source_regions_20261126/definitions/Z; canonical SHA-256: e1b594b6ad523c483c859b3e83787ec4adcb708e1b8055bf9b00f3ebf39d6968

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. At least one of: (i) $\rho=0$, $\kappa>1$ and $\varepsilon\ge S_0$; (ii) $\kappa=1$ and $\varepsilon\ge S=\sqrt{2L\Delta}$. Here $q_{\rm geom}=\sqrt{\kappa^2-1}$, $G_{\rm geom}=\sqrt{2L\Delta}$, $t_0=\min\{q_{\rm geom}G_{\rm geom}/\kappa,2L\}$, and $S_0=\sqrt{G_{\rm geom}^2-t_0^2}+q_{\rm geom}t_0$. No lower bound on $\Lambda_\Phi$ is needed for this sufficient zero-cost statement.

#### Native field: A

Native pointer: /joint_analysis/source_regions_20261126/definitions/A; canonical SHA-256: f1eb31df719d650fbb6651121e0f86f78ae1a376729ce28dd950e8ff42ceb034

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\rho=0$, $\kappa>1$, $\Lambda_\Phi\ge L\kappa^2$, and $0<\varepsilon<S_0$, with $S_0$ defined in Z. The strict inequality entails $S_0>0$.

#### Native field: old_E

Native pointer: /joint_analysis/source_regions_20261126/old_E; canonical SHA-256: b3a81a39bbac271ffa94679366316e5ec6032134654420e2b37140620bc87820

All native parameter/model constraints and $2\bar\Lambda_\Phi\Delta\le\varepsilon^2$.

#### Native field: old_S

Native pointer: /joint_analysis/source_regions_20261126/old_S; canonical SHA-256: ab62e307c0564ad64cf52a1a210d958650a6845dfeb7aa9713895286dfcd346f

$L_f=L_g=C_f=L>0$, $0<\Delta\le L$, $\kappa=L/\mu\ge C_s$, $C_s\le\theta=\rho/\mu\le c_s\kappa$, $0<\varepsilon\le c_s\min\{L,\kappa\sqrt{L\Delta}\}$, $\Lambda_\Phi\ge B_\Phi$, $R_0,\sigma_f,\sigma_g\ge0$. Here $c_s>0$ is a sufficiently small and $C_s>0$ a sufficiently large universal constant fixed by the normalization proof. Let $T_0=\kappa^2L\Delta/\varepsilon^2$, $K_0=T_0(1+\theta^2\kappa^6\sigma_g^2L^2/\varepsilon^4)$, $D_0=\lceil C_d(1+K_0)(1+T_0)\theta^2\log(2+K_0T_0)\rceil$ for a sufficiently large universal $C_d$. Require $d_x\ge D_0$ and $d_y\ge D_0+2$, or take the stated worst case over arbitrary finite dimensions.

#### Native field: old_N

Native pointer: /joint_analysis/source_regions_20261126/old_N; canonical SHA-256: 20681456a0777796bb2d3640970998631f90ba7aaaf4f79cd23b85002f1773a6

The complete S predicate, additionally $\theta\le2C_s$ and $\sigma_g>0$. Write $D_\sigma=(1+\kappa)^2 E_\rho^2\sigma_g^2/\varepsilon^4$. Require $B_\Phi\Delta/\varepsilon^2\ge1$, $D_\sigma\ge1+\kappa$, $E_\rho^2\sigma_g^2/\varepsilon^2\ge\sigma_f^2$, and $E_\rho^2/\varepsilon^2\ge\kappa^2+1$.

#### Native field: precedence

Native pointer: /joint_analysis/source_regions_20261126/precedence; canonical SHA-256: d7452615ae8f779c2e5208d38adf0e669f62bafaee626103e475806347269cdd

#### Native item 1

Native pointer: /joint_analysis/source_regions_20261126/precedence/0; canonical SHA-256: 43e6e2bebb3774311cf0c867d2fae5da733792224e8bac1d455eff172ff6af27

E

#### Native item 2

Native pointer: /joint_analysis/source_regions_20261126/precedence/1; canonical SHA-256: 468bcc9e8c2c33fb07e7a3b88170dd5e81a8a0ba85d03d58c82a3fa161477c3b

Z

#### Native item 3

Native pointer: /joint_analysis/source_regions_20261126/precedence/2; canonical SHA-256: 88d38f39d978353fa8f9a7feb4126be7e3ec54a85459bf3724566c21b2f12b93

C split by old N / old S minus N / outside old S

#### Native item 4

Native pointer: /joint_analysis/source_regions_20261126/precedence/3; canonical SHA-256: ca5b9a0236036a6c086bd2612fd0a4995b6fc272d7ee7350af45f72d38387af6

J minus C split by old N / old S minus N / outside old S

#### Native item 5

Native pointer: /joint_analysis/source_regions_20261126/precedence/4; canonical SHA-256: 65aef5e867d44f116ccec3af3261363bd462c25c66cd08023dc69747efc213f4

K

#### Native item 6

Native pointer: /joint_analysis/source_regions_20261126/precedence/5; canonical SHA-256: 798640599597df7a8daa32b1132f07850a68b5e71bd295650399a38074f52804

A

#### Native item 7

Native pointer: /joint_analysis/source_regions_20261126/precedence/6; canonical SHA-256: 064e57f6fd487d3b93b428c29d822bcf6fb09244614bcb2a63a2291e3161b4e2

old N remaining

#### Native item 8

Native pointer: /joint_analysis/source_regions_20261126/precedence/7; canonical SHA-256: 1699d36e19f2439f6dbc4e2938946b341afb07bb574ecebb8e60d9097314b4fe

old S minus N remaining

#### Native item 9

Native pointer: /joint_analysis/source_regions_20261126/precedence/8; canonical SHA-256: 46bfa3f8dc12462586f41c3a07dfe8439318889dc38a781c75882f7977550ff7

old residual remaining

#### Native field: symbols

Native pointer: /joint_analysis/source_regions_20261126/symbols; canonical SHA-256: c33b66c068f8b82397eec0c4260ad7a0f3e32811d34a0c00c64c3b324bd14209

#### Native field: S0

Native pointer: /joint_analysis/source_regions_20261126/symbols/S0; canonical SHA-256: b70b8cf0a51257f1a2ad6aa79f8fac2b6efd931c213227235c2429669d9f4a00

\sqrt{G_{\rm geom}^2-t_0^2}+\sqrt{\kappa^2-1}\,t_0

#### Native field: G_geom

Native pointer: /joint_analysis/source_regions_20261126/symbols/G_geom; canonical SHA-256: b1a5cdb244d70f51ffdcf4503d9fc2263c151927da2ffdff3026b55d26ddf8e1

\sqrt{2L\Delta}

#### Native field: t0

Native pointer: /joint_analysis/source_regions_20261126/symbols/t0; canonical SHA-256: 6e69107db7bc8774d1795edf3a9a2eef8cef31f3e71890b92416ebc58722393e

\min\{\sqrt{\kappa^2-1}\sqrt{2L\Delta}/\kappa,2L\}

#### Native field: D

Native pointer: /joint_analysis/source_regions_20261126/symbols/D; canonical SHA-256: bc5715d770eee0e7df80cb529398fccd4eba8ddd2dd00c688a925cd410cb4f2e

L\chi\kappa^{5/2}\Delta\varepsilon^{-2}

#### Native field: U

Native pointer: /joint_analysis/source_regions_20261126/symbols/U; canonical SHA-256: 4a74e4d6a2d16d70591179b7f870856e3436f5d155a60d8a930ae1f9a75e3937

L\kappa^4\sigma_f^2\Delta\varepsilon^{-4}

#### Native field: G

Native pointer: /joint_analysis/source_regions_20261126/symbols/G; canonical SHA-256: 34b6cae642bfbda4c91b6ce2edead9d3849dff3eae244dd3ab9eb84d363799ac

L^3\theta^2\chi\kappa^8\sigma_g^2\Delta\varepsilon^{-6}

#### Native field: D_curv

Native pointer: /joint_analysis/source_regions_20261126/symbols/D_curv; canonical SHA-256: ab9388fab301f3abe8fc75d7fea9f908da88260675655c2bef6e92bcd413e060

L\kappa^{5/2}\Delta\varepsilon^{-2}

#### Native field: G_curv

Native pointer: /joint_analysis/source_regions_20261126/symbols/G_curv; canonical SHA-256: 27e5767fcaeacdff001c8d9e0c76ec5993b5ed9cbc3297d128e92348c7e42302

L^3\theta^2\kappa^8\sigma_g^2\Delta\varepsilon^{-6}

#### Native field: scope

Native pointer: /joint_analysis/source_regions_20261126/scope; canonical SHA-256: 911061800a4d3f75c03beca63af1ac758605c2b34b9bdab93bcd5a29e6fc7fa5

Each source validity guard includes the native common-budget normalization; active predicates refer to these complete guards. New rows concern q1 except the explicitly separate fixed-structural accuracy quantity.

#### Native field: guard_region_refs

Native pointer: /joint_analysis/source_regions_20261126/guard_region_refs; canonical SHA-256: cf35e055b90a24548eca5a09b6b7be3d29c441e36f6f656cecf307c720adfc17

#### Native field: J

Native pointer: /joint_analysis/source_regions_20261126/guard_region_refs/J; canonical SHA-256: e6ab815bee315072b537e5ed5d5daeda80d9047ca7d6f1143930cee8f1fc53fe

BL_SPEC_joint_expected_cost__main__r_source_j_guard_20261126

#### Native field: C

Native pointer: /joint_analysis/source_regions_20261126/guard_region_refs/C; canonical SHA-256: 98f79d330a6d9f493eab452e42d942ea688ac69d293b6a070ed5b6de165c2158

BL_SPEC_joint_expected_cost__main__r_source_c_guard_20261126

#### Native field: K

Native pointer: /joint_analysis/source_regions_20261126/guard_region_refs/K; canonical SHA-256: 1dacb08574d7ecf406cb02c96a202e7c1c4989e2786ca6fa9ea11e5765a1e575

BL_SPEC_joint_expected_cost__main__r_source_k_guard_20261126

#### Native field: Z

Native pointer: /joint_analysis/source_regions_20261126/guard_region_refs/Z; canonical SHA-256: 31169ed56bf35653e2a1bceddc61630c0db4ec6dd63de8334fcfe948f12e553f

BL_SPEC_joint_expected_cost__main__r_source_z_guard_20261126

#### Native field: A

Native pointer: /joint_analysis/source_regions_20261126/guard_region_refs/A; canonical SHA-256: ea0d351363e3f91c44a99367b84cedd7037299618a761947d290fbb17b2e330d

BL_SPEC_joint_expected_cost__main__r_source_a_guard_20261126

#### Native field: historical_region_refs

Native pointer: /joint_analysis/source_regions_20261126/historical_region_refs; canonical SHA-256: 44709ca86e4c7755337207a3df82c36ea1697027ce3c77799825d1173fe5ee50

#### Native field: E

Native pointer: /joint_analysis/source_regions_20261126/historical_region_refs/E; canonical SHA-256: 3059026c3591fcd4af002a5f6c68561b2c8bd84793d86d29319dbb30a8cf931c

BL_SPEC_joint_expected_cost__main__r_effective_zero_20261122

#### Native field: S

Native pointer: /joint_analysis/source_regions_20261126/historical_region_refs/S; canonical SHA-256: 834bc3ddd67b355d467aed3101acf4f0dbd3e8f078a0ee41cbff45dd0bd427ba

BL_SPEC_joint_expected_cost__main__r_source_compatible_20261122

#### Native field: N

Native pointer: /joint_analysis/source_regions_20261126/historical_region_refs/N; canonical SHA-256: c9adb3314e51120309898403308df6ac3b13e7fddf4e0a030bae4cb34de542da

BL_SPEC_joint_expected_cost__main__r_bounded_variation_noise_20261122

#### Native field: scope_predicates

Native pointer: /joint_analysis/source_regions_20261126/scope_predicates; canonical SHA-256: 6a03a0bd1a10173e6d3e0a5f0a81ee4c34bf1eea4c3b2393f88ca4ffa4d925c1

Native ASTs encode each new validity guard and its active intersections. Existing E/S/N regimes remain exact preserved references; their original theorem and dimensional quantifiers are unchanged.

#### Native field: structural_findings_20261126

Native pointer: /joint_analysis/structural_findings_20261126; canonical SHA-256: 8e459d07b7e7fb6a10e8f793d85c4a50ec16a7824bc768611de2138572a5a5cb

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/0; canonical SHA-256: aa3e27369e470cd54c753c9b9bc0be3a6106cc4e75d6c0988aea9c40b1d72069

#### Native field: id

Native pointer: /joint_analysis/structural_findings_20261126/0/id; canonical SHA-256: 7e16607b54c8afc26d31824dd007e434efdc1ab656aa03e139e9612a217722c4

BL_SPEC_joint_expected_cost__main__structure_perfect_conditioning_20261126

#### Native field: kind

Native pointer: /joint_analysis/structural_findings_20261126/0/kind; canonical SHA-256: f183253a10be84fd221cdaf80ae62e186b168c424b28b31c4dddee844966bac7

oracle_equivalence_and_risk_upper

#### Native field: predicate

Native pointer: /joint_analysis/structural_findings_20261126/0/predicate; canonical SHA-256: d50e4dec51fd84d6098fc48b3941af02e30507732d33997a55a05483a9e835a1

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\kappa=1$, with arbitrary $\rho,R_0,\sigma_f,\sigma_g$.

#### Native field: statement

Native pointer: /joint_analysis/structural_findings_20261126/0/statement; canonical SHA-256: 394b1b53d5839ec48a2ae63c37e6cb524c42311bfc55e21cb14332b10ac0ac7c

$y^*(x)=a$ is constant. For integers $m\ge0$, $T,b\ge1$, an algorithm uses exactly $m+Tb$ calls and has risk at most $\sqrt{2L\Delta/T+\gamma_m^2+\sigma_f^2/b}$, $\gamma_0^2=L^2R_0^2$, $\gamma_m^2=L^2R_0^2\sigma_g^2/(mL^2R_0^2+\sigma_g^2)$ for $m\ge1$, with $0/0=0$. If $R_0=0$ and $\Lambda_\Phi\ge L$, the problem is exactly equivalent in expected risk and expected calls to ordinary $L$-smooth nonconvex SFO with gap $\Delta$ and variance budget $\sigma_f^2$.

#### Native field: independent_curvature

Native pointer: /joint_analysis/structural_findings_20261126/0/independent_curvature; canonical SHA-256: b73aba242b2382b49ee45eb94f2ab46f7346d5ca36a5c498b69fd814e56c6b3a

The risk upper passes to every curvature subclass. The two-direction ordinary-SFO equivalence and exact zero-threshold necessity require Lambda_Phi>=L.

#### Native field: evidence_refs

Native pointer: /joint_analysis/structural_findings_20261126/0/evidence_refs; canonical SHA-256: 286c31cff248207d42b5db7c53fe1531600bbd02611eb222fb71cb410f3b1308

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/0/evidence_refs/0; canonical SHA-256: ffa4b3bcafd3c5e175fec72f2f0ec96a7e23c61eebb22cd7372388e4bf71d995

BL_SPEC_joint_expected_cost__main__e_endpoint_structure_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/structural_findings_20261126/0/proof_refs; canonical SHA-256: 2e76295aa6baea439b6a1b8627a17e5e65f00ac70f2a812da8876b8af8a8a1fa

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/0/proof_refs/0; canonical SHA-256: b857fc5495bc7f583e2c9bbaf2fa8d789661f059e8882fdcc96aa6851e6687d9

BL_SPEC_joint_expected_cost__main__proof_endpoint_structure_contract_20261126

#### Native field: source_refs

Native pointer: /joint_analysis/structural_findings_20261126/0/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/0/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native item 2

Native pointer: /joint_analysis/structural_findings_20261126/1; canonical SHA-256: 222f09d269076ef4a9fe4e0d823b2c846114be290b4d375d3bdc91cbe127371b

#### Native field: id

Native pointer: /joint_analysis/structural_findings_20261126/1/id; canonical SHA-256: 2c5859ef19eb03c9cb6ed06934257d6ee5e131b554fa90e7668357244b5736b7

BL_SPEC_joint_expected_cost__main__structure_affine_zero_threshold_20261126

#### Native field: kind

Native pointer: /joint_analysis/structural_findings_20261126/1/kind; canonical SHA-256: 40eb24862fd1f3377eb4406707da3a55150f5e7c1d3263ec405f3dbf49701a49

exact_zero_cost_boundary

#### Native field: predicate

Native pointer: /joint_analysis/structural_findings_20261126/1/predicate; canonical SHA-256: 7deb4b4d22b826b3155766ad4c2d909e1c6a17504dedf8aaeba745a68bd6c08d

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\rho=0$, $\Lambda_\Phi\ge L\kappa^2$.

#### Native field: statement

Native pointer: /joint_analysis/structural_findings_20261126/1/statement; canonical SHA-256: 09b344b8c5ee55a78df7d142f211d661c81b34beb6b37383c127db9060230f1f

The exact zero-query minimax risk is $S_0$; $Q^*=0$ if and only if $\varepsilon\ge S_0$, including equality. When $\Delta=0$, $S_0=0$.

#### Native field: evidence_refs

Native pointer: /joint_analysis/structural_findings_20261126/1/evidence_refs; canonical SHA-256: dd9205534ee44d9edfdd6f8c9fd9ffb59f5e9fe650e0c4615053ee8f90d84d48

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/1/evidence_refs/0; canonical SHA-256: ae92ed5872921e48f71af79d8a3b4f1292394c431b1b6bf7811152488d1a2b13

BL_SPEC_joint_expected_cost__main__e_zero_activation_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/structural_findings_20261126/1/proof_refs; canonical SHA-256: 6270322a9687dd5834eb0cc76d2f8d0b1470a3ffddc7dfdf3740f3d3691b6025

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/1/proof_refs/0; canonical SHA-256: a2817aac8df941cc94d1b44cefc147512408527a4df24a2fa9216aec694c6555

BL_SPEC_joint_expected_cost__main__proof_zero_activation_contract_20261126

#### Native field: source_refs

Native pointer: /joint_analysis/structural_findings_20261126/1/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/1/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

#### Native item 3

Native pointer: /joint_analysis/structural_findings_20261126/2; canonical SHA-256: c163dd4f7c1d89d967eb1aa1cb9a0939ba5f982fe99a16eb40b6d5c749398ec7

#### Native field: id

Native pointer: /joint_analysis/structural_findings_20261126/2/id; canonical SHA-256: d0895b929869b442b59fcea4923e84e438a17b8c68b26f217f89a1f2f56b653b

BL_SPEC_joint_expected_cost__main__structure_uniform_lower_noise_20261126

#### Native field: kind

Native pointer: /joint_analysis/structural_findings_20261126/2/kind; canonical SHA-256: 1dbcb21e4d77b8644659bb29dc1c50734ccadf6ce9d62664b6d445a222d9030c

uniform_noise_finiteness_classification

#### Native field: quantity

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity; canonical SHA-256: 70ab9f27f20c36e18423c1fc4fd07c6cfe8beeb6a45f111e62eb51a1166c853c

#### Native field: id

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity/id; canonical SHA-256: 7cee1fce78fd2f5472c0fae7a74f2a3953f7e1f1e5f6c221bc87174112411d42

BL_SPEC_joint_expected_cost__main__q_uniform_lower_noise_20261126

#### Native field: expression

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity/expression; canonical SHA-256: 0b07ba71a9f4b737f78c23ddf9484b1e5c136fb6d7f457a83055a1e600ec4b13

N_\infty(\varepsilon;P_{-\sigma_g})=\sup_{0\le\sigma_g<\infty}Q^*(\varepsilon;P_{-\sigma_g},\sigma_g)

#### Native field: parent_quantity_ref

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity/parent_quantity_ref; canonical SHA-256: 4e018db1849ad72748353026374c93971258270fa3598be949890b481effe48b

BL_SPEC_joint_expected_cost__main__q1

#### Native field: outer_quantifier

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity/outer_quantifier; canonical SHA-256: 36e616b39a3ee826c6ce6a997abc699e72cfd621f3f9ae8efff655b7f6e359b1

supremum over all finite lower-noise budgets; other structural budgets and epsilon fixed

#### Native field: units

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity/units; canonical SHA-256: a1e41a285f731c5321ccc8929ef129dd96005bd000452df7352be45c87c6f6b8

oracle responses

#### Native field: ordinary_fixed_sigma_comparison

Native pointer: /joint_analysis/structural_findings_20261126/2/quantity/ordinary_fixed_sigma_comparison; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: predicate

Native pointer: /joint_analysis/structural_findings_20261126/2/predicate; canonical SHA-256: ed599ac3eea90f09a6f224c47360f67c7391aae8c65b6bd941b613b7156c0ff9

All native model and parameter constraints; $L_f=L_g=C_f=L>0$, $\kappa=L/\mu$, $\theta=\rho/\mu$, $\chi=1+\theta$; $R_0,\sigma_f,\sigma_g$ are finite and nonnegative. $\rho=0$, $\Delta>0$, $R_0>0$, $\kappa>1$, $\Lambda_\Phi\ge L\kappa^2$. Put $d_{\rm cond}=\sqrt{1-\kappa^{-2}}$, $d_g=(\sqrt5-1)/2$, $r=\min\{R_0,\sqrt{2\Delta/L}\}$ and $A=L\kappa r$. Require $d_{\rm cond}\ge d_g$ and $r\le1/(2-d_{\rm cond})$, both inclusive.

#### Native field: branches

Native pointer: /joint_analysis/structural_findings_20261126/2/branches; canonical SHA-256: 13df4862fe73f4ea8c356b5d714e89463efef21a6bddcfb839874ad38af7e5ce

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/0; canonical SHA-256: 52a8ec66c44b66106a7d765104e6fa5e2d4620a9c654da382553ef6e22ac5322

#### Native field: predicate

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/0/predicate; canonical SHA-256: 23621022b1016d25206ab225c883def9e9b7f8343c66ceace1cc041e4520c895

$\Delta\le LR_0^2/2$

#### Native field: finite_iff

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/0/finite_iff; canonical SHA-256: 69b1ad3f5ae5399b6bccc6d18c0aff02aa85a128c00eb4261c1878a621a54ccf

$\varepsilon\ge A$

#### Native field: equality

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/0/equality; canonical SHA-256: 64a9fc5daee6887625706e348ab44822929c6773e5df2d96589d8810b7e38a36

Included; zero calls suffice on the whole finite side.

#### Native item 2

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/1; canonical SHA-256: 050a9f60a4f50c5db1fc7f4739dd2a6ed78c2bf725c38510c319826b7cd63480

#### Native field: predicate

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/1/predicate; canonical SHA-256: 5551ebb8d68fbf10da1ff942b0fd66de2ae45f78fd1d8ae29f0ac956ad175925

$\Delta>LR_0^2/2$

#### Native field: finite_iff

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/1/finite_iff; canonical SHA-256: d6978172165965f6a911d9582297f18c717b1eb6aa7b1dc08e6fe7385fce748c

$\varepsilon>A$

#### Native field: equality

Native pointer: /joint_analysis/structural_findings_20261126/2/branches/1/equality; canonical SHA-256: 378afc3f7fbe3a8c48a0644d9e70692fd309ad093d91709c4e27a87075a08e4b

Excluded; N_infty diverges at epsilon=A as well as below A.

#### Native field: scope

Native pointer: /joint_analysis/structural_findings_20261126/2/scope; canonical SHA-256: ab081c4726cdbdf8c4800f2c1553530c95a8fad3cc6967943a67d0448fe1db80

Divergence is a supremum over finite noise budgets, not an infinite-complexity claim for a single finite sigma_g. Other initialization regions and matching finite-noise critical rates are not classified.

#### Native field: evidence_refs

Native pointer: /joint_analysis/structural_findings_20261126/2/evidence_refs; canonical SHA-256: 286c31cff248207d42b5db7c53fe1531600bbd02611eb222fb71cb410f3b1308

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/2/evidence_refs/0; canonical SHA-256: ffa4b3bcafd3c5e175fec72f2f0ec96a7e23c61eebb22cd7372388e4bf71d995

BL_SPEC_joint_expected_cost__main__e_endpoint_structure_20261126

#### Native field: proof_refs

Native pointer: /joint_analysis/structural_findings_20261126/2/proof_refs; canonical SHA-256: 2e76295aa6baea439b6a1b8627a17e5e65f00ac70f2a812da8876b8af8a8a1fa

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/2/proof_refs/0; canonical SHA-256: b857fc5495bc7f583e2c9bbaf2fa8d789661f059e8882fdcc96aa6851e6687d9

BL_SPEC_joint_expected_cost__main__proof_endpoint_structure_contract_20261126

#### Native field: source_refs

Native pointer: /joint_analysis/structural_findings_20261126/2/source_refs; canonical SHA-256: 4b8e127b920ac1a062e0c52a8c5bba4ff80e77dfd5ad5898b8e5668ea12f6dbb

#### Native item 1

Native pointer: /joint_analysis/structural_findings_20261126/2/source_refs/0; canonical SHA-256: c8799b019cf43ca6f5efbeb0c1fd7c40bee23264f7e1017ad16b8341f5d64f5f

COLOMBO_SFO_JOINT_20261126

## References

[1] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Closing the Accuracy Gap in Stochastic First-Order Bilevel Optimization. 2026. arXiv:2610.03633v2, 2026-10-19.

https://arxiv.org/pdf/2610.03633v2

[2] Colombo Team. Near-Optimal Joint Complexity of Stochastic Bilevel Optimization: Conditioning, Hessian Variation, and Separate Noise Budgets. User-supplied PDF, uploaded 2026-11-26; 81 pages; SHA-256 0582d5faf902c7f9e32311896699d6143f6513da195abb031e407c7d816c402a.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/SFO_JOINT_20261126/manuscript.pdf
