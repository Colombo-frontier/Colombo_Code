# Finite-sum minimization with convex components: components Lipschitz on the domain, strongly convex average; selected component subgradients

**Setting ID.** `SO_FO_F01_nonsmooth_sc`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex components; convexity: Strongly convex; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; structure: Finite sum

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component subgradient; operation: Component subgradient; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}F(x)$$

The complete objective is the finite sum $F(x)=n^{-1}\sum_{i=1}^n f_i(x)$. Component information is available only through the declared component oracle.

### Admissible model

The $n$ unknown components are globally convex and $L$-Lipschitz. Their average $F$ is $\mu$-strongly convex on the public ball $Q$. Simultaneous global Lipschitz continuity and global strong convexity are not required.

Feasible geometry: $Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad \mu > 0\\\mu\,R \le \frac{L}{2},\quad \varepsilon \le c\,L\,R,\quad L > 0,\quad R > 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $L,\ R$.

Public lower bounds: $\mu$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in Q$ and receives the following information about that component.

$$g_i\in\partial f_i(x),\quad\|g_i\|\le L$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

Exact Euclidean projection onto the public domain; its internal computation is free

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=F(\widehat{x})-F^\star$$

$F^\star=\inf_{x\in Q}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One selected-component subgradient costs one call; the component index is chosen by the algorithm, under a fixed call budget.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f_i,F$: Unknown components and finite-sum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\frac1n\sum_{i=1}^n f_i(x)$$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in Q}F(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\partial f_i(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f_i(x)=\{g:f_i(u)\ge f_i(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f_i\}$$

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$\mu$: Lower bound on the strong-convexity modulus of the objective specified by the model **Domain:** $\mu>0$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$H_{\rm ns}$: $\min\{L^2R^2/\epsilon^2,L^2/(\mu\epsilon)\}$: the high-dimensional query scale for nonsmooth strongly convex optimization.

$$H_{\rm ns}=\min\{{\frac{L\,R}{\varepsilon}}^{2},\frac{{L}^{2}}{\mu\,\varepsilon}\}$$

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One selected-component subgradient costs one call; indices are sampled uniformly, under a fixed sample budget.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Sufficiently high dimension for a nonsmooth strongly convex average

**Region.** $d\ge CH_{\rm ns}$

**Quantity.** Q1

**Resource.** One selected-component subgradient costs one call; indices are sampled uniformly, under a fixed sample budget.

**Status.** Optimal

**Lower bound.** B3

$$
cH_{\rm ns}
$$

**Upper bound.** B1, B2

$$
CH_{\rm ns}
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** Compare on the intersection of F01.nonsmooth-sc-R.parameter-domain and F01.nonsmooth-sc-hd. Keep the two algorithms separate before taking their minimum. The sufficiently high-dimensional lower bound matches; $n$ does not change this worst-case class.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Projected subgradient descent with uniformly sampled components

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
CL^2R^2/\varepsilon^2
$$

**Sources.** [1](https://www2.isye.gatech.edu/~nemirovs/SIOPT_RSA_2009.pdf)

**Conditions.** $$0<\mu R\le L/2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\mu R\le L/2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: selected component subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [1](https://www2.isye.gatech.edu/~nemirovs/SIOPT_RSA_2009.pdf) theorem: §2.2, Eqs.(2.19)–(2.21); finite sum uniform sampling

### B2 - Epoch-based or weighted strongly convex subgradient method

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
CL^2/(\mu\varepsilon)
$$

**Sources.** [2](https://jmlr.org/papers/volume15/hazan14a/hazan14a.pdf)

**Conditions.** $$0<\mu R\le L/2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $0<\mu R\le L/2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: selected component subgradients. Algorithms may use only these interfaces and the auxiliary operations explicitly declared public.

**Guarantee conversion.** After fixing the instance and admissible response law, take expectation over the randomness declared by the target contract and control the underlying error.

**Source location.** [2](https://jmlr.org/papers/volume15/hazan14a/hazan14a.pdf) theorem: Theorem1; uniform component sampling

### B3 - Replication of the same strongly convex hard instance

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cH_{\rm ns}
$$

**Sources.** [3](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [4](https://arxiv.org/pdf/1405.4980) [5](https://arxiv.org/pdf/1407.5144) [6](https://arxiv.org/pdf/1401.1792)

**Conditions.** $$d\ge CH_{\rm ns}$$

**Dimension conditions.** $d\ge CH_{\rm ns}$

**Oracle correspondence.** Applicable interfaces: selected component subgradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Local argument.** A1, A2

## 5. Local arguments

### A1 - Finite-sum simulation and hidden components

**Scope.** Exact component gradients; the declared average objective and component regularity.

**Algorithm scope.** Deterministic full-gradient upper witnesses; lower constructions preserve their source algorithm scopes.

A full gradient of $F=n^{-1}\sum_i f_i$ costs $n$ component calls. Mean-square smoothness implies
$$
\|\nabla F(x)-\nabla F(y)\|
\le(n^{-1}\sum_i\|\nabla f_i(x)-\nabla f_i(y)\|^2)^{1/2}
\le\beta\|x-y\|.
$$
Individual smoothness also implies this. Full-gradient convex, strongly convex, PL, stationarity, and certificate algorithms therefore transfer with an $n$ multiplier. A zero-query endpoint remains zero. Convexity or PL of the average must be stated separately.

For an unrestricted smooth finite-sum $\Omega(n)$ baseline, hide an index $J$. All components have public quadratic curvature $\beta$; only component $J$ has an unknown linear term $\mp n\beta R x_1$. Their average is
$\beta\|x\|^2/2\mp\beta Rx_1$, with minimizer distance $R$. Until $J$ is queried, its sign is hidden. A budget much smaller than $n$ misses it with constant probability, giving loss of order $\beta R^2$. This construction requires a model allowing the component linear offsets.

For an expected-budget lower-bound conversion, truncate after a sufficiently large constant multiple of the expected budget. Markov's inequality makes truncation unlikely enough to preserve a constant-probability hard-instance lower bound. This does not convert an expected-budget upper bound to a pathwise budget.

Replicating the same hard function in every component preserves its one-function lower bound without multiplying by $n$. This covers nonsmooth strongly convex and one-dimensional logarithmic subclasses.

In the cited span-restricted construction, individual smoothness is $\sqrt n$ times the native mean-square parameter. Substitute native parameter $\beta/\sqrt n$ to obtain the recorded individual-smoothness lower bound. Keep the original span, dimension, and accuracy restrictions. Rescaling does not expand the lower algorithm class.

**Limits of the argument.** Replication gives no extra factor n. The rescaled lower theorem remains span-restricted.

**Sources.** [3](https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf) [4](https://arxiv.org/pdf/1405.4980)

### A2 - Strongly convex information-theoretic reductions

**Scope.** Exact value and one full subgradient; original query domain and public regularizer.

**Algorithm scope.** Lower bounds against arbitrary randomized adaptive algorithms.

The imported ingredients are Braun–Guzmán–Pokutta's string-guessing simulation (Lemma V.4), recursive boxes (Section IV and Lemma IV.7), and Proposition III.3. Their arbitrary-randomized local-information scope includes values and subgradients.

For $\mu R\le L/2$, put $a=L/2$ and
$$
F_s(x)=a\max_{i\le m}s_ix_i+\mu\|x\|^2/2.
$$
At $x_i=-s_i\min\{R/\sqrt m,a/(\mu m)\}$, its value is at most
$-\tfrac a2\min\{R/\sqrt m,a/(\mu m)\}$.
Whenever

$$m\le c\min\{d,(LR/\epsilon)^2,L^2/(\mu\epsilon)\},$$

any sufficiently accurate output identifies all signs. Subtracting the public quadratic leaves the imported string simulation and proves the dimension-truncated power term.

For the logarithmic term, set $R_{\rm loc}=\min\{R,\sqrt{\epsilon/\mu}\}$, $b=R_{\rm loc}/\sqrt d$, and
$$
h_s(x)=ab\max_{i\le d}\phi_{s_i}(x_i/b),\qquad
F_s=h_s+\mu\|x\|^2/2.
$$
The recursive convex one-Lipschitz functions $\phi_s$ have equal minima and continue as $|u|$ outside $[-1,1]$. A minimizer $y$ of $h_s$ lies in the small box. An $O(\epsilon)$-solution of $F_s$ is an $O(\epsilon)$-solution of $h_s$, because only the comparison term $\mu\|y\|^2/2$ enters the bound. Outside the box, a public absolute-value tail attains the maximum and supplies feedback without revealing bits. Inside, Lemma IV.7 applies. The resulting lower term is
$$
\Omega\!\left(d\log_+\!\left[{L\over\epsilon\sqrt d}
\min\{R,\sqrt{\epsilon/\mu}\}\right]\right).
$$
Combining it with the power term gives the displayed $d\log(1+H_\epsilon/d)$ rate. Markov's inequality converts expected error to constant-probability accuracy. Near the compatibility boundary, replace $a$ by $L_{\rm rem}/2$ and retain $\epsilon\le cL_{\rm rem}^2/\mu$. A globally convex Lipschitz extension is the supremum of the supporting affine functions on the compact query domain.

For matching $1\le p\le2$, use a public prox $\psi_p$ that is one-strongly convex in $\ell_p$, satisfies $\psi_p(x)\le C\Gamma_p(d)\|x\|_p^2$, and has Lipschitz constant at most $CR\Gamma_p(d)$ on $RB_p^d$. A construction is
$$
u=\max\{p,\min\{2,1+1/\log(2d)\}\},\quad
\psi_p(x)={\|x\|_u^2\over2(u-1)d^{2(1/u-1/p)}}.
$$
The squared-norm fact is supplied by Juditsky–Nesterov. In $m$ coordinates use a normalized Hadamard basis $v_i$ and
$h_s=a m^{1/p-1/2}\max_i s_i\langle v_i,x\rangle$.
The point $y=-R_{\rm loc}m^{-1/p}\sum_i s_iv_i$ has
$\|y\|_p\le R_{\rm loc}$, $h_s(y)=-aR_{\rm loc}/\sqrt m$, and
$\psi_p(y)\le C\Gamma_p(d)R_{\rm loc}^2$.
Optimizing $R_{\rm loc}\le R$ gives
$\min\{d,(LR/\epsilon)^2,L^2/[\mu\Gamma_p(d)\epsilon]\}$.
Subtract the public prox before the information simulation. Restricting $m$ to powers of two changes only constants.

For $p>2$, standard coordinate signs and $\psi_p=\|\cdot\|_2^2/2$ give
$\min\{d,(LR/\epsilon)^p,L^2/(\mu\epsilon)\}$.
Recursive boxes of half-width $R_{\rm loc}d^{-1/p}$ give the companion logarithmic term. The declared compatibility slack reserves a constant share of the Lipschitz budget for the hidden function.

For general $(p,q,r)$, set $\mu_{\rm quad}=\mu d^{2(1/r-1/2)_+}$. The public quadratic is $\mu$-strongly convex in $\ell_r$, and its gradient norm on $RB_p^d$ is at most
$\mu_{\rm quad}R d^{(1-1/p-1/q)_+}$ in $\ell_{q^\star}$.
Under the stated slack condition, a hidden single-coordinate slope of size $L/2$ is legal. The same sign and box arguments give the general formulas, with constants inside variable powers retained.

The $p>2$ upper term $(L^2/(\mu\epsilon))^{p/2}$ follows by restarting a convex $C_p(LR/u)^p$ method at error scale $u$, using radius $O(\sqrt{u/\mu})$. The geometrically decreasing stages are dominated by the final stage. These reductions do not assert uniform optimality across geometries.

**Limits of the argument.** Uses identified primary information-theoretic lemmas. Retain compatibility slack, norm dependence, and the accuracy windows.

**Sources.** [5](https://arxiv.org/pdf/1407.5144) [6](https://arxiv.org/pdf/1401.1792)

## References

[1] Arkadi Nemirovski, Anatoli Juditsky, Guanghui Lan and Alexander Shapiro. Robust Stochastic Approximation Approach to Stochastic Programming. 2009; Section 2.2, equations (2.19)-(2.21), PDF p.7; uniform finite-sum sampling reduction.

https://www2.isye.gatech.edu/~nemirovs/SIOPT_RSA_2009.pdf

[2] Elad Hazan and Satyen Kale. Beyond the Regret Minimization Barrier: Optimal Algorithms for Stochastic Strongly-Convex Optimization. 2014; JMLR 15:2489–2512; Theorem 1.

https://jmlr.org/papers/volume15/hazan14a/hazan14a.pdf

[3] Dongruo Zhou and Quanquan Gu. Lower Bounds for Smooth Nonconvex Finite-Sum Optimization. 2019; Definition 3.3; Theorem 4.2; Section 4.3 and Proposition 4.9.

https://proceedings.mlr.press/v97/zhou19b/zhou19b.pdf

[4] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[5] Gábor Braun; Cristóbal Guzmán; Sebastian Pokutta. Lower Bounds on the Oracle Complexity of Nonsmooth Convex Optimization via Information Theory. 2017; arXiv v3 2023.

https://arxiv.org/pdf/1407.5144

[6] Anatoli Juditsky; Yuri Nesterov. Primal-dual subgradient methods for minimizing uniformly convex functions; journal version: Deterministic and Stochastic Primal-Dual Subgradient Algorithms for Uniformly Convex Minimization. 2014.

https://arxiv.org/pdf/1401.1792
