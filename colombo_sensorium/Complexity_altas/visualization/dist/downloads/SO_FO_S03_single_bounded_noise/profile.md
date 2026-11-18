# Smooth nonconvex stationarity: fresh gradients with uniformly bounded noise

**Setting ID.** `SO_FO_S03_single_bounded_noise`

Single-objective optimization

The oracle returns one unbiased gradient estimate per independent sample. A single probability-one set gives the same error bound simultaneously at every query point. The bracket takes the worst case over finite dimensions.

**Status.** Fully optimal

**TASK tags.** task family: Single objective; formulation: First order stationarity

**MODEL tags.** convexity: Convexity not assumed; geometry: Full space; smoothness: Lipschitz gradient

**ORACLE tags.** access order: First-order interface; feedback quality: Stochastic; operation: Stochastic gradient

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed

**OUTPUT tags.** object: Point

**METRIC tags.** criterion: Gradient norm

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** measure: Samples; budget: Fixed worst-case budget

## 1. Setting specification

### Task

Find a point satisfying the stationarity criterion specified under the accuracy measure.

$$\min_{x\in \mathbb{R}^d}f(x)$$

### Admissible model

The hidden objective $f:\mathbb R^d\to\mathbb R$ is globally differentiable, bounded below, and has $\beta$-Lipschitz gradient in the Euclidean norm. The public starting point $x_0$ satisfies $f(x_0)-\inf f\le\Delta$.

The brackets below concern positive budgets $\beta,\Delta,\sigma$ and the high-accuracy regime $0<\varepsilon\le 2^{-20}\min\{\sigma,\sqrt{\beta\Delta}\}$. The lower-bound dimension is allowed to grow with the accuracy and query budget.

### Oracle interface

A query selects an arbitrary $x\in\mathbb R^d$ and receives only the full stochastic vector $g(x,Z)$. The map $g$ is jointly Borel and unbiased at every $x$.

There exists a single measurable set $\mathcal Z_0$ of probability one on which $\|g(x,z)-\nabla f(x)\|_2\le\sigma$ holds simultaneously for all $x$. Each response uses a fresh independent draw from the same hidden law. Samples cannot be reused.

The interface imposes neither continuity of the sample map nor an obligation to return a gradient of a scalar sample function.

### Output

Return a point $\widehat x\in\mathbb R^d$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(I,\widehat{x})=\|\nabla f(\widehat{x})\|_2$$

$\varepsilon$ is a gradient-norm tolerance. Expected norm and expected squared norm are different performance requirements.

### Resource accounting

One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

The algorithm may use private randomness independent of the fixed problem instance and oracle samples.

Queries and the final output are arbitrary measurable functions of the transcript and private seed. There is no span, zero-respecting, or bounded-query-radius restriction.

The response cap is fixed uniformly over all execution paths. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\forall I\,\forall\mathcal{O}\in\mathcal{O}(I):\ \mathbb{E}_{A,\mathcal{O}}\ell(I,\widehat{x})\le\varepsilon$$

The probability space includes observation noise and the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in \mathbb{R}^d$.

$f$: Unknown objective, with domain and structure specified by the model

$\nabla f$: Full gradient of the differentiable objective or smooth term with respect to the decision variable

$x_0$: Public initial point satisfying the stated initial-distance or initial-suboptimality condition

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in \mathbb{R}^d}f(x)$$

$d$: Ambient Euclidean dimension, public in each instance. The bracket takes the supremum over finite dimensions. **Domain:** $d\in\mathbb{N}_{\ge1}$.

$\beta$: Public upper bound on the gradient smoothness constant. Any mean-square interpretation is specified in the model. **Domain:** $\beta>0$.

$\Delta$: Public upper bound on initial suboptimality. **Domain:** $\Delta>0$.

$\sigma$: Uniform almost-sure bound on the Euclidean norm of the centered stochastic gradient error. **Domain:** $\sigma>0$.

$\|g(x,z)-\nabla f(x)\|_2\le\sigma$ for all $x$ on one common probability-one set.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Worst-case fixed cap over every finite dimension, admissible objective and fixed oracle law. The dimension is public to the algorithm.

### R1 - Uniformly bounded noise, high accuracy, dimension-free minimax

**Region.** $\beta,\Delta,\sigma>0$, $0<\varepsilon\le 2^{-20}\min\{\sigma,\sqrt{\beta\Delta}\}$, worst case over finite dimensions.

**Quantity.** Q1

**Resource.** One full stochastic-gradient sample costs one call; a batch of $b$ samples costs $b$ calls.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Upper bound.** B1

$$
O\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The upper and lower bounds match up to universal constants in the dimension-free minimax comparison.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Conditions.** $\beta,\Delta,\sigma>0$, $0<\varepsilon\le 2^{-20}\min\{\sigma,\sqrt{\beta\Delta}\}$, worst case over finite dimensions.

**Oracle mapping.** The native access is one full stochastic gradient per fresh draw from a fixed law, with uniform almost-sure bounded centered error.

**Output mapping.** Arbitrary measurable point of the Euclidean space.

**Resource mapping.** One sample per response, fixed worst-case cap. The lower bound permits fewer queries by padding the transcript.

### B1 - Randomized-output stochastic gradient descent with a fixed sample budget

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/1309.5549)

**Dimension conditions.** Uniform over all finite dimensions.

**Guarantee conversion.** On each fixed instance, expectation is over oracle draws and private randomness. A squared-gradient upper bound at tolerance squared implies this expected-norm upper bound by Jensen.

**Source location.** [2](https://arxiv.org/pdf/1309.5549) theorem: Corollary 2.2, Equation (2.14); pdf pages: 8; printed pages: 8

The uniform almost-sure error bound gives the second-moment bound $\sigma^2$. Choosing $\widetilde D=\sqrt{2\Delta/\beta}$ in the source gives $\mathbb E\|\nabla f(x_R)\|_2^2\le2\beta\Delta/N+2\sqrt{2\beta\Delta}\,\sigma/\sqrt N$. Set this at most $\varepsilon^2$ and use Jensen.

### B2 - Jin's bounded sign-channel lower bound for unrestricted randomized algorithms

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(\frac{\beta\Delta}{\varepsilon^2}+\frac{\beta\Delta\sigma^2}{\varepsilon^4}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2608.09004v1)

**Dimension conditions.** For each prescribed query budget in the lower-bound window the source constructs a finite dimension depending on the budget and public parameters, prior to choosing the algorithm on that space.

**Guarantee conversion.** On each fixed instance, expectation is over oracle draws and private randomness. The source directly lower bounds the expected gradient norm.

**Source location.** [1](https://arxiv.org/pdf/2608.09004v1) theorem: Definition 3.1, Theorem 4.1, Lemma 7.1, Equation (85); pdf pages: 3; 10; 21; printed pages: 3; 10; 21

The source's hard oracle uses independent product-uniform samples. Its bounded sign response and uniformly bounded mean correction give one error bound for every point and sample. The sequential information argument handles arbitrary adaptive queries and outputs.

## References

[1] Jikai Jin. A Tight Lower Bound for Smooth Nonconvex Stochastic Optimization with Bounded Gradient Noise. arXiv:2608.09004v1, 10 August 2026.

https://arxiv.org/pdf/2608.09004v1

[2] Saeed Ghadimi and Guanghui Lan. Stochastic First- and Zeroth-order Methods for Nonconvex Stochastic Programming. SIAM Journal on Optimization 23(4), 2013.

https://arxiv.org/pdf/1309.5549
