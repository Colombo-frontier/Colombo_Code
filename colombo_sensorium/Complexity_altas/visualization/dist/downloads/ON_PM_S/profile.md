# Finite partial monitoring: signal feedback and observability classes

**Setting ID.** `ON_PM_S`

Online learning and bandits

After acting, the learner receives only the feedback specified by a public signal matrix; the true loss may remain hidden. The objective is to compete with the best fixed action. Local and global observability must be determined jointly from the loss and signal matrices.

**Status.** Fully optimal

**TASK tags.** formulation: Finite partial monitoring; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** stochastic model: Bounded loss matrix; structure: Finite partial monitoring; structure: Public signal map

**ORACLE tags.** feedback quality: Source-declared exact feedback (may be a random reward); interface family: Partial monitoring signal; operation: Observe action outcome signal; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** measure: Native feedback; measure: Rounds

## 1. Setting specification

### Task

After acting, the learner receives only the feedback specified by a public signal matrix; the true loss may remain hidden. The objective is to compete with the best fixed action. Local and global observability must be determined jointly from the loss and signal matrices.

### Admissible model

Entries of the public loss matrix $L$ lie in $[0,1]$. Knowing the matrix does not reveal the current hidden outcome column $o_t$.

The public signal map $H$ takes arbitrary finite symbols; signals need not equal numerical losses.

The hidden outcome sequence $o_{1:T}$ is oblivious and fixed before interaction.

The public finite game is $G=(L,H)$. Let $C_i$ be the outcome-distribution region where action $i$ is optimal. Duplicate loss rows and degenerate actions with nonempty $C_i$ strictly contained in another $C_j$ are excluded. Local/global observability defines comparison branches rather than simultaneous model assumptions.

Fix the game $G$ satisfying $K,M\ge2$. Actions lie in $[K]$, outcomes in $[M]$, and signals in the finite range of the matrix $H$.

The game classification holds with only $T$ growing. It does not establish joint minimax optimality in $K,M$ and estimator constant $v$.

### Oracle interface

Action-outcome signal:

$$
t,\ a_t\in[K]\ \longmapsto\ Y_t=H(a_t,o_t)
$$

The environment outcome $o_t$ is already fixed but hidden when the learner chooses action $a_t$.

The learner incurs $L(a_t,o_t)$ and observes only the signal $H(a_t,o_t)$.

The outcome $o_t$ and incurred loss are hidden unless inferable from the signal and public matrices.

No signal from a second action in the same round is supplied.

Public inputs: $T$ and the complete fixed game $G=(L,H)$.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_tL(a_t,o_t)-\min_{a\in[K]}\sum_tL(a,o_t),\qquad Y_t=H(a_t,o_t)
$$

### Resource accounting

One signal is observed per round, for T signal events. No fictitious gradient or function-value charges are introduced.

All causal randomized strategies are allowed.

Public-game preprocessing, cell and observability calculations, and internal policy optimization have separate costs. An information-theoretic existence bound does not automatically give an efficient implementation.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
R_T^*(G)=\inf_{\mathcal{A}\,\mathrm{knowing}\,G}\sup_{o_{1:T}\in[M]^T}\mathbb{E}_{\mathcal{A}}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$G$: Public fixed finite partial-monitoring game **Domain:** Finite matrix-map pairs.

The game is $G=(L,H)$, where L is the loss matrix and H the signal map.

$K$: The number of actions available to the learner. **Domain:** $K\in\mathbb N,\ K\ge2$.

The action set is $[K]$.

$M$: Number of possible environment outcomes **Domain:** $M\in\mathbb N,\ M\ge2$.

Hidden outcome $o_t\in[M]$

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$v$: Minimum uniform-norm bound needed to represent neighboring-action loss differences **Domain:** $v\ge0$, finite on the corresponding observable branch.

For each neighboring action pair a,b choose $h_{ab}:[K]\times\Sigma_H\to\mathbb R$ so that $L(a,o)-L(b,o)=\sum_{c=1}^K h_{ab}(c,H(c,o))$ holds for every outcome o. The value v is the smallest number satisfying $\|h_{ab}\|_\infty\le v$ simultaneously. The locally observable branch restricts the construction to local actions.

$L$: Public loss matrix **Domain:** $L\in[0,1]^{K\times M}$.

$L(a,o)$ is the loss of action $a$ under the hidden outcome $o$.

$H,\Sigma_H$: Public signal map and its finite range **Domain:** $H:[K]\times[M]\to\Sigma_H$.

After choosing $a_t$, observe only $H(a_t,o_t)$.

$o_t,a_t$: The hidden outcome and actual action. **Domain:** $o_t\in[M],\ a_t\in[K]$.

The entire outcome sequence is fixed before interaction.

$\Delta_M$: The probability simplex of environment outcomes. **Domain:** $\Delta_M\subset\mathbb R^M$.

$\Delta_M=\{p\ge0:\sum_op_o=1\}$.

$C_a$: The region of outcome distributions for which action a is optimal. **Domain:** $C_a\subseteq\Delta_M$.

