# Unknown linear control with disturbance-response comparators and Markov variation

**Setting ID.** `ONX_CONTROL_UNKNOWN_DRC_VARIATION`

Online learning and bandits

Counterfactual expected regret with full state and cost feedback, bounded natural trajectories, and instancewise squared Markov-variation budgets.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Online control regret; task family: Online bandit

**ORACLE tags.** feedback quality: Exact; operation: Current cost function; operation: Full state observation; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** quantifier: Algorithm before instance

**RESOURCE tags.** measure: T

## 1. Setting specification

### Task

Minimize expected counterfactual regret for an unknown linear system against bounded finite-memory disturbance-response controllers.

### Admissible model

The deterministic instance $(A_t,B_t,w_t,c_t)_{t=1}^T$ is fixed before the controller seed. The state obeys $x_{t+1}=A_tx_t+B_tu_t+w_t$, $x_1=0$, with $x_t\in\mathbb R^{d_x}$ and unrestricted $u_t\in\mathbb R^{d_u}$. The natural trajectory has zero input: $x_1^{\mathrm{nat}}=0$, $x_{t+1}^{\mathrm{nat}}=A_tx_t^{\mathrm{nat}}+w_t$.

Let $G_t^{[i]}=A_t\cdots A_{t-i+1}B_{t-i}$ for $0\le i<t$, with $G_t^{[0]}=B_t$ and zero padding for $i\ge t$. The public regularity budgets satisfy $\|x_t^{\mathrm{nat}}\|\le R_{\mathrm{nat}}$ and $\sum_{i\ge\ell}\|G_t^{[i]}\|_{\mathrm{op}}\le R_G\rho^\ell$ for every $\ell\ge0$, where $0<\rho<1$.

Each cost is convex and nonnegative on the full state–input space, obeys $c_t(x,u)\le L\max\{1,\|x\|^2+\|u\|^2\}$, and every subgradient obeys $\|g\|\le L\max\{1,\|x\|+\|u\|\}$. Nonsmooth costs and quadratic growth are allowed.

The instancewise variation budget is $V_{[T]}=T^{-1}\inf_G\sum_{t=1}^T\|G-G_t\|_{\ell_2,F}^2\le v$, with $\|G\|_{\ell_2,F}^2=\sum_{i\ge0}\|G^{[i]}\|_F^2$. This is squared deviation from a constant Markov operator, not successive-difference variation.

### Oracle interface

Observe the full state x_t, choose u_t, incur c_t(x_t,u_t), and then observe the next state and the entire current cost function. The actual dynamics and disturbances are hidden. Public information consists of the horizon, dimensions, regularity and comparator budgets. Internal computation and input magnitudes are unrestricted. The model does not supply a strong-controllability promise or a known stabilizing state-feedback matrix.

### Output

The output is the actual causal control trajectory. Each comparator must be evaluated on its own counterfactual trajectory under the same matrices and disturbances.

### Loss or accuracy criterion

The comparator parameters satisfy $\mathcal M_m(R_M)=\{(M^{[0]},\ldots,M^{[m-1]}):\sum_{i=0}^{m-1}\|M^{[i]}\|_{\mathrm{op}}\le R_M\}$ and use $u_t^M=\sum_{i=0}^{m-1}M^{[i]}x_{t-i}^{\mathrm{nat}}$, with prehistory zero. Regret is $\operatorname{Reg}_T(A;I)=\mathbb E_A\sum_t c_t(x_t,u_t)-\inf_{M\in\mathcal M_m(R_M)}\sum_t c_t(x_t^M,u_t^M)$.

### Resource accounting

The fixed horizon T counts control transitions and full state/cost feedback. Every probing and identification input incurs its actual cost. There is no uncharged system-identification phase and no input-norm restriction.

### Algorithm views and success guarantees

All measurable randomized causal controllers with arbitrary real-valued inputs are allowed. They may use the public parameter budgets, but do not receive the realized disturbances or the unknown dynamics.

$$
\sup_{I:V_{[T]}\le v}\operatorname{Reg}_T(A;I)\le r
$$

The fixed instance precedes controller randomization. The variation budget is satisfied by every instance, not merely on average under a hard prior.

**Budget convention.** fixed_horizon

## 2. Notation and parameters

$d_x$: State dimension **Domain:** $d_x\ge1$ integer.

