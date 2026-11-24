# Convex minimization with a fixed non-Euclidean proximal oracle

**Setting ID.** `SO_FO_P01_fixed_non_euclidean`

Single-objective optimization

A hidden finite convex objective is accessed only through the exact proximal point associated with a fixed power of an ell-p distance and a fixed positive coefficient.

**Status.** Fully optimal on the documented comparison domain

**TASK tags.** solution concept: Objective minimization; task family: Single objective

**MODEL tags.** convexity: Convex

**ORACLE tags.** feedback quality: Exact; operation: Fixed non euclidean prox; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**GUARANTEE tags.** mode: Probability; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N prox

## 1. Setting specification

### Task

Minimize an unknown finite convex function $f:\mathbb R^d\to\mathbb R$ globally and return a point with small objective gap.

### Admissible model

Fix $2<p<s<\infty$ and $\lambda,R>0$. The class consists of finite convex functions having at least one attained global minimizer $x^\star$ with $\|x^\star\|_p\le R$. No uniform Lipschitz, smoothness, or objective-scale bound is imposed.

The localization ball is only a promise about one global minimizer. It does not restrict query centers or final outputs.

### Oracle interface

The only Oracle interface is $$P_f(c)=\operatorname*{argmin}_{x\in\mathbb R^d}\{f(x)+\lambda\|x-c\|_p^s\},\qquad c\in\mathbb R^d.$$ One call returns this unique minimizer only, with no accompanying function value or subgradient.

The positive coefficient $\lambda$ and exponents $p,s$ are public and fixed for the entire interaction. The algorithm may choose the center but may not choose another regularization coefficient or power. Public inputs are $d,p,s,\lambda,R,\varepsilon$; the objective is hidden.

### Output

Return any measurable $\widehat x\in\mathbb R^d$ determined by the transcript. It need not be a queried center or a proximal response.

### Loss or accuracy criterion

The loss is $f(\widehat x)-f^\star$, where $f^\star=\min_{x\in\mathbb R^d}f(x)$.

### Resource accounting

One exact fixed-coefficient proximal reply costs one call. The total number of calls is bounded on every instance and every realization of the private seed. Exact internal computation, storage, and specification of arbitrary finite query centers are uncharged.

### Algorithm views and success guarantees

#### Randomized / 2/3 success

Queries, stopping decisions, and the output are measurable functions of the preceding transcript and an instance-independent private random seed. The unknown instance is fixed before the seed is realized. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage using public inputs and received information are uncharged. The stated budget must hold on every execution path.

$$
\forall f:\ \Pr(f(\widehat x)-f^\star\le\varepsilon)\ge2/3
$$

The guarantee is per fixed objective, with an independent private seed and a pathwise query cap.

**Budget convention.** fixed_worst_case

#### Deterministic / Pointwise error

The algorithm is deterministic and adaptive. Queries, stopping, and the output may use the complete preceding transcript. No span, support, zero-respecting, or memory restriction is imposed.

Internal exact-real computation and storage are uncharged. The stated budget holds on every admissible instance and every response history.

$$
\forall f:\ f(\widehat x)-f^\star\le\varepsilon
$$

The error bound is deterministic for every admissible objective.

**Budget convention.** fixed_worst_case

## 2. Notation and parameters

$d$: Ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$p$: Norm exponent **Domain:** $2<p<s<\infty$.

$s$: Fixed regularization power **Domain:** $s>p$.

$\lambda$: Fixed proximal regularization coefficient **Domain:** $\lambda>0$.

$R$: Radius of a global minimizer in ell-p **Domain:** $R>0$.

$\varepsilon$: Target objective error **Domain:** $\varepsilon>0$.

$\kappa$: Normalized target scale **Domain:** $\kappa>0$.

$\kappa=\lambda R^s/\varepsilon$

$\rho$: Accuracy exponent denominator **Domain:** $\rho>0$.

$\rho=s+s/p-1$

$C_p$: Explicit sufficient-dimension coefficient **Domain:** $C_p>0$.

$C_p=2+12\cdot64^p$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

**View.** Randomized / 2/3 success

$$
Q^*_{\rm rand}(\varepsilon;d)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{P_f}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

#### Q2 - minimax metric resource quantity

**View.** Deterministic / Pointwise error

$$
Q^*_{\rm det}(\varepsilon;d)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{P_f}$; description: All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

### R1 - High-dimensional fixed-coefficient proximal complexity

