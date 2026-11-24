# Weak Minty root finding with fresh operator samples.

**Setting ID.** `CV_S_WEAK_MINTY_ROOT_FRESH`

Variational inequalities

$$
F(z^\star)=0,\qquad z^\star\in\mathbb{R}^d.
$$

**Status.** Bounds missing

**TASK tags.** solution concept: Root residual; task family: Variational inequality

**MODEL tags.** initialization: Initial distance; monotonicity: Weak minty; smoothness: Lipschitz

**ORACLE tags.** feedback quality: Stochastic unbiased bounded variance; interface family: Fresh operator; operation: Stochastic operator value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Root residual

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Worst-instance expected cost; measure: N operator sample; setup: Initialization included

## 1. Setting specification

### Task

$$
F(z^\star)=0,\qquad z^\star\in\mathbb{R}^d.
$$

### Admissible model

The function or operator $F:\mathbb{R}^d\to\mathbb{R}^d$ is $\beta$-Lipschitz and has a zero $z^\star$ satisfying $\|z_0-z^\star\|_2\le R_0$.

$$
\langle F(z),z-z^\star\rangle\ge-\rho\|F(z)\|_2^2\quad(\forall z),\qquad0\le\rho\beta<\frac12.
$$

Global monotonicity, a scalar potential, and sample mean-square smoothness are not assumed.

### Oracle interface

Public inputs include dimension $d$ and $R_0$, $\beta$, $\varepsilon$, $\rho$, and $\sigma$, together with the stated initial-point and feasible-domain information. Analytic representations of hidden functions, operators, or matrices are not revealed.

$$
z\in\mathbb{R}^d\longmapsto G_F(z;\xi).
$$

Let $\mathcal H_t$ denote the full history before query t. Conditional on $\mathcal H_t,z_t$, the response $G_t\in\mathbb R^d$ satisfies $\mathbb E[G_t\mid\mathcal H_t,z_t]=F(z_t)$ and $\mathbb E[\|G_t-F(z_t)\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$. Each call uses an independent fresh sample.

No reusable sample identifier or cross-point sample reuse is available. No mean-square smoothness of sample gradients or operators is additionally assumed. Blocks within a full vector may be correlated.

### Output

Return $\widehat{z}\in\mathbb{R}^d$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|F(\widehat{z})\|_2
$$

### Resource accounting

Each full-vector sample costs one $N_{\mathrm{sample}}$ call.

Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\|F(\widehat{z})\|_2\right]\le\varepsilon.
$$

Expectation is outside the complete error expression; internal maxima or suprema are not moved outside it.

**Budget convention.** worst_instance_expected_calls

## 2. Notation and parameters

$R_0$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** A nonnegative real.

$\|z_0-z^\star\|_2\le R_0$

$\beta$: Euclidean Lipschitz upper bound for the population operator on the declared query domain **Domain:** Positive real number.

$\|F(z)-F(w)\|_2\le\beta\|z-w\|_2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Tolerance for the true root residual or Euclidean norm of an admissible graph element. **Domain:** Positive real number.

$\rho$: Coefficient of the weak Minty negative term relative to the same zero. **Domain:** $0\le\rho\beta<1/2$.

$\langle F(z),z-z^\star\rangle\ge-\rho\|F(z)\|_2^2$

$\sigma$: Standard-deviation upper bound for noise in the full stochastic response, controlling the joint squared norm rather than summing independent block budgets. **Domain:** A nonnegative real.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

$\theta$: Dimensionless weak Minty parameter **Domain:** $0\le\theta<1/2$.

$\theta=\rho\beta$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $\mathbb R^d$.

$G_F(z;\xi),G_t$: Random vector sample of population operator $F$ and its response at time $t$. **Domain:** $\mathbb R^d$.

$\xi,\mathcal H_t,z_t$: Current fresh-sample seed, complete pre-query history, and query point. **Domain:** The seed space, history-generated $\sigma$-algebra, and declared query domain.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm sample}$: Number of fresh-sample complete-operator-vector calls **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$N_\varepsilon$: Geometric stage scale **Domain:** $N_\varepsilon>0$.

$N_\varepsilon=(\beta R_0/\varepsilon)^2$

$A_\varepsilon$: Noise inflation factor **Domain:** $A_\varepsilon\ge1$.

$A_\varepsilon=1+\sigma^2/\varepsilon^2$

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** output: domain: zhat in R^d; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: ||F(zhat)||; guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: E[||F(zhat)||]<=epsilon.

**Resource contract.** budget: sup_instance E[N_oracle] (expected stopping-work budget); primary: N_operator_sample; unit: one declared oracle call; auxiliary: projection and known prox evaluations separately retained

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

#### Q2 - minimax metric resource quantity

$$
C^\star_\infty=\sup_{d\ge1}\inf_A\sup_{I,\mathcal O}\mathbb E\tau_A
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $\sup_{I,\mathcal O}\mathbb E\tau$; description: Worst-instance expected work under the linked expected-residual guarantee.

### R1 - The bound’s native applicability window.

**Region.** Hold $\beta,R_0,\rho,\sigma$ fixed and assume $0\le\rho\beta<1/2$ and $\varepsilon>0$. The internal step size lies strictly between $\rho$ and $1/\beta$, bounded away from both endpoints. This record concerns accuracy dependence with structural parameters fixed.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

