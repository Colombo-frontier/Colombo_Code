# Weakly convex stochastic programs with unknown constraints and separate constraint-value budgets

**Setting ID.** `SO_FO_N08_WEAK_CONSTRAINT_VALUES`

Single-objective optimization

Constraint levels have a separate information cost under a near-KKT criterion with signed expected feasibility and almost-sure complementarity.

**Status.** Bounds missing

**TASK tags.** solution concept: Constrained near kkt; task family: Single objective

**MODEL tags.** convexity: Weakly convex

**ORACLE tags.** derivative order: Order 0; feedback quality: Stochastic unbiased bounded second moment; feedback quality: Stochastic unbiased bounded variance; operation: Stochastic constraint subgradient vector; operation: Stochastic constraint value vector; operation: Stochastic objective subgradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** measure: N csub; measure: N cval; measure: N obj

## 1. Setting specification

### Task

Solve $\min_{x\in X} f(x)$ subject to the unknown expectation inequalities $g_i(x)=\mathbb E g_i(x,\xi)\le0$, $i=1,\ldots,m$, to the stated near-KKT criterion.

### Admissible model

The public set $X\subset\mathbb R^d$ is nonempty compact convex with diameter at most $D>0$ and a feasible point exists. The functions are finite on an open convex neighborhood of X. The objective is rho_f-weakly convex and each constraint is rho_g-weakly convex. Every ambient subgradient on X has norm at most l_f for f and l_g for each g_i.

Write $g_+(x)=\sum_i[g_i(x)]_+$. Public fixed constants $B>0$, $\bar\rho>\rho_g$ and $B_g>m\rho_gD^2$ satisfy: every $x\in X$ with $0<g_+(x)\le B_g$ admits $y\in\operatorname{relint}X$ such that $\max_i g_i(y)+(\bar\rho/2)\|y-x\|_2^2\le-B$. All structural, moment and qualification budgets are fixed as epsilon tends to zero.

### Oracle interface

Three separately charged interfaces are available at any x in X. An objective-subgradient sample zeta_f has conditional mean in the ambient partial f(x) and conditional second moment at most S_f squared. A vector constraint-subgradient sample (zeta_gi) has conditional means in partial g_i(x) and conditional sum of squared norms at most S_g squared. A vector constraint-value sample G has conditional mean g(x) and centered conditional variance at most sigma_v squared.

Fresh calls use independent randomness and the moment statements hold conditional on the history and selected query. A value observation may include an opaque sample handle for paid reuse at another point; every evaluation is charged. There is no free sampler revealing unknown constraint levels. Projection onto the known set and computation on known quantities are free.

### Output

Return $\widehat x\in X$. Validity is certified by existence of random latent witnesses $w\in X$ and $\lambda\in\mathbb R_+^m$; they need not be computed or returned and may live on an extension of the output probability space.

### Loss or accuracy criterion

Require simultaneously $\mathbb E\|\widehat x-w\|_2\le\varepsilon$, $\mathbb E g_i(w)\le\varepsilon$ for every i, $|\lambda_i g_i(w)|\le\varepsilon$ almost surely for every i, and $\mathbb E\operatorname{dist}(0,\partial f(w)+\sum_i\lambda_i\partial g_i(w)+N_X(w))\le\varepsilon$. Feasibility is signed expected feasibility, not the expectation of its positive part. Complementarity is pathwise.

### Resource accounting

The native resource is $(N_{\rm obj},N_{\rm csub},N_{\rm cval})$. For prescribed pathwise subgradient caps $B_f,B_s$, optimize $\inf_A\sup_{P\in\mathcal P}\mathbb E_PN_{\rm cval}$ over algorithms meeting the complete near-KKT criterion and satisfying $N_{\rm obj}\le B_f$, $N_{\rm csub}\le B_s$ on every execution. Algorithms terminate almost surely. This is a conditional value-query complexity, not a full Pareto frontier of all three counters.

### Algorithm views and success guarantees

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

A private random seed independent of the fixed instance is permitted.

$$
\forall P\in\mathcal P:\ \exists(w,\lambda)\text{ satisfying all four near-KKT inequalities}
$$

The witnesses are allowed to be random but complementarity holds almost surely. The whole criterion is required on every fixed admissible instance and legal oracle law.

**Budget convention.** mixed_pathwise_subgradient_caps_expected_value_calls

## 2. Notation and parameters

$d$: Public ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$m$: Number of constraints **Domain:** $m\in\mathbb N_{\ge1}$.

$D$: Known diameter upper bound **Domain:** $D>0$.