$C_a=\{p:\sum_oL(a,o)p_o\le\sum_oL(b,o)p_o\ \forall b\}$.

$a,b$: Adjacent optimal actions in the observability definition **Domain:** An action index.

Actions $a,b$ are adjacent if cells $C_a,C_b$ each have affine dimension $M-1$ and their intersection has dimension $M-2$.

$h_{ab}$: Signal function representing the loss difference between adjacent actions **Domain:** $h_{ab}:[K]\times\Sigma_H\to\mathbb R$.

Global observability requires $L(a,o)-L(b,o)=\sum_ch_{ab}(c,H(c,o))$. For a nondegenerate game, local observability uses only signals from the neighboring actions $a,b$.

$c(G)$: Positive constant in the fixed-game lower bound **Domain:** Positive real number in the nonzero-regret branch.

Constants may depend on the entire public fixed game G. No universal lower-bound constant uniform in K, M, or v is asserted.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_tL(a_t,o_t)-\min_{a\in[K]}\sum_tL(a,o_t)$.

$\mathcal R_T^*(G)$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*(G)&=\inf_{\mathcal A(G)}\sup_{o_{1:T}\in[M]^T}\mathbb E_{\mathcal A}[R_T(G)],\\ R_T(G)&=\sum_{t=1}^T L(a_t,o_t)-\min_{a\in[K]}\sum_{t=1}^T L(a,o_t),\\ G&=(L,H)\quad\text{fixed and public}.\end{aligned}
$$

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes the learner's private randomness and, when allowed, the environment strategy's randomness. A fixed loss sequence introduces no additional observation noise.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts observed signals; a signal need not be the numerical loss.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*(G)&=\inf_{\mathcal A(G)}\sup_{o_{1:T}\in[M]^T}\mathbb E_{\mathcal A}[R_T(G)],\\ R_T(G)&=\sum_{t=1}^T L(a_t,o_t)-\min_{a\in[K]}\sum_{t=1}^T L(a,o_t),\\ G&=(L,H)\quad\text{fixed and public}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - ZERO

**Region.** The game $G$ has no neighboring nondominated actions.

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
0
$$

**Upper bound.** B1

$$
0
$$

**Comparison argument.** Only individually audited compatible claims enter. A known uniformly dominant action can be used.

### R2 - LOCAL

**Region.** The game G has neighboring actions and is locally observable.

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B4

$$
c(G)sqrtT
$$

**Upper bound.** B3

$$
K^{3/2}(M+1)\sqrt{8T lnK}
$$

**Gap or comparison.** The powers of T agree for a fixed game.

**Comparison argument.** Only individually audited compatible claims enter. Nondegenerate local observability; K,M fixed.

### R3 - GLOBAL

**Region.** The game $G$ is globally observable but not locally observable.

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B6

$$
c(G)T^{2/3}
$$

**Upper bound.** B5

$$
3(TKv)^{2/3}(lnK/2)^{1/3}
$$

**Gap or comparison.** The powers of T agree for a fixed game.

**Comparison argument.** Only individually audited compatible claims enter. v is a public-game estimator norm; fixed G.

### R4 - HARD

**Region.** The game G is not globally observable.

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B8

$$
c(G)T
$$

**Upper bound.** B7

$$
T
$$

**Gap or comparison.** The powers of T agree for a fixed game.

**Comparison argument.** Only individually audited compatible claims enter. Trivial loss-range upper and indistinguishability lower.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - Dominant action / arbitrary action

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*(G)\le0
$$

**Sources.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf)

**Conditions.** The fixed nondegenerate finite game has no adjacent nondominated actions; use the zero-regret branch of the classification theorem.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Constants may depend on the public fixed game G; only horizon T is tracked here.

**Logarithmic factors.** None.

**Source location.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf) theorem: Theorems 9–12; pdf pages: 8; 9

This classifies a fixed game. The locally observable upper bound is $K^{3/2}(M+1)\sqrt{8T\log K}$ and globally observable upper bound $3(TKv)^{2/3}(\log K/2)^{1/3}$. Source game-dependent constants remain fixed.

### B2 - Nondegenerate-game classification hard outcome distributions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*(G)\ge0
$$

**Sources.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf)

**Conditions.** The fixed nondegenerate finite game has no adjacent nondominated actions; use the zero-regret branch of the classification theorem.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Each fixed game in a nonzero branch has its own positive lower-bound constant c(G). No positive constant uniform over all games is asserted.

**Logarithmic factors.** None.

**Source location.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf) theorem: Classification for games against adversarial opponents (unnumbered); pdf pages: 8

Nondegenerate finite games fall into four regret-rate classes according to their information structure: zero, $\sqrt T$, $T^{2/3}$, and $T$. The lower-bound constructions cover randomized policies. Asymptotics hold for each fixed game, with constants that may depend on the game.

### B3 - Classification-achieving partial-monitoring strategy

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*(G)\le K^{3/2}(M+1)\sqrt{8T\log K}
$$

