# Distributed first-order optimization: relaxed smoothness with the DNS communication protocol

**Setting ID.** `SO_FO_O03_relaxed_DNS_pair`

Single-objective optimization

Find a point satisfying the stationarity criterion specified under the accuracy measure.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** formulation: First order stationarity; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Gradient dependent smoothness; stochastic model: Bounded gradient heterogeneity; stochastic model: Bounded variance; structure: Distributed; structure: Fixed network

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; interface family: Mixed; interface family: Stochastic local gradient gossip; operation: Stochastic local gradient gossip; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Node points; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: First order stationarity; criterion: Stationarity measure

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; precision: Bit precision not counted

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}F(x)$$

Node $i\in\{1,\ldots,m\}$ holds a local function $f_i$, and the aggregate objective is $F(x)=m^{-1}\sum_{i=1}^m f_i(x)$. Nodes exchange information only through the declared communication protocol.

### Admissible model

There are $m$ differentiable local functions $f_i$, with $F=m^{-1}\sum_{i=1}^m f_i$ and $F(x_0)-\inf F\le\Delta$. Whenever $\|x-y\|\le1/\beta_{\mathrm{rel}}$, $\|\nabla f_i(x)-\nabla f_i(y)\|\le(\beta_0+\beta_{\mathrm{rel}}\|\nabla f_i(x)\|)\|x-y\|$. Also, $\|\nabla f_i(x)-\nabla F(x)\|\le\zeta$. The radius is infinite when $\beta_{\mathrm{rel}}=0$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad m \ge 2,\quad \gamma_W > 0,\quad \gamma_W \le 1\\r_W \ge 0,\quad r_W \le (m-1),\quad d \ge 1,\quad \beta_0 > 0\\\beta_{\rm rel} \ge 0,\quad \zeta \ge 0,\quad \Delta > 0,\quad \sigma \ge 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ m,\ \varepsilon,\ x_0$.

Public upper bounds: $\beta_0,\beta_{\rm rel},\zeta,\Delta,\sigma$. Public lower bound on the spectral gap: $\gamma_W$.

The unknown objects are the local functions $f_1,\ldots,f_m$ held at the nodes.

Node $i$ may query only the following information about its local function at an admissible point $x_i$. The ambient space is $\mathbb R^d$.

$$g_i(x,\xi),\quad\mathbb{E}_tg_i=\nabla f_i(x),\quad\mathbb{E}_t\|g_i-\nabla f_i(x)\|^2\le\sigma^2$$

Samples within a same-point batch and noise at different nodes are conditionally independent. Common-sample reuse is not granted.

### Output

Return $\widehat{\boldsymbol x}=(\widehat x_1,\ldots,\widehat x_m)\in(\mathbb R^d)^m$, one ambient point per node.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

### Loss or accuracy criterion

$$\ell_i(I,\widehat{\boldsymbol x})=\|\nabla F(\widehat{x}_i)\|_2$$

### Resource accounting

Joint budget $(N_{\mathrm{samp,total}},N_{\mathrm{comm}})$ achieved by one algorithm. Every local sample in a batch is charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Permitted local linear operations on historical vectors are free. Communication is counted in the specified rounds and ambient vectors; no additional encoding, aggregate-gradient, or unlimited-bandwidth interface is granted.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

The public communication matrix $W$ is fixed, symmetric, positive semidefinite, and doubly stochastic, with spectral gap $\gamma_W=1-\lambda_2(W)$. The protocol permits multiplication by $W$ and local linear combinations of historical vectors, including the accelerated gossip and local memory used by DNSGD. The interface does not directly return the aggregate gradient.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}:\quad\max_i\mathbb{E}\|\nabla F(\widehat{x}_i)\|_2\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,x_i$: Global decision variable and node-local variables **Domain:** $x,x_i\in \mathbb{R}^d$.

