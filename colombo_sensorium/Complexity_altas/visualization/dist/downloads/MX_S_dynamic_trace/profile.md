# Dynamic trace estimation with access to past matrices and pointwise-in-time correctness

**Setting ID.** `MX_S_dynamic_trace`

Matrix computation

For a fixed sequence $A_1,\ldots,A_T$, output estimates of $\tau_t=\operatorname{tr}(A_t)$ sequentially. The interface for $A_{t+1}$ becomes available only after output $\widehat\tau_t$.

**Status.** Bounds missing

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Explicit matrix class; stochastic model: Schatten variation budget

**ORACLE tags.** feedback quality: Exact; interface family: Past matrix matvec; operation: Past matrix matvec; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online scalar sequence

**METRIC tags.** criterion: Per time absolute trace

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: N

## 1. Setting specification

### Task

For a fixed sequence $A_1,\ldots,A_T$, output estimates of $\tau_t=\operatorname{tr}(A_t)$ sequentially. The interface for $A_{t+1}$ becomes available only after output $\widehat\tau_t$.

### Admissible model

The matrices $A_t\in\mathbb{R}^{d\times d}$ may be nonsymmetric and indefinite. The entire sequence is fixed before the algorithmic seed is drawn. Assume $1\le p\le2$, $\|A_t\|_{S_p}\le1$, $\|A_{t+1}-A_t\|_{S_p}\le\alpha$, and $0\le\alpha<1$.

### Oracle interface

Inputs $d,T,p,\alpha,\varepsilon,\delta$ are public. At time $t$ choose $j\le t$ and any $v\in\mathbb{R}^d$ to obtain exact $A_jv$. Future matrices are inaccessible, while past matrices remain accessible. A difference product requires subtraction of two charged native products.

### Output

Return a scalar $\widehat\tau_t$ at each time. Earlier outputs cannot be supplied retrospectively after the sequence ends. No additional certificate is required.

### Loss or accuracy criterion

The base loss indexed by $t$ is $|\widehat\tau_t-\operatorname{tr}(A_t)|$, with threshold $\varepsilon$. This is an absolute error; norm normalization is already part of the model assumptions.

### Resource accounting

Record calls at every time and matrix and sum them to obtain $N$; one $(A_{t+1}-A_t)v$ costs two calls. Compare the displayed algorithms under a fixed total budget. Expected cost is a separate quantity.

Reading public inputs and performing exact internal arithmetic, storage, and postprocessing are free in this query model. The budget is not a running-time or bit-complexity claim.

### Algorithm views and success guarantees

Randomized adaptive online algorithms are allowed. The algorithm must output the current estimate before the next interface becomes available. Storage and exact internal arithmetic are unrestricted, with no Krylov or linear-span condition.

Choose one algorithm, then require $\Pr(|\widehat\tau_t-\operatorname{tr}(A_t)|\le\varepsilon)\ge1-\delta$ for every admissible fixed sequence and each fixed time $t$. Probability is over private randomness; simultaneous correctness at every time is not required.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$T$: Total number of matrix interfaces revealed sequentially **Domain:** $T\in\mathbb N,\ T\ge1$.

$(A_1,\ldots,A_T)$

$p$: Schatten norm exponent shared by the input norm and variation budget. **Domain:** $1\le p\le2$.

$\|M\|_{S_p}=(\sum_i\sigma_i(M)^p)^{1/p}$

$\alpha$: Schatten-norm bound on differences between consecutive matrices **Domain:** $0\le\alpha<1$.

$\|A_{t+1}-A_t\|_{S_p}\le\alpha$

$\varepsilon$: The absolute trace-error tolerance at each time. **Domain:** $\varepsilon>0$.

$|\widehat\tau_t-\operatorname{tr}(A_t)|\le\varepsilon$

$\delta$: Allowed failure probability at each fixed time **Domain:** $0<\delta<1$.

