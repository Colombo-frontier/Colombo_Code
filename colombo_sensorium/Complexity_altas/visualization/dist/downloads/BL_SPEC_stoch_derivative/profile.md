# Strongly convex lower level: stochastic gradients and derivative-vector products

**Setting ID.** `BL_SPEC_stoch_derivative`

Bilevel optimization

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

**Status.** Bounds missing; Joint budget unresolved

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** convexity: Lower objective strongly convex in its lower variable; initialization: Initial distance; smoothness: Hessian or cross derivative lipschitz; smoothness: Lipschitz gradient; smoothness: Value lipschitz; stochastic model: Bounded gradient variance

**ORACLE tags.** feedback quality: Sample; interface family: Derivative vector; operation: Cross derivative vector product; operation: Hessian vector product; operation: Partial gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N grad f; measure: N grad g; measure: N hvp; measure: N jvp; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve the bilevel problem $\min_x\Phi(x)$, where $\Phi(x)=f(x,y^*(x))$ and $y^*(x)=\operatorname*{argmin}_y g(x,y)$ is the unique global lower-level solution. The upper- and lower-level variables are $x\in\mathbb{R}^{d_x}$ and $y\in\mathbb{R}^{d_y}$. Seek approximate stationarity of the reduced objective under the declared criterion and guarantee; assumptions on $f$, $g$, and $\Phi$ are specified separately.

The population functions are $f=\mathbb E_\xi F(\cdot;\xi)$ and $g=\mathbb E_\zeta G(\cdot;\zeta)$. Upper- and lower-level sample seeds are denoted by $\xi,\zeta$.

### Admissible model

For every fixed upper-level point $x$, $g(x,\cdot)$ is $\mu$-strongly convex on all of $\mathbb{R}^{d_y}$. Convexity in $x$ or joint convexity in $(x,y)$ is not required.

The population full gradient $\nabla f=(\nabla_x f,\nabla_y f)$ is globally $L$-Lipschitz in $(x,y)$. Convexity of $f$ is not required.

The population full gradient $\nabla g=(\nabla_x g,\nabla_y g)$ is globally $L$-Lipschitz in $(x,y)$.

The objective $\Phi$ has a finite lower bound. A point $x_0$ is given and satisfies $\Phi(x_0)-\inf_x\Phi(x)\le\Delta$. Convexity or existence of a global minimizer of $\Phi$ is not required.

The initial point $(x_0,y_0)$ and bound $\|y_0-y^*(x_0)\|\le R_0$ are given. This is an initialization budget, not a requirement that the oracle return $y^*$.

The function $f$ is jointly $M$-Lipschitz in the full variable $(x,y)$. This budget is recorded as $C_f=M$ and therefore bounds the full gradient. It is stronger than a bound only on $f_y$.

The function $g_{xy}$ is $\tau$-Lipschitz in $(x,y)$, and $g_{yy}$ is $\rho$-Lipschitz. These budgets are specified separately and are not combined into an unspecified common constant.

For almost every upper-level sample xi, $F(\cdot;\xi)$ is jointly $M=C_f$-Lipschitz and $\nabla F$ is jointly $L$-Lipschitz, with constants uniform over all samples.

For almost every lower-level sample, $G(x,\cdot;\zeta)$ is $\mu$-strongly convex; $\nabla G$ is jointly $L$-Lipschitz, and the joint Lipschitz budgets for $G_{xy}$ and $G_{yy}$ are $\tau,\rho$. These bounds hold uniformly over samples.

The population functions are sample expectations and the derivative estimators are unbiased. At every point, $\mathbb{E}\|\nabla G-\nabla g\|^2\le\sigma^2$ holds, including conditional on the past before fresh sampling. Unbiasedness is not asserted separately for a fixed sample realization.

### Oracle interface

Public inputs include dimension, target accuracy, quantitative model budgets, and initial points. Functions, lower-level optimizers, and the reduced objective are hidden.

Upper-level interface: choose $b\in\{x,y\}$ and $(x,y)$ and receive $\nabla_b F(x,y;\xi)$. The two partial gradients at the same fixed point may share an upper-level sample, but are charged separately.

For a lower-level gradient query, choose $b\in\{x,y\}$ and $(x,y)$ and return $\nabla_bG(x,y;\zeta)$ from a fresh lower-level sample. Each partial gradient lies in the space of its corresponding variable block.

