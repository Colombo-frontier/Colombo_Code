# Federated linear bandits: synchronous two-point feedback and gradient heterogeneity

**Setting ID.** `ONX_FED_TWO_LINEAR`

Online learning and bandits

Multiple clients face separate linear losses and exchange information only at prescribed synchronization rounds. Each client simultaneously queries two values of its current local function, and both query points incur loss. The comparator is one fixed point shared by all clients.

**Status.** Bounds missing

**TASK tags.** formulation: Onx fed two linear; task family: Online bandit

**MODEL tags.** structure: Linear

**ORACLE tags.** interface family: Distributed two point; operation: Distributed two point; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; communication: Local-information protocol between synchronizations; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Average two point regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Multiple clients face separate linear losses and exchange information only at prescribed synchronization rounds. Each client simultaneously queries two values of its current local function, and both query points incur loss. The comparator is one fixed point shared by all clients.

### Admissible model

There are $M$ clients interacting simultaneously in $\mathbb{R}^d$ for $T=L_{\mathrm{comm}}R_{\mathrm{comm}}$ rounds each. They synchronize once every $L_{\mathrm{comm}}$ rounds, for $R_{\mathrm{comm}}$ synchronizations.

$$
f_t^m(x)=\langle g_t^m,x\rangle+b_t^m,\qquad \|g_t^m\|_2\le G.
$$

$$
f_t(x)=\frac1M\sum_{m=1}^{M}f_t^m(x),\qquad \frac1M\sum_{m=1}^{M}\|\nabla f_t^m(x)-\nabla f_t(x)\|_2^2\le\zeta^2\quad(\forall t,x).
$$

The adversary may depend on all previous actions and the algorithm but not on current private randomness. Every client uses the same hindsight comparator:

$$
x^\star\in\operatorname*{arg\,min}_{\|x\|_2\le B}\sum_{t=1}^{T}\sum_{m=1}^{M}f_t^m(x).
$$

### Oracle interface

Each client simultaneously submits $x_t^{m,1},x_t^{m,2}\in\mathbb{R}^d$ in each round, then receives exact values of the same current local function at both points.

The second point cannot depend on the first response. There is no independent measurement noise; variance from randomized directions is part of estimator analysis.

Both query points incur loss. The comparator ball $\{x:\|x\|_2\le B\}$ does not constrain all query points.

The quantities $M,d,T,L_{\mathrm{comm}},R_{\mathrm{comm}},G,B,\zeta$ are public.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

Each client simultaneously outputs two queries $x_t^{m,1},x_t^{m,2}\in\mathbb{R}^d$ per round, and both incur local loss. Comparator constraint $\|x\|_2\le B$ does not restrict those points. Loss cannot be recomputed afterwards at their center or average.

### Loss or accuracy criterion

$$
\overline R_T=\frac1{2MT}\,\mathbb{E}_{\mathcal{A}}\!\left[\sum_{t=1}^{T}\sum_{m=1}^{M}\sum_{j=1}^{2}\Bigl(f_t^m(x_t^{m,j})-f_t^m(x^\star)\Bigr)\right].
$$

### Resource accounting

$$
N=2MT,\qquad T=L_{\mathrm{comm}}R_{\mathrm{comm}}.
$$

The quantity $N$ counts scalar value evaluations, $T$ counts rounds per client, and $R_{\mathrm{comm}}$ counts synchronizations. These resources are not interchangeable.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

Between synchronizations, each client uses only its new local observations and history shared at the previous synchronization. Synchronization occurs every $L_{\mathrm{comm}}$ rounds, with no message-length bound.

Between synchronizations, clients use only new local observations and information shared at the preceding synchronization. Complete states or observations may be exchanged at synchronization.

Communication bits are neither bounded nor charged. A finite number of synchronizations does not imply bounded message length.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

This is average regret per actual query point. Multiply by $2MT$ for total two-point regret. Expectation includes randomized queries, with worst case over admissible adaptive loss environments.

## 2. Notation and parameters

$B$: Radius of the common comparator ball **Domain:** $B>0$.

The comparator satisfies $\|x^\star\|_2\le B$. B is not a bound on absolute rewards in this specification.

$G$: Uniform Euclidean bound on the full loss gradient in each round **Domain:** $G>0$.

The condition $\|\nabla f_t(x)\|_2\le G$ holds for all t and x specified by the model.

$L_{\mathrm{comm}}$: Local rounds between consecutive synchronizations. **Domain:** $L_{\mathrm{comm}}\in\mathbb N,\ L_{\mathrm{comm}}\ge1$.

Synchronize after every $L_{\mathrm{comm}}$ local rounds.

$M$: Number of clients participating synchronously **Domain:** $M\in\mathbb N,\ M\ge1$.

Client index $m\in[M]$

