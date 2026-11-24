# Ell-p smooth convex optimization with a common minimizer localized in two norms

**Setting ID.** `SO_FO_C05_radius_lp_FG`

Single-objective optimization

A globally ell-p smooth convex objective has one minimizer satisfying simultaneous Euclidean and ell-p radius bounds. Queries and outputs are unrestricted in the full space.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Objective minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz gradient

**ORACLE tags.** feedback quality: Exact; operation: Function value and gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**GUARANTEE tags.** mode: Expectation; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N first order

## 1. Setting specification

### Task

Minimize an unknown convex objective globally on $\mathbb R^d$ using exact function values and full gradients.

### Admissible model

For $2\le p\le\infty$, $f:\mathbb R^d\to\mathbb R$ is convex and differentiable, and $$\|\nabla f(x)-\nabla f(y)\|_{p^*}\le L\|x-y\|_p\qquad(x,y\in\mathbb R^d),$$ where $1/p+1/p^*=1$.

There exists one attained global minimizer $x^\star$ satisfying both $\|x^\star\|_2\le R_2$ and $\|x^\star\|_p\le R_p$. The two bounds concern the same minimizer. They impose no restriction on queries or outputs.

### Oracle interface

At any finite $x\in\mathbb R^d$, one query returns $(f(x),\nabla f(x))$ exactly. The public inputs are $d,p,L,R_2,R_p,\varepsilon$ and, for the probability criterion, $\delta$. The function and a minimizer are hidden.

### Output

Return any measurable point $\widehat x\in\mathbb R^d$ determined by the transcript, possibly unqueried. No value or optimality certificate is required.

### Loss or accuracy criterion

The base loss is $f(\widehat x)-f^\star$, where $f^\star=\min_{x\in\mathbb R^d}f(x)$.

### Resource accounting

One exact bundled value-gradient response costs one call, irrespective of its vector dimension. Every execution uses at most the stated budget. Internal exact arithmetic, storage, and computation on received data are uncharged.

### Algorithm views and success guarantees

#### Deterministic / Pointwise error

The algorithm is deterministic and adaptive. Queries, stopping, and the output may use the complete preceding transcript. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage are uncharged. The stated budget holds on every admissible instance and every response history.

$$
\forall f:\ f(\widehat x)-f^\star\le\varepsilon
$$

The guarantee holds deterministically for every admissible function.

**Budget convention.** fixed_worst_case

#### Randomized / Expected loss

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall f:\ \mathbb E[f(\widehat x)-f^\star]\le\varepsilon
$$

Expectation is over private algorithmic randomization after fixing the objective.

**Budget convention.** fixed_worst_case

#### Randomized / Failure probability delta

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall f:\ \Pr(f(\widehat x)-f^\star>\varepsilon)\le\delta
$$

The requested failure probability is public. One algorithm must satisfy this bound on every admissible objective.

**Budget convention.** fixed_worst_case

## 2. Notation and parameters

$d$: Ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$p$: Smoothness norm exponent **Domain:** $2\le p\le\infty$.

$L$: Global ell-p gradient Lipschitz modulus **Domain:** $L>0$.

$R_2$: Euclidean radius of the common minimizer **Domain:** $R_2>0$.

$R_p$: Ell-p radius of the same minimizer **Domain:** $R_p>0$.

$\varepsilon$: Target objective error **Domain:** $\varepsilon>0$.

$\delta$: Failure probability **Domain:** $0<\delta\le1/3$.

$T$: Worst-case full first-order query budget **Domain:** $T\in\mathbb N_{\ge0}$.

$r$: Smaller scalar localization radius **Domain:** $r>0$.

$r=\min\{R_2,R_p\}$

$H$: Dimension logarithm **Domain:** $H>=1$.

$H=\log(ed)$

$A$: Euclidean acceleration scale **Domain:** $A>0$.

$A=\sqrt{LR_2^2/\varepsilon}$

$B$: Ell-p acceleration scale **Domain:** $B>0$.

$B=(LR_p^2/\varepsilon)^{p/(p+2)}$, with exponent $1$ at $p=\infty$

$S$: Joint dimension-accuracy scale **Domain:** $S>0$.

$S=\min\{d,A,B\}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

