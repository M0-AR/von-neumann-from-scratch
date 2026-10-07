"""05 — Monte Carlo: pi (dartboard) + neutron shield (Richtmyer/von Neumann 1947).
Neutron: step length Exp(1), 30% absorbed else isotropic scatter in 1-D slab
simplified to: per unit thickness survival ~0.5 (calibrated random walk).
We implement slab transmission: particle at x=0 moving +1; each collision:
absorb w.p. 0.3 else flip direction w.p. 0.5 and advance Exp(mean-free-path=0.5).
Count transmitted x>thickness.
"""
import random, math
def estimate_pi(n, seed=0):
    rng=random.Random(seed); inside=0
    for _ in range(n):
        x=rng.random(); y=rng.random()
        if x*x+y*y<=1: inside+=1
    return 4*inside/n

def neutron_transmission(thickness, n=100000, seed=0, absorb=0.3, mfp=0.8):
    rng=random.Random(seed); through=0
    for _ in range(n):
        x=0.0; d=+1.0
        while True:
            x+=rng.expovariate(1.0/mfp)*d
            if x>thickness: through+=1; break
            if x<0: break  # reflected out
            if rng.random()<absorb: break  # absorbed
            d=+1.0 if rng.random()<0.5 else -1.0
    return through/n
