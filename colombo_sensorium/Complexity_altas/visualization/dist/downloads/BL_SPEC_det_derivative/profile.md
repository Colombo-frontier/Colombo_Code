# Strongly convex lower levels: exact gradients and derivative–vector products.

**Setting ID.** `BL_SPEC_det_derivative`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; initialization: Initial inverse certificate; smoothness: Hessian or cross derivative lipschitz; smoothness: Lipschitz gradient; smoothness: Value lipschitz

**ORACLE tags.** feedback quality: Exact; interface family: Derivative vector; operation: Cross derivative vector product; operation: Hessian vector product; operation: Partial gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; measure: N hvp; measure: N jvp; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The population full gradient $\nabla f=(\nabla_x f,\nabla_y f)$ is globally $L$-Lipschitz in $(x,y)$. Convexity of $f$ is not required.

The population full gradient $\nabla g=(\nabla_x g,\nabla_y g)$ is globally $L$-Lipschitz in $(x,y)$.

The objective $\Phi$ has a finite lower bound. A point $x_0$ is given and satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$. Convexity or existence of a global minimizer of $\Phi$ is not required.

The initial point $(x_0,y_0)$ and bound $\|y_0-y^*(x_0)\|\le R_0$ are given. This is an initialization budget, not a requirement that the oracle return $y^*$.

The function $f$ is jointly $M$-Lipschitz in the full variable $(x,y)$. This budget is recorded as $C_f=M$ and therefore bounds the full gradient. It is stronger than a bound only on $f_y$.

The function $g_{xy}$ is $\tau$-Lipschitz in $(x,y)$, and $g_{yy}$ is $\rho$-Lipschitz. These budgets are specified separately and are not combined into an unspecified common constant.

AID initialization also supplies $v_0$ and fixes the public upper bound $D_0\ge\|y_0-y^*(x_0)\|^2+\|v_0-v^*(x_0)\|^2$. It does not supply $v^*$ or a free inverse matrix.

The adjoint solution is $v^*(x)=g_{yy}(x,y^*(x))^{-1}\nabla_yf(x,y^*(x))$. It is a hidden mathematical object; the input supplies the initial value $v_0$ and error bound $D_0$.

### Oracle interface

Public inputs include dimension, target accuracy, quantitative model budgets, and initial points. Functions, lower-level optimizers, and the reduced objective are hidden.

Upper-level partial gradient: $(x,y,b)\mapsto\nabla_b f(x,y)$, where $b\in\{x,y\}$. Selecting the x-block returns a vector in $\mathbb R^{d_x}$; selecting the y-block returns a vector in $\mathbb R^{d_y}$. One call returns only the selected block.

The lower-level partial gradient is $(x,y,b)\mapsto\nabla_b g(x,y)$, with block selection and output space as specified above.

Cross-derivative–vector products take the form $(x,y,v)\mapsto g_{xy}(x,y)v\in\mathbb R^{d_x}$, where $v\in\mathbb R^{d_y}$.

Hessian-vector product: $(x,y,v)\mapsto g_{yy}(x,y)v\in\mathbb R^{d_y}$, where $v\in\mathbb R^{d_y}$.

All four response types are exact, and query points and directions may be adaptive. Every Hessian–vector product used by internal conjugate gradients is charged. Exact lower-level solutions and matrix inverses are not oracle primitives.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Retain joint budget $(N_{\nabla f},N_{\nabla g},N_J,N_H)$ for f partial gradients, g partial gradients, cross-derivative products, and Hessian-vector products. Each response increments its corresponding coordinate; two partial gradients cost two calls.

Initialization oracle calls count toward the total. A finite initialization bound is an instance-class assumption, not free access to an inner solver.

The budget is a fixed worst-case cap on every execution path; every actual response within a batch is counted.

Internal processing of available information is free. Comparisons use the explicitly specified scalarization or resource vector. Different resources without given weights cannot be assembled coordinatewise from separate algorithms.

### Algorithm views and success guarantees

