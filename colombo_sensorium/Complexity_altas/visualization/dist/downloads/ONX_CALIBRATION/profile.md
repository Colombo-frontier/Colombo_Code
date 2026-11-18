# Binary sequential calibration with arbitrary causal randomized predictors

**Setting ID.** `ONX_CALIBRATION`

Online learning and bandits

Each round, the predictor outputs a probability while the environment simultaneously selects a binary outcome. Both may use the past, but the environment cannot observe the current realized prediction first. The objective is standard cumulative absolute calibration error.

**Status.** Polynomial gap present

**TASK tags.** formulation: Onx cal polytime; formulation: Onx cal unrestricted; task family: Online bandit

**MODEL tags.** structure: Binary outcomes

**ORACLE tags.** interface family: Simultaneous binary outcome; operation: Simultaneous binary outcome; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** adaptivity: Causal protocol; randomization: Private randomness allowed

**OUTPUT tags.** certificate: No additional output certificate required; object: Online trajectory

**METRIC tags.** criterion: Absolute calibration

**GUARANTEE tags.** mode: Expectation; randomness: Algorithm private seed; randomness: Oracle samples

**RESOURCE tags.** accounting: Joint coordinates retained; measure: Native feedback; measure: Rounds; setup: Initialization included

## 1. Setting specification

### Task

Each round, the predictor outputs a probability while the environment simultaneously selects a binary outcome. Both may use the past, but the environment cannot observe the current realized prediction first. The objective is standard cumulative absolute calibration error.

### Admissible model

The outcome $y_t\in\{0,1\}$ and prediction $p_t\in[0,1]$ are generated simultaneously each round. The outcome strategy may use all past predictions and outcomes, but not the realization of the current prediction or the current private seed.

### Oracle interface

The predictor chooses $p_t\in[0,1]$ while the adversary simultaneously chooses $y_t\in\{0,1\}$.

Both players may use past predictions and outcomes. When choosing $y_t$, the adversary cannot observe the current realized random prediction $p_t$.

The quantity $p_t,y_t$ is revealed after both parties act. No true conditional mean or other privileged prediction interface is supplied.

Received feedback may be stored and reused in computation. Unrevealed information cannot be requested from past rounds, and consumed random samples cannot receive additional queries. Current-round exceptions are limited to the explicitly supplied full-function access or same-sample two-point interface.

### Output

Output a probability $p_t\in[0,1]$ each round. Evaluation uses the realized prediction and outcome trajectories; predictions cannot be rewritten after the game ends.

### Loss or accuracy criterion

$$
\operatorname{Cal}_T=\sum_{p\in\{p_1,\ldots,p_T\}}\left|\sum_{t:p_t=p}(y_t-p_t)\right|.
$$

The outer sum runs only over distinct prediction probabilities actually used. The criterion is neither per-round absolute error nor an approximation after binning.

### Resource accounting

There are $T$ predictions and $N=T$ binary outcome observations. Computation is accounted for separately. An information-theoretic existence result does not itself give an efficient algorithm.

Exploration, initialization, and system identification all consume the stated online budget. Queries, arithmetic, communication rounds or bits, and memory remain joint resources. No arithmetic or bit-complexity optimality is asserted.

### Algorithm views and success guarantees

#### Randomized unrestricted computation

$$
\inf_{\mathcal{A}}\ \sup_{\mathcal{E}\ \text{\text{nonanticipating}}}\ \mathbb{E}_{\mathcal{A},\mathcal{E}}\!\left[\operatorname{Cal}_T\right].
$$

Expectation includes both players' randomness; the target is neither a pathwise nor a high-probability calibration guarantee.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Control $\mathbb{E}[\operatorname{Cal}_T]$ against every admissible outcome strategy, with expectation over both predictor and outcome-strategy randomness. Choose an admissible predictor first, then take the worst case over environment strategies.

#### Randomized polynomial time

$$
\inf_{\mathcal{A}}\ \sup_{\mathcal{E}\ \text{\text{nonanticipating}}}\ \mathbb{E}_{\mathcal{A},\mathcal{E}}\!\left[\operatorname{Cal}_T\right].
$$

Expectation includes both players' randomness; the target is neither a pathwise nor a high-probability calibration guarantee.

Per-round and total computation must obey the declared polynomial-time restriction. An existence-only minimax policy with unlimited computation is not an admissible upper-bound witness.

