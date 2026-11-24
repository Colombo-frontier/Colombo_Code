# Coordinate subgradient minimization on product domains with an independent optimizer radius

**Setting ID.** `SO_FO_CS01_product_radius_csg`

Single-objective optimization

A coherent scalar coordinate interface is studied uniformly over public product geometries. The optimizer-distance budget is independent of the domain diameter, and coordinatewise-motion algorithms form a separate view.

**Status.** Logarithmic gap; Bounds missing

**TASK tags.** solution concept: Objective minimization; task family: Single objective

**MODEL tags.** convexity: Convex; smoothness: Lipschitz

**ORACLE tags.** feedback quality: Exact; operation: Coordinate subgradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** postprocessing: Unqueried output explicitly allowed

**GUARANTEE tags.** quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N coordinate subgradient

## 1. Setting specification

### Task

Given a public compact product domain $D$ and initial point $x_1\in D$, minimize a hidden convex function over $D$. The complexity is uniform over the permitted public geometries, with the algorithm selected after the geometry is known.

### Admissible model

The public domain is $$D=\prod_{i=1}^d[\ell_i,u_i],\qquad-\infty<\ell_i\le u_i<\infty.$$ Singleton factors are allowed. There is no bound on $\operatorname{diam}(D)/R_B$.

An instance is a finite convex Euclidean $G$-Lipschitz function $f:D\to\mathbb R$ and one fixed Borel map $g:D\to\mathbb R^d$ such that $$f(z)\ge f(x)+\langle g(x),z-x\rangle,\quad\|g(x)\|_2\le G\qquad(x,z\in D).$$ At boundary points this supporting inequality is relative to $D$.

At least one constrained minimizer satisfies $\frac12\|x^\star-x_1\|_2^2\le R_B^2$. The radius $R_B$ is independent of the size of the product domain. The pair $(f,g)$ is fixed before the private seed is sampled.

### Oracle interface

One query chooses $(x,i)\in D\times\{1,\ldots,d\}$ and returns only the exact scalar $g_i(x)$. All coordinates at a point arise from the same pre-fixed vector $g(x)$. No function values, active labels, full gradients, coordinate minimizers, or off-domain observations are supplied.

The public inputs are $d,G,R_B,\varepsilon,D,x_1$. Projection onto the known product domain and operations on public geometry are free.

### Output

Return any measurable feasible point $\widehat x\in D$ determined by the transcript, including an unqueried point or an average of iterates.

### Loss or accuracy criterion

The loss is $f(\widehat x)-\min_{z\in D}f(z)$. The requirement concerns worst-instance expected loss over the independent private seed.

### Resource accounting

Every scalar coordinate response costs one call. The query cap holds on every seed and every legal response history. Exact centroid and support computations on known models, arithmetic, and storage are uncharged; their computational runtime is not a charged resource.

### Algorithm views and success guarantees

#### Unrestricted coordinates / Expected loss

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall(D,x_1)\ \exists A_{D,x_1}\ \forall(f,g):\mathbb E[f(\widehat x)-\min_Df]\le\varepsilon
$$

The policy family is chosen using the public geometry. Expected error is uniform over all admissible hidden coherent instances, with a pathwise scalar-query cap.

**Budget convention.** fixed_worst_case

#### Coordinatewise motion / Expected loss

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

If a query is made, the first query point is $x_1$. Successive actual query points obey $X_{t+1}-X_t\in\operatorname{span}\{e_{I_t}\}$. The output may be any feasible function of the transcript; no prescribed stepsize formula or last-iterate restriction is imposed.

$$
\forall(D,x_1)\ \exists A_{D,x_1}\ \forall(f,g):\mathbb E[f(\widehat x)-\min_Df]\le\varepsilon
$$

The same worst-geometry expected-error guarantee is required under the stated motion restriction.

**Budget convention.** fixed_worst_case

## 2. Notation and parameters

$d$: Number of scalar subgradient coordinates **Domain:** $d\in\mathbb N_{\ge1}$.