Algorithms may use private randomness. Queries, stopping, and postprocessing may be arbitrary measurable functions of the transcript. The output may be unqueried, a random selection of a past point, or an admissible average. No linear-span or zero-respecting restriction is imposed. Queries are sequential; each actual response in a parallel batch is charged separately. Arithmetic, linear algebra, and storage using received data are uncharged. Internal operations, memory, and communication are not tracked by this quantity.

The algorithm depends only on public inputs and the query transcript. For every admissible instance require $\mathbb E\|\nabla\Phi(\widehat x)\|_2^2\le\varepsilon^2$. The oracle is exact, so expectation is over private algorithmic randomness, including any random output-index selection. The query cap must hold on every execution path.

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

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu>0$.

$C_f$: The upper function’s Lipschitz budget in the entire joint variable, denoted M in the source. **Domain:** $C_f=M\ge0$.

$\|\nabla f(x,y)\|\le M=C_f$

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: Joint Lipschitz upper bound for the lower-variable Hessian block $g_{yy}$. **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: Public initial lower-level distance bound **Domain:** $R_0\ge0$.

$\|y_0-y^*(x_0)\|\le R_0$

$\kappa$: Lower-level condition number **Domain:** $\kappa\ge1$.

$\kappa=L/\mu$

$\tau$: Joint-variable Lipschitz upper bound for the lower cross-Hessian block. **Domain:** $\tau\ge0$.

$D_0$: Public bound on the sum of the squared initial lower-level distance and squared adjoint-solution distance **Domain:** $D_0\ge0$.

$\|y_0-y^*(x_0)\|^2+\|v_0-v^*(x_0)\|^2\le D_0$

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$v$: The algorithm-selected direction for a derivative–vector query. **Domain:** $v\in\mathbb R^{d_y}$.

$M$: Lipschitz budget used in the source for the joint upper-level function value **Domain:** $M=C_f$.

$v_0$: Public initial vector for the adjoint linear system **Domain:** $v_0\in\mathbb R^{d_y}$.

$v^*$: Solution of the adjoint linear system at the exact lower-level solution **Domain:** $v^*(x)\in\mathbb R^{d_y}$.

$v^*(x)=g_{yy}(x,y^*(x))^{-1}\nabla_yf(x,y^*(x))$

$K,x_k,R$: The outer iteration count, kth outer point, and independent uniform output index. **Domain:** $K\ge1,\ 0\le k<K,\ R\sim\operatorname{Unif}\{0,\ldots,K-1\}$.

$\eta_{\rm src}$: Squared-gradient tolerance from the source, renamed to distinguish it from this profile's norm tolerance **Domain:** $\eta_{\rm src}=\varepsilon^2$.

$\mathcal C(\varepsilon),\mathbf N,b,\preceq$: Set of joint budgets attaining the tolerance, call vector, four-dimensional integer budget, and coordinatewise inequalities. **Domain:** $\mathbf N,b\in\mathbb N_0^4$.

$\mathfrak A_{\rm spec},\mathfrak A_\varepsilon,\mathcal A,I,\mathcal O,\omega$: The admissible algorithm class, its accuracy-achieving subclass, algorithm, instance, oracle law, and execution randomness define the quantifiers for the joint attainable set.

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_J$: The number of lower cross-derivative–vector responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_H$: Number of lower-level Hessian-vector product responses **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$L_\Phi$: Effective reduced-gradient Lipschitz upper bound implied by the regularity budgets, used to bound iterations.

## 3. Complexity bracket

### Compared quantities

#### Q1 - achievable resource set

$$
\begin{gathered}\mathcal C(\varepsilon)=\{b\in\mathbb N_0^4:\ \exists\mathcal A\in\mathfrak A_\varepsilon,\ \forall(I,\mathcal O,\omega),\ \mathbf N_{\mathcal A}\preceq b\},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|^2\le\varepsilon^2\}.\\\mathbf N=(N_{\nabla f},N_{\nabla g},N_J,N_H).\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Accuracy regime with fixed regularity budgets

