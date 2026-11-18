# Finite-precision Lanczos: joint-resource guarantee for a matrix-function action

**Setting ID.** `MX_S_finite_precision_lanczos`

Matrix computation

Compute the Lanczos approximation $\widehat y$ to $h(A)b$ in the specified floating-point model.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** task family: Matrix computation

**MODEL tags.** spectral structure: Explicit matrix class; spectral structure: Symmetric spectral interval

**ORACLE tags.** feedback quality: Deterministic roundoff; feedback quality: Relative roundoff; interface family: Finite precision matvec; operation: Finite precision matvec; operation: Public scalar function evaluation; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Deterministic algorithms

**OUTPUT tags.** certificate: No additional output certificate required; object: Vector

**METRIC tags.** criterion: Absolute function action error

**GUARANTEE tags.** time uniformity: Fixed time or accuracy

**RESOURCE tags.** accounting: Joint coordinates retained; measure: B fp; measure: N h; measure: N mv

## 1. Setting specification

### Task

Compute the Lanczos approximation $\widehat y$ to $h(A)b$ in the specified floating-point model.

### Admissible model

Assume $A=A^{\mathsf T}\in\mathbb{R}^{d\times d}$ with spectrum in $[a,b_{\mathrm{spec}}]$, $\|A\|_{\mathrm{op}}\le\Lambda$, and $b\in\mathbb{R}^d\setminus\{0\}$. The function $h$ satisfies $|h(x)|\le C_h$ on the extended interval $[a-\eta,b_{\mathrm{spec}}+\eta]$, where $0<\eta\le\|A\|_{\mathrm{op}}$.

### Oracle interface

Spectral bounds, $h,b,\Lambda,\eta,C_h$, and the target error are public. Floating-point operations follow the source relative-rounding model with unit roundoff $u$ and no overflow or underflow. Products satisfy $\|\operatorname{fl}(Av)-Av\|_2\le2d^{3/2}\|A\|_{\mathrm{op}}\|v\|_2u$ for each vector; exact $Av$ is not supplied.

A public scalar-function interface evaluates $h(x)$ to relative accuracy $u$ on the extended spectral interval: $|\operatorname{fl}(h(x))-h(x)|\le u|h(x)|$. This is the implementation assumption in Section 5. Count these calls separately as $N_h$; the running time of an expensive scalar function is not implicitly constant.

### Output

Return the point $\widehat y\in\mathbb R^d$ produced by the specified finite-precision algorithm. No separate error certificate is required.

### Loss or accuracy criterion

The base loss is $\|\widehat{y}-h(A)b\|_2/\|b\|_2$ with threshold $\varepsilon_{\mathrm{out}}$. Define $\delta_k=\inf_{\deg q<k}\max_{x\in[a-\eta,b_{\mathrm{spec}}+\eta]}|q(x)-h(x)|$, the polynomial-approximation error in the source bound.

### Resource accounting

The joint resource is $(N_{\mathrm{mv}},b_{\mathrm{fp}},N_h)$. There are at most $k$ approximate matrix-vector products. The specified postprocessing evaluates $h$ at at most $k$ tridiagonal eigenvalues, hence $N_h\le k$. The quantity $b_{\mathrm{fp}}$ is the effective mantissa precision for the entire run.

The three quantities remain independent resource coordinates. The source gives sufficient mantissa precision, and the scalar-function interface must additionally attain the stated relative evaluation error. Full arithmetic or bit-operation time depends on the implementation.

### Algorithm views and success guarantees

Use the source k-step finite-precision Lanczos algorithm with Gu-Eisenstat tridiagonal eigendecomposition. Adding full reorthogonalization changes the algorithm and its guarantee. Rounding follows Requirement 1 and the matrix-product error assumptions.

For every fixed admissible input and arithmetic error satisfying the stated rounding model, the source gives a deterministic action-error bound. There is no private randomness or success-probability parameter.

**Budget convention.** fixed worst-case joint budget; no expectation substituted

## 2. Notation and parameters

$d$: The order of the square input matrix and the dimension of each query vector. **Domain:** $d\in\mathbb N,\ d\ge1$.

$A\in\mathbb R^{d\times d}$

$a$: Left endpoint of the public spectral interval **Domain:** $a\in\mathbb R,\ a\le b_{\rm spec}$.

$a\le\lambda_{\min}(A)$

$b_{\mathrm{spec}}$: Right endpoint of the public spectral interval, distinguished from vector $b$. **Domain:** $b_{\rm spec}\in\mathbb R,\ b_{\rm spec}\ge a$.

$\lambda_{\max}(A)\le b_{\rm spec}$

$\Lambda$: Public spectral-norm upper bound for the input matrix **Domain:** $\Lambda>0$.

$\|A\|_{\rm op}\le\Lambda$

$\eta$: Width of the extension on either side of the public spectral interval **Domain:** $0<\eta\le\|A\|_{\rm op}$.

$[a-\eta,b_{\rm spec}+\eta]$

$C_h$: Absolute bound on the public function over the extended spectral interval **Domain:** $C_h\ge0$.

$\sup_{x\in[a-\eta,b_{\rm spec}+\eta]}|h(x)|\le C_h$

$k$: Number of iterations of the specified finite-precision Lanczos algorithm **Domain:** $k\in\mathbb N$.

$N_{\rm mv}\le k$

$\varepsilon_{\mathrm{round}}$: The auxiliary accuracy used by the source theorem to control rounding error. **Domain:** $0<\varepsilon_{\mathrm{round}}\le1$.

The rounding-error contribution is at most $\varepsilon_{\mathrm{round}}C_h\|b\|_2$.

$\varepsilon_{\mathrm{out}}$: Final matrix-function action tolerance relative to the input-vector norm **Domain:** $\varepsilon_{\mathrm{out}}>0$.

$\|\widehat y-h(A)b\|_2\le\varepsilon_{\mathrm{out}}\|b\|_2$

$b_{\mathrm{fp}}$: Number of binary significand bits used throughout the algorithm **Domain:** $b_{\mathrm{fp}}\in\mathbb N$.

$u=\Theta(2^{-b_{\mathrm{fp}}})$

$u$: Unit roundoff for elementary floating-point operations, matrix multiplication, and the scalar-function interface **Domain:** $0<u<1$.

$u=\Theta(2^{-b_{\mathrm{fp}}})$

$A$: The hidden real symmetric input matrix. **Domain:** $\mathbb R^{d\times d}$.

$b$: The public nonzero action vector. **Domain:** $\mathbb R^d\setminus\{0\}$.

$h$: Public scalar function satisfying the stated absolute-value and relative-evaluation-error conditions on the expanded spectral interval **Domain:** $[a-\eta,b_{\rm spec}+\eta]\to\mathbb R$.

$\widehat y$: The vector produced by the specified finite-precision Lanczos and tridiagonal postprocessing. **Domain:** $\mathbb R^d$.

$\delta_k$: Best uniform polynomial-approximation error on the extended spectral interval with degree strictly less than $k$ **Domain:** A nonnegative real.

$$
\delta_k=\inf_{q\in\mathbb R[z],\,\deg q<k}\max_{z\in[a-\eta,b_{\rm spec}+\eta]}|q(z)-h(z)|.
$$

$\operatorname{fl}$: Result produced under the specified floating-point model **Domain:** Use the same unit roundoff u.

$N_{\mathrm{mv}}$: Total number of approximate matrix-vector product queries **Domain:** $\mathbb N_0$.

$N_{\rm mv}\le k$

$N_h$: The number of evaluations of public h at eigenvalues in tridiagonal postprocessing. **Domain:** $\mathbb N_0$.

$N_h\le k$