### R2 - Dimension-uniform expected-work weak-Minty complexity

**Region.** $R_0,\beta>0$, $\sigma\ge0$, $0\le\rho\beta\le1/4$, $0<\varepsilon\le c_0\beta R_0$. One explicit source choice is $c_0=1/(256\sqrt{514})$. The upper bound holds in every finite dimension. Theorem matching supplies a lower-bound dimension $d_\varepsilon\le C_2N_\varepsilon\log(2+N_\varepsilon A_\varepsilon)$; the primary quantity is the supremum over finite dimensions. The hard mean has a unique root and satisfies the stronger Minty condition rho=0.

**Quantity.** Q2

**Resource.** Worst-instance expected work under the linked expected-residual guarantee.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega(N_\varepsilon A_\varepsilon)
$$

**Upper bound.** B2

$$
O(N_\varepsilon A_\varepsilon)
$$

**Gap or comparison.** Universal constant-factor matching.

## 4. Bounds and supporting evidence

### B1 - See the cited theorem

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The corresponding FBF/KM methods use stochastic samples, randomized output indices, or random MLMC work.

$$
\widetilde{O}(\varepsilon^{-4})
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v306/main/assets/alacaoglu26a/alacaoglu26a.pdf)

**Conditions.** Set the convex term and the state-dependent variance slope to zero in the composite weak Minty theorem. Tighten the internal target using the source residual conversion. Expected work remains an expected-resource quantity. This record certifies accuracy dependence only at fixed structural parameters.

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v306/main/assets/alacaoglu26a/alacaoglu26a.pdf) Assumptions1,3; Theorem3.1; Lemma3.5; Remark3.2

Expected-work resolvent displacement upper, with root specialization and same-point Lipschitz conversion.

For r=0 and B=0, oracle is fixed-distribution fresh field with uniform variance. Choose rho<eta<1/L. Source notation has -rho||F||^2. For u=J_etaF(z), ||F(z)||<= (L+eta^(-1))||z-u||. Therefore source expected displacement at scaled tolerance yields same-point expected root norm. No free computation of u required by output mapping; all MLMC samples counted. No full joint-parameter optimal lower inferred.

### B2 - Minibatch damped extragradient

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(N_\varepsilon A_\varepsilon)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N03/manuscript.pdf)

**Conditions.** $R_0,\beta>0$, $\sigma\ge0$, $0\le\rho\beta\le1/4$, $0<\varepsilon\le c_0\beta R_0$. One explicit source choice is $c_0=1/(256\sqrt{514})$.; The source upper proof allows the broader conditional-noise class, hence applies to independent fresh responses.

**Dimension conditions.** The upper bound holds in every finite dimension. Theorem matching supplies a lower-bound dimension $d_\varepsilon\le C_2N_\varepsilon\log(2+N_\varepsilon A_\varepsilon)$; the primary quantity is the supremum over finite dimensions. The hard mean has a unique root and satisfies the stronger Minty condition rho=0.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N03/manuscript.pdf) Theorem matching; Theorem upper; equation matching; verified labels: thm:matching (line 216), eq:matching (line 220), sec:upper (line 422), thm:upper (line 514)

Minibatch damped extragradient. Adaptive algorithms with a deterministic upper sample cap.

The source upper proof allows the broader conditional-noise class, hence applies to independent fresh responses.

### B3 - Gated hidden codewords and Bernoulli masking with expected-work truncation

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(N_\varepsilon A_\varepsilon)
$$

**Sources.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N03/manuscript.pdf)

**Conditions.** $R_0,\beta>0$, $\sigma\ge0$, $0\le\rho\beta\le1/4$, $0<\varepsilon\le c_0\beta R_0$. One explicit source choice is $c_0=1/(256\sqrt{514})$.; The hard oracle uses independent Bernoulli randomness and lies inside the existing fresh model.

**Dimension conditions.** The upper bound holds in every finite dimension. Theorem matching supplies a lower-bound dimension $d_\varepsilon\le C_2N_\varepsilon\log(2+N_\varepsilon A_\varepsilon)$; the primary quantity is the supremum over finite dimensions. The hard mean has a unique root and satisfies the stronger Minty condition rho=0.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [2](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N03/manuscript.pdf) Theorem matching; Sections scaling and expected-work lower bounds; verified labels: thm:matching (line 216), eq:matching (line 220)

Gated hidden codewords and Bernoulli masking with expected-work truncation. All randomized adaptive algorithms, arbitrary queries and outputs, and almost surely finite stopping.

The hard oracle uses independent Bernoulli randomness and lies inside the existing fresh model.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Ahmet Alacaoglu; Jun-Hyun Kim. Solving Stochastic Variational Inequalities without the Bounded Variance Assumption. 2026. ICML PMLR306:1647--1679.

https://raw.githubusercontent.com/mlresearch/v306/main/assets/alacaoglu26a/alacaoglu26a.pdf

[2] Colombo_N03. Optimal Sample Complexity of Stochastic Weak-Minty Root Finding. N03_weak_minty_root_finding.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N03/manuscript.pdf