$\rho_f$: Objective weak-convexity bound **Domain:** $\rho_f\ge0$.

$\rho_g$: Constraint weak-convexity bound **Domain:** $\rho_g\ge0$.

$l_f$: Norm bound for every objective subgradient on X **Domain:** $l_f\ge0$.

$l_g$: Norm bound for every constraint subgradient on X **Domain:** $l_g\ge0$.

$S_f$: Objective sample second-moment scale **Domain:** $S_f\ge0$.

$S_g$: Constraint-vector sample second-moment scale **Domain:** $S_g\ge0$.

$\sigma_v$: Centered constraint-value noise scale **Domain:** $\sigma_v\ge0$.

$B$: Uniform qualification margin **Domain:** $B>0$.

$\bar\rho$: Uniform qualification curvature **Domain:** $\bar\rho>\rho_g$.

$B_g$: Qualification violation range **Domain:** $B_g>m\rho_gD^2$.

$\varepsilon$: Common tolerance in the four near-KKT requirements **Domain:** $\varepsilon>0$.

$B_f$: Pathwise objective-subgradient budget **Domain:** $B_f\in\mathbb N_0$.

$B_s$: Pathwise vector constraint-subgradient budget **Domain:** $B_s\in\mathbb N_0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathfrak C_{\rm val}(\varepsilon;B_f,B_s)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $\min\sup_P\mathbb EN_{\rm cval}\ \text{subject to }N_{\rm obj}\le B_f,\ N_{\rm csub}\le B_s$; description: The subgradient caps are pathwise, while the optimized value count is expected.

#### Q2 - minimax metric resource quantity

$$
\mathfrak C_{\rm val}(\varepsilon;C\varepsilon^{-4},C\varepsilon^{-4})
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $\min\sup_P\mathbb EN_{\rm cval}\ \text{under the two fixed subgradient caps}$; description: All upper resource coordinates are witnessed by one algorithm.

### R1 - General fixed-class value-query upper bound

**Region.** All structural budgets are fixed and satisfy MODEL; $0<\varepsilon\le\varepsilon_0(\mathcal P)$; $B_f,B_s\ge C_{\mathcal P}\varepsilon^{-4}$ for a sufficiently large fixed class-dependent constant. Every fixed finite d and m satisfying the model.

**Quantity.** Q1

**Resource.** The subgradient caps are pathwise, while the optimized value count is expected.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O(\varepsilon^{-2}\log(1/\varepsilon))
$$

**Gap or comparison.** No class-uniform matching claim is made for noiseless or one-dimensional subclasses.

### R2 - Matching value complexity on a fixed noisy two-dimensional class

**Region.** $d=2$, $m=1$, $X=[-1,1]^2$, $D=2\sqrt2$, $\rho_f=2$, $\rho_g=0$, $l_f=S_f=4$, $l_g=S_g=1$, $\sigma_v=1$, $B=1/2$, $\bar\rho=1/16$, $B_g=2$. The fixed class includes both source instances for every family parameter $0<\eta\le20^{-4}$. Require $0<\varepsilon\le\min\{20^{-4},\varepsilon_0(\mathcal P)\}$ and $B_f=B_s=C\varepsilon^{-4}$ up to integer rounding, for sufficiently large fixed C. The matching lower bound is already two-dimensional with one affine constraint. The class is the union over eta, fixed before target epsilon is chosen.

**Quantity.** Q2

**Resource.** All upper resource coordinates are witnessed by one algorithm.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(\varepsilon^{-2}\log(1/\varepsilon))
$$

**Upper bound.** B2

$$
O(\varepsilon^{-2}\log(1/\varepsilon))
$$

**Gap or comparison.** The explicit lower coefficient is 1/32768 in Theorem mainlower; upper/lower are constant-factor matching.

## 4. Bounds and supporting evidence

### B1 - Initial constraint-level estimation plus stochastic segment integration and stopped path-energy control

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\varepsilon^{-2}\log(1/\varepsilon))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf)

**Conditions.** All structural budgets are fixed and satisfy MODEL; $0<\varepsilon\le\varepsilon_0(\mathcal P)$; $B_f,B_s\ge C_{\mathcal P}\varepsilon^{-4}$ for a sufficiently large fixed class-dependent constant.; One algorithm jointly achieves N_obj<=C epsilon^-4, N_csub<=C(epsilon^-4+epsilon^-3 log(1/epsilon)), N_cval<=C epsilon^-2 log(1/epsilon). Constants depend only on the declared fixed class bounds.

