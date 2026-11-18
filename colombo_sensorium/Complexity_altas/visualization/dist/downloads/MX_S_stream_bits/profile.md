# Low-rank approximation from a finite-bit row stream: one-pass memory

**Setting ID.** `MX_S_stream_bits`

Matrix computation

After one pass over the rows of $A\in\mathbb{R}^{m\times n}$, return a rank-$k$ orthogonal right projection.

**Status.** Polynomial gap present

**TASK tags.** formulation: Row streaming lowrank; solution concept: Relative frobenius squared projection; task family: Matrix computation

**MODEL tags.** spectral structure: Finite encoded matrix; structure: Row stream

**ORACLE tags.** feedback quality: Exact; interface family: Row stream; operation: Matrix stream update; public information: Hidden objects explicitly declared; public information: Public inputs explicitly declared

**ALGORITHMS tags.** memory: Finite-bit retained state; randomization: Private randomness allowed; restriction: No past requery; restriction: No additional span restriction explicitly imposed; restriction: One pass

**OUTPUT tags.** certificate: No additional output certificate required; object: Orthogonal projector or basis

**METRIC tags.** criterion: Relative squared projection residual

**GUARANTEE tags.** randomness: Algorithm private seed; time uniformity: Fixed time or accuracy

**RESOURCE tags.** measure: Memory bits; measure: Passes; measure: Stream rows

## 1. Setting specification

### Task

After one pass over the rows of $A\in\mathbb{R}^{m\times n}$, return a rank-$k$ orthogonal right projection.

### Admissible model

Entries of $A$ lie in the public finite alphabet $\{0,\pm1,\pm1/\sqrt q\}$ with public encoding of integer $q\ge1$. The row sequence is fixed in advance. Assume $m,n\ge1$, $1\le k<\min\{m,n\}$, and $\varepsilon>0$.

### Oracle interface

The information $m,n,k,\varepsilon$ and encoding parameter $q$ are public. A call reveals only the next complete row. Consumed rows are unavailable; after the stream, the algorithm cannot query $Av$ or reread the input.

### Output

After the stream, use only retained state to output $P=P^{\mathsf T}=P^2\in\mathbb{R}^{n\times n}$ with $\operatorname{rank}(P)=k$; an orthonormal-basis representation is allowed. Returning $AP$ is unnecessary.

### Loss or accuracy criterion

Let $A_k$ be any best rank-$k$ Frobenius approximation. Success requires $\|A(I_n-P)\|_{\mathrm{F}}^2\le(1+\varepsilon)\|A-A_k\|_{\mathrm{F}}^2$; the residual is explicitly squared. When the optimal residual is zero, the row space must be recovered exactly.

### Resource accounting

The native resource is peak simultaneous memory in bits, $S_{\mathrm{bit}}$. One pass is a fixed protocol requirement and is not added to bit memory. Input encoding, working state, and output-encoding requirements must be retained.

The cost limit holds for every input and private seed. The final output must be decoded from the charged state, without an unregistered external cache.

### Algorithm views and success guarantees

Randomized computable one-pass streaming algorithms are allowed. The retained state is a finite bit string, including random-generator state under the declared memory model. No span or running-time restriction is added beyond one pass and bit memory.

The algorithm is selected using only public inputs. For every admissible input fixed before its private seed is generated, the success event has probability at least $2/3$ over that private randomness.

**Budget convention.** One pass; peak memory is bounded for every input and random seed.

## 2. Notation and parameters

$m$: Number of rows of the input matrix **Domain:** $m\in\mathbb N,\ m\ge1$.

$A\in\mathbb R^{m\times n}$

$n$: Number of columns of the input matrix **Domain:** $n\in\mathbb N,\ n\ge1$.

$A\in\mathbb R^{m\times n}$

$k$: The exact rank of the orthogonal right projection returned after the stream. **Domain:** $k\in\mathbb N,\ 1\le k<\min\{m,n\}$.

$\operatorname{rank}(P)=k$

$\varepsilon$: Additional relative factor over the optimal squared Frobenius residual **Domain:** $\varepsilon>0$.

$\|A(I_n-P)\|_F^2\le(1+\varepsilon)\|A-A_k\|_F^2$

$q$: The encoding parameter for the public finite input alphabet. **Domain:** $q\in\mathbb N,\ q\ge1$.

$A_{ij}\in\{0,\pm1,\pm q^{-1/2}\}$

$C_0$: Sufficient row- and column-dimension constants for the communication reduction in ST, Theorem 1 **Domain:** The quantity $C_0>0$ is universal and fixed.

$m,n\ge C_0k/\varepsilon$

$A$: The input matrix arriving in a precommitted row order. **Domain:** $\mathbb R^{m\times n}$.

$P$: Right orthogonal projector returned after the stream ends **Domain:** $\mathbb R^{n\times n}$.

$P=P^{\mathsf T}=P^2,\quad\operatorname{rank}(P)=k$

$I_n$: The order-n identity matrix. **Domain:** $\mathbb R^{n\times n}$.

$A_k$: Best Frobenius approximation of rank at most $k$ **Domain:** $\mathbb R^{m\times n}$.

$A_k\in\arg\min_{\operatorname{rank}(B)\le k}\|A-B\|_F$

$\|M\|_{\mathrm F}$: The Frobenius norm. **Domain:** An arbitrary real or complex matrix.

$\|M\|_{\mathrm F}=(\sum_{ij}|M_{ij}|^2)^{1/2}=(\sum_i\sigma_i(M)^2)^{1/2}$

$c,C$: Positive universal constants in the corresponding bound. Identically named constants in different theorems need not have the same value. **Domain:** Independent of the dimension, accuracy, and probability parameters tracked by this bound.

$O,\Omega,\Theta$: Upper, lower, and two-sided bounds up to constants in the same applicable regime **Domain:** Hidden constants have only the parameter dependence explicitly permitted by the associated bound.

$S_{\mathrm{bit}}$: Maximum bit length of the state retained simultaneously during execution **Domain:** $\mathbb N_0$.

$M^\star_{\mathrm{bits}}$: Minimum worst-case bit memory sufficient for the guarantee over the permitted public encodings and input streams **Domain:** $\mathbb N_0\cup\{+\infty\}$.

$\varepsilon_0$: The sufficiently small accuracy constant in the ST reduction. **Domain:** Fixed universal positive constant.

$r_0$: The number of identity-block rows in the ST communication reduction. **Domain:** Auxiliary quantity satisfying the source proof's integer conditions.

$r_0=\Theta(k/\varepsilon),\quad q=n-r_0$

## 3. Complexity bracket

### Compared quantities

#### Q1 - memory complexity

$$
M^\star_{\mathrm{bits}}(m,n,k,\varepsilon)
$$

**Scope.** The algorithm receives the public encoding parameter q. Complexity is worst-case over admissible public encodings and fixed input streams. The source lower bound uses the hard encoding subclass q=n-r_0; it is not claimed for every individually fixed q.

**Optimization direction.** minimize

The public alphabet parameter is $q$. The quantity takes the worst case over admissible encodings; $S_{\mathrm{bit}}$ is the charged persistent-state length in bits.

### R1 - The finite-encoding row-stream lower-bound window.

**Region.** Assume $0<\varepsilon<\varepsilon_0$, $m\ge C_0k/\varepsilon$, and $n\ge C_0k/\varepsilon$. Inputs use the specified exact finite encoding. The constant $C_0,\varepsilon_0>0$ is sufficient in the source theorem.

**Quantity.** Q1

**Resource.** Number of stored bits

**Status.** Polynomial gap

**Achievable budgets.** B2

**Necessary constraints.** No admitted claim in this comparison

**Gap or comparison.** Upper/lower envelope ratio O(m epsilon/k), constant on C_0 k/epsilon <= m <= 2 C_0 k/epsilon within R.

**Comparison argument.** The lower bound and its guard remain conditionally retained from the accepted baseline. The upper bound is charged finite-symbol storage using the existing symbolic-output permission; see MX_S_stream_bits__main__p_store. On R, Omega(nk/epsilon) <= M_bits^star <= O(mn). The envelope ratio is O(m epsilon/k); the stated low-row slab is matched up to universal constants. No finite-bit Frequent Directions claim is adopted.

### R2 - Low-row optimal finite-bit memory

**Region.** R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. ADDITIONALLY m <= 2*C_0*k/epsilon; both sufficient lower inequalities remain inclusive and epsilon<epsilon_0 remains strict.

**Quantity.** Q1

**Resource.** Number of stored bits

**Status.** Optimal

**Achievable budgets.** B2

**Necessary constraints.** No admitted claim in this comparison

**Gap or comparison.** Theta(1) on R intersect {m<=2 C_0 k/epsilon}, with universal source constants.

**Comparison argument.** MX_S_stream_bits__main__p_low_row_closure_20261116

## 4. Bounds and supporting evidence

### B1 - Communication lower bound for randomized one-pass row streams, measured in bits of memory

**Admission.** Included in the bracket

**Direction.** lower

**Witness or lower-bound scope.** The stated restricted randomized class

$$
S_{\mathrm{bit}}\ge c\,\frac{nk}{\varepsilon}
$$

