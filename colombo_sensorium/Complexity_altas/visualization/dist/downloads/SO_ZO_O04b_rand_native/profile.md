# Noisy comparisons: a fixed bounded query cube

**Setting ID.** `SO_ZO_O04b_rand_native`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Other quantified gap present; Bounds missing

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Lipschitz gradient

**ORACLE tags.** access order: Zeroth-order interface; interface family: Noisy comparison; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Probability

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

Strong convexity is defined in the Euclidean norm: $f((1-t)x+ty)\le(1-t)f(x)+tf(y)-\frac{\mu}{2}t(1-t)\|x-y\|_2^2$ for $x,y$ and $t\in[0,1]$ in the domain.

$0<\mu\le\beta$. The unique minimizer satisfies $x_*\in Q_c:=[-R,R]^d$, and the known initial point is $0$. Consequently, the initial objective gap is at most $\beta dR^2/2$.

The comparison kernel has parameters $a\ge0$, $0<c_0\le1/4$, and $\nu>0$; when $a=0$, require $\nu\le c_0$. These parameters describe the feedback distribution and do not alter the objective's strong-convexity and smoothness budgets.

### Oracle interface

Both entries of the pair $(x,y)$ must belong to $Q_c=[-R,R]^d$. The response is $C_t\in\{-1,1\}$. When $f(x)\ne f(y)$, conditional on the history and current pair, the probability of correct ordering is at least $\frac12+\min\{c_0,\nu|f(y)-f(x)|^a\}$, where the correct sign is $\operatorname{sign}(f(y)-f(x))$.

Each instance has a fixed unknown response kernel on point pairs. Repeated comparisons use fresh independent randomness, and ties may be resolved arbitrarily. Performance is worst-case over all admissible response kernels.

The public inputs are $d$, $\beta$, $\mu$, $R$, $\varepsilon$, $a$, $c_0$, $\nu$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in Q_c=[-R,R]^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One point-pair comparison costs $1$ call. Every repeated comparison and every comparison in a line search is charged. The budget $T$ counts scalar comparison replies.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. The error requirement is $\Pr(\ell(I,\widehat{x})\le \varepsilon)\ge2/3$.

Probability is over both the algorithm's seed and all feedback randomness, after fixing the instance and admissible environment law.

Oracle cost uses a deterministic worst-case budget: $N\le T$ on every possible execution path. For multiple resources, coordinatewise caps apply jointly along the same path.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$R$: Half side length of the minimizer-localization cube **Domain:** $R>0$.

$x_*\in[-R,R]^d$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$a$: Margin exponent for the correctness probability of a noisy comparison **Domain:** $a\ge0$.

$c_0$: Saturation level of the comparison's advantage over random guessing **Domain:** $0<c_0\le1/4$.

$\nu$: Margin coefficient in comparison correctness probability **Domain:** $\nu>0$, with $\nu\le c_0$ when $a=0$.

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

$\bar\varepsilon$: Normalized optimization accuracy for comparison feedback **Domain:** $\bar\varepsilon>0$.

$\bar\varepsilon=\varepsilon/(\mu R^2)$

$\bar\nu$: Normalized comparison-margin coefficient **Domain:** $\bar\nu>0$.

$\bar\nu=\nu(\mu R^2)^a$

$x,y,u$: Function arguments and dummy variables in the formulas **Domain:** $x,y,u\in\mathbb{R}^d$; spherical domains are embedded in $\mathbb{R}^{d+1}$.

Admissible ranges are specified separately by the task, model and oracle in this profile.

$\widehat{x}$: Final algorithm output **Domain:** $Q_c=[-R,R]^d$.

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

$Q_c,C_t$: Localization cube and comparison-reply signs **Domain:** $Q_c=[-R,R]^d,\ C_t\in\{-1,1\}$.

Distinguish the query domain from the localization region.

$\chi$: Comparison-model alias for the smoothness-to-strong-convexity ratio **Domain:** $\chi\ge1$.

$\chi=\beta/\mu=\kappa$

$M,H$: Number of grid points and depth of the comparison-elimination tree **Domain:** $M\in\mathbb{N},\ M\ge2,\ H\in\mathbb{N}$.

