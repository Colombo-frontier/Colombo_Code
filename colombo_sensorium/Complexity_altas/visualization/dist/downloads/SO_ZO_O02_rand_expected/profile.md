# Exact comparison feedback for smooth strongly convex objectives

**Setting ID.** `SO_ZO_O02_rand_expected`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Polynomial gap present

**Gap classes present.** Polynomial gap; Logarithmic gap

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; initialization: Global initial gap; smoothness: Lipschitz gradient

**ORACLE tags.** access order: Zeroth-order interface; interface family: Exact comparison; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

Strong convexity is defined in the Euclidean norm: $f((1-t)x+ty)\le(1-t)f(x)+tf(y)-\frac{\mu}{2}t(1-t)\|x-y\|_2^2$ for $x,y$ and $t\in[0,1]$ in the domain.

$f_*:=\inf_{x\in\mathbb{R}^d}f(x)>-\infty$, and the given initial point $x_0$ satisfies $f(x_0)-f_*\le\Delta$.

### Oracle interface

Any finite point pair $(x,y)\in\mathbb{R}^d\times\mathbb{R}^d$ may be queried, returning $\operatorname{sign}(f(x)-f(y))\in\{-1,0,1\}$. Equal values produce zero. Neither the magnitude of the difference nor either function value is revealed.

The public inputs are $d$, $\beta$, $\mu$, $\Delta$, $\varepsilon$, $x_0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One point-pair comparison costs $1$ call. Every repeated comparison and every comparison in a line search is charged. The budget $T$ counts scalar comparison replies.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$\Delta$: Known upper bound on the initial objective gap **Domain:** $\Delta\ge0$.

$f(x_0)-\inf_{x\in\mathbb{R}^d}f(x)\le\Delta$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

$Q_\Delta$: Normalized ratio of the initial objective gap to the target accuracy **Domain:** $Q_\Delta\ge0$.

$Q_\Delta=\Delta/\varepsilon$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $\mathbb{R}^d$.

$I$: Complete problem instance **Domain:** $I\in\mathcal{I}$.

Includes the unknown objective and its admissible feedback distribution or environment law. Public parameters are fixed before the quantifiers.

$\mathcal{I}$: Admissible instance class determined by the eight specification fields in this profile **Domain:** Instances satisfying the public parameter bounds.

$\mathcal{A}$: Algorithm or strategy **Domain:** Measurable adaptive strategies allowed in this profile.

The algorithm is selected before the hidden instance.

$\ell$: Base loss or residual **Domain:** $\ell:\mathcal{I}\times\mathcal{X}_{\mathrm{out}}\to[0,+\infty]$.

The exact formula appears in this profile's performance-criterion section.

$\mathbb{E},\Pr$: Expectation and probability **Domain:** Evaluated over the algorithmic and feedback randomness specified by this profile's guarantee.

Fix the instance first; aggregate cost and error separately.

$\inf,\sup$: Infimum and supremum **Domain:** Evaluated only over the variable sets explicitly specified in the formula.

In the risk definition, the infimum over algorithms precedes the supremum over instances or centers.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product **Domain:** $\|x\|_2=\sqrt{\langle x,x\rangle}$.

$\langle x,y\rangle=x^\top y$

$B_p(c,R)$: Closed norm ball **Domain:** $p\in[1,\infty],\ R\ge0$.

$B_p(c,R)=\{x:\|x-c\|_p\le R\}$; $B_2$ denotes the Euclidean ball.

$N,T$: Actual call count and declared budget **Domain:** $N,T\in\mathbb{N}_0$.

A fixed budget bounds every execution path; the Markov specification uses an expected budget.

$O,\Omega,\Theta,\widetilde{O}$: Asymptotic upper bounds, lower bounds, matching orders, and upper bounds with hidden logarithms **Domain:** Within the joint parameter window specified for each complexity regime.

Dependence of hidden constants on fixed parameters is stated separately for each bound. Tilde notation may hide logarithmic factors only in the declared variables.

$c,C,c_\alpha,C_\alpha$: Positive constant in a proof or asymptotic bound **Domain:** $0<c,C,c_\alpha,C_\alpha<\infty$.

Unsubscripted constants have the dependencies stated in the bound; constants subscripted by $\alpha$ may depend only on the fixed smoothness order.

$\log,\log_+,e$: Natural logarithm, truncated logarithm, and Euler's number **Domain:** $z>0$.

$\log_+(z)=\max\{0,\log z\}$; $e=\exp(1)$, and $\log_2$ denotes the base-two logarithm.

$f,f_*$: Population objective and its optimal value **Domain:** $f:\mathcal{X}_{\mathrm{fun}}\to\mathbb{R}$.

$f_*=\inf_{x\in \mathbb{R}^d}f(x)$.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$R_{\mathrm{hard}}$: Localization radius chosen by the lower-bound proof **Domain:** $R_{\mathrm{hard}}>0$.

It ensures that the hard subclass meets the known initial-gap bound without providing additional algorithmic information. Its choice is stated separately for each bound.

