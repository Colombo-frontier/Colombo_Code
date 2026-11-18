# Linear contextual bandits with conditionally sub-Gaussian noise and high-probability pseudo-regret

**Setting ID.** `ONX_LIN_CONTEXT_SUBGAUSS_HP`

Online learning and bandits

The current action set is revealed before play. The learner observes the chosen action's linear reward plus conditionally sub-Gaussian noise. The target is an instancewise high-probability bound on cumulative pseudo-regret. The optimal action may vary by round, and noise may be a martingale difference.

**Status.** Bounds missing; Other quantified gap present; Logarithmic gap present

**Gap classes present.** Other quantified gap; Logarithmic gap

The regional bracket below specifies the quantified gaps and their parameter dependence.

**TASK tags.** formulation: Onx lin context subgauss hp; task family: Online bandit

**MODEL tags.** structure: Linear

**ORACLE tags.** interface family: Selected reward; operation: Selected reward; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Pseudo regret

**GUARANTEE tags.** randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

The current action set is revealed before play. The learner observes the chosen action's linear reward plus conditionally sub-Gaussian noise. The target is an instancewise high-probability bound on cumulative pseudo-regret. The optimal action may vary by round, and noise may be a martingale difference.

### Admissible model

The current action set $\mathcal{D}_t\subseteq\{x\in\mathbb{R}^d:\|x\|_2\le L\}$ may depend on the past but is revealed before the action is chosen. The fixed unknown parameter satisfies $\|\theta_*\|_2\le S$. The source regret normalization requires the absolute mean reward of every admissible action to be at most $1$.

$$
Y_t=\langle x_t,\theta_*\rangle+\eta_t,\qquad |\langle x,\theta_*\rangle|\le1\quad(x\in\mathcal{D}_t).
$$

$$
\mathbb{E}\!\left[e^{\lambda\eta_t}\mid\mathcal{F}_{t-1},x_t\right]\le e^{\lambda^2\sigma^2/2}\quad(\lambda\in\mathbb{R}).
$$

### Oracle interface

The order is: observe $\mathcal D_t$, choose $x_t\in\mathcal D_t$, then receive scalar reward $Y_t$.

Causal randomized policies may solve the optimistic maximization problem over the current action set exactly. Inputs $L,S,\sigma,d,\delta_{\mathrm{conf}}$ are public and $\theta_*$ hidden. Advance knowledge of the horizon is not required.

Noise satisfies a conditional moment-generating-function bound and may be a martingale difference. IID Gaussian noise is only a subclass.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

The output is the complete action trajectory satisfying feasibility and timing requirements. Randomized mixtures may be implemented before acting. Retrospective averages or convex combinations cannot replace actions that have already incurred loss. No additional optimal value or certificate is required.

### Loss or accuracy criterion

$$
R_T=\sum_{t=1}^{T}\left(\max_{x\in\mathcal{D}_t}\langle x,\theta_*\rangle-\langle x_t,\theta_*\rangle\right).
$$

### Resource accounting

There are $N=T$ scalar rewards. Internal action maximization and matrix updates have separate arithmetic costs.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

All measurable causal randomized algorithms obeying the stated information protocol are allowed. No linear-span, zero-support, or specific iteration restriction is added implicitly. Internal computation and memory are unrestricted except for the explicit computation, communication, or privacy constraints.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

With the source confidence sequence, the pseudo-regret bound holds uniformly over time with probability at least $1-\delta_{\mathrm{conf}}$. It is not automatically a guarantee for reward regret that includes realized noise.

## 2. Notation and parameters

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

$\sigma$: Conditional sub-Gaussian scale of the reward noise **Domain:** $\sigma\ge0$.

For every $s\in\mathbb R$, $\mathbb E[e^{s\eta_t}\mid\mathcal H_{t-1},a_t]\le e^{s^2\sigma^2/2}$.

$\mathcal D_t$: The predictable current action set revealed before acting. **Domain:** $\mathcal D_t\subseteq B_2^d(L)$.

$\theta_*,x_t$: Fixed hidden parameter and current action **Domain:** $\|\theta_*\|_2\le S,\ x_t\in\mathcal D_t$.

Every admissible action has mean reward of absolute value at most $1$.

$\eta_t,Y_t$: Conditionally sub-Gaussian noise and the actual scalar observation. **Domain:** Real random variable.

$Y_t=\langle x_t,\theta_*\rangle+\eta_t$.

$\mathcal F_{t-1}$: The available history before the current action. **Domain:** Sigma-algebra.

History includes past actions, rewards, and revealed contexts. Current noise is not yet visible.

$\lambda$: The test parameter in the noise moment-generating-function inequality. **Domain:** $\lambda\in\mathbb R$.

The condition holds for every lambda; this variable is distinct from the ridge-regularization parameter.

$\lambda_{\mathrm{ridge}}$: Public ridge-regularization scale in OFUL **Domain:** Positive real number.

