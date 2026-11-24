# Strongly convex noisy value optimization with Schatten-Lipschitz Hessians and no curvature upper bound

**Setting ID.** `SO_ZO_N10_schatten_hessian_gaussian`

Single-objective optimization

The full Schatten range p from two to infinity parameterizes Hessian regularity under independent Gaussian scalar values. The risk comparison separates large-budget asymptotics from all-budget lower bounds.

**Status.** Bounds missing

**TASK tags.** solution concept: Strongly convex minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz Hessian

**ORACLE tags.** feedback quality: Stochastic gaussian; operation: Function value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar function value (order 0)

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N noisy value

## 1. Setting specification

### Task

Minimize a hidden strongly convex objective globally on $\mathbb R^d$ using noisy scalar values, with terminal objective error as the loss.

### Admissible model

For $p\in[2,\infty]$, $f:\mathbb R^d\to\mathbb R$ is $C^2$ and satisfies $$\nabla^2 f(x)\succeq\mu I,\qquad\|\nabla^2f(x)-\nabla^2f(y)\|_{S_p}\le\rho\|x-y\|_2$$ for every $x,y\in\mathbb R^d$. The unique global minimizer obeys $\|x_*\|_2\le R$.

The Schatten norm $\|A\|_{S_p}$ is the ell-p norm of the singular values, with $S_2$ the Frobenius norm and $S_\infty$ the operator norm. There is no global upper bound on the Hessian or gradient. The known minimizer ball does not constrain queries or output.

### Oracle interface

One query at any $x_t\in\mathbb R^d$ returns $Y_t=f(x_t)+\xi_t$, where the noises are fresh independent $N(0,1)$ variables, independent of the algorithmic seed and past observations. Opposite-point observations have independent noise; no same-sample reuse or noiseless values are available.

Public inputs are $d,p,\mu,\rho,R$ and a horizon $T$ or target error $\varepsilon$. The objective is hidden.

### Output

Return any measurable $\widehat x\in\mathbb R^d$ from the transcript, whether or not it was queried.

### Loss or accuracy criterion

The base loss is $f(\widehat x)-f(x_*)$. For a fixed horizon, the minimax risk is $$\mathcal E_T^{(p)}=\inf_A\sup_{f\in\mathcal F_{S_p}(d,\mu,\rho,R)}\mathbb E[f(\widehat x)-f(x_*)].$$ Expectation includes private randomization and observation noise.

### Resource accounting

Each scalar noisy value costs one evaluation. Repeated values, every side of a finite difference, localization, and validation are all charged. The algorithm uses at most $T$ evaluations on every execution. Exact specification of finite query coordinates, arithmetic, and storage are free.

### Algorithm views and success guarantees

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall f:\ \mathbb E[f(\widehat x)-f(x_*)]\le\varepsilon
$$

The expectation averages the independent Gaussian observations and private randomization after the function is fixed. The evaluation count is capped on every path.

**Budget convention.** fixed_worst_case

## 2. Notation and parameters

$d$: Ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$p$: Schatten norm exponent **Domain:** $2\le p\le\infty$.

$\mu$: Global strong-convexity modulus **Domain:** $\mu>0$.

$\rho$: Schatten-p Hessian Lipschitz modulus **Domain:** $\rho>0$.

$R$: Known Euclidean radius of the minimizer **Domain:** $R>0$.

$T$: Pathwise scalar-evaluation horizon **Domain:** $T\in\mathbb N_{\ge1}$.

$\varepsilon$: Expected objective-error target **Domain:** $\varepsilon>0$.

$T_0$: Unquantified sufficient threshold for the eventual two-sided risk bound **Domain:** $T_0=T_0(d,p,\mu,\rho,R)\in\mathbb N_{\ge1}$.

Any sufficiently large threshold supplied by Theorem thm:schatten after universal multiplicative constants are fixed. No explicit dimension dependence is asserted.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
\mathcal E_T^{(p)}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{scalar\ value}}\le T$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q2 - minimax metric resource quantity

$$
T_*^{(p)}(\varepsilon)=\inf\{T\in\mathbb N:\mathcal E_T^{(p)}\le\varepsilon\}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{scalar\ value}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

### R1 - Frobenius endpoint: large-budget minimax risk

**Region.** $p=2$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window. Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted. This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Upper bound.** B1

