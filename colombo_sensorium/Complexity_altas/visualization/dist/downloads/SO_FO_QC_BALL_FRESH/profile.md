# Smooth quasar-convex minimization on a ball: fresh stochastic gradients

**Setting ID.** `SO_FO_QC_BALL_FRESH`

Single-objective optimization

Minimize expected objective gap over a public Euclidean ball with a fixed budget of unbiased, bounded-variance gradient calls.

**Status.** Logarithmic gap present; Other quantified gap present; Bounds missing

**Gap classes present.** Logarithmic gap; Other quantified gap

**TASK tags.** task family: Single objective; formulation: Global minimization

**MODEL tags.** geometry: Euclidean ball; smoothness: Population gradient lipschitz

**ORACLE tags.** operation: Stochastic gradient; feedback quality: Stochastic

**ALGORITHMS tags.** randomization: Private randomness allowed

**OUTPUT tags.** object: Primal point

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** mode: Expectation

**RESOURCE tags.** measure: N grad; budget: Fixed worst-case budget

## 1. Setting specification

### Task

Solve $\min_{x\in Q} f(x)$ using stochastic gradient responses queried inside $Q$. At a fixed query budget, minimize the worst-case expected objective gap of the returned feasible point.

### Admissible model

The public feasible set is the Euclidean ball $Q=B_2(0,D)=\{x\in\mathbb R^d:\|x\|_2\le D\}$. The unknown differentiable $f:\mathbb R^d\to\mathbb R$ has an $L$-Lipschitz gradient on the full space. At least one global minimizer is in $Q$, and the set $S=\arg\min_{x\in Q} f(x)$ is convex.

For all $x\in Q$, let $p_S(x)$ be the Euclidean projection onto the minimizer set. The model requires

$$\tau(f(x)-f_*)\le \langle\nabla f(x),x-p_S(x)\rangle.$$

The projection onto the hidden minimizer set defines quasar-convexity and is used in analysis. Only the projection onto the public ball is an available operation.

### Oracle interface

Each call at $x\in Q$ returns a single full stochastic gradient $g(x;\xi)\in\mathbb R^d$. Conditional on the query and past, $\mathbb E[g(x;\xi)]=\nabla f(x)$ and $\mathbb E\|g(x;\xi)-\nabla f(x)\|_2^2\le\sigma^2$.

The oracle law is fixed before interaction. Each call uses fresh independent randomness. There is no value feedback or sample handle. The learner can project onto $Q$ using its public center and radius.

### Output

Return a feasible point $\widehat x\in Q$. Any measurable feasible postprocessing is allowed, including an unqueried point, random iterate or convex combination. No function value or certificate is required.

### Loss or accuracy criterion

Evaluate the unnormalized loss $f(\widehat x)-f_*\,,\qquad f_*=\min_{x\in Q} f(x)$. It is finite and nonnegative. The minimizer promise means $f_*$ also equals the full-space minimum.

### Resource accounting

Every full response costs one call, including all responses to batch queries. The cap is $N\le T$ on every run. Internal computation, storage and projection onto $Q$ are free.

### Algorithm views and success guarantees

Private randomization and arbitrary measurable adaptive queries and postprocessing are allowed. The private seed is independent of the fixed instance and oracle samples.

Charge each stochastic gradient response. Public ball projection, internal arithmetic, and storage are free.

Choose one algorithm for the public parameters. For each fixed admissible objective and oracle law, take the expectation of the objective gap over the algorithm's private random seed and oracle noise. Then take the worst case over those instances.

The call cap $N\le T$ applies on every path, independent of the average error guarantee.

## 2. Notation and parameters

$d$: Dimension of the variable space. **Domain:** $d\in\mathbb N$, $d\ge1$.

$L$: Population-gradient Lipschitz constant in the Euclidean norm. **Domain:** $L>0$.

$D$: Radius of the public ball centered at the origin. **Domain:** $D>0$.

$\tau$: Quasar-convexity parameter on the feasible ball. **Domain:** $0<\tau\le1$.

$\sigma$: Upper bound on the standard deviation of a full stochastic gradient. **Domain:** $\sigma\ge0$.

