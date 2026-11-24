# Higher-order strongly monotone variational inequalities on compact convex sets with tangent residual

**Setting ID.** `CV_S_STRONG_HIGH_VI_TANGENT`

Variational inequalities

Complete feasible operator jets determine the optimal polynomial condition exponent for constrained strongly monotone VIs; root finding and solution-distance tasks remain separate.

**Status.** Logarithmic gap; Bounds missing

**TASK tags.** solution concept: Constrained variational inequality; task family: Variational inequality

**MODEL tags.** monotonicity: Strong monotonicity

**ORACLE tags.** feedback quality: Exact; operation: Operator taylor jet; operator derivative order: Parameterized order p−1 (see exact operation binding); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Probability; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N operator jet

## 1. Setting specification

### Task

Solve the variational inequality $0\in F(x)+N_X(x)$ on a known compact convex set by returning a feasible point with small tangent residual.

### Admissible model

Fix an integer $p\ge2$. The public set $X\subseteq\mathbb R^d$ is nonempty compact convex with diameter at most D, and a feasible start x_0 is supplied. The operator is $C^{p-1}$ on an open neighborhood of X and satisfies $\langle F(x)-F(y),x-y\rangle\ge\mu\|x-y\|_2^2$ and $\|D^{p-1}F(x)-D^{p-1}F(y)\|_{\rm op}\le L_p\|x-y\|_2$ on X.

The positive mu and L_p are lower and upper promises, not necessarily sharp moduli. No scalar potential or bound on lower derivatives is imposed. The unique VI solution need not be a zero of F, especially at the boundary. All norms are Euclidean induced multilinear operator norms.

### Oracle interface

At a feasible point return the exact complete operator jet $(F,DF,\ldots,D^{p-1}F)$. Count every call, including calls inside regularized subproblems, unsuccessful radius guesses, restarts and a final certificate check. Projections onto the known domain and exact solves of models formed only from returned jets are uncharged internal operations. An unknown-operator resolvent is not supplied for free.

### Output

Return any measurable feasible point $\widehat x\in X$, possibly unqueried. The upper witness additionally returns an evaluated certificate $(\widehat x,n,F(\widehat x))$ with $n\in N_X(\widehat x)$ and a charged evaluation of F at the output.

### Loss or accuracy criterion

The error is $r_{\rm tan}(x)=\operatorname{dist}(0,F(x)+N_X(x))$. Here $N_X(x)=\{n:\langle n,u-x\rangle\le0\text{ for all }u\in X\}$. The probability guarantee concerns this residual itself, not the root residual or distance to the solution.

### Resource accounting

One complete jet costs one query. A deterministic cap holds on every path for arbitrary measurable adaptive policies, and queries and outputs must stay feasible. The dimension-uniform comparison takes the worst case over all finite d, all legal public domains and starts, and all compatible operators.

### Algorithm views and success guarantees

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

A private random seed independent of the fixed instance is permitted.

$$
\forall I:\ \Pr(r_{\rm tan}(\widehat x)\le\varepsilon)\ge2/3
$$

The objective operator and domain are fixed before the independent private seed; feasibility and the query cap hold on every path.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$d$: Public ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$p$: Fixed operator-jet smoothness order **Domain:** $p\in\mathbb N,\ p\ge2$.

$L_p$: Lipschitz bound for derivative of order p-1 **Domain:** $L_p>0$.

$\mu$: Strong-monotonicity lower bound **Domain:** $\mu>0$.

$D$: Known domain diameter bound **Domain:** $D>0$.

$\varepsilon$: Tangent-residual tolerance **Domain:** $\varepsilon>0$.

$\kappa_D$: Diameter-normalized condition parameter **Domain:** $\kappa_D>0$.

$\kappa_D=L_pD^{p-1}/\mu$

$\theta$: Relative residual tolerance **Domain:** $\theta>0$.

$\theta=\varepsilon/(\mu D)$

$\alpha_p$: Condition exponent **Domain:** $\alpha_p>0$.

$\alpha_p=2/(3p-1)$

$\kappa_{0,p}$: Sufficient condition threshold in the source lower bound **Domain:** $\kappa_{0,p}>0$ depends only on p.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
T^\star_{{\rm rand},\infty}(\varepsilon;L_p,\mu,D)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\rm jet}$; description: Fixed worst-case cap on feasible complete-jet queries.

### R1 - All-parameter upper bound outside the matching lower window

**Region.** $p\ge2$ fixed; $L_p,\mu,D,\varepsilon>0$; either $\kappa_D<\kappa_{0,p}$ or $\theta>1/16$. All finite dimensions.

**Quantity.** Q1

**Resource.** Fixed worst-case cap on feasible complete-jet queries.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_p\!\left(1+\kappa_D^{2/(3p-1)}+\log_+(1/\theta)\right)
$$

**Gap or comparison.** The source does not give its condition-dependent lower bound outside this window.

### R2 - Condition-dominated relative-accuracy window

