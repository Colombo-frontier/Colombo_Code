# Nonconvex–strongly concave optimization with a bundled full-Hessian interface.

**Setting ID.** `CV_S_HESSIAN_NCSC`

Minimax optimization

$$
\min_x\Phi(x),\quad\Phi(x)=\max_y f(x,y).
$$

**Status.** Logarithmic gap present

**TASK tags.** formulation: Minimize value function; task family: Minimax

**MODEL tags.** convexity: No convexity promise in block; convexity: Nonconvex strongly concave; convexity: Strong concavity in the declared block; initialization: Initial localization; smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** feedback quality: Exact; interface family: Full hessian bundle; operation: Payoff value gradient full hessian; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; confidence: Fixed numerical success / failure probability; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N bundle; precision: Bit precision not counted

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
z\in\mathbb{R}^{d_x+d_y}\longmapsto(f(z),\nabla f(z),\nabla^2f(z)).
$$

One exact call returns the complete joint Hessian, function value, and joint gradient.

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

A bundled value, gradient, and full-Hessian response costs one $N_{\mathrm{bundle}}$ call. Derivative costs are not split further.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$A_1$: The primal progress scale obtained using first-order smoothness alone. **Domain:** Positive real number.

$A_1=\Delta\beta/\varepsilon^2$

$A_2$: Scale of the leading second-order high-accuracy term **Domain:** Positive real number.

$A_2=\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2}=A_1\sqrt r$

$C_0$: Universal sufficient constant in the nontrivial accuracy regime; no numerical value is specified. **Domain:** Positive constant without an assigned numerical value.

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$I_0$: Initialization-call upper bound for the first regularized saddle problem; the relations below specify its verified polynomial scale and hidden logarithms **Domain:** Nonnegative resource upper-bound function.

$I_0\le\widetilde O(\mathcal S_{\rm init})$

$M_{\mathrm{main}}$: The scale determining whether the leading term dominates initialization. **Domain:** Positive real number.

$M_{\mathrm{main}}=A_1\Psi_\kappa(r)$

$\Psi_\kappa(r)$: Dimensionless multiplier in the three-branch full-Hessian rate. **Domain:** Positive real number.

$\Psi_\kappa(r)=\begin{cases}r^{1/2},&0<r\le1,\\ r^{2/7},&1\le r\le\kappa^{7/4},\\ \kappa^{1/2},&r\ge\kappa^{7/4}.\end{cases}$

$R_y$: Distance bound from the initial dual point to the unique best response at the same initial primal point **Domain:** A nonnegative real.

$\|y_0-y^\star(x_0)\|_2\le R_y$

$R_{y,0}^{\mathrm{prox}}$: A bound on dual distance from the initial point to the first regularized saddle point. **Domain:** Positive real number.

$R_{y,0}^{\mathrm{prox}}=R_y+\kappa\sqrt{\Delta/\beta}$

$\mathcal S_{\mathrm{init}}$: The explicit power-law scale of the initialization upper bound, excluding unexpanded logarithms. **Domain:** Positive real number.

$\mathcal S_{\mathrm{init}}=1+\min\{\sqrt\kappa,(\rho R_{y,0}^{\mathrm{prox}}/\mu_y)^{2/7}\}$

$\beta$: Euclidean Lipschitz upper bound for the population payoff's complete joint gradient. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le\beta\|z-w\|_2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the population smoothness upper bound, or mean-square average smoothness for finite sums, to the dual strong-concavity lower bound **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$r$: Dimensionless ratio separating the main complexity regimes **Domain:** Positive real number.

$r=\rho\kappa^{3/2}\varepsilon/\beta^2$

$\rho$: Lipschitz upper bound for the complete joint Hessian in spectral norm. **Domain:** Positive real number.

$\|\nabla^2f(z)-\nabla^2f(w)\|_{\rm op}\le\rho\|z-w\|_2$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

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

$$
\|T\|_{\rm op}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}\|T[u_1,\ldots,u_j]\|_2
$$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm bundle}$: Number of bundled function-value, complete joint-gradient, and complete-Hessian calls **Domain:** Nonnegative integer count; expected work is its expectation.

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
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm bundle}(\mathcal A,I,\omega)
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - High-accuracy Hessian regime

**Region.** Assume $0<r\le1$ and $A_1\ge C_0$, and require the leading term $A_1\Psi_\kappa(r)$ to dominate the one-time initialization bound $I_0+1$.

**Quantity.** Q1

**Resource.** Number of joint responses explicitly allowed by this profile

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2})
$$

**Upper bound.** B1

$$
\widetilde{O}(I_0+\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2})
$$

**Comparison argument.** This comparison certifies matching leading power-law terms only. Retain all polylogarithmic factors and initialization-dominated regions; full-parameter optimality is not asserted.

