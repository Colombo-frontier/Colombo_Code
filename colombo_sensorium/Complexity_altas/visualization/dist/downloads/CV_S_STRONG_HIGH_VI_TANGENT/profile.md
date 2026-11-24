# Higher-order strongly monotone variational inequalities on compact convex sets with tangent residual

**Setting ID.** `CV_S_STRONG_HIGH_VI_TANGENT`

Variational inequalities

Certified restart of a monotone full-jet solver and strong-monotonicity calibration of a random-frame family give scoped bounds for constrained tangent residuals. Constants depend on the fixed derivative order.

**Status.** Logarithmic gap; Bounds missing

**TASK tags.** solution concept: Constrained variational inequality; task family: Variational inequality

**MODEL tags.** monotonicity: Strong monotonicity

**ORACLE tags.** feedback quality: Exact; operation: Operator taylor jet; operator derivative order: Parameterized order p−1 (see exact operation binding); public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** randomization: Private randomness allowed; restriction: No additional span restriction explicitly imposed

**OUTPUT tags.** certificate: No additional output certificate required

**METRIC tags.** criterion: Tangential residual

**GUARANTEE tags.** aggregation: Per instance; mode: Probability; quantifier: Algorithm before instance

**RESOURCE tags.** budget: Fixed worst-case budget; measure: N operator jet

## 1. Setting specification

### Task

Solve $0\in F(x)+N_X(x)$ on a known compact convex set, measured by the original-domain tangent residual.

### Admissible model

Fix an integer $p\ge2$. Public inputs are $d\ge1$, a nonempty compact convex $X\subseteq\mathbb R^d$ with $\operatorname{diam}(X)\le D$, a feasible $x_0$, and $L_p,\mu,D,\varepsilon>0$.

The hidden operator is $C^{p-1}$ on an open neighborhood of $X$. On $X$, $\langle F(x)-F(y),x-y\rangle\ge\mu\|x-y\|_2^2$ and $\|D^{p-1}F(x)-D^{p-1}F(y)\|_{\rm op}\le L_p\|x-y\|_2$. The declared moduli are promises: actual strong monotonicity may exceed $\mu$ and actual derivative Lipschitz modulus may be smaller than $L_p$.

No bounds on lower derivatives, $\|F\|$, or a scalar potential are imposed. Compactness and continuity give a VI solution; strong monotonicity makes it unique. The solution can be a boundary point with nonzero $F$.

### Oracle interface

At any feasible $x\in X$, receive the exact complete operator jet $(F(x),DF(x),\ldots,D^{p-1}F(x))$. No values outside $X$ and no free resolvent of the unknown operator are available.

Projection onto the known $X$ and exact solves of models formed only from public geometry and returned Taylor coefficients are free internal operations. Adding a known affine regularization to a returned jet requires no extra information.

### Output

Return a feasible point $\widehat x\in X$, possibly unqueried. The upper witness additionally returns $n\in N_X(\widehat x)$ and an evaluated $F(\widehat x)$; this stronger certificate is not required of lower-bound algorithms.

### Loss or accuracy criterion

$r_{\rm tan}(x)=\operatorname{dist}(0,F(x)+N_X(x))$, with $N_X(x)=\{n:\langle n,z-x\rangle\le0\ \forall z\in X\}$. This is neither the weak Minty gap nor distance to the solution.

### Resource accounting

Count one unit for each complete jet query, including nested subproblem work, repeated points, restarts and the final certificate evaluation. The budget is a fixed cap on every execution, not expected work. The main minimax quantity takes the worst case over all finite dimensions and legal public sets and starts; dimension is supplied to the algorithm.

### Algorithm views and success guarantees

Arbitrary measurable adaptive policies and outputs are allowed, with an independent private random seed and no span, zero-respecting or tensor-update restriction. All queried points must be feasible. Exact arithmetic and storage are uncharged.

For every fixed admissible instance, $\Pr(r_{\rm tan}(\widehat x)\le\varepsilon)\ge2/3$. Only the algorithm seed is random. The deterministic upper witness succeeds on every instance.

**Budget convention.** fixed_worst_case_cap

## 2. Notation and parameters

$d$: Public ambient dimension **Domain:** $d\in\mathbb N_{\ge1}$.

$p$: Fixed operator-jet smoothness order **Domain:** $p\in\mathbb N,\ p\ge2$.

$L_p$: Lipschitz bound for derivative of order p-1 **Domain:** $L_p>0$.

$\mu$: Strong-monotonicity lower bound **Domain:** $\mu>0$.

$D$: Known domain diameter bound **Domain:** $D>0$.

$\varepsilon$: Tangent-residual tolerance **Domain:** $\varepsilon>0$.

$\kappa_D$: Diameter-normalized condition parameter **Domain:** $\kappa_D>0$.

$\kappa_D=L_pD^{p-1}/\mu$

$\theta$: Relative residual tolerance **Domain:** $\theta>0$.

$\theta=\varepsilon/(\mu D)$

$\alpha_p$: Condition exponent **Domain:** $\alpha_p>0$.

$\alpha_p=2/(3p-1)$

$\kappa_{0,p}$: Sufficient condition threshold in the source lower bound **Domain:** $\kappa_{0,p}>0$ depends only on p.

## 3. Complexity bracket

### Compared quantities

#### Q1 - minimax metric resource quantity

$$
T^\star_{{\rm rand},\infty}(\varepsilon;L_p,\mu,D)=\inf\{N:\exists\mathcal A\ \forall d,X,x_0,F,\ N_{\mathcal A}\le N\ \text{on every run},\ \Pr(r_{\rm tan}(\widehat x)\le\varepsilon)\ge2/3\}
$$

**Scope.** Worst case over finite dimensions and all admissible public compact domains and starts. The dimension is an algorithm input. Upper bounds hold for each finite dimension; a lower bound uses only its explicitly sufficient high-dimensional ball construction.

**Optimization direction.** minimize

This is a dimension-envelope, fixed-path-budget complexity. No averaging over instances, expected-work interpretation, or optimality in each fixed small dimension is implicit.

**Resource contract.** expression: $N_{\rm jet}$; description: Fixed worst-case cap on feasible complete-jet queries.

