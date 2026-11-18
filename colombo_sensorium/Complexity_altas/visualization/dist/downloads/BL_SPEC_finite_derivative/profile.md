# Finite-sum bilevel optimization: component gradients and derivative-vector products

**Setting ID.** `BL_SPEC_finite_derivative`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Bounded initial potential; initialization: Initial auxiliary domain; structure: Component regularities; structure: Finite sum

**ORACLE tags.** feedback quality: Exact; interface family: Derivative vector; operation: Component gradient; operation: Cross derivative vector product; operation: Hessian vector product; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; measure: N hvp; measure: N jvp; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

The upper objective is $f=n_f^{-1}\sum_{i=1}^{n_f}f_i$. Its components may be nonconvex.

Assume $g=(1/n_g)\sum_{j=1}^{n_g}g_j$; per-component strong convexity ensures uniqueness of the lower-level mean solution.

Each $f_i$ is twice differentiable. Function values, full gradients, and full Hessians have the respective global joint Lipschitz budgets $L^F_0,L^F_1,L^F_2$, uniformly across components.

Every $g_j$ is three times differentiable. The full first, second, and third derivatives have the respective global joint Lipschitz budgets $L^G_1,L^G_2,L^G_3$. Every $g_j(x,\cdot)$ is $\mu$-strongly convex, uniformly over components.

The objective $\Phi$ is bounded below. The source initial Lyapunov quantity minus $\inf\Phi$ has public finite upper bound $V_0$, fixed independently of accuracy and component counts. It includes the upper-level gap, lower-level value gap, and an adjoint quadratic potential.

The initial SRBA adjoint vector $v_0$ lies in the known ball $\|v_0\|\le L^F_0/\mu$. Subsequent projections apply only to this auxiliary vector; x and y may still be queried throughout their Euclidean spaces. Projection onto this known ball is an arithmetic operation, not a hidden projection oracle.

### Oracle interface

Public inputs are dimension, target accuracy, the model's budgets, and the initial point. The original functions, their lower-level solutions, and the reduced objective are hidden. Queries are restricted to the stated interfaces; inner optima and undeclared derivatives are not available for free.

The interface returns $(i,x,y), i\in\{1,\ldots,n_f\}\longmapsto \nabla f_i(x,y)$: exact derivatives or derivative–vector products of a selected component. No fresh population-noise oracle is supplied.

$(j,x,y), j\in\{1,\ldots,n_g\}\longmapsto \nabla g_j(x,y)$. Return the exact derivative or derivative-vector action of the selected component. No fresh noisy population oracle is provided.

$(j,x,y,v), j\in\{1,\ldots,n_g\}, v\in R^{d_y}\longmapsto (g_j)_{xy}(x,y)v$. Return the exact derivative or derivative-vector product of the selected component. There is no fresh noisy population oracle.

$(j,x,y,v), j\in\{1,\ldots,n_g\}, v\in R^{d_y}\longmapsto (g_j)_{yy}(x,y)v$ The selected component's derivative or derivative-vector action is exact. No fresh noisy population oracle is provided.

The same component index may be used at consecutive iterates. Every operation is still charged separately.

Equation (11), page 5 of the source bundles $[\nabla F_i,\nabla G_j,(G_j)_{yy}v,(G_j)_{xy}v]$, where $F_i,G_j$ are the upper- and lower-level components. Here the four operations are charged separately. At most four primitive calls simulate one source call; the other responses are not free with one gradient call.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Retain $(N_{\nabla f},N_{\nabla g},N_J,N_H)$. The scalar bound uses the sum $N$ of four call counts. The algorithm selects components; a full pass costs $n_f+n_g$ gradient calls, with vector products counted separately.

Initialization oracle calls count toward the total. A finite initialization bound is an instance-class assumption, not free access to an inner solver.

The budget is a fixed worst-case cap on every execution path; every actual response within a batch is counted.

Internal processing of available information is free. Comparisons use the explicitly specified scalarization or resource vector. Different resources without given weights cannot be assembled coordinatewise from separate algorithms.

### Algorithm views and success guarantees

Algorithms may use private randomness. Queries, stopping, and postprocessing may be arbitrary measurable functions of the transcript. The output may be unqueried, a random selection of a past point, or an admissible average. No linear-span or zero-respecting restriction is imposed. Queries are sequential; each actual response in a parallel batch is charged separately. Arithmetic, linear algebra, and storage using received data are uncharged. Internal operations, memory, and communication are not tracked by this quantity.

Choose one algorithm from the public parameters, then require $\mathbb{E}\|\nabla\Phi(\widehat{x})\|_2^2\le\varepsilon^2$ for every admissible instance and legal oracle law. Expectation includes all algorithmic and feedback randomness, with the instance fixed first.

**Budget convention.** fixed worst-case total number of calls on every execution

## 2. Notation and parameters

$x,y$: The upper- and lower-level variables. **Domain:** $x\in\mathbb R^{d_x},y\in\mathbb R^{d_y}$.

$f,g$: The original upper- and lower-level real-valued functions. **Domain:** $f,g:\mathbb R^{d_x}\times\mathbb R^{d_y}\to\mathbb R$.

$\widehat x,x_0,y_0$: Output outer point, public outer initial point, and public lower-level initial point **Domain:** Each lies in its corresponding variable space.

$\Phi$: The reduced objective. **Domain:** Defined in the task specification.

$y^*$: Mapping to the unique lower-level global minimizer **Domain:** Constraints specified under TASK.

$\nabla,\|\cdot\|$: Euclidean gradient and vector norm; matrix and higher-derivative norms are the induced Euclidean operator norms

$\mathbb E,\Pr,\inf,\sup$: Expectation, probability, infimum, and supremum, with aggregation order and randomness specified by the guarantee.

$\mathcal O,\Omega,\Theta,\widetilde{\mathcal O}$: Asymptotic upper, lower, matching-order, and declared-logarithm upper bounds; fixed parameters are specified in each evidence record

$c,C$: Positive absolute constants or functions of fixed budgets, with dependencies specified by the corresponding result **Domain:** $0<c,C<\infty$.

$\varepsilon$: Target accuracy. Whether error is squared is determined by the metric and guarantee formulas. **Domain:** $\varepsilon>0$.

$d_x$: Upper-level dimension **Domain:** Positive integer.

$d_y$: Lower-level dimension **Domain:** Positive integer.

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$n_f$: Number of upper-level finite-sum components **Domain:** Positive integer.

$n_g$: Number of lower-level finite-sum components **Domain:** Positive integer.

$n_{\mathrm{tot}}$: The sum of upper- and lower-level component counts. **Domain:** Positive integer.

$n_{\mathrm{tot}}=n_f+n_g$

$L^F_0$: Joint Lipschitz upper bound for each upper-level component value **Domain:** Finite and nonnegative.

$L^F_1$: A joint Lipschitz bound on each upper-level component’s full gradient. **Domain:** Finite and nonnegative.

$L^F_2$: Joint Lipschitz upper bound for each upper component's complete Hessian. **Domain:** Finite and nonnegative.

$L^G_1$: Joint Lipschitz upper bound for each lower component's complete first derivative. **Domain:** Finite and nonnegative.

$L^G_2$: A joint Lipschitz bound on each lower-level component’s full second derivative. **Domain:** Finite and nonnegative.

$L^G_3$: Joint Lipschitz upper bound for the complete third derivative of each lower-level component **Domain:** Finite and nonnegative.

$V_0$: Public upper bound on the finite-sum derivative method's initial Lyapunov gap, including objective gap and tracking error. **Domain:** Finite and nonnegative, fixed as accuracy and component count vary.

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$v$: The algorithm-selected direction for a derivative–vector query. **Domain:** $v\in\mathbb R^{d_y}$.

$f_i,g_j$: Upper- and lower-level component functions in the finite sums **Domain:** $1\le i\le n_f,\ 1\le j\le n_g$.

$i,j$: Upper- and lower-level component indices queried by the algorithm

$v_0,v_t$: Public initial adjoint vector and the algorithm's adjoint iterates. **Domain:** $v_0,v_t\in\mathbb R^{d_y}$.

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_J$: The number of lower cross-derivative–vector responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_H$: Number of lower-level Hessian-vector product responses **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O,\omega}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|^2\le\varepsilon^2\}.\\C=N_{\nabla f}+N_{\nabla g}+N_J+N_H.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Native squared-gradient regime of SRBA

