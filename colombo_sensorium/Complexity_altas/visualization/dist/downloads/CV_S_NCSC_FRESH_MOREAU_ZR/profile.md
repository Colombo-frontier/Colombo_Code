# Nonconvex–strongly concave minimax: Moreau stationarity with zero-respecting fresh gradients

**Setting ID.** `CV_S_NCSC_FRESH_MOREAU_ZR`

Minimax optimization

Minimize the worst-case joint-gradient call cap for expected Moreau-envelope stationarity under a public dual box and a primal–dual initialization-gap budget.

**Status.** Other quantified gap present; Bounds missing

**TASK tags.** task family: Minimax; formulation: Minimize value function; solution concept: Moreau envelope gradient

**MODEL tags.** convexity: Nonconvex strongly concave; smoothness: Population gradient lipschitz

**ORACLE tags.** operation: Stochastic joint gradient; feedback quality: Stochastic

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: Zero respecting

**OUTPUT tags.** object: Primal point; support: Zero respecting

**METRIC tags.** criterion: Moreau envelope gradient

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** measure: N grad; budget: Fixed worst-case budget

## 1. Setting specification

### Task

$$
\Phi(x)=\max_{y\in\mathcal Y}f(x,y),\qquad\min_{x\in\mathbb R^{d_x}}\Phi(x).
$$

### Admissible model

Let $\mathcal Y$ be a public bounded coordinate box containing the origin. The start is $(x_0,y_0)=(0,0)$. The unknown payoff $f$ is $C^2$ on a neighborhood of $\mathbb R^{d_x}\times\mathcal Y$ and jointly $L$-smooth on this domain in the Euclidean norm.

For every $x$, the function $f(x,\cdot)$ is $\mu$-strongly concave on $\mathcal Y$. For every $y\in\mathcal Y$, the function $f(\cdot,y)$ is bounded below. There is no primal convexity assumption.

The public budget $G$ bounds the initial primal–dual gap. This is the gap between the best dual value at the initial primal point and the smallest primal value at the initial dual point.

$$
G_0=\max_{y\in\mathcal Y}f(0,y)-\inf_{x\in\mathbb R^{d_x}}f(x,0)\le G.
$$

### Oracle interface

Public inputs are the block dimensions $d_x,d_y$, the box endpoints, $L,\mu,G,\sigma,\varepsilon$, and the origin start.

At an adaptively chosen feasible point $(x,y)$, receive one fresh full vector $G_f(x,y;\xi)=(G_x,G_y)$. Conditional on the previous transcript and the current query, its mean is $\nabla f(x,y)$ and its expected squared Euclidean error is at most $\sigma^2$.

The two blocks may be dependent within the response. The sample is independent of earlier samples and cannot be reused at a second query point. The oracle response need not be the gradient of a scalar sample loss.

Projection onto $\mathcal Y$ uses the public box endpoints. The payoff, inner maximizers, and the Moreau gradient are hidden.

### Output

Return a single primal vector $\widehat x$. Every nonzero coordinate of $\widehat x$ must have appeared in a primal response. A dual vector or a certificate is unnecessary.

### Loss or accuracy criterion

Set $\eta=1/(2L)$ and define the Moreau envelope of the primal value by

$$
\Phi_\eta(x)=\min_{z\in\mathbb R^{d_x}}\left\{\Phi(z)+\frac{\|z-x\|_2^2}{2\eta}\right\}.
$$

Evaluate the unsquared norm $\|\nabla\Phi_{\eta}(\widehat x)\|_2$. The proximal point in this definition is part of the evaluation criterion.

### Resource accounting

One full joint-gradient sample costs one $N_{\rm grad}$ call. Both blocks are returned together and do not count as two calls.

Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

The first query is at the origin and the zero-query output is zero. Each later primal and dual query block is supported on the union of coordinates observed in its own response block. The output is supported on the observed primal union.

The algorithm can adapt to all past responses and use private randomness independent of the samples. Discovered coordinates can return to zero. The restriction uses the union over the full history.

For each fixed feasible instance and oracle law, $\mathbb E\|\nabla\Phi_\eta(\widehat x)\|_2\le\varepsilon$. The expectation is over the algorithm's private randomness and the fresh oracle samples.

**Budget convention.** fixed worst-case query cap

## 2. Notation and parameters

$d$: Total Euclidean dimension. Each block dimension is public and the comparison takes the worst case over all finite dimensions. **Domain:** Integer at least $2$.

$d=d_x+d_y$

$L$: Joint population gradient Lipschitz constant on the product domain. **Domain:** Positive real number.

$\|\nabla f(z)-\nabla f(w)\|_2\le L\|z-w\|_2$.