$\lambda_{\mathrm{ridge}}=\max\{1,L^2\}$.

$R_T$: Cumulative pseudoregret evaluated using the mean functions **Domain:** Nonnegative real-valued random variable.

$R_T=\sum_t[\max_{x\in\mathcal D_t}\langle x,\theta_*\rangle-\langle x_t,\theta_*\rangle]$. Realized observation noise is excluded from loss differences. Probability or expectation is specified separately by the success guarantee.

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
R_T=\sum_{t=1}^{T}\left(\max_{x\in\mathcal D_t}\langle x,\theta_*\rangle-\langle x_t,\theta_*\rangle\right).
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Arbitrary statistical confidence and time-uniform pseudo-regret, with $\lambda=\max{1,L^{2}}$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Lower bound missing

**Lower bound.** Admitted envelope

**Upper bound.** B1

$$
O\!\left(\sqrt{Td\log(1+TL^2/(d\lambda))}[\sqrt\lambda S+\sigma\sqrt{\log(1/\delta)+d\log(1+TL^2/(d\lambda))}]\right)
$$

### R2 - Positive-noise and fixed-or-higher confidence window

**Region.** $d\ge3$, $T\ge1$, $L,S,\sigma>0$, and $0<\delta_{\mathrm{conf}}\le1/32$. The lower bound uses fixed public action sets and Gaussian reward noise.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Other quantified gap

**Lower bound.** B2

$$
\frac18\min\!\left\{LST,\ T,\ \frac{\sigma(d-2)}4\sqrt T\right\}
$$

**Upper bound.** B1

$$
O\!\left(\sqrt{Td\log(1+TL^2/(d\lambda))}[\sqrt\lambda S+\sigma\sqrt{\log(1/\delta)+d\log(1+TL^2/(d\lambda))}]\right)
$$

**Gap or comparison.** Both envelopes hold on this window. Dependence on all public parameters need not match.

**Comparison argument.** Both envelopes hold on this window. Dependence on all public parameters need not match.

### R3 - Unit parameters and long horizons

**Region.** $d\ge3$, $T\ge d^2$, $L=S=\sigma=1$, and $\delta_{\mathrm{conf}}=1/32$.

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\frac{d-2}{32}\sqrt T
$$

**Upper bound.** B1

$$
O\!\left(d\sqrt T\log(1+T/d)\right)
$$

**Gap or comparison.** The lower and upper differ by at most a factor of order $\log(1+T/d)$.

**Comparison argument.** The lower and upper differ by at most a factor of order $\log(1+T/d)$.

## 4. Bounds and supporting evidence

### B1 - OFUL: self-normalized confidence ellipsoids and exact optimistic optimization.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
4\sqrt{Td\log(1+TL^2/(d\lambda_{\rm ridge}))}\left[\sqrt{\lambda_{\rm ridge}}S+\sigma\sqrt{2\log(1/\delta_{\rm conf})+d\log(1+TL^2/(d\lambda_{\rm ridge}))}\right]
$$

**Sources.** [1](https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf)

**Conditions.** Require $\|x\|_2\le L$, $\|\theta\|_2\le S$, and $|\langle x,\theta\rangle|\le1$. The noise is a conditionally sub-Gaussian martingale difference with parameter $\sigma$.; Choose $\lambda_{\mathrm{ridge}}=\max\{1,L^2\}$. A single event holds for all time horizons simultaneously with probability at least $1-\delta_{\mathrm{conf}}$.

**Oracle correspondence.** Preserve this setting's feedback type, within-round coupling, and historical information

**Guarantee conversion.** The accompanying argument states the native guarantee and necessary conversion.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**rewards.** T

**matrix updates.** T

**optimistic argmax.** Internal optimization over T public action sets.

**Constants.** Dependence is allowed only on parameters declared fixed in the applicability conditions.

**Logarithmic factors.** The displayed expression uses no notation that suppresses logarithmic factors.

**Derivation.** The source uses $L$ for the squared action-norm bound; replace it by $L^2$. Choose ridge parameter $\lambda_{\mathrm{ridge}}\ge L^2$ so that leverage scores are at most one. The self-normalized confidence radius and the determinant ratio in the elliptical-potential argument give the displayed bound, with 4 as a conservative constant. The criterion is pseudo-regret; realized noise is not included in reward differences.

**Source location.** [1](https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf) theorem: Theorems 2–3; ellipsoidal-potential analysis in Appendix C

The source uses $L$ for the squared action-norm bound; replace it by $L^2$. Choose ridge parameter $\lambda_{\mathrm{ridge}}\ge L^2$ so that leverage scores are at most one. The self-normalized confidence radius and the determinant ratio in the elliptical-potential argument give the displayed bound, with 4 as a conservative constant. The criterion is pseudo-regret; realized noise is not included in reward differences.

### B2 - Gaussian hard subclass and bounded pseudo-regret transfer

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All algorithm necessity: All randomized adaptive algorithms

