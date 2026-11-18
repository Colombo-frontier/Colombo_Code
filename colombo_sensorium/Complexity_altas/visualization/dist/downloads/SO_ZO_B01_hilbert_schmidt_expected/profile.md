# Higher-order smooth strongly convex optimization in the Hilbert–Schmidt norm with mixed value error

**Setting ID.** `SO_ZO_B01_hilbert_schmidt_expected`

Single-objective optimization

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

**Status.** Logarithmic gap present

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Higher order holder; smoothness: Lipschitz gradient

**ORACLE tags.** access order: Zeroth-order interface; interface family: Biased adversarial noisy value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Fixed worst-case budget

## 1. Setting specification

### Task

Minimize $f$ globally over $\mathbb{R}^d$ and return a point with small objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is twice differentiable, with $\mu I_d\preceq\nabla^2f(x)\preceq\beta I_d$, where $0<\mu<\beta$. Its unique minimizer lies in $B_2(0,R)$.

$\alpha>2$. Set $m=\lceil\alpha\rceil-1$ and $\gamma_\alpha=\alpha-m\in(0,1]$. The $m$th derivative of $f$ satisfies $\|D^mf(x)-D^mf(y)\|_{\mathrm{HS}}\le H_\alpha\|x-y\|_2^{\gamma_\alpha}$ for every $x,y$ in the ambient space.

Derivative tensors use the Hilbert–Schmidt norm, the square root of the sum of squared tensor coordinates in an orthonormal basis.

### Oracle interface

At any finite $x_t\in\mathbb{R}^d$, the oracle returns $Y_t=f(x_t)+b(x_t)+\xi_t+e_t$. The fixed unknown function $b$ satisfies $|b(x)-b(y)|\le L_b\|x-y\|_2$.

$\xi_t$ is fresh independent centered noise with $\mathbb{E}\xi_t^2\le\sigma_v^2$. The error $e_t$ satisfies $|e_t|\le\eta_v$ and may depend on the current query and preceding interaction. The guarantee must hold for every admissible bias function and error strategy.

The public inputs are $d$, $\beta$, $\mu$, $R$, $\alpha$, $H_\alpha$, $\tau$, $L_b$, $\eta_v$, $\sigma_v$, $\varepsilon$, $T$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

Each scalar function value or noisy observation costs $1$ call. Every location in a multipoint finite difference, every initialization query, and every reference observation is charged.

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

$R$: Localization radius for a global minimizer **Domain:** $R>0$.

$x_*\in B_2(0,R)$

$\alpha$: Higher-order smoothness order **Domain:** $\alpha>2$.

Use $m=\lceil\alpha\rceil-1$ and $\gamma_\alpha=\alpha-m$ for the integer derivative order and its Hölder exponent.

$H_\alpha$: Hölder modulus of the highest derivative in the specified tensor norm **Domain:** $H_\alpha>0$.

$\tau$: Dimension-correction exponent for Hilbert-Schmidt regularity **Domain:** $\tau\ge0$.

$\tau=(\alpha-1)/2$ when $m$ is even; $\tau=(m-1)/2$ when $m$ is odd.

$L_b$: Lipschitz bound on the fixed systematic bias function **Domain:** $L_b\ge0$.

$|b(x)-b(y)|\le L_b\|x-y\|_2$

$\eta_v$: Budget for query-adaptive bounded scalar error **Domain:** $\eta_v\ge0$.

$|e_t|\le\eta_v$

$\sigma_v$: Upper bound on scalar observation-noise scale **Domain:** $\sigma_v\ge0$.

$\mathbb{E}\xi^2\le\sigma_v^2$; conditional-variance assumptions are interpreted with respect to the specified interaction history.

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$T$: Known query budget or argument of the risk curve **Domain:** $T\in\mathbb{N}_0$.

Use $N\le T$ in the fixed-budget specification and $\mathbb{E}[N]\le T$ in the expected-budget specification.

$m$: Integer order of the highest Hölder-continuous derivative **Domain:** $m\in\mathbb{N},\ m\ge2$.

$m=\lceil\alpha\rceil-1$

$\gamma_\alpha$: Hölder exponent of the highest derivative **Domain:** $0<\gamma_\alpha\le1$.

