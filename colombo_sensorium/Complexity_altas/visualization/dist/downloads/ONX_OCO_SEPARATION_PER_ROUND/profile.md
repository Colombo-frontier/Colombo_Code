# Online convex optimization with exact separation and per-round query caps

**Setting ID.** `ONX_OCO_SEPARATION_PER_ROUND`

Online learning and bandits

Expected regret for exactly feasible actions on an unknown convex body, with a separately enforced separation budget on each round.

**Status.** Logarithmic gap; Other quantified gap

**Gap classes present.** Logarithmic gap; Other quantified gap

**TASK tags.** solution concept: Unknown domain online regret; task family: Online bandit

**MODEL tags.** convexity: Convex

**ORACLE tags.** feedback quality: Exact; operation: Current loss and subgradient; operation: Strong separation certificate; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance

**RESOURCE tags.** measure: Q per round; measure: T

## 1. Setting specification

### Task

Minimize adversarial online convex regret while maintaining exact feasibility in an unknown convex body under a strictly enforced separation-query cap on every round.

### Admissible model

The unknown compact convex body satisfies $rB_2^d\subseteq K\subseteq RB_2^d$ with public common center zero and public $0<r\le R$. Set $\kappa=R/r$; these supplied radii need not be optimal for the individual body.

After the current action, the convex loss may depend on the past and that action. A returned subgradient at the action has norm at most G. The guarantee is uniform over comparators and admissible adaptive loss sequences.

### Oracle interface

Before each action, at most Q calls to an exact strong separation oracle may be made. On any query z in the full Euclidean space, it returns inside if z belongs to K, or a unit vector a satisfying $\sup_{x\in K}\langle a,x\rangle<\langle a,z\rangle$. The oracle may choose any valid response.

The learner then plays $w_t\in K$ and receives the current convex loss and a subgradient $g_t\in\partial f_t(w_t)$ with $\|g_t\|\le G$. The upper algorithms use only the subgradient. All preprocessing access to K is charged from round 1; unused calls cannot be carried to a future round. Arithmetic and tests against explicitly stored inequalities are not unknown-body queries.

### Output

Every played point must be feasible almost surely for every admissible body and every valid separation oracle. Approximate feasibility is not allowed.

### Loss or accuracy criterion

$R_T=\sup_{u\in K}\sum_{t=1}^T[f_t(w_t)-f_t(u)]$. The risk is the infimum over almost-surely feasible capped learners of worst-case expected regret over bodies, valid oracle responses, and admissible loss adversaries.

### Resource accounting

The resource is the joint pair (T,Q), where Q is a hard per-round cap rather than an average or total budget; total separation calls are at most QT. One loss/subgradient response is obtained after each action. Internal arithmetic, bit precision, and known-inequality processing are uncharged.

### Algorithm views and success guarantees

All randomized adaptive learners may make full-space separation queries, but must respect the hard cap before each action and be feasible almost surely for every body and valid response rule.

$$
\sup_{K,\mathrm{Sep},f_{1:T}}\mathbb E R_T\le r_{\mathrm{reg}}
$$

Expected regret is taken over learner randomization while feasibility and the query cap hold almost surely on every round.

**Budget convention.** fixed_per_round_oracle_cap

## 2. Notation and parameters

$d$: Euclidean dimension **Domain:** $d\ge1$ integer.

$T$: Horizon **Domain:** $T\ge1$ integer.

$G$: Subgradient norm bound **Domain:** $G>0$.

$R$: Public enclosing-ball radius **Domain:** $R>0$.

$r$: Public inscribed-ball radius **Domain:** $0<r\le R$.

$\kappa$: Public asphericity upper bound **Domain:** $\kappa\ge1$.

$\kappa=R/r$

$Q$: Strict separation-query cap on every round **Domain:** $Q\ge1$ integer.

$L_T$: Query reserve for the deterministic fallback **Domain:** $L_T\ge1$ integer.

$L_T=1+\lceil\log_2(\kappa T)\rceil$

