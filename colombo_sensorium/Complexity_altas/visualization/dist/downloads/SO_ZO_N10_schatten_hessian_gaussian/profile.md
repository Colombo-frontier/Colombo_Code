# Strongly convex noisy value optimization with Schatten-Lipschitz Hessians and no curvature upper bound

**Setting ID.** `SO_ZO_N10_schatten_hessian_gaussian`

Single-objective optimization

Schatten-Lipschitz Hessians under independent Gaussian scalar observations, with no upper curvature bound. Frobenius and scalar asymptotics are matched; general Schatten regimes retain explicit dimension gaps. An independent normalized operator hard subclass closes its own eventual window and supplies a finite-budget lower bound.

**Status.** Bounds missing

The regional bracket below specifies the quantified gaps and their parameter dependence.

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

$T_0$: Unquantified sufficient threshold for the independently sourced eventual risk bracket **Domain:** $T_0=T_0(d,p,\mu,\rho,R)\in\mathbb N$, $T_0\ge d^2$.

An integer $T_0(d,p,\mu,\rho,R)\ge d^2$ large enough for the upper transfer from Yu et al. (2024), Theorem 3.1, with Frobenius modulus $\rho_F=\rho d^{1/2-1/p}$, and the lower transfer from Theorem 3.2 with modulus $\rho$. No explicit parameter or dimension dependence is asserted. This is a sufficient threshold for a bracket, which need not be matching.

$\rho_F$: Frobenius modulus implied by the Schatten-p modulus **Domain:** $\rho_F>0$.

$\rho_F=\rho d^{1/2-1/p}$

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

### R1 - Frobenius endpoint: independent matching asymptotic risk

**Region.** $p=2$, fixed integer $d\ge1$, and fixed $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers. Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

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

### R2 - Intermediate Schatten norms: explicit dimension gap

**Region.** Fixed $2<p<\infty$, integer $d\ge2$, and $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers. Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Polynomial gap

**Lower bound.** B4

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Upper bound.** B3

$$
O(\rho^{2/3}d^{4/3-2/(3p)}/(\mu T^{2/3}))
$$

**Gap or comparison.**

$$
O(d^{1/3-2/(3p)})
$$

### R3 - Operator norm away from the normalized closure: explicit dimension gap

**Region.** $p=\infty$, fixed integer $d\ge2$, and fixed $\mu,\rho,R>0$ with $(\mu,\rho,R)\ne(1,1,1)$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers. Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold. The normalized operator closure has its own regime and is excluded from this comparison.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Polynomial gap

**Lower bound.** B6

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Upper bound.** B5

$$
O(\rho^{2/3}d^{4/3}/(\mu T^{2/3}))
$$

**Gap or comparison.**

$$
O(d^{1/3})
$$

### R4 - One dimension: all Schatten norms coincide

**Region.** $d=1$, fixed $2<p\le\infty$, and fixed $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers. Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B8

$$
\Omega(\rho^{2/3}/(\mu T^{2/3}))
$$

**Upper bound.** B7

$$
O(\rho^{2/3}/(\mu T^{2/3}))
$$

**Gap or comparison.** O(1)

### R5 - Normalized operator class: matching eventual risk

**Region.** $p=\infty$, $\mu=\rho=R=1$, fixed integer $d\ge2$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers. Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold. The common model has no Hessian upper bound. Only the lower-bound witness belongs to $I\preceq\nabla^2 f\preceq3I$. The comparison is eventual; it does not assert the normalized all-budget upper bound for the larger class.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B10

$$
\Omega(d^{4/3}/T^{2/3})
$$

**Upper bound.** B9

$$
O(d^{4/3}/T^{2/3})
$$

**Gap or comparison.** O(1)

### R6 - Frobenius or scalar case: high-precision scalar-query complexity

**Region.** Either $p=2$ with fixed $d\ge1$, or $d=1$ with fixed $2<p\le\infty$; fix $\mu,\rho,R>0$ and take $\varepsilon\downarrow0$. Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B12