$x_0$: Public initial point **Domain:** $x_0\in\mathbb{R}^d$.

Belongs to the feasible domain required by the model.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One binary comparison reply

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

#### Q2 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One binary comparison reply

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime O02.R1

**Region.** $\kappa\ge2$, $\Delta/\varepsilon\ge128^2$, $\Delta/\varepsilon\ge\min\{\kappa,d^2\}$.

**Quantity.** Q1

**Resource.** One binary comparison reply

**Status.** Logarithmic gap

**Lower bound.** B2, B5

$$
\Omega(d\max\{\min(d,\sqrt\kappa),\log Q_\Delta\})
$$

**Upper bound.** B1, B4

$$
\min\{\widetilde{O}(d\sqrt\kappa\log Q_\Delta),O(d^2\log(d\kappa Q_\Delta))\}
$$

**Gap or comparison.** $\operatorname{polylog}(d,\kappa ,Q\Delta )$

### R2 - Parameter regime O02.R2

**Region.** $\kappa\ge2$, $128^2\le\Delta/\varepsilon<\min\{\kappa,d^2\}$.

**Quantity.** Q1

**Resource.** One binary comparison reply

**Status.** Polynomial gap

**Lower bound.** B2, B5

$$
\Omega(d\sqrt{Q_\Delta})
$$

**Upper bound.** B1, B4

$$
\min\{\widetilde{O}(d\sqrt\kappa\log Q_\Delta),O(d^2\log(d\kappa Q_\Delta))\}
$$

**Gap or comparison.** $\widetilde{O}(\min\{d,\sqrt\kappa\}/\sqrt{Q_\Delta})$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Comparison-based coordinate acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left(d\sqrt\kappa\log(\Delta/\varepsilon)\right)
$$

