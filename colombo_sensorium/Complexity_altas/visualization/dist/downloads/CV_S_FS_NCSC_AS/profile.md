# Finite-sum nonconvex-strongly-concave minimax optimization under mean-square smoothness

**Setting ID.** `CV_S_FS_NCSC_AS`

Minimax optimization

$$
\min_x\Phi(x),\quad\Phi(x)=\max_y\frac1n\sum_{i=1}^n f_i(x,y).
$$

**Status.** Logarithmic gap; Polynomial gap; Bounds missing

**Gap classes present.** Logarithmic gap; Polynomial gap

**TASK tags.** formulation: Minimize finite sum value; task family: Minimax

**MODEL tags.** convexity: No convexity promise in block; convexity: Nonconvex strongly concave; initialization: Exact dual initialization; smoothness: Mean square average; smoothness: Mean square component smoothness

**ORACLE tags.** feedback quality: Exact; index control: Algorithm selects; interface family: Component gradient; operation: Component joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; query domain: Full space; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** adaptivity: Adaptive; randomization: Private randomness allowed; restriction: Explicitly no additional algorithm restrictions; restriction: No additional span restriction explicitly imposed; restriction: No additional zero-respecting restriction explicitly imposed; restriction: Zero respecting

**OUTPUT tags.** certificate: No additional output certificate required; object: Point; object: Primal point; postprocessing: Measurable postprocessing; postprocessing: Unqueried output explicitly allowed; support: Zero respecting

**METRIC tags.** criterion: Reduced-objective gradient norm

**GUARANTEE tags.** aggregation: Per instance; aggregation: Second moment of the complete error; confidence: Fixed numerical success / failure probability; mode: Expectation; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** accounting: Joint coordinates retained; budget: Fixed worst-case budget; budget: Worst-instance expected cost; measure: N component; precision: Bit precision not counted; setup: Initialization included

## 1. Setting specification

### Task

$$
\min_x\Phi(x),\quad\Phi(x)=\max_y\frac1n\sum_{i=1}^n f_i(x,y).
$$

### Admissible model

Assume $f=n^{-1}\sum_{i=1}^n f_i$, with each $f_i:\mathbb{R}^{d_x+d_y}\to\mathbb{R}$ continuously differentiable. For all full-space points $z,w$,

$$
\frac1n\sum_{i=1}^n\|\nabla f_i(z)-\nabla f_i(w)\|_2^2\le\beta^2\|z-w\|_2^2.
$$

Only the mean function $f(x,\cdot)$ must be uniformly $\mu_y$-strongly concave. Components need not be concave or individually $\beta$-smooth; $f(\cdot,y)$ and $\Phi$ may be nonconvex.

The public initial point is $(0,0)$, with promises $y^\star(0)=0$ and $\Phi(0)-\inf_x\Phi(x)\le\Delta<\infty$. Attainment of the primal minimum is not required. Assume $n\ge2$ and $\kappa=\beta/\mu_y\ge1$.

### Oracle interface

Public inputs include block dimensions $d_x,d_y$ and $\Delta$, $\beta$, $\varepsilon$, $\mu_y$, and $n$, together with the stated initial points and feasible-set information. Analytic representations of hidden functions, operators, and matrices are not supplied.

$$
(i,x,y)\longmapsto\nabla f_i(x,y),\quad i\in\{1,\ldots,n\},\ (x,y)\in\mathbb{R}^{d_x+d_y}.
$$

The algorithm selects a component index and query point. Each index always refers to the same fixed component. The response is its exact full joint gradient, without a function value, Hessian, best response, or reduced gradient. There is no random oracle noise.

### Output

Return a single primal point $\widehat{x}\in\mathbb{R}^{d_x}$; no dual point or computable certificate is required.

### Loss or accuracy criterion

$$
\|\nabla\Phi(\widehat{x})\|_2
$$

$\nabla\Phi(x)=\nabla_x f(x,y^\star(x))$.

### Resource accounting

One component joint-gradient call counts once in $N_{\rm component}$. A complete mean gradient requires $n$ calls.

Count all information calls for one instance and one requested accuracy, including initialization. Exact-real arithmetic, storage, and solving known models from public inputs and returned data are uncharged. This query-complexity quantity does not certify arithmetic or bit complexity.

### Algorithm views and success guarantees

#### Randomized zero respecting expected rms

Randomized adaptive zero-respecting algorithms are permitted. The first query is at $(0,0)$. At query $t$, the supports of $x$ and $y$ lie in the unions of the corresponding previously returned gradient supports. The support of output $\widehat{x}$ lies in the union of all returned $x$-gradient supports.

Component indices, values on exposed coordinates, and stopping decisions may be fully adaptive. Unexposed coordinates or arbitrary coordinate rotations cannot be used to circumvent the support restriction.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\|\nabla\Phi(\widehat{x})\|_2\right)^2\right]\le\varepsilon^2.
$$

Expectation is only over the algorithm's private seed. Exact responses from fixed components contain no oracle noise.

**Output qualification.** Unqueried outputs are allowed but must obey the stated zero-respecting rule.

**Resource qualification.** Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

**Budget convention.** worst-case expected total component calls; random stopping allowed

#### Randomized unrestricted expected rms

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

Choose one algorithm, then require the guarantee for every admissible instance and stochastic-feedback mechanism.

$$
\mathbb{E}\!\left[\left(\|\nabla\Phi(\widehat{x})\|_2\right)^2\right]\le\varepsilon^2.
$$

Expectation is only over the algorithm's private seed. Exact responses from fixed components contain no oracle noise.

**Output qualification.** The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

**Resource qualification.** Use expected work on the worst instance. The algorithm stops almost surely, with call count $\tau$ satisfying $\sup_I\mathbb{E}[\tau]\le N$. This does not require every execution path to finish within $N$ calls.

**Budget convention.** worst_instance_expected_calls

#### Randomized unrestricted fixed probability

