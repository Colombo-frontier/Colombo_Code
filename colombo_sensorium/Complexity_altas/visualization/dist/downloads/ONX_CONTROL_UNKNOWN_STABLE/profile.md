# Unknown linear nonstochastic control: known stabilizer and strong controllability.

**Setting ID.** `ONX_CONTROL_UNKNOWN_STABLE`

Online learning and bandits

The controller observes the full state and chooses an input for an unknown linear system driven by bounded disturbances. A stabilizing feedback matrix is known, and strong controllability is assumed. Performance is compared with the counterfactual trajectory of the best fixed stabilizing linear controller under the same disturbances. Interactions used for system identification are charged to the budget.

**Status.** Bounds missing

**TASK tags.** formulation: Onx control unknown stable; task family: Online bandit

**MODEL tags.** structure: Unknown stable dynamics

**ORACLE tags.** interface family: State and full cost; operation: State and full cost; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Counterfactual control regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

The controller observes the full state and chooses an input for an unknown linear system driven by bounded disturbances. A stabilizing feedback matrix is known, and strong controllability is assumed. Performance is compared with the counterfactual trajectory of the best fixed stabilizing linear controller under the same disturbances. Interactions used for system identification are charged to the budget.

### Admissible model

$$
x_{t+1}=Ax_t+Bu_t+w_t,\qquad x_t\in\mathbb{R}^{d_x},\quad u_t\in\mathbb{R}^{d_u},\quad x_0=0.
$$

The quantity $A,B$ is fixed and unknown. The disturbance sequence is fixed before interaction and satisfies $\|w_t\|_2\le W$; disturbances need not be independent random noise.

Cost functions $c_t(x,u)$ are fixed in advance, differentiable, and convex. For every radius $D\ge1$, $\|x\|_2,\|u\|_2\le D$ implies $\|\nabla c_t(x,u)\|_2\le GD$. The known stabilizer $K_0$ admits the following closed-loop decomposition:

$$
A-BK_0=QLQ^{-1},\qquad \|L\|_2\le1-\gamma,\qquad 0<\gamma\le1,
$$

$$
\max\{\|A\|_2,\|B\|_2,\|K_0\|_2,\|Q\|_2,\|Q^{-1}\|_2\}\le C_{\mathrm{stab}}.
$$

Closed-loop strong controllability additionally requires the following matrix to have full row rank and satisfy:

$$
C_k=[B,(A-BK_0)B,\ldots,(A-BK_0)^{k_{\mathrm{ctrl}}-1}B],\qquad \|(C_kC_k^{\mathsf T})^{-1}\|_2\le C_{\mathrm{ctrl}}.
$$

Control times are consistently indexed by $t=0,\ldots,T-1$, giving T control actions and matching the initial state $x_0=0$.

### Oracle interface

Observe the complete state $x_t$, choose $u_t$, and incur $c_t(x_t,u_t)$; then receive the complete current cost function and next state.

Neither $A,B$ nor the disturbances themselves are supplied directly. Any causal controller is allowed; algorithms are not restricted to a particular linear feedback form.

The information $d_x,d_u,T,G,W,K_0,\gamma,C_{\mathrm{stab}},C_{\mathrm{ctrl}},k_{\mathrm{ctrl}},\delta_{\mathrm{conf}}$ is public.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

Sequentially output control inputs $u_t\in\mathbb{R}^{d_u}$ and evaluate the actual system trajectory. Each comparator controller induces its own counterfactual states; learner states cannot be substituted for them.

### Loss or accuracy criterion

$$
\begin{gathered}K\in\mathcal{K}\ \Longleftrightarrow\ \exists Q_K,L_K:\ A-BK=Q_KL_KQ_K^{-1},\\ \|L_K\|_2\le1-\gamma,\qquad \max\{\|A\|_2,\|B\|_2,\|K\|_2,\|Q_K\|_2,\|Q_K^{-1}\|_2\}\le C_{\mathrm{stab}}.\end{gathered}
$$

$$
R_T=\sum_{t=0}^{T-1}c_t(x_t,u_t)-\min_{K\in\mathcal K}\sum_{t=0}^{T-1}c_t(x_t^K,-Kx_t^K),\qquad x_{t+1}^K=(A-BK)x_t^K+w_t,\ x_0^K=0.
$$

### Resource accounting

