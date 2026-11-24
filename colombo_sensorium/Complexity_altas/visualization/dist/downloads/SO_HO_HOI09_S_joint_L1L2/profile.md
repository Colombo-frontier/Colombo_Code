# Nonconvex stationarity with separate exact gradient and Hessian queries under joint smoothness

**Setting ID.** `SO_HO_HOI09_S_joint_L1L2`

Single-objective optimization

The strict gradient-Hessian budget frontier is determined for derivative-only information under simultaneous gradient and Hessian Lipschitz bounds.

**Status.** Fully optimal on the documented comparison domain

**TASK tags.** solution concept: Gradient stationarity; task family: Single objective

**MODEL tags.** smoothness: Lipschitz gradient; smoothness: Lipschitz Hessian

**ORACLE tags.** feedback quality: Exact; operation: Gradient; operation: Hessian; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative; scalar derivative order: Scalar-function second derivative

**ALGORITHMS tags.** randomization: Deterministic; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** postprocessing: Unqueried output explicitly allowed

**GUARANTEE tags.** aggregation: Per instance; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N gradient; measure: N hessian

## 1. Setting specification

### Task

Find $\widehat x$ satisfying $\|\nabla f(\widehat x)\|_2\le\varepsilon$ while minimizing the gradient-query cap under a prescribed strict full-Hessian-query cap.

### Admissible model

For each public finite dimension $d$, the unknown $f\in C^2(\mathbb R^d)$ has finite infimum, $f(x_0)-\inf f\le\Delta$, $\operatorname{Lip}(\nabla f)\le L_1$ and $\operatorname{Lip}(\nabla^2f)\le L_2$. All budgets and the initial point are public; derivative norms are induced Euclidean operator norms. There is no convexity or query-radius restriction.

### Oracle interface

At an arbitrary point choose exactly one of $O_g(x)=\nabla f(x)$ and $O_H(x)=\nabla^2f(x)$. A Hessian query returns the full matrix but neither the function value nor its gradient. The two counters are charged separately, and there is no function-value channel.

### Output

The output may be any transcript-dependent point of $\mathbb R^d$, including an unqueried point.

### Loss or accuracy criterion

The error is $\|\nabla f(\widehat x)\|_2$ and the guarantee must hold deterministically on every instance.

### Resource accounting

A feasible pair $(g,h)\in\mathbb N_0^2$ is witnessed by one algorithm with $N_g\le g$ and $N_H\le h$ on every input. Define $G^\star_\infty(h;\varepsilon)$ by minimizing $g$ with a guarantee uniform over all finite dimensions. Internal subproblem solves and exact-real arithmetic are uncharged.

### Algorithm views and success guarantees

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

The algorithm is deterministic and uses no private random seed.

$$
\forall f:\ \|\nabla f(\widehat x)\|_2\le\varepsilon
$$

Success and both resource caps hold on every instance.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$d$: Public finite ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$L_1$: Global gradient Lipschitz bound **Domain:** $L_1>0$.

$L_2$: Global Hessian Lipschitz bound **Domain:** $L_2>0$.

$\Delta$: Initial objective gap **Domain:** $\Delta>0$.

$\varepsilon$: Gradient-norm tolerance **Domain:** $\varepsilon>0$.

$h$: Strict integer Hessian-query cap **Domain:** $h\in\mathbb N_0$.

$A$: Second-order complexity scale **Domain:** $A>0$.

$A=\Delta\sqrt{L_2}\varepsilon^{-3/2}$

$B$: Gradient-only complexity scale **Domain:** $B>0$.

$B=\Delta\sqrt{L_1}L_2^{1/4}\varepsilon^{-7/4}$

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
G^\star_\infty(h;\varepsilon)
$$

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $(N_g,N_H),\ N_H\le h;\ \min N_g$; description: The Hessian cap is an integer hard cap; a rich derivative does not include a gradient.

### R1 - No Hessian calls

