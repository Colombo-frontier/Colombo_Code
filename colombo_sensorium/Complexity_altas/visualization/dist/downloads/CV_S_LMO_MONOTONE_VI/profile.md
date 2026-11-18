# Monotone VIs with operator values and a linear-minimization interface.

**Setting ID.** `CV_S_LMO_MONOTONE_VI`

Variational inequalities

Solve the monotone VI $0\in F(z)+N_K(z)$, measuring error by weak gap.

**Status.** Joint budget unresolved

**TASK tags.** solution concept: Weak gap; task family: Variational inequality

**MODEL tags.** monotonicity: Monotone operator; monotonicity: Monotonicity

**ORACLE tags.** feedback quality: Exact; interface family: Operator and lmo; operation: Linear minimization; operation: Operator value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; support: Returned atom hull

**METRIC tags.** criterion: Weak gap

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N lmo; measure: N operator value; setup: Initialization included

## 1. Setting specification

### Task

Solve the monotone VI $0\in F(z)+N_K(z)$, measuring error by weak gap.

### Admissible model

The set $K\subset\mathbb{R}^d$ is hidden, nonempty, compact, and convex. An enclosing ball, a diameter bound $D_K$, and a feasible point $z_0$ are public. The operator $F$ is monotone and $\beta$-Lipschitz on $K$.

The complete analytic set description is hidden. No extra information sufficient for free projection is supplied.

### Oracle interface

$$
z\in K\longmapsto F(z),\qquad c\in\mathbb{R}^d\longmapsto s(c)\in\arg\min_{s\in K}\langle c,s\rangle.
$$

Both responses are exact. Ties in linear minimization are resolved by an admissible deterministic rule fixed before interaction. Correctness is required for every such rule.

### Output

The output $\widehat{z}$ must lie in the convex hull of $z_0$ and all returned $s(c)$.

### Loss or accuracy criterion

$$
G_M(\widehat{z})=\sup_{u\in K}\langle F(u),\widehat{z}-u\rangle.
$$

### Resource accounting

The joint budget is $(N_F,N_{\rm LMO})$; each operation adds $1$ to its corresponding coordinate. Preserve jointly attainable budgets. Without specified weights, do not sum coordinates or combine coordinatewise bounds from different algorithms.

A fixed joint budget $(B_F,B_{\rm LMO})$ requires $N_F\le B_F$ and $N_{\rm LMO}\le B_{\rm LMO}$ on every admissible instance and every execution path. Early stopping within this budget is allowed.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

Deterministic adaptive algorithms are allowed. Feasible queries and outputs are constructed from the public initial point and returned atoms. Queries outside the unknown set cannot be used to obtain additional information.

The same deterministic algorithm must satisfy the guarantee for every admissible instance.

$$
G_M(\widehat{z})\le\varepsilon.
$$

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$D_K$: A Euclidean-diameter bound on the feasible domain. **Domain:** Positive real number.

$\operatorname{diam}(K)=\sup_{u,v\in K}\|u-v\|_2\le D_K$

$\beta$: Euclidean Lipschitz upper bound for the population operator on the declared query domain **Domain:** Positive real number.

$\|F(z)-F(w)\|_2\le\beta\|z-w\|_2$

$d$: Finite Euclidean dimension of the operator domain; regime quantifiers specify whether complexity is uniform in dimension **Domain:** Positive integer.

$\varepsilon$: Target tolerance for the complete weak-VI gap or global saddle gap, in the units of that gap. **Domain:** Positive real number.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$F$: The unknown operator is single-valued. Monotonicity, strong monotonicity, or weak Minty properties use the specification’s explicit inequalities. **Domain:** A vector map from the declared query domain into $\mathbb R^d$.

$z,u,v$: The operator argument and comparison point in the inequality. **Domain:** The ambient space is $\mathbb R^d$. Formulas constrained by $K$ require the corresponding point to lie in $K$.

$K$: Hidden nonempty compact convex feasible set; only an enclosing ball, diameter bound, and initial point are public. **Domain:** A subset of Euclidean space.

$K\subset\mathbb R^d$

$N_K(z)$: Use the Euclidean normal cone of the closed convex feasible set K at the feasible point z. The same definition applies blockwise to $N_X$ and $N_Y$. **Domain:** $z\in K,\quad N_K(z)\subset\mathbb R^d$.

$N_K(z)=\{v:\langle v,u-z\rangle\le0\ \forall u\in K\}$

$z_0,z^\star$: Public initial point and the same solution appearing in the model assumption **Domain:** Feasible domain of this profile; the distance bound refers to the same solution.

$\widehat z$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** $K\subset\mathbb R^d$.

$N_F$: The number of complete exact operator-value calls. **Domain:** Nonnegative integer count; expected work is its expectation.

$N_{\rm LMO}$: Number of linear minimization oracle calls **Domain:** Nonnegative integer count; expected work is its expectation.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$c,s(c)$: Linear-objective vector and a minimizer returned by the LMO **Domain:** $c\in\mathbb R^d,\ s(c)\in K$.

$s(c)\in\arg\min_{u\in K}\langle c,u\rangle$

$G_M$: The weak VI gap at the current feasible point. **Domain:** A nonnegative real.

$G_M(z)=\sup_{u\in K}\langle F(u),z-u\rangle$

$B_F,B_{\rm LMO}$: One algorithm simultaneously meets the fixed operator-value and LMO budgets. **Domain:** Pair of nonnegative integers.

## 3. Complexity bracket

### Compared quantities

#### Q1 - achievable resource region