**View.** Deterministic / Pointwise error

$$
Q^*_{\rm det}(\varepsilon)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{value+gradient}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q2 - minimax metric resource quantity

**View.** Randomized / Expected loss

$$
Q^*_{\rm exp}(\varepsilon)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{value+gradient}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q3 - minimax metric resource quantity

**View.** Randomized / Failure probability delta

$$
Q^*_{\rm hp}(\varepsilon,\delta)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{value+gradient}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q4 - minimax metric resource quantity

**View.** Deterministic / Pointwise error

$$
\mathcal R_T^{\rm det}=\inf_{A\,\rm det}\sup_f[f(\widehat x)-f^*]
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{value+gradient}}\le T$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q5 - minimax metric resource quantity

**View.** Randomized / Expected loss

$$
\mathcal R_T^{\rm exp}=\inf_A\sup_f\mathbb E[f(\widehat x)-f^*]
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{value+gradient}}\le T$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

### R1 - Joint two-radius frontier in the positive-query range

**Region.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$. All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket. The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Views.** Deterministic / Pointwise error

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
cS/H
$$

**Upper bound.** B1

$$
C\left[1+\min\left\{A,H^2B,d\left(1+\log\frac{Lr^2}{\varepsilon}\right)\right\}\right]
$$

**Gap or comparison.**

$$
O\!\left(H[1+H^2+\log(Lr^2/\varepsilon)]\right)
$$

### R2 - Zero-query accuracy range

**Region.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains. All d>=1. The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Views.** Deterministic / Pointwise error

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B4

$$
0
$$

**Upper bound.** B3

$$
0
$$

**Gap or comparison.** Exact zero-query equality.

### R3 - Joint two-radius frontier in the positive-query range

**Region.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$. All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket. The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B6

$$
cS/H
$$

**Upper bound.** B5

$$
C\left[1+\min\left\{A,H^2B,d\left(1+\log\frac{Lr^2}{\varepsilon}\right)\right\}\right]
$$

**Gap or comparison.**

$$
O\!\left(H[1+H^2+\log(Lr^2/\varepsilon)]\right)
$$

### R4 - Zero-query accuracy range

**Region.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains. All d>=1. The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Views.** Randomized / Expected loss

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B8

$$
0
$$

**Upper bound.** B7

$$
0
$$

**Gap or comparison.** Exact zero-query equality.

### R5 - Joint two-radius frontier in the positive-query range

**Region.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$. All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket. The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Views.** Randomized / Failure probability delta

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B10

$$
cS/H
$$

**Upper bound.** B9

$$
C\left[1+\min\left\{A,H^2B,d\left(1+\log\frac{Lr^2}{\varepsilon}\right)\right\}\right]
$$

**Gap or comparison.**

$$
O\!\left(H[1+H^2+\log(Lr^2/\varepsilon)]\right)
$$

### R6 - Zero-query accuracy range

**Region.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains. All d>=1. The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Views.** Randomized / Failure probability delta

**Quantity.** Q3

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B12

$$
0
$$

**Upper bound.** B11

$$
0
$$

**Gap or comparison.** Exact zero-query equality.

### R7 - Fixed finite p: sharp error before dimension saturation

**Region.** Fix $2\le p<\infty$; $L,R_2,R_p>0$ and integers $1\le T\le d/100$. $d\ge100T$; p is fixed and finite. This constant-factor error statement is not asserted uniformly at $p=\infty$.

**Views.** Deterministic / Pointwise error

**Quantity.** Q4

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B14

$$
c_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Upper bound.** B13

$$
C_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Gap or comparison.**

$$
O_p(1)
$$

### R8 - Fixed finite p: sharp error before dimension saturation

**Region.** Fix $2\le p<\infty$; $L,R_2,R_p>0$ and integers $1\le T\le d/100$. $d\ge100T$; p is fixed and finite. This constant-factor error statement is not asserted uniformly at $p=\infty$.

**Views.** Randomized / Expected loss

**Quantity.** Q5

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B16

$$
c_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Upper bound.** B15

$$
C_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Gap or comparison.**

$$
O_p(1)
$$

## 4. Bounds and supporting evidence

