# Distributed first-order optimization: time-varying graph and Hilbert space

**Setting ID.** `SO_FO_O03_varying_hilbert`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Joint budget unresolved

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz gradient; structure: Distributed; structure: Infinite dimensional source model; structure: Local objectives; structure: Time varying network

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Local gradient gossip; interface family: Mixed; operation: Local gradient gossip; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Explicit restriction; randomization: Deterministic

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Node points; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Distance

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in \ell_2}F(x)$$

Node $i\in\{1,\ldots,m\}$ holds a local function $f_i$, and the aggregate objective is $F(x)=m^{-1}\sum_{i=1}^m f_i(x)$. Nodes exchange information only through the declared communication protocol.

### Admissible model

The $m$ unknown local functions $f_i$ are globally $\beta$-smooth and $\mu$-strongly convex, and $F=m^{-1}\sum_{i=1}^m f_i$. The time-varying matrices $W_t$ satisfy the consensus nullspace/range conditions and $\|(I-W_t)z\|^2\le(1-1/\chi)\|z\|^2$ for every disagreement vector $z$. Here $\chi$ is not the spectral ratio used for a fixed $W$. The initial primal-dual Lyapunov scale is at most $E_0$. The ambient space is the separable Hilbert space $\ell_2$, as in the source long-chain model; no finite dimension $d$ is fixed.

The ambient space is the real Hilbert space $\ell_2$. All distances, inner products, gradients, and local regularity assumptions use its Hilbert norm and inner product.

Each local function is strongly convex and smooth in the ambient Hilbert norm; the complete objective is $F$. The algorithm view states the network protocol's span restriction, and the resource definition states the communication unit.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad m \ge 2,\quad \mu > 0,\quad \kappa \ge C\\\chi \ge 3,\quad \varepsilon \le c\,E_0,\quad \beta > 0,\quad \chi > 0\\E_0 > 0,\quad \mu \le \beta\end{gathered}$$

### Oracle interface

Public numerical inputs: $m,\ \varepsilon$.

Public upper bounds: $\beta,\ \chi,\ E_0$.

Public lower bounds: $\mu$.

The unknown objects are the local functions $f_1,\ldots,f_m$ held at the nodes.

Node $i$ may query only the following information about its local function at an admissible point $x_i$. The ambient space is $\ell_2$.

$$\nabla f_i(x_i)\text{ at node }i;\quad\text{allowed neighbor messages}$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

Only primal gradients are available; no gradient oracle for a Fenchel conjugate is granted.

### Output

Return $\widehat{\boldsymbol x}=(\widehat x_1,\ldots,\widehat x_m)\in(\ell_2)^m$, one ambient point per node.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

The output must also satisfy the support, atomic-hull, or historical-span restriction of its algorithm view. An unqueried output remains subject to these restrictions.

### Loss or accuracy criterion

$$\|\boldsymbol x-\boldsymbol x^\star\|_2^2$$

$\boldsymbol{x}^\star=(x^\star,\ldots,x^\star)$, where $x^\star$ is the unique minimizer of $F$. The squared product-space distance is the sum of the squared distances at all nodes, without division by the number of nodes $m$.

### Resource accounting

Joint budget $(N_\nabla,N_{\mathrm{comm}})$ counting parallel local-gradient rounds per node and communication rounds. Each round transmits a constant number of ambient vectors along the graph.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Permitted local linear operations on historical vectors are free. Communication is counted in the specified rounds and ambient vectors; no additional encoding, aggregate-gradient, or unlimited-bandwidth interface is granted.

### Algorithm views and success guarantees

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

Local queries, outputs, and memory must remain in the span of the permitted historical vectors. Arbitrary nonlinear encoding protocols are excluded.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

## 2. Notation and parameters

$x,x_i$: Global decision variable and node-local variables **Domain:** $x,x_i\in \ell_2$.

$\widehat{\boldsymbol x}$: Product vector formed from the outputs of all nodes **Domain:** $\widehat{\boldsymbol x}\in (\ell_2)^m$.

