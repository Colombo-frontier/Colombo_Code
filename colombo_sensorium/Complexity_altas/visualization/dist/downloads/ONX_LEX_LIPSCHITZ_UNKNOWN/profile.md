# Metric Lipschitz lexicographic bandits without tradeoff side information

**Setting ID.** `ONX_LEX_LIPSCHITZ_UNKNOWN`

Online learning and bandits

Expected coordinate regret without a tradeoff envelope, quantified by primary-tie metric entropy and regular packing growth.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Lexicographic bandit regret; task family: Online bandit

**ORACLE tags.** feedback quality: Stochastic subgaussian; operation: Two coordinate reward vector; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance

**RESOURCE tags.** measure: N arm pull; measure: N reward coordinate

## 1. Setting specification

### Task

Minimize simultaneous coordinate regret for a two-objective lexicographic stochastic bandit without a supplied tradeoff envelope.

### Admissible model

The public arm space $(\mathcal X,D)$ is a nonempty compact metric space with diameter at most one. The two means take values in [0,1] and are 1-Lipschitz. Compactness ensures the lexicographic optimum exists.

There are two fixed reward means $\mu^1,\mu^2$ taking values in $[0,1]$. The primary optimum set is $\mathcal X_1^*=\arg\max_x\mu^1(x)$, and a lexicographic optimum $x^*$ maximizes $\mu^2$ over that set. Primary ties are permitted.

The local tradeoff is $\lambda_* =\inf\{\lambda\ge0:\mu^2(x)-\mu^2(x^*)\le\lambda[\mu^1(x^*)-\mu^1(x)]\ \forall x\}$. No value or upper bound for $\lambda_*$ is supplied. The same policy must handle all admissible means without such side information.

The local tradeoff can be infinite on compact infinite spaces. The main no-envelope guarantees hold on this class and their lower bounds also hold on the finite-tradeoff subclass.

### Oracle interface

At round $t$, choose an arm $X_t$ using the past and an independent random seed; then observe both coordinates $(Y_t^1,Y_t^2)$. Each coordinate is conditionally 1-sub-Gaussian around its fixed mean: $\mathbb E[\exp(\theta(Y_t^i-\mu^i(X_t)))\mid\mathcal H_{t-1},X_t]\le\exp(\theta^2/2)$. Independence between coordinates is not required. There is no feedback for unselected arms and no sample reuse interface.

The horizon and metric are public. A measurable maximal-net oracle, given a nonempty compact subset U and r>0, returns a finite inclusion-maximal r-separated subset. Its computational cost is not charged as a reward observation. Mean functions, primary ties, and near-optimality packing parameters are hidden; the policy uses no tradeoff envelope.

### Output

The output is the sequence of selected arms. One policy must control both objective regrets against the same lexicographic optimum.

### Loss or accuracy criterion

Define $\Delta_i(x)=\mu^i(x^*)-\mu^i(x)$ and signed coordinate regret $R_i(T)=\sum_{t=1}^T\Delta_i(X_t)$. The simultaneous expected criterion is $\max_{i\le2}\mathbb E R_i(T)$. The secondary regret can be negative, so the maximum is taken after each expectation.

### Resource accounting

There is one arm pull and two scalar reward observations per round, so the fixed horizon is $T$, the pull count is $T$, and the number of observed reward coordinates is $2T$. Computation and storage are unrestricted.

Metric-net computation and reward samples are separate resources. The comparison is information theoretic and does not charge the net construction.

### Algorithm views and success guarantees

All measurable randomized causal policies may use T, the metric, and the declared maximal-net interface. The upper policy is independent of the tradeoff and of the near-optimality packing parameters.

$$
\forall\nu:\quad\max_{i\le2}\mathbb E_\nu R_i(T)\le r
$$

The supremum is over fixed Lipschitz means and admissible conditional reward laws on the specified public metric space.

**Budget convention.** fixed_horizon

## 2. Notation and parameters

$T$: Horizon **Domain:** $T\ge2$ integer.