There are $T$ control steps and $N=T$ transition/cost observations. Initial system identification consumes part of this horizon and incurs cost. The source exploration length is $T_0$, of order $T^{2/3}\log(1/\delta_{\mathrm{conf}})$, and must fit within the horizon.

The stability upper bound $C_{\mathrm{stab}}$ retains its source meaning. It is not denoted by $\kappa$, which is reserved here for condition numbers.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The comparator class $\mathcal{K}$ consists of fixed linear controllers $u_t=-Kx_t$ satisfying the same $C_{\mathrm{stab}},\gamma$ strong-stability bound. A comparator uses the same initial state and fixed disturbance sequence, but generates its own state trajectory $x_t^K$.

All sums run over $T$ control times. The guarantee holds with probability at least $1-\delta_{\mathrm{conf}}$ over the learner's exploration randomness. The comparator's counterfactual state trajectory cannot be replaced by the learner's actual trajectory.

## 2. Notation and parameters

$G$: The growth coefficient for cost gradients in the state and control radius. **Domain:** $G>0$.

For every $D\ge1$, the condition $\|x\|_2,\|u\|_2\le D$ implies $\|\nabla c_t(x,u)\|_2\le GD$.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$\delta_{\mathrm{conf}}$: The allowed statistical failure probability. **Domain:** $0<\delta_{\mathrm{conf}}<1$.

Used only for statistical correctness or high-probability performance, and distinct from the privacy relaxation parameter.

$d_x$: State-space dimension **Domain:** $d_x\in\mathbb N,\ d_x\ge1$.

$x_t,w_t\in\mathbb R^{d_x}$.

$d_u$: Control-input dimension **Domain:** $d_u\in\mathbb N,\ d_u\ge1$.

$u_t\in\mathbb R^{d_u}$.

$W$: Euclidean norm bound on the fixed disturbance sequence **Domain:** $W\ge0$.

$\|w_t\|_2\le W$. Independent random noise is not required.

$K_0$: Public initial stable feedback matrix **Domain:** $K_0\in\mathbb R^{d_u\times d_x}$.

The closed loop under $u_t=-K_0x_t$ satisfies the declared strong-stability condition.

$\gamma$: Stability margin in the closed-loop contraction **Domain:** $0<\gamma\le1$.

The quantity is $\|L\|_2\le1-\gamma$, where $A-BK_0=QLQ^{-1}$.

$C_{\mathrm{stab}}$: Matrix-norm bound in the strong-stability condition **Domain:** $C_{\mathrm{stab}}>0$.

The bound $\|A\|_2,\|B\|_2,\|K_0\|_2,\|Q\|_2,\|Q^{-1}\|_2$ applies simultaneously; the comparator obeys the same bound.

$k_{\mathrm{ctrl}}$: The block count of the closed-loop controllability matrix. **Domain:** $k_{\mathrm{ctrl}}\in\mathbb N,\ k_{\mathrm{ctrl}}\ge1$.

$C_k=[B,(A-BK_0)B,\ldots,(A-BK_0)^{k_{\mathrm{ctrl}}-1}B]$.

$C_{\mathrm{ctrl}}$: A bound on the norm of the inverse controllability Gram matrix. **Domain:** $C_{\mathrm{ctrl}}>0$.

The matrix $C_k$ has full row rank and satisfies $\|(C_kC_k^{\mathsf T})^{-1}\|_2\le C_{\mathrm{ctrl}}$.

$A,B$: The fixed unknown state-transition and control-input matrices. **Domain:** $A\in\mathbb R^{d_x\times d_x},\ B\in\mathbb R^{d_x\times d_u}$.

Environment dynamics are $x_{t+1}=Ax_t+Bu_t+w_t$.

$x_t,u_t,w_t$: Actual states, actual controls, and an obliviously fixed disturbance sequence **Domain:** Real vector of the corresponding dimension.

$x_0=0$, with control times $t=0,\ldots,T-1$.

$Q,L$: The similarity-transform and contraction matrices in the known stabilizer’s closed-loop decomposition. **Domain:** The condition $Q,L\in\mathbb R^{d_x\times d_x}$ holds, and Q is invertible.

The quantities $A-BK_0=QLQ^{-1}$ are existence witnesses in the strong-stability promise and are not directly supplied to the learner.