$M\le(2+2R\sqrt{\beta d/\varepsilon})^d$, $H=\lceil\log_2M\rceil$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=Q_c=[-R,R]^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$b_0$: Correctness-advantage scale in the comparison-information lower bound **Domain:** $b_0>0$.

$b_0=\nu$ when $a=0$; $b_0=c_0$ when $a>0$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One binary comparison reply

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Additional theorem window

**Region.** Fixed query cube; $d\ge8$, $0<\varepsilon\le c\mu R^2$ and $M\ge2$, with margin parameters as specified in the model.

**Quantity.** Q1

**Resource.** One binary comparison reply

**Status.** Other quantified gap

**Lower bound.** B2

$$
\Omega(d\nu^{-2}\log(\mu R^2/\varepsilon))\ (a=0);\quad\Omega(dc_0^{-2}\log(\mu R^2/\varepsilon))\ (a>0)
$$

**Upper bound.** B1

$$
CM\log(6M)[c_0^{-2}+\nu^{-2}(2H/\varepsilon)^{2a}]
$$

**Gap or comparison.** $O\!\left(\frac{M\log(6M)[c_0^{-2}+\nu^{-2}(2H/\varepsilon)^{2a}]}{d b_0^{-2}\log(\mu R^2/\varepsilon)}\right),\quad b_0=\nu\ (a=0),\ b_0=c_0\ (a>0)$

### R2 - Additional theorem window

**Region.** $a>0$, $d\ge16$, $\nu(2\mu dR^2)^a\le\min\{c_0,1/4\}$, $\varepsilon\le c^{\prime}\mu dR^2$.

**Quantity.** Q1

**Resource.** One binary comparison reply

**Status.** Upper bound missing

**Lower bound.** B3

$$
c\,d/[\nu^2(2\mu dR^2)^{2a}]
$$

**Upper bound.** No admitted bound for this comparison

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Each pairwise ordering response costs one call. Bounds transfer between value and comparison interfaces only through the stated direction of simulation.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

**Resource mapping.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

### B1 - Fixed feasible grid with repeated-comparison elimination

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
N\le C M\log(6M)[c_0^{-2}+\nu^{-2}(2H/\varepsilon)^{2a}],\quad M\le(2+2R\sqrt{\beta d/\varepsilon})^d,\ H=\lceil\log_2 M\rceil
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf)

**Conditions.** Use a grid with at least two points, $0<\varepsilon\le c\mu R^2$. When $a=0$, the bracketed expression may be set directly to $\nu^{-2}$. This is a verifiable upper bound on the same domain, without a claim that it is the strongest known; JNR12, Theorem 2 itself establishes only the full-space version.

**Local argument.** A1

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf) theorem: Oracle (1), PDF page 2; Theorems 1–2, page 3; Lemma 1 and lower proof, pages 5–6; Theorems 5–6 and robust line search, page 8

### B2 - Packing under ordering feedback and saturation tests on a fixed domain

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
a=0:\ \Omega\!\left(d\nu^{-2}\log(\mu R^2/\varepsilon)\right);\quad a>0:\ \Omega\!\left(dc_0^{-2}\log(\mu R^2/\varepsilon)\right)
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf)

**Conditions.** $d\ge8$ and $0<\varepsilon\le c\mu R^2$, with a fixed constant success probability. Restricting both queried points to the known cube preserves this information lower bound.

**Local argument.** A1

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf) theorem: Oracle (1), PDF page 2; Theorems 1–2, page 3; Lemma 1 and lower proof, pages 5–6; Theorems 5–6 and robust line search, page 8

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf) theorem: Oracle (1), PDF page 2; Theorems 1–2, page 3; Lemma 1 and lower proof, pages 5–6; Theorems 5–6 and robust line search, page 8

### B3 - Packing under ordering feedback and saturation tests on a fixed domain

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
N\ge c\,d/[\nu^2(2\mu dR^2)^{2a}]
$$

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf)

**Conditions.** $a>0,\ d\ge16,\ \nu(2\mu dR^2)^a\le\min(c_0,1/4),\ \varepsilon\le c'\mu dR^2$. Only the saturation lower bound on this fixed domain is asserted; it does not imply an $\varepsilon^{-2a}$ query lower bound at all accuracy levels.

