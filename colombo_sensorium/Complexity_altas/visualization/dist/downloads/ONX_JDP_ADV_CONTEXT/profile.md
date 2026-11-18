# Jointly private linear bandits with predictable adversarial contexts

**Setting ID.** `ONX_JDP_ADV_CONTEXT`

Online learning and bandits

Each round reveals a context or action-feature set before an action is chosen and its reward with linear mean is observed. The algorithm satisfies joint differential privacy, limiting the influence of one user's information on actions shown to other users. Contexts may depend on the past.

**Status.** Bounds missing

**TASK tags.** formulation: Onx jdp adv context; task family: Online bandit

**MODEL tags.** structure: Linear

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: Joint differential privacy

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Time rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round reveals a context or action-feature set before an action is chosen and its reward with linear mean is observed. The algorithm satisfies joint differential privacy, limiting the influence of one user's information on actions shown to other users. Contexts may depend on the past.

### Admissible model

A predictable action set $\mathcal{A}_t\subset\mathbb{R}^d$ is revealed each round. Contexts may depend on the past transcript. The parameter $\theta_\star$ is fixed and unknown.

$$
\|a\|_2\le L\quad(a\in\mathcal{A}_t),\qquad \|\theta_\star\|_2\le S,\qquad |\langle a,\theta_\star\rangle|\le B.
$$

$$
Y_t=\langle a_t,\theta_\star\rangle+\eta_t,\qquad \mathbb{E}[\eta_t\mid\mathcal{H}_{t-1},a_t]=0.
$$

Noise is conditionally $\sigma$-sub-Gaussian given the pre-action history and current action. The privacy sensitivity argument additionally requires realized action-reward pairs to satisfy the following bounds almost surely:

$$\|(a_t,Y_t)\|_2\le\widetilde{L}\qquad\text{almost surely}.$$

### Oracle interface

The learner first observes the current context and action set, then selects $a_t$ and receives only that action’s scalar reward. The released action transcript satisfies joint privacy. Rewards for other actions remain hidden.

The parameters $d,T,L,S,\sigma,B,\widetilde{L},\epsilon_{\mathrm{priv}},\delta_{\mathrm{priv}},\delta_{\mathrm{conf}}$ are public. Reward parameters and future information of the admissible environment remain hidden.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^{T}\left(\max_{a\in\mathcal{A}_t}\langle a,\theta_\star\rangle-\langle a_t,\theta_\star\rangle\right).
$$

### Resource accounting

The procedure uses $N=T$ reward observations. The source combines linear UCB with a tree mechanism protecting sufficient statistics. Internal matrix and privacy computations do not provide additional free reward queries.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

Neighboring streams $\mathsf D,\mathsf D^{\prime}$ differ only in one user's context/reward pair. The protected output is every action except that user's current recommendation, received privately. For every measurable event $E$, require:

$$
\Pr\!\left(\mathcal{M}(\mathsf D)_{-t}\in E\right)\le e^{\epsilon_{\mathrm{priv}}}\Pr\!\left(\mathcal{M}(\mathsf D^{\prime})_{-t}\in E\right)+\delta_{\mathrm{priv}}.
$$

The privacy relaxation $\delta_{\mathrm{priv}}$ is distinct from the statistical failure probability $\delta_{\mathrm{conf}}$.

Causal policies satisfying $(\epsilon_{\mathrm{priv}},\delta_{\mathrm{priv}})$ joint differential privacy are admissible.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

The pseudo-regret must obey the bound with probability at least $1-\delta_{\mathrm{conf}}$, uniformly over contexts, reward distributions, and parameters satisfying the boundedness conditions. Realized observation noise is not included in the regret.

## 2. Notation and parameters

$B$: Absolute bound on linear mean reward **Domain:** $B\ge0$.

The bound is $|\langle a,\theta_\star\rangle|\le B$; it does not bound the absolute observed reward Y.

$L$: Euclidean norm bound on action or feature vectors **Domain:** $L>0$.

The condition is $\|a\|_2\le L$, with the same meaning if actions are denoted x.

$S$: A Euclidean-norm bound on the hidden linear reward parameter. **Domain:** $S\ge0$.

The quantity is $\|\theta_\star\|_2\le S$; it is not a switching budget.

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$d$: The ambient dimension of actions or feature vectors. **Domain:** $d\in\mathbb N,\ d\ge1$.

Vectors belong to $\mathbb R^d$; dimension is still denoted d when a non-Euclidean norm is used.

$\delta_{\mathrm{conf}}$: The allowed statistical failure probability. **Domain:** $0<\delta_{\mathrm{conf}}<1$.

Used only for statistical correctness or high-probability performance, and distinct from the privacy relaxation parameter.

$\delta_{\mathrm{priv}}$: Additive allowance in approximate differential privacy **Domain:** $0\le\delta_{\mathrm{priv}}<1$.

Additive allowance in the output-event probability inequality for adjacent inputs; not statistical confidence.

$\epsilon_{\mathrm{priv}}$: The multiplicative differential-privacy parameter. **Domain:** $\epsilon_{\mathrm{priv}}>0$.

Use the factor $e^{\epsilon_{\mathrm{priv}}}$ when comparing probabilities of output events under adjacent data inputs.

$\sigma$: Conditional sub-Gaussian scale of the reward noise **Domain:** $\sigma\ge0$.

For every $s\in\mathbb R$, $\mathbb E[e^{s\eta_t}\mid\mathcal H_{t-1},a_t]\le e^{s^2\sigma^2/2}$.

$\widetilde L$: Joint Euclidean norm bound for the actual action and reward **Domain:** $\widetilde L\ge0$.

The condition $\|(a_t,Y_t)\|_2\le\widetilde L$ holds almost surely and controls the sensitivity of the privacy mechanism.

$\mathcal A_t$: Predictable action set revealed before acting **Domain:** $\mathcal A_t\subseteq\mathbb R^d$.

Determined by past observations; all actions satisfy the stated norm and mean bounds.

$\theta_\star,a_t,Y_t,\eta_t$: The hidden parameter, selected action, realized reward, and observation noise. **Domain:** A quantity in the linear reward model.

Assume $Y_t=\langle a_t,\theta_\star\rangle+\eta_t$ and $a_t\in\mathcal A_t$; noise has conditional mean zero.

$\overline B$: The source mean bound, which is at least one. **Domain:** Positive real number.

$\overline B=\max\{1,B\}$.

$\mathcal M$: The jointly private mechanism releasing recommended actions. **Domain:** A causal randomized algorithm.

$\mathsf D,\mathsf D^{\prime}$: Adjacent streams differ in one user’s context and reward record. **Domain:** Adjacent input data streams.

The comparison concerns the full induced distributions of the output action sequence.

$\mathcal M(\mathsf D)_{-t}$: The output sequence with the current user’s action at position t removed. **Domain:** Action-sequence random variable.

Joint privacy protects all actions visible to other users. The current recommendation at time $t$ is received privately by that user.

$E$: A measurable output event in the privacy definition. **Domain:** Measurable subset of the output space.

The privacy inequality holds for every such event.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_t[\max_{a\in\mathcal A_t}\langle a,\theta_\star\rangle-\langle a_t,\theta_\star\rangle]$ Realized observation noise is excluded from the loss difference. Probability or expectation aggregation is specified separately by the guarantee.

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

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

The quantity $N=T$ counts cumulative native scalar feedback under a one-point or one-arm protocol.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

$$
R_T=\sum_{t=1}^{T}\left(\max_{a\in\mathcal A_t}\langle a,\theta_\star\rangle-\langle a_t,\theta_\star\rangle\right).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Assume $T\ge 2$, $0<\epsilon_{\rm priv}\le 1$, and $0<\delta_{\rm priv}<1/e$; statistical confidence is arbitrary, with joint sensitivity for bounded actions and rewards.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1, B2

$$
\min\left\{2T\min\{B,LS\},\,O\!\left(\overline B\sqrt T\left[\sigma\!\left(d\log T+\log\frac1{\delta_{\rm conf}}\right)+S\widetilde{L}\log T\sqrt{\frac{d\left(\sqrt d+\log(T/\delta_{\rm conf})\right)\log(1/\delta_{\rm priv})}{\epsilon_{\rm priv}}}\right]\right)\right\}
$$

**Gap or comparison.** No positive registered lower bound; multiplicative gap unassessed. If B=0 or S=0, R_T=0 exactly and a ratio is inapplicable.

**Comparison argument.** ONX_JDP_ADV_CONTEXT__main__p1

### R2 - Exact zero pseudo-regret at fixed online budget

**Region.** r1 AND (B=0 OR S=0), with the unchanged T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 conditions.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Gap or comparison.** Not applicable: exact zero pseudo-regret. The observation budget remains T; no 0/0 ratio or zero-query complexity is asserted.

**Comparison argument.** ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

## 4. Bounds and supporting evidence

### B1 - LinUCB with shifted-Gaussian binary-tree private statistics.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\overline B\sqrt T\left[\sigma\!\left(d\log T+\log\frac1{\delta_{\rm conf}}\right)+S\widetilde{L}\log T\sqrt{\frac{d\left(\sqrt d+\log(T/\delta_{\rm conf})\right)\log(1/\delta_{\rm priv})}{\epsilon_{\rm priv}}}\right]\right)
$$