$\mu$: Uniform strong concavity modulus of the lower block. **Domain:** $0<\mu\le L$.

$f(x,\cdot)$ is $\mu$-strongly concave on $\mathcal Y$.

$\kappa$: Ratio of joint gradient smoothness to dual strong concavity. **Domain:** $\kappa\ge1$.

$\kappa=L/\mu$.

$G$: Public upper bound on the initial primal–dual gap. **Domain:** Positive real.

$G_0=\max_{y\in\mathcal Y}f(0,y)-\inf_{x\in\mathbb R^{d_x}}f(x,0)\le G$

$\sigma$: Upper bound on the standard deviation of the full vector. **Domain:** Nonnegative real.

$\mathbb E[\|G_t-\mathbb E[G_t\mid\mathcal H_t,z_t]\|_2^2\mid\mathcal H_t,z_t]\le\sigma^2$

$\varepsilon$: Tolerance for the expectation of the unsquared Moreau-gradient norm. **Domain:** Positive real number.

$\mathcal Y$: Public bounded dual box containing zero.

$\Phi_\eta$: Moreau envelope of the primal value.

$\eta=1/(2L)$.

$N_{\rm grad}$: Number of fresh joint-gradient calls.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm grad}(\mathcal A,I,\omega)
$$

**Scope.** Worst case over all admissible finite block dimensions, public boxes, hidden payoffs, and oracle laws.

**Optimization direction.** minimize

The infimum is over zero-respecting methods meeting the expected-norm criterion on every fixed instance. The budget is a deterministic call cap over all instances and execution paths.

### R1 - High accuracy and high noise

**Region.** $\kappa\ge370$, $\varepsilon^2\le LG/(440\cdot370)$, $\sigma\ge\varepsilon$.

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega\!\left(\frac{\kappa L G\sigma^2}{\varepsilon^4}\right)
$$

**Upper bound.** B1

$$
O\!\left(\frac{\kappa L G\sigma^2}{\varepsilon^4}\right)
$$

**Gap or comparison.** Universal constant factor

**Comparison argument.** Upper and lower bounds match up to universal constants under Zhou's Theorem 1.

### R2 - High accuracy and low noise

**Region.** $\kappa\ge370$, $\varepsilon^2\le LG/(440\cdot370)$, $0\le\sigma<\varepsilon$.

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Other quantified gap

**Lower bound.** B4

$$
\Omega\!\left(\frac{LG}{\varepsilon^2}+\frac{\kappa LG\sigma^2}{\varepsilon^4}\right)
$$

**Upper bound.** B3

$$
O\!\left(\frac{\kappa LG}{\varepsilon^2}\right)
$$

**Gap or comparison.** $U/L_{\rm bound}\lesssim\kappa/(1+\kappa\sigma^2/\varepsilon^2)$

**Comparison argument.** The quotient is at most a universal multiple of $\kappa/(1+\kappa\sigma^2/\varepsilon^2)$. The stated bounds do not determine the optimum throughout this window.

### R3 - Outside the certified lower-bound window

**Region.** $\kappa<370$ or $\varepsilon^2>LG/(440\cdot370)$.

**Quantity.** Q1

**Resource.** The number of gradient-interface responses.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5

$$
O\!\left(\kappa\max\{1,\sigma^2/\varepsilon^2\}\left(1+LG/\varepsilon^2\right)\right)
$$

**Comparison argument.** The SAPD+ upper bound is available here. No matching lower bound is certified by the cited construction.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** All finite dimensions for the upper. The lower uses a finite hard dimension depending on parameters.

**Oracle mapping.** Each partial gradient can use one independent joint response with the other block discarded. The lower already returns a full vector.

**Guarantee mapping.** The expected unsquared envelope-gradient norm is the target. The upper uses Jensen on the averaged squared-norm estimate.

**Output mapping.** The returned primal point satisfies the blockwise support rule.

**Resource mapping.** Count all fresh responses under a deterministic worst-case cap.

### B1 - SAPD+ with a uniformly selected outer iterate and support-preserving projection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** SAPD+ selects an independent uniform outer index.

