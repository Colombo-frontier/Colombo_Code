# Stochastic linear bandits on a Euclidean ball with independent scalar Gaussian noise.

**Setting ID.** `ON_LINSTO_S`

Online learning and bandits

The learner chooses actions in the Euclidean unit ball and observes their inner products with a fixed unknown parameter plus independent standard Gaussian noise. The target is cumulative mean reward relative to the best fixed action. Reducing action magnitude does not reduce the noise variance.

**Status.** Fully optimal

**TASK tags.** formulation: Stochastic linear bandit; solution concept: Minimize expected cumulative pseudo regret; task family: Online bandit

**MODEL tags.** geometry: Parameter ball; stochastic model: Additive scalar noise; structure: Linear

**ORACLE tags.** feedback quality: Gaussian additive noise; interface family: Selected reward; operation: Observe scalar linear loss; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Action trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Matrix updates; measure: Native feedback; measure: Optimistic solves; measure: Rounds

## 1. Setting specification

### Task

The learner chooses actions in the Euclidean unit ball and observes their inner products with a fixed unknown parameter plus independent standard Gaussian noise. The target is cumulative mean reward relative to the best fixed action. Reducing action magnitude does not reduce the noise variance.

### Admissible model

The hidden reward parameter $\theta$ is fixed before interaction and satisfies $\|\theta\|_2\le1$.

Scalar observation noise is i.i.d. $Z_t\sim N(0,1)$ and independent of the pre-action history. The observation variance remains one even when $x_t=0$. This specification uses additive scalar noise.

The actual action is also the sole observation point and satisfies $\|x_t\|_2\le1$.

Require $d,T\ge1$. Both actions and the unknown parameter lie in the unit Euclidean ball.

### Oracle interface

Linear rewards with independent scalar noise:

$$
t,\ x_t\in B_2^d(1)\ \longmapsto\ Y_t\mid\mathcal{H}_{t-1},x_t\sim\mathcal{N}(\langle x_t,\theta\rangle,1)
$$

Choose action $x_t$, then draw fresh noise $Z_t$ and return one scalar observation.

Neither $\theta$, a gradient, nor projections onto other directions in the same round are returned.

The same x may be measured again in another round, with fresh noise and a new charge.

Public inputs are $d,T$, action domain $B_2^d(1)$, parameter-norm bound one, and known scalar noise $\mathcal N(0,1)$.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
Y_t=\langle x_t,\theta\rangle+Z_t,\quad Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal{N}(0,1),\qquad R_T=\sum_t(\|\theta\|_2-\langle x_t,\theta\rangle)
$$

### Resource accounting

$T$ rounds provide $T$ scalar noisy linear observations.

Any causal randomized policy is allowed. OFUL is one verified upper-bound method.

OFUL maintains a $d\times d$ design matrix and confidence set and solves an optimistic decision problem. Matrix updates and optimistic optimization are not one bandit call.

Information calls, arithmetic, communication rounds, and memory are measured separately. Exact real internal computation is excluded from information complexity unless explicitly charged. This does not imply a bit-complexity bound.

### Algorithm views and success guarantees

All measurable causal randomized policies respecting the stated timing are allowed. The private seed is independent of the fixed instance and future samples. Apart from explicit feedback, output, and budget requirements, there are no restrictions on linear spans, iteration form, internal arithmetic, memory, or communication.

$$
\inf_{\mathcal{A}}\sup_{\|\theta\|_2\le1}\mathbb{E}_{\mathcal{A},Z}[R_T]
$$

Choose one algorithm using public inputs before taking the worst case over all admissible instances. Expectation covers the algorithm's private randomness and the observation randomness specified by the model. Comparator choice and the order of summation, minimization, and expectation follow the displayed formula.

**Budget convention.** There are T sequential interaction rounds. Native feedback count is determined by the per-round protocol and is not an independent budget to minimize.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\theta$: Fixed hidden linear-reward parameter **Domain:** $\theta\in B_2^d(1)$.

$x_t$: Current action and sole observation point **Domain:** $x_t\in B_2^d(1)$.

$Z_t$: Independent scalar observation noise. **Domain:** $Z_t\overset{\mathrm{i.i.d.}}\sim\mathcal N(0,1)$.

Noise variance does not scale with the action norm; the zero action also has observation variance one.

$Y_t$: Scalar reward observed in the current round **Domain:** $Y_t\in\mathbb R$.

$Y_t=\langle x_t,\theta\rangle+Z_t$.

$\lambda,S,L,R_{\mathrm{noise}},\delta$: Source notation in the earlier OFUL branch **Domain:** Used only to specialize this upper bound.

These denote the ridge parameter, parameter-norm bound, action-norm bound, sub-Gaussian noise scale, and failure probability, respectively. Set the first four to one and impose $\delta=1/T$.

