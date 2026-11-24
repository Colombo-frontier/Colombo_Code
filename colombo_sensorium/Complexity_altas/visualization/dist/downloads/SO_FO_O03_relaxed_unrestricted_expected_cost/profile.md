# Decentralized relaxed-smooth optimization with unrestricted local work and expected sample cost

**Setting ID.** `SO_FO_O03_relaxed_unrestricted_expected_cost`

Single-objective optimization

Dimension-envelope expected sample complexity with heterogeneous local objectives, fresh stochastic gradients, and a known exact communication matrix.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Distributed gradient stationarity; task family: Single objective

**MODEL tags.** smoothness: Relaxed smoothness

**ORACLE tags.** feedback quality: Exact; feedback quality: Stochastic unbiased bounded variance; operation: Fixed network mixing; operation: Fresh local stochastic gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance

**RESOURCE tags.** measure: N communication; measure: N sample

## 1. Setting specification

### Task

Minimize $f(x)=m^{-1}\sum_{i=1}^m f_i(x)$ and have every node return an expected first-order stationary point of this average.

### Admissible model

For each finite dimension $d$, the continuously differentiable local objectives satisfy $f(x_0)-\inf f\le\Delta$. Only the average must be bounded below. For every node and $\|x-y\|\le1/L_1$, $\|\nabla f_i(x)-\nabla f_i(y)\|\le(L_0+L_1\|\nabla f_i(x)\|)\|x-y\|$. Uniform heterogeneity is $\|\nabla f_i(x)-\nabla f(x)\|\le H$ on the full space.

The known fixed communication matrix $W$ is symmetric, entrywise nonnegative, doubly stochastic, and positive semidefinite, with $0\preceq W\preceq I$ and $\ker(I-W)=\operatorname{span}\{\mathbf1\}$. The initial point and all numerical upper bounds are public. The matrix is held fixed in the minimax definition.

### Oracle interface

A local query selects a node $i$ and a point $x\in\mathbb R^d$ and returns $G_i(x;\xi)$ satisfying $\mathbb E[G_i\mid\mathcal F]=\nabla f_i(x)$ and $\mathbb E[\|G_i-\nabla f_i(x)\|^2\mid\mathcal F]\le\sigma^2$ for the complete pre-query history $\mathcal F$. Every call uses fresh randomness. No same-sample second-point reuse or smoothness of random responses is provided. Function values are not returned.

One communication call applies W to any finite stack of local vectors. Exact real local arithmetic is unrestricted and may use the known matrix, signed coefficients, and public randomness. Communication calls are counted separately but are not capped when the total sample count is optimized.

### Output

Each node returns a locally available point $\widehat x_i\in\mathbb R^d$. Outputs can differ and need not be queried points; no span restriction is imposed.

### Loss or accuracy criterion

$\max_{1\le i\le m}\mathbb E\|\nabla f(\widehat x_i)\|\le\varepsilon$ on every admissible fixed instance and oracle.

### Resource accounting

$S$ is the total number of local gradient responses over all nodes; every batch response counts. Stopping-time query counts are allowed and the cost is $\sup_I\mathbb E S$. Communication cost $C_{\mathrm{comm}}$ is separate and unconstrained in this projection. For fixed finite dimension let $S_d^*=\inf_A\sup_I\mathbb E S$ subject to the stationarity guarantee; the dimension-envelope quantity is $S^*=\sup_{d\ge1}S_d^*$.

### Algorithm views and success guarantees

Randomized adaptive protocols may select nodes and full-space query points, use stopping-time sample counts, unrestricted exact local computations, and the declared W communication interface. Each output must be locally available.

$$
\forall I,\mathcal O:\quad\max_i\mathbb E\|\nabla f(\widehat x_i)\|\le\varepsilon
$$

The expectation includes fresh response randomness and private/public algorithmic randomness. The instance and oracle are fixed before this expectation.

**Budget convention.** worst_case_expected_total_samples

