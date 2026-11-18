# Stochastic convex bandits: one-point observations with independent Gaussian noise.

**Setting ID.** `ON_BCO1_STO_S`

Online learning and bandits

A fixed unknown convex function is defined on the unit Euclidean ball. Each round reveals one value with independent Gaussian noise at the point where loss is incurred. The objective is cumulative true function loss. The unknown additive offset is not supplied as free information.

**Status.** Polynomial gap present

**TASK tags.** formulation: Stochastic one point bandit convex pseudo regret; solution concept: Minimize expected cumulative pseudo regret; task family: Online bandit

**MODEL tags.** convexity: Convex; convexity: Convex in action; smoothness: Lipschitz in action; stochastic model: Additive gaussian noise

**ORACLE tags.** derivative order: Order 0; feedback quality: Noisy function value; interface family: One point value; operation: Evaluate loss at action; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** measure: Membership calls; measure: Native feedback; measure: Projections; measure: Rounds; measure: Sampling calls

## 1. Setting specification

### Task

A fixed unknown convex function is defined on the unit Euclidean ball. Each round reveals one value with independent Gaussian noise at the point where loss is incurred. The objective is cumulative true function loss. The unknown additive offset is not supplied as free information.

### Admissible model

The fixed unknown convex objective $f$ is continuous and 1-Lipschitz on the unit ball. Differentiability and Lipschitz gradients are not required. An unknown additive constant leaves regret unchanged but affects absolute observed values.

Scalar observation noise $Z_t$ is i.i.d. N(0,1) and independent of the history before action selection.

The unique action and query point is $x_t$: loss is incurred where the single observation is taken.

Require $d,T\ge1$, with actual queries satisfying $x_t\in B_2^d(1)$.

Function values need not lie in [0,1]. The 1-Lipschitz condition controls only their variation within the ball.

### Oracle interface

One-point function value with fresh noise:

$$
t,\ x_t\in B_2^d(1)\ \longmapsto\ Y_t\mid\mathcal{H}_{t-1},x_t\sim\mathcal{N}(f(x_t),1)
$$

Each round returns only one number, with no exact f value or gradient.

Repeating a point consumes another round and produces independent noise. A same-noise difference pair is not free.

If the upper-bound algorithm first calibrates $f(0)$, those calls consume budget $T$. The value cannot be treated as known.

Public inputs are $d,T$, the unit-ball domain, Lipschitz bound one, and independent Gaussian scalar noise of variance one. The value $f(0)$ is hidden.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
Y_t=f(x_t)+Z_t,\quad Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal{N}(0,1),\quad R_T=\sum_t\left(f(x_t)-\min_{u\in B_2^d(1)}f(u)\right)
$$

### Resource accounting

$T$ rounds provide $T$ noisy function values; all calibration and exploration samples are included in $T$.

Any causal randomized policy is allowed. One-point smoothing and stochastic Newton upper bounds must both respect the actual query budget.

The 2024 Newton upper bound calibrates the unknown additive offset and uses the public ball geometry. Membership tests, sampling, and matrix operations are recorded separately from loss queries.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{f\,\mathrm{convex},\ \mathrm{Lip}_2(f)\le1}\mathbb{E}_{\mathcal{A},Z}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$C_0$: Sufficiently large universal regime constant used in both the lower-bound and calibration arguments **Domain:** Take $C_0\ge16$ as a fixed constant satisfying the source window.

Only regions such as $d\ge C_0$ and $T\ge C_0d^2$ are specified; the source gives no replacement numerical threshold.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$f$: The fixed unknown convex objective. **Domain:** $f:B_2^d(1)\to\mathbb R$.

The function is continuous and one-Lipschitz on the ball; $f(0)$ is hidden.

$x_t$: The only query point that incurs loss. **Domain:** $x_t\in B_2^d(1)$.

$Z_t,Y_t$: Independent noise and the observed function value. **Domain:** $Z_t\sim\mathcal N(0,1),\ Y_t\in\mathbb R$.

$Y_t=f(x_t)+Z_t$.

$n_0,\widehat f_0$: Charged calibration rounds and estimation of the function value at the origin **Domain:** Algorithmic initialization quantity.

Assume $n_0=\lceil2\log(4T)\rceil$; $\widehat f_0$ is the mean of these $n_0$ observations at the origin.

