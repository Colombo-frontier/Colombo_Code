# Minimization of a finite maximum of convex functions: unknown offsets and component-gradient-only access; selected component gradients

**Setting ID.** `SO_FO_F04_component_G`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Infinite complexity

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; convexity: Convex components; geometry: Euclidean ball; geometry: Full space; smoothness: Lipschitz function; structure: Finite max; structure: Unknown component offsets

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Component gradient; operation: Component gradient; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Component calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}F(x)$$

The complete objective is $F(x)=\max_{1\le i\le n}f_i(x)$. It may be nonsmooth even when all components are smooth.

### Admissible model

The $n$ unknown components are convex and differentiable in a neighborhood of the public ball $Q$, with $\|\nabla f_i\|\le L$ and $\beta$-Lipschitz gradients. Their constant offsets are unknown. The maximum $F=\max_i f_i$ is generally nonsmooth.

Feasible geometry: $Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$.

Unless another geometry is specified, vectors use the Euclidean norm $\|\cdot\|_2$, and matrices and higher derivatives use the corresponding operator norm. The assumptions hold uniformly throughout the declared domain.

Individual smoothness means $\|\nabla f_i(u)-\nabla f_i(v)\|_2\le\beta\|u-v\|_2$ simultaneously for every $i\in\{1,\ldots,n\}$ and every pair $u,v$ in the declared model domain.

Admissible parameter domain:

$$\begin{gathered}\varepsilon > 0,\quad d \ge 1,\quad n \ge 1,\quad L > 0\\R > 0,\quad \beta \ge 0\end{gathered}$$

### Oracle interface

Public numerical inputs: $d,\ n,\ \varepsilon$.

Public upper bounds: $L,\ \beta,\ R$.

The unknown objects are the component functions $f_1,\ldots,f_n$.

For each query, the algorithm chooses $i\in\{1,\ldots,n\}$ and $x\in Q$ and receives the following information about that component.

$$\nabla f_i(x)$$

All responses come from one fixed unknown instance. The algorithm adaptively chooses query points and any indices permitted by the interface.

Exact Euclidean projection onto the public domain; its internal computation is free

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$F(\widehat{x})-\min_{u\in Q}F(u)$$

