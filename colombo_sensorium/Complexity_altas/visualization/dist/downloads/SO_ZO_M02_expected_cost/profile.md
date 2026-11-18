# Smooth strongly convex stochastic objectives with two values per Markov state and samplewise smoothness

**Setting ID.** `SO_ZO_M02_expected_cost`

Single-objective optimization

Minimize the stationary expectation objective $f(x)=\mathbb{E}_{Z\sim\pi}F(x;Z)$, using function-value interactions under dependent states to return a point with small expected objective gap.

**Status.** Bounds missing

**TASK tags.** formulation: Global minimization; solution concept: Global minimization; task family: Single objective

**MODEL tags.** convexity: Strongly convex; smoothness: Mean gradient lipschitz; smoothness: Sample gradient lipschitz; stochastic model: Uniform sample gradient deviation

**ORACLE tags.** access order: Zeroth-order interface; interface family: Markov same state paired value; public information: Public inputs explicitly declared; query domain: Full space

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Objective gap

**GUARANTEE tags.** aggregation: Per instance; mode: Expectation

**RESOURCE tags.** budget: Worst-instance expected cost

## 1. Setting specification

### Task

Minimize the stationary expectation objective $f(x)=\mathbb{E}_{Z\sim\pi}F(x;Z)$, using function-value interactions under dependent states to return a point with small expected objective gap.

### Admissible model

$f:\mathbb{R}^d\to\mathbb{R}$ is differentiable and satisfies $\|\nabla f(x)-\nabla f(y)\|_2\le\beta\|x-y\|_2$ for every $x,y\in\mathbb{R}^d$.

Strong convexity is defined in the Euclidean norm: $f((1-t)x+ty)\le(1-t)f(x)+tf(y)-\frac{\mu}{2}t(1-t)\|x-y\|_2^2$ for $x,y$ and $t\in[0,1]$ in the domain.

$f(x)=\mathbb{E}_{Z\sim\pi}F(x;Z)$, where $\pi$ is the stationary distribution of the hidden Markov chain. The known initial point $x^0,x_f^0$ and bound $r_0$ satisfy $\mu^{-1}(f(x_f^0)-f_*)+\|x^0-x_*\|_2^2\le r_0$.

Each sample function $F(\cdot;z)$ is globally $\beta$-smooth, with $\mathbb{E}_\pi\nabla F(x;Z)=\nabla f(x)$ and, for every $x,z$, $\|\nabla F(x;z)-\nabla f(x)\|_2\le\sigma_g$. Sample convexity is not required.

### Oracle interface

A hidden homogeneous Markov chain is initialized from its stationary distribution $\pi$; its transition kernel $P$ satisfies $\sup_{z,z'}\|P^k(z,\cdot)-P^k(z',\cdot)\|_{\mathrm{TV}}\le4^{-\lfloor k/\tau_{\mathrm{mix}}\rfloor}$. Neither states nor the transition kernel are revealed.

At any finite point $x$, a query returns the current state's sample function value $F(x;Z)$. Unbiasedness under the stationary marginal does not imply conditional unbiasedness given an adaptive history.

Two paid exact evaluations are allowed at each state before the chain advances. Each pair costs two scalar calls. No free transitions, full gradients or state contents are provided.

The public inputs are $d$, $\beta$, $\mu$, $\sigma_g$, $\tau_{\mathrm{mix}}$, $r_0$, $\varepsilon$, $x^0$, $x_f^0$, together with the sets, kernels and auxiliary operations explicitly declared above. Information about the unknown objective and any undisclosed sample distribution is obtained only through the stated interface.

### Output

Return $\widehat{x}\in \mathbb{R}^d$. The output may be an unqueried point, a random choice among previous points, or an average or convex combination that remains in the stated space. No function value, gradient, inner solution, or accuracy certificate must accompany the output.

### Loss or accuracy criterion

The base loss is $\ell(I,x)=f(x)-f_*$, where $f_*=\inf_{u\in \mathbb{R}^d}f(u)$. This nonnegative loss is evaluated at the output, with tolerance $\varepsilon$.

### Resource accounting

One scalar sample-function value costs $1$ call; two points with the same sample handle or Markov state cost $2$ calls. Batches, initialization and repeated visits are charged per value. An empty handle supplies no free instance information.