$\widehat{\boldsymbol x}$: Product vector formed from the outputs of all nodes **Domain:** $\widehat{\boldsymbol x}\in (\mathbb{R}^d)^m$.

$$\widehat{\boldsymbol x}=(\widehat{x}_1,\ldots,\widehat{x}_m)$$

$f_i,F$: Local objectives and their average **Domain:** $i\in\{1,\ldots,m\}$.

$$F(x)=\frac1m\sum_{i=1}^m f_i(x)$$

$\nabla F$: Full gradient of the differentiable complete objective with respect to the decision variable

$\nabla f_i$: Full gradient of differentiable component $i$

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \mathbb{R}^d}F(x)$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\mathbb{E}_t$: Conditional expectation given the previous history and current query; the query is selected before the fresh observation is drawn

$\xi$: Random observation sample; the oracle's interaction protocol determines sample-reuse permissions

$g(x,z)$: Stochastic gradient map generated by sample $z$ at query point $x$

$W,W_t$: Fixed or time-varying communication matrix; spectral normalization and allowed multiplications are specified by the model and algorithm view

$\mathbf1$: All-ones vector of length $m$

$\lambda_2(W)$: Second-largest eigenvalue of the doubly stochastic communication matrix, with eigenvalues ordered nonincreasingly

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$m$: Number of network nodes; a positive integer. **Domain:** $m\ge2$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Public upper bound on the scale of the conditional centered noise moment. **Domain:** $\sigma\ge0$.

$\beta_0$: Baseline gradient scale in the relaxed-smoothness condition. **Domain:** $\beta_0>0$.

$\beta_{\rm rel}$: Coefficient multiplying the gradient norm in relaxed smoothness; its units are inverse length. **Domain:** $\beta_{\rm rel}\ge0$.

$\zeta$: Uniform bound on the difference between local and aggregate gradients. **Domain:** $\zeta\ge0$.

$\gamma_W$: Spectral gap $1-\lambda_2(W)$ of the known symmetric doubly stochastic matrix; distinct from the moment exponent. **Domain:** $0<\gamma_W\le1$.

$r_W$: Number of distinct eigenvalues of $W$ other than $1$. **Domain:** $0\le r_W\le m-1$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\beta_F$: Baseline relaxed-smoothness scale $\beta_0+\beta_{\mathrm{rel}}\zeta$ of the average objective.

$$\beta_F=\beta_0+\beta_{\rm rel}\,\zeta$$

$K_\varepsilon$: Optimization-iteration scale $1+\beta_F\Delta/\epsilon^2+\beta_{\mathrm{rel}}\Delta/\epsilon$; this is not the communication count.

$$K_\varepsilon=1+\frac{\beta_F\,\Delta}{{\varepsilon}^{2}}+\frac{\beta_{\rm rel}\,\Delta}{\varepsilon}$$

$N_{\mathrm{samp}},N_{\mathrm{comm}}$: Total samples across all nodes and communication rounds **Domain:** All are nonnegative integers.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Joint resource vector

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Stochastic nonconvex optimization under relaxed smoothness

**Region.** $\beta_0>0,\ \beta_{\rm rel},\zeta,\sigma\ge0,\ 0<\gamma_W\le1,\ 0\le r_W\le m-1$

**Quantity.** Q1

**Resource.** Joint resource vector

**Status.** Joint budget unresolved

**Achievable budgets.** B1

**Necessary constraints.** No admitted claim in this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$\beta_0>0,\ \beta_{\rm rel},\zeta,\sigma\ge0,\ 0<\gamma_W\le1,\ 0\le r_W\le m-1$$

**Dimension conditions.** $\beta_0>0,\ \beta_{\rm rel},\zeta,\sigma\ge0,\ 0<\gamma_W\le1,\ 0\le r_W\le m-1$

**Oracle mapping.** Applicable interfaces: local stochastic gradients and communication. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee mapping.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Two-resource budget achieved by DNSGD

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Randomized witness