Cross-Hessian vector product: $(x,y,v)\mapsto G_{xy}(x,y;\zeta)v\in\mathbb R^{d_x}$, where $v\in\mathbb R^{d_y}$, using a fresh lower-level sample.

Hessian–vector products take the form $(x,y,v)\mapsto G_{yy}(x,y;\zeta)v\in\mathbb R^{d_y}$, where $v\in\mathbb R^{d_y}$. Each product uses a fresh lower-level sample.

Queries may use the entire joint Euclidean space. Every fresh draw is conditionally unbiased given the history before that draw. The second upper-level partial gradient from the same sample is unbiased only relative to the history preceding that sample. Lower-level updates, cross-derivative products, and Neumann-series product batches are independent. The interface does not permit reuse of a sample at different points.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

In this unconstrained model with a strongly convex lower level, $\nabla\Phi(x)=\nabla_x f(x,y^*)-g_{xy}(x,y^*)g_{yy}(x,y^*)^{-1}\nabla_y f(x,y^*)$, where $g_{xy}=\mathrm{D}_y\nabla_x g$ and $g_{yy}=\mathrm{D}_y\nabla_y g$, and $y^*$ denotes $y^*(x)$. The identity defines the hypergradient without granting additional query access.

### Resource accounting

Retain the joint budget $(N_{\nabla f},N_{\nabla g},N_J,N_H)$, counting sampled F-partial gradients, sampled G-partial gradients, cross-Hessian vector products, and Hessian-vector products separately. Each sample response increments its coordinate by one; a batch is not a free bundled call.

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

$L$: Common joint-variable Lipschitz upper bound for the complete gradients at both levels **Domain:** $L\ge\mu>0$.

$C_f$: The upper function’s Lipschitz budget in the entire joint variable, denoted M in the source. **Domain:** $C_f=M\ge0$.

The bound is $\|\nabla f(x,y)\|\le M$; in the stochastic version it also holds for every upper-level sample.

$\mu$: The uniform strong-convexity modulus in the lower-level variable. **Domain:** $\mu>0$.

$\rho$: Joint Lipschitz upper bound for the lower-variable Hessian block $g_{yy}$. **Domain:** $\rho\ge0$.

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$R_0$: Public initial lower-level distance bound **Domain:** $R_0\ge0$.

$\|y_0-y^*(x_0)\|\le R_0$

$\kappa$: Lower-level condition number **Domain:** $\kappa\ge1$.

$\kappa=L/\mu$

$\tau$: Joint-variable Lipschitz upper bound for the lower cross-Hessian block. **Domain:** $\tau\ge0$.

$\sigma$: Conditional standard-deviation bound for a fresh full lower-level gradient estimate **Domain:** $\sigma\ge0$.

$\mathbb E[\|\nabla G-\nabla g\|^2\mid\mathcal H]\le\sigma^2$

$g_{xy},g_{yy}$: Mixed lower-level Hessian block and lower-variable Hessian block **Domain:** $g_{xy}\in\mathbb R^{d_x\times d_y},g_{yy}\in\mathbb R^{d_y\times d_y}$.

$g_{xy}=\mathrm D_y\nabla_xg,\quad g_{yy}=\mathrm D_y\nabla_yg$

$v$: The algorithm-selected direction for a derivative–vector query. **Domain:** $v\in\mathbb R^{d_y}$.

$K,x_k,R$: The outer iteration count, kth outer point, and independent uniform output index. **Domain:** $K\ge1,\ 0\le k<K,\ R\sim\operatorname{Unif}\{0,\ldots,K-1\}$.

$\eta_{\rm src}$: Squared-gradient tolerance from the source, renamed to distinguish it from this profile's norm tolerance **Domain:** $\eta_{\rm src}=\varepsilon^2$.

$\mathcal C(\varepsilon),\mathbf N,b,\preceq$: Set of joint budgets attaining the tolerance, call vector, four-dimensional integer budget, and coordinatewise inequalities. **Domain:** $\mathbf N,b\in\mathbb N_0^4$.

$\mathfrak A_{\rm spec},\mathfrak A_\varepsilon,\mathcal A,I,\mathcal O,\omega$: The admissible algorithm class, its accuracy-achieving subclass, algorithm, instance, oracle law, and execution randomness define the quantifiers for the joint attainable set.

$F,G$: Upper- and lower-level stochastic sample functions

$f(x,y)=\mathbb E_\xi F(x,y;\xi),\quad g(x,y)=\mathbb E_\zeta G(x,y;\zeta)$

