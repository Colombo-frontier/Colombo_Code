# Strongly convex quadratic objective accuracy: full-Hessian interface

**Setting ID.** `SO_HO_HOI03_S_full`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Fully optimal

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Full space; smoothness: Lipschitz gradient; structure: Quadratic

**ORACLE tags.** access order: Higher-order interface; feedback quality: Exact; interface family: Exact jet 2; operation: Exact jet 2; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Deterministic algorithms; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective is $f(x)=x^\top A x/2-b^\top x+c$, where $A\in\mathbb{R}^{d\times d}$ is symmetric, with $\mu I_d\preceq A\preceq\beta I_d$ and $0<\mu\le\beta$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

Admissible parameter domain:

$$d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$$

### Oracle interface

Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

The public inputs are $x_0$, the target accuracy, and $d$, $\varepsilon_f$, $\beta$, $\mu$, $\Delta$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive deterministic algorithms are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$f(\widehat{x})-f^*\le \varepsilon_f.$$

The running-cost guarantee is specified separately under RESOURCE.

## 2. Notation and parameters

$x,\widehat{x},x_0$: Query or decision point, algorithm output, and public initial point. **Domain:** $\mathbb{R}^d$.

$\mathbb{R}^d$: Real coordinate space; vectors use the Euclidean norm unless otherwise stated. **Domain:** $d$ is a positive integer.

$\langle u,v\rangle,\ \|u\|_2$: Euclidean inner product and norm.

$$\langle u,v\rangle=u^\top v,\qquad\|u\|_2=\sqrt{\langle u,u\rangle}.$$

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,2\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$J_{2}f(x)$: Function value and the complete tuple of derivatives from order one through the specified maximum order.

$$J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x)).$$

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$A,b,c$: Unknown symmetric positive-definite quadratic matrix, linear coefficient vector and constant term. **Domain:** $A\in\mathbb{R}^{d\times d}$, $b\in\mathbb{R}^d$, $c\in\mathbb{R}$.

$I_d$: The identity matrix in dimension $d$.

$A\preceq B$: Loewner order: the symmetric matrix $B-A$ is positive semidefinite.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\varepsilon_f$: Target accuracy **Domain:** $\varepsilon_f>0$.

$\beta$: Spectral upper bound **Domain:** $\beta>0$.

$\mu$: Positive spectral lower bound **Domain:** $\mu>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<C<\infty$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Nontrivial quadratic accuracy

**Region.** $d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$

**Quantity.** Q1

**Resource.** Each primitive response costs one call; all additional gradient queries at other points are also charged.

**Status.** Optimal

**Lower bound.** B2

$$
1
$$

**Upper bound.** B1

$$
1
$$

**Gap or comparison.** $1$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$

**Dimension conditions.** $d\ge1,\ 0<\mu\le\beta,\ 0<\varepsilon_f<\Delta$

**Oracle mapping.** Each query selects $x$ in $\mathbb{R}^d$ and returns the complete exact tuple $J_{2}f(x)=(f(x),Df(x),\ldots,D^{2}f(x))$. The fixed objective uniquely determines the response, with no stochastic noise.

**Guarantee mapping.** Deterministic-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each primitive response specified under ORACLE costs one unit. Queries at new points introduced by any inner procedure also count toward the total.

### B1 - Solve a linear system after one complete second-order reply

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Sources.** [1](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf)

**Local argument.** HO_QUADRATIC_INTERFACES

### B2 - Two translated quadratics indistinguishable without queries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All deterministic adaptive algorithms

$$
1
$$

**Sources.** [1](https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf)

**Local argument.** HO_QUADRATIC_INTERFACES

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 390111ee023deac2990879572a0ddf218b1c074d4227fa61d7c4f0506940753f

### Native proof: HO_QUADRATIC_INTERFACES

Native pointer: /proofs/0; canonical SHA-256: f5e858611eb3682777975cc17e716eab048da72d71e06061804848a95aad2444

#### Native field: algorithm_scope

Native pointer: /proofs/0/algorithm_scope; canonical SHA-256: cf3009e0d88b229779376cbde670ab56e921a1bd4541e806421399d5f281c3bb

Full-Hessian and HVP interfaces remain separate settings or oracle views as defined. The lower statement here concerns one-call impossibility for the full interface, not general HVP optimality.

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: ff6eb4c8d60ae195afb2a5b1e888144991f021177ddc2dc60821a1303bdf45c0

