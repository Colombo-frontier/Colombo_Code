# Stochastic convex bandits: two evaluations of the same sample and loss at the center.

**Setting ID.** `ON_BCO2_STO_S`

Online learning and bandits

Each round generates a fresh random convex loss. The algorithm chooses two probe points in advance and receives both values from the same sample. Only the center incurs population mean loss. Sample Lipschitz constants are controlled in second moment and need not be uniformly bounded sample by sample.

**Status.** Fully optimal

**TASK tags.** formulation: Stochastic same sample two point convex pseudo regret; solution concept: Minimize expected cumulative pseudo regret; task family: Online bandit

**MODEL tags.** convexity: Convex; convexity: Sample convex

**ORACLE tags.** derivative order: Order 0; feedback quality: Exact values of same random function; interface family: Two point common sample; operation: Evaluate same sample pair; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** measure: Fresh samples; measure: Native feedback; measure: Projections; measure: Rounds

## 1. Setting specification

### Task

Each round generates a fresh random convex loss. The algorithm chooses two probe points in advance and receives both values from the same sample. Only the center incurs population mean loss. Sample Lipschitz constants are controlled in second moment and need not be uniformly bounded sample by sample.

### Admissible model

Each round draws a fresh full random function $F(\cdot;\xi)$. Every sample function is convex and globally $G(\xi)$-Lipschitz. Only $\mathbb{E}[G(\xi)^2]\le L^2$ is required; individual samples need not satisfy $G(\xi)\le L$.

The population objective is $f$, with finite f = E F. Its optimizer is defined within the ball.

The center $x_t$ incurs the loss and is selected before seeing sample $\xi_t$. Its function value is not returned as a third response.

Both probes $z_t^+,z_t^-$ may lie anywhere in $\mathbb R^d$. They must be chosen jointly before either response for the round is observed.

Require $d,T\ge1$ and $L,R>0$.

Action centers lie in $B_2^d(R)$, while the two probes have query domain $\mathbb{R}^d$; each has its own explicit feasibility conditions.

### Oracle interface

Two evaluations of the same sample:

$$
x_t\in B_2^d(R),\quad z_t^+,z_t^-\in\mathbb{R}^d\ \longmapsto\ \big(F(z_t^+;\xi_t),F(z_t^-;\xi_t)\big)
$$

Choose the center and both probes before drawing one fresh independent sample $\xi_t$.

Both values come from the same sample function indexed by $\xi_t$. There is no additional independent measurement noise.

Probes incur no additional loss. The center does not receive a free third value observation.

Queries within a pair are nonadaptive: the second point cannot depend on the first response.

Public inputs are $d,T,L,R$ and the root-mean-square sample Lipschitz bound. The sample distribution and realizations are hidden.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
f(x)=\mathbb{E}_\xi F(x;\xi),\quad \mathbb{E} G(\xi)^2\le L^2,\quad R_T=\sum_t\left(f(x_t)-\min_{u\in B_2^d(R)}f(u)\right)
$$

### Resource accounting

Each round uses one fresh sample and two function values, totaling T samples and 2T scalar values.

Any causal policy respecting the two-point protocol is admissible. The symmetric-difference witness uses $z_t^\pm=x_t\pm h_tu_t$, with random unit direction $u_t$ and smoothing radius $h_t$.

