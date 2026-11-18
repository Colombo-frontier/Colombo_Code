# Global minimization of convex Lipschitz functions: function value and one full subgradient

**Setting ID.** `SO_FO_C01_FSG`

Single-objective optimization

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; task family: Single objective

**MODEL tags.** convexity: Convex; geometry: Full space; geometry: Norm ball; geometry: Norm mismatch allowed; smoothness: Lipschitz function

**ORACLE tags.** access order: First-order interface; feedback quality: Exact; interface family: Fsg; operation: Value subgradient; public information: Computable access; public information: Hidden objects explicitly declared; public information: Known upper bound; public information: Known exact value; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; computation: Internal arithmetic uncharged; randomization: Deterministic; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required; feasibility: Required; object: Feasible point; postprocessing: Unqueried output explicitly allowed

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Deterministic; mode: Expectation; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; measure: Oracle calls; precision: Bit precision not counted

## 1. Setting specification

### Task

Find an approximate global minimizer, with accuracy measured by suboptimality of the complete objective.

$$\min_{x\in Q}f(x)$$

### Admissible model

The public feasible set is $Q=RB_p^d=\{x\in\mathbb R^d:\|x\|_p\le R\}$. The unknown function $f:\mathbb R^d\to\mathbb R$ is globally convex and satisfies $|f(x)-f(y)|\le L\|x-y\|_q$. The exponent $p$ specifies the feasible geometry and $q$ the Lipschitz geometry. The unknown instance is $f$ on fixed public $Q$; the notation $(Q,f)$ simply records both objects.

Admissible parameter domain:

$$L>0,\quad R>0,\quad d\in\mathbb{N}_{\ge1},\quad \varepsilon>0,\quad p\ge1,\quad q\ge1$$

### Oracle interface

Public numerical inputs: $d,\ p,\ q,\ \varepsilon$.

Public upper bounds: $L,\ R$.

The unknown object is the objective $f$.

Query points lie in $Q$; feedback consists of function value and one full subgradient:

$$(f(x),g),\ g\in\partial f(x),\quad\|g\|_{q^\star}\le L,\quad1/q+1/q^\star=1$$

All responses are consistent with one fixed function instance. If several subgradients are admissible, the oracle selects one; the algorithm receives only that vector.

### Output

Return a point $\widehat x\in Q$.

The output may be unqueried or constructed from the query history, provided it is feasible. No additional function value or accuracy certificate is required.

### Loss or accuracy criterion

$$\ell(f,x)=f(x)-f^\star$$

$f^\star=\inf_{x\in Q}f(x)$. The existence, compactness, or initial-suboptimality assumptions ensure that the optimal value in this comparison is finite.

### Resource accounting

One declared full first-order response costs one call; its vector coordinates are not charged separately.

Cost is bounded uniformly on every execution path. All calls used for initialization, repetition, batching, or candidate verification are counted.

Real arithmetic, precision, and storage applied to already available information are uncharged. Public geometric operations are limited to those explicitly granted by the oracle. Query complexity alone does not imply arithmetic, memory, or communication complexity.

### Algorithm views and success guarantees

#### Deterministic / Pointwise guarantee

The algorithm uses no private random numbers. Query and stopping decisions may depend adaptively on the observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \ell(I,\widehat{x})\le\varepsilon$$

The error guarantee holds for every instance; it is not averaged over an input distribution.

#### Randomized / Expected loss

Private randomization is allowed. Queries, stopping decisions, and postprocessing may adapt to observed feedback.

No additional span, zero-respecting, linear-iteration, or memory restriction is imposed.

Interaction is adaptive to the feedback history. Every actual response is charged separately, including responses in parallel or batch queries. Internal real arithmetic, storage, and postprocessing are uncharged.

Select an algorithm using the public parameters, and then require the following for every admissible instance and response rule:

$$\exists A\ \forall I,\mathcal{O}:\ \mathbb{E}_A[\ell(I,\widehat{x})]\le\varepsilon$$

The probability space includes the algorithm's private randomness. The instance and its admissible oracle law are fixed before randomness is averaged.

## 2. Notation and parameters

$x,\widehat{x}$: Query points and final output; their permitted spaces are specified separately by the oracle and output contracts **Domain:** $\widehat{x}\in Q$.

$f$: Unknown objective, with domain and structure specified by the model

$f^\star$: Optimal value of the complete task; the oracle need not return it

$$f^\star=\inf_{x\in Q}f(x)$$

$Q$: Feasible set of the task

$$Q=RB_p^d$$

$\mathbb{R}^d$: Real vector space with $d$ coordinates

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product

$\|\cdot\|_p,\|\cdot\|_q$: Standard finite-dimensional norm with the indicated exponent **Domain:** Endpoint norm $\|x\|_\infty=\max_{1\le j\le d}|x_j|$.

$$\|x\|_a=(\sum_{j=1}^d|x_j|^a)^{1/a},\quad1\le a<\infty$$

$B_p^d$: Unit ball of the $p$ norm

