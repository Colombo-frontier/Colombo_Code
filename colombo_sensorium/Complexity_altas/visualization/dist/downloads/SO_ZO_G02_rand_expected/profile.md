# Global optimization in a Matérn RKHS with exact values

**Setting ID.** `SO_ZO_G02_rand_expected`

Single-objective optimization

Find an approximate global minimizer of the unknown objective over $X$. Evaluate the final recommendation by simple regret $f(\widehat{x})-\min_{u\in X}f(u)$; losses incurred during queries are not accumulated.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convexity not assumed; smoothness: Matern rkhs norm bound

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact value; public information: Public inputs explicitly declared; operation: Function value; feedback quality: Exact

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find an approximate global minimizer of the unknown objective over $X$. Evaluate the final recommendation by simple regret $f(\widehat{x})-\min_{u\in X}f(u)$; losses incurred during queries are not accumulated.

### Admissible model

$X\subset\mathbb{R}^d$ is a known compact domain with nonempty interior. The known kernel $k$ is a Matérn kernel with smoothness parameter $\nu>0$. Its amplitude and positive length scale are fixed and known.

The unknown objective belongs to the kernel's reproducing kernel Hilbert space $\mathcal{H}_k$ on $X$ and satisfies $\|f\|_{\mathcal{H}_k}\le B$ and $B>0$. Continuity and compactness ensure that a minimum is attained.

### Oracle interface

At any finite query point $x$ in $X$, the oracle returns the single exact scalar $f(x)$. The reply is uniquely determined and contains no gradient, subgradient or derivative-vector product.

The public inputs are $d$, $\nu$, $B$, $k$, $X$, $\varepsilon$, $T$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in X$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in X}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\nu$: Matérn kernel smoothness parameter **Domain:** $\nu>0$.

$B$: Radius of the RKHS norm ball **Domain:** $B>0$.

$\|f\|_{\mathcal{H}_k}\le B$

$k$: Fully known positive-semidefinite kernel and its scale parameters **Domain:** $k:X\times X\to\mathbb{R}$.

$\mathcal{H}_k$ is the reproducing kernel Hilbert space of kernel $k$ on $X$.

$X$: Fully known feasible or search domain **Domain:** $X\subset\mathbb{R}^d$; compact with nonempty interior.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$T$: Known query budget or argument of the risk curve **Domain:** $T\in\mathbb{N}_0$.

Use $N\le T$ in the fixed-budget specification and $\mathbb{E}[N]\le T$ in the expected-budget specification.

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $X$.

$I$: Complete problem instance **Domain:** $I\in\mathcal{I}$.

Includes the unknown objective and its admissible feedback distribution or environment law. Public parameters are fixed before the quantifiers.

$\mathcal{I}$: Admissible instance class determined by the eight specification fields in this profile **Domain:** Instances satisfying the public parameter bounds.

$\mathcal{A}$: Algorithm or strategy **Domain:** Measurable adaptive strategies allowed in this profile.

The algorithm is selected before the hidden instance.

$\ell$: Base loss or residual **Domain:** $\ell:\mathcal{I}\times\mathcal{X}_{\mathrm{out}}\to[0,+\infty]$.

The exact formula appears in this profile's performance-criterion section.

$\mathbb{E},\Pr$: Expectation and probability **Domain:** Evaluated over the algorithmic and feedback randomness specified by this profile's guarantee.

Fix the instance first; aggregate cost and error separately.

$\inf,\sup$: Infimum and supremum **Domain:** Evaluated only over the variable sets explicitly specified in the formula.

In the risk definition, the infimum over algorithms precedes the supremum over instances or centers.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product **Domain:** $\|x\|_2=\sqrt{\langle x,x\rangle}$.

$\langle x,y\rangle=x^\top y$

$B_p(c,R)$: Closed norm ball **Domain:** $p\in[1,\infty],\ R\ge0$.

$B_p(c,R)=\{x:\|x-c\|_p\le R\}$; $B_2$ denotes the Euclidean ball.

$N,T$: Actual call count and declared budget **Domain:** $N,T\in\mathbb{N}_0$.

A fixed budget bounds every execution path; the Markov specification uses an expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching orders, and upper bounds with hidden logarithms **Domain:** Within the joint parameter window specified for each complexity regime.

Dependence of hidden constants on fixed parameters is stated separately for each bound. Tilde notation may hide logarithmic factors only in the declared variables.

$c,C,c_\alpha,C_\alpha$: Positive constant in a proof or asymptotic bound **Domain:** $0<c,C,c_\alpha,C_\alpha<\infty$.

Unsubscripted constants have the dependencies stated in the bound; constants subscripted by $\alpha$ may depend only on the fixed smoothness order.

$\log,\log_+,e$: Natural logarithm, truncated logarithm, and Euler's number **Domain:** $z>0$.

$\log_+(z)=\max\{0,\log z\}$; $e=\exp(1)$, and $\log_2$ denotes the base-two logarithm.

$r_T$: Error scale of the final recommendation under the budget **Domain:** $T\in\mathbb{N}_0$.

Under an expectation guarantee, the quantity is $\inf_{\mathcal{A}:N\le T}\sup_I\mathbb{E}[f(\widehat{x})-f_*]$. Under a fixed-success-probability guarantee, it is the $2/3$ quantile threshold with the same quantifier order.

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in X}f(x)$.

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=X$ and $\mathcal{X}=X$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime G02.R1

**Region.** Fix $d,\nu>0,B>0$, the complete Matérn kernel and compact domain $X$. The set $X$ has nonempty interior; set $\varepsilon\downarrow0$.

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_{d,\nu}((B/\varepsilon)^{d/\nu})
$$

**Upper bound.** B1

$$
O_{d,\nu}((B/\varepsilon)^{d/\nu})
$$

**Gap or comparison.** $O_{d,\nu}(1)$

### R2 - Sufficient zero-query accuracy region

**Region.** ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

**Quantity.** Q1

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Gap or comparison.** Not applicable: exact zero call cost; no division by zero.

## 4. Bounds and supporting evidence

### B1 - Quasi-uniform sampling and kernel interpolation

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
r_T=O(T^{-\nu/d})
$$

**Sources.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf)

**Conditions.** Fix $d,\nu,\theta,B,X$; quasi-uniform sampling and interpolation achieve the upper bound.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf) pdf pages: 9; printed pages: 2887; theorem: Theorem 1, p. 2887

### B2 - Packing of local RKHS wells

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
r_T=\Omega(T^{-\nu/d})
$$

**Sources.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf)

**Conditions.** Fix the dimension, complete Matérn kernel and $B>0$, with $T\to\infty$. The lower bound ranges over the same RKHS ball and covers randomized adaptive queries and unqueried recommendations.

**Oracle correspondence.** Exact scalar function values; every location required by a finite difference must belong to this setting's query domain.

**Guarantee conversion.** The source takes the worst objective for the expected loss of each randomized strategy. Both fixed sample points and the final recommendation enter the indistinguishable-well argument.

**Output rule.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf) pdf pages: 9; printed pages: 2887; theorem: Theorem 1 and Appendix A.2

### B3 - Fixed feasible recommendation with no oracle queries

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
C^\star_{\mathrm{main},\pi}(\varepsilon;\theta)\le 0
$$

**Sources.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf)

**Conditions.** ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

**Oracle correspondence.** No objective observations are obtained. The exact scalar oracle is unchanged.

**Guarantee conversion.** Deterministic regret≤2 B M_k implies expected regret≤ε for every fixed admissible instance.