$\gamma_\alpha=\alpha-m$

$s$: Dimension exponent in the high-order statistical complexity **Domain:** $s>0$.

$s=2-\tau/(\alpha-1)$

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

$r_c$: Available curvature slack in the hard-function construction **Domain:** $r_c>0$.

$r_c=\min\{\mu,(\beta-\mu)/2\}$

$h_\varepsilon$: Smoothing scale associated with the target accuracy **Domain:** $h_\varepsilon>0$.

$h_\varepsilon=(\mu\varepsilon d^\tau/H_\alpha^2)^{1/[2(\alpha-1)]}$; also denoted by $h_*$ in the complexity bounds.

$\eta_*$: Tolerable scale of adversarial scalar error **Domain:** $\eta_*>0$.

$\eta_*=\sqrt{\mu\varepsilon}\,h_\varepsilon/\sqrt d$

$T_*$: Call scale of the leading high-order statistical term **Domain:** $T_*\ge0$.

$T_*=d^s\sigma_v^2H_\alpha^{2/(\alpha-1)}(\mu\varepsilon)^{-\alpha/(\alpha-1)}$

$\Phi_0$: Error scale before saturation of the high-order statistical lower bound **Domain:** $\Phi_0>0$.

$\Phi_0=\min\{\mu R^2,r_c^{2(\alpha-1)/(\alpha-2)}\mu^{-1}H_\alpha^{-2/(\alpha-2)}\}$

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

$Y_t,\xi_t,t$: Scalar-observation number, noise, and call index **Domain:** $Y_t,\xi_t\in\mathbb{R},\ t\in\mathbb{N}$.

Noise independence, distribution class and scale are fixed by this profile's oracle.

$\mathcal{F}_{t-1}$: The history before the current query **Domain:** The $\sigma$-algebra generated by the algorithm's seed and previous feedback.

The current query may depend on this history.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$m,\gamma_\alpha$: Integer derivative order and Hölder exponent of the high-order regularity condition **Domain:** $m\ge2,\ 0<\gamma_\alpha\le1$.

$m=\lceil\alpha\rceil-1$, $\gamma_\alpha=\alpha-m$

$\|T\|_{\mathrm{HS}}$: Hilbert-Schmidt tensor norm **Domain:** Defined through tensor coordinates in a Euclidean orthonormal basis.

$\|T\|_{\mathrm{HS}}=(\sum_{i_1,\ldots,i_m}|T[e_{i_1},\ldots,e_{i_m}]|^2)^{1/2}$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$I_d,\preceq$: Identity matrix and positive-semidefinite order **Domain:** $I_d\in\mathbb{R}^{d\times d}$; the order applies to real symmetric matrices of the same size.

$A\preceq B$ means that $v^\top(B-A)v\ge0$ for every $v\in\mathbb{R}^d$.

$b,e_t$: Fixed systematic bias function and query-adaptive scalar errors **Domain:** $b:\mathbb{R}^d\to\mathbb{R},\ e_t\in\mathbb{R}$.

$\operatorname{Lip}(b)\le L_b$, $|e_t|\le\eta_v$.

$h_*$: Smoothing-scale alias in the bias-tolerance bound **Domain:** $h_*>0$.

$h_*=h_\varepsilon$

$\varepsilon_0$: Accuracy threshold in the lower bound for bounded adversarial error **Domain:** $\varepsilon_0>0$.

$\varepsilon_0=\min\{\mu R^2/32,\mu^{-1}(r_c r_\alpha/(\sqrt{32}K_*))^{2(\alpha-1)/(\alpha-2)}d^{\nu_*/(\alpha-2)}H_\alpha^{-2/(\alpha-2)}\}$

$r_\alpha,K_*,\nu_*,\ell_*$: Constants and dimension exponents in the high-order local-perturbation construction **Domain:** $r_\alpha,K_*,\ell_*>0,\ \nu_*\ge0$.

For the operator norm or an odd-order Hilbert–Schmidt norm: $r_\alpha=(\sqrt{32}K_\alpha)^{1/(\alpha-1)}$, $K_*=\max\{1,K_2\}$, $\nu_*=\tau$, and $\ell_*=1$. For an even-order Hilbert–Schmidt norm, replace the corresponding constants by $\widetilde{K}_\alpha,\widetilde{K}_2$, with $\nu_*=0$ and $\ell_*=L_\vartheta$.

