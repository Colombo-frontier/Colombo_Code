# Finite-sum nonconvex-strongly-concave minimax optimization with individually smooth components

**Setting ID.** `CV_S_FS_NCSC_IS`

Minimax optimization

Unrestricted randomized component-gradient complexity is matched up to logarithmic factors under exact dual initialization and strong concavity only of the average.

**Status.** Logarithmic gap

**TASK tags.** solution concept: Reduced gradient stationarity; task family: Minimax

**MODEL tags.** convexity: Nonconvex strongly concave; smoothness: Individual smoothness

**ORACLE tags.** feedback quality: Exact; operation: Component joint gradient; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared; scalar derivative order: Scalar-function first derivative

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**GUARANTEE tags.** aggregation: Second moment of the complete error; mode: Expectation; mode: Probability; quantifier: Algorithm before instance; randomness: Algorithm private seed

**RESOURCE tags.** budget: Fixed worst-case budget; budget: Worst-instance expected cost; measure: N component gradient

## 1. Setting specification

### Task

Find first-order stationarity of the true reduced objective $\Phi(x)=\max_{y\in\mathbb R^{d_y}} f(x,y)$, where $f(x,y)=n^{-1}\sum_{i=1}^n f_i(x,y)$, on unconstrained Euclidean spaces.

### Admissible model

Every component obeys the individual smoothness condition $\|\nabla f_i(z)-\nabla f_i(z^\prime)\|_2\le\beta\|z-z^\prime\|_2$ globally, with the same public beta.

Each component is continuously differentiable. Only the average dual function $f(x,\cdot)$ is required to be mu_y-strongly concave; individual components may be nonconcave in y. Thus the dual optimizer is unique and $\nabla\Phi(x)=\nabla_x f(x,y^\star(x))$.

The public initialization is $(0,0)$ with exact dual promise $y^\star(0)=0$ and primal gap $\Phi(0)-\inf\Phi\le\Delta$. The dimensions and n,beta,mu_y,Delta are public. Component gradients, query norms and dual optimizers away from the initial point need not be bounded.

### Oracle interface

At an adaptively selected index i and arbitrary joint point, receive only the exact full joint gradient $\nabla f_i(x,y)$. The same index always identifies the same fixed component. One component call costs one unit and a full mean gradient costs n. There are no function values, Hessians, reduced gradients or free dual maximizers in this interface.

The source lower bound is proved for the stronger packet $(f_i,\nabla f_i)$ and therefore applies to this gradient-only interface by discarding the extra value. The upper algorithms use only gradients.

### Output

Return any measurable primal point $\widehat x$, possibly unqueried and with unrestricted coordinate support. No dual point or certificate is required.

### Loss or accuracy criterion

The error is $\|\nabla\Phi(\widehat x)\|_2$. The expected-squared criterion and constant-probability criterion are separate views with separate resource semantics.

### Resource accounting

Count every selected component joint-gradient call, including initialization and repetition. In the expected-RMS view optimize worst-instance expected work with almost sure termination. In the probability view require a fixed cap on every path. Internal arithmetic and memory are free. The matched quantities take a worst case over finite dimensions.

### Algorithm views and success guarantees

#### Unrestricted randomized / Expected RMS and expected work

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

A private random seed independent of the fixed instance is permitted.

$$
\forall I:\ \mathbb E\|\nabla\Phi(\widehat x)\|_2^2\le\varepsilon^2
$$

The instance is fixed before the private seed. Accuracy and expected work are each worst-case over individual instances.

**Budget convention.** worst_instance_expected_calls

#### Unrestricted randomized / Constant probability and fixed budget

Queries, stopping decisions and outputs are arbitrary measurable functions of the observed history and public inputs. No linear-span or zero-respecting restriction is imposed. Internal exact-real computation and storage are uncharged.

A private random seed independent of the fixed instance is permitted.

$$
\forall I:\ \Pr(\|\nabla\Phi(\widehat x)\|_2\le\varepsilon)\ge2/3
$$

The query cap holds even on unsuccessful executions. Probability is over private randomness; the component oracle is exact.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$d_x$: Public primal dimension **Domain:** $d_x\in\mathbb N_{\ge1}$.

$d_y$: Public dual dimension **Domain:** $d_y\in\mathbb N_{\ge1}$.

$n$: Number of components **Domain:** $n\in\mathbb N_{\ge1}$.

$\beta$: IS component-gradient regularity upper bound **Domain:** $\beta>0$.

$\mu_y$: Strong concavity lower bound for the average dual problem **Domain:** $0<\mu_y\le\beta$.

$\Delta$: Initial reduced-objective gap **Domain:** $\Delta>0$.

$\kappa$: Condition ratio **Domain:** $\kappa\ge1$.

$\kappa=\beta/\mu_y$

$\varepsilon$: Reduced-gradient norm tolerance **Domain:** $\varepsilon>0$.

$a$: Dimensionless gap-to-accuracy scale **Domain:** $a>0$.

$a=\beta\Delta/\varepsilon^2$

$a_{\rm U06}$: Source sufficient small-accuracy threshold **Domain:** $a_{\rm U06}>0$ is the universal constant A_* in Theorem main.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

**View.** Unrestricted randomized / Expected RMS and expected work

$T^\star_{IS,\infty}$ for the linked guarantee and work convention

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\rm component}$; description: Expected total calls with expected squared residual.

#### Q2 - minimax metric resource quantity

**View.** Unrestricted randomized / Constant probability and fixed budget

$T^\star_{IS,\infty}$ for the linked guarantee and work convention

