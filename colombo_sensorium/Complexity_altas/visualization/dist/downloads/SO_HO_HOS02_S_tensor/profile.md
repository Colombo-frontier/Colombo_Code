# Stochastic convex objective accuracy: complete high-order tensors with orderwise mean-square errors

**Setting ID.** `SO_HO_HOS02_S_tensor`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Euclidean ball; geometry: Full space; smoothness: Higher order lipschitz

**ORACLE tags.** access order: Higher-order interface; feedback quality: Stochastic; interface family: Fresh full k derivative tuple; operation: Fresh full k derivative tuple; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^k$, with $k\ge3$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_k\|x-y\|_{2}.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

### Oracle interface

After selecting any $x\in\mathbb{R}^d$, a fresh sample returns the complete tensor tuple $(g_j(x))_{j=1}^k$. Conditional on the history $\mathcal{H}$,

$$\mathbb{E}[g_1(x)\mid\mathcal{H}]=\nabla f(x),\qquad\mathbb{E}[\|g_j(x)-D^jf(x)\|_{\mathrm{op}}^2\mid\mathcal{H}]\le\sigma_j^2\quad(1\le j\le k).$$

Derivative estimates of order two and higher may be biased. Different orders in one reply may be correlated and need not derive from a common scalar sample loss. Calls use independent fresh samples without reuse; no value channel is provided.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $R$, $M_k$, $(\sigma_j)_{j=1}^k$, $\varepsilon_f$, $\sigma_1$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

### Output

Return $\widehat{x}\in \mathbb{R}^d$.

The output may be an unqueried point, a feasible average of past iterates, or another feasible postprocessing result. No function value or additional computable certificate is required.

### Loss or accuracy criterion

The base error is

$$\mathcal{E}(\widehat{x})=f(\widehat{x})-f^*.$$

Here $f^*=\inf_{x\in \mathbb{R}^d}f(x)$. The lower-boundedness or attainment assumption makes this error finite and nonnegative.

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

$D^jf(x),\ \nabla f(x),\ \nabla^2f(x)$: Fréchet derivative of order $j$, gradient and Hessian. **Domain:** $j\in\{0,\ldots,k\}$ and $D^0f=f$.

$\|T\|_{\mathrm{op}},\ \|T\|_{\mathrm{op},2}$: Induced operator norm of a Euclidean multilinear tensor; the spectral norm for matrices.

$$\|T\|_{\mathrm{op}}=\|T\|_{\mathrm{op},2}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|.$$

$\mathcal{E}$: Base error defined in the metric specification; expectation or probability aggregation is imposed by the guarantee.

$N$: Total number of original oracle calls; the unit cost is specified in the resource convention. **Domain:** $N\in\mathbb{Z}_{\ge0}$.

$T^*$: Minimum worst-case budget for one algorithm to meet the requirement on the full instance class, within the specified regime, guarantee and resource projection. Expected-resource specifications instead minimize the per-instance expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching bounds up to constants, and upper bounds omitting the declared logarithmic factors. **Domain:** Hidden constants, fixed parameters, and omitted logarithmic variables are specified for each bound.

$\inf,\sup,\min,\max$: Infimum, supremum, attained minimum and attained maximum.

$c,C$: Positive universal constants without assigned numerical values; a subscript permits dependence only on the indicated fixed parameters. **Domain:** $0<c,C<\infty$.

$f,f^*$: Unknown objective and its global infimum over the specified feasible domain.

$$f^*=\inf_{x\in \mathbb{R}^d}f(x).$$

$\mathbb{E},\Pr$: Expectation and probability after fixing the instance; their randomness sources are specified by the guarantee.

$\mathcal{H}$: The complete history before the current query. Conditional unbiasedness and moment bounds are evaluated after the query is selected and before the fresh sample is drawn.

$g_j(x)$: Full tensor estimate of the derivative of order $j$ returned from one fresh sample. **Domain:** $1\le j\le k$.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge 3}$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k>0$.

$(\sigma_j)_{j=1}^k$: Root mean-square errors by derivative order **Domain:** $(\sigma_j)_{j=1}^k\in\mathbb{R}_{\ge0}^k$.

$\varepsilon_f$: Expected objective-gap accuracy **Domain:** $\varepsilon_f>0$.

$\sigma_1$: First coordinate of the derivative-noise vector, used for numerical regime classification **Domain:** $\sigma_1\ge0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete response through order k costs one call. Each iteration uses a constant number of responses, with the constant allowed to depend on fixed k, and the iteration budget is fixed. Exact global model minimization and real arithmetic are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Each complete response through order k costs one call. Each iteration uses a constant number of responses, with the constant allowed to depend on fixed k, and the iteration budget is fixed. Exact global model minimization and real arithmetic are free.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Statistically dominated regime

**Region.** $(\sigma_1R/\varepsilon_f)^2\ge\max\{1,\max_{2\le j\le k}(\sigma_jR^j/\varepsilon_f)^{1/j},(M_kR^{k+1}/\varepsilon_f)^{1/(k+1)}\}$

**Quantity.** Q1