**Sources.** [3](https://proceedings.neurips.cc/paper_files/paper/2024/file/26289c647c6828e862e271ca3c490486-Paper-Conference.pdf)

**Conditions.** Set each coordinate to $\beta _i\le \beta$; the original expression is $\widetilde{O}((\sum_i\sqrt{\beta _i})/\sqrt\mu\log(\Delta/\varepsilon))$. Line-search precision introduces an additional logarithm.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Source location.** [3](https://proceedings.neurips.cc/paper_files/paper/2024/file/26289c647c6828e862e271ca3c490486-Paper-Conference.pdf) theorem: Theorem 4.1 and the subsequent oracle-call accounting; pdf pages: 7; printed pages: 7

### B2 - Comparison-information packing and the exact-value subclass

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\log(\Delta/\varepsilon)\right)
$$

**Sources.** [2](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf)

**Conditions.** Use shifted spherical quadratics with a known Hessian and center radius $\sqrt{2\Delta/\mu}$. One reply has at most three possible symbols; $\varepsilon\le c\Delta$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A1

**Source location.** [2](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf) theorem: Theorem 1 and its finite-information packing argument, PDF page 3

### B3 - Comparison-information packing and the exact-value subclass

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(d\min\{d,\sqrt\kappa,\sqrt{\Delta/\varepsilon}\}\right)
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [5](https://arxiv.org/html/2610.19652v1)

**Conditions.** $\varepsilon\le c\Delta$. The hard construction sets $R_{\mathrm{hard}}=\sqrt{2\Delta/\beta}$ to satisfy the initial-gap bound. This radius is chosen in the proof and is not an additional public input.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4; pdf pages: 4; printed pages: 4

### B4 - Comparison-based coordinate acceleration or localization

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(d^2\log(d\kappa Q_\Delta))
$$

**Sources.** [4](https://arxiv.org/html/2405.11454v1)

**Conditions.** $\kappa \ge 1$ and $Q\Delta =\Delta /\varepsilon \ge 16$; $global \mu -SC,\beta -smooth,$ with initial $gap\le \Delta$.

**Guarantee conversion.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Local argument.** A3

**Source location.** [4](https://arxiv.org/html/2405.11454v1) theorem: Version 1, Theorem 3; strong convexity converts the initial-gap bound to a localization radius; pdf pages: 9

### B5 - Comparison-information packing and the exact-value subclass

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(d\min\{d,\sqrt\kappa,\sqrt{Q_\Delta}\})
$$

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [5](https://arxiv.org/html/2610.19652v1)

**Conditions.** $\kappa \ge 2$; $Q\Delta \ge 48$.

**Guarantee conversion.** The source lower bound covers adaptive randomized algorithms. The subclass reduction preserves the objective gap and accuracy window; deterministic algorithms are included in this quantifier range.

**Local argument.** A2

**Source location.** [1](https://arxiv.org/html/2610.00345v1) theorem: Corollary 2.4, with $R=\sqrt{2\Delta/\beta}$; pdf pages: 4

## 5. Local arguments

### A1 - Finite feedback entropy gives a precision lower bound

**Scope.** Exact comparison feedback, arbitrary adaptive randomized queries, and a public initial-gap budget in the strongly convex model.

At sufficiently small $\varepsilon/\Delta$, at least $\Omega(d\log(\Delta/\varepsilon))$ comparisons are necessary, including an expected-error guarantee.

Use shifted isotropic quadratics $f_\theta(x)=\mu\|x-\theta\|^2/2$ with centers in a ball of radius $\sqrt{2\Delta/\mu}$ about the initial point. They are $\mu$-strongly convex and $\beta$-smooth for any public $\beta\ge\mu$. Pack the center ball at separation greater than twice the success radius $\sqrt{6\varepsilon/\mu}$. Standard volume comparison gives a packing of logarithmic size at least $c d\log(\Delta/\varepsilon)$ on a sufficiently small fixed accuracy window.

Each exact comparison has at most three outcomes and thus conveys at most $\log3$ nats, even for adaptive query points and after conditioning on the independent random seed. Fano's inequality requires a constant fraction of the packing entropy to identify the center with probability $2/3$. A target expected gap at most $\varepsilon$ implies this success level at error $3\varepsilon$ by Markov, and the separated success balls decode the center. This proves the bound without imposing a spatial restriction on queries.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [2](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf)

### A2 - Exact-value lower bounds transferred to comparison feedback

**Scope.** The comparison oracle returns only the exact order of two function values. Query/output domains, model budgets, and guarantees are preserved.

Two exact scalar values simulate one comparison. Therefore a fixed-success exact-value lower bound $L$ gives a comparison lower bound $L/2$. Expected-error targets require a separate constant-factor accuracy conversion.

At each adaptive comparison request $(x,y)$, query both exact values and return their order, including the declared tie convention. The same seed and transcript generate the same next query and output, using at most twice the comparison budget. Hence a comparison algorithm contradicts a value lower theorem only when all source model and guarantee conditions match.

For smooth convex objectives, apply the dimension/accuracy branch of Dorn et al., Theorem 2.1, at $Q\ge32$, and its logarithmic strongly convex subclass at $Q\ge128^2$; maximize only on their common window. For a strongly convex model with initial gap $\Delta$, choose a hard-instance radius $R_h=\sqrt{2\Delta/\beta}$. Smoothness at the global minimizer gives the required initial gap. If the target guarantee is expected error $\varepsilon$, Markov supplies success $2/3$ at error $3\varepsilon$; then the source scale is $Q_h=2\Delta/(3\varepsilon)$ and must be at least 32. No new public radius is added to the target specification.

For nonconvex gradient stationarity, use the exact-value hard subclass with a proof-only Lipschitz budget satisfying $L^2\ge\beta\Delta$. The source cap $B=\min\{\beta\Delta,L^2\}$ becomes $\beta\Delta$. Retain its small-gradient window and dimension requirement $d\ge C(\beta\Delta/\varepsilon^2)\log(2+\beta\Delta/\varepsilon^2)$. The same two-value simulation then gives the registered comparison lower bound.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/html/2610.00345v1) [5](https://arxiv.org/html/2610.19652v1)

### A3 - Using a public strong-convexity radius in a convex comparison method

**Scope.** Global convexity and smoothness, strong convexity $\mu$, initial gap $\Delta$, and exact comparisons.

A deterministic comparison upper is $O(d^2\log(d\kappa\Delta/\varepsilon))$ in the stated nontrivial window.

Strong convexity gives $\|x_0-x_*\|^2\le2\Delta/\mu$. Translate $x_0$ to zero and apply Zhang and Li's convex comparison theorem with public radius $R_{\rm loc}=\sqrt{2\Delta/\mu}$. Its scale is $\beta R_{\rm loc}^2/\varepsilon=2\kappa\Delta/\varepsilon$. Substitution yields the displayed count. The algorithm uses comparisons only and its pointwise objective-error guarantee also implies expected error. It is a separate upper branch, to be compared with other admissible accelerated comparison algorithms rather than substituted into their formulas.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [4](https://arxiv.org/html/2405.11454v1)

## References

[1] Dorn, Dvinskikh, Loginov, Osmanov, Shestakov, Tupitsa and Gasnikov. Lower Bounds For Gradient-Free Convex Optimization And Convex-Concave Saddle-Point Problems. arXiv:2610.00345v1.

https://arxiv.org/html/2610.00345v1

[2] Jamieson, Nowak and Recht. Query Complexity of Derivative-Free Optimization. NeurIPS 2012.

https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf

[3] Lobanov, Gasnikov and Krasnov. Acceleration Exists! Optimization Problems When Oracle Can Only Compare Objective Function Values. NeurIPS 2024, pp. 21428--21460.

https://proceedings.neurips.cc/paper_files/paper/2024/file/26289c647c6828e862e271ca3c490486-Paper-Conference.pdf

[4] Zhang and Li. Comparisons Are All You Need for Optimizing Smooth Functions. arXiv:2405.11454v1, 2024; the specified early version.

https://arxiv.org/html/2405.11454v1

[5] Xia and Yuan. On Global Joint Lower Bounds in Zeroth-Order Nonconvex Optimization. arXiv:2610.19652v1, 2026-10-14.

https://arxiv.org/html/2610.19652v1