$G$: Bound on the Euclidean norm of the coherent selected subgradient **Domain:** $G>0$.

$R_B$: Independent optimizer-distance budget **Domain:** $R_B>0$.

$\|x^\star-x_1\|_2\le\sqrt2R_B$ for some minimizer

$\varepsilon$: Expected objective-error target **Domain:** $\varepsilon>0$.

$D$: Public compact product domain **Domain:** $D=\prod_i[\ell_i,u_i]$, finite endpoints.

$x_1$: Public initial point **Domain:** $x_1\in D$.

$q$: Normalized inverse accuracy **Domain:** $q>0$.

$q=GR_B/\varepsilon$

$d_0$: Universal lower-bound dimension threshold **Domain:** $d_0\in\mathbb N$.

Universal threshold in Theorem thm:main; no numerical value is asserted.

$q_0$: Universal lower-bound inverse-accuracy threshold **Domain:** $q_0>=1$.

Universal threshold in Theorem thm:main; independent of d,G,R_B and the geometry.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

**View.** Unrestricted coordinates / Expected loss

$$
T_{\rm coord}^*(d,G,R_B,\varepsilon)=\inf\{T:\forall(D,x_1)\exists A_{D,x_1}\text{ with cap }T\text{ and the expected-loss guarantee}\}
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{coordinate\ scalar}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q2 - minimax metric resource quantity

**View.** Coordinatewise motion / Expected loss

$$
T_{\rm upd}^*(d,G,R_B,\varepsilon)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\mathrm{coordinate\ scalar}}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

### R1 - Unrestricted scalar queries: moderate

**Region.** $d\ge d_0$ and $q_0\le q\le\sqrt d$; $G,R_B>0$ and $q=GR_B/\varepsilon$. $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$. This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial. The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Views.** Unrestricted coordinates / Expected loss

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(dq^2/\log(eq^2))
$$

**Upper bound.** B1

$$
O(dq^2)
$$

**Gap or comparison.**

$$
O(\log(eq^2))
$$

### R2 - Unrestricted scalar queries: high accuracy

**Region.** $d\ge d_0$ and $q\ge\max\{q_0,\sqrt d\}$; $G,R_B>0$ and $q=GR_B/\varepsilon$. $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$. This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial. The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Views.** Unrestricted coordinates / Expected loss

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B3

$$
O(\min\{dq^2,d^2\log(edq)\})
$$

**Gap or comparison.**

$$
O(\log(ed)\log(edq))
$$

### R3 - Remaining dimensions or coarse positive-query accuracy: upper bound

**Region.** $d\ge1$, $q>1/\sqrt2$, and either $d<d_0$ or $q<q_0$. All d>=1 in the displayed complement of the lower-bound window. The near-optimal high-dimensional rows are excluded from this region.

**Views.** Unrestricted coordinates / Expected loss

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5

$$
\min\left\{\lceil2dq^2\rceil,d\left(\lceil2ed\log(4\sqrt2\,d^2q)\rceil+1\right)\right\}
$$

**Gap or comparison.** No matching source lower bound is specified for this complementary window.

### R4 - Sufficient zero-query accuracy

**Region.** $\varepsilon\ge\sqrt2GR_B$ (equivalently $q\le1/\sqrt2$). All d>=1. No converse sharp zero-query threshold for the worst-geometry class is asserted.

**Views.** Unrestricted coordinates / Expected loss

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B7

$$
0
$$

**Upper bound.** B6

$$
0
$$

**Gap or comparison.** Exact zero calls within the displayed sufficient region.

### R5 - Coordinatewise motion: moderate

**Region.** $d\ge d_0$ and $q_0\le q\le\sqrt d$; $G,R_B>0$ and $q=GR_B/\varepsilon$. $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$. This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial. The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Views.** Coordinatewise motion / Expected loss

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B9

$$
\Omega(dq^2/\log(eq^2))
$$

**Upper bound.** B8

$$
O(dq^2)
$$

