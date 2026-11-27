# Finite-sum convex-concave saddle-point problems: component gradients and expected global gap

**Setting ID.** `CV_S_FS_SADDLE_GAP`

Minimax optimization

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$.

**Status.** Bounds missing

**TASK tags.** task family: Minimax

**MODEL tags.** smoothness: Mean square average; structure: Finite sum

**ORACLE tags.** feedback quality: Exact; index control: Algorithm selects; interface family: Component gradient; operation: Component joint gradient; operation: Projection; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Point

**METRIC tags.** criterion: Saddle-point gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Worst-instance expected cost; measure: N component; measure: N projection; setup: Initialization included

## 1. Setting specification

### Task

Solve $\min_{x\in X}\max_{y\in Y}f(x,y)$.

### Admissible model

The set $K\subset\mathbb{R}^d$ is known, nonempty, compact, and convex, with $\operatorname{diam}(K)\le D_K$. The operator $F=n^{-1}\sum_iF_i$ is monotone; components need not be monotone.

$$
\frac1n\sum_i\|F_i(z)-F_i(w)\|_2^2\le\beta^2\|z-w\|_2^2\quad(z,w\in K).
$$

Assume $K=X\times Y$; the average $f=n^{-1}\sum_i f_i$ is convex-concave, and $F_i=(\nabla_xf_i,-\nabla_yf_i)$ holds. Individual $f_i$ need not be convex-concave.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $D_K$, $\beta$, $\varepsilon$, and $n$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(i,x,y)\longmapsto(\nabla_xf_i(x,y),\nabla_yf_i(x,y))
$$

The algorithm selects an index and feasible point. A component may be queried at multiple points, with each evaluation charged. Values are exact; randomness comes from the algorithm, not the oracle.

Exact Euclidean projection onto the known set is allowed. Its calls are recorded separately and excluded from the primary query count.

### Output

Return $\widehat{z}\in K$, equivalently $(\widehat{x},\widehat{y})\in X\times Y$.

The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

### Loss or accuracy criterion

$$
\max_{v\in Y}f(\widehat{x},v)-\min_{u\in X}f(u,\widehat{y})
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
\mathbb{E}\!\left[\max_{v\in Y}f(\widehat{x},v)-\min_{u\in X}f(u,\widehat{y})\right]\le\varepsilon.
$$

Expectation is outside the complete error expression; internal maxima or suprema are not moved outside it.

**Budget convention.** worst_instance_expected_calls

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the entire feasible product domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$\beta$: Mean-square average Lipschitz upper bound for component joint gradients **Domain:** Positive real number.

$\frac1n\sum_{i=1}^n\|\nabla f_i(z)-\nabla f_i(w)\|_2^2\le\beta^2\|z-w\|_2^2$

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$n$: Fixed number of finite-sum components; the full function or operator is their 1/n average **Domain:** Positive integer.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$f_i,i$: The fixed ith real-valued component and the algorithm-selected index. **Domain:** $i\in\{1,\ldots,n\},\quad f_i:\text{the declared product domain}\to\mathbb R$.

$f=\frac1n\sum_{i=1}^n f_i$

$K$: A known nonempty compact convex feasible set. **Domain:** A subset of Euclidean space.

$K=X\times Y\subset\mathbb R^{d_x+d_y}$

$X,Y$: Both primal and dual domains are known, nonempty, compact, and convex. Their product has diameter at most $D_K$. **Domain:** $X\subset\mathbb R^{d_x},\ Y\subset\mathbb R^{d_y}$.

$\widehat x,\widehat y$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** Feasible variable pairs in $\mathbb R^{d_x}\times\mathbb R^{d_y}$.

$\widehat z$: Joint output consisting of the two variable blocks **Domain:** $\mathbb R^{d_x+d_y}$.

$\widehat z=(\widehat x,\widehat y)$

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm component}$: Number of full joint-gradient queries to a specified component **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm projection}$: Projection count, uncharged in the primary query-cost projection **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$F$: Saddle operator induced by the payoff function **Domain:** $X\times Y\to\mathbb R^{d_x+d_y}$.

$F(x,y)=(\nabla_xf(x,y),-\nabla_yf(x,y))$

$F_i$: Saddle-point operator associated with the $i$th component gradient **Domain:** $X\times Y\to\mathbb R^{d_x+d_y}$.

$F_i=(\nabla_xf_i,-\nabla_yf_i)$

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** output: domain: zhat in K; postprocessing: arbitrary measurable transcript-based output unless algorithm restriction expressly states otherwise; metric: max_{y in Y} f(xhat,y)-min_{x in X}f(x,yhat); guarantee: One algorithm family chosen from public inputs satisfies for every legal instance and oracle law: E[max_{y in Y} f(xhat,y)-min_{x in X}f(x,yhat)]<=epsilon.

**Resource contract.** budget: sup_instance E[N_oracle] (expected stopping-work budget); primary: N_component; unit: one declared oracle call; auxiliary: projection and known prox evaluations separately retained

This is the native source metric/resource guarantee. Joint precision, block size, runtime and oracle components stay separate; do not infer a scalar optimal query complexity.

### R1 - The bound’s native applicability window.

**Region.** Assume $n\ge2$ and $\varepsilon>0$. Both total component work and the global saddle-gap guarantee are in expectation.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Use the original algorithm’s uniform certificate inequality together with the convex–concave saddle-point ergodic inequality, then take the supremum over comparison points to control the global gap. A small weak VI gap at a point alone does not imply a small saddle gap there.

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

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Ahmet Alacaoglu; Yura Malitsky. Stochastic Variance Reduction for Variational Inequality Methods. 2022. COLT2022 PMLR178.

https://proceedings.mlr.press/v178/alacaoglu22a/alacaoglu22a.pdf