Only the declared oracle resource is charged. Computation and storage using existing information, together with explicitly known geometric and proximal operations, are free.

Observations needed to advance the chain are also counted in $N$. The retained resource is the expected scalar budget $\mathbb{E}[N]\le T$; states cannot be skipped for free.

### Algorithm views and success guarantees

Private randomization is allowed, with the seed independent of the instance and external randomness. Queries, stopping and postprocessing may be arbitrary measurable adaptive functions of the history. No linear-span or zero-respecting restriction is imposed.

Interactions are sequential, and every actual response in a batch is charged separately. Except for explicitly listed auxiliary interfaces, arithmetic, linear algebra, storage, and internal computation on available information are free, with no additional communication or memory restriction. Finite-difference steps must be finite and positive; real-number precision is not charged separately.

After fixing the public inputs, choose one algorithm that works for every admissible instance and reply law. Require $\mathbb{E}[\ell(I,\widehat{x})]\le \varepsilon$, fixing the instance before averaging over algorithmic and feedback randomness.

The cost requirement is imposed separately for every admissible instance: $\mathbb{E}[N]\le T$. This does not require the call count on every execution path to be below $T$.

## 2. Notation and parameters

$d$: Dimension of the variable space **Domain:** $d\in\mathbb{N},\ d\ge1$.

$\beta$: Public upper bound on the gradient Lipschitz constant **Domain:** $\beta>0$.

The object, norm and domain are fixed by the specific inequalities in this profile's model.

$\mu$: Public lower bound on the strong-convexity modulus **Domain:** $\mu>0$.

$\sigma_g$: Uniform norm bound on sample-gradient deviations from the population gradient **Domain:** $\sigma_g\ge0$.

$\|\nabla F(x;Z)-\nabla f(x)\|_2\le\sigma_g$, with the probability and scope specified by the model.

$\tau_{\mathrm{mix}}$: Upper bound on the geometric mixing time **Domain:** $\tau_{\mathrm{mix}}\in\mathbb{N},\ \tau_{\mathrm{mix}}\ge1$.

$r_0$: Upper bound on the potential formed from initial distance and objective gap **Domain:** $r_0\ge0$.

$\mu^{-1}(f(x_f^0)-f_*)+\|x^0-x_*\|_2^2\le r_0$

$\varepsilon$: Error target; norm and squared-norm criteria use different thresholds **Domain:** $\varepsilon>0$.

$\kappa$: Ratio of the known smoothness and strong-convexity bounds **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu$

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

$Z,F(\cdot;Z)$: Hidden sample and its associated sample function **Domain:** Samples lie in an admissible probability space; each sample function is real-valued on the declared domain.

The population objective is the expectation under the sample distribution or stationary distribution.

$G(Z)$: Random sample Lipschitz coefficient **Domain:** $G(Z)\ge0$.

The model's difference inequality holds for each sample, with the moment budget fixed as specified here.

$\nabla f,\nabla^2f,D^jf$: Gradient, Hessian, and higher Fréchet derivatives **Domain:** $\nabla f\in\mathbb{R}^d,\ \nabla^2f\in\mathbb{R}^{d\times d}$; $D^jf$ is a $j$-linear form.

Used only at derivative orders and on regions where the model guarantees its existence.

$\|\cdot\|_{\mathrm{op}}$: Euclidean induced matrix or tensor operator norm **Domain:** Take the supremum over Euclidean unit input vectors of the corresponding order.

$\|T\|_{\mathrm{op}}=\sup_{\|u_1\|_2,\ldots,\|u_j\|_2\le1}|T[u_1,\ldots,u_j]|$

$\mathcal{X}_{\mathrm{fun}},\mathcal{X}_{\mathrm{out}},\mathcal{X}$: Function domain, admissible output domain and optimization domain **Domain:** Each is the Euclidean space or subset explicitly specified in this profile.

$\mathcal{X}_{\mathrm{out}}=\mathbb{R}^d$ and $\mathcal{X}=\mathbb{R}^d$; the function domain is the region on which the model imposes regularity.

$N^*$: Optimal worst-case oracle complexity satisfying the complete guarantee **Domain:** $N^*\in[0,+\infty]$.