$(\mathcal X,D)$: Public compact metric arm space **Domain:** $\operatorname{diam}(\mathcal X)\le1$.

$\lambda_*$: Unknown local tradeoff **Domain:** $\lambda_*\in[0,\infty]$.

$S$: Compact tie component in the anchor-plus-tie regimes **Domain:** $S\ne\varnothing$, $\operatorname{diam}(S)\le1/4$.

$a$: Anchor arm **Domain:** $\mathcal X=\{a\}\cup S$, $D(a,z)=1$ for z in S.

$d_p$: Packing-growth exponent **Domain:** $d_p\ge0$.

$Z$: Packing-profile size coefficient **Domain:** $Z\ge1$.

$c_-,c_+$: Regular metric packing and covering constants **Domain:** $c_-,c_+>0$.

$r_0$: Maximum radius in regular metric growth assumptions **Domain:** $0<r_0\le1/16$.

$r_s$: Dyadic radius for the entropy frontier **Domain:** $s\ge0$ integer, $r_s>0$.

$r_s=2^{-s-4}$

$s_T$: Final dyadic entropy scale **Domain:** $s_T\in\mathbb N$.

$s_T=\lceil\log_2(16T)\rceil+2$

$M_s$: Tie-space packing number **Domain:** $M_s\ge1$.

$M_s=\operatorname{Pack}(S,r_s)$

$\Psi_T^\infty(S)$: Critical entropy regret scale **Domain:** $\Psi_T^\infty(S)>0$.

$\Psi_T^\infty(S)=T\max_{0\le s\le s_T}\min\{r_s,(M_s/T)^{1/3}\}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathfrak M_T(\mathcal X)=\inf_\pi\sup_{\nu\in\mathcal F(\mathcal X)}\max_{i\le2}\mathbb E_\nu R_i(T)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $T$; description: Each played round and its prescribed feedback are charged.

### R1 - Arbitrary compact anchor-plus-tie entropy

**Region.** $T\ge2$; $\mathcal X=\{a\}\cup S$, $D(a,S)=1$, and S is nonempty compact with diameter at most 1/4; no envelope is supplied. An arbitrary compact metric space; all dependence on metric complexity is explicit through the packing numbers M_s. The bound is metric-wise on the specified anchor-plus-tie geometry, not a lower bound for every subclass satisfying only a one-sided profile upper bound.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(\Psi_T^\infty(S))
$$

**Upper bound.** B1

$$
O(\log^{2/3}(eT)\Psi_T^\infty(S))
$$

**Gap or comparison.** Ratio at most $O(\log^{2/3}(eT))$.

### R2 - Regular packing growth on anchor-plus-tie spaces

**Region.** $\mathcal X=\{a\}\cup S$, $D(a,S)=1$, $\operatorname{diam}(S)\le1/4$; fix $d_p\ge0$, $c_-,c_+>0$, $0<r_0\le1/16$. For some $Z\ge1$, require $\operatorname{Pack}(S,4r)\ge c_-Zr^{-d_p}$ and $\operatorname{Cov}(S,r)\le c_+Zr^{-d_p}$ for all $0<r\le r_0$. d_p is a metric packing exponent, not an ambient Euclidean dimension. It and c_-,c_+,r_0 are fixed in the source matching statement.

**Quantity.** Q1

**Resource.** Each played round and its prescribed feedback are charged.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\widetilde\Omega_{d_p,c_-,c_+,r_0}(\min\{T,Z^{1/(d_p+3)}T^{(d_p+2)/(d_p+3)}\})
$$

**Upper bound.** B3

$$
\widetilde O_{d_p,c_-,c_+,r_0}(\min\{T,Z^{1/(d_p+3)}T^{(d_p+2)/(d_p+3)}\})
$$

**Gap or comparison.** Only logarithmic factors remain with the listed metric regularity constants fixed.

## 4. Bounds and supporting evidence

### B1 - Multiscale primary filtering and entropy crossing.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\log^{2/3}(eT)\Psi_T^\infty(S))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $T\ge2$; $\mathcal X=\{a\}\cup S$, $D(a,S)=1$, and S is nonempty compact with diameter at most 1/4; no envelope is supplied.; The bound is metric-wise on the specified anchor-plus-tie geometry, not a lower bound for every subclass satisfying only a one-sided profile upper bound.