**Output rule.** A fixed x0∈X, chosen using public X, is a permitted unqueried recommendation.

**Resource conversion.** N=0 on every execution path; native call cost is nonnegative.

**Local argument.** SO_ZO_G02_rand_expected__main__p_zero_query

**Source location.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf) character range: 17000; 19000; pdf pages: 7; 8; printed pages: 2885; 2886; section: 3.1 Reproducing-Kernel Hilbert Spaces

RKHS identity is the external premise; the zero-query statement is the explicit analyst derivation SO_ZO_G02_rand_expected__main__p_zero_query. Native norm, output, expected guarantee and nonnegative cost premises are frozen baseline records listed in that proof.

### B4 - Nonnegativity of the native minimax call cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
C^\star_{\mathrm{main},\pi}(\varepsilon;\theta)\ge 0
$$

**Conditions.** ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

**Oracle correspondence.** No objective observations are obtained. The exact scalar oracle is unchanged.

**Guarantee conversion.** Deterministic regret≤2 B M_k implies expected regret≤ε for every fixed admissible instance.

**Output rule.** A fixed x0∈X, chosen using public X, is a permitted unqueried recommendation.

**Resource conversion.** N=0 on every execution path; native call cost is nonnegative.

**Local argument.** SO_ZO_G02_rand_expected__main__p_zero_query

**Source location.** [1](https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf) character range: 17000; 19000; pdf pages: 7; 8; printed pages: 2885; 2886; section: 3.1 Reproducing-Kernel Hilbert Spaces

RKHS identity is the external premise; the zero-query statement is the explicit analyst derivation SO_ZO_G02_rand_expected__main__p_zero_query. Native norm, output, expected guarantee and nonnegative cost premises are frozen baseline records listed in that proof.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: cbd92f347ed55ebac836135340f220208cd9cd19bf0d0680a248d01b860e5b17

### Native proof: SO_ZO_G02_rand_expected__main__p_zero_query

Native pointer: /proofs/0; canonical SHA-256: 4b85df0af3791b7ec80f2b665e7375771ea80622b0f4a5252c90d0e06453e558

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: c7d16c28b7d9bb37763b08aa010368b892e9316963e23bb81e6636e3007f3379

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: 4ae49661a54a4aafe02ef9e9af16df79a9f189b408e44ce5f5b4df5bfdab16fc

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: 68013277173c79d4c1ee9741038dd2c09288dfa58c725a525a1e2000c9c05fd8

581466a38e9818524dc18b5f43add4fa6edbaa026559116ace1ccd0ecee23195

#### Native item 2

Native pointer: /proofs/0/baseline_refs/1; canonical SHA-256: ff803957fcf91fd9c8d52c8426bee9ff0c0bec3c83d5ae88fe1e971e85742480

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/1/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/1/sha256; canonical SHA-256: f56a36b82682699509506c0e0b7b41ced379fd83db604774676eb66571e0c6ee

ac3ec3302a84ec5782e031bd58d142e47763e55c7de0b252bb7fc0ea7592fef1

#### Native item 3

Native pointer: /proofs/0/baseline_refs/2; canonical SHA-256: 4e9b5960a8111354811ea47654a6e412942ed5826f747193f6f72b004464de56

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/2/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/2/sha256; canonical SHA-256: 6dfbb90a94d1c26ac8e7f6f31fc8a4ec47ca6b9e77bd4c7fbf0ae036fac23b24

9aa08a801dfa11be6333ee008faa85742b748093c67fbbc76b82ca63e1bb20d6

#### Native item 4

Native pointer: /proofs/0/baseline_refs/3; canonical SHA-256: 6bfd3a90211b384c8aaa3b69e3cd5a289481b3be8d04b23372f03327303378ac

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/3/sha256; canonical SHA-256: d171eac79b91131da47b04b37beabed4b96e875073e9470a6b67b2c96f2cbe65

e0d2f8e493b12bf04335a719504f2e78919711caada86956e2c0949da9b2df1f

#### Native item 5

Native pointer: /proofs/0/baseline_refs/4; canonical SHA-256: bff6204c617b42a1ceef8e9407a766a5f6bfe59e18c27e9a7d35375ef612eea2

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/4/sha256; canonical SHA-256: bc3b1764ee67c8aeb957a97ed94d046b021645cae82e9a24947afefaa4d59755

70e53c24fab31d7905bb6b818f798b5d521c22e826de1595ec3bb04d9c572c5a

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: source_hashes

Native pointer: /proofs/0/source_hashes; canonical SHA-256: 8f85e07e5d60a8795319f3baa370609cd7a518e0b55a09f3f310bf0e404c4600

#### Native item 1

Native pointer: /proofs/0/source_hashes/0; canonical SHA-256: 53d77ee69eed455106e8a6ebf1ae2b0a23d88514ca45feb5c03be66a88014f99

72e5b25c2e3a79a2282e2a5672be6152fb9120853cc978cef6548124fe0dbf7a

#### Native field: source_locator

Native pointer: /proofs/0/source_locator; canonical SHA-256: 14b34d6cad0aeaa4ec681990f72b9ee702cf52f26838197d8d7730e0457f5127

Bull, JMLR 12 (2011), §3.1, printed pp.2885–2886, archived characters 17000–19000: RKHS inner product and reproducing identity. Bull does not state this zero-query conclusion.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 4e42602dd74e81704f3b36561a6e4833c16266849ab9e96c63545645a4bb5863

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: ea6f7268b67961bb6301dcd6da052cbcb8ff5229f70d4bbd4d74651405384e93

SO_SRC_52c81802676000d4

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 266407e97621a82ead3d3dcd74e7b648511abec09c9de87851cb823805be2105

The native minimax expected-simple-regret call complexity equals zero whenever ε≥2 B M_k, M_k=sup_{x∈X}sqrt(k(x,x)).

#### Native field: steps

Native pointer: /proofs/0/steps; canonical SHA-256: 6746779d21b2507a3492b3c812beca933b113b9d79e42cbb1b8cba9f1f96c5df

#### Native item 1

Native pointer: /proofs/0/steps/0; canonical SHA-256: 1ee5c25f3e7ad6abecbccac0d0c64db576b503fd2142f6730eb31e219e435b98

The native Matérn kernel is continuous with positive fixed amplitude. Its diagonal on nonempty compact X therefore has 0<M_k<∞. No normalization k(x,x)=1 is assumed.

#### Native item 2

Native pointer: /proofs/0/steps/1; canonical SHA-256: 18862a36bd94acf618ba4f9a277ce068a3ba65d9c1a22240f30845a6ec554846

Choose one x0∈X using only the known domain, before any objective observations. Output x0 and make N=0 oracle calls. The output contract expressly permits unqueried recommendations.

#### Native item 3

Native pointer: /proofs/0/steps/2; canonical SHA-256: 6ae9177536c6f996cafa42579aa6637c4b67c82237dda1eb3cfa14048ac971f3

Write k_x=k(·,x). The reproducing identity gives f(x)=⟨f,k_x⟩ and ||k_x||²=k(x,x). Nonnegativity of ||f-t k_x||² for real t yields |f(x)|²≤||f||² k(x,x), including the zero-diagonal case.

#### Native item 4

Native pointer: /proofs/0/steps/3; canonical SHA-256: bb1bbf8760edb8d793cc04a7c11ff70abb7d6f428d3b88cff3d46a048f491b52