$$
(CK_\varepsilon[m+\sigma^2/\varepsilon^2+\beta_{\rm rel}^2\sigma^2/\beta_F^2],\ \widetilde{O}(\gamma_W^{-1/2}K_\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2509.08726)

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2509.08726) theorem: Assumptions1–5, Proposition1; Thm1/Cor1, PDF pp.2–3; AppendixD; arXivv3

## 5. Local arguments

### A1 - Normalization and finite-step spectral consensus

**Scope.** Fresh local stochastic gradients and the explicitly declared matrix-multiplication protocol.

**Algorithm scope.** Randomized normalized-SGD output; same-algorithm joint attainable resource vectors.

Relaxed smoothness and the heterogeneity bound make the average objective $(\beta_F,\beta_{\rm rel})$-smooth, where $\beta_F=\beta_0+\beta_{\rm rel}\zeta$. For the cited DNSGD theorem, divide the objective by $\beta_F$, substituting $\Delta/\beta_F,\epsilon/\beta_F,\sigma/\beta_F$. Let
$K_\epsilon=1+\beta_F\Delta/\epsilon^2+\beta_{\rm rel}\Delta/\epsilon$.
The integer batch
$$
b=C\left\lceil1+{\sigma^2\over m\epsilon^2}
+{\beta_{\rm rel}^2\sigma^2\over m\beta_F^2}\right\rceil
$$
and the theorem's initialization give the recorded total-sample budget by multiplying $mb$ by its iteration count. Its gossip count retains $\gamma_W^{-1/2}$ and the stated logarithms. The minimum batch preserves the noiseless baseline. Random iteration selection is private randomization.

In the stronger protocol with known full spectrum, exact arithmetic, and signed historical linear combinations, let $r_W$ count the distinct eigenvalues of $W$ other than one. Then
$$
P_W(t)=\prod_{\lambda\ne1}(t-\lambda)/(1-\lambda),\qquad
P_W(W)=\mathbf1\mathbf1^\top/m.
$$
Spectral decomposition proves the identity. Degree $r_W\le m-1$ means $r_W$ matrix multiplications compute exact averaging.

At a common point, each node takes
$b=\lceil C(1+\sigma^2/(m\epsilon^2))\rceil$ fresh samples. Their exact average $\widehat g$ has expected error $O(\epsilon)$. Every node makes the normalized step with
$\eta=c\min\{\epsilon/\beta_F,1/\beta_{\rm rel}\}$, taking zero step if the estimate vanishes. Relaxed descent and
$\langle\nabla F,\widehat g/\|\widehat g\|\rangle
\ge\|\nabla F\|-2\|\widehat g-\nabla F\|$
give expected decrease at least $c\eta\|\nabla F\|-C\eta\epsilon$.
Sum for $CK_\epsilon$ steps and return a uniform random iterate. All nodes attain the stated expected norm guarantee, with joint budget
$$
(CK_\epsilon[m+\sigma^2/\epsilon^2],\;Cr_WK_\epsilon).
$$
Both coordinates belong to one algorithm. Known spectrum and signed coefficients are substantive permissions; for fixed $m$, this construction precludes an unconditional communication lower bound diverging as $\gamma_W^{-1/2}$ in that protocol.

**Limits of the argument.** Finite-step consensus additionally requires known exact spectrum, signed coefficients, and exact arithmetic. It is not available under every communication protocol.

**Sources.** [1](https://arxiv.org/pdf/2509.08726)

## References

[1] Luo Luo, Xue Cui, Tingkai Jia and Cheng Chen. Decentralized Stochastic Nonconvex Optimization under the (L0,L1)-Smoothness. 2026; KDD 2026; arXiv:2509.08726v3, 1 June 2026, 15 pp.; Assumptions 1–5 and Proposition 1 p.2; Theorem 1 and Corollary 1 p.3; Appendix D; DOI 10.1145/3770855.3817843..

https://arxiv.org/pdf/2509.08726