Direction sampling, two function-value queries, and ball projection are recorded as separate resources. The quantity $h_t$ is an algorithm-chosen smoothing radius, not a numerical accuracy requested from the oracle.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{(F,P)}\mathbb{E}_{\mathcal{A},\xi_{1:T}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$L$: Root-mean-square bound on the global Lipschitz constants of the sample functions **Domain:** $L>0$.

Assume $\mathbb E_{\xi}[G(\xi)^2]\le L^2$; the condition $G(\xi)\le L$ need not hold for every sample.

$R$: Euclidean-ball radius of the center-action set **Domain:** $R>0$.

$B_2^d(R)=\{x\in\mathbb R^d:\|x\|_2\le R\}$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\xi_t,F(\cdot;\xi_t)$: The round’s fresh sample and complete sample function. **Domain:** Independent identically distributed samples and a convex real-valued function.

The two value evaluations in a round share one sample. Different rounds use independent fresh samples.

$P$: The common distribution of samples ξ. **Domain:** A probability distribution.

Instances in the minimax objective consist of the sample-function family $F$ and distribution $P$, with $\xi_t$ drawn i.i.d. from $P$.

$G(\xi)$: Global Euclidean Lipschitz constant of a sample function. **Domain:** A nonnegative random variable.

Assume $|F(x;\xi)-F(y;\xi)|\le G(\xi)\|x-y\|_2$ and $\mathbb E G(\xi)^2\le L^2$.

$f$: Population objective **Domain:** Finite-valued convex function.

$f(x)=\mathbb E_\xi F(x;\xi)$.

$x_t$: Center action that incurs population loss **Domain:** $x_t\in B_2^d(R)$.

$z_t^+,z_t^-$: Two probe points for the same sample. **Domain:** $z_t^+,z_t^-\in\mathbb R^d$.

Both points must be fixed before either current response is returned. They may lie outside the center ball.

$\delta_{\mathrm{sm}},u_t,g_t$: Smoothing radius, spherical direction, and two-point gradient estimate **Domain:** Used only by the upper-bound algorithm.

Assume $z_t^\pm=x_t\pm\delta_{\mathrm{sm}}u_t$ and $g_t=\frac d{2\delta_{\mathrm{sm}}}[F(z_t^+;\xi_t)-F(z_t^-;\xi_t)]u_t$; draw $u_t$ uniformly from the unit sphere.

$\bar x$: Average center used in the online-to-offline lower-bound reduction **Domain:** $\bar x\in B_2^d(R)$.

The quantity $\bar x=T^{-1}\sum_tx_t$ is used only in the proof and does not replace actions already taken.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

The loss is $R_T=\sum_t[f(x_t)-\min_{u\in B_2^d(R)}f(u)]$. Realized observation noise is excluded from the loss difference; probability or expectation aggregation is specified separately by the guarantee.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{(F,P)\in\mathcal I}\mathbb E_{\mathcal A,\xi_{1:T}}[R_T],\\ R_T&=\sum_{t=1}^T\left(f(x_t)-\min_{u\in B_2^d(R)}f(u)\right),\\ f(x)&=\mathbb E_{\xi\sim P}F(x;\xi).\end{aligned}
$$

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes learner randomness and the explicitly specified reward or sample randomness. Conditional expectations retain their stated history conditioning.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$B_2^d(r)$: Closed Euclidean ball of radius r **Domain:** $r\ge0$.

$B_2^d(r)=\{x\in\mathbb R^d:\|x\|_2\le r\}$. The symbol r is a placeholder radius, instantiated as R or 1 in the relevant specification.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The count $N=2T$ measures scalar value evaluations in the two-point protocol. Loss remains charged at the center.

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

The sample-function family and distribution are $(F,P)$. Samples are i.i.d. from $P$; almost surely $F(\cdot;\xi)$ is convex and $G(\xi)$-Lipschitz on $\mathbb R^d$. Assume $\mathbb E_PG(\xi)^2\le L^2$ and a finite population mean function.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative pseudo regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{(F,P)\in\mathcal I}\mathbb E_{\mathcal A,\xi_{1:T}}[R_T],\\ R_T&=\sum_{t=1}^T\left(f(x_t)-\min_{u\in B_2^d(R)}f(u)\right),\\ f(x)&=\mathbb E_{\xi\sim P}F(x;\xi).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $T\ge d\ge 1; L,R>0$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
(LR/24)\sqrt{dT}
$$

**Upper bound.** B1

$$
C LRsqrt(dT)
$$

**Gap or comparison.** Universal constants.

**Comparison argument.** Admit only individually checked claims compatible with this contract.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $T\ge d\ge1$ and $L,R>0$. The two values in a round come from the same fresh sample function, whose Lipschitz constant has second moment at most $L^2$. The center incurs mean loss.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Symmetric two-point smoothing plus OGD

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le C L R\sqrt{dT}
$$

**Sources.** [2](https://jmlr.org/papers/volume18/16-632/16-632.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**fresh samples.** T

**native feedback.** 2T values

**projections.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Conditional on the current sample $\xi_t$, the two-point variance lemma gives $\mathbb E_u\|g_t\|_2^2\le cdG(\xi_t)^2$, where $G(\xi_t)$ is the sample function's Lipschitz constant. Averaging over the sample yields $cdL^2$; the bias uses $\mathbb EG\le L$. The common-sample difference cancels additive function offsets, so no function-level bound is needed. Choose smoothing radius $\delta_{\mathrm{sm}}$ small enough that $L\delta_{\mathrm{sm}} T\le LR\sqrt{dT}$ and apply online gradient analysis.

**Source location.** [2](https://jmlr.org/papers/volume18/16-632/16-632.pdf) theorem: Corollary 2; Theorem 1 proof; pdf pages: 1; 4; 5; 6; 7

The center $w_t$ incurs loss; the two probes in the same round provide only feedback. Multiply the source's average regret by $T$. In the random-sample variant, replace the pointwise squared Lipschitz bound with the sample Lipschitz constant's second moment.

### B2 - Duchi et al. q=2 Gaussian linear sample family + online-to-batch

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge\frac{LR}{24}\sqrt{dT}
$$

**Sources.** [1](https://www.cs.yale.edu/homes/wibisono/DucJorWaiWib15.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**fresh samples.** T

**native feedback.** 2T values

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** For any online learner, let $\bar x=T^{-1}\sum_tx_t$. Convexity of the ball makes the average feasible, and convexity of the function gives $\mathbb E[f(\bar x)-f^\star]\le\mathbb E R_T/T$. The source proves optimization error at least $(LR/24)\min\{1,\sqrt{d/T}\}$ for an interface allowing two evaluations per sample. The same transcript and averaged output respect that interface, giving the cumulative pseudo-regret lower bound when $T\ge d$.

**Source location.** [1](https://www.cs.yale.edu/homes/wibisono/DucJorWaiWib15.pdf) theorem: Proposition 1, q=2; Section V-A; pdf pages: 6; 7; 11; 12; printed pages: 2793; 2794; 2798; 2799; equations: (2); (19); (20)

The source uses a second-moment bound on gradients/Lipschitz constants and a Gaussian linear sample hard family. Both evaluations in a round share sample $X_t$. Its optimization error lower bound $(LR/24)\min\{1,\sqrt{d/T}\}$ is converted by the stated argument to an online cumulative pseudo-regret lower bound.

## References

[1] John C. Duchi; Michael I. Jordan; Martin J. Wainwright; Andre Wibisono. Optimal Rates for Zero-Order Convex Optimization: The Power of Two Function Evaluations. 2015. IEEE Transactions on Information Theory 61(5):2788–2806.

https://www.cs.yale.edu/homes/wibisono/DucJorWaiWib15.pdf

[2] Ohad Shamir. An Optimal Algorithm for Bandit and Zero-Order Convex Optimization with Two-Point Feedback. 2017. JMLR 18(52):1–11.

https://jmlr.org/papers/volume18/16-632/16-632.pdf
