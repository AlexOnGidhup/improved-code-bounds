# Tiefe Saat-Augmentierung mit Checkpoints.
# python deep.py seedfile m n d chunk_iters maxstag rngseed outprefix tlimit_s
import sys,time,numpy as np
from kernel import search
path=sys.argv[1]; m=int(sys.argv[2]); n=int(sys.argv[3]); d=int(sys.argv[4])
chunk=int(sys.argv[5]); maxstag=int(sys.argv[6]); rs=int(sys.argv[7]); pre=sys.argv[8]; tlim=float(sys.argv[9])
N3=3**n; NB=2**m; NV=NB*N3
assert NV<=5_000_000  # ~0.4 GB
dig=np.zeros((N3,n),dtype=np.int8)
for j in range(n): dig[:,j]=(np.arange(N3)//3**j)%3
pw=np.array([3**j for j in range(n)],dtype=np.int64)
popc=np.array([bin(b).count('1') for b in range(NB)],dtype=np.int8)
f=(dig!=0).sum(1).astype(np.int8)
W=[l.strip() for l in open(path) if l.strip()]
cur=np.array([sum(int(w[i])<<i for i in range(m))*N3+sum(int(w[m+j])*3**j for j in range(n)) for w in W],dtype=np.int64)
t0=time.time(); c=0; n0=len(cur)
while time.time()-t0<tlim:
    best,nfree=search(cur,f,dig,pw,popc,NB,N3,n,d,chunk,rs+c,100000,maxstag)
    c+=1
    print(f"{path} chunk {c} t={time.time()-t0:.0f}s start={len(cur)} frei0={nfree} best={len(best)}",flush=True)
    if len(best)>len(cur):
        cur=best
        lines=[''.join(str(((int(v)//N3)>>i)&1) for i in range(m))+''.join(str(x) for x in dig[int(v)%N3]) for v in cur]
        open(f"{pre}_{len(cur)}.txt",'w').write('\n'.join(lines)+'\n')
        print("geschrieben",f"{pre}_{len(cur)}.txt",flush=True)