For every admissible f, ||f||≤B implies |f(x)|≤B M_k. Thus f(x0)-min_X f≤|f(x0)|+sup_X|f|≤2 B M_k.

#### Native item 5

Native pointer: /proofs/0/steps/4; canonical SHA-256: 5c50d437b84b7bd5c950d58f5daaed20b53c0f34b39c8f2ac4b75e5a959315c8

This deterministic pointwise guarantee implies the native expected-loss guarantee with the instance fixed before averaging, for ε≥2 B M_k including equality. No randomness, observation, initialization or hidden oracle is used, so every execution path has zero cost.

#### Native item 6

Native pointer: /proofs/0/steps/5; canonical SHA-256: 8095c3398c88f9ec2d42753dd7927d12a36176cb41b07402c87bb6af22379172

The frozen quantity is an infimum over nonnegative resource costs. It is therefore ≥0. The exhibited zero-query algorithm proves it ≤0 on the endpoint region, hence C*=0 there.

#### Native item 7

Native pointer: /proofs/0/steps/6; canonical SHA-256: 7f45e97a832986e8a9f9cc0fe7b17c6950d908262cc5b5055d53cd02a457b713

The threshold is an exact sufficient inequality only. No necessity, optimal zero-query transition, finite reconstruction property, or extension of the small-ε asymptotic theorem is asserted.

#### Native field: supports

Native pointer: /proofs/0/supports; canonical SHA-256: 678e7d12c9a2e0fac58ef02904588332df2508e5e83e9d5913601566f4d45f00

#### Native item 1

Native pointer: /proofs/0/supports/0; canonical SHA-256: 76bc91a05a40c466b71f10b1dafe044f244b69e98929f0c932d02c590facda13

SO_ZO_G02_rand_expected__main__b3

#### Native item 2

Native pointer: /proofs/0/supports/1; canonical SHA-256: 238bd6ea110a92d723cead402597072edf0a1fcd31676f0c839e2b18fb70df67

SO_ZO_G02_rand_expected__main__b4

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: c3b2b6613a30248bb1ff8206b0cd081d7dca260bc2fdf21594b0f54d021d3064

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 29910fbf96e14d7acfd6ba87b24362c51971f0eec4c251d6bfbdaa62d2c0e8cc

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 7cbac01d1e570bbc68300cd5e6c90866acc62222ea46a47fa5219ef6f0a43b5b

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: d4836906c2f630666c663e338a4094d19dba387a7e2949b81a2de09cebf6d481

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: ca9376bcbe96da6149beac493e74c2dee951d62a67a191108cf4d3e5f4411dbe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 3f26ea92340f6375fbe6b0c830f673a47c27a18f3f4202fba8f0814091f9f9ca

Original c1 small-ε asymptotic region.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 80ca81eeab68164c13c6d8454e54a404ccf3cfce156b450a2a3fa081e0e5ae1b

SO_ZO_G02_rand_expected__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 00f825bbbd0ac5945108f29b0e3102aafd6bf9c824f526fc8ffed7b81245dac9

Conditionally retain the original deterministic quasi-uniform interpolation upper bound; deterministic algorithms are allowed by main/g1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: fabe5aa082b93b86d4e9eaef3ad3e99e8425b997a10ef31cbe268b63e7e5c0dc

For each fixed d≥1, ν>0, B>0, complete Matérn kernel k with fixed positive amplitude and length scale, and compact X with nonempty interior: ε↓0, equivalently T→∞ in the dual regret formulation.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: fa0e7da50eba29ee85bf3dd9fb9cb0abab7a1990c218330bf08d7c51c91a12fe

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 3f26ea92340f6375fbe6b0c830f673a47c27a18f3f4202fba8f0814091f9f9ca

Original c1 small-ε asymptotic region.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 49bce727e3a9650bddc37fc01e5bdbfc40e154d42edea44621920959b551232b

SO_ZO_G02_rand_expected__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 51c98cb98d73c9655163881dda4942564118321f8668756643486e04a403bfd5

Conditionally retain the randomized-adaptive lower bound, including unqueried recommendations.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: fabe5aa082b93b86d4e9eaef3ad3e99e8425b997a10ef31cbe268b63e7e5c0dc

For each fixed d≥1, ν>0, B>0, complete Matérn kernel k with fixed positive amplitude and length scale, and compact X with nonempty interior: ε↓0, equivalently T→∞ in the dual regret formulation.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: ca3c72ba7c45e508d77bc0b69a901c667608952e4c219be3e6eb995bc95683c5

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: e25141c904bfc927270d63d1566d0b1aa159cc566f8868fa4695a859b8374ccd

Empty for the ε↓0 asymptotic cone.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 76bc91a05a40c466b71f10b1dafe044f244b69e98929f0c932d02c590facda13

SO_ZO_G02_rand_expected__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 164a996b11fd78e98da744599aff377b94cd862832e9a2f3253d2fa406ff02b2

At fixed B,k,X the endpoint has a strictly positive accuracy threshold; do not extrapolate it to ε↓0.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/bound_uses/3; canonical SHA-256: f9e25bc7acbdc90c74a29aa52fb76eeeeb8806db2eaba9f1415687d8df592796

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/adopted_region; canonical SHA-256: 76d342120b04b4d2378e20a9f4f59f88c0683ef04a98db4c2a22e2e50a7a16de

None in c1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/bound_id; canonical SHA-256: 238bd6ea110a92d723cead402597072edf0a1fcd31676f0c839e2b18fb70df67

SO_ZO_G02_rand_expected__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/reason; canonical SHA-256: 5112be9610eec48ba1cecc8d7933389077054d71f084bc7c77100214e93205cd

Its endpoint validity/adoption guard does not enter c1; no nonnegative-cost row is imported into the original asymptotic envelope.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/3/validity_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 4c99ac129dc0ea14540a20ed08b5b615c4d19a5f4737e8c0c609d4e0911b7537

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 5601d9b901acf605b4ea051ff147461f8c6eece02ff0991f75b524f19af5ecf3

No substitution T=0 into a T→∞ theorem.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 6ca2b47ebf1f524a329dc8535c2268f5b65a59a81e2c6b88eeb41bde2487863c

No finite-dimensional exact-reconstruction branch is inferred for this infinite-dimensional Matérn class.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 024ff7eaea2caa18862917e37cfdc15c3bc1e64cea242ad4612447f91605c678

The retained theorem covers fixed d=1 as well as each fixed d>1; no dimension-uniform constants are asserted.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 153b10862c00c3e7b2f396bb4ab5a85a390fd0ff95ab0e8c9fcc3cdec0e74754

ε=0 lies outside the native accuracy domain.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 15b3fae1ada89957874eecebeedf0f6b151e9f667e0258b70e087d5ebb8fc362

No relation ε=c g(d) is imposed, so this is a fixed-structure family, not a relation slice.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 95975fbeb49fca433f95136103497d1e6634695b8cad352c5daf3092bdb7c045

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 356ca51c51cdb952034764f73ca9afca9282d1cdb75c9dd99c98797579b9fce1

SO_ZO_G02_rand_expected_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: 5c7c087d7dfed8f8e4c4f2d3f18db7fcbf75e892f80dad69e6c3b5fb76b2c91c

SO_ZO_G02_rand_expected_p_45a98071d4

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/2; canonical SHA-256: 23bd96cfb31242b8e6f847198896dce37c41252ffbffad39f3fd7f47dac875bf

