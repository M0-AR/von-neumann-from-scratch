"""01 — Minimax perfect play for tic-tac-toe (von Neumann 1928).
Board: 9-char string, 'X','O',' '. +1 X wins, -1 O wins, 0 draw.
X maximises, O minimises. Node counter reproduces the ~549,946 claim.
"""
WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def winner(board):
    for a,b,c in WINS:
        if board[a] != ' ' and board[a]==board[b]==board[c]:
            return board[a]
    return None

def is_full(board):
    return ' ' not in board

def minimax(board, turn, counter=None):
    if counter is not None:
        counter[0]+=1
    w = winner(board)
    if w=='X': return 1
    if w=='O': return -1
    if is_full(board): return 0
    vals=[]
    for i,ch in enumerate(board):
        if ch==' ':
            nb=board[:i]+turn+board[i+1:]
            v=minimax(nb,'O' if turn=='X' else 'X',counter)
            vals.append(v)
    return max(vals) if turn=='X' else min(vals)

from functools import lru_cache
@lru_cache(maxsize=None)
def _minimax_fast(board, turn):
    w=winner(board)
    if w=='X': return 1
    if w=='O': return -1
    if is_full(board): return 0
    if turn=='X':
        best=-10
        for i,ch in enumerate(board):
            if ch==' ':
                v=_minimax_fast(board[:i]+turn+board[i+1:],'O')
                if v>best: best=v
                if best==1: break
        return best
    else:
        best=10
        for i,ch in enumerate(board):
            if ch==' ':
                v=_minimax_fast(board[:i]+turn+board[i+1:],'X')
                if v<best: best=v
                if best==-1: break
        return best

def best_move(board, turn):
    best=None; bestv=-10 if turn=='X' else 10
    for i,ch in enumerate(board):
        if ch==' ':
            nb=board[:i]+turn+board[i+1:]
            v=_minimax_fast(nb,'O' if turn=='X' else 'X')
            if (turn=='X' and v>bestv) or (turn=='O' and v<bestv):
                bestv=v; best=i
    return best,bestv

def play_vs_random(seed=0, n=1000, as_x=True):
    import random
    rng=random.Random(seed)
    w=d=l=0
    for _ in range(n):
        b=' '*9; turn='X'
        while True:
            if (turn=='X')==as_x:
                m,_=best_move(b,turn)
            else:
                empt=[i for i,c in enumerate(b) if c==' ']
                m=rng.choice(empt)
            b=b[:m]+turn+b[m+1:]
            win=winner(b)
            if win or is_full(b):
                if win=='X': res='X'
                elif win=='O': res='O'
                else: res='D'
                me='X' if as_x else 'O'
                if res=='D': d+=1
                elif res==me: w+=1
                else: l+=1
                break
            turn='O' if turn=='X' else 'X'
    return w,d,l