**Scope.** The union of the explicit parameter and dimension domains of the linked comparison regimes; each bound retains its own applicability conditions.

**Optimization direction.** minimize

**Resource contract.** expression: $N_{\rm component}$; description: Fixed total-call cap with probability at least 2/3.

### R1 - IS / Expected RMS and work / small condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $1\le\kappa\le\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Unrestricted randomized / Expected RMS and expected work

**Quantity.** Q1

**Resource.** Expected total calls with expected squared residual.

**Status.** Logarithmic gap

**Lower bound.** B2

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Upper bound.** B1

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R2 - IS / Expected RMS and work / large condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $\kappa>\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Unrestricted randomized / Expected RMS and expected work

**Quantity.** Q1

**Resource.** Expected total calls with expected squared residual.

**Status.** Logarithmic gap

**Lower bound.** B4

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Upper bound.** B3

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R3 - IS / Constant probability and fixed budget / small condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $1\le\kappa\le\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Unrestricted randomized / Constant probability and fixed budget

**Quantity.** Q2

**Resource.** Fixed total-call cap with probability at least 2/3.

**Status.** Logarithmic gap

**Lower bound.** B6

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Upper bound.** B5

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

### R4 - IS / Constant probability and fixed budget / large condition

**Region.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $\kappa>\sqrt n$. Exact dual initialization is imposed. Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

**Views.** Unrestricted randomized / Constant probability and fixed budget

**Quantity.** Q2

**Resource.** Fixed total-call cap with probability at least 2/3.

**Status.** Logarithmic gap

**Lower bound.** B8

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Upper bound.** B7

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Gap or comparison.** Only the logarithmic overheads of the cited upper algorithms remain.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Dimension conditions.** Upper algorithms apply to every finite pair of block dimensions. Lower bounds are worst cases over finite dimensions and can require exponential growth with the serialized path length, not merely polynomial dimension. In equation optimization-dimension the source block dimension is $D_0=\lceil32(8K_*+8)a_*^{-2}\sum_{t=0}^{H_0}n^t\rceil$, where $a_*=1/8600000$, $K_*=\lfloor c_{\rm inf}nH_0\rfloor$, $c_{\rm inf}=(a_*^2/2)^2/(4e)$, and $H_0=M_0m_0$ is the construction serial depth. The primal and dual blocks are assembled from this source as in Theorem distributional-hardness and Section parameter calibration. No fixed-dimensional or arithmetic-runtime matching conclusion follows.

### B1 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted randomized / Expected RMS and expected work

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $1\le\kappa\le\sqrt n$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B2 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted randomized / Expected RMS and expected work

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $1\le\kappa\le\sqrt n$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

### B3 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted randomized / Expected RMS and expected work

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $\kappa>\sqrt n$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B4 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted randomized / Expected RMS and expected work

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $\kappa>\sqrt n$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

### B5 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted randomized / Constant probability and fixed budget

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a\sqrt n\,\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $1\le\kappa\le\sqrt n$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B6 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted randomized / Constant probability and fixed budget

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a\sqrt n\,\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $1\le\kappa\le\sqrt n$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

### B7 - RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch

**Admission.** Included in the bracket

**Direction.** upper

**View.** Unrestricted randomized / Constant probability and fixed budget

**Witness or lower-bound scope.** Randomized witness

$$
\widetilde O(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $\kappa>\sqrt n$. Exact dual initialization is imposed.; The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equations main-complexity and two-regimes; Section upper and appendix upper-interfaces; verified labels: thm:main (line 252), eq:main-complexity (line 261), eq:two-regimes (line 281), sec:upper (line 609), sec:upper-interfaces (line 2354)

RPDA in the small-condition branch; Catalyst with a variance-reduced inner solver in the large-condition branch. Unrestricted randomized algorithms.

The upper analysis requires only AS and average dual strong concavity; IS implies AS with the same beta. For constant confidence, the source uses a stricter target and runtime truncation, not an unjustified transfer of the RMS guarantee to the fallback.

### B8 - Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation

**Admission.** Included in the bracket

**Direction.** lower

**View.** Unrestricted randomized / Constant probability and fixed budget

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega(n+a n^{3/4}\sqrt\kappa)
$$

**Sources.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf)

**Conditions.** $\beta,\Delta,\varepsilon>0$, $0<\mu_y\le\beta$, $a\ge a_{\rm U06}$, $n\ge1$, and $\kappa>\sqrt n$. Exact dual initialization is imposed.; The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

**Constants.** Constants are independent of n,beta,mu_y,Delta,epsilon and dimension.

**Logarithmic factors.** The tilde hides the polylogarithmic factors in the RPDA and Catalyst upper bounds, retained by the source theorem.

**Source location.** [1](https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf) Theorem main; equation main-complexity; Theorem distributional-hardness; verified labels: thm:main (line 252), eq:main-complexity (line 261), thm:distributional-hardness (line 2024), eq:distributional-hardness (line 2032)

Orthogonal source recovery, quadratic saddle relays and globally smooth primal activation. All randomized adaptive component queries and arbitrary measurable outputs.

The hard family satisfies individual smoothness and average strong concavity but may have nonconcave components. Its enriched value-gradient lower bound also applies after deleting the value channel.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

## References

[1] Colombo_U06. Unrestricted Randomized Complexity of Finite-Sum Nonconvex--Strongly-Concave Minimax Optimization. NCSC_Unrestricted_Randomized_Paper.tex.

https://github.com/WU-Wendao/Colombo/blob/main/colombo_sensorium/Complexity_altas/data/sources/colombo/U06/manuscript.pdf
