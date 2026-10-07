"""02 — Mixed strategies / minimax theorem. Penalty-kick game.
Payoff = P(kicker scores)*100. Rows: Kicker L/R, Cols: Keeper L/R.
Empirical matrix from 1417 pro penalties (Palacios-Huerta 2003 style):
  [[58, 95],[93, 70]]  (guess-right: 58 left, 70 right; guess-wrong: ~93-95)
Solve 2x2 analytically + fictitious play (Brown 1951) -> GAN analogy.
"""
import random
PAYOFF=[[58.0,95.0],[93.0,70.0]]

def solve_2x2(m=PAYOFF):
    a,b,c,d=m[0][0],m[0][1],m[1][0],m[1][1]
    p=(d-c)/((a-b-c+d)) if (a-b-c+d)!=0 else 0.5  # P(row0)
    q=(d-b)/((a-b-c+d)) if (a-b-c+d)!=0 else 0.5  # P(col0)
    v=(a*d-b*c)/((a-b-c+d)) if (a-b-c+d)!=0 else 0.0
    return p,q,v

def expected(p,q,m=PAYOFF):
    return (p*(m[0][0]*q+m[0][1]*(1-q))+(1-p)*(m[1][0]*q+m[1][1]*(1-q)))

def fictitious_play(n=100000, seed=0):
    rng=random.Random(seed)
    # counts of opponent actions
    kick_counts=[1,1]; keep_counts=[1,1]
    kp=0; kp_hist=[]
    for t in range(n):
        # kicker best-replies to keeper empirical mix
        q=keep_counts[0]/sum(keep_counts)
        eu_L=PAYOFF[0][0]*q+PAYOFF[0][1]*(1-q)
        eu_R=PAYOFF[1][0]*q+PAYOFF[1][1]*(1-q)
        k=0 if eu_L>eu_R else 1
        # keeper best-replies (minimises) to kicker empirical mix
        p=kick_counts[0]/sum(kick_counts)
        eu_L2=PAYOFF[0][0]*p+PAYOFF[1][0]*(1-p)
        eu_R2=PAYOFF[0][1]*p+PAYOFF[1][1]*(1-p)
        g=0 if eu_L2<eu_R2 else 1
        kick_counts[k]+=1; keep_counts[g]+=1
    p=kick_counts[0]/sum(kick_counts); q=keep_counts[0]/sum(keep_counts)
    return p,q