$\delta_{\mathrm{sm}},u_t$: The spherical smoothing radius and random direction. **Domain:** $0<\delta_{\mathrm{sm}}\le1/2,\ u_t\in\mathbb S^{d-1}$.

The smoothing branch uses $\delta_{\mathrm{sm}}\asymp\sqrt d\,T^{-1/4}$ and directions uniform on the Euclidean unit sphere.

$g_t$: Stochastic gradient estimate from spherical smoothing **Domain:** $g_t\in\mathbb R^d$.

$g_t=(d/\delta_{\mathrm{sm}})(Y_t-\widehat f_0)u_t$.

$\delta_{\mathrm{conf}}$: Internal failure probability for the Newton branch or calibration event **Domain:** Used only for the proof or algorithm tuning.

The Newton branch uses $\delta_{\mathrm{conf}}=1/(2T)$, independently of the smoothing radius.

$h,M$: The function and symmetric-domain geometric scales after specializing the Newton theorem. **Domain:** Used only in this argument.

The expression is $h=(f-\widehat f_0+2)/4$; for the present symmetric ball, use $M=d^{-1/2}$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_t[f(x_t)-\min_{u\in B_2^d(1)}f(u)]$ Realized observation noise is excluded from the loss difference. Probability or expectation aggregation is specified separately by the guarantee.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{f\in\mathcal I}\mathbb E_{\mathcal A,Z}[R_T],\\ R_T&=\sum_{t=1}^T\left(f(x_t)-\min_{u\in B_2^d(1)}f(u)\right).\end{aligned}
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

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

$\mathcal I$: The complete environment class in the current minimax objective. **Domain:** Collection of function classes or reward-distribution classes.

The objective f is fixed, real-valued, continuous, convex, and 1-Lipschitz on the unit Euclidean ball. Its additive level f(0) is arbitrary and hidden. Each query adds independent standard Gaussian noise.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative pseudo regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{f\in\mathcal I}\mathbb E_{\mathcal A,Z}[R_T],\\ R_T&=\sum_{t=1}^T\left(f(x_t)-\min_{u\in B_2^d(1)}f(u)\right).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - INTERMEDIATE

**Region.** $d\ge C_0, C0d^2\le T\le d^{10/3}$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B3

$$
c \sqrt{d}T^{3/4}
$$

**Upper bound.** B1

$$
C \sqrt{d} T^{3/4}
$$

**Gap or comparison.** Controlled by universal constants after an explicit reduction calibrates the unknown function level.

**Comparison argument.** Only individually audited compatible claims enter. Proof-constant window; C_0 is not assigned an invented numerical threshold.

### R2 - LONG

**Region.** $d\ge C_0; T\ge \max{C0d^2,d^{10/3}}$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Polynomial gap

**Lower bound.** B3

$$
c d^{4/3}sqrtT
$$

**Upper bound.** B1, B2

\min{C \sqrt{d}T^{3/4}, C d^{3/2}sqrtT polylog(Td)}

**Gap or comparison.** The ratio is at most O(d^(1/6) polylog(Td)); a tighter ratio is available near the crossover of the first upper bound.

**Comparison argument.** Only individually audited compatible claims enter. Verified envelope gap; no assertion that this gap itself is an open problem proven by this audit.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require $d\ge C_0$ and $T\ge C_0d^2$, where $C_0$ is a sufficiently large universal constant. The fixed convex function is defined on the unit ball and has Lipschitz constant at most one. One-point observations contain independent standard Gaussian noise.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - One-point smoothing + projected OGD, with initial level calibration

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le C\sqrt d\,T^{3/4}
$$

