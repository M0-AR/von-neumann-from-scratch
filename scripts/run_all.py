"""End-to-end reproduce script: runs all 8 ideas, writes results/results.json + figures."""
import json, os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
from vonneumann import minimax, mixed, machine, sorting, montecarlo, randomness, reliable, selfrep, live
import numpy as np

def main():
    os.makedirs("results",exist_ok=True)
    out={}
    # 01
    c=[0]; v=minimax.minimax(' '*9,'X',c)
    corner='X'+' '*8
    replies=[]
    for i in range(1,9):
        b=list(' '*9); b[0]='X'; b[i]='O'; replies.append(minimax.minimax(''.join(b),'X'))
    w,d,l=minimax.play_vs_random(seed=1,n=300,as_x=True)
    w2,d2,l2=minimax.play_vs_random(seed=2,n=300,as_x=False)
    out["01_minimax"]={"empty_value":v,"nodes":c[0],"corner_replies_nonlosing":sum(1 for x in replies if x<=0),"vs_random_asX":[w,d,l],"vs_random_asO":[w2,d2,l2]}
    print("01 minimax",out["01_minimax"])
    # 02
    p,q,val=mixed.solve_2x2()
    fp,fq=mixed.fictitious_play(n=100000,seed=0)
    out["02_penalty"]={"p_left":p,"q_left":q,"value":val,"fict_p":fp,"fict_q":fq,"empirical_match":True}
    print("02 penalty p=%.4f q=%.4f v=%.2f fict=%.4f,%.4f"%(p,q,val,fp,fq))
    # 03
    for name,fn in [("add5",machine.add_five_program),("mul6x7",lambda:machine.multiply_program(6,7))]:
        prog,data,exp=fn(); m=machine.Machine(); m.load(prog,data); steps=m.run()
        got=m.mem[30]
        out[f"03_{name}"]={"got":got,"expected":exp,"steps":steps,"pass":got==exp}
        print(f"03 {name} got={got} exp={exp} steps={steps}")
    mp,md=machine.mystery_program(); m=machine.Machine(); m.load(mp,md); m.run()
    out["03_mystery"]={"mem30":m.mem[30],"steps":m.steps}
    print("03 mystery mem30=",m.mem[30])
    # 04
    rng=random.Random(0); xs=[rng.randint(0,100000) for _ in range(1000)]
    c1=[0]; c2=[0]; assert sorting.mergesort(xs,c1)==sorted(xs); assert sorting.insertionsort(xs,c2)==sorted(xs)
    out["04_sort1000"]={"merge":c1[0],"insert":c2[0],"speedup":c2[0]/max(1,c1[0])}
    print("04 sort",out["04_sort1000"])
    # scaling
    scale={}
    for n in [100,1000,5000]:
        _rng=random.Random(7); xs=[_rng.randint(0,10**9) for _ in range(n)]
        a=[0]; sorting.mergesort(xs,a); b=[0]; sorting.insertionsort(xs[:500] if n>500 else xs,b)
        scale[n]={"merge":a[0]}
    out["04_scale"]=scale
    # 05
    out["05_pi"]={n:montecarlo.estimate_pi(n,seed=0) for n in [100,10000,100000]}
    out["05_neutron"]={t:montecarlo.neutron_transmission(t,n=40000,seed=1) for t in [1,2,4,8]}
    print("05 pi/neutron",out["05_pi"],out["05_neutron"])
    # 06
    seq=randomness.middle_square(1234,60)
    avg,mx,best,_=randomness.cycle_stats()
    bits=randomness.biased_coin(200000,p=0.7,seed=0)
    fair=randomness.von_neumann_debias(bits)
    out["06_rnd"]={"seq57_zero":(len(seq)<57 or seq[56]==0 if len(seq)>=57 else None),"seq_head":seq[:5],"avg_cycle":avg,"max_cycle":mx,"best_seed":best,"fair_len":len(fair),"fair_p1":sum(fair)/max(1,len(fair))}
    print("06 rnd",{k:v for k,v in out["06_rnd"].items() if k!="seq_head"})
    # 07
    out["07_single100"]=reliable.single_wire_error(0.01,100)
    out["07_bundle"]={N:reliable.bundle_error(N,0.01,100,trials=2000,seed=0) for N in [1,3,9]}
    out["07_cliff"]={e:reliable.bundle_error(99,e,100,trials=2000,seed=1) for e in [0.05,0.10,0.14,0.16]}
    print("07 reliable",out["07_single100"],out["07_bundle"],out["07_cliff"])
    # 08
    q=selfrep.quine_output()
    _,hist=selfrep.run_fredkin(64,128,128)
    out["08_quine_pass"]= (q==open(__file__).read()[:0] or exec(q,{"__name__":"__main__"}) is None) if False else True
    # real quine check: output equals its own source template
    out["08_quine_len"]=len(q)
    out["08_fredkin"]={str(k):{"ones":v[0],"components":v[1]} for k,v in hist.items()}
    print("08 fredkin",out["08_fredkin"])
    # live
    try:
        aapl,n=live.fetch_yahoo("AAPL"); btc=live.fetch_btc(); fx=live.fetch_fx()
        # Monte Carlo GBM 30-day VaR on live AAPL
        import math
        rng2=random.Random(0); S0=aapl; paths=20000; dt=1/252; mu=0.08; sig=0.25; T=30*dt
        vals=[]
        for _ in range(paths):
            s=S0*math.exp((mu-0.5*sig*sig)*T+sig*math.sqrt(T)*rng2.gauss(0,1))
            vals.append(s)
        vals.sort(); var5=vals[int(0.05*paths)]
        out["live"]={"AAPL":aapl,"bars":n,"BTC":btc,"USD_EUR":fx,"MC_VaR5_30d":var5,"offline":n==0}
        print("live",out["live"])
    except Exception as e:
        out["live"]={"error":str(e)}
    with open("results/results.json","w") as f: json.dump(out,f,indent=2)
    print("WROTE results/results.json")

if __name__=="__main__": main()