$$\widehat{\boldsymbol x}=(\widehat{x}_1,\ldots,\widehat{x}_m)$$

$f_i,F$: Local objectives and their average **Domain:** $i\in\{1,\ldots,m\}$.

$$F(x)=\frac1m\sum_{i=1}^m f_i(x)$$

$\nabla f_i$: Full gradient of differentiable component $i$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in \ell_2}F(x)$$

$x^\star$: A global minimizer whose existence is promised by the model; unique under strong convexity

$\ell_2$: Hilbert space of square-summable real sequences

$$\ell_2=\{x=(x_j)_{j\ge1}:\sum_{j\ge1}x_j^2<\infty\}$$

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Norm and inner product of the real Hilbert space

$W,W_t$: Fixed or time-varying communication matrix; spectral normalization and allowed multiplications are specified by the model and algorithm view

$\mathbf1$: All-ones vector of length $m$

$\boldsymbol x^\star$: Consensus vector obtained by placing the unique minimizer of the aggregate objective at every node

$$\boldsymbol x^\star=(x^\star,\ldots,x^\star)$$

$\lambda_{\max},\lambda_{\min}^{+}$: Largest eigenvalue and smallest strictly positive eigenvalue of the fixed symmetric positive-semidefinite communication matrix

$m$: Number of network nodes; a positive integer. **Domain:** $m\ge2$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$\chi$: Network condition parameter; its definitions differ for fixed and time-varying graphs, as specified in each model. **Domain:** $\chi\ge1$.

$E_0$: Initial Lyapunov distance scale, including primal and dual information; it is not automatically an objective gap. **Domain:** $E_0>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$\kappa$: Function condition number $\beta/\mu$.

$$\kappa=\frac{\beta}{\mu}$$

$N_{\nabla},N_{\mathrm{comm}}$: Parallel local-gradient rounds and communication rounds **Domain:** All are nonnegative integers.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

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

### R1 - Standard high-accuracy strongly convex window of the cited result

**Region.** $\mu>0,\ \kappa\ge C,\ \chi\ge3,\ 0<\varepsilon\le cE_0$

**Quantity.** Q1

**Resource.** Joint resource vector

**Status.** Joint budget unresolved

**Achievable budgets.** B1

**Necessary constraints.** B2

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$\mu>0,\ \kappa\ge C,\ \chi\ge3,\ 0<\varepsilon\le cE_0$$

**Dimension conditions.** $\mu>0,\ \kappa\ge C,\ \chi\ge3,\ 0<\varepsilon\le cE_0$

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Hilbert-space implementation of the source algorithm

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Deterministic witness

$$
(C\sqrt\kappa\log(CE_0/\varepsilon),C\chi\sqrt\kappa\log(CE_0/\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2106.04469)

**Oracle correspondence.** Applicable interfaces: local gradients and neighbor communication. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** The error bound holds separately for every admissible instance.

**Source location.** [1](https://arxiv.org/pdf/2106.04469) theorem: §2.4; Theorem6; §3.1 Theorems2–3; PDF pp.5–6,10

### B2 - Long-chain lower bound under the source span-memory model

**Admission.** Included in the bracket

**Direction.** necessary

**Witness or lower-bound scope.** The stated restricted deterministic class

$$
(c\sqrt\kappa\log(E_0/\varepsilon),c\chi\sqrt\kappa\log(E_0/\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2106.04469)

**Oracle correspondence.** Applicable interfaces: local gradients and neighbor communication. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [1](https://arxiv.org/pdf/2106.04469) theorem: §2.4; Theorem6; §3.1 Theorems2–3; PDF pp.5–6,10

## References

[1] Dmitry Kovalev, Elnur Gasanov, Peter Richtarik and Alexander Gasnikov. Lower Bounds and Optimal Algorithms for Smooth and Strongly Convex Decentralized Optimization Over Time-Varying Networks. 2021; Sections 2.4 and 3.1; Theorems 2, 3 and 6, PDF pp.6 and 10.

https://arxiv.org/pdf/2106.04469