Take the infimum over admissible algorithms, followed by the worst case over the instances of this profile. With multiple resources, use this scalar only for an explicitly specified resource projection.

$x_*$: A global minimizer or quadratic center whose existence is promised by the model **Domain:** Belongs to the localization domain specified here; used only under the stated existence promise.

The full-space minimizer is unique in the strongly convex class. The center of a positive semidefinite quadratic model need not be unique.

$P,\pi,Z_t$: Markov transition kernel, stationary distribution and hidden states **Domain:** Probability kernel and probability measure on the same state space.

$\pi P=\pi$; initialize with $Z_0\sim\pi$.

$\|P-Q\|_{\mathrm{TV}}$: Total variation distance between probability distributions **Domain:** Probability distributions on the same measurable space.

$\|P-Q\|_{\mathrm{TV}}=\sup_A|P(A)-Q(A)|$, where the supremum is over all measurable sets.

$x^0,x_f^0,x_f^N$: Two initial iterates and the final companion iterate **Domain:** Both belong to $\mathbb{R}^d$.

The final output is the companion iterate of the selected method, with its information obtained through paid observations.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

$$
C^\star_{v,\pi}(\varepsilon;\theta)=\inf\{B\ge0:\exists\mathcal A\in\mathfrak A_v,\ C_\pi(\mathcal A,I)\le B\ \text{and}\ G_v(\mathcal A,I;\varepsilon)\ \forall I\}
$$

**Definition.** one paid scalar function value

**Scope.** declared_joint_parameter_window

**Optimization direction.** minimize

Here v is the selected algorithm view, G_v its complete success guarantee, I an admissible fixed instance, theta the remaining parameters, and C_pi the declared resource projection. C_pi uses the view's fixed-path or expected-work budget convention, including initialization. No change of guarantee or scalarization is implicit.

### R1 - Parameter regime M02.R1

**Region.** $d\ge1$, $\beta\ge\mu>0$, $\sigma_g>0$, integer $\tau_{\mathrm{mix}}\ge1$, $r_0>0$ and $0<\varepsilon<\mu r_0$. The statistical term satisfies $(d+\tau_{\mathrm{mix}})\sigma_g^2/(\mu\varepsilon)\ge Cd\sqrt\kappa[1+\log(\mu r_0/\varepsilon)]$. The interface allows two values at the same Markov state, with stationary initialization and an expected query budget.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
\widetilde{O}((d+\tau_{\rm mix})\sigma_g^2/(\mu\varepsilon))
$$

### R2 - Parameter regime M02.R_zero

**Region.** $\varepsilon\ge\mu r_0$.

**Quantity.** Q1

**Resource.** one paid scalar function value

**Status.** Optimal

**Lower bound.** B3

$$
0
$$

**Upper bound.** B2

$$
0
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Preserve the hidden-state transition protocol, replies per state and original Markov mixing assumption. State contents and transitions supply no free information.

**Guarantee mapping.** Error is measured in expectation for each instance. Running cost is separately measured in expectation and cannot be interpreted directly as a fixed budget on each execution path.

**Output mapping.** Use the source algorithm's companion iterate $x_f^N\in\mathbb{R}^d$.

**Resource mapping.** Expected total number of paid scalar calls, including observations required to advance the state.

### B1 - Markovian acceleration using two values from the same state

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde{O}\!\left[d\sqrt\kappa\log(\mu r_0/\varepsilon)+\frac{(d+\tau_{\rm mix})\sigma_g^2}{\mu\varepsilon}\right]
$$