$\forall t:\Pr(|\widehat\tau_t-\operatorname{tr}(A_t)|\le\varepsilon)\ge1-\delta$

$A_t$: The $t$th arriving fixed hidden matrix, which may be nonsymmetric and indefinite **Domain:** $\mathbb R^{d\times d},\ 1\le t\le T$.

$t,j$: Current time and index of the arrived matrix queried in this call. **Domain:** $1\le j\le t\le T$.

$\tau_t,\widehat\tau_t$: The current true trace and its estimate, which must be output before the next interface opens. **Domain:** $\mathbb R$.

$\tau_t=\operatorname{tr}(A_t)$

$\sigma_i(M)$: Singular values in nonincreasing order **Domain:** $1\le i\le\min\{\operatorname{rows}(M),\operatorname{cols}(M)\}$.

$\sigma_1(M)\ge\cdots\ge\sigma_{\min\{\operatorname{rows}(M),\operatorname{cols}(M)\}}(M)\ge0$

$\|M\|_{S_p}$: The Schatten norm shared by input and difference matrices. **Domain:** A nonnegative real.

$\|M\|_{S_p}=(\sum_i\sigma_i(M)^p)^{1/p}$

$L_\alpha$: The positive logarithmic factor in the dynamic upper bound. **Domain:** $0<\alpha\le1/2$.

$L_\alpha=\log(2/\alpha)$

$H_{\alpha,\delta}$: Confidence logarithm in the dynamic upper bound **Domain:** $0<\alpha\le1/2,\ 0<\delta<1/2$.

$H_{\alpha,\delta}=\log(2/(\alpha\delta))$

$N$: Total single-vector query budget across all times and all historical matrices **Domain:** $\mathbb N_0$.

$N^\star$: Minimum worst-case total query budget sufficient for the stated pointwise probability guarantee **Domain:** $\mathbb N_0\cup\{+\infty\}$.

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon,\delta;d,T,p,\alpha)
$$

**Scope.** Take the worst total budget over complete admissible sequences fixed before the seed is generated. The success requirement applies separately at each fixed time.

**Optimization direction.** minimize

### R1 - An upper bound for general Schatten variation budgets.

**Region.** Assume $1\le p\le2$, $0<\alpha\le1/2$, $\varepsilon>0$, and $0<\delta<1/2$. Every model matrix has Schatten norm at most one. Define $L_\alpha=\log(2/\alpha)$ and $H_{\alpha,\delta}=\log(2/(\alpha\delta))$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
N\le C\left[(T\alpha+1)L_\alpha^{1+p}\left(\frac{\sqrt{H_{\alpha,\delta}}}{\varepsilon}\right)^p+T H_{\alpha,\delta}\right]
$$

**Comparison argument.** The upper bound applies on the general variation-budget window. The broader lower-bound claim in Theorem 5.3 cites Lemma 5.1 and Appendix D.1, which establish only a single-segment scaling reduction with $\alpha=1/(T-1)$. A matching bound over the full window requires a multisegment direct-sum argument and is not certified by this row.

### R2 - Refined upper bound in terms of the nuclear-norm variation budget

**Region.** Assume $p=1$, $0<\alpha\le1/2$, $\varepsilon>0$, and $0<\delta<1/2$. Use the same truncated logarithm $L_\alpha,H_{\alpha,\delta}$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B2

$$
N\le C\left[\frac{(T\alpha+1)L_\alpha^2\sqrt{H_{\alpha,\delta}}}{\varepsilon}+T\min\left\{1,\frac{\alpha}{\varepsilon}\right\}H_{\alpha,\delta}\right]
$$

**Comparison argument.** Refined p=1 upper bound retaining min{1,alpha/epsilon}. Applicability of the full piecewise high-confidence lower bound still requires independent verification.

### R3 - Static endpoint with zero variation

**Region.** $\alpha=0$, $1\le p\le2$, $T\ge1$, $0<\delta<1/2$, $\varepsilon>0$.