Arbitrary measurable sequential adaptive randomized algorithms are allowed. The private seed is independent of the hidden instance. Queries, stopping, and output may use the full history, without additional span, zero-respecting, communication, or memory restrictions.

A single algorithm is chosen from the public input and must satisfy the guarantee for every fixed admissible instance.

$$
\Pr\!\left(\|\nabla\Phi(\widehat{x})\|_2\le\varepsilon\right)\ge\frac23.
$$

Probability is over private algorithmic randomness only. The unknown instance is fixed before interaction.

**Output qualification.** The output may be any measurable postprocessing of the history, including an unqueried point, average, or convex combination. It must satisfy the stated domain and feasibility requirements; no additional function value or computable certificate is required.

**Resource qualification.** Use a fixed worst-case budget: calls never exceed the prespecified $N$ on any instance or random execution path. Earlier stopping within the budget is permitted.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$\Delta$: A public bound on the initial reduced-objective value above its infimum. Attainment of the infimum is not required. **Domain:** Positive real number.

$\Phi(0)-\inf_x\Phi(x)\le\Delta$

$\beta$: Mean-square average Lipschitz upper bound for component joint gradients **Domain:** Positive real number.

$\frac1n\sum_{i=1}^n\|\nabla f_i(z)-\nabla f_i(w)\|_2^2\le\beta^2\|z-w\|_2^2$

$c_0$: Universal small constant in the lower-bound accuracy window; no numerical value is specified. **Domain:** Positive constant without an assigned numerical value.

$d$: The joint Euclidean dimension is $d=d_x+d_y$. Within its stated window, the lower bound may choose finite block dimensions. **Domain:** Integer at least $2$.

$\varepsilon$: Euclidean norm tolerance for the true reduced gradient; the mean-square contract targets its square $\varepsilon^2$. **Domain:** Positive real number.

$\kappa$: Ratio of the population smoothness upper bound, or mean-square average smoothness for finite sums, to the dual strong-concavity lower bound **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\mu_y$: A uniform strong-convexity lower bound for −f(x,·) at every fixed x; equivalently, the dual strong-concavity modulus of f. **Domain:** $0<\mu_y\le\beta$.

$f(x,v)\le f(x,y)+\langle\nabla_yf(x,y),v-y\rangle-\frac{\mu_y}{2}\|v-y\|_2^2$

$n$: Fixed number of finite-sum components; the full function or operator is their 1/n average **Domain:** Integer at least $2$.

$\|\cdot\|_2,\langle\cdot,\cdot\rangle$: Euclidean norm and inner product; the product-space norm is the square root of the sum of the squared block norms. **Domain:** The specified finite-dimensional real vector space.

$\|v\|_2=\sqrt{\langle v,v\rangle}$

$d_x,d_y$: Positive integer primal and dual block dimensions; joint dimension $d=d_x+d_y$ **Domain:** Positive integer.

$f$: Unknown real-valued payoff, with primal and dual input blocks. **Domain:** $f:(x,y)\mapsto f(x,y)\in\mathbb R$.

$x,y,z$: Primal variable, dual variable, and joint point **Domain:** $x\in\mathbb R^{d_x},\ y\in\mathbb R^{d_y},\ z=(x,y)\in\mathbb R^{d_x+d_y}$.

$z=(x,y)$

$\nabla f,\nabla_x f,\nabla_y f$: Complete joint gradient and its two blocks **Domain:** $\nabla_x f\in\mathbb R^{d_x},\ \nabla_y f\in\mathbb R^{d_y}$.

$\nabla f=(\nabla_x f,\nabla_y f)$

$\Phi$: Reduced objective after global dual maximization; neither its value nor gradient is an additional free interface **Domain:** Real-valued function on the primal-variable space.

$\Phi(x)=\max_{y\in \mathbb R^{d_y}}f(x,y)$

$y^\star(x)$: The unique global dual maximizer at fixed primal x. **Domain:** $y^\star(x)\in\mathbb R^{d_y}$.

$y^\star(x)=\arg\max_{y\in\mathbb R^{d_y}}f(x,y)$

$f_i,i$: The fixed ith real-valued component and the algorithm-selected index. **Domain:** $i\in\{1,\ldots,n\},\quad f_i:\text{the declared product domain}\to\mathbb R$.

$f=\frac1n\sum_{i=1}^n f_i$

$x_0,y_0$: The public initial primal and dual variables. **Domain:** The respective feasible domains. Both equal zero when the origins are explicitly fixed.

$\widehat x$: The point or variable blocks ultimately returned by the algorithm, corresponding to the hatted variables in the error formula. **Domain:** A feasible primal point in $\mathbb R^{d_x}$.

$\mathbb E,\Pr$: Expectation and probability over the explicitly allowed algorithm and sample randomness, with the hidden instance fixed. **Domain:** Operations on the corresponding probability space.

$N_{\rm component}$: Number of full joint-gradient queries to a specified component **Domain:** Nonnegative integer count; expected work is its expectation.

$\tau$: Cumulative primary information calls at termination of one run; almost surely finite, with random stopping allowed. **Domain:** A nonnegative integer-valued random variable.

$\sup_I\mathbb E[\tau]\le N$

$N$: A worst-instance upper bound on expected total information calls at termination. **Domain:** A nonnegative real.

$N^\star$: The infimum principal query budget among algorithms satisfying every stated instancewise output guarantee. **Domain:** Nonnegative extended real value; by convention, positive infinity if no successful algorithm or no uniform finite budget exists.

$\mathcal A,I$: An algorithm selected from public inputs and an admissible hidden instance fixed before interaction **Domain:** The specified algorithm and model classes.

$\omega$: A complete realization of algorithmic and sample randomness. **Domain:** Corresponding sample space.

$O,\Omega,\Theta,\widetilde O$: Asymptotic upper and lower bounds, constant-factor matching, and upper bounds hiding the stated logarithmic factors, within the corresponding regions. **Domain:** Nonnegative complexity function; subscript p permits additional dependence only on fixed p.