$C$: Universal constant in the sufficient mantissa-precision condition **Domain:** Fixed positive constant absorbing the logarithm base and mantissa-counting convention.

$T_k,\widetilde\lambda_i$: The order-k tridiagonal matrix in finite-precision Lanczos and the approximate eigenvalues computed in postprocessing **Domain:** $T_k\in\mathbb R^{k\times k},\ 1\le i\le k$.

$q$: A real-coefficient polynomial in the uniform-approximation definition. **Domain:** $q\in\mathbb R[z],\ \deg q<k$.

$\lambda_i(A)$: Eigenvalues of a real symmetric or Hermitian matrix in nonincreasing order. **Domain:** $1\le i\le d$.

$\lambda_1(A)\ge\cdots\ge\lambda_d(A)$

$\|z\|_2$: Euclidean norm of a vector **Domain:** Finite-dimensional real or complex vector.

$\|z\|_2=(\sum_i|z_i|^2)^{1/2}$

$\|M\|_{\mathrm{op}}$: The matrix operator norm induced by the Euclidean norm. **Domain:** Any compatible matrix.

$\|M\|_{\mathrm{op}}=\max_{\|z\|_2=1}\|Mz\|_2=\sigma_1(M)$

$\log$: Natural logarithm **Domain:** Positive real argument.

$\log x=\ln x$

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

## 3. Complexity bracket

### Compared quantities

#### Q1 - source scoped metric resource statement

**Metric contract.** $\|\widehat y-h(A)b\|_2\le\varepsilon_{\rm out}\|b\|_2$ deterministically.

**Resource contract.** projection: Do not scalarize the resources. Retain matrix–vector products N_mv, mantissa bits b_fp, and scalar function evaluations N_h. The inequality for b_fp is a sufficient implementation condition.; vector: N_mv; b_fp; N_h

An attainable joint-resource guarantee for the specified finite-precision Lanczos algorithm. Matrix-product count, mantissa bits, and scalar-function evaluations are recorded separately. The mantissa inequality is a sufficient implementation condition.

### R1 - Joint regime of approximation error and rounding precision

**Region.** Require $0<\varepsilon_{\mathrm{round}}\le1$, $0<\eta\le\|A\|_{\mathrm{op}}$, and $7k\delta_k+\varepsilon_{\mathrm{round}}C_h\le\varepsilon_{\mathrm{out}}$, together with the floating-point model in Requirements 1-2 and the specified tridiagonal postprocessing. The stated mantissa length is sufficient for implementation.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Joint budget unresolved

**Achievable budgets.** B1, B2

**Necessary constraints.** No admitted claim in this comparison

**Comparison argument.** Retain the baseline b1 branch for k=1, with its unchanged source guard. For k>=2 use b2 under the source sufficient-precision conditions and r1. The final inequality in the proof of Theorem 1 gives coefficient 3k+4, and 7k-(3k+4)=4(k-1)>=0. Resource coordinates and sufficient-precision order are unchanged; see MX_S_finite_precision_lanczos__main__e2_sharper_proof for the complete source-to-target mapping. The old claim remains valid as conditionally retained history for all its former domain but is dominated by b2 on the k>=2 overlap.

### R2 - Additional tolerance window certified by the unrelaxed source proof

**Region.** All fixed source model, Requirements 1–2, scalar relative-evaluation and Lanczos/Gu–Eisenstat postprocessing conditions; k>=2; b_fp>=C log(d*k*Lambda/(epsilon_round*eta)) with the source's sufficiently large universal constant; (3*k+4)*delta_k+epsilon_round*C_h<=epsilon_out<7*k*delta_k+epsilon_round*C_h.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Joint budget unresolved

**Achievable budgets.** B2

**Necessary constraints.** No admitted claim in this comparison

**Comparison argument.** The guarded b2 certificate meets epsilon_out on this strict additional tolerance window; b1 does not certify success there. Same main/g1, quantity and resource vector. See MX_S_finite_precision_lanczos__main__e2_sharper_proof for the full mapping; no necessary-resource constraint is claimed.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Resource mapping.** Retain the joint budget (N_mv,b_fp,N_h), without an undefined weighted sum.

### B1 - k-step finite-precision Lanczos with the specified Gu–Eisenstat tridiagonal postprocessing.

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Deterministic witness

$$
N_{\mathrm{mv}}\le k,\quad N_h\le k,\quad b_{\mathrm{fp}}\ge C\log\frac{dk\Lambda}{\varepsilon_{\mathrm{round}}\eta}\quad\Longrightarrow\quad \frac{\|\widehat y-h(A)b\|_2}{\|b\|_2}\le7k\delta_k+\varepsilon_{\mathrm{round}}C_h
$$