$K_\alpha,K_2,\widetilde{K}_\alpha,\widetilde{K}_2,L_\vartheta$: Fixed positive constant in the smooth cutoff construction **Domain:** Depends only on the fixed $\alpha$.

Fixed by the cutoff-function construction in the high-order smoothness source; not an instance input.

$C_{\mathrm{hid}}$: Hidden construction coefficient in the adversarial-error lower bound **Domain:** $C_{\mathrm{hid}}>0$.

$C_{\mathrm{hid}}=2\sqrt{32}\,\ell_*r_\alpha$

$(L_b)_{\max}$: Maximum tolerable systematic-bias magnitude at a fixed budget and accuracy **Domain:** Takes values in $[0,+\infty]$; all remaining model bounds and $T,\varepsilon$ are fixed.

Set the adversarial value-error amplitude to zero. Take the supremum of systematic-bias Lipschitz bounds for which one algorithm meets the error and cost guarantees uniformly over all admissible objectives, fixed bias functions and noise laws.

$(\eta_v)_{\max}$: Maximum tolerable adversarial value-error amplitude at a fixed budget and accuracy **Domain:** Takes values in $[0,+\infty]$; all remaining model bounds and $T,\varepsilon$ are fixed.

Set the systematic-bias Lipschitz bound to zero. Take the supremum of adversarial error amplitudes for which one algorithm meets the error and cost guarantees uniformly over all admissible objectives, error strategies and noise laws.

## 3. Complexity bracket

### Compared quantities

#### Q1 - maximum admissible noise

$$
\eta^\star_v(B,\varepsilon;\theta)=\sup\{\eta\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi\le B,\ G_v(\mathcal A,I;\varepsilon)\ \forall I\in\mathcal I(\eta;\theta)\}
$$

**Definition.** Maximum tolerable Lipschitz amplitude of systematic bias; larger values are better

**Scope.** declared_joint_parameter_window

**Optimization direction.** maximize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit. The amplitude eta denotes the specific noise or bias parameter named by this quantity; the other error components are held as stated in its regime.

#### Q2 - maximum admissible noise

$$
\eta^\star_v(B,\varepsilon;\theta)=\sup\{\eta\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi\le B,\ G_v(\mathcal A,I;\varepsilon)\ \forall I\in\mathcal I(\eta;\theta)\}
$$

**Definition.** Maximum tolerable amplitude of adversarial value error; larger values are better

**Scope.** declared_joint_parameter_window

**Optimization direction.** maximize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit. The amplitude eta denotes the specific noise or bias parameter named by this quantity; the other error components are held as stated in its regime.

#### Q3 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** One scalar function value or observation

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime B01.R1

**Region.** Hilbert-Schmidt model, $m=\lceil\alpha\rceil-1$; $\tau=(\alpha-1)/2$ for even $m$ and $\tau=(m-1)/2$ for odd $m$. Fix $\alpha>2$, $0<\mu<\beta$ and $H_\alpha,R,\sigma_v>0$. Require $\eta_v=0$, $0<\varepsilon<\mu R^2/2$ and $T\ge C_\alpha[T_*(\varepsilon)+d\sqrt\kappa(1+\log(\beta R^2/\varepsilon))]$; $C_\alpha$ is the fixed constant in the source upper bound.

**Quantity.** Q1

**Resource.** Maximum tolerable Lipschitz amplitude of systematic bias; larger values are better

**Status.** Optimal

**Lower bound.** B1

$$
(L_b)_{\max}\ge c_\alpha\sqrt{\mu\varepsilon}
$$

**Upper bound.** B2

$$
(L_b)_{\max}\le\sqrt{2\mu\varepsilon}
$$

**Gap or comparison.** $O_\alpha (1)$

### R2 - Parameter regime B01.R2

