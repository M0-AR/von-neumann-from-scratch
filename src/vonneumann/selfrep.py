"""08 — Machines that copy themselves.
A) Quine: s is description used twice (as template + as data).
B) Fredkin replicator: next cell = 1 iff ODD number of 4 von-Neumann neighbours are 1.
   next = (N+S+E+W) mod 2 == 1. Copies ANY pattern at t=8,16?,24,56 (powers pattern).
   We count connected components to verify 1->4->16->64 copies.
"""
from collections import deque
QUINE = 's={0!r}\nprint(s.format(s))'

def quine_output():
    s='s={0!r}\nprint(s.format(s))'
    return s.format(s)

def step_fredkin(grid):
    H=len(grid); W=len(grid[0])
    ng=[[0]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            n=0
            if y>0: n+=grid[y-1][x]
            if y<H-1: n+=grid[y+1][x]
            if x>0: n+=grid[y][x-1]
            if x<W-1: n+=grid[y][x+1]
            ng[y][x]=1 if n%2==1 else 0
    return ng

def seed_v(H=128,W=128):
    g=[[0]*W for _ in range(H)]
    cy,cx=H//2,W//2
    # Connected small V (verified: 1 comp -> 4 @t8 -> 16 @t24 -> 64 @t56 on >=128 grid).
    # Diagonal-only V gives 5 comps and 20 @t8 (4x per cell); orthogonal connectivity
    # is required for clean 1->4->16->64 counting. Boundary needs margin >= t.
    for dy,dx in [(0,0),(1,0),(2,-1),(2,1),(2,0)]:
        g[cy+dy][cx+dx]=1
    return g

def count_components(grid):
    H=len(grid); W=len(grid[0]); seen=[[False]*W for _ in range(H)]; c=0
    for y in range(H):
        for x in range(W):
            if grid[y][x] and not seen[y][x]:
                c+=1
                dq=deque([(y,x)]); seen[y][x]=True
                while dq:
                    yy,xx=dq.popleft()
                    for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
                        ny,nx=yy+dy,xx+dx
                        if 0<=ny<H and 0<=nx<W and grid[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx]=True; dq.append((ny,nx))
    return c

def run_fredkin(steps=64, H=128, W=128):
    g=seed_v(H,W); hist={0:(sum(map(sum,g)),count_components(g))}
    for t in range(1,steps+1):
        g=step_fredkin(g)
        if t in (1,2,8,16,24,56,64):
            hist[t]=(sum(map(sum,g)),count_components(g))
    return g,hist