**Sources.** [1](https://papers.neurips.cc/paper/5407-low-rank-approximation-lower-bounds-in-row-update-streams.pdf)

**Conditions.** For this quantity's worst case over admissible public encodings, use the source construction's $q=n-r_0$.

**Dimension conditions.** Assume $m,n\ge C_0k/\epsilon$. The source hard subclass uses integer $r_0=\Theta(k/\epsilon)$ and $q=n-r_0$, requiring $r_0+k$ rows; extra rows may be zero padded.

**Oracle correspondence.** The rows arrive once in a fixed order, with entries exactly encoded over a finite alphabet. Persistent state is finite-bit. Matrix-vector access, rereading, and additional passes are unavailable.

**Guarantee conversion.** Success probability is at least 2/3 for each fixed admissible encoded input. Randomized state transitions are allowed, and the original sufficient-dimension conditions remain in force.

**Output rule.** Return an encoding of a right rank-$k$ subspace, with a $(1+\epsilon)$ relative guarantee for squared Frobenius residual. The hard instance uses only the source's finite alphabet.

**Resource conversion.** The native resource is peak retained bits $S_{\mathrm{bit}}$. One pass is a fixed protocol and is not added to memory cost. Preserve input encoding, working state, and output encoding. The cap holds for each input and private seed. Final output must decode from charged state, without unrecorded external storage.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**memory bits.**

$$
\Omega (nk/eps)
$$

**passes.** 1

**Constants.** Universal constants, with only the parameter dependence permitted by this bound’s region and expression.

**Source location.** [1](https://papers.neurips.cc/paper/5407-low-rank-approximation-lower-bounds-in-row-update-streams.pdf) pdf pages: 2; 3; 4; section: main result and proof; theorem: Theorem 1; construction in §2

ST Theorem 1 gives an $\Omega(nk/\varepsilon)$-bit memory lower bound for a single-pass randomized row stream with only a right-subspace output. Its construction uses $[I,R]$ and standard-basis rows, with entries of $R$ equal to $\pm1/\sqrt q$, $q=n-r_0$, and $r_0=\Theta(k/\varepsilon)$. This hard subclass has the permitted public encoding.

### B2 - Store the exact finite input and return its symbolic optimal spectral subspace

**Admission.** Included in the bracket

**Direction.** upper

**Witness or lower-bound scope.** Randomized computable one-pass streaming algorithms are allowed. The retained state is a finite bit string, including random-generator state under the declared memory model. No span or running-time restriction is added beyond one pass and bit memory.

$$
M^\star_{\mathrm{bits}}(m,n,k,\varepsilon)\le Cmn
$$

**Conditions.** Use the frozen permission for symbolic subspace output interpreted from charged state and public parameters.

**Dimension conditions.** The proof holds on the full target D; native adoption is restricted to MX_S_stream_bits__main__r1.

**Oracle correspondence.** One forward pass in the existing fixed row order; no additional input access.

**Guarantee conversion.** Deterministic success for every admissible fixed stream, hence g1.

**Output rule.** The charged label array with a fixed canonical top-k right-subspace interpretation is a finite symbolic subspace description.

**Resource conversion.** 3mn+O(n+log(mn)+1) charged bits, including buffering, counters, control and the input-dependent output description. Public q is referenced symbolically; no numerical eigensolver is executed by the streaming computation.

**Simultaneous resource costs.** All coordinates refer to this one witness or necessary constraint.

**memory bits.** O(mn)

**passes.** 1

**Constants.** Universal; uniform in m,n,k,epsilon and public q.

**Derivation.** {'baseline_refs': [{'pointer': '/common_specification', 'sha256': 'd7a4a1edd933453a49dbde086da25de983499909559aa204221edb919aa5d248'}, {'pointer': '/views', 'sha256': '45438d4637c770b52fe943888d225ac8fc23175aa5b325522de9dd8581dead62'}, {'pointer': '/quantities/0', 'sha256': 'aacb2dc9226620418624e2942329f7e9680cb76552c97fc3836c1d6dbda3a6a7'}, {'pointer': '/parameters', 'sha256': '5656623b89324a9dc9ef1606fab7c823be839faf219fe80c23ecb74868ab099b'}, {'pointer': '/resource_projections/0', 'sha256': '6475c23b23fc580b42e7a939999b5bbea70b96e7789338cb56a9a7c15ba4dec3'}], 'proof_refs': ['MX_S_stream_bits__main__p_store']}

**Local argument.** MX_S_stream_bits__main__p_store

The complete construction, memory accounting and variational optimality argument are recorded in MX_S_stream_bits__main__p_store. No external theorem or real-register conversion is introduced.

## Maintenance appendix: Native proof extensions

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

Native pointer: /proofs; canonical SHA-256: ec091ceb52b4cb222afc8350decf7ad99e7a7ace979faf55028663e8fecdb308

### Native proof: MX_S_stream_bits__main__p_store

Native pointer: /proofs/0; canonical SHA-256: b02db66812bc0a7b495c1d3cc7f3f604536d74e26f7b6c9435ccc4a40bb218fe

#### Native field: argument

Native pointer: /proofs/0/argument; canonical SHA-256: 243d48c1e810f455cf663e3e8104a5ea2d27fe245d46b5e3b317905e011c6688

#### Native item 1

Native pointer: /proofs/0/argument/0; canonical SHA-256: dc747a2d0003d4840896a52d138c6fbd01fe4ca909758401a13327acef51c0aa

Assign three-bit labels to the five permitted entry values. Duplicate values when q=1 cause no difficulty. Append all mn labels in stream order. A current-row buffer, counters, fixed control and output constructor tag use O(n+log(mn)+1) further bits. Since m,n>=2, the peak and final descriptor sizes are at most 3mn+O(n+log(mn)+1)=O(mn). The bound holds deterministically. Public m,n,k,q are available to the interpretation; no digits of q are stored.

#### Native item 2

Native pointer: /proofs/0/argument/1; canonical SHA-256: c5dfd7d095734e688460fe4170c46f4cb322c6a0025f06e534f782b86d509157

The output is the retained label array interpreted by a fixed symbolic subspace constructor. It denotes the leading k-dimensional eigenspace of G=A^T A, reconstructing A from its labels and public q. To resolve eigenvalue ties, order distinct eigenvalues decreasingly; in each eigenspace project e_1,...,e_n onto that eigenspace and Gram-Schmidt in this order, skipping zero remainders and taking positive normalizing roots. Concatenate the resulting orthonormal lists and select their first k vectors. This uniquely defines P=sum_{j<=k}u_j u_j^T.

#### Native item 3

Native pointer: /proofs/0/argument/2; canonical SHA-256: 58cbd5551693fea510ac675f6acc2517ba7a5d49b43e595f008f60e079a82fe5

This constructor is the mathematical interpretation of the permitted symbolic output, not a numerical eigensolver executed in uncharged working space. Every input-dependent datum in that representation remains in the charged label array. For each integer q all entries are algebraic, and the canonical spectral rule has a computable exact interpretation. No input rereading, external cache, evaluated coordinates or exact-real registers are used by the streaming computation. A model requiring evaluated coordinate output would need a different proof; the frozen view expressly permits symbolic subspace descriptions.

#### Native item 4

Native pointer: /proofs/0/argument/3; canonical SHA-256: 88bcc37f5155766afd78850fa684802cd37a985463aeec3349db271b7aa6d584

Let lambda_1>=...>=lambda_n>=0 be the eigenvalues of G. For any rank-k orthogonal Q, its diagonal weights w_j in this eigenbasis lie in [0,1] and sum to k. Moving weight to larger eigenvalues gives tr(GQ)=sum lambda_j w_j <= sum_{j<=k}lambda_j. The constructed P attains equality, hence ||A(I-P)||_F^2=sum_{j>k}lambda_j.

#### Native item 5

Native pointer: /proofs/0/argument/4; canonical SHA-256: 04bc2cd6465062e84446f20052d8915bc016ce4b9656723760a6e71fc4520af1

For any rank-at-most-k matrix B, extend its row space to a k-dimensional subspace with projector Q. Orthogonality gives ||A-B||_F^2=||A(I-Q)||_F^2+||AQ-B||_F^2 >= sum_{j>k}lambda_j. B=AP attains equality. Thus the output achieves exactly ||A-A_k||_F^2, meeting g1 for every epsilon>0 with probability one. If rank(A)<k, canonical nullspace vectors complete the subspace to rank exactly k, with zero residual.

#### Native item 6

Native pointer: /proofs/0/argument/5; canonical SHA-256: 595595633feefa83ee2bcacb0eef95be84c27cf35e1ff5726eb049adff667338

The construction is uniform in m,n,k,epsilon and public q, including k=1, q=1 and zero optimal residual. Its proof applies on D; this local native adoption is restricted to the unchanged registered R.

#### Native field: baseline_refs

Native pointer: /proofs/0/baseline_refs; canonical SHA-256: d0faefaa833e1eb9ce21d37368cfb2e78bb181c3852c2180560d764bfeeaad33

#### Native item 1

Native pointer: /proofs/0/baseline_refs/0; canonical SHA-256: c444fd99901421500aef7f9e29c71241f806bc4110faea482eb1388c3b61b2a2

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/0/sha256; canonical SHA-256: f2ddce2889314c58271d1038250221b8234bc90e49d6bd25c18046c3bd0aed8d

d7a4a1edd933453a49dbde086da25de983499909559aa204221edb919aa5d248

#### Native item 2

Native pointer: /proofs/0/baseline_refs/1; canonical SHA-256: e20db0113e9aef202c69ceb31d80c41c678aada9abdf4488c9398ad9d461a5d3

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/1/sha256; canonical SHA-256: 06e8f317eadf7aefaa725d4193c6b928b6cedf7e6f0d8fea3e3ae890eb07e7f6

45438d4637c770b52fe943888d225ac8fc23175aa5b325522de9dd8581dead62

#### Native item 3

Native pointer: /proofs/0/baseline_refs/2; canonical SHA-256: ed768b118170d56e834b4e5ea13b129ebaa21814f53023d6a057856167aa40d4

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/2/pointer; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/2/sha256; canonical SHA-256: 2df29bcdddc0297aad2b6cfaa953703f0b0a204d784ab3a59f1b4083547d8d10

aacb2dc9226620418624e2942329f7e9680cb76552c97fc3836c1d6dbda3a6a7

#### Native item 4

Native pointer: /proofs/0/baseline_refs/3; canonical SHA-256: eb0a5534eb899243ef52164c0a7118492a83322a2e445f48dfa7f167e7f008bb

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/3/pointer; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/3/sha256; canonical SHA-256: 636e4ed2cc7986b466c1f1a4db3b3bf67689c3a493883009349c0f282327e622

5656623b89324a9dc9ef1606fab7c823be839faf219fe80c23ecb74868ab099b

#### Native item 5

Native pointer: /proofs/0/baseline_refs/4; canonical SHA-256: fc6a60e605ca7ed5f0685770064d8658fe70b74428f4228351c3e56cf9a41e6a

#### Native field: pointer

Native pointer: /proofs/0/baseline_refs/4/pointer; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native field: sha256

Native pointer: /proofs/0/baseline_refs/4/sha256; canonical SHA-256: 5438bbe4f1cc21451a62e17fc15daa730792ee65b361b2de9c171dcf10f42d0b

6475c23b23fc580b42e7a939999b5bbea70b96e7789338cb56a9a7c15ba4dec3

#### Native field: conclusion

Native pointer: /proofs/0/conclusion; canonical SHA-256: 231689df5dc8cd95169b5c00ed8b801b560f7ac542395a8e642170eecea6b421

M_bits^star <= 3mn+O(n+log(mn)+1)=O(mn), with universal constants and no dependence on public q.

#### Native field: source_refs

Native pointer: /proofs/0/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: statement

Native pointer: /proofs/0/statement; canonical SHA-256: c370398dccf8b4c29152b99838bb7ee04d52de879150bdab937937668cfbcb3f

Under the existing symbolic-subspace-output contract, deterministic one-pass storage of the finite entry labels achieves the optimal rank-k squared Frobenius residual with O(mn) charged bits.

### Native proof: MX_S_stream_bits__main__p_low_row_closure_20261116

Native pointer: /proofs/1; canonical SHA-256: 1e22f8ef3d6170376bf7997993c5bad3f1d3a4c1e1ed361309e18f80f2df258a

#### Native field: baseline_refs

Native pointer: /proofs/1/baseline_refs; canonical SHA-256: fa0a2f243723866ebd1026d10b321817f677f7d20626c056d89af1286af026ee

#### Native item 1

Native pointer: /proofs/1/baseline_refs/0; canonical SHA-256: c444fd99901421500aef7f9e29c71241f806bc4110faea482eb1388c3b61b2a2

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/0/pointer; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/0/sha256; canonical SHA-256: f2ddce2889314c58271d1038250221b8234bc90e49d6bd25c18046c3bd0aed8d

d7a4a1edd933453a49dbde086da25de983499909559aa204221edb919aa5d248

#### Native item 2

Native pointer: /proofs/1/baseline_refs/1; canonical SHA-256: e20db0113e9aef202c69ceb31d80c41c678aada9abdf4488c9398ad9d461a5d3

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/1/pointer; canonical SHA-256: 5063a21a606682113dc69ed6b9d72fe0dd7e6e4567bf7d12d974c9929ec16acf

/views

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/1/sha256; canonical SHA-256: 06e8f317eadf7aefaa725d4193c6b928b6cedf7e6f0d8fea3e3ae890eb07e7f6

45438d4637c770b52fe943888d225ac8fc23175aa5b325522de9dd8581dead62

#### Native item 3

Native pointer: /proofs/1/baseline_refs/2; canonical SHA-256: a7cbb4789dd60388d35c619cfda518031787f4a06d0f85f3193f623dce4d590c

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/2/pointer; canonical SHA-256: 526f619ec2b99bd98a91f820f937aadd19d267cc4478f18fb787bb37e25a782b

/quantities

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/2/sha256; canonical SHA-256: 4adee316507ebd41d34b8d1c0be6dc311a8c0e9925caf35a949a594e52cce5fc

b938ec24b5a91e0555a83e8b01bc9aced9d9eadc98a6ef0e86a1c03f6f1c84e6

#### Native item 4

Native pointer: /proofs/1/baseline_refs/3; canonical SHA-256: 3dfb92feed1901f248442f03a28b475c50138a9249a2526aa2e953b6a98e5754

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/3/pointer; canonical SHA-256: 3dfac9f90fd7e6e77d27fde2e31446ad9c96322c69f01c50e3ad5f465d990791

/resource_projections

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/3/sha256; canonical SHA-256: 7ab644c20dab74a63879f40fc5121926bceaf07f0c9d634d13a415802285c19a

51c7909c60f9e84405453ba5c3393eab714c47afa234f008efa19de9cdf3cd57

#### Native item 5

Native pointer: /proofs/1/baseline_refs/4; canonical SHA-256: 40bfea280563dc90602dc4883f05a870253d23dfa7211eb95804729a79b28819

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/4/pointer; canonical SHA-256: 75e7040ee9b7f6bb53623ed289617ff0705a4d81718776cbba42cdc3e6039b04

/bounds

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/4/sha256; canonical SHA-256: 7c5b7a55f2cebc763f1cfadc9ebd56e5f9786c044456acbc6bb6d3038cc3f293

11b9ccd4517bfd25da92456c47ffec116702433a4275cad0993b0751e5e724d3

#### Native item 6

Native pointer: /proofs/1/baseline_refs/5; canonical SHA-256: 8767319da44905a4d92dc77e465afd5cd54f8bdbadf937b6aa7e68cf0d3aa38a

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/5/pointer; canonical SHA-256: b5a3c8e5a69ebbfa3a635cdb498215b14ffa316a5c88100937281d883417d1bf

/proofs

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/5/sha256; canonical SHA-256: 84c75042f759c53944f2d227e246a831cb22921da5c20ff0656a0bd3ff758109

34262234f82f6cd5a2c441713a237e8b223929613a9f58d04797dbcab33a9f29

#### Native item 7

Native pointer: /proofs/1/baseline_refs/6; canonical SHA-256: 214bb7164971a259fc5bfb4428717dca8b5873de7e48dd97d831d0fe8ac02818

#### Native field: pointer

Native pointer: /proofs/1/baseline_refs/6/pointer; canonical SHA-256: 827389749d3001e88ba1259848cb6989c8ddd64d1399694733d555d9bbe48702

/joint_analysis

#### Native field: sha256

Native pointer: /proofs/1/baseline_refs/6/sha256; canonical SHA-256: 8b0960b8814392eec20a823b1b43a3f201b4f6fd14d211ea1058f7e75483ccae

979b47eae020888556824eade78ffb22db83e0c3aeb3bc7d7651632698bcf131

#### Native field: body

Native pointer: /proofs/1/body; canonical SHA-256: 86f67a682ed982515f7122f08babe0d3e01e26362a2cc82f06d730206817cf19

Retain the exact accepted native b1 lower and b2 upper, including their view main/g1/q1/resource and all original R guards. The minimax quantity is worst-case over the admissible public encodings q, not an individually fixed-q complexity. The b1 source construction supplies S_bits^star >= c n k/epsilon on R. The fully charged deterministic construction p_store supplies S_bits^star <= 3mn+O(n+log(mn)+1) <= C mn with universal C on D, uniformly in the public q, using the existing symbolic-output contract and no additional input access. Since k<min(m,n), both m,n>=2 and the stated overhead is absorbed uniformly. On S=R intersect{m<=2 C_0 k/epsilon}, the upper is at most 2 C C_0 n k/epsilon. Thus c n k/epsilon <= S_bits^star <= 2 C C_0 n k/epsilon: Theta(nk/epsilon), with only universal source constants C_0,epsilon_0 fixed, never hiding m,n,k,epsilon or q. This also equals Theta(mn) on S since C_0 k/epsilon<=m<=2 C_0 k/epsilon. The upper succeeds deterministically and has the native pathwise memory cap, hence preserves per-input success >=2/3. Its finite-label charged output handles zero optimal residual and rank deficiency by the existing canonical exact spectral interpretation; we do not replace it with a numerical coordinate-output algorithm or free external eigensolver. No new output, finite precision, RAM-word, oracle/pass or q-pointwise assumption is introduced. S is nonempty as a parameter region: set k=1, choose epsilon=min(epsilon_0/2,C_0/4,1/4)>0, and m=n=ceil(C_0/epsilon); C_0/epsilon>=4 ensures m<=2 C_0/epsilon and k<min(m,n). The source lower still ranges over its own legal encoding subclass, not necessarily q=1. The equality m=2 C_0 k/epsilon is included whenever integral; epsilon=epsilon_0 is not. Outside S the old c1 remains polynomial_gap on R, and D minus R remains unassessed. This is publication of a closure already explicitly stated in the baseline joint annotation, not a new source theorem, a strict extension beyond R, or a full-domain minimax solution.

#### Native field: scope

Native pointer: /proofs/1/scope; canonical SHA-256: fe416cf855abcf4bf7805e7143b9aabea734093cc00d40b27a012dfd69522426

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. ADDITIONALLY m <= 2*C_0*k/epsilon; both sufficient lower inequalities remain inclusive and epsilon<epsilon_0 remains strict.

#### Native field: source_refs

Native pointer: /proofs/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: title

Native pointer: /proofs/1/title; canonical SHA-256: c216c5acd926ed3e6ed975261adc3df5f22ee6b95537a873c59564e74860d26c

Native low-row finite-bit matching-bracket publication

## Maintenance appendix: Complete native joint analysis

Read-only presentation of the stored native record. Integrity hashes identify source values; this appendix grants no new theorem, source-read credit, review or approval.

### Native joint analysis

Native pointer: /joint_analysis; canonical SHA-256: 9462d5eb6d19af9551377b3b816c88aa6fa2741fcf2f5474c345637e929c1e38

#### Native field: comparisons

Native pointer: /joint_analysis/comparisons; canonical SHA-256: ed3434b402d1f755791a64a8646441c50158db89ee9275c5790bc87790d48d4f

#### Native item 1

Native pointer: /joint_analysis/comparisons/0; canonical SHA-256: 59171f75bec4a2e1d2aea9fc18f1c5848b63aed7b128f9030d290cd1614ef164

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/0/bound_uses; canonical SHA-256: 71ca7da0c63683de465f03b12474bb36d66959f61abb0d3a5c9a04c5945a6fab

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/0; canonical SHA-256: 64167ab62607ab47026afe41f5188e4e130fdb5ec5c98ad784b036e2a757237e

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/adopted_region; canonical SHA-256: 566ea0542be1acaae3138a60ce83e604d7b71c48d1c996cbed8f676e5ad9fd0c

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/bound_id; canonical SHA-256: a7c3e8260e2c6d4cc31f95eeeaab96b247225cc32936599de80b6bae2779f498

MX_S_stream_bits__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/mapping_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/reason; canonical SHA-256: f8b51408a18dfcffce22c0c55e9b5eabbbefb8ec242b69f6935dbb2c82837209

Conditionally retain the exact accepted lower row and its source-construction guard. The hard encoding q=n-r_0 is a permitted subclass of the worst-case-over-encodings quantity; no pointwise-in-q extrapolation is made.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/0/validity_region; canonical SHA-256: 566ea0542be1acaae3138a60ce83e604d7b71c48d1c996cbed8f676e5ad9fd0c

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/bound_uses/1; canonical SHA-256: 47df0d4cb5cbb0cfa0a2cfd1b556b40cfbbc0099809cdcceb38968541b3eab9c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/adopted_region; canonical SHA-256: 566ea0542be1acaae3138a60ce83e604d7b71c48d1c996cbed8f676e5ad9fd0c

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/bound_id; canonical SHA-256: c73827c3acfd43062f4a30acf4f5eae672cb612752fa25221223d10a0aa07957

MX_S_stream_bits__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs; canonical SHA-256: ea5fd11201c23f2962f44289d94c62b88337130af9bbfdab1f3edac108e2035e

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 845522c0eaaf2958da61e20a725b74cfd024a3c6d2783a22e91f2f150f0bf0d4

MX_S_stream_bits__main__p_store

#### Native field: reason

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/reason; canonical SHA-256: d39def8d3925dabfe84dadd2e95529d15938799f7e729449fa0864287ef08d94

Three-bit entry labels and the permitted symbolic optimal-subspace description give deterministic O(mn) bits. All input-dependent output data stay in charged state; proof MX_S_stream_bits__main__p_store.

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/0/bound_uses/1/validity_region; canonical SHA-256: 8702361d50a3def74b1ca81ba8b9478c494a9b17848c3108730c359ef513101f

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/0/boundary_checks; canonical SHA-256: 6fa42b3641dca18b28e7b21cbcd9acabde815f38f02a3f2656f016374f7b167a

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/boundary_checks/0; canonical SHA-256: 1b560be153c7e454ca86dcc6b76174916b2f515202cf6fd6016ae6d80d26b1a8

The strict epsilon < epsilon_0 guard is preserved; no lower-bound assertion is extended to epsilon=epsilon_0.

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/boundary_checks/1; canonical SHA-256: 5895cb40830ba57fce6300c717df722962d05af6eab20fa63dc740092ca9682a

The sufficient inequalities m,n >= C_0 k/epsilon are retained inclusively. These are source activation conditions, not established intrinsic phase transitions.

#### Native item 3

Native pointer: /joint_analysis/comparisons/0/boundary_checks/2; canonical SHA-256: 036c32fea6e972b0f6514630799231bb419bdf97d75cfcb0151b5014497def3c

As epsilon decreases at fixed finite m,n,k, the source window eventually fails. The storage proof remains finite and precision independent because its symbolic output is exactly optimal, so there is no extrapolation of nk/epsilon beyond the guard.

#### Native item 4

Native pointer: /joint_analysis/comparisons/0/boundary_checks/3; canonical SHA-256: 0e074b92a968656caa6de718d1551c1075ece1e46913e651c62cc8935374e707

On the low-row slab C_0 k/epsilon <= m <= 2 C_0 k/epsilon, upper O(mn) is O(nk/epsilon); the retained lower side closes the rate there. This is an asymptotic rate statement with universal source constants.

#### Native item 5

Native pointer: /joint_analysis/comparisons/0/boundary_checks/4; canonical SHA-256: c7623ae70787a6718469a633e6132fd561597739a4ade7d0f1b63595baff9965

If rank(A)<k or A=0, the canonical nullspace completion gives rank exactly k and zero residual. No positive-optimum rounding assumption is used.

#### Native item 6

Native pointer: /joint_analysis/comparisons/0/boundary_checks/5; canonical SHA-256: 7e1ac3ec2ce90cef4a11680faf1e94e5226113ebc48778297b99a907100a2e3b

k=1 and q=1 satisfy the construction. Since k<min(m,n), m=1 or n=1 and k=n are outside the target. Row-call and pass counts are fixed protocol quantities; no zero-bit or one-call result is asserted.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/0/comparison_id; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/0/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/0/fixed_parameters; canonical SHA-256: b3919ce9ac53b03f848cdd150ae1749d2526ca8e950b07ce6b8e781399430ba0

#### Native item 1

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/0; canonical SHA-256: e2139ce8ac0004812b0693b1a06e2fd2ffac12e112d5130e9e0ed2bc54d984b3

C_0

#### Native item 2

Native pointer: /joint_analysis/comparisons/0/fixed_parameters/1; canonical SHA-256: 007ab56c0578075b0e94c1c78d87a220040d30a5282eb4be7b2b4e2a54800403

epsilon_0

#### Native field: gap

Native pointer: /joint_analysis/comparisons/0/gap; canonical SHA-256: d6d774d24d24415887f48a164d75e30a1afebc9b87d6c0c151fc4cca5735f631

The ratio of these recorded upper/lower rates is O(m epsilon/k). They match up to universal constants on R intersect {m <= 2 C_0 k/epsilon}. The joint window permits this ratio to grow with m; no globally sharp rate is claimed.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/0/lower_envelope; canonical SHA-256: abfb5dbf9fcd9797daa1f3e07427bada929c0fb142b3414a860e8a5bb89d0778

Omega(nk/epsilon) on R, conditionally retained from MX_S_stream_bits__main__b1.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/0/remaining_gap; canonical SHA-256: 894b7538eebbfeb35cfa78636d4e86482c05b8d1ddc6139a40ec5daa0c0b34b7

A potentially growing factor O(m epsilon/k) remains between the recorded rates outside the low-row slab. Stronger finite-bit sketching and complementary-domain brackets remain unassessed.

#### Native field: role

Native pointer: /joint_analysis/comparisons/0/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/0/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/0/upper_envelope; canonical SHA-256: 4acc7ac3354095fbba2e2c538d2fa9b488fae58c1e739b0b8db4c72dc12b0850

O(mn) on R, from MX_S_stream_bits__main__b2.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1; canonical SHA-256: f71413b4ce7486f619dca2879af98a2588f36858c1f5f0e7858f52a67059c35d

#### Native field: bound_uses

Native pointer: /joint_analysis/comparisons/1/bound_uses; canonical SHA-256: 06346c2e4467202cd666b258de47780acf0bb422b46a8215d47dd78b552c33c3

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0; canonical SHA-256: d0a37bdd0dd5a347167096e58e292e17756e5474fd087433be7bad7660a0c2f9

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/adopted_region; canonical SHA-256: fe416cf855abcf4bf7805e7143b9aabea734093cc00d40b27a012dfd69522426

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. ADDITIONALLY m <= 2*C_0*k/epsilon; both sufficient lower inequalities remain inclusive and epsilon<epsilon_0 remains strict.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/bound_id; canonical SHA-256: a7c3e8260e2c6d4cc31f95eeeaab96b247225cc32936599de80b6bae2779f498

MX_S_stream_bits__main__b1

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs; canonical SHA-256: db714892c1916841da733b62999b549e257557fb2d154eb5d32f8f381907fda0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/mapping_proof_refs/0; canonical SHA-256: 5d3ee89d8afb05ffe7950bf00588162028a598b71cdec1df79499fafadfd945e

MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/reason; canonical SHA-256: c865ca97d9c2de7529d17317544cbb29216e3942ce8ae1f9264218a92bd9c5cd

Exact same quantity/view/guarantee/resource; original bound plus low-row algebra in MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/0/validity_region; canonical SHA-256: 566ea0542be1acaae3138a60ce83e604d7b71c48d1c996cbed8f676e5ad9fd0c

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/bound_uses/1; canonical SHA-256: b9c1f31c44882dec106f1945f5058298d86c64c589cfdd13def81fafb619051c

#### Native field: adopted_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/adopted_region; canonical SHA-256: fe416cf855abcf4bf7805e7143b9aabea734093cc00d40b27a012dfd69522426

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. ADDITIONALLY m <= 2*C_0*k/epsilon; both sufficient lower inequalities remain inclusive and epsilon<epsilon_0 remains strict.

#### Native field: bound_id

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/bound_id; canonical SHA-256: c73827c3acfd43062f4a30acf4f5eae672cb612752fa25221223d10a0aa07957

MX_S_stream_bits__main__b2

#### Native field: disposition

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/disposition; canonical SHA-256: 531cecca496a7f46e4aa9ef40641db12f8bef53aaa6b67c429d2c0717dc599ce

included

#### Native field: mapping_proof_refs

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs; canonical SHA-256: db714892c1916841da733b62999b549e257557fb2d154eb5d32f8f381907fda0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/mapping_proof_refs/0; canonical SHA-256: 5d3ee89d8afb05ffe7950bf00588162028a598b71cdec1df79499fafadfd945e

MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native field: reason

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/reason; canonical SHA-256: c865ca97d9c2de7529d17317544cbb29216e3942ce8ae1f9264218a92bd9c5cd

Exact same quantity/view/guarantee/resource; original bound plus low-row algebra in MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native field: validity_region

Native pointer: /joint_analysis/comparisons/1/bound_uses/1/validity_region; canonical SHA-256: 8702361d50a3def74b1ca81ba8b9478c494a9b17848c3108730c359ef513101f

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity.

#### Native field: boundary_checks

Native pointer: /joint_analysis/comparisons/1/boundary_checks; canonical SHA-256: 732fcf32b23a8acd606ccbbee23ae942bfe7ad8c36c9c638a3702ae6f814b761

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/boundary_checks/0; canonical SHA-256: 1b560be153c7e454ca86dcc6b76174916b2f515202cf6fd6016ae6d80d26b1a8

The strict epsilon < epsilon_0 guard is preserved; no lower-bound assertion is extended to epsilon=epsilon_0.

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/boundary_checks/1; canonical SHA-256: 5895cb40830ba57fce6300c717df722962d05af6eab20fa63dc740092ca9682a

The sufficient inequalities m,n >= C_0 k/epsilon are retained inclusively. These are source activation conditions, not established intrinsic phase transitions.

#### Native item 3

Native pointer: /joint_analysis/comparisons/1/boundary_checks/2; canonical SHA-256: 036c32fea6e972b0f6514630799231bb419bdf97d75cfcb0151b5014497def3c

As epsilon decreases at fixed finite m,n,k, the source window eventually fails. The storage proof remains finite and precision independent because its symbolic output is exactly optimal, so there is no extrapolation of nk/epsilon beyond the guard.

#### Native item 4

Native pointer: /joint_analysis/comparisons/1/boundary_checks/3; canonical SHA-256: 0e074b92a968656caa6de718d1551c1075ece1e46913e651c62cc8935374e707

On the low-row slab C_0 k/epsilon <= m <= 2 C_0 k/epsilon, upper O(mn) is O(nk/epsilon); the retained lower side closes the rate there. This is an asymptotic rate statement with universal source constants.

#### Native item 5

Native pointer: /joint_analysis/comparisons/1/boundary_checks/4; canonical SHA-256: c7623ae70787a6718469a633e6132fd561597739a4ade7d0f1b63595baff9965

If rank(A)<k or A=0, the canonical nullspace completion gives rank exactly k and zero residual. No positive-optimum rounding assumption is used.

#### Native item 6

Native pointer: /joint_analysis/comparisons/1/boundary_checks/5; canonical SHA-256: 7e1ac3ec2ce90cef4a11680faf1e94e5226113ebc48778297b99a907100a2e3b

k=1 and q=1 satisfy the construction. Since k<min(m,n), m=1 or n=1 and k=n are outside the target. Row-call and pass counts are fixed protocol quantities; no zero-bit or one-call result is asserted.

#### Native item 7

Native pointer: /joint_analysis/comparisons/1/boundary_checks/6; canonical SHA-256: 623f946ef3e40aac0c0d6da4b8af9eb90858651c8f535ebc21027dbf43dd5d14

m<=2 C_0 k/epsilon included; m,n>=C_0 k/epsilon and strict epsilon<epsilon_0 retained.

#### Native item 8

Native pointer: /joint_analysis/comparisons/1/boundary_checks/7; canonical SHA-256: 8463a57a6dfbbdebad5a4e52dbd78c4b70ed131c814009282f569f48f01f0756

The public q remains internal to the minimax worst case; no pointwise-q lower is asserted.

#### Native field: comparison_id

Native pointer: /joint_analysis/comparisons/1/comparison_id; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: constant_dependencies

Native pointer: /joint_analysis/comparisons/1/constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: fixed_parameters

Native pointer: /joint_analysis/comparisons/1/fixed_parameters; canonical SHA-256: b3919ce9ac53b03f848cdd150ae1749d2526ca8e950b07ce6b8e781399430ba0

#### Native item 1

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/0; canonical SHA-256: e2139ce8ac0004812b0693b1a06e2fd2ffac12e112d5130e9e0ed2bc54d984b3

C_0

#### Native item 2

Native pointer: /joint_analysis/comparisons/1/fixed_parameters/1; canonical SHA-256: 007ab56c0578075b0e94c1c78d87a220040d30a5282eb4be7b2b4e2a54800403

epsilon_0

#### Native field: gap

Native pointer: /joint_analysis/comparisons/1/gap; canonical SHA-256: b8ff3c68e6934e9a9f9a4b777cb1346ff056ea90d57902051e68569543e2e925

Theta(1), universal constants only.

#### Native field: lower_envelope

Native pointer: /joint_analysis/comparisons/1/lower_envelope; canonical SHA-256: c7088df800e69594391419eba18ee45b5ea6761c149e68b135ba13bb64164449

Omega(nk/epsilon) under the unchanged entire R source guard.

#### Native field: remaining_gap

Native pointer: /joint_analysis/comparisons/1/remaining_gap; canonical SHA-256: bda75671bbc82388d238cb1c938866e9e26da2ec91ed86a6392f64885d8775da

No rate gap on this declared slab. Native output and conditional retained lower-source premises are unchanged. No largest matching slab or global optimality is asserted.

#### Native field: role

Native pointer: /joint_analysis/comparisons/1/role; canonical SHA-256: 8f94b762b3127329eb134abfe8b8ca262f59c15e9c4e0e3f86d45886d57a82de

joint

#### Native field: slice

Native pointer: /joint_analysis/comparisons/1/slice; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: upper_envelope

Native pointer: /joint_analysis/comparisons/1/upper_envelope; canonical SHA-256: c61bfc4485ae810c9a57ea61c2e7c6e6e102a814fc346bb6097bb8504ad8bf3d

O(nk/epsilon) from O(mn) and m<=2 C_0 k/epsilon.

#### Native field: domain_map

Native pointer: /joint_analysis/domain_map; canonical SHA-256: f1caceaf527ba8d1db05b23cd877876f147100c6ed450db75a8723a31052b030

#### Native field: cells

Native pointer: /joint_analysis/domain_map/cells; canonical SHA-256: 1a94dac3f0e08c39cb7adb8bb128135ba735098e997047d802a600ff00edd9fd

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0; canonical SHA-256: eb1470294e1de0b08a4676f8fbed52a1a2c5bf7b6790e5699aaf2223dda211ea

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/0/cell_id; canonical SHA-256: 06c7fc37629d9ddfd2aecff6a505232e98ef7ce990719406b2afe8c7551aecda

low_row_closed

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/0/closure; canonical SHA-256: 44627aad0023fb7cff9c3b30d64b42dd30e9a6c598f67caebb1c397608c05caf

established

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs; canonical SHA-256: db714892c1916841da733b62999b549e257557fb2d154eb5d32f8f381907fda0

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/closure_proof_refs/0; canonical SHA-256: 5d3ee89d8afb05ffe7950bf00588162028a598b71cdec1df79499fafadfd945e

MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids; canonical SHA-256: f617877c937165d4da9e1f8db5900fc14b27ac6e5d7951dce7d844cae9bd4264

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/0/comparison_ids/0; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/0/note; canonical SHA-256: 95558ff0e4a31d407c0fd9ad6f00dc6480543dfc8c4a0f7b3abb637b8c7041c4

Already-derived matching slab now has a native optimal comparison; conditional retained source premise, no strict new-domain claim.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/0/predicate; canonical SHA-256: fe416cf855abcf4bf7805e7143b9aabea734093cc00d40b27a012dfd69522426

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. ADDITIONALLY m <= 2*C_0*k/epsilon; both sufficient lower inequalities remain inclusive and epsilon<epsilon_0 remains strict.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/0/publication; canonical SHA-256: a69462fe54b27704b355b6dec96d5354e1787d3558bb014af0138fca1c0a04a0

native_comparison

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/0/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/0/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 2

Native pointer: /joint_analysis/domain_map/cells/1; canonical SHA-256: 4c374dbce9772dbc4f6c5ab118b6098f73db13aac58af2101a9b39b2389d0d0d

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/1/cell_id; canonical SHA-256: 80e675e0cf2b3ff1a1bc0f779d95b03ec97b717fab4b5633d4096adb9bde4e81

registered_window_outside_low_row

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/1/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/1/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids; canonical SHA-256: 95ac95ef4cc7b4da0b6b0a8ba71a933821bcb9e348991e1093d4f6c168826a84

#### Native item 1

Native pointer: /joint_analysis/domain_map/cells/1/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/1/note; canonical SHA-256: 0f0b5557c6590743b8815b28cf90e4f6a9be652d7f096aa31d5f0afbd2f263aa

Old broad c1 remains polynomial_gap; stronger rates are unassessed.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/1/predicate; canonical SHA-256: ab9652710f37646130c65c0ab96f843bde315dc3bd4629a1991d3e50e66a7afe

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. AND m>2*C_0*k/epsilon

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/1/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/1/role; canonical SHA-256: 1b1fe0e945e26ad153b0c6e5a2c8d455f335b5494422c167d6c3f82d99f1da92

joint_region

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/1/state; canonical SHA-256: bfb102db3cbcffdcf0a4e0c3eac375212a53ed39ea018e0164ca2b33d711c834

bounds_recorded

#### Native item 3

Native pointer: /joint_analysis/domain_map/cells/2; canonical SHA-256: 4e697caeb83060ddd22a5d50a33fd59fa163a6045045abd4c99ba7966682ed10

#### Native field: cell_id

Native pointer: /joint_analysis/domain_map/cells/2/cell_id; canonical SHA-256: 7e767166fae7ad55199595f15b014cd0120df03c878b93d835e19b9b9bc8eb8f

unassessed_complement

#### Native field: closure

Native pointer: /joint_analysis/domain_map/cells/2/closure; canonical SHA-256: c1672a184c5e9c7f4ad1d8e613a970b1a4eb14b001d5b8b0c47a3ee5c8d86d8a

not_claimed

#### Native field: closure_proof_refs

Native pointer: /joint_analysis/domain_map/cells/2/closure_proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/domain_map/cells/2/comparison_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: note

Native pointer: /joint_analysis/domain_map/cells/2/note; canonical SHA-256: 06d870967d100080cbb350ddb88f5761c2b4dd3408407cd6786bcd0b3f74f5b4

The storage proof is valid here, but native adoption and bracket assembly in this local proposal cover R. No lower-side or optimality conclusion is made for the complement.

#### Native field: predicate

Native pointer: /joint_analysis/domain_map/cells/2/predicate; canonical SHA-256: a132ae46bd1f59191521511e65417b300a5a4adeef0c2ca7c47eb63b5cd141c3

D outside R: epsilon >= epsilon_0 or m < C_0 k/epsilon or n < C_0 k/epsilon, subject to D.

#### Native field: publication

Native pointer: /joint_analysis/domain_map/cells/2/publication; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: role

Native pointer: /joint_analysis/domain_map/cells/2/role; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: state

Native pointer: /joint_analysis/domain_map/cells/2/state; canonical SHA-256: 74290158c1d7358ba35f80dfe316caf17a6c837914836d2fec5bc5cfac234003

unassessed

#### Native field: partition_argument

Native pointer: /joint_analysis/domain_map/partition_argument; canonical SHA-256: c4909609fd2e3a10e9693274b34d7165a31b0260beb69de91c162230ee75192b

Within R the predicates m<=2 C_0 k/epsilon and m>2 C_0 k/epsilon partition it exactly; together with D outside R they partition D. c1 remains the broad nonoptimal native comparison, and c2 publishes only the matching subregion. This is not new coverage outside the previously registered R.

#### Native field: residual_domain

Native pointer: /joint_analysis/domain_map/residual_domain; canonical SHA-256: ad80631bb50e530bfce0ec685dbc994b292515749f4f6a06ba35f79d83b65a69

D outside R is explicitly unassessed as a bracket. No target points are silently omitted.

#### Native field: status

Native pointer: /joint_analysis/domain_map/status; canonical SHA-256: 4f62e2d589ff517ecc4f19af0681d4da8258888404419debd532d6d7cfaefde0

accounted

#### Native field: impact

Native pointer: /joint_analysis/impact; canonical SHA-256: 6f32fbee9258fd037b699dca92bf159bf5794227aaf48c004c636e9d41cb258f

#### Native item 1

Native pointer: /joint_analysis/impact/0; canonical SHA-256: e7acdb6644d174aeee1a6e5045d038995c0c60ecd669e8fd5a770bb3eecb3cfc

#### Native field: argument

Native pointer: /joint_analysis/impact/0/argument; canonical SHA-256: 0a50af9ac8bdd2a5a504f731a6f01e548d321b40669404cdb08786b77fd32e1c

The complete charged-state construction is MX_S_stream_bits__main__p_store. Dividing O(mn) by Omega(nk/epsilon) gives O(m epsilon/k). Filling the upper side does not assert that full storage is optimal throughout R.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/0/boundary_type; canonical SHA-256: 78e6d55e7765ffb0df4f9ea66fe2223a14c7d96737509bcd9a33e16cf708d733

asymptotic

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/0/comparison_ids; canonical SHA-256: 95ac95ef4cc7b4da0b6b0a8ba71a933821bcb9e348991e1093d4f6c168826a84

#### Native item 1

Native pointer: /joint_analysis/impact/0/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/0/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/0/finding_id; canonical SHA-256: c232521d181ae8a6404310d6227108d5f5266c6c2d66d136db8a97d76f1ae253

finite_label_storage_upper

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/0/improvement_region; canonical SHA-256: e746baae1d5335691df168023876edd21061211158d78e0545995f50a9d7345c

All of R receives a previously missing upper side. The rate is newly matched up to constants on R intersect {m <= 2 C_0 k/epsilon}.

#### Native field: kind

Native pointer: /joint_analysis/impact/0/kind; canonical SHA-256: c79804a9af09f202b7176fc199502111d6b5758795913d2e7758fb9d2c622133

bound_improvement

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/0/new_envelope; canonical SHA-256: cd3151ba728df2602177c1f5b0f29d80334015df8875defffc0012108dccfb2c

On R: lower Omega(nk/epsilon); upper O(mn).

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/0/old_envelope; canonical SHA-256: 8438b7f57d10aa3ae9452fbf7cc5823920ebdb0b58f27436c6b1987916d24bc4

On R: lower Omega(nk/epsilon); upper missing.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/0/unchanged_region; canonical SHA-256: ef966b4dcfad27862ef95c9978e89a4dfb4f43cc0b3bff21c4715c6cb51db6d1

The retained lower formula and guard are unchanged. Native brackets outside R are not changed.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/0/validity_region; canonical SHA-256: 8702361d50a3def74b1ca81ba8b9478c494a9b17848c3108730c359ef513101f

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity.

#### Native field: witness

Native pointer: /joint_analysis/impact/0/witness; canonical SHA-256: 31706f647d9102324c564725538a0b2d264d3c9d088b8783114979d08083c1f0

For any admissible point of R the explicit finite-label algorithm supplies an upper bound where none was registered; taking m between C_0 k/epsilon and 2 C_0 k/epsilon makes both recorded rates Theta(nk/epsilon).

#### Native item 2

Native pointer: /joint_analysis/impact/1; canonical SHA-256: 1888266bd24a007df6dd4528d2ab94038433ddcee9bf78ad96f124f014adce94

#### Native field: argument

Native pointer: /joint_analysis/impact/1/argument; canonical SHA-256: 064f2dbeece271c199da249c946b37715294c4675b957c6dfb9712df43e95700

This is the first joint annotation, based on fully read frozen records. It preserves the worst-case-over-q quantity and the four native joint variables without metadata normalization.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/1/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/1/comparison_ids; canonical SHA-256: 95ac95ef4cc7b4da0b6b0a8ba71a933821bcb9e348991e1093d4f6c168826a84

#### Native item 1

Native pointer: /joint_analysis/impact/1/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/1/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/1/finding_id; canonical SHA-256: efeda344d67933de0a2a0000453b1af19597369b5066048675b2f359c3a92eed

initial_joint_annotation

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/1/improvement_region; canonical SHA-256: dfb563b513a1adc927d0973f9fab3f779e30dec27f779f7b56c21b928a2d0dbd

No mathematical bound improvement is attributed to this presentation finding.

#### Native field: kind

Native pointer: /joint_analysis/impact/1/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/1/new_envelope; canonical SHA-256: f58c72b751d2c7d53298732709620025625fdf9ece400bbb38e7e2ed35a9397b

The retained lower guard, parameter roles and complement are explicit. The separate storage finding alone supports the scientific upper/status change.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/1/old_envelope; canonical SHA-256: 397d75d55726e16e830f2dd2488411eac4c7e38734673e396f7a7e85dd562010

The frozen profile had one guarded lower bound, a missing upper side and no joint analysis.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/1/unchanged_region; canonical SHA-256: f312cc067196972e8fdc33d7a1b08b70cdf0a909472799ef6f18792447b93581

All frozen scientific rows and guards covered by this finding; the separately justified new upper is not a presentation edit.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/1/validity_region; canonical SHA-256: 8702361d50a3def74b1ca81ba8b9478c494a9b17848c3108730c359ef513101f

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity.

#### Native field: witness

Native pointer: /joint_analysis/impact/1/witness; canonical SHA-256: 425961257009d0408b6b56c56fbe6ad83a939690ce45a32e95b40d174c13feff

The complete mechanical candidate inventory contains only MX_S_stream_bits__main__b1; it is explicitly included with its original guard, and D outside R is recorded as unassessed.

#### Native item 3

Native pointer: /joint_analysis/impact/2; canonical SHA-256: e2736824117d5046d94001e5de693ee06a53ecf8a69f8e875f8b8a26f9652044

#### Native field: argument

Native pointer: /joint_analysis/impact/2/argument; canonical SHA-256: 74a54690de9b4cae50514b814acabd053e7a6080cc498eef1f22d084981e9284

The read projection theorem has the right squared loss and rank-k output, but its floating-point storage and the table's RAM-word convention do not provide the required uniform bit-state and exact-zero-residual implementation for this contract. A possible conversion remains pending, rather than being treated as a matching bit upper.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/2/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/2/comparison_ids; canonical SHA-256: 95ac95ef4cc7b4da0b6b0a8ba71a933821bcb9e348991e1093d4f6c168826a84

#### Native item 1

Native pointer: /joint_analysis/impact/2/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/2/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/2/finding_id; canonical SHA-256: 6a645b65be8d38f999242b615bcedde6f1dbc6b72afffdb936fc4ae8111fe5eb

frequent_directions_resource_screen

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/2/improvement_region; canonical SHA-256: 9876e5a84061a3affe66a6e7252ea09a2a45859aaa46dfcd9a0ea6377e1d0373

None established for this finite-bit target by the read theorem.

#### Native field: kind

Native pointer: /joint_analysis/impact/2/kind; canonical SHA-256: 0156322ed8506611831c391ce78dbd50d13a3d191f80b7a2c8880d6a2de161b1

no_effect

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/2/new_envelope; canonical SHA-256: 02caae98a87f8f1165b9bcaf33d68f1666b15553286d5d5246ba01d8fd35dfc1

The same envelope; the examined Frequent Directions claim is not adopted.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/2/old_envelope; canonical SHA-256: 8c450a34bbe915b465a96d4f367004b8e9ba3b0242a79c23cf06a773ba22346f

With the independently derived storage update: Omega(nk/epsilon) <= M_bits^star <= O(mn) on R.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/2/unchanged_region; canonical SHA-256: 7b86d1733263c991e9bcf90fa3aa813c5f8d91e082aa0d0ebcf1ca4cfe292404

All target points.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/2/validity_region; canonical SHA-256: abf04070e42fc2fa9e41c8d17454ba5d756931306ecfc9053a1b4e7db497a8b9

The source's real-valued row-stream setting and k<ell sketch regime; no finite-bit target validity region has been established.

#### Native field: witness

Native pointer: /joint_analysis/impact/2/witness; canonical SHA-256: a99b906676c742dbfd2295f782a49429e146f3377519f0b72f8c331325c80828

arXiv:1501.01711v2, Theorem 1.2, archived characters 11900-15900, expressly counts O(kd/epsilon) floating-point numbers.

#### Native item 4

Native pointer: /joint_analysis/impact/3; canonical SHA-256: 2143c726a79556d381612766519f8f79f31e23855f77140f462e6a4fdec97f65

#### Native field: argument

Native pointer: /joint_analysis/impact/3/argument; canonical SHA-256: 86f67a682ed982515f7122f08babe0d3e01e26362a2cc82f06d730206817cf19

Retain the exact accepted native b1 lower and b2 upper, including their view main/g1/q1/resource and all original R guards. The minimax quantity is worst-case over the admissible public encodings q, not an individually fixed-q complexity. The b1 source construction supplies S_bits^star >= c n k/epsilon on R. The fully charged deterministic construction p_store supplies S_bits^star <= 3mn+O(n+log(mn)+1) <= C mn with universal C on D, uniformly in the public q, using the existing symbolic-output contract and no additional input access. Since k<min(m,n), both m,n>=2 and the stated overhead is absorbed uniformly. On S=R intersect{m<=2 C_0 k/epsilon}, the upper is at most 2 C C_0 n k/epsilon. Thus c n k/epsilon <= S_bits^star <= 2 C C_0 n k/epsilon: Theta(nk/epsilon), with only universal source constants C_0,epsilon_0 fixed, never hiding m,n,k,epsilon or q. This also equals Theta(mn) on S since C_0 k/epsilon<=m<=2 C_0 k/epsilon. The upper succeeds deterministically and has the native pathwise memory cap, hence preserves per-input success >=2/3. Its finite-label charged output handles zero optimal residual and rank deficiency by the existing canonical exact spectral interpretation; we do not replace it with a numerical coordinate-output algorithm or free external eigensolver. No new output, finite precision, RAM-word, oracle/pass or q-pointwise assumption is introduced. S is nonempty as a parameter region: set k=1, choose epsilon=min(epsilon_0/2,C_0/4,1/4)>0, and m=n=ceil(C_0/epsilon); C_0/epsilon>=4 ensures m<=2 C_0/epsilon and k<min(m,n). The source lower still ranges over its own legal encoding subclass, not necessarily q=1. The equality m=2 C_0 k/epsilon is included whenever integral; epsilon=epsilon_0 is not. Outside S the old c1 remains polynomial_gap on R, and D minus R remains unassessed. This is publication of a closure already explicitly stated in the baseline joint annotation, not a new source theorem, a strict extension beyond R, or a full-domain minimax solution.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/3/boundary_type; canonical SHA-256: 9316fd5c0370b0116fce9325e72bc288488b83f2977030ced0f683670e4b2f49

exact

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/3/comparison_ids; canonical SHA-256: f617877c937165d4da9e1f8db5900fc14b27ac6e5d7951dce7d844cae9bd4264

#### Native item 1

Native pointer: /joint_analysis/impact/3/comparison_ids/0; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/3/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/3/finding_id; canonical SHA-256: 117bd9386446c4d0a8cbc41d6a29a93ab40c1df2f0abde57985f749d2df1f503

stream_low_row_native_closure_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/3/improvement_region; canonical SHA-256: 80817f5b97b3f326501aba12a1e704dca3bff4b3bd79e49c22eaa900978445bc

No new numeric bound or strict extension outside old R; native publication of the existing matching consequence.

#### Native field: kind

Native pointer: /joint_analysis/impact/3/kind; canonical SHA-256: 7249f099445029410a160bddb6fd935004aff56d921f462672a9f41815a78001

explicit_region_registration

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/3/new_envelope; canonical SHA-256: 6531ed6c06fc0e969567a4b90cc4be58ce034be8c0074118912afb36e0ae9656

Native c2 separately publishes Theta(nk/epsilon) on the same-contract slab. Old c1 remains polynomial_gap.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/3/old_envelope; canonical SHA-256: 1f8db03f7a154c4ae1f2b59348d592eb6591ead55510709d0a7e3e22f3aa6826

The broad c1 already had O(mn) versus Omega(nk/epsilon), and its joint analysis explicitly recognized constant matching on this low-row slab.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/3/unchanged_region; canonical SHA-256: ed2b16b328bf76ba50a4b74dfe913af93d3795d678d22f3d5c7c137b127e0261

All immutable contracts, old c1 formula/status and all lower guards. D outside R remains unassessed.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/3/validity_region; canonical SHA-256: fe416cf855abcf4bf7805e7143b9aabea734093cc00d40b27a012dfd69522426

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. ADDITIONALLY m <= 2*C_0*k/epsilon; both sufficient lower inequalities remain inclusive and epsilon<epsilon_0 remains strict.

#### Native field: witness

Native pointer: /joint_analysis/impact/3/witness; canonical SHA-256: c288de7e0a81df806de84a16a298146bb9eecc8651de950a11d38890b1041a9e

k=1;epsilon=min(epsilon_0/2,C_0/4,1/4);m=n=ceil(C_0/epsilon) is a legal point of the slab.

#### Native item 5

Native pointer: /joint_analysis/impact/4; canonical SHA-256: 059b40dbc7b8edafff9c1408eb9d3dbdd78b9e7e9636d8b8d788a2de2f6b6850

#### Native field: argument

Native pointer: /joint_analysis/impact/4/argument; canonical SHA-256: 920a15592fb9c690b7bf5c60800c0de92740b768cb4490c24dbbdfc56f88ec3c

Explicit canonical state/summary correction where applicable and conditional v2 synthesis migration. All native inequalities, source guards and contracts are retained unless separately enumerated in the pinned profile. Remaining literature, normalization and unassessed-domain obligations are not resolved by this migration. Publish the already-established matched low-row slice R intersect {m<=2*C0*k/epsilon} as a separate optimal native comparison, using the same accepted bits upper/lower and the complete native combination proof.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/4/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/4/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/impact/4/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/4/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/4/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/4/finding_id; canonical SHA-256: 3d694c92d3d8e91b9df26dfb7ab345746e6e6f4d3ace18c5ba2af371d40798a0

curated_feedback_MX_S_stream_bits_20261116

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/4/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/4/kind; canonical SHA-256: 57ff9dd3ff31d2bc394a3b00bbf1317613b380fe0891401bfc1c3a07a94f3993

correction

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/4/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/4/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/4/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/4/validity_region; canonical SHA-256: afba1478408d1549cd7a3bf6b314119e5e85e93630f97271622a3350b261fe49

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity. The minimized resource is peak retained bits for the main one-pass algorithm view and per-input success probability at least 2/3. The upper construction is also uniform for each public q; the retained lower bound is for the worst case over q, not every individually fixed q.

#### Native field: witness

Native pointer: /joint_analysis/impact/4/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native item 6

Native pointer: /joint_analysis/impact/5; canonical SHA-256: 1afe8d15f6e02e86491dba96456165fb278386c273b692e495c324037329ecf0

#### Native field: argument

Native pointer: /joint_analysis/impact/5/argument; canonical SHA-256: 27f13269515265b1342c5f746170f0138e34ac988e3697d1c69e363782cc4706

The exact previously adopted science is conditionally retained. Correct only open-cell closure-publication metadata to the current explicit unassessed convention; no bound, guard, comparison, scientific contract or summary changes. Grouped cross-ID opportunities remain unassessed pending work, without any adopted reduction. This is presentation restructuring, not a new theorem or blind research.

#### Native field: boundary_type

Native pointer: /joint_analysis/impact/5/boundary_type; canonical SHA-256: 0296f22b01d3da51783b5e145c24403c9066251dff0d2f86a33204d0d2b0cd38

not_applicable

#### Native field: comparison_ids

Native pointer: /joint_analysis/impact/5/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/impact/5/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/impact/5/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: extension_witness

Native pointer: /joint_analysis/impact/5/extension_witness; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: finding_id

Native pointer: /joint_analysis/impact/5/finding_id; canonical SHA-256: ab149194c58e14750331645cecd849d6ad9287cd3e4521a502ff01fd33dee51a

curated_feedback_MX_S_stream_bits_20261116_42b1a1bbfb

#### Native field: improvement_region

Native pointer: /joint_analysis/impact/5/improvement_region; canonical SHA-256: 81a158f98ff637af0d622b4a3853f29fad5745273e3842b600adb901cb43095e

Only the explicitly proved local regions; canonical code repairs alone do not improve inequalities.

#### Native field: kind

Native pointer: /joint_analysis/impact/5/kind; canonical SHA-256: f980a6033e731764ab6b313b09320614ed53f4475e6913ab95626394dc59b056

synthesis_only

#### Native field: new_envelope

Native pointer: /joint_analysis/impact/5/new_envelope; canonical SHA-256: 94ec5ad95d931dd789ca32c17c70fb12963e526befacac6400154bb84a0c4dc4

Exact prepared native comparisons and their guarded syntheses; this curation adds no unstated rate claim.

#### Native field: old_envelope

Native pointer: /joint_analysis/impact/5/old_envelope; canonical SHA-256: e681f7209687aaf72c80f792fc38b67417a0dccd17ece3d1ff81c546f773cb1e

Exact frozen baseline, retained except for the explicitly enumerated candidate changes.

#### Native field: unchanged_region

Native pointer: /joint_analysis/impact/5/unchanged_region; canonical SHA-256: 44c7f6e062dbc75b9247f22ce4a64392ddfd8802dd0387f1209691e0f5ce1cf0

All other claims retain their original guards and conditional evidence basis.

#### Native field: validity_region

Native pointer: /joint_analysis/impact/5/validity_region; canonical SHA-256: afba1478408d1549cd7a3bf6b314119e5e85e93630f97271622a3350b261fe49

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity. The minimized resource is peak retained bits for the main one-pass algorithm view and per-input success probability at least 2/3. The upper construction is also uniform for each public q; the retained lower bound is for the worst case over q, not every individually fixed q.

#### Native field: witness

Native pointer: /joint_analysis/impact/5/witness; canonical SHA-256: 5355b9fb3c529abb99043b7f05f8eca4b1418754a2e9d740ac1f257db9cae2ae

Prepared proof records and the exact changed comparison predicates.

#### Native field: normalization_requests

Native pointer: /joint_analysis/normalization_requests; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: pending_obligations

Native pointer: /joint_analysis/pending_obligations; canonical SHA-256: 9020cf9e8dafbf6ddfc320fa2722e7f73eec19344bbb7f959df825aebdd842e4

#### Native item 1

Native pointer: /joint_analysis/pending_obligations/0; canonical SHA-256: 417a3c7db629335470e4c9a1b7591be108b1e73549364be5e72bc9c444029462

Sharper finite-bit upper bounds remain unassessed: arXiv:1501.01711v2 Theorem 1.2 counts floating-point numbers; a uniform bit-state, roundoff and exact-zero-residual conversion has not been established.

#### Native item 2

Native pointer: /joint_analysis/pending_obligations/1; canonical SHA-256: dce2b9a0aafd8ed437636d484f5b60cd67be792f970cf9c044842fbd4c601332

Primary theorem/mapping reads remain for arXiv:2109.11703v2, 1705.07140v3 and 1602.00412v2; their possible stronger finite-bit projector bounds are not adopted.

#### Native item 3

Native pointer: /joint_analysis/pending_obligations/2; canonical SHA-256: 9f00bceaa989c1a233cea3248ef75f1134113cafe4927f37404999821a7b6c93

Learned/robust variants arXiv:2503.00937v1 and 1705.05067v3 remain optional theorem-level leads; applicability without extra prediction capabilities and with this relative projector guarantee is unverified.

#### Native item 4

Native pointer: /joint_analysis/pending_obligations/3; canonical SHA-256: d26e21a68eb907c50e74da63fe29531f583525708c8ea80cd1d609be193559fd

The complementary domain D outside R has no completed bracket synthesis in this update; lower-dimensional and other-accuracy branches remain unassessed.

#### Native item 5

Native pointer: /joint_analysis/pending_obligations/4; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: provenance

Native pointer: /joint_analysis/provenance; canonical SHA-256: e806fe6da03b54f3bf81fc37f442594dc82f5d26399ad3b084d9af5314010b90

#### Native item 1

Native pointer: /joint_analysis/provenance/0; canonical SHA-256: b83aeac692f9c07188abd1ba11cd10d3947050f23883aad0ed4a324f08d58e84

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/0/bound_id; canonical SHA-256: a7c3e8260e2c6d4cc31f95eeeaab96b247225cc32936599de80b6bae2779f498

MX_S_stream_bits__main__b1

#### Native field: mapping

Native pointer: /joint_analysis/provenance/0/mapping; canonical SHA-256: aa75eb45106d778d565660c309b1d7ad48b75d68c1e5bdd093fe1c42c3ffd374

Retain the accepted finite-alphabet right-projector, per-input 2/3-success, one-pass bit-memory mapping conditionally. This annotation does not recertify the old theorem or extend its guard.

#### Native field: origin

Native pointer: /joint_analysis/provenance/0/origin; canonical SHA-256: 1587d37ff9394a18bd27593510d9b06024d7bec02b3ba0ac518868fba9abc518

retained_baseline

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/0/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/0/source_domain; canonical SHA-256: 81f5620d0b78947f06aa9bc865a072ff8fcf1178ee62905289a9a5b14e3b659e

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1. The frozen hard subclass uses q=n-r_0 with integer r_0=Theta(k/epsilon).

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/0/source_locator; canonical SHA-256: e68d8fedbafaad05f8eb46c6feff0923c3ed42da03bad1413eb1ffc0bb3e7258

Frozen /bounds/0 sha256 ab037475f123ac6145939097b92a48e9f7d4ba4f06a156f9f1eabbbc270d6eb0 and /evidence/0 sha256 710b7c7056384d4ed1ae6636cc25eaa8a67e3c225ccb54a142accdba5351ef23; original evidence names NeurIPS 2014 Theorem 1 and section 2.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/0/source_refs; canonical SHA-256: 2e40d80af60a871524dcc10447e878101dbfa4279ebac40fcd7ebd9eb36da8a1

#### Native item 1

Native pointer: /joint_analysis/provenance/0/source_refs/0; canonical SHA-256: eff073318934e313ec401f0775ad538d7a3459aa901621ad161e36c5e2a52211

MX_SRC_ST

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/0/target_domain; canonical SHA-256: 566ea0542be1acaae3138a60ce83e604d7b71c48d1c996cbed8f676e5ad9fd0c

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1.

#### Native item 2

Native pointer: /joint_analysis/provenance/1; canonical SHA-256: f559355df056daee27ba97fcc0646a4657cdf31e18eff96b9b818b074628ea69

#### Native field: bound_id

Native pointer: /joint_analysis/provenance/1/bound_id; canonical SHA-256: c73827c3acfd43062f4a30acf4f5eae672cb612752fa25221223d10a0aa07957

MX_S_stream_bits__main__b2

#### Native field: mapping

Native pointer: /joint_analysis/provenance/1/mapping; canonical SHA-256: a07662f00186192ca8059158b109beb143539a607e65dd887f28500a74af476e

Use five-valued entry labels, charge their full storage and output description, and apply the existing symbolic-subspace-output interpretation. The variational trace argument proves exact optimality. Deterministic success contains g1, and q stays a public symbol.

#### Native field: origin

Native pointer: /joint_analysis/provenance/1/origin; canonical SHA-256: b7167154a1fddca6e1de90fdc2618479b6f91483b65a20e75787b38bfd2ae6f5

analyst_derivation

#### Native field: proof_refs

Native pointer: /joint_analysis/provenance/1/proof_refs; canonical SHA-256: ea5fd11201c23f2962f44289d94c62b88337130af9bbfdab1f3edac108e2035e

#### Native item 1

Native pointer: /joint_analysis/provenance/1/proof_refs/0; canonical SHA-256: 845522c0eaaf2958da61e20a725b74cfd024a3c6d2783a22e91f2f150f0bf0d4

MX_S_stream_bits__main__p_store

#### Native field: source_domain

Native pointer: /joint_analysis/provenance/1/source_domain; canonical SHA-256: 8702361d50a3def74b1ca81ba8b9478c494a9b17848c3108730c359ef513101f

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity.

#### Native field: source_locator

Native pointer: /joint_analysis/provenance/1/source_locator; canonical SHA-256: 3c736df118182c75ff9b37c5a3fdac14ddd897a6530fb9dcfc4feb05ffb00a3d

Exact baseline premises /common_specification, /views, /quantities/0, /parameters, /resource_projections/0, with canonical hashes in proof MX_S_stream_bits__main__p_store.

#### Native field: source_refs

Native pointer: /joint_analysis/provenance/1/source_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: target_domain

Native pointer: /joint_analysis/provenance/1/target_domain; canonical SHA-256: 566ea0542be1acaae3138a60ce83e604d7b71c48d1c996cbed8f676e5ad9fd0c

R: m,n integers, 1 <= k < min(m,n), 0 < epsilon < epsilon_0, m >= C_0 k/epsilon, n >= C_0 k/epsilon; worst case over admissible public q >= 1.

#### Native field: synthesis_coverage

Native pointer: /joint_analysis/synthesis_coverage; canonical SHA-256: 02ed4b83a9a9aa4bf87cd067176a777b53b9eec0e0cf7834d7c11b7f96b4d02c

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: gap_basis

Native pointer: /joint_analysis/synthesis_coverage/gap_basis; canonical SHA-256: 88bc670ca99c5d2acb1243e5e5fd21f0b795c16c627e10e97e985091ad96a280

registered_envelope

#### Native field: literature

Native pointer: /joint_analysis/synthesis_coverage/literature; canonical SHA-256: d4d3066227543deefb2bd165a10a4f8922532486377109007e37e62d29936c86

#### Native field: scope

Native pointer: /joint_analysis/synthesis_coverage/literature/scope; canonical SHA-256: f44902418633a6a927c42d0e451b78fdca596b9167d496f6305c3031528c835c

No new blind literature search in this migration. Conditional retention of the exact preceding accepted analysis and its finite historical scope; all stated pending work remains pending.

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/literature/status; canonical SHA-256: 75e1201b5806b4beceaea38103cfdedaa20e45f4ee6d958b61e380cb5772cd57

not_assessed

#### Native field: obligations

Native pointer: /joint_analysis/synthesis_coverage/obligations; canonical SHA-256: 95ebf23d710cd6a4f1f63ab9ea987bd1b18640acb458eecff7fb3047d4ff7887

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0; canonical SHA-256: 1193ff21748e9e8cec8f17d56bf754467d92a13dfd48d44f0706d3eb5201e0e9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/argument; canonical SHA-256: 8d40081b154deb201cba29da4830b6caa3bbfece1173ab60d3299d87037178d7

The only compatible same-contract b1 and b2 remain included. On the new slab their full guarded min/max is matched by MX_S_stream_bits__main__p_low_row_closure_20261116; on broad c1 retain the growing O(m epsilon/k) quotient. No other quantity/resource route is substituted.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs; canonical SHA-256: 8f499a51b6cf55b701b8ccbb8f28e91a50e84e0991b87430300f52a3f9ef6997

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/0; canonical SHA-256: a7c3e8260e2c6d4cc31f95eeeaab96b247225cc32936599de80b6bae2779f498

MX_S_stream_bits__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/bound_refs/1; canonical SHA-256: c73827c3acfd43062f4a30acf4f5eae672cb612752fa25221223d10a0aa07957

MX_S_stream_bits__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids; canonical SHA-256: 95ac95ef4cc7b4da0b6b0a8ba71a933821bcb9e348991e1093d4f6c168826a84

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/id; canonical SHA-256: cbd717faae83a18dcd0984f69326879d0fe1418a4573e90441638e7d8eb23ec6

synthesis-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs; canonical SHA-256: f143618bf594765885c0d5dbce8744a265ac6ef22488225ee8901c4e927d602b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/0; canonical SHA-256: 5d3ee89d8afb05ffe7950bf00588162028a598b71cdec1df79499fafadfd945e

MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/proof_refs/1; canonical SHA-256: 845522c0eaaf2958da61e20a725b74cfd024a3c6d2783a22e91f2f150f0bf0d4

MX_S_stream_bits__main__p_store

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/0/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1; canonical SHA-256: 2f858c7dff59d41e18d01ebe737a8c3f51235e930133556003b3c7f9433d8da9

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/argument; canonical SHA-256: 8d40081b154deb201cba29da4830b6caa3bbfece1173ab60d3299d87037178d7

The only compatible same-contract b1 and b2 remain included. On the new slab their full guarded min/max is matched by MX_S_stream_bits__main__p_low_row_closure_20261116; on broad c1 retain the growing O(m epsilon/k) quotient. No other quantity/resource route is substituted.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs; canonical SHA-256: 8f499a51b6cf55b701b8ccbb8f28e91a50e84e0991b87430300f52a3f9ef6997

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/0; canonical SHA-256: a7c3e8260e2c6d4cc31f95eeeaab96b247225cc32936599de80b6bae2779f498

MX_S_stream_bits__main__b1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/bound_refs/1; canonical SHA-256: c73827c3acfd43062f4a30acf4f5eae672cb612752fa25221223d10a0aa07957

MX_S_stream_bits__main__b2

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids; canonical SHA-256: f617877c937165d4da9e1f8db5900fc14b27ac6e5d7951dce7d844cae9bd4264

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/comparison_ids/0; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/id; canonical SHA-256: ebcba919e62a1ab3932a5511960ae541204ef3e4e612a3e2b58eaa7aea342c2d

synthesis-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/kind; canonical SHA-256: bfae5f6daa03006fec98e26fd755918445e662d473f2937f56185e6284333167

compatible_candidates

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/lead; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs; canonical SHA-256: f143618bf594765885c0d5dbce8744a265ac6ef22488225ee8901c4e927d602b

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/0; canonical SHA-256: 5d3ee89d8afb05ffe7950bf00588162028a598b71cdec1df79499fafadfd945e

MX_S_stream_bits__main__p_low_row_closure_20261116

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/proof_refs/1; canonical SHA-256: 845522c0eaaf2958da61e20a725b74cfd024a3c6d2783a22e91f2f150f0bf0d4

MX_S_stream_bits__main__p_store

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/1/state; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native item 3

Native pointer: /joint_analysis/synthesis_coverage/obligations/2; canonical SHA-256: df1673a47790bfe6dd8d1de6bdd9de11ce84ebe5b1807db2ad7d920b77e013dd

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/argument; canonical SHA-256: 7ea09ad2df83cccaf4ac3c53bb488e2188216d0e70275870f88f3399b8264a18

The new slab publication does not resolve this retained finite-bit/source/complement lead.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/id; canonical SHA-256: ee0723fb651d69d8b00007c3dd0b2c26b442a1967d558ed1d9371a71edb04df1

retained-lead-0

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/lead; canonical SHA-256: 417a3c7db629335470e4c9a1b7591be108b1e73549364be5e72bc9c444029462

Sharper finite-bit upper bounds remain unassessed: arXiv:1501.01711v2 Theorem 1.2 counts floating-point numbers; a uniform bit-state, roundoff and exact-zero-residual conversion has not been established.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/2/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 4

Native pointer: /joint_analysis/synthesis_coverage/obligations/3; canonical SHA-256: c64b52c642a2f2c96818059e0fc98b2a939a2c7bf27857aa4ca4d7d22b5230a4

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/argument; canonical SHA-256: 7ea09ad2df83cccaf4ac3c53bb488e2188216d0e70275870f88f3399b8264a18

The new slab publication does not resolve this retained finite-bit/source/complement lead.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/id; canonical SHA-256: de5fdce7447be2c5dd002fa7eea0d3d3e4f728f8906029886fcd58eea30d3a38

retained-lead-1

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/lead; canonical SHA-256: dce2b9a0aafd8ed437636d484f5b60cd67be792f970cf9c044842fbd4c601332

Primary theorem/mapping reads remain for arXiv:2109.11703v2, 1705.07140v3 and 1602.00412v2; their possible stronger finite-bit projector bounds are not adopted.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/3/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 5

Native pointer: /joint_analysis/synthesis_coverage/obligations/4; canonical SHA-256: e87591aecd4b601e61b858065d8eb807329ab355676785c903434f43395fbd62

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/argument; canonical SHA-256: 7ea09ad2df83cccaf4ac3c53bb488e2188216d0e70275870f88f3399b8264a18

The new slab publication does not resolve this retained finite-bit/source/complement lead.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/id; canonical SHA-256: 4c7d4a772953abffa3df06e0cd216ac0d2f671d6e76981ada88387a5a5729fbd

retained-lead-2

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/lead; canonical SHA-256: 9f00bceaa989c1a233cea3248ef75f1134113cafe4927f37404999821a7b6c93

Learned/robust variants arXiv:2503.00937v1 and 1705.05067v3 remain optional theorem-level leads; applicability without extra prediction capabilities and with this relative projector guarantee is unverified.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/4/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 6

Native pointer: /joint_analysis/synthesis_coverage/obligations/5; canonical SHA-256: 73dbe1281f51ff1270e03585cc6d45c160f55875d9e6a7d9b1f9f01611110d26

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/argument; canonical SHA-256: 7ea09ad2df83cccaf4ac3c53bb488e2188216d0e70275870f88f3399b8264a18

The new slab publication does not resolve this retained finite-bit/source/complement lead.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/id; canonical SHA-256: 84ddb173c0857af2ff34c0d7ff506f90439c9f7fc2aa9015e25581e45f580730

retained-lead-3

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/lead; canonical SHA-256: d26e21a68eb907c50e74da63fe29531f583525708c8ea80cd1d609be193559fd

The complementary domain D outside R has no completed bracket synthesis in this update; lower-dimensional and other-accuracy branches remain unassessed.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/5/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native item 7

Native pointer: /joint_analysis/synthesis_coverage/obligations/6; canonical SHA-256: 491efa19215d47cef2d98bb6a3d57f1dc5391ebe6532927a9f7b8ea3536688ba

#### Native field: affects_gap

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/affects_gap; canonical SHA-256: b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b

Native value (boolean): true

#### Native field: argument

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/argument; canonical SHA-256: fc4c68ce157c7a2f8540ddb7c3741c6e85dd9d2117ba6ccc960c85a288c87e26

The registered envelope is assessed only for this finite curation. This does not certify literature exhaustion or the unassessed complement.

#### Native field: bound_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/bound_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: cell_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/cell_ids; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: comparison_ids

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids; canonical SHA-256: 4f1b006c0bf912af343e1ae7ceafc4f2940bb5bd2f0a31c8bba2f70c80fbfa8d

#### Native item 1

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/0; canonical SHA-256: 380856d893568018c61d4bbc208052c17ebe5aa1a4fd88302fdd8e9f274124c5

MX_S_stream_bits__main__c1

#### Native item 2

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/comparison_ids/1; canonical SHA-256: 4a2f7d49af8213bf236463e476721b387d5cb2848b69b48a87bf14d9f7a2fad6

MX_S_stream_bits__main__c2_low_row

#### Native field: id

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/id; canonical SHA-256: 8f3893b390dbf1c98368d6b451c613dd05f798a42d5bd62383775de81d03258c

curated-scope-limit

#### Native field: kind

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/kind; canonical SHA-256: a79094d5206499c86794e049e918245ccb55ee6590e84c279e1d00b26cceffc7

material_lead

#### Native field: lead

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/lead; canonical SHA-256: 77c7bfa320b590e1beb7a14ec5097a427bc13246621fe8348df6050c3a5280e6

This is feedback-guided curation, not a new blind or exhaustive literature search. Preserve all native pending obligations.

#### Native field: proof_refs

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/proof_refs; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: state

Native pointer: /joint_analysis/synthesis_coverage/obligations/6/state; canonical SHA-256: 12adac54ac6f7140109391b670b3cbcd51f083d8f5ee62ce26857c794ed67d36

pending

#### Native field: status

Native pointer: /joint_analysis/synthesis_coverage/status; canonical SHA-256: 8ac24611cfe47c129e37108bc6adc6843c4fe8fb9c37c27fac8a1835ba660307

partial

#### Native field: target

Native pointer: /joint_analysis/target; canonical SHA-256: 6396047a7513a0bd06e9467e136d7827b87b4ecccb3f5b27e893cb69d8d4ba62

#### Native field: allowed_constant_dependencies

Native pointer: /joint_analysis/target/allowed_constant_dependencies; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: contract_refs

Native pointer: /joint_analysis/target/contract_refs; canonical SHA-256: eca301e35276a64270abf446fff08349848c8b79e39029dacb17f5a7e080c950

#### Native item 1

Native pointer: /joint_analysis/target/contract_refs/0; canonical SHA-256: ca04624bce4c51f581bf1916545176dc59691d417183c0bb0be9d36b4218387d

/common_specification

#### Native item 2

Native pointer: /joint_analysis/target/contract_refs/1; canonical SHA-256: b91103c440937fa2adc4e43c26a410dfc6f7e6000ced0d07f988b89ea330217f

/views/0

#### Native item 3

Native pointer: /joint_analysis/target/contract_refs/2; canonical SHA-256: 15dd24a7978859271fb001237c07a1f13bc0e4f3f2e6e1c7067cb4ee24f6b0af

/views/0/guarantees/0

#### Native item 4

Native pointer: /joint_analysis/target/contract_refs/3; canonical SHA-256: cd119ad47e9ced40b85135236eae81d1dcf7308ea9db8b43913681bf4ad6234c

/quantities/0

#### Native item 5

Native pointer: /joint_analysis/target/contract_refs/4; canonical SHA-256: af27968018201257d1ad04238c4bdc9761a84ab7c257fb50c11373bdb5dd72c0

/resource_projections/0

#### Native item 6

Native pointer: /joint_analysis/target/contract_refs/5; canonical SHA-256: b03f479ecad29417fe64d54febfa007ef0a050d7da8e3b9696bb89a91557a509

/parameters

#### Native field: fixed_parameters

Native pointer: /joint_analysis/target/fixed_parameters; canonical SHA-256: 6492543a457b74807f43f494e5a8a50b730ddc8f113ae87a2e987b50654bd0b1

#### Native item 1

Native pointer: /joint_analysis/target/fixed_parameters/0; canonical SHA-256: f22080e1777704d819622e7347d9427e4906c8bca7e0a6853adb033f44efac40

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/0/domain; canonical SHA-256: 4e8a83dd97872aab676882cad462c41b098da540b25bc96cd6354d1e62572d98

Universal positive source-proof constant, independent of the joint variables; used only in the retained sufficient-dimension guard.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/0/parameter_ref; canonical SHA-256: 5b3061c473e595921f9f65e49f1a925e0fb8fd4e5daa13322acc77332a385e84

MX_S_stream_bits_p_1d0d24b110

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/0/symbol; canonical SHA-256: e2139ce8ac0004812b0693b1a06e2fd2ffac12e112d5130e9e0ed2bc54d984b3

C_0

#### Native item 2

Native pointer: /joint_analysis/target/fixed_parameters/1; canonical SHA-256: 794b0c76a500b48f5c5d1cbda2f3c5a32332a762dd02ce4ca68fbbe6673dd1cb

#### Native field: domain

Native pointer: /joint_analysis/target/fixed_parameters/1/domain; canonical SHA-256: 366fcf7f2cd659c3f2c2e107078b0e7fc61564afa51382b654a23e8160857f2e

Universal positive source-theorem cutoff appearing in the frozen regime; no native parameter ID is declared for this auxiliary constant.

#### Native field: parameter_ref

Native pointer: /joint_analysis/target/fixed_parameters/1/parameter_ref; canonical SHA-256: 74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b

Native value (null): null

#### Native field: symbol

Native pointer: /joint_analysis/target/fixed_parameters/1/symbol; canonical SHA-256: 007ab56c0578075b0e94c1c78d87a220040d30a5282eb4be7b2b4e2a54800403

epsilon_0

#### Native field: full_domain

Native pointer: /joint_analysis/target/full_domain; canonical SHA-256: afba1478408d1549cd7a3bf6b314119e5e85e93630f97271622a3350b261fe49

D: m,n positive integers, 1 <= k < min(m,n), epsilon > 0. Complexity is worst-case over public integers q >= 1 and fixed streams over {0,+1,-1,+1/sqrt(q),-1/sqrt(q)}; q is not an individually fixed argument of the minimax quantity. The minimized resource is peak retained bits for the main one-pass algorithm view and per-input success probability at least 2/3. The upper construction is also uniform for each public q; the retained lower bound is for the worst case over q, not every individually fixed q.

#### Native field: joint_variables

Native pointer: /joint_analysis/target/joint_variables; canonical SHA-256: 005dc7347d71103c7a88cc842eb5a9e008b4605f83d976db9a239c086a0035b6

#### Native item 1

Native pointer: /joint_analysis/target/joint_variables/0; canonical SHA-256: 779e5185e38ba480610a6a7b97ef4bcd60f0cce8fa90dc8e75e5ff951c49f8b4

MX_S_stream_bits_p_35c061cc2e

#### Native item 2

Native pointer: /joint_analysis/target/joint_variables/1; canonical SHA-256: 78959c9dc358e18199a65dcaf717f7282e4bd083d95839d4b0aa8453484d3526

MX_S_stream_bits_p_a20059fb21

#### Native item 3

Native pointer: /joint_analysis/target/joint_variables/2; canonical SHA-256: 54aef0fb8b12be9d2cab87368f56d6947955fda2a9e87adbedb93882e65b8797

MX_S_stream_bits_p_12a952329f

#### Native item 4

Native pointer: /joint_analysis/target/joint_variables/3; canonical SHA-256: 20f18e37e218aef0ad96ae48daef4ced3e50153879632b4c0fa336180a2797ad

MX_S_stream_bits_p_d812b5336c

#### Native field: normalized_variables

Native pointer: /joint_analysis/target/normalized_variables; canonical SHA-256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945

Native value (empty_array): []

#### Native field: resolution

Native pointer: /joint_analysis/target/resolution; canonical SHA-256: 0772fde17309bd271c343f359e848907b3a93b420878fd1e0b68bbdadcd98eda

resolved

#### Native field: uniform_in

Native pointer: /joint_analysis/target/uniform_in; canonical SHA-256: 005dc7347d71103c7a88cc842eb5a9e008b4605f83d976db9a239c086a0035b6

#### Native item 1

Native pointer: /joint_analysis/target/uniform_in/0; canonical SHA-256: 779e5185e38ba480610a6a7b97ef4bcd60f0cce8fa90dc8e75e5ff951c49f8b4

MX_S_stream_bits_p_35c061cc2e

#### Native item 2

Native pointer: /joint_analysis/target/uniform_in/1; canonical SHA-256: 78959c9dc358e18199a65dcaf717f7282e4bd083d95839d4b0aa8453484d3526

MX_S_stream_bits_p_a20059fb21

#### Native item 3

Native pointer: /joint_analysis/target/uniform_in/2; canonical SHA-256: 54aef0fb8b12be9d2cab87368f56d6947955fda2a9e87adbedb93882e65b8797

MX_S_stream_bits_p_12a952329f

#### Native item 4

Native pointer: /joint_analysis/target/uniform_in/3; canonical SHA-256: 20f18e37e218aef0ad96ae48daef4ced3e50153879632b4c0fa336180a2797ad

MX_S_stream_bits_p_d812b5336c

#### Native field: version

Native pointer: /joint_analysis/version; canonical SHA-256: d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35

Native value (number): 2

## References

[1] David P. Woodruff. Low Rank Approximation Lower Bounds in Row-Update Streams. 2014. NeurIPS 2014 proceedings, Theorem 1.

https://papers.neurips.cc/paper/5407-low-rank-approximation-lower-bounds-in-row-update-streams.pdf
