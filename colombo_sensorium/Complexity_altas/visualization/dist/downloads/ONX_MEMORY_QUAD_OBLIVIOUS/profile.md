# Quadratic bandits with memory and an obliviously fixed loss sequence

**Setting ID.** `ONX_MEMORY_QUAD_OBLIVIOUS`

Online learning and bandits

The current scalar quadratic loss depends on a window of recent actions, and the learner observes only its value on that window. The comparator uses the same fixed action throughout every window. The complete loss sequence is fixed before interaction.

**Status.** Bounds missing

**TASK tags.** formulation: Onx memory quad oblivious; task family: Online bandit

**MODEL tags.** convexity: Convex quadratic memory

**ORACLE tags.** interface family: Memory window value; operation: Memory window value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Policy regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

The current scalar quadratic loss depends on a window of recent actions, and the learner observes only its value on that window. The comparator uses the same fixed action throughout every window. The complete loss sequence is fixed before interaction.

### Admissible model

The action in each round is $x_t\in[0,1]$, with fixed initial history $x_{1-m:0}=0$. The memory length $m\ge2$ includes the current action. A window consisting of the previous two actions and the current action therefore has $m=3$.

$$f_t:[0,1]^m\to\mathbb R\ \text{is convex quadratic},\qquad |f_t(z)|\le B,\qquad \|\nabla f_t(z)\|_2\le L\quad(\forall z\in[0,1]^m).$$

All $f_{1:T}$ are fixed before the learner's private randomness is generated; loss coefficients do not depend on earlier realized actions.

### Oracle interface

The algorithm chooses $x_t$ using past scalar feedback and then observes the realized memory loss $f_t(x_{t-m+1:t})$. No gradient is returned.

There is no additional measurement noise beyond the randomness of the environment and algorithm.

Causal randomized policies must always act in $[0,1]$. The data $T,m,B,L$ and initial history are public; quadratic coefficients are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathbb{E}\!\left[\sum_{t=1}^{T}f_t(x_{t-m+1:t})-\min_{u\in[0,1]}\sum_{t=1}^{T}f_t(u,\ldots,u)\right].
$$

### Resource accounting

The learner's actions before round $1$ are zero. The displayed constant-$u$ comparator uses $u$ before round $1$. Requiring shared zero prehistory changes only the first $m-1$ terms; the benchmarks differ by at most $2B(m-1)$. Retain this finite-horizon distinction.

One scalar response per round, with $N=T$.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Take the infimum over causal algorithms and supremum over admissible loss rules, averaging over randomness. Fixed loss functions are replayed within constant-length windows; the comparator uses the explicitly stated history convention.

## 2. Notation and parameters

$B$: Absolute loss bound over all memory windows **Domain:** $B>0$.

For every $z\in[0,1]^m$, $|f_t(z)|\le B$.

$L$: Euclidean gradient bound over the complete memory-window variable **Domain:** $L>0$.

The expression is $\|\nabla f_t(z)\|_2\le L$, with the gradient taken with respect to all m window coordinates.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$m$: Total memory-window length, including the current action **Domain:** $m\in\mathbb N,\ m\ge2$.

The round-$t$ loss depends on $x_{t-m+1},\ldots,x_t$. Memory $m=3$ means the previous two actions and the current action.

$x_t$: The actual current action. **Domain:** $x_t\in[0,1]$.

The initial history is $x_{1-m:0}=0$.

$x_{t-m+1:t}$: Window of actual actions used to evaluate the current loss **Domain:** $x_{t-m+1:t}\in[0,1]^m$.

Includes the current action and the preceding $m-1$ actions.

$f_t$: Convex quadratic loss on the complete window variable **Domain:** $f_t:[0,1]^m\to\mathbb R$.

All coefficients are fixed before interaction.

$u$: Comparator constant across the memory window **Domain:** $u\in[0,1]$.

The comparator replaces every window coordinate by u at each time while leaving the original loss function unchanged.

$R_T^{\mathrm{mem}}$: Regret against constant-window comparators for losses with memory **Domain:** Real-valued random variable.

$$
\sum_{t=1}^Tf_t(x_{t-m+1:t})-\min_{u\in[0,1]}\sum_{t=1}^Tf_t(u,\ldots,u)
$$. The delayed-adaptation variant does not rerun the environmental history that generated the losses.

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

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
\mathbb E\!\left[\sum_{t=1}^{T}f_t(x_{t-m+1:t})-\min_{u\in[0,1]}\sum_{t=1}^{T}f_t(u,\ldots,u)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** The loss sequence is obliviously fixed; a lower bound using a delayed adaptive adversary does not apply.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Both bounds missing

**Lower bound.** Admitted envelope

**Upper bound.** Admitted envelope

## 4. Bounds and supporting evidence

## References

[1] Arun Suggala; Y. Jennifer Sun; Praneeth Netrapalli; Elad Hazan. Second Order Methods for Bandit Optimization and Control. 2024. COLT 2024, PMLR 247.

https://proceedings.mlr.press/v247/suggala24a/suggala24a.pdf