$$
\Omega(\rho d^{3/2}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Upper bound.** B11

$$
O(\rho d^{3/2}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Gap or comparison.** O(1)

### R7 - General Schatten class: high-precision query bracket

**Region.** Fixed $2<p\le\infty$, integer $d\ge2$, and $\mu,\rho,R>0$; exclude $(p,\mu,\rho,R)=(\infty,1,1,1)$; take $\varepsilon\downarrow0$. Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Polynomial gap

**Lower bound.** B14

$$
\Omega(\rho d^{3/2}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Upper bound.** B13

$$
O(\rho d^{2-1/p}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Gap or comparison.**

$$
O(d^{1/2-1/p})
$$

### R8 - Normalized operator class: matching high-precision complexity

**Region.** $p=\infty$, $\mu=\rho=R=1$, fixed integer $d\ge2$; take $\varepsilon\downarrow0$. Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B16

$$
\Omega(d^2\varepsilon^{-3/2})
$$

**Upper bound.** B15

$$
O(d^2\varepsilon^{-3/2})
$$

**Gap or comparison.** O(1)

### R9 - Normalized operator class: finite-budget lower bound below the eventual window

**Region.** $p=\infty$, $\mu=\rho=R=1$, integer $d\ge1$, and $1\le T<T_0(d,\infty,1,1,1)$. The cited lower inequality holds for every integer d,T>=1. This row is restricted to the complement of the eventual comparison window. A bounded-Hessian-subclass upper bound does not bound the full unbounded-curvature model. No all-budget constant-risk upper bound is asserted.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Upper bound missing

**Lower bound.** B17

$$
\Omega(\min\{1,(d^2/T)^{2/3}\})
$$

**Upper bound.** No admitted bound for this comparison

**Gap or comparison.** No independently adopted upper bound in this startup region.

### R10 - General Schatten class: finite-budget bracket not established throughout the startup region

**Region.** Fixed $2\le p\le\infty$, integer $d\ge1$, and $\mu,\rho,R>0$; $1\le T<T_0(d,p,\mu,\rho,R)$; exclude $(p,\mu,\rho,R)=(\infty,1,1,1)$. All integer d>=1 in the displayed startup domain. T0 is only a sufficient threshold for the eventual asymptotic bracket. The independently cited results recorded here do not supply a finite-budget bracket throughout this full parameter domain. The eventual risk results do not assert startup guarantees. The normalized operator startup region has its own comparison and is excluded here.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Both bounds missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** No admitted bound for this comparison

**Gap or comparison.** No independent finite-budget bracket is recorded throughout this parameter region.

## 4. Bounds and supporting evidence

### B1 - Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $p=2$, fixed integer $d\ge1$, and fixed $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

### B2 - Gaussian Frobenius hard subclass and inclusion into the Schatten class

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $p=2$, fixed integer $d\ge1$, and fixed $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.2; Appendix B, especially B.2

Gaussian Frobenius hard subclass and inclusion into the Schatten class

The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

### B3 - Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}d^{4/3-2/(3p)}/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** Fixed $2<p<\infty$, integer $d\ge2$, and $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

### B4 - Gaussian Frobenius hard subclass and inclusion into the Schatten class

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** Fixed $2<p<\infty$, integer $d\ge2$, and $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.2; Appendix B, especially B.2

Gaussian Frobenius hard subclass and inclusion into the Schatten class

The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

### B5 - Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}d^{4/3}/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $p=\infty$, fixed integer $d\ge2$, and fixed $\mu,\rho,R>0$ with $(\mu,\rho,R)\ne(1,1,1)$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.; The normalized operator closure has its own regime and is excluded from this comparison.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

### B6 - Gaussian Frobenius hard subclass and inclusion into the Schatten class

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}d/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $p=\infty$, fixed integer $d\ge2$, and fixed $\mu,\rho,R>0$ with $(\mu,\rho,R)\ne(1,1,1)$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.; The normalized operator closure has its own regime and is excluded from this comparison.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.2; Appendix B, especially B.2

Gaussian Frobenius hard subclass and inclusion into the Schatten class

The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

### B7 - Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho^{2/3}/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $d=1$, fixed $2<p\le\infty$, and fixed $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

### B8 - Gaussian Frobenius hard subclass and inclusion into the Schatten class

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho^{2/3}/(\mu T^{2/3}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $d=1$, fixed $2<p\le\infty$, and fixed $\mu,\rho,R>0$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.2; Appendix B, especially B.2

Gaussian Frobenius hard subclass and inclusion into the Schatten class

The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.

### B9 - Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d^{4/3}/T^{2/3})
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $p=\infty$, $\mu=\rho=R=1$, fixed integer $d\ge2$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.; The common model has no Hessian upper bound. Only the lower-bound witness belongs to $I\preceq\nabla^2 f\preceq3I$. The comparison is eventual; it does not assert the normalized all-budget upper bound for the larger class.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Frobenius bootstrap and curvature-adapted estimator after Schatten norm conversion

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.

### B10 - Normalized operator hard subclass with unrestricted adaptive Gaussian queries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(d^{4/3}/T^{2/3})
$$

**Sources.** [2](https://arxiv.org/html/2610.00276v2)

**Conditions.** $p=\infty$, $\mu=\rho=R=1$, fixed integer $d\ge2$; $T\ge T_0(d,p,\mu,\rho,R)$, where $T_0\ge d^2$ is sufficiently large for both cited Frobenius transfers.; At smoothness order $\beta=3$, Definition 3.1 and Theorem 3.2 of Zhang et al. give a lower bound on the subclass $I\preceq\nabla^2 f\preceq3I$, operator Hessian Lipschitz constant one, and $\|x_*\|_2\le1$. This is a subclass of the present $p=\infty,\mu=\rho=R=1$ model. The lower bound is therefore valid for the larger class with no Hessian upper bound. The theorem permits arbitrary randomized adaptive algorithms, unrestricted query points and arbitrary transcript-measurable outputs. The bounded-Hessian upper bound from that theorem is not transferred to the larger class.; The common model has no Hessian upper bound. Only the lower-bound witness belongs to $I\preceq\nabla^2 f\preceq3I$. The comparison is eventual; it does not assert the normalized all-budget upper bound for the larger class.

**Dimension conditions.** Fix d,p,mu,rho,R before taking T to infinity. T0 is a sufficient threshold, not an explicit or dimension-uniform threshold.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [2](https://arxiv.org/html/2610.00276v2) Definition 3.1; Theorem 3.2, equation (10), beta=3; Appendix C

Normalized operator hard subclass with unrestricted adaptive Gaussian queries

At smoothness order $\beta=3$, Definition 3.1 and Theorem 3.2 of Zhang et al. give a lower bound on the subclass $I\preceq\nabla^2 f\preceq3I$, operator Hessian Lipschitz constant one, and $\|x_*\|_2\le1$. This is a subclass of the present $p=\infty,\mu=\rho=R=1$ model. The lower bound is therefore valid for the larger class with no Hessian upper bound. The theorem permits arbitrary randomized adaptive algorithms, unrestricted query points and arbitrary transcript-measurable outputs. The bounded-Hessian upper bound from that theorem is not transferred to the larger class.

### B11 - Monotone inversion of the cited expected-risk bound

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho d^{3/2}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** Either $p=2$ with fixed $d\ge1$, or $d=1$ with fixed $2<p\le\infty$; fix $\mu,\rho,R>0$ and take $\varepsilon\downarrow0$.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.; This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

**Dimension conditions.** Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Monotone inversion of the cited expected-risk bound

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound. This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

### B12 - Monotone inversion of the cited expected-risk bound

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho d^{3/2}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** Either $p=2$ with fixed $d\ge1$, or $d=1$ with fixed $2<p\le\infty$; fix $\mu,\rho,R>0$ and take $\varepsilon\downarrow0$.; The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.; This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

**Dimension conditions.** Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.2; Appendix B, especially B.2

Monotone inversion of the cited expected-risk bound

The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound. This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

### B13 - Monotone inversion of the cited expected-risk bound

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(\rho d^{2-1/p}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** Fixed $2<p\le\infty$, integer $d\ge2$, and $\mu,\rho,R>0$; exclude $(p,\mu,\rho,R)=(\infty,1,1,1)$; take $\varepsilon\downarrow0$.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.; This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

**Dimension conditions.** Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Monotone inversion of the cited expected-risk bound

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound. This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

### B14 - Monotone inversion of the cited expected-risk bound

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\rho d^{3/2}/(\mu^{3/2}\varepsilon^{3/2}))
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** Fixed $2<p\le\infty$, integer $d\ge2$, and $\mu,\rho,R>0$; exclude $(p,\mu,\rho,R)=(\infty,1,1,1)$; take $\varepsilon\downarrow0$.; The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound.; This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

**Dimension conditions.** Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.2; Appendix B, especially B.2

Monotone inversion of the cited expected-risk bound

The inequality $\|A\|_{S_p}\le\|A\|_F$ gives $\mathcal F_2(\rho,\mu,R)\subseteq\mathcal F_p(\rho,\mu,R)$. Apply the standard-Gaussian lower bound of Yu et al., Theorem 3.2. Its strict strong-convexity subclass is contained in the target class. If the source terminal point is interpreted as a queried point, append one query at an arbitrary measurable output; replacing T by T+1 does not change the eventual rate. This inclusion retains the dimension factor d, not the stronger Schatten dimension factor in the upper bound. This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

### B15 - Monotone inversion of the cited expected-risk bound

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d^2\varepsilon^{-3/2})
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf)

**Conditions.** $p=\infty$, $\mu=\rho=R=1$, fixed integer $d\ge2$; take $\varepsilon\downarrow0$.; The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound.; This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

**Dimension conditions.** Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf) Theorem 3.1; Section 2, assumptions A1–A3; Algorithm 4; Appendix E

Monotone inversion of the cited expected-risk bound

The singular-value inequality $\|A\|_F\le d^{1/2-1/p}\|A\|_{S_p}$ embeds the target class into the Frobenius class with $\rho_F=\rho d^{1/2-1/p}$. Apply Yu et al., Theorem 3.1. If its strict curvature convention is read literally, use a lower bound $\mu/2$. For the displayed sub-Gaussian tail convention, divide every observation and objective by $\sqrt2$; the Gaussian noise then has variance $1/2$. These are constant-factor changes and preserve the number of scalar queries. The source does not assume an upper Hessian bound. This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

### B16 - Monotone inversion of the cited expected-risk bound

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(d^2\varepsilon^{-3/2})
$$

**Sources.** [2](https://arxiv.org/html/2610.00276v2)

**Conditions.** $p=\infty$, $\mu=\rho=R=1$, fixed integer $d\ge2$; take $\varepsilon\downarrow0$.; At smoothness order $\beta=3$, Definition 3.1 and Theorem 3.2 of Zhang et al. give a lower bound on the subclass $I\preceq\nabla^2 f\preceq3I$, operator Hessian Lipschitz constant one, and $\|x_*\|_2\le1$. This is a subclass of the present $p=\infty,\mu=\rho=R=1$ model. The lower bound is therefore valid for the larger class with no Hessian upper bound. The theorem permits arbitrary randomized adaptive algorithms, unrestricted query points and arbitrary transcript-measurable outputs. The bounded-Hessian upper bound from that theorem is not transferred to the larger class.; This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

**Dimension conditions.** Fix d,p,mu,rho,R before taking epsilon to zero. The sufficiently small epsilon threshold may depend on these fixed parameters.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [2](https://arxiv.org/html/2610.00276v2) Definition 3.1; Theorem 3.2, equation (10), beta=3; Appendix C

Monotone inversion of the cited expected-risk bound

At smoothness order $\beta=3$, Definition 3.1 and Theorem 3.2 of Zhang et al. give a lower bound on the subclass $I\preceq\nabla^2 f\preceq3I$, operator Hessian Lipschitz constant one, and $\|x_*\|_2\le1$. This is a subclass of the present $p=\infty,\mu=\rho=R=1$ model. The lower bound is therefore valid for the larger class with no Hessian upper bound. The theorem permits arbitrary randomized adaptive algorithms, unrestricted query points and arbitrary transcript-measurable outputs. The bounded-Hessian upper bound from that theorem is not transferred to the larger class. This query-complexity statement is a derived inversion of the indicated eventual risk bracket, with all structural parameters and d fixed as $\varepsilon\downarrow0$. Risk is nonincreasing in the query budget. Its positive eventual lower bound implies positivity at every finite budget, so the required budget diverges as accuracy tends to zero. Integer rounding and an optional terminal query affect only universal constants. No joint uniform startup threshold in dimension and accuracy is asserted.

### B17 - Normalized operator hard subclass with unrestricted adaptive Gaussian queries

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(\min\{1,(d^2/T)^{2/3}\})
$$

**Sources.** [2](https://arxiv.org/html/2610.00276v2)

**Conditions.** $p=\infty$, $\mu=\rho=R=1$, integer $d\ge1$, and $1\le T<T_0(d,\infty,1,1,1)$.; At smoothness order $\beta=3$, Definition 3.1 and Theorem 3.2 of Zhang et al. give a lower bound on the subclass $I\preceq\nabla^2 f\preceq3I$, operator Hessian Lipschitz constant one, and $\|x_*\|_2\le1$. This is a subclass of the present $p=\infty,\mu=\rho=R=1$ model. The lower bound is therefore valid for the larger class with no Hessian upper bound. The theorem permits arbitrary randomized adaptive algorithms, unrestricted query points and arbitrary transcript-measurable outputs. The bounded-Hessian upper bound from that theorem is not transferred to the larger class.; A bounded-Hessian-subclass upper bound does not bound the full unbounded-curvature model. No all-budget constant-risk upper bound is asserted.

**Dimension conditions.** The cited lower inequality holds for every integer d,T>=1. This row is restricted to the complement of the eventual comparison window.

**Constants.** Universal positive constants. Sufficient asymptotic thresholds may depend on the fixed structural parameters and dimension.

**Source location.** [2](https://arxiv.org/html/2610.00276v2) Definition 3.1; Theorem 3.2, equation (10), beta=3; Appendix C

Normalized operator hard subclass with unrestricted adaptive Gaussian queries

At smoothness order $\beta=3$, Definition 3.1 and Theorem 3.2 of Zhang et al. give a lower bound on the subclass $I\preceq\nabla^2 f\preceq3I$, operator Hessian Lipschitz constant one, and $\|x_*\|_2\le1$. This is a subclass of the present $p=\infty,\mu=\rho=R=1$ model. The lower bound is therefore valid for the larger class with no Hessian upper bound. The theorem permits arbitrary randomized adaptive algorithms, unrestricted query points and arbitrary transcript-measurable outputs. The bounded-Hessian upper bound from that theorem is not transferred to the larger class.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Qian Yu; Yining Wang; Baihe Huang; Qi Lei; Jason D. Lee. Stochastic Zeroth-Order Optimization under Strongly Convexity and Lipschitz Hessian: Minimax Sample Complexity. 2024. NeurIPS 2024, volume 37; arXiv:2406.19617v1.

https://papers.nips.cc/paper_files/paper/2024/file/b444ad72520a5f5c467343be88e352ed-Paper-Conference.pdf

[2] Haihan Zhang; Wendao Wu; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Sharp Minimax Rates for Highly Smooth Strongly Convex Zeroth-Order Optimization. 2026. arXiv:2610.00276v2.

https://arxiv.org/html/2610.00276v2