**Region.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)\le\kappa_D^{2/(3p-1)}$. This includes each fixed relative accuracy as kappa_D tends to infinity. The upper bound is valid in every finite dimension. For the lower bound the public domain can be $B_2^d(D/2)$ with start zero. Let $m=\lfloor(c_p^{\rm sc}\kappa_D)^{2/(3p-1)}\rfloor$, with $c_p^{\rm sc}$ from equation lower-constants. Any $d\ge m+\lceil2048m^3\ln(8(m^2+1))\rceil$ suffices. The explicit source threshold is $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. This is a sufficient high-dimensional construction, not a claim for every fixed small d.

**Quantity.** Q1

**Resource.** Fixed worst-case cap; the upper witness is deterministic.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega_p(\kappa_D^{2/(3p-1)})
$$

**Upper bound.** B2

$$
O_p\!\left(1+\kappa_D^{2/(3p-1)}+\log_+(1/\theta)\right)
$$

**Gap or comparison.** The explicit logarithmic accuracy term is dominated by the condition term, so the upper/lower ratio is O_p(1).

### R3 - Smaller relative accuracy with a remaining logarithmic factor

**Region.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)>\kappa_D^{2/(3p-1)}$. The upper bound is valid in every finite dimension. For the lower bound the public domain can be $B_2^d(D/2)$ with start zero. Let $m=\lfloor(c_p^{\rm sc}\kappa_D)^{2/(3p-1)}\rfloor$, with $c_p^{\rm sc}$ from equation lower-constants. Any $d\ge m+\lceil2048m^3\ln(8(m^2+1))\rceil$ suffices. The explicit source threshold is $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. This is a sufficient high-dimensional construction, not a claim for every fixed small d.

**Quantity.** Q1

**Resource.** Fixed worst-case cap on feasible queries.

**Status.** Logarithmic gap

**Lower bound.** B5

$$
\Omega_p(\kappa_D^{2/(3p-1)})
$$

**Upper bound.** B4

$$
O_p\!\left(1+\kappa_D^{2/(3p-1)}+\log_+(1/\theta)\right)
$$

**Gap or comparison.** Upper/lower ratio is at most $O_p(1+\log_+(1/\theta)/\kappa_D^{2/(3p-1)})$. No matching lower bound for the additive accuracy logarithm is asserted.

## 4. Bounds and supporting evidence

### B1 - Certified restart of the log-free monotone full-jet solver

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_p\!\left(1+\kappa_D^{2/(3p-1)}+\log_+(1/\theta)\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf)

**Conditions.** $p\ge2$ fixed; $L_p,\mu,D,\varepsilon>0$; either $\kappa_D<\kappa_{0,p}$ or $\theta>1/16$.; The source imports Theorem 5.1 of Zhang-Chen-Pan-Liu-Yang-Zhang (2026) and preserves feasibility, original-domain normal cones, and all final evaluations.

**Dimension conditions.** All finite dimensions.

**Constants.** Constants depend only on p.

**Logarithmic factors.** The additive logarithm is explicit.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf) Proposition literature-restart, equation sharper-upper; Corollary frontier; verified labels: prop:literature-restart (line 539), eq:sharper-upper (line 543), cor:frontier (line 597)

Certified restart of the log-free monotone full-jet solver. Deterministic feasible algorithms returning an evaluated tangent certificate.

The source imports Theorem 5.1 of Zhang-Chen-Pan-Liu-Yang-Zhang (2026) and preserves feasibility, original-domain normal cones, and all final evaluations.

### B2 - Certified restart of the log-free monotone full-jet solver

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_p\!\left(1+\kappa_D^{2/(3p-1)}+\log_+(1/\theta)\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)\le\kappa_D^{2/(3p-1)}$. This includes each fixed relative accuracy as kappa_D tends to infinity.; The source imports Theorem 5.1 of Zhang-Chen-Pan-Liu-Yang-Zhang (2026) and preserves feasibility, original-domain normal cones, and all final evaluations.

**Dimension conditions.** The upper bound is valid in every finite dimension. For the lower bound the public domain can be $B_2^d(D/2)$ with start zero. Let $m=\lfloor(c_p^{\rm sc}\kappa_D)^{2/(3p-1)}\rfloor$, with $c_p^{\rm sc}$ from equation lower-constants. Any $d\ge m+\lceil2048m^3\ln(8(m^2+1))\rceil$ suffices. The explicit source threshold is $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. This is a sufficient high-dimensional construction, not a claim for every fixed small d.

**Constants.** Constants depend only on p.

**Logarithmic factors.** No hidden logarithms in the imported-solver upper bound.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf) Proposition literature-restart, equation sharper-upper; Corollary frontier; verified labels: prop:literature-restart (line 539), eq:sharper-upper (line 543), cor:frontier (line 597)

Certified restart of the log-free monotone full-jet solver. Deterministic feasible algorithms returning an evaluated tangent certificate.

The source imports Theorem 5.1 of Zhang-Chen-Pan-Liu-Yang-Zhang (2026) and preserves feasibility, original-domain normal cones, and all final evaluations.