**Region.** $2<p<s<\infty$, $\lambda,R,\varepsilon>0$, and $d\ge\lceil C_p(1+\kappa^{(p+3)/\rho})\rceil$. $d\ge\lceil(2+12\cdot64^p)(1+(\lambda R^s/\varepsilon)^{(p+3)/(s+s/p-1)})\rceil$. This is sufficient, not necessary. The lower construction is one finite distribution sampled before the algorithmic seed. The fixed coefficient is an essential part of the interface.

**Views.** Randomized / 2/3 success

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega_{p,s}(1+\kappa^{1/\rho})
$$

**Upper bound.** B1

$$
O_{p,s}(1+\kappa^{1/\rho})
$$

**Gap or comparison.**

$$
O_{p,s}(1)
$$

### R2 - Exact one-query regime

**Region.** $\varepsilon\ge\lambda R^s$, $d\ge1$, $2<p<s<\infty$, $\lambda,R>0$. All integer dimensions d>=1. There is no objective-scale bound, so zero queries cannot guarantee any finite positive target uniformly over the class.

**Views.** Randomized / 2/3 success

**Quantity.** Q1

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B4

$$
1
$$

**Upper bound.** B3

$$
1
$$

**Gap or comparison.** 1

### R3 - High-dimensional fixed-coefficient proximal complexity

**Region.** $2<p<s<\infty$, $\lambda,R,\varepsilon>0$, and $d\ge\lceil C_p(1+\kappa^{(p+3)/\rho})\rceil$. $d\ge\lceil(2+12\cdot64^p)(1+(\lambda R^s/\varepsilon)^{(p+3)/(s+s/p-1)})\rceil$. This is sufficient, not necessary. The lower construction is one finite distribution sampled before the algorithmic seed. The fixed coefficient is an essential part of the interface.

**Views.** Deterministic / Pointwise error

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega_{p,s}(1+\kappa^{1/\rho})
$$

**Upper bound.** B5

$$
O_{p,s}(1+\kappa^{1/\rho})
$$

**Gap or comparison.**

$$
O_{p,s}(1)
$$

### R4 - Exact one-query regime

**Region.** $\varepsilon\ge\lambda R^s$, $d\ge1$, $2<p<s<\infty$, $\lambda,R>0$. All integer dimensions d>=1. There is no objective-scale bound, so zero queries cannot guarantee any finite positive target uniformly over the class.

**Views.** Deterministic / Pointwise error

**Quantity.** Q2

**Resource.** All charged oracle operations are counted, including initialization and verification. The budget is a worst-case cap unless the resource expression explicitly specifies another cost.

**Status.** Optimal

**Lower bound.** B8

$$
1
$$

**Upper bound.** B7

$$
1
$$

**Gap or comparison.** 1

## 4. Bounds and supporting evidence

### B1 - Fixed-coefficient implementation of Adil--Bullins--Jambulapati--Sidford proximal acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 2/3 success

**Witness or lower-bound scope.** Deterministic witness

$$
O_{p,s}(1+\kappa^{1/\rho})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $2<p<s<\infty$, $\lambda,R,\varepsilon>0$, and $d\ge\lceil C_p(1+\kappa^{(p+3)/\rho})\rceil$.; The upper bound is valid in every dimension, including nonsmooth finite objectives.; The lower construction is one finite distribution sampled before the algorithmic seed. The fixed coefficient is an essential part of the interface.

**Dimension conditions.** $d\ge\lceil(2+12\cdot64^p)(1+(\lambda R^s/\varepsilon)^{(p+3)/(s+s/p-1)})\rceil$. This is sufficient, not necessary.

**Constants.** Constants depend only on fixed p and s.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Theorem thm:matching; Section sec:upper; Proposition prop:upper

Fixed-coefficient implementation of Adil--Bullins--Jambulapati--Sidford proximal acceleration. Deterministic unrestricted-center algorithms

The upper bound is valid in every dimension, including nonsmooth finite objectives.

### B2 - Random hidden coordinates, a common radial term, and exact truncation of proximal replies

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / 2/3 success

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega_{p,s}(1+\kappa^{1/\rho})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $2<p<s<\infty$, $\lambda,R,\varepsilon>0$, and $d\ge\lceil C_p(1+\kappa^{(p+3)/\rho})\rceil$.; The lower construction is one finite distribution sampled before the algorithmic seed. The fixed coefficient is an essential part of the interface.

**Dimension conditions.** $d\ge\lceil(2+12\cdot64^p)(1+(\lambda R^s/\varepsilon)^{(p+3)/(s+s/p-1)})\rceil$. This is sufficient, not necessary.

**Constants.** Constants depend only on fixed p and s.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Theorems thm:budget and thm:matching; eq:dimension-corollary