**Region.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h=0$. Upper bounds hold in every finite dimension. The Hessian-rich product lower bound is one-dimensional. For the scarce-Hessian lower bound, Lemma matrix-lift gives sufficient dimension $C(Jd_0+J+g+h+1)$, with $J=2(h+1)$, $d_0\le C_{\rm dim}m$ from Lemma local-gadget, and local scales $\delta=\Delta/(6J)$, $\nu=L_2/C_*$, $\ell=\min\{L_1/C_*,\delta\nu/\varepsilon\}$ from equation poor-calibration-final. The construction dimension is allowed to depend on the proposed pair; no fixed-dimensional matching claim is made.

**Quantity.** Q1

**Resource.** The Hessian cap is an integer hard cap; a rich derivative does not include a gradient.

**Status.** Optimal

**Lower bound.** B2

$$
\Omega\!\left(B\right)
$$

**Upper bound.** B1

$$
O\!\left(B\right)
$$

**Gap or comparison.** Constant-factor matching throughout this branch.

### R2 - Scarce Hessian budget

**Region.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h\in\mathbb N$, $1\le h\le A$. Upper bounds hold in every finite dimension. The Hessian-rich product lower bound is one-dimensional. For the scarce-Hessian lower bound, Lemma matrix-lift gives sufficient dimension $C(Jd_0+J+g+h+1)$, with $J=2(h+1)$, $d_0\le C_{\rm dim}m$ from Lemma local-gadget, and local scales $\delta=\Delta/(6J)$, $\nu=L_2/C_*$, $\ell=\min\{L_1/C_*,\delta\nu/\varepsilon\}$ from equation poor-calibration-final. The construction dimension is allowed to depend on the proposed pair; no fixed-dimensional matching claim is made.

**Quantity.** Q1

**Resource.** The Hessian cap is an integer hard cap; a rich derivative does not include a gradient.

**Status.** Optimal

**Lower bound.** B4

$$
\Omega\!\left(\min\{B,A^{3/2}/\sqrt h\}\right)
$$

**Upper bound.** B3

$$
O\!\left(\min\{B,A^{3/2}/\sqrt h\}\right)
$$

**Gap or comparison.** Constant-factor matching throughout this branch.

### R3 - Hessian-rich budget

**Region.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h\in\mathbb N$, $h>A$. Upper bounds hold in every finite dimension. The Hessian-rich product lower bound is one-dimensional. For the scarce-Hessian lower bound, Lemma matrix-lift gives sufficient dimension $C(Jd_0+J+g+h+1)$, with $J=2(h+1)$, $d_0\le C_{\rm dim}m$ from Lemma local-gadget, and local scales $\delta=\Delta/(6J)$, $\nu=L_2/C_*$, $\ell=\min\{L_1/C_*,\delta\nu/\varepsilon\}$ from equation poor-calibration-final. The construction dimension is allowed to depend on the proposed pair; no fixed-dimensional matching claim is made.

**Quantity.** Q1

**Resource.** The Hessian cap is an integer hard cap; a rich derivative does not include a gradient.

**Status.** Optimal

**Lower bound.** B6

$$
\Omega\!\left(\max\{1,A^2/h\}\right)
$$

**Upper bound.** B5

$$
O\!\left(\max\{1,A^2/h\}\right)
$$

**Gap or comparison.** Constant-factor matching throughout this branch.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Upper bounds hold in every finite dimension. The Hessian-rich product lower bound is one-dimensional. For the scarce-Hessian lower bound, Lemma matrix-lift gives sufficient dimension $C(Jd_0+J+g+h+1)$, with $J=2(h+1)$, $d_0\le C_{\rm dim}m$ from Lemma local-gadget, and local scales $\delta=\Delta/(6J)$, $\nu=L_2/C_*$, $\ell=\min\{L_1/C_*,\delta\nu/\varepsilon\}$ from equation poor-calibration-final. The construction dimension is allowed to depend on the proposed pair; no fixed-dimensional matching claim is made.

