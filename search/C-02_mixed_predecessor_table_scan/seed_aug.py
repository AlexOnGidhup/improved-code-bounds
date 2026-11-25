# Saat-Erweiterung: python seed_aug.py seedfile m n d iters seed out maxstag
# seedfile: kanonisch, m Binaerziffern dann n Ternaerziffern je Zeile
import sys,time,numpy as np
from kernel import search
path=sys.argv[1]; m=int(sys.argv[2]); n=int(sys.argv[3]); d=int(sys.argv[4])
iters=int(sys.argv[5]); seed=int(sys.argv[6]); out=sys.argv[7]; maxstag=int(sys.argv[8]) if len(sys.argv)>8 else 300
N3=3**n; NB=2**m; NV=NB*N3
assert NV<=4_000_000
dig=np.zeros((N3,n),dtype=np.int8)
for j in range(n): dig[:,j]=(np.arange(N3)//3**j)%3
pw=np.array([3**j for j in range(n)],dtype=np.int64)
popc=np.array([bin(b).count('1') for b in range(NB)],dtype=np.int8)
f=(dig!=0).sum(1).astype(np.int8)
W=[l.strip() for l in open(path) if l.strip()]
init=np.array([sum(int(w[i])<<i for i in range(m))*N3+sum(int(w[m+j])*3**j for j in range(n)) for w in W],dtype=np.int64)
t0=time.time()
best,nfree=search(init,f,dig,pw,popc,NB,N3,n,d,iters,seed,100000,maxstag)
print(f"{path}: seed={len(W)} freie Woerter={nfree} best={len(best)} t={time.time()-t0:.0f}s",flush=True)
if len(best)>len(W):
    lines=[]
    for v in best:
        b=int(v)//N3;t=int(v)%N3
        lines.append(''.join(str((b>>i)&1) for i in range(m))+''.join(str(x) for x in dig[t]))
    open(out,'w').write('\n'.join(lines)+'\n')
    print("geschrieben",out)