### B1 - Choose among Euclidean acceleration, power-prox acceleration, and finite-dimensional localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** Deterministic witness

$$
C\left[1+\min\left\{A,H^2B,d\left(1+\log\frac{Lr^2}{\varepsilon}\right)\right\}\right]
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$.; The upper bound has no dependence on $\delta$. For each fixed finite $p$, the factor $H^2$ multiplying $B$ can be replaced by a constant depending on $p$.; The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Dimension conditions.** All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket.

**Constants.** The displayed constants are universal, including uniformity in p.

**Logarithmic factors.** $H=\log(ed)$ and the displayed $\log(Lr^2/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Theorem thm:main, eq:main-explicit

Choose among Euclidean acceleration, power-prox acceleration, and finite-dimensional localization. Deterministic unrestricted-query algorithms

The upper bound has no dependence on $\delta$. For each fixed finite $p$, the factor $H^2$ multiplying $B$ can be replaced by a constant depending on $p$.

### B2 - A fixed globally smooth hard distribution controlling exposed affine pieces and posterior information

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** randomized_hard_family

$$
cS/H
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$.; The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Dimension conditions.** All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket.

**Constants.** The displayed constants are universal, including uniformity in p.

**Logarithmic factors.** $H=\log(ed)$ and the displayed $\log(Lr^2/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Theorem thm:main; Theorem thm:distribution; Appendix app:main-theorem

A fixed globally smooth hard distribution controlling exposed affine pieces and posterior information. All unrestricted adaptive randomized algorithms

### B3 - Output the origin

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains.; The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Proposition prop:zero-query

Output the origin. Deterministic algorithm

### B4 - Nonnegativity of the call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains.; The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Proposition prop:zero-query

Nonnegativity of the call budget. All algorithms

### B5 - Choose among Euclidean acceleration, power-prox acceleration, and finite-dimensional localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\left[1+\min\left\{A,H^2B,d\left(1+\log\frac{Lr^2}{\varepsilon}\right)\right\}\right]
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$.; The upper bound has no dependence on $\delta$. For each fixed finite $p$, the factor $H^2$ multiplying $B$ can be replaced by a constant depending on $p$.; The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Dimension conditions.** All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket.

**Constants.** The displayed constants are universal, including uniformity in p.

**Logarithmic factors.** $H=\log(ed)$ and the displayed $\log(Lr^2/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Theorem thm:main, eq:main-explicit

Choose among Euclidean acceleration, power-prox acceleration, and finite-dimensional localization. Deterministic unrestricted-query algorithms

The upper bound has no dependence on $\delta$. For each fixed finite $p$, the factor $H^2$ multiplying $B$ can be replaced by a constant depending on $p$.

### B6 - A fixed globally smooth hard distribution controlling exposed affine pieces and posterior information

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** randomized_hard_family

$$
cS/H
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$.; The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Dimension conditions.** All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket.

**Constants.** The displayed constants are universal, including uniformity in p.

**Logarithmic factors.** $H=\log(ed)$ and the displayed $\log(Lr^2/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Theorem thm:main; Theorem thm:distribution; Appendix app:main-theorem

A fixed globally smooth hard distribution controlling exposed affine pieces and posterior information. All unrestricted adaptive randomized algorithms

### B7 - Output the origin

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains.; The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Proposition prop:zero-query

Output the origin. Deterministic algorithm

### B8 - Nonnegativity of the call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains.; The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Proposition prop:zero-query

Nonnegativity of the call budget. All algorithms

### B9 - Choose among Euclidean acceleration, power-prox acceleration, and finite-dimensional localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Failure probability delta

**Witness or lower-bound scope.** Deterministic witness

$$
C\left[1+\min\left\{A,H^2B,d\left(1+\log\frac{Lr^2}{\varepsilon}\right)\right\}\right]
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$.; The upper bound has no dependence on $\delta$. For each fixed finite $p$, the factor $H^2$ multiplying $B$ can be replaced by a constant depending on $p$.; The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Dimension conditions.** All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket.

**Constants.** The displayed constants are universal, including uniformity in p.

**Logarithmic factors.** $H=\log(ed)$ and the displayed $\log(Lr^2/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Theorem thm:main, eq:main-explicit

Choose among Euclidean acceleration, power-prox acceleration, and finite-dimensional localization. Deterministic unrestricted-query algorithms

The upper bound has no dependence on $\delta$. For each fixed finite $p$, the factor $H^2$ multiplying $B$ can be replaced by a constant depending on $p$.

### B10 - A fixed globally smooth hard distribution controlling exposed affine pieces and posterior information

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Failure probability delta

**Witness or lower-bound scope.** randomized_hard_family

$$
cS/H
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $d\ge1$, $2\le p\le\infty$, $L,R_2,R_p>0$, $0<\varepsilon<Lr^2/2$; for the probability view $0<\delta\le1/3$.; The dimension branch retains its logarithmic accuracy dependence; no accuracy-independent $O(d)$ upper bound is asserted.

**Dimension conditions.** All integer dimensions d>=1; no dimension-growth assumption is needed for this displayed bracket.

**Constants.** The displayed constants are universal, including uniformity in p.

**Logarithmic factors.** $H=\log(ed)$ and the displayed $\log(Lr^2/\varepsilon)$.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Theorem thm:main; Theorem thm:distribution; Appendix app:main-theorem

A fixed globally smooth hard distribution controlling exposed affine pieces and posterior information. All unrestricted adaptive randomized algorithms

### B11 - Output the origin

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Failure probability delta

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains.; The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Proposition prop:zero-query

Output the origin. Deterministic algorithm

### B12 - Nonnegativity of the call budget

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Failure probability delta

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** $\varepsilon\ge L\min\{R_2,R_p\}^2/2$ with the declared parameter domains.; The converse zero-query threshold is also valid; for probability it uses $\delta<1/2$.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Proposition prop:zero-query

Nonnegativity of the call budget. All algorithms

### B13 - Choose acceleration in the better of the two geometries

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** Deterministic witness

$$
C_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** Fix $2\le p<\infty$; $L,R_2,R_p>0$ and integers $1\le T\le d/100$.; This constant-factor error statement is not asserted uniformly at $p=\infty$.

**Dimension conditions.** $d\ge100T$; p is fixed and finite.

**Constants.** Constants depend only on fixed p.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Corollary cor:risk, eq:risk-rate

Choose acceleration in the better of the two geometries. Deterministic algorithms

### B14 - Fixed smooth randomized hard distribution

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** randomized_hard_family

$$
c_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** Fix $2\le p<\infty$; $L,R_2,R_p>0$ and integers $1\le T\le d/100$.; This constant-factor error statement is not asserted uniformly at $p=\infty$.

**Dimension conditions.** $d\ge100T$; p is fixed and finite.

**Constants.** Constants depend only on fixed p.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Corollary cor:risk; Theorem thm:distribution with s=p

Fixed smooth randomized hard distribution. All adaptive randomized algorithms

### B15 - Choose acceleration in the better of the two geometries

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** Fix $2\le p<\infty$; $L,R_2,R_p>0$ and integers $1\le T\le d/100$.; This constant-factor error statement is not asserted uniformly at $p=\infty$.

**Dimension conditions.** $d\ge100T$; p is fixed and finite.

**Constants.** Constants depend only on fixed p.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Corollary cor:risk, eq:risk-rate

Choose acceleration in the better of the two geometries. Deterministic algorithms

### B16 - Fixed smooth randomized hard distribution

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** randomized_hard_family

$$
c_pL\min\{R_2^2/(T+1)^2,R_p^2/(T+1)^{1+2/p}\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf)

**Conditions.** Fix $2\le p<\infty$; $L,R_2,R_p>0$ and integers $1\le T\le d/100$.; This constant-factor error statement is not asserted uniformly at $p=\infty$.

**Dimension conditions.** $d\ge100T$; p is fixed and finite.

**Constants.** Constants depend only on fixed p.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf) Corollary cor:risk; Theorem thm:distribution with s=p

Fixed smooth randomized hard distribution. All adaptive randomized algorithms

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U02. Smooth Convex Optimization with Simultaneous Euclidean and $\ell_p$ Radius Bounds. Colombo_Two_Radius_Oracle_Complexity.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U02/manuscript.pdf