Private randomization is allowed, with the seed independent of the fixed instance and future external samples. Internal arithmetic, memory, linear spans, and iteration forms are unrestricted except for the stated computation, communication, privacy, and within-round interaction limits.

Control $\mathbb{E}[\operatorname{Cal}_T]$ against every admissible outcome strategy, with expectation over both predictor and outcome-strategy randomness. Choose an admissible predictor first, then take the worst case over environment strategies.

## 2. Notation and parameters

$T$: Online rounds within the fixed evaluation horizon. **Domain:** $T\in\mathbb N,\ T\ge1$.

The information protocol fixes feedback count per round. The horizon $T$ is not an independent cumulative scalar-query count.

$p_t,y_t$: Probability forecast and binary outcome at round $t$ **Domain:** $p_t\in[0,1],\ y_t\in\{0,1\}$.

The current outcome strategy cannot first observe the realized random prediction. Both choices are revealed after they are made.

$\mathcal P_T$: Set of distinct prediction values actually used during an interaction **Domain:** A finite set with at most T elements.

The set is $\mathcal P_T=\{p_1,\ldots,p_T\}$. Exactly equal numerical values belong to the same group.

$\operatorname{Cal}_T$: Absolute calibration error grouped by the exact forecast values **Domain:** Real number in $[0,T]$.

$\operatorname{Cal}_T=\sum_{p\in\mathcal P_T}|\sum_{t:p_t=p}(y_t-p_t)|$.

$\mathcal E$: Outcome-generation policy that cannot observe the current realized prediction **Domain:** Causal environment policy.

The strategy may depend on all previous predictions and outcomes and may also randomize.

$\mathcal A$: Learning policies satisfying the specified information, computation, and privacy restrictions **Domain:** A measurable causal policy.

Actions may depend only on revealed information and the private seed. Additional restrictions are governed by the algorithm protocol in this profile.

$t$: Interaction-time index **Domain:** $t\in\{1,\ldots,T\}$.

$\mathbb E$: Mean operator **Domain:** Expectation over the specified random variables.

Expectation covers the joint randomness of the predictor and admissible environment. Absolute values and grouping by prediction value precede expectation.

$\log,\log_2$: Natural and binary logarithms **Domain:** Function on the positive real axis.

$\log x=\ln x$, $\log_2x=\log x/\log2$.

$c,C$: Positive constant in the bound without an assigned numerical value **Domain:** Positive real number.

Constants apply only under the associated bound’s conditions and fixed-parameter convention. Unspecified theorem constants are not treated as additional algorithm inputs.

$O,\Omega,\widetilde O,\widetilde\Omega$: Asymptotic upper and lower bounds, including explicitly permitted logarithmic suppression. **Domain:** Asymptotic comparison notation.

The result applies only in the regime declared for that bound. Tilde notation hides only its stated logarithms and fixed-parameter dependencies, never additional polynomial parameter factors.

$N$: Cumulative observations counted according to the declared feedback type. **Domain:** Nonnegative integer or integer-valued stopping time.

$N=T$, the number of binary outcomes observed after the actions.

$\gamma_{\mathrm{cal}}$: Fixed positive exponent correction in the efficient calibration theorem **Domain:** $0<\gamma_{\mathrm{cal}}<1$.

This is the quantity $\epsilon_{AB}$ in source Theorem 1, whose existence follows from the sign-preservation bound in Lemma 3. It is not a tunable accuracy, privacy parameter, or numerically known constant in this profile.

$T^{2/3-\gamma_{\mathrm{cal}}/18}$: The calibration-error exponent of this efficient algorithm. **Domain:** Asymptotic rate guaranteed by the theorem.

The source does not supply a numerical decimal exponent that can be substituted here.

## 3. Complexity bracket

### Compared quantities

#### Q1 - native performance

**View.** Randomized unrestricted computation

$$
\operatorname{Cal}_T=\sum_{p\in\{p_1,\ldots,p_T\}}\left|\sum_{t:p_t=p}(y_t-p_t)\right|.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

#### Q2 - native performance

**View.** Randomized polynomial time

$$
\operatorname{Cal}_T=\sum_{p\in\{p_1,\ldots,p_T\}}\left|\sum_{t:p_t=p}(y_t-p_t)\right|.
$$

**Scope.** Compare only within this setting and the explicit regime, retaining multiple objectives and time normalization.

**Optimization direction.** minimize

