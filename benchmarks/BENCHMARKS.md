# Benchmarks (measured 2026-10-07, linux/python3.12, seeds fixed)
- minimax empty: 549946 nodes, value 0
- penalty: p=38.33% q=41.67% v=79.58; fict 38.27/41.54 @100k
- machine add5: 63 in 55 steps; mul 42 in 56 steps; mystery 1024
- sort1000: merge 8726 vs insert 252826 = 28.97x
- pi: 3.04/3.1352/3.14844; neutron 0.476/0.235/0.060/0.0037
- middle-square: mean 43.71 max 111 seed 6239; debias 41992 bits @200k 49.79%
- reliable single 43.37%; N=99 cliff 0/0.003/0.355/0.494
- fredkin 4@8 16@24 64@56 (128 grid); live AAPL 336.9 BTC 83392 VaR5 294.99
Full JSON: results/results.json