### R2 - Intermediate Hessian regime

**Region.** Require $1\le r\le\kappa^{7/4}$ and $A_1\ge C_0$, with the leading term $A_1\Psi_\kappa(r)$ at least as large as the one-time initialization bound $I_0+1$.

**Quantity.** Q1

**Resource.** Number of joint responses explicitly allowed by this profile

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega(\Delta\rho^{2/7}\kappa^{3/7}\beta^{3/7}\varepsilon^{-12/7})
$$

**Upper bound.** B3

$$
\widetilde{O}(I_0+\Delta\rho^{2/7}\kappa^{3/7}\beta^{3/7}\varepsilon^{-12/7})
$$

**Comparison argument.** This comparison certifies matching leading power-law terms only. Retain all polylogarithmic factors and initialization-dominated regions; full-parameter optimality is not asserted.

### R3 - The first-order-dominated region.

**Region.** Assume $r\ge\kappa^{7/4}$ and $A_1\ge C_0$, with leading term $A_1\Psi_\kappa(r)$ dominating the one-time initialization bound $I_0+1$.

**Quantity.** Q1

**Resource.** Number of joint responses explicitly allowed by this profile

**Status.** Logarithmic gap

**Lower bound.** B6

$$
\Omega(\Delta\beta\sqrt\kappa\,\varepsilon^{-2})
$$

**Upper bound.** B5

$$
\widetilde{O}(I_0+\Delta\beta\sqrt\kappa\,\varepsilon^{-2})
$$

**Comparison argument.** This comparison certifies matching leading power-law terms only. Retain all polylogarithmic factors and initialization-dominated regions; full-parameter optimality is not asserted.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - saddle-envelope cubic steps / reduced-dual accelerated tensor solves / first-order branch

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The full-Hessian upper bound in source Theorem 4.1 is implemented by deterministic Taylor or cubic models together with a first-order branch.

$$
\widetilde{O}(I_0+\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** Compare matching leading terms only when they dominate $I_0+1$. Retain actual initialization cost $I_0$.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N bundle.**

$$
\widetilde O(I_0+\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2})
$$

**linear algebra.** uncharged exact internal computation

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Several logarithmic factors from inner solves and line searches are not fully expanded.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) Section3; Theorem4.1

Bundled (f,gradient,full Hessian), L-gradient and rho-Hessian smooth NC-SC; three r-regimes.

All finite dimensions; arbitrary randomized output with fixed cap and success2/3. Initial gap Delta and dual distance R_y. r=rho*kappa^(3/2)*epsilon/L^2. Lower assumes A1=LDelta/epsilon^2>=C and already R_y=0. Near-matching phase rates require leading term >= I0+1; otherwise retain initialization. FOSP of Phi, not SOSP or HVP cost.

The upper bound includes the one-time initialization cost $I_0$. The lower bound holds even under exact dual initialization $R_y=0$. Each of the three comparisons closes only where its leading term dominates $I_0+1$.

### B2 - all-derivative lift or private-handle serial product

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega(\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The hard construction uses sufficiently large finite dimension and has initial dual distance $R_y=0$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\Delta\sqrt\rho\,\kappa^{3/4}\varepsilon^{-3/2})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) Section3; Theorem4.1

Bundled (f,gradient,full Hessian), L-gradient and rho-Hessian smooth NC-SC; three r-regimes.

All finite dimensions; arbitrary randomized output with fixed cap and success2/3. Initial gap Delta and dual distance R_y. r=rho*kappa^(3/2)*epsilon/L^2. Lower assumes A1=LDelta/epsilon^2>=C and already R_y=0. Near-matching phase rates require leading term >= I0+1; otherwise retain initialization. FOSP of Phi, not SOSP or HVP cost.

The upper bound includes the one-time initialization cost $I_0$. The lower bound holds even under exact dual initialization $R_y=0$. Each of the three comparisons closes only where its leading term dominates $I_0+1$.

### B3 - saddle-envelope cubic steps / reduced-dual accelerated tensor solves / first-order branch

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The full-Hessian upper bound in source Theorem 4.1 is implemented by deterministic Taylor or cubic models together with a first-order branch.

$$
\widetilde{O}(I_0+\Delta\rho^{2/7}\kappa^{3/7}\beta^{3/7}\varepsilon^{-12/7})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** Compare matching leading terms only when they dominate $I_0+1$. Retain actual initialization cost $I_0$.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N bundle.**

$$
\widetilde O(I_0+\Delta\rho^{2/7}\kappa^{3/7}\beta^{3/7}\varepsilon^{-12/7})
$$

**linear algebra.** uncharged exact internal computation

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Several logarithmic factors from inner solves and line searches are not fully expanded.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) Section3; Theorem4.1