### R1 - All-parameter upper bound outside the matching lower window

**Region.** $p\ge2$ fixed and $L_p,\mu,D,\varepsilon>0$; either $\kappa_D<\kappa_{0,p}$ or $\theta>1/16$. All finite dimensions.

**Quantity.** Q1

**Resource.** Fixed worst-case cap on feasible complete-jet queries.

**Status.** Lower bound missing

**Lower bound.** No admitted bound for this comparison

**Upper bound.** B1

$$
O_p\!\left(1+\kappa_D^{\alpha_p}+\log_+(1/\theta)\right)
$$

**Gap or comparison.** No parameter-dependent lower bound is recorded outside the calibrated chain window; the upper bound remains valid.

### R2 - Condition-dominated relative-accuracy window

**Region.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)\le\kappa_D^{\alpha_p}$. For fixed $p$, take $m=\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor\ge2$. The lower bound holds on $X=B_2^d(D/2)$ with start zero whenever $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. Here $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$ for the fixed gate of 2609.13462v2, $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, and $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. Upper bounds hold in every finite dimension. The comparison quantity takes a worst case over finite dimensions.

**Quantity.** Q1

**Resource.** Fixed worst-case cap; the upper witness is deterministic.

**Status.** Optimal

**Lower bound.** B3

$$
\Omega_p(\kappa_D^{\alpha_p})
$$

**Upper bound.** B2

$$
O_p\!\left(1+\kappa_D^{\alpha_p}+\log_+(1/\theta)\right)
$$

**Gap or comparison.** $O_p(1)$: the explicit accuracy logarithm is at most the condition term and $\kappa_D\ge\kappa_{0,p}$.

### R3 - Smaller relative accuracy with a remaining logarithmic factor

**Region.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)>\kappa_D^{\alpha_p}$. For fixed $p$, take $m=\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor\ge2$. The lower bound holds on $X=B_2^d(D/2)$ with start zero whenever $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. Here $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$ for the fixed gate of 2609.13462v2, $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, and $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. Upper bounds hold in every finite dimension. The comparison quantity takes a worst case over finite dimensions.

**Quantity.** Q1

**Resource.** Fixed worst-case cap on feasible queries.

**Status.** Logarithmic gap

**Lower bound.** B5

$$
\Omega_p(\kappa_D^{\alpha_p})
$$

**Upper bound.** B4

$$
O_p\!\left(1+\kappa_D^{\alpha_p}+\log_+(1/\theta)\right)
$$

**Gap or comparison.** $O_p(1+\log_+(1/\theta)/\kappa_D^{\alpha_p})$. No matching lower bound for the additive accuracy logarithm is asserted.

## 4. Bounds and supporting evidence

The following conditions apply to every bound in this profile, in addition to each bound's stated region and algorithm scope.

**Oracle mapping.** Only feasible complete operator jets are queried; all nested calls and final evaluations are charged.

**Output mapping.** The target is the tangent residual for the original X. The upper witness returns an actual original-domain normal certificate; the lower bound permits arbitrary feasible outputs.

### B1 - Certified restart on the original compact domain

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_p\!\left(1+\kappa_D^{\alpha_p}+\log_+(1/\theta)\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.23557v1)

**Conditions.** $p\ge2$ fixed and $L_p,\mu,D,\varepsilon>0$; either $\kappa_D<\kappa_{0,p}$ or $\theta>1/16$.; All eight-axis contracts of this profile hold. The upper witness is deterministic; the lower class is unrestricted randomized with fixed success probability 2/3 and fixed pathwise query cap.

**Dimension conditions.** Every finite dimension.

**Constants.** Constants depend only on the fixed integer p and the once-fixed smooth gate. The threshold and sufficient dimension are explicit; no uniform claim as p grows is made.

**Derivation.** Theorem 5.1 of 2609.23557v1, with Assumptions 2.1--2.4, Algorithm 1 and Lemma 2.1, returns a feasible $u$ and an evaluated vector $v=F(u)+n$, $n\in N_X(u)$, with $\|v\|\le\eta$ in at most $C_p[1+(L_pR^p/\eta)^{\alpha_p}]$ complete-jet calls whenever $\|z-x^\star\|\le R$, where $\alpha_p=2/(3p-1)$. The constant $C_p$ depends only on fixed $p$.

The source writes its scale as the exact initial distance. A supplied upper bound $R$ is sufficient: choose its equation (8) with $\eta_0=(L_pR^{p-1})^{-1}$ and its inner tolerance with $R$. In the proof of Theorem 4.1, equations (11)--(13) use the initial distance only through the upper estimates $\|z-x^\star\|\le R$, $\sum_t\|e_t\|\le R$, $\|u_t-x^\star\|\le2R$ and $P_0\le6R^2/\eta_0$. The distance-energy and query-sum bounds in Lemma 5.1 and Theorem 5.1 then keep the same scale. Thus the subroutine requires no knowledge of the exact distance.

For the unique VI solution choose $n^\star=-F(x^\star)\in N_X(x^\star)$. Monotonicity of the normal cone and $\mu$-strong monotonicity give $\mu\|u-x^\star\|^2\le\langle F(u)+n,u-x^\star\rangle\le\|v\|\|u-x^\star\|$, hence $\|u-x^\star\|\le\|v\|/\mu$.

Set $R_j=D2^{-j}$, $z_0=x_0$, and $S=\max\{1,\lceil\log_2(\mu D/\varepsilon)\rceil\}$. At each $j=0,\ldots,S-1$, run the certified monotone solver on the same original set $X$, starting from $z_j$, with residual tolerance $\eta_j=\mu R_j/2$. Set $z_{j+1}=u_j$. The preceding inequality inductively proves $\|z_{j+1}-x^\star\|\le R_{j+1}$.

The last actual certificate obeys $\|v_{S-1}\|\le\mu D2^{-S}\le\varepsilon$. The final conclusion is therefore a tangent-residual certificate, not merely distance contraction. The normal cone remains $N_X$ throughout: there is no restriction to an intersected ball and no normal-cone transfer.

