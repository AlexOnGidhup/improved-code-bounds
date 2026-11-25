# Nebenklassensuche mit vorgegebenem H = ternaerer [n,2]-Code, gegeben durch Vielfachheiten der 4 Punkte von PG(1,3).
# python coset3.py m n d mults(a,b,c,e) rounds iters seed
import sys,time,itertools,numpy as np
from kernel import search
m=int(sys.argv[1]); n=int(sys.argv[2]); d=int(sys.argv[3]); mult=[int(x) for x in sys.argv[4].split(',')]
rounds=int(sys.argv[5]); iters=int(sys.argv[6]); seed=int(sys.argv[7])
assert sum(mult)==n and mult[0]>=1 and mult[1]>=1
k=2; r=n-k
pts=[(1,0),(0,1),(1,1),(1,2)]
cols=[pts[0]]*(mult[0]-1)+[pts[1]]*(mult[1]-1)+[pts[2]]*mult[2]+[pts[3]]*mult[3]
A=np.array(cols,dtype=np.int64).T.reshape(2,r)
N3=3**r; NB=2**m; NV=NB*N3
assert NV<=3_000_000
dig=np.zeros((N3,r),dtype=np.int8)
for j in range(r): dig[:,j]=(np.arange(N3)//3**j)%3
pw=np.array([3**j for j in range(r)],dtype=np.int64)
popc=np.array([bin(b).count('1') for b in range(NB)],dtype=np.int8)
cs=np.array(list(itertools.product(range(3),repeat=k)),dtype=np.int64)
f=np.full(N3,99,dtype=np.int8)
for c in cs:
    sh=(c@A)%3
    f=np.minimum(f,(((dig+sh[None,:])%3!=0).sum(1)+(c!=0).sum()).astype(np.int8))
rng=np.random.default_rng(seed)
gbest=0;t0=time.time()
for rd in range(rounds):
    Kb,_=search(np.array([0],dtype=np.int64),f,dig,pw,popc,NB,N3,r,d,iters,int(rng.integers(1<<30)),100000,300)
    if len(Kb)>gbest:
        gbest=len(Kb)
        lines=[]
        for v in Kb:
            b=int(v)//N3;t=int(v)%N3
            for c in cs:
                tt=(dig[t]+(c@A))%3
                lines.append(''.join(str((b>>i)&1) for i in range(m))+''.join(map(str,c))+''.join(map(str,tt)))
        open(f"c3_{m}_{n}_{d}_{'-'.join(map(str,mult))}.txt",'w').write('\n'.join(lines)+'\n')
    print(f"({m},{n},{d}) mult={mult} round {rd} cosets={len(Kb)} size={9*len(Kb)} best={9*gbest} t={time.time()-t0:.0f}s",flush=True)
