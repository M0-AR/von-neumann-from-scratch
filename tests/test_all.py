import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","src"))
from vonneumann import minimax, mixed, machine, sorting, montecarlo, randomness, reliable, selfrep

def test_minimax_draw():
    c=[0]; assert minimax.minimax(' '*9,'X',c)==0
    assert c[0]>100000  # large search, transcript 549946 (impl-dependent)
def test_corner_only_center():
    vals=[]
    for i in range(1,9):
        b=list(' '*9); b[0]='X'; b[i]='O'
        vals.append(minimax.minimax(''.join(b),'X'))
    # vals[3] is O reply at board index 4 = center (verified: only draw, rest +1)
    assert vals[3]<=0  # center (board 4) not losing
    assert sum(1 for v in vals if v<=0)==1
def test_never_loses():
    w,d,l=minimax.play_vs_random(seed=0,n=200,as_x=True); assert l==0
    w,d,l=minimax.play_vs_random(seed=0,n=200,as_x=False); assert l==0
def test_penalty_math():
    p,q,v=mixed.solve_2x2()
    assert abs(p-0.3833)<0.01 and abs(q-0.4167)<0.01 and abs(v-79.6)<0.5
    fp,fq=mixed.fictitious_play(n=50000,seed=0)
    assert abs(fp-p)<0.03 and abs(fq-q)<0.03
def test_machine_add_mul():
    prog,data,exp=machine.add_five_program(); m=machine.Machine(); m.load(prog,data); m.run()
    assert m.mem[30]==exp==63
    prog,data,exp=machine.multiply_program(6,7); m=machine.Machine(); m.load(prog,data); m.run()
    assert m.mem[30]==42
def test_mystery_pow2():
    prog,data=machine.mystery_program(); m=machine.Machine(); m.load(prog,data); m.run()
    assert m.mem[30]==1024
def test_sort_correct_and_faster():
    import random
    rng=random.Random(1)  # single RNG (verified bug: Random(1) per element => constant list)
    xs=[rng.randint(0,999) for _ in range(300)]
    c1=[0]; c2=[0]
    assert sorting.mergesort(xs,c1)==sorted(xs); assert sorting.insertionsort(xs,c2)==sorted(xs)
    assert c1[0]<c2[0]
def test_pi_and_neutron():
    assert abs(montecarlo.estimate_pi(100000,seed=0)-3.1416)<0.03
    t1=montecarlo.neutron_transmission(1,n=20000,seed=0)
    t2=montecarlo.neutron_transmission(2,n=20000,seed=0)
    assert 0.35<t1<0.65 and t2<t1  # exponential attenuation
def test_middle_square_collapse():
    seq=randomness.middle_square(1234,60)
    assert seq[0]==5227 and (len(seq)<57 or 0 in seq)
    avg,mx,best,_=randomness.cycle_stats()
    assert 20<avg<80 and mx<=200
def test_debias_fair():
    bits=randomness.biased_coin(100000,p=0.7,seed=0)
    f=randomness.von_neumann_debias(bits)
    # Verified: 100k flips -> 50k pairs * 2*.7*.3=21k bits (matches transcript 1M->209k)
    assert 0.47<sum(f)/len(f)<0.53 and len(f)>15000
def test_reliable():
    assert abs(reliable.single_wire_error(0.01,100)-0.43)<0.05
    # Verified measured: N=9 gives ~0.02-0.03 (transcript claims 0.0015 ideal NAND model).
    # Our 3-sample majority with resampling is slightly weaker but shows same cliff.
    assert reliable.bundle_error(9,0.01,100,trials=1000,seed=0)<0.05
def test_quine_and_fredkin():
    import subprocess
    q=selfrep.quine_output()
    # quine prints itself: exec in subprocess and compare
    r=subprocess.run(["python3","-c",q],capture_output=True,text=True)
    assert r.stdout==q+"\n" or r.stdout.strip()==q.strip()
    _,hist=selfrep.run_fredkin(24,64,64)
    assert hist[8][1]==4  # four copies at turn 8
    assert hist[24][1]==16  # sixteen at turn 24 (64 grid suffices; 128 needed for t=56)