### R1 - SUPPORTED

**Region.** Assume $T\ge1$ and standard absolute calibration. The environment cannot observe the current realized prediction.

**Views.** Randomized unrestricted computation

**Quantity.** Q1

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Polynomial gap

**Lower bound.** B2

$$
\Omega(T^{0.54389})
$$

**Upper bound.** B1

$$
O(T^{0.662942288})
$$

### R2 - SUPPORTED

**Region.** The source fixes $\gamma_{\mathrm{cal}}>0$ and gives total computation $O(T^{7/2}\log^2T)$.

**Views.** Randomized polynomial time

**Quantity.** Q2

**Resource.** Fixed native online budget, with computational, communication, and privacy resources retained separately.

**Status.** Polynomial gap

**Lower bound.** B4

$$
\Omega(T^{0.54389})
$$

**Upper bound.** B3

$$
O(\log^2T\;T^{2/3-\gamma_{\rm cal}/18})
$$

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Retain the specified feedback type, sample coupling, public information, and environment permissions.

### B1 - A minimax reduction from strengthened sign-preserving games to calibration.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized unrestricted computation

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(T^{0.662942288}\right)
$$

**Sources.** [2](https://arxiv.org/pdf/2610.07623v2)

**Conditions.** The criterion is $T\ge1$: expected standard cumulative absolute calibration error. The adversary cannot foresee the current realized randomized prediction.; The preprint statement has been read. Its minimax reduction does not by itself implement a polynomial-time predictor.

**Source location.** [2](https://arxiv.org/pdf/2610.07623v2) Theorem 1.1 p.2; Section 6 explicit feasible tuple and Appendix A certificate

### B2 - Hard outcome process for the strengthened sign-preservation game

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized unrestricted computation

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(T^{0.54389}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2406.13668v1)

**Conditions.** Use a randomized outcome adversary fixed before interaction, targeting expected standard absolute calibration error.

**Source location.** [1](https://arxiv.org/pdf/2406.13668v1) Theorem 1.3, PDF p.3 (printed p.2)

### B3 - A polynomial-time calibrator from the efficient sign-preserving reduction.

**Admission.** Included in the bracket

**Direction.** upper

**View.** Randomized polynomial time

**Witness or lower-bound scope.** Randomized witness

$$
O\!\left(\log^2T\;T^{,2/3-\gamma_{\mathrm{cal}}/18}\right)
$$

**Sources.** [3](https://arxiv.org/pdf/2607.12928v1)

**Conditions.** The quantity $\gamma_{\mathrm{cal}}>0$ is a fixed exponent correction from the sign-preserving reduction, corresponding to $\epsilon_{AB}$ in the source. It is neither an accuracy parameter nor a privacy parameter.; Total arithmetic work is $O(T^{7/2}\log^2T)$. The explicit exponent $0.662942288$ from another reduction does not automatically apply to this efficient algorithm.

**Source location.** [3](https://arxiv.org/pdf/2607.12928v1) Theorem 1, PDF p.2

### B4 - Hard outcome process for the strengthened sign-preservation game

**Admission.** Included in the bracket

**Direction.** lower

**View.** Randomized polynomial time

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega\!\left(T^{0.54389}\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2406.13668v1)

**Conditions.** The hard outcome process is randomized before interaction. The metric is the specified expected standard calibration error, and the predictor may use private randomness.

**Derivation.** The source lower bound covers every causal randomized forecaster and hence its polynomial-time subclass. This transfer does not require making the hard process computationally solvable by the algorithm.

**Source location.** [1](https://arxiv.org/pdf/2406.13668v1) Theorem 1.3, PDF p.3 (printed p.2)

## References

[1] Yuval Dagan; Constantinos Daskalakis; Maxwell Fishelson; Noah Golowich; Robert Kleinberg; Princewill Okoroafor. Improved bounds for calibration via stronger sign preservation games. 2024. 2406.13668v1.

https://arxiv.org/pdf/2406.13668v1

[2] Eric Dai; Maxwell Fishelson. Explicit Asymptotic Bounds for Sequential Calibration Beyond T^(2/3). 2026. 2610.07623v2.

https://arxiv.org/pdf/2610.07623v2

[3] Zihan Zhang. Efficient Sequential Calibration with O(T^(2/3-epsilon)) Error Bound. 2026. 2607.12928v1.

https://arxiv.org/pdf/2607.12928v1