$\mathfrak A_\varepsilon$: Algorithms using the allowed interfaces, algorithm restrictions, and output domain, and satisfying the displayed complete error guarantee for every fixed admissible instance **Domain:** The algorithm class is defined at fixed public parameters and target tolerance $\varepsilon$.

$a$: The dimensionless scale of the initial primal objective gap. **Domain:** Positive real number.

$a=\beta\Delta/\varepsilon^2$

$a_\star$: A common sufficient constant for all applicable lower-bound regimes; constants from different sources are not identified without justification. **Domain:** Universal positive constant.

$d_x$: Primal-space dimension **Domain:** Positive integer.

$d_y$: The dimension of the dual-variable space. **Domain:** Positive integer.

$\ell_R$: Logarithmic RPDA initialization and final-refinement overhead. **Domain:** Positive real number.

$\ell_R=1+\log(2+\kappa)+\log(2+(1+\kappa)^2a)$

$\kappa_0$: Sufficient condition-number threshold for the componentwise nonconvex-strongly-concave lower bound. **Domain:** Universal positive constant.

$\log,\ln,\log_+$: Natural logarithm and its nonnegative truncation **Domain:** Arguments of log and ln are positive; the argument of $\log_+$ may be zero.

$\log_+(t)=\log(\max\{1,t\})$

$N$: A uniform cap on principal information calls for every admissible instance and execution path. **Domain:** Nonnegative integer.

$a_{\rm U06}$: Source sufficient small-accuracy threshold **Domain:** $a_{\rm U06}>0$ is the universal constant A_* in Theorem main.

## 3. Complexity bracket

### Compared quantities

#### Q1 - target accuracy cost

**View.** Randomized zero respecting expected rms

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \mathbb E_\omega[N_{\rm component}(\mathcal A,I,\omega)]
$$

**Scope.** Take the worst case over admissible finite-dimensional instances. Theorems with dimension conditions apply only within those windows and do not establish fixed-dimensional saturation rates.

**Optimization direction.** minimize

Each call counts the complete response package specified by this interface. The algorithm class retains the stated randomization, adaptivity, and output conditions and must satisfy the full error guarantee for every fixed admissible instance. Expectations include the algorithm's seed and sampled observations; the stated random stopping rules are allowed.

#### Q2 - target accuracy cost

**View.** Randomized unrestricted expected rms

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \mathbb E_\omega[N_{\rm component}(\mathcal A,I,\omega)]
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

Each call counts the complete response package specified by this interface. The algorithm class retains the stated randomization, adaptivity, and output conditions and must satisfy the full error guarantee for every fixed admissible instance. Expectations include the algorithm's seed and sampled observations; the stated random stopping rules are allowed.

#### Q3 - target accuracy cost

**View.** Randomized unrestricted fixed probability

$$
N^\star(\varepsilon)=\inf_{\mathcal A\in\mathfrak A_\varepsilon}\sup_I \sup_\omega N_{\rm component}(\mathcal A,I,\omega)
$$

**Scope.** The instancewise guarantee uses the same contract; dimension obeys the specification and theorem region.

**Optimization direction.** minimize

One call is charged for the full response specified by the interface. The algorithm class obeys the declared randomization, adaptivity, and output rules and must satisfy the complete error guarantee on every fixed admissible instance. The call cap is uniform over instances and execution paths.

### R1 - Small-condition-number regime

**Region.** Require $n\ge2$, $0<\varepsilon^2\le c_0\beta\Delta$, and $1\le\kappa\le\sqrt n$.

**Views.** Randomized zero respecting expected rms

**Quantity.** Q1

**Resource.** Expected total number of component queries.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(n+\sqrt n\,\kappa\beta\Delta/\varepsilon^2)
$$

**Upper bound.** B1

$$
\widetilde{O}(n+\sqrt n\,\kappa\beta\Delta/\varepsilon^2)
$$

**Comparison argument.** Compare only the powers of n, $\kappa$, and $\varepsilon$. The logarithmic factors are not fully resolved, so this row does not certify a precise multiplicative logarithmic gap.

### R2 - The large-condition-number region for expected work.

**Region.** Assume $n\ge2$, $0<\varepsilon^2\le c_0\beta\Delta$, and $\kappa\ge\sqrt n$.

**Views.** Randomized zero respecting expected rms

**Quantity.** Q1

**Resource.** Expected total number of component queries.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega(n+n^{3/4}\sqrt\kappa\,\beta\Delta/\varepsilon^2)
$$

**Upper bound.** B3

$$
\widetilde{O}(n+n^{3/4}\sqrt\kappa\,\beta\Delta/\varepsilon^2)
$$

**Comparison argument.** Compare only the powers of n, $\kappa$, and $\varepsilon$. The logarithmic factors are not fully resolved, so this row does not certify a precise multiplicative logarithmic gap.

### R3 - Condition number exactly equal to $1$

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. The value $a_\star$ is a common sufficient constant for all cited lower-bound thresholds. Also require $\kappa=1$.

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B9

$$
\Omega(n+\sqrt n\,a)
$$

**Upper bound.** B8

$$
O(n+\sqrt n\,a)
$$

**Gap or comparison.** $O(1)$

### R4 - Boundary regime with a universally bounded condition number

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. The value $a_\star$ is a common sufficient constant for all cited lower-bound thresholds. Also require $\sqrt n<\kappa<\kappa_0$.

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B9

$$
\Omega(n+\sqrt n\,a)
$$

**Upper bound.** B7, B6

$$
O\!\left(\min\{n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa),(n+\kappa^2)(1+a+\ell_R)\}\right)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The budget $\kappa<\kappa_0$ constrains both $n<\kappa_0^2$, which are universally bounded. The component lower bound requiring $\kappa\ge\kappa_0$ is not invoked in this regime.

### R5 - Outside the lower-bound accuracy threshold

**Region.** Assume $n\ge2$, $\kappa\ge1$, and $0<a<a_\star$.

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B5, B6, B7, B8

Choose the registered upper bound for the relevant $\kappa$ region.

