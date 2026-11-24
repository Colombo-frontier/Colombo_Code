# Lipschitz convex finite-sum minimization with ball-restricted exact component values

**Setting ID.** `SO_ZO_E09c_ball`

Single-objective optimization

Finite-population exact component-value queries are restricted to the feasible Euclidean ball. The expected-error frontier explicitly retains dimension, population size, and accuracy.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Finite sum minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz

**ORACLE tags.** feedback quality: Exact; operation: Component function value; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar function value (order 0)

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Expectation; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N component value

## 1. Setting specification

### Task

Minimize $F(x)=N^{-1}\sum_{i=1}^N f_i(x)$ over the public Euclidean ball $X=B_2(0,R)$ using selected component values.

### Admissible model

Each fixed client function $f_i:X\to\mathbb R$ is finite, convex, and $L$-Lipschitz in the Euclidean norm. Neither smoothness nor a shared minimizer is assumed. No definition or regularity outside $X$ is required. Boundary minimizers are permitted.

The complete tuple $(f_1,\ldots,f_N)$ is fixed before private randomization. Revisiting a client accesses the same function rather than a fresh stochastic loss.

### Oracle interface

One call selects $(i,x)\in\{1,\ldots,N\}\times X$ and returns exactly one scalar $f_i(x)$. Both the client and the feasible point may be selected adaptively. Off-domain queries are not legal.

The public inputs are $d,N,L,R,\varepsilon$. A complete average, a group average, or a two-point difference must be computed from its actual component calls; no aggregate-value interface is supplied for free.

### Output

Return a measurable feasible $\widehat x\in X$, which need not have been queried.

### Loss or accuracy criterion

The loss is $F(\widehat x)-F^\star$, where $F^\star=\min_{x\in X}F(x)$. Only this loss is averaged over the independent private seed.

### Resource accounting

Each selected scalar component value costs one call. The cap holds for every fixed seed and every possible scalar history, including initialization and verification. Internal computation, storage, projection, and operations on public domain geometry are uncharged. Communication rounds are not a resource of this comparison.

### Algorithm views and success guarantees

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall(f_i):\ \mathbb E[F(\widehat x)-F^\star]\le\varepsilon
$$

The expectation is over the algorithmic seed after fixing all client functions. Every query and the output must be feasible, and the total component-value count is capped on every execution.

**Budget convention.** fixed_worst_case

## 2. Notation and parameters

$d$: Ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$N$: Number of fixed client functions **Domain:** $N\in\mathbb N_{\ge1}$.

$L$: Uniform Lipschitz budget for every component **Domain:** $L>0$.

$R$: Radius of the feasible and query ball **Domain:** $R>0$.

$\varepsilon$: Expected objective-error tolerance **Domain:** $\varepsilon>0$.

$\rho$: Normalized inverse accuracy **Domain:** $\rho>0$.

$\rho=LR/\varepsilon$

$\Lambda$: Logarithmic scale **Domain:** $\Lambda>e$.

$\Lambda=e+d+N+\rho$

$d_\star$: Universal dimension threshold **Domain:** $d_\star\in\mathbb N$.

Universal threshold in Theorem thm:main-rate.

$\rho_\star$: Universal inverse-accuracy threshold **Domain:** $\rho_\star\in\mathbb N$.

Universal threshold in Theorem thm:main-rate.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
q_\varepsilon(d,N,L,R)=\inf\{Q:\exists A\text{ with pathwise cap }Q,\ \sup_{(f_i)}\mathbb E[F(\widehat x)-F^*]\le\varepsilon\}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{component\ scalar}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q2 - minimax metric resource quantity

$$
q_\varepsilon(d,N,L,R)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{component\ scalar}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

### R1 - Moderate-accuracy branch

**Region.** $\rho^2\le d+N$; $d\ge d_\star$, $N\ge1$, $L,R>0$, $\rho=LR/\varepsilon\ge\rho_\star$. $d\ge d_\star$, a universal threshold independent of N,L,R and epsilon; no hidden exponential dimensional requirement. The lower bound applies to the ball-restricted interface. It is not transported to full-space queries. Exact real arithmetic and centroid computation are uncharged; the result counts oracle information rather than communication or computational runtime.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
cd\rho^2/\log\Lambda
$$

**Upper bound.** B1

$$
Cd\rho^2\log^2\Lambda
$$

**Gap or comparison.**

$$
O(\log^3\Lambda)
$$

### R2 - High-accuracy finite-population branch

**Region.** $\rho^2\ge d+N$; $d\ge d_\star$, $N\ge1$, $L,R>0$, $\rho=LR/\varepsilon\ge\rho_\star$. $d\ge d_\star$, a universal threshold independent of N,L,R and epsilon; no hidden exponential dimensional requirement. The lower bound applies to the ball-restricted interface. It is not transported to full-space queries. Exact real arithmetic and centroid computation are uncharged; the result counts oracle information rather than communication or computational runtime.

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
cd(d+N)/\log\Lambda
$$

**Upper bound.** B3

$$
Cd(d+N)\log^2\Lambda
$$

**Gap or comparison.**

$$
O(\log^3\Lambda)
$$

### R3 - Sufficient zero-query accuracy

**Region.** $\varepsilon\ge LR$, with $d,N\ge1$ and $L,R>0$. Every d>=1. The matching positive-query theorem uses its own universal dimension and inverse-accuracy thresholds.

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B6

$$
0
$$

**Upper bound.** B5