SO_ZO_G02_rand_expected_p_d920326707

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/3; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/4; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 95975fbeb49fca433f95136103497d1e6634695b8cad352c5daf3092bdb7c045

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 356ca51c51cdb952034764f73ca9afca9282d1cdb75c9dd99c98797579b9fce1

SO_ZO_G02_rand_expected_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: 5c7c087d7dfed8f8e4c4f2d3f18db7fcbf75e892f80dad69e6c3b5fb76b2c91c

SO_ZO_G02_rand_expected_p_45a98071d4

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/2; canonical SHA-256: 23bd96cfb31242b8e6f847198896dce37c41252ffbffad39f3fd7f47dac875bf

SO_ZO_G02_rand_expected_p_d920326707

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/3; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/4; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 51b61b87b28380e0231588e61d444b9b8f282bd09026f9693cb6c2657848ac84

Θ(1) multiplicative rate gap on the documented asymptotic domain. Native O_{d,ν}(1) shorthand is read together with the full fixed-kernel/domain/norm guard; it is not a uniform theorem over structural inputs.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: e99fed06473ebeb6fce7540d745f2b1f60ebc90c4bdebe2552b1ddda2745ade9

Retained Ω((B/ε)^(d/ν)) under the same fixed-structure small-ε guard; equivalently r_T=Ω(T^(-ν/d)).

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: e9cf4ed706a935832cc1ea05e3917755f65ff979910279923c8aaedc3e2023f2

No asymptotic rate gap in the retained domain; exact constants, dimension-uniform rates and intermediate accuracy are unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: beab05139434940e36ad3dcc20e5d9efb95ed240ef508cb738d6ce0869955592

Retained O((B/ε)^(d/ν)) as ε↓0 for each fixed d,ν,B,k,X; equivalently r_T=O(T^(-ν/d)) as T→∞.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 9a7f251b35d101418aa8b16471371e2292bd34e22dcc17fe7456723aa208e8f8

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 3d5e7c1ff8f25d04b32ff0cf43327a2d2e41738e821ab5dd82a79a9200512224

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 3dd22c7731a6a136aefc0d3b9ea900aa973e248f9959b39f9f829c9a86fcc514

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: a5b05e89dad1d1da8bf655b1b19410ebbc03353ab19cf5cf01bc85c292ff0897

None in c2.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 80ca81eeab68164c13c6d8454e54a404ccf3cfce156b450a2a3fa081e0e5ae1b

SO_ZO_G02_rand_expected__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: dd94c6e20026fcf2b8455f0834937bddfee9cde54faaca6ac75e47acb41f90dc

The old upper bound has a small-ε asymptotic guard and supplies no finite-accuracy endpoint statement.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: fabe5aa082b93b86d4e9eaef3ad3e99e8425b997a10ef31cbe268b63e7e5c0dc

For each fixed d≥1, ν>0, B>0, complete Matérn kernel k with fixed positive amplitude and length scale, and compact X with nonempty interior: ε↓0, equivalently T→∞ in the dual regret formulation.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 7255554a2631ee964491d69dcb6fd6ee867f685c42084594b01f2913821a0019

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: a5b05e89dad1d1da8bf655b1b19410ebbc03353ab19cf5cf01bc85c292ff0897

None in c2.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 49bce727e3a9650bddc37fc01e5bdbfc40e154d42edea44621920959b551232b

SO_ZO_G02_rand_expected__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: 714673a2cdd63e6c9e89c7fcf5f63de547ec5c881e9f5fbc7ac84ff456c503db

The old positive asymptotic lower expression cannot be evaluated at coarse ε as a finite-domain lower bound.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: fabe5aa082b93b86d4e9eaef3ad3e99e8425b997a10ef31cbe268b63e7e5c0dc

For each fixed d≥1, ν>0, B>0, complete Matérn kernel k with fixed positive amplitude and length scale, and compact X with nonempty interior: ε↓0, equivalently T→∞ in the dual regret formulation.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 904a9c3625f99caf205a2c27123aaa24c66416c33caa5f379d2473df21322fba

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 76bc91a05a40c466b71f10b1dafe044f244b69e98929f0c932d02c590facda13

SO_ZO_G02_rand_expected__main__b3

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 5ca556a777bcb4a251df7383afa81418dc5fe953834b6389cf9d60a722d462d4

A fixed feasible unqueried recommendation has loss≤2 B M_k on every objective.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/bound_uses/3; canonical SHA-256: 460f814059075bb61aa9e1bab6e23a09ad60a8d548e86239c7ff77fb348417c9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/adopted_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/bound_id; canonical SHA-256: 238bd6ea110a92d723cead402597072edf0a1fcd31676f0c839e2b18fb70df67

SO_ZO_G02_rand_expected__main__b4

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/mapping_proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/reason; canonical SHA-256: 524c176ad10064a7ad492b3cff5bc118d00d2c9a05419dc67a84ee600155c64d

The native resource cost is nonnegative; paired with b3 this proves exact equality, not a separate main-rate lower improvement.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/3/validity_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 0449d32b898bff353bd9f88976d21a9dbfb8acc10cf73229eea36c8fe987120e

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 78eceaba5f8f06b11d15b6cd289850e560f2d5b439971c0b5b3675b92a662ce6

Equality ε=2 B M_k is included by the native ≤ε guarantee.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 88fdfce163023559a21db74ea9e148485ad992df4ad5ac0c212318783c7e4c51

T=0 is feasible and every larger cap remains feasible.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 555ea45e9caba706bad01904e1c605a9ac01ced3693528b8044d5b1aaf815bad

The kernel amplitude is retained in M_k; k(x,x)=1 is not silently assumed.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 959c45597cc74953f76fd71768927e18ad07968fa20445f6b68dd5fa69118fba

No necessity of ε≥2 B M_k is claimed.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/boundary_checks/4; canonical SHA-256: 20559800178503c5c1c36519e7a1262798f78522d3f68b94728e6312d6c0df86

Below this sufficient threshold the zero-query proof gives no exclusion or positive lower bound.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 95975fbeb49fca433f95136103497d1e6634695b8cad352c5daf3092bdb7c045

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: 356ca51c51cdb952034764f73ca9afca9282d1cdb75c9dd99c98797579b9fce1

SO_ZO_G02_rand_expected_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/1; canonical SHA-256: 5c7c087d7dfed8f8e4c4f2d3f18db7fcbf75e892f80dad69e6c3b5fb76b2c91c

SO_ZO_G02_rand_expected_p_45a98071d4

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/2; canonical SHA-256: 23bd96cfb31242b8e6f847198896dce37c41252ffbffad39f3fd7f47dac875bf

SO_ZO_G02_rand_expected_p_d920326707

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/3; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/4; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 701443cb68ff9aed6bb20443004e87fd14130ab043f4a2a5275f498319aecd22

Exact cost 0; multiplicative ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 58b6e52387b3a94086da9cbda02d22146cc9448809f6ead899d21407a3f76a59

0 calls, by nonnegative cost.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 43db5f2dd39d3456a1b01177bf4cbe0a4827533f75ef252a9a7bc77203cb23e4

None on this sufficient zero-query region. Its maximal extension and the minimum necessary accuracy for zero queries are unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 8511cda547132aa313499aaf6dcb51543046181bc12753a4bc1150478d24614f

0 calls whenever ε≥2 B M_k.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: d8d5907a72615fe3b23a04a1f86684a3eb78b88165aa999cd1cb029350ff18be

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 4d1ab163985277c680a93aa811c478f393937fbb011ad76c945d61fb40d425d5

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: a7636c83d98ab5bd009348823c0c90505fba3c60c0064128c7c12be2e2353e2f

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 7b37ba204afb50d661659f0ceb5c279a046e764ecf46c32b9c03adeaf841dc41

