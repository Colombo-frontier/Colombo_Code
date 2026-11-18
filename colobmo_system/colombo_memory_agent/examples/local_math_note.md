# Complete Educational Example: Coordinate Information and Euclidean Geometry

This file presents an independent mathematical derivation prepared for this delivery to demonstrate memory granularity and test interfaces; no novelty is claimed, and no independent Reviewer has been run.

## Setting and Theorem
Let d>=1 be an integer, L,R>0, and 0<=T<=d an integer. Set V={-1,+1}^d,
f_v(x)=(L/sqrt(d)) <v,x>, with feasible set Q={x:||x||_2<=R}.
The functions are convex and L-Lipschitz on R^d. The algorithm knows only d,L,R and this function family.
Each query selects i∈{1,...,d} (optionally with any x∈Q) and obtains the exact coordinate derivative
∂_i f_v(x)=L v_i/sqrt(d), at a cost of one call. No function value or other coordinate is returned.
Arbitrary adaptive randomized algorithms, arbitrary outputs in Q, and free internal computation are allowed; every execution path uses at most T queries.
Performance is sup_v E_A[f_v(xhat)-min_Q f_v].
The minimax performance for this family is exactly L R(1-sqrt(T/d)).

### Complete Proof
First, ||∇f_v||_2=L, the optimizer is x_v^*=-R v/sqrt(d), and the optimal value is -LR.
Upper bound: if T=0, output 0. If T>=1, query a fixed set S of T distinct coordinates and output
x_i=-R v_i/sqrt(T) (i∈S), with all other coordinates 0. The norm is R and the function value is -LR sqrt(T/d),
so the stated gap holds for every v. No randomness is used.

Lower bound: first let v have independent uniform signs, with the algorithm's random seed independent of v. After fixing the seed,
a transcript fixes only the signs of coordinates already queried. The next coordinate and query point are chosen adaptively from the existing
transcript; unqueried signs remain conditionally independent with mean 0. This follows inductively: querying a known
coordinate adds no constraint, while querying a new coordinate fixes only that sign. Let S be the final set of distinct queried coordinates;
then |S|<=T. Conditional on the transcript and seed, the output xhat is a known vector in Q, so
E[f_v(xhat)|history,seed]=(L/sqrt(d)) sum_{i∈S}v_i xhat_i
>=-(L/sqrt(d))*sqrt(|S|)*||xhat_S||_2>=-LR sqrt(T/d).
Thus the average gap over random v and the algorithm's seed is >=LR(1-sqrt(T/d)). Since the set of v is finite, there exists
a fixed v whose expected gap over algorithmic randomness alone is at least this value. Combining with the upper bound yields equality.

### Escape Under Different Information Access
One full-gradient query returns every sign, so a single call determines the exact optimizer.
Even adding only exact function values invalidates this lower bound: choose x_i=R*3^{-i},
so ||x||_2<R. Set z=sqrt(d)*f_v(x)/(LR)=sum_i v_i*3^{-i}.
If two sign strings first differ at j, the leading term of their difference has absolute value 2*3^{-j}, while the tail has absolute value strictly less than
2 sum_{i>j}3^{-i}=3^{-j}, so cancellation is impossible. In a model with free internal computation/exact real comparisons,
sequential recovery also requires only O(d) exact arithmetic/comparison operations: v_j=sign(z), then set z=3z−v_j;
the leading remaining sign always dominates its tail. This is not a result for finite-precision or noisy oracles.
Thus "one real number carries information about only one sign" is false for an exact-value oracle.

## Comparison with the gap→gradient Lemma
Let f be C^1 on the full space, with ∇f globally L-Lipschitz, L>0, and f_*=inf_{R^d}f>−∞.
Applying the descent lemma at y=x−∇f(x)/L gives
f(y)<=f(x)−||∇f(x)||²/(2L), hence ||∇f(x)||²<=2L(f(x)−f_*).
Neither convexity nor attainment of the optimum is required. The global infimum f_* cannot be arbitrarily replaced by a constrained optimum: take f(x)=(x+1)^2/2,
Q=[0,∞); at x=0 the constrained gap is 0 but the gradient is 1.
This short lemma and counterexample also appear in the user-provided v1 design specification; they are used here to demonstrate a complete record.