**Dimension conditions.** An arbitrary compact metric space; all dependence on metric complexity is explicit through the packing numbers M_s.

**Constants.** Universal constants.

**Logarithmic factors.** Only the displayed horizon logarithm.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:entropy; Section sec:entropy; Appendix app:entropy

Multiscale primary filtering and entropy crossing.. Policies with metric-net access; no entropy sequence or tradeoff information is required.

### B2 - One-scale separated primary improvements around a primary-tie set.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\Omega(\Psi_T^\infty(S))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $T\ge2$; $\mathcal X=\{a\}\cup S$, $D(a,S)=1$, and S is nonempty compact with diameter at most 1/4; no envelope is supplied.; The bound is metric-wise on the specified anchor-plus-tie geometry, not a lower bound for every subclass satisfying only a one-sided profile upper bound.

**Dimension conditions.** An arbitrary compact metric space; all dependence on metric complexity is explicit through the packing numbers M_s.

**Constants.** Universal constants.

**Logarithmic factors.** Only the displayed horizon logarithm.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:entropy; Appendix app:entropy

One-scale separated primary improvements around a primary-tie set.. Every randomized causal policy with the declared metric information.

### B3 - Profile-oblivious primary filtering.

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O_{d_p,c_-,c_+,r_0}(\min\{T,Z^{1/(d_p+3)}T^{(d_p+2)/(d_p+3)}\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $\mathcal X=\{a\}\cup S$, $D(a,S)=1$, $\operatorname{diam}(S)\le1/4$; fix $d_p\ge0$, $c_-,c_+>0$, $0<r_0\le1/16$. For some $Z\ge1$, require $\operatorname{Pack}(S,4r)\ge c_-Zr^{-d_p}$ and $\operatorname{Cov}(S,r)\le c_+Zr^{-d_p}$ for all $0<r\le r_0$.

**Dimension conditions.** d_p is a metric packing exponent, not an ambient Euclidean dimension. It and c_-,c_+,r_0 are fixed in the source matching statement.

**Constants.** Constants may depend on the fixed d_p,c_-,c_+,r_0, and are uniform in T and Z.

**Logarithmic factors.** Logarithmic factors in T and displayed profile parameters only. No dimension-uniform claim in varying d_p is asserted.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:regular-metric; Corollary cor:power-upper

Profile-oblivious primary filtering.. One policy independent of the regularity and tradeoff parameters.

### B4 - Disjoint hidden cone improvements on a regular tie space.

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde\Omega_{d_p,c_-,c_+,r_0}(\min\{T,Z^{1/(d_p+3)}T^{(d_p+2)/(d_p+3)}\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf)

**Conditions.** $\mathcal X=\{a\}\cup S$, $D(a,S)=1$, $\operatorname{diam}(S)\le1/4$; fix $d_p\ge0$, $c_-,c_+>0$, $0<r_0\le1/16$. For some $Z\ge1$, require $\operatorname{Pack}(S,4r)\ge c_-Zr^{-d_p}$ and $\operatorname{Cov}(S,r)\le c_+Zr^{-d_p}$ for all $0<r\le r_0$.

**Dimension conditions.** d_p is a metric packing exponent, not an ambient Euclidean dimension. It and c_-,c_+,r_0 are fixed in the source matching statement.

**Constants.** Constants may depend on the fixed d_p,c_-,c_+,r_0, and are uniform in T and Z.

**Logarithmic factors.** Logarithmic factors in T and displayed profile parameters only. No dimension-uniform claim in varying d_p is asserted.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf) Theorem thm:regular-metric; Appendix app:metric-lower

Disjoint hidden cone improvements on a regular tie space.. All randomized causal policies.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U07. Primary Ties and the Price of Unknown Trade-offs in Lexicographic Bandits. primary_ties_unknown_tradeoffs.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U07/manuscript.pdf
