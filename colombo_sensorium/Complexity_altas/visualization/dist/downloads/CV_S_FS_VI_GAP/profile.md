# Finite-sum monotone variational inequalities: component values and expected weak gap.

**Setting ID.** `CV_S_FS_VI_GAP`

Variational inequalities

Solve $0\in F(z)+N_K(z)$.

**Status.** Bounds missing

**TASK tags.** solution concept: Weak gap; task family: Variational inequality

**MODEL tags.** smoothness: Mean square average; structure: Finite sum

**ORACLE tags.** feedback quality: Exact; index control: Algorithm selects; interface family: Component operator; operation: Component operator value; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Weak gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Worst-instance expected cost; measure: N component; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

Solve $0\in F(z)+N_K(z)$.

### Admissible model

The set $K\subset\mathbb{R}^d$ is known, nonempty, compact, and convex, with $\operatorname{diam}(K)\le D_K$. The operator $F=n^{-1}\sum_iF_i$ is monotone; components need not be monotone.

$$
\frac1n\sum_i\|F_i(z)-F_i(w)\|_2^2\le\beta^2\|z-w\|_2^2\quad(z,w\in K).
$$

### Oracle interface

Public inputs comprise the dimension $d$ and parameters $D_K$, $\beta$, $\varepsilon$, and $n$, together with the stated initial point and feasible-set information. Analytic descriptions of hidden functions, operators, and matrices are not supplied.

$$
(i,z)\longmapsto F_i(z)
$$

The algorithm selects an index and feasible point. A component may be queried at multiple points, with each evaluation charged. Values are exact; randomness comes from the algorithm, not the oracle.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return $\widehat{z}\in K$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\sup_{u\in K}\langle F(u),\widehat{z}-u\rangle
$$

Compactness makes this gap finite; expectation is applied to the complete gap.

### Resource accounting

One full vector response from a selected component costs one $N_{\rm component}$ call. A full average costs $n$ calls. Projection counts are retained separately.

Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\sup_{u\in K}\langle F(u),\widehat{z}-u\rangle\right]\le\varepsilon.
$$

Expectation is outside the complete error expression; internal maxima or suprema are not moved outside it.

**Budget convention.** worst_instance_expected_calls

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the feasible domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$\beta$: A mean-square average Lipschitz bound on component-operator differences. **Domain:** Positive real number.

$\frac1n\sum_{i=1}^n\|F_i(z)-F_i(w)\|_2^2\le\beta^2\|z-w\|_2^2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$n$: Fixed number of finite-sum components; the full function or operator is their 1/n average **Domain:** Positive integer.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$F_i,i$: Fixed component operators and algorithm-selected indices **Domain:** $i\in\{1,\ldots,n\},\ F_i:\text{query domain}\to\mathbb R^d$.

$F=\frac1n\sum_{i=1}^n F_i$

$K$: A known nonempty compact convex feasible set. **Domain:** A subset of Euclidean space.

$K\subset\mathbb R^d$

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $K\subset\mathbb R^d$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm component}$: Number of full operator-value queries to a specified component **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** output: domain: zhat in K; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: sup_{u in K}<F(u),zhat-u>; guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: E[sup_{u in K}<F(u),zhat-u>]<=epsilon.

**Resource contract.** budget: sup_instance E[N_oracle] (expected stopping-work budget); primary: N_component; unit: one declared oracle call; auxiliary: projection and known prox evaluations separately retained

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

### R1 - The bound’s native applicability window.

**Region.** Assume $n\ge2$ and $\varepsilon>0$. Both total component work and weak VI gap are controlled in expectation.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The source Theorem 4 and Corollary 6 use finite sums. Dividing the components by $n$ gives the average normalization used here. The initial squared distance to a point in the domain is controlled by $D_K^2$.

### B1 - See the cited theorem

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The variance-reduced extragradient/Mirror-Prox algorithm of Alacaoglu–Malitsky genuinely samples components and refreshes reference points randomly.

$$
O\!\left(n+\frac{\sqrt n\,\beta D_K^2}{\varepsilon}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v178/alacaoglu22a/alacaoglu22a.pdf)

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Source location.** [1](https://proceedings.mlr.press/v178/alacaoglu22a/alacaoglu22a.pdf) Assumption1; Algorithm1; Theorem4; Remark5; Corollary6

Expected total component calls O(n+sqrt(n)L D_K^2/epsilon) for expected Minty weak gap.

Source writes sum F, ours average: source components F_i/n, uniform estimator returns our F_i. Same index evaluated at two points, two charged calls. No individual component monotonicity. Full pass n. Native loopless count is expected work. Saddle-gap transfer uses source Eq12–14 and convex-concave inequality, not equivalence of output Minty gap and full saddle gap.

## References

[1] Ahmet Alacaoglu; Yura Malitsky. Stochastic Variance Reduction for Variational Inequality Methods. 2022. COLT2022 PMLR178.

https://proceedings.mlr.press/v178/alacaoglu22a/alacaoglu22a.pdf