**Sources.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf)

**Conditions.** A fixed nondegenerate finite game has adjacent nondominated actions and is locally observable. Lower-bound constants may depend on that fixed game.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Constants may depend on the public fixed game G; only horizon T is tracked here.

**Logarithmic factors.** None.

**Source location.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf) theorem: Theorems 9–12; pdf pages: 8; 9

This classifies a fixed game. The locally observable upper bound is $K^{3/2}(M+1)\sqrt{8T\log K}$ and globally observable upper bound $3(TKv)^{2/3}(\log K/2)^{1/3}$. Source game-dependent constants remain fixed.

### B4 - Nondegenerate-game classification hard outcome distributions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*(G)\ge c(G)\sqrt T
$$

**Sources.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf)

**Conditions.** A fixed nondegenerate finite game has adjacent nondominated actions and is locally observable. Lower-bound constants may depend on that fixed game.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Each fixed game in a nonzero branch has its own positive lower-bound constant c(G). No positive constant uniform over all games is asserted.

**Logarithmic factors.** None.

**Source location.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf) theorem: Classification for games against adversarial opponents (unnumbered); pdf pages: 8

Nondegenerate finite games fall into four regret-rate classes according to their information structure: zero, $\sqrt T$, $T^{2/3}$, and $T$. The lower-bound constructions cover randomized policies. Asymptotics hold for each fixed game, with constants that may depend on the game.

### B5 - Classification-achieving partial-monitoring strategy

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*(G)\le3(TKv)^{2/3}\left(\frac{\log K}{2}\right)^{1/3}
$$

**Sources.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf)

**Conditions.** A fixed nondegenerate finite game is globally observable but not locally observable. Lower-bound constants may depend on the fixed game.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Constants may depend on the public fixed game G; only horizon T is tracked here.

**Logarithmic factors.** None.

**Source location.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf) theorem: Theorems 9–12; pdf pages: 8; 9

This classifies a fixed game. The locally observable upper bound is $K^{3/2}(M+1)\sqrt{8T\log K}$ and globally observable upper bound $3(TKv)^{2/3}(\log K/2)^{1/3}$. Source game-dependent constants remain fixed.

### B6 - Nondegenerate-game classification hard outcome distributions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*(G)\ge c(G)T^{2/3}
$$

**Sources.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf)

**Conditions.** A fixed nondegenerate finite game is globally observable but not locally observable. Lower-bound constants may depend on the fixed game.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Each fixed game in a nonzero branch has its own positive lower-bound constant c(G). No positive constant uniform over all games is asserted.

**Logarithmic factors.** None.

**Source location.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf) theorem: Classification for games against adversarial opponents (unnumbered); pdf pages: 8

Nondegenerate finite games fall into four regret-rate classes according to their information structure: zero, $\sqrt T$, $T^{2/3}$, and $T$. The lower-bound constructions cover randomized policies. Asymptotics hold for each fixed game, with constants that may depend on the game.

### B7 - Dominant action / arbitrary action

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*(G)\le T
$$

**Sources.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf)

**Conditions.** The fixed nondegenerate finite game is not globally observable and belongs to the linear-regret branch.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Constants may depend on the public fixed game G; only horizon T is tracked here.

**Logarithmic factors.** None.

**Source location.** [2](https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf) theorem: Theorems 9–12; pdf pages: 8; 9

This classifies a fixed game. The locally observable upper bound is $K^{3/2}(M+1)\sqrt{8T\log K}$ and globally observable upper bound $3(TKv)^{2/3}(\log K/2)^{1/3}$. Source game-dependent constants remain fixed.

### B8 - Nondegenerate-game classification hard outcome distributions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*(G)\ge c(G)T
$$

**Sources.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf)

**Conditions.** The fixed nondegenerate finite game is not globally observable and belongs to the linear-regret branch.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Each fixed game in a nonzero branch has its own positive lower-bound constant c(G). No positive constant uniform over all games is asserted.

**Logarithmic factors.** None.

**Source location.** [1](https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf) theorem: Classification for games against adversarial opponents (unnumbered); pdf pages: 8

Nondegenerate finite games fall into four regret-rate classes according to their information structure: zero, $\sqrt T$, $T^{2/3}$, and $T$. The lower-bound constructions cover randomized policies. Asymptotics hold for each fixed game, with constants that may depend on the game.

## References

[1] Gábor Bartók; Dean P. Foster; Dávid Pál; Alexander Rakhlin; Csaba Szepesvári. Partial Monitoring—Classification, Regret Bounds, and Algorithms. 2014. author PDF dated 2014-05-16; MOR 39(4):967–997.

https://sites.ualberta.ca/~szepesva/papers/partial_monitoring-mor.pdf

[2] Tor Lattimore; Csaba Szepesvári. An Information-Theoretic Approach to Minimax Regret in Partial Monitoring. 2019. COLT / PMLR 99:2111–2139.

https://proceedings.mlr.press/v99/lattimore19a/lattimore19a.pdf
