# Reduced bilevel objective: direct hypergradient access

**Setting ID.** `BL_SPEC_direct_reduced`

Bilevel optimization

Given the bilevel representation $\Phi(x)=f(x,y^*(x))$ with the unique global lower-level minimizer $y^*(x)=\operatorname*{argmin}_yg(x,y)$, seek an approximate stationary point of $\min_{x\in\mathbb{R}^{d_x}}\Phi(x)$. The information object is the reduced objective itself; lower-level strong convexity is not additionally assumed.

**Status.** Bounds missing

**TASK tags.** formulation: Bilevel unique reduced; task family: Bilevel

**MODEL tags.** existence: Unique inner solution; existence: Unique lower; initialization: Initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; interface family: Direct hypergradient; operation: Reduced objective gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; object: Outer point x hat

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N reduced gradient; precision: Bit precision not counted

## 1. Setting specification

### Task

Given the bilevel representation $\Phi(x)=f(x,y^*(x))$ with the unique global lower-level minimizer $y^*(x)=\operatorname*{argmin}_yg(x,y)$, seek an approximate stationary point of $\min_{x\in\mathbb{R}^{d_x}}\Phi(x)$. The information object is the reduced objective itself; lower-level strong convexity is not additionally assumed.

### Admissible model

For each $x$, the unconstrained lower minimum exists and is unique. No additional strong convexity, PL condition, or gradient/Hessian budget is assumed for $g$.

Assume directly that the optimized objective $\Phi$ is differentiable and $\nabla\Phi$ is $L_\Phi$-Lipschitz. This is not inferred from unstated regularity of f and g.

A point $x_0$ is given with $\Phi(x_0)-\inf_x\Phi(x)\le\Delta<\infty$.

### Oracle interface

The only charged interface is $x\mapsto\nabla\Phi(x)$, returning the exact full hypergradient. It directly accesses the reduced objective; one call does not include an implementation using primitive $f,g$ evaluations and lower-level solves. Inputs $L_\Phi,\Delta,x_0$ are public and $\Phi$ is hidden.

### Output

Output one outer point $\widehat{x}\in\mathbb{R}^{d_x}$. An inner solution, function value, or computable accuracy certificate is not required. Arbitrary admissible postprocessing and unqueried outputs are allowed.

### Loss or accuracy criterion

The base error is $\|\nabla\Phi(\widehat{x})\|_2^2$. The tolerance $\varepsilon$ is always expressed on the gradient-norm scale. The mean-square requirement is equivalent to the RMS gradient being at most this tolerance.

### Resource accounting

The resource $N$ counts only exact hypergradient calls, one unit each, under a fixed worst-case budget. Implementation cost of the original inner algorithm is outside this information-complexity model.

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

$\Delta$: Public upper bound on the initial reduced-objective gap **Domain:** $\Delta\ge0$.

$\Phi(x_0)-\inf_x\Phi(x)\le\Delta$

$L_\Phi$: An effective Lipschitz bound on the reduced gradient. **Domain:** $L_\Phi>0$.

$T,t$: Gradient-descent call count and iteration index

$h$: An arbitrary hard single-level function used in a lower-bound embedding.

$N_{\nabla\Phi}$: The number of direct reduced-gradient responses. **Domain:** A nonnegative integer. The resource section specifies the runtime-cost guarantee.