fine_accuracy

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: d9a541dfe000a63d98a4f743bcbff7bd571b42f85692e178b625b6c8287a841f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 2987695c487267ecfe65899af690fd2711cef1ebdde730733a0f54efa3b67b45

Retained small-accuracy asymptotic bracket only; ε_0 is not numerically known and is not a sharp transition. Feasibility depends on whether T reaches the bracketed cost. Existing optimal comparison states are conditionally retained; this metadata migration issues no new native-proof closure certificate for historical source-only records.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 484099163ad5923c721a17ed02a8bfe61a5e243cd60580b24b7510ff10037dc8

0<ε<ε_0, T∈N_0; fixed native structural inputs. Choose an existential fixed ε_0∈(0,2 B M_k) sufficiently small for the retained asymptotic cost bounds.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 5d0fb9620ee8c1ca5a75f6e71b75d2dbb0c3584cee021f81e84aac9116cbe3db

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: a7848e8bf2d182666b3b985e71619f448b58c5ea46a6aa7fd1f37864d5ca1bea

intermediate_accuracy

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: b43eb32c7b93c25b002a6c459235555a7862f5ed73781f6d273594e07e0a0b65

Finite-accuracy costs, one-query consequences, a sharper zero-query threshold and budget saturation are not assembled. This cell is not a proved open problem.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 89ce036d1ae6bba0eb20df905f00f9ef5f7b269d34fe75411de939162f9a6a11

ε_0≤ε<2 B M_k, T∈N_0; the same fixed structural inputs.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: a96aa49b825410a4c169c9290823c8d8569608c50a66a5829f153c3c0df8af1b

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: a1663bf2bfb82a8e4d0361be3a8f3151310759b4f74fa95489445a8f384dd2f0

zero_query

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: a6a7300ab88e00af7c0c31a4ab0d86a7c397dc441d3f3711e9d127ebc4c10699

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 166724120fd69c1acc4669638f66866de6b6ef204f72607b09b9bae3644ef492

Exactly C*=0 by explicit proof. All T≥0 are feasible. The sufficient threshold includes equality but is not claimed necessary.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 4ef7e161ae12b48dd292d6e57b29f4e43acde731bcced88bc68e3dfd23fc4a68

For the positive-amplitude Matérn kernel, 0<M_k<∞. The retained ε↓0 two-sided cost statement supplies a positive structural small-accuracy threshold; shrink it below 2 B M_k and call it ε_0. The three intervals (0,ε_0), [ε_0,2 B M_k), [2 B M_k,∞) are disjoint and cover ε>0, each crossed with all T∈N_0. These are bookkeeping cells, not asserted intrinsic phase transitions.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: d700d3a8a62b3f5bf39d14a3a9fe02bbd13c963da7f67e53dc68015447d5e142

No set-theoretic remainder: the intermediate-accuracy cell is explicitly unassessed. Dependence uniform in varying d, ν, B, k or X is outside this fixed-structure assessment and is not inferred.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: b2a1982cd0bf96372f1f3c52bdc3ef3d118f6300f7f6a7a2a683e7d3de41fcfd

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 960f588648c54667585589d7b61beeebf1217c9c3aa66ca5eebd274117876b56

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 5032e56af8e445579b6755061139596dc55449b8a0c6f174f9e9a9f64de08868

The inequality ε≥2 B M_k and its inclusive endpoint are exact sufficient conditions. The threshold is not an intrinsic or necessary transition. This is an endpoint/domain addition, not a main-exponent improvement.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 4e26aba6f1b2eac1906d821800a7190455e91828a1fc7a67770606a93fb9b7b2

G02_zero_query_endpoint

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 52466ac258db30b611a25a2748e651e626d67fc4ce43ed0a6ad2598d708d3f9f

Entire new c2 region: fills an unregistered endpoint with an exact call-cost result.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 40539d6b065a7742c948857e2c1937068b0178dae66b3b9563774b3eba0e06a7

c1 unchanged; new c2 has upper=lower=0 calls on ε≥2 B M_k.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 787c1c2aadcd38d2eebb8651ca620e71f4ea245c254074f3cf62315d3a2d1487

c1 contained only the small-ε asymptotic two-sided bracket; no native comparison or envelope was registered for ε≥2 B M_k.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 8ca7fb7d5f897a15e099dd6fbfc8675a6f69326b713ac2e64f85a1314be5c6dd

Original ε↓0 c1 bracket; no new assertion in 0<ε<2 B M_k outside the retained asymptotic cone.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 515d53c7a63bbb9225a6825da88b582ca998ebf48f5176b80adb8c3f0e4ff901

Choose a fixed x0∈X, query nothing, output x0. Reproducing identity and ||f||≤B give loss≤2 B M_k; costs cannot be negative.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 2eb9b352733c8cbadcfe41d8d8a556407330504cc8fe486bb3c3b3d7c528e913

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: d6a7661104d15de7c0ad826ad7bdfe540b8cd8c178c008855919ad12bceb62bf

First annotation adds interpretation and domain accounting. Scientific endpoint edits are separately supported by G02_zero_query_endpoint.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: d9a541dfe000a63d98a4f743bcbff7bd571b42f85692e178b625b6c8287a841f

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: f497fcb18ce18b8371fe2671888183faf24cbc71790c0e7b3fb8d3706f7fe887

G02_first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: bf34ac9990e887737508d30b7c4069fef936d16c0fa96c8cc47f221cbcbf9a4b

No numerical improvement from presentation.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: bd535ca2acdadde8ed5a451881fedf4ae719dadf5a0aa59322a52aa6adf6c9cf

Same bracket and status, with explicit fixed structural dependencies, ε/T tradeoff interpretation, endpoint separation and unassessed complement.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: fc7ce91dee61b9351aa017aa4efda0b58e6330b9cdc748fbb5f7ca8bd3b56e88

Original guarded O/Ω((B/ε)^(d/ν)) cost bracket with optimal status.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: d19ba3d0af668717ff39edf411d9078d62dcd5f0ec1a90759ed2dc19b190480c

All old scientific rows, guards, formulas, active references and statuses.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 02087d2659f6123d37e15913ded936cc478d039753bab79a0158aa534a2ab67a

The entire native domain is recorded; scientific retention applies only to original c1.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 5bb79f7817009d6a06424b4e3720d64bb429b7adad1d52abd4ab1018fbb86335

Exact baseline contract, parameter, view, quantity, resource, comparison and bound rows were read.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 9dc1ff7cb430d8330eb894df2d2a3059522b5254d1b4088841c4e5996c45de49

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 6907a2cd3437cd81fcdb07f8adf9b3211fcd7f822eaa19d71ff2e35e4b58650b

The exact-EI algorithmic improvement does not tighten this unrestricted minimax rate bracket. No finite-accuracy constants or uniform structural extension are adopted; the squared-exponential branch is outside the fixed Matérn contract.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: d9a541dfe000a63d98a4f743bcbff7bd571b42f85692e178b625b6c8287a841f

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: fb6e55aea79e22b4aa56af9cb346e14da69beddd822c0c9a6cb0988f35b05a4d

G02_fixed_prior_EI_2607_29245v2

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 5d2f329f22c380015182d03f5bfb4024544fc5c573b0c2e82c4517b6d9e8474d