**Sources.** [1](https://arxiv.org/pdf/1708.07788v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N h.** At most k evaluations of the public scalar function

**N mv.** k

**b fp.** Sufficient condition: b_fp>=C log(d*k*Lambda/(epsilon_round*eta)).

**Constants.** C is the universal sufficient-precision constant in source Theorem 1. Logarithm-base and mantissa-count conventions affect only C.

**Source location.** [1](https://arxiv.org/pdf/1708.07788v2) pdf pages: 3; 10; 11; 17; 18; 43; 44; theorem: Theorem 1; Requirements 1–2; Eq.(33); Appendix A.2 Lemma 23, Eq.(83); theorem or section: Theorem 1; Requirements 1–2; Eq.(33); Appendix A.2 Lemma 23, Eq.(83)

Theorem 1 and equation (33) give normalized error $7k\delta_k+\epsilon_{\rm round}C_h$ and sufficient machine precision. Requirements 1-2 specify elementary rounding and matrix-product error. Appendix A.2, Lemma 23 evaluates h entrywise on a k-dimensional diagonal eigenvalue matrix; equation (83) uses relative evaluation error. This implementation therefore uses at most k evaluations of h. The joint-resource statement gives sufficient precision, not a necessary bit lower bound.

### B2 - k-step finite-precision Lanczos with the specified Gu–Eisenstat tridiagonal postprocessing.

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Deterministic witness

$$
k\ge 2,\quad N_{\mathrm{mv}}\le k,\quad N_h\le k,\quad b_{\mathrm{fp}}\ge C\log\frac{dk\Lambda}{\varepsilon_{\mathrm{round}}\eta}\quad\Longrightarrow\quad \frac{\|\widehat y-h(A)b\|_2}{\|b\|_2}\le(3k+4)\delta_k+\varepsilon_{\mathrm{round}}C_h
$$

**Sources.** [1](https://arxiv.org/pdf/1708.07788v2)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N h.** At most k evaluations of the public scalar function

**N mv.** k

**b fp.** Sufficient condition: b_fp>=C log(d*k*Lambda/(epsilon_round*eta)).

**Constants.** C is the universal sufficient-precision constant already chosen in the proof of source Theorem 1, Eqs. (35)–(40). No explicit numerical bit threshold is claimed; neither the precision nor query-count asymptotic exponent is improved.

**Source location.** [1](https://arxiv.org/pdf/1708.07788v2) equations: 35; 36; 37; 38; 39; 40; 83; pdf pages: 10; 11; 17; 18; 19; 43; 44; printed pages: 9; 10; 16; 17; 18; 42; 43; section: Section 6, proof of Theorem 1; Section 5; Appendix A.2; theorem: Theorem 1 proof, final displayed inequality; Requirements 1–2; Lemma 23; theorem or section: Musco–Musco–Sidford, arXiv:1708.07788v2 (2024-11-18), Theorem 1 proof, Eqs. (35)–(40) and its last displayed inequality, physical PDF pp. 17–19 (printed pp. 16–18), source characters 42400–50900; Requirements 1–2 at 27000–33500; Appendix A.2 Lemma 23/Eq. (83) at 106800–114300.

Primary source SHA256: b38a13e4b0253d9f935e7fdd7dad72250216a99f909eabdc3cccc2aba5583565. Version/date and the cited ranges were independently read in this scout session.

The retained 3k+4 coefficient is explicitly printed in the source proof; this proposal makes no square-root-k or other unproved rate claim.

The old claim remains historically stored. Neither the sufficient bit condition nor this proof implies a minimax or necessary bit lower bound.

New adoption is restricted to k>=2, so the logarithm's argument is at least 2. The equality case k=1 remains an unchanged conditional-baseline branch; no new low-precision endpoint claim is made.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 50acefc0e93a564a69780ba8e253219898167a930c999bba6775b4688565a764

### Native proof: MX_S_finite_precision_lanczos__proof__strict_certificate_window_20261116

Native pointer: /proofs/0; canonical SHA-256: c1d22f391d0ba62b998a7cc2f2fbfbc992183b1f9c3b50f96628b2ae6010a76d

#### Native field: body

Native pointer: /proofs/0/body; canonical SHA-256: 3ee7877a78c3f793e79a8c666b62d50a8f775fe6c6fbfb224b0643b26e069582

Retain the exact accepted native source certificates 7*k*delta_k+epsilon_round*C_h and (3*k+4)*delta_k+epsilon_round*C_h, with all their source-sufficient precision and interval assumptions. This proof concerns their sufficient output-tolerance windows, not a necessary bit or minimax oracle bound. For the witness recorded below, h(t)=1+t^2/100 on [-1,1]. Averaging an affine approximant with its reflection cannot increase its uniform error, so an optimal degree<2 approximant can be chosen constant. The midpoint of h's range [1,101/100] is 201/200 and its error delta_2=1/200. At k=2, epsilon_round=1/1000 and C_h=101/100, the new certificate is 10/200+101/100000=5101/100000; the old is 14/200+101/100000=7101/100000. The chosen positive tolerance 6101/100000 lies strictly between them. Choose any finite precision satisfying all retained source-sufficient precision inequalities; the witness does not assert that this precision is necessary. The exact retained spectral/interval witness is: For a concrete legal strip point, take d=3, A=diag(-1/2,0,1/2), b=(1,1,1), a=-1/2, b_spec=1/2, eta=Lambda=1/2, h(t)=1+t^2/100 on [-1,1], C_h=101/100, k=2, epsilon_round=1/1000, and source-sufficient precision. The best degree<2 uniform error is delta_2=1/200, since the optimal affine approximant is the constant 201/200. The new and old certificates are respectively 5101/100000 and 7101/100000. epsilon_out=6101/100000 lies strictly between them.

#### Native field: evidence_basis

Native pointer: /proofs/0/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 7da365a354f89f52e6cd0c31217c753f17d85f32beec18f41bfa22c0f3c15fee

Strict tolerance-certificate window from retained coefficients

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 36aad59da6fdc2aa4dc4313a91b8bc6287d3a902217f522de582cd4cef60d688

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: 7e61ab3c51795ab5c9e1b73e7e0bfdb9eab3f6697d2cc907bc03e0e42219e15d

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 6e2120791b06078f0178d1a6429a63cafabb3abdeb79613841cc0fab8bf4ac8b

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 03e8600a002c2538c2a81a3f764b86a968d8b92f4f65c23cad1b1edf96b85baa

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: c1fcf6e3112b60adec7f906e53536b9422c60570de0d89bd4163fe0ae6dc0dfb

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: f1972e88a9eb4d652d1ac09db59df93ffe4f88d00f6fba3957e390623b4fa38b

S AND k=1 AND 7*k*delta_k+epsilon_round*C_h<=epsilon_out.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 59f1d48619f90b80d07a90a42edee0db5510bd7527c41441ef5c9f5aaac0b8fe

MX_S_finite_precision_lanczos__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: 9efd5da522afd7287a770ecfafb5f8a6ba94429bf8ef0b927f74c67fb929444e

Conditionally retain this unchanged branch. On k>=2 it is dominated by b2; no claim is removed from history and its source validity is not recertified.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 06929c82746e89425e1ac4181bf818b6d5cecb30325d5c067bc2611f7301311c

The unchanged frozen r1/source theorem domain.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: fe244f09e2c29e9af1f8cb83905b71af65eb01b2fe2092a6e557e5d3488ca369

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: aa9688e483bc174d33b0e31fc6e1580ea4e38b18b25070deccd99a2f6511c008

S AND k>=2 AND 7*k*delta_k+epsilon_round*C_h<=epsilon_out.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 2607dd903e3fc0c424cbcf30732d2c587043bdaa2d83ff49941ddfc4d985173d

MX_S_finite_precision_lanczos__main__b2_sharper_proof

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: 48f24d91a321a897ad0089086fd817c6eb0be146fcd57a7ab87349fd8af12ae2

The source proof maps directly to the same fixed contract and dominates b1 throughout this adopted intersection.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 34ffc8484e1c318d197fd6761be0ba3d4945a6fb2a71d202fa080ea3c6a45e0a

S AND k>=2.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: c1cc56eb8dcc422bfca648ced89a13bfdbb755812edea529a5f15cf8e8abadf7

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 4044fa73ee25944dd3236ab43fb15e92dde748044e37cc4253b64db534258c92

For k=1 the coefficients agree: 3k+4=7k. For delta_k=0 both errors are epsilon_round*C_h, so there is no strict improvement.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 6f8e9638a25a46aa495c63b2eb7e7425cb7396ede5a4cc125db1a3b7e703a6d9

If C_h=0, h is identically zero on the extended interval and delta_k=0; under the source conditions the error certificate is zero. This does not assert zero resource use by the fixed algorithm.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: da9d008a01c1d6aeaeae70452958890ce68554d04c9fdafe75f351c62983738c

The native strict conditions eta>0 and epsilon_out>0 remain; eta=||A||op and epsilon_round=1 are allowed by the source. No eta=0 endpoint or A=0 input is added.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: e4b6e3ab0bd10a81163c0e290a8091026b02dbeaa59d8ac1127d8312a51a24d8

The sufficient mantissa condition has an unspecified universal constant. No numerical precision transition or necessary bit threshold is asserted.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: 6cf6c3d87655cb1a29feb9c8bb87a2b787d61f9b839158ce3966c37a5b075e79

Low dimension, including d=1, does not justify importing exact-arithmetic k=d saturation in this roundoff model. No finite-precision exact reconstruction claim is adopted.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 483ab289c26b22e3de538c5ccb85088927ebad8a886bb7e94c4c0131d09d2225

A zero-output or other zero/one-query substitute would change the fixed algorithm. Its generic error consequence is not imported as a bound for this quantity.

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/boundary_checks/6; canonical SHA-256: 5523db9975c40899db1adf8ccb5494ea7e2b24e3bd4513e9aa2e7dffde5e9475

The coefficient comparison is for the same k, eta and epsilon_round. No monotonicity of k*delta_k or optimal allocation across different k or extension intervals is assumed.

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/boundary_checks/7; canonical SHA-256: 533927925661a7c095b24fc8ffb6ae29a691556705f648eb04ea32cca98d5e13

New adoption uses k>=2, making d*k*Lambda/(epsilon_round*eta)>=2. No zero logarithm is used to certify arbitrary low precision; the k=1 branch is only conditionally retained baseline.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: b039ab2209fa5b1e277550f8c7a5ecea9c80fafa400f14c06786e3da6c78d1b9

No scalar ratio is defined for this joint resource vector; necessary_resource_constraint remains missing.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: d7a27a5576ea057c336720d800b52c0d3f52f275a4dca54a0f06759a1e69a92f

No compatible necessary resource constraint is registered or adopted. Nonnegative resource coordinates are not a substantive lower bound.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 0b2e5b93a47ebe3e2eca870c5d00532201d05ab36a3b691ea4c890ca18ca773d

The error prefactor is improved, not the iteration or precision exponent. Optimal joint necessity and sharper compatible sufficient bounds remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 9e57f1f38a9a2361744c39bbd267cd64ac8611e916f1dc985af96e0a2cd25cae

For k=1 retain the baseline b1 sufficient error 7*delta_1+epsilon_round*C_h and its source guard. For k>=2 under S, b2 gives N_mv<=k, N_h<=k, b_fp>=C log(d*k*Lambda/(epsilon_round*eta)) and error<=(3*k+4)*delta_k+epsilon_round*C_h. These are guarded achievable joint-resource certificates.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 3d0ead460d22a6b433e1424a568e7f49ccd4ee5ec45cc249e0f27178c5f6e986

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 70a04c40328a057d6e708a23a4f8282d58ba389948a28d0e1c3999c9044d3e43

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 79480cef5ddbf7a1cd5599b08f9a4628421d001959821d3bdbce9a356c5a05a9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: 30a0924a3360be687d1df9fcbbfdff62c01bc0fd14036ab9076cf7f451568666

none

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 59f1d48619f90b80d07a90a42edee0db5510bd7527c41441ef5c9f5aaac0b8fe

MX_S_finite_precision_lanczos__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: cd3dc2faf64131ada5c13311e93814ad6ada2d5b7ae8b2c083062a1f704cc84e

inapplicable

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 0bb13501e747a4fdfbd02d63d777efa90952daeded5143d3edf1a3f068bb298f

On this strict strip the old certificate exceeds epsilon_out. This says the old bound does not certify success, not that the algorithm fails.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 0aa8e409f8f576cb3cbdcfc3a93a4ddb9d457f1c4dfc73f3d827c24d478f5b8a

The old error inequality is retained under S, but its registered output-success region requires 7*k*delta_k+epsilon_round*C_h<=epsilon_out.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 8b5866c42569254036ce66b4c269ac01a4cf98d3f0366ebbd91fd5ab707bf03c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: cd1447c4849a944b2fe7f8c35e80238930040eb3a3c84598e73bd7ff45cbd606

S AND (3*k+4)*delta_k+epsilon_round*C_h<=epsilon_out<7*k*delta_k+epsilon_round*C_h.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 2607dd903e3fc0c424cbcf30732d2c587043bdaa2d83ff49941ddfc4d985173d

MX_S_finite_precision_lanczos__main__b2_sharper_proof

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: d03d4a3010468f9e5f7f2992568fb227bc87f5dd53d09ade5f134f604493c906

The unrelaxed proof certifies the requested output tolerance on this additional guarded region.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 34ffc8484e1c318d197fd6761be0ba3d4945a6fb2a71d202fa080ea3c6a45e0a

S AND k>=2.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: c7b921e3a84a01ce5d4270ecf0e5a17617bd5974a7bc6f4bd7f5e7e35a751e65

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: caa59548fff790f980a29ff7995acb16cde881a4926cced8e270223085bf8d4a

The new lower tolerance boundary is included; the old upper boundary belongs to c1. The strip is empty when k=1 or delta_k=0.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: e7e43c4ab7e3ffc56747638bf415c5ff67c571100ce4c33e61ca8c93df67d1ea

All source precision, scalar evaluation, eta and rounding guards remain. Since k>=2, the precision logarithm has argument at least 2; its universal constant is still unspecified.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 563d07de10ffaea570f2fa3db581991e3fb155d5bf9b2273d20188d6f8391b58

No zero-query substitute, finite-dimensional exact-arithmetic saturation, necessary precision threshold or scalar gap ratio is imported.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: c143564103b69f0fe77cab0140ac53cc1621dff253cea9cbe2b74552233dbdd1

An additional achievable region is recorded; no necessary resource constraint or gap ratio is established.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: d7a27a5576ea057c336720d800b52c0d3f52f275a4dca54a0f06759a1e69a92f

No compatible necessary resource constraint is registered or adopted. Nonnegative resource coordinates are not a substantive lower bound.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 18dfd812621b274ade168d652fd281608f9d135bbee33c2685324e8e1a460c73

Only sufficiency is established. No claim that these two regions exhaust achievable performance of the fixed algorithm.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: ab7d1e7463cfbab07eb0df300e0a18d0ad2e01817c7ac96d2bdff48fd6795196

Attainable joint budget N_mv<=k, N_h<=k, b_fp>=C log(d*k*Lambda/(epsilon_round*eta)), with all guards S, giving normalized error <= (3*k+4)*delta_k+epsilon_round*C_h. It is an achievable resource region, not a scalar query upper envelope.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: 52b758c22a6ddd5e29ee31d2f3075dd9b613debcc736896b919d79abdfd01e5c

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 4a2e0ff962de60c83002da36b4f386e33d6ea822c862a0297cf54e6ad5e6ad12

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 35421eaa5bd47239bb9536b481a7bb52aa2137899c339fc582c40d31f2515e0a

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 4c12879ad572016a423c6c5464693f04ea7048168713233258f56967a44d42fd

retained_window

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 5875d6444e8569177978c897efe0cc50a58ca60b21f1c3446d4e334b3f72189c

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: d684e0c5fb869a210dd00793d3b03b61ecd7d1e6026d3193a2f2f2ea4b9efa95

The registered r1 window is preserved. Its active sufficient certificate is tightened; the necessary joint-resource side remains missing.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 167b6ae2b8edaab82c79703ea35cae5152809e2d651430d678ea13de328a54c3

Full target domain AND S AND 7*k*delta_k+epsilon_round*C_h<=epsilon_out.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: d683649d45ac1946019d0cdf77c47d9c87e08aaecbc64ea138f2f208639c3e6d

missing_lower

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 0afd2136be73daf2e14a821a830e9cc0f8e9301fd3b6660016f863bef951e181

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: b2b92cf4cd1a7c1708350c45cde1073d94abe43ef093a840d5d99cde17d616d8

additional_sharp_window

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: f87e4d6aacbdb9540bde269fcd52018e24f9f6f15c722919c22f105a8d0fce35

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: bd72d124af3653057eb1857458ae5dceb7f6ba37e3dfe17ec74149020ca807e2

A proved additional sufficient region for the same algorithm and quantity, with no necessary-resource result.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: da8a1c905c129bfd87e86d4fc6bf03ae1662b4b2fdaeecb4fa5e84e72483479b

Full target domain AND S AND (3*k+4)*delta_k+epsilon_round*C_h<=epsilon_out<7*k*delta_k+epsilon_round*C_h.

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

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 4f34763ddfd1eb5443f91f4f3c1e347961925c93620b7c640215cdba68468e0a

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 7e767166fae7ad55199595f15b014cd0120df03c878b93d835e19b9b9bc8eb8f

unassessed_complement

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

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 3cb1c5e082c6cb052e62e0a803aac891ebb584d67694bd81853b4d34c2283e94

Includes configurations below sufficient source precision or outside the proved error-budget windows. Failure of a sufficient condition is not impossibility.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: b271bc4a190b739d9471bf95199f065989ec0b2993b8311718f4f636b72515aa

Full target domain minus (retained_window union additional_sharp_window).

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

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: baa720fe70bba1c7b69b2625cf072722b2ed36b7b7d54db2518f57f0d0e5ac42

Since delta_k>=0 and k>=1 on S, 3k+4<=7k. Within S the two certified cells split the inequality (3*k+4)*delta_k+epsilon_round*C_h<=epsilon_out into the disjoint cases epsilon_out>=7*k*delta_k+epsilon_round*C_h and epsilon_out<7*k*delta_k+epsilon_round*C_h. All other legal points are assigned to the set-theoretic complement. This is coverage bookkeeping, not a scientific assessment of that complement.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: cbe3bfabc84513bf867fd289e4f92c4bc1f238e001f42a995c065d2e5bef7fc2

Exactly the cell unassessed_complement, including any native zero-step convention; it is accounted for as unassessed, not certified open.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 390d3f29d6fcfe808e428092fb17baaf272b6a7d7352e5004ed9332ad885fb71

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: 66091cb16865144bcebb6a71df24b32a068058194ceacfa0ddbea98e03956619

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 595ce4dde38e02a57f7d44509c542cf52887da41843feeba2867b9bf9c6a0a24

The source explicitly proves the unrelaxed coefficient. Algebra gives 7k-(3k+4)=4(k-1). This is a finite-coefficient certificate improvement, not a new asymptotic main-rate exponent or a numerical precision threshold. New adoption is restricted to k>=2; the equality branch k=1 is conditional baseline retention.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 5875d6444e8569177978c897efe0cc50a58ca60b21f1c3446d4e334b3f72189c

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: 2af10739ea6ae95e2dae11ff15719d2d1b472248df5cbd7757e79372c3c08b86

lanczos_unrelaxed_source_coefficient

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 9d5089588e118abe2d76aa8c7e0792fc4b3d00b6ad324a8f657cafada26d9a9b

Within that intersection, k>1 AND delta_k>0: the explicit error certificate decreases by 4*(k-1)*delta_k.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: abb3d3be2216fd2ae5153f8c435b8b00c3644c1913ffca914d20c0e1a20096f2

Same joint resources and source guards, normalized error <= (3*k+4)*delta_k+epsilon_round*C_h.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: ce4ae197fe9df1cc6ef1555bd34e4a523b056597f626052fee67b8c7230cb1b8

Same joint resources and source guards, normalized error <= 7*k*delta_k+epsilon_round*C_h.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 127f34b31d0a51cba070cb61738dfd0591663af32cb24ae88a81b4fabda4d5de

k=1 or delta_k=0; all resource exponents and the necessary side remain unchanged.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: af75394f2a74ace81f2a75529af97db7ca16ad89242454a9fad3213c41f6bd65

S; adopted intersection with r1.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 6912f0efb9c9c57360187479ead580594e8dcd4ececa4c68357c0d470e2b52a8

At k=2 the polynomial-error coefficient decreases from 14 to 10. Take the concrete input below with epsilon_out>=7101/100000 to remain in r1.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 4be028641db92b6d6cbb42a0148cfb04b14846d91c1ab4b30c0b42ac5919f0a7

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 5a4729193ffdfee727655fcfa6968e120a8b9b26d96fc972f51b57dd3c33a6f1

The source inequality implies the final tolerance whenever the new expression is <=epsilon_out. The two windows are disjoint by the strict old threshold. Exactness refers to this symbolic error-budget split conditional on S, not the unspecified absolute precision constant. The impact is historical relative to the pre-sharp certificate; current baseline c2 is preserved. New v2 fields specify its actual success inequality, not source applicability alone.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/1/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: dfd0a6268244b714aa2115ef7f324c071356f74ff36f8b57c3c6ab1248bafadd

#### Native field: new_domain

Native pointer: /joint_analysis/impact/1/extension_witness/new_domain; canonical SHA-256: b4e2a667c0a9f40519238de0a41e3915d705902a576310736562f36b82a0570a

Historical sharper success window: the retained k=1 branch, or S with k>=2 and (3*k+4)*delta_k+epsilon_round*C_h<=epsilon_out. S alone states source applicability and does not certify output success.

#### Native field: old_domain

Native pointer: /joint_analysis/impact/1/extension_witness/old_domain; canonical SHA-256: 84117c61304d3f9ee698cc59551ba0401b344d89aa0965c2e0bd05a421362f74

Historical pre-sharp source-success window: S and 7*k*delta_k+epsilon_round*C_h<=epsilon_out, including the retained k=1 branch.

#### Native field: outside_old_argument

Native pointer: /joint_analysis/impact/1/extension_witness/outside_old_argument; canonical SHA-256: a526564a0727c09831440ea5245e58c197db20436801a2de80ab8a6a837145f4

At the concrete k=2 witness the new complete error certificate is 5101/100000, the old one 7101/100000, and epsilon_out=6101/100000 is strictly between them. Thus the new sufficient certificate window contains a legal point outside the old sufficient window. This is an algorithm-certificate extension, not a minimax frontier claim. This is the retained historical certificate-window extension relative to the pre-sharp certificate. The current frozen copy already contains c2; this metadata curation adds no further rate or certified-domain extension beyond it.

#### Native field: outside_old_witness

Native pointer: /joint_analysis/impact/1/extension_witness/outside_old_witness; canonical SHA-256: 1f5c976416bc1ef34026a4f904cdcbd810c0021d65e76d898666b544d0786d59

For a concrete legal strip point, take d=3, A=diag(-1/2,0,1/2), b=(1,1,1), a=-1/2, b_spec=1/2, eta=Lambda=1/2, h(t)=1+t^2/100 on [-1,1], C_h=101/100, k=2, epsilon_round=1/1000, and source-sufficient precision. The best degree<2 uniform error is delta_2=1/200, since the optimal affine approximant is the constant 201/200. The new and old certificates are respectively 5101/100000 and 7101/100000. epsilon_out=6101/100000 lies strictly between them.

#### Native field: proof_refs

Native pointer: /joint_analysis/impact/1/extension_witness/proof_refs; canonical SHA-256: 24c154d0bbe8c8aa79f31f7f36a6d990dbe0b67b83cc4e6654ac37aa3f49fce7

#### Native item 1

Native pointer: /joint_analysis/impact/1/extension_witness/proof_refs/0; canonical SHA-256: 4e9aa3a3160dba245f68ac2dd234034faed26740e25efb96a9b6d3629e1d86f4

MX_S_finite_precision_lanczos__proof__strict_certificate_window_20261116

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 2ffe952260b8d1e73a0d49577fdec3c40300643461b43060135fffbfd4de55ad

lanczos_unrelaxed_tolerance_extension

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: 08a9771e484b86175f4b1fc0a1bfbe453db0f9035f0362cbd6dd237956d6226f

The strict additional_sharp_window cell.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: 6c09510eb937226bbc6ce35656f44dccd8607964af9f29cac4e5cd5bd9bdc3c4

domain_extension

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 45e6830035ce84ed4f7fe87489dcc89e65c0e6aac686fc36b318d991681868c6

Record also (3*k+4)*delta_k+epsilon_round*C_h<=epsilon_out<7*k*delta_k+epsilon_round*C_h with the same sufficient joint budget.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 7757673982a648cc22522f96da95907cd8e9ff2ee7197c6d9ca73fa5e7a3cd02

Only the registered source-success window 7*k*delta_k+epsilon_round*C_h<=epsilon_out was recorded.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: ee37a630baef8c17895b311b2742665a490581efc3df8059b783bb39f732338a

The old r1 region remains certified; the unassessed complement and all necessary-resource claims remain unassessed.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 0b6f1a225607812d99240668c23c571bc4afc9cbb8962d5a9c7c90f6a0657ed3

S.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 1f5c976416bc1ef34026a4f904cdcbd810c0021d65e76d898666b544d0786d59

For a concrete legal strip point, take d=3, A=diag(-1/2,0,1/2), b=(1,1,1), a=-1/2, b_spec=1/2, eta=Lambda=1/2, h(t)=1+t^2/100 on [-1,1], C_h=101/100, k=2, epsilon_round=1/1000, and source-sufficient precision. The best degree<2 uniform error is delta_2=1/200, since the optimal affine approximant is the constant 201/200. The new and old certificates are respectively 5101/100000 and 7101/100000. epsilon_out=6101/100000 lies strictly between them.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 1c4d87436d8f58d822371fb922c9245572684006a789036183d712b4f2959995

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 732444dee82bfa70d5eb5a8c3b512231ddd0ade8af61592a55ef2dcf38d2f12c

Complete the tracked native parameter list through the controlled metadata operation, using dependencies and universal constants already explicit in the frozen records. No new normalization coordinate, scalarization, minimax interpretation or scientific premise is introduced.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/2/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 33fa70d59df5d108e9d0d4afbdfe17c432c29f209e0b1a8444e9824e56cb41de

lanczos_first_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 5812355bac08322eba6c4e7c7443d5550f1e894ab4eadced644ea94fd733c4f4

No additional scientific region beyond the separately source-backed coefficient and tolerance-window changes.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 99068db003b29855054e5367e3466ede3ee641c7182aac2a1b13220b95f67406

First explicit joint target, guarded domain map, candidate accounting and residual scope. Scientific changes are supported separately by lanczos_unrelaxed_source_coefficient and lanczos_unrelaxed_tolerance_extension.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: d5def1b69541a1826a524a8ba10107e6e348057b27d3ccb944d0dd2257b06a6d

One frozen source-scoped joint-resource comparison, no supplied joint analysis; the old formula is retained as history.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: cc3911f95093c2695acddc30803cc6e6cd4d0a17900642856a6d2943e44e7752

Fixed algorithm, oracle, metric, guarantee, resource vector, parameter domains and the absence of a necessary side.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 58eaa38b5c92dc05e9e520636a6181d3ac95dc10178f9d19207c397d15999743

The fixed target domain, with science assessed only on the two certified cells.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: fdaa6950a1655834569ab1bcc6ea06a4c015b9f244f938b57006d46397c7e0fb

The only compatible old candidate b1 is included on the retained k=1 branch, dominated for k>=2 in c1, and does not certify success in c2.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 0f580ae77be4f12f710badfbcb481b7b4313ef9196a0f9f6fc4e13d1903a3692

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 6b0c31ada3e15c8e142d545b288540149be91d3c1e806abbc87712e1dd8bb6cb

Retain the accepted sharper fixed-algorithm certificate. Add a complete arithmetic witness proving the strict output-tolerance certificate window, not a minimax or necessary precision improvement; preserve every source-sufficient precision condition. Upgrade only the synthesis/impact bookkeeping otherwise. This revision addresses the preserved actual independent-review issues. Publication and typed projection obligations are explicit; every mathematical formula and adoption guard is verified against the exact native candidate, and historical effects are not reported as new frontier gains.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/3/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 780f6a53184abead86795546d0b62b6ecae2bd665eb83b984ff6e19dc6f7b6f6

curated_feedback_MX_S_finite_precision_lanczos_20261116_2a144b4edf

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

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

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: faedd2e3cd81f0da2729ce0682a1a10b782740019fd9308cefe72a3d6025fe5b

The immutable source-scoped quantity MX_S_finite_precision_lanczos__main__q1 in main/g1 with resource_868aec111b: the specified finite-precision Lanczos/Gu–Eisenstat implementation, not a minimax over algorithms. Jointly vary all listed native parameters on their declared domains: d>=1, k and b_fp natural, 0<u<1 linked to b_fp, epsilon_out>0, 0<epsilon_round<=1, Lambda>0, C_h>=0, a<=b_spec, and 0<eta<=||A||op<=Lambda, with symmetric A having spectrum in [a,b_spec], b nonzero, |h|<=C_h on [a-eta,b_spec+eta], and the fixed rounding/scalar interfaces without overflow/underflow. delta_k is the existing contract's polynomial-approximation error, not a new parameter. The theorem branches require k>=1; a zero iteration convention, if permitted by the native natural-number domain, is left in the residual cell. Constants are universal; no public dimension, precision or spectral scale is hidden. For use below, S is a sufficient source-applicability guard, not a restriction of the full target domain: S: the fixed model, deterministic main/g1 view, source Requirements 1–2, no overflow/underflow, the specified Lanczos/Gu–Eisenstat postprocessing, k>=1, 0<epsilon_round<=1, 0<eta<=||A||op<=Lambda, the stated relative scalar-function accuracy, and the source sufficient-precision realization b_fp>=C log(d*k*Lambda/(epsilon_round*eta)), with the universal constant sufficiently large as in the proof of Theorem 1. The relation u=Theta(2^(-b_fp)) is retained.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 16901b6a5969833a9313186c5b3c50e040cedea421e9b2ec78287101c8df240b

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 8e4370dc024cfc85b8898ab76a97d8a58f40e96542d796d8b4d3398cdd811b9b

Finish primary-source assessment of arXiv:2609.08066v1 and its precise relation to the fixed Algorithm 1 and action-error/output guarantee.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 15a8b5427781bb151590b7c927ad6a0069d3c89a90511ae47dfcb86af2e6fcc1

Finish arXiv:2608.21268v2 beyond independently read characters 0–10000 (Section 1, Section 2.1, and the start of Section 2.2) before drawing a general exclusion or deriving an action-error transfer.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: e25a1d5e846c0582060367797962e2e0a577197619dcc48552768c56fb7be938

Inspect arXiv:2410.11090v2 (2026-08-18 revision), arXiv:2106.09806v2, and the special-function/spectral-distribution leads 2608.07160v1, 2503.04427v1, 2303.03358v3, 2302.14842v3 for additional compatible guarded bounds; their metadata alone are not theorem evidence.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: daf1ce4ec170b27018be25aeeb8a11a729794fbe728f7763a9854ad0463b931d

A possible square-root-k sharpening via the Frobenius norm of the computed Lanczos basis has not been formulated and checked with complete precision/postprocessing constants; it is not used in this proposal.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: c4dde75a9f3a1b0614a901558684800c3dc3c283e768898e4034b3f7cb5ce72b

The legal complement of the two certified cells has no assembled envelope here. No conclusion about missing theorems or intrinsic phase transitions follows.

#### Native item 6

Native pointer: /joint_analysis/pending_obligations/5; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 2f5c3a70f6acf3c1aa4e195dfc1b360a2efc7cefcf7fb36f1f1ce5a78003aa82

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 1a89aca9ac88b8641ed9a25fdb2667fa8cd984777f79268226e0b8ad75c75501

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 59f1d48619f90b80d07a90a42edee0db5510bd7527c41441ef5c9f5aaac0b8fe

MX_S_finite_precision_lanczos__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: bc561f5a414c730a5e6f7f58003aca6ed7ff13876e1630516b3e27b2f7b88745

Unchanged baseline statement is conditionally retained and is not freshly recertified as a necessary or optimal bound.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 94137cfd34b2ac6ccacb543cbdcb8861d7960d6b091314d6531d53d81730e3be

Frozen source theorem domain and r1 guard.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: 593dc44b440894efd46dec1281629f50059b682a4e08221c10fcadd5db5e1cb9

Frozen /bounds/0, canonical SHA256 ab21771c29894e4fdd97c86e29d4d65b1f1dfe01d7dadf08bc870592f1215b16; conditional retention on the k=1 branch.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: f79665b9a2f10593d9b740a8d328290a3a82ecc62ae2a6686257410fbe22c231

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: 70fd816360b175f5796c25a779a0254b9891a55e33939f914750289a2f30eaae

MX_SRC_LA

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 3345cd1ff1138e9fea8beff818cd286d4ddc824023b25874c7ef8a8f2f14f472

The unchanged r1/source branch is retained actively at k=1 and historically elsewhere; b2 dominates on the k>=2 overlap.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 43f5226bc1d0d67854db7593f549014d75b246e7b20fad84a802a26dc1ad0293

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 2607dd903e3fc0c424cbcf30732d2c587043bdaa2d83ff49941ddfc4d985173d

MX_S_finite_precision_lanczos__main__b2_sharper_proof

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 04b78d5057959c01d5948845125650263f6d82359380b58538ad188eb487baad

Use n=d, x=b, f=h, epsilon=epsilon_round, epsilon_mach=u. The actual spectral interval enlarged by eta is contained in the public interval [a-eta,b_spec+eta], hence delta_actual<=delta_k. The public C_h bounds h there, and Lambda>=||A||op makes the displayed sufficient precision conservative. The proof's last displayed inequality before its runtime discussion is ||f(A)x-y||<=[(3k+4)delta_k+epsilon*C]||x||. Thus division by nonzero ||b|| gives the new normalized error. If the theorem statement is read with strict |f|<C, apply it with C_h+zeta and let zeta decrease to zero: its precision condition is independent of C. The same k-step implementation and Appendix A.2, Lemma 23/Eq. (83) use at most k matrix products and at most k scalar evaluations. No algorithm, oracle, output, rounding quantifier or resource projection changes.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: ddae27b67763f9c9e97b1642e696a251d27b99db3a39ead8f5cc37d45be99181

source_theorem

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 2b6b3f31ab7f7d77f5267310e36aa316609bf1087af5d3dc5e7c051493d44392

The real-symmetric, finite-precision, deterministic Algorithm 1/Gu–Eisenstat source domain, with the universal sufficient-precision realization in Theorem 1's proof.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: f4f78390dec8003e4671f64b7e71fd5de7c38bef252ea4af3eb9b35dc6105eb7

Musco–Musco–Sidford, arXiv:1708.07788v2 (2024-11-18), Theorem 1 proof, Eqs. (35)–(40) and its last displayed inequality, physical PDF pp. 17–19 (printed pp. 16–18), source characters 42400–50900; Requirements 1–2 at 27000–33500; Appendix A.2 Lemma 23/Eq. (83) at 106800–114300. Source SHA256 b38a13e4b0253d9f935e7fdd7dad72250216a99f909eabdc3cccc2aba5583565; native evidence MX_S_finite_precision_lanczos__main__e2_sharper_proof.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: f79665b9a2f10593d9b740a8d328290a3a82ecc62ae2a6686257410fbe22c231

#### Native item 1

Native pointer: /joint_analysis/provenance/1/source_refs/0; canonical SHA-256: 70fd816360b175f5796c25a779a0254b9891a55e33939f914750289a2f30eaae

MX_SRC_LA

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 7082c733c7007f2e00b803de81f0a801763bd3c2242165c0072d2d4f526b01ea

S AND k>=2, adopted on the retained and additional success windows.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 9e5626bb843ae5ee2cac4f11bd98c91d85475c005ad10105d181cdb808566ffd

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 0955fc8b6dcce520dfe83ad0a375de7a927bebcc62fc3f4cc834177ad6d88fe7

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 4b11ed1d5bc86f654df4991c4e3fad3f242b58b14ec72a73c124b647d06b2d35

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 2f332936aefa12d36be05feb873ff6a0282058221a5d21e17d06b65575f9c855

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 59f1d48619f90b80d07a90a42edee0db5510bd7527c41441ef5c9f5aaac0b8fe

MX_S_finite_precision_lanczos__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 2607dd903e3fc0c424cbcf30732d2c587043bdaa2d83ff49941ddfc4d985173d

MX_S_finite_precision_lanczos__main__b2_sharper_proof

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 5875d6444e8569177978c897efe0cc50a58ca60b21f1c3446d4e334b3f72189c

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 3278a71847ea0dfef3dfc750a7a39deb717063e54d3b74129907c7a3af3dfdd0

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 2f332936aefa12d36be05feb873ff6a0282058221a5d21e17d06b65575f9c855

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 59f1d48619f90b80d07a90a42edee0db5510bd7527c41441ef5c9f5aaac0b8fe

MX_S_finite_precision_lanczos__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 2607dd903e3fc0c424cbcf30732d2c587043bdaa2d83ff49941ddfc4d985173d

MX_S_finite_precision_lanczos__main__b2_sharper_proof

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: f87e4d6aacbdb9540bde269fcd52018e24f9f6f15c722919c22f105a8d0fce35

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: c88244b31de3611e0f898490625a2e8089149e5d2be6a619b4a85ce2deb796c2

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 8e4370dc024cfc85b8898ab76a97d8a58f40e96542d796d8b4d3398cdd811b9b

Finish primary-source assessment of arXiv:2609.08066v1 and its precise relation to the fixed Algorithm 1 and action-error/output guarantee.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: f9d231f8d5ebfc1c7ca38063baa582bea6bd7fb68e277595dfd5a59c951d3cb9

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 15a8b5427781bb151590b7c927ad6a0069d3c89a90511ae47dfcb86af2e6fcc1

Finish arXiv:2608.21268v2 beyond independently read characters 0–10000 (Section 1, Section 2.1, and the start of Section 2.2) before drawing a general exclusion or deriving an action-error transfer.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: ae6e8d58187809fef154cc3755f7a981ba41e5721afa40ce9a0c42cc1bb79bed

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: e25a1d5e846c0582060367797962e2e0a577197619dcc48552768c56fb7be938

Inspect arXiv:2410.11090v2 (2026-08-18 revision), arXiv:2106.09806v2, and the special-function/spectral-distribution leads 2608.07160v1, 2503.04427v1, 2303.03358v3, 2302.14842v3 for additional compatible guarded bounds; their metadata alone are not theorem evidence.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: efe77e121834642375466787a3f25b709121fa5e856745ad04a4e568112ba03d

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: daf1ce4ec170b27018be25aeeb8a11a729794fbe728f7763a9854ad0463b931d

A possible square-root-k sharpening via the Frobenius norm of the computed Lanczos basis has not been formulated and checked with complete precision/postprocessing constants; it is not used in this proposal.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: f3a5467b0572dfaeac0795e673f89df06081fb4b240da92ffe3cbfc3d492d4ff

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: a0050dd45f09b8c1454f66ddc34c7e3533ab3f980a23fb9c8576d4ecdca8fe45

retained-material-lead-4

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: c4dde75a9f3a1b0614a901558684800c3dc3c283e768898e4034b3f7cb5ce72b

The legal complement of the two certified cells has no assembled envelope here. No conclusion about missing theorems or intrinsic phase transitions follows.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 8

Native pointer: /joint_analysis/synthesis_coverage/obligations/7; canonical SHA-256: c9280676efe25efe2ebf8689d73334b49bdc4fd08f5451349660791da4edb097

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids; canonical SHA-256: 7490e6412d73799cac057b5118b037cae835e618169a6009fbd5805bbb2005ad

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/0; canonical SHA-256: b4c629877ab2e8627a2ef998997cf3910be60a407beac7901863c45c9ba0e5a4

MX_S_finite_precision_lanczos__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/comparison_ids/1; canonical SHA-256: ea6b3e35ceb9be1b6876381a5074ab1fd01d547c8e65eaeecf5da82edb862756

MX_S_finite_precision_lanczos__main__c2_sharper_window

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/id; canonical SHA-256: 7b66618750ce506ccf40819cef50f764846b4ebf660cc36789c8ef551ca05dfe

curated-scope-limit-2a144b4edf

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/7/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: f0695dfc53f8163953677fbd89343ce5b4b9692e26fbd615827509384ccdbf35

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: 3c0d891bc9205d7110a7fb2ff33896582b265891ed9becff5494e68dc57e8835

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: faedd2e3cd81f0da2729ce0682a1a10b782740019fd9308cefe72a3d6025fe5b

The immutable source-scoped quantity MX_S_finite_precision_lanczos__main__q1 in main/g1 with resource_868aec111b: the specified finite-precision Lanczos/Gu–Eisenstat implementation, not a minimax over algorithms. Jointly vary all listed native parameters on their declared domains: d>=1, k and b_fp natural, 0<u<1 linked to b_fp, epsilon_out>0, 0<epsilon_round<=1, Lambda>0, C_h>=0, a<=b_spec, and 0<eta<=||A||op<=Lambda, with symmetric A having spectrum in [a,b_spec], b nonzero, |h|<=C_h on [a-eta,b_spec+eta], and the fixed rounding/scalar interfaces without overflow/underflow. delta_k is the existing contract's polynomial-approximation error, not a new parameter. The theorem branches require k>=1; a zero iteration convention, if permitted by the native natural-number domain, is left in the residual cell. Constants are universal; no public dimension, precision or spectral scale is hidden. For use below, S is a sufficient source-applicability guard, not a restriction of the full target domain: S: the fixed model, deterministic main/g1 view, source Requirements 1–2, no overflow/underflow, the specified Lanczos/Gu–Eisenstat postprocessing, k>=1, 0<epsilon_round<=1, 0<eta<=||A||op<=Lambda, the stated relative scalar-function accuracy, and the source sufficient-precision realization b_fp>=C log(d*k*Lambda/(epsilon_round*eta)), with the universal constant sufficiently large as in the proof of Theorem 1. The relation u=Theta(2^(-b_fp)) is retained.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 87bb47040a0022f18b7cc73ec61ed06e8d76e762478286712ca5a967f836da0e

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: f8b4aefe29b43d96534df3191d9681b40ed40a135b4f7f597d65c05b889e4c70

MX_S_finite_precision_lanczos_p_22f33202a6

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 73f8aac8ab6a26632d7bf1340d7dad1964f73eb412a570ac9a04fa4325723057

MX_S_finite_precision_lanczos_p_6e9125a233

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 149e780adc0d198586cfc1c22a99edd4b3f6f8276a895ab1cbf622ebf4f58a70

MX_S_finite_precision_lanczos_p_88d0b17d69

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 4873942219ab0002d578dd9907ff74aa86e7800a5d5b2a057433d93790c086e4

MX_S_finite_precision_lanczos_p_06577fccb1

#### Native item 5

Native pointer: /joint_analysis/target/joint_variables/4; canonical SHA-256: 31dda120b3b4b7e0eead76df89d03dfba136a62e95e92a30388de0cc53ef21dc

MX_S_finite_precision_lanczos_p_c6f4869841

#### Native item 6

Native pointer: /joint_analysis/target/joint_variables/5; canonical SHA-256: b6d1f263060f695f4aefa097ed1a07c7fb6108c985c50a6535a46f8fab5b8190

MX_S_finite_precision_lanczos_p_1a87213055

#### Native item 7

Native pointer: /joint_analysis/target/joint_variables/6; canonical SHA-256: 0683e45557739acc351ccb9b22e192c4778a1b116727a7d66490907b2a8b8c26

MX_S_finite_precision_lanczos_p_8975d0411a

#### Native item 8

Native pointer: /joint_analysis/target/joint_variables/7; canonical SHA-256: 37994caab24d96e500b4d37cef96ab678d3be5ab07ca98958630eae4e19b7148

MX_S_finite_precision_lanczos_p_4cb221720f

#### Native item 9

Native pointer: /joint_analysis/target/joint_variables/8; canonical SHA-256: 6e8b17761ba529fe2cb2a2c47f44be025a02f0f0c6a21045641562e1f4f5de8f

MX_S_finite_precision_lanczos_p_379b08d916

#### Native item 10

Native pointer: /joint_analysis/target/joint_variables/9; canonical SHA-256: 57c4da5fb8729641a437c1bcbbda0ab0a95db20ba568e8ab2a55a86020c276bd

MX_S_finite_precision_lanczos_p_73dad158ac

#### Native item 11

Native pointer: /joint_analysis/target/joint_variables/10; canonical SHA-256: 67db6713d400260dafb99f199d4b103f889883f7603200ee000ab857e1e81c57

MX_S_finite_precision_lanczos_p_1d1d52d4bc

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 87bb47040a0022f18b7cc73ec61ed06e8d76e762478286712ca5a967f836da0e

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: f8b4aefe29b43d96534df3191d9681b40ed40a135b4f7f597d65c05b889e4c70

MX_S_finite_precision_lanczos_p_22f33202a6

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 73f8aac8ab6a26632d7bf1340d7dad1964f73eb412a570ac9a04fa4325723057

MX_S_finite_precision_lanczos_p_6e9125a233

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 149e780adc0d198586cfc1c22a99edd4b3f6f8276a895ab1cbf622ebf4f58a70

MX_S_finite_precision_lanczos_p_88d0b17d69

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 4873942219ab0002d578dd9907ff74aa86e7800a5d5b2a057433d93790c086e4

MX_S_finite_precision_lanczos_p_06577fccb1

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 31dda120b3b4b7e0eead76df89d03dfba136a62e95e92a30388de0cc53ef21dc

MX_S_finite_precision_lanczos_p_c6f4869841

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: b6d1f263060f695f4aefa097ed1a07c7fb6108c985c50a6535a46f8fab5b8190

MX_S_finite_precision_lanczos_p_1a87213055

#### Native item 7

Native pointer: /joint_analysis/target/uniform_in/6; canonical SHA-256: 0683e45557739acc351ccb9b22e192c4778a1b116727a7d66490907b2a8b8c26

MX_S_finite_precision_lanczos_p_8975d0411a

#### Native item 8

Native pointer: /joint_analysis/target/uniform_in/7; canonical SHA-256: 37994caab24d96e500b4d37cef96ab678d3be5ab07ca98958630eae4e19b7148

MX_S_finite_precision_lanczos_p_4cb221720f

#### Native item 9

Native pointer: /joint_analysis/target/uniform_in/8; canonical SHA-256: 6e8b17761ba529fe2cb2a2c47f44be025a02f0f0c6a21045641562e1f4f5de8f

MX_S_finite_precision_lanczos_p_379b08d916

#### Native item 10

Native pointer: /joint_analysis/target/uniform_in/9; canonical SHA-256: 57c4da5fb8729641a437c1bcbbda0ab0a95db20ba568e8ab2a55a86020c276bd

MX_S_finite_precision_lanczos_p_73dad158ac

#### Native item 11

Native pointer: /joint_analysis/target/uniform_in/10; canonical SHA-256: 67db6713d400260dafb99f199d4b103f889883f7603200ee000ab857e1e81c57

MX_S_finite_precision_lanczos_p_1d1d52d4bc

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Cameron Musco; Christopher Musco; Aaron Sidford. Stability of the Lanczos Method for Matrix Function Approximation. 2018. arXiv:1708.07788v2, revised 2024-11-18; SODA 2018.

https://arxiv.org/pdf/1708.07788v2