**Region.** Hilbert-Schmidt model, $m=\lceil\alpha\rceil-1$; $\tau=(\alpha-1)/2$ for even $m$ and $\tau=(m-1)/2$ for odd $m$. Fix $\alpha>2$, $0<\mu<\beta$ and $H_\alpha,R,\sigma_v>0$. Require $L_b=0$, $0<\varepsilon\le\varepsilon_0$ and $T\ge C_\alpha[T_*(\varepsilon)+d\sqrt\kappa(1+\log(\beta R^2/\varepsilon))]$. Compute $\varepsilon_0$ from the complete formula in this profile; $C_\alpha$ is the fixed constant in the source upper bound.

**Quantity.** Q2

**Resource.** Maximum tolerable amplitude of adversarial value error; larger values are better

**Status.** Logarithmic gap

**Lower bound.** B1

$$
(\eta_v)_{\max}\ge c_\alpha\eta_*
$$

**Upper bound.** B2

$$
(\eta_v)_{\max}\le C_{\rm hid}\min\{\sqrt d,\sqrt{\log(4T)}\}\eta_*
$$

**Gap or comparison.** $O_\alpha(\min\{\sqrt d,\sqrt{\log(4T)}\})$

### R3 - Parameter regime B01.R3

**Region.** Hilbert-Schmidt model, $m=\lceil\alpha\rceil-1$; $\tau=(\alpha-1)/2$ for even $m$ and $\tau=(m-1)/2$ for odd $m$. Fix $\alpha>2$, $0<\mu<\beta$ and $H_\alpha,R,\sigma_v>0$. Require $0<\varepsilon\le c_\alpha\Phi_0/2$, $L_b\le\min\{\mu R,c_\alpha^{\prime}\sqrt{\mu\varepsilon}\}$, $\eta_v\le c_\alpha^{\prime}\eta_*$ and $d\sqrt\kappa[1+\log(\beta R^2/\varepsilon)]\le T_*(\varepsilon)$. The fixed constants satisfy $0<c_\alpha\le1$ and $c_\alpha^{\prime}>0$.

**Quantity.** Q3

**Resource.** One scalar function value or observation

**Status.** Optimal

**Lower bound.** B4

$$
\Omega_\alpha (T_*(\varepsilon ))
$$

**Upper bound.** B3

$$
O_\alpha (T_*(\varepsilon ))
$$

**Gap or comparison.** $O_\alpha (1)$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Scalar observations follow the independent-noise, conditional-noise, or mixed-error law specified here; every repeated observation is charged separately.

**Guarantee mapping.** Error uses this profile's accuracy scale and aggregation order. The source theorem's expectation, probability, and asymptotic quantifiers are retained separately.

**Output mapping.** The output need only lie in this setting's prescribed space. Permitted averages and unqueried outputs must still satisfy its feasibility conditions.

### B1 - High-order finite differences with accelerated restarts

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** Algorithmic witness: Randomized witness

$$
L_b\le c\sqrt{\mu\varepsilon},\qquad \eta_v\le c\eta_*
$$

**Meaning of the inequality.** A lower bound on the maximal tolerable amplitude is certified by one algorithm through a sufficient guarantee. It is not a complexity lower bound against all algorithms.

**Max admissible systematic lipschitz bias.**

$$
(L_b)_{\max}\ge c_\alpha\sqrt{\mu\varepsilon}
$$

**Max admissible adversarial value bias.**

$$
(\eta_v)_{\max}\ge c_\alpha\eta_*
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** Fix $\alpha>2$ and the stated tensor norm, with $0<\mu<\beta$ and $R,H_\alpha,\sigma_v>0$. The smoothing scale is $h_\varepsilon=(\mu\varepsilon d^\tau/H_\alpha^2)^{1/[2(\alpha-1)]}$ and the tolerance scale is $\eta_*=\sqrt{\mu\varepsilon}h_\varepsilon/\sqrt d$. The sufficient budget retains both $T_*(\varepsilon)$ and $d\sqrt\kappa[1+\log(\beta R^2/\varepsilon)]$.

**Resource conversion.** This quantity is a tolerable error amplitude, stated as a sufficient or necessary condition. It cannot be divided by an oracle-complexity bound to form a gap ratio.

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Theorem 1(c); pdf pages: 3

### B2 - Indistinguishability under bias and a statistical hard subclass

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** All algorithm necessity: All randomized adaptive algorithms

$$
(L_b)_{\max}\le C\sqrt{\mu\varepsilon},\quad (\eta_v)_{\max}\le C\min\{\sqrt d,\sqrt{\log(4T)}\}\eta_*
$$