$A,\|\theta\|_A,\sigma$: Ellipsoidal parameter, dual-reward scale, and noise scale in the E2TC derivation **Domain:** Used only to specialize this upper bound.

For the current unit ball, use $A=I_d$, so $\|\theta\|_A=\|\theta\|_2$, and set $\sigma=1$.

$D,a,e_1$: Actual dimension, signal amplitude, and first coordinate unit vector in the low-dimensional lower bound **Domain:** Used only in the lower-bound proof.

Set $D=d$, $a=1/(4\sqrt T)$, and hard parameters $\theta=\pm ae_1$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_t(\|\theta\|_2-\langle x_t,\theta\rangle)$ Realized observation noise is excluded from the loss difference. Probability or expectation aggregation is specified separately by the guarantee.

$\mathcal R_T^*$: Minimax expected regret under the current information protocol and parameter region. **Domain:** A nonnegative real.

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\|\theta\|_2\le1}\mathbb E_{\mathcal A,Z}[R_T],\\ R_T&=\sum_{t=1}^T(\|\theta\|_2-\langle x_t,\theta\rangle).\end{aligned}
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

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax cumulative pseudo regret

$$
\begin{aligned}\mathcal R_T^*&=\inf_{\mathcal A}\sup_{\|\theta\|_2\le1}\mathbb E_{\mathcal A,Z}[R_T],\\ R_T&=\sum_{t=1}^T(\|\theta\|_2-\langle x_t,\theta\rangle).\end{aligned}
$$

**Scope.** Compare only this specification and the listed parameter regions.

**Optimization direction.** minimize

### R1 - MAIN

**Region.** $T\ge d^2; d\ge 1; T\ge 2$

**Quantity.** Q1

**Resource.** Native sequential interaction rounds or samples; additional resources remain attached to each bound.

**Status.** Optimal

**Lower bound.** B2, B4

$$
\Omega(d\sqrt T)
$$

**Upper bound.** B3

$$
O(d\sqrt T)
$$

**Gap or comparison.** E2TC at COLT 2025 removes the logarithmic factor in earlier bounds; retain its original applicability region.

**Comparison argument.** Only individually audited compatible claims enter. Baseline bracket; no claim that remaining logarithm is necessary or that all action geometries share this rate.

### R2 - ALL_D_T

**Region.** All integers $d,T\ge1$, with noise variance fixed to $1$

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(\min\{T,d\sqrt T\})
$$

**Upper bound.** B3

$$
O(\min\{T,d\sqrt T\})
$$

**Gap or comparison.** Constant ratio; dimension $d=1$ is included.

### R3 - SAT

**Region.** $1\le T\le d^{2}$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(T)
$$

**Upper bound.** B3

$$
O(T)
$$

**Gap or comparison.** Constant ratio

### R4 - LONG

**Region.** $T\ge d^{2}$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(d\sqrt T)
$$

**Upper bound.** B3

$$
O(d\sqrt T)
$$

**Gap or comparison.** Constant ratio

## 4. Bounds and supporting evidence

### B1 - OFUL

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\mathcal{R}_T^*\le C d\sqrt T\log(2T)
$$

**Sources.** [3](https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf)

**Conditions.** This bound requires $d\ge1$, $T\ge2$, and $T\ge d^2$, with actions in the unit Euclidean ball, parameter norm at most one, and unit Gaussian scalar observation noise.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle correspondence.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee conversion.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output rule.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource conversion.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T scalar observations

**optimistic solves.**

$$
\le T
$$

**matrix updates.** ≤T rank-one d×d updates

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** This simplified expression retains one log(2T) factor. The source gives a sharper determinant and logarithmic expression.

**Derivation.** In Theorem 3 set $\lambda=S=L=R_{\mathrm{noise}}=1$ and $\delta=1/T$. Although Gaussian observations are unbounded, the mean reward difference per round is at most two. Adding the failure-event contribution, at most $2T\delta$, to the high-probability regret bound gives the expected bound.

**Source location.** [3](https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf) theorem: Theorem 3; pdf pages: 5

Use OFUL's high-probability bound under $\lambda=S=L=R_{\mathrm{noise}}=1$ and $\delta=1/T$. Mean gaps per round are at most two, so failure contributes at most $2T\delta$ to expected regret. Optimistic optimization remains a required algorithmic operation.

### B2 - Gaussian scalar-noise hypercube family in Theorem24.2

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\mathcal{R}_T^*\ge\frac{d\sqrt T}{16\sqrt3}
$$