$F^\star=\inf_{x\in Q}F(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One component-gradient query costs one call. No function-value anchor is supplied.

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

$f_i,F$: Unknown components and finite-maximum objective **Domain:** $i\in\{1,\ldots,n\}$.

$$F(x)=\max_{1\le i\le n}f_i(x)$$

$\nabla f_i$: Full gradient of differentiable component $i$

$F^\star$: Optimal value of the complete task; the oracle need not return it

$$F^\star=\inf_{x\in Q}F(x)$$

$Q$: Feasible set of the task

$$Q=\{x\in\mathbb{R}^d:\|x\|_2\le R\}$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$d$: Ambient dimension; a positive integer tracked explicitly. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$n$: Public number of components in the finite sum or finite maximum. **Domain:** $n\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the Lipschitz constant of the objective or components. **Domain:** $L>0$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta\ge0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$c$: Sufficiently small universal positive constant, potentially different between theorems; it is not a numerical threshold. **Domain:** $0<c<1$.

$C$: Sufficiently large universal constant, independent of the tracked parameters; no numerical value is specified. **Domain:** $C>1$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

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

**Definition.** One component-gradient query costs one call. No function-value anchor is supplied.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Unknown relative additive offsets cause nonidentifiability

**Region.** $n\ge2,\quad0<\varepsilon<LR/2$

**Quantity.** Q1

**Resource.** One component-gradient query costs one call. No function-value anchor is supplied.

**Status.** Infinite complexity

**Lower bound.** B1

$$
+\infty
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $$n\ge2,\quad0<\varepsilon<LR/2$$

**Dimension conditions.** $n\ge2,\quad0<\varepsilon<LR/2$

**Oracle mapping.** Applicable interfaces: selected component gradients. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee mapping.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Two instances with identical full-gradient histories

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
T_{\rm rand}^{\rm CompG}=+\infty
$$

**Sources.** [1](https://arxiv.org/pdf/2311.10886) [2](https://arxiv.org/pdf/1405.4980) [3](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [4](https://arxiv.org/pdf/2609.20701)

**Local argument.** A1, A2, A3, A4

## 5. Local arguments

### A1 - Finite maxima, hidden offsets, and budget conversion

**Scope.** Component values and gradients for simulation; component gradients alone for the offset impossibility.

**Algorithm scope.** Deterministic simulation upper witnesses; randomized hidden-index lower bounds; randomized budget conversion when needed.

With component value-gradient access, query all $n$ components, select an active one, and use its gradient as a subgradient of $F=\max_i f_i$. This transfers subgradient and certificate algorithms at cost $n$ per full response. The maximum is $L$-Lipschitz; the center has gap at most $LR$.

For an $\Omega(n)$ lower bound, hide an index $J$. Its component is $LR+Lx_1$ or $LR-Lx_1$; every other component is zero. The hidden component is nonnegative on the ball and dominates the maximum. Before it is queried, the two signs have average loss $LR$ for any common output. A fixed budget hits $J$ with probability at most $T/n$. Thus $\Omega(n)$ calls are necessary at nontrivial accuracy, for arbitrary randomized algorithms.

When $\beta=0$, each component is affine. One value-gradient query reconstructs its formula, so $n$ calls and free internal optimization solve the problem exactly. Replicating a smooth one-dimensional hard function in all components gives the logarithmic lower term with scale $\min\{LR,\beta R^2\}$. Combine it with the hidden-index term by taking a maximum, not a product.

With component gradients alone, relative additive offsets are invisible. The pair $Lx$, $-Lx+c$ has the same gradients for all $c$, but its maximum has different minimizers. Two offsets with separated interior minimizers give a positive worst-case error for every common output distribution, independently of the query budget.

For an imported upper bound with a constant-probability joint event of acceptable error and budget, truncate each run, repeat independently, and evaluate all components at every candidate to choose the best exact maximum. Feasible outputs have gap at most $2LR$. Reducing failure to $\epsilon/(4LR)$ therefore gives expected error at most $\epsilon$. Repetition and validation calls are charged, producing the recorded logarithmic overhead.

**Limits of the argument.** Additive offsets and the guarantee/budget conversion must be kept explicit.

**Sources.** [1](https://arxiv.org/pdf/2311.10886)

### A2 - Projected and weighted subgradient bounds

**Scope.** Public Euclidean projection; unbiased conditional subgradient mean and a total second-moment bound, or exact subgradients.

**Algorithm scope.** Deterministic policies and deterministic averages; randomness may come from observations.

Projection onto a public closed convex set gives
$$
\|x_{t+1}-x^\star\|^2\le\|x_t-x^\star\|^2
-2\eta_t\langle g_t,x_t-x^\star\rangle+\eta_t^2\|g_t\|^2.
$$
For convex $f$, initial distance at most $R$, and conditional second moment at most $V$, the constant step $R/\sqrt{VK}$ and averaged output have expected gap at most $R\sqrt{V/K}$. Exact subgradients correspond to $V=L^2$.

Under $\mu$-strong convexity, use $\eta_t=2/[\mu(t+1)]$. With $a_t=\mathbb E\|x_t-x^\star\|^2$,
$$
\mathbb E[f(x_t)-f^\star]\le{\mu(t-1)\over4}a_t
-{\mu(t+1)\over4}a_{t+1}+{V\over\mu(t+1)}.
$$
Multiply by $t$, sum, and use convexity. The weighted output
$\sum_{t=1}^K2t\,x_t/[K(K+1)]$ has expected gap at most $2V/[\mu(K+1)]$. Neither output rule requires private randomness. Apply norm conversion before these inequalities, preserving all dimension factors.

**Limits of the argument.** Norm-conversion factors must be applied explicitly. No noisy cutting-plane result follows from this recursion.

### A3 - Subgradient certificates and centroid cuts

**Scope.** One full subgradient is sufficient. Public compact convex geometry and exact internal geometric computation are available.

**Algorithm scope.** Deterministic upper-bound witness; valid as an upper bound for randomized views.

Let $Q\subset\mathbb R^d$ be public, compact, convex, and full dimensional, with diameter at most $D$ in the stated norm. Suppose all returned subgradients have dual norm at most $L$. Query $g_i\in\partial f(x_i)$ at the centroid of the current body and retain $\langle g_i,x_i-x\rangle\ge0$. The centroid halfspace theorem bounds the retained volume by $(1-e^{-1})^T\operatorname{vol}(Q)$.

The computable certificate is
$$
\Gamma_T=\min_{\lambda\in\Delta_T}\max_{x\in Q}\sum_i\lambda_i\langle g_i,x_i-x\rangle
=\max_{x\in Q}\min_i\langle g_i,x_i-x\rangle.
$$
The equality is convex minimax. Subgradient inequalities and convexity imply
$f(\sum_i\lambda_ix_i)-\min_Qf\le\Gamma_T$.
If $\Gamma_T>\epsilon$, choose $z\in Q$ with all cut margins greater than $\epsilon$. The copy $(1-a)z+aQ$, where $a=\epsilon/[2(\epsilon+LD)]$, survives every cut. Its volume is $a^d\operatorname{vol}(Q)$, contradicting centroid shrinkage once $T>C d\log(2+LD/\epsilon)$. If the body loses volume earlier, the same positive-volume argument already certifies the error. No function values or inscribed-ball estimate are required.

For $Q=RB_p^d$ and $\ell_q$-Lipschitz objectives, use $D=2Rd^{(1/q-1/p)_+}$. Returning the center has error at most $LRd^{(1/q-1/p)_+}$, giving the coarse zero-query regime. Exact centroid, minimax, and public geometric calculations are uncharged internal operations.

For a deterministic selector with total movement at most $W(T)$ on nested convex sets, instead impose deep cuts of margin $2LW(T)/T$. If all $T$ sets are nonempty, every move has length at least $2W(T)/T$, contradicting the movement bound. At the first empty intersection, minimax gives error at most $2LW(T)/T$. Substitution of the cited stable-movement theorem yields the recorded nondual upper bound. Its deterministic information scope is distinct from the scope of randomized implementations.

**Limits of the argument.** The stable-selector branch imports its movement theorem and does not claim efficient deterministic arithmetic time.

**Sources.** [2](https://arxiv.org/pdf/1405.4980) [3](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [4](https://arxiv.org/pdf/2609.20701)

### A4 - A one-dimensional lower bound with exact values and gradients

**Scope.** Exact values and gradients; unbounded real-line queries, with higher-dimensional embeddings.

**Algorithm scope.** Lower bounds against arbitrary randomized adaptive algorithms, including unqueried output.

Fix $1<\kappa=\beta/\mu$. Choose a fixed smooth $\psi$, equal to $-x$ on $[-1/2,1/2]$ and zero outside $[-1,1]$, and let $C_\psi=\max\{1,\|\psi''\|_\infty\}$. Set
$$
\beta_0=(\beta+\mu)/2,\quad a={\kappa-1\over8C_\psi(\kappa+1)},\quad
\eta=a/4,\quad \rho_0={(1-\eta)\over a}\sqrt{\Delta/\beta}.
$$
For independent uniform signs $b_i$, define $u_0=0$,
$u_i=u_{i-1}+b_i a\rho_{i-1}$, $\rho_i=\eta\rho_{i-1}$, and
$$
f_b(x)=\beta_0x^2/2+
\beta_0\sum_{i=1}^N b_i a\rho_{i-1}^2
\psi((x-u_{i-1})/\rho_{i-1}).
$$
The two child intervals $I_i=[u_i-\rho_i,u_i+\rho_i]$ are disjoint and lie inside the central half of the parent. Second derivatives of successive bumps have disjoint shell supports. Thus $\mu\le f_b''\le\beta$, and $f_b''\ge7\beta/16$. Within $I_i$, the partial sum through level $i$ is a quadratic centered at $u_i$. The final minimizer is $u_N$, with $|u_N|\le\sqrt{\Delta/\beta}$ and initial gap at most $\Delta/2$.

A stronger oracle reveals the next bit when the query lies in the current unresolved interval, continuing only while it lies in the selected child. Unrevealed bumps vanish near the query, so the revealed prefix computes the exact value and derivative. Conditional on history, a fixed point belongs to at most one child; one query reveals at most $\sum_{j\ge1}2^{-(j-1)}=2$ new bits in expectation.

Treat the final output as one more such query. If $|\widehat x-u_N|<\rho_N$, all $N$ bits are revealed. Its probability is at most $2(T+1)/N$. Otherwise the loss is at least
$c\beta\rho_N^2=c'\Delta\eta^{2(N-1)}$.
Choose $N$ at the accuracy scale and use opposite translations to exclude zero calls. For expected error and constant-probability accuracy,
$$
T\ge c\left[1+{\log(\Delta/\epsilon)\over
\log(C\kappa/(\kappa-1))}\right].
$$
Queries may be arbitrary, randomized, adaptive, and unbounded.

Fixing $\kappa=2$, $\Delta=c\beta R^2$, gives the initial-distance logarithmic bound. The gradient version uses
$|f_b'(x)|\ge(7\beta/16)|x-u_N|$.
Add a public quadratic to embed in higher dimension. For composite minimization, apply the construction on total curvature interval $[\mu,\mu+\beta]$, with public $h(x)=\mu x^2/2$; the unknown remainder is convex and $\beta$-smooth, and every proximal response for $h$ is independent of the hidden bits.

**Limits of the argument.** Curvature, initialization, and nontrivial-accuracy restrictions remain explicit; the composite transfer lower-bounds unknown-gradient calls.

## References

[1] Yair Carmon, Arun Jambulapati, Yujia Jin and Aaron Sidford. A Whole New Ball Game: A Primal Accelerated Method for Matrix Games and Minimizing the Maximum of Smooth Functions. 2023 preprint; STOC 2024; Table 1; Section 2.5; Definitions 8.1–8.2; Theorem 8.1 and Section 8.1.

https://arxiv.org/pdf/2311.10886

[2] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[3] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf

[4] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701
