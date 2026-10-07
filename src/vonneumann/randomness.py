"""06 — Fake randomness: middle-square + von Neumann debiasing (1951).
Middle-square 4-digit: x_{n+1} = middle4(x_n^2 padded to 8).
Debias: HT->1, TH->0, HH/TT discard. Works for ANY unknown bias.
"""
import random
def middle_square(seed, n):
    x=seed; out=[]
    for _ in range(n):
        s=str(x*x).zfill(8)[2:6]
        x=int(s); out.append(x)
        if x==0: break
    return out

def cycle_stats():
    res={}
    for seed in range(10000):
        seen={}; x=seed; L=0
        while x not in seen:
            seen[x]=L; L+=1
            s=str(x*x).zfill(8)[2:6]; x=int(s)
            if L>10000: break
        res[seed]=L
    vals=list(res.values())
    return sum(vals)/len(vals), max(vals), max(res,key=res.get), res

def von_neumann_debias(bits):
    out=[]
    for i in range(0,len(bits)-1,2):
        a,b=bits[i],bits[i+1]
        if a==0 and b==1: out.append(0)
        elif a==1 and b==0: out.append(1)
    return out

def biased_coin(n, p=0.7, seed=0):
    rng=random.Random(seed)
    return [1 if rng.random()<p else 0 for _ in range(n)]
