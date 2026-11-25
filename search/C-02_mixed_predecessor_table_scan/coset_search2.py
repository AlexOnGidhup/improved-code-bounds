# Nebenklassen-Clique-Suche fuer gemischte binaer/ternaere Codes N(m,n,d).
# H = ternaerer linearer [n,k]-Code (systematisch [I|A]) auf den ternaeren Koordinaten.
# Quotient Q = Z2^m x Z3^r, r=n-k. Clique im Cayley-Graphen via lokaler Suche.
import sys, time, itertools, os
import numpy as np
from numba import njit

m=int(sys.argv[1]); n=int(sys.argv[2]); d=int(sys.argv[3]); k=int(sys.argv[4])
tlimit=float(sys.argv[5]); seed=int(sys.argv[6])
tag=sys.argv[7] if len(sys.argv)>7 else ''
k2=int(sys.argv[9]) if len(sys.argv)>9 else 0
mr=m-k2
r=n-k
rng=np.random.default_rng(seed)
N3=3**r; NB=2**mr; NV=NB*N3
assert NV<=3_000_000, "Quotient zu gross"
dig=np.zeros((N3,r),dtype=np.int8)
for j in range(r):
    dig[:,j]=(np.arange(N3)//3**j)%3
pw=np.array([3**j for j in range(r)],dtype=np.int64)
popc0=np.array([bin(b).count('1') for b in range(max(NB,2**k2))],dtype=np.int8)
def make_H2():
    # binaerer [m,k2]-Code [I|B] mit Minimalgewicht >= d; Zeilen von B als Bitmasken ueber mr Bits
    while True:
        B=[int(x) for x in rng.integers(0,NB,size=k2)]
        ok=True; sh=[0]*(2**k2)
        for c in range(2**k2):
            x=0
            for i in range(k2):
                if (c>>i)&1: x^=B[i]
            sh[c]=x
            if c and popc0[c]+popc0[x]<d: ok=False;break
        if ok: return B,sh
def compute_f2(sh):
    f2=np.full(NB,99,dtype=np.int8)
    bs=np.arange(NB)
    for c in range(2**k2):
        f2=np.minimum(f2,(popc0[bs^sh[c]]+popc0[c]).astype(np.int8))
    return f2

def make_H():
    # zufaelliges A mit Minimalgewicht >= d
    if k==0: return np.zeros((0,r),dtype=np.int64)
    cs=np.array(list(itertools.product(range(3),repeat=k)),dtype=np.int64)[1:]
    while True:
        A=rng.integers(0,3,size=(k,r))
        W=(cs!=0).sum(1)+(((cs@A)%3)!=0).sum(1)
        if W.min()>=d: return A

def compute_f(A):
    cs=np.array(list(itertools.product(range(3),repeat=k)),dtype=np.int64).reshape(3**k,k)
    f=np.full(N3,99,dtype=np.int8)
    for c in cs:
        sh=(c@A)%3
        w=((dig+sh[None,:])%3!=0).sum(1)+(c!=0).sum()
        f=np.minimum(f,w.astype(np.int8))
    return f

@njit(cache=True)
def upd(cnt,a,sign,f,dig,pw,popc,NB,N3,r,d):
    ba=a//N3; ta=a%N3
    g=np.empty(N3,np.int8)
    for t in range(N3):
        s=0
        for j in range(r):
            x=dig[t,j]-dig[ta,j]
            if x<0: x+=3
            s+=x*pw[j]
        g[t]=f[s]
    for b in range(NB):
        thr=d-popc[b^ba]
        base=b*N3
        for t in range(N3):
            if g[t]<thr:
                cnt[base+t]+=sign

@njit(cache=True)
def nonadj(a,v,f,dig,pw,popc,N3,r,d):
    ba=a//N3; ta=a%N3; bv=v//N3; tv=v%N3
    s=0
    for j in range(r):
        x=dig[tv,j]-dig[ta,j]
        if x<0: x+=3
        s+=x*pw[j]
    return popc[ba^bv]+f[s]<d

@njit(cache=True)
def search(f,dig,pw,popc,NB,N3,r,d,iters,seed,target):
    np.random.seed(seed)
    NV=NB*N3
    cnt=np.zeros(NV,np.int32)
    inK=np.zeros(NV,np.bool_)
    tabu=np.zeros(NV,np.int64)
    buf0=np.empty(NV,np.int64); buf1=np.empty(NV,np.int64)
    K=np.empty(4096,np.int64); nK=0
    best=np.empty(4096,np.int64); nbest=0
    # start with 0
    K[0]=0; nK=1; inK[0]=True
    upd(cnt,0,1,f,dig,pw,popc,NB,N3,r,d)
    stagn=0
    for it in range(iters):
        # reservoir sample cnt==0 and cnt==1
        c0=-1;n0=0;c1=-1;n1=0
        for v in range(NV):
            cv=cnt[v]
            if cv==0:
                buf0[n0]=v;n0+=1
            elif cv==1 and n0==0 and (not inK[v]) and tabu[v]<=it:
                buf1[n1]=v;n1+=1
        if n0>0: c0=buf0[np.random.randint(n0)]
        elif n1>0: c1=buf1[np.random.randint(n1)]
        if c0>=0:
            K[nK]=c0;nK+=1;inK[c0]=True
            upd(cnt,c0,1,f,dig,pw,popc,NB,N3,r,d)
            if nK>nbest:
                nbest=nK
                for i in range(nK): best[i]=K[i]
                stagn=0
                if nbest>=target: break
        elif c1>=0 and stagn<400:
            # find conflicting member
            u=-1
            for i in range(nK):
                if nonadj(K[i],c1,f,dig,pw,popc,N3,r,d):
                    u=i;break
            uu=K[u]
            K[u]=K[nK-1];nK-=1;inK[uu]=False
            upd(cnt,uu,-1,f,dig,pw,popc,NB,N3,r,d)
            tabu[uu]=it+2+np.random.randint(6)
            K[nK]=c1;nK+=1;inK[c1]=True
            upd(cnt,c1,1,f,dig,pw,popc,NB,N3,r,d)
            stagn+=1
        else:
            # perturbation: remove some random members
            nrem=1+np.random.randint(3)
            if stagn>=400: nrem=max(1,nK//3)
            stagn=0
            for _ in range(nrem):
                if nK<=1: break
                u=np.random.randint(nK)
                uu=K[u]
                K[u]=K[nK-1];nK-=1;inK[uu]=False
                upd(cnt,uu,-1,f,dig,pw,popc,NB,N3,r,d)
                tabu[uu]=it+5+np.random.randint(10)
    return best[:nbest].copy()

def write_code(A,Kset,path):
    cs=np.array(list(itertools.product(range(3),repeat=k)),dtype=np.int64).reshape(3**k,k)
    lines=[]
    for v in Kset:
        b=int(v)//N3; t=int(v)%N3
        for c2 in range(2**k2):
            b2=b^SH[c2]
            bb=[(c2>>i)&1 for i in range(k2)]+[(b2>>i)&1 for i in range(mr)]
            for c in cs:
                tt=(dig[t]+(c@A))%3
                lines.append(''.join(map(str,bb))+''.join(map(str,c))+''.join(map(str,tt)))
    open(path,'w').write('\n'.join(lines)+'\n')

t0=time.time(); gbest=0
iters=int(sys.argv[8]) if len(sys.argv)>8 else 3000
rnd=0
while time.time()-t0<tlimit:
    A=make_H(); f=compute_f(A)
    Bm,SH=make_H2(); popc=compute_f2(SH)
    S=int(((popc[:,None]+f[None,:])>=d).sum())
    Kb=search(f,dig,pw,popc,NB,N3,r,d,iters,int(rng.integers(1<<30)),4000)
    size=len(Kb)*3**k*2**k2
    rnd+=1
    print(f"round {rnd} t={time.time()-t0:.0f}s |S|={S}/{NV} cosets={len(Kb)} size={size} best={max(gbest,size)}",flush=True)
    if size>gbest:
        gbest=size
        write_code(A,Kb,f"cand_{m}_{n}_{d}_k{k}_b{k2}{tag}.txt")