**Region.** All model budgets and initialization conditions apply, together with $\varepsilon>0$. The displayed asymptotic rate assumes fixed structural budgets and $\varepsilon\downarrow0$.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Joint budget unresolved

**Achievable budgets.** B1

**Necessary constraints.** No admitted claim in this comparison

**Gap or comparison.** All four coordinates belong to one algorithm’s joint budget. No comparable necessary-resource constraint is currently available, so an upper-to-lower ratio is undefined.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Oracle mapping.** Exact partial gradients of f and g, $g_{xy}$ vector products, and $g_{yy}$ vector products are available. Partial gradients are charged according to the declared atomic operations. Every HVP in internal conjugate-gradient iterations is charged; no inner-solve primitive is provided.

**Guarantee mapping.** The source uses $\varepsilon$ for squared-gradient tolerance. Write it as $\eta_{\rm src}$ to avoid ambiguity and substitute $\eta_{\rm src}=\varepsilon^2$ consistently. The target here is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$.

**Output mapping.** After the prescribed K iterations, draw $R\in\{0,\ldots,K-1\}$ independently and uniformly, and return $\widehat x=x_R$. The bound on the average squared gradient becomes an expected squared-gradient bound for this output; the same guarantee is not claimed for the last iterate.

**Resource mapping.** Charged resources are $N_{\nabla f}$, $N_{\nabla g}$, $N_J$, and $N_H$, with a fixed worst-case cap per execution. All four bounds hold simultaneously. There is no free inner-solve operation; its primitive queries count in the corresponding coordinates.

### B1 - AID-BiO

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Randomized witness

$$
\begin{aligned}N_{\nabla f}&=\mathcal O(\kappa^3\varepsilon^{-2}),&N_{\nabla g}&=\widetilde{\mathcal O}(\kappa^4\varepsilon^{-2}),\\N_J&=\mathcal O(\kappa^3\varepsilon^{-2}),&N_H&=\widetilde{\mathcal O}(\kappa^{7/2}\varepsilon^{-2}).\end{aligned}
$$

**Sources.** [1](https://proceedings.mlr.press/v139/ji21c/ji21c.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f.**

$$
O(\kappa ^3\varepsilon ^{-2})
$$

**N grad g.**

$$
\widetilde O(\kappa^4\varepsilon^{-2})
$$

**N JVP.**

$$
O(\kappa ^3\varepsilon ^{-2})
$$

**N HVP.**

$$
\widetilde O(\kappa^{7/2}\varepsilon^{-2})
$$

**Constants.** In the accuracy asymptotics, hold regularity, initialization, and noise budgets fixed while allowing dimension to vary. Condition-number powers are reported as in the source theorem and do not certify joint optimality. The source inner-loop lengths contain condition-number logarithms, so the relevant resource coordinates retain soft-O notation.

**Logarithmic factors.** With other budgets fixed and condition number tracked, lower-level gradient iterations and CG length may contain $\log(2+\kappa)$. For fixed $\kappa$, every resource coordinate has accuracy dependence $\mathcal O(\varepsilon^{-2})$.

**Derivation.** Apply $\eta_{\rm src}=\varepsilon^2$ simultaneously to all resource coordinates of the same source algorithm and return an independently uniformly selected outer iterate. This preserves the four-dimensional joint budget. The source average bound is $(64L_\Phi\Delta+5D_0)/K$. Choose positive integer K at least its numerator divided by $\varepsilon^2$. The effective reduced-gradient Lipschitz bound $L_\Phi$ is controlled by the model's regularity budgets.

**Source location.** [1](https://proceedings.mlr.press/v139/ji21c/ji21c.pdf) theorem: Theorem 1; section: 3–4.1; pdf pages: 5; 6; supplement: Appendix E, equations (21), (30), (31)

## References

[1] Kaiyi Ji; Junjie Yang; Yingbin Liang. Bilevel Optimization: Convergence Analysis and Enhanced Design. 2021. PMLR 139, ICML 2021.

https://proceedings.mlr.press/v139/ji21c/ji21c.pdf
