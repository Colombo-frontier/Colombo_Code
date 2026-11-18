# Stochastic convex objective accuracy: unbiased gradients and biased complete Hessians

**Setting ID.** `SO_HO_HOS01_S_full`

Single-objective optimization

Solve $\min_{x\in X}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Other quantified gap present; Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Convex body; geometry: Full space; smoothness: Lipschitz Hessian

**ORACLE tags.** access order: Higher-order interface; feedback quality: Stochastic; interface family: Fresh gradient full hessian; operation: Fresh gradient full hessian; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in X}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f$ is convex and $C^2$ on an open convex neighborhood of the compact convex domain $X$, with $X\subset\mathbb{R}^d$ and $\operatorname{diam}_2(X)\le D$.

$$\|D^{2}f(x)-D^{2}f(y)\|_{\mathrm{op},2}\le M_2\|x-y\|_{2}.$$

All regularity assumptions hold on this neighborhood. The noise class is specified by the conditional moment bounds under ORACLE.

### Oracle interface

After selecting $x\in X$, a fresh independent sample returns a vector $g(x)$ and a complete symmetric matrix $H(x)$. Conditional on the history and selected query point,

$$\mathbb{E}[g(x)\mid\mathcal{H}]=\nabla f(x),\quad\mathbb{E}[\|g(x)-\nabla f(x)\|_2^2\mid\mathcal{H}]\le\sigma_1^2,$$

$$\mathbb{E}[\|H(x)-\nabla^2f(x)\|_{\mathrm{op}}^2\mid\mathcal{H}]\le\sigma_2^2.$$

The Hessian estimate may be biased. The two components returned by one call may be correlated. Different calls use independent fresh samples, and sample reuse is unavailable. No function-value channel is provided.

A description of the feasible set, feasibility tests and global minimization of known models formed from existing replies are supplied as public auxiliary operations.

The public inputs are $x_0$, the target accuracy, and $d$, $D$, $M_2$, $\sigma_1$, $\sigma_2$, $\varepsilon_f$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in X$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in X}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

### Resource accounting

Each complete stochastic response specified under ORACLE costs one unit; each fresh-sample response within a batch is charged separately.

The resource budget is a fixed worst-case cap on every execution path. Initialization, stopping checks, and all actual responses in a batch are included.

Arithmetic, linear algebra, tensor operations, storage, and global solution of known models are free. Bit complexity, communication, and wall-clock time are not counted.

### Algorithm views and success guarantees

Arbitrary measurable adaptive algorithms with private randomness are allowed.

No linear-span, Krylov or zero-respecting restriction is imposed. Memory and internal computation are unrestricted.

Information is acquired adaptively in query order. Parallel submission does not reduce the number of actual responses counted. There is no communication-round or memory budget. Exact real arithmetic and arbitrarily small positive query separations are allowed.

Choose one algorithm from the public inputs, then require its guarantee separately for every admissible instance and oracle law.

$$\mathbb{E}\!\left[f(\widehat{x})-f^*\right]\le \varepsilon_f.$$

Expectation or probability is evaluated after fixing the instance; randomness comes from the algorithm's private seed and oracle sampling.

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

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in X}f(x).$$

$X$: The feasible set specified by the model, also used as the query and output domain. Convexity or ball geometry is assumed only when stated in the model.

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$\mathcal{H}$: The complete history before the current query. Conditional unbiasedness and moment bounds are evaluated after the query is selected and before the fresh sample is drawn.

$g(x),H(x)$: Gradient vector and full symmetric Hessian estimate returned from one fresh sample.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$D$: Known upper bound on the diameter of the convex domain **Domain:** $D>0$.

$M_2$: Lipschitz upper bound for the population Hessian **Domain:** $M_2>0$.

$\sigma_1$: Root-mean-square gradient error **Domain:** $\sigma_1\ge0$.

$\sigma_2$: Root mean-square operator-norm error of the Hessian estimate; bias is permitted **Domain:** $\sigma_2\ge0$.

$\varepsilon_f$: Expected objective-gap accuracy **Domain:** $\varepsilon_f>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Fixed worst-case call budget. A full (g,H) reply costs one call, as does a gradient-only reply. AG26 uses two independent draws per iteration, or three calls under separate derivative accounting, a constant-factor difference. Internal model minimization is free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Gradient statistical error dominates

**Region.** $(\sigma_1D/\varepsilon_f)^2\ge\max\{1,(\sigma_2D^2/\varepsilon_f)^{1/2},(M_2D^3/\varepsilon_f)^{2/7}\}$

**Quantity.** Q1

**Resource.** Fixed worst-case call budget. A full (g,H) reply costs one call, as does a gradient-only reply. AG26 uses two independent draws per iteration, or three calls under separate derivative accounting, a constant-factor difference. Internal model minimization is free.

**Status.** Optimal

**Lower bound.** B2

$$
c(\sigma_1D/\varepsilon_f)^2
$$

**Upper bound.** B1

$$
C[1+(\sigma_1D/\varepsilon_f)^2+(\sigma_2D^2/\varepsilon_f)^{1/2}+(M_2D^3/\varepsilon_f)^{2/7}]
$$

**Gap or comparison.** $O(1)$

### R2 - Remaining positive gradient-noise regime

**Region.** $\Theta_{rest}\cap\{\sigma_1>0\}$

**Quantity.** Q1