$d_u$: Input dimension **Domain:** $d_u\ge1$ integer.

$T$: Horizon **Domain:** $T\ge2$ integer.

$m$: Comparator memory **Domain:** $m\ge1$ integer.

$R_{\mathrm{nat}}$: Natural-trajectory norm budget **Domain:** $R_{\mathrm{nat}}>0$.

$R_G$: Markov-tail budget **Domain:** $R_G>0$.

$\rho$: Markov-tail geometric decay factor **Domain:** $0<\rho<1$.

$R_M$: Sum of comparator matrix norms **Domain:** $R_M>0$.

$L$: Cost and subgradient growth budget **Domain:** $L>0$.

$v$: Instancewise normalized squared Markov-variation budget **Domain:** $v\ge0$.

$\mathfrak p$: Ordered structural parameter tuple **Domain:** Public tuple.

$\mathfrak p=(d_x,d_u,R_{\mathrm{nat}},R_G,\rho,R_M,L)$

$c_m$: Fixed coefficient allowed in logarithmic comparator memory **Domain:** $c_m>0$.

$m\le c_m\log(2T)$ in logarithmic-memory regimes

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathcal C_{T,m}(v;\mathfrak p)=\inf_A\sup_{I\in\mathfrak I_T(v;\mathfrak p)}\operatorname{Reg}_T(A;I)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

### R1 - Zero Markov variation in two states and one input

**Region.** $\mathfrak p=(2,1,2,2,1/2,1,8)$, $v=0$; m is fixed or $1\le m\le c_m\log(2T)$ for fixed c_m; T is sufficiently large and $m\le\sqrt T$. Exactly d_x=2 and d_u=1; no dimension-growing lower-bound requirement. The hard instance already has constant A,B and a comparator of memory one. The theorem does not require strong controllability.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(T^{2/3}/\log(2T))
$$

**Upper bound.** B1

$$
\widetilde O(T^{2/3})
$$

**Gap or comparison.** Only polynomial factors in log(2T) remain.

### R2 - Whole-horizon variation profile below saturation

**Region.** $\mathfrak p=(3,3,4,2,1/2,1,8)$, $0\le v\le1/64$; m is fixed or $1\le m\le c_m\log(2T)$ for fixed c_m; T is sufficiently large and $m\le\sqrt T$. Exactly d_x=d_u=3. The two sublinear contributions cross at $v=T^{-2/3}$ up to logarithmic factors. The statement concerns whole-horizon regret, not optimal regret on every subinterval simultaneously.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega(T^{2/3}/\log(2T)+T\sqrt v)
$$

**Upper bound.** B3

$$
\widetilde O(T^{2/3}+T\sqrt v)
$$

**Gap or comparison.** Only horizon logarithms remain, uniformly over the displayed v interval.

### R3 - Linear saturation for larger variation

**Region.** $\mathfrak p=(3,3,4,2,1/2,1,8)$, $v\ge1/64$; m is fixed or at most logarithmic in T as above; T is sufficiently large. Exactly d_x=d_u=3.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega(T)
$$

**Upper bound.** B5

$$
128T
$$

**Gap or comparison.** Constant-factor matching.

## 4. Bounds and supporting evidence

### B1 - The full-information unknown-system controller imported in the manuscript from Minasyan–Gradu–Simchowitz–Hazan Theorem 3.4, specialized to zero variation.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(T^{2/3})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf)

**Conditions.** $\mathfrak p=(2,1,2,2,1/2,1,8)$, $v=0$; m is fixed or $1\le m\le c_m\log(2T)$ for fixed c_m; T is sufficiently large and $m\le\sqrt T$.; The hard instance already has constant A,B and a comparator of memory one. The theorem does not require strong controllability.

**Dimension conditions.** Exactly d_x=2 and d_u=1; no dimension-growing lower-bound requirement.

**Constants.** The displayed structural tuple is fixed; logarithmic-memory constants may depend on c_m.

**Logarithmic factors.** Source tilde-O hides finite powers of log(2T); fixed or logarithmic comparator memory is included in these factors.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf) Corollary cor:matching; equations eq:matching and eq:importedupper

The full-information unknown-system controller imported in the manuscript from Minasyan–Gradu–Simchowitz–Hazan Theorem 3.4, specialized to zero variation.. Randomized causal controllers with full state and cost-function feedback.