$$
O\!\left(\frac{\kappa L G\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.30877) [2](https://arxiv.org/abs/2205.15084v4)

**Conditions.** $\kappa\ge370$, $\varepsilon^2\le LG/(440\cdot370)$, $\sigma\ge\varepsilon$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
O\!\left(\frac{\kappa L G\sigma^2}{\varepsilon^4}\right)
$$

**Constants.** Universal constants in the stated windows.

**Source location.** [1](https://arxiv.org/pdf/2609.30877) theorem: Section 6.2 Eq. (32) and Appendix D; pdf pages: 11; 12; 17; 18

The upper proof specializes SAPD+ Theorems 1 and 3, uses a public projection, and counts independent joint-gradient responses.

### B2 - Dual probability zero-chain and constant-factor transfer to the Moreau envelope

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** zero_respecting

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega\!\left(\frac{\kappa L G\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.30877)

**Conditions.** $\kappa\ge370$, $\varepsilon^2\le LG/(440\cdot370)$, $\sigma\ge\varepsilon$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
\Omega\!\left(\frac{\kappa L G\sigma^2}{\varepsilon^4}\right)
$$

**Constants.** Universal constants in the stated windows.

**Source location.** [1](https://arxiv.org/pdf/2609.30877) theorem: Theorem 1 and its Section 6.2 proof; pdf pages: 6; 11; 12

The controlled cross derivatives on the hard instance allow the primal-gradient lower bound to transfer to the Moreau gradient at the returned point.

### B3 - SAPD+ with a uniformly selected outer iterate and support-preserving projection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** SAPD+ selects an independent uniform outer index.

$$
O\!\left(\frac{\kappa LG}{\varepsilon^2}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.30877) [2](https://arxiv.org/abs/2205.15084v4)

**Conditions.** $\kappa\ge370$, $\varepsilon^2\le LG/(440\cdot370)$, $0\le\sigma<\varepsilon$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
O\!\left(\frac{\kappa LG}{\varepsilon^2}\right)
$$

**Constants.** Universal constants in the stated windows.

**Source location.** [1](https://arxiv.org/pdf/2609.30877) theorem: Section 6.2 Eq. (32) and Appendix D; pdf pages: 11; 12; 17; 18

The upper proof specializes SAPD+ Theorems 1 and 3, uses a public projection, and counts independent joint-gradient responses.

### B4 - Dual probability zero-chain and constant-factor transfer to the Moreau envelope

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** zero_respecting

**Algorithm-scope qualification.** The verified source theorem allows arbitrary randomized adaptive algorithms. Domain, output, dimension, and fixed-budget conditions remain those of the specification and region.

$$
\Omega\!\left(\frac{LG}{\varepsilon^2}+\frac{\kappa LG\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.30877)

**Conditions.** $\kappa\ge370$, $\varepsilon^2\le LG/(440\cdot370)$, $0\le\sigma<\varepsilon$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
\Omega\!\left(\frac{LG}{\varepsilon^2}+\frac{\kappa LG\sigma^2}{\varepsilon^4}\right)
$$

**Constants.** Universal constants in the stated windows.

**Derivation.** Repeat the lower-bound transfer in Section 6.2 with $\Delta'=G/1.14$ and target $2\varepsilon$. The application of Theorem 2 precedes the high-noise simplification. Keeping both terms yields the displayed bound.

**Source location.** [1](https://arxiv.org/pdf/2609.30877) theorem: Theorem 2, Lemmas 3 and 6, and Section 6.2; pdf pages: 6; 9; 10; 11; 12

The controlled cross derivatives on the hard instance allow the primal-gradient lower bound to transfer to the Moreau gradient at the returned point.

### B5 - SAPD+ with a uniformly selected outer iterate and support-preserving projection

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** SAPD+ selects an independent uniform outer index.

$$
O\!\left(\kappa\max\{1,\sigma^2/\varepsilon^2\}\left(1+LG/\varepsilon^2\right)\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.30877) [2](https://arxiv.org/abs/2205.15084v4)

**Conditions.** $\kappa<370$ or $\varepsilon^2>LG/(440\cdot370)$.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N grad.**

$$
O\!\left(\kappa\max\{1,\sigma^2/\varepsilon^2\}\left(1+LG/\varepsilon^2\right)\right)
$$

**Constants.** Universal constants in the stated windows.

**Source location.** [1](https://arxiv.org/pdf/2609.30877) theorem: Section 6.2 Eq. (32) and Appendix D; pdf pages: 11; 12; 17; 18

The upper proof specializes SAPD+ Theorems 1 and 3, uses a public projection, and counts independent joint-gradient responses.

## References

[1] Qihao Zhou. Tight Stochastic Condition-Number Dependence in Nonconvex-Strongly-Concave Minimax Optimization. 2026. arXiv:2609.30877v1, 25 September 2026.

https://arxiv.org/pdf/2609.30877

[2] Xuan Zhang; Necdet Serhat Aybat; Mert Gürbüzbalaban. SAPD+: An Accelerated Stochastic Method for Nonconvex-Concave Minimax Problems. 2024. arXiv:2205.15084v4, 13 October 2024.

https://arxiv.org/abs/2205.15084v4