**Region.** The quantity $n_f,n_g$ is a positive integer. Hold regularity and initialization budgets fixed, with squared-gradient tolerance $\eta=\varepsilon^2$ sufficiently small.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Lower bound missing

**Lower bound.** B3

$$
0\text{ on }r_1\cap r_{\rm zero};\quad\text{unrecorded on }r_1\setminus r_{\rm zero}
$$

**Upper bound.** B1, B2

$$
\begin{cases}0,&r_1\cap r_{\rm zero},\\O(N+\sqrt{N}\varepsilon^{-2}),&r_1\setminus r_{\rm zero}.\end{cases}
$$

**Gap or comparison.** Exact Q*=0 on r1 intersect r_zero, if nonempty; ratio inapplicable there. On r1 outside r_zero, the unrestricted-algorithm lower rate remains missing. The source linear-span lower theorem is not adopted.

**Comparison argument.** Zero endpoint follows from the explicit baseline-derived proof. The SRBA branch is conditionally retained with its old guard; this is not fresh recertification.

## 4. Bounds and supporting evidence

### B1 - SRBA

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\mathcal{O}\!\left(n_{\mathrm{tot}}+\sqrt{n_{\mathrm{tot}}}\,\varepsilon^{-2}\right),\qquad n_{\mathrm{tot}}=n_f+n_g
$$

