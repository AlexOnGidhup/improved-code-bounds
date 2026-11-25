# Saat-Augmentierung im Quotienten nach einer ternaeren Untergruppe <h> der Ordnung 3 (Checkpoints).
# python deepH.py seedfile m n d h chunk_iters maxstag rngseed outprefix tlimit_s
# h = Ternaerwort der Laenge n (nur Ternaerteil); die Saat muss unter Translation mit h invariant sein.
import sys,time,numpy as np
from kernel import search
path=sys.argv[1]; m=int(sys.argv[2]); n=int(sys.argv[3]); d=int(sys.argv[4]); h=[int(c) for c in sys.argv[5]]
chunk=int(sys.argv[6]); maxstag=int(sys.argv[7]); rs=int(sys.argv[8]); pre=sys.argv[9]; tlim=float(sys.argv[10])
assert len(h)==n
p=min(i for i in range(n) if h[i])
if h[p]==2: h=[(2*x)%3 for x in h]
hr=np.array(h[:p]+h[p+1:],dtype=np.int64)
r=n-1; N3=3**r; NB=2**m; NV=NB*N3
assert NV<=5_000_000
dig=np.zeros((N3,r),dtype=np.int8)
for j in range(r): dig[:,j]=(np.arange(N3)//3**j)%3
pw=np.array([3**j for j in range(r)],dtype=np.int64)
popc=np.array([bin(b).count('1') for b in range(NB)],dtype=np.int8)
f=np.full(N3,99,dtype=np.int8)
for c in range(3):
    w=(((dig+c*hr[None,:])%3)!=0).sum(1)+(c!=0)
    f=np.minimum(f,w.astype(np.int8))
W=[l.strip() for l in open(path) if l.strip()]
reps=set()
for w in W:
    b=sum(int(w[i])<<i for i in range(m)); t=[int(c) for c in w[m:]]
    c=t[p]; t=[(x-c*y)%3 for x,y in zip(t,h)]
    q=t[:p]+t[p+1:]
    reps.add(b*N3+sum(q[j]*3**j for j in range(r)))
assert len(reps)*3==len(W), "Saat nicht h-invariant"
cur=np.array(sorted(reps),dtype=np.int64)
def write(cur):
    lines=[]
    for v in cur:
        b=int(v)//N3; q=[int(x) for x in dig[int(v)%N3]]
        t0=q[:p]+[0]+q[p:]
        for c in range(3):
            t=[(x+c*y)%3 for x,y in zip(t0,h)]
            lines.append(''.join(str((b>>i)&1) for i in range(m))+''.join(map(str,t)))
    fn=f"{pre}_{len(lines)}.txt"
    open(fn,'w').write('\n'.join(lines)+'\n'); print("geschrieben",fn,flush=True)
t0=time.time(); c=0
while time.time()-t0<tlim:
    best,nfree=search(cur,f,dig,pw,popc,NB,N3,r,d,chunk,rs+c,100000,maxstag)
    c+=1
    print(f"{path} chunk {c} t={time.time()-t0:.0f}s start={3*len(cur)} frei0={nfree} best={3*len(best)}",flush=True)
    if len(best)>len(cur):
        cur=best; write(cur)