For $f(x)=x^TAx/2-b^Tx+c$ with $\mu I\preceq A\preceq\beta I$, a complete second-order response at $x_0$ gives A and $b=Ax_0-\nabla f(x_0)$. Free internal linear algebra returns $A^{-1}b$. When $0<\varepsilon_f<\Delta$, choose $A=\mu I$ and centers $x_0\pm\sqrt{2\Delta/\mu}\,e_1$. Their acceptable balls have radius $\sqrt{2\varepsilon_f/\mu}$, are disjoint, and give the zero-query lower bound. Thus the nontrivial complete-jet cost is exactly one.

An HVP returns only $Av$. Querying d basis vectors recovers A, while a set of fewer than d query directions has an orthogonal vector u such that a perturbation $\tau uu^{\mathsf T}$ leaves their responses unchanged. This is a matrix-recovery observation, not by itself a d-call lower bound for optimization.

Conjugate gradients uses an initial residual and one matrix product per iteration, terminating exactly within d iterations in exact arithmetic. Its Chebyshev estimate is
$$f(x_t)-f^*\le4\left(\frac{\sqrt\kappa-1}{\sqrt\kappa+1}\right)^{2t}(f(x_0)-f^*),\qquad\kappa=\beta/\mu.$$
Combine this with finite termination to obtain the linked upper bound. At $\kappa=1$, $A=\mu I$ is already determined by the public budgets and one gradient suffices. Polynomial-approximation lower bounds for Krylov methods cannot be promoted to arbitrary adaptive randomized HVP lower bounds after dropping their algorithm restrictions.

#### Native field: limitations

Native pointer: /proofs/0/limitations; canonical SHA-256: 918705965626e3df518889587e400c0256e29c0f4de1cd53ae94b6c6343683b9

The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

#### Native field: scope

Native pointer: /proofs/0/scope; canonical SHA-256: cf3009e0d88b229779376cbde670ab56e921a1bd4541e806421399d5f281c3bb

Full-Hessian and HVP interfaces remain separate settings or oracle views as defined. The lower statement here concerns one-call impossibility for the full interface, not general HVP optimality.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: b63a125c8fe8af156b5bde326786fb40dbfd88e16ab0c86d144aa6e6d267e6fd

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 76f7f1d469f61f81c72ba12b954046d401b8dc5233d3e86ef52231a8e4070189

SO_SRC_d696ef7ec0f25978

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 15848f1be96e7f2b1706714d8d377a74330a88758ea991e28c1f899217be4f66

One complete second-order response solves a known quadratic model exactly; HVP access has a distinct recovery and iterative cost.

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 95ef7140fcbde8f9fe5706a6e98458bff38723dbc06040ba4d37b7a25e01e28c

Quadratics: complete Hessians versus directional products

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 14e2a6e1405459a2cc9dc444a7bf2c3102764904d42dfe03c53920632d9c2192

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 7879de5cc06867bd1bb91084065ca64fe56fd6ec2b2445b591cb24731a01a753

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: fe17b132ca59010e33a71816b2a9205ce2a68ce07d869a32df7dcb7d7dc49860

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: ca6b46b4dd0827ba40749db685cc8398aec3760d0852dc975d5abd52c2747ba7

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 31b48c22ffb0b3adc237a4a6a1ba2a5f7d767037ed10f795c9c2837bd11cfff8

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 3f5716ca7b50ab1e8f01c026d636e4def96dc10a9bbb65d84411accc397572e9

SO_HO_HOI03_S_full__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: f37036fd1941ece8e32240e79b3f0703fd563a9ba0a9fa21709d6d61daa78fb2

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 78dd64d4fbf79cd6d8a9dafca646e903200c19b076900c2434134da89258ed0f

HO_QUADRATIC_INTERFACES

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 5144203b2fac52ef72b8827b1c2d665387a94a1305ec8d5e6c3be5cd82b63383

Retain the already active upper claim under the identical view, guarantee, quantity, resource and regime. Its retained local proof uses one complete reply at x0 followed by free exact linear algebra; no dimension, precision or condition parameter enters a hidden call cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 78e2a50875d83e2cf928ac4d9a39e8efaf36bbe386e0809eaea67f5c647bbaff

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: e0caf5157efb7275d6e99380b2a0130ec74c63986f01c68d43314a4d2b136390