None demonstrated.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: ccbba323f9a3a73944223fbdb49e52f5bc68d5912a5810f7cf0498387ad449f3

Unchanged; no additional bound adopted.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: e92cc61d712c9781e8ff818682a9f26f1b5c2ebb03de2aa1a5de8dde734ad8f4

Retained small-ε minimax exponent d/ν, dual regret exponent ν/d.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: d84b92f5130414880ad3c3b9296756e3fb82d06be245e1e66500ebbc1eecf998

Original c1.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 919f3e29a228ff22540d67915fc6a851e229ac265ed795e411957b3d6914bc02

Theorem 7.3's stated fixed-B Matérn compact-nonempty-interior large-N scope, with the paper's kernel normalization and fixed initial design.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 389f790f6552ecfa0bd0af38734ac0c49aa4a3a500d7ba74f0c488b07f3e8f1e

arXiv:2607.29245v2 Theorem 7.3, Eq.(7.4), read at characters 46000–50800, gives the same N^(-ν/d) exponent.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: b8b84b3fd0e16b16ff769eea07a310a2165b702f53efc581680dd14de41f6768

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: b6807a4e38c811454c15d83d5d34d54e720d8ad16b5dc950adf50f1d6e6e6590

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. Fresh revision addresses the preserved actual independent reviewer metadata issues with exact typed pending resource opportunities and honest closed/open publication bookkeeping. Unproved mappings remain pending, distinct IDs remain distinct, and no source guard or native inequality is broadened.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 6ef7ebc7da0be29f8c96e7631cf1949e92a31d5d6ec5db95bf7332880c31fade

curated_feedback_SO_ZO_G02_rand_expected_20261116_2f6e197d61

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: 12c299f274b3812f5bc9176a4a0ebfa244ae6bb730d0547689c483aab37685f6

Native quantity SO_ZO_G02_rand_expected__main__q1 in view main, guarantee g1, resource resource_cfa2de84ae: least worst-case path cap on scalar exact-value calls ensuring E[f(xhat)-min_X f]≤ε for every fixed f with ||f||_Hk≤B. ε>0 and T∈N_0 describe the accuracy/budget feasibility tradeoff T≥C*(ε); T is the optimized resource, not a second accuracy coordinate. The dual risk curve varies T. Structural d≥1, ν>0, B>0, complete known Matérn k with fixed positive amplitude/length scale, and compact X with nonempty interior are fixed separately for each theorem. Constants are not asserted uniform across those structural inputs. M_k is the known diagonal scale defined above.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 6b6117f9e3f9e56fa2ce424b2055ecd54225df0a34ed835010fe3622364f8237

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 9e03cbb1c3351d7322d79e566929371f88e0948261c304adb0c905119bf2aa25

Theorem-read follow-up for arXiv:2610.19925v1 (GP-TS/GP-CTS): metadata advertises the same optimal exponent but no source was fetched or read; finite-accuracy refinements remain unassessed.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 146dbe3fcfa203937fc4f05de29f08c810d4eb26ed70545770b11a7d6aa196ae

Any randomized-expected transfer from arXiv:2209.09655v1's deterministic entropy lower bounds remains unproved and unadopted.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: f28400f8d16cfd828f76ccc1300b6aebcf9dbf8f4a15423359bdb4942c88c37e

Finite-accuracy and one-query behavior in the intermediate cell, a sharper zero-query threshold, and uniform dependence on structural inputs remain unassessed. None can improve the exact zero cost on c2.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: 9fe21bac84498fd8e04a748573030d282337df978c9658d142204aadf7f47b90

Independent reviewer must verify the endpoint proof, frozen premises, all new native rows and the complete prepared joint analysis.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 967389e7bb6239d52446e562fa3eea9cc1bb59ac772cf3d91c4eac5395d1b878

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 405ae21e977af46051d936ee2b5b00876b38a5016dc97c410b0abced564c17fa

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 80ca81eeab68164c13c6d8454e54a404ccf3cfce156b450a2a3fa081e0e5ae1b

SO_ZO_G02_rand_expected__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 30f92b5ffa96751d9154ad085207485086f94e812f3754775c1d6d70e5992d75

Scientific row, guard and active references retained unchanged. Full structural constant dependencies made explicit in the first analysis.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: fabe5aa082b93b86d4e9eaef3ad3e99e8425b997a10ef31cbe268b63e7e5c0dc

For each fixed d≥1, ν>0, B>0, complete Matérn kernel k with fixed positive amplitude and length scale, and compact X with nonempty interior: ε↓0, equivalently T→∞ in the dual regret formulation.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: d9fc5fc4afd1754e0117a358938f4aa3b1c7cfa46c7a740c94b65b69f70227c6

Frozen /bounds/0 and /evidence/0; unchanged conditional maintenance premises, not fresh recertification.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4e42602dd74e81704f3b36561a6e4833c16266849ab9e96c63545645a4bb5863

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: ea6f7268b67961bb6301dcd6da052cbcb8ff5229f70d4bbd4d74651405384e93

SO_SRC_52c81802676000d4

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: baa1474713a4695d49dc0edd03deb370e81cb24ca1755d63ac7f3b0d86a2001e

Original comparison SO_ZO_G02_rand_expected__main__c1 only.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: e3586b448e72b86e4797e57d15965b3dedad2b2b4042ae6121f52cc111497b4b

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 49bce727e3a9650bddc37fc01e5bdbfc40e154d42edea44621920959b551232b

SO_ZO_G02_rand_expected__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 30f92b5ffa96751d9154ad085207485086f94e812f3754775c1d6d70e5992d75

Scientific row, guard and active references retained unchanged. Full structural constant dependencies made explicit in the first analysis.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: fabe5aa082b93b86d4e9eaef3ad3e99e8425b997a10ef31cbe268b63e7e5c0dc

For each fixed d≥1, ν>0, B>0, complete Matérn kernel k with fixed positive amplitude and length scale, and compact X with nonempty interior: ε↓0, equivalently T→∞ in the dual regret formulation.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 8c52e69db7ef35ec5a52c6f9510879c145755537924c5a07ace31176aa2d08e9

Frozen /bounds/1 and /evidence/1; unchanged conditional maintenance premises, not fresh recertification.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4e42602dd74e81704f3b36561a6e4833c16266849ab9e96c63545645a4bb5863

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: ea6f7268b67961bb6301dcd6da052cbcb8ff5229f70d4bbd4d74651405384e93

SO_SRC_52c81802676000d4

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: baa1474713a4695d49dc0edd03deb370e81cb24ca1755d63ac7f3b0d86a2001e

Original comparison SO_ZO_G02_rand_expected__main__c1 only.

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: e79bd73a16b08592ea018bb9313fe2b940fc8463a89fc36eb733a2bfb5257f4a

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 76bc91a05a40c466b71f10b1dafe044f244b69e98929f0c932d02c590facda13

SO_ZO_G02_rand_expected__main__b3

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: f90edca2cd14ecd669200e777770f8729d0b2bbffa0186541d19d2267a7c7072

Apply the identity to the unchanged native RKHS norm ball and actual kernel diagonal; choose one public feasible point with no observations. Deterministic regret implies expected regret under main/g1 with zero path cost.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: b75c398c5bdadd17c34034ec4621629943135c9bc47c9ab8ebcf9c6a917bfef7

RKHS evaluation/reproducing identity on a kernel's restriction to X; the source identity is not a zero-query theorem.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: a0f31897515b04d0e8c447c330585ef5215f7f87d381b0bfcacc773d620d40ef