**Sources.** [1](https://proceedings.mlr.press/v238/dagreou24a/dagreou24a.pdf)

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Oracle correspondence.** The algorithm chooses component indices. Exact component f/g gradients, $g_{xy}$-vector products, and $g_{yy}$-vector products are charged separately. A joint tuple in the source can be simulated with at most four such operations, and all scan costs are included. There is no inner-solve primitive.

**Guarantee conversion.** The native target is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$, a root-mean-square tolerance, rather than $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon^2$. If the source denotes squared-gradient tolerance by $\eta$, the exact substitution is $\eta=\varepsilon^2$.

**Output rule.** Return one outer point $\widehat x$. Expectation uses the oracle and algorithm randomness stated in the contract.

**Resource conversion.** Charged resources are $N_{\nabla f}$, $N_{\nabla g}$, $N_J$, and $N_H$. Use a fixed worst-case cap on each execution, not expected calls. Constants may depend on the six declared component-derivative budgets, $\mu$, and the uniform initial potential $V_0$. The symbol $L,\rho,\Delta$ is not a parameter of this specification.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N HVP.**

$$
O(n_{\mathrm{tot}}+\sqrt n_{\mathrm{tot}}\varepsilon ^{-2})
$$

**N JVP.**

$$
O(n_{\mathrm{tot}}+\sqrt n_{\mathrm{tot}}\varepsilon ^{-2})
$$

**N grad f.**

$$
O(n_{\mathrm{tot}}+\sqrt n_{\mathrm{tot}}\varepsilon ^{-2})
$$

**N grad g.**

$$
O(n_{\mathrm{tot}}+\sqrt n_{\mathrm{tot}}\varepsilon ^{-2})
$$

**N inner solve.** 0

**Constants.** Hold the stated regularity and initialization budgets fixed. Joint optimality is not claimed for parameters whose dependence is untracked.

**Derivation.** Rename the source upper-level component count $m$ as $n_f$ and the lower-level count $n$ as $n_g$, and substitute the squared-gradient tolerance $\eta=\varepsilon^2$. Each sampled direction uses only a constant number of the registered component operations.

**Source location.** [1](https://proceedings.mlr.press/v238/dagreou24a/dagreou24a.pdf) pdf pages: 3; 6; 7; section: 2–3; theorem: Corollary 3.6

### B2 - Zero-query output

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

**Dimension conditions.** Every finite dimension in the fixed model, uniformly.

**Oracle correspondence.** No primitive responses, inner solver or hidden-function evaluations are used.

**Guarantee conversion.** Pointwise ||grad Phi(x0)||^2<=epsilon^2 implies the native expectation-of-squared-norm guarantee.

**Output rule.** Return the public outer initial point x0; the contract permits unqueried outputs and requires no inner solution or certificate.

**Resource conversion.** All four primitive response counts and their scalar sum are exactly zero; a fixed worst-case cap of zero.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N HVP.** 0

**N JVP.** 0

**N grad f.** 0

**N grad g.** 0

**Constants.** Exact zero, uniform in accuracy, component counts and dimensions.

**Derivation.** Complete proof in BL_SPEC_finite_derivative__main__p_zero: use the native hypergradient row operator and the full joint Hessian bound to obtain ||grad Phi||<=L^F_0 L^G_1/mu, then return x0.

**Local argument.** BL_SPEC_finite_derivative__main__p_zero

Uses frozen model/output/resource/quantity premises; introduces no external theorem.

### B3 - Nonnegativity

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** analyst_derivation

$$
0
$$

**Conditions.** Full native domain AND epsilon>=L^F_0 L^G_1/mu

**Dimension conditions.** Uniform in every finite dimension.

**Oracle correspondence.** Each permitted response has nonnegative unit cost.

**Guarantee conversion.** Every algorithm satisfying the same native g1 guarantee has nonnegative minimax oracle cost.

**Output rule.** Applies to all permitted measurable outputs; no restricted algorithm class is assumed.

**Resource conversion.** The scalar sum of the four nonnegative response counts is nonnegative.

**Constants.** Exact zero, uniform in accuracy, component counts and dimensions.

**Derivation.** Every primitive call has nonnegative unit cost, so the fixed worst-case total cost and its minimax infimum are nonnegative. Restrict this universally valid fact to Full declared domain AND epsilon >= L^F_0 L^G_1 / mu to pair with the zero-query construction. No positive main-rate lower bound is asserted.

**Local argument.** BL_SPEC_finite_derivative__main__p_zero

Uses frozen model/output/resource/quantity premises; introduces no external theorem.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 283b4778c7e664c2d3bc334cfcea8b6eb2cd8192c2f753711bb8572c12ee9490

### Native proof: BL_SPEC_finite_derivative__main__p_zero

Native pointer: /proofs/0; canonical SHA-256: 85c0cc5e4b954c9743950ee12cc18187f8726d7c20e725db606296a800a0a436

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: 32c3515ff1ad8dfc25a3e51a8b1dc160f5f48cdd55969a9ffe83129eb28b7ea4

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: e4af8bb52beb3d188a02502814a11eeadfb8e3920e8668a4b4cd990a0e1eae0f

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: 15d5755b2b7b990b992fa9be67a628dad504eb0b1a4a96a7b6bf0967ea11062e

d33a17a1aba6105ecfb9ae35ddb4e6b7b242df14fd4e312375199362fe1184bd

#### Native item 2

Native pointer: /proofs/0/baseline_refs/1; canonical SHA-256: f8a65a4d269387ecc517e60c6675bd471fa13b1de9fc9a8f3f5df74cc60ba2e3

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/1/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/1/sha256; canonical SHA-256: f9c40791ab59f6ff1bd23eb0bbd55017c26f1c05f6bc8cb2eb74889db54441e9

8c88a0efe678a145d782a3dc529b252dc4b48f5da0b01c949bc3d4e4d0d0d94c

#### Native item 3

Native pointer: /proofs/0/baseline_refs/2; canonical SHA-256: 2079f5f0e1e8be36f6556d2bce988d56d679f703a78f9649c6666c797951a142

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/2/sha256; canonical SHA-256: d0a08d1a58ae73d321724128ae84a5abf2f45c66e541992893c245033c1565c6

8437b8515bc06f353548e01356cfa72978feb00e47575c2c5d89819fbf594e81

#### Native item 4

Native pointer: /proofs/0/baseline_refs/3; canonical SHA-256: 6e2b54c5239da9d7cfab90673b52beb07afe7af3fbcde0b9db68eb59ec9e9e81

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/3/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/3/sha256; canonical SHA-256: 25b8946945fee5301854ad5b19163f07ab099e498c4c44fe3ad4a8463b9bb7bb

d97d2b478ffd20573cb9422637964e5c9b5fb8577a74fb033c9b9095e2c2597d

#### Native item 5

Native pointer: /proofs/0/baseline_refs/4; canonical SHA-256: bca927000bff7e6e35101fe1faee841f4b28f832c2054a85b44d69ee4341f6a3

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/4/sha256; canonical SHA-256: 55dffa2e1f5b152dff137dcb38bac47a0b04002ca8af65474d2040838fbf6ea7

fd19c50dc5cbe6d31f7b8408a3fe9b0866f63f570e249a91326a5b72eb7b18ed

#### Native item 6

Native pointer: /proofs/0/baseline_refs/5; canonical SHA-256: 4d6ff2b8dad388caef4c8f6d832a730190ecc9d3d394a45ed3ab8017d0496c06

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/5/pointer; canonical SHA-256: b44a2fd7032b4504a0ddaadb1add048a3dc61965eb6a56b6915d532318c5217f

/symbols/5

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/5/sha256; canonical SHA-256: e345da4cc079dfe7c84fa67da532a830da0978d6bdeba54e68c133e4973b374f

a416fa77f489a2997fd40e62c6a4fead552e73047a9790c8c926a8c16cf5dca1

#### Native field: guarantee_id

Native pointer: /proofs/0/guarantee_id; canonical SHA-256: 49c3b80dc4f4d5988cec8b039b96c617ba3e3a2bf9d8cb58887203d2fe297ecc

g1

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: parameter_refs

Native pointer: /proofs/0/parameter_refs; canonical SHA-256: 0f7ba9f41405f76001a7215286f97281dbab4c7dfe978097ad7bef49a9a73f11

#### Native item 1

Native pointer: /proofs/0/parameter_refs/0; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native item 2

Native pointer: /proofs/0/parameter_refs/1; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native item 3

Native pointer: /proofs/0/parameter_refs/2; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native item 4

Native pointer: /proofs/0/parameter_refs/3; canonical SHA-256: 2d45e1738e78eda2df6560560b3cba22fcebbe6ead8ee7fc777e824335e230e5

BL_SPEC_finite_derivative_p_0d1c5067b5

#### Native field: proof

Native pointer: /proofs/0/proof; canonical SHA-256: 8ad0d78edea7738287f13a62545920fdbcd968d90bd149a13c68129597b3626a

Retain the frozen joint Euclidean norm conventions and native hypergradient identity. A differentiable L^F_0-Lipschitz component has gradient norm at most L^F_0; averaging preserves this bound for f. Differentiating each L^G_1-Lipschitz gradient gives ||Hess g_j||<=L^G_1, hence ||Hess g||<=L^G_1 after averaging. At (x,y*(x)), write Hess g=[[A,D],[D^T,C]], with C>=mu I. Set k=L^G_1/mu>=1 for a nonempty admissible class. For every w, applying Hess g to (0,C^-1 w) gives ||D C^-1 w||^2+||w||^2 <= (L^G_1)^2 ||C^-1 w||^2 <= k^2 ||w||^2. Thus ||D C^-1||<=sqrt(k^2-1), and the row operator [I,-D C^-1] has norm at most k. The native identity grad Phi=f_x-D C^-1 f_y now yields ||grad Phi(x)||<=L^F_0 k at every x. Output the public outer initial point x0 without querying any interface. The contract requires neither an inner point nor a computed certificate; no initialization oracle responses are needed to return x0. For epsilon>=L^F_0 k the deterministic squared-gradient error is <=epsilon^2, including equality. All four response counts are zero on every execution. Nonnegative response costs imply Q*>=0, so Q*=0 on this sufficient region. The proof covers L^F_0=0. It asserts no converse below the threshold and is uniform in sample counts and dimensions; it uses no V_0 premise.

#### Native field: quantity_ref

Native pointer: /proofs/0/quantity_ref; canonical SHA-256: 5a5cc046a79f887c527f717e016cdb1199463b5fb9478eff1555dfd812c78530

BL_SPEC_finite_derivative__main__q1

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 526b795a96aff8fa3b33a26acaef57bd236177e0e137b3ee7d4c0241f7eedf09

Q*=0 on Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: view_id

Native pointer: /proofs/0/view_id; canonical SHA-256: e4a9e4d8baa71a9d8ebf56ec8ae3ea1e82be9f96ae6fe89e36d701d4a5337f30

main

### Native proof: BL_SPEC_finite_derivative__proof__canonical_bracket_justification_20261116

Native pointer: /proofs/1; canonical SHA-256: 4269837cdca5129e12454783ab99aeafb275fd3864ccdd6978fc11a86358d0e1

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 684c665b3c4a236b79d382a25b94eb03fc9570c5fe4b721f3a0d02e3cd7a093a

Use the exact frozen native comparisons, bounds, proof records and joint ledger listed by the current curator's baseline_refs; no new external theorem is assumed. For a fixed comparison predicate and unchanged quantity, view, guarantee and resource, matching upper/lower zero implies exact complexity zero by nonnegativity. Its canonical main state is optimal and a multiplicative ratio is inapplicable. Matching positive-cost upper/lower orders likewise use optimal; saturation is a separate region property. An alias does not establish any new inequality. Aggregate summary counts are the histogram of these actual native states; missing sides are their union; only logarithmic_gap, polynomial_gap and other_quantified_gap belong to gap_classes. Joint-budget-unclosed is its own special state and does not define a scalar ratio. These are definitions of the existing Atlas status contract, not a new claim about unassessed literature. 

#### Native field: comparison_refs

Native pointer: /proofs/1/comparison_refs; canonical SHA-256: c20406c284d0402187f439c9fee257d8f34423f2a86008c1c7c51cb3ff448c1d

#### Native item 1

Native pointer: /proofs/1/comparison_refs/0; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: evidence_basis

Native pointer: /proofs/1/evidence_basis; canonical SHA-256: 46f58402184a9d56ab63bdeb88c6d69e5d38f27b890634b1772adff172da2801

retained_baseline_derivation

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 336d0ebff1d6dfa719b832f9eb07ca4dbb207686cf09b2f52a51e286debb6c9b

Canonical state and previously proved region publication

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 8cfda4940f60b2751c1a01963188e193a7626fc51ad38845f814ce64f6de4688

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: e1d1d8e1eacf0fb269fe4d99763c062913732585052dbdbd247ad469c2b0a2a4

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 5b1d23f3780cbea68dd66e3628d2595cf75e9152fe443ae6bf57d5e91b6e4e51

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 93f606d3685fd8d530f1fdcaf952be7f09b744d9e926ea88e66cd03eafd8bc40

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: f07b3eae73c5d0f3cf09be5bc7d307dc560ebe11945c10fc488e74650fee5ed1

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 127ccd5627c8f387a6202ff2e30df46bd8a97322e27410e094e55ba400e19f05

r1 outside r_zero

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: 7c2e5fb6a9afac277357c6cddca84b2036476b75c4b1436b6202cc3701654d1a

BL_SPEC_finite_derivative__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: eb751df3570f74c969e6e4eb77a60a15ef9dda20fa6a3111b89087760594f405

Conditionally retain SRBA only on its original guard, except where exact zero dominates.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 3056d68ed14abf936476cae06aa906123d38bcfeea5105de7c531deed8eb7b39

The unchanged native small-accuracy predicate of BL_SPEC_finite_derivative__main__r1

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: c1e1bfd487afbf6178caef65223c2f22c11bccfdf0ba78d6dcd8a66eb8723168

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 88ec3fd38f947df36f4b863a94512f9d25306a7b9f588155d9d7911c5e0b49d2

r1 intersect r_zero (possibly empty)

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: 96138fb695c03501531e22d6439b9807ebcadb499348a219bee63137228975d0

BL_SPEC_finite_derivative__main__b_zero_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: ec97ab70ff3060cd98a031e95b52fb258e4e7801105cf7816422247547878ac6

Zero-query upper dominates every positive upper branch on the overlap.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/bound_uses/2; canonical SHA-256: 06ce755799a96adac42766d4c1cf0dedd7258b147bae93e1f9c72ed16b880336

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/adopted_region; canonical SHA-256: 88ec3fd38f947df36f4b863a94512f9d25306a7b9f588155d9d7911c5e0b49d2

r1 intersect r_zero (possibly empty)

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/bound_id; canonical SHA-256: 6a36d9bbff5cce9e3fdcbd6b4e28bee469c3666bd7e79a32c5dd4930e86c4179

BL_SPEC_finite_derivative__main__b_zero_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/reason; canonical SHA-256: 499b3ce53c182a80a378c7acd8b6314f3327441e61f6c27cd9273b1388644f45

Nonnegative cost pairs with upper zero only on the guarded endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/2/validity_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: a9f2dcb2a50a612dbc005c873168ee7d421d47c2c9c1f44f3c83b3af82efe3d6

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 5ecb115fe80c0ef63e75763c334eac9dabd449931a16d0d44cafdc636466635f

Inclusive epsilon=L^F_0 L^G_1/mu is proved; epsilon below that value is not asserted nontrivial.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 8d08aef21bbb8a240c63e2c826855cfa8e1fde26e81f5cdc6cbdd95d8703a05c

r1 intersect r_zero may be empty; the inherited small-accuracy predicate has no numerical threshold supplied.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: b9594aecc2e7ae41633e50e4e4daf2e945f144bb7d3c00fb5f702ef5bb5528cd

N>=2; N versus sqrt(N) epsilon^-2 crosses at the asymptotic scale N~epsilon^-4, not a source activation threshold.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: c8da9b9e9d76f196702c580609ba3d87698bfdd308ce02555a76b6c903acfaee

Uniform over every positive split (n_f,n_g) and finite dimensions; no finite-dimensional saturation or sqrt(n_g) lower term is inferred.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 618b232d30949d65f6ab78e20951986ae572212bdfbc5b8ece1edf90a3888a4f

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/0; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/1; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/2; canonical SHA-256: b3daae27ea656aa19f7588c4168c4fb4f196e8c9fefcc43277441dce748480d1

BL_SPEC_finite_derivative_p_afd0fcb3ea

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/3; canonical SHA-256: d06f3f33345c2411bed358a411c60015e0aac5d9bef459ddaeb244ad1a2e748c

BL_SPEC_finite_derivative_p_5152685aa1

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/4; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/5; canonical SHA-256: 6af61e8159cd9c8139513834b7046f264636a554c0a04e5128d4d36b8d91766e

BL_SPEC_finite_derivative_p_e013029b9a

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/6; canonical SHA-256: 8ac0420987ed12a4b72805a027b29927aa29e1d2cbdc85e38eb35ec235585da9

BL_SPEC_finite_derivative_p_f2c2e40655

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/constant_dependencies/7; canonical SHA-256: 4f38338bdc6a3ce82d6393be7041d8db7254d007d1159524fda3eed3c34cc503

BL_SPEC_finite_derivative_p_5915d9f603

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: 618b232d30949d65f6ab78e20951986ae572212bdfbc5b8ece1edf90a3888a4f

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/2; canonical SHA-256: b3daae27ea656aa19f7588c4168c4fb4f196e8c9fefcc43277441dce748480d1

BL_SPEC_finite_derivative_p_afd0fcb3ea

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/3; canonical SHA-256: d06f3f33345c2411bed358a411c60015e0aac5d9bef459ddaeb244ad1a2e748c

BL_SPEC_finite_derivative_p_5152685aa1

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/4; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/5; canonical SHA-256: 6af61e8159cd9c8139513834b7046f264636a554c0a04e5128d4d36b8d91766e

BL_SPEC_finite_derivative_p_e013029b9a

#### Native item 7

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/6; canonical SHA-256: 8ac0420987ed12a4b72805a027b29927aa29e1d2cbdc85e38eb35ec235585da9

BL_SPEC_finite_derivative_p_f2c2e40655

#### Native item 8

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/7; canonical SHA-256: 4f38338bdc6a3ce82d6393be7041d8db7254d007d1159524fda3eed3c34cc503

BL_SPEC_finite_derivative_p_5915d9f603

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: e8fe3f328f369b508431d9b8d2e966e0fd35b1c46d93634ec5797c70f9ef459d

Zero/zero ratio is inapplicable on the endpoint overlap. No quantified multiplicative gap is established elsewhere because the lower side is missing.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: 1d0fa451c525d9cd2c6b1c08b051b9a2cecaed79ba46de72ab7c5799a61f8b27

0 on r1 intersect r_zero; no adopted lower bound on r1 outside r_zero.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 5a8c885ca63fac41232c074cb64592d46d1daf926d14c28bd1b6f6a17e49ecc7

Unrestricted-algorithm main-rate lower missing on r1 outside r_zero; sharper upper leads are pending.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: b68d25912d5356b5c82bfa6c24a9d47c58d22213e35b1f9141a559a734f09136

0 on r1 intersect r_zero; O(N+sqrt(N) epsilon^-2), N=n_f+n_g on r1 outside r_zero.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: 5628cbc9aa528cfb9dc03e85f286ace3f1f2cf752d7329f01a8de357e2892e7e

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: dc542e9915ebed8ad9f6199b81e62eb0116e5d06a93ca36166a4280662611f49

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: 7266ec43ce1bf77d4423f142698bd7f3c970788aeec41878512e13e1c3562c32

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: e6845188b1d2aebdf19d13c1613d7a49b5806a7fe336ec775fa182b36719bbc1

empty

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: 7c2e5fb6a9afac277357c6cddca84b2036476b75c4b1436b6202cc3701654d1a

BL_SPEC_finite_derivative__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 6c23c78a0102a9e2da3aa478cd9cf4aecd86c88debd51020733eca2126deb18d

dominated

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: 23d9705de46d4ffbc909be110660e6e135e6bd2a28a231001c451745856efa86

Whenever its original source guard holds, exact zero is at least as strong; no application outside r1.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: cda77ab75642c1d3541be2f7196d92faf8015ef4dd4bef9adbf96339b12e92f1

r1 intersect r_zero; unavailable elsewhere in r_zero

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: 4804d58d5dc31b84284d1eeef658bf5b2fe037912d715cfded3350d741d6c21f

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: 96138fb695c03501531e22d6439b9807ebcadb499348a219bee63137228975d0

BL_SPEC_finite_derivative__main__b_zero_upper

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: b7fe8ce070daa4f532632772bf79724f01520f67254da7c85907d52d8ed0c9c8

Return x0 with exact zero cost.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/bound_uses/2; canonical SHA-256: 56498182f0a6b4df09225c2ae3f4fec9c91133ffa8a492fae032ee16c71feca3

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/adopted_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/bound_id; canonical SHA-256: 6a36d9bbff5cce9e3fdcbd6b4e28bee469c3666bd7e79a32c5dd4930e86c4179

BL_SPEC_finite_derivative__main__b_zero_lower

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/mapping_proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/reason; canonical SHA-256: 600808d12efb24726205acaf66b967aea1bf46b2f3c36991cf64ebb06b9ea2d9

Nonnegative cost certifies the matching endpoint lower value.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/2/validity_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 6616b2d98a16893eddff6baa3da974987c1ee234b3817b5fc8c994dbfcba7bda

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 4680d650555529a295e808d8adb07cbd45e8adfbb2d583e4685da60718546deb

All native structural constraints remain imposed.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 3c5ac1e21aeb21f5a281a5f7b38fb122ef287869530cdae960a14dcd2a0575d5

The threshold is sufficient and inclusive, not a necessary transition.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: f2334d8f8b700faace20d78ae1c09469aa5f04e67fe4d6c95dc53dffc54adeec

L^F_0=0 yields zero throughout epsilon>0 by the same proof.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: a85fe2fce9309814ae19120f1810ca335e5e5b890b78575afe1c95aedcb0f0bc

Output x0 is legal without an inner solution, certificate or initialization calls.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: 618b232d30949d65f6ab78e20951986ae572212bdfbc5b8ece1edf90a3888a4f

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/1; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/2; canonical SHA-256: b3daae27ea656aa19f7588c4168c4fb4f196e8c9fefcc43277441dce748480d1

BL_SPEC_finite_derivative_p_afd0fcb3ea

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/3; canonical SHA-256: d06f3f33345c2411bed358a411c60015e0aac5d9bef459ddaeb244ad1a2e748c

BL_SPEC_finite_derivative_p_5152685aa1

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/4; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/5; canonical SHA-256: 6af61e8159cd9c8139513834b7046f264636a554c0a04e5128d4d36b8d91766e

BL_SPEC_finite_derivative_p_e013029b9a

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/6; canonical SHA-256: 8ac0420987ed12a4b72805a027b29927aa29e1d2cbdc85e38eb35ec235585da9

BL_SPEC_finite_derivative_p_f2c2e40655

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/7; canonical SHA-256: 4f38338bdc6a3ce82d6393be7041d8db7254d007d1159524fda3eed3c34cc503

BL_SPEC_finite_derivative_p_5915d9f603

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: 6321f81fa51fd169fab8041a4ad37e77bdeb24be16c63cb3653b9c9abb46569e

Exact Q*=0; multiplicative ratio inapplicable.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: 6c73df66c82fd85fc970cab6fe4801a1a496c5c786c82dd53915a5f67d11d815

0 throughout r_zero.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: 37a434b236b1f411708c1adeae73c1fad4953ab679efaaf7e671d3472cd483ce

No gap on this sufficient endpoint. The optimal zero-query threshold below it has not been characterized.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: 6c73df66c82fd85fc970cab6fe4801a1a496c5c786c82dd53915a5f67d11d815

0 throughout r_zero.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: c103af4c53665bfbd8d0b60cf3166457331aa83fca6843a5be2248bc7972ab86

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 2c01d2d7cc0c04b9f6cf29d8ec121fbda070017c001ae48f0d85198eaa8410df

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: 3d26520a94c540ec06710a0495263434d8d8bfafcb29bb4ce6167b0b021af2f4

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 148efc3d671576b72ad15084272bde671155f870452c2f69df80d366ea9ad530

small_nonzero_unresolved

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: 47f702a1f443b5f7acde2d21d8fa9bff4e85936058b10acbbcc1dabf3ac90c6f

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 077a0ff1cd322c38d67deaaa620a99888c1077b1cbfa1fa49361142707c47953

Only the retained SRBA upper is adopted; a main-rate lower is missing from this record.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: 2d431bcff4272e9698944c83c0678003561c1e610e3dc2f89440709e593dc0d7

r1 AND NOT r_zero

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

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: d9d4b74588caff9210929c92def655fcebdf532f4323f3903017cb3b059f16ff

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: b19e946a5e3fa96765ce90cf12c7f717d52bea0d26fb13b62539189cfe6d7430

small_zero_overlap

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: c20406c284d0402187f439c9fee257d8f34423f2a86008c1c7c51cb3ff448c1d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 944530f9fa536f514ec35d1d5e53a7c77c9328313f1b61c32a2cf5d364bb4efd

Possibly empty for fixed structural budgets; if present, Q*=0 and ratios are inapplicable.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: 0ff30775cd1f95a497f4658c6e74565ae12c9d5477111ec93777046700362bbc

r1 AND r_zero

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 5f52e1a746be4864c8077692000ab2cfb95fb0bc8be92abca2902db787ba8b4f

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 1af4a6381cfbe5651158cf58f36c3b91b64c79cad829450193c886a1d33dc4bc

zero_outside_small

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: c20406c284d0402187f439c9fee257d8f34423f2a86008c1c7c51cb3ff448c1d

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids/0; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: f6f2a85630ad368fd149388882d7c2b419083af6b0cf791dc6a8cacae31065cb

New exact zero endpoint within the full native domain, independent of the SRBA source threshold.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: 7249c7507af19f4498a6d9e73ca8bd9a103a7f0bc459a82f435be37614abbc78

r_zero AND NOT r1

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 4

Native pointer: /joint_analysis/domain_map/cells/3; canonical SHA-256: e4b89da038183ebaf7fde44308f83baf22a4c63e6fb40ee1ae40a2e1f2b85858

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/3/cell_id; canonical SHA-256: 9b540bde6a9b006dd1c8728a35fa95fd45a474dd62a7693fe0180e94ea2fcaf2

residual_unassessed

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/3/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/3/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/3/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/3/note; canonical SHA-256: 6ffad17ae77503614f3b5d36e9b5978174aa4e97be5780a6b2b270fdcc1714ed

No scientific assessment of best bounds or positive complexity in this complement.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/3/predicate; canonical SHA-256: 72563e5ced30206747da19962cb2f3a4950288f8f764341d54fbca04e4d4003d

Full declared domain AND NOT r1 AND NOT r_zero

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/3/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/3/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/3/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: 335b08f878f3d2eb2cf958d1552741c8c3f0e299d19a0dbf7af746336648c6a3

Within the full native domain, the four Boolean cells of membership in r1 and r_zero are disjoint and cover it, allowing empty cells. r1 is retained symbolically; no numerical small-accuracy threshold is inferred.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: 18993ebd43a592f042c91e50d93ac5f5a0346ef605d9659004313252b585806f

Outside (r1 union r_zero), represented explicitly by residual_unassessed.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 88d94f82919f2c0a697215c0e46239a18affbdac5eddc6a1d17f7427fb22dfd7

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: a134cb30e5a38ccf62ee11148d9dcfb2812d8e8e71b5677475e5bddfa9241486

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: fd09139d6f2213b01f1926802ca5a0995c089f337499ad15b243ee6d1beb1dd4

The stated sufficient activation inequality is exact and inclusive. It is not a sharp phase transition and does not advance the small-accuracy main rate.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/0/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: 6eea65a6e60be51a5c0d4e51792461553c5bd5d0a2fa01ad0b02f86b94cbf097

Newly closed r_zero outside r1; upper tightened and endpoint closed on r1 intersect r_zero if nonempty.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: ccdf4c88a6fb756f2473e77460e154f78636fee11cf280852b6f42e3ba49d773

zero_query_endpoint

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: 7fc74229c2d145a21cd3d76d8f6f575bd23c6c295bc6f69a1aa23179a6906e00

Q*=0 on r_zero; on r1 outside r_zero retain upper O(N+sqrt(N) epsilon^-2), N=n_f+n_g and missing lower.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 5879e0bf1981e93c58c7b589bc68da13f868e148bfbb891819b2275d782cc8d2

On r1: upper O(N+sqrt(N) epsilon^-2), N=n_f+n_g, lower missing. Outside r1: no registered comparison.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: 1344d199cff91da38232717353c58f45bdf8f9135063ee2c3f42f4b202070177

r1 outside r_zero; all regions outside r1 union r_zero remain unassessed.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: f4643213cfd610de1646216a02850b9847afd558f5486b99a59fde7cd2ba449c

Return public x0; proof gives ||grad Phi(x0)||<=L^F_0 L^G_1/mu and nonnegative response counts force Q*=0.

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 02d88cc9d1dfc47072117af902ae6d7cfdcec08666fc808133e8b49a811e8492

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: ddd6cc22253327b18c823be7cf33657067c4138140dbf18e65db0c44c69f3640

First joint annotation preserves quantity metadata and definitions. The actual endpoint edits are justified separately by the exact baseline derivation.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 47f702a1f443b5f7acde2d21d8fa9bff4e85936058b10acbbcc1dabf3ac90c6f

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: 87bb047ff9493bb70f20d12d9532dbd2220005730c50476e9ef58170e69a7323

joint_first_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: aa357284d22d908ed2a0788e2abefecb3ba70318ca1e8eac1374ccc868b051ae

None from presentation alone.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: 657912d2c47a6f5720e1a7e873779cb126568d0c2e25d239fa7708b3427ff094

Same SRBA branch retained on its guard; the separate endpoint finding supports every scientific alteration.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 4372bcb05a7cfd21b25abd97c70da6d717b6c1dd99cb03348e2021622e5a48b9

Single guarded SRBA upper O(N+sqrt(N) epsilon^-2), N=n_f+n_g with missing lower.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: e949f49eecc28f98c2ca912228b370e1968ec3c357a94b40ab1a94ad358dbbf0

All conditionally retained premises and SRBA's source validity guard.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 3056d68ed14abf936476cae06aa906123d38bcfeea5105de7c531deed8eb7b39

The unchanged native small-accuracy predicate of BL_SPEC_finite_derivative__main__r1

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: bdb6925289476d5e6457ff3c9663e546386eec94fdc915477ce036dded41413e

The sole baseline compatible bound is explicitly accounted for; target tracks epsilon and native derived N uniformly over decompositions and dimensions.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: 6f5b21a2bdc159ba21ca4f50061cf659ef793f6a70cf948b9a9a92b6df2cf441

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 9e5e1a561a263084b10376b38070350159e00fcf9c144d445d0f1d3cee39ef87

A lower bound for that larger class is not a target lower bound. Additional target HVP/JVP access also needs simulation, although its quadratic lower families would make those replies known. No such bound is adopted.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 47f702a1f443b5f7acde2d21d8fa9bff4e85936058b10acbbcc1dabf3ac90c6f

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: bdf2a533911d29b286edf9098d231a406fba31cee298d777f488b37b3e079bcf

recent_first_order_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 50446632d7eed558fb7d733ed5a6dd99640a04b4464028aab864dc38ad6db49e

None established.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: ca509749b04d207766d64f6862c73d865c0c45f13008d1f9d40cf7ca5789486a

No adopted change from arXiv:2610.24538v1.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 0198d24b3ea225d2ce2235c19402893be018586912129850ffa75edd8db56097

Retained O(N+sqrt(N) epsilon^-2), N=n_f+n_g; no unrestricted main lower.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 0cde35fe1463709e637acd00cdd9264f6db0d80e4e0e8f569722177209b0a235

All active target envelopes.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: 139b30f9f3e0a5df84b40b318c5dad7dbc56ad5f9e031403b3b7b078ca83385c

Read source Assumptions 1-3, Theorem 5.1, Proposition 3.2 and Appendix F; target applicability is not established for its lower families.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: 6dfe3785f55d55848825398ad23bcb63111b9f6e418d039ff649e1d967bef80b

The upper has dimension-dependent logarithms; the lower proof uses a larger component class, including C1 Huber functions and an unbounded-gradient quadratic upper needle.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 8b43992ca1759f1be55166e1b880460db0446031f9c3356644a07ac0334d42f4

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 64bc32c90c46cbea0a89052356bedac4507e6c0a23d73abbf99fa8aab3a312cb

The source lower theorem does not apply to every randomized adaptive measurable algorithm allowed by the target. Its upper corollary is already represented, with squared tolerance converted to epsilon^2.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: 47f702a1f443b5f7acde2d21d8fa9bff4e85936058b10acbbcc1dabf3ac90c6f

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: eaece403bc086ef0fe8e681e8d36c0eab739a2204d11773ddb273b7bf84f228c

srba_restricted_lower_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 45f1160f7272623c213cff5e47fa967191c639d6175a43417f9298408bb4eb84

None.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: e61c51c59aac7c6a685782fee13e263a0b28bb890963c549e8fc04cd08b90ad7

No additional bound adopted from the read source.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 49aa600a47f0929b769e8645ec65f34fe660ef7e2f652c59c208610d262a392d

Guarded SRBA upper O(N+sqrt(N) epsilon^-2), unrestricted-algorithm lower missing.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: 0bf3bb5e0cff84a2e534a0afc38c312c635c7acf8146e2adb2b6a65772c66242

All native envelopes except the separately proved zero endpoint.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: fc766490e3c1787e3f01789e987c25bf169b8ee548c5f00be4c9837ebf4edd90

Source Section 4, Definition 4.2 and Theorem 2: linear bilevel algorithms on a larger upper-function class.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: 031ccb64b29d947c18a05fa0d08d6fafa4e6e7d94959ba861d2e0a6c9cf51d65

The source enforces span restrictions absent from the fixed target; lower-bound quantifiers cannot be enlarged by annotation.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: b6373f49968b8dc9558ae64149ad9325577e8b3598f9a1c546df16c23e55029f

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 82ad21831e5823d21add25baf8dbc12b0bbe0afc6c9339aedbb1202444ba4cfb

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 04399ac216f1992493dedfbc3376696fb20a0708e26ded61bb2b9dfcae73848d

curated_feedback_BL_SPEC_finite_derivative_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: 81c5aa329542b3489c46f8ebd949069d35530772f4c59b4e32d9cb22950e40bd

The complete declared parameter domain: epsilon>0; n_f,n_g,d_x,d_y positive integers; N=n_f+n_g; fixed admissible public derivative budgets, mu>0 and V_0>=0. Dimensions are supremized, not fixed in hidden constants.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: afa974bfb0c85caf22b59926e47138bfd790272cf11c8b795429f2fb959fea05

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: f9fb771770ba3efb854cf3b144d8b5ea113a32794f5c2fe155a04fd7a658633b

curated_feedback_BL_SPEC_finite_derivative_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

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

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: 81c5aa329542b3489c46f8ebd949069d35530772f4c59b4e32d9cb22950e40bd

The complete declared parameter domain: epsilon>0; n_f,n_g,d_x,d_y positive integers; N=n_f+n_g; fixed admissible public derivative budgets, mu>0 and V_0>=0. Dimensions are supremized, not fixed in hidden constants.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 3c1f51ccf3462b1aaedb7eecced1eab0991743182ad013099ce62402caa5b06d

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 333de6e2f5b249a2d9d8b247ebe7e3b36c1312d9a3425526b69e3ec98c9ffea4

Read and assess arXiv:2306.14853v5 (2026-05-25), especially higher-smoothness acceleration and its primitive-call, output, dimension and fixed-budget conversions; it is unrelated to the proved endpoint.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: 7ddb3445aa0fb135d79bfcac9c7314a7e33f75fcab82322de1df1bd1e5e704da

Main-rate lower bounds for the target's globally value/gradient/Hessian-Lipschitz upper components and unrestricted randomized algorithms remain unassembled; the two read source lower bounds do not establish them.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: f048c4b99a9801f261121d133fc23966b0b734f645e7130c6d2836adfbdbff10

Assess sharper small-accuracy upper branches, including the large-N comparison noted by SRBA, without assuming bounded component-gradient variance absent from the contract.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: d1af5d5cf3e2c29fc4b9ba0ddcc61a0531936a233a6fd79726bfaffc3a7e6a2c

The non-endpoint complement outside r1 is explicitly unassessed; no absence or open-problem claim is made.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: 100bdbfe56035f5d6b6db6e61ce98ab90048de9016b465d8d8efdd130172f4c0

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: 5e0aa2d503a274777f1ce365a0ddd24503df5116f4d5299c26b3cf0b64483559

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: 7c2e5fb6a9afac277357c6cddca84b2036476b75c4b1436b6202cc3701654d1a

BL_SPEC_finite_derivative__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: 817503b6b275a7b4c5b44cb3370759887848b36eb6c176dd90915c1a1ea87aff

Native squared-gradient tolerance eta=epsilon^2; N=n_f+n_g; each joint tuple uses at most four primitive calls. No new scientific certification.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 3056d68ed14abf936476cae06aa906123d38bcfeea5105de7c531deed8eb7b39

The unchanged native small-accuracy predicate of BL_SPEC_finite_derivative__main__r1

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: caa6791e16c52736e3bcc73a8e9a8f66e7c00eedb7bd908b3acd50de45e0a469

Frozen /bounds/0 and /evidence/0; Corollary 3.6. Unchanged premise retained conditionally.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 35a577344dd98c4b42f67da7138cd24eae38a016924ce3af2d8abb53f0e8019b

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: f5ee094d65439f6dd7e0af82b500a4845a59f004296066ff442267d8de8ce3ef

BL_SRC_dagreou2024

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: bcddef9fe55f9e1ba2d0e8f376cdcd5c8b3211ca88f84390613f85705805b65e

r1 outside r_zero (zero dominates on overlap)

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: 226f5238d426bfb98238eedad03a01b1d4da32c5b3f3ac7b56e58642609b37da

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: 96138fb695c03501531e22d6439b9807ebcadb499348a219bee63137228975d0

BL_SPEC_finite_derivative__main__b_zero_upper

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: 5dd0c5c453b2aef3b8d2be23220f2fea1a50abfa4318d3533d139d34d1b5857c

Use the native hypergradient row operator [I,-D C^-1], whose norm is at most L^G_1/mu under the frozen Euclidean and full-Hessian bounds. Return public x0 with all four response counts zero.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 81c5aa329542b3489c46f8ebd949069d35530772f4c59b4e32d9cb22950e40bd

The complete declared parameter domain: epsilon>0; n_f,n_g,d_x,d_y positive integers; N=n_f+n_g; fixed admissible public derivative budgets, mu>0 and V_0>=0. Dimensions are supremized, not fixed in hidden constants.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 9aa4ef32ab3109f845c283bd20c0f17c9e6d826e57f62afdb32e90caba6d8cce

Frozen /common_specification, /parameters, /views and /quantities/0; full new proof in BL_SPEC_finite_derivative__main__p_zero

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native item 3

Native pointer: /joint_analysis/provenance/2; canonical SHA-256: 6de17287b3b0f5720a4bd30a81a4690eb97550dc66356177fc07409f5b285d22

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/2/bound_id; canonical SHA-256: 6a36d9bbff5cce9e3fdcbd6b4e28bee469c3666bd7e79a32c5dd4930e86c4179

BL_SPEC_finite_derivative__main__b_zero_lower

#### Native field: mapping

Native pointer: /joint_analysis/provenance/2/mapping; canonical SHA-256: 0d97cc8f661aa9803e87d07522634c1adc47aac14df89c192745abfec2c37054

Restrict nonnegative minimax cost to the endpoint; combine with the matching zero upper.

#### Native field: origin

Native pointer: /joint_analysis/provenance/2/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/2/proof_refs; canonical SHA-256: b1baea19a3b0fcbf370be5d5a9ca71c78de31593821aae6a019069b3e7b09e03

#### Native item 1

Native pointer: /joint_analysis/provenance/2/proof_refs/0; canonical SHA-256: 06fa8b468165ba0446c78252321991035ee6870fe13fb4f7931d2f1101853301

BL_SPEC_finite_derivative__main__p_zero

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/2/source_domain; canonical SHA-256: 81c5aa329542b3489c46f8ebd949069d35530772f4c59b4e32d9cb22950e40bd

The complete declared parameter domain: epsilon>0; n_f,n_g,d_x,d_y positive integers; N=n_f+n_g; fixed admissible public derivative budgets, mu>0 and V_0>=0. Dimensions are supremized, not fixed in hidden constants.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/2/source_locator; canonical SHA-256: b88f329258a426fe815407e242081011b092a9c994422a1b369a522ecd6a6f4a

Frozen nonnegative quantity and unit response cost rules; BL_SPEC_finite_derivative__main__p_zero

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/2/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/2/target_domain; canonical SHA-256: cc08a97246115395e7c42c9edfd840b283c5f7a34ff2d8696a1c53c4eabb4987

Full declared domain AND epsilon >= L^F_0 L^G_1 / mu

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: dc3d09d6abeb5fbee20de2a83c161c899ff527c7ffcff74ec81e923872344dcc

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

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

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: cece53ca95ba0ea60784e8ec9e3693005b13faf614875d2aacd7d2b1beccdc31

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 6339593fbdb31d76852c623e04384596f22503c9acbbb3793b980db75d44af0f

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: f731475b145899ca3503c731d7ce93077db89814c332fd2217601fb6599650a6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: 7c2e5fb6a9afac277357c6cddca84b2036476b75c4b1436b6202cc3701654d1a

BL_SPEC_finite_derivative__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: 6a36d9bbff5cce9e3fdcbd6b4e28bee469c3666bd7e79a32c5dd4930e86c4179

BL_SPEC_finite_derivative__main__b_zero_lower

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/2; canonical SHA-256: 96138fb695c03501531e22d6439b9807ebcadb499348a219bee63137228975d0

BL_SPEC_finite_derivative__main__b_zero_upper

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 47f702a1f443b5f7acde2d21d8fa9bff4e85936058b10acbbcc1dabf3ac90c6f

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: ea414675f24e0655ead545e0f46537be257f7b1b8b6009e54c0338b1573809cf

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa

Native value (boolean): false

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: b034a9bb30ea7c7c9704b620dc3d27844f8f795e54940ec8dac69c8b5f47de70

Conditionally retain the exact native compatible-bound ledger for this comparison, including every listed bound's disposition and guard. This migration does not recertify retained source theorems. Any new local consequence is separately proved in the native candidate.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: f731475b145899ca3503c731d7ce93077db89814c332fd2217601fb6599650a6

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: 7c2e5fb6a9afac277357c6cddca84b2036476b75c4b1436b6202cc3701654d1a

BL_SPEC_finite_derivative__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: 6a36d9bbff5cce9e3fdcbd6b4e28bee469c3666bd7e79a32c5dd4930e86c4179

BL_SPEC_finite_derivative__main__b_zero_lower

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/2; canonical SHA-256: 96138fb695c03501531e22d6439b9807ebcadb499348a219bee63137228975d0

BL_SPEC_finite_derivative__main__b_zero_upper

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: c20406c284d0402187f439c9fee257d8f34423f2a86008c1c7c51cb3ff448c1d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: ff69e1362be4b8aafae4ca7981d41de80f4627fe7513a2da4bfba206a42bca82

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: 5fb9e42df502b1d9454b377a6c5fec9fc66bd3fff8ec90fca2422a6d85a7bd4e

retained-material-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 333de6e2f5b249a2d9d8b247ebe7e3b36c1312d9a3425526b69e3ec98c9ffea4

Read and assess arXiv:2306.14853v5 (2026-05-25), especially higher-smoothness acceleration and its primitive-call, output, dimension and fixed-budget conversions; it is unrelated to the proved endpoint.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: 42aaa94471cf08d72834a627075187a7b03b401fc6699ea84c1e04c791707e86

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: d5551f8177575ae403ffcc792a53d49e993aeb3d2f2735854a5b9075f9cd66e8

retained-material-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: 7ddb3445aa0fb135d79bfcac9c7314a7e33f75fcab82322de1df1bd1e5e704da

Main-rate lower bounds for the target's globally value/gradient/Hessian-Lipschitz upper components and unrestricted randomized algorithms remain unassembled; the two read source lower bounds do not establish them.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: e21fcb9d3adec72545bfff02f7c2d7e5fe3a85f445c9bdaa6971928704c64af6

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 188c1e84832880eef4caaf4bcf2389b38b1aa9347aad1f495fc45c772e316996

retained-material-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: f048c4b99a9801f261121d133fc23966b0b734f645e7130c6d2836adfbdbff10

Assess sharper small-accuracy upper branches, including the large-N comparison noted by SRBA, without assuming bounded component-gradient variance absent from the contract.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: bbe42e6b48167b2fb78b13bc579099be021839eaabac4509590ec5b5fc02b593

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 13b33126af2b17e2ed543e3e9293f8d41c7ed03431a6a0c724436a461669191d

retained-material-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: d1af5d5cf3e2c29fc4b9ba0ddcc61a0531936a233a6fd79726bfaffc3a7e6a2c

The non-endpoint complement outside r1 is explicitly unassessed; no absence or open-problem claim is made.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 233b99ee17e5ceb468ab23e1dc2c2c79f42e83c23f7ddd3549d855978ecad0f9

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

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 085dd92d11e70d58906128ca46ba0b6062edccab8589fe339b858a6d24493aaa

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 70f11e8b911f2a7ded3f5bc5d7cb5d383f60a70f1a4b060b900157ac8b4e79a2

BL_SPEC_finite_derivative__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: ce129def391c08c8d2a4c4dba1ef3663a09f302cf6e3ff4de48d5edd660a91fb

BL_SPEC_finite_derivative__main__c_zero

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

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

Native pointer: /joint_analysis/target; canonical SHA-256: f130b98638b1ede4889370cc2cf6e3cdbfabf942040d95d4e3a3b6afd728d3e6

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 618b232d30949d65f6ab78e20951986ae572212bdfbc5b8ece1edf90a3888a4f

#### Native item 1

Native pointer: /joint_analysis/target/allowed_constant_dependencies/0; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native item 2

Native pointer: /joint_analysis/target/allowed_constant_dependencies/1; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native item 3

Native pointer: /joint_analysis/target/allowed_constant_dependencies/2; canonical SHA-256: b3daae27ea656aa19f7588c4168c4fb4f196e8c9fefcc43277441dce748480d1

BL_SPEC_finite_derivative_p_afd0fcb3ea

#### Native item 4

Native pointer: /joint_analysis/target/allowed_constant_dependencies/3; canonical SHA-256: d06f3f33345c2411bed358a411c60015e0aac5d9bef459ddaeb244ad1a2e748c

BL_SPEC_finite_derivative_p_5152685aa1

#### Native item 5

Native pointer: /joint_analysis/target/allowed_constant_dependencies/4; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native item 6

Native pointer: /joint_analysis/target/allowed_constant_dependencies/5; canonical SHA-256: 6af61e8159cd9c8139513834b7046f264636a554c0a04e5128d4d36b8d91766e

BL_SPEC_finite_derivative_p_e013029b9a

#### Native item 7

Native pointer: /joint_analysis/target/allowed_constant_dependencies/6; canonical SHA-256: 8ac0420987ed12a4b72805a027b29927aa29e1d2cbdc85e38eb35ec235585da9

BL_SPEC_finite_derivative_p_f2c2e40655

#### Native item 8

Native pointer: /joint_analysis/target/allowed_constant_dependencies/7; canonical SHA-256: 4f38338bdc6a3ce82d6393be7041d8db7254d007d1159524fda3eed3c34cc503

BL_SPEC_finite_derivative_p_5915d9f603

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: fe8f1c955fd933f5e225f175e38edb81b7db1ff5154b56487500d657bb4c25e0

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: d32bd71612d21ac63b68d46032bd16a12332f66ea33977974f7dd53b37dda7ae

/regimes/1

#### Native item 7

Native pointer: /joint_analysis/target/contract_refs/6; canonical SHA-256: b44a2fd7032b4504a0ddaadb1add048a3dc61965eb6a56b6915d532318c5217f

/symbols/5

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 639a16ed1ddbf6f1cc654088db4750ecb7026c62a2938e66b4023ab0b0d05ae5

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: 07f86c1eda76e0700ae44e9f6b9f1d88249746e121fe5b8b52f84d52e318ce25

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 0ad3fc3d8ba4ed44adcaa98e49dc5b1ab5f91b4d9cd79167882e9ae5b7436fc9

Positive, fixed; admissible budgets require mu<=L^G_1.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: 7886bfd08bf6df84f6d583da4fc47ebed064df4c2c7a72047b2aef853851749f

BL_SPEC_finite_derivative_p_efcabfd5ff

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: 62e46f6d20e4aaeeb75ee133df9a180a003490fadecfc423fd6877209c64e4a4

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: 0aa3d0b7e28e92b193f6612caa7454d176230a1557f436e1a51b03a3f103d361

BL_SPEC_finite_derivative_p_ed05e891f8

#### Native item 3

Native pointer: /joint_analysis/target/fixed_parameters/2; canonical SHA-256: 88cb7f59243b72e908f71fe4ef24288bcde32952f2e10050d3ee4807f112f920

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/2/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/2/parameter_ref; canonical SHA-256: b3daae27ea656aa19f7588c4168c4fb4f196e8c9fefcc43277441dce748480d1

BL_SPEC_finite_derivative_p_afd0fcb3ea

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/2/symbol; canonical SHA-256: b3daae27ea656aa19f7588c4168c4fb4f196e8c9fefcc43277441dce748480d1

BL_SPEC_finite_derivative_p_afd0fcb3ea

#### Native item 4

Native pointer: /joint_analysis/target/fixed_parameters/3; canonical SHA-256: 8e66422e8d363525fb8f6fbb452ca0b1eacb60f6f3db15924f546b00c2c8d6af

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/3/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/3/parameter_ref; canonical SHA-256: d06f3f33345c2411bed358a411c60015e0aac5d9bef459ddaeb244ad1a2e748c

BL_SPEC_finite_derivative_p_5152685aa1

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/3/symbol; canonical SHA-256: d06f3f33345c2411bed358a411c60015e0aac5d9bef459ddaeb244ad1a2e748c

BL_SPEC_finite_derivative_p_5152685aa1

#### Native item 5

Native pointer: /joint_analysis/target/fixed_parameters/4; canonical SHA-256: b55e6acf17b15efae33b172cb4527cca77d4667e89abda83135503743688ccc3

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/4/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/4/parameter_ref; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/4/symbol; canonical SHA-256: 425cbdffdd3134e7660bf8440193ef47f6e600e41e046661ec7c97d80999b06e

BL_SPEC_finite_derivative_p_5d43efa8ba

#### Native item 6

Native pointer: /joint_analysis/target/fixed_parameters/5; canonical SHA-256: d771a079e168ba963b6288661b25184f4d05625210de576d0285d12a07daad42

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/5/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/5/parameter_ref; canonical SHA-256: 6af61e8159cd9c8139513834b7046f264636a554c0a04e5128d4d36b8d91766e

BL_SPEC_finite_derivative_p_e013029b9a

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/5/symbol; canonical SHA-256: 6af61e8159cd9c8139513834b7046f264636a554c0a04e5128d4d36b8d91766e

BL_SPEC_finite_derivative_p_e013029b9a

#### Native item 7

Native pointer: /joint_analysis/target/fixed_parameters/6; canonical SHA-256: 24367c3a07225903eaec620f37e0192948bfe809423e5b0fefce8c755477d0b0

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/6/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/6/parameter_ref; canonical SHA-256: 8ac0420987ed12a4b72805a027b29927aa29e1d2cbdc85e38eb35ec235585da9

BL_SPEC_finite_derivative_p_f2c2e40655

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/6/symbol; canonical SHA-256: 8ac0420987ed12a4b72805a027b29927aa29e1d2cbdc85e38eb35ec235585da9

BL_SPEC_finite_derivative_p_f2c2e40655

#### Native item 8

Native pointer: /joint_analysis/target/fixed_parameters/7; canonical SHA-256: e528becd6b82c56028d758f67cff8088752864bd424fe2cdbf0833371acc0526

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/7/domain; canonical SHA-256: f62c4f6d71852e1537cc590f269dd4e00ad9d178ac76e7e66b002209ad548bf8

Finite nonnegative public budget, fixed independently of epsilon and component counts.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/7/parameter_ref; canonical SHA-256: 4f38338bdc6a3ce82d6393be7041d8db7254d007d1159524fda3eed3c34cc503

BL_SPEC_finite_derivative_p_5915d9f603

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/7/symbol; canonical SHA-256: 4f38338bdc6a3ce82d6393be7041d8db7254d007d1159524fda3eed3c34cc503

BL_SPEC_finite_derivative_p_5915d9f603

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: 81c5aa329542b3489c46f8ebd949069d35530772f4c59b4e32d9cb22950e40bd

The complete declared parameter domain: epsilon>0; n_f,n_g,d_x,d_y positive integers; N=n_f+n_g; fixed admissible public derivative budgets, mu>0 and V_0>=0. Dimensions are supremized, not fixed in hidden constants.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 14ea7da1ac295ef5b60b4bb46ab357f4188184c1bb7d96ae0d8d53157bce0ecd

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 2d45e1738e78eda2df6560560b3cba22fcebbe6ead8ee7fc777e824335e230e5

BL_SPEC_finite_derivative_p_0d1c5067b5

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 6dc57b3467bf906e2b1e2a8a1ead3850dd1e6d4e6df28221d50c826776f7d673

BL_SPEC_finite_derivative_p_6cb2ff880d

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 3ccbba4efaf29c6329f2ba8b5f9c3560f2da5d52f92166c000881fe49e9687f8

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 2d45e1738e78eda2df6560560b3cba22fcebbe6ead8ee7fc777e824335e230e5

BL_SPEC_finite_derivative_p_0d1c5067b5

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 6dc57b3467bf906e2b1e2a8a1ead3850dd1e6d4e6df28221d50c826776f7d673

BL_SPEC_finite_derivative_p_6cb2ff880d

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 7a9dda625ab2d8059c25eca0a2274fb4ec8c57b658cd4727aa388fcfe4a855d6

BL_SPEC_finite_derivative_p_9e69b29b82

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: bf460f6b2083793189c15cc6775ab8d0c5853e62c3e38d4ffd9fdf7051d204a3

BL_SPEC_finite_derivative_p_b117c65560

#### Native item 5

Native pointer: /joint_analysis/target/uniform_in/4; canonical SHA-256: 5197927e2deeb6e5bf99c37da9b40bc446f5515001237674e6dd78d37606b02c

BL_SPEC_finite_derivative_p_a136776370

#### Native item 6

Native pointer: /joint_analysis/target/uniform_in/5; canonical SHA-256: b57b4f7eb74da68ac7257a4b2dd3293559cdd43331fa768fd38bfb07a8dd1ad0

BL_SPEC_finite_derivative_p_dc5f6d3bad

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] Mathieu Dagréou; Thomas Moreau; Samuel Vaiter; Pierre Ablin. A Lower Bound and a Near-Optimal Algorithm for Bilevel Empirical Risk Minimization. 2024. AISTATS 2024, PMLR 238.

https://proceedings.mlr.press/v238/dagreou24a/dagreou24a.pdf