$D_T$: Localization dimension–logarithm scale **Domain:** $D_T>0$.

$D_T=d\log(e\kappa T)$

$q$: Unreserved localization calls in the hybrid **Domain:** $q=Q-L_T\ge1$ in the hybrid regime.

$q=Q-L_T$

$M$: Horizon-truncated dimension **Domain:** $M\ge1$.

$M=\min\{T,d\}$

$N_Q$: Truncated dimension divided by the cap **Domain:** $N_Q\ge0$.

$N_Q=\min\{T,(d-1)/Q\}$

$j$: Hidden-facet count in the exact lower bound **Domain:** $1\le j\le d-1$ integer.

$\delta_{j,\kappa}$: Normalized hidden-facet comparator advantage **Domain:** $\delta_{j,\kappa}\ge0$.

$\delta_{j,\kappa}=(\kappa^2-1)/[2\kappa^2(\sqrt{(\kappa^2+1)/(2\kappa^2)}+\sqrt{1+j/\kappa^2})]$

$a$: Fixed exponent describing the polynomial-in-logarithms budget regime **Domain:** $a>0$ fixed independently of d,T,kappa,Q.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathfrak R_Q^{\mathrm{sep}}(d,T,\kappa;G,R)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $(T,Q)$; description: Q is charged separately on each of T rounds; fallback and localization share the same cap.

### R1 - All asphericities with the specified logarithmic cap

**Region.** $d,T\ge1$ integers, $G,R,r>0$, $r\le R$; fix $a>0$. The strict cap is either $Q=Q_*=2L_T$ or satisfies $L_T+1\le Q\le[\log(edT\kappa)]^a$ (when the latter interval is nonempty). All finite dimensions, including d=1. More generally the same logarithmic rate holds for $L_T+1\le Q\le[\log(edT\kappa)]^a$ for any fixed a>0 when this interval is nonempty; hidden logarithmic exponents may depend on a. This assertion does not include the literal cap Q=1 merely because one is bounded by a polylogarithm.

**Quantity.** Q1

**Resource.** Q is charged separately on each of T rounds; fallback and localization share the same cap.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\widetilde\Omega(GR\min\{T,\sqrt T+\min\{M,\kappa\sqrt M\}\})
$$

**Upper bound.** B1

$$
\widetilde O(GR\min\{T,\sqrt T+\min\{M,\kappa\sqrt M\}\})
$$

**Gap or comparison.** Only logarithmic factors in d,T,kappa remain.

### R2 - Arbitrary query cap: explicit upper/lower frontier

**Region.** $d\ge2$, $T\ge1$, $\kappa\ge1$, and integer $Q\ge1$. Exclude the preceding closed logarithmic-budget region: require $Q\ne2L_T$ and either $Q<L_T+1$ or $Q>[\log(edT\kappa)]^a$, with the same fixed a. Every finite d≥2; the exact lower formula retains its floor and facet-count range. The general-cap bounds themselves remain valid inside the excluded logarithmic-budget region; that region is represented by its sharper matching comparison.

**Quantity.** Q1

**Resource.** Strict per-round separation cap, no preprocessing credit.

**Status.** Other quantified gap

**Lower bound.** B4

$$
\Omega\!\left(GR\max\{\sqrt T,\max_{1\le j\le d-1}\delta_{j,\kappa}\lfloor\min\{T,j/(4Q)\}\rfloor\}\right)
$$

**Upper bound.** B3

$$
O(GR\min\{T,\sqrt T+D_T/Q\})
$$

**Gap or comparison.** The explicit expressions give the supported frontier; their ratio is not asserted to be logarithmic for arbitrary growing Q.

### R3 - Hybrid reserve available: general cap and asphericity

