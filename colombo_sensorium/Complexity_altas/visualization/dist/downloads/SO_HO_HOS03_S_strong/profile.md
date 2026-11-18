# Stochastic strongly convex objective accuracy: complete high-order tensors with strong convexity and orderwise mean-square errors

**Setting ID.** `SO_HO_HOS03_S_strong`

Single-objective optimization

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

**Status.** Other quantified gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; geometry: Euclidean ball; geometry: Full space; smoothness: Higher order lipschitz

**ORACLE tags.** access order: Higher-order interface; feedback quality: Stochastic; interface family: Fresh full k derivative tuple; operation: Fresh full k derivative tuple; public information: Hidden objects explicitly declared; public information: Known lower bound; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Solve $\min_{x\in \mathbb{R}^d}f(x)$ to obtain an objective-value approximation relative to the global infimum.

### Admissible model

The objective $f:\mathbb{R}^d\to\mathbb{R}$ is convex and $C^k$, with $k\ge2$.

$$\|D^{k}f(x)-D^{k}f(y)\|_{\mathrm{op},2}\le M_k\|x-y\|_{2}.$$

There exists a global minimizer $x^*$ satisfying $\|x^*-x_0\|_2\le R$.

Also assume global $\mu$-strong convexity: $\nabla^2f(x)\succeq\mu I_d$ and $\mu>0$.

The objective has a finite infimum, and the public initial point $x_0$ satisfies $f(x_0)-\inf_{x\in \mathbb{R}^d}f(x)\le\Delta$.

### Oracle interface

After selecting any $x\in\mathbb{R}^d$, a fresh sample returns the complete tensor tuple $(g_j(x))_{j=1}^k$. Conditional on the history $\mathcal{H}$,

$$\mathbb{E}[g_1(x)\mid\mathcal{H}]=\nabla f(x),\qquad\mathbb{E}[\|g_j(x)-D^jf(x)\|_{\mathrm{op}}^2\mid\mathcal{H}]\le\sigma_j^2\quad(1\le j\le k).$$

Derivative estimates of order two and higher may be biased. Different orders in one reply may be correlated and need not derive from a common scalar sample loss. Calls use independent fresh samples without reuse; no value channel is provided.

The public inputs are $x_0$, the target accuracy, and $d$, $k$, $R$, $\mu$, $M_k$, $\Delta$, $(\sigma_j)$, $\varepsilon_f$, $\sigma_1$. Numerical constants are admissible bounds and need not equal the sharp constants of the instance. The objective, unqueried derivatives, minimizer and minimum value are hidden.

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

$I_d$: The identity matrix in dimension $d$.

$A\preceq B$: Loewner order: the symmetric matrix $B-A$ is positive semidefinite.

$d$: Ambient dimension; dimension requirements are stated separately for each bound. **Domain:** $d\in\mathbb{N}_{\ge 1}$.

$k$: Maximum order of the query interface and Taylor model; this integer is fixed before other parameters are compared. **Domain:** $k\in\mathbb{N}_{\ge 2}$.

$R$: Upper bound on the distance from the known initial point to at least one global minimizer. **Domain:** $R>0$.

$\mu$: Strong-convexity parameter **Domain:** $\mu>0$.

$M_k$: Global Lipschitz upper bound for the order-$k$ derivative in the tensor operator norm. **Domain:** $M_k>0$.

$\Delta$: Upper bound on the difference between the objective value at the known initial point and its global infimum. **Domain:** $\Delta>0$.

$(\sigma_j)$: Root-error bounds by derivative order **Domain:** $(\sigma_j)\in\mathbb{R}_{\ge0}^k$.

$\varepsilon_f$: Accuracy **Domain:** $\varepsilon_f>0$.

$\sigma_1$: First coordinate of the derivative-noise vector, used for numerical regime classification **Domain:** $\sigma_1\ge0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** Number of complete order-k replies. The achievable baseline uses a fixed budget. The original AG24 restart controls expected runtime and uses an unknown radius, so it is retained separately as a candidate.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Statistical lower-bound window

**Region.** $0<\varepsilon_f\le\min\{\mu R^2/8,\Delta/4\},\quad\sigma_1>0$

**Quantity.** Q1

**Resource.** Number of complete order-k replies. The achievable baseline uses a fixed budget. The original AG24 restart controls expected runtime and uses an unknown radius, so it is retained separately as a candidate.