SO_HO_HOI03_S_full__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: f37036fd1941ece8e32240e79b3f0703fd563a9ba0a9fa21709d6d61daa78fb2

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 78dd64d4fbf79cd6d8a9dafca646e903200c19b076900c2434134da89258ed0f

HO_QUADRATIC_INTERFACES

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 3ea1f6ef780e3fc670737af86bd82cfeb56a2313666e9cdd84af06ce5133aa49

Retain the already active unrestricted deterministic lower claim on exactly its existing guard. The retained local proof uses A=mu I and two translated centers with disjoint acceptable balls whenever epsilon_f < Delta; this is a zero-query impossibility argument already present in the baseline, not a new lower-rate improvement.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: eb5787b04d8ac93ef8ed13c4ae6983e175c9b5c64c542e5aaf33c0f1d5d69591

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 0c23779dc480cb24cffc77592dbd7cefdfa8e50ab417ccbde4c67208f51b8978

d=1 is included: the retained upper and translated-quadratic lower arguments have no sufficient-large-dimension guard.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 9e6ebe76e7d2775bbddadaf6306773ebffa2a713b228c7e375e41a8acfc4488c

mu=beta is included: positive definiteness and the retained witness A=mu I remain valid; hidden translation still prevents zero-query success.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 704d83d7efbd5f374bb38b6de08d646278b55477db59c6b58e202b1400ccce6f

For every strict 0 < epsilon_f < Delta, including approach to either endpoint, both retained claims use the same guard. The retained proof gives center distance 2 sqrt(2 Delta/mu) and acceptable radius sqrt(2 epsilon_f/mu), so their balls remain disjoint for every strict inequality.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 82f23c05f5ff49ea7b6b5d92aa795eb1b76d9cc01820cbb7060268373037375e

epsilon_f=Delta is excluded by the immutable contract; no zero-query endpoint or changed guard is adopted. epsilon_f=0, mu=0 and d=0 are also excluded.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 1d1286ccbfacd9ccba6243fa5de965a966a0a32245474b3ab9f4a12e6b011895

One full Hessian reply already reaches exact reconstruction saturation, uniformly in d, beta, mu, Delta and epsilon_f. Arithmetic, bit and storage costs are outside this resource projection.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 0247a388f04da047c6b7ec80b080502a7b2b7116d17e2fc436b0cd3b8356a5e0

Both mechanically compatible catalogue bounds are included. There are no unused native candidates, slices, dominance crossovers or source-activation thresholds to add. HVP, gradient-only, Krylov-restricted and randomized results cannot be substituted into this fixed contract.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: 09e54f0da1f25fe64433e46a729cbeb18d30520c29b5ad39bf3558e5f3c2d68e

Upper/lower ratio = 1 throughout the full target domain; the retained minimax cost is exactly 1.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 5507b13782c6e2f4f41c380337a485c03fe518d79c1f939bc3e985b0a58b282d

1 complete exact second-order oracle call on the full domain d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 22754f4786b79782343fca0a16b1fa96fa03e3742b56970621da38993caac5b9

No recorded upper/lower gap remains on this domain, conditional on the accepted baseline. This annotation does not independently recertify unchanged premises or establish exhaustive source/revision coverage.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 5507b13782c6e2f4f41c380337a485c03fe518d79c1f939bc3e985b0a58b282d

1 complete exact second-order oracle call on the full domain d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 783f4eaf41287a409d16bc7666695713b68f9ad7b81c96913d5e3faaa5576061

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: f574763fb4a6058e858461d61c97a7bc9d465f258fb67135e7f6eab8c1ad2b90

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: fc393de9f2f1c43d28fdf76a91076c6c99458ae61ef7d2560864a505068ff8a5

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: af83c61a494b25ca33aeb58127714b57b926cd7e3bcc4fea345cf1ef1fbd2008

existing-SO_HO_HOI03_S_full__main__c1

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: f37036fd1941ece8e32240e79b3f0703fd563a9ba0a9fa21709d6d61daa78fb2

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 78dd64d4fbf79cd6d8a9dafca646e903200c19b076900c2434134da89258ed0f