$$
0
$$

**Gap or comparison.** Exact zero calls in this region.

## 4. Bounds and supporting evidence

### B1 - Choose the smaller of two-point selected-client estimation and balanced-group lifted-epigraph localization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
Cd\rho^2\log^2\Lambda
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf)

**Conditions.** $\rho^2\le d+N$; $d\ge d_\star$, $N\ge1$, $L,R>0$, $\rho=LR/\varepsilon\ge\rho_\star$.; The first branch has an $O(d\rho^2)$ upper bound without the displayed extra logarithms; the displayed common envelope remains valid.; The lower bound applies to the ball-restricted interface. It is not transported to full-space queries.; Exact real arithmetic and centroid computation are uncharged; the result counts oracle information rather than communication or computational runtime.

**Dimension conditions.** $d\ge d_\star$, a universal threshold independent of N,L,R and epsilon; no hidden exponential dimensional requirement.

**Constants.** Universal positive constants, with universal d_star and rho_star.

**Logarithmic factors.** Only powers of $\log(e+d+N+LR/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf) Theorem thm:main-rate, eq:main-rate; Theorem thm:explicit-frontier

Choose the smaller of two-point selected-client estimation and balanced-group lifted-epigraph localization. Unrestricted adaptive randomized algorithms

The first branch has an $O(d\rho^2)$ upper bound without the displayed extra logarithms; the displayed common envelope remains valid.

### B2 - Independent affine client groups and grouped random support functions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
cd\rho^2/\log\Lambda
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf)

**Conditions.** $\rho^2\le d+N$; $d\ge d_\star$, $N\ge1$, $L,R>0$, $\rho=LR/\varepsilon\ge\rho_\star$.; The lower bound applies to the ball-restricted interface. It is not transported to full-space queries.; Exact real arithmetic and centroid computation are uncharged; the result counts oracle information rather than communication or computational runtime.

**Dimension conditions.** $d\ge d_\star$, a universal threshold independent of N,L,R and epsilon; no hidden exponential dimensional requirement.

**Constants.** Universal positive constants, with universal d_star and rho_star.

**Logarithmic factors.** Only powers of $\log(e+d+N+LR/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf) Theorem thm:main-rate, eq:main-rate; Section sec:lower

Independent affine client groups and grouped random support functions. All adaptive randomized selected-client algorithms

### B3 - Choose the smaller of two-point selected-client estimation and balanced-group lifted-epigraph localization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
Cd(d+N)\log^2\Lambda
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf)

**Conditions.** $\rho^2\ge d+N$; $d\ge d_\star$, $N\ge1$, $L,R>0$, $\rho=LR/\varepsilon\ge\rho_\star$.; The first branch has an $O(d\rho^2)$ upper bound without the displayed extra logarithms; the displayed common envelope remains valid.; The lower bound applies to the ball-restricted interface. It is not transported to full-space queries.; Exact real arithmetic and centroid computation are uncharged; the result counts oracle information rather than communication or computational runtime.

**Dimension conditions.** $d\ge d_\star$, a universal threshold independent of N,L,R and epsilon; no hidden exponential dimensional requirement.

**Constants.** Universal positive constants, with universal d_star and rho_star.

**Logarithmic factors.** Only powers of $\log(e+d+N+LR/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf) Theorem thm:main-rate, eq:main-rate; Theorem thm:explicit-frontier

Choose the smaller of two-point selected-client estimation and balanced-group lifted-epigraph localization. Unrestricted adaptive randomized algorithms

The first branch has an $O(d\rho^2)$ upper bound without the displayed extra logarithms; the displayed common envelope remains valid.

### B4 - Independent affine client groups and grouped random support functions

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** randomized_hard_family

$$
cd(d+N)/\log\Lambda
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf)

**Conditions.** $\rho^2\ge d+N$; $d\ge d_\star$, $N\ge1$, $L,R>0$, $\rho=LR/\varepsilon\ge\rho_\star$.; The lower bound applies to the ball-restricted interface. It is not transported to full-space queries.; Exact real arithmetic and centroid computation are uncharged; the result counts oracle information rather than communication or computational runtime.

**Dimension conditions.** $d\ge d_\star$, a universal threshold independent of N,L,R and epsilon; no hidden exponential dimensional requirement.

**Constants.** Universal positive constants, with universal d_star and rho_star.

**Logarithmic factors.** Only powers of $\log(e+d+N+LR/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf) Theorem thm:main-rate, eq:main-rate; Section sec:lower

Independent affine client groups and grouped random support functions. All adaptive randomized selected-client algorithms

### B5 - Return the center of the ball

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf)

**Conditions.** $\varepsilon\ge LR$, with $d,N\ge1$ and $L,R>0$.; The matching positive-query theorem uses its own universal dimension and inverse-accuracy thresholds.

**Dimension conditions.** Every d>=1.

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf) Section sec:model, paragraph immediately before sec:main

Return the center of the ball. Deterministic algorithm

### B6 - Nonnegative query count

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf)

**Conditions.** $\varepsilon\ge LR$, with $d,N\ge1$ and $L,R>0$.; The matching positive-query theorem uses its own universal dimension and inverse-accuracy thresholds.

**Dimension conditions.** Every d>=1.

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf) Section sec:model

Nonnegative query count. All algorithms

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U05. Near-Optimal Oracle Bounds for Distributed Zeroth-Order Convex Optimization. distributed_zeroth_order_colombo.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U05/manuscript.pdf
