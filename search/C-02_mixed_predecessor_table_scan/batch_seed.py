# python batch_seed.py m n d iters maxstag outprefix seedfiles...
import sys,time,numpy as np
from kernel import search
m=int(sys.argv[1]); n=int(sys.argv[2]); d=int(sys.argv[3]); iters=int(sys.argv[4]); maxstag=int(sys.argv[5]); pre=sys.argv[6]
N3=3**n; NB=2**m; NV=NB*N3
assert NV<=4_000_000
dig=np.zeros((N3,n),dtype=np.int8)
for j in range(n): dig[:,j]=(np.arange(N3)//3**j)%3
pw=np.array([3**j for j in range(n)],dtype=np.int64)
popc=np.array([bin(b).count('1') for b in range(NB)],dtype=np.int8)
f=(dig!=0).sum(1).astype(np.int8)
gbest=0
for path in sys.argv[7:]:
    W=[l.strip() for l in open(path) if l.strip()]
    init=np.array([sum(int(w[i])<<i for i in range(m))*N3+sum(int(w[m+j])*3**j for j in range(n)) for w in W],dtype=np.int64)
    t0=time.time()
    best,nfree=search(init,f,dig,pw,popc,NB,N3,n,d,iters,12345,100000,maxstag)
    print(f"{path}: seed={len(W)} frei={nfree} best={len(best)} t={time.time()-t0:.0f}s",flush=True)
    if len(best)>max(len(W),gbest):
        gbest=len(best)
        lines=[''.join(str(((int(v)//N3)>>i)&1) for i in range(m))+''.join(str(x) for x in dig[int(v)%N3]) for v in best]
        open(f"{pre}_{len(best)}.txt",'w').write('\n'.join(lines)+'\n')
        print("geschrieben",f"{pre}_{len(best)}.txt",flush=True)