**Status.** Other quantified gap

**Lower bound.** B2

$$
c\sigma_1^2/(\mu\varepsilon_f)
$$

**Upper bound.** B1

$$
C_k[1+(\sigma_1R/\varepsilon_f)^2+\sum_{j=2}^k(\sigma_jR^j/\varepsilon_f)^{1/j}+(M_kR^{k+1}/\varepsilon_f)^{1/(k+1)}]
$$

**Gap or comparison.** $O_k\!\left(\frac{\mu\varepsilon_f}{\sigma_1^2}\left[1+\left(\frac{\sigma_1R}{\varepsilon_f}\right)^2+\sum_{j=2}^{k}\left(\frac{\sigma_jR^j}{\varepsilon_f}\right)^{1/j}+\left(\frac{M_kR^{k+1}}{\varepsilon_f}\right)^{1/(k+1)}\right]\right)$

### R2 - The known initial-gap bound already meets the target

**Region.** $\varepsilon_f\ge\Delta$

**Quantity.** Q1

**Resource.** Number of complete order-k replies. The achievable baseline uses a fixed budget. The original AG24 restart controls expected runtime and uses an unknown radius, so it is retained separately as a candidate.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** After selecting any $x\in\mathbb{R}^d$, a fresh sample returns the complete tensor tuple $(g_j(x))_{j=1}^k$. Conditional on the history $\mathcal{H}$,

**Guarantee mapping.** Expected-error guarantee for every instance

**Output mapping.** Return $\widehat{x}\in \mathbb{R}^d$.

**Resource mapping.** Each complete stochastic response specified under ORACLE costs one unit; each fresh-sample response within a batch is charged separately.

### B1 - Convex stochastic-tensor baseline using admissible public inputs

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
C_k[1+(\sigma_1R/\varepsilon_f)^2+\sum_{j=2}^k(\sigma_jR^j/\varepsilon_f)^{1/j}+(M_kR^{k+1}/\varepsilon_f)^{1/(k+1)}]
$$

