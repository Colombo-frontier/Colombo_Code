# Unknown-tail stochastic nonconvex stationarity with known smoothness and initial gap

**Setting ID.** `SO_FO_S03_unknown_alpha_known_scales`

Single-objective optimization

A common algorithm adapts to an unknown moment exponent and noise scale when population smoothness and initial-gap budgets are known.

**Status.** Logarithmic gap; Bounds missing

**TASK tags.** solution concept: Gradient stationarity; task family: Single objective

**MODEL tags.** smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Stochastic unbiased conditional moment; operation: Stochastic gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N gradient sample

## 1. Setting specification

### Task

Construct one budget-indexed algorithm family for smooth nonconvex stationarity that adapts to an unknown centered-noise moment exponent.

### Admissible model

The differentiable lower-bounded $F:\mathbb R^d\to\mathbb R$ satisfies $F(x_0)-\inf F\le\Delta$ and $\operatorname{Lip}(\nabla F)\le L$. The positive budgets $L,\Delta$, initial point and finite dimension are public. For some fixed $p\in(1,2]$ and $\sigma\ge0$, the oracle noise has centered conditional pth moment at most $\sigma^p$. Neither p nor sigma is supplied to the algorithm.

### Oracle interface

A query at a history-measurable point returns only a full vector $g_t$ with $\mathbb E[g_t\mid\mathcal F_{t-1}]=\nabla F(x_t)$ and $\mathbb E[\|g_t-\nabla F(x_t)\|_2^p\mid\mathcal F_{t-1}]\le\sigma^p$. The conditional law may depend on the history. No function value, repeated evaluation of one sample at different points, or sample-gradient smoothness is available.

### Output

Return an arbitrary measurable point $\widehat x_T$ after at most T charged gradient observations.

### Loss or accuracy criterion

The risk is $\mathcal R_T^{\mathsf A}(p;L,\Delta,\sigma)=\sup_{d,I,\mathcal O}\mathbb E\|\nabla F(\widehat x_T)\|_2$, with one common family $\mathsf A=(\mathsf A_T)$ required to apply for every fixed p. Constants in the analyzed risk may depend on p; the algorithm does not.

### Resource accounting

T is a public deterministic cap on every path. Training, candidate generation, validation and selection calls all count. Pointwise inversion of a risk bound at a specified p is an analysis quantity and does not furnish a stopping rule that knows p.

### Algorithm views and success guarantees

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

A private random seed independent of the fixed instance is permitted.

The complete algorithm family is the same for all p and sigma. Known smoothness and gap budgets may enter its step sizes; unknown tail and noise scales may not.

$$
\mathcal R_T^{\mathsf A}(p;L,\Delta,\sigma)=\sup_{d,I,\mathcal O}\mathbb E\|\nabla F(\widehat x_T)\|_2
$$

Choose one common family with inputs only T,L,Delta,x0 and d. For every fixed p, evaluate its risk uniformly over the corresponding instance and oracle class. The family may not encode a p-dependent tuning choice.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$d$: Public finite ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$T$: Public total sample cap **Domain:** $T\in\mathbb N_{\ge1}$.

$L$: Known population-gradient smoothness bound **Domain:** $L>0$.

$\Delta$: Known initial gap bound **Domain:** $\Delta>0$.

$p$: Unknown fixed centered-noise moment exponent **Domain:** $1<p\le2$.

$\sigma$: Unknown centered-noise scale **Domain:** $\sigma\ge0$.

$\varepsilon$: Tolerance used for pointwise risk inversion **Domain:** $\varepsilon>0$.

$a(p)$: Normalized risk exponent **Domain:** $a(p)>0$.

$a(p)=(p-1)/(3p-2)$

$b(p)$: Mean-estimation exponent **Domain:** $b(p)>0$.

$b(p)=(p-1)/p$

$n$: Training budget per candidate in the portfolio inequality **Domain:** $n\in\mathbb N,\ n\ge8$.

$m$: Fresh validation samples per candidate **Domain:** $m\in\mathbb N_{\ge1}$.

$M$: Number of dyadic candidates **Domain:** $M\in\mathbb N$.

$M=|\mathcal T_n|,\quad\mathcal T_n=\{2^j:j\in\mathbb Z_{\ge0},2^j\le n/2\}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$\mathcal R_T^{\mathsf A}(p;1,1,1)$, with one common family for all p

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\rm sample}\le T$; description: All candidate training and validation responses count toward the fixed cap.

#### Q2 - minimax metric resource quantity

$$
\mathcal R_T^{\mathsf A}(p;L,\Delta,\sigma)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $M(n+m)\le T$; description: Separate per-candidate training and validation allocations are charged in full.

### R1 - Normalized unknown-tail risk with known smoothness and gap

**Region.** $L=\Delta=\sigma=1$ for evaluation of the instance class, fixed $1<p\le2$, and all sufficiently large integer T (the sufficient threshold may depend on p). The algorithm is not given p or sigma. Upper bounds hold in every finite dimension. The lower bound permits a dimension depending on T; Corollary sample-complexity imports Liu, extended-version Theorem 11. No fixed-dimensional lower rate is asserted.

**Quantity.** Q1

**Resource.** All candidate training and validation responses count toward the fixed cap.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega_p\!\left(T^{-(p-1)/(3p-2)}\right)
$$