**Meaning of the inequality.** An upper bound on the maximal tolerable amplitude is a necessary restriction that applies to all allowed algorithms. It is not an upper bound on the running cost of one algorithm.

**Max admissible systematic lipschitz bias.**

$$
(L_b)_{\max}\le\sqrt{2\mu\varepsilon}
$$

**Max admissible adversarial value bias.**

$$
(\eta_v)_{\max}\le C_{\mathrm{hid}}\min\{\sqrt d,\sqrt{\log(4T)}\}\eta_*
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** Fix $\alpha>2$ and this specification's tensor norm, with $0<\mu<\beta$ and $R,H_\alpha,\sigma_v>0$. The systematic-bias branch uses $\eta_v=0$ and $0<\varepsilon<\mu R^2/2$; the adversarial-value-error branch uses $L_b=0$ and $0<\varepsilon\le\varepsilon_0$, where $\varepsilon_0$ is defined by the complete formula in the symbol table. The two results separately limit the maximal tolerable amplitudes.

**Resource conversion.** This quantity is a tolerable error amplitude, stated as a sufficient or necessary condition. It cannot be divided by an oracle-complexity bound to form a gap ratio.

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Theorem 1(c); Theorem H.1; pdf pages: 3

### B3 - High-order finite differences with accelerated restarts

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
O_\alpha(T_*(\varepsilon)+d\sqrt\kappa(1+\log(\beta R^2/\varepsilon)))
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** Fix $\alpha>2$ and the stated tensor norm, with $0<\mu<\beta$, $\sigma_v>0$ and $0<\varepsilon<\beta R^2$. Bias satisfies $L_b\le c_\alpha\sqrt{\mu\varepsilon}$ and $\eta_v\le c_\alpha\eta_*$; $\tau$ has the definition specified by this model.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Theorem1(c); pdf pages: 4

### B4 - Indistinguishability under bias and a statistical hard subclass

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_\alpha(T_*(\varepsilon))
$$

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

**Conditions.** Fix $\alpha>2$, with $0<\mu<\beta$, $\sigma_v>0$ and $0<\varepsilon\le c_\alpha\Phi_0/2$. The allowed bias bound $L_b,\eta_v\ge0$ is arbitrary; the hard subclass may have zero bias.

**Resource conversion.** Atomic calls under a fixed cap on every execution path. All feedback obtained during initialization, differencing and inner iterations is charged.

**Local argument.** A1

**Source location.** [1](https://arxiv.org/pdf/2610.05517v2) theorem: Inversion of the risk lower bound in Theorem 1(b); pdf pages: 4

## 5. Local arguments

### A1 - Inverting a capped statistical risk lower bound

**Scope.** The stated higher-smoothness norm, curvature slack, noise class, and small-error threshold of the source theorem are retained.

If the source risk lower is $c_\alpha\min\{\Phi_T,\Phi_0\}$, then $0<\varepsilon\le c_\alpha\Phi_0/2$ forces $\Phi_T\le\varepsilon/c_\alpha$, giving the registered $\Omega_\alpha(T_*(\varepsilon))$ call lower.

A worst-case expected-error guarantee cannot hold if the source lower exceeds its target. On the stated window the capped term $c_\alpha\Phi_0$ is larger than $\varepsilon$, so necessarily the decaying branch satisfies $c_\alpha\Phi_T\le\varepsilon$. Invert that branch algebraically; its fixed-order multiplicative factors become constants depending on $\alpha$. If the target oracle permits additional bias or adversarial error, choose the legal zero-bias subclass. This containment transfers the statistical lower without requiring the bias budgets to vanish in the whole model. Operator-norm and Hilbert--Schmidt derivative budgets define different classes, so each uses its own source $\Phi_T$, $\Phi_0$, and exponent.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://arxiv.org/pdf/2610.05517v2)

## References

[1] Loginov, Dvinskikh, Tupitsa, Osmanov, Dorn and Gasnikov. Minimax Oracle Call Complexity, Rounds and Admissible Noise in Zeroth-Order Optimization of Highly Smooth Functions. arXiv:2610.05517v2, 2026-10-14.

https://arxiv.org/pdf/2610.05517v2