$$B_p^d=\{x\in\mathbb{R}^d:\|x\|_p\le1\}$$

$\partial f(x)$: Ambient subdifferential of the corresponding convex function

$$\partial f(x)=\{g:f(u)\ge f(x)+\langle g,u-x\rangle\ \forall u\in\operatorname{dom}f\}$$

$g$: One subgradient vector selected and returned by the oracle, rather than the entire subdifferential

$d$: Dimension; a public positive integer whose dependence is tracked jointly **Domain:** $d\in\mathbb{N}_{\ge1}$.

$L$: Public upper bound on the function Lipschitz constant **Domain:** $L>0$.

$R$: Radius of the public feasible ball **Domain:** $R>0$.

$\varepsilon$: Target tolerance for the underlying error defined by the accuracy measure **Domain:** $\varepsilon>0$.

$p$: Public norm exponent specifying the feasible-set or localization geometry **Domain:** $1\le p\le\infty$.

$q$: Public norm exponent specifying the Lipschitz or gradient-regularity geometry **Domain:** $1\le q\le\infty$.

$c$: Sufficiently small universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $0<c<1$.

$C$: Sufficiently large universal positive constant, not specified numerically and potentially different between theorems. **Domain:** $C>1$.

$S_{p,q}$: Natural suboptimality scale

$$S_{p,q}=L\,R\,({d}^{\max\{0,(\frac{1}{q}-\frac{1}{p})\}})$$

$\theta_{p,q}$: Convergence exponent for mismatched geometry; not an accuracy tolerance

$$\theta_{p,q}=(\frac{1}{p}-\max\{0,(\frac{1}{q}-0.5)\})$$

$q^\star$: Hölder conjugate exponent of $q$ **Domain:** $q^\star\in[1,\infty]$.

$$1/q+1/q^\star=1,\quad1^\star=\infty,\quad\infty^\star=1$$

$a$: A positive constant fixed independently of $d,L,R,\varepsilon$, used only to select a sufficiently high-accuracy window. Hidden constants may depend on $a$. **Domain:** $a>0$.

$c_{p}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $p$. **Domain:** $c_{p}>0$.

$C_{p}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $p$. **Domain:** $C_{p}>0$.

$c_{p,q}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $p$,$q$. **Domain:** $c_{p,q}>0$.

$C_{p,q}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $p$,$q$. **Domain:** $C_{p,q}>0$.

$c_{a}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $a$. **Domain:** $c_{a}>0$.

$C_{a}$: Positive multiplicative constant, not specified numerically, depending only on the following parameters fixed in advance: $a$. **Domain:** $C_{a}>0$.

$T$: Total budget for the declared resource projection; for a risk curve, the budget is fixed in advance **Domain:** $T\in\mathbb{N}_{\ge0}$.

$\ell$: The underlying loss or error defined by the accuracy measure; its expected, probabilistic, or worst-case aggregation is specified by the success contract

$I,\mathcal{O},A$: Admissible instance, a response rule consistent with that instance, and an algorithm; the algorithm is selected before the unknown instance

$O,\Omega,\Theta,\widetilde{O},\widetilde\Omega$: Notation for asymptotic upper and lower bounds, constant-factor matching rates, and explicitly permitted logarithmic factors. Hidden-constant dependence is specified in each regime.

$\log$: Natural logarithm; changing to another fixed base affects only a constant

$\log_+$: Truncated positive logarithm

$$\log_+u=\max\{0,\log u\}$$

$[a]_+$: Positive part of a real number

$$[a]_+=\max\{a,0\}$$

$\mathbb{E}$: Expectation over the declared randomness after fixing the instance and admissible response law

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

**View.** Deterministic / Pointwise guarantee

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q3 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q4 - target accuracy cost

**View.** Randomized / Expected loss

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - All nontrivial accuracy levels in Euclidean geometry

**Region.** $p=q=2,\quad0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B4, B5

$$
c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]
$$

**Upper bound.** B3, B1

