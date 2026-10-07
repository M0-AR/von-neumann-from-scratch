"""03 — Stored-program computer (EDVAC 1945, 101pp).
Memory = list of ints. ACC + PC. Instruction = op*100 + addr.
7 ops: 1 LOAD, 2 ADD, 3 SUB, 4 STORE, 5 JUMP, 6 JUMPIFZERO, 7 HALT.
Self-modifying code: program rewrites its own ADD addr (cell 1 holds 220...).
"""
HALT=7
class Machine:
    def __init__(self, mem_size=64):
        self.mem=[0]*mem_size; self.acc=0; self.pc=0; self.steps=0
    def load(self, prog, data):
        for k,v in prog.items(): self.mem[k]=v
        for k,v in data.items(): self.mem[k]=v
    def step(self):
        instr=self.mem[self.pc]
        op,addr=divmod(instr,100)
        npc=self.pc+1
        if op==1: self.acc=self.mem[addr]
        elif op==2: self.acc+=self.mem[addr]
        elif op==3: self.acc-=self.mem[addr]
        elif op==4: self.mem[addr]=self.acc
        elif op==5: npc=addr
        elif op==6:
            if self.acc==0: npc=addr
        elif op==7: return False
        else: raise ValueError(f"bad op {op}")
        self.pc=npc; self.steps+=1
        return True
    def run(self, limit=100000):
        while self.steps<limit:
            if self.mem[self.pc]//100==HALT: self.steps+=1; break
            if not self.step(): break
        return self.steps

def add_five_program():
    # Adds mem[20..24] -> mem[30]. Self-modifying pointer at cell 1.
    # Layout: 0:LOAD 20? Actually cell1 will be mutated ADD 20..24.
    # Code: 0 LOAD 31(zero) ; 1 ADD 20 ; 2 STORE 30 ; 3 LOAD 1 ; 4 ADD 32(one) ; 5 STORE 1
    #       6 LOAD 33(count) ; 7 SUB 32 ; 8 STORE 33 ; 9 JUMPIFZERO 11 ; 10 JUMP 0 ; 11 HALT
    # Wait: above double-counts. Simpler loop: acc accumulates? Need running total in 30.
    # Correct loop: 0 LOAD 30; 1 ADD 20; 2 STORE 30; 3 LOAD 1; 4 ADD 32; 5 STORE 1;
    # 6 LOAD 33; 7 SUB 32; 8 STORE 33; 9 JUMPIFZERO 11(end); 10 JUMP 0; 11 HALT
    prog={0:130,1:220,2:430,3:101,4:232,5:401,6:133,7:332,8:433,9:611,10:500,11:700}
    data={20:7,21:11,22:13,23:15,24:17, 30:0,31:0,32:1,33:5}
    return prog,data,63

def multiply_program(a=6,b=7):
    # Repeated addition: total in 30, counter in 33 (=b), addend a in 34.
    # 0 LOAD 30; 1 ADD 34; 2 STORE 30; 3 LOAD 33; 4 SUB 32; 5 STORE 33;
    # 6 JUMPIFZERO 8; 7 JUMP 0; 8 HALT
    prog={0:130,1:234,2:430,3:133,4:332,5:433,6:608,7:500,8:700}
    data={30:0,32:1,33:b,34:a}
    return prog,data,a*b

def mystery_program():
    # Mystery: computes 2^10 = 1024 by doubling loop (solution hidden from README puzzle).
    # 0 LOAD 30; 1 ADD 30 (double); 2 STORE 30; 3 LOAD 33; 4 SUB 32; 5 STORE 33;
    # 6 JUMPIFZERO 8; 7 JUMP 0; 8 HALT ; init 30=1? Actually start 30=1, count 33=10.
    # First iter: 1+1=2 ... after 10 iters 1024? Let's trace: init 30=1? step doubles 10 times -> 1024. yes.
    prog={0:130,1:230,2:430,3:133,4:332,5:433,6:608,7:500,8:700}
    data={30:1,32:1,33:10}
    return prog,data