### B1 - Gradient-only method and the imported first-order lower bound

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(B\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf)

**Conditions.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h=0$.; One algorithm attains both stated coordinate caps.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf) Corollary complete-frontier; Lemma gradient-only; verified labels: cor:complete-frontier (line 407), eq:complete-frontier (line 409), lem:gradient-only (line 644)

Gradient-only method and the imported first-order lower bound. Deterministic adaptive algorithms.

One algorithm attains both stated coordinate caps.

### B2 - Gradient-only method and the imported first-order lower bound

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Deterministic witness

$$
\Omega\!\left(B\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf)

**Conditions.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h=0$.; Arbitrary query points and unqueried outputs are allowed.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf) Corollary complete-frontier and its proof; verified labels: cor:complete-frontier (line 407), eq:complete-frontier (line 409)

Gradient-only method and the imported first-order lower bound. All deterministic measurable adaptive algorithms.

Arbitrary query points and unqueried outputs are allowed.

### B3 - Strict integer lazy-extragradient schedule and sequential full-matrix resisting construction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\min\{B,A^{3/2}/\sqrt h\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf)

**Conditions.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h\in\mathbb N$, $1\le h\le A$.; One algorithm attains both stated coordinate caps.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf) Theorem main part 2; Theorem strict; verified labels: thm:main (line 375), thm:strict (line 615)

Strict integer lazy-extragradient schedule and sequential full-matrix resisting construction. Deterministic adaptive algorithms.

One algorithm attains both stated coordinate caps.

### B4 - Strict integer lazy-extragradient schedule and sequential full-matrix resisting construction

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Deterministic witness

$$
\Omega\!\left(\min\{B,A^{3/2}/\sqrt h\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf)

**Conditions.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h\in\mathbb N$, $1\le h\le A$.; Arbitrary query points and unqueried outputs are allowed.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf) Theorem poor-complete; Corollary complete-frontier; verified labels: cor:complete-frontier (line 407), eq:complete-frontier (line 409), thm:poor-complete (line 1162)

Strict integer lazy-extragradient schedule and sequential full-matrix resisting construction. All deterministic measurable adaptive algorithms.

Arbitrary query points and unqueried outputs are allowed.

### B5 - Gradient transport through Hessian integration and one-dimensional product obstruction

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O\!\left(\max\{1,A^2/h\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf)

**Conditions.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h\in\mathbb N$, $h>A$.; One algorithm attains both stated coordinate caps.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf) Theorem main part 3; Theorem transport; verified labels: thm:main (line 375), sec:transport (line 438), thm:transport (line 494)

Gradient transport through Hessian integration and one-dimensional product obstruction. Deterministic adaptive algorithms.

One algorithm attains both stated coordinate caps.

### B6 - Gradient transport through Hessian integration and one-dimensional product obstruction

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Deterministic witness

$$
\Omega\!\left(\max\{1,A^2/h\}\right)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf)

**Conditions.** $0<\varepsilon\le c_0\min\{L_1^2/L_2,\Delta^{2/3}L_2^{1/3}\}$ for the sufficiently small universal $c_0$ in equation regime; hence $B\ge A\ge128$. $h\in\mathbb N$, $h>A$.; Arbitrary query points and unqueried outputs are allowed.

**Constants.** All unmarked constants are universal.

**Logarithmic factors.** None.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf) Theorem lower; Corollary complete-frontier; verified labels: cor:complete-frontier (line 407), eq:complete-frontier (line 409), thm:lower (line 761)

Gradient transport through Hessian integration and one-dimensional product obstruction. All deterministic measurable adaptive algorithms.

Arbitrary query points and unqueried outputs are allowed.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_0904. Sharp Deterministic Gradient--Hessian Tradeoffs for Finding Stationary Points. 0904_gradient_hessian_tradeoffs.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/0904/manuscript.pdf