**Sources.** [1](https://arxiv.org/pdf/2406.06506v1) [3](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T including calibration

**native feedback.** T one-point observations

**projections.**

$$
\le T
$$

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** First use $n_0=\lceil2\log(4T)\rceil$ charged rounds at the origin to estimate $f(0)$ by $\widehat f_0$. With probability at least $1-1/(2T)$, the estimation error is at most one, so $|f(x)-\widehat f_0|\le2$ throughout the unit ball. With smoothing radius $\delta_{\mathrm{sm}}$, choose a center in the contracted ball and query the center plus $\delta_{\mathrm{sm}} u_t$, where $u_t$ is a random unit direction. The loss is incurred at this query point. The estimator $g_t=(d/\delta_{\mathrm{sm}})(Y_t-\widehat f_0)u_t$ has conditional second moment at most $5d^2/\delta_{\mathrm{sm}}^2$. Smoothing and contraction cost $O(\delta_{\mathrm{sm}} T)$, and the online gradient term is $O(d\sqrt T/\delta_{\mathrm{sm}})$. Choose $\delta_{\mathrm{sm}}\asymp\sqrt d\,T^{-1/4}\le1/2$. Under $T\ge C_0d^2$, the initialization cost $O(\log T)$ and the failure-event contribution are absorbed. Each round uses one charged function value; the baseline is not obtained for free.

**Source location.** [1](https://arxiv.org/pdf/2406.06506v1) theorem: Theorem 2; stochastic algorithm analysis; pdf pages: 1; 2

The source assumes convex losses taking values in $[0,1]$ and conditionally sub-Gaussian noise. The unit ball is symmetric, giving $M=d^{-1/2}$ and upper bound $O(d^{3/2}\sqrt T\,\operatorname{polylog}(Td/\delta))$. Calibrate the unknown additive level through charged initialization before applying the theorem.

**Source location.** [3](https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf) theorem: Theorem 1; pdf pages: 4

Projected online gradient descent has dynamic regret at most $7D^2/(4\eta)+DP/\eta+\eta TL^2/2$, with its step size tuned using the public path budget.

### B2 - Online Newton stochastic algorithm on symmetric ball

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le C d^{3/2}\sqrt T\,\operatorname{polylog}(Td)
$$

**Sources.** [1](https://arxiv.org/pdf/2406.06506v1)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T including calibration

**native feedback.** T

**membership calls.** algorithm dependent; polynomial implementation available

**sampling calls.** initialization plus algorithm dependent

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** Suppress polylogarithmic factors in $T$, $d$, and $1/\delta_{\mathrm{conf}}$, with $\delta_{\mathrm{conf}}=1/(2T)$. The theorem overview does not specify a single logarithmic exponent.

**Derivation.** Use the same charged initialization to estimate $\widehat f_0$. On successful calibration, $h=(f-\widehat f_0+2)/4$ lies in $[0,1]$, and subsequent independent noise is $1/4$-sub-Gaussian after scaling. In the source Theorem 2 use symmetric-ball parameter $M=d^{-1/2}$ and failure probability $1/(2T)$, rescale regret by four, and add initialization and failure costs. Public ball geometry supports the required sampling and membership tests. Retain the source polylogarithmic order without claiming optimal runtime.

**Source location.** [1](https://arxiv.org/pdf/2406.06506v1) theorem: Theorem 2; stochastic algorithm analysis; pdf pages: 1; 2

The source assumes convex losses taking values in $[0,1]$ and conditionally sub-Gaussian noise. The unit ball is symmetric, giving $M=d^{-1/2}$ and upper bound $O(d^{3/2}\sqrt T\,\operatorname{polylog}(Td/\delta))$. Calibrate the unknown additive level through charged initialization before applying the theorem.

### B3 - Hidden-curvature Gaussian hard functions, latest v3

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge c\min\{\sqrt d\,T^{3/4},\ d^{4/3}\sqrt T\}
$$

**Sources.** [2](https://arxiv.org/pdf/2607.18652v3)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [2](https://arxiv.org/pdf/2607.18652v3) theorem: Theorem 1.2; pdf pages: 2; 3; 4

Use the lower bound in the cited source version. A fixed convex function on the unit ball has Lipschitz constant at most one, and evaluations receive independent standard Gaussian noise. Under $d\ge C$ and $T\ge Cd^2$, the lower bound is $c\min\{\sqrt d\,T^{3/4},d^{4/3}\sqrt T\}$.

## References

[1] Hidde Fokkema; Dirk van der Hoeven; Tor Lattimore; Jack J. Mayo. Online Newton Method for Bandit Convex Optimisation. 2024. arXiv:2406.06506v1, 2024-06-10.

https://arxiv.org/pdf/2406.06506v1

[2] Nived Rajaraman; Yanjun Han. The Price of Hidden Curvature: Improved Lower Bounds for Bandit Convex Optimization. 2026. 2607.18652v3.

https://arxiv.org/pdf/2607.18652v3

[3] Lijun Zhang; Shiyin Lu; Zhi-Hua Zhou. Adaptive Online Learning in Dynamic Environments. 2018. NeurIPS 2018 main paper.

https://www.lamda.nju.edu.cn/lusy/pdf/zhang2018adaptive.pdf