**Region.** $d\ge2$, $T\ge1$, $\kappa\ge2$, and $Q\ge L_T+1$; let $q=Q-L_T$ and $N_Q=\min\{T,(d-1)/Q\}$. Exclude the preceding closed logarithmic-budget region: require $Q\ne2L_T$ and either $Q<L_T+1$ or $Q>[\log(edT\kappa)]^a$, with the same fixed a. Every finite d≥2. The general-cap bounds themselves remain valid inside the excluded logarithmic-budget region; that region is represented by its sharper matching comparison.

**Quantity.** Q1

**Resource.** The L_T fallback calls are included inside Q; q is the remaining cap.

**Status.** Other quantified gap

**Lower bound.** B6

$$
\Omega\!\left(GR\min\{T,\sqrt T+\min\{N_Q,\kappa\sqrt{N_Q/Q}\}\}\right)
$$

**Upper bound.** B5

$$
O\!\left(GR\min\{T,\kappa\sqrt T,\sqrt T+D_T/Q,\sqrt T+\kappa\sqrt{D_T/(Q-L_T)}\}\right)
$$

**Gap or comparison.** When the intermediate-asphericity terms dominate, the geometric upper/lower ratio is of order $Q/\sqrt{Q-L_T}$ apart from logarithms; it is $O(\sqrt Q)$ for $Q\ge2L_T$. No uniform sqrt(Q) statement is made near the reserve threshold.

## 4. Bounds and supporting evidence

### B1 - Gaussian localization with a deterministic feasible separation fallback.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(GR\min\{T,\sqrt T+\min\{M,\kappa\sqrt M\}\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf)

**Conditions.** $d,T\ge1$ integers, $G,R,r>0$, $r\le R$; fix $a>0$. The strict cap is either $Q=Q_*=2L_T$ or satisfies $L_T+1\le Q\le[\log(edT\kappa)]^a$ (when the latter interval is nonempty).; More generally the same logarithmic rate holds for $L_T+1\le Q\le[\log(edT\kappa)]^a$ for any fixed a>0 when this interval is nonempty; hidden logarithmic exponents may depend on a.; This assertion does not include the literal cap Q=1 merely because one is bounded by a polylogarithm.

**Dimension conditions.** All finite dimensions, including d=1.

**Constants.** Universal for Q=2L_T; for the broader logarithmic-budget range, logarithmic exponents and constants may depend on the fixed a.

**Logarithmic factors.** Finite powers of log(edT*kappa).

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf) Corollary cor:main; equation eq:main; Theorem thm:upper

Gaussian localization with a deterministic feasible separation fallback.. Randomized almost-surely feasible strict-cap learners.

### B2 - Independent hidden signs in facets, combined with the known-ball online lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde\Omega(GR\min\{T,\sqrt T+\min\{M,\kappa\sqrt M\}\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf)

**Conditions.** $d,T\ge1$ integers, $G,R,r>0$, $r\le R$; fix $a>0$. The strict cap is either $Q=Q_*=2L_T$ or satisfies $L_T+1\le Q\le[\log(edT\kappa)]^a$ (when the latter interval is nonempty).; More generally the same logarithmic rate holds for $L_T+1\le Q\le[\log(edT\kappa)]^a$ for any fixed a>0 when this interval is nonempty; hidden logarithmic exponents may depend on a.; This assertion does not include the literal cap Q=1 merely because one is bounded by a polylogarithm.

**Dimension conditions.** All finite dimensions, including d=1.

**Constants.** Universal for Q=2L_T; for the broader logarithmic-budget range, logarithmic exponents and constants may depend on the fixed a.

**Logarithmic factors.** Finite powers of log(edT*kappa).

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf) Corollary cor:main; Theorem thm:lower; proof in Section sec:consequences

Independent hidden signs in facets, combined with the known-ball online lower bound.. Every randomized strict-cap feasible learner.

### B3 - Origin fallback with all Q calls allocated to localization.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(GR\min\{T,\sqrt T+D_T/Q\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf)