**Resource.** Fixed worst-case call budget. A full (g,H) reply costs one call, as does a gradient-only reply. AG26 uses two independent draws per iteration, or three calls under separate derivative accounting, a constant-factor difference. Internal model minimization is free.

**Status.** Other quantified gap

**Lower bound.** B2

$$
c(\sigma_1D/\varepsilon_f)^2
$$

**Upper bound.** B1

$$
C[1+(\sigma_1D/\varepsilon_f)^2+(\sigma_2D^2/\varepsilon_f)^{1/2}+(M_2D^3/\varepsilon_f)^{2/7}]
$$

**Gap or comparison.** $O(1+(\varepsilon_f/\sigma_1D)^2[1+(\sigma_2D^2/\varepsilon_f)^{1/2}+(M_2D^3/\varepsilon_f)^{2/7}])$

### R3 - Zero gradient noise

**Region.** $\Theta_{all}\cap\{\sigma_1=0\}$

**Quantity.** Q1

**Resource.** Fixed worst-case call budget. A full (g,H) reply costs one call, as does a gradient-only reply. AG26 uses two independent draws per iteration, or three calls under separate derivative accounting, a constant-factor difference. Internal model minimization is free.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C[1+(\sigma_1D/\varepsilon_f)^2+(\sigma_2D^2/\varepsilon_f)^{1/2}+(M_2D^3/\varepsilon_f)^{2/7}]
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** After selecting $x\in X$, a fresh independent sample returns a vector $g(x)$ and a complete symmetric matrix $H(x)$. Conditional on the history and selected query point,

**Guarantee mapping.** Expected-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in X$.

**Resource mapping.** Each complete stochastic response specified under ORACLE costs one unit; each fresh-sample response within a batch is charged separately.

### B1 - Accelerated stochastic contracting cubic Newton method

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C[1+(\sigma_1D/\varepsilon_f)^2+(\sigma_2D^2/\varepsilon_f)^{1/2}+(M_2D^3/\varepsilon_f)^{2/7}]
$$

**Sources.** [1](https://arxiv.org/pdf/2610.11693v2)

**Conditions.** $d\ge1,\ D,M_2,\varepsilon_f>0,\ \sigma_1,\sigma_2\ge0$

**Dimension conditions.** $d\ge1,\ D,M_2,\varepsilon_f>0,\ \sigma_1,\sigma_2\ge0$

**Source location.** [1](https://arxiv.org/pdf/2610.11693v2) theorem: Algorithm 2; Theorem 5.1; explicit Theorem C.7; pdf pages: 9

### B2 - One-dimensional affine objective with Gaussian gradient observations; every Hessian reply is zero

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(\sigma_1D/\varepsilon_f)^2
$$

**Conditions.** $\Theta_{all}\cap\{\sigma_1>0\}$

**Dimension conditions.** $\Theta_{all}\cap\{\sigma_1>0\}$

**Local argument.** A1

## 5. Local arguments

### A1 - Gaussian testing lower bound on a compact convex domain

**Scope.** Expected objective gap, fixed maximum query budget, and no exact function-value response. The one-dimensional hard domain must be allowed by the target domain family.

**Algorithm scope.** Expected objective gap, fixed maximum query budget, and no exact function-value response. The one-dimensional hard domain must be allowed by the target domain family.

Without exact function values, complete stochastic Hessian information does not remove the gradient-noise lower bound $\Omega(\sigma_1^2D^2/\varepsilon_f^2)$.

On $X=[-D/2,D/2]$, take $f_+(x)=ax$ and $f_-(x)=-ax$ with $a=4\varepsilon_f/D$. Both Hessians are zero, so every nonnegative Hessian-regularity and Hessian-noise budget is satisfied. A call returns $g_t=\pm a+\xi_t$, with independent $\xi_t\sim\mathcal N(0,\sigma_1^2)$, and $H_t=0$. Query locations convey no extra information.

Pad an early-stopped transcript to T observations. The two transcript laws have KL divergence at most $2Ta^2/\sigma_1^2$. Pinsker gives $\operatorname{TV}\le a\sqrt T/\sigma_1$. Under an equal prior, the minimum Bayes objective-gap risk over outputs in X is
$$\frac{aD}{2}(1-\operatorname{TV}),$$
because conditional linear-loss minimization selects the endpoint favored by the posterior. If $T\le\sigma_1^2D^2/(256\varepsilon_f^2)$, then $\operatorname{TV}\le1/4$ and this risk is at least $3\varepsilon_f/2$. Both instances cannot have expected gap at most $\varepsilon_f$. This proves the lower bound for every adaptive randomized algorithm, with embedding along one coordinate in higher dimensions.

The bound is informative for $\sigma_1>0$. At zero gradient noise its right side is only the trivial zero inequality. It does not apply to an additional exact-value channel. When comparing with the complete stochastic-Hessian upper bound, constant-factor closure is valid only where this statistical term dominates all other displayed terms.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] Artem Agafonov; Aslan Ashabokov; Dmitry Kamzolov; Alexander D'yakonov; Alexander Gasnikov; Martin Takáč. Matching the Lower Bounds: Stochastic Contracting Cubic Newton and Its Optimal Acceleration. arXiv:2610.11693v2, 2026-10-13; latest history checked 2026-10-29.

https://arxiv.org/pdf/2610.11693v2