**Gap or comparison.**

$$
O(\log(eq^2))
$$

### R6 - Coordinatewise motion: high accuracy

**Region.** $d\ge d_0$ and $q\ge\max\{q_0,\sqrt d\}$; $G,R_B>0$ and $q=GR_B/\varepsilon$. $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$. This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial. The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Views.** Coordinatewise motion / Expected loss

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Logarithmic gap

**Lower bound.** B11

$$
\Omega(d^2/\log(ed))
$$

**Upper bound.** B10

$$
O(\min\{dq^2,d^2\log(edq)\})
$$

**Gap or comparison.**

$$
O(\log(ed)\log(edq))
$$

### R7 - Remaining dimensions or coarse positive-query accuracy: upper bound

**Region.** $d\ge1$, $q>1/\sqrt2$, and either $d<d_0$ or $q<q_0$. All d>=1 in the displayed complement of the lower-bound window. The near-optimal high-dimensional rows are excluded from this region.

**Views.** Coordinatewise motion / Expected loss

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B12

$$
\min\left\{\lceil2dq^2\rceil,2d\left(\lceil2ed\log(4\sqrt2\,d^2q)\rceil+1\right)\right\}
$$

**Gap or comparison.** No matching source lower bound is specified for this complementary window.

### R8 - Sufficient zero-query accuracy

**Region.** $\varepsilon\ge\sqrt2GR_B$ (equivalently $q\le1/\sqrt2$). All d>=1. No converse sharp zero-query threshold for the worst-geometry class is asserted.

**Views.** Coordinatewise motion / Expected loss

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B14

$$
0
$$

**Upper bound.** B13

$$
0
$$

**Gap or comparison.** Exact zero calls within the displayed sufficient region.

## 4. Bounds and supporting evidence

### B1 - Projected coordinate subgradient updates or value-free centroid localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(dq^2)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q_0\le q\le\sqrt d$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-upper

Projected coordinate subgradient updates or value-free centroid localization. Unrestricted adaptive algorithms

The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.

### B2 - Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(dq^2/\log(eq^2))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q_0\le q\le\sqrt d$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-lower and normalized-box assertion

Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality. All unrestricted randomized algorithms, hence also the restricted-motion class

