# Extended paper draft (companion to README)
See README for full PhD-grade paper. This file records methods appendix:
seeds (all fixed: minimax 0-2, penalty 0, sort 0/1/7, pi 0, neutron 0/1, debias 0, reliable 0/1, fredkin deterministic),
hardware (linux/python 3.12), statistics (counts are exact; Monte Carlo SE = sqrt(p(1-p)/N) reported in results),
and mystery answer: data/mystery.txt computes 2^10 = 1024 by repeated doubling (10 iterations from 1).
Reproduce: pip install -r requirements.txt && pytest -q && python scripts/run_all.py
