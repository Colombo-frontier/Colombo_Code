# Combinatorial semi-bandits: summed coordinate loss and selected-coordinate feedback.

**Setting ID.** `ON_COMB_S`

Online learning and bandits

Each round, the learner selects an allowed combination, incurs the sum of its coordinate losses, and observes each selected coordinate separately. The upper bound holds for every admissible action set. The lower bound requires a specified hard action set and does not apply to singleton action sets.

**Status.** Fully optimal

**TASK tags.** formulation: Online combinatorial semibandit; solution concept: Minimize expected cumulative regret; task family: Online bandit

**MODEL tags.** stochastic model: Coordinate loss range; structure: Constant cardinality

**ORACLE tags.** feedback quality: Source-declared exact feedback (may be a random reward); interface family: Semi bandit; operation: Observe selected coordinates; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: External regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** measure: Convex projections; measure: Native feedback; measure: Observed coordinates; measure: Rounds

## 1. Setting specification

### Task

Each round, the learner selects an allowed combination, incurs the sum of its coordinate losses, and observes each selected coordinate separately. The upper bound holds for every admissible action set. The lower bound requires a specified hard action set and does not apply to singleton action sets.

### Admissible model

The public combinatorial action set $\mathcal{X}$ is nonempty, and every action activates m coordinates. The minimax quantity takes the worst case over public action sets; it does not assert equal hardness for every fixed combinatorial geometry.

The hidden coordinate-loss vector is $z_t$, with each coordinate in [0,1], so total action loss lies in [0,m].

The selected combinatorial action $a_t$ must belong to $\mathcal{X}$. The m selected coordinates are observed.

Require $d\ge1$, $1\le m\le d/2$, and $T\ge1$. Dimension and horizon windows with matching bounds are specified in their respective regions.

The per-round loss is a sum over coordinates, without division by $m$.

### Oracle interface

Semi-bandit feedback on the selected coordinates:

$$
t,\ a_t\in\mathcal{X}\ \longmapsto\ (z_{t,j})_{j:\ a_{t,j}=1}
$$

Exactly m coordinate values are returned, allowing total loss to be computed. Unselected coordinates remain hidden.

Every coordinate revealed in a round comes from the same loss vector $z_t$ and is feedback for one online action.

The action set $\mathcal X$ is public, but no additional unit-cost linear optimization oracle is assumed.

Public inputs are $d,T,m$ and nonempty action set $\mathcal X$. Every action activates exactly $m$ coordinates.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathcal{X}\subset\{a\in\{0,1\}^d:\|a\|_1=m\},\quad R_T=\sum_t\langle a_t,z_t\rangle-\min_{a\in\mathcal{X}}\sum_t\langle a,z_t\rangle
$$

### Resource accounting

One semi-bandit event per round supplies $m$ scalars: $T$ rounds and $mT$ observed coordinates in total.

The algorithm family may depend on public $\mathcal{X}$. Internal computation need not be polynomial time.

OSMD requires updates over conv($\mathcal{X}$) and randomized action selection. The feedback bound does not establish that these operations are computationally efficient for arbitrary $\mathcal{X}$.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\begin{aligned}[c]\mathcal{R}_T^*&=\inf_{\mathcal{A}(\cdot)}\sup_{\mathcal{X}\in\mathfrak X_{d,m}}\sup_{z_{1:T}\in([0,1]^d)^T}\mathbb{E}_{\mathcal{A}(\mathcal{X})}[R_T(\mathcal{X})],\\ R_T(\mathcal{X})&=\sum_{t=1}^T\langle a_t,z_t\rangle-\min_{a\in\mathcal{X}}\sum_{t=1}^T\langle a,z_t\rangle,\\ \mathfrak X_{d,m}&=\{\varnothing\ne\mathcal{X}\subset\{0,1\}^d:\ \|a\|_1=m\ \forall a\in\mathcal{X}\}.\end{aligned}
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: Total number of coordinates in a combinatorial action **Domain:** $d\in\mathbb N,\ d\ge1$.

Actions lie in $\{0,1\}^d$ and select exactly $m$ coordinates.

$m$: Number of active coordinates in each combinatorial action **Domain:** $m\in\mathbb N,\ 1\le m\le d/2$.

Every action $a\in\mathcal X$ satisfies $\|a\|_1=m$. A round's loss sums $m$ coordinate losses.

$\mathcal X$: The public nonempty combinatorial action set. **Domain:** $\mathcal X\subseteq\{a\in\{0,1\}^d:\|a\|_1=m\}$.

The learner knows X; the minimax worst case also ranges over admissible public action sets.

$a_t,a$: The current combinatorial action and fixed comparator action. **Domain:** $a_t,a\in\mathcal X$.

$z_t$: Hidden coordinate-loss vector **Domain:** $z_t\in[0,1]^d$.

The total round loss is $\langle a_t,z_t\rangle\in[0,m]$. Only activated coordinates are revealed.