Bull 2011 §3.1, printed pp.2885–2886, hash 72e5b25c2e3a79a2282e2a5672be6152fb9120853cc978cef6548124fe0dbf7a, characters 17000–19000; native proof SO_ZO_G02_rand_expected__main__p_zero_query.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4e42602dd74e81704f3b36561a6e4833c16266849ab9e96c63545645a4bb5863

#### Native item 1

Native pointer: /joint_analysis/provenance/2/source_refs/0; canonical SHA-256: ea6f7268b67961bb6301dcd6da052cbcb8ff5229f70d4bbd4d74651405384e93

SO_SRC_52c81802676000d4

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native item 4

Native pointer: /joint_analysis/provenance/3; canonical SHA-256: 956b797e586b95cfe2f7f68abffd83d6d2629c6f9c91d33194f94227bf1086fc

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/3/bound_id; canonical SHA-256: 238bd6ea110a92d723cead402597072edf0a1fcd31676f0c839e2b18fb70df67

SO_ZO_G02_rand_expected__main__b4

#### Native field: mapping

Native pointer: /joint_analysis/provenance/3/mapping; canonical SHA-256: 5607edb0a3bc2c8a580a4268e134d5112ecb9d64c59dcc65b8af7ed675193784

Nonnegative cost gives C*≥0; adopt only alongside the zero-query witness in c2.

#### Native field: origin

Native pointer: /joint_analysis/provenance/3/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/3/proof_refs; canonical SHA-256: ae53d620ad46afc29667951be1984aa69479c86db07189158fcc2f15da2fc697

#### Native item 1

Native pointer: /joint_analysis/provenance/3/proof_refs/0; canonical SHA-256: 2332d34f35f33c3ce7d1084e6312b6697364167a15419516fe921bd6226170c6

SO_ZO_G02_rand_expected__main__p_zero_query

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/3/source_domain; canonical SHA-256: 3dbf252ecb228f3c1439174cd8296df3b7a41dfeffc304877755cd4865524af9

Nonnegative scalar call counts in the frozen minimax cost definition.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/3/source_locator; canonical SHA-256: 8f7dc91089cc96b090bfa526b79bd4e49e1c928c74a883a60f8535290dbc4c3e

Frozen /quantities/0 canonical hash ac3ec3302a84ec5782e031bd58d142e47763e55c7de0b252bb7fc0ea7592fef1 and /common_specification/resource; proof SO_ZO_G02_rand_expected__main__p_zero_query.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/3/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/3/target_domain; canonical SHA-256: 5ae1c27951785bb11756d4380dcc95c012e6b82a7ad637575beb90ded72c9327

ε ≥ 2 B M_k, where M_k = sup_{x∈X} sqrt(k(x,x)); T∈N_0 arbitrary; all native structural inputs fixed.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 9226bd851193f960e033c041dfc7a81d512ec3ac57682f1e64097aa6e55556bb

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 022fc86aef16eaa36510ef7d995bcb05aeefe2ecad27156decfaac82e2377ccb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: b0fabc30037c552861a6a6747be3b9c5980ab503205f6b2d62907f73939a853a

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: cb8711bbc83f6ca854e44b3adf21baf04c08c6c0e46db362ba5ad3177c0c9d29

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 80ca81eeab68164c13c6d8454e54a404ccf3cfce156b450a2a3fa081e0e5ae1b

SO_ZO_G02_rand_expected__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 49bce727e3a9650bddc37fc01e5bdbfc40e154d42edea44621920959b551232b

SO_ZO_G02_rand_expected__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 76bc91a05a40c466b71f10b1dafe044f244b69e98929f0c932d02c590facda13

SO_ZO_G02_rand_expected__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/3; canonical SHA-256: 238bd6ea110a92d723cead402597072edf0a1fcd31676f0c839e2b18fb70df67

SO_ZO_G02_rand_expected__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: d9a541dfe000a63d98a4f743bcbff7bd571b42f85692e178b625b6c8287a841f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: d708dab090bc5468ff8f259240c700d4c807d8af8c4cdc95b200be8bf0840874

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: cb8711bbc83f6ca854e44b3adf21baf04c08c6c0e46db362ba5ad3177c0c9d29

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 80ca81eeab68164c13c6d8454e54a404ccf3cfce156b450a2a3fa081e0e5ae1b

SO_ZO_G02_rand_expected__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 49bce727e3a9650bddc37fc01e5bdbfc40e154d42edea44621920959b551232b

SO_ZO_G02_rand_expected__main__b2

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 76bc91a05a40c466b71f10b1dafe044f244b69e98929f0c932d02c590facda13

SO_ZO_G02_rand_expected__main__b3

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/3; canonical SHA-256: 238bd6ea110a92d723cead402597072edf0a1fcd31676f0c839e2b18fb70df67

SO_ZO_G02_rand_expected__main__b4

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: a6a7300ab88e00af7c0c31a4ab0d86a7c397dc441d3f3711e9d127ebc4c10699

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: cb711756142254df0c082b82797b2559b09e52cff27916df54a3a789df98a650

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 9e03cbb1c3351d7322d79e566929371f88e0948261c304adb0c905119bf2aa25

Theorem-read follow-up for arXiv:2610.19925v1 (GP-TS/GP-CTS): metadata advertises the same optimal exponent but no source was fetched or read; finite-accuracy refinements remain unassessed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: e5104dd3c0cc2610202243c817f73bbefdb481f558008fa1843a659bbc8bc7f9

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 146dbe3fcfa203937fc4f05de29f08c810d4eb26ed70545770b11a7d6aa196ae

Any randomized-expected transfer from arXiv:2209.09655v1's deterministic entropy lower bounds remains unproved and unadopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: 88d10e09e60ba8aac0f6e3f37f51278e29e7474c2efc069bfd672881937371ce

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: f28400f8d16cfd828f76ccc1300b6aebcf9dbf8f4a15423359bdb4942c88c37e

Finite-accuracy and one-query behavior in the intermediate cell, a sharper zero-query threshold, and uniform dependence on structural inputs remain unassessed. None can improve the exact zero cost on c2.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: efaece9255b6dd383cf83958a15a2160172d7d09cf9b353d27fce1e85ac7a95f

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: 9fe21bac84498fd8e04a748573030d282337df978c9658d142204aadf7f47b90

Independent reviewer must verify the endpoint proof, frozen premises, all new native rows and the complete prepared joint analysis.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: a61c915c6b95e55ee1805ef33516a7474b6a9f4b5aca4436c66052901e23a544

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 57f26bf65d837298451b28ab66594e6fd472ab93da9e90892f5d80c0f182d6a8

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 1f087363cd13608689f391ab2651f768d89bad2c7447d312c7a8a69e78ccbbbb

SO_ZO_G02_rand_expected__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 4204f09d56cad5b6f04c7bada3bcf0af9c5abf64373abc8ac69ad8a24b239bc0

SO_ZO_G02_rand_expected__main__c2

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 3e40840a600894217220d41fef8b41e169aa04b880d86f4edc42a2656c986f9a

curated-scope-limit-2f6e197d61

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 63fb27af81515626517ef650f9387c99e285ae8b3b605a5c145a4bf60f506364

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 95975fbeb49fca433f95136103497d1e6634695b8cad352c5daf3092bdb7c045

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 356ca51c51cdb952034764f73ca9afca9282d1cdb75c9dd99c98797579b9fce1