$R_{\mathrm{comm}}$: Total synchronization count **Domain:** $R_{\mathrm{comm}}\in\mathbb N,\ R_{\mathrm{comm}}\ge1$.

$T=L_{\mathrm{comm}}R_{\mathrm{comm}}$.

$T$: The total number of local interaction rounds per client. **Domain:** $T=L_{\mathrm{comm}}R_{\mathrm{comm}}$.

Total function-value feedback count is $2MT$. Loss is averaged across all clients and both queried points.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\zeta$: A root-mean-square bound on client-gradient heterogeneity. **Domain:** $\zeta\ge0$.

$M^{-1}\sum_m\|\nabla f_t^m(x)-\nabla f_t(x)\|_2^2\le\zeta^2$; $f_t=M^{-1}\sum_mf_t^m$.

$m,j$: Client index and index of the current round's probe point **Domain:** $m\in[M],\ j\in\{1,2\}$.

The quantity m is neither a memory length nor a separately specified objective count.

$f_t^m,f_t$: Client losses and their average across clients. **Domain:** A convex real-valued function on the full space.

$f_t(x)=M^{-1}\sum_m f_t^m(x)$.

$x_t^{m,j}$: The jth point incurring actual loss for client m in round t **Domain:** $x_t^{m,j}\in\mathbb R^d$.

Both query points are submitted before feedback, and both are included in the loss.

$x^\star$: Fixed comparator shared by all clients over the entire horizon **Domain:** $\|x^\star\|_2\le B$.

$x^\star\in\arg\min_{\|x\|_2\le B}\sum_{t,m}f_t^m(x)$.

$\overline R_T$: Expected regret averaged over all actual two-point evaluations **Domain:** Real number.

$\overline R_T=(2MT)^{-1}\mathbb E\sum_{t,m,j}[f_t^m(x_t^{m,j})-f_t^m(x^\star)]$.

$\mathbf1\{L_{\mathrm{comm}}>1\}$: Indicator factor activated when synchronization does not occur every round **Domain:** $\{0,1\}$.

Equals $0$ under synchronization every round and $1$ otherwise.

$g_t^m,b_t^m$: Slope and intercept of an affine loss **Domain:** $g_t^m\in\mathbb R^d,\ b_t^m\in\mathbb R$.

The affine losses are $f_t^m(x)=\langle g_t^m,x\rangle+b_t^m$, with $\|g_t^m\|_2\le G$. Intercepts cancel from comparator regret.

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

$N=2MT$ counts scalar function values across all clients.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
\overline R_T=\frac1{2MT}\,\mathbb E_{\mathcal A}\!\left[\sum_{t=1}^{T}\sum_{m=1}^{M}\sum_{j=1}^{2}\Bigl(f_t^m(x_t^{m,j})-f_t^m(x^\star)\Bigr)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** $T=L_{\rm comm} R_{\rm comm}$, with heterogeneity zeta and average two-point regret.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
\begin{aligned}[c]O\!\Bigg(&\frac{GB}{\sqrt T}+GB\sqrt{\frac d{MT}}\\ &+\mathbf1\{L_{\mathrm{comm}}>1\}\left[\frac{\sqrt{\zeta G}\,B d^{1/4}}{L_{\mathrm{comm}}^{1/4}\sqrt{R_{\mathrm{comm}}}}+\frac{\zeta B}{\sqrt{R_{\mathrm{comm}}}}\right]\Bigg).\end{aligned}
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $T=L_{\mathrm{comm}}R_{\mathrm{comm}}$. The expression still averages over two evaluation points. The quantity $\zeta$ bounds root-mean-square gradient heterogeneity across clients.; The condition $\mathbf1\{L_{\mathrm{comm}}>1\}$ means that clients do not synchronize every round. This corollary alone does not give a matching lower bound at every communication level.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - FedOSGD for linear losses with heterogeneity analysis

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\begin{aligned}[c]O\!\Bigg(&\frac{GB}{\sqrt T}+GB\sqrt{\frac d{MT}}\\ &+\mathbf1\{L_{\mathrm{comm}}>1\}\left[\frac{\sqrt{\zeta G}\,B d^{1/4}}{L_{\mathrm{comm}}^{1/4}\sqrt{R_{\mathrm{comm}}}}+\frac{\zeta B}{\sqrt{R_{\mathrm{comm}}}}\right]\Bigg).\end{aligned}
$$

**Sources.** [1](https://proceedings.mlr.press/v202/patel23a/patel23a.pdf)

**Source location.** [1](https://proceedings.mlr.press/v202/patel23a/patel23a.pdf) Corollary 5.3, PDF p.8

## References

[1] Kumar Kshitij Patel; Lingxiao Wang; Aadirupa Saha; Nati Srebro. Federated Online and Bandit Convex Optimization. 2023. ICML 2023, PMLR 202.

https://proceedings.mlr.press/v202/patel23a/patel23a.pdf