$T$: Deterministic worst-case cap on the number of gradient responses. **Domain:** $T\in\mathbb N$, $T\ge1$.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax fixed budget error

$$
R_T^*=\inf_{A:N_A\le T\ \mathrm{on\ every\ path}}\ \sup_I\ \mathbb E_{A,\xi}[f(\widehat x)-f_*]
$$

**Definition.** Expected objective gap at budget T

**Optimization direction.** minimize

Take the expectation for each fixed instance, then the worst case over all admissible objectives and oracle laws.

### R1 - Noise-dominated high-dimensional window

**Region.** $\sigma>0$, $d\ge 3\log_{16/15}(2/\tau)$, and $T\ge 16\sigma^2/(\tau^2L^2D^2)$ and $\tau\sigma\sqrt{T}\ge LD$.

**Quantity.** Q1

**Resource.** Expected gap under a deterministic cap on fresh gradient responses.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega\!\left(\frac{D\sigma}{\tau\sqrt{T\ln(2/\tau)}}\right)
$$

**Upper bound.** B1

$$
O(D\sigma/(\tau\sqrt{T}))
$$

**Gap or comparison.** The ratio is at most $O(\sqrt{\ln(2/\tau)})$.

### R2 - Transient and noise in the high-dimensional window

**Region.** $\sigma>0$, $d\ge 3\log_{16/15}(2/\tau)$, and $T\ge 16\sigma^2/(\tau^2L^2D^2)$ and $\tau\sigma\sqrt{T}<LD$.

**Quantity.** Q1

**Resource.** Expected gap under a deterministic cap on fresh gradient responses.

**Status.** Other quantified gap

**Lower bound.** B4

$$
\Omega\!\left(\frac{D\sigma}{\tau\sqrt{T\ln(2/\tau)}}\right)
$$

**Upper bound.** B3

$$
O\!\left(\frac{LD^2}{\tau^2T}+\frac{D\sigma}{\tau\sqrt T}\right)
$$

**Gap or comparison.** The ratio is at most $O((1+LD/(\tau\sigma\sqrt{T}))\sqrt{\ln(2/\tau)})$.

### R3 - Outside the certified lower-bound window

**Region.** $\sigma=0$, $d<3\log_{16/15}(2/\tau)$, or $T<16\sigma^2/(\tau^2 L^2D^2)$.

**Quantity.** Q1

**Resource.** Expected gap under a deterministic cap on fresh gradient responses.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5

$$
O\!\left(\frac{LD^2}{\tau^2T}+\frac{D\sigma}{\tau\sqrt T}\right)
$$

**Gap or comparison.** The same projected SGD bound remains valid.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Full fresh gradient response with bounded variance.

**Guarantee mapping.** Expected function gap over both randomness sources.

**Output mapping.** One feasible point in the public ball.

**Resource mapping.** Deterministic cap of T gradient responses.

### B1 - Projected stochastic gradient and a uniform iterate

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O(D\sigma/(\tau\sqrt{T}))
$$