Every stage costs at most $C_p[1+2^{\alpha_p}\kappa_D^{\alpha_p}2^{-j\alpha_p(p-1)}]$, where $\kappa_D=L_pD^{p-1}/\mu$. Summing gives $C_p[S+2^{\alpha_p}\kappa_D^{\alpha_p}/(1-2^{-\alpha_p(p-1)})]$. For fixed $p\ge2$ this is $O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$, where $\theta=\varepsilon/(\mu D)$ and $\log_+(t)=\max\{0,\log t\}$. The cost includes all inner jet evaluations and all returned certificates.

All queried centers and model solutions in source Algorithms 1--3 are in $X$, with projection onto the known $X$. A regularized operator $F+\eta^{-1}(\cdot-z)$ uses one original jet per query and has the same Lipschitz bound on $D^{p-1}$ for $p\ge2$. Source Assumptions 2.3--2.4 impose their inequalities on $X$; the neighborhood regularity used here supplies the same Taylor data. The bound is dimension-independent; constants are not asserted uniform when $p$ grows.

**Local argument.** CV_S_STRONG_HIGH_VI_TANGENT__restart_from_monotone_solver_20261124

**Source location.** [1](https://arxiv.org/pdf/2609.23557v1) Assumptions 2.1--2.4; Definition 2.1; Lemma 2.1; Algorithm 1; equation (8); Theorems 4.1 and 5.1; equations (11)--(13), (22)--(23).

$T^\star_{{\rm rand},\infty}\le O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$ for all positive model parameters and fixed $p\ge2$; a deterministic feasible witness supplies an actual tangent certificate.

The local argument specifies the original-domain tangent certificate, fixed query budget, public parameter mapping, fixed-order constants and dimension scope.

### B2 - Certified restart on the original compact domain

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_p\!\left(1+\kappa_D^{\alpha_p}+\log_+(1/\theta)\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.23557v1)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)\le\kappa_D^{\alpha_p}$.; All eight-axis contracts of this profile hold. The upper witness is deterministic; the lower class is unrestricted randomized with fixed success probability 2/3 and fixed pathwise query cap.

**Dimension conditions.** Every finite dimension.

**Constants.** Constants depend only on the fixed integer p and the once-fixed smooth gate. The threshold and sufficient dimension are explicit; no uniform claim as p grows is made.

**Derivation.** Theorem 5.1 of 2609.23557v1, with Assumptions 2.1--2.4, Algorithm 1 and Lemma 2.1, returns a feasible $u$ and an evaluated vector $v=F(u)+n$, $n\in N_X(u)$, with $\|v\|\le\eta$ in at most $C_p[1+(L_pR^p/\eta)^{\alpha_p}]$ complete-jet calls whenever $\|z-x^\star\|\le R$, where $\alpha_p=2/(3p-1)$. The constant $C_p$ depends only on fixed $p$.

The source writes its scale as the exact initial distance. A supplied upper bound $R$ is sufficient: choose its equation (8) with $\eta_0=(L_pR^{p-1})^{-1}$ and its inner tolerance with $R$. In the proof of Theorem 4.1, equations (11)--(13) use the initial distance only through the upper estimates $\|z-x^\star\|\le R$, $\sum_t\|e_t\|\le R$, $\|u_t-x^\star\|\le2R$ and $P_0\le6R^2/\eta_0$. The distance-energy and query-sum bounds in Lemma 5.1 and Theorem 5.1 then keep the same scale. Thus the subroutine requires no knowledge of the exact distance.

For the unique VI solution choose $n^\star=-F(x^\star)\in N_X(x^\star)$. Monotonicity of the normal cone and $\mu$-strong monotonicity give $\mu\|u-x^\star\|^2\le\langle F(u)+n,u-x^\star\rangle\le\|v\|\|u-x^\star\|$, hence $\|u-x^\star\|\le\|v\|/\mu$.

Set $R_j=D2^{-j}$, $z_0=x_0$, and $S=\max\{1,\lceil\log_2(\mu D/\varepsilon)\rceil\}$. At each $j=0,\ldots,S-1$, run the certified monotone solver on the same original set $X$, starting from $z_j$, with residual tolerance $\eta_j=\mu R_j/2$. Set $z_{j+1}=u_j$. The preceding inequality inductively proves $\|z_{j+1}-x^\star\|\le R_{j+1}$.

The last actual certificate obeys $\|v_{S-1}\|\le\mu D2^{-S}\le\varepsilon$. The final conclusion is therefore a tangent-residual certificate, not merely distance contraction. The normal cone remains $N_X$ throughout: there is no restriction to an intersected ball and no normal-cone transfer.

Every stage costs at most $C_p[1+2^{\alpha_p}\kappa_D^{\alpha_p}2^{-j\alpha_p(p-1)}]$, where $\kappa_D=L_pD^{p-1}/\mu$. Summing gives $C_p[S+2^{\alpha_p}\kappa_D^{\alpha_p}/(1-2^{-\alpha_p(p-1)})]$. For fixed $p\ge2$ this is $O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$, where $\theta=\varepsilon/(\mu D)$ and $\log_+(t)=\max\{0,\log t\}$. The cost includes all inner jet evaluations and all returned certificates.

All queried centers and model solutions in source Algorithms 1--3 are in $X$, with projection onto the known $X$. A regularized operator $F+\eta^{-1}(\cdot-z)$ uses one original jet per query and has the same Lipschitz bound on $D^{p-1}$ for $p\ge2$. Source Assumptions 2.3--2.4 impose their inequalities on $X$; the neighborhood regularity used here supplies the same Taylor data. The bound is dimension-independent; constants are not asserted uniform when $p$ grows.

**Local argument.** CV_S_STRONG_HIGH_VI_TANGENT__restart_from_monotone_solver_20261124