**Resource.** Each complete response through order k costs one call. Each iteration uses a constant number of responses, with the constant allowed to depend on fixed k, and the iteration budget is fixed. Exact global model minimization and real arithmetic are free.

**Status.** Optimal

**Lower bound.** B2

$$
c(\sigma_1R/\varepsilon_f)^2
$$

**Upper bound.** B1

$$
C_k[1+(\sigma_1R/\varepsilon_f)^2+\sum_{j=2}^k(\sigma_jR^j/\varepsilon_f)^{1/j}+(M_kR^{k+1}/\varepsilon_f)^{1/(k+1)}]
$$

**Gap or comparison.** $O_k(1)$

### R2 - Complement of the joint small-noise region

**Region.** $\Theta_{\rm all}\setminus\Theta_{\rm noise}$

**Quantity.** Q2

**Resource.** Each complete response through order k costs one call. Each iteration uses a constant number of responses, with the constant allowed to depend on fixed k, and the iteration budget is fixed. Exact global model minimization and real arithmetic are free.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
C_k[1+(\sigma_1R/\varepsilon_f)^2+\sum_{j=2}^k(\sigma_jR^j/\varepsilon_f)^{1/j}+(M_kR^{k+1}/\varepsilon_f)^{1/(k+1)}]
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** After selecting any $x\in\mathbb{R}^d$, a fresh sample returns the complete tensor tuple $(g_j(x))_{j=1}^k$. Conditional on the history $\mathcal{H}$,

**Guarantee mapping.** Expected-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete stochastic response specified under ORACLE costs one unit; each fresh-sample response within a batch is charged separately.

### B1 - Accelerated stochastic tensor method

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C_k[1+(\sigma_1R/\varepsilon_f)^2+\sum_{j=2}^k(\sigma_jR^j/\varepsilon_f)^{1/j}+(M_kR^{k+1}/\varepsilon_f)^{1/(k+1)}]
$$

**Sources.** [1](https://arxiv.org/pdf/2309.01570v3)

**Conditions.** $k\ge3,\ R,M_k,\varepsilon_f>0,\ \sigma_j\ge0$

**Dimension conditions.** $k\ge3,\ R,M_k,\varepsilon_f>0,\ \sigma_j\ge0$

**Source location.** [1](https://arxiv.org/pdf/2309.01570v3) theorem: Theorem 5.6, first bullet; Assumptions 5.1/5.3; exact subproblem τ=0; pdf pages: 7

### B2 - Quadratic with an unknown linear term; high-order responses are deterministic and reveal no sign information

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c(\sigma_1R/\varepsilon_f)^2
$$

**Conditions.** $\Theta_{all}\cap\{\sigma_1>0\}$

**Dimension conditions.** $\Theta_{all}\cap\{\sigma_1>0\}$

**Local argument.** A1

## 5. Local arguments

### A1 - Gaussian testing lower bound with minimizer localization

**Scope.** Arbitrary adaptive randomized complete-derivative algorithms, with fixed cap, expected objective accuracy, positive gradient noise, and no exact values.

**Algorithm scope.** Arbitrary adaptive randomized complete-derivative algorithms, with fixed cap, expected objective accuracy, positive gradient noise, and no exact values.

For full-space convex objectives with a minimizer within R, complete high-order stochastic derivatives without values require $\Omega(\sigma_1^2R^2/\varepsilon_f^2)$ calls.

Let $x_0=0$, hidden sign $s\in\{-1,+1\}$, and $f_s(x)=\lambda(x-sR)^2/2$ with $\lambda=8\varepsilon_f/R^2$. The minimizer is $sR$. All derivatives of order at least two are sign-independent, and every highest-order Lipschitz modulus for $k\ge2$ is zero. After subtracting $\lambda x$ from the noisy gradient, each observation is a Gaussian with mean $-s\lambda R$ and variance $\sigma_1^2$. Even granting $\lambda$ publicly can only help the algorithm, and adaptive queries do not increase the per-call KL divergence.

Use the sign of the output as a test. A wrong sign puts it at distance at least R from the true minimizer, giving gap at least $\lambda R^2/2$. The equal-prior Bayes risk is therefore at least
$$\lambda R^2(1-\operatorname{TV})/4=2\varepsilon_f(1-\operatorname{TV}).$$
For $T\le\sigma_1^2R^2/(1024\varepsilon_f^2)$, total variation is at most 1/4, contradicting expected gap at most $\varepsilon_f$ on both instances.

This construction uses no lower-order curvature cap. If an additional $\beta$ bound is imposed, the extra window $\lambda\le\beta$ must be checked. Exact function values would reveal additional sign information and are excluded.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] Artem Agafonov; Dmitry Kamzolov; Alexander Gasnikov; Ali Kavis; Kimon Antonakopoulos; Volkan Cevher; Martin Takáč. Advancing the Lower Bounds: An Accelerated, Stochastic, Second-order Method with Optimal Adaptation to Inexactness. ICLR 2024; arXiv:2309.01570v3 (2024-05-26).

https://arxiv.org/pdf/2309.01570v3