**Quantity.** Q1

**Resource.** Number of right matrix-vector product queries

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
O\!\left(\min\{d,(\sqrt{\log(1/\delta)}/\varepsilon)^p+\log(1/\delta)\}\right)
$$

**Comparison argument.** A valid achievable branch at the static endpoint. A relative-norm lower bound is not transferred without checking a construction with the required fixed norm.

## 4. Bounds and supporting evidence

### B1 - Randomized segmented binary-tree trace estimation; all previous matrices remain accessible, with a pointwise-in-time error guarantee

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C\left[(T\alpha+1)L_\alpha^{1+p}\left(\frac{\sqrt{H_{\alpha,\delta}}}{\varepsilon}\right)^p+T H_{\alpha,\delta}\right]
$$

**Sources.** [1](https://arxiv.org/pdf/2209.15219v1)

**Oracle correspondence.** A tree node is computed only after its right endpoint arrives. Each difference product costs two original-matrix calls.

**Constants.** Fixed declared regularity and initialization budgets; no unlisted joint-parameter optimality is asserted.

**Source location.** [1](https://arxiv.org/pdf/2209.15219v1) pdf pages: 3; 7; 8; 9; 10; 18; 19; theorem or section: Dynamic model; Theorems 3.1 and B.2; theorem: Dynamic model; Theorems 3.1 and B.2

The DT dynamic model permits queries to all matrices that have arrived and guarantees absolute trace accuracy at each fixed time. Theorem 3.1 gives an upper bound for $p\in[1,2]$. At $p=1$, Theorem B.2 improves the second term to $T\min\{1,\alpha/\varepsilon\}H_{\alpha,\delta}$. A difference product costs two primitive calls.

### B2 - Randomized binary-tree estimation that skips sufficiently small increments, for nuclear norm p = 1.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C\left[\frac{(T\alpha+1)L_\alpha^2\sqrt{H_{\alpha,\delta}}}{\varepsilon}+T\min\left\{1,\frac{\alpha}{\varepsilon}\right\}H_{\alpha,\delta}\right]
$$

**Sources.** [1](https://arxiv.org/pdf/2209.15219v1)

**Resource conversion.** Count every primitive matrix product; a difference product costs two calls.

**Constants.** Fixed declared regularity and initialization budgets; no unlisted joint-parameter optimality is asserted.

**Source location.** [1](https://arxiv.org/pdf/2209.15219v1) pdf pages: 3; 7; 8; 9; 10; 18; 19; theorem or section: Dynamic model; Theorems 3.1 and B.2; theorem: Dynamic model; Theorems 3.1 and B.2

The DT dynamic model permits queries to all matrices that have arrived and guarantees absolute trace accuracy at each fixed time. Theorem 3.1 gives an upper bound for $p\in[1,2]$. At $p=1$, Theorem B.2 improves the second term to $T\min\{1,\alpha/\varepsilon\}H_{\alpha,\delta}$. A difference product costs two primitive calls.

### B3 - One static Schatten-normalized trace estimate reused over time, or standard-basis reconstruction.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
N\le C\min\left\{d,\left(\frac{\sqrt{\log(1/\delta)}}{\varepsilon}\right)^p+\log(1/\delta)\right\}
$$

**Sources.** [1](https://arxiv.org/pdf/2209.15219v1)

**Constants.** Positive universal constants, permitted to depend on any explicitly fixed auxiliary parameters.

**Derivation.** When α = 0, every A_t equals A_1 exactly.

**Source location.** [1](https://arxiv.org/pdf/2209.15219v1) theorem: Theorem B.1 plus α=0 identity

## References

[1] David P. Woodruff; Fred Zhang; Qiuyi (Richard) Zhang. Optimal Query Complexities for Dynamic Trace Estimation. 2022. arXiv:2209.15219v1; 2022-09-30.

https://arxiv.org/pdf/2209.15219v1