Random hidden coordinates, a common radial term, and exact truncation of proximal replies. All adaptive randomized algorithms with unrestricted centers and arbitrary measurable output

### B3 - Query the fixed proximal oracle at center zero

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / 2/3 success

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $\varepsilon\ge\lambda R^s$, $d\ge1$, $2<p<s<\infty$, $\lambda,R>0$.; There is no objective-scale bound, so zero queries cannot guarantee any finite positive target uniformly over the class.

**Dimension conditions.** All integer dimensions d>=1.

**Constants.** Exact equality; no suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Section sec:upper, eq:one-query

Query the fixed proximal oracle at center zero. Deterministic nonadaptive algorithm

### B4 - Two separated scaled absolute-value objectives

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / 2/3 success

**Witness or lower-bound scope.** randomized_hard_family

$$
1
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $\varepsilon\ge\lambda R^s$, $d\ge1$, $2<p<s<\infty$, $\lambda,R>0$.; There is no objective-scale bound, so zero queries cannot guarantee any finite positive target uniformly over the class.

**Dimension conditions.** All integer dimensions d>=1.

**Constants.** Exact equality; no suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Lemma lem:zero

Two separated scaled absolute-value objectives. All randomized algorithms

### B5 - Fixed-coefficient implementation of Adil--Bullins--Jambulapati--Sidford proximal acceleration

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** Deterministic witness

$$
O_{p,s}(1+\kappa^{1/\rho})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $2<p<s<\infty$, $\lambda,R,\varepsilon>0$, and $d\ge\lceil C_p(1+\kappa^{(p+3)/\rho})\rceil$.; The upper bound is valid in every dimension, including nonsmooth finite objectives.; The lower construction is one finite distribution sampled before the algorithmic seed. The fixed coefficient is an essential part of the interface.

**Dimension conditions.** $d\ge\lceil(2+12\cdot64^p)(1+(\lambda R^s/\varepsilon)^{(p+3)/(s+s/p-1)})\rceil$. This is sufficient, not necessary.

**Constants.** Constants depend only on fixed p and s.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Theorem thm:matching; Section sec:upper; Proposition prop:upper

Fixed-coefficient implementation of Adil--Bullins--Jambulapati--Sidford proximal acceleration. Deterministic unrestricted-center algorithms

The upper bound is valid in every dimension, including nonsmooth finite objectives.

### B6 - Random hidden coordinates, a common radial term, and exact truncation of proximal replies

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** randomized_hard_family

$$
\Omega_{p,s}(1+\kappa^{1/\rho})
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $2<p<s<\infty$, $\lambda,R,\varepsilon>0$, and $d\ge\lceil C_p(1+\kappa^{(p+3)/\rho})\rceil$.; The lower construction is one finite distribution sampled before the algorithmic seed. The fixed coefficient is an essential part of the interface.

**Dimension conditions.** $d\ge\lceil(2+12\cdot64^p)(1+(\lambda R^s/\varepsilon)^{(p+3)/(s+s/p-1)})\rceil$. This is sufficient, not necessary.

**Constants.** Constants depend only on fixed p and s.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Theorems thm:budget and thm:matching; eq:dimension-corollary

Random hidden coordinates, a common radial term, and exact truncation of proximal replies. All adaptive randomized algorithms with unrestricted centers and arbitrary measurable output

### B7 - Query the fixed proximal oracle at center zero

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** Deterministic witness

$$
1
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $\varepsilon\ge\lambda R^s$, $d\ge1$, $2<p<s<\infty$, $\lambda,R>0$.; There is no objective-scale bound, so zero queries cannot guarantee any finite positive target uniformly over the class.

**Dimension conditions.** All integer dimensions d>=1.

**Constants.** Exact equality; no suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Section sec:upper, eq:one-query

Query the fixed proximal oracle at center zero. Deterministic nonadaptive algorithm

### B8 - Two separated scaled absolute-value objectives

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise error

**Witness or lower-bound scope.** randomized_hard_family

$$
1
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf)

**Conditions.** $\varepsilon\ge\lambda R^s$, $d\ge1$, $2<p<s<\infty$, $\lambda,R>0$.; There is no objective-scale bound, so zero queries cannot guarantee any finite positive target uniformly over the class.

**Dimension conditions.** All integer dimensions d>=1.

**Constants.** Exact equality; no suppressed constants.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf) Lemma lem:zero

Two separated scaled absolute-value objectives. All randomized algorithms

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_B2. Optimal Randomized Complexity of Fixed Non-Euclidean Proximal Oracles. B2_proximal_oracles_publication.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/B2/manuscript.pdf