SO_ZO_G02_rand_expected_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 5c7c087d7dfed8f8e4c4f2d3f18db7fcbf75e892f80dad69e6c3b5fb76b2c91c

SO_ZO_G02_rand_expected_p_45a98071d4

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: 23bd96cfb31242b8e6f847198896dce37c41252ffbffad39f3fd7f47dac875bf

SO_ZO_G02_rand_expected_p_d920326707

#### Native item 4

Native pointer: /joint_analysis/target/allowed_constant_dependencies/3; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native item 5

Native pointer: /joint_analysis/target/allowed_constant_dependencies/4; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 0f312fb9ed196ecd3d74c17c74179c1db54e67f48131f2f2a8af1a4d3508beef

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

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 15dd24a7978859271fb001237c07a1f13bc0e4f3f2e6e1c7067cb4ee24f6b0af

/views/0/guarantees/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: cc65c380ab5d7173b93650dc4949698f6e90c5d2a977b8f8b8eca51c2532e1a8

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 4108b49c689e63dc5bda6f8a6fa6d7f586c89d063bde884a286342f160d317e2

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: a261dbf140eae16b1b73d6ffd721c713b05e5b70368374330e6ca23ee951d021

$d\in\mathbb{N},\ d\ge1$

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 356ca51c51cdb952034764f73ca9afca9282d1cdb75c9dd99c98797579b9fce1

SO_ZO_G02_rand_expected_p_bb728db2b9

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 356ca51c51cdb952034764f73ca9afca9282d1cdb75c9dd99c98797579b9fce1

SO_ZO_G02_rand_expected_p_bb728db2b9

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: bd3f654bc3777f5b6b30c0474e4dd671fa11443a0a402cd115d6120832c495a6

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 6a31bf0e0f1c5c569fd832c9f5efff45e01a0c965256338473b701471a8e0517

$\nu>0$

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 5c7c087d7dfed8f8e4c4f2d3f18db7fcbf75e892f80dad69e6c3b5fb76b2c91c

SO_ZO_G02_rand_expected_p_45a98071d4

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: 5c7c087d7dfed8f8e4c4f2d3f18db7fcbf75e892f80dad69e6c3b5fb76b2c91c

SO_ZO_G02_rand_expected_p_45a98071d4

#### Native item 3

Native pointer: /joint_analysis/target/fixed_parameters/2; canonical SHA-256: aed536242ab3c62f770a395d5a4e2a9a126ccd56fb648db868ca7d649f95252c

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/2/domain; canonical SHA-256: 0d525d25f1a809f3f17f8adec748e73f20db21c99ef239362c8bc09dcb4359a4

$B>0$

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/2/parameter_ref; canonical SHA-256: 23bd96cfb31242b8e6f847198896dce37c41252ffbffad39f3fd7f47dac875bf

SO_ZO_G02_rand_expected_p_d920326707

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/2/symbol; canonical SHA-256: 23bd96cfb31242b8e6f847198896dce37c41252ffbffad39f3fd7f47dac875bf

SO_ZO_G02_rand_expected_p_d920326707

#### Native item 4

Native pointer: /joint_analysis/target/fixed_parameters/3; canonical SHA-256: 06e7776b32f4b347007e2d0c04e47d8b1db7370b26efee7740b2edd24126567d

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/3/domain; canonical SHA-256: b7de4cedf25bd1efe7496997ba0c84e96f0cf1b6b69cee8c962cec8f8b04cb4f

$k:X\times X\to\mathbb{R}$

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/3/parameter_ref; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/3/symbol; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native item 5

Native pointer: /joint_analysis/target/fixed_parameters/4; canonical SHA-256: fe1c673db61d3fac6542e89d4dedeae89cece21b80532483f7770a45ff615b80

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/4/domain; canonical SHA-256: d0b05d6b2fa7afa7d2ed01d6806d6f4727f8c15e698a40e1557612205e64919b

$X\subset\mathbb{R}^d$; compact with nonempty interior

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/4/parameter_ref; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/4/symbol; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 12c299f274b3812f5bc9176a4a0ebfa244ae6bb730d0547689c483aab37685f6

Native quantity SO_ZO_G02_rand_expected__main__q1 in view main, guarantee g1, resource resource_cfa2de84ae: least worst-case path cap on scalar exact-value calls ensuring E[f(xhat)-min_X f]≤ε for every fixed f with ||f||_Hk≤B. ε>0 and T∈N_0 describe the accuracy/budget feasibility tradeoff T≥C*(ε); T is the optimized resource, not a second accuracy coordinate. The dual risk curve varies T. Structural d≥1, ν>0, B>0, complete known Matérn k with fixed positive amplitude/length scale, and compact X with nonempty interior are fixed separately for each theorem. Constants are not asserted uniform across those structural inputs. M_k is the known diagonal scale defined above.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: e72ba2c6f6ddbaa8d88f05241d3ef63b699d8cd5604af8b6c31eecca94462b8f

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 2fbfa8c688d9d7bfe021b5933c9130df6aa9cb1d9d03b86c20e9d0df1e934ffd

SO_ZO_G02_rand_expected_p_5c322c6737

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: f5b3e057feb3919b685c0ec38e797bc8ae5df2e7b7dc766156cb1efb08053633

SO_ZO_G02_rand_expected_p_aebd246b97

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 1f444506903264489e1c0c5a2a71bf873d72057577567ec17cf107233c9193db

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0; canonical SHA-256: 5f2a36c7416522b6f6f53fd5f75638dfacc204571e687ed583e2693a643bbc1a

#### Native field: expression

Native pointer: /joint_analysis/target/normalized_variables/0/expression; canonical SHA-256: bdce857303d003fa6f9b017b4b27227c7f838b27c3b039957158731d60d20aa2

M_k := sup_{x∈X} sqrt(k(x,x)), a known finite positive structural scale, not an additional independently varying input. The endpoint uses the original ε and B without changing their units or roles.

#### Native field: parameter_refs

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs; canonical SHA-256: 527146582e4a19f16555a1d4c44d5dada43fb18ab5ccd6b7c37eeb3471d5c62e

#### Native item 1

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/0; canonical SHA-256: 50845c55ce9f864fefceb660a0f6ca6498a0f2b7b52f4bdc43807ec8715ea259

SO_ZO_G02_rand_expected_p_fbdd52935e

#### Native item 2

Native pointer: /joint_analysis/target/normalized_variables/0/parameter_refs/1; canonical SHA-256: 6b89febcc04a773eb950ab1341c816f673f6baa38400a631031d15412ea0296f

SO_ZO_G02_rand_expected_p_fdf1bafcfd

#### Native field: symbol

Native pointer: /joint_analysis/target/normalized_variables/0/symbol; canonical SHA-256: 7e544133c83b6d05b3531ad8292f4e1b6b01d9ad9a01b695665ed9c82faf24c0

M_k

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: e72ba2c6f6ddbaa8d88f05241d3ef63b699d8cd5604af8b6c31eecca94462b8f

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 2fbfa8c688d9d7bfe021b5933c9130df6aa9cb1d9d03b86c20e9d0df1e934ffd

SO_ZO_G02_rand_expected_p_5c322c6737

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: f5b3e057feb3919b685c0ec38e797bc8ae5df2e7b7dc766156cb1efb08053633

SO_ZO_G02_rand_expected_p_aebd246b97

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Bull. Convergence Rates of Efficient Global Optimization Algorithms. JMLR 12(88):2879--2904, 2011.

https://www.jmlr.org/papers/volume12/bull11a/bull11a.pdf