**Sources.** [1](https://proceedings.mlr.press/v291/saad25a.html)

**Conditions.** $\sigma>0$, $d\ge 3\log_{16/15}(2/\tau)$, and $T\ge 16\sigma^2/(\tau^2L^2D^2)$ and $\tau\sigma\sqrt{T}\ge LD$.

**Derivation.** Let $x_0=0$ and $x_{t+1}=P_Q(x_t-\eta g_t)$ with $\eta=\min\{\tau/(2L),D/(\sigma\sqrt{T})\}$, using $+\infty$ for the second term at $\sigma=0$. For $p_t=P_S(x_t)$, projection nonexpansiveness and quasar-convexity give $\mathbb E_t\operatorname{dist}(x_{t+1},S)^2\le\operatorname{dist}(x_t,S)^2-2\eta\tau(f(x_t)-f_*)+\eta^2\mathbb E_t\|g_t\|^2$. Global smoothness and the global minimum promise give $\|\nabla f(x_t)\|^2\le2L(f(x_t)-f_*)$, so the coefficient of the gap after absorbing the second moment is at most $-\eta\tau$. Sum over $t=0,\dots,T-1$, use $\operatorname{dist}(0,S)\le D$, and return a uniform sampled iterate. The gap is at most $D^2/(\eta\tau T)+\eta\sigma^2/\tau$.

**Source location.** [1](https://proceedings.mlr.press/v291/saad25a.html) theorem: Section 1 and Table 1, with the projected SGD derivation in this profile; pdf pages: 2; 6

Let $x_0=0$ and $x_{t+1}=P_Q(x_t-\eta g_t)$ with $\eta=\min\{\tau/(2L),D/(\sigma\sqrt{T})\}$, using $+\infty$ for the second term at $\sigma=0$. For $p_t=P_S(x_t)$, projection nonexpansiveness and quasar-convexity give $\mathbb E_t\operatorname{dist}(x_{t+1},S)^2\le\operatorname{dist}(x_t,S)^2-2\eta\tau(f(x_t)-f_*)+\eta^2\mathbb E_t\|g_t\|^2$. Global smoothness and the global minimum promise give $\|\nabla f(x_t)\|^2\le2L(f(x_t)-f_*)$, so the coefficient of the gap after absorbing the second moment is at most $-\eta\tau$. Sum over $t=0,\dots,T-1$, use $\operatorname{dist}(0,S)\le D$, and return a uniform sampled iterate. The gap is at most $D^2/(\eta\tau T)+\eta\sigma^2/\tau$.

### B2 - Packed radial objectives and KL divergence decomposition

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** arbitrary_randomized

$$
\Omega\!\left(\frac{D\sigma}{\tau\sqrt{T\ln(2/\tau)}}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v291/saad25a.html)

**Conditions.** $\sigma>0$, $d\ge 3\log_{16/15}(2/\tau)$, and $T\ge 16\sigma^2/(\tau^2L^2D^2)$ and $\tau\sigma\sqrt{T}\ge LD$.

**Derivation.** Use Appendix D's packing with $d_0=\lceil2\log_{16/15}(2/\tau)\rceil$, $m\ge2/\tau^2$, and the radial objectives with centers of norm at most $2D/3$. Their gradients are globally $L$-Lipschitz: the radial derivative has slope of magnitude at most $L$ and its tangential Lipschitz factor is at most $L$. The affine ambient minimizer set intersects $Q$ in a convex set. The QC inner product only uses the first $d_0$ coordinates and is unchanged by projecting onto this intersection. Set the construction's width to $\Delta=\sigma/(4L\tau\sqrt{d_0 T})$. The displayed budget guard ensures $\Delta<D/16$. Equation (19) bounds the mean KL divergence by $3/64$. Pinsker's inequality and the disjoint packing therefore give a universal positive average misidentification probability. Equation (17) then yields $\Omega(LD\Delta)$, the displayed lower bound. The guard is deliberately narrower than the theorem statement to make the width condition explicit.

**Source location.** [1](https://proceedings.mlr.press/v291/saad25a.html) theorem: Theorem 9 and Appendix D, Equations (17)–(19); pdf pages: 7; 33; 34; 35; 36; 37; 38

Use Appendix D's packing with $d_0=\lceil2\log_{16/15}(2/\tau)\rceil$, $m\ge2/\tau^2$, and the radial objectives with centers of norm at most $2D/3$. Their gradients are globally $L$-Lipschitz: the radial derivative has slope of magnitude at most $L$ and its tangential Lipschitz factor is at most $L$. The affine ambient minimizer set intersects $Q$ in a convex set. The QC inner product only uses the first $d_0$ coordinates and is unchanged by projecting onto this intersection. Set the construction's width to $\Delta=\sigma/(4L\tau\sqrt{d_0 T})$. The displayed budget guard ensures $\Delta<D/16$. Equation (19) bounds the mean KL divergence by $3/64$. Pinsker's inequality and the disjoint packing therefore give a universal positive average misidentification probability. Equation (17) then yields $\Omega(LD\Delta)$, the displayed lower bound. The guard is deliberately narrower than the theorem statement to make the width condition explicit.

### B3 - Projected stochastic gradient and a uniform iterate

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{LD^2}{\tau^2T}+\frac{D\sigma}{\tau\sqrt T}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v291/saad25a.html)

**Conditions.** $\sigma>0$, $d\ge 3\log_{16/15}(2/\tau)$, and $T\ge 16\sigma^2/(\tau^2L^2D^2)$ and $\tau\sigma\sqrt{T}<LD$.

**Derivation.** Let $x_0=0$ and $x_{t+1}=P_Q(x_t-\eta g_t)$ with $\eta=\min\{\tau/(2L),D/(\sigma\sqrt{T})\}$, using $+\infty$ for the second term at $\sigma=0$. For $p_t=P_S(x_t)$, projection nonexpansiveness and quasar-convexity give $\mathbb E_t\operatorname{dist}(x_{t+1},S)^2\le\operatorname{dist}(x_t,S)^2-2\eta\tau(f(x_t)-f_*)+\eta^2\mathbb E_t\|g_t\|^2$. Global smoothness and the global minimum promise give $\|\nabla f(x_t)\|^2\le2L(f(x_t)-f_*)$, so the coefficient of the gap after absorbing the second moment is at most $-\eta\tau$. Sum over $t=0,\dots,T-1$, use $\operatorname{dist}(0,S)\le D$, and return a uniform sampled iterate. The gap is at most $D^2/(\eta\tau T)+\eta\sigma^2/\tau$.

**Source location.** [1](https://proceedings.mlr.press/v291/saad25a.html) theorem: Section 1 and Table 1, with the projected SGD derivation in this profile; pdf pages: 2; 6

Let $x_0=0$ and $x_{t+1}=P_Q(x_t-\eta g_t)$ with $\eta=\min\{\tau/(2L),D/(\sigma\sqrt{T})\}$, using $+\infty$ for the second term at $\sigma=0$. For $p_t=P_S(x_t)$, projection nonexpansiveness and quasar-convexity give $\mathbb E_t\operatorname{dist}(x_{t+1},S)^2\le\operatorname{dist}(x_t,S)^2-2\eta\tau(f(x_t)-f_*)+\eta^2\mathbb E_t\|g_t\|^2$. Global smoothness and the global minimum promise give $\|\nabla f(x_t)\|^2\le2L(f(x_t)-f_*)$, so the coefficient of the gap after absorbing the second moment is at most $-\eta\tau$. Sum over $t=0,\dots,T-1$, use $\operatorname{dist}(0,S)\le D$, and return a uniform sampled iterate. The gap is at most $D^2/(\eta\tau T)+\eta\sigma^2/\tau$.

### B4 - Packed radial objectives and KL divergence decomposition

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** arbitrary_randomized

$$
\Omega\!\left(\frac{D\sigma}{\tau\sqrt{T\ln(2/\tau)}}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v291/saad25a.html)

**Conditions.** $\sigma>0$, $d\ge 3\log_{16/15}(2/\tau)$, and $T\ge 16\sigma^2/(\tau^2L^2D^2)$ and $\tau\sigma\sqrt{T}<LD$.

**Derivation.** Use Appendix D's packing with $d_0=\lceil2\log_{16/15}(2/\tau)\rceil$, $m\ge2/\tau^2$, and the radial objectives with centers of norm at most $2D/3$. Their gradients are globally $L$-Lipschitz: the radial derivative has slope of magnitude at most $L$ and its tangential Lipschitz factor is at most $L$. The affine ambient minimizer set intersects $Q$ in a convex set. The QC inner product only uses the first $d_0$ coordinates and is unchanged by projecting onto this intersection. Set the construction's width to $\Delta=\sigma/(4L\tau\sqrt{d_0 T})$. The displayed budget guard ensures $\Delta<D/16$. Equation (19) bounds the mean KL divergence by $3/64$. Pinsker's inequality and the disjoint packing therefore give a universal positive average misidentification probability. Equation (17) then yields $\Omega(LD\Delta)$, the displayed lower bound. The guard is deliberately narrower than the theorem statement to make the width condition explicit.

**Source location.** [1](https://proceedings.mlr.press/v291/saad25a.html) theorem: Theorem 9 and Appendix D, Equations (17)–(19); pdf pages: 7; 33; 34; 35; 36; 37; 38

Use Appendix D's packing with $d_0=\lceil2\log_{16/15}(2/\tau)\rceil$, $m\ge2/\tau^2$, and the radial objectives with centers of norm at most $2D/3$. Their gradients are globally $L$-Lipschitz: the radial derivative has slope of magnitude at most $L$ and its tangential Lipschitz factor is at most $L$. The affine ambient minimizer set intersects $Q$ in a convex set. The QC inner product only uses the first $d_0$ coordinates and is unchanged by projecting onto this intersection. Set the construction's width to $\Delta=\sigma/(4L\tau\sqrt{d_0 T})$. The displayed budget guard ensures $\Delta<D/16$. Equation (19) bounds the mean KL divergence by $3/64$. Pinsker's inequality and the disjoint packing therefore give a universal positive average misidentification probability. Equation (17) then yields $\Omega(LD\Delta)$, the displayed lower bound. The guard is deliberately narrower than the theorem statement to make the width condition explicit.

### B5 - Projected stochastic gradient and a uniform iterate

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\frac{LD^2}{\tau^2T}+\frac{D\sigma}{\tau\sqrt T}\right)
$$

**Sources.** [1](https://proceedings.mlr.press/v291/saad25a.html)

**Conditions.** $\sigma=0$, $d<3\log_{16/15}(2/\tau)$, or $T<16\sigma^2/(\tau^2 L^2D^2)$.

**Derivation.** Let $x_0=0$ and $x_{t+1}=P_Q(x_t-\eta g_t)$ with $\eta=\min\{\tau/(2L),D/(\sigma\sqrt{T})\}$, using $+\infty$ for the second term at $\sigma=0$. For $p_t=P_S(x_t)$, projection nonexpansiveness and quasar-convexity give $\mathbb E_t\operatorname{dist}(x_{t+1},S)^2\le\operatorname{dist}(x_t,S)^2-2\eta\tau(f(x_t)-f_*)+\eta^2\mathbb E_t\|g_t\|^2$. Global smoothness and the global minimum promise give $\|\nabla f(x_t)\|^2\le2L(f(x_t)-f_*)$, so the coefficient of the gap after absorbing the second moment is at most $-\eta\tau$. Sum over $t=0,\dots,T-1$, use $\operatorname{dist}(0,S)\le D$, and return a uniform sampled iterate. The gap is at most $D^2/(\eta\tau T)+\eta\sigma^2/\tau$.

**Source location.** [1](https://proceedings.mlr.press/v291/saad25a.html) theorem: Section 1 and Table 1, with the projected SGD derivation in this profile; pdf pages: 2; 6

Let $x_0=0$ and $x_{t+1}=P_Q(x_t-\eta g_t)$ with $\eta=\min\{\tau/(2L),D/(\sigma\sqrt{T})\}$, using $+\infty$ for the second term at $\sigma=0$. For $p_t=P_S(x_t)$, projection nonexpansiveness and quasar-convexity give $\mathbb E_t\operatorname{dist}(x_{t+1},S)^2\le\operatorname{dist}(x_t,S)^2-2\eta\tau(f(x_t)-f_*)+\eta^2\mathbb E_t\|g_t\|^2$. Global smoothness and the global minimum promise give $\|\nabla f(x_t)\|^2\le2L(f(x_t)-f_*)$, so the coefficient of the gap after absorbing the second moment is at most $-\eta\tau$. Sum over $t=0,\dots,T-1$, use $\operatorname{dist}(0,S)\le D$, and return a uniform sampled iterate. The gap is at most $D^2/(\eta\tau T)+\eta\sigma^2/\tau$.

## References

[1] El Mehdi Saad, Wei-Cheng Lee and Francesco Orabona. New Lower Bounds for Stochastic Non-Convex Optimization through Divergence Decomposition. 2025. COLT 2025, PMLR 291, arXiv:2502.14060v2.

https://proceedings.mlr.press/v291/saad25a.html
