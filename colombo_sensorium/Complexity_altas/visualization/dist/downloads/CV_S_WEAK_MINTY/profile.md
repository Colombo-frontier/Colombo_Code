# Weak-Minty inclusion: state-dependent noise and resolvent displacement

**Setting ID.** `CV_S_WEAK_MINTY`

Variational inequalities

$$
0\in F(z)+\partial r(z).
$$

**Status.** Bounds missing

**TASK tags.** formulation: Weak minty inclusion; solution concept: Resolvent displacement; task family: Variational inequality

**MODEL tags.** convexity: Convex composite; convexity: Proper closed convex; initialization: Initial localization; monotonicity: Weak minty; smoothness: Operator lipschitz

**ORACLE tags.** feedback quality: E sample f z b z z0 sigma; feedback quality: Exact; interface family: State noise and prox; operation: Known prox; operation: Stochastic operator value; operator derivative order: Operator value (order 0); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Resolvent displacement

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** measure: N prox; measure: N sample; precision: Bit precision not counted

## 1. Setting specification

### Task

$$
0\in F(z)+\partial r(z).
$$

### Admissible model

The function $F:\mathbb{R}^d\to\mathbb{R}^d$ is $\beta$-Lipschitz, and $r$ is proper, lower semicontinuous, and convex. There exists $z^\star$ satisfying $0\in(F+\partial r)(z^\star)$ and $\|z_0-z^\star\|_2\le R$.

For every $(z,v)\in\operatorname{graph}(F+\partial r)$, $\langle v,z-z^\star\rangle\ge-\rho\|v\|_2^2$. The public fixed step size satisfies $0\le\rho<\eta<1/\beta$.

### Oracle interface

Public inputs include dimension $d$ and $B$, $R$, $\beta$, $\varepsilon$, $\eta$, $\rho$, $\sigma$, together with the stated initial point and feasible geometry. Hidden analytic representations are not revealed.

$$
z\longmapsto G_F(z;\xi),\qquad(\gamma,u)\longmapsto\operatorname{prox}_{\gamma r}(u).
$$

Fresh responses are conditionally unbiased and satisfy $\mathbb{E}[\|G_F(z;\xi)-F(z)\|_2^2\mid\mathcal{H},z]\le B^2\|z-z_0\|_2^2+\sigma^2$. Samples cannot be reused, and the proximal interface is exact.

The operations $\operatorname{prox}_{\gamma r}(u)=\arg\min_v\{r(v)+\|v-u\|_2^2/(2\gamma)\}$ and $\gamma>0$ are available. The resolvent of the entire unknown $F+\partial r$ is not supplied.

### Output

Return $\widehat{z}\in\mathbb{R}^d$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\|\widehat{z}-J_{\eta(F+\partial r)}(\widehat{z})\|_2.
$$

Define $J_{\eta(F+\partial r)}=(\operatorname{Id}+\eta(F+\partial r))^{-1}$; $\eta\beta<1$ ensures the map is single-valued on the whole space. The error is not divided by $\eta$ and is not tangent residual at the original output.

### Resource accounting

Fresh-sample operator calls $N_{\rm sample}$ and proximal calls are recorded separately. The primary comparison uses expected $N_{\rm sample}$.

Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\|\widehat{z}-J_{\eta(F+\partial r)}(\widehat{z})\|_2\right]\le\varepsilon.
$$

Expectation is outside the complete error expression; internal maxima or suprema are not moved outside it.

**Budget convention.** expected total fresh stochastic operator calls; randomized multilevel inner work

## 2. Notation and parameters

$B$: Slope governing growth of the state-dependent variance with distance from the initial point **Domain:** A nonnegative real.

$\mathbb E[\|G_t-F(z_t)\|_2^2\mid\mathcal H_t,z_t]\le B^2\|z_t-z_0\|_2^2+\sigma^2$

$R$: Euclidean distance bound from the public initial point to the same solution promised by the model; not the entire domain diameter **Domain:** Positive real number.

$\|z_0-z^\star\|_2\le R$

$\beta$: Euclidean Lipschitz upper bound for the population operator on the declared query domain **Domain:** Positive real number.

$\|F(z)-F(w)\|_2\le\beta\|z-w\|_2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Tolerance for the expected norm of the resolvent displacement, without division by the step size **Domain:** Positive real number.

$\eta$: The fixed public step size used to evaluate resolvent displacement. **Domain:** $\rho<\eta<1/\beta$.

$0\le\rho<\eta<1/\beta$

$\rho$: Coefficient of the weak Minty negative term relative to the same solution. **Domain:** $0\le\rho<1/\beta$.

$\langle v,z-z^\star\rangle\ge-\rho\|v\|_2^2\quad\bigl(v\in(F+\partial r)(z)\bigr)$

$\sigma$: Constant standard-deviation term in the state-dependent variance bound **Domain:** A nonnegative real.

$\mathbb E[\|G_t-F(z_t)\|_2^2\mid\mathcal H_t,z_t]\le B^2\|z_t-z_0\|_2^2+\sigma^2$

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

$N_{\rm prox}$: The number of exact proximal calls for convex r. **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs, a hidden admissible object fixed before interaction, and an oracle law satisfying the declared conditional means, variances, and independence protocol. **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$r$: A proper lower-semicontinuous convex regularizer. **Domain:** $r:\mathbb R^d\to\mathbb R\cup\{+\infty\}$.