**Upper bound.** B1

$$
O_p\!\left((\log(eT)/T)^{(p-1)/(3p-2)}\right)
$$

**Gap or comparison.** The risk ratio is at most $O_p((\log(eT))^{(p-1)/(3p-2)})$. Pointwise sample complexity is between $\Omega_p(\varepsilon^{-(3p-2)/(p-1)})$ and $O_p(\varepsilon^{-(3p-2)/(p-1)}\log(e/\varepsilon))$.

### R2 - General-scale portfolio oracle inequality

**Region.** $L,\Delta>0$, $\sigma\ge0$, fixed $1<p\le2$, integers $n\ge8,m\ge1$, and $M(n+m)\le T$. The upper bound holds for every finite d.

**Quantity.** Q2

**Resource.** Separate per-candidate training and validation allocations are charged in full.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B3

$$
O_p\!\left(\min_{\tau\in\mathcal T_n}\{\sqrt{L\Delta\tau/n}+\sigma\tau^{-(p-1)/p}\}+\sigma M^{1/p}m^{-(p-1)/p}\right)
$$

**Gap or comparison.** Only the displayed upper bound is recorded for the full joint parameter domain.

## 4. Bounds and supporting evidence

### B1 - Dyadic minibatch normalized-gradient portfolio and fresh empirical-gradient validation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O_p\!\left((\log(eT)/T)^{(p-1)/(3p-2)}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf)

**Conditions.** $L=\Delta=\sigma=1$ for evaluation of the instance class, fixed $1<p\le2$, and all sufficiently large integer T (the sufficient threshold may depend on p). The algorithm is not given p or sigma.; The same family simultaneously satisfies the displayed pointwise risk curve for each fixed p.

**Dimension conditions.** Upper bounds hold in every finite dimension. The lower bound permits a dimension depending on T; Corollary sample-complexity imports Liu, extended-version Theorem 11. No fixed-dimensional lower rate is asserted.

**Constants.** Constants and sufficient large-budget thresholds may depend on fixed p; they are not uniform as p decreases to 1.

**Logarithmic factors.** A single logarithm in pointwise sample complexity; its displayed power in risk.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf) Theorem main-upper; equation main-upper; verified labels: sec:main-upper (line 544), thm:main-upper (line 569), eq:main-upper (line 572)

Dyadic minibatch normalized-gradient portfolio and fresh empirical-gradient validation. One randomized common algorithm family independent of p and sigma.

The same family simultaneously satisfies the displayed pointwise risk curve for each fixed p.

### B2 - Known-index stochastic first-order lower bound, valid for the smaller class of tuning-free families

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_p\!\left(T^{-(p-1)/(3p-2)}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf)

**Conditions.** $L=\Delta=\sigma=1$ for evaluation of the instance class, fixed $1<p\le2$, and all sufficiently large integer T (the sufficient threshold may depend on p). The algorithm is not given p or sigma.; The source lower construction obeys the centered moment convention and allows growing dimension.

**Dimension conditions.** Upper bounds hold in every finite dimension. The lower bound permits a dimension depending on T; Corollary sample-complexity imports Liu, extended-version Theorem 11. No fixed-dimensional lower rate is asserted.

**Constants.** Constants and sufficient large-budget thresholds may depend on fixed p; they are not uniform as p decreases to 1.

**Logarithmic factors.** A single logarithm in pointwise sample complexity; its displayed power in risk.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf) Corollary sample-complexity; equation liu-lower; cited Liu Theorem 11; verified labels: eq:liu-lower (line 672), cor:sample-complexity (line 681), eq:sample-complexity (line 683)

Known-index stochastic first-order lower bound, valid for the smaller class of tuning-free families. Every randomized T-query method, even when p is known.

The source lower construction obeys the centered moment convention and allows growing dimension.

### B3 - Dyadic portfolio with independent public allocation choices

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O_p\!\left(\min_{\tau\in\mathcal T_n}\{\sqrt{L\Delta\tau/n}+\sigma\tau^{-(p-1)/p}\}+\sigma M^{1/p}m^{-(p-1)/p}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf)

**Conditions.** $L,\Delta>0$, $\sigma\ge0$, fixed $1<p\le2$, integers $n\ge8,m\ge1$, and $M(n+m)\le T$.; This nonasymptotic bound remains valid when the analysis-optimal batch size lies outside the interior dyadic range.

**Dimension conditions.** The upper bound holds for every finite d.

**Constants.** Constants depend only on fixed p.

**Logarithmic factors.** No logarithms are suppressed in the displayed allocation formula.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf) Theorem parameter-oracle; equation parameter-oracle; verified labels: thm:parameter-oracle (line 634), eq:parameter-oracle (line 645)

Dyadic portfolio with independent public allocation choices. One common family using L and Delta but not p or sigma.

This nonasymptotic bound remains valid when the analysis-optimal batch size lies outside the interior dyadic range.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_N05. Near-Optimal Smooth Nonconvex Optimization with an Unknown Tail Index. 2026. N05_unknown_tail_index_publication.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/N05/manuscript.pdf

[2] Zijian Liu. Online Convex Optimization with Heavy Tails: Old Algorithms, New Regrets, and Applications. 2026. Extended version, March 19, 2026; Theorem 11 as cited by the supplied manuscript.

https://arxiv.org/abs/2508.07473v3