**Comparison argument.** Enforce each upper bound's condition-number restriction separately. Complete matching is unavailable outside the lower bounds' common accuracy window.

### R6 - Condition number exactly equal to $1$

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. The value $a_\star$ is a common sufficient constant for all cited lower-bound thresholds. Also require $\kappa=1$.

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B15

$$
\Omega(n+\sqrt n\,a)
$$

**Upper bound.** B14

$$
O(n+\sqrt n\,a)
$$

**Gap or comparison.** $O(1)$

### R7 - Boundary regime with a universally bounded condition number

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. The value $a_\star$ is a common sufficient constant for all cited lower-bound thresholds. Also require $\sqrt n<\kappa<\kappa_0$.

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Optimal

**Lower bound.** B15

$$
\Omega(n+\sqrt n\,a)
$$

**Upper bound.** B13, B12

$$
O\!\left(\min\{n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa),(n+\kappa^2)(1+a+\ell_R)\}\right)
$$

**Gap or comparison.** $O(1)$

**Comparison argument.** The budget $\kappa<\kappa_0$ constrains both $n<\kappa_0^2$, which are universally bounded. The component lower bound requiring $\kappa\ge\kappa_0$ is not invoked in this regime.

### R8 - Outside the lower-bound accuracy threshold

**Region.** Assume $n\ge2$, $\kappa\ge1$, and $0<a<a_\star$.

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B11, B12, B13, B14

Choose the registered upper bound for the relevant $\kappa$ region.

**Comparison argument.** Enforce each upper bound's condition-number restriction separately. Complete matching is unavailable outside the lower bounds' common accuracy window.

### R9 - AS / Expected RMS and work / small condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Logarithmic gap

**Lower bound.** B18

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Upper bound.** B17

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R10 - AS / Expected RMS and work / large condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Logarithmic gap

**Lower bound.** B20

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Upper bound.** B19

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R11 - AS / Constant probability and fixed budget / small condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Logarithmic gap

**Lower bound.** B22

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Upper bound.** B21

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R12 - AS / Constant probability and fixed budget / large condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Logarithmic gap

**Lower bound.** B24

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Upper bound.** B23

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R13 - Small-condition-number regime — remaining domain

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. The value $a_\star$ is a common sufficient constant for all cited lower-bound thresholds. Also require $1<\kappa\le\sqrt n$. Restricted to the complement of: ($\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.).

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B9

$$
\Omega(n+\sqrt n\,a)
$$

**Upper bound.** B5

$$
O(\sqrt n\,\kappa a+n\ell_R)
$$

**Gap or comparison.** $O\!\left(\frac{\sqrt n\,\kappa a+n\ell_R}{n+\sqrt n\,a}\right)$

**Comparison argument.** When n, $\kappa$, and a vary jointly, the envelope permits a polynomial gap $\kappa$. The gap may shrink if $\kappa$ is fixed or the n term dominates. If $\kappa\ge\kappa_0$, also take the maximum with the identical-component lower bound.

### R14 - Large-condition-number regime — remaining domain

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. Choose $a_\star$ as a common sufficient constant for all cited lower-bound thresholds. Also require $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Restricted to the complement of: ($\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.).

**Views.** Randomized unrestricted expected rms

**Quantity.** Q2

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B9, B10

$$
\Omega\!\left(\max\{n+\sqrt n\,a,\sqrt\kappa\,a\}\right)
$$

**Upper bound.** B7, B6

$$
O\!\left(\min\{n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa),(n+\kappa^2)(1+a+\ell_R)\}\right)
$$

**Gap or comparison.** $\frac{\min\{n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa),(n+\kappa^2)(1+a+\ell_R)\}}{\max\{n+\sqrt n\,a,\sqrt\kappa a\}}$

**Comparison argument.** Minimize upper bounds over complete algorithms and maximize lower bounds. Both lower bounds allow arbitrary randomized algorithms.

### R15 - Small-condition-number regime — remaining domain

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. The value $a_\star$ is a common sufficient constant for all cited lower-bound thresholds. Also require $1<\kappa\le\sqrt n$. Restricted to the complement of: ($\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.).

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B15

$$
\Omega(n+\sqrt n\,a)
$$

**Upper bound.** B11

$$
O(\sqrt n\,\kappa a+n\ell_R)
$$

**Gap or comparison.** $O\!\left(\frac{\sqrt n\,\kappa a+n\ell_R}{n+\sqrt n\,a}\right)$

**Comparison argument.** When n, $\kappa$, and a vary jointly, the envelope permits a polynomial gap $\kappa$. The gap may shrink if $\kappa$ is fixed or the n term dominates. If $\kappa\ge\kappa_0$, also take the maximum with the identical-component lower bound.

### R16 - Large-condition-number regime — remaining domain

**Region.** Assume $n\ge2$ and $a=\beta\Delta/\varepsilon^2\ge a_\star$. Choose $a_\star$ as a common sufficient constant for all cited lower-bound thresholds. Also require $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Restricted to the complement of: ($\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.).

**Views.** Randomized unrestricted fixed probability

**Quantity.** Q3

**Resource.** The principal resource specified in the resource section. Primitive operations and unit costs are measured along this axis.

**Status.** Polynomial gap

**Lower bound.** B15, B16

$$
\Omega\!\left(\max\{n+\sqrt n\,a,\sqrt\kappa\,a\}\right)
$$

**Upper bound.** B13, B12

$$
O\!\left(\min\{n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa),(n+\kappa^2)(1+a+\ell_R)\}\right)
$$

**Gap or comparison.** $\frac{\min\{n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa),(n+\kappa^2)(1+a+\ell_R)\}}{\max\{n+\sqrt n\,a,\sqrt\kappa a\}}$

**Comparison argument.** Minimize upper bounds over complete algorithms and maximize lower bounds. Both lower bounds allow arbitrary randomized algorithms.

## 4. Bounds and supporting evidence

### B1 - RPDA

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized zero respecting expected rms

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The variance-reduced inner loops of RPDA or Catalyst actually sample components randomly. Randomization describes the witness, not merely the admissible class.