$\partial r$: The set-valued subdifferential of convex r. **Domain:** $\mathbb R^d\rightrightarrows\mathbb R^d$.

$\partial r(z)=\{v:r(u)\ge r(z)+\langle v,u-z\rangle\ \forall u\}$

$J_{\eta(F+\partial r)}$: The complete resolvent used to evaluate error; not an available free interface. **Domain:** $\mathbb R^d\to\mathbb R^d$.

$J_{\eta(F+\partial r)}=(\operatorname{Id}+\eta(F+\partial r))^{-1}$

$\gamma,\operatorname{prox}_{\gamma r}$: A selectable positive proximal step and the unique point returned by that proximal map. **Domain:** $\gamma>0,\quad\mathbb R^d\to\mathbb R^d$.

$\operatorname{prox}_{\gamma r}(u)=\arg\min_v\{r(v)+\|v-u\|_2^2/(2\gamma)\}$

$\operatorname{graph}(F+\partial r)$: The composite operator graph. The weak Minty condition holds for every graph element. **Domain:** $\mathbb R^d\times\mathbb R^d$.

$\{(z,v):v\in F(z)+\partial r(z)\}$

$\operatorname{Id}$: The identity map on $\mathbb R^d$. **Domain:** Linear map.

$\operatorname{Id}(u)=u$

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \mathbb E_\omega[N_{\rm sample}(\mathcal A,I,\omega)]
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

Each call counts the complete response package specified by this interface. The algorithm class retains the stated randomization, adaptivity, and output conditions and must satisfy the full error guarantee for every fixed admissible instance. Expectations include the algorithm's seed and sampled observations; the stated random stopping rules are allowed.

### R1 - High-accuracy regime with fixed structural budgets

**Region.** $0\le\rho<\eta<1/\beta$. Hold every structural parameter fixed and let $\varepsilon\downarrow0$.

**Quantity.** Q1

**Resource.** Expected number of actual sample responses.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
\widetilde{O}(\varepsilon^{-4})
$$

**Comparison argument.** No matching lower has been independently verified in this native goal/oracle/noise specification.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $0\le\rho<\eta<1/\beta$. Exact $\operatorname{prox}_r$ is available, but the full resolvent appearing in the performance measure is not an additional oracle.; The source endpoint $\eta\le1/\beta$ is not certified: the inner strong-monotonicity modulus $1-\eta\beta$ must be strictly positive.; Without an explicit conversion, resolvent displacement at an output point cannot be interpreted as its tangent residual.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle mapping.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee mapping.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output mapping.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource mapping.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

### B1 - Krasnoselskii-Mann outer iteration with MLMC-FBF inner solve

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The corresponding FBF/KM methods use stochastic samples, randomized output indices, or random MLMC work.

$$
\widetilde{O}(\varepsilon^{-4})
$$

**Sources.** [1](https://raw.githubusercontent.com/mlresearch/v306/main/assets/alacaoglu26a/alacaoglu26a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**E N sample.**

$$
\widetilde O(\varepsilon^{-4})
$$

**E N prox.** one per constant-number FBF step; same-order expected inner work

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Accuracy logarithms remain unexpanded. Hidden constants may depend on all declared fixed structural parameters.

**Derivation.** Use only the strict-interior range $\rho<\eta<1/\beta$. Lipschitz continuity makes $I+\eta F$ strongly monotone with modulus at least $1-\eta\beta>0$, and adding $\eta\partial r$ preserves this property. The full resolvent is therefore single-valued and everywhere defined. Constants in Appendices C.1 and C.5 of the source are finite for each fixed strict-interior parameter choice, giving the upper bound through fresh operator samples and proximal access to $r$. The endpoint $\eta=1/\beta$ is not included automatically.

**Source location.** [1](https://raw.githubusercontent.com/mlresearch/v306/main/assets/alacaoglu26a/alacaoglu26a.pdf) theorem: Theorem3.1; LemmaC.1; RemarkC.2; TheoremC.5; section: Section3 / AppendixC; pdf pages: 6; 19; 21; 22; equations: (C.5)

Use the parameters $\alpha=1-\rho/\eta$ from the detailed theorem. The target is resolvent displacement at the selected outer point. Internal MLMC-FBF approximates the unknown resolvent using only native operator samples and the proximal map of $r$. No full unknown-operator resolvent is provided freely.

Theorems 3.1 and C.5 state $\eta\le1/L$, but the estimates in Lemma C.1, Remark C.2, and (C.5) require a positive strong-monotonicity modulus. The admitted range is therefore the strict interior $\rho<\eta<1/\beta$.

For the endpoint counterexample take $d=1$, $r=0$, and $F(x)=\beta\max\{0,\min\{x,2-x\}\}$. It is $\beta$-Lipschitz and satisfies the weak Minty condition with $\rho=0$ relative to $z^\star=0$. At $\eta=1/\beta$, every $x\in[1,2]$ satisfies $(\operatorname{Id}+\eta F)(x)=2$, so $J_{\eta F}(2)=[1,2]$. The endpoint resolvent is not single-valued.

## References

[1] Ahmet Alacaoglu; Jun-Hyun Kim. Solving Stochastic Variational Inequalities without the Bounded Variance Assumption. 2026. ICML PMLR306:1647--1679.

https://raw.githubusercontent.com/mlresearch/v306/main/assets/alacaoglu26a/alacaoglu26a.pdf