### B3 - Projected coordinate subgradient updates or value-free centroid localization

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(\min\{dq^2,d^2\log(edq)\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q\ge\max\{q_0,\sqrt d\}$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-upper

Projected coordinate subgradient updates or value-free centroid localization. Unrestricted adaptive algorithms

The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.

### B4 - Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(d^2/\log(ed))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q\ge\max\{q_0,\sqrt d\}$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-lower and normalized-box assertion

Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality. All unrestricted randomized algorithms, hence also the restricted-motion class

### B5 - Projected coordinate method or centroid method with the applicable routing factor

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** randomized_or_deterministic

$$
\min\left\{\lceil2dq^2\rceil,d\left(\lceil2ed\log(4\sqrt2\,d^2q)\rceil+1\right)\right\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge1$, $q>1/\sqrt2$, and either $d<d_0$ or $q<q_0$.; The near-optimal high-dimensional rows are excluded from this region.

**Dimension conditions.** All d>=1 in the displayed complement of the lower-bound window.

**Constants.** The displayed cap is explicit.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-upper; Corollary cor:update

Projected coordinate method or centroid method with the applicable routing factor. The algorithms of this view

### B6 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $\varepsilon\ge\sqrt2GR_B$ (equivalently $q\le1/\sqrt2$).; No converse sharp zero-query threshold for the worst-geometry class is asserted.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Proposition prop:zero

Return the public initial point. Deterministic algorithm

### B7 - Nonnegative call count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted coordinates / Expected loss

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $\varepsilon\ge\sqrt2GR_B$ (equivalently $q\le1/\sqrt2$).; No converse sharp zero-query threshold for the worst-geometry class is asserted.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Proposition prop:zero

Nonnegative call count. All algorithms

### B8 - Projected coordinate subgradient updates or value-free centroid localization with coordinatewise routing

**Admission.** Included in the bracket

**Direction.** upper

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(dq^2)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q_0\le q\le\sqrt d$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-upper; Corollary cor:update, eq:update-upper

Projected coordinate subgradient updates or value-free centroid localization with coordinatewise routing. Algorithms satisfying the coordinatewise-motion restriction

The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.

### B9 - Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality

**Admission.** Included in the bracket

**Direction.** lower

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(dq^2/\log(eq^2))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q_0\le q\le\sqrt d$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-lower; normalized-box assertion; Corollary cor:update

Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality. All unrestricted randomized algorithms, hence also the restricted-motion class

### B10 - Projected coordinate subgradient updates or value-free centroid localization with coordinatewise routing

**Admission.** Included in the bracket

**Direction.** upper

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** randomized_or_deterministic

$$
O(\min\{dq^2,d^2\log(edq)\})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q\ge\max\{q_0,\sqrt d\}$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-upper; Corollary cor:update, eq:update-upper

Projected coordinate subgradient updates or value-free centroid localization with coordinatewise routing. Algorithms satisfying the coordinatewise-motion restriction

The first branch is randomized with an averaged output; centroid localization is deterministic. Routing increases its scalar cap by at most two.

### B11 - Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality

**Admission.** Included in the bracket

**Direction.** lower

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega(d^2/\log(ed))
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge d_0$ and $q\ge\max\{q_0,\sqrt d\}$; $G,R_B>0$ and $q=GR_B/\varepsilon$.; This is a worst-geometry statement, not a lower bound for every product domain. A singleton domain can be trivial.; The normalized hard box has $R_B=1$ independently of its diameter, which grows as $\sqrt d$.

**Dimension conditions.** $d\ge d_0$, a universal source threshold. The lower bound already holds on the single normalized box $[-1,1]^d$ with $G=R_B=1$.

**Constants.** Universal constants; d0 and q0 are universal thresholds.

**Logarithmic factors.** Only the displayed logarithms in d and q.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-lower; normalized-box assertion; Corollary cor:update

Random support functions with radial localization and posterior-energy accounting for the extra coordinate equality. All unrestricted randomized algorithms, hence also the restricted-motion class

### B12 - Projected coordinate method or centroid method with the applicable routing factor

**Admission.** Included in the bracket

**Direction.** upper

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** randomized_or_deterministic

$$
\min\left\{\lceil2dq^2\rceil,2d\left(\lceil2ed\log(4\sqrt2\,d^2q)\rceil+1\right)\right\}
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $d\ge1$, $q>1/\sqrt2$, and either $d<d_0$ or $q<q_0$.; The near-optimal high-dimensional rows are excluded from this region.

**Dimension conditions.** All d>=1 in the displayed complement of the lower-bound window.

**Constants.** The displayed cap is explicit.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Theorem thm:main, eq:main-upper; Corollary cor:update

Projected coordinate method or centroid method with the applicable routing factor. The algorithms of this view

### B13 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $\varepsilon\ge\sqrt2GR_B$ (equivalently $q\le1/\sqrt2$).; No converse sharp zero-query threshold for the worst-geometry class is asserted.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Proposition prop:zero

Return the public initial point. Deterministic algorithm

### B14 - Nonnegative call count

**Admission.** Included in the bracket

**Direction.** lower

**View.** Coordinatewise motion / Expected loss

**Witness or lower-bound scope.** elementary

$$
0
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf)

**Conditions.** $\varepsilon\ge\sqrt2GR_B$ (equivalently $q\le1/\sqrt2$).; No converse sharp zero-query threshold for the worst-geometry class is asserted.

**Dimension conditions.**

$$
All d>=1.
$$

**Constants.** No suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf) Proposition prop:zero

Nonnegative call count. All algorithms

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U03. Near-Optimal Complexity of Convex Optimization with Exact Coordinate Subgradient Oracles. coordinate_subgradient_complexity.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U03/manuscript.pdf
