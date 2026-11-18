# Jointly private linear bandits with independent contexts and a uniform positive gap

**Setting ID.** `ONX_JDP_IID_GAP`

Online learning and bandits

Each round reveals a context or action-feature set before the learner chooses an action and observes its reward with linear conditional mean. The algorithm must satisfy joint differential privacy: one user's information has limited influence on actions shown to other users. Contexts are i.i.d. from an unknown distribution. All suboptimal actions have a common positive gap lower bound.

**Status.** Bounds missing

**TASK tags.** formulation: Onx jdp iid gap; task family: Online bandit

**MODEL tags.** structure: Linear

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round reveals a context or action-feature set before the learner chooses an action and observes its reward with linear conditional mean. The algorithm must satisfy joint differential privacy: one user's information has limited influence on actions shown to other users. Contexts are i.i.d. from an unknown distribution. All suboptimal actions have a common positive gap lower bound.

### Admissible model

Contexts $x_t$ are drawn independently from an unknown distribution $P$. The finite action set $\mathcal{A}$ and feature map $\phi$ are public. The fixed unknown parameter and all features lie in the Euclidean unit ball:

$$
\|\phi(x,a)\|_2\le1,\quad\|\theta_\star\|_2\le1,\quad Y_t\in[-1,1],\quad\mathbb{E}[Y_t\mid x_t,a_t,\mathcal{H}_{t-1}]=\langle\phi(x_t,a_t),\theta_\star\rangle.
$$

A fresh reward is sampled from the current conditional distribution. Observe the context, act, then receive the selected action's reward.

Define $f^\star(x,a)=\langle\phi(x,a),\theta_\star\rangle$. Optimal actions may tie for any context, but all suboptimal actions obey the same positive gap condition:

$$
a\notin\operatorname*{arg\,max}_{b\in\mathcal{A}}f^\star(x,b)\ \Longrightarrow\ \max_{b\in\mathcal{A}}f^\star(x,b)-f^\star(x,a)\ge\Delta_{\min}>0.
$$

### Oracle interface

Causal policies satisfying $(\epsilon_{\mathrm{priv}},\delta_{\mathrm{priv}})$ joint privacy are permitted. The parameters $T,d,\mathcal{A},\phi,\epsilon_{\mathrm{priv}},\delta_{\mathrm{priv}}$ are public.

The context distribution $P$, reward parameter $\theta_\star$, and positive gap $\Delta_{\min}$ are hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
\mathbb{E}\!\left[\sum_{t=1}^{T}\left(\max_{a\in\mathcal{A}}\langle\phi(x_t,a),\theta_\star\rangle-\langle\phi(x_t,a_t),\theta_\star\rangle\right)\right].
$$

### Resource accounting

$N=T$ selected-arm reward observations.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

Neighboring streams $\mathsf D,\mathsf D^{\prime}$ differ only in one user's context/reward pair. The protected output is every action except that user's current recommendation, received privately. For every measurable event $E$, require:

$$
\Pr\!\left(\mathcal{M}(\mathsf D)_{-t}\in E\right)\le e^{\epsilon_{\mathrm{priv}}}\Pr\!\left(\mathcal{M}(\mathsf D^{\prime})_{-t}\in E\right)+\delta_{\mathrm{priv}}.
$$

The privacy relaxation constrains the entire output mechanism. Performance is measured in expectation, without a separate external statistical failure probability.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Take the infimum over admissible jointly private strategies before the supremum over unknown i.i.d. context distributions and admissible reward environments. Expectation includes contexts, reward noise, and privacy-algorithm randomness. Every environment must also satisfy the uniform gap condition above.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\delta_{\mathrm{priv}}$: Additive allowance in approximate differential privacy **Domain:** $0\le\delta_{\mathrm{priv}}<1$.

Additive allowance in the output-event probability inequality for adjacent inputs; not statistical confidence.

$\epsilon_{\mathrm{priv}}$: The multiplicative differential-privacy parameter. **Domain:** $\epsilon_{\mathrm{priv}}>0$.

Use the factor $e^{\epsilon_{\mathrm{priv}}}$ when comparing probabilities of output events under adjacent data inputs.

$d_{\mathcal A}$: Maximum dimension spanned by action features in a single context. **Domain:** $0\le d_{\mathcal A}\le\min\{d,|\mathcal A|\}$.

$$
d_{\mathcal A}=\max_x\dim\operatorname{span}\{\phi(x,a):a\in\mathcal A\}
$$.

$\sigma_{\mathrm{priv}}$: Normalized noise coefficient in the source Gaussian privacy channel **Domain:** $\sigma_{\mathrm{priv}}>0$.

On the bound's window $0<\delta_{\rm priv}<1$, $\sigma_{\mathrm{priv}}=4\sqrt{\log(2.5/\delta_{\mathrm{priv}})}/\epsilon_{\mathrm{priv}}$. Actual mechanism noise also scales with query sensitivity and is distinct from reward noise.