$$
\frac18\min\!\left\{LST,\ T,\ \frac{\sigma(d-2)}4\sqrt T\right\}
$$

**Sources.** [2](https://arxiv.org/abs/2502.17175v1)

**Conditions.** $d\ge3$, $T\ge1$, $L,S,\sigma>0$, and $0<\delta_{\mathrm{conf}}\le1/32$. The lower bound uses fixed public action sets and Gaussian reward noise.

**Dimension conditions.** Ambient dimension $d\ge3$.

**Oracle correspondence.** The target permits a fixed public radius-L ball and conditionally Gaussian scalar rewards as a subclass.

**Guarantee conversion.** The source gives an expectation on one admissible Gaussian instance; the local tail argument applies to the fixed-horizon consequence of the target time-uniform guarantee.

**Output rule.** The complete causal action trajectory determines pseudo-regret; realized reward noise is excluded.

**Resource conversion.** One scalar reward per round, evaluated after T rounds.

**Local argument.** A1

**Source location.** [2](https://arxiv.org/abs/2502.17175v1) theorem: Theorem 2.1 and its Gaussian hard-family proof; section: Sections 1.1 and 2; pdf pages: 2; 4

The source proves an expected pseudo-regret lower bound. The Atlas proof below converts it to a probability bound on the same admissible instance using its pathwise cap.

In this preprint theorem the ambient dimension equals the dimension parameter plus two.

## 5. Local arguments

### A1 - From the Gaussian expected-regret lower bound to an anytime obstruction

**Scope.** $d\ge3$, $T\ge1$, $L,S,\sigma>0$, and $0<\delta_{\mathrm{conf}}\le1/32$. The lower bound uses fixed public action sets and Gaussian reward noise.

**Algorithm scope.** All admissible causal randomized algorithms, including policies told the horizon.

Restrict the profile to the fixed public action set $\mathcal D_t=L B_2^d$ at every time. Put $w_t=x_t/L$ and $\phi=L\theta_\star$. Then $w_t\in B_2^d$ and the scalar reward is $Y_t=w_t^{\mathsf T}\phi+\eta_t$. Choose independent $\eta_t\sim\mathcal N(0,\sigma^2)$, independent also of the learner's private randomness. Conditional on $\mathcal F_{t-1},x_t$, this has exactly the declared sub-Gaussian moment generating function.

Set $B=\min\{LS,1,\sigma(d-2)/(4\sqrt T)\}>0$. Apply Theorem 2.1 of Zhang, Hadiji and Combes with $A=I_d$, center zero, and with its dimension parameter equal to $d-2$. It yields a fixed Gaussian instance with $\|\phi\|_2=B$ and $\mathbb E R_T\ge BT/4$; the choice of $B$ makes $BT/4$ the smaller branch in the theorem. The restrictions $\|\theta_\star\|_2=B/L\le S$ and $|w^{\mathsf T}\phi|\le B\le1$ hold for every feasible action. Both action sets and the normalization are public; $\phi$ remains hidden.

For this same instance, $\max_{\|w\|_2\le1}w^{\mathsf T}\phi=B$. Consequently $R_T=\sum_{t=1}^T(B-w_t^{\mathsf T}\phi)$ is pathwise in $[0,2BT]$; realized Gaussian reward noise is absent from this metric. With $p=\Pr(R_T\ge BT/8)$, $\mathbb E R_T\le BT/8+2BTp$, so $p\ge1/16$. Any cap strictly below $BT/8$ fails at this fixed $T$ with probability at least $1/16>1/32\ge\delta_{\mathrm{conf}}$, and therefore fails the uniform-in-time guarantee as well. The probability conversion is a local consequence of the bounded hard instance and is separate from the paper's expected-regret theorem.

In the unit window, $B=(d-2)/(4\sqrt T)$ and $BT/8=(d-2)\sqrt T/32$. The existing OFUL envelope reduces to $O(d\sqrt T\log(1+T/d))$ since $\lambda_{\rm ridge}=1$, $d\ge3$, $T\ge d^2$, and the confidence is fixed.

**Limits of the argument.** This transfer does not characterize dependence on statistical confidence outside the displayed window.

**Sources.** [2](https://arxiv.org/abs/2502.17175v1)

## References

[1] Yasin Abbasi-Yadkori; Dávid Pál; Csaba Szepesvári. Improved Algorithms for Linear Stochastic Bandits. 2011. NeurIPS 24:2312–2320.

https://proceedings.neurips.cc/paper/2011/file/e1d5be1c7f2f456670de3d53c7b54f4a-Paper.pdf

[2] Raymond Zhang; Hédi Hadiji; Richard Combes. Linear Bandits on Ellipsoids: Minimax Optimal Algorithms. 2025. COLT 2025, PMLR 291:6016–6040; source locator uses arXiv:2502.17175v1..

https://arxiv.org/abs/2502.17175v1
