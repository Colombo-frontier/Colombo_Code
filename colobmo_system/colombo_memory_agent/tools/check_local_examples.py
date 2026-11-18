#!/usr/bin/env python3
"""Exact finite checks of selected local examples, NOT an independent scientific review."""
from fractions import Fraction as F
import json,math

def main():
    tests=[]
    # PJ92 printed gain branch: stable positive eigenvalues do not ensure I-gamma A stable.
    gamma=F(1,10);eigenvalues=[F(1),F(100)]
    assert gamma<F(2)/min(eigenvalues)
    multipliers=[1-gamma*x for x in eigenvalues]
    assert multipliers==[F(9,10),F(-9)]
    tests.append({'id':'PJ92_two_dimensional_gain','passed':True,'gain':'1/10','iteration_eigenvalues':['9/10','-9'],
                  'scope':'The displayed numerical example; general CLT branches are not checked here.'})
    # Truncated Neumann expectations checked exactly for a scalar Hessian.
    H,L,N=F(1),F(2),4;q=1-H/L
    printed=sum(q**j for j in range(1,N+1))/L
    corrected=sum(q**j for j in range(N))/L
    assert printed==q*(1-q**N)/H
    assert corrected==(1-q**N)/H
    assert sum(F(0)**j for j in range(1,8))==0
    tests.append({'id':'Neumann_indexing_scalar','passed':True,'printed_expectation':str(printed),'corrected_expectation':str(corrected),
                  'scope':'Finite scalar formula and H=L diagnostic; does not certify stochastic outer-loop rates.'})
    # PL/QG factor diagnostic under the explicitly stored conventions.
    mu,b,a,theta=F(2),F(3),F(1),F(1)
    h=mu*a*a/2;grad=mu*a
    assert grad*grad/2==mu*h
    assert h<(4*mu)*a*a/2
    assert b/mu>b/(2*mu)
    tests.append({'id':'PL_QG_constant_conventions','passed':True,'scope':'Scalar quadratic under the definitions in the record.'})
    # Horizon-one normalization check (the analytical prior expectation is in the record).
    assert F(1,2)<F(6,10)
    tests.append({'id':'product_circle_T1_numeric_comparison','passed':True,'n':6,'claimed_lower':'3/5','prior_expected_regret':'1/2',
                  'scope':'Only numerical comparison; prior calculation remains a local mathematical argument.'})
    # Algebraic cubic remainder identity for representative nonnegative rational q,r.
    for q in [F(0),F(1,3),F(2)]:
        for r in [F(0),F(1,2),F(3)]:
            assert q**3/3-r*q*q/2+r**3/6==(q-r)**2*(2*q+r)/6
    tests.append({'id':'cubic_model_remainder_identity','passed':True,'scope':'Finite rational examples, not proof of global model necessity.'})
    print(json.dumps({'type':'finite_same_conversation_math_checks','tests':tests,
                      'independent_scientific_review':False,'formal_verification':False},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