$N,Q$: This is the total call budget under the stated resource projection. If only one symbol is used, the two names are aliases for that same budget. **Domain:** RESOURCE specifies which operations are summed; no additional unit cost is introduced.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
\begin{gathered}Q^*(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_{I,\mathcal O,\omega}C_{\mathcal A},\\\mathfrak A_\varepsilon=\{\mathcal A\in\mathfrak A_{\rm spec}:\ \forall(I,\mathcal O),\ \mathbb E\|\nabla\Phi_I(\hat x_{\mathcal A})\|^2\le\varepsilon^2\}.\\C=N_{\nabla\Phi}.\end{gathered}
$$

**Scope.** worst admissible instance and arbitrary finite dimension unless model fixes dimensions

**Optimization direction.** minimize resources subject to accuracy

### R1 - Positive tolerance and initial function-value gap

**Region.** Assume $\varepsilon>0$, $\Delta\ge0$, and $L_\Phi>0$. This is the full declared error domain for direct reduced gradients. The upper bound does not measure implementation cost through the original bilevel interface.

**Quantity.** Q1

**Resource.** Sum the unit costs of actual primitive responses in the oracle specification. Separate requests for the two levels cost two calls.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

ceil(2 L_\Phi  \Delta /\varepsilon ^2) reduced-gradient calls (0 if \Delta =0)

**Gap or comparison.** Retain the gradient-descent upper bound on the complete original parameter window. A later high-accuracy window with fixed structural budgets also has a verified single-level-embedding lower bound.

**Comparison argument.** Each included claim has verified statement and applicability; mathematics review is separately labeled. No numerical threshold inferred from asymptotics.

### R2 - High-accuracy regime with fixed structural budgets

**Region.** Fix all positive regularity and initialization budgets, with $\varepsilon\downarrow0$ and $\Delta>0$, and impose the accuracy conditions of the source upper-bound theorem. The lower bound uses sufficiently large finite dimension.

**Quantity.** Q1

**Resource.** Joint resource budget

**Status.** Optimal

**Lower bound.** B2

**Upper bound.** B1

**Gap or comparison.** For sufficiently small accuracy and the stated dimension-growth window, upper and lower bounds differ by universal constants.

## 4. Bounds and supporting evidence

### B1 - gradient descent step 1/L_Φ and uniform output

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
\left\lceil\frac{2L_\Phi\Delta}{\varepsilon^2}\right\rceil\quad(\Delta=0\Rightarrow0)
$$

**Dimension conditions.** Valid in every finite dimension of the declared model. No additional dimension dependence is introduced beyond the formula.

**Oracle correspondence.** One query returns exact $\nabla\Phi(x)$ and costs one unit. Its implementation is unspecified, so this response does not imply free solution of the inner problem defined by $f,g$.

**Guarantee conversion.** The native target is $\mathbb E\|\nabla\Phi(\widehat x)\|^2\le\varepsilon^2$, a root-mean-square tolerance, rather than $\mathbb E\|\nabla\Phi(\widehat x)\|\le\varepsilon^2$.

**Output rule.** Return deterministically the queried point with smallest observed gradient norm. The instancewise bound also meets this setting's root-mean-square criterion.

**Resource conversion.** The charged resource is $N_{\nabla\Phi}$, with a fixed worst-case budget per execution rather than an expected count.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N reduced gradient.** ceil(2L_ΦΔ/ε²)

**N inner solve.** 0

**N grad f.** 0

**N grad g.** 0

**N HVP.** 0

**N JVP.** 0

**Constants.** No additional hidden parameter

**Derivation.** Choose step size $1/L_\Phi$. Smooth descent gives $$
\Phi(x_{t+1})\le\Phi(x_t)-\frac{\|\nabla\Phi(x_t)\|^2}{2L_\Phi}.
$$. Summing over $T$ steps bounds the smallest queried squared gradient norm by $2L_\Phi\Delta/T$. Return the earliest queried point attaining this minimum; no randomized output selection is needed. If $\Delta=0$, return $x_0$ directly. This is the explicit smooth-descent argument.

### B2 - Carmon–Duchi–Hinder–Sidford randomized hard family embedded with an independent quadratic lower level

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(L_\Phi\Delta\varepsilon^{-2})
$$

**Sources.** [1](https://arxiv.org/abs/1710.11606)

**Conditions.** The initial lower-level distance may be zero. The quantity $\nabla_yf=0$ satisfies every nonnegative upper bound.

**Dimension conditions.** The upper bound holds in all finite dimensions. The cited unconstrained lower bound allows dimension to grow with accuracy and is not claimed for every fixed dimension.

**Constants.** Unshown regularity, initialization, and noise budgets are fixed. Their joint parameter dependence is not certified as closed.

**Derivation.** Embed any single-level hard function as $f(x,y)=h(x)$ and $g(x,y)=\|y\|^2/2$. Primitive gradients provide no more information than the single-level full-derivative interface.

**Source location.** [1](https://arxiv.org/abs/1710.11606) theorem: Theorems 1–2, p=1; section: Sections 4–5

Set $f(x,y)=h(x)$ and $g(x,y)=\mu\|y\|^2/2$. Then $y^*=0$ and $\Phi=h$; lower-level queries contain no information about $h$, while $\nabla_yf=0$ and $\nabla^2g$ are constant. An arbitrary unqueried terminal point can be checked with one extra query. Adjusting accuracy constants does not change the asymptotic order.

## References

[1] Yair Carmon; John C. Duchi; Oliver Hinder; Aaron Sidford. Lower Bounds for Finding Stationary Points I. 2020. arXiv:1710.11606v3; Mathematical Programming 184 (2020).

https://arxiv.org/abs/1710.11606