**Sources.** [1](https://proceedings.mlr.press/v306/prokhorov26a.html)

**Conditions.** The chain starts in stationarity and satisfies the stated geometric mixing condition. Samples are smooth with uniformly bounded gradient deviations. Cost is the expected number of paid scalar calls, and the output is the companion iterate.

**Local argument.** A1

**Source location.** [1](https://proceedings.mlr.press/v306/prokhorov26a.html) theorem: Theorem 1 prime; potential function in Eq. (20); pdf pages: 7; printed pages: 7

**Source location.** [1](https://proceedings.mlr.press/v306/prokhorov26a.html) theorem: Theorem 1 prime; potential function in Eq. (20)

**Source location.** [1](https://proceedings.mlr.press/v306/prokhorov26a.html) theorem: Theorem 1 prime; potential function in Eq. (20); pdf pages: 14; printed pages: 14

### B2 - Return the public initial point

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
0
$$

**Conditions.** $\varepsilon\ge\mu r_0$.

**Local argument.** A2

### B3 - Nonnegative oracle cost

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
0
$$

**Conditions.** $\varepsilon\ge\mu r_0$.

**Local argument.** A2

## 5. Local arguments

### A1 - Objective-gap conversion for the Markov upper bounds

**Scope.** The source uniform-noise assumptions and expected random call budget remain in force; no fixed-cap lower comparison is asserted by this conversion.

The native potential
$$r_N=\frac{f(x_f^N)-f_*}{\mu}+\|x^N-x_*\|^2$$
converts to expected objective gap by outputting $x_f^N$ and setting the potential target to $\varepsilon/\mu$.

Both terms in the potential are nonnegative. Thus $\mathbb E r_N\le\varepsilon/\mu$ implies $\mathbb E[f(x_f^N)-f_*]\le\varepsilon$. Substitute this target into the published smooth one-point and two-point theorems. This gives the registered terms
$$\widetilde O\!\left[d\sqrt\kappa\log(\mu r_0/\varepsilon)+\kappa d(d+\tau_{\rm mix})\sigma_v^2/\varepsilon^2\right]$$
and
$$\widetilde O\!\left[d\sqrt\kappa\log(\mu r_0/\varepsilon)+(d+\tau_{\rm mix})\sigma_g^2/(\mu\varepsilon)\right].$$
Using only an upper smoothness bound on squared distance would introduce an unnecessary extra condition-number loss; the companion iterate avoids that loss directly.

Two limitations remain separate. The source Gaussian lower construction initially satisfies moment bounds, while the upper model assumes uniform bounds; the proposed clipping-and-debiasing transfer is not supplied here as a complete compatible lower proof. Also, the upper's expected random cost and the lower's fixed cap are different resource conventions. Neither mismatch is removed by this objective conversion. Accordingly, the strict uniform-noise, expected-cost view retains a certified upper and a missing compatible lower. Conditional lower formulas do not enter its closed bracket.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

**Sources.** [1](https://proceedings.mlr.press/v306/prokhorov26a.html)

### A2 - Zero-query certificates

**Scope.** The stated sufficient accuracy regions only; no assertion that every certificate is sharp.

A public feasible point whose objective gap is at most $G_0$ solves every target $\varepsilon\ge G_0$ with exactly zero calls.

For a convex mean objective that is $L$-Lipschitz on a ball of radius $R$, the center has gap at most $LR$. A sample Lipschitz modulus $G$ with $\mathbb E G^r\le L^r$, $r>1$, implies $\mathbb E G\le L$, so the same certificate applies to moment models. Integrability at one point ensures that the mean is defined.

If a globally $\beta$-smooth objective has a global minimizer within distance $R$ of the public initial point, its gradient vanishes at that minimizer and the smoothness inequality gives gap at most $\beta R^2/2$. In a declared norm, use the corresponding radius in that norm. For $B_p(R)$ with Euclidean regularity this radius is $R$ when $p\le2$ and $R d^{1/2-1/p}$ when $p\ge2$.

For a known positive semidefinite quadratic matrix $A$, the center has gap at most $\lambda_{\max}(A)R^2/2$; if $A=0$, the loss is identically zero. A public initial-gap promise $\Delta$ directly gives the certificate $G_0=\Delta$. For the Markov potential $r_0$, its companion initial iterate has gap at most $\mu r_0$. These are different certificates with different model assumptions; in particular, an unknown matrix with no public spectral bound does not acquire a uniform certificate.

Call counts are nonnegative. Together with the stated algorithm, this proves exact zero complexity on each certified region. The upper/lower ratio is undefined, so it is stored as null rather than as $0/0$.

**Limits of the argument.** Local argument and specification transfer; cited external theorems remain primary dependencies.

## References

[1] Boris Prokhorov, Semyon Chebykin, Alexander Gasnikov, Aleksandr Beznosikov. Gradient-Free Approaches is a Key to an Efficient Interaction with Markovian Stochasticity. ICML2026 PMLR306:99867-99905.

https://proceedings.mlr.press/v306/prokhorov26a.html