**Local argument.** A1

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf) theorem: Oracle (1), PDF page 2; Theorems 1–2, page 3; Lemma 1 and lower proof, pages 5–6; Theorems 5–6 and robust line search, page 8

**Source location.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf) theorem: Oracle (1), PDF page 2; Theorems 1–2, page 3; Lemma 1 and lower proof, pages 5–6; Theorems 5–6 and robust line search, page 8

## 5. Local arguments

### A1 - Noisy comparisons on fixed and unrestricted query domains

**Scope.** Independent binary responses with the declared clipped comparison margin. The domain remains fixed when an accuracy parameter varies.

An entropy lower holds on either query domain. A grid tournament supplies a conservative fixed-cube upper. A separate saturation lower for positive margin exponent retains the cube radius explicitly.

For the entropy lower use $f_\theta(x)=\mu\|x-\theta\|^2/2$ and a packing of the public center cube $[-R,R]^d$ at separation greater than $2\sqrt{2\varepsilon/\mu}$. For $\varepsilon\le c\mu R^2$ and $d\ge8$, its logarithmic cardinality is at least $cd\log(\mu R^2/\varepsilon)$. Choose an admissible independent Bernoulli link attaining the declared clipped margin. For exponent $a=0$ all response probabilities lie in $[1/2-\nu,1/2+\nu]$; for $a>0$ they lie in $[1/2-c_0,1/2+c_0]$. If the corresponding half-width $b\le1/4$, each KL contribution is at most $Cb^2$, regardless of the query location. Chain rule and Fano give $T\ge cd b^{-2}\log(\mu R^2/\varepsilon)$. This also permits all-space queries.

For the fixed-cube upper, choose a Cartesian grid with coordinate spacing at most $\sqrt{\varepsilon/(\beta d)}$. Its nearest point to a global minimizer has squared distance at most $\varepsilon/(4\beta)$ and hence gap at most $\varepsilon/8$. Let its size be $M\le(2+2R\sqrt{\beta d/\varepsilon})^d$ and set $H=\lceil\log_2M\rceil$. Use a balanced knockout tournament. At each of at most $M-1$ matches, a fixed majority batch distinguishes all gaps at least $\varepsilon/(2H)$ with failure probability at most $\delta/(M-1)$. The batch is at most
$$C[c_0^{-2}+\nu^{-2}(2H/\varepsilon)^{2a}]\log(2M/\delta),$$
or $C\nu^{-2}\log(2M/\delta)$ for $a=0$. On the union good event, each mistaken match adds at most $\varepsilon/(2H)$ loss along the winning path; its depth is at most $H$, so the champion has gap below $\varepsilon$. This uses only legal cube points and a fixed worst-case budget, without knowing an exact link function.

For the fixed-cube saturation lower with $a>0$, take the source's sign centers $R\omega$ in the same cube. All within-function value gaps are at most $2\mu dR^2$. If $b=\nu(2\mu dR^2)^a\le\min\{c_0,1/4\}$, each binary response has KL at most $Cb^2$. A Varshamov--Gilbert center packing has logarithmic size $\Omega(d)$ and squared separation $\Omega(dR^2)$. Fano implies $T\ge cd/[\nu^2(2\mu dR^2)^{2a}]$ to reach error at most $c'\mu dR^2$. Holding $R$ fixed does not turn this formula into an $\varepsilon^{-2a}$ lower bound for every accuracy.

The native unrestricted-domain upper is imported directly from the source's robust line-search theorem after its notation change $\kappa_{\rm source}=a+1$, $\tau_{\rm source}=\mu$, $L_{\rm source}=\beta$, and margin coefficient $\mu_{\rm source}=\nu$. Its fixed nuisance parameters and hidden logarithms are retained. The positive-exponent native lower proof that shrinks its query cube with the horizon is not used as a verified fixed-domain lower.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf)

## References

[1] Jamieson, Nowak and Recht. Query Complexity of Derivative-Free Optimization. NeurIPS 2012.

https://papers.nips.cc/paper_files/paper/2012/file/e6d8545daa42d5ced125a4bf747b3688-Paper.pdf