HO_QUADRATIC_INTERFACES

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: d750ba489f8f27fb1c0a4f5915e6f41e2667e26e26de749c9bcddeb34f7071ab

The sole native comparison and regime equal the full fixed target domain. Both sides are conditionally retained with exact envelope 1; there is no unrepresented target region. Literature verification is a separate unfinished obligation.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 3cd997aa83348e97b083848cdb5e60584c43a59e944e59ae988ec68a7f2c427b

The contract parameter domain, /regimes/0 predicate, and /comparisons/0 predicate impose exactly d >= 1, mu > 0, beta >= mu, epsilon_f > 0, epsilon_f < Delta; /parameters additionally makes d integral. Thus the single cell covers the full domain and disjointness is automatic. No domain extension is proposed.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: bf63cae1156200d905182254d68e1861f90bee6a4e33cc0d14d39c1fff95b167

Empty within the immutable target domain. Parameters d=0, mu=0, epsilon_f=0, and epsilon_f >= Delta are outside this contract.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: c0a29d3ac357193d08c1245713ed75d393efb495d15a2c2a2543908690bf8920

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 26ae9eafb24de18005bc489bda680a60b21f1fbc65a08e0d50b34c264f10f9a9

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: cd5cf968568b940ec4b197b0ea0bfa42f03c7d6e412ba198c6f3e0b8f68a7358

This is the first resolved presentation of retained scientific data. The recorded proof already states exact one-call cost, with no hidden parameter-dependent constants. No new normalized coordinate, external premise, transfer, bound or status is introduced.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 44052719ae6753dc8e56e22fa2e03b66786a73983f44d17ce71ef5404c2ddc32

SO_HO_HOI03_S_full__joint_uniform_annotation_v1

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 78d25ec9b4d4d45765f2de14795dcd5c1390c876d97643fb7492c399beade463

Empty: no scientific inequality, guard, active reference, envelope or status changes.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 8521b3cca8e242c1c3cacf8ba0e868dc254c5d8255f460fede655b7ff224bc3c

Upper=1, lower=1, ratio=1 on the identical guard. Add explicit joint uniformity, a single full-domain cell, retained provenance, candidate accounting and endpoint notes.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 67fc382caa40556cfa48948369e3a0f8f34c89fe30261eed23ebbca78db04a0d

Upper=1, lower=1, ratio=1 on d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta; the supplied joint-analysis draft had unresolved parameter roles and domain coverage.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 92b3daee81a58aeef7b0dd6a0b1cd4eba2301238e91110a86dc19492faa2503a

The entire target domain d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 54edb3111d656c78a94bfc75d035309df79c95f64dcecac19e626b8df1f9e5c4

Native /quantities/0 tracks all five parameters with fixed_parameters=[]; /comparisons/0 and /regimes/0 share the full contract guard; both compatible bounds are already active.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 04f65024a370583548d573dbe0e6429da492dc6c6982e8931e8969abcd5ce3fb

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 93019437de9339619270dcda0ec15afb195c2cb4e192fdbda8de2388d5ff0b7a

curated_feedback_SO_HO_HOI03_S_full_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 575b7f28cf68776371b9240f51c7fac69f078e493d3213256721f3956a97abb5

For quantity SO_HO_HOI03_S_full__main__q1, view main, deterministic guarantee g1, and resource resource_2314d30f1e (worst-case number of complete exact second-order replies): d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta. Minimize the call budget of one deterministic adaptive algorithm that returns a point with objective gap <= epsilon_f for every admissible hidden quadratic with mu I <= A <= beta I and initial gap <= Delta. All five native parameters vary jointly; x0 is arbitrary public input. Exact internal linear algebra and output at an unqueried point are free under the retained contract.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: dae236e599791d0e46525dda936859c8f5f58f13fe6f0e836d74b540d38ef0e6

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 21bf28a8ccb29c4e3437dce8abaa3473212c4262c9770e0df8c79b4c0172e1eb

Optional primary-source verification remains unfinished: the cited Hestenes–Stiefel 1952 NIST PDF exceeds the download limit (failure/event 86258e6cb08d4fb0f2884ce5fa5849f7cf7112e72539c999ae505c69341c41e0). No source hash or source_read was obtained. Any future source-based adoption requires a successfully archived primary version and decisive reading; this presentation-only finding does not depend on it.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: b5ef26557fdc680fc158dbb94ad236c5121218fd2bc285c7f73c1dae732a7c75