**Sources.** [2](https://tor-lattimore.com/downloads/book/book.pdf)

**Conditions.** This bound requires $d\ge1$, $T\ge2$, and $T\ge d^2$, with actions in the unit Euclidean ball, parameter norm at most one, and unit Gaussian scalar observation noise.

**Dimension conditions.** Dimension, arm count, and horizon must satisfy the stated region. Large-dimension and asymptotic source conditions are retained.

**Oracle correspondence.** Preserve current-round feedback content, response timing, and sample coupling, without adding access to hidden objects.

**Guarantee conversion.** Retain this setting's cumulative regret, error probability, stopping time, or error exponent, including the order of aggregation. Required conversions are stated in the bound's derivation.

**Output rule.** Use the actual action trajectory or terminal recommendation required by the specification. Post-hoc averaging is allowed only where an explicit derivation justifies that transfer.

**Resource conversion.** Native queries and initialization use the declared resource units. No extra samples or revisits to past rounds are free.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** T

**Constants.** Universal constants independent of the parameters explicitly tracked in this claim

**Logarithmic factors.** None.

**Source location.** [2](https://tor-lattimore.com/downloads/book/book.pdf) theorem: Theorem 24.2; pdf pages: 299; 300; printed pages: 290; 291

Actions lie in the unit ball and feedback has independent standard Gaussian scalar noise. Hard parameters satisfy $\|\theta\|_2^2=d^2/(48T)$ and yield lower bound $d\sqrt T/(16\sqrt3)$; $T\ge d^2$ ensures they lie in the unit ball.

### B3 - E2TC: explore, test, then commit

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
C\min\{T,d\sqrt T\}
$$

**Sources.** [1](https://proceedings.mlr.press/v291/zhang25b.html)

**Conditions.** Assume integer $d,T\ge1$, actions in the unit Euclidean ball, $\|\theta\|_2\le1$, and independent standard Gaussian scalar noise.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** Corollary 8 gives $O(\min\{\sigma d\sqrt T+d\|\theta\|_A,\ T\|\theta\|_A\})$. Set $A=I$, $\sigma=1$, and $\|\theta\|_2\le1$ and use $d\le d\sqrt T$ to obtain the stated worst-case upper bound.

**Source location.** [1](https://proceedings.mlr.press/v291/zhang25b.html) theorem: Corollary 8, Theorem 7

Corollary 8 gives $O(\min\{\sigma d\sqrt T+d\|\theta\|_A,\ T\|\theta\|_A\})$. Set $A=I$, $\sigma=1$, and $\|\theta\|_2\le1$ and use $d\le d\sqrt T$ to obtain the stated worst-case upper bound.

### B4 - Local spherical hard instances; dimensions d = 1,2 use two Gaussian sign hypotheses.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{T,d\sqrt T\}
$$

**Sources.** [1](https://proceedings.mlr.press/v291/zhang25b.html)

**Conditions.** The bound requires integer $d,T\ge 1$ and the same standard-Gaussian unit-ball model.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** The source lower bound writes ambient dimension as $d+2$. If actual dimension is denoted $D$, then $D\ge3$ implies $D-2\ge D/3$, so relabeling preserves the order. For $D=1,2$, embed the two parameters $\theta=\pm ae_1$ with $a=1/(4\sqrt T)$. Under any policy the KL divergence between transcript laws is at most $2a^2T=1/8$. Pinsker's inequality gives constant sign-error probability and cumulative regret $\Omega(\sqrt T)$. Since $\min\{T,D\sqrt T\}\le2\sqrt T$, the required order also holds in these small dimensions.

**Source location.** [1](https://proceedings.mlr.press/v291/zhang25b.html) theorem: Theorem 1 and the accompanying two-hypothesis argument in low dimension

The source lower bound writes ambient dimension as $d+2$. If actual dimension is denoted $D$, then $D\ge3$ implies $D-2\ge D/3$, so relabeling preserves the order. For $D=1,2$, embed the two parameters $\theta=\pm ae_1$ with $a=1/(4\sqrt T)$. Under any policy the KL divergence between transcript laws is at most $2a^2T=1/8$. Pinsker's inequality gives constant sign-error probability and cumulative regret $\Omega(\sqrt T)$. Since $\min\{T,D\sqrt T\}\le2\sqrt T$, the required order also holds in these small dimensions.

## References

[1] Raymond Zhang; Hédi Hadiji; Richard Combes. Linear Bandits on Ellipsoids: Minimax Optimal Algorithms. 2025. COLT2025, PMLR291:6016–6040.

https://proceedings.mlr.press/v291/zhang25b.html

[2] Tor Lattimore; Csaba Szepesvári. Bandit Algorithms. 2020. online book PDF accessed 2026-10-31; printed/PDF pages recorded separately.

https://tor-lattimore.com/downloads/book/book.pdf

[3] Yasin Abbasi-Yadkori; Dávid Pál; Csaba Szepesvári. Improved Algorithms for Linear Stochastic Bandits. 2011. NeurIPS 24:2312–2320.

https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf
