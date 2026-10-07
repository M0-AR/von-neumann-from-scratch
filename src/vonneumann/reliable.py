"""07 — Reliable machines from bad parts (von Neumann 1952 multiplexing).
Chain of L=100 stages, gate flip prob e. Single wire: P(wrong)= (1-(1-2e)^L)/2.
Multiplexed: bundle N wires, each stage: each new wire = majority of 3 random
old wires + voter flips w.p. e. Threshold for 3-XOR/majority ~ 1/6 (Evans-Schulman).
"""
import random
def single_wire_error(e=0.01, L=100):
    return (1-(1-2*e)**L)/2

def bundle_error(N=9, e=0.01, L=100, trials=2000, seed=0):
    rng=random.Random(seed); wrong=0
    for _ in range(trials):
        wires=[0]*N
        for _ in range(L):
            new=[]
            for _ in range(N):
                a,b,c=rng.choice(wires),rng.choice(wires),rng.choice(wires)
                v=1 if (a+b+c)>=2 else 0
                if rng.random()<e: v^=1
                new.append(v)
            wires=new
        ones=sum(wires)
        if ones>N/2: wrong+=1  # true value 0, majority says 1
    return wrong/trials