## 2. Notation and parameters

$d$: Public finite ambient dimension in each instance **Domain:** $d\in\mathbb N_{\ge1}$.

$m$: Number of nodes **Domain:** $m\in\mathbb N_{\ge2}$.

$L_0$: Baseline gradient variation budget **Domain:** $L_0>0$.

$L_1$: Gradient-dependent relaxed smoothness budget **Domain:** $L_1>0$.

$\Delta$: Initial average objective gap **Domain:** $\Delta>0$.

$H$: Uniform local-gradient disagreement budget **Domain:** $H\ge0$.

$\sigma$: Conditional oracle standard-deviation upper bound **Domain:** $\sigma\ge0$.

$\varepsilon$: Expected gradient norm tolerance **Domain:** $\varepsilon>0$.

$x_0$: Common public initial point **Domain:** $x_0\in\mathbb R^d$.

$W$: Known communication matrix **Domain:** $W\in\mathbb R^{m\times m}$ with the stated spectral and stochasticity properties.

$r(W)$: Number of distinct eigenvalues of W **Domain:** $2\le r(W)\le m$.

$r(W)=\#\{\text{distinct eigenvalues of }W\}$

$L_H$: Aggregate smoothness scale **Domain:** $L_H>0$.

$L_H=L_0+L_1H$

$A_\varepsilon$: Fine-accuracy deterministic scale **Domain:** $A_\varepsilon>0$.

$A_\varepsilon=L_H\Delta/\varepsilon^2$

$B_\varepsilon$: Coarse-accuracy deterministic scale **Domain:** $B_\varepsilon>0$.

$B_\varepsilon=L_1\Delta/\varepsilon$

$P_\varepsilon$: Fresh-noise factor **Domain:** $P_\varepsilon\ge1$.

$P_\varepsilon=1+\sigma^2/\varepsilon^2$

$N_\varepsilon$: Effective component count **Domain:** $1\le N_\varepsilon\le m+1$.

$N_\varepsilon=1+\min\{m,H^2/\varepsilon^2\}$

$\Xi_\varepsilon$: Explicit lower-bound logarithmic loss **Domain:** $\Xi_\varepsilon\ge1$.

$\Xi_\varepsilon=[1+\log(1+L_1\varepsilon/L_0)]^4$

$\mathcal L_\varepsilon$: Upper-bound logarithmic factor **Domain:** $\mathcal L_\varepsilon>1$.

$\mathcal L_\varepsilon=1+\log(2+m+A_\varepsilon+B_\varepsilon+P_\varepsilon+H/\varepsilon+L_1\varepsilon/L_0)$

$\mathfrak F_\varepsilon$: Combined minimax sample scale **Domain:** $\mathfrak F_\varepsilon>0$.

$\mathfrak F_\varepsilon=(A_\varepsilon+B_\varepsilon)P_\varepsilon+A_\varepsilon\sqrt{N_\varepsilon}+N_\varepsilon$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
S^*=\sup_{d\ge1}\inf_A\sup_I\mathbb E S
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $\sup_I\mathbb E S$; description: Expected total local gradient responses; communication is unrestricted in this projection.

### R1 - All nontrivial accuracies: expected sample envelope

**Region.** $m\ge2$, $L_0,L_1,\Delta>0$, $H,\sigma\ge0$, and $0<\varepsilon^2\le c_0\Delta L_H$ for the universal sufficiently small constant in Theorem thm:main; W is any fixed admissible public matrix. The upper bound holds in every finite dimension. The lower bounds choose sufficiently large finite dimension in the constructions of Theorem thm:main, Section 5, and Appendices on the retiring and terminally flat chains. The compared quantity takes sup over finite d; no fixed-dimension minimax assertion is made. For $B_\varepsilon\le A_\varepsilon$, the lower bound strengthens to $\Omega(\mathfrak F_\varepsilon)$ without Xi_epsilon. For $B_\varepsilon>A_\varepsilon$, $N_\varepsilon<2$ and the rate reduces to the coarse fresh-noise scale. An accompanying communication upper bound does not establish a joint sample–communication minimax frontier.