$$
\widetilde{O}(n+\sqrt n\,\kappa\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Exact dual initialization $y^\star(0)=0$; queries and outputs obey this profile's zero-support rule.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**E N component.**

$$
\widetilde O(n+\sqrt n\,\kappa\beta\Delta/\varepsilon^2)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Retain logarithmic factors from initialization, final refinement, and Catalyst inner iterations. Their complete explicit powers have not been extracted.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorems1--3; Definition2; section: Sections2,4; pdf pages: 3; 4; 5; 6

The source lower bound concerns expected gradient norm and therefore also rules out the stronger mean-square guarantee, but its algorithm class remains zero-respecting. The small-condition-number upper-bound branch has a fixed call count; the large-condition-number branch controls expected work. They cannot both be labeled fixed worst-case budgets.

### B2 - dual-chain plus component hiding

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized zero respecting expected rms

**Witness or lower-bound scope.** The stated restricted randomized class

**Algorithm-scope qualification.** The lower bound covers randomized methods satisfying the zero-respecting condition on every path. It does not extend to arbitrary randomized queries.

$$
\Omega(n+\sqrt n\,\kappa\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The hard family and outputs obey the zero-respecting definition. This lower bound does not cover arbitrary-query algorithms.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(n+\sqrt n\,\kappa\beta\Delta/\varepsilon^2)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorems1--3; Definition2; section: Sections2,4; pdf pages: 3; 4; 5; 6

The source lower bound concerns expected gradient norm and therefore also rules out the stronger mean-square guarantee, but its algorithm class remains zero-respecting. The small-condition-number upper-bound branch has a fixed call count; the large-condition-number branch controls expected work. They cannot both be labeled fixed worst-case budgets.

### B3 - Catalyst reduction with inherited expected-work subsolver

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized zero respecting expected rms

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The variance-reduced inner loops of RPDA or Catalyst actually sample components randomly. Randomization describes the witness, not merely the admissible class.

$$
\widetilde{O}(n+n^{3/4}\sqrt\kappa\,\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Exact dual initialization $y^\star(0)=0$; queries and outputs obey this profile's zero-support rule.

**Dimension conditions.** The upper bound holds in every admissible finite dimension. The lower bound applies only in its separately stated dimension window.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**E N component.**

$$
\widetilde O(n+n^{3/4}\sqrt\kappa\,\beta\Delta/\varepsilon^2)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** Retain logarithmic factors from initialization, final refinement, and Catalyst inner iterations. Their complete explicit powers have not been extracted.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorems1--3; Definition2; section: Sections2,4; pdf pages: 3; 4; 5; 6

The source lower bound concerns expected gradient norm and therefore also rules out the stronger mean-square guarantee, but its algorithm class remains zero-respecting. The small-condition-number upper-bound branch has a fixed call count; the large-condition-number branch controls expected work. They cannot both be labeled fixed worst-case budgets.

### B4 - dual-chain plus component hiding

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized zero respecting expected rms

**Witness or lower-bound scope.** The stated restricted randomized class

**Algorithm-scope qualification.** The lower bound covers randomized methods satisfying the zero-respecting condition on every path. It does not extend to arbitrary randomized queries.

$$
\Omega(n+n^{3/4}\sqrt\kappa\,\beta\Delta/\varepsilon^2)
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Dimension conditions.** The hard family and outputs obey the zero-respecting definition. This lower bound does not cover arbitrary-query algorithms.

**Oracle correspondence.** Use only primitive operations recorded under ORACLE. Unknown inner solutions and reduced gradients are not supplied for free.

**Guarantee conversion.** The error criterion, sources of randomness, and expectation/probability quantifiers match this specification. Any conversion is explained separately below.

**Output rule.** Outputs belong to the declared space and are evaluated by this profile's METRIC. Different gaps, norms, and squared norms are not interchanged.

**Resource conversion.** All resource costs come from one algorithm or one hard construction. Initialization and nested calls are included.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N.**

$$
\Omega(n+n^{3/4}\sqrt\kappa\,\beta\Delta/\varepsilon^2)
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Logarithmic factors.** None.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorems1--3; Definition2; section: Sections2,4; pdf pages: 3; 4; 5; 6

The source lower bound concerns expected gradient norm and therefore also rules out the stronger mean-square guarantee, but its algorithm class remains zero-respecting. The small-condition-number upper-bound branch has a fixed call count; the large-condition-number branch controls expected work. They cannot both be labeled fixed worst-case budgets.

### B5 - Randomized recursive proximal difference algorithm, RPDA

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O\!\left(\sqrt n\,\kappa a+n\ell_R\right).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O\!\left(\sqrt n\,\kappa a+n\ell_R\right).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** RPDA is a specific randomized witness, and its zero-respecting updates also belong to the larger allowed class. Each full gradient costs $n$ component calls, and a two-point component difference costs two calls. Counts include initialization, main iterations, and refinement; $\ell_R=1+\log(2+\kappa)+\log(2+(1+\kappa)^2a)$ records these logarithmic overheads. Run the source algorithm directly at mean-square tolerance $\varepsilon$. Its native guarantee is the target, and its fixed call cap also bounds expected calls. No Markov conversion or truncation is required.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorem 3; Algorithm 1; Appendix H, (49)–(50), H.6; pdf pages: 6; 8; 25; 26; 30

The admissible algorithm class contains the original RPDA, so its existence upper bound remains valid. Retain its native mean-square guarantee and fixed call count separately.

The mean-square guarantee directly uses tolerance $\varepsilon$. The fixed-budget probability guarantee uses $\varepsilon/\sqrt3$, without an additional work-truncation step.

### B6 - Randomized recursive proximal difference algorithm, RPDA

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O\!\left((n+\kappa^2)(1+a+\ell_R)\right).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O\!\left((n+\kappa^2)(1+a+\ell_R)\right).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** RPDA is a specific randomized witness, and its zero-respecting updates also belong to the larger allowed class. Each full gradient costs $n$ component calls, and a two-point component difference costs two calls. Counts include initialization, main iterations, and refinement; $\ell_R=1+\log(2+\kappa)+\log(2+(1+\kappa)^2a)$ records these logarithmic overheads. Run the source algorithm directly at mean-square tolerance $\varepsilon$. Its native guarantee is the target, and its fixed call cap also bounds expected calls. No Markov conversion or truncation is required.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorem 3; Algorithm 1; Appendix H, (49)–(50), H.6; pdf pages: 6; 8; 25; 26; 30

The admissible algorithm class contains the original RPDA, so its existence upper bound remains valid. Retain its native mean-square guarantee and fixed call count separately.

The mean-square guarantee directly uses tolerance $\varepsilon$. The fixed-budget probability guarantee uses $\varepsilon/\sqrt3$, without an additional work-truncation step.

### B7 - Catalyst with gradient-based SVRG inner iterations.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O\!\left(n^{3/4}\sqrt\kappa\,(1+a)\ln^2(2+\kappa)\right).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1) [3](https://arxiv.org/pdf/2103.15888v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O\!\left(n^{3/4}\sqrt\kappa\,(1+a)\ln^2(2+\kappa)\right).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** Divide every returned gradient by $\beta$ to simulate $\bar f=f/\beta$ without changing component-call counts. The normalized strong-concavity parameter is $1/\kappa$. For $\kappa\ge\sqrt n$, set regularization $1/\sqrt n$, obtaining work $O(n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa))$ from the source formula. Full gradients and residual checks each cost $n$ component calls; $1+a$ retains at least one outer iteration. The source theorem directly controls $\mathbb E\|\nabla\Phi(\widehat x)\|_2^2$ and worst-instance expected work. Set its internal tolerance to $\varepsilon$ without converting it to a fixed-budget probability guarantee.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Appendix I; (67); pdf pages: 30

Use the verified gradient-only SVRG implementation. Full average gradients and full residual checks each cost $n$ component calls.

**Source location.** [3](https://arxiv.org/pdf/2103.15888v1) theorem: Theorem 4.1; Corollary 4.1; (28); Appendix D.4, (128); pdf pages: 12; 13; 42

Normalize by the smoothness constant while retaining $\log^2(2+\kappa)$ explicitly. Expected cost and the mean-square guarantee use the source result directly; the fixed-probability guarantee requires Markov's inequality and fixed-budget truncation.

The original complexity expression and key conversion steps were checked. The entire internal-solver analysis was not independently reproved line by line.

### B8 - Decoupling at condition number one and finite-sum variance reduction.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O(n+\sqrt n\,a).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O(n+\sqrt n\,a).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** If $\kappa=1$, mean-square average smoothness, strong concavity of the average, and exact dual initialization imply $\Phi(x)=f(x,0)$. Only the average function must decouple. The source finite-sum variance-reduced method gives a fixed call cap $O(n+\sqrt n\,a)$ with randomized component sampling. Run directly at mean-square tolerance $\varepsilon$. The native guarantee is the target, and the fixed cap also bounds expected calls. No Markov conversion or truncation is needed.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Proposition 4; Appendix G; pdf pages: 24; 25

Under $\kappa=1$ and exact dual initialization, the source proves $\Phi(x)=f(x,0)$. This identity need not hold for each component separately.

The mean-square view uses the native guarantee directly. Fixed success probability requires only constant-factor tightening of the internal tolerance.

### B9 - Embedding an arbitrary-randomized finite-sum lower bound with an independent strongly concave quadratic term

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Explicit instance embedding from a lower bound for arbitrary randomized algorithms, without substituting a zero-respecting lower bound.

$$
N^\star\ge\Omega(n+\sqrt n\,a).
$$

**Sources.** [2](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\ge\Omega(n+\sqrt n\,a).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** For the source finite-sum hard instance $g_i(x)$, define $f_i(x,y)=g_i(x)-(\mu_y/2)\|y\|_2^2$. This embedding preserves the smoothness bound, initial primal gap, and reduced objective, and makes the dual optimum zero for every $x$. One component joint-gradient query is simulated by one source query. The source result applies directly when $n\ge1024$. For $2\le n<1024$, set $k=\lceil1024/n\rceil$ and average the $kn$ source components in equal groups. Each target query costs $k\le512$ source queries, losing only a universal constant. Dimension may grow with the budget; queries, component selection, and unqueried outputs have no span restriction. If expected calls are at most $Q$, truncate at $\lceil6Q\rceil$ calls. The mean-square guarantee bounds the probability of error exceeding $\sqrt6\varepsilon$ by $1/6$. Adding timeout probability at most $1/6$ gives the source fixed-budget success guarantee. Retain the corresponding constant tightening of the source accuracy window.

**Source location.** [2](https://arxiv.org/pdf/2609.00045v3) theorem: Theorem 3.1; Appendix C, (112)–(113); Appendix F.1–F.3, (302)–(305); pdf pages: 4; 5; 26; 50

The explicit native lower bound directly covers $n\ge1024$. The extension to $2\le n<1024$ uses averaging over equal-sized groups, with at most $512$ source queries per target query.

Adding an independent strongly concave dual quadratic preserves the model, primal initial gap, and exact dual initialization.

### B10 - Identical-component embedding of the unrestricted randomized NC–SC lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Explicit instance embedding from a lower bound for arbitrary randomized algorithms, without substituting a zero-respecting lower bound.

$$
N^\star\ge\Omega(\sqrt\kappa\,a).
$$

**Sources.** [4](https://arxiv.org/pdf/2610.00229v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\ge\Omega(\sqrt\kappa\,a).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** Set all $n$ components equal to one exact-gradient NC-SC hard function. Average smoothness and exact dual initialization are preserved. Component indices reveal nothing, and each query equals one source joint-gradient call. The unrestricted randomized source lower bound gives $\Omega(\sqrt\kappa\,a)$ with its condition-number threshold and nontrivial accuracy window. To convert expected work and a mean-square guarantee to the source fixed budget, truncate at six times the expected budget and use source tolerance $\sqrt6\varepsilon$. The two failure probabilities are each at most $1/6$. Tighten the sufficient constant in the accuracy window accordingly.

**Source location.** [4](https://arxiv.org/pdf/2610.00229v2) theorem: Definitions 3.1–3.3; Theorem 3.4; Corollary 3.5; Sections 5.5–5.6; pdf pages: 6; 7; 8; 14

Set every component equal to one hard payoff. One component-gradient call then exactly simulates one source full joint-gradient call.

Retain the source condition-number threshold, nontrivial-accuracy window, and worst-case quantifier allowing finite dimension to grow with the budget.

### B11 - Randomized recursive proximal difference algorithm, RPDA

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O\!\left(\sqrt n\,\kappa a+n\ell_R\right).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O\!\left(\sqrt n\,\kappa a+n\ell_R\right).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** RPDA is a specific randomized algorithm. Its updates are zero-respecting, so it also belongs to the larger algorithm class allowed here. A full gradient costs $n$ component calls; a two-point difference for the same component costs two calls. Counts include initialization, main iterations, and final refinement, and $\ell_R=1+\log(2+\kappa)+\log(2+(1+\kappa)^2a)$ records precisely these logarithmic overheads. Run the algorithm with internal mean-square tolerance $\eta=\varepsilon/\sqrt3$. Markov's inequality gives $\Pr(\|\nabla\Phi(\widehat x)\|_2>\varepsilon)\le\eta^2/\varepsilon^2=1/3$. The source algorithm already has a fixed call cap, so no runtime truncation is required.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorem 3; Algorithm 1; Appendix H, (49)–(50), H.6; pdf pages: 6; 8; 25; 26; 30

The admissible algorithm class contains the original RPDA, so its existence upper bound remains valid. Retain its native mean-square guarantee and fixed call count separately.

The mean-square guarantee directly uses tolerance $\varepsilon$. The fixed-budget probability guarantee uses $\varepsilon/\sqrt3$, without an additional work-truncation step.

### B12 - Randomized recursive proximal difference algorithm, RPDA

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O\!\left((n+\kappa^2)(1+a+\ell_R)\right).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O\!\left((n+\kappa^2)(1+a+\ell_R)\right).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** RPDA is a specific randomized algorithm. Its updates are zero-respecting, so it also belongs to the larger algorithm class allowed here. A full gradient costs $n$ component calls; a two-point difference for the same component costs two calls. Counts include initialization, main iterations, and final refinement, and $\ell_R=1+\log(2+\kappa)+\log(2+(1+\kappa)^2a)$ records precisely these logarithmic overheads. Run the algorithm with internal mean-square tolerance $\eta=\varepsilon/\sqrt3$. Markov's inequality gives $\Pr(\|\nabla\Phi(\widehat x)\|_2>\varepsilon)\le\eta^2/\varepsilon^2=1/3$. The source algorithm already has a fixed call cap, so no runtime truncation is required.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Theorem 3; Algorithm 1; Appendix H, (49)–(50), H.6; pdf pages: 6; 8; 25; 26; 30

The admissible algorithm class contains the original RPDA, so its existence upper bound remains valid. Retain its native mean-square guarantee and fixed call count separately.

The mean-square guarantee directly uses tolerance $\varepsilon$. The fixed-budget probability guarantee uses $\varepsilon/\sqrt3$, without an additional work-truncation step.

### B13 - Catalyst with gradient-based SVRG inner iterations.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O\!\left(n^{3/4}\sqrt\kappa\,(1+a)\ln^2(2+\kappa)\right).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1) [3](https://arxiv.org/pdf/2103.15888v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O\!\left(n^{3/4}\sqrt\kappa\,(1+a)\ln^2(2+\kappa)\right).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** Divide every returned gradient by $\beta$ to simulate $\bar f=f/\beta$ without changing component-query counts. The normalized strong-concavity parameter is $1/\kappa$. When $\kappa\ge\sqrt n$, choose regularization $1/\sqrt n$; the source bound gives work $O(n^{3/4}\sqrt\kappa(1+a)\log^2(2+\kappa))$. Charge $n$ component calls for every full gradient and residual check; $1+a$ ensures at least one outer iteration. Set internal mean-square tolerance $\eta=\varepsilon/\sqrt6$ and let $B(\eta)$ bound expected calls uniformly, including initialization and checks. Truncate at $N=\max\{1,\lceil6B(\eta)\rceil\}$ calls and return a fixed feasible point on timeout. By a union bound, error or timeout has probability at most $1/6+1/6=1/3$. No independence is needed, and only a constant factor is lost.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Appendix I; (67); pdf pages: 30

Use the verified gradient-only SVRG implementation. Full average gradients and full residual checks each cost $n$ component calls.

**Source location.** [3](https://arxiv.org/pdf/2103.15888v1) theorem: Theorem 4.1; Corollary 4.1; (28); Appendix D.4, (128); pdf pages: 12; 13; 42

Normalize by the smoothness constant while retaining $\log^2(2+\kappa)$ explicitly. Expected cost and the mean-square guarantee use the source result directly; the fixed-probability guarantee requires Markov's inequality and fixed-budget truncation.

The original complexity expression and key conversion steps were checked. The entire internal-solver analysis was not independently reproved line by line.

### B14 - Decoupling at condition number one and finite-sum variance reduction.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** Randomized witness

**Algorithm-scope qualification.** The recorded RPDA, SVRG, or decoupled finite-sum methods actually sample components randomly. Guarantee conversion does not remove this randomness.

$$
N^\star\le O(n+\sqrt n\,a).
$$

**Sources.** [1](https://arxiv.org/pdf/2610.04944v1)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\le O(n+\sqrt n\,a).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** When $\kappa=1$, mean-square average smoothness, strong concavity of the average function, and exact dual initialization imply $\Phi(x)=f(x,0)$. This concerns the average function only; individual components need not decouple. The source finite-sum variance-reduced method gives a deterministic call cap $O(n+\sqrt n\,a)$, while component sampling remains randomized. Run it at internal mean-square tolerance $\eta=\varepsilon/\sqrt3$. Markov's inequality yields $\Pr(\|\nabla\Phi(\widehat x)\|_2>\varepsilon)\le\eta^2/\varepsilon^2=1/3$. Its existing fixed call cap requires no truncation.

**Source location.** [1](https://arxiv.org/pdf/2610.04944v1) theorem: Proposition 4; Appendix G; pdf pages: 24; 25

Under $\kappa=1$ and exact dual initialization, the source proves $\Phi(x)=f(x,0)$. This identity need not hold for each component separately.

The mean-square view uses the native guarantee directly. Fixed success probability requires only constant-factor tightening of the internal tolerance.

### B15 - Embedding an arbitrary-randomized finite-sum lower bound with an independent strongly concave quadratic term

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Explicit instance embedding from a lower bound for arbitrary randomized algorithms, without substituting a zero-respecting lower bound.

$$
N^\star\ge\Omega(n+\sqrt n\,a).
$$

**Sources.** [2](https://arxiv.org/pdf/2609.00045v3)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\ge\Omega(n+\sqrt n\,a).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** For a source finite-sum hard instance $g_i(x)$, define $f_i(x,y)=g_i(x)-(\mu_y/2)\|y\|_2^2$. This preserves smoothness, the initial primal gap, and the reduced objective, and gives dual optimum zero for every $x$. One component joint-gradient query is simulated by one source query. The source result applies directly when $n\ge1024$. For $2\le n<1024$, let $k=\lceil1024/n\rceil$ and average the $kn$ source components in equal groups. Each target query uses $k\le512$ source calls, costing only a universal constant factor. Dimension may grow with the budget; queries, component choices, and unqueried outputs have no span restriction. Exact simulation preserves the fixed budget and instancewise success probability, yielding the $\Omega(n+\sqrt n\,a)$ lower bound without additional logarithmic loss.

**Source location.** [2](https://arxiv.org/pdf/2609.00045v3) theorem: Theorem 3.1; Appendix C, (112)–(113); Appendix F.1–F.3, (302)–(305); pdf pages: 4; 5; 26; 50

The explicit native lower bound directly covers $n\ge1024$. The extension to $2\le n<1024$ uses averaging over equal-sized groups, with at most $512$ source queries per target query.

Adding an independent strongly concave dual quadratic preserves the model, primal initial gap, and exact dual initialization.

### B16 - Identical-component embedding of the unrestricted randomized NC–SC lower bound.

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** All randomized adaptive algorithms

**Algorithm-scope qualification.** Explicit instance embedding from a lower bound for arbitrary randomized algorithms, without substituting a zero-respecting lower bound.

$$
N^\star\ge\Omega(\sqrt\kappa\,a).
$$

**Sources.** [4](https://arxiv.org/pdf/2610.00229v2)

**Conditions.** Every condition in the eight-axis specification and associated regime must hold jointly. Sufficient constants from different theorems are not assumed identical.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**N component.**

$$
N^\star\ge\Omega(\sqrt\kappa\,a).
$$

**Constants.** Use the source theorem’s universal constants except where derivative order or structural budgets are explicitly fixed. Unspecified sufficient thresholds remain symbolic.

**Derivation.** Set all $n$ components equal to one exact-gradient NC-SC hard function. Average smoothness and exact dual initialization are unchanged, indices reveal nothing, and each query is one source joint-gradient call. The unrestricted randomized source lower bound yields $\Omega(\sqrt\kappa\,a)$ with its condition-number threshold and accuracy window. Simulation preserves the fixed call cap, output, and $2/3$ success probability; it uses no condition-number lower bound restricted to zero-respecting algorithms.

**Source location.** [4](https://arxiv.org/pdf/2610.00229v2) theorem: Definitions 3.1–3.3; Theorem 3.4; Corollary 3.5; Sections 5.5–5.6; pdf pages: 6; 7; 8; 14

Set every component equal to one hard payoff. One component-gradient call then exactly simulates one source full joint-gradient call.

Retain the source condition-number threshold, nontrivial-accuracy window, and worst-case quantifier allowing finite dimension to grow with the budget.

### B17 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B18 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

### B19 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B20 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted expected rms

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

### B21 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B22 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $1<\kappa\le\sqrt n$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

### B23 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B24 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted fixed probability

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge\max\{a_\star,a_{\rm U06}\}$, $n\ge2$, and $\kappa>\sqrt n$ and $\kappa\ge\kappa_0$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [5](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Qihao Zhou. Near-Optimal Complexity of Finite-Sum Nonconvex-Strongly-Concave Minimax Optimization. 2026. arXiv:2610.04944v1, 2026-10-04.

https://arxiv.org/pdf/2610.04944v1

[2] Yuxing Peng; Zhiqing Tang; Weijia Jia. Dense Weak Hiding: Closing Complexity Gaps in Nonconvex and PL Finite-Sum Optimization under Individual Smoothness. 2026. arXiv:2609.00045v3.

https://arxiv.org/pdf/2609.00045v3

[3] Siqi Zhang; Junchi Yang; Cristóbal Guzmán; Negar Kiyavash; Niao He. The Complexity of Nonconvex-Strongly-Concave Minimax Optimization. 2021. arXiv:2103.15888v1.

https://arxiv.org/pdf/2103.15888v1

[4] Wendao Wu; Haihan Zhang; Chenheng Zhang; Yanyi Li; Chunyuan Zheng; Cong Fang; Haoxuan Li; Zhouchen Lin. Sharp Fresh-Gradient Complexity of Nonconvex--Strongly-Concave Minimax Optimization. 2026. arXiv:2610.00229v2, 2026-10-19.

https://arxiv.org/pdf/2610.00229v2

[5] Colombo_U06. Unrestricted Randomized Complexity of Finite-Sum Nonconvex--Strongly-Concave Minimax Optimization. NCSC_Unrestricted_Randomized_Paper.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf
