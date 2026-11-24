# Nonconvex stationarity with priced value-gradient and full-Hessian jets under joint smoothness

**Setting ID.** `SO_HO_HOI10_S_weighted_jet_L1L2`

Single-objective optimization

A high-dimensional weighted oracle frontier connects a mixed-query rate with the gradient-only accuracy exponent.

**Status.** Fully optimal on the documented comparison domain

**TASK tags.** solution concept: Gradient stationarity; task family: Single objective

**MODEL tags.** smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** feedback quality: Exact; operation: Value gradient hessian jet; operation: Value gradient jet; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N ordinary jet; measure: N rich jet

## 1. Setting specification

### Task

Find an approximate first-order stationary point while minimizing the weighted number of ordinary value-gradient and rich full-Hessian queries.

### Admissible model

The unknown bounded-below $C^2$ objective $f:\mathbb R^d\to\mathbb R$ satisfies $f(0)-\inf f\le1$, $\operatorname{Lip}(\nabla f)\le1$ and $\operatorname{Lip}(\nabla^2f)\le1$, with Euclidean operator norms. These are fixed normalized budgets; no convexity or bounded query domain is imposed.

### Oracle interface

An ordinary call returns $(f(x),\nabla f(x))$ and costs one. A rich call returns $(f(x),\nabla f(x),\nabla^2f(x))$ and costs the public price $\tau\ge1$. A rich call is charged once in $H$, not again in $G$. Separate value requests, if made, count as ordinary calls. Queries may be arbitrary exact-real vectors.

### Output

Return any measurable transcript-dependent $\widehat x\in\mathbb R^d$, possibly unqueried.

### Loss or accuracy criterion

The error is $\|\nabla f(\widehat x)\|_2$; success probability must be at least $2/3$ separately for every fixed objective.

### Resource accounting

The weighted cost is $G+\tau H$ and is bounded on every input and every random execution. Internal computation is free. The lower bound concerns the explicit high-dimensional regime; the deterministic upper algorithm works in every dimension.

### Algorithm views and success guarantees

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

A private random seed independent of the fixed instance is permitted.

$$
\forall f:\ \Pr(\|\nabla f(\widehat x)\|_2\le\varepsilon)\ge2/3
$$

Probability is over the private seed; the objective is fixed independently of that seed.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$d$: Public ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$\tau$: Price of one rich full-Hessian jet **Domain:** $\tau\ge1$.

$\varepsilon$: Gradient-norm tolerance **Domain:** $\varepsilon>0$.

$\Delta$: Normalized initial-gap upper bound **Domain:** $\Delta=1$.

$L_1$: Normalized gradient Lipschitz bound **Domain:** $L_1=1$.

$L_2$: Normalized Hessian Lipschitz bound **Domain:** $L_2=1$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
Q^{(d),\star}_{\rm rand}(\tau,\varepsilon)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $G+\tau H$; description: Fixed weighted cap on every execution.

### R1 - Intermediate Hessian prices

**Region.** $0<\varepsilon\le\varepsilon_0$ for the universal threshold of Theorem main; $1\le\tau\le\varepsilon^{-3/4}$. $d\ge\max\{\lceil\tau\rceil,C_d\varepsilon^{-9/2}\min\{\tau^{2/3},\varepsilon^{-1/2}\}\}$ as in equation dimension-main, with a universal sufficient $C_d>0$. The upper bound itself holds in every finite dimension.

**Quantity.** Q1

**Resource.** Fixed weighted cap on every execution.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega(\tau^{1/3}\varepsilon^{-3/2})
$$

**Upper bound.** B1

$$
O(\tau^{1/3}\varepsilon^{-3/2})
$$

**Gap or comparison.** The rate is matched without logarithmic loss.

### R2 - Expensive Hessian prices

**Region.** $0<\varepsilon\le\varepsilon_0$ for the universal threshold of Theorem main; $\tau>\varepsilon^{-3/4}$. $d\ge\max\{\lceil\tau\rceil,C_d\varepsilon^{-9/2}\min\{\tau^{2/3},\varepsilon^{-1/2}\}\}$ as in equation dimension-main, with a universal sufficient $C_d>0$. The upper bound itself holds in every finite dimension.

**Quantity.** Q1

**Resource.** Fixed weighted cap on every execution.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega(\varepsilon^{-7/4})
$$

**Upper bound.** B3

$$
O(\varepsilon^{-7/4})
$$

**Gap or comparison.** The rate is matched without logarithmic loss.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** $d\ge\max\{\lceil\tau\rceil,C_d\varepsilon^{-9/2}\min\{\tau^{2/3},\varepsilon^{-1/2}\}\}$ as in equation dimension-main, with a universal sufficient $C_d>0$. The upper bound itself holds in every finite dimension.

### B1 - Weighted Hessian-saving Newton method or gradient-only acceleration

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O(\tau^{1/3}\varepsilon^{-3/2})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf)

**Conditions.** $0<\varepsilon\le\varepsilon_0$ for the universal threshold of Theorem main; $1\le\tau\le\varepsilon^{-3/4}$.; The source counts ordinary calls explicitly even when the implementation uses derivative-only responses.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf) Theorem main; equations main and two-regimes; subsection Deriving the upper bound; verified labels: thm:main (line 245), eq:main (line 256), eq:two-regimes (line 263), prop:upper (line 314)

Weighted Hessian-saving Newton method or gradient-only acceleration. Deterministic algorithms, hence valid in the randomized class.

The source counts ordinary calls explicitly even when the implementation uses derivative-only responses.

### B2 - Smooth macro-block construction with delayed linear-system disclosure

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\tau^{1/3}\varepsilon^{-3/2})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf)

**Conditions.** $0<\varepsilon\le\varepsilon_0$ for the universal threshold of Theorem main; $1\le\tau\le\varepsilon^{-3/4}$.; The lower bound allows both strengthened value-containing oracle packets and requires the stated sufficient dimension.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf) Theorem main; equations main and dimension-main; verified labels: thm:main (line 245), eq:dimension-main (line 248), eq:main (line 256)

Smooth macro-block construction with delayed linear-system disclosure. Arbitrary randomized adaptive queries and unqueried outputs.

The lower bound allows both strengthened value-containing oracle packets and requires the stated sufficient dimension.

### B3 - Weighted Hessian-saving Newton method or gradient-only acceleration

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O(\varepsilon^{-7/4})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf)

**Conditions.** $0<\varepsilon\le\varepsilon_0$ for the universal threshold of Theorem main; $\tau>\varepsilon^{-3/4}$.; The source counts ordinary calls explicitly even when the implementation uses derivative-only responses.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf) Theorem main; equations main and two-regimes; subsection Deriving the upper bound; verified labels: thm:main (line 245), eq:main (line 256), eq:two-regimes (line 263), prop:upper (line 314)

Weighted Hessian-saving Newton method or gradient-only acceleration. Deterministic algorithms, hence valid in the randomized class.

The source counts ordinary calls explicitly even when the implementation uses derivative-only responses.

### B4 - Smooth macro-block construction with delayed linear-system disclosure

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(\varepsilon^{-7/4})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf)

**Conditions.** $0<\varepsilon\le\varepsilon_0$ for the universal threshold of Theorem main; $\tau>\varepsilon^{-3/4}$.; The lower bound allows both strengthened value-containing oracle packets and requires the stated sufficient dimension.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf) Theorem main; equations main and dimension-main; verified labels: thm:main (line 245), eq:dimension-main (line 248), eq:main (line 256)

Smooth macro-block construction with delayed linear-system disclosure. Arbitrary randomized adaptive queries and unqueried outputs.

The lower bound allows both strengthened value-containing oracle packets and requires the stated sufficient dimension.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_A4. Matching Gradient--Hessian Query Bounds via a Smooth Macro-Block Construction. A4_gradient_hessian_matching_publication.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/A4/manuscript.pdf