**Sources.** [1](https://arxiv.org/abs/1810.00068)

**Conditions.** Require $T\ge2$, $0<\varepsilon_{\mathrm{priv}}\le1$, $0<\delta_{\mathrm{priv}}<1/e$, and $0<\delta_{\mathrm{conf}}<1$.; The joint norm of actions and rewards is at most $\widetilde L$ almost surely, and noise is conditionally sub-Gaussian. Contexts are predictable and may depend on past history.; The displayed $\overline B=\max\{1,B\}$ supplies the normalization required by the source lower bound. The complete public output sequence remains jointly differentially private.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**native feedback.** Use the native per-round protocol specified by the contract.

**rounds.** T

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** Only the logarithms in $\widetilde O$ are suppressed; see the evidence record.

**Derivation.** The source $n$ corresponds to horizon $T$, its confidence parameter $\alpha$ to $\delta_{\mathrm{conf}}$, and $\varepsilon,\delta$ to the privacy parameter. Corollary 12 gives pseudo-regret with probability at least $1-\delta_{\mathrm{conf}}$. Matrix shifts affect only internal noisy Gram statistics and grant no additional reward queries.

**Source location.** [1](https://arxiv.org/abs/1810.00068) theorem: Corollary12; Theorem5; Section4.2

The source $n$ corresponds to horizon $T$, its confidence parameter $\alpha$ to $\delta_{\mathrm{conf}}$, and $\varepsilon,\delta$ to the privacy parameter. Corollary 12 gives pseudo-regret with probability at least $1-\delta_{\mathrm{conf}}$. Matrix shifts affect only internal noisy Gram statistics and grant no additional reward queries.

### B2 - Deterministic mean-reward diameter cap.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
2T\min\{B,LS\}
$$

**Conditions.** Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).; Use the frozen bounds ||a||_2<=L, ||theta_star||_2<=S and |<a,theta_star>|<=B.

**Oracle correspondence.** Same T rounds and one selected scalar reward per round; no extra oracle access.

**Guarantee conversion.** Pathwise inequality; no confidence or privacy conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**native feedback.** Same T selected-reward observations as b1.

**rounds.** T

**Constants.** Exact coefficient 2, uniform in every native parameter.

**Derivation.** For every feasible action a, |<a,theta_star>|<=||a||_2||theta_star||_2<=LS by Cauchy-Schwarz and the frozen norm bounds. The independent mean bound also gives |<a,theta_star>|<=B. Thus comparator and selected-action means lie in [-min{B,LS},min{B,LS}]; every nonnegative pseudo-regret summand is <=2 min{B,LS}. Summing yields 0<=R_T<=2T min{B,LS} pathwise. Apply this inequality to the SAME admissible private strategy retained in b1 on r1: actions, privacy parameters, output and T selected-reward observations are unchanged. If its old event is R_T<=C F with probability >=1-delta_conf, intersection with this probability-one inequality gives R_T<=min{C F,2T min{B,LS}} at the same confidence, without algorithm selection or union-bound loss. F denotes exactly the explicit rate inside b1's O expression; C is a retained admissible constant. B=0 or S=0 forces exact zero regret by nonnegativity, while the observation budget remains T. The inequality is valid throughout the contract, but native algorithmic adoption here is restricted to r1, using its retained witness. No positive lower bound or matching minimax saturation threshold follows.

**Local argument.** ONX_JDP_ADV_CONTEXT__main__p1

**Source location.**  section: Frozen model norm/mean bounds and cumulative pseudo-regret definition; theorem: ONX_JDP_ADV_CONTEXT__main__p1

For every feasible action a, |<a,theta_star>|<=||a||_2||theta_star||_2<=LS by Cauchy-Schwarz and the frozen norm bounds. The independent mean bound also gives |<a,theta_star>|<=B. Thus comparator and selected-action means lie in [-min{B,LS},min{B,LS}]; every nonnegative pseudo-regret summand is <=2 min{B,LS}. Summing yields 0<=R_T<=2T min{B,LS} pathwise. Apply this inequality to the SAME admissible private strategy retained in b1 on r1: actions, privacy parameters, output and T selected-reward observations are unchanged. If its old event is R_T<=C F with probability >=1-delta_conf, intersection with this probability-one inequality gives R_T<=min{C F,2T min{B,LS}} at the same confidence, without algorithm selection or union-bound loss. F denotes exactly the explicit rate inside b1's O expression; C is a retained admissible constant. B=0 or S=0 forces exact zero regret by nonnegativity, while the observation budget remains T. The inequality is valid throughout the contract, but native algorithmic adoption here is restricted to r1, using its retained witness. No positive lower bound or matching minimax saturation threshold follows.

### B3 - Exact zero pseudo-regret specialization of retained p1

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

$$
0
$$

**Conditions.** r1 AND (B=0 OR S=0), with the unchanged T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 conditions.

**Oracle correspondence.** Unchanged online protocol: T rounds, one selected scalar reward observation each round; no new information or skipped observation is claimed.

**Guarantee conversion.** Pathwise R_T=0, hence probability-one satisfaction of the existing regret guarantee; the retained admissible strategy preserves its existing JDP guarantee.

**Output rule.** The native online action/output sequence is unchanged.

**Resource conversion.** The fixed observation budget stays N=T. This bound is on regret, not on query cost.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**native feedback.** T selected-reward observations; zero applies only to pseudo-regret.

**rounds.** T

**Local argument.** ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

### B4 - Nonnegative pseudo-regret, equal to zero on the stated mean-zero region

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

$$
0
$$

**Conditions.** r1 AND (B=0 OR S=0), with the unchanged T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 conditions.

**Oracle correspondence.** Unchanged online protocol: T rounds, one selected scalar reward observation each round; no new information or skipped observation is claimed.

**Guarantee conversion.** Pathwise R_T=0, hence probability-one satisfaction of the existing regret guarantee; the retained admissible strategy preserves its existing JDP guarantee.

**Output rule.** The native online action/output sequence is unchanged.

**Resource conversion.** The fixed observation budget stays N=T. This bound is on regret, not on query cost.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**native feedback.** T selected-reward observations; zero applies only to pseudo-regret.

**rounds.** T

**Local argument.** ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 58e15ce7edaa6cb12a8543cdafe54d6f220fc52d3b50c6674b2be12249ee75c2

### Native proof: ONX_JDP_ADV_CONTEXT__main__p1

Native pointer: /proofs/0; canonical SHA-256: 905f437d9f8fe601a477603ebff6819fb4a813da649b66058e23dd9fde2e4e08

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: 61d16bc7da2f8e7d08ddba3da967ae092c9cf0ab2b98a0179f340623328223d8

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: 2e95d0eb1a6905424633172bcd7e4411575b8f3d16d2d6e9ebaf14e43a5c4069

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: 4c912cf2e1a175c1cb5b832904e58c246797c48f04f2238ac60f1a67b0195101

16b7929fd4c7e616448fc5393657f56a795ae4544a7fe7b8838f88816b52aa5e

#### Native item 2

Native pointer: /proofs/0/baseline_refs/1; canonical SHA-256: ebc7df61c4a1cdee94d95251eff612c0f5abf207ac69f7c91f6428f5338dc3b9

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/1/pointer; canonical SHA-256: fcb08eed64b4a410c707257e2627768d9015ea03c3773356050232768b9d2a16

/bounds/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/1/sha256; canonical SHA-256: c26c03e0a9e84e89c125d314a996301625a1a220cd82d8efbf0df56d04259ac6

90d2add9d6eab94b55f635f49468fffe98fb804607512d3a595db8d13e57ff8c

#### Native item 3

Native pointer: /proofs/0/baseline_refs/2; canonical SHA-256: 225295f18293f1a250b08a94f3225e46aa86f856b76fb7ff760a0a003aedeb67

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/2/pointer; canonical SHA-256: 093a9ad2f779c83c2483d0b2930a00cfedd078d5514a96b1e08bc8c92c96a35b

/comparisons/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/2/sha256; canonical SHA-256: 0df5df0785ee219285bcab8f02f00c1c7ad39afab7bba99be9c7045be3c7238e

d63f5d3501fef8bee33073ac2e368859a92e9dd482beb6e36334eb10ad2dbc95

#### Native item 4

Native pointer: /proofs/0/baseline_refs/3; canonical SHA-256: 4c8c7d7c1746d09a8d3967bc4f0eb59a988300584b22b5f6966c1f296fcf9a8b

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/3/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/3/sha256; canonical SHA-256: 78496ced592b204f7b07621f11820a92713cc538bb2a679d0d111a400a81a7f4

6074df69dfb04f8d9a9372664c0204ea31b898b82f1eb3fef3e94e00b3e1cb05

#### Native field: bound_refs

Native pointer: /proofs/0/bound_refs; canonical SHA-256: 144cba620b75190e58b30a204d4b025e4db4a8ceb5aedd00c23e5d9ea014e1ae

#### Native item 1

Native pointer: /proofs/0/bound_refs/0; canonical SHA-256: a03f0e47c1aa5504c4e0df90c0c7661db5f521a061f37bdda3595acbd4ef07b9

ONX_JDP_ADV_CONTEXT__main__b1

#### Native item 2

Native pointer: /proofs/0/bound_refs/1; canonical SHA-256: 8712023087c229d8bdd7314624a677b4318ee7fa1b49dcade5f387d12f653711

ONX_JDP_ADV_CONTEXT__main__b2

#### Native field: guarantee_id

Native pointer: /proofs/0/guarantee_id; canonical SHA-256: 49c3b80dc4f4d5988cec8b039b96c617ba3e3a2bf9d8cb58887203d2fe297ecc

g1

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof

Native pointer: /proofs/0/proof; canonical SHA-256: 208b26696788fbaf9959530901a65c439bf0550168a71bc4f8cec903c108bb4c

For every feasible action a, |<a,theta_star>|<=||a||_2||theta_star||_2<=LS by Cauchy-Schwarz and the frozen norm bounds. The independent mean bound also gives |<a,theta_star>|<=B. Thus comparator and selected-action means lie in [-min{B,LS},min{B,LS}]; every nonnegative pseudo-regret summand is <=2 min{B,LS}. Summing yields 0<=R_T<=2T min{B,LS} pathwise. Apply this inequality to the SAME admissible private strategy retained in b1 on r1: actions, privacy parameters, output and T selected-reward observations are unchanged. If its old event is R_T<=C F with probability >=1-delta_conf, intersection with this probability-one inequality gives R_T<=min{C F,2T min{B,LS}} at the same confidence, without algorithm selection or union-bound loss. F denotes exactly the explicit rate inside b1's O expression; C is a retained admissible constant. B=0 or S=0 forces exact zero regret by nonnegativity, while the observation budget remains T. The inequality is valid throughout the contract, but native algorithmic adoption here is restricted to r1, using its retained witness. No positive lower bound or matching minimax saturation threshold follows.

#### Native field: quantity_ref

Native pointer: /proofs/0/quantity_ref; canonical SHA-256: d3dc028e871ffa1079512b535269aa34ddf27210214bcebb26a40f4fd4ecc709

ONX_JDP_ADV_CONTEXT__main__q1

#### Native field: region_refs

Native pointer: /proofs/0/region_refs; canonical SHA-256: b24fdc3e43378243b584d93be1647adc48596cb2df94f3ea67e295f2e86dd631

#### Native item 1

Native pointer: /proofs/0/region_refs/0; canonical SHA-256: da53591294f48b0db7a09676eaff1ad6418e8e331cdb5722d3e81f9f01f1f561

ONX_JDP_ADV_CONTEXT__main__r1

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: e8fabcb74723d69f8d25584ca9f12abdd74d2fb4792cd386b511d18fe67cc9fd

Pathwise bounded-mean upper cap intersected with retained b1 on r1.

#### Native field: view_id

Native pointer: /proofs/0/view_id; canonical SHA-256: e4a9e4d8baa71a9d8ebf56ec8ae3ea1e82be9f96ae6fe89e36d701d4a5337f30

main

### Native proof: ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

Native pointer: /proofs/1; canonical SHA-256: 609ea8c203b26781395eef22ee6357ed1299e62cb16c1362631f2e2b3920bec3

#### Native field: baseline_refs

Native pointer: /proofs/1/baseline_refs; canonical SHA-256: 1f5267d27cbfa12e8a1bd4979685ef55ca4c28fe7edf3afd7b4b359e6edd25da

#### Native item 1

Native pointer: /proofs/1/baseline_refs/0; canonical SHA-256: 523957280d4d1b3d44412080a24463ed2e0b7fd8386130d38078a769b9bb268a

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/0/pointer; canonical SHA-256: 5996f3d3c2a8fd6a8ed489bf2bb3ae9ea3149a27330820b5671197242e7659c9

/proofs/0

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/0/sha256; canonical SHA-256: 2676719cde7e25b1199b846de958eb981fba6504e5908e09aad20d0b63957919

905f437d9f8fe601a477603ebff6819fb4a813da649b66058e23dd9fde2e4e08

#### Native item 2

Native pointer: /proofs/1/baseline_refs/1; canonical SHA-256: 2e95d0eb1a6905424633172bcd7e4411575b8f3d16d2d6e9ebaf14e43a5c4069

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/1/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/1/sha256; canonical SHA-256: 4c912cf2e1a175c1cb5b832904e58c246797c48f04f2238ac60f1a67b0195101

16b7929fd4c7e616448fc5393657f56a795ae4544a7fe7b8838f88816b52aa5e

#### Native item 3

Native pointer: /proofs/1/baseline_refs/2; canonical SHA-256: 4811f6a476ad67c28ce48720da4f848f2788aa26c451f5ed2a2d5743398f7048

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/2/sha256; canonical SHA-256: df869ffa26cee9339aac4a5cfb5227ec70b06882eea384bc800c16be8b9022f2

d4d34a4d6b60a59b6ea45fd984800b2e64e492ec788ce05b4fddfddc2def7bbe

#### Native item 4

Native pointer: /proofs/1/baseline_refs/3; canonical SHA-256: 4c8c7d7c1746d09a8d3967bc4f0eb59a988300584b22b5f6966c1f296fcf9a8b

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/3/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/3/sha256; canonical SHA-256: 78496ced592b204f7b07621f11820a92713cc538bb2a679d0d111a400a81a7f4

6074df69dfb04f8d9a9372664c0204ea31b898b82f1eb3fef3e94e00b3e1cb05

#### Native item 5

Native pointer: /proofs/1/baseline_refs/4; canonical SHA-256: f49bda3659b2018e7774f63cdd045273a5ef91871151b4466acc83cad9b3400b

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/4/sha256; canonical SHA-256: 1265ef15dad3eb1a4fa6f73ade549d5410db5a3e4765ef6982b97a7de450543e

3c366da6c2a21774924d3a5801f11ef686a3a174e8ed629cace44da08854269a

#### Native field: guarantee_id

Native pointer: /proofs/1/guarantee_id; canonical SHA-256: 49c3b80dc4f4d5988cec8b039b96c617ba3e3a2bf9d8cb58887203d2fe297ecc

g1

#### Native field: kind

Native pointer: /proofs/1/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof

Native pointer: /proofs/1/proof; canonical SHA-256: fa80434bb43b13c40c8e9befff737ba2584e79a92c283d23f389c35a3cbd46b9

Condition on the exact retained p1 proof, fixed native pseudo-regret quantity, view/guarantee and online resource. It gives 0<=R_T<=2T min{B,LS} pathwise for every feasible trajectory. If B=0, the independent public bound on every mean forces each comparator and chosen-action mean to be zero. If S=0, theta_star=0 forces the same conclusion. In either case min{B,LS}=0 (L>0 is unchanged), hence each pseudo-regret summand and their sum are exactly zero for every legal instance and history. The same admissible private strategy witnessing b1/b2 on r1 is retained; its actions, selected-reward observations, output protocol, privacy parameters and guarantee are not changed. Its zero-regret event therefore holds with probability one and implies the native confidence requirement. The necessary lower bound 0 is metric nonnegativity, and on this region every admissible strategy has regret exactly zero. This is a matching performance-value bracket, not a lower or upper bound of zero on the observation budget: N remains T. No positive-scale lower bound, full-DP conversion or extension outside r1 is asserted.

#### Native field: proof_refs

Native pointer: /proofs/1/proof_refs; canonical SHA-256: c6a287e2c0154536db6b5ee7677cfb266a9997ff520cfff2265c8242d7d0fd37

#### Native item 1

Native pointer: /proofs/1/proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native field: quantity_ref

Native pointer: /proofs/1/quantity_ref; canonical SHA-256: d3dc028e871ffa1079512b535269aa34ddf27210214bcebb26a40f4fd4ecc709

ONX_JDP_ADV_CONTEXT__main__q1

#### Native field: region_refs

Native pointer: /proofs/1/region_refs; canonical SHA-256: ec2aeb017a39f3f458fe3031a3b5600d4dc005db6844d9c5c39d1d20f8e65462

#### Native item 1

Native pointer: /proofs/1/region_refs/0; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/1/statement; canonical SHA-256: 6c579e099706c4da39be54175685f03ab4a2d18fe02483378578115342375940

On r1 and B=0 or S=0, the native pseudo-regret R_T is exactly zero while the retained strategy still uses T selected-reward observations.

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: d6f6153a16ccea07cd5f00b3abeb418ed961a401f254dc988bfce68eb6b3cbca

Native registration of the already-proved zero pseudo-regret region

#### Native field: view_id

Native pointer: /proofs/1/view_id; canonical SHA-256: e4a9e4d8baa71a9d8ebf56ec8ae3ea1e82be9f96ae6fe89e36d701d4a5337f30

main

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: a52e96a6c49cf8934f9e3e7d5bab9aaff5519c26df8ac4282f1a8e9429c3764f

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 2f55113585c02f0a30eb4a870086728cd68172dfd6b80a5357d6d0288ba15d04

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: b1295160a345d2d6eb6edf511dc671c18e36a6d11b348a9627188e3d85965a41

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 714a8b2f2f0bd64f1c1c628c817191fc547d219978647082f7265cdcc832a548

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 7716bcce4baab66c051720b02e32e49b04ffb02b9b55d4d2a9ac370523c4995d

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: a03f0e47c1aa5504c4e0df90c0c7661db5f521a061f37bdda3595acbd4ef07b9

ONX_JDP_ADV_CONTEXT__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: ecf2b84de5b721340b15dbf1a67d343b1c70f831bc3657299d0d3bb147a48593

The only frozen mechanically compatible bound. Its exact existing learning claim and guard are retained conditionally; it supplies the learning branch of the minimum.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 4f164f27b87c893f065b7bf0c7a2c19fe0e9ca739db65afe83251abfb7ddaa7f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 8712023087c229d8bdd7314624a677b4318ee7fa1b49dcade5f387d12f653711

ONX_JDP_ADV_CONTEXT__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: c6a287e2c0154536db6b5ee7677cfb266a9997ff520cfff2265c8242d7d0fd37

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 27cba37cd98447ae8cbbf9020b254e91757bae3b2eada02a8b0037ee809d8f57

Universal pathwise diameter inequality, adopted using the same retained b1 witness on r1. It supplies the cap and exact zero-mean endpoint without changing queries, output or privacy.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: c89362c78d149f67f9e4abe54872cf63e3c808c4544a249b3200df9b4ad1fc22

Fixed main/g1 contract: integers T,d>=1; B,S,sigma,L_tilde>=0, L>0, epsilon_priv>0, 0<=delta_priv<1 and 0<delta_conf<1; predictable history-dependent action sets and the frozen bounded linear reward/noise model.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: f78eff42ff73f6a9ee8c111486aefc2c020dee45a1370ab234576d6b6e07e64a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 296768e07a0d1bfdcf6736602a7bba2de60619059a842c0e59edbad84921d8d1

Not adopted into the full c1 comparison; the regional statement is registered separately.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: fb5f8d8b61aad8599ebcada706e6af83df2bab149adf06107fa397aaa082b8f7

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_upper_20261116

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 572e34c0d7d336563544b199f9a95ef5a90dd66472c2fe618a63f9c4a4427054

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: b697909db19b8d88a47250a808dab636cb6ad646ce01632d6c94b1693471841d

This statement certifies only r1 intersect (B=0 or S=0). It supplies no positive-scale lower bound and leaves the old full c1 missing_lower state unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: e9538415f762f99dad195e302419c0506062da54dec61bda6de6bc2adb944140

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 296768e07a0d1bfdcf6736602a7bba2de60619059a842c0e59edbad84921d8d1

Not adopted into the full c1 comparison; the regional statement is registered separately.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: c90d4d4727cf9e9da3c76437f3e87e43f13864ea6ebdd6482532b370126e28c9

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_lower_20261116

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: 572e34c0d7d336563544b199f9a95ef5a90dd66472c2fe618a63f9c4a4427054

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: b697909db19b8d88a47250a808dab636cb6ad646ce01632d6c94b1693471841d

This statement certifies only r1 intersect (B=0 or S=0). It supplies no positive-scale lower bound and leaves the old full c1 missing_lower state unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: a589555d357fe7fab2dffd0322399389907a5307bb289d146e54fb6312f74e57

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 2aac7ba5c258f5d481ef2cee59c2098d3b811bc6e0eb787c89670f216fed6832

The strict r1 privacy thresholds and T>=2 remain source-activation guards; no intrinsic phase transition is asserted.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 4834cb5d9202fc1069e4c80a083f8215fd02d4abac15608d71294b712b812b31

The cap coefficient 2 is exact. B=0 or S=0 forces every comparator and selected mean to vanish.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 6c4a95e997102b0e037e0dd15c01042b4c1f43b1f1bcc700f85e6a08d664fc3e

d=1 and sigma=0 are allowed. No exact-reconstruction or sharper low-dimensional rate is inferred.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 95c75abe5acb4aa292caa9558ddbe08fdb5382de3621f81bd5a491272c5e7b6d

For B=L=S=sigma=1, L_tilde=2, d=1, delta_conf=1/4, delta_priv=1/10 and epsilon_priv=T^(-2), the old F is superlinear while the new cap is 2T.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: c1ac6ae7207fc51e2e949026ec3aa6f438fac6858a7a369c7975a310b2085d1b

For fixed positive structural parameters and fixed d/privacy/confidence, b1 is sqrt(T) times logarithms and remains the better asymptotic rate as T grows.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 93d191f7863ffab5aa9cde43a545336c20b39eca1e17dc1b827223331e82830e

At fixed T and positive scale, increasing d or decreasing delta_conf can make the displayed learning rate exceed the cap. Positive-scale crossover constants remain unspecified.

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/boundary_checks/6; canonical SHA-256: 011ee80be109f59fc8213dabea4f8bb59d66d84bcf6708cad598ab78cbf34f4d

The zero-regret endpoint leaves the budget at T reward observations; pure privacy and T=1 remain outside native adoption.

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/boundary_checks/7; canonical SHA-256: 0319d6853bd392e1d09474f283551d372f4869f8d3cb3328a04ef39ba8809e60

Active native upper refs are exactly b1 and b2, lower refs remain empty, and row_1 still points to the same updated comparison.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 962a14402564f752326661b018433414e0791fc8c7b25deb034b14442aa49053

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/2; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/3; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/4; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 962a14402564f752326661b018433414e0791fc8c7b25deb034b14442aa49053

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/2; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/3; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/4; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 267a4c338dcd6c654f408290f8dc651b858ddf1835fe6b744e9842c5d0432c40

At positive scale a multiplicative gap is unassessed because no positive lower is registered. At zero mean the exact regret is 0 and a ratio is inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: b1dc9e0463a188b3bea35bfb9aa22c35ebc562ba560514b7731f23e6431744ed

No registered nontrivial lower. The definition supplies R_T>=0 only. Together with b2 this gives exact zero on B=0 or S=0; the positive-scale lower side remains missing.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 37e974817c3986d38d0d33c216712e8b2b356eedc44e8ac25bf70ec11e69eebd

No positive lower bound or matching minimax saturation region is established. Potentially sharper literature results remain pending independently of this valid two-branch upper envelope.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: c9717159ac87fbf18e16b1de9cee87458fcc5d8fdbfb17128d0f9ca3c6a6667f

\min\left\{2T\min\{B,LS\},\,O\!\left(\overline B\sqrt T\left[\sigma\!\left(d\log T+\log\frac1{\delta_{\rm conf}}\right)+S\widetilde{L}\log T\sqrt{\frac{d\left(\sqrt d+\log(T/\delta_{\rm conf})\right)\log(1/\delta_{\rm priv})}{\epsilon_{\rm priv}}}\right]\right)\right\}; On r1, with probability >=1-delta_conf, R_T<=min{C F,2T min{B,LS}}, where O(F) is exactly b1's displayed formula and C is a retained admissible constant. No positive lower bound is added.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: bf928e289a0d28f7f4869fd3c049edf1edbaba1e320296aa9170ce5f4809ac02

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 6b7dee3de98239abff94e4e3eaac50bebb0463968d754390d14f47816b1c5876

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 307fbff7d6ffc0332049e88cbe8adc7cfbfa273e00be3fca9fad4be0461e4bc8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 2887c86586e5b331c15ef41d6a1d1c2bc9d4b302f6ef6fb221a8a4a29ff39b2e

Not selected in the exact-zero regional comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: a03f0e47c1aa5504c4e0df90c0c7661db5f521a061f37bdda3595acbd4ef07b9

ONX_JDP_ADV_CONTEXT__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: c3a18b9c6b8bb0cdd16381c86a6fc8423a67cb2fe229b757de543a5253c9fe0f

The new exact-zero performance bracket is a specialization of retained p1 on this region; old upper statements are unnecessary here and remain unchanged elsewhere.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 028c513bed6bb31e26e8bd9f73dd5ca774a7c3daebe25a58491eb63d70ed8bce

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 2887c86586e5b331c15ef41d6a1d1c2bc9d4b302f6ef6fb221a8a4a29ff39b2e

Not selected in the exact-zero regional comparison.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 8712023087c229d8bdd7314624a677b4318ee7fa1b49dcade5f387d12f653711

ONX_JDP_ADV_CONTEXT__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: c6a287e2c0154536db6b5ee7677cfb266a9997ff520cfff2265c8242d7d0fd37

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: c3a18b9c6b8bb0cdd16381c86a6fc8423a67cb2fe229b757de543a5253c9fe0f

The new exact-zero performance bracket is a specialization of retained p1 on this region; old upper statements are unnecessary here and remain unchanged elsewhere.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: c89362c78d149f67f9e4abe54872cf63e3c808c4544a249b3200df9b4ad1fc22

Fixed main/g1 contract: integers T,d>=1; B,S,sigma,L_tilde>=0, L>0, epsilon_priv>0, 0<=delta_priv<1 and 0<delta_conf<1; predictable history-dependent action sets and the frozen bounded linear reward/noise model.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 163194f2d02ad7704cbaa6c5d4ab9a5b98c3b99bc69d3dd9afdd60e0b84c3372

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: fb5f8d8b61aad8599ebcada706e6af83df2bab149adf06107fa397aaa082b8f7

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_upper_20261116

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 572e34c0d7d336563544b199f9a95ef5a90dd66472c2fe618a63f9c4a4427054

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: b697909db19b8d88a47250a808dab636cb6ad646ce01632d6c94b1693471841d

This statement certifies only r1 intersect (B=0 or S=0). It supplies no positive-scale lower bound and leaves the old full c1 missing_lower state unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: cd98fa50f354055f619a1056d8e03b9b6bcf3b10aefd0506c09deffa7f400cda

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: c90d4d4727cf9e9da3c76437f3e87e43f13864ea6ebdd6482532b370126e28c9

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_lower_20261116

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 572e34c0d7d336563544b199f9a95ef5a90dd66472c2fe618a63f9c4a4427054

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: b697909db19b8d88a47250a808dab636cb6ad646ce01632d6c94b1693471841d

This statement certifies only r1 intersect (B=0 or S=0). It supplies no positive-scale lower bound and leaves the old full c1 missing_lower state unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: e43285a8ba246aaf7ac552a11e51b40d49bbf272be4b3e3b9d1e03c8e0bf3808

ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 0036340799608384959b9555088db2d2362cbfd336cb0733b5ea6fe704773128

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 31288a7b70a9a55f8e78d5b2bf48d0f150a22f44ffc0c68a7a2bc15d8bd55e69

B=0 or S=0 makes every admissible action mean zero. Privacy and confidence ranges remain those of r1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: b0e96516a8e0ec71cbed8d7c15e03d7d232124090bc12fbaf93f4629f6e624d4

This is a performance-value closure, not a zero-observation algorithm.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 962a14402564f752326661b018433414e0791fc8c7b25deb034b14442aa49053

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/0; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/1; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/2; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/3; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/constant_dependencies/4; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 962a14402564f752326661b018433414e0791fc8c7b25deb034b14442aa49053

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/1; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/2; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/3; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/4; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: e7390c8b69f6e4da9ef8cf2a51d5b96ad672732f5d95f69fdfd0d6c5acdc8404

No multiplicative ratio at exact zero pseudo-regret; N=T observations remain.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 6f5ea4e6f232a8f4702e1bb26f741b0b2c2c7445f9f8f015f1ffc8cd509c62f9

0 on ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 94d84715723d2655dc067d88e7d7f06e744622aff60df681cb96ffeeb4cebc01

No regret-value gap on this region. Positive-scale c1 and outside-r1 science remain partial.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 6f5ea4e6f232a8f4702e1bb26f741b0b2c2c7445f9f8f015f1ffc8cd509c62f9

0 on ONX_JDP_ADV_CONTEXT__main__r_zero_regret_20261116

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: f77ae4f5de12ec60948ff77d05e436094d0693a8318b2f35447c54f7b4449821

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: dea71f051f9b91669f182c4c077fc4cead02de5c9e20dbd77b1c7030aab2b628

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 9ac6243697e1395aa955e0a72b544351270275d4272fb6fe09e0e25578bce7d9

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: db8321aa7895c875dfd3d17ac924c117e03e6b3f09cbb3fbb05364a32c3cb4c7

r1_zero_means

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: ad62be6536ce6c7efa5c7cbfc194bc8cdabd403aaff415e61071dd3d3294a997

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/1; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 1b559115b8a3a40a970b42ddac7fea8484af93c9bf418162e6e819e82f097adb

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 0782e4688e8581b6eb611e4180ec7f29945884caa150af5ebc3314ab1432f74f

Native c_zero_regret registers exact pseudo-regret value zero by p1 and its specialization. It uses the same q1, main/g1 and online resource with T selected-reward observations. No exact_cost=0 or zero-query attribute is present.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: fc42a4b29e6dbd304a2ff1311c67f10f006774f1d8b4b874326a07c1684a4db3

r1 AND (B=0 OR S=0).

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 48e741f74d317c82bf13bd1769522a0302728086d0d805e4e93de9fdd6e8d13c

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: ad6d3396132b4ce3369e6dd4a31f6276067c853d7d7305c251d4b8e231d030f3

r1_positive_scale

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: c6edbf397674cc58d415763430c6757b0c5959fa69246f2bac17f778b8dbb664

The learning upper and exact diameter cap are assembled. A positive high-probability lower bound is missing from the registered bracket.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: fe7db6df00783562b25937ed78885056488cdb6f3535cf69b680357540fdfcfd

r1 AND B>0 AND S>0.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 9503e4247b8b754774db11b2b8274b26ab7eda8ca0616470103bfea0b73e477b

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: a2bc8e5f606b08e4f15ba5627282c37e9a68a3410b6478661af2679d3035e44a

outside_r1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 7a3acdbb5918ae9cac97b1592cd708310aaad5c68493f453e4a05e037c050f05

Includes T=1 and the remaining privacy ranges. No native comparison or algorithmic adoption is added.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 05c84a36335857465de1bce0f4c65a0a723191e19b05c23472d333f982b80dd5

Full contract AND NOT (T>=2 AND epsilon_priv<=1 AND 0<delta_priv<1/e).

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: e47d262660a8a50bd8f960eb266e7b72210cf72d6136c5db7f48320a4a2c1e20

Within the fixed contract, r1 and its logical complement partition the domain. Because L>0 and B,S>=0, r1 splits disjointly into B=0 or S=0, versus B>0 and S>0. sigma=0 and L_tilde=0 remain inside these cells without an unsupported special branch. Accounting is not scientific certification of every cell.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: d8cb8c14f31f4108b5901286185dfabcce30b3d8377c088c7d1b9feb6c3977f5

No points omitted from domain bookkeeping; outside_r1 is scientifically unassessed. Sharper bounds and the positive lower side inside r1 also remain pending.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: a15f84756931c8211a806863b19aac6f676554da731ed6be6d25183ea0a4f6e5

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: d1f31c56e05540b8317bbcb62fee3e0114f8c820831b1672151500a6bf3057e1

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: d2de17ad7422d3d900160ac823424b89136b9c85a506ab91dce30df2b6ef0b2b

For every feasible action a, |<a,theta_star>|<=||a||_2||theta_star||_2<=LS by Cauchy-Schwarz and the frozen norm bounds. The independent mean bound also gives |<a,theta_star>|<=B. Thus comparator and selected-action means lie in [-min{B,LS},min{B,LS}]; every nonnegative pseudo-regret summand is <=2 min{B,LS}. Summing yields 0<=R_T<=2T min{B,LS} pathwise. Apply this inequality to the SAME admissible private strategy retained in b1 on r1: actions, privacy parameters, output and T selected-reward observations are unchanged. If its old event is R_T<=C F with probability >=1-delta_conf, intersection with this probability-one inequality gives R_T<=min{C F,2T min{B,LS}} at the same confidence, without algorithm selection or union-bound loss. F denotes exactly the explicit rate inside b1's O expression; C is a retained admissible constant. B=0 or S=0 forces exact zero regret by nonnegativity, while the observation budget remains T. The inequality is valid throughout the contract, but native algorithmic adoption here is restricted to r1, using its retained witness. No positive lower bound or matching minimax saturation threshold follows. The zero-mean boundary is exact; positive-scale crossover F of order T min{B,LS} is asymptotic because C is unspecified.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: c6ffcfc2f4aaf9e27a11f71e9ac7baf58b8f3f00d099dc92bd522477aa4ca032

bounded_mean_cap

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: d262f5db23c02337b69596da4b2fb6c9bf48b9b9cc540c899c7795db0603a783

Positive-scale joint families with F/[T min{B,LS}]->infinity; also exact zero-mean endpoints where the old displayed formula was positive.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 16c3fc23712a419c2a1b445d854100b92867f9e7e27ac547e69642fe085fd2e0

On r1, with probability >=1-delta_conf, R_T<=min{C F,2T min{B,LS}}, where O(F) is exactly b1's displayed formula and C is a retained admissible constant. No positive lower bound is added.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 882d0d0b1d40e2180a02a1bb8b64c3cfeec9eb65819e66abf99a0f276d41b067

If F=o(T min{B,LS}), b1 retains its asymptotic rate. At comparable scales no precise constant-factor improvement is certified. Outside r1 no bracket is changed.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 10060b96d6fb5c64cfb8d92d46bca76b65f1cec6abccd300d1aa9b98e485e78d

B=L=S=sigma=1, L_tilde=2, d=1, delta_conf=1/4, delta_priv=1/10, epsilon_priv=T^(-2): old F superlinear, cap 2T. B=0 is separately an exact zero-regret endpoint.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 7b0e6afbe5d5da3e57e4318a9c384db4fabf64919b2050631f005b1302f81682

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: a2b36b353eb95563860ab4ae7816a7589c160b5403c3edd89d5060009997cbb6

This result supplies no eligible native bound as stated and has no active bracket reference. Its screening is separate from the contract-derived cap.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: e9d442cc8897416006ab4a73e912ba177d2952bc62c91044d31f98e5a6fdb3d4

arxiv_2404_09413v1_stochastic_contexts

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 50446632d7eed558fb7d733ed5a6dd99640a04b4464028aab864dc38ad6db49e

None established.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: a7dd2fbb66c65b6026fe835a0f4f2869d53847ff596998589471496f6f788f77

The paper's stated model/guarantee; no adoption into this target.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: e550b1ba8061a64a62a8852fb0c685fc418c5698d78bfeb6a41dcdceeb91951c

Li, Simchi-Levi and Wang, arXiv:2404.09413v1, 15 April 2024, Section 1.1, PDF pp.3-4, read 5705:10000: the model assumes i.i.d. stochastic contexts and finite actions, and defines expected regret. Footnote 1 explicitly says its analysis does not handle adversarial contexts. Stronger local privacy alone does not remove these restrictions or establish this target's uniform high-probability guarantee. No upper transfer is adopted.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 4ae0978c70c48c23ca613b69bfcaf6ff4ac06974c9fb7e007e2bf0f0fff394bb

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: a2b36b353eb95563860ab4ae7816a7589c160b5403c3edd89d5060009997cbb6

This result supplies no eligible native bound as stated and has no active bracket reference. Its screening is separate from the contract-derived cap.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 47d522b9ac6cae17c0a6d23c507977eb1efcebdbf8f19a24046298e785e3d325

arxiv_2207_03445v1_fixed_actions

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 50446632d7eed558fb7d733ed5a6dd99640a04b4464028aab864dc38ad6db49e

None established.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: a7dd2fbb66c65b6026fe835a0f4f2869d53847ff596998589471496f6f788f77

The paper's stated model/guarantee; no adoption into this target.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 1e422ca7569abe0cc65cebefc64782e909f32e03d7c0d96cacc75d6352b153a2

arXiv:2207.03445v1, 7 July 2022, Section 2 and start of Section 3, PDF pp.3-5, read 8000:18000: the action set A is fixed, adjacency protects reward sequences only, and elimination repeatedly samples chosen arms from the fixed set. Its advertised sqrt(T)+1/epsilon upper is not a uniform algorithm for predictable varying action sets with joint context/reward adjacency. No transfer or new native bound is adopted.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 346f43c48afbc2fa7f83e27dce2daceda57e00267921efb98963928062d5e528

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: a2b36b353eb95563860ab4ae7816a7589c160b5403c3edd89d5060009997cbb6

This result supplies no eligible native bound as stated and has no active bracket reference. Its screening is separate from the contract-derived cap.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 45dae854ff0d1388728f2b07b9cf841903dd5e470e1b5e60a29be886bb293a6e

jdp2018_pure_expected_lower

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 50446632d7eed558fb7d733ed5a6dd99640a04b4464028aab864dc38ad6db49e

None established.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: c227aef2d702bf9358a34c1ce9df2da4dd740c2bc42355ba66cd1391670819e9

The uncapped upper b1; no registered lower bound.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: a7dd2fbb66c65b6026fe835a0f4f2869d53847ff596998589471496f6f788f77

The paper's stated model/guarantee; no adoption into this target.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: d127584c2434c775416a2029376a2fc3e55dc9d18402e6c827a7d68aad54ced9

Shariff-Sheffet, arXiv:1810.00068v1, 28 September 2018, Section 5, Claim 14 and Corollary 15, PDF pp.8-9, read 28000:38000: the MAB privacy lower bound concerns pure epsilon-DP, an expected sublinear-regret class, and asymptotic fixed gaps. It does not directly lower-bound the larger approximate-JDP class in r1 or give the native arbitrary-confidence guarantee. Claim 13 instead concerns standard DP of the whole transcript. Neither is adopted; no unproved subclass or probability conversion fills the lower side.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: a75c94a955711f84e7b174770cd563ebbb973dea61267c1a747dc730af567280

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: fc4c9f7c911698bb4fd0d9d494fdab3547c70f8274e0e02505eb88aa913e9037

The native region selector and certificate now expose the already-proved consequence as a matching regret bracket. The performance value zero is not a complexity or observation count.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 1b559115b8a3a40a970b42ddac7fea8484af93c9bf418162e6e819e82f097adb

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: ac3f96f434d28bd7318ad4b2f638b50a0443a8334514216a8dc99a405d338523

ONX_JDP_ADV_CONTEXT__finding__register_zero_regret_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 6aad8fb0c497c1f1d2b4f037fa93de7652679efd309285af0624adc85cca6129

Publication of an already proved regional regret-value equality only; no new rate, larger source domain or observation saving.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: fec6cff0e35dad14eddede25bc407a31b2374eb8d834568d31513c8088544cc2

Independent native optimal comparison with upper=lower=0 on r1 intersect (B=0 or S=0).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: f1f2bbd1a1db828a044beaa1ece5a8fadbb69ff609adb894721e5f895f0edf58

p1 already proves exact zero pseudo-regret on the mean-zero part of r1, but the full c1 comparison remains missing_lower.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: c79239dbf4b3f233114d418ff99216b41deff1ef06aeba01d23287b01eb0040c

Old full c1 inequalities/missing_lower state, all positive-scale points, outside-r1 science, privacy and observation budget.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 7154d5315031935f63710a9361397f8d94f1d994c1c32e76b1378ee3fe59ae8d

r1 AND (B=0 OR S=0), with the unchanged T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 conditions.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 16e08ff18b54b57de3e3cc69dde26d2cdd72bb586e6c8c043819d28f866f81fe

Each pseudo-regret summand is identically zero when B=0 or S=0, by retained p1; T observations remain.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: 5ae3a2151e8e7e016644e3943ebf5a6b748e8d213ab68bf6ab9c9ead4452536c

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 56d9e66e2b9e81d38efa09f7945f6b7dcc51e209c7f0ffd714ef558bc9d54771

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 7510b4861d22051445a30a0c3be60f7ae2f7d4f2cb5cff9e3c9be098a06ba843

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: c39d9cd49fbd846ace958410a24e5f3e32ab83a83b884f77e829af4285adb910

curated_feedback_ONX_JDP_ADV_CONTEXT_20261116_2a144b4edf

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: c9ffb5563d355e926c473cd07169e9b1c0a9af5b12f3acb883ee8b306067f24e

Fixed main/g1 contract: integers T,d>=1; B,S,sigma,L_tilde>=0, L>0, epsilon_priv>0, 0<=delta_priv<1 and 0<delta_conf<1; predictable history-dependent action sets and the frozen bounded linear reward/noise model. Optimize the native main/g1 minimax high-probability cumulative pseudo-regret jointly in T,d and the three privacy/confidence parameters, for each fixed admissible structural tuple. No precision coordinate is introduced; the new exact cap is also uniform in all structural parameters.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: b5f352e940837874f6f1b12ddffeff56a3a37cae6abc2c143c156e9f28078fac

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: c7c4e5f379df858cc48a1d9f49c057ed2cc4c3888d8ab138a7ba6cff32e3ed65

arXiv:2602.00417v2: verify identity-link specialization, reward-law assumptions, full Theorem J.8, all-T branches and explicit constants before transfer. Hash ca9337688c368cf4bc35aa1984ed6c4410e333663b350c0ae00d0355dbe740be; only characters 0:10000 and 30000:36500 read; decisive formula extraction remains uncertain.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: aa73c0a52c88821e5a15c35dbcdd0adf8bbce20d0942b8a231c7f60f99f0a1cf

Identify and read Chen et al. (2025), cited in arXiv:2602.00417v2 Remark 6.4, and the Azize-Basu 2024 linear-bandit results; check predictable contexts, joint context/reward privacy, confidence and cutoff.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: edb7c791513551c4c22fbe703081ad457fc5e3c589e936683d78379af570deb3

Read arXiv:2405.14038v3 (FLIPHAT) lower-bound assumptions; prove any bounded-reward subclass transfer and expectation-to-high-probability conversion.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 55b07f1c96114661f500e767dc7b1372fe09d73bc0b415c51410362bb976e4a2

Read arXiv:2202.05567v1 and 2112.06008v1 shuffle upper bounds for exact timing, trust assumptions, predictable contexts, parameter dependence and JDP containment; only metadata was examined.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 747676d2ebf8a94d94699fb69e4d550591d90bd8f37b95bb10c326fc2bf9e790

Assemble a bounded-reward nonprivate high-probability lower transfer, including d=1, sigma=0 and large-d/T branches; no such theorem is adopted.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 61a1e2d45da60c24f7739cb2b04710fe0f1287a293fa653a98231d676c7c118e

Outside r1, T=1, delta_priv=0, epsilon_priv>1 or delta_priv>=1/e remain unassessed for native adoption. The diameter inequality alone is not a complete bracket or an admissibility proof there.

#### Native item 7

Native pointer: /joint_analysis/pending_obligations/6; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 0e000f8ae88057b87cffbd3618528c071b327dac8cf74a34f3744664692d9ecc

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 291a051b8caeb3ef77b28883ee413a514cfd8b0127cd199e7fd23b573cebced1

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: a03f0e47c1aa5504c4e0df90c0c7661db5f521a061f37bdda3595acbd4ef07b9

ONX_JDP_ADV_CONTEXT__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 7992a5860d10d55f2a7d18decdbe5dc724ec731437bc1fc2f068da070bfe0227

Unchanged source n=T, alpha=delta_conf and privacy mapping, selected scalar reward per round and max{1,B} normalization from the baseline.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 90f1a8dbd14e7444a73f2d066637bca002cf4997b75eecbda8c3a2a5ea5a788a

Frozen /bounds/0 and /evidence/0; Corollary 12, arXiv:1810.00068v1, PDF p.8. Archived hash f6b60c8d7e4318ad5d8a3a927be968a32a79c550dbf4593b17d4ea3381ae5de5 read 28000:38000. Conditional retention, not fresh certification of all old premises.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 87ec60efb24d27e6a1c3eb60cea25db0782c14fe65a8ccd85e92d2d7282597ab

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: a800a02878f997244f874707250aff2f493ef28852905ea7367b8362658a210c

ONX_SRC_JDP2018

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 604f5d5cc1624c079101b4ed32ad0b44a27e061c33bb399d3fe3890fcb537774

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 8712023087c229d8bdd7314624a677b4318ee7fa1b49dcade5f387d12f653711

ONX_JDP_ADV_CONTEXT__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 40b04c9b66302ae103602a2fcb79f871e46437a4f13650b039113d67d5585a2e

Cauchy-Schwarz and the mean bound control every regret summand. Apply the exact inequality to the same retained admissible private strategy; all resource and guarantee contracts are preserved.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: c6a287e2c0154536db6b5ee7677cfb266a9997ff520cfff2265c8242d7d0fd37

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: c89362c78d149f67f9e4abe54872cf63e3c808c4544a249b3200df9b4ad1fc22

Fixed main/g1 contract: integers T,d>=1; B,S,sigma,L_tilde>=0, L>0, epsilon_priv>0, 0<=delta_priv<1 and 0<delta_conf<1; predictable history-dependent action sets and the frozen bounded linear reward/noise model.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: b6959f9c4d286b5cb5ce89cbe6d0cc7fba969c39e56884eac49f664bc4bf52de

Fully read frozen /common_specification, canonical hash 16b7929fd4c7e616448fc5393657f56a795ae4544a7fe7b8838f88816b52aa5e; complete premise hashes and derivation in ONX_JDP_ADV_CONTEXT__main__p1.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: ae2b7f6ff9b04a8b26da46680dfbc4a64a12bc1958a250d2a0406d45db406c4c

Fixed contract with T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 (unchanged r1).

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: f7baa00b76528aa7e39a21af79025d507de14fe06f37580af149274691c2e478

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: fb5f8d8b61aad8599ebcada706e6af83df2bab149adf06107fa397aaa082b8f7

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_upper_20261116

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 58f77fd571b3d668be113913210b86578dd6133d5b6ae9a7fb69154f33a84ace

Restrict p1 to the mean-zero region and use pseudo-regret nonnegativity. Preserve the same native quantity, online protocol and T-observation budget.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: ad62be6536ce6c7efa5c7cbfc194bc8cdabd403aaff415e61071dd3d3294a997

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native item 2

Native pointer: /joint_analysis/provenance/2/proof_refs/1; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: b0872fc85d965598f96d6ad32ef663a761d13b61f6696d97bb5b3c5bbab7e2fe

The p1 pathwise bound on r1 with the fixed public bounded-mean and parameter-norm promises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: faf6e682d5ea696109c7f00590ba0b9a4c98cc9b2b3baa5f25efdaee80f66d88

Retained native p1 proof; no new external source theorem.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 7154d5315031935f63710a9361397f8d94f1d994c1c32e76b1378ee3fe59ae8d

r1 AND (B=0 OR S=0), with the unchanged T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 conditions.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: c7937b1ea6eaacb3842b28cf12c3bae01becbca0c9a25ebf09a313a9eac35722

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: c90d4d4727cf9e9da3c76437f3e87e43f13864ea6ebdd6482532b370126e28c9

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_lower_20261116

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 58f77fd571b3d668be113913210b86578dd6133d5b6ae9a7fb69154f33a84ace

Restrict p1 to the mean-zero region and use pseudo-regret nonnegativity. Preserve the same native quantity, online protocol and T-observation budget.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: ad62be6536ce6c7efa5c7cbfc194bc8cdabd403aaff415e61071dd3d3294a997

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native item 2

Native pointer: /joint_analysis/provenance/3/proof_refs/1; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: b0872fc85d965598f96d6ad32ef663a761d13b61f6696d97bb5b3c5bbab7e2fe

The p1 pathwise bound on r1 with the fixed public bounded-mean and parameter-norm promises.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: faf6e682d5ea696109c7f00590ba0b9a4c98cc9b2b3baa5f25efdaee80f66d88

Retained native p1 proof; no new external source theorem.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 7154d5315031935f63710a9361397f8d94f1d994c1c32e76b1378ee3fe59ae8d

r1 AND (B=0 OR S=0), with the unchanged T>=2, 0<epsilon_priv<=1, 0<delta_priv<1/e and 0<delta_conf<1 conditions.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 3603a6c03b20ae0c9a87923a3568eb25848a5c8836548f865e1aade58389cfe1

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 7510b4861d22051445a30a0c3be60f7ae2f7d4f2cb5cff9e3c9be098a06ba843

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 3a7d444079b2c92b04eb83f448f13cbaf94055a44cc12c5dd8b0f66b1e07a313

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: cc4f162e41f3f8c62c856908e405d1776d97cb1971270d48a6bbc5ffb7f6622c

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 1266c089bb0e747763ccf04ceea8b2af31a8e6cad79a69ece70649d54d2fff9b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: a03f0e47c1aa5504c4e0df90c0c7661db5f521a061f37bdda3595acbd4ef07b9

ONX_JDP_ADV_CONTEXT__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 8712023087c229d8bdd7314624a677b4318ee7fa1b49dcade5f387d12f653711

ONX_JDP_ADV_CONTEXT__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: c90d4d4727cf9e9da3c76437f3e87e43f13864ea6ebdd6482532b370126e28c9

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_lower_20261116

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: fb5f8d8b61aad8599ebcada706e6af83df2bab149adf06107fa397aaa082b8f7

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_upper_20261116

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 1fe37637337aa6771fd07e8f07f1113f730f77263d24d44ff81fce9970305ac2

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: c7c4e5f379df858cc48a1d9f49c057ed2cc4c3888d8ab138a7ba6cff32e3ed65

arXiv:2602.00417v2: verify identity-link specialization, reward-law assumptions, full Theorem J.8, all-T branches and explicit constants before transfer. Hash ca9337688c368cf4bc35aa1984ed6c4410e333663b350c0ae00d0355dbe740be; only characters 0:10000 and 30000:36500 read; decisive formula extraction remains uncertain.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: c4c65404c3aa1502d1a20bb361a3fb21010beaf6d7bada8ffc6168063383ff84

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: aa73c0a52c88821e5a15c35dbcdd0adf8bbce20d0942b8a231c7f60f99f0a1cf

Identify and read Chen et al. (2025), cited in arXiv:2602.00417v2 Remark 6.4, and the Azize-Basu 2024 linear-bandit results; check predictable contexts, joint context/reward privacy, confidence and cutoff.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 2bdf126e14a16a88e1f09db153ff557ef7c518f03047f8d66bd6b73c28c5cef1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: edb7c791513551c4c22fbe703081ad457fc5e3c589e936683d78379af570deb3

Read arXiv:2405.14038v3 (FLIPHAT) lower-bound assumptions; prove any bounded-reward subclass transfer and expectation-to-high-probability conversion.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 3fed053329dea4553c545b8ad0fb2b7aedb93abc87aab6be090e364da807664e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 55b07f1c96114661f500e767dc7b1372fe09d73bc0b415c51410362bb976e4a2

Read arXiv:2202.05567v1 and 2112.06008v1 shuffle upper bounds for exact timing, trust assumptions, predictable contexts, parameter dependence and JDP containment; only metadata was examined.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 9aa9651de4bdccbc6ea0ebda53ec986050ddc008be8354b0a1ed39a19144c1e3

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 747676d2ebf8a94d94699fb69e4d550591d90bd8f37b95bb10c326fc2bf9e790

Assemble a bounded-reward nonprivate high-probability lower transfer, including d=1, sigma=0 and large-d/T branches; no such theorem is adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 66368b01e57b2b9e808551aa78702899713a9992844fc155c0041511c8b1f56d

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: fcdc34f896045ad30a0d0e0ab2455abdd393a1ed265843d758f460732da7bc7d

Explicitly unassessed retained work; this migration neither resolves it nor identifies it as a proved literature-open problem.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 186e0420e5e0ed990878ebea142dc16d4547b8e14bda02b17ba5da46fcde7813

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 816e64d45ab01655b0cdb3174cc88338b9552319d4504b2ed46ed2504883fbc8

retained-material-lead-5

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 61a1e2d45da60c24f7739cb2b04710fe0f1287a293fa653a98231d676c7c118e

Outside r1, T=1, delta_priv=0, epsilon_priv>1 or delta_priv>=1/e remain unassessed for native adoption. The diameter inequality alone is not a complete bracket or an admissibility proof there.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: c452764d2a2af58e710caab32941060f3f19179f1e81bda0c3e19f09807fa7ce

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: 519bd8ca57c3e11102083b6e12404b51f0377571d87cb5f64e739292e3fc7126

The same-contract candidates are explicitly accounted for in the new regional ledger: select exact upper/lower zero, retain the two original upper statements conditionally as unnecessary on this branch. This changes no full-domain inequality.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 0dfc3fdbc9ad417b5e9611aef2c8042f58e4db2ada037fa87cc987d7ed45d90e

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/0; canonical SHA-256: a03f0e47c1aa5504c4e0df90c0c7661db5f521a061f37bdda3595acbd4ef07b9

ONX_JDP_ADV_CONTEXT__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/1; canonical SHA-256: 8712023087c229d8bdd7314624a677b4318ee7fa1b49dcade5f387d12f653711

ONX_JDP_ADV_CONTEXT__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/2; canonical SHA-256: fb5f8d8b61aad8599ebcada706e6af83df2bab149adf06107fa397aaa082b8f7

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_upper_20261116

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs/3; canonical SHA-256: c90d4d4727cf9e9da3c76437f3e87e43f13864ea6ebdd6482532b370126e28c9

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_lower_20261116

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: d3365650118b3e8dc1f799d311c570df618b80eca185057d07356827d7d1b889

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids/0; canonical SHA-256: db8321aa7895c875dfd3d17ac924c117e03e6b3f09cbb3fbb05364a32c3cb4c7

r1_zero_means

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 1b559115b8a3a40a970b42ddac7fea8484af93c9bf418162e6e819e82f097adb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 8b2e21f49118312df22d6cf7db0f541ceb8edbe3c52388f2940c752056fef474

typed-compatible-zero-regret

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: ad62be6536ce6c7efa5c7cbfc194bc8cdabd403aaff415e61071dd3d3294a997

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs/1; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 9

Native pointer: /joint_analysis/synthesis_coverage/obligations/8; canonical SHA-256: 2c15a7dc260fc60fb4248e93a0c5f17007d2a2d4162c51407122a5e2a6d7bc88

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/argument; canonical SHA-256: 1c38af18ccbe0c61d91e877161921ee956736056c10bc5d7cb81be3d483c53e3

The new native optimal comparison and two explicitly guarded performance bounds register the exact zero-regret equality proved by p1 and its specialization. This resolves publication only; no zero-observation or positive-scale closure is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs; canonical SHA-256: 3942e80b0de9c092037984233bade7500580e60952b4df3c2f08eac0150c09bd

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/0; canonical SHA-256: fb5f8d8b61aad8599ebcada706e6af83df2bab149adf06107fa397aaa082b8f7

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_upper_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/bound_refs/1; canonical SHA-256: c90d4d4727cf9e9da3c76437f3e87e43f13864ea6ebdd6482532b370126e28c9

ONX_JDP_ADV_CONTEXT__main__b_zero_regret_lower_20261116

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids; canonical SHA-256: d3365650118b3e8dc1f799d311c570df618b80eca185057d07356827d7d1b889

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/cell_ids/0; canonical SHA-256: db8321aa7895c875dfd3d17ac924c117e03e6b3f09cbb3fbb05364a32c3cb4c7

r1_zero_means

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids; canonical SHA-256: 1b559115b8a3a40a970b42ddac7fea8484af93c9bf418162e6e819e82f097adb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/comparison_ids/0; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/id; canonical SHA-256: b71f1a97e433eddef053f9fec96a003bcafc677780c1a5441cd8517bf0cac062

typed-publish-zero-regret

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/kind; canonical SHA-256: 50133df05f664fa7a089f5165d8e064594aa92d2dedff6eb73c481199b11b5cd

closed_region_publication

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs; canonical SHA-256: ad62be6536ce6c7efa5c7cbfc194bc8cdabd403aaff415e61071dd3d3294a997

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs/0; canonical SHA-256: 4e83e3e2e4e17a1d856f045f55b19cb7d8f7d33c832c60f36a0471bb1464e05d

ONX_JDP_ADV_CONTEXT__main__p1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/proof_refs/1; canonical SHA-256: b6a58d67ecdb8327008807c106012785d97d08436597efb2b1f3543bc0be74ca

ONX_JDP_ADV_CONTEXT__main__proof_register_zero_regret_20261116

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/8/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 10

Native pointer: /joint_analysis/synthesis_coverage/obligations/9; canonical SHA-256: a37f56f1863ca7ace798c6806e7375c65a294fb35a54fee6c0eb27ae87d2c70a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids; canonical SHA-256: 7510b4861d22051445a30a0c3be60f7ae2f7d4f2cb5cff9e3c9be098a06ba843

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/0; canonical SHA-256: d2a8187d40362a21c0299d537b5c000d4358840c592d571aa29b3e7340e4850c

ONX_JDP_ADV_CONTEXT__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/comparison_ids/1; canonical SHA-256: 6c5c4c27f1d2d352488b95792ff94266652f3436db7b1b812ca3cdee2e856031

ONX_JDP_ADV_CONTEXT__main__c_zero_regret_20261116

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/id; canonical SHA-256: 7b66618750ce506ccf40819cef50f764846b4ebf660cc36789c8ef551ca05dfe

curated-scope-limit-2a144b4edf

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/9/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 5efaf3c4bce6f6695b138b4f21406db1671486da61305ac4eb6abb3a2b10806d

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 962a14402564f752326661b018433414e0791fc8c7b25deb034b14442aa49053

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native item 4

Native pointer: /joint_analysis/target/allowed_constant_dependencies/3; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native item 5

Native pointer: /joint_analysis/target/allowed_constant_dependencies/4; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: ae7a4f4c57d65546fee1f86a43b98d8c23c8d1767a283c535d685324fa534abb

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 8c85ebc02f99d6f50afe439708033fa173119840372b5528121db24f5a4d488d

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 00743be3fb54c934e92197c7ca4d35c8eb38a80029d799678e9d6378b0fb0bbc

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 6af3fa72bf44df8bc471a1dcd94446eb6b4f1fccbe355a5417228d49ec35c54b

B>=0, fixed structural mean bound, including B=0.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: aa727bfe43db3a9136b156f52cd3ad030d2f2adbf41b8b86b25450b777471207

ONX_JDP_ADV_CONTEXT_p_0f75425378

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: f75dc3e52c57a8897b78532a93d1304278e51706ed240aa87824305d764825c5

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 1b399f4607207cfa1587436abc01863c93113f919a6bce4629dbf21be921a97c

L>0, fixed structural action norm bound.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: d7c9bcd919d0658b3c4d2c1801ac8f82a9d0d8c5e197c7caac81bea4684b9e1b

ONX_JDP_ADV_CONTEXT_p_ab84939b9e

#### Native item 3

Native pointer: /joint_analysis/target/fixed_parameters/2; canonical SHA-256: 4dde10343baff561f28fc03de48a96f728e213b4b824c7143c73420b8c56d30b

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/2/domain; canonical SHA-256: a96fe636b52ba32cd99aa6e87711f4b2b9eebe00731a22c602f1a536d57725ff

S>=0, fixed structural parameter norm bound, including S=0.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/2/parameter_ref; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/2/symbol; canonical SHA-256: 0253feeea38958629d7c744f6f675840195ecdf0e0751c290540e6446b2ba836

ONX_JDP_ADV_CONTEXT_p_f4d67bcd40

#### Native item 4

Native pointer: /joint_analysis/target/fixed_parameters/3; canonical SHA-256: 32cccb920a1ed272230874f801d0dc7e2c298faf01878027e958d2dc113ab677

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/3/domain; canonical SHA-256: 11f5dfa267fe9c00db8ffc81d2bea383993d3c7c6d3ab6bed2eea7e3b09700da

sigma>=0, fixed conditional noise bound.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/3/parameter_ref; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/3/symbol; canonical SHA-256: ab4cb68f1f4f0dbcaf1aa0d4a42716a810aa90fcf53ff5dc8be6ae9267454a7a

ONX_JDP_ADV_CONTEXT_p_9e2f1be437

#### Native item 5

Native pointer: /joint_analysis/target/fixed_parameters/4; canonical SHA-256: d456f007287732d2849bf30f3f9b5ceb96e79609233cff177b835d25e9cc04a4

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/4/domain; canonical SHA-256: 22cbcaad4d07678efb37ac7184415fae0f9c4ed2ed66fd236c2821de581d94f4

L_tilde>=0, fixed realized action/reward norm bound.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/4/parameter_ref; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/4/symbol; canonical SHA-256: 1dba9afcd65cd76008ddb7f2f621310144923f12b8c56d811ecd55ac0809eb93

ONX_JDP_ADV_CONTEXT_p_ff43ceaf7a

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: c9ffb5563d355e926c473cd07169e9b1c0a9af5b12f3acb883ee8b306067f24e

Fixed main/g1 contract: integers T,d>=1; B,S,sigma,L_tilde>=0, L>0, epsilon_priv>0, 0<=delta_priv<1 and 0<delta_conf<1; predictable history-dependent action sets and the frozen bounded linear reward/noise model. Optimize the native main/g1 minimax high-probability cumulative pseudo-regret jointly in T,d and the three privacy/confidence parameters, for each fixed admissible structural tuple. No precision coordinate is introduced; the new exact cap is also uniform in all structural parameters.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 2623e53069e3f53fc4f3815d18a81f9faef0dea901887760b0f6da99145f8b5e

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 5d5adf13ef97a26cdf2b2dc87e0e16f407d7626c4d19d1b9cb0ad1186a353c88

ONX_JDP_ADV_CONTEXT_p_0c093224ff

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 39065fa76994585982bf4fe3f76556a4ef22d6d1362b07557f890c005a1d688d

ONX_JDP_ADV_CONTEXT_p_6e898943e7

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 49a3022760deec7dc98f5b6b3f7f24f7c717d671f4f9e608777fe61268c0db1a

ONX_JDP_ADV_CONTEXT_p_e9a6206170

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: fa10387fa01767aafe295fe56abedd3ac9d631448a5382df6511980b3fdb798e

ONX_JDP_ADV_CONTEXT_p_9f27ce45c8

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 90c899bc752341a0575b735c4befb81c9c5b938b7e57c2d8212e422f49b3d49a

ONX_JDP_ADV_CONTEXT_p_23f704c160

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 2623e53069e3f53fc4f3815d18a81f9faef0dea901887760b0f6da99145f8b5e

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 5d5adf13ef97a26cdf2b2dc87e0e16f407d7626c4d19d1b9cb0ad1186a353c88

ONX_JDP_ADV_CONTEXT_p_0c093224ff

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 39065fa76994585982bf4fe3f76556a4ef22d6d1362b07557f890c005a1d688d

ONX_JDP_ADV_CONTEXT_p_6e898943e7

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 49a3022760deec7dc98f5b6b3f7f24f7c717d671f4f9e608777fe61268c0db1a

ONX_JDP_ADV_CONTEXT_p_e9a6206170

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: fa10387fa01767aafe295fe56abedd3ac9d631448a5382df6511980b3fdb798e

ONX_JDP_ADV_CONTEXT_p_9f27ce45c8

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 90c899bc752341a0575b735c4befb81c9c5b938b7e57c2d8212e422f49b3d49a

ONX_JDP_ADV_CONTEXT_p_23f704c160

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Roshan Shariff; Or Sheffet. Differentially Private Contextual Linear Bandits. 2018. arXiv1810.00068; original NeurIPS2018 paper.

https://arxiv.org/abs/1810.00068