**Quantity.** Q1

**Resource.** Expected total local gradient responses; communication is unrestricted in this projection.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\mathfrak F_\varepsilon/\Xi_\varepsilon)
$$

**Upper bound.** B1

$$
O(\mathcal L_\varepsilon^3\mathfrak F_\varepsilon)
$$

**Gap or comparison.** Upper/lower ratio is $O(\mathcal L_\varepsilon^3\Xi_\varepsilon)$; only the displayed logarithms remain.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** The upper bound holds in every finite dimension. The lower bounds choose sufficiently large finite dimension in the constructions of Theorem thm:main, Section 5, and Appendices on the retiring and terminally flat chains. The compared quantity takes sup over finite d; no fixed-dimension minimax assertion is made.

### B1 - Normalized descent with robust dyadic component-gradient differences and fresh-noise estimation.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\mathcal L_\varepsilon^3\mathfrak F_\varepsilon)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N15/manuscript.pdf)

**Conditions.** $m\ge2$, $L_0,L_1,\Delta>0$, $H,\sigma\ge0$, and $0<\varepsilon^2\le c_0\Delta L_H$ for the universal sufficiently small constant in Theorem thm:main; W is any fixed admissible public matrix.; The same sample-efficient algorithm has expected communication cost O((r(W)-1)(1+A_epsilon+B_epsilon)).; For $B_\varepsilon\le A_\varepsilon$, the lower bound strengthens to $\Omega(\mathfrak F_\varepsilon)$ without Xi_epsilon. For $B_\varepsilon>A_\varepsilon$, $N_\varepsilon<2$ and the rate reduces to the coarse fresh-noise scale.; An accompanying communication upper bound does not establish a joint sample–communication minimax frontier.

**Constants.** Universal constants.

**Logarithmic factors.** Only the explicitly defined L_epsilon and Xi_epsilon factors.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N15/manuscript.pdf) Theorem thm:main; equations eq:main-explicit and eq:main-communication

Normalized descent with robust dyadic component-gradient differences and fresh-noise estimation.. Randomized unrestricted local protocols.

The same sample-efficient algorithm has expected communication cost O((r(W)-1)(1+A_epsilon+B_epsilon)).

### B2 - Smooth embedding, hidden-sign discovery, retiring finite-sum chain, and terminally flat fresh-noise chain.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega(\mathfrak F_\varepsilon/\Xi_\varepsilon)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N15/manuscript.pdf)

**Conditions.** $m\ge2$, $L_0,L_1,\Delta>0$, $H,\sigma\ge0$, and $0<\varepsilon^2\le c_0\Delta L_H$ for the universal sufficiently small constant in Theorem thm:main; W is any fixed admissible public matrix.; For $B_\varepsilon\le A_\varepsilon$, the lower bound strengthens to $\Omega(\mathfrak F_\varepsilon)$ without Xi_epsilon. For $B_\varepsilon>A_\varepsilon$, $N_\varepsilon<2$ and the rate reduces to the coarse fresh-noise scale.; An accompanying communication upper bound does not establish a joint sample–communication minimax frontier.

**Constants.** Universal constants.

**Logarithmic factors.** Only the explicitly defined L_epsilon and Xi_epsilon factors.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N15/manuscript.pdf) Theorem thm:main; Section 5 and retiring/terminally flat chain appendices

Smooth embedding, hidden-sign discovery, retiring finite-sum chain, and terminally flat fresh-noise chain.. All randomized adaptive protocols with stopping-time sample counts and arbitrary outputs.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_N15. Sample Complexity and Communication Limits of Decentralized Optimization under Relaxed Smoothness. N15_decentralized_relaxed_smoothness.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N15/manuscript.pdf