### B3 - Flat-gated strongly monotone operator chain with calibrated monotonicity modulus

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_p(\kappa_D^{2/(3p-1)})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)\le\kappa_D^{2/(3p-1)}$. This includes each fixed relative accuracy as kappa_D tends to infinity.; The fixed hard operator is independent of the private seed. The lower bound applies when kappa_D>=kappa_0,p and theta<=1/16.

**Dimension conditions.** The upper bound is valid in every finite dimension. For the lower bound the public domain can be $B_2^d(D/2)$ with start zero. Let $m=\lfloor(c_p^{\rm sc}\kappa_D)^{2/(3p-1)}\rfloor$, with $c_p^{\rm sc}$ from equation lower-constants. Any $d\ge m+\lceil2048m^3\ln(8(m^2+1))\rceil$ suffices. The explicit source threshold is $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. This is a sufficient high-dimensional construction, not a claim for every fixed small d.

**Constants.** Constants depend only on p.

**Logarithmic factors.** No hidden logarithms in the imported-solver upper bound.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf) Theorem lower; equation randomized-lower and lower-dimension; verified labels: thm:lower (line 502), eq:randomized-lower (line 510), sec:lower (line 1256), eq:lower-dimension (line 1457)

Flat-gated strongly monotone operator chain with calibrated monotonicity modulus. Arbitrary randomized adaptive feasible full-jet queries and outputs.

The fixed hard operator is independent of the private seed. The lower bound applies when kappa_D>=kappa_0,p and theta<=1/16.

### B4 - Certified restart of the log-free monotone full-jet solver

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_p\!\left(1+\kappa_D^{2/(3p-1)}+\log_+(1/\theta)\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)>\kappa_D^{2/(3p-1)}$.; The source imports Theorem 5.1 of Zhang-Chen-Pan-Liu-Yang-Zhang (2026) and preserves feasibility, original-domain normal cones, and all final evaluations.

**Dimension conditions.** The upper bound is valid in every finite dimension. For the lower bound the public domain can be $B_2^d(D/2)$ with start zero. Let $m=\lfloor(c_p^{\rm sc}\kappa_D)^{2/(3p-1)}\rfloor$, with $c_p^{\rm sc}$ from equation lower-constants. Any $d\ge m+\lceil2048m^3\ln(8(m^2+1))\rceil$ suffices. The explicit source threshold is $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. This is a sufficient high-dimensional construction, not a claim for every fixed small d.

**Constants.** Constants depend only on p.

**Logarithmic factors.** The remaining multiplicative discrepancy is at most logarithmic in inverse relative accuracy.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf) Proposition literature-restart, equation sharper-upper; Corollary frontier; verified labels: prop:literature-restart (line 539), eq:sharper-upper (line 543), cor:frontier (line 597)

Certified restart of the log-free monotone full-jet solver. Deterministic feasible algorithms returning an evaluated tangent certificate.

The source imports Theorem 5.1 of Zhang-Chen-Pan-Liu-Yang-Zhang (2026) and preserves feasibility, original-domain normal cones, and all final evaluations.

### B5 - Flat-gated strongly monotone operator chain with calibrated monotonicity modulus

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_p(\kappa_D^{2/(3p-1)})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)>\kappa_D^{2/(3p-1)}$.; The fixed hard operator is independent of the private seed. The lower bound applies when kappa_D>=kappa_0,p and theta<=1/16.

**Dimension conditions.** The upper bound is valid in every finite dimension. For the lower bound the public domain can be $B_2^d(D/2)$ with start zero. Let $m=\lfloor(c_p^{\rm sc}\kappa_D)^{2/(3p-1)}\rfloor$, with $c_p^{\rm sc}$ from equation lower-constants. Any $d\ge m+\lceil2048m^3\ln(8(m^2+1))\rceil$ suffices. The explicit source threshold is $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. This is a sufficient high-dimensional construction, not a claim for every fixed small d.

**Constants.** Constants depend only on p.

**Logarithmic factors.** The remaining multiplicative discrepancy is at most logarithmic in inverse relative accuracy.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf) Theorem lower; equation randomized-lower and lower-dimension; verified labels: thm:lower (line 502), eq:randomized-lower (line 510), sec:lower (line 1256), eq:lower-dimension (line 1457)

Flat-gated strongly monotone operator chain with calibrated monotonicity modulus. Arbitrary randomized adaptive feasible full-jet queries and outputs.

The fixed hard operator is independent of the private seed. The lower bound applies when kappa_D>=kappa_0,p and theta<=1/16.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U11. Higher-Order Oracle Complexity of Strongly Monotone Variational Inequalities. strongly_monotone_vi.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U11/manuscript.pdf

[2] Xinliang Zhang; Lesi Chen; Linxuan Pan; Chengchang Liu; Junchi Yang; Jingzhao Zhang. Optimal High-Order Methods for Solving Monotone Variational Inequalities. 2026. arXiv:2609.23557v1; Theorem 5.1 as used in Proposition literature-restart.

https://arxiv.org/abs/2609.23557