Bundled (f,gradient,full Hessian), L-gradient and rho-Hessian smooth NC-SC; three r-regimes.

All finite dimensions; arbitrary randomized output with fixed cap and success2/3. Initial gap Delta and dual distance R_y. r=rho*kappa^(3/2)*epsilon/L^2. Lower assumes A1=LDelta/epsilon^2>=C and already R_y=0. Near-matching phase rates require leading term >= I0+1; otherwise retain initialization. FOSP of Phi, not SOSP or HVP cost.

The upper bound includes the one-time initialization cost $I_0$. The lower bound holds even under exact dual initialization $R_y=0$. Each of the three comparisons closes only where its leading term dominates $I_0+1$.

### B4 - all-derivative lift or private-handle serial product

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega(\Delta\rho^{2/7}\kappa^{3/7}\beta^{3/7}\varepsilon^{-12/7})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The hard construction uses sufficiently large finite dimension and has initial dual distance $R_y=0$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\Delta\rho^{2/7}\kappa^{3/7}\beta^{3/7}\varepsilon^{-12/7})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) Section3; Theorem4.1

Bundled (f,gradient,full Hessian), L-gradient and rho-Hessian smooth NC-SC; three r-regimes.

All finite dimensions; arbitrary randomized output with fixed cap and success2/3. Initial gap Delta and dual distance R_y. r=rho*kappa^(3/2)*epsilon/L^2. Lower assumes A1=LDelta/epsilon^2>=C and already R_y=0. Near-matching phase rates require leading term >= I0+1; otherwise retain initialization. FOSP of Phi, not SOSP or HVP cost.

The upper bound includes the one-time initialization cost $I_0$. The lower bound holds even under exact dual initialization $R_y=0$. Each of the three comparisons closes only where its leading term dominates $I_0+1$.

### B5 - saddle-envelope cubic steps / reduced-dual accelerated tensor solves / first-order branch

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

**Algorithm-scope qualification.** The full-Hessian upper bound in source Theorem 4.1 is implemented by deterministic Taylor or cubic models together with a first-order branch.

$$
\widetilde{O}(I_0+\Delta\beta\sqrt\kappa\,\varepsilon^{-2})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** Compare matching leading terms only when they dominate $I_0+1$. Retain actual initialization cost $I_0$.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N bundle.**

$$
\widetilde O(I_0+\Delta\beta\sqrt\kappa\,\varepsilon^{-2})
$$

**linear algebra.** uncharged exact internal computation

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Several logarithmic factors from inner solves and line searches are not fully expanded.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) Section3; Theorem4.1

Bundled (f,gradient,full Hessian), L-gradient and rho-Hessian smooth NC-SC; three r-regimes.

All finite dimensions; arbitrary randomized output with fixed cap and success2/3. Initial gap Delta and dual distance R_y. r=rho*kappa^(3/2)*epsilon/L^2. Lower assumes A1=LDelta/epsilon^2>=C and already R_y=0. Near-matching phase rates require leading term >= I0+1; otherwise retain initialization. FOSP of Phi, not SOSP or HVP cost.

The upper bound includes the one-time initialization cost $I_0$. The lower bound holds even under exact dual initialization $R_y=0$. Each of the three comparisons closes only where its leading term dominates $I_0+1$.

### B6 - all-derivative lift or private-handle serial product

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega(\Delta\beta\sqrt\kappa\,\varepsilon^{-2})
$$

**Sources.** [1](https://arxiv.org/pdf/2610.16771v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The hard construction uses sufficiently large finite dimension and has initial dual distance $R_y=0$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(\Delta\beta\sqrt\kappa\,\varepsilon^{-2})
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.16771v2) Section3; Theorem4.1

Bundled (f,gradient,full Hessian), L-gradient and rho-Hessian smooth NC-SC; three r-regimes.

All finite dimensions; arbitrary randomized output with fixed cap and success2/3. Initial gap Delta and dual distance R_y. r=rho*kappa^(3/2)*epsilon/L^2. Lower assumes A1=LDelta/epsilon^2>=C and already R_y=0. Near-matching phase rates require leading term >= I0+1; otherwise retain initialization. FOSP of Phi, not SOSP or HVP cost.

The upper bound includes the one-time initialization cost $I_0$. The lower bound holds even under exact dual initialization $R_y=0$. Each of the three comparisons closes only where its leading term dominates $I_0+1$.

## References

[1] Fangqing Zhang; Haihan Zhang; Wendao Wu; Chenheng Zhang; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Full-Hessian Oracle Complexity for Nonconvex--Strongly-Concave Minimax Optimization. 2026. arXiv:2610.16771v2, 2026-10-19.

https://arxiv.org/pdf/2610.16771v2