$$
C\min\{(LR/\varepsilon)^2,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The accepted envelopes differ by at most a logarithmic factor throughout the nontrivial Euclidean domain, with constant-factor optimal subregions. Ratio: $C\log(2+d)$

### R2 - Sufficiently high dimension or coarser accuracy in Euclidean geometry

**Region.** $p=q=2,\quad d\ge C(LR/\varepsilon)^2,\quad\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B4, B27

$$
c(LR/\varepsilon)^2
$$

**Upper bound.** B3, B26

$$
C(LR/\varepsilon)^2
$$

**Gap or comparison.** $C$

### R3 - Sufficiently high accuracy in Euclidean geometry

**Region.** $p=q=2,\ d\ge2,\quad\varepsilon\le cLRd^{-1/2-a},\quad a>0\text{fixed}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B5, B28

$$
c_a d\log(2+LR/\varepsilon)
$$

**Upper bound.** B1, B24

$$
C d\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $C_a$

### R4 - One-dimensional Euclidean geometry

**Region.** $p=q=2,\quad d=1,\quad\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B4, B5, B27, B28

$$
c\log(2+LR/\varepsilon)
$$

**Upper bound.** B1, B24

$$
C\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $C$

### R5 - Zero-query regime

**Region.** $\varepsilon\ge LRd^{(1/q-1/p)_+}$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q2; Q4

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** Nonnegativity of the compared quantity

$$
0
$$

**Upper bound.** B2, B25

$$
0
$$

### R6 - Matching norm with 1<p<=2

**Region.** $1<p=q\le2,\quad\varepsilon\le c_pLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B9, B10

$$
c_p[\min\{d,(LR/\varepsilon)^{\max\{2,p\}}\}+d\log_+(LR/(\varepsilon d^{1/\max\{2,p\}}))]
$$

**Upper bound.** B6, B1

$$
C_p\min\{(LR/\varepsilon)^2,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_p\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C_p\log(2+d)$; Permitted fixed-parameter dependence: p.

### R7 - Matching norm with p>2

**Region.** $2<p=q<\infty,\quad\varepsilon\le c_pLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B9, B10

$$
c_p[\min\{d,(LR/\varepsilon)^{\max\{2,p\}}\}+d\log_+(LR/(\varepsilon d^{1/\max\{2,p\}}))]
$$

**Upper bound.** B7, B8, B1

$$
C_p\min\{(LR/\varepsilon)^p,d^{1-2/p}(LR/\varepsilon)^2,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_p\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C_p\log(2+d)$; Permitted fixed-parameter dependence: p.

### R8 - Matched power-law rate in matching norms: low regime

**Region.** $d\ge C_p(LR/\varepsilon)^{\max\{2,p\}},\quad1<p=q\le2$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B9, B32

$$
c_p(LR/\varepsilon)^2
$$

**Upper bound.** B6, B29

$$
C_p(LR/\varepsilon)^2
$$

**Gap or comparison.** $C_p$

### R9 - Matched power-law rate in matching norms: high regime

**Region.** $d\ge C_p(LR/\varepsilon)^{\max\{2,p\}},\quad2<p=q<\infty$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B9, B32

$$
c_p(LR/\varepsilon)^p
$$

**Upper bound.** B7, B30

$$
C_p(LR/\varepsilon)^p
$$

**Gap or comparison.** $C_p$

### R10 - Matching l1 endpoint

**Region.** $p=q=1,\quad0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B12, B13

$$
c[\min\{d,(LR/\varepsilon)^2\log(2+d\varepsilon^2/(L^2R^2))\}+d\log_+(LR/(\varepsilon\sqrt d))]
$$

**Upper bound.** B11, B1

$$
C\min\{(LR/\varepsilon)^2\log(2d),d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C\log(2d)$

### R11 - Matching infinity-norm endpoint

**Region.** $p=q=\infty,\quad0<\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee; Randomized / Expected loss

**Quantity.** Q1; Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Optimal

**Lower bound.** B14, B37

$$
cd\log(2+LR/\varepsilon)
$$

**Upper bound.** B1, B24

$$
Cd\log(2+LR/\varepsilon)
$$

**Gap or comparison.** $C$

### R12 - Mismatched geometry with $p<\min\{q,2\}$

**Region.** $1\le p<\min\{q,2\},\quad\varepsilon\le c_{p,q}LR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B17, B18

$$
c_{p,q}[\min\{d,(LR/\varepsilon)^{1/\theta_{p,q}}\}+d\log_+(LR/(\varepsilon d^{\theta_{p,q}}))]
$$

**Upper bound.** B15, B1

$$
\min\{\min\{T:\ C_{p,q}LR[1+\sqrt{\log(2d)}\log^{1-1/\min\{q,2\}}(2T)]/T^{\theta_{p,q}}\le\varepsilon\},Cd\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: An explicit conservative polylogarithmic ratio for fixed geometry; it is not claimed that this factor is necessary at every transition point. Ratio: $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$; Permitted fixed-parameter dependence: p,q.

### R13 - Mismatched geometry with $p\ge2$

**Region.** $2\le p<q,\quad\varepsilon\le c_{p,q}LR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B17, B18

$$
c_{p,q}[\min\{d,(LR/\varepsilon)^{1/\theta_{p,q}}\}+d\log_+(LR/(\varepsilon d^{\theta_{p,q}}))]
$$

**Upper bound.** B16, B1

$$
C_p\min\{(LR/\varepsilon)^p,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: An explicit conservative polylogarithmic ratio for fixed geometry; it is not claimed that this factor is necessary at every transition point. Ratio: $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$; Permitted fixed-parameter dependence: p,q.

### R14 - l1 domain / l2 Lipschitz regularity

**Region.** $p=1,\quad q=2,\quad\varepsilon\le cLR$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B20, B18

$$
c[\min\{d,LR/\varepsilon\}+d\log_+(LR/(\varepsilon d))]
$$

**Upper bound.** B19, B15, B1

$$
C\min\{(LR/\varepsilon)\sqrt{\log(2d)\log(2+(LR/\varepsilon)\sqrt{\log(2d)})},d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2+d)\log(2+LR/\varepsilon)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C\log(2+d)\log(2+LR/\varepsilon)$

### R15 - Geometry with q<p

**Region.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Views.** Deterministic / Pointwise guarantee

**Quantity.** Q1

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B22, B23

$$
c_{p,q}[\min\{d,(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}}\}+d\log_+(LRd^{1/q-1/p-1/\max\{2,q\}}/\varepsilon)]
$$

**Upper bound.** B21, B1

$$
C_{p,q}\min\{(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}},d\log(2+LRd^{1/q-1/p}/\varepsilon)\}
$$

**Gap or comparison.** $C_{p,q}\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C_{p,q}\log(2+d)$; Permitted fixed-parameter dependence: p,q.

### R16 - All nontrivial accuracy levels in Euclidean geometry

**Region.** $p=q=2,\quad0<\varepsilon\le cLR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B27, B28

$$
c[\min\{d,(LR/\varepsilon)^2\}+d\log_+(LR/(\varepsilon\sqrt d))]
$$

**Upper bound.** B26, B24

$$
C\min\{(LR/\varepsilon)^2,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: The accepted envelopes differ by at most a logarithmic factor throughout the nontrivial Euclidean domain, with constant-factor optimal subregions. Ratio: $C\log(2+d)$

### R17 - Matching norm with 1<p<=2

**Region.** $1<p=q\le2,\quad\varepsilon\le c_pLR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B32, B33

$$
c_p[\min\{d,(LR/\varepsilon)^{\max\{2,p\}}\}+d\log_+(LR/(\varepsilon d^{1/\max\{2,p\}}))]
$$

**Upper bound.** B29, B24

$$
C_p\min\{(LR/\varepsilon)^2,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_p\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C_p\log(2+d)$; Permitted fixed-parameter dependence: p.

### R18 - Matching norm with p>2

**Region.** $2<p=q<\infty,\quad\varepsilon\le c_pLR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B32, B33

$$
c_p[\min\{d,(LR/\varepsilon)^{\max\{2,p\}}\}+d\log_+(LR/(\varepsilon d^{1/\max\{2,p\}}))]
$$

**Upper bound.** B30, B31, B24

$$
C_p\min\{(LR/\varepsilon)^p,d^{1-2/p}(LR/\varepsilon)^2,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_p\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C_p\log(2+d)$; Permitted fixed-parameter dependence: p.

### R19 - Matching l1 endpoint

**Region.** $p=q=1,\quad0<\varepsilon\le cLR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B35, B36

$$
c[\min\{d,(LR/\varepsilon)^2\log(2+d\varepsilon^2/(L^2R^2))\}+d\log_+(LR/(\varepsilon\sqrt d))]
$$

**Upper bound.** B34, B24

$$
C\min\{(LR/\varepsilon)^2\log(2d),d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C\log(2d)$

### R20 - Mismatched geometry with $p<\min\{q,2\}$

**Region.** $1\le p<\min\{q,2\},\quad\varepsilon\le c_{p,q}LR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B40, B41

$$
c_{p,q}[\min\{d,(LR/\varepsilon)^{1/\theta_{p,q}}\}+d\log_+(LR/(\varepsilon d^{\theta_{p,q}}))]
$$

**Upper bound.** B38, B24

$$
\min\{\min\{T:\ C_{p,q}LR[1+\sqrt{\log(2d)}\log^{1-1/\min\{q,2\}}(2T)]/T^{\theta_{p,q}}\le\varepsilon\},Cd\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: An explicit conservative polylogarithmic ratio for fixed geometry; it is not claimed that this factor is necessary at every transition point. Ratio: $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$; Permitted fixed-parameter dependence: p,q.

### R21 - Mismatched geometry with $p\ge2$

**Region.** $2\le p<q,\quad\varepsilon\le c_{p,q}LR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B40, B41

$$
c_{p,q}[\min\{d,(LR/\varepsilon)^{1/\theta_{p,q}}\}+d\log_+(LR/(\varepsilon d^{\theta_{p,q}}))]
$$

**Upper bound.** B39, B24

$$
C_p\min\{(LR/\varepsilon)^p,d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: An explicit conservative polylogarithmic ratio for fixed geometry; it is not claimed that this factor is necessary at every transition point. Ratio: $C_{p,q}[\log(2+d)\log(2+LR/\varepsilon)]^{2+2/\theta_{p,q}}$; Permitted fixed-parameter dependence: p,q.

### R22 - l1 domain / l2 Lipschitz regularity

**Region.** $p=1,\quad q=2,\quad\varepsilon\le cLR$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B43, B41

$$
c[\min\{d,LR/\varepsilon\}+d\log_+(LR/(\varepsilon d))]
$$

**Upper bound.** B42, B38, B24

$$
C\min\{(LR/\varepsilon)\sqrt{\log(2d)\log(2+(LR/\varepsilon)\sqrt{\log(2d)})},d\log(2+LR/\varepsilon)\}
$$

**Gap or comparison.** $C\log(2+d)\log(2+LR/\varepsilon)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C\log(2+d)\log(2+LR/\varepsilon)$

### R23 - Geometry with q<p

**Region.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Views.** Randomized / Expected loss

**Quantity.** Q3

**Resource.** One declared full first-order response costs one call; its vector coordinates are not charged separately.

**Status.** Logarithmic gap

**Lower bound.** B45, B46

$$
c_{p,q}[\min\{d,(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}}\}+d\log_+(LRd^{1/q-1/p-1/\max\{2,q\}}/\varepsilon)]
$$

**Upper bound.** B44, B24

$$
C_{p,q}\min\{(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}},d\log(2+LRd^{1/q-1/p}/\varepsilon)\}
$$

**Gap or comparison.** $C_{p,q}\log(2+d)$

**Comparison argument.** The comparison uses the same model, query domain, output requirement, success guarantee, and resource convention. The upper envelope minimizes over applicable algorithms; the lower envelope maximizes over applicable hard instances. A finite sum of lower bounds is used only up to a constant factor. Rate comparison: Both bounds and their validity regions are retained for this contract. An intersection of upper bounds alone does not establish a minimax transition. Ratio: $C_{p,q}\log(2+d)$; Permitted fixed-parameter dependence: p,q.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Output mapping.** The output must lie in the declared output space and satisfy its feasibility, support, or atomic-hull restrictions. Permission to return an unqueried point does not remove these restrictions.

**Resource mapping.** Every primitive response is charged. Sample, component, proximal, and communication costs use the units declared for the target setting. Resource coordinates achieved by one algorithm remain a joint vector; coordinatewise minima from different algorithms are not combined.

### B1 - Centroid cutting planes and subgradient certificates

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C d\log(2+LRd^{(1/q-1/p)_+}/\varepsilon)
$$

**Sources.** [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le c LRd^{(1/q-1/p)_+}$$

**Dimension conditions.** $0<\varepsilon\le c LRd^{(1/q-1/p)_+}$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has a subgradient-only implementation. Cuts use the returned subgradient; the feasible ball has $q$-norm diameter at most $2Rd^{(1/q-1/p)_+}$.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B2 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge LRd^{(1/q-1/p)_+}$$

**Dimension conditions.** $\varepsilon\ge LRd^{(1/q-1/p)_+}$

**Oracle correspondence.** Return the public ball center without querying the unknown objective.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B3 - Euclidean projected subgradient descent or mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C(LR/\varepsilon)^2
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$p=q=2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B4 - Information-theoretic hard instances for nonsmooth convex optimization

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,(LR/\varepsilon)^2\}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1 and Proposition V.5 with its proof; the literal dimension range of VI.3 is not adopted without its qualifications

### B5 - Multiscale information-theoretic hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c d\log_+\frac{LR}{\varepsilon\sqrt d}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1 and Proposition V.5 with its proof; the literal dimension range of VI.3 is not adopted without its qualifications

### B6 - Mirror descent for matching norms

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
\frac C{p-1}(LR/\varepsilon)^2
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$1<p=q\le2,\quad\varepsilon\le c_pLR$$

**Dimension conditions.** $1<p=q\le2,\quad\varepsilon\le c_pLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B7 - Mirror descent for matching norms

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_p(LR/\varepsilon)^p
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$2<p=q<\infty,\quad\varepsilon\le c_pLR$$

**Dimension conditions.** $2<p=q<\infty,\quad\varepsilon\le c_pLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B8 - Euclidean subgradient descent after norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C d^{1-2/p}(LR/\varepsilon)^2
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$2<p=q<\infty,\quad\varepsilon\le c_pLR$$

**Dimension conditions.** $2<p=q<\infty,\quad\varepsilon\le c_pLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B9 - Information-theoretic hard instances for matching geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_p\min\{d,(LR/\varepsilon)^{\max\{2,p\}}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1<p=q<\infty,\quad\varepsilon\le c_p LR$$

**Dimension conditions.** $1<p=q<\infty,\quad\varepsilon\le c_p LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B10 - Multiscale hard instances for matching geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_p d\log_+\frac{LR}{\varepsilon d^{1/\max\{2,p\}}}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$1<p=q<\infty,\quad\varepsilon\le c_p LR$$

**Dimension conditions.** $1<p=q<\infty,\quad\varepsilon\le c_p LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

### B11 - Entropy-regularized mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C(LR/\varepsilon)^2\log(2d)
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$p=q=1,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=1,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B12 - Information-theoretic hard instances in $\ell_1$ geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,(LR/\varepsilon)^2\log(2+d\varepsilon^2/(L^2R^2))\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$p=q=1,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=1,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B13 - Multiscale hard instances in $\ell_1$ geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd\log_+\frac{LR}{\varepsilon\sqrt d}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=1,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=1,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

### B14 - Hard instances on an $\ell_\infty$ box

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd\log(2+LR/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=\infty,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=\infty,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

### B15 - Stable Movement

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
\min\left\{T\in\mathbb{N}:\frac{C_{p,q}LR[1+\sqrt{\log(2d)}\log^{1-1/\min\{q,2\}}(2T)]}{T^{\theta_{p,q}}}\le\varepsilon\right\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf)

**Conditions.** $$1\le p<\min\{q,2\},\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $1\le p<\min\{q,2\},\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem9; Eqs.(24)–(28)

### B16 - Mirror descent for mismatched geometry

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_p(LR/\varepsilon)^p
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$2\le p<q,\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $2\le p<q,\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B17 - Hard instances for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}\min\{d,(LR/\varepsilon)^{1/\theta_{p,q}}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B18 - Multiscale reduction for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}d\log_+\frac{LR}{\varepsilon d^{\theta_{p,q}}}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B19 - Accelerated mirror method for mismatched geometry

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C\frac{LR}{\varepsilon}\sqrt{\log(2d)\log(2+(LR/\varepsilon)\sqrt{\log(2d)})}
$$

**Sources.** [5](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,\quad q=2,\quad\varepsilon\le cLR$$

**Dimension conditions.** $p=1,\quad q=2,\quad\varepsilon\le cLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [5](https://arxiv.org/pdf/2609.32910) theorem: AppendixE.1, PropositionE.1, LemmaE.2

### B20 - Hard instances for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,LR/\varepsilon\}
$$

**Sources.** [5](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,\quad q=2,\quad\varepsilon\le cLR$$

**Dimension conditions.** $p=1,\quad q=2,\quad\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [5](https://arxiv.org/pdf/2609.32910) theorem: Proposition D.6, PDF p. 36; full-space value-subgradient queries are allowed; $d\ge2^{p+2}T$

### B21 - Norm embedding and mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** Deterministic witness

$$
C_{p,q}(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}}
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$$

**Dimension conditions.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B22 - Hard instances from reverse norm embedding

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}\min\{d,(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$$

**Dimension conditions.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B23 - Reverse norm embedding and multiscale reduction

**Admission.** Included in the bracket

**Direction.** lower

**View.** Deterministic / Pointwise guarantee

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}d\log_+\frac{LRd^{1/q-1/p-1/\max\{2,q\}}}{\varepsilon}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$$

**Dimension conditions.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B24 - Centroid cutting planes and subgradient certificates

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C d\log(2+LRd^{(1/q-1/p)_+}/\varepsilon)
$$

**Sources.** [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$0<\varepsilon\le c LRd^{(1/q-1/p)_+}$$

**Dimension conditions.** $0<\varepsilon\le c LRd^{(1/q-1/p)_+}$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has a subgradient-only implementation. Cuts use the returned subgradient; the feasible ball has $q$-norm diameter at most $2Rd^{(1/q-1/p)_+}$.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B25 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Sources.** [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

**Conditions.** $$\varepsilon\ge LRd^{(1/q-1/p)_+}$$

**Dimension conditions.** $\varepsilon\ge LRd^{(1/q-1/p)_+}$

**Oracle correspondence.** Return the public ball center without querying the unknown objective.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

### B26 - Euclidean projected subgradient descent or mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C(LR/\varepsilon)^2
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$p=q=2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B27 - Information-theoretic hard instances for nonsmooth convex optimization

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,(LR/\varepsilon)^2\}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1 and Proposition V.5 with its proof; the literal dimension range of VI.3 is not adopted without its qualifications

### B28 - Multiscale information-theoretic hard instances

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c d\log_+\frac{LR}{\varepsilon\sqrt d}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=2,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=2,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem V.1 and Proposition V.5 with its proof; the literal dimension range of VI.3 is not adopted without its qualifications

### B29 - Mirror descent for matching norms

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
\frac C{p-1}(LR/\varepsilon)^2
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$1<p=q\le2,\quad\varepsilon\le c_pLR$$

**Dimension conditions.** $1<p=q\le2,\quad\varepsilon\le c_pLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B30 - Mirror descent for matching norms

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_p(LR/\varepsilon)^p
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$2<p=q<\infty,\quad\varepsilon\le c_pLR$$

**Dimension conditions.** $2<p=q<\infty,\quad\varepsilon\le c_pLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B31 - Euclidean subgradient descent after norm conversion

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C d^{1-2/p}(LR/\varepsilon)^2
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$2<p=q<\infty,\quad\varepsilon\le c_pLR$$

**Dimension conditions.** $2<p=q<\infty,\quad\varepsilon\le c_pLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B32 - Information-theoretic hard instances for matching geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_p\min\{d,(LR/\varepsilon)^{\max\{2,p\}}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1<p=q<\infty,\quad\varepsilon\le c_p LR$$

**Dimension conditions.** $1<p=q<\infty,\quad\varepsilon\le c_p LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B33 - Multiscale hard instances for matching geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_p d\log_+\frac{LR}{\varepsilon d^{1/\max\{2,p\}}}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$1<p=q<\infty,\quad\varepsilon\le c_p LR$$

**Dimension conditions.** $1<p=q<\infty,\quad\varepsilon\le c_p LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

### B34 - Entropy-regularized mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C(LR/\varepsilon)^2\log(2d)
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$p=q=1,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=1,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B35 - Information-theoretic hard instances in $\ell_1$ geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,(LR/\varepsilon)^2\log(2+d\varepsilon^2/(L^2R^2))\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$p=q=1,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=1,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B36 - Multiscale hard instances in $\ell_1$ geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd\log_+\frac{LR}{\varepsilon\sqrt d}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=1,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=1,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

### B37 - Hard instances on an $\ell_\infty$ box

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
cd\log(2+LR/\varepsilon)
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144)

**Conditions.** $$p=q=\infty,\quad0<\varepsilon\le cLR$$

**Dimension conditions.** $p=q=\infty,\quad0<\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

### B38 - Stable Movement

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
\min\left\{T\in\mathbb{N}:\frac{C_{p,q}LR[1+\sqrt{\log(2d)}\log^{1-1/\min\{q,2\}}(2T)]}{T^{\theta_{p,q}}}\le\varepsilon\right\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf)

**Conditions.** $$1\le p<\min\{q,2\},\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $1\le p<\min\{q,2\},\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Local argument.** A1

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem9; Eqs.(24)–(28)

### B39 - Mirror descent for mismatched geometry

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_p(LR/\varepsilon)^p
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$2\le p<q,\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $2\le p<q,\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B40 - Hard instances for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}\min\{d,(LR/\varepsilon)^{1/\theta_{p,q}}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B41 - Multiscale reduction for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}d\log_+\frac{LR}{\varepsilon d^{\theta_{p,q}}}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$$

**Dimension conditions.** $1\le p<q\le\infty,\quad\varepsilon\le c_{p,q}LR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B42 - Accelerated mirror method for mismatched geometry

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C\frac{LR}{\varepsilon}\sqrt{\log(2d)\log(2+(LR/\varepsilon)\sqrt{\log(2d)})}
$$

**Sources.** [5](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,\quad q=2,\quad\varepsilon\le cLR$$

**Dimension conditions.** $p=1,\quad q=2,\quad\varepsilon\le cLR$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [5](https://arxiv.org/pdf/2609.32910) theorem: AppendixE.1, PropositionE.1, LemmaE.2

### B43 - Hard instances for mismatched geometry

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c\min\{d,LR/\varepsilon\}
$$

**Sources.** [5](https://arxiv.org/pdf/2609.32910)

**Conditions.** $$p=1,\quad q=2,\quad\varepsilon\le cLR$$

**Dimension conditions.** $p=1,\quad q=2,\quad\varepsilon\le cLR$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [5](https://arxiv.org/pdf/2609.32910) theorem: Proposition D.6, PDF p. 36; full-space value-subgradient queries are allowed; $d\ge2^{p+2}T$

### B44 - Norm embedding and mirror descent

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** Deterministic witness

$$
C_{p,q}(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}}
$$

**Sources.** [1](https://arxiv.org/pdf/1107.4080)

**Conditions.** $$1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$$

**Dimension conditions.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Oracle correspondence.** A query returns $(f(x),g)$, where $g\in\partial f(x)$ and $\|g\|_{q^\star}\le L$. The upper bound has an implementation using only the subgradient, so the additional function value may be ignored.

**Guarantee conversion.** A deterministic error bound for every instance also gives the same expected-error bound. Probability guarantees are used only when an explicit conversion to the target contract is recorded.

**Source location.** [1](https://arxiv.org/pdf/1107.4080) theorem: Lemma 2 and Section 7: mirror descent in the declared norm geometry

### B45 - Hard instances from reverse norm embedding

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}\min\{d,(LRd^{1/q-1/p}/\varepsilon)^{\max\{2,q\}}\}
$$

**Sources.** [3](https://arxiv.org/pdf/2609.20701) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$$

**Dimension conditions.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [3](https://arxiv.org/pdf/2609.20701) theorem: Theorem 19: power-law lower bound for fixed geometry, with the dimension truncation retained

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

### B46 - Reverse norm embedding and multiscale reduction

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized / Expected loss

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
c_{p,q}d\log_+\frac{LRd^{1/q-1/p-1/\max\{2,q\}}}{\varepsilon}
$$

**Sources.** [2](https://arxiv.org/pdf/1407.5144) [4](https://arxiv.org/pdf/2609.20687)

**Conditions.** $$1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$$

**Dimension conditions.** $1\le q<p\le\infty,\quad\varepsilon\le c_{p,q}LRd^{1/q-1/p}$

**Oracle correspondence.** Applicable interfaces: one full subgradient, function value and one full subgradient. Lower bounds transfer only through the explicitly recorded simulations from a stronger interface to a weaker one.

**Guarantee conversion.** The hard-instance quantifiers cover the algorithm class explicitly specified for this bound. Each target setting retains its expected-error or success-probability criterion; a deterministic lower bound is not promoted to a randomized lower bound.

**Source location.** [2](https://arxiv.org/pdf/1407.5144) theorem: Theorem IV.2, Proposition VI.7, and the recursive-box proof

**Source location.** [4](https://arxiv.org/pdf/2609.20687) theorem: Appendix A, equations (11)–(12), Facts 31–32, and equation (19)

## 5. Local arguments

### A1 - Subgradient certificates and centroid cuts

**Scope.** One full subgradient is sufficient. Public compact convex geometry and exact internal geometric computation are available.

**Algorithm scope.** Deterministic upper-bound witness; valid as an upper bound for randomized views.

Let $Q\subset\mathbb R^d$ be public, compact, convex, and full dimensional, with diameter at most $D$ in the stated norm. Suppose all returned subgradients have dual norm at most $L$. Query $g_i\in\partial f(x_i)$ at the centroid of the current body and retain $\langle g_i,x_i-x\rangle\ge0$. The centroid halfspace theorem bounds the retained volume by $(1-e^{-1})^T\operatorname{vol}(Q)$.

The computable certificate is
$$
\Gamma_T=\min_{\lambda\in\Delta_T}\max_{x\in Q}\sum_i\lambda_i\langle g_i,x_i-x\rangle
=\max_{x\in Q}\min_i\langle g_i,x_i-x\rangle.
$$
The equality is convex minimax. Subgradient inequalities and convexity imply
$f(\sum_i\lambda_ix_i)-\min_Qf\le\Gamma_T$.
If $\Gamma_T>\epsilon$, choose $z\in Q$ with all cut margins greater than $\epsilon$. The copy $(1-a)z+aQ$, where $a=\epsilon/[2(\epsilon+LD)]$, survives every cut. Its volume is $a^d\operatorname{vol}(Q)$, contradicting centroid shrinkage once $T>C d\log(2+LD/\epsilon)$. If the body loses volume earlier, the same positive-volume argument already certifies the error. No function values or inscribed-ball estimate are required.

For $Q=RB_p^d$ and $\ell_q$-Lipschitz objectives, use $D=2Rd^{(1/q-1/p)_+}$. Returning the center has error at most $LRd^{(1/q-1/p)_+}$, giving the coarse zero-query regime. Exact centroid, minimax, and public geometric calculations are uncharged internal operations.

For a deterministic selector with total movement at most $W(T)$ on nested convex sets, instead impose deep cuts of margin $2LW(T)/T$. If all $T$ sets are nonempty, every move has length at least $2W(T)/T$, contradicting the movement bound. At the first empty intersection, minimax gives error at most $2LW(T)/T$. Substitution of the cited stable-movement theorem yields the recorded nondual upper bound. Its deterministic information scope is distinct from the scope of randomized implementations.

**Limits of the argument.** The stable-selector branch imports its movement theorem and does not claim efficient deterministic arithmetic time.

**Sources.** [6](https://arxiv.org/pdf/1405.4980) [7](https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf) [3](https://arxiv.org/pdf/2609.20701)

## References

[1] Nathan Srebro; Karthik Sridharan; Ambuj Tewari. On the Universality of Online Mirror Descent. 2011.

https://arxiv.org/pdf/1107.4080

[2] Gábor Braun; Cristóbal Guzmán; Sebastian Pokutta. Lower Bounds on the Oracle Complexity of Nonsmooth Convex Optimization via Information Theory. 2017; arXiv v3 2023.

https://arxiv.org/pdf/1407.5144

[3] David Martínez-Rubio; Cristóbal Guzmán. Stable Movement for Nondual Lipschitz Convex Optimization: Efficiency and Nearly Optimal Oracle Rates. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20701

[4] David Martínez-Rubio; Brian Bullins; Cristóbal Guzmán; Mathieu Molina. The First-Order Oracle Complexity of Lipschitz Convex Optimization in Nondual Settings. 2026-09-17; preprintv1.

https://arxiv.org/pdf/2609.20687

[5] Timofei Loginov, Alexander Gasnikov, Yuriy Dorn, Aleksandr Shestakov, Nazarii Tupitsa, Osman Osmanov and Darina Dvinskikh. The Complexity of Convex Optimization with Mismatched Geometry. 2026-09-26, arXiv v1 preprint.

https://arxiv.org/pdf/2609.32910

[6] Sébastien Bubeck. Convex Optimization: Algorithms and Complexity. 2015.

https://arxiv.org/pdf/1405.4980

[7] Arkadi Nemirovski; Shmuel Onn; Uriel G. Rothblum. Accuracy Certificates for Computational Problems with Convex Structure. 2010.

https://www2.isye.gatech.edu/~nemirovs/MOR_AccuracyCertificates.pdf