**Dimension conditions.** Every fixed finite d and m satisfying the model.

**Constants.** Constants depend on the fixed geometric, regularity, moment and qualification budgets.

**Logarithmic factors.** The factor log(1/epsilon) is explicit.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf) Theorem upper; equation mainupper; Corollary matching; verified labels: thm:upper (line 214), eq:mainupper (line 219), cor:matching (line 237)

Initial constraint-level estimation plus stochastic segment integration and stopped path-energy control. Randomized algorithms with deterministic caps on all three counters.

One algorithm jointly achieves N_obj<=C epsilon^-4, N_csub<=C(epsilon^-4+epsilon^-3 log(1/epsilon)), N_cval<=C epsilon^-2 log(1/epsilon). Constants depend only on the declared fixed class bounds.

### B2 - Initial constraint-level estimation plus stochastic segment integration and stopped path-energy control

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\varepsilon^{-2}\log(1/\varepsilon))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf)

**Conditions.** $d=2$, $m=1$, $X=[-1,1]^2$, $D=2\sqrt2$, $\rho_f=2$, $\rho_g=0$, $l_f=S_f=4$, $l_g=S_g=1$, $\sigma_v=1$, $B=1/2$, $\bar\rho=1/16$, $B_g=2$. The fixed class includes both source instances for every family parameter $0<\eta\le20^{-4}$. Require $0<\varepsilon\le\min\{20^{-4},\varepsilon_0(\mathcal P)\}$ and $B_f=B_s=C\varepsilon^{-4}$ up to integer rounding, for sufficiently large fixed C.; One algorithm jointly achieves N_obj<=C epsilon^-4, N_csub<=C(epsilon^-4+epsilon^-3 log(1/epsilon)), N_cval<=C epsilon^-2 log(1/epsilon). Constants depend only on the declared fixed class bounds.

**Dimension conditions.** The matching lower bound is already two-dimensional with one affine constraint. The class is the union over eta, fixed before target epsilon is chosen.

**Constants.** Only the displayed fixed class bounds and the sufficiently large cap coefficient C enter constants.

**Logarithmic factors.** The factor log(1/epsilon) is required by the stated KKT convention.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf) Theorem upper; equation mainupper; Corollary matching; verified labels: thm:upper (line 214), eq:mainupper (line 219), cor:matching (line 237)

Initial constraint-level estimation plus stochastic segment integration and stopped path-energy control. Randomized algorithms with deterministic caps on all three counters.

One algorithm jointly achieves N_obj<=C epsilon^-4, N_csub<=C(epsilon^-4+epsilon^-3 log(1/epsilon)), N_cval<=C epsilon^-2 log(1/epsilon). Constants depend only on the declared fixed class bounds.

### B3 - Two affine unknown levels with identical subgradient information and Gaussian value noise

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\varepsilon^{-2}\log(1/\varepsilon))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf)

**Conditions.** $d=2$, $m=1$, $X=[-1,1]^2$, $D=2\sqrt2$, $\rho_f=2$, $\rho_g=0$, $l_f=S_f=4$, $l_g=S_g=1$, $\sigma_v=1$, $B=1/2$, $\bar\rho=1/16$, $B_g=2$. The fixed class includes both source instances for every family parameter $0<\eta\le20^{-4}$. Require $0<\varepsilon\le\min\{20^{-4},\varepsilon_0(\mathcal P)\}$ and $B_f=B_s=C\varepsilon^{-4}$ up to integer rounding, for sufficiently large fixed C.; The matched class must contain the fixed two-dimensional family in Section lower. The lower bound remains valid when value samples have paid reuse handles.

**Dimension conditions.** The matching lower bound is already two-dimensional with one affine constraint. The class is the union over eta, fixed before target epsilon is chosen.

**Constants.** Only the displayed fixed class bounds and the sufficiently large cap coefficient C enter constants.

**Logarithmic factors.** The factor log(1/epsilon) is required by the stated KKT convention.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf) Theorem mainlower; equation mainlower; Section lower and Corollary matching; verified labels: thm:mainlower (line 227), eq:mainlower (line 232), cor:matching (line 237), sec:lower (line 863)

Two affine unknown levels with identical subgradient information and Gaussian value noise. All randomized adaptive algorithms, including expected stopping times and unlimited exact subgradient information.

The matched class must contain the fixed two-dimensional family in Section lower. The lower bound remains valid when value samples have paid reuse handles.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_N10. Sharp Constraint-Value Complexity for Weakly Convex Stochastic Programs. 2026. N10_constraint_value_complexity.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N10/manuscript.pdf