$C_k$: Closed-loop controllability matrix **Domain:** $C_k\in\mathbb R^{d_x\times(k_{\mathrm{ctrl}}d_u)}$.

Construct the matrix by concatenating the columns $B,(A-BK_0)B,\ldots,(A-BK_0)^{k_{\mathrm{ctrl}}-1}B$.

$\mathcal K,K$: Permitted fixed feedback-comparator class and its elements **Domain:** $K\in\mathbb R^{d_u\times d_x}$.

Every K satisfies the same $C_{\mathrm{stab}},\gamma$ strong-stability condition. Here K denotes a controller, not an arm count or a restriction on the learner's strategy class.

$Q_K,L_K$: Witness of the closed-loop decomposition for comparator $K$ **Domain:** The matrix $Q_K$ is square and invertible.

Require $A-BK=Q_KL_KQ_K^{-1}$ and the contraction and norm bounds of the comparator class.

$x_t^K$: Counterfactual state generated using the fixed comparator $K$ **Domain:** $x_t^K\in\mathbb R^{d_x}$.

Assume $x_0^K=0$ and $x_{t+1}^K=(A-BK)x_t^K+w_t$, using the same disturbance sequence as the learner.

$c_t,D$: The current cost function and test radius in its gradient-growth condition. **Domain:** Convex real-valued function and arbitrary real $D\ge1$.

D is a universally quantified test radius, not an additional fixed model parameter.

$T_0$: The length of the initial system-identification phase. **Domain:** $0\le T_0\le T$.

These steps consume the horizon T and incur cost. The source algorithm’s exploration length must be feasible.

$R_T$: Cumulative control regret relative to a separately defined counterfactual state trajectory **Domain:** Real-valued random variable.

$R_T=\sum_{t=0}^{T-1}c_t(x_t,u_t)-\min_{K\in\mathcal K}\sum_{t=0}^{T-1}c_t(x_t^K,-Kx_t^K)$.

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{0,\ldots,T-1\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes the learner's private randomness and, when allowed, the environment strategy's randomness. A fixed loss sequence introduces no additional observation noise.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The resource $N=T$ counts control transitions and current-cost feedback events, including system identification.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
R_T=\sum_{t=0}^{T-1}c_t(x_t,u_t)-\min_{K\in\mathcal K}\sum_{t=0}^{T-1}c_t(x_t^K,-Kx_t^K),\qquad x_{t+1}^K=(A-BK)x_t^K+w_t,\ x_0^K=0.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Stability and controllability promises hold, and the source exploration length fits within T. All polynomial parameters are retained.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
O\!\left(\operatorname{poly}\!\left(C_{\mathrm{stab}},C_{\mathrm{ctrl}},\gamma^{-1},k_{\mathrm{ctrl}},d_x,d_u,W,G\right)T^{2/3}\log\!\frac1{\delta_{\mathrm{conf}}}\right)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Require source Assumptions 3, 4, 6, and 8, namely the stated boundedness, stability, and strong-controllability conditions. The exploration length must fit within the horizon, and complete state and cost feedback are used.; The quantity $\operatorname{poly}$ is a polynomial left unexpanded in the source. Its arguments are, in order, the strong-stability constant, strong-controllability constant, inverse stability margin, number of controllability blocks, state dimension, input dimension, disturbance bound, and cost-gradient growth constant. These dependencies are not claimed to be sharp.; This upper bound has no registered matching lower bound for general unknown input matrices. The matrix $A=0,d_x=2,d_u=1$ in catalog item Q6 generally fails the full-row-rank controllability condition, so the two settings are not exact counterparts.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - Online control by system identification followed by a perturbed-action policy

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\operatorname{poly}\!\left(C_{\mathrm{stab}},C_{\mathrm{ctrl}},\gamma^{-1},k_{\mathrm{ctrl}},d_x,d_u,W,G\right)T^{2/3}\log\!\frac1{\delta_{\mathrm{conf}}}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v117/hazan20a/hazan20a.pdf)

**Source location.** [1](https://proceedings.mlr.press/v117/hazan20a/hazan20a.pdf) Theorem 12, PDF p.7

## References

[1] Elad Hazan; Sham M. Kakade; Karan Singh. The Nonstochastic Control Problem. 2020. ALT 2020, PMLR 117.

https://proceedings.mlr.press/v117/hazan20a/hazan20a.pdf