$j$: Coordinate index **Domain:** $j\in[d]$.

$q$: Regularization exponent in the source OSMD theorem **Domain:** Used only to tune this algorithm.

The combined upper bound specializes to $q=2$. Here $q$ is neither a conjugate exponent nor a recommendation distribution.

$R_T$: Cumulative loss difference relative to the comparator specified in this profile **Domain:** Real-valued random variable.

$R_T=\sum_t\langle a_t,z_t\rangle-\min_{a\in\mathcal X}\sum_t\langle a,z_t\rangle$.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A(\cdot)}\sup_{\mathcal X\in\mathfrak X_{d,m}}\sup_{z_{1:T}\in([0,1]^d)^T}\mathbb E_{\mathcal A(\mathcal X)}[R_T(\mathcal X)],\\ R_T(\mathcal X)&=\sum_{t=1}^T\langle a_t,z_t\rangle-\min_{a\in\mathcal X}\sum_{t=1}^T\langle a,z_t\rangle,\\ \mathfrak X_{d,m}&=\{\varnothing\ne\mathcal X\subset\{0,1\}^d:\ \|a\|_1=m\ \forall a\in\mathcal X\}.\end{aligned}
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

There are T feedback events revealing mT active-coordinate losses. If N counts scalar coordinates, then $N=mT$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - cumulative regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A(\cdot)}\sup_{\mathcal X\in\mathfrak X_{d,m}}\sup_{z_{1:T}\in([0,1]^d)^T}\mathbb E_{\mathcal A(\mathcal X)}[R_T(\mathcal X)],\\ R_T(\mathcal X)&=\sum_{t=1}^T\langle a_t,z_t\rangle-\min_{a\in\mathcal X}\sum_{t=1}^T\langle a,z_t\rangle,\\ \mathfrak X_{d,m}&=\{\varnothing\ne\mathcal X\subset\{0,1\}^d:\ \|a\|_1=m\ \forall a\in\mathcal X\}.\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $d$ is a multiple of $m$, $d\ge2m$, and $T\ge d/m$.

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2

$$
c \sqrt{mdT}
$$

**Upper bound.** B1

$$
2\sqrt{2mdT}
$$

**Gap or comparison.** Universal constants.

**Comparison argument.** Only individually audited compatible claims enter. Worst-case over public A, not per-action-set exact complexity.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** The integer $d$ is a multiple of $m$; require $d\ge2m$ and $T\ge d/m$. Each round selects $m$ coordinates and returns their losses individually.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle mapping.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee mapping.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output mapping.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource mapping.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

### B1 - OSMD with q=2 regularizer

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{R}_T^*\le2\sqrt{2mdT}
$$

**Sources.** [1](https://arxiv.org/pdf/1204.4710v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T semi-bandit vectors

**observed coordinates.** mT

**convex projections.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/1204.4710v2) theorem: Theorem 4; pdf pages: 12

Each round selects $m$ of the $d$ coordinates, whose individual losses lie in $[0,1]$, and reveals semi-bandit feedback. OSMD gives $2\sqrt{2mdT}$ when $q=2$. The total loss per round ranges over $[0,m]$.

### B2 - Public A formed by choosing one arm in each of m groups of size d/m

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge c\sqrt{mdT}
$$

**Sources.** [1](https://arxiv.org/pdf/1204.4710v2) [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**observed coordinates.** mT

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Derivation.** Choose the public action set as a Cartesian product of $m$ groups, each containing $d/m$ coordinates. In each round choose one coordinate per group and observe all $m$ selected coordinate losses. Independent Bernoulli hard instances across groups give the direct-sum lower bound $mc\sqrt{(d/m)T}=c\sqrt{mdT}$. This is a worst-case public action set; a singleton action set has zero regret.

**Source location.** [1](https://arxiv.org/pdf/1204.4710v2) theorem: Section 3, lower-bound discussion; pdf pages: 11

On the public product action set, a direct sum of $m$ independent $d/m$-arm hard instances gives $\Omega(\sqrt{mdT})$. One observation per group corresponds exactly to the $m$ component responses in one round.

**Source location.** [2](https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf) theorem: Theorem 30 and proof; section: Appendix B; pdf pages: 28; 29; 30; printed pages: 2812; 2813; 2814

Use only the K-armed bandit branch with source sampling budget $m_{\mathrm{src}}=T$. In context-block reductions each block uses its own length. Bernoulli hard instances and Yao's principle give the randomized-learner lower bound.

## References

[1] Jean-Yves Audibert; Sébastien Bubeck; Gábor Lugosi. Regret in Online Combinatorial Optimization. 2014. 1204.4710v2.

https://arxiv.org/pdf/1204.4710v2

[2] Jean-Yves Audibert; Sébastien Bubeck. Regret Bounds and Minimax Policies under Partial Monitoring. 2010. JMLR 11:2785–2836.

https://jmlr.org/papers/volume11/audibert10a/audibert10a.pdf