Broader literature and revision coverage is unassessed. The fresh terminal exact-title arXiv query returned zero records; the previously retired Crossref corpus and cursor were not exhausted or re-examined. This synthesis is conditional retention, not a completed literature certificate.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 4d1910ac99226bb1451ea55b999cd7443378984f08a965d7f9d9891b8bdcfae2

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 0cb1350638a115bd8b960c7b8049c8153ae46420424221b12391ba89439c1e02

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 3f5716ca7b50ab1e8f01c026d636e4def96dc10a9bbb65d84411accc397572e9

SO_HO_HOI03_S_full__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 0eceead778debca1d194278ff2c0aa77270e1a0cceb5718d32f9b6f626dbb02e

Identity retention of the existing contract: the exact reply gives A and b=Ax0-gradient f(x0); the retained free linear solve returns A^{-1}b. Existing source_refs remain in the native row; they are not newly verified source evidence here.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: f37036fd1941ece8e32240e79b3f0703fd563a9ba0a9fa21709d6d61daa78fb2

#### Native item 1

Native pointer: /joint_analysis/provenance/0/proof_refs/0; canonical SHA-256: 78dd64d4fbf79cd6d8a9dafca646e903200c19b076900c2434134da89258ed0f

HO_QUADRATIC_INTERFACES

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: a1c97d2bb1854b943883f2250ef0c6c39c17cedb22c6cbc5ce389133e045ac56

Retained local full-Hessian argument on d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta; no external theorem version is newly adopted.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 7dd42fbcfb4d9c6351d59eb34bcaa2bbafd5336aa84a34392ff2cd0d729a1bce

Frozen /bounds (first row), /evidence (first row), and /proofs/0 body, first paragraph; canonical hashes are in the finding baseline_refs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 75fbe4799dbf364a91615129a83b8123aba5191f0b0177f08e8891ab456ac6fd

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: e0caf5157efb7275d6e99380b2a0130ec74c63986f01c68d43314a4d2b136390

SO_HO_HOI03_S_full__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 4835d5f5efa55a172991d2a2b9e6fb0f708c76f67d699efed4edb74d2a863f2a

Identity retention of the existing deterministic claim. The retained witnesses have A=mu I, centers x0 +/- sqrt(2 Delta/mu)e1, initial gap Delta and disjoint epsilon_f-acceptable balls. They are admissible for every beta >= mu; all models, outputs, guarantees and call costs are unchanged.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: f37036fd1941ece8e32240e79b3f0703fd563a9ba0a9fa21709d6d61daa78fb2

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 78dd64d4fbf79cd6d8a9dafca646e903200c19b076900c2434134da89258ed0f

HO_QUADRATIC_INTERFACES

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 5631353c48f5018caaff1ca7e9930dc58fa6b7307eecf1993a85b521a60ee20b

Retained local translated-quadratic argument on d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta; no external theorem version is newly adopted.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: cf119639b498837040504763ba479a59337a5c0158e7436c0d9bb34c8f858a3d

Frozen /bounds (second row), /evidence (second row), and /proofs/0 body, first paragraph; canonical hashes are in the finding baseline_refs.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 0ff71e86183c9301a3e0c83d0309b9c74093db792ac9da0d8c55f56d056afbce

d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 2ebfbd23595ca082a53a7193a74d928418cfdb1299b71ae9ee837d7acee30c8f

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: bd6de4327ca624de368dc810ce163cd3eb85f87e8615bbfa69395d727a608855

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 8a3f5aeadf5a164a434d3b55cafad5ccbb2fe3c755ed6b137b3f1c1dfced5ac2

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 225ba96bac8d766a8038567d80162d93da9d988b315d0311ff6d2b0cf23e9f6a

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 3f5716ca7b50ab1e8f01c026d636e4def96dc10a9bbb65d84411accc397572e9

SO_HO_HOI03_S_full__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: e0caf5157efb7275d6e99380b2a0130ec74c63986f01c68d43314a4d2b136390

SO_HO_HOI03_S_full__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 65283e0551f656531cd3c387cd98b37f71497f4034a730cfae67974339544003

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 21bf28a8ccb29c4e3437dce8abaa3473212c4262c9770e0df8c79b4c0172e1eb