**Sources.** [1](https://arxiv.org/pdf/2309.01570v3)

**Conditions.** $k\ge2,\ \mu,R,M_k,\Delta,\varepsilon_f>0$

**Dimension conditions.** $k\ge2,\ \mu,R,M_k,\Delta,\varepsilon_f>0$

**Source location.** [1](https://arxiv.org/pdf/2309.01570v3) theorem: Theorem 5.6, ignoring strong convexity; pdf pages: 7

### B2 - One-dimensional Gaussian mean estimation

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\sigma_1^2/(\mu\varepsilon_f)
$$

**Conditions.** $0<\varepsilon_f\le\min\{\mu R^2/8,\Delta/4\},\quad\sigma_1>0$

**Dimension conditions.** $0<\varepsilon_f\le\min\{\mu R^2/8,\Delta/4\},\quad\sigma_1>0$

**Local argument.** A1

### B3 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A2

### B4 - Nonnegativity of oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon_f\ge\Delta$

**Dimension conditions.** $\varepsilon_f\ge\Delta$

**Local argument.** A2

## 5. Local arguments

### A1 - Strongly convex Gaussian testing lower bound

**Scope.** Strong convexity, positive gradient noise, expected gap, fixed query cap, and the explicit localization/initial-gap window.

**Algorithm scope.** Strong convexity, positive gradient noise, expected gap, fixed query cap, and the explicit localization/initial-gap window.

Within $\varepsilon_f\le\min\{\mu R^2/8,\Delta/4\}$, expected objective accuracy requires $\Omega(\sigma_1^2/(\mu\varepsilon_f))$ complete stochastic-derivative calls.

Take $f_s(x)=\mu(x-sa)^2/2$ with $a^2=8\varepsilon_f/\mu$. The stated window ensures $a\le R$ and initial gap $\mu a^2/2=4\varepsilon_f\le\Delta$. The noisy gradient hides mean $\pm\mu a$; the exact Hessian $\mu$ and all higher derivatives reveal no sign.

The same sign test gives Bayes gap risk at least $2\varepsilon_f(1-\operatorname{TV})$. For $T\le\sigma_1^2/(128\mu\varepsilon_f)$, the two Gaussian transcript laws have $\operatorname{TV}\le1/4$, so the risk exceeds $\varepsilon_f$. This proves the statistical lower bound for arbitrary randomized algorithms without an exact value channel.

This argument certifies only the statistical difficulty. It does not certify a candidate restart algorithm that requires hidden distances to the minimizer or provides only an expected work analysis when the specification demands a fixed cap.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

### A2 - Zero-query and polynomial-recovery endpoints

**Scope.** Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

**Algorithm scope.** Applies only to the indicated objective-gap, first-order, or spectral second-order criteria. A true minimizer need not satisfy a finite-radius high-order Taylor-decrease criterion; those criteria require their own argument. Public-domain, curvature, and accuracy conditions remain those of the linked bound.

Zero-query guarantees follow from a public initial-error bound. A zero highest-order regularity modulus permits exact polynomial recovery from one complete jet.

For a full-space differentiable objective with $f(x_0)-\inf f\le\Delta$, the condition $\Delta=0$ makes $x_0$ a global minimizer. Its gradient is zero, and its Hessian is positive semidefinite whenever it exists. Thus first-order and spectral second-order stationarity require no query. An objective-gap target also requires no query when $\varepsilon_f\ge\Delta$. Nonnegative query cost proves exact optimality of these zero bounds.

If a public gradient-Lipschitz bound $\beta$ is part of the specification, the descent lemma gives $\|\nabla f(x_0)\|^2\le2\beta\Delta$. For convex full-space objectives with a minimizer within distance $R$, it also gives $f(x_0)-f^*\le\beta R^2/2$ and $\|\nabla f(x_0)\|\le\beta R$. These sufficient zero-query regions require that explicit first-order regularity assumption. If only the highest derivative is controlled, positive quadratics can have arbitrary curvature and arbitrarily large initial gap despite zero highest-order modulus.

On a connected Euclidean domain, $M_k=0$ or $M_{k,\nu}=0$ makes $D^kf$ constant, so $f$ is a polynomial of degree at most $k$. One complete jet determines all coefficients. Under the specified free internal computation, a known polynomial can then be optimized on a compact public domain, or combined with a public regularizer and solved through the declared known-model interface.

A bounded-below polynomial on the full space need not attain its infimum. For approximate spectral stationarity, shift $x_0$ to zero and minimize $f(x)+\eta\|x\|^2/2$. This function is coercive, and its minimizer $x_\eta$ satisfies $\eta\|x_\eta\|^2/2\le\Delta$, $\|\nabla f(x_\eta)\|\le\sqrt{2\eta\Delta}$, and $\nabla^2f(x_\eta)\succeq-\eta I$. Choosing $\eta\le\min\{\varepsilon_H,\varepsilon_g^2/(2\Delta)\}$ meets both targets. For global objective accuracy, exact polynomial coefficients permit arbitrary-accuracy internal global optimization; no additional unknown-function query is needed.

To exclude zero queries in a nontrivial region, choose two positive quadratics centered on opposite sides of $x_0$, with the same public budgets and disjoint acceptable-output sets. A zero-query algorithm has the same output distribution on both instances, so their success probabilities sum to at most one. It cannot succeed with probability at least $2/3$ on each. With only highest-order regularity, curvature can be increased until the acceptable sets are disjoint at any prescribed positive accuracy and positive localization radius. In an initial-gap model with additional curvature restrictions, retain the bound's explicit accuracy and compatibility window.

If both a global PL constant $\mu$ and a gradient-Lipschitz upper bound $\beta$ are supplied, then $2\mu(f-f_*)\le\|\nabla f\|^2\le2\beta(f-f_*)$. When $\mu>\beta>0$, every gap is zero and the class contains only constant objectives. This degeneracy does not apply without the extra $\beta$ assumption.

**Limits of the argument.** The mapped bound retains its complete model, oracle, algorithm view, guarantee, quantity, resource projection, and parameter-region conditions. This argument does not enlarge that scope.

## References

[1] Artem Agafonov; Dmitry Kamzolov; Alexander Gasnikov; Ali Kavis; Kimon Antonakopoulos; Volkan Cevher; Martin Takáč. Advancing the Lower Bounds: An Accelerated, Stochastic, Second-order Method with Optimal Adaptation to Inexactness. ICLR 2024; arXiv:2309.01570v3 (2024-05-26).

https://arxiv.org/pdf/2309.01570v3