### B2 - A=0 with one hidden entry of B, bounded multiscale disturbances, and a convex movement cost.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega(T^{2/3}/\log(2T))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf)

**Conditions.** $\mathfrak p=(2,1,2,2,1/2,1,8)$, $v=0$; m is fixed or $1\le m\le c_m\log(2T)$ for fixed c_m; T is sufficiently large and $m\le\sqrt T$.; The hard instance already has constant A,B and a comparator of memory one. The theorem does not require strong controllability.

**Dimension conditions.** Exactly d_x=2 and d_u=1; no dimension-growing lower-bound requirement.

**Constants.** The displayed structural tuple is fixed; logarithmic-memory constants may depend on c_m.

**Logarithmic factors.** Source tilde-O hides finite powers of log(2T); fixed or logarithmic comparator memory is included in these factors.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf) Theorem thm:main; Corollary cor:matching

A=0 with one hidden entry of B, bounded multiscale disturbances, and a convex movement cost.. Every randomized causal controller, including unbounded probing inputs.

### B3 - Unknown-system control with the source full-information variation guarantee.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(T^{2/3}+T\sqrt v)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf)

**Conditions.** $\mathfrak p=(3,3,4,2,1/2,1,8)$, $0\le v\le1/64$; m is fixed or $1\le m\le c_m\log(2T)$ for fixed c_m; T is sufficiently large and $m\le\sqrt T$.; The two sublinear contributions cross at $v=T^{-2/3}$ up to logarithmic factors. The statement concerns whole-horizon regret, not optimal regret on every subinterval simultaneously.

**Dimension conditions.** Exactly d_x=d_u=3.

**Constants.** Uniform in v; the structural tuple and comparator-memory coefficient are fixed.

**Logarithmic factors.** Only finite powers of log(2T).

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf) Corollary cor:variation; equation eq:varmatch and proof using eq:importedupper

Unknown-system control with the source full-information variation guarantee.. Causal randomized controllers with the declared regularity budgets.

### B4 - Combination of the stationary hidden-coefficient obstruction and an instancewise-budget variation construction.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega(T^{2/3}/\log(2T)+T\sqrt v)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf)

**Conditions.** $\mathfrak p=(3,3,4,2,1/2,1,8)$, $0\le v\le1/64$; m is fixed or $1\le m\le c_m\log(2T)$ for fixed c_m; T is sufficiently large and $m\le\sqrt T$.; The two sublinear contributions cross at $v=T^{-2/3}$ up to logarithmic factors. The statement concerns whole-horizon regret, not optimal regret on every subinterval simultaneously.

**Dimension conditions.** Exactly d_x=d_u=3.

**Constants.** Uniform in v; the structural tuple and comparator-memory coefficient are fixed.

**Logarithmic factors.** Only finite powers of log(2T).

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf) Corollary cor:variation; equations eq:varbaseline, eq:varsecond and its combined lower bound

Combination of the stationary hidden-coefficient obstruction and an instancewise-budget variation construction.. Every randomized causal controller.

### B5 - The zero-input controller follows the bounded natural trajectory.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
128T
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf)

**Conditions.** $\mathfrak p=(3,3,4,2,1/2,1,8)$, $v\ge1/64$; m is fixed or at most logarithmic in T as above; T is sufficiently large.

**Dimension conditions.** Exactly d_x=d_u=3.

**Constants.** Universal for the displayed fixed tuple.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf) Corollary cor:variation; equations eq:saturation and proof

The zero-input controller follows the bounded natural trajectory.. Deterministic controller.

### B6 - Variation construction at sigma=1/8.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega(T)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf)

**Conditions.** $\mathfrak p=(3,3,4,2,1/2,1,8)$, $v\ge1/64$; m is fixed or at most logarithmic in T as above; T is sufficiently large.

**Dimension conditions.** Exactly d_x=d_u=3.

**Constants.** Universal for the displayed fixed tuple.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf) Corollary cor:variation; equation eq:saturation

Variation construction at sigma=1/8.. Every randomized causal controller.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_Q6. A Near-Optimal Regret Lower Bound for Unknown Nonstochastic Linear Control. Q6_matching_bounds_proof.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/Q6/manuscript.pdf