$\xi,\zeta,\mathcal H$: The upper-level seed, lower-level seed, and pre-sampling history.

$M$: A sample-uniform joint Lipschitz budget for upper-level values. **Domain:** $M=C_f$.

$F_x,F_y,G_{xy},G_{yy}$: Upper-level sample partial gradients and lower-level sample Hessian blocks; derivative and population versions use the same block and dimension conventions

$B_j,j$: The independent lower-level sample batch and term index for the jth Neumann-series term. **Domain:** Every response in each batch is charged separately.

$N_{\nabla f}$: Upper-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_{\nabla g}$: Lower-level primitive-gradient responses, full or partial as specified by the interface. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_J$: The number of lower cross-derivative–vector responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N_H$: Number of lower-level Hessian-vector product responses **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

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

**Oracle mapping.** Sampled F/G partial gradients and stochastic Jacobian/Hessian-vector products satisfy the stated samplewise regularity and fresh-sample conditional unbiasedness conditions. Same-sample coupling follows the oracle protocol and does not permit unrestricted reuse across points. Each partial gradient or vector product is charged separately; no inner-solve primitive is available.

**Guarantee mapping.** The source uses $\varepsilon$ for squared-gradient tolerance. Write it as $\eta_{\rm src}$ to avoid ambiguity and substitute $\eta_{\rm src}=\varepsilon^2$ consistently. The target here is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$.

**Output mapping.** After the prescribed K iterations, draw $R\in\{0,\ldots,K-1\}$ independently and uniformly, and return $\widehat x=x_R$. The bound on the average squared gradient becomes an expected squared-gradient bound for this output; the same guarantee is not claimed for the last iterate.

**Resource mapping.** Charged resources are $N_{\nabla f}$, $N_{\nabla g}$, $N_J$, and $N_H$, with a fixed worst-case cap per execution. All four bounds hold simultaneously. There is no free inner-solve operation; its primitive queries count in the corresponding coordinates.

### B1 - stocBiO

**Admission.** Included in the bracket

**Direction.** achievable

**Witness or lower-bound scope.** Randomized witness

$$
\begin{aligned}N_{\nabla f}&=\mathcal O(\kappa^5\varepsilon^{-4}),&N_{\nabla g}&=\widetilde{\mathcal O}(\kappa^9\varepsilon^{-4}),\\N_J&=\mathcal O(\kappa^5\varepsilon^{-4}),&N_H&=\widetilde{\mathcal O}(\kappa^6\varepsilon^{-4}).\end{aligned}
$$

**Sources.** [1](https://proceedings.mlr.press/v139/ji21c/ji21c.pdf)

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad f.**

$$
O(\kappa ^5\varepsilon ^{-4})
$$

**N grad g.**

$$
\widetilde O(\kappa^9\varepsilon^{-4})
$$

**N JVP.**

$$
O(\kappa ^5\varepsilon ^{-4})
$$

**N HVP.**

$$
\widetilde O(\kappa ^6\varepsilon ^{-4})
$$

**Constants.** In the accuracy asymptotics, hold regularity, initialization, and noise budgets fixed while allowing dimension to vary. Condition-number powers are reported as in the source theorem and do not certify joint optimality. The source inner-loop lengths contain condition-number logarithms, so the relevant resource coordinates retain soft-O notation.

**Logarithmic factors.** The inner-loop length contains $\log(2+\kappa)$. The Hessian-vector-product coordinate also contains $\log(2+\kappa^2/\varepsilon^2)$ from truncating the Neumann series; the source suppresses this factor in tilde notation.

**Derivation.** Apply the same substitution $\eta_{\rm src}=\varepsilon^2$ simultaneously to every resource coordinate of the source algorithm. Independently select a historical outer iterate uniformly for output. This conversion preserves the four-dimensional joint budget.

**Source location.** [1](https://proceedings.mlr.press/v139/ji21c/ji21c.pdf) theorem: Theorem 3; section: 3–4.2; pdf pages: 5; 6; supplement: Appendix G.3, equations (63)–(68) and final complexity calculation

## References

[1] Kaiyi Ji; Junjie Yang; Yingbin Liang. Bilevel Optimization: Convergence Analysis and Enhanced Design. 2021. PMLR 139, ICML 2021.

https://proceedings.mlr.press/v139/ji21c/ji21c.pdf