**Conditions.** $d\ge2$, $T\ge1$, $\kappa\ge1$, and integer $Q\ge1$. Exclude the preceding closed logarithmic-budget region: require $Q\ne2L_T$ and either $Q<L_T+1$ or $Q>[\log(edT\kappa)]^a$, with the same fixed a.; The general-cap bounds themselves remain valid inside the excluded logarithmic-budget region; that region is represented by its sharper matching comparison.

**Dimension conditions.** Every finite d≥2; the exact lower formula retains its floor and facet-count range.

**Constants.** Universal constants.

**Logarithmic factors.** All logarithms in the upper formula appear through D_T.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf) Theorem thm:upper; equation eq:upper-origin

Origin fallback with all Q calls allocated to localization.. Randomized feasible learners obeying the literal cap.

### B4 - Hidden-facet learning under one fixed legal oracle and a known-ball component.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(GR\max\{\sqrt T,\max_{1\le j\le d-1}\delta_{j,\kappa}\lfloor\min\{T,j/(4Q)\}\rfloor\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf)

**Conditions.** $d\ge2$, $T\ge1$, $\kappa\ge1$, and integer $Q\ge1$. Exclude the preceding closed logarithmic-budget region: require $Q\ne2L_T$ and either $Q<L_T+1$ or $Q>[\log(edT\kappa)]^a$, with the same fixed a.; The general-cap bounds themselves remain valid inside the excluded logarithmic-budget region; that region is represented by its sharper matching comparison.

**Dimension conditions.** Every finite d≥2; the exact lower formula retains its floor and facet-count range.

**Constants.** Universal constants.

**Logarithmic factors.** All logarithms in the upper formula appear through D_T.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf) Theorem thm:lower; equation eq:lower-exact

Hidden-facet learning under one fixed legal oracle and a known-ball component.. All randomized learners feasible for every body.

### B5 - Select the best known-parameter strategy between fallback-only, origin localization, and the hybrid.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(GR\min\{T,\kappa\sqrt T,\sqrt T+D_T/Q,\sqrt T+\kappa\sqrt{D_T/(Q-L_T)}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf)

**Conditions.** $d\ge2$, $T\ge1$, $\kappa\ge2$, and $Q\ge L_T+1$; let $q=Q-L_T$ and $N_Q=\min\{T,(d-1)/Q\}$. Exclude the preceding closed logarithmic-budget region: require $Q\ne2L_T$ and either $Q<L_T+1$ or $Q>[\log(edT\kappa)]^a$, with the same fixed a.; The general-cap bounds themselves remain valid inside the excluded logarithmic-budget region; that region is represented by its sharper matching comparison.

**Dimension conditions.** Every finite d≥2.

**Constants.** Universal constants.

**Logarithmic factors.** The displayed D_T and L_T retain the logarithms.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf) Theorem thm:upper; equation eq:upper-hybrid

Select the best known-parameter strategy between fallback-only, origin localization, and the hybrid.. Randomized feasible strict-cap learners.

### B6 - Optimized hidden-facet construction plus the online lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega\!\left(GR\min\{T,\sqrt T+\min\{N_Q,\kappa\sqrt{N_Q/Q}\}\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf)

**Conditions.** $d\ge2$, $T\ge1$, $\kappa\ge2$, and $Q\ge L_T+1$; let $q=Q-L_T$ and $N_Q=\min\{T,(d-1)/Q\}$. Exclude the preceding closed logarithmic-budget region: require $Q\ne2L_T$ and either $Q<L_T+1$ or $Q>[\log(edT\kappa)]^a$, with the same fixed a.; The general-cap bounds themselves remain valid inside the excluded logarithmic-budget region; that region is represented by its sharper matching comparison.

**Dimension conditions.** Every finite d≥2.

**Constants.** Universal constants.

**Logarithmic factors.** The displayed D_T and L_T retain the logarithms.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf) Theorem thm:lower; equation eq:lower-simple

Optimized hidden-facet construction plus the online lower bound.. All randomized strict-cap feasible learners.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U08. Minimax Regret under Per-Round Separation-Oracle Budgets. separation_oracle_oco.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U08/manuscript.pdf