$$
O(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Gap or comparison.** O(1)

### R2 - Intermediate Schatten norms: large-budget minimax risk

**Region.** Fixed $2<p<\infty$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window. Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted. This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(\rho^{2/3}d^{4/3-2/(3p)}/(\mu T^{2/3}))
$$

**Upper bound.** B3

$$
O(\rho^{2/3}d^{4/3-2/(3p)}/(\mu T^{2/3}))
$$

**Gap or comparison.** O(1)

### R3 - Operator endpoint: large-budget minimax risk

**Region.** $p=\infty$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window. Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted. This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega(\rho^{2/3}d^{4/3}/(\mu T^{2/3}))
$$

**Upper bound.** B5

$$
O(\rho^{2/3}d^{4/3}/(\mu T^{2/3}))
$$

**Gap or comparison.** O(1)

### R4 - High-precision scalar-query complexity

**Region.** Fix $2\le p\le\infty$, integer $d\ge1$, and $\mu,\rho,R>0$; take $\varepsilon\downarrow0$. Every fixed d>=1; the sufficiently small accuracy threshold may depend on the fixed parameters. Integer rounding is absorbed only in the stated high-precision asymptotic window.

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B8

$$
\Omega\!\left(\frac{\rho d^{2-1/p}}{\mu^{3/2}\varepsilon^{3/2}}\right)
$$

**Upper bound.** B7

$$
O\!\left(\frac{\rho d^{2-1/p}}{\mu^{3/2}\varepsilon^{3/2}}\right)
$$

**Gap or comparison.** O(1)

### R5 - Startup budgets: a finite-budget lower obstruction

**Region.** $d\ge1$ and $1\le T<T_0(d,p,\mu,\rho,R)$ are integers, $2\le p\le\infty$, and $\mu,\rho,R>0$. Every integer d>=1. The three branches are lower-bound scales and are not asserted to be upper bounds for the unbounded-curvature class. The stated lower inequality itself holds for all budgets. The eventual two-sided risk bound holds after $T_0$; no explicit polynomial dependence of this sufficient threshold on the parameters is asserted.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Upper bound missing

**Lower bound.** B9

$$
\frac{3}{64\cdot5120^2}\min\left\{\frac{\mu^3d^{2/p}}{\rho^2},\mu R^2,\frac{\rho^{2/3}d^{4/3-2/(3p)}}{\mu T^{2/3}}\right\}
$$

**Upper bound.** No admitted bound for this comparison

**Gap or comparison.** Only a lower direction is stated in the unquantified startup window.

## 4. Bounds and supporting evidence

### B1 - Localization in an estimated metric, orthogonal finite differences, and robust Newton correction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** $p=2$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window.; The upper bound is uniform over the whole objective class before taking the large-T limit.; This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Dimension conditions.** Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted.

**Constants.** Universal positive multiplicative constants independent of all displayed parameters. Only the asymptotic threshold may depend on the fixed parameters.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Theorem thm:schatten; Corollary cor:operator; Appendix app:upper

Localization in an estimated metric, orthogonal finite differences, and robust Newton correction. Unrestricted randomized adaptive algorithms

The upper bound is uniform over the whole objective class before taking the large-T limit.

### B2 - Shared radial cutoff, adaptive total-information testing, and Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** $p=2$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window.; This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Dimension conditions.** Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted.

**Constants.** Universal positive multiplicative constants independent of all displayed parameters. Only the asymptotic threshold may depend on the fixed parameters.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Theorem thm:schatten; Corollary cor:schatten-finite

Shared radial cutoff, adaptive total-information testing, and Schatten norm conversion. All unrestricted randomized adaptive algorithms

### B3 - Localization in an estimated metric, orthogonal finite differences, and robust Newton correction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}d^{4/3-2/(3p)}/(\mu T^{2/3}))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** Fixed $2<p<\infty$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window.; The upper bound is uniform over the whole objective class before taking the large-T limit.; This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Dimension conditions.** Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted.

**Constants.** Universal positive multiplicative constants independent of all displayed parameters. Only the asymptotic threshold may depend on the fixed parameters.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Theorem thm:schatten; Corollary cor:operator; Appendix app:upper

Localization in an estimated metric, orthogonal finite differences, and robust Newton correction. Unrestricted randomized adaptive algorithms

The upper bound is uniform over the whole objective class before taking the large-T limit.

### B4 - Shared radial cutoff, adaptive total-information testing, and Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}d^{4/3-2/(3p)}/(\mu T^{2/3}))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** Fixed $2<p<\infty$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window.; This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Dimension conditions.** Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted.

**Constants.** Universal positive multiplicative constants independent of all displayed parameters. Only the asymptotic threshold may depend on the fixed parameters.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Theorem thm:schatten; Corollary cor:schatten-finite

Shared radial cutoff, adaptive total-information testing, and Schatten norm conversion. All unrestricted randomized adaptive algorithms

### B5 - Localization in an estimated metric, orthogonal finite differences, and robust Newton correction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}d^{4/3}/(\mu T^{2/3}))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** $p=\infty$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window.; The upper bound is uniform over the whole objective class before taking the large-T limit.; This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Dimension conditions.** Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted.

**Constants.** Universal positive multiplicative constants independent of all displayed parameters. Only the asymptotic threshold may depend on the fixed parameters.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Theorem thm:schatten; Corollary cor:operator; Appendix app:upper

Localization in an estimated metric, orthogonal finite differences, and robust Newton correction. Unrestricted randomized adaptive algorithms

The upper bound is uniform over the whole objective class before taking the large-T limit.

### B6 - Shared radial cutoff, adaptive total-information testing, and Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}d^{4/3}/(\mu T^{2/3}))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** $p=\infty$; fix integer $d\ge1$ and $\mu,\rho,R>0$, and restrict to $T\ge T_0(d,p,\mu,\rho,R)$ in the eventual large-budget window.; This is an asymptotic risk comparison, not an all-budget equality. The model has no global curvature upper bound.

**Dimension conditions.** Every fixed integer d>=1. The sufficiently large threshold T0 may depend on d,p,mu,rho,R; no dimension-uniform startup threshold is asserted.

**Constants.** Universal positive multiplicative constants independent of all displayed parameters. Only the asymptotic threshold may depend on the fixed parameters.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Theorem thm:schatten; Corollary cor:schatten-finite

Shared radial cutoff, adaptive total-information testing, and Schatten norm conversion. All unrestricted randomized adaptive algorithms

### B7 - Invert the matching large-budget expected-risk bound

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{\rho d^{2-1/p}}{\mu^{3/2}\varepsilon^{3/2}}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** Fix $2\le p\le\infty$, integer $d\ge1$, and $\mu,\rho,R>0$; take $\varepsilon\downarrow0$.; Integer rounding is absorbed only in the stated high-precision asymptotic window.

**Dimension conditions.** Every fixed d>=1; the sufficiently small accuracy threshold may depend on the fixed parameters.

**Constants.** Universal multiplicative constants; parameter-dependent precision threshold.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Corollary cor:sample, eq:sample

Invert the matching large-budget expected-risk bound. Unrestricted randomized algorithms

### B8 - Invert the asymptotic lower bound, using the strictly positive all-budget obstruction

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega\!\left(\frac{\rho d^{2-1/p}}{\mu^{3/2}\varepsilon^{3/2}}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** Fix $2\le p\le\infty$, integer $d\ge1$, and $\mu,\rho,R>0$; take $\varepsilon\downarrow0$.; Integer rounding is absorbed only in the stated high-precision asymptotic window.

**Dimension conditions.** Every fixed d>=1; the sufficiently small accuracy threshold may depend on the fixed parameters.

**Constants.** Universal multiplicative constants; parameter-dependent precision threshold.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Corollary cor:sample, eq:sample

Invert the asymptotic lower bound, using the strictly positive all-budget obstruction. All unrestricted randomized algorithms

### B9 - A globally well-conditioned radial-cutoff hard family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\frac{3}{64\cdot5120^2}\min\left\{\frac{\mu^3d^{2/p}}{\rho^2},\mu R^2,\frac{\rho^{2/3}d^{4/3-2/(3p)}}{\mu T^{2/3}}\right\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf)

**Conditions.** $d\ge1$ and $1\le T<T_0(d,p,\mu,\rho,R)$ are integers, $2\le p\le\infty$, and $\mu,\rho,R>0$.; The three branches are lower-bound scales and are not asserted to be upper bounds for the unbounded-curvature class.; The stated lower inequality itself holds for all budgets. The eventual two-sided risk bound holds after $T_0$; no explicit polynomial dependence of this sufficient threshold on the parameters is asserted.

**Dimension conditions.** Every integer d>=1.

**Constants.** The displayed lower constant is explicit and universal.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf) Corollary cor:schatten-finite, eq:schatten-finite; Theorem thm:finite

A globally well-conditioned radial-cutoff hard family. All adaptive randomized algorithms

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_H17. Hessian Norms and Minimax Rates in Noisy Zeroth-Order Optimization. H17_Hessian_Norms_Colombo_Team.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/H17/manuscript.pdf