$$
\mathcal B_v(\varepsilon;\theta)=\{b\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_j(\mathcal A,I)\le b_j\ \forall j,I,\quad G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Jointly attainable budgets under the stated success guarantee

**Scope.** The full documented joint parameter domain in D_K, beta, d and epsilon, with deterministic Minty-gap guarantee and fixed worst-case two-coordinate budgets. Admitted bounds and their guards are recorded in bounds and comparisons.

**Optimization direction.** pareto_minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - The declared parameter domain.

**Region.** All admissible parameters in the eight-part specification; subregions with two-sided evidence have not yet been separated.

**Quantity.** Q1

**Resource.** Identity projection on the declared joint resource vector; no scalar weights are supplied.

**Status.** Joint budget unresolved

**Achievable budgets.** B1, B2, B3

**Necessary constraints.** B4

**Gap or comparison.** For epsilon>=beta D_K^2, the attainable budget region is exactly {B_F>=1,B_LMO>=1}. Otherwise only inner/outer budget-region inclusions are proved; no scalar ratio is defined for this unweighted vector resource. For d=1 the LMO coordinate is exactly 1 with the stated operator allowance. For d>=2 the recorded operator allowance is O(1+R), LMO allowance O((1+R)^2), while necessity only gives B_F>=1 and B_LMO>=max(1,[1/(d+1)+8/R]^-1-1).

### R2 - Exact coarse joint(1,1)budget region

**Region.** epsilon>=beta*D_K^2; D_K>0,beta>0,epsilon>0,d a positive integer; exact unchanged hidden-K, deterministic all-legal-oracles, atom-hull output contract.

**Quantity.** Q1

**Resource.** Identity projection on the declared joint resource vector; no scalar weights are supplied.

**Status.** Optimal

**Achievable budgets.** B2

**Necessary constraints.** B4

**Gap or comparison.** Exact attainable region {BF>=1,BLMO>=1}, minimum vector(1,1). Scalar multiplicative ratio is inapplicable.

**Comparison argument.** CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

## 4. Bounds and supporting evidence

### B1 - upper

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

**Local argument.** CV_S_LMO_MONOTONE_VI__proof_spmp

### B2 - upper

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

**Local argument.** CV_S_LMO_MONOTONE_VI__proof_one_pair

### B3 - upper

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** upper

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

**Local argument.** CV_S_LMO_MONOTONE_VI__proof_interval

### B4 - lower

**Admission.** Not admitted to the bracket; retained for traceability

**Direction.** lower

**Witness or lower-bound scope.** Algorithm scope stated in the evidence below

**Local argument.** CV_S_LMO_MONOTONE_VI__proof_necessary

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: f63171fffc3646f099ce398d805b98406e627c54abd1e2a160ce5904a1bb6625

### Native proof: CV_S_LMO_MONOTONE_VI__proof_spmp

Native pointer: /proofs/0; canonical SHA-256: 1b0627744d9d02543aa548888795e815c34dfb609ace6425d814a05c1b3e2de4

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: 015dfaaf96532270b059c51b3aff98bb3fc3ffd3acade4c668efe998497649db

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: 81dc163dfb302c91d3fafd779f7ebaaa8b8727c6908c5490a49d91bd670799bf

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: 895d940455206702d1e66f411c95b9e78b4fad25685090c205a5973ebbb6530c

0d21d6ef29a61c579e8cdeba4c335aa3372dfb037604326fffd8f5fad7a54c0a

#### Native item 2

Native pointer: /proofs/0/baseline_refs/1; canonical SHA-256: 5072ded359a4eb3df3f619eb8aff57ba95142adfe39bfa6f1d77efe9c0e335dd

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/1/sha256; canonical SHA-256: f28266ac6e509744135b4364170f8c76a0ce8b1dee192f8c5122d47248f7a7a2

2c7b1df600523d1be2112a79ff1211ff1d895ebf665cae0d2296757a15f3a21a

#### Native item 3

Native pointer: /proofs/0/baseline_refs/2; canonical SHA-256: fb96603310c46beda0b58a152467ef921524083f4ef31bcbb406003ae36f73f2

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/2/sha256; canonical SHA-256: 58af2b3883b83fc2f48e17b445ae6c78e69b661a980802a1e50e42e8a4d847af

19534c6f68b542d5e3883b8d52516e41313dd97f94a1fd509ea7f84df4019531

#### Native item 4

Native pointer: /proofs/0/baseline_refs/3; canonical SHA-256: 37ba47c329179fd19333b2b289dea4fe55730d773c54ab5cab38b27dedb90d25

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/3/sha256; canonical SHA-256: 974745f0da8135c40e3bcfbb91eaf3f29f119668eabb638ea9b0f1346e81a1e3

eac332745d9f91823e5f0d2de62b28a5d0b4716d2f0550d74b50d8e79e507a4e

#### Native item 5

Native pointer: /proofs/0/baseline_refs/4; canonical SHA-256: 95b02ce40db0ba35b94e7c2c9b9a82043bb340e6f27caecaf4c93b457d00e391

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/4/sha256; canonical SHA-256: d7c08b935fbf2c77e94727712c5a936aa6e58bea820c6a04ae8ec30c582ad8be

7b134acce0b9ee091a0367735d14eb2ba3119d0ea243dd61643106b4476f0aec

#### Native field: bound_refs

Native pointer: /proofs/0/bound_refs; canonical SHA-256: 2a634a02e07767fa7501dd85452f8a8da153a0cceff65ac50138a1313ca6a6c5

#### Native item 1

Native pointer: /proofs/0/bound_refs/0; canonical SHA-256: e92a94bb27a4b8f02591e6708b3732cfc3abb5998f8510ed22d0405164cb7ed0

CV_S_LMO_MONOTONE_VI__main__b_spmp

#### Native field: proof

Native pointer: /proofs/0/proof; canonical SHA-256: 519cc27daa7ded8fde9ab99385a3f593e1d1fe2729c7afb83589a63d58e79128

Write D=D_K, eta=1/beta, C=D^2, delta=epsilon/(4beta), R=beta D^2/epsilon. To approximately minimize q(w)=eta<g,w>+||w-x||^2/2 over K, initialize s0=LMO(g). Since s0 minimizes the linear term, H0=q(s0)-min q<=C/2 and its FW gap G0=max_v<eta g+s0-x,s0-v><=C. Thus no bound on ||g|| is required. Quadratic smoothness gives q(s+alpha(v-s))<=q(s)-alpha G(s)+C alpha^2/2, where v=LMO(eta g+s-x). If delta>=C return s0. Otherwise run m=ceil(8C/delta) FW updates with alpha_j=2/(j+2), j=0,...,m-1. Convexity gives G>=H; induction in the preceding descent inequality yields H_m<=2C/(m+2)<delta/4. Now test G using one LMO per test. If G>delta, update with alpha=delta/C. Each failure reduces q by strictly more than delta^2/(2C). Consequently one of n=ceil(C/(2delta)) tests must succeed, since n failures would reduce q by at least delta/4, contradicting H_m<delta/4. Each prox therefore costs at most Q=1+ceil(32R)+ceil(2R) LMO calls; it uses no new F calls. All updates are convex combinations of already feasible points and returned atoms. Use x1=z0; for t=1,...,T=ceil(R), query F(xt), compute yt with this prox at center xt, query F(yt), and compute x(t+1) with the same center and g=F(yt). A successful gap test gives <eta g+w-x,w-u><=delta for every u in K. The two inequalities, the identity for squared distances and eta beta=1 give eta<F(yt),yt-u><=(||xt-u||^2-||x(t+1)-u||^2)/2+2delta: the remaining cross term eta<F(yt)-F(xt),yt-x(t+1)> is absorbed by (||yt-xt||^2+||yt-x(t+1)||^2)/2. This is also Theorem 3.1 in the read source. Sum over t and use monotonicity <F(u),yt-u><=<F(yt),yt-u>. The average ybar has Minty gap <=beta D^2/(2T)+2beta delta<=epsilon. Costs on every execution path are at most (2T,2TQ), including initialization, with all F queries and output in the permitted atom hull. Linear minimizers need not be vertices or unique; every legal tie choice satisfies the proof.

#### Native field: reference_refs

Native pointer: /proofs/0/reference_refs; canonical SHA-256: f9a238b627f815d7af576cc300c5db2b6e8bdfa80d14d4f596bdbe7d53250005

#### Native item 1

Native pointer: /proofs/0/reference_refs/0; canonical SHA-256: 662dbed8e47cb1449ad07daef87dd27a3d8269def745b3fc363bf22815bebd39

CV_S_LMO_MONOTONE_VI__ref_1507_01476v1

#### Native field: source_hashes

Native pointer: /proofs/0/source_hashes; canonical SHA-256: a1a1fbc26b25177d1943b5dbf1dfedec0fdbfd1b007016bae9557d6488097f59

#### Native item 1

Native pointer: /proofs/0/source_hashes/0; canonical SHA-256: 7a78d3cbc3b7c064a62409c7bbf49ccc9755172aac351eaefdc7cef41a7fd021

c6379033381588a1c92fcf22c15653801ddf441765115a435e429a75e1e3dfb7

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: a5aaeac17dab70082668b18225219bd4c4c1ceedd28df6e06b95d483733d7d03

Uniform full-LMO specialization and explicit query caps.

### Native proof: CV_S_LMO_MONOTONE_VI__proof_one_pair

Native pointer: /proofs/1; canonical SHA-256: a9047a2a5b556d66f82ecd8d2307374ffa7cf288e3969f778d21f5f4f5505c29

#### Native field: baseline_refs

Native pointer: /proofs/1/baseline_refs; canonical SHA-256: 015dfaaf96532270b059c51b3aff98bb3fc3ffd3acade4c668efe998497649db

#### Native item 1

Native pointer: /proofs/1/baseline_refs/0; canonical SHA-256: 81dc163dfb302c91d3fafd779f7ebaaa8b8727c6908c5490a49d91bd670799bf

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/0/sha256; canonical SHA-256: 895d940455206702d1e66f411c95b9e78b4fad25685090c205a5973ebbb6530c

0d21d6ef29a61c579e8cdeba4c335aa3372dfb037604326fffd8f5fad7a54c0a

#### Native item 2

Native pointer: /proofs/1/baseline_refs/1; canonical SHA-256: 5072ded359a4eb3df3f619eb8aff57ba95142adfe39bfa6f1d77efe9c0e335dd

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/1/sha256; canonical SHA-256: f28266ac6e509744135b4364170f8c76a0ce8b1dee192f8c5122d47248f7a7a2

2c7b1df600523d1be2112a79ff1211ff1d895ebf665cae0d2296757a15f3a21a

#### Native item 3

Native pointer: /proofs/1/baseline_refs/2; canonical SHA-256: fb96603310c46beda0b58a152467ef921524083f4ef31bcbb406003ae36f73f2

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/2/sha256; canonical SHA-256: 58af2b3883b83fc2f48e17b445ae6c78e69b661a980802a1e50e42e8a4d847af

19534c6f68b542d5e3883b8d52516e41313dd97f94a1fd509ea7f84df4019531

#### Native item 4

Native pointer: /proofs/1/baseline_refs/3; canonical SHA-256: 37ba47c329179fd19333b2b289dea4fe55730d773c54ab5cab38b27dedb90d25

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/3/sha256; canonical SHA-256: 974745f0da8135c40e3bcfbb91eaf3f29f119668eabb638ea9b0f1346e81a1e3

eac332745d9f91823e5f0d2de62b28a5d0b4716d2f0550d74b50d8e79e507a4e

#### Native item 5

Native pointer: /proofs/1/baseline_refs/4; canonical SHA-256: 95b02ce40db0ba35b94e7c2c9b9a82043bb340e6f27caecaf4c93b457d00e391

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/4/sha256; canonical SHA-256: d7c08b935fbf2c77e94727712c5a936aa6e58bea820c6a04ae8ec30c582ad8be

7b134acce0b9ee091a0367735d14eb2ba3119d0ea243dd61643106b4476f0aec

#### Native field: bound_refs

Native pointer: /proofs/1/bound_refs; canonical SHA-256: 1ffd9e93b47e6f1a967eefa79e06882e472da04d7fb6e33d1522aec28b439198

#### Native item 1

Native pointer: /proofs/1/bound_refs/0; canonical SHA-256: 626e2b5c0f78d9dcff026456a13519721fb49c1de672c9d8456f2536d7c8d632

CV_S_LMO_MONOTONE_VI__main__b_one_pair

#### Native field: proof

Native pointer: /proofs/1/proof; canonical SHA-256: d823b99e1b2e8d1212d3fe2ee46b50f109ce287f3eab972374fa5e0564b7f4ba

Query g=F(z0), then s=LMO(g), and output s. For every u in K, <F(u),s-u>=<g,s-u>+<F(u)-g,s-u><=beta||u-z0||||s-u||<=beta D_K^2, because <g,s-u><=0 by exact linear minimization. This holds for all legal fixed tie choices, and output s is an allowed atom. Thus epsilon>=beta D_K^2 admits budget (1,1). Combined with the independently proved necessary B_F,B_LMO>=1, this determines the entire attainable budget region on this sufficient coarse region. The threshold is an exact sufficient algorithm threshold; no assertion of its sharpness is made.

#### Native field: source_hashes

Native pointer: /proofs/1/source_hashes; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/1/statement; canonical SHA-256: 2f133705a4d77d35b5f58db70359250cfaaace2cc8fed2ed31cf8f28035ef8a9

One-pair coarse-accuracy upper bound.

### Native proof: CV_S_LMO_MONOTONE_VI__proof_interval

Native pointer: /proofs/2; canonical SHA-256: 01d52dd0cbf17958019918bd2ea4af9c185f2d0673bf1cea927ccfd5ee1f320d

#### Native field: baseline_refs

Native pointer: /proofs/2/baseline_refs; canonical SHA-256: 015dfaaf96532270b059c51b3aff98bb3fc3ffd3acade4c668efe998497649db

#### Native item 1

Native pointer: /proofs/2/baseline_refs/0; canonical SHA-256: 81dc163dfb302c91d3fafd779f7ebaaa8b8727c6908c5490a49d91bd670799bf

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/0/sha256; canonical SHA-256: 895d940455206702d1e66f411c95b9e78b4fad25685090c205a5973ebbb6530c

0d21d6ef29a61c579e8cdeba4c335aa3372dfb037604326fffd8f5fad7a54c0a

#### Native item 2

Native pointer: /proofs/2/baseline_refs/1; canonical SHA-256: 5072ded359a4eb3df3f619eb8aff57ba95142adfe39bfa6f1d77efe9c0e335dd

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/1/sha256; canonical SHA-256: f28266ac6e509744135b4364170f8c76a0ce8b1dee192f8c5122d47248f7a7a2

2c7b1df600523d1be2112a79ff1211ff1d895ebf665cae0d2296757a15f3a21a

#### Native item 3

Native pointer: /proofs/2/baseline_refs/2; canonical SHA-256: fb96603310c46beda0b58a152467ef921524083f4ef31bcbb406003ae36f73f2

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/2/sha256; canonical SHA-256: 58af2b3883b83fc2f48e17b445ae6c78e69b661a980802a1e50e42e8a4d847af

19534c6f68b542d5e3883b8d52516e41313dd97f94a1fd509ea7f84df4019531

#### Native item 4

Native pointer: /proofs/2/baseline_refs/3; canonical SHA-256: 37ba47c329179fd19333b2b289dea4fe55730d773c54ab5cab38b27dedb90d25

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/3/sha256; canonical SHA-256: 974745f0da8135c40e3bcfbb91eaf3f29f119668eabb638ea9b0f1346e81a1e3

eac332745d9f91823e5f0d2de62b28a5d0b4716d2f0550d74b50d8e79e507a4e

#### Native item 5

Native pointer: /proofs/2/baseline_refs/4; canonical SHA-256: 95b02ce40db0ba35b94e7c2c9b9a82043bb340e6f27caecaf4c93b457d00e391

#### Native field: pointer

Native pointer: /proofs/2/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/2/baseline_refs/4/sha256; canonical SHA-256: d7c08b935fbf2c77e94727712c5a936aa6e58bea820c6a04ae8ec30c582ad8be

7b134acce0b9ee091a0367735d14eb2ba3119d0ea243dd61643106b4476f0aec

#### Native field: bound_refs

Native pointer: /proofs/2/bound_refs; canonical SHA-256: 3a9c4c7a753896f2764e24a5a273948f25f842305612439c5e357f0b190fc6ae

#### Native item 1

Native pointer: /proofs/2/bound_refs/0; canonical SHA-256: b09e4cbf9094e0eed8e5b6eb32c6dbdaf2f93ba6c9bfb32cb29fbfcbd02215c9

CV_S_LMO_MONOTONE_VI__main__b_interval

#### Native field: proof

Native pointer: /proofs/2/proof; canonical SHA-256: 9e2fcb0f8f2dce4a2a3188f69ff6b9de0761679175941e199ee19eb4fa07134b

When d=1, compact convex K is a closed interval, possibly a point, and monotonicity means F is nondecreasing. Query F(z0). If it is zero, z0 has zero Minty gap. Otherwise call LMO(F(z0)); the unique relevant endpoint a is the left endpoint when F(z0)>0 and the right endpoint when F(z0)<0. Query F(a). If F(a) has the same weak sign as F(z0), output a, which solves the VI exactly. Otherwise a and z0 bracket signs. Write the ordered bracket [l,r] with F(l)<=0<=F(r). Repeatedly query its midpoint and retain a sign bracket (stop if the value is zero). After k=max(0,ceil(log2(beta D_K^2/epsilon)/2)) queries the bracket length h<=D_K/2^k. Output its midpoint z. For u outside [l,r], monotonicity gives F(u)(z-u)<=0. Inside, the endpoint signs and Lipschitz property give |F(u)|<=beta h and |z-u|<=h, so F(u)(z-u)<=beta h^2<=epsilon. Every queried point and the output is a convex combination of z0 and the sole returned atom. Costs are at most (2+k,1), including initialization. On epsilon<beta D_K^2, this dominates the main construction: for R>1, (log2 R)/2<=R-1, hence k<=ceil(R)-1 and 2+k<=2ceil(R); its LMO allowance is also smaller. On epsilon>=beta D_K^2 the one-pair upper bound dominates this cap.

#### Native field: source_hashes

Native pointer: /proofs/2/source_hashes; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/2/statement; canonical SHA-256: 9b75fba411ff7390f8e353eaf1286832ba9248c24513e38c12c29c40cdfabd0f

Dimension-one bisection using one LMO.

### Native proof: CV_S_LMO_MONOTONE_VI__proof_necessary

Native pointer: /proofs/3; canonical SHA-256: c8961874a7e9bf2a84880fd8458557a98ae282ae4c6e7c1011c0360c096112fe

#### Native field: baseline_refs

Native pointer: /proofs/3/baseline_refs; canonical SHA-256: 015dfaaf96532270b059c51b3aff98bb3fc3ffd3acade4c668efe998497649db

#### Native item 1

Native pointer: /proofs/3/baseline_refs/0; canonical SHA-256: 81dc163dfb302c91d3fafd779f7ebaaa8b8727c6908c5490a49d91bd670799bf

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/0/sha256; canonical SHA-256: 895d940455206702d1e66f411c95b9e78b4fad25685090c205a5973ebbb6530c

0d21d6ef29a61c579e8cdeba4c335aa3372dfb037604326fffd8f5fad7a54c0a

#### Native item 2

Native pointer: /proofs/3/baseline_refs/1; canonical SHA-256: 5072ded359a4eb3df3f619eb8aff57ba95142adfe39bfa6f1d77efe9c0e335dd

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/1/sha256; canonical SHA-256: f28266ac6e509744135b4364170f8c76a0ce8b1dee192f8c5122d47248f7a7a2

2c7b1df600523d1be2112a79ff1211ff1d895ebf665cae0d2296757a15f3a21a

#### Native item 3

Native pointer: /proofs/3/baseline_refs/2; canonical SHA-256: fb96603310c46beda0b58a152467ef921524083f4ef31bcbb406003ae36f73f2

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/2/sha256; canonical SHA-256: 58af2b3883b83fc2f48e17b445ae6c78e69b661a980802a1e50e42e8a4d847af

19534c6f68b542d5e3883b8d52516e41313dd97f94a1fd509ea7f84df4019531

#### Native item 4

Native pointer: /proofs/3/baseline_refs/3; canonical SHA-256: 37ba47c329179fd19333b2b289dea4fe55730d773c54ab5cab38b27dedb90d25

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/3/sha256; canonical SHA-256: 974745f0da8135c40e3bcfbb91eaf3f29f119668eabb638ea9b0f1346e81a1e3

eac332745d9f91823e5f0d2de62b28a5d0b4716d2f0550d74b50d8e79e507a4e

#### Native item 5

Native pointer: /proofs/3/baseline_refs/4; canonical SHA-256: 95b02ce40db0ba35b94e7c2c9b9a82043bb340e6f27caecaf4c93b457d00e391

#### Native field: pointer

Native pointer: /proofs/3/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/3/baseline_refs/4/sha256; canonical SHA-256: d7c08b935fbf2c77e94727712c5a936aa6e58bea820c6a04ae8ec30c582ad8be

7b134acce0b9ee091a0367735d14eb2ba3119d0ea243dd61643106b4476f0aec

#### Native field: bound_refs

Native pointer: /proofs/3/bound_refs; canonical SHA-256: 4ff4d1ce6e0ba6f32924d6c8eba080c62b738219753b93b67cd4c253e06b0593

#### Native item 1

Native pointer: /proofs/3/bound_refs/0; canonical SHA-256: d0194442f7f6f39a94d3dd45088b62f63be57f907d469d4dc3ef8c3335481696

CV_S_LMO_MONOTONE_VI__main__b_necessary

#### Native field: proof

Native pointer: /proofs/3/proof; canonical SHA-256: 557de0c97ab8a19b63e08705063b60e9498d6148ca1e26425cc60f1093bf517c

First, use K=[-D_K/2,D_K/2]e1 in R^d and public z0=0, with identical public enclosing ball and identical legal LMO rule. Constant fields F=+M e1 and F=-M e1 are monotone and beta-Lipschitz for every M. Without an F query, the deterministic transcript and output are identical on these two instances. At least one weak gap is >=M D_K/2, so M>2epsilon/D_K rules out every cap B_F<1. Without an LMO call, the allowed output hull is {z0}; the constant field +M e1 then has gap M D_K/2 irrespective of F queries, ruling out B_LMO<1. Thus no uniform zero-query region exists at any finite positive epsilon. For the rate-dependent constraint, let K be a regular d-simplex in R^d with d+1 centered vertices v_i of side D_K, public z0=v_1, and F(x)=beta x. It is an admissible monotone beta-Lipschitz instance. Choose a legal deterministic LMO rule that returns a minimizing vertex, with fixed index tie-breaking; target correctness must cover this rule. After m LMO calls, the output z is supported on at most m+1 vertices. The Gram matrix has <v_i,v_j>=(D_K^2/2)(1_{i=j}-1/(d+1)), so for z=sum lambda_i v_i, ||z||^2=(D_K^2/2)(sum lambda_i^2-1/(d+1))>=(D_K^2/2)(1/(m+1)-1/(d+1)). Here sum lambda_i=1, lambda_i>=0, and Cauchy-Schwarz on the support proves sum lambda_i^2>=1/(m+1). The inequality remains valid, though possibly trivial, when m>=d. Since 0 in K and u=z/2 in K, Minty gap >=<beta z/2,z/2>=beta||z||^2/4. Consequently epsilon accuracy requires 1/(m+1)<=1/(d+1)+8epsilon/(beta D_K^2). Since m<=B_LMO, the stated necessary budget inequality follows. Operator queries cannot evade the hull support constraint; there are no additional target assumptions. This constructs a subclass of the original target preserving queries, output restriction, deterministic guarantee and both cost coordinates. The bound is meaningful up to the finite-dimensional support scale d, not a theorem of exact reconstruction or uniform saturation at d calls.

#### Native field: source_hashes

Native pointer: /proofs/3/source_hashes; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/3/statement; canonical SHA-256: 39961ba16b583f2f40665d0ca9a9f1d7b6919c80736c1202abef6a05a296abdf

Necessary joint constraints, zero-query exclusion, and simplex support lower bound.

### Native proof: CV_S_LMO_MONOTONE_VI__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/4; canonical SHA-256: ad9c32206f6b48f11cd2feae2c90f4aeb2c17dc44b683c224a775dcf0c5e7808

#### Native field: body

Native pointer: /proofs/4/body; canonical SHA-256: 684c665b3c4a236b79d382a25b94eb03fc9570c5fe4b721f3a0d02e3cd7a093a

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. 

#### Native field: comparison_refs

Native pointer: /proofs/4/comparison_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: evidence_basis

Native pointer: /proofs/4/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/4/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/4/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

### Native proof: CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

Native pointer: /proofs/5; canonical SHA-256: 6d2fe2048daca815fa624eff7048478e694a45d033a0edb552be57bde599b65c

#### Native field: baseline_refs

Native pointer: /proofs/5/baseline_refs; canonical SHA-256: 792ccaa44f3303ba08a9dea9243759d307f5ef3c96375dbd100f0eea5c495732

#### Native item 1

Native pointer: /proofs/5/baseline_refs/0; canonical SHA-256: 81dc163dfb302c91d3fafd779f7ebaaa8b8727c6908c5490a49d91bd670799bf

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/0/sha256; canonical SHA-256: 895d940455206702d1e66f411c95b9e78b4fad25685090c205a5973ebbb6530c

0d21d6ef29a61c579e8cdeba4c335aa3372dfb037604326fffd8f5fad7a54c0a

#### Native item 2

Native pointer: /proofs/5/baseline_refs/1; canonical SHA-256: 5072ded359a4eb3df3f619eb8aff57ba95142adfe39bfa6f1d77efe9c0e335dd

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/1/sha256; canonical SHA-256: f28266ac6e509744135b4364170f8c76a0ce8b1dee192f8c5122d47248f7a7a2

2c7b1df600523d1be2112a79ff1211ff1d895ebf665cae0d2296757a15f3a21a

#### Native item 3

Native pointer: /proofs/5/baseline_refs/2; canonical SHA-256: 37ba47c329179fd19333b2b289dea4fe55730d773c54ab5cab38b27dedb90d25

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/2/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/2/sha256; canonical SHA-256: 974745f0da8135c40e3bcfbb91eaf3f29f119668eabb638ea9b0f1346e81a1e3

eac332745d9f91823e5f0d2de62b28a5d0b4716d2f0550d74b50d8e79e507a4e

#### Native item 4

Native pointer: /proofs/5/baseline_refs/3; canonical SHA-256: 86791f2dfbfa99bfc6e2a1383f07c447985cefc9192520d8d30662078491448a

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/3/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/3/sha256; canonical SHA-256: 718c6838cb252f2d5922b43d179bef8a9efba36ab0efc9046d20d1bfd41ed180

5ce46166fd25890d03e773cf38365a22a19c04f01aafcf8479b19ada7f55c8ea

#### Native item 5

Native pointer: /proofs/5/baseline_refs/4; canonical SHA-256: 6c42cd0cb86f62c8bc6d520f2cf258f557f09e359cce7b4bf984ddfd27d8c750

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/4/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/4/sha256; canonical SHA-256: ad168456ead85facf42e02a466ef01049cdad342e64f1d69d3be3db1b01fb339

c9c5efe875ed0db15f91d1b664647bb7d19327a67c71e9440218db2fda86761b

#### Native item 6

Native pointer: /proofs/5/baseline_refs/5; canonical SHA-256: 5afbd4c0008f89edd6cd28ca975b9250b2d960794ba068c6b0bb43d34db75770

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/5/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/5/sha256; canonical SHA-256: 975059c019a7e26c6839cdfe14e9d51cf690283dc32dbd7fbb8326d0d9230925

c43b7b755a13621cc47f744cd90f5bc3667afba5f863de3d149c222ae96ce6a0

#### Native item 7

Native pointer: /proofs/5/baseline_refs/6; canonical SHA-256: 6e7ee25e2b93fa7e1f222c743f25b1f27e824fa014adb8320661cfaf02d45ade

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/6/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/6/sha256; canonical SHA-256: 8bacc9a41842ff4ef0dc2b589ccdc9ba6cff525f25003e8f7fc8ac15a037765c

2fe9ccdd589e88c927de04840c5b3eeabf10dde8df6157ab0c69f1bd43c56711

#### Native item 8

Native pointer: /proofs/5/baseline_refs/7; canonical SHA-256: bc13d3b14dc7c1375c0b989a33748102f9ff1b12a99944f6597375ecd9d0c0b8

#### Native field: pointer

Native pointer: /proofs/5/baseline_refs/7/pointer; canonical SHA-256: 827389749d3001e88ba1259848cb6989c8ddd64d1399694733d555d9bbe48702

/joint_analysis

#### Native field: sha256

Native pointer: /proofs/5/baseline_refs/7/sha256; canonical SHA-256: cc2dea05b5ec16460dd21dd259705a08b4007fb02ae5853905f8809c9dd3b671

3de58614b87ed5dbcd08ee27b37d38fe78db30a8572a49131a72a3f16dca71c3

#### Native field: body

Native pointer: /proofs/5/body; canonical SHA-256: 1b97747ec9f1de666122bcd70e35727e8ec58f3bcb31b1c31d9292ea20af42ac

Retain the exact native deterministic hidden-K model, feasible publicz0, monotone beta-LipschitzF, exact arbitrary-direction LMO with every legal fixed tie rule, and atom-hull query/output restriction. The SAME algorithm queries g=F(z0), then s=LMO(g), and outputs this atom s, with all initialization included, exact pathwise budget(1,1). For everyu inK, <F(u),s-u>=<g,s-u>+<F(u)-g,s-u><=beta||u-z0||||s-u||<=beta DK². Thus on the closed coarse predicate epsilon>=beta DK² this single output succeeds deterministically for everyinstance and every tie rule. Necessity of bothcoordinates is the exact accepted proof_necessary: on K=[-DK/2,DK/2]e1 and z0=0, constant fields+Me1 and-Me1 are monotone and beta-Lipschitz for arbitraryM. Without anyFcall, same public inputs/K/LMO map imply an identical deterministic transcript/output. The average of their weakgaps is M DK/2, so M>2epsilon/DK contradicts a uniform guarantee: BF>=1. Without anLMOcall, every permissible output lies in the initial hull{z0}, regardless ofFqueries. Field+Me1 then has weakgapM DK/2>epsilon, so BLMO>=1. Separate adversarial instances suffice because a single advertised cap must work for allinstances. No bounded-operator-norm assumption limitsM, and no free projection or evaluated hidden-domain output is allowed. Hence everyattainable pair has BF>=1,BLMO>=1, while the same(1,1) algorithm establishes everypair aboveit. The exact attainable region is therefore{BF>=1,BLMO>=1}; no splicing of scalar optimizers or a scalar ratio is involved. The extra simplex inequality in oldb_necessary is compatible and redundant here: R=beta DK²/epsilon<=1 gives RHS=1/(d+1)+8/R>=8 while1/(BLMO+1)<=1/2 forBLMO>=1. The threshold is sufficient, not proved sharp or the largest(1,1)region. Fine-accuracy operator/Pareto rates and fullc1 remain unclosed. This is publication of a previously proved consequence, not a new paper result or extension outside the original fullD.

#### Native field: proof_refs

Native pointer: /proofs/5/proof_refs; canonical SHA-256: 777c7a275cc530f7e4a6c82ae589c19ea90d35888d4f2fcbaa092c52bc84f7ae

#### Native item 1

Native pointer: /proofs/5/proof_refs/0; canonical SHA-256: 1e679974c1fef754077c247a39dd9da8829b8de5a0690ba4338aca529bd20e62

CV_S_LMO_MONOTONE_VI__proof_one_pair

#### Native item 2

Native pointer: /proofs/5/proof_refs/1; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: scope

Native pointer: /proofs/5/scope; canonical SHA-256: 5655922b0f56fe46e682143b87f7a18cb2a4f383ac66df7db815eef97832c31d

epsilon>=beta*D_K^2; D_K>0,beta>0,epsilon>0,d a positive integer; exact unchanged hidden-K, deterministic all-legal-oracles, atom-hull output contract.

#### Native field: source_refs

Native pointer: /proofs/5/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/5/title; canonical SHA-256: efc9bbc87975cfe00a0f1fdea5e1c28a52562f87de599b3df680058518e8eb1f

Exact joint-budget region from the retained simultaneous witness and necessary constraints

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 26d9f88090d559ba59135c66b334cff7bb61ccb7accaf85ef2e57af528014cb5

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 5487f016d61dda015d28de2da76637921785e39d60e8ac0c4face7943e4f93f7

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 949eed4c1e65c7c2e2b5a530a11dac7c9a29608897659e46a01accc5ff1755a6

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 3ea3b33a5577a5cfe8a90642344c86faefb3ed5ec409e42f0c1cf6076bfe223e

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 5a57fd93738ba6d90b52ccff6b7e26184b9ee89a81465c407796502ca01e6359

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: ebdcae01a6a5351ec121f06cc3270a4654bb1c62ab25d57b3115baf3c12bec06

d>=2 and 0<epsilon<beta D_K^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: e92a94bb27a4b8f02591e6708b3732cfc3abb5998f8510ed22d0405164cb7ed0

CV_S_LMO_MONOTONE_VI__main__b_spmp

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 78226fa232120d2fc2a43039c728e3443602230a4e5da2d652f28d8c97bc5d7b

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 9b62c2507b00fae6234cd8f17988947ca387a9e0c3857e910ca881b3f8bf4a6b

CV_S_LMO_MONOTONE_VI__proof_spmp

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 2a2af57b037adc47e148a22ff19ec07ea4dbb554897e6b6be04d25edd4015d28

No old mechanically compatible bounds exist. Source theorem and explicit finite-cap mapping are valid uniformly over the full domain. The one-pair construction dominates on the coarse region and the interval construction dominates for d=1 in the fine region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: ed61aa0d85122cf496e0c86563e464ad3cd53a1db86f9b2586f0565ab03ae4d8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: f958b3e37a24619f09ffb859c5b584a2d9eb8b30267b387fdf6e0b4f838e30ab

epsilon>=beta D_K^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 626e2b5c0f78d9dcff026456a13519721fb49c1de672c9d8456f2536d7c8d632

CV_S_LMO_MONOTONE_VI__main__b_one_pair

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 777c7a275cc530f7e4a6c82ae589c19ea90d35888d4f2fcbaa092c52bc84f7ae

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 1e679974c1fef754077c247a39dd9da8829b8de5a0690ba4338aca529bd20e62

CV_S_LMO_MONOTONE_VI__proof_one_pair

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/1; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 83d255db27daa2f5b48ba8956abd460c4fa06322b5486baae58ce9e1642e4348

Joint vector (1,1) attains the coordinatewise necessary minimum; its guard includes equality. No assertion outside the sufficient guard.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: f958b3e37a24619f09ffb859c5b584a2d9eb8b30267b387fdf6e0b4f838e30ab

epsilon>=beta D_K^2

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: d336125c63fb57b55651c4d931a02c5d2d063ebeeb8d82348837f87933213d01

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 6f9e822207c9020b25322302268d10c4541de4bd2f9b601a4ca45c7566c56e8c

d=1 and 0<epsilon<beta D_K^2

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: b09e4cbf9094e0eed8e5b6eb32c6dbdaf2f93ba6c9bfb32cb29fbfcbd02215c9

CV_S_LMO_MONOTONE_VI__main__b_interval

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: 0f17eb2f5e0aa02620e0ecc21927976437d2a5435c87a3294f53082150d080f0

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: dc1adde386af58edc3c114e31533a7b22ef6bd135af3959547bfccdbe58f54b4

CV_S_LMO_MONOTONE_VI__proof_interval

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 2c491f9f383e7d4acec108915c70d131d06edf8e490416d5df14a788ab56db5c

One relevant endpoint plus sign bisection uses exactly one LMO in the worst case. For R>1, k<=ceil(R)-1, so its F cap and LMO cap dominate the generic vector. On the coarse region (1,1) dominates it. No transfer to d>=2.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 090c620d3d1eda71f0fd9bef20773922d629249622a281c02f988750fe385f65

d=1 and D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: b42210f0f41f3a4e91e3ef12e69570d3bfbf28391c714d7bbd229c5231af64e7

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: d0194442f7f6f39a94d3dd45088b62f63be57f907d469d4dc3ef8c3335481696

CV_S_LMO_MONOTONE_VI__main__b_necessary

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: b987e10801cfe223c3cf8a638eba9bb7016852dae552f17b99dbe5a41aaba335

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 0d25befd7e84ff4551a87bfb383778b9105d01dd32851515d8e317deb802872c

Necessary constraints hold for every admissible algorithm; the simplex argument remains valid when its numerical right side makes it trivial. The two global one-call constraints remain nontrivial there. These are outer constraints on one budget region, not coordinatewise upper costs assembled from different algorithms.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 21e6d6e4676b943d46a6b52f41c9b70ffc470b40e5a976323ca634a2e2cfebc2

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 0478e145722e0ef13bda818355e8df3771ed9c1ac73a17250baea732c9af451f

epsilon=beta D_K^2 belongs to the exact one-pair branch; its strict complement uses the other guards.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 3fa9104fcb8d85e0f46d7bb033d30e363d9c7c0305b1c1a4e416a0efb9e2325d

Unbounded constant fields exclude zero F or zero LMO budgets even when epsilon is arbitrarily large; beta controls variation, not field magnitude.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 1476901d00ab98c986a8be211b2c291b6f6c4570b0d69c005669bf4bdc95de26

d=1 includes singleton K and endpoint solutions. The one-LMO bisection branch handles both with the same cap and no inaccessible projection.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 65b63c189ac4d95132c6e82a7343685a5ef24f83b30a415397ea44e62b7779d7

R=beta D_K^2/epsilon is the declared normalized inverse-accuracy coordinate. The scaling in target.normalized_variables preserves both query coordinates and all native parameter identities.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 5d5d20a90b9d5e620522bb3852f8799ea0dbe5526dcdc8e31458965aa5b4a8f5

The source theorem activates on all positive beta,D_K,epsilon and every finite d. Its sufficient step-size condition eta<=1/beta holds at equality.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 512e7ae2a75be7d2949fe0997be9eb637c03d5f8341ac5cf28145076092d25a8

The simplex lower constraint tends toward the support scale d as epsilon decreases for fixed d. This is lower-bound saturation, not a proved d-call upper or exact reconstruction theorem.

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/boundary_checks/6; canonical SHA-256: da1bb0f2cd6c8c40af84a8b835d843106fe304e5e27d45955a08630507e61a35

For d>=2, the crossover d approximately beta D_K^2/epsilon in the lower constraint is asymptotic; no exact phase transition or globally strongest rate is claimed.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 729f1515cf01f4d926bb915ef72b7633991578def7a4731af66c4ea0363eb6d5

For epsilon>=beta D_K^2, the attainable budget region is exactly {B_F>=1,B_LMO>=1}. Otherwise only inner/outer budget-region inclusions are proved; no scalar ratio is defined for this unweighted vector resource. For d=1 the LMO coordinate is exactly 1 with the stated operator allowance. For d>=2 the recorded operator allowance is O(1+R), LMO allowance O((1+R)^2), while necessity only gives B_F>=1 and B_LMO>=max(1,[1/(d+1)+8/R]^-1-1).

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 5235acb57236eca6ae066e665d46f802159ec4faa50f8ff075659d52bc40dde3

Every attainable budget satisfies B_F>=1, B_LMO>=1, and 1/(B_LMO+1)<=1/(d+1)+8epsilon/(beta D_K^2).

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: bce0c2f7bb01ea2bd4fd686a924f1e33586d486de0f6249d4fd8a3e21053602d

Outside the coarse region the full Pareto boundary and operator lower rate are unresolved. The interval branch fixes the LMO coordinate given its F cap but does not settle optimal F complexity. Other theorem leads remain scientifically unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 5d9179384b863e6ad652b6635c37fb25df3fbfb439931cf7a3789f96c5445def

Upward closure of the union of jointly attained vectors: (1,1) when epsilon>=beta D_K^2; (2+k,1), k=max(0,ceil(log2(beta D_K^2/epsilon)/2)), when d=1 and epsilon<beta D_K^2; (2T,2TQ), T=ceil(beta D_K^2/epsilon), Q=1+ceil(32beta D_K^2/epsilon)+ceil(2beta D_K^2/epsilon), when d>=2 and epsilon<beta D_K^2. Coordinates always come from one algorithm.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 4e314112c96707b819600cba559ed17c8c57ebf00323f01810b874a0f3f80269

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 5172baf484494724d4d63cc06431170ed01a4a919403b17deb2d174ec0f766e4

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: dd3621377d19fa625e90cd9f6d5ef701f4a56d3cfd842aac27a2797eff0fffbc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 50dbe559f043827cd1f8e795a8df6ecc6891d58f5ff3416bf40fd2a227b13b9a

Not adopted; original guard retained.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: e92a94bb27a4b8f02591e6708b3732cfc3abb5998f8510ed22d0405164cb7ed0

CV_S_LMO_MONOTONE_VI__main__b_spmp

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 721b9250ef6951ab010e823b6c6eb63b066f85358c89a1496ffd931cb32f129e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 8eb8040ac5c89dbdb170cd8e1af4d889fc143cf95466ac8a9fbba4245281c3e6

Retained upper is no sharper on its source-valid overlap than the same-algorithm exact minimum vector; outside its original guard it is not asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 4ed470022ffd43017f6219cb8dc6eeb41ab4539e849b5eeabf087bf45a1cf8d8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: 5655922b0f56fe46e682143b87f7a18cb2a4f383ac66df7db815eef97832c31d

epsilon>=beta*D_K^2; D_K>0,beta>0,epsilon>0,d a positive integer; exact unchanged hidden-K, deterministic all-legal-oracles, atom-hull output contract.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 626e2b5c0f78d9dcff026456a13519721fb49c1de672c9d8456f2536d7c8d632

CV_S_LMO_MONOTONE_VI__main__b_one_pair

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 721b9250ef6951ab010e823b6c6eb63b066f85358c89a1496ffd931cb32f129e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 9ec1c65ffbde7186fb882a3933da6f5466c8648cb6419f90507ee6ab84094d9e

Exact native same-quantity witness/necessary side, fully combined in CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: f958b3e37a24619f09ffb859c5b584a2d9eb8b30267b387fdf6e0b4f838e30ab

epsilon>=beta D_K^2

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: f737c880750178a47ea32f40842daee3de8be35356a655269d113409407216fc

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 50dbe559f043827cd1f8e795a8df6ecc6891d58f5ff3416bf40fd2a227b13b9a

Not adopted; original guard retained.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: b09e4cbf9094e0eed8e5b6eb32c6dbdaf2f93ba6c9bfb32cb29fbfcbd02215c9

CV_S_LMO_MONOTONE_VI__main__b_interval

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: 721b9250ef6951ab010e823b6c6eb63b066f85358c89a1496ffd931cb32f129e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 8eb8040ac5c89dbdb170cd8e1af4d889fc143cf95466ac8a9fbba4245281c3e6

Retained upper is no sharper on its source-valid overlap than the same-algorithm exact minimum vector; outside its original guard it is not asserted.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 090c620d3d1eda71f0fd9bef20773922d629249622a281c02f988750fe385f65

d=1 and D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: ce52f0d282e44db7035927f5a92aa577e21fdccd8ed33b9443fff71b536d554a

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 5655922b0f56fe46e682143b87f7a18cb2a4f383ac66df7db815eef97832c31d

epsilon>=beta*D_K^2; D_K>0,beta>0,epsilon>0,d a positive integer; exact unchanged hidden-K, deterministic all-legal-oracles, atom-hull output contract.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: d0194442f7f6f39a94d3dd45088b62f63be57f907d469d4dc3ef8c3335481696

CV_S_LMO_MONOTONE_VI__main__b_necessary

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: 721b9250ef6951ab010e823b6c6eb63b066f85358c89a1496ffd931cb32f129e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 9ec1c65ffbde7186fb882a3933da6f5466c8648cb6419f90507ee6ab84094d9e

Exact native same-quantity witness/necessary side, fully combined in CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 5b241f78538400f979600ab1e135661597d59d592c210b8778ec23ab22b0608c

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: fe220f953bda9f3c5d270f91a5788e121f48eef73a41f1957d6d189790caf3cd

Equality in the sufficient activation guard is included.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 59b82f1828abbfd200688c2fd78983a9690c004d24b46dcae55e95c24d48661d

Every cost coordinate comes from the SAME witness; no scalarization or coordinatewise combination.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: d0efc1ebe9c454cc572c72d3f85ebc15a53659af6859598abcfbefe8d6c50d85

Exact joint-region equality; scalar multiplicative ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: ba1a6c6c630da21cab40064a3316e07cfa0e5fa00445414901d988b6b6ced24d

Every admissible budget is componentwise >= (1, 1).

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: eceb39ba8d1bc97239eea3e601ee208874bd7a45e0609ab86cf98c1928b4e6fa

No Pareto gap on this sufficient region. No converse/largest-region or full-domain optimality claim.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: c2c6550ab2446b9706669b2c3bffec5fc9c52f916289a3eba9eab464891fb3e6

All componentwise budgets above (1, 1) achieved by one algorithm.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 15736cbf52cf73ab4f976fe7aa88b9ba85273f28dd8a9d51e52df140a7ce3eca

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 848fec3da88d43b878be69901d1dae11ccd03d24102e7b317cbb945c6dbf2951

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 61696c28ceb8a86f5a7a29bd74cb44b91ab5ec864eef51f80daa1dd97ad1ebfb

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 9532ab6dfeb875fd31a73ef56dd6823e962b3f357d0626a78ddd810a7614fdbc

coarse

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 00c7dc252b78f58a88f3bf000a927064b3ef1f9e918ccfe894bcadb91ea7679c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/1; canonical SHA-256: 1e679974c1fef754077c247a39dd9da8829b8de5a0690ba4338aca529bd20e62

CV_S_LMO_MONOTONE_VI__proof_one_pair

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/2; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: be0d5488b67cfd3ce2b15518e1e8172d64cd4483282fbbbd81d1a9e2855b5bec

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 65d76858bc8d7afd3ceb3583079fc0256923bb741f17207c1f9c1b75327e2044

Exact joint-region equality is now published by its own optimal comparison. Only this sufficient endpoint is closed; old full-domain c1 remains unclosed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 40f55e6940def2681c23ebbce9454e21827be84e4a90d6e87d7971355e250a76

epsilon>=beta D_K^2 and D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: dcc156d1e144367f729b3b83e8138861d73a0101b911327d5448dcbac2266eec

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 7934fc1fd76be5e11657ab125d352ff3e68687537a5e2ca970d2f5ba26a2cd1c

interval_fine

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 9562ef5dc8a3e6f460d4da46faa1e5bd273e018f9b97ef0a4f349cda37e507f2

One-LMO bisection upper and necessary joint constraints. Operator dependence is not proved optimal.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 6f9e822207c9020b25322302268d10c4541de4bd2f9b601a4ca45c7566c56e8c

d=1 and 0<epsilon<beta D_K^2

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 995b7eefde075583c285734d44152c4b0d27c5bc6105cdc7f93987d3a18dbb7d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: b7552a4b0e191a3155323db0920bf5eab6561299c1c79b6a83f4b5a9ad63db2a

higher_fine

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 7743da0783c661cda9f7be3a7d6a73948c13165c5ce14a6871ac2cd798ddac8e

Uniform full-LMO Mirror-Prox upper and simplex necessary LMO constraint. Fine-accuracy Pareto boundary remains unresolved.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: ebdcae01a6a5351ec121f06cc3270a4654bb1c62ab25d57b3115baf3c12bec06

d>=2 and 0<epsilon<beta D_K^2

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: a47444acb8da86541fef1712ae113cae5167d58516e53ecdd2e066af8671cddb

Positive epsilon and beta D_K^2 split uniquely into epsilon>=beta D_K^2 and its strict complement. In the complement the positive integer d is either 1 or >=2. Hence these cells are disjoint and cover exactly the frozen domain, without adding an endpoint epsilon=0.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 2075cca71b44d559ebe868fc885e2ba7abfea92b090cef2645bc1f1f526a7a73

Empty for accounting of the recorded inner/outer inclusions. No claim of a complete literature assessment: sharper bounds and Pareto boundaries in the two fine-accuracy cells remain unassessed.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 0d06bf0b22e66c754b36410d9d149180ba4eca053f7129f6ad0d042a209bd8f6

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 5d64bafba084aff2c0799ce96d243e093913362035c24c8d432e84647570cb22

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: cb98737ccb363a4234179ccd9853f63a845ad3257fc58e2ecb17a8f84e02692e

Theorem mapping establishes a main-rate upper, O(1+R) operator calls simultaneously with O((1+R)^2) LMO calls, not independent coordinate optimizations.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 0c4b271ffafef35154ea0214c1ea0515c3f28008675dea29efc0af99fb9b287b

spmp_full_lmo

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: ebdcae01a6a5351ec121f06cc3270a4654bb1c62ab25d57b3115baf3c12bec06

d>=2 and 0<epsilon<beta D_K^2

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 6948e813711fbd8e432a7cc42413e7488415f39498fa02e616a5aa97680a5349

Let R=beta D_K^2/epsilon, T=ceil(R), Q=1+ceil(32R)+ceil(2R). One deterministic algorithm attains (B_F,B_LMO)=(2T,2TQ).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 205aae2479194e1b8954cdaa79953fb0d5d6bfb3564c194cfd1f5259c9144955

No recorded upper budget.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: d9f7a6c7749ae54e620b134a492b2229e2eaf2ea1c3042215b619d7b1e3db88f

In the final union, this term is dominated on d=1 and on epsilon>=beta D_K^2 by other newly proved terms.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 5ccd79f2c17be9cace018bd2e461f8d25b827fb3e2d48d80c137853d485664ba

d=2 and epsilon=beta D_K^2/8 gives T=8,Q=273 and a finite joint cap (16,4368) where none was recorded.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: f8041852bdeb8221805f6643cc99b6d777bd91cb07316baf4367334421e69295

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: a007788cba5ef01a8b0dab0452eeb0132299eb3e33d1ec0040d8846dcc863516

The exact necessary inequality is proved. Its order-min(d,R) interpretation and d approximately R crossover are asymptotic and are not a matching lower for the quadratic upper.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 3bb6e15ebe12ea2ee6da990c0aa9634b7a51279689166bca9c856350a2959401

simplex_necessary

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 5235acb57236eca6ae066e665d46f802159ec4faa50f8ff075659d52bc40dde3

Every attainable budget satisfies B_F>=1, B_LMO>=1, and 1/(B_LMO+1)<=1/(d+1)+8epsilon/(beta D_K^2).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 2e35d70514041b7154d1f005c0c6d13655fc53239851f9d29283d9314fa3278b

No recorded necessary constraint.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: a59b5fe663796d30ae14356680d40c18fff96080d446efb4259f87a8bcc94a3e

The simplex component adds nothing beyond B_LMO>=1 where [1/(d+1)+8epsilon/(beta D_K^2)]^-1-1<=1; the global constraints remain active.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 81d26b554537cdc6c3f435db23d3b51cfcd76716804ff32ac87cb35a905c0cab

For epsilon=beta D_K^2/(8(d+1)), the simplex constraint forces B_LMO>=(d-1)/2; growing d proves a rate-dependent necessity beyond one call.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 1a2868e5fbb27d2ff727acde2017f62d488397b141b03aa7748cd7e951837116

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 0ebe9f7e9c24820221ccac2336c7b6879fb41c9911156cfce795613befbc2337

The sufficient threshold follows from the explicit inequality beta D_K^2<=epsilon. It is not claimed to be the largest exact one-pair region.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 8c111cf833a7c3e4efe00f3c57aa1b8ddd3f1b411ad21b8a76aff33bd2c38b28

one_pair_endpoint

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: f958b3e37a24619f09ffb859c5b584a2d9eb8b30267b387fdf6e0b4f838e30ab

epsilon>=beta D_K^2

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: a097e7883e68e5eb8b87f59d6db2e55c5641fc88e62b8b50418deb420aa77a8c

Attainable region exactly {B_F>=1,B_LMO>=1}.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: bf2173c60a585f0dca4603feec6ec922951a28fdfe4d9c1967b7eaa58de05370

No upper or lower recorded; the generic proposed vector is larger.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: f2a653738c4fea2ebaee164e72c2bc05d661448887673fbc800802b728bfc27d

0<epsilon<beta D_K^2

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: f958b3e37a24619f09ffb859c5b584a2d9eb8b30267b387fdf6e0b4f838e30ab

epsilon>=beta D_K^2

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: a987dda523c14fa237fc0f8f43545d9add6eba2e3110bbdf76ea0d5fb54f84fe

At epsilon=beta D_K^2 and every d>=1, one call to each oracle suffices and each is necessary.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 6a9cbb3052157310128c9abda94814e50099a1415ac8885a5de1554f8a6eced0

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: b72c59146fa8c8dd903a5fd949dc001b1018e9c0969ac0b5012c47376d70a139

The displayed conservative length criterion and ceilings prove the guard and cap. No claim about the best bisection constant or optimal F count is made.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 0a2b2fac8b5ff18522bc869c9f90a8b46007ec8f6a95ba957570f4be0611eb51

interval_one_lmo

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 6f9e822207c9020b25322302268d10c4541de4bd2f9b601a4ca45c7566c56e8c

d=1 and 0<epsilon<beta D_K^2

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 794fe9d7a3e75e7afd8f0588cd1c384bb0d06ae0ca384a1e6feb56b8d4057d28

If d=1, let k=max(0,ceil(log2(beta D_K^2/epsilon)/2)). One deterministic algorithm attains (B_F,B_LMO)=(2+k,1).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: afc9239e5f7c7de749d9fa2a1fa3ccb917050dce4511907b5b5d3d386cd0a663

No upper recorded; the generic proposed cap is (2T,2TQ).

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: bb0898c8d0bcc70bb68bb267efba5b23ab05d200374a1bac73d3c971fbec6731

All d>=2; also the coarse region where (1,1) is already smaller.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 090c620d3d1eda71f0fd9bef20773922d629249622a281c02f988750fe385f65

d=1 and D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: f483e943952a3a127633b44c087496358a429b936a5fb03b8b3b35067b0aaf11

d=1, epsilon=beta D_K^2/16 gives k=2 and cap (4,1), versus generic cap (32,17440).

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: cdd503544dfa72c5d24a969af37fad37088a052317f0d931f4a3b412318a299d

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 21d06314c3fd88d552ddb941241da9d6e4959b630a2d3fd82c4636c5250c395e

Presentation and inventory metadata are separated from the proof-backed new inclusions. The analysis_scope edit is semantic bookkeeping independent of validity of any new bound.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: fcdd6190343c888ccea6f4d6f5a5f625d1457b21baf2334f1792d2ec063b793b

first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 4aab97ccc7f15dc8d51dcf5170d0ab2114d83549a7946c5d9063f69286892b7b

Interpretation only; no additional scientific improvement beyond the four bound findings.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 038f56b414d44219c39939523cd27996dc0122824813d13376877553a6e08374

Explicit joint target, full-domain guarded accounting, and the same mathematical quantity.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: c479cfd55c7cfe127f737144ac7e1eaf5b845a9d2f0cfc3817caa0ff3a0c7a24

No existing joint analysis; fixed comparison identity and quantity formula.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 210571391a64730dde92777531ebfdad0b3497484064d5f5b59e835fd32f6a3a

The sole comparison ID, view, guarantee, resource vector and four tracked parameter IDs are preserved.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: 59ead389df534cb106c6305701ff6815c43a802b81a4d1480d8991da6b6a1abc

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 1b97747ec9f1de666122bcd70e35727e8ec58f3bcb31b1c31d9292ea20af42ac

Retain the exact native deterministic hidden-K model, feasible publicz0, monotone beta-LipschitzF, exact arbitrary-direction LMO with every legal fixed tie rule, and atom-hull query/output restriction. The SAME algorithm queries g=F(z0), then s=LMO(g), and outputs this atom s, with all initialization included, exact pathwise budget(1,1). For everyu inK, <F(u),s-u>=<g,s-u>+<F(u)-g,s-u><=beta||u-z0||||s-u||<=beta DK². Thus on the closed coarse predicate epsilon>=beta DK² this single output succeeds deterministically for everyinstance and every tie rule. Necessity of bothcoordinates is the exact accepted proof_necessary: on K=[-DK/2,DK/2]e1 and z0=0, constant fields+Me1 and-Me1 are monotone and beta-Lipschitz for arbitraryM. Without anyFcall, same public inputs/K/LMO map imply an identical deterministic transcript/output. The average of their weakgaps is M DK/2, so M>2epsilon/DK contradicts a uniform guarantee: BF>=1. Without anLMOcall, every permissible output lies in the initial hull{z0}, regardless ofFqueries. Field+Me1 then has weakgapM DK/2>epsilon, so BLMO>=1. Separate adversarial instances suffice because a single advertised cap must work for allinstances. No bounded-operator-norm assumption limitsM, and no free projection or evaluated hidden-domain output is allowed. Hence everyattainable pair has BF>=1,BLMO>=1, while the same(1,1) algorithm establishes everypair aboveit. The exact attainable region is therefore{BF>=1,BLMO>=1}; no splicing of scalar optimizers or a scalar ratio is involved. The extra simplex inequality in oldb_necessary is compatible and redundant here: R=beta DK²/epsilon<=1 gives RHS=1/(d+1)+8/R>=8 while1/(BLMO+1)<=1/2 forBLMO>=1. The threshold is sufficient, not proved sharp or the largest(1,1)region. Fine-accuracy operator/Pareto rates and fullc1 remain unclosed. This is publication of a previously proved consequence, not a new paper result or extension outside the original fullD.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: be0d5488b67cfd3ce2b15518e1e8172d64cd4483282fbbbd81d1a9e2855b5bec

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: 171cf9cc2a149d16ea6330f69a3f16aec83f1df4e67ffb1e180456082e46198a

CV_S_LMO_MONOTONE_VI_native_joint_closure_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: fdefc8f8a874bdbd4583d85fb847649698ca1fb1197f07a72bf0c34fe250920b

Native publication of an already-proved local closure, not a new numeric main rate or strict extension outside the old full domain.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: d76b71d162b60d20b833b7b3873125dec455770f2594c14a5f0941d5d9b6126b

A separate native optimal comparison publishes exact attainable region above (1, 1).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: 7d581c0075e512ebaf42ee4b04fe446bc247a399313f936fdc9d2bdb1b3201b7

Existing joint analysis already stated the exact local minimum vector but linked only broad joint_budget_unclosed c1.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 3eef3e1b9316e2cc107146014425a730f3382115503cec7048ed25555f3a40f8

Old fullc1 and all old upper/lower source guards; fine/complement/Pareto obligations remain pending.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: 5655922b0f56fe46e682143b87f7a18cb2a4f383ac66df7db815eef97832c31d

epsilon>=beta*D_K^2; D_K>0,beta>0,epsilon>0,d a positive integer; exact unchanged hidden-K, deterministic all-legal-oracles, atom-hull output contract.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: e94f7c096ff583ca5dddeb6473a1fd6310e6c0aa5b3b1fc7c0841326bc02fc2a

The same fully accounted algorithm attains (1, 1) and the complete necessary constraints match it.

#### Native item 7

Native pointer: /joint_analysis/impact/6; canonical SHA-256: d73bd462acf2788aac2b143601c3b00bce175c6766bfff5040c4ca14956cd6a8

#### Native field: argument

Native pointer: /joint_analysis/impact/6/argument; canonical SHA-256: 56d9e66e2b9e81d38efa09f7945f6b7dcc51e209c7f0ffd714ef558bc9d54771

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/6/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/6/comparison_ids; canonical SHA-256: 0b707b330b0c8139052a6014bc4353f43e9c5dac214bc4a6669d814a5498f5ca

#### Native item 1

Native pointer: /joint_analysis/impact/6/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/6/comparison_ids/1; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/6/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/6/finding_id; canonical SHA-256: 8fd33f9e40aedc24fe8d43256c0220565d9c19ccb60ae4b8a5b6273960e17db9

curated_feedback_CV_S_LMO_MONOTONE_VI_20261116_ab3e5d3796

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/6/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/6/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/6/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/6/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/6/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/6/validity_region; canonical SHA-256: 17e13e1a62bb386ff69db9ed790841488bb61f90dbe9bef62f46ac989002b75a

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract. The target is the upward-closed region of deterministic fixed worst-case vector budgets for guarantee g1, quantity CV_S_LMO_MONOTONE_VI__main__q_declared; no scalarization. All four parameters vary jointly.

#### Native field: witness

Native pointer: /joint_analysis/impact/6/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 9b87f056586def6f882f46bd3bad4165d3f314659eec5df2062c426a45cdbfdb

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 6d52999c2a65ac4b796be3706a82e1f973a9b3814bb89207af6ac4fc9bb8495a

Scientific screening of remaining metadata leads from search c5f5aebb928ca8f85f90d9bb2e99d23d5eb6b526207cdf033839fa97269c29de: arXiv 2001.09013v9 (inexact models), 1506.02444v3 (affine decomposition), and possible subclass-only results 2610.17127v1, 2510.03842v1, 2403.12859v2; no claims from their unread theorem text are adopted.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 5b4832e8662f4cb5c742e29d1760f7a95cd93f1b8e485b4693ca26abe7309431

Sharper fine-accuracy operator lower bounds, Pareto tradeoffs, and finite-dimensional saturation beyond the proved interval branch remain unassessed. The nonsmooth-optimization optimality discussion in 1507.01476 does not establish a matching lower bound for this smooth VI contract.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 09c2026f6312bcabdd63831bba82d2a4e7ac3c3ff96beae9b149b2a64c0cb68c

Independent reviewer must verify every new proof, the source-to-target mapping, guarded envelope and the exact analysis_scope metadata operation; no publication is authorized by this handoff.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: a69abc872d5a0056cac89040e1113e5a85522a1c8dc858605b23715569961843

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: b1750c0ee8335d379ab4f548432c8a21c3594efec82739a94479cc52bd2c8a86

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: e92a94bb27a4b8f02591e6708b3732cfc3abb5998f8510ed22d0405164cb7ed0

CV_S_LMO_MONOTONE_VI__main__b_spmp

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: b7ee79334a7e7f662c67a96fcb8777d6b10b706c8a9fc8d75e04b1ed98bce464

Use K as the sole nontrivial block, L=beta and Theta<=D_K^2/2. Explicit residual schedule and initialization give the stated simultaneous fixed caps, with all feasible points in the allowed hull and correctness for every legal LMO tie rule.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 78226fa232120d2fc2a43039c728e3443602230a4e5da2d652f28d8c97bc5d7b

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 9b62c2507b00fae6234cd8f17988947ca387a9e0c3857e910ca881b3f8bf4a6b

CV_S_LMO_MONOTONE_VI__proof_spmp

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 3ca907d276806dc6738fbf44e347e0a23d6d6034c57fd31b287bf3d79cc5b1f5

Monotone L-Lipschitz structured VI with M=0, singleton proximal block allowed, compact Euclidean LMO block and quadratic distance generator.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 98cfb199f367877f26a7306521cfa307e65df92a36acaef866e777575a6eeb3f

Actual fetched 1507.01476v1 hash: Theorem 3.1 pp.5-6, Proposition 3.1 p.7, full-LMO specialization p.8, Proposition 3.2 p.9; source_read [12900,26600), [43500,50000).

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: f9a238b627f815d7af576cc300c5db2b6e8bdfa80d14d4f596bdbe7d53250005

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 662dbed8e47cb1449ad07daef87dd27a3d8269def745b3fc363bf22815bebd39

CV_S_LMO_MONOTONE_VI__ref_1507_01476v1

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 1e496acb1c4e2bf6988a13ca0dea4f57c6a39117ad6f38bdb79743f765ee76ac

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 626e2b5c0f78d9dcff026456a13519721fb49c1de672c9d8456f2536d7c8d632

CV_S_LMO_MONOTONE_VI__main__b_one_pair

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: dbf64efc42561edb771688e9e4e9da989ce89ec6b5c131d4ad7d0a6b2a5964c6

Direct linear-optimality and Lipschitz inequality; no external theorem. Necessary one-call constraints give exact region equality.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 777c7a275cc530f7e4a6c82ae589c19ea90d35888d4f2fcbaa092c52bc84f7ae

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 1e679974c1fef754077c247a39dd9da8829b8de5a0690ba4338aca529bd20e62

CV_S_LMO_MONOTONE_VI__proof_one_pair

#### Native item 2

Native pointer: /joint_analysis/provenance/1/proof_refs/1; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 83dff5e5be410274d5667d0a807e407d51a5d5a11a8cbd90613f25ab69bac40d

Frozen /common_specification, /views, /quantities/0, /parameters, /resource_projections/0, with exact hashes in native proofs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: f958b3e37a24619f09ffb859c5b584a2d9eb8b30267b387fdf6e0b4f838e30ab

epsilon>=beta D_K^2

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: c3f9c758d687907e9815c94e325a8ef659546daf3401bde1d92e1b09cb80fa2b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: b09e4cbf9094e0eed8e5b6eb32c6dbdaf2f93ba6c9bfb32cb29fbfcbd02215c9

CV_S_LMO_MONOTONE_VI__main__b_interval

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 2c29438b2d5ff813de295a67fb8fea0e71e8bb813d8614aecf608bc3b0b148b2

A compact convex subset of R is an interval; native signed LMO supplies the relevant endpoint. Monotonicity and Lipschitz bounds certify the sign-bracket midpoint without free projections.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: 0f17eb2f5e0aa02620e0ecc21927976437d2a5435c87a3294f53082150d080f0

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: dc1adde386af58edc3c114e31533a7b22ef6bd135af3959547bfccdbe58f54b4

CV_S_LMO_MONOTONE_VI__proof_interval

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 33e356d93142e39ee4a7894abf4bbe496ebad933e9c7250e04d86d0884ceccb4

d=1 within D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: b29a6fc694a6636017a6fe7028c0f96e04a7b04193a9dbdd5af07b46bae9be9e

Frozen model, deterministic view and atom-hull output contract; exact hashes in native proof.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 33e356d93142e39ee4a7894abf4bbe496ebad933e9c7250e04d86d0884ceccb4

d=1 within D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 58583b6a8ffbbc99b1b23c3d4c49d7d9c3a0834b93b970e5cefdf5b8c2c8ae44

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: d0194442f7f6f39a94d3dd45088b62f63be57f907d469d4dc3ef8c3335481696

CV_S_LMO_MONOTONE_VI__main__b_necessary

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 2058b8afe69141f43357005680b2b5bc0fc86f65ac02f77c74e9f4690713287c

These subclasses are contained in the target. Both original query interfaces and cost coordinates, the deterministic all-instance guarantee and allowed output hull are preserved. Lower bounds for one legal tie rule suffice because correctness is required for every legal tie rule.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: ede9164e34fb157c4f3376d7721f7e47b8b07e22a23dc384c0fd8f471be26298

subclass_transfer

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: b987e10801cfe223c3cf8a638eba9bb7016852dae552f17b99dbe5a41aaba335

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: eadb9783a8c003c74bc8aae727ff4c784e008c4f0df7f067d0672ee8ea44a6b8

Admissible constant fields on a segment and F(x)=beta x on a centered regular d-simplex with legal fixed vertex-returning tie rule.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: ffcd6c68afe514d2caf841cda2392be3b1ff70c48bb8645c6b70cd78659c8608

Complete new subclass constructions from the frozen contract; exact premise hashes in native proof.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 91ccafe92815d4740450e11825951baac9fa064e6c7151fd5f8c2a7f1350459f

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 6d9829b16cb0cee96ede7d11c84943cab95c81fcb5fcb99d51bc0dd90a817995

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 0b707b330b0c8139052a6014bc4353f43e9c5dac214bc4a6669d814a5498f5ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: cbd44be67db7f845bf482f62c14c4c0803dddd417c1f08c2e386d604eab6d91f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: d42a524bc33100de73005fdbb572ccc28805e3fe6fb6bdae14fa5e9b1c1acd2e

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 7bb91e9a81231a99d9cb3e5ae9177254d5a6ce3e50f8cb8ad5b2465cec459514

All same-contract candidates are explicitly judged in the native comparison bound-use ledger. The newly published local closure follows from matching same-algorithm achievable/necessary regions in CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116. Retained broad/fine entries keep their original guards and unresolved status; no new theorem or old-source recertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: a2a7a918524a32b677366b8c58ef9acefe108787b1fcba4e92c829c2a0a17f47

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: b09e4cbf9094e0eed8e5b6eb32c6dbdaf2f93ba6c9bfb32cb29fbfcbd02215c9

CV_S_LMO_MONOTONE_VI__main__b_interval

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: d0194442f7f6f39a94d3dd45088b62f63be57f907d469d4dc3ef8c3335481696

CV_S_LMO_MONOTONE_VI__main__b_necessary

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 626e2b5c0f78d9dcff026456a13519721fb49c1de672c9d8456f2536d7c8d632

CV_S_LMO_MONOTONE_VI__main__b_one_pair

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: e92a94bb27a4b8f02591e6708b3732cfc3abb5998f8510ed22d0405164cb7ed0

CV_S_LMO_MONOTONE_VI__main__b_spmp

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: e47e715feebec146e3cb948bc48fa7aeacff5f62c311b4a98e5bef77e0bd7e12

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: 00c7dc252b78f58a88f3bf000a927064b3ef1f9e918ccfe894bcadb91ea7679c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: 1e679974c1fef754077c247a39dd9da8829b8de5a0690ba4338aca529bd20e62

CV_S_LMO_MONOTONE_VI__proof_one_pair

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/2; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 5e5a642c31a759159d900dd99eaff9fdd06fbb765dac5b1d43604be1d0245de1

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 7bb91e9a81231a99d9cb3e5ae9177254d5a6ce3e50f8cb8ad5b2465cec459514

All same-contract candidates are explicitly judged in the native comparison bound-use ledger. The newly published local closure follows from matching same-algorithm achievable/necessary regions in CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116. Retained broad/fine entries keep their original guards and unresolved status; no new theorem or old-source recertification is claimed.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: cf42a6fac5fef67bb250b7b361372618a2f6c5fbfc333c416092b50ce65e7524

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: d0194442f7f6f39a94d3dd45088b62f63be57f907d469d4dc3ef8c3335481696

CV_S_LMO_MONOTONE_VI__main__b_necessary

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 626e2b5c0f78d9dcff026456a13519721fb49c1de672c9d8456f2536d7c8d632

CV_S_LMO_MONOTONE_VI__main__b_one_pair

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: be0d5488b67cfd3ce2b15518e1e8172d64cd4483282fbbbd81d1a9e2855b5bec

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 00c7dc252b78f58a88f3bf000a927064b3ef1f9e918ccfe894bcadb91ea7679c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: 231590ddf149d0d721385363e578960f8f075a2998693fc1f01383c91cce0d73

CV_S_LMO_MONOTONE_VI__main__p_native_joint_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: 1e679974c1fef754077c247a39dd9da8829b8de5a0690ba4338aca529bd20e62

CV_S_LMO_MONOTONE_VI__proof_one_pair

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/2; canonical SHA-256: fab8ae528737d43c877de2bf1cb7b91751df94c759af27ccccba8d2925680204

CV_S_LMO_MONOTONE_VI__proof_necessary

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 5c2beb259d7414a3d022f8ba0cce7425863ea392d0ec4f48c5ba794d5a26f982

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 0b707b330b0c8139052a6014bc4353f43e9c5dac214bc4a6669d814a5498f5ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 6d52999c2a65ac4b796be3706a82e1f973a9b3814bb89207af6ac4fc9bb8495a

Scientific screening of remaining metadata leads from search c5f5aebb928ca8f85f90d9bb2e99d23d5eb6b526207cdf033839fa97269c29de: arXiv 2001.09013v9 (inexact models), 1506.02444v3 (affine decomposition), and possible subclass-only results 2610.17127v1, 2510.03842v1, 2403.12859v2; no claims from their unread theorem text are adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: c87d8149d0bc663a13ee41b706a64dfd00c5fc4c42515254eb0d2fb0f3e5c328

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 0b707b330b0c8139052a6014bc4353f43e9c5dac214bc4a6669d814a5498f5ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 5b4832e8662f4cb5c742e29d1760f7a95cd93f1b8e485b4693ca26abe7309431

Sharper fine-accuracy operator lower bounds, Pareto tradeoffs, and finite-dimensional saturation beyond the proved interval branch remain unassessed. The nonsmooth-optimization optimality discussion in 1507.01476 does not establish a matching lower bound for this smooth VI contract.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: e4f070820a7f2817c3c7a400ae2ff6ede2a4ba8df6affcd178706f0acfcdf801

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 4dfd630104b5d1d52ec3591271a6a996eac3f93a1e66858b83007027c2253ecc

This retained source/complement obligation is not resolved by local native publication.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 0b707b330b0c8139052a6014bc4353f43e9c5dac214bc4a6669d814a5498f5ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 09c2026f6312bcabdd63831bba82d2a4e7ac3c3ff96beae9b149b2a64c0cb68c

Independent reviewer must verify every new proof, the source-to-target mapping, guarded envelope and the exact analysis_scope metadata operation; no publication is authorized by this handoff.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: c631af0eb1bb6e07e6abb9dd685407543921a22e43bb8ae094fc588a7488afaf

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 0b707b330b0c8139052a6014bc4353f43e9c5dac214bc4a6669d814a5498f5ca

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 3a40322b90603de0cb3f2c8d70b8adf4c0f3641f9d3ed4e42f9280a5e4422a51

CV_S_LMO_MONOTONE_VI__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 2f4f8bc88ca4a001d981e2d0fd3a3f618ffaad2377e4ab4949f5250f613d2d31

CV_S_LMO_MONOTONE_VI__main__c2_coarse_pair

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 39db3a595dcbc9f7067df9b13e1c2baaeb45d73aeccd1bbaf635d557970911ed

curated-scope-limit-ab3e5d3796

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 4b4f2ad0831a30c5a26adcd1b7fc47bdc3ba3e130531736a165a1c888565b4e3

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 4304865fb9380b8e5026516ee258d6d2db6d0529b9b6477699845a832349fa13

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 15dd24a7978859271fb001237c07a1f13bc0e4f3f2e6e1c7067cb4ee24f6b0af

/views/0/guarantees/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: c755f1baff94528700d44695fa31dd26882367fcf3b2eea8d0550531fcc4028b

/regimes/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 17e13e1a62bb386ff69db9ed790841488bb61f90dbe9bef62f46ac989002b75a

D_K>0, beta>0, epsilon>0, d a positive integer, with the frozen hidden-domain/oracle/output contract. The target is the upward-closed region of deterministic fixed worst-case vector budgets for guarantee g1, quantity CV_S_LMO_MONOTONE_VI__main__q_declared; no scalarization. All four parameters vary jointly.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 874be8812c02cc07c4fc6ad1b54b78716fadc4ea3af7d92d29b0a6ae8eb120f8

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: afbe748c5ed967665a8aef5dae2117679557bf9fd50d26ce3170eed23ff692f8

CV_S_LMO_MONOTONE_VI_p_4230d60963

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 63ee80611ce3d64c64eb5f6b6983b3d1e45731504feb904649bf5ae3d64ee1bb

CV_S_LMO_MONOTONE_VI_p_f1b3e20dc2

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: e03acc75c639f7d9927e588fe143f107ccdd7beab72f21fea1dee8d6f8340440

CV_S_LMO_MONOTONE_VI_p_5af4186cb6

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: d787db69e9bb15dc1f284472845a0e4de4f3952e80a63379185b6eec00629ecc

CV_S_LMO_MONOTONE_VI_p_258cd1f3e7

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 6442decc3bcc7dfaaea234d1b68981f60e90634c46a64b8a3461a8da6d0bb897

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 50d5cdd84ab33c17b9ad4297d50667a1bcd3568cbc6da06cd955713a32e4a14f

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: 9c5f886f8123ad056892469c3234ed45e6f66715ce9f77537142b78acaaa0caa

R=beta D_K^2/epsilon (inverse normalized accuracy). Under x=(z-z0)/D_K and F'(x)=F(z0+D_K x)/(beta D_K), the domain has diameter at most 1, the operator is monotone and 1-Lipschitz, and the Minty gap is divided by beta D_K^2. Operator and LMO calls and the allowed atom hull are preserved by these known affine/scalar transformations, so normalized tolerance is 1/R. The four native joint variables remain tracked; R is a derived coordinate, not a new native alias.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 3ee532e8959bf1193150f7cc8a0f2f173f4eacab6bca3624a5117756cb1f9d13

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: afbe748c5ed967665a8aef5dae2117679557bf9fd50d26ce3170eed23ff692f8

CV_S_LMO_MONOTONE_VI_p_4230d60963

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 63ee80611ce3d64c64eb5f6b6983b3d1e45731504feb904649bf5ae3d64ee1bb

CV_S_LMO_MONOTONE_VI_p_f1b3e20dc2

#### Native item 3

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/2; canonical SHA-256: d787db69e9bb15dc1f284472845a0e4de4f3952e80a63379185b6eec00629ecc

CV_S_LMO_MONOTONE_VI_p_258cd1f3e7

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: d7425aeca0691c2fde605cfb1b386316dd4a1ee8705b05fc7fec4557dad77232

R

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 874be8812c02cc07c4fc6ad1b54b78716fadc4ea3af7d92d29b0a6ae8eb120f8

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: afbe748c5ed967665a8aef5dae2117679557bf9fd50d26ce3170eed23ff692f8

CV_S_LMO_MONOTONE_VI_p_4230d60963

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 63ee80611ce3d64c64eb5f6b6983b3d1e45731504feb904649bf5ae3d64ee1bb

CV_S_LMO_MONOTONE_VI_p_f1b3e20dc2

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: e03acc75c639f7d9927e588fe143f107ccdd7beab72f21fea1dee8d6f8340440

CV_S_LMO_MONOTONE_VI_p_5af4186cb6

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: d787db69e9bb15dc1f284472845a0e4de4f3952e80a63379185b6eec00629ecc

CV_S_LMO_MONOTONE_VI_p_258cd1f3e7

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Niao He; Zaid Harchaoui. Semi-proximal Mirror-Prox for Nonsmooth Composite Minimization. 1507.01476v1.

https://arxiv.org/pdf/1507.01476v1