Optional primary-source verification remains unfinished: the cited Hestenes–Stiefel 1952 NIST PDF exceeds the download limit (failure/event 86258e6cb08d4fb0f2884ce5fa5849f7cf7112e72539c999ae505c69341c41e0). No source hash or source_read was obtained. Any future source-based adoption requires a successfully archived primary version and decisive reading; this presentation-only finding does not depend on it.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: 738055f2f2d1592cab43945279e705b53976c3e69d2f78fadb50606f9607d533

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: b5ef26557fdc680fc158dbb94ad236c5121218fd2bc285c7f73c1dae732a7c75

Broader literature and revision coverage is unassessed. The fresh terminal exact-title arXiv query returned zero records; the previously retired Crossref corpus and cursor were not exhausted or re-examined. This synthesis is conditional retention, not a completed literature certificate.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 0c1fefc8878c3023f0c8992f040182f27bc15f098cb53a199dab467c5ea68c87

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: d22486c12422e9d3f9ac5ccc39b1192f678aa871dd8bc0687d284e249ad7fdfb

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: fa7735a306637e0f08844b94df58088ac4d14bf14cdabe7266bec60c297dcc04

SO_HO_HOI03_S_full__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 467d952c7021718a69f5f416a0a5cf34e8cb869e8f8af1950d4453381885e6c7

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 1058648a7775a9dac8e75dddfe453a6a50a6211b380e9604b340015ace7362fe

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 575b7f28cf68776371b9240f51c7fac69f078e493d3213256721f3956a97abb5

For quantity SO_HO_HOI03_S_full__main__q1, view main, deterministic guarantee g1, and resource resource_2314d30f1e (worst-case number of complete exact second-order replies): d in N, d >= 1, 0 < mu <= beta, 0 < epsilon_f < Delta. Minimize the call budget of one deterministic adaptive algorithm that returns a point with objective gap <= epsilon_f for every admissible hidden quadratic with mu I <= A <= beta I and initial gap <= Delta. All five native parameters vary jointly; x0 is arbitrary public input. Exact internal linear algebra and output at an unqueried point are free under the retained contract.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 43799865a7303216091064d600e14fa547664bdffb730a4336b934be9683116b

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 669e722a097ea398473a1d0080ccd8d2a67c44f2aad5f8b531a27b4c0d102879

SO_HO_HOI03_S_full_p_20ab1f5fe8

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: eeb5e233369227b8050f40577f4fb724b70d697e434692dcf7c7a3583fdd2f30

SO_HO_HOI03_S_full_p_0c819dc462

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 16c7cb7ef49e85d55a076eeeac387aba58075ae6409467b0a65b33fbb9d8770d

SO_HO_HOI03_S_full_p_c6b6f18d70

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: e9134d4cb71f8a1323059fee17bd9fe34df57f6a811965813727e7e66493efa7

SO_HO_HOI03_S_full_p_255fbd175b

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 896750debaf2cbd0d5591ef03ccaeee9959e115f1b167ea8539aae184839c890

SO_HO_HOI03_S_full_p_360c30de02

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 43799865a7303216091064d600e14fa547664bdffb730a4336b934be9683116b

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 669e722a097ea398473a1d0080ccd8d2a67c44f2aad5f8b531a27b4c0d102879

SO_HO_HOI03_S_full_p_20ab1f5fe8

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: eeb5e233369227b8050f40577f4fb724b70d697e434692dcf7c7a3583fdd2f30

SO_HO_HOI03_S_full_p_0c819dc462

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 16c7cb7ef49e85d55a076eeeac387aba58075ae6409467b0a65b33fbb9d8770d

SO_HO_HOI03_S_full_p_c6b6f18d70

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: e9134d4cb71f8a1323059fee17bd9fe34df57f6a811965813727e7e66493efa7

SO_HO_HOI03_S_full_p_255fbd175b

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 896750debaf2cbd0d5591ef03ccaeee9959e115f1b167ea8539aae184839c890

SO_HO_HOI03_S_full_p_360c30de02

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Magnus R. Hestenes, Eduard Stiefel. Methods of Conjugate Gradients for Solving Linear Systems. J. Res. NBS 49(6), 1952, 409–436.

https://nvlpubs.nist.gov/nistpubs/jres/049/jresv49n6p409_a1b.pdf