**Source location.** [1](https://arxiv.org/pdf/2609.23557v1) Assumptions 2.1--2.4; Definition 2.1; Lemma 2.1; Algorithm 1; equation (8); Theorems 4.1 and 5.1; equations (11)--(13), (22)--(23).

$T^\star_{{\rm rand},\infty}\le O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$ for all positive model parameters and fixed $p\ge2$; a deterministic feasible witness supplies an actual tangent certificate.

The local argument specifies the original-domain tangent certificate, fixed query budget, public parameter mapping, fixed-order constants and dimension scope.

### B3 - Strong-monotonicity calibration of an existing random-frame family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_p(\kappa_D^{\alpha_p})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.13462v2)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)\le\kappa_D^{\alpha_p}$.; All eight-axis contracts of this profile hold. The upper witness is deterministic; the lower class is unrestricted randomized with fixed success probability 2/3 and fixed pathwise query cap.; The stronger explicit statement is $T^\star_{{\rm rand},\infty}\ge m\ge\frac12(c_p^{\rm sc}\kappa_D)^{\alpha_p}$.

**Dimension conditions.** For fixed $p$, take $m=\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor\ge2$. The lower bound holds on $X=B_2^d(D/2)$ with start zero whenever $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. Here $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$ for the fixed gate of 2609.13462v2, $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, and $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. Upper bounds hold in every finite dimension. The comparison quantity takes a worst case over finite dimensions.

**Constants.** Constants depend only on the fixed integer p and the once-fixed smooth gate. The threshold and sufficient dimension are explicit; no uniform claim as p grows is made.

**Derivation.** Use only the family in 2609.13462v2, Section 10. Fix its smooth even gate $\rho$ and $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$. For integer $m\ge2$, set $R=D/2$, $q=1-1/(2m)$, $c=R/(2\sqrt m)$, $\tau=R/(16m^{3/2})$ and $\lambda=L_p\tau^{p-1}/B_p$, exactly as equation (10.4).

For a hidden orthonormal frame $V=(v_1,\ldots,v_m)$ define $T_V(x)=cv_1+q\sum_{i=1}^{m-1}h_\tau(\langle v_i,x\rangle)v_{i+1}$ and $F_V=\lambda(\operatorname{Id}-T_V)$ on the public ball $X=B_2^d(R)$, with public start $0$. Lemma 10.2 gives global strong monotonicity $\mu_m=\lambda/(2m)$, Lipschitz $(p-1)$st derivative at most $L_p$, a unique interior zero and $r_{\rm tan}(x)=\|F_V(x)\|$ even at the boundary. No change of target metric is required.

Writing $a_p=(3p-1)/2$ and $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, direct substitution gives $\mu_m=c_p^{\rm sc}L_pD^{p-1}/m^{a_p}$. The residual barrier in equation (11.3) is $L_pR^p/[8B_p16^{p-1}m^{a_p}]=\mu_mD/8$.

Assume $\kappa_D\ge\kappa_{0,p}:=2^{a_p}/c_p^{\rm sc}$ and set $m=\lfloor(c_p^{\rm sc}\kappa_D)^{1/a_p}\rfloor\ge2$. Then $m^{a_p}\le c_p^{\rm sc}\kappa_D$, so $\mu_m\ge\mu$. The hard family is therefore inside the promised $\mu$-strongly monotone class; the modulus is an available lower bound, not an equality requirement.

Apply Theorem 11.3 with the fixed cap $N=m-1$ and source failure parameter $\delta=1/4$. It requires $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. For every adaptive randomized algorithm with this cap and any feasible measurable output, some fixed frame has probability at least $3/4$ of residual at least $\mu_mD/8$.

If $0<\theta\le1/16$, this barrier is at least $\mu D/8\ge2\varepsilon$. A per-instance success guarantee of $2/3$ is therefore impossible with $m-1$ queries. Consequently $T^\star_{{\rm rand},\infty}\ge m\ge\frac12(c_p^{\rm sc}\kappa_D)^{\alpha_p}=\Omega_p(\kappa_D^{\alpha_p})$. The same fixed-dimensional statement holds for every $d$ satisfying the displayed sufficient threshold, on the public ball family.

The source discloses all scalar parameters and even the template, while only the frame is hidden. Declaring $\mu$ and calibrating $m$ from public parameters does not invalidate its information argument. The bound is for arbitrary randomized complete-jet queries, not a span-restricted algorithm class. For fixed $p$, the sufficient dimension is $O_p(\kappa_D^{6/(3p-1)}\log(2+\kappa_D))$; the explicit threshold above is authoritative. No lower bound of this order is asserted in every fixed small dimension, or for the additive accuracy logarithm.

**Local argument.** CV_S_STRONG_HIGH_VI_TANGENT__strong_parameterization_of_chain_20261124

**Source location.** [2](https://arxiv.org/pdf/2609.13462v2) Definition 3.1; equation (10.1); equations (10.4)--(10.6); Lemma 10.2; Lemma 10.4; Theorem 11.3, equations (11.2)--(11.3).

$T^\star_{{\rm rand},\infty}\ge\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor=\Omega_p(\kappa_D^{\alpha_p})$ for $\kappa_D\ge\kappa_{0,p}$ and $0<\theta\le1/16$, with the stated sufficient dimension.

The local argument specifies the original-domain tangent certificate, fixed query budget, public parameter mapping, fixed-order constants and dimension scope.

### B4 - Certified restart on the original compact domain

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Deterministic witness

$$
O_p\!\left(1+\kappa_D^{\alpha_p}+\log_+(1/\theta)\right)
$$

**Sources.** [1](https://arxiv.org/pdf/2609.23557v1)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)>\kappa_D^{\alpha_p}$.; All eight-axis contracts of this profile hold. The upper witness is deterministic; the lower class is unrestricted randomized with fixed success probability 2/3 and fixed pathwise query cap.

**Dimension conditions.** Every finite dimension.

**Constants.** Constants depend only on the fixed integer p and the once-fixed smooth gate. The threshold and sufficient dimension are explicit; no uniform claim as p grows is made.

**Derivation.** Theorem 5.1 of 2609.23557v1, with Assumptions 2.1--2.4, Algorithm 1 and Lemma 2.1, returns a feasible $u$ and an evaluated vector $v=F(u)+n$, $n\in N_X(u)$, with $\|v\|\le\eta$ in at most $C_p[1+(L_pR^p/\eta)^{\alpha_p}]$ complete-jet calls whenever $\|z-x^\star\|\le R$, where $\alpha_p=2/(3p-1)$. The constant $C_p$ depends only on fixed $p$.

The source writes its scale as the exact initial distance. A supplied upper bound $R$ is sufficient: choose its equation (8) with $\eta_0=(L_pR^{p-1})^{-1}$ and its inner tolerance with $R$. In the proof of Theorem 4.1, equations (11)--(13) use the initial distance only through the upper estimates $\|z-x^\star\|\le R$, $\sum_t\|e_t\|\le R$, $\|u_t-x^\star\|\le2R$ and $P_0\le6R^2/\eta_0$. The distance-energy and query-sum bounds in Lemma 5.1 and Theorem 5.1 then keep the same scale. Thus the subroutine requires no knowledge of the exact distance.

For the unique VI solution choose $n^\star=-F(x^\star)\in N_X(x^\star)$. Monotonicity of the normal cone and $\mu$-strong monotonicity give $\mu\|u-x^\star\|^2\le\langle F(u)+n,u-x^\star\rangle\le\|v\|\|u-x^\star\|$, hence $\|u-x^\star\|\le\|v\|/\mu$.

Set $R_j=D2^{-j}$, $z_0=x_0$, and $S=\max\{1,\lceil\log_2(\mu D/\varepsilon)\rceil\}$. At each $j=0,\ldots,S-1$, run the certified monotone solver on the same original set $X$, starting from $z_j$, with residual tolerance $\eta_j=\mu R_j/2$. Set $z_{j+1}=u_j$. The preceding inequality inductively proves $\|z_{j+1}-x^\star\|\le R_{j+1}$.

The last actual certificate obeys $\|v_{S-1}\|\le\mu D2^{-S}\le\varepsilon$. The final conclusion is therefore a tangent-residual certificate, not merely distance contraction. The normal cone remains $N_X$ throughout: there is no restriction to an intersected ball and no normal-cone transfer.

Every stage costs at most $C_p[1+2^{\alpha_p}\kappa_D^{\alpha_p}2^{-j\alpha_p(p-1)}]$, where $\kappa_D=L_pD^{p-1}/\mu$. Summing gives $C_p[S+2^{\alpha_p}\kappa_D^{\alpha_p}/(1-2^{-\alpha_p(p-1)})]$. For fixed $p\ge2$ this is $O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$, where $\theta=\varepsilon/(\mu D)$ and $\log_+(t)=\max\{0,\log t\}$. The cost includes all inner jet evaluations and all returned certificates.

All queried centers and model solutions in source Algorithms 1--3 are in $X$, with projection onto the known $X$. A regularized operator $F+\eta^{-1}(\cdot-z)$ uses one original jet per query and has the same Lipschitz bound on $D^{p-1}$ for $p\ge2$. Source Assumptions 2.3--2.4 impose their inequalities on $X$; the neighborhood regularity used here supplies the same Taylor data. The bound is dimension-independent; constants are not asserted uniform when $p$ grows.

**Local argument.** CV_S_STRONG_HIGH_VI_TANGENT__restart_from_monotone_solver_20261124

**Source location.** [1](https://arxiv.org/pdf/2609.23557v1) Assumptions 2.1--2.4; Definition 2.1; Lemma 2.1; Algorithm 1; equation (8); Theorems 4.1 and 5.1; equations (11)--(13), (22)--(23).

$T^\star_{{\rm rand},\infty}\le O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$ for all positive model parameters and fixed $p\ge2$; a deterministic feasible witness supplies an actual tangent certificate.

The local argument specifies the original-domain tangent certificate, fixed query budget, public parameter mapping, fixed-order constants and dimension scope.

### B5 - Strong-monotonicity calibration of an existing random-frame family

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** All randomized adaptive algorithms

$$
\Omega_p(\kappa_D^{\alpha_p})
$$

**Sources.** [2](https://arxiv.org/pdf/2609.13462v2)

**Conditions.** $p\ge2$ fixed, $\kappa_D\ge\kappa_{0,p}$, $0<\theta\le1/16$, and $\log_+(1/\theta)>\kappa_D^{\alpha_p}$.; All eight-axis contracts of this profile hold. The upper witness is deterministic; the lower class is unrestricted randomized with fixed success probability 2/3 and fixed pathwise query cap.; The stronger explicit statement is $T^\star_{{\rm rand},\infty}\ge m\ge\frac12(c_p^{\rm sc}\kappa_D)^{\alpha_p}$.

**Dimension conditions.** For fixed $p$, take $m=\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor\ge2$. The lower bound holds on $X=B_2^d(D/2)$ with start zero whenever $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. Here $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$ for the fixed gate of 2609.13462v2, $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, and $\kappa_{0,p}=2^{(3p-1)/2}/c_p^{\rm sc}$. Upper bounds hold in every finite dimension. The comparison quantity takes a worst case over finite dimensions.

**Constants.** Constants depend only on the fixed integer p and the once-fixed smooth gate. The threshold and sufficient dimension are explicit; no uniform claim as p grows is made.

**Derivation.** Use only the family in 2609.13462v2, Section 10. Fix its smooth even gate $\rho$ and $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$. For integer $m\ge2$, set $R=D/2$, $q=1-1/(2m)$, $c=R/(2\sqrt m)$, $\tau=R/(16m^{3/2})$ and $\lambda=L_p\tau^{p-1}/B_p$, exactly as equation (10.4).

For a hidden orthonormal frame $V=(v_1,\ldots,v_m)$ define $T_V(x)=cv_1+q\sum_{i=1}^{m-1}h_\tau(\langle v_i,x\rangle)v_{i+1}$ and $F_V=\lambda(\operatorname{Id}-T_V)$ on the public ball $X=B_2^d(R)$, with public start $0$. Lemma 10.2 gives global strong monotonicity $\mu_m=\lambda/(2m)$, Lipschitz $(p-1)$st derivative at most $L_p$, a unique interior zero and $r_{\rm tan}(x)=\|F_V(x)\|$ even at the boundary. No change of target metric is required.

Writing $a_p=(3p-1)/2$ and $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, direct substitution gives $\mu_m=c_p^{\rm sc}L_pD^{p-1}/m^{a_p}$. The residual barrier in equation (11.3) is $L_pR^p/[8B_p16^{p-1}m^{a_p}]=\mu_mD/8$.

Assume $\kappa_D\ge\kappa_{0,p}:=2^{a_p}/c_p^{\rm sc}$ and set $m=\lfloor(c_p^{\rm sc}\kappa_D)^{1/a_p}\rfloor\ge2$. Then $m^{a_p}\le c_p^{\rm sc}\kappa_D$, so $\mu_m\ge\mu$. The hard family is therefore inside the promised $\mu$-strongly monotone class; the modulus is an available lower bound, not an equality requirement.

Apply Theorem 11.3 with the fixed cap $N=m-1$ and source failure parameter $\delta=1/4$. It requires $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. For every adaptive randomized algorithm with this cap and any feasible measurable output, some fixed frame has probability at least $3/4$ of residual at least $\mu_mD/8$.

If $0<\theta\le1/16$, this barrier is at least $\mu D/8\ge2\varepsilon$. A per-instance success guarantee of $2/3$ is therefore impossible with $m-1$ queries. Consequently $T^\star_{{\rm rand},\infty}\ge m\ge\frac12(c_p^{\rm sc}\kappa_D)^{\alpha_p}=\Omega_p(\kappa_D^{\alpha_p})$. The same fixed-dimensional statement holds for every $d$ satisfying the displayed sufficient threshold, on the public ball family.

The source discloses all scalar parameters and even the template, while only the frame is hidden. Declaring $\mu$ and calibrating $m$ from public parameters does not invalidate its information argument. The bound is for arbitrary randomized complete-jet queries, not a span-restricted algorithm class. For fixed $p$, the sufficient dimension is $O_p(\kappa_D^{6/(3p-1)}\log(2+\kappa_D))$; the explicit threshold above is authoritative. No lower bound of this order is asserted in every fixed small dimension, or for the additive accuracy logarithm.

**Local argument.** CV_S_STRONG_HIGH_VI_TANGENT__strong_parameterization_of_chain_20261124

**Source location.** [2](https://arxiv.org/pdf/2609.13462v2) Definition 3.1; equation (10.1); equations (10.4)--(10.6); Lemma 10.2; Lemma 10.4; Theorem 11.3, equations (11.2)--(11.3).

$T^\star_{{\rm rand},\infty}\ge\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor=\Omega_p(\kappa_D^{\alpha_p})$ for $\kappa_D\ge\kappa_{0,p}$ and $0<\theta\le1/16$, with the stated sufficient dimension.

The local argument specifies the original-domain tangent certificate, fixed query budget, public parameter mapping, fixed-order constants and dimension scope.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: 784e60fe7f22297c0209265be9f8e949bcc1ac0cb8268e2b6abd81c7c5af0298

### Native proof: CV_S_STRONG_HIGH_VI_TANGENT__restart_from_monotone_solver_20261124

Native pointer: /proofs/0; canonical SHA-256: ace24da56b4f69ce86337ceee93661fbfa5287a4505ab9c1e4357a81f9a73a0e

#### Native field: kind

Native pointer: /proofs/0/kind; canonical SHA-256: cfa542c409fb3d47432f3fbd509c4920e1f04ad8c0dc55e0c4abfec8293a7d89

local_mathematical_derivation

#### Native field: title

Native pointer: /proofs/0/title; canonical SHA-256: 36e20d7a9a67f5b2d05f2c0ac9221597c7ea99530afed5fcdd42e35e77a922b3

Certified restart on the original compact domain

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 7fd82bbde22376e5d886b0e7b4838c7cd74109ac46f3c2cde19ddd255c8482d5

#### Native item 1

Native pointer: /proofs/0/source_refs/0; canonical SHA-256: 24369682e51b4d5eb2472abf9b1016c795d02a570c3bd52551d774bea6eae373

CV_SRC_mvi_optimal_2609_23557

#### Native field: premises

Native pointer: /proofs/0/premises; canonical SHA-256: 1d4f5abc8df3ca579392d357f6d19b1cb20deab2fd8db3acf40af41cc4758631

#### Native item 1

Native pointer: /proofs/0/premises/0; canonical SHA-256: f5e8638f58226ff985bfb37cf53eda66f1b7f46b552effd51cbb98b5ebb6a689

#### Native field: source_ref

Native pointer: /proofs/0/premises/0/source_ref; canonical SHA-256: 24369682e51b4d5eb2472abf9b1016c795d02a570c3bd52551d774bea6eae373

CV_SRC_mvi_optimal_2609_23557

#### Native field: locator

Native pointer: /proofs/0/premises/0/locator; canonical SHA-256: 3d7058a038f9a08d54910e44172772b97892a86bcec41e7b160956dff6ae02ce

Assumptions 2.1--2.4; Definition 2.1; Lemma 2.1; Algorithm 1; equation (8); Theorems 4.1 and 5.1; equations (11)--(13), (22)--(23).

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: 23ea1d48f9524ce8e56eeffee52fcef1bf5e79c2bc95ba69a9f16ddb813c33fc

$T^\star_{{\rm rand},\infty}\le O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$ for all positive model parameters and fixed $p\ge2$; a deterministic feasible witness supplies an actual tangent certificate.

#### Native field: derivation_paragraphs

Native pointer: /proofs/0/derivation_paragraphs; canonical SHA-256: a63987df80d21cd3ea472dd2a43095846e64f6973e8bb5a26eeefa816cec7bbe

#### Native item 1

Native pointer: /proofs/0/derivation_paragraphs/0; canonical SHA-256: d01be054b2d3d0093161b79b479966d3c3f5e3849bd876dc9f55ce2779ecf095

Theorem 5.1 of 2609.23557v1, with Assumptions 2.1--2.4, Algorithm 1 and Lemma 2.1, returns a feasible $u$ and an evaluated vector $v=F(u)+n$, $n\in N_X(u)$, with $\|v\|\le\eta$ in at most $C_p[1+(L_pR^p/\eta)^{\alpha_p}]$ complete-jet calls whenever $\|z-x^\star\|\le R$, where $\alpha_p=2/(3p-1)$. The constant $C_p$ depends only on fixed $p$.

#### Native item 2

Native pointer: /proofs/0/derivation_paragraphs/1; canonical SHA-256: a1a547f6c4bb9b9203fd9f94baf7f169d6a53642c190bf2a311c9180bce031c8

The source writes its scale as the exact initial distance. A supplied upper bound $R$ is sufficient: choose its equation (8) with $\eta_0=(L_pR^{p-1})^{-1}$ and its inner tolerance with $R$. In the proof of Theorem 4.1, equations (11)--(13) use the initial distance only through the upper estimates $\|z-x^\star\|\le R$, $\sum_t\|e_t\|\le R$, $\|u_t-x^\star\|\le2R$ and $P_0\le6R^2/\eta_0$. The distance-energy and query-sum bounds in Lemma 5.1 and Theorem 5.1 then keep the same scale. Thus the subroutine requires no knowledge of the exact distance.

#### Native item 3

Native pointer: /proofs/0/derivation_paragraphs/2; canonical SHA-256: b6c59b73bdf25dff58f22d749c1c0e9c14ba1967e786756c0219b77de7a4f514

For the unique VI solution choose $n^\star=-F(x^\star)\in N_X(x^\star)$. Monotonicity of the normal cone and $\mu$-strong monotonicity give $\mu\|u-x^\star\|^2\le\langle F(u)+n,u-x^\star\rangle\le\|v\|\|u-x^\star\|$, hence $\|u-x^\star\|\le\|v\|/\mu$.

#### Native item 4

Native pointer: /proofs/0/derivation_paragraphs/3; canonical SHA-256: 795a7b3c72863223680b92ce8f1cceb8a314e180139d4dcfed1ce030c44e7498

Set $R_j=D2^{-j}$, $z_0=x_0$, and $S=\max\{1,\lceil\log_2(\mu D/\varepsilon)\rceil\}$. At each $j=0,\ldots,S-1$, run the certified monotone solver on the same original set $X$, starting from $z_j$, with residual tolerance $\eta_j=\mu R_j/2$. Set $z_{j+1}=u_j$. The preceding inequality inductively proves $\|z_{j+1}-x^\star\|\le R_{j+1}$.

#### Native item 5

Native pointer: /proofs/0/derivation_paragraphs/4; canonical SHA-256: 9ce8d4eb069f3784a83b380d1c3b971b1b0f3821ffa86f1cd8e2d7c539823088

The last actual certificate obeys $\|v_{S-1}\|\le\mu D2^{-S}\le\varepsilon$. The final conclusion is therefore a tangent-residual certificate, not merely distance contraction. The normal cone remains $N_X$ throughout: there is no restriction to an intersected ball and no normal-cone transfer.

#### Native item 6

Native pointer: /proofs/0/derivation_paragraphs/5; canonical SHA-256: a6ef7219028eac2afa94f71dabccac1b64cf7ef76966c5763e29265161ffe819

Every stage costs at most $C_p[1+2^{\alpha_p}\kappa_D^{\alpha_p}2^{-j\alpha_p(p-1)}]$, where $\kappa_D=L_pD^{p-1}/\mu$. Summing gives $C_p[S+2^{\alpha_p}\kappa_D^{\alpha_p}/(1-2^{-\alpha_p(p-1)})]$. For fixed $p\ge2$ this is $O_p(1+\kappa_D^{\alpha_p}+\log_+(1/\theta))$, where $\theta=\varepsilon/(\mu D)$ and $\log_+(t)=\max\{0,\log t\}$. The cost includes all inner jet evaluations and all returned certificates.

#### Native item 7

Native pointer: /proofs/0/derivation_paragraphs/6; canonical SHA-256: bf7944a7cebe28ea52b90ca23450187ff086482df6e091f31c1a51ca0e7493b8

All queried centers and model solutions in source Algorithms 1--3 are in $X$, with projection onto the known $X$. A regularized operator $F+\eta^{-1}(\cdot-z)$ uses one original jet per query and has the same Lipschitz bound on $D^{p-1}$ for $p\ge2$. Source Assumptions 2.3--2.4 impose their inequalities on $X$; the neighborhood regularity used here supplies the same Taylor data. The bound is dimension-independent; constants are not asserted uniform when $p$ grows.

### Native proof: CV_S_STRONG_HIGH_VI_TANGENT__strong_parameterization_of_chain_20261124

Native pointer: /proofs/1; canonical SHA-256: 83154e85462feca1bb7d45ce5529acfa360084a03174737162061c36a43200e1

#### Native field: kind

Native pointer: /proofs/1/kind; canonical SHA-256: cfa542c409fb3d47432f3fbd509c4920e1f04ad8c0dc55e0c4abfec8293a7d89

local_mathematical_derivation

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: 2a3abab2419709af6939215422050f9926e1a3d9a42c5584dd93718c5833b0c4

Strong-monotonicity calibration of an existing random-frame family

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 9f8c9cab29d4ea94ca4fa5735db7f4bdad01cba2cb8df2cce3e56c9b4d58d40a

#### Native item 1

Native pointer: /proofs/1/source_refs/0; canonical SHA-256: b70e46d42424a8870809d331d34d1680a1453ac27a9751da325a70da76632683

CV_SRC_mvi_higher_2609_13462

#### Native field: premises

Native pointer: /proofs/1/premises; canonical SHA-256: f8229b708c1181211de344dd16a5bf785c6fbe7a55617354caf954ecb7b6c4ac

#### Native item 1

Native pointer: /proofs/1/premises/0; canonical SHA-256: 5af2a10e3e17d2c8d99a09475b048bc7da10875abcdd150bf40b02e5f1803878

#### Native field: source_ref

Native pointer: /proofs/1/premises/0/source_ref; canonical SHA-256: b70e46d42424a8870809d331d34d1680a1453ac27a9751da325a70da76632683

CV_SRC_mvi_higher_2609_13462

#### Native field: locator

Native pointer: /proofs/1/premises/0/locator; canonical SHA-256: ad6a05ec0a971d3d2e885367cff490da45cf1c60c2a5aa9679b72c1a09cde3d5

Definition 3.1; equation (10.1); equations (10.4)--(10.6); Lemma 10.2; Lemma 10.4; Theorem 11.3, equations (11.2)--(11.3).

#### Native field: statement

Native pointer: /proofs/1/statement; canonical SHA-256: c84557db90cc64793e2a47aa388d41ac9d6a2b88b4105b0654813feea4f77bbe

$T^\star_{{\rm rand},\infty}\ge\lfloor(c_p^{\rm sc}\kappa_D)^{\alpha_p}\rfloor=\Omega_p(\kappa_D^{\alpha_p})$ for $\kappa_D\ge\kappa_{0,p}$ and $0<\theta\le1/16$, with the stated sufficient dimension.

#### Native field: derivation_paragraphs

Native pointer: /proofs/1/derivation_paragraphs; canonical SHA-256: 8945705b0e2f5f367a0e91eeee6ea5ce58604ae568a481a391061e21f773516e

#### Native item 1

Native pointer: /proofs/1/derivation_paragraphs/0; canonical SHA-256: 8669e9811ac8825628e262ca0c6a4a3cb6dbf311e3f2435f6c0c28812151aae5

Use only the family in 2609.13462v2, Section 10. Fix its smooth even gate $\rho$ and $B_p=\max\{1,\|\rho^{(p-1)}\|_\infty\}$. For integer $m\ge2$, set $R=D/2$, $q=1-1/(2m)$, $c=R/(2\sqrt m)$, $\tau=R/(16m^{3/2})$ and $\lambda=L_p\tau^{p-1}/B_p$, exactly as equation (10.4).

#### Native item 2

Native pointer: /proofs/1/derivation_paragraphs/1; canonical SHA-256: 93c257e06cd187130de1d05aa810e614a64c92b6dc30421b061acf44a13d733e

For a hidden orthonormal frame $V=(v_1,\ldots,v_m)$ define $T_V(x)=cv_1+q\sum_{i=1}^{m-1}h_\tau(\langle v_i,x\rangle)v_{i+1}$ and $F_V=\lambda(\operatorname{Id}-T_V)$ on the public ball $X=B_2^d(R)$, with public start $0$. Lemma 10.2 gives global strong monotonicity $\mu_m=\lambda/(2m)$, Lipschitz $(p-1)$st derivative at most $L_p$, a unique interior zero and $r_{\rm tan}(x)=\|F_V(x)\|$ even at the boundary. No change of target metric is required.

#### Native item 3

Native pointer: /proofs/1/derivation_paragraphs/2; canonical SHA-256: a527cfdd780120de9739fe5b64f2ddee38d14b53adff8a06d6c0943471b341b6

Writing $a_p=(3p-1)/2$ and $c_p^{\rm sc}=1/(2^pB_p16^{p-1})$, direct substitution gives $\mu_m=c_p^{\rm sc}L_pD^{p-1}/m^{a_p}$. The residual barrier in equation (11.3) is $L_pR^p/[8B_p16^{p-1}m^{a_p}]=\mu_mD/8$.

#### Native item 4

Native pointer: /proofs/1/derivation_paragraphs/3; canonical SHA-256: 28763e886855a2cd616c824d32536a4e8780824c72e5577b10ca9be8669af44c

Assume $\kappa_D\ge\kappa_{0,p}:=2^{a_p}/c_p^{\rm sc}$ and set $m=\lfloor(c_p^{\rm sc}\kappa_D)^{1/a_p}\rfloor\ge2$. Then $m^{a_p}\le c_p^{\rm sc}\kappa_D$, so $\mu_m\ge\mu$. The hard family is therefore inside the promised $\mu$-strongly monotone class; the modulus is an available lower bound, not an equality requirement.

#### Native item 5

Native pointer: /proofs/1/derivation_paragraphs/4; canonical SHA-256: 3bb93c52169d9f749167776b157ab7191ece5ba62dc668c8e0cd6585d47cc261

Apply Theorem 11.3 with the fixed cap $N=m-1$ and source failure parameter $\delta=1/4$. It requires $d\ge m+\lceil2048m^3\log(8(m^2+1))\rceil$. For every adaptive randomized algorithm with this cap and any feasible measurable output, some fixed frame has probability at least $3/4$ of residual at least $\mu_mD/8$.

#### Native item 6

Native pointer: /proofs/1/derivation_paragraphs/5; canonical SHA-256: 61c1acdd53a5bf5163d627c21c144125f62c77814dfaa02b90029fd3dedfa76e

If $0<\theta\le1/16$, this barrier is at least $\mu D/8\ge2\varepsilon$. A per-instance success guarantee of $2/3$ is therefore impossible with $m-1$ queries. Consequently $T^\star_{{\rm rand},\infty}\ge m\ge\frac12(c_p^{\rm sc}\kappa_D)^{\alpha_p}=\Omega_p(\kappa_D^{\alpha_p})$. The same fixed-dimensional statement holds for every $d$ satisfying the displayed sufficient threshold, on the public ball family.

#### Native item 7

Native pointer: /proofs/1/derivation_paragraphs/6; canonical SHA-256: 61c8242da362a9fd1121689e0e309581a91db8058e45ac9f0f8a5cb4009180f2

The source discloses all scalar parameters and even the template, while only the frame is hidden. Declaring $\mu$ and calibrating $m$ from public parameters does not invalidate its information argument. The bound is for arbitrary randomized complete-jet queries, not a span-restricted algorithm class. For fixed $p$, the sufficient dimension is $O_p(\kappa_D^{6/(3p-1)}\log(2+\kappa_D))$; the explicit threshold above is authoritative. No lower bound of this order is asserted in every fixed small dimension, or for the additive accuracy logarithm.

## References

[1] Xinliang Zhang; Lesi Chen; Linxuan Pan; Chengchang Liu; Junchi Yang; Jingzhao Zhang. Optimal High-Order Methods for Solving Monotone Variational Inequalities. 2026. arXiv:2609.23557v1.

https://arxiv.org/pdf/2609.23557v1

[2] Haihan Zhang; Wendao Wu; Chenheng Zhang; Cong Fang; Haoxuan Li; Zhouchen Lin. Matching Higher-Order Oracle Complexity for Smooth Monotone Variational Inequalities. 2026. arXiv:2609.13462v2.

https://arxiv.org/pdf/2609.13462v2