$\Delta_{\min}$: Lower bound on every positive suboptimality gap across all contexts **Domain:** $0<\Delta_{\min}\le2$, when suboptimal actions exist.

Every suboptimal action a satisfies $\max_b f^\star(x,b)-f^\star(x,a)\ge\Delta_{\min}$. Tied optimal actions are allowed, and this lower bound is not supplied to the algorithm.

$\mathcal M$: The jointly private mechanism releasing recommended actions. **Domain:** A causal randomized algorithm.

$\mathsf D,\mathsf D^{\prime}$: Adjacent streams differ in one user’s context and reward record. **Domain:** Adjacent input data streams.

The comparison concerns the full induced distributions of the output action sequence.

$\mathcal M(\mathsf D)_{-t}$: The output sequence with the current user’s action at position t removed. **Domain:** Action-sequence random variable.

Joint privacy protects all actions visible to other users. The current recommendation at time $t$ is received privately by that user.

$E$: A measurable output event in the privacy definition. **Domain:** Measurable subset of the output space.

The privacy inequality holds for every such event.

$P,x_t$: Unknown context distribution and the independent context in the current round **Domain:** A probability distribution and its samples.

Assume $x_t\overset{\mathrm{i.i.d.}}\sim P$; reveal $x_t$ to the learner before action selection.

$\mathcal A,\phi$: Public finite action set and public feature map **Domain:** Finite set and d-dimensional map.

$\phi(x,a)\in B_2^d(1)$.

$\theta_\star$: Fixed hidden reward parameter **Domain:** $\theta_\star\in B_2^d(1)$.

$a_t,Y_t$: Current action and the reward observed after acting **Domain:** $a_t\in\mathcal A,\ Y_t\in[-1,1]$.

$\mathbb E[Y_t\mid x_t,a_t,\mathcal H_{t-1}]=\langle\phi(x_t,a_t),\theta_\star\rangle$.

$f^\star(x,a)$: Mean reward of action $a$ in context $x$ **Domain:** A real number in [-1,1].

$f^\star(x,a)=\langle\phi(x,a),\theta_\star\rangle$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_t[\max_{a\in\mathcal A}\langle\phi(x_t,a),\theta_\star\rangle-\langle\phi(x_t,a_t),\theta_\star\rangle]$ Realized observation noise is excluded from the loss difference. Probability or expectation aggregation is specified separately by the guarantee.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation includes learner randomness and the explicitly specified reward or sample randomness. Conditional expectations retain their stated history conditioning.

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
\mathbb E\!\left[\sum_{t=1}^{T}\left(\max_{a\in\mathcal A}\langle\phi(x_t,a),\theta_\star\rangle-\langle\phi(x_t,a_t),\theta_\star\rangle\right)\right].
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** IID contexts and a uniform positive gap; other conditions are those attached to the recorded bounds.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
O(d_{\mathcal{A}}^3d\log^2T/\Delta_{\min})+\widetilde{O}(\sigma_{\rm priv}d_{\mathcal{A}}d\sqrt{d+\log T}\log T)
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** Contexts are IID, and every suboptimal action has mean gap at least $\Delta_{\min}>0$.; Require $0<\varepsilon_{\mathrm{priv}}\le1$ and $0<\delta_{\mathrm{priv}}\le1/2$, with bounded actions and rewards. The parameter $\Delta_{\min}$ need not be an algorithm input.

**Oracle mapping.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee mapping.** The accompanying argument states the native guarantee and necessary conversion.

### B1 - Algorithm 6: information-weighted differentially private regression with batched elimination

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{d_{\mathcal{A}}^{3}d\log^2T}{\Delta_{\min}}\right)+\widetilde{O}\!\left(\sigma_{\rm priv}d_{\mathcal{A}}d\sqrt{d+\log T}\log T\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2502.13115)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rounds.** T

**native feedback.** Use the native per-round protocol specified by the contract.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** Here $\widetilde O$ additionally suppresses only the factor $\log\log T$. The privacy-noise quantity $\sigma_{\mathrm{priv}}$ is defined in source Definition 3. Preserve the expected pseudo-regret guarantee; it is not an instancewise high-probability statement.

**Source location.** [1](https://arxiv.org/pdf/2502.13115) Definition 3, PDF p.5; Assumption 1; Theorem 6.3, PDF p.23

Here $\widetilde O$ additionally suppresses only the factor $\log\log T$. The privacy-noise quantity $\sigma_{\mathrm{priv}}$ is defined in source Definition 3. Preserve the expected pseudo-regret guarantee; it is not an instancewise high-probability statement.

## References

[1] Fan Chen; Jiachun Li; Alexander Rakhlin; David Simchi-Levi. Beyond Covariance Matrix: The Statistical Complexity of Private Linear Regression. 2025. 2502.13115v2.

https://arxiv.org/pdf/2502.13115
