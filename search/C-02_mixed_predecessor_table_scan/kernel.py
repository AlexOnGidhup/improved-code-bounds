import numpy as np
from numba import njit

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
def search(init,f,dig,pw,popc,NB,N3,r,d,iters,seed,target,maxstag):
    np.random.seed(seed)
    NV=NB*N3
    cnt=np.zeros(NV,np.int32)
    inK=np.zeros(NV,np.bool_)
    tabu=np.zeros(NV,np.int64)
    buf0=np.empty(NV,np.int64); buf1=np.empty(NV,np.int64)
    K=np.empty(8192,np.int64); nK=0
    best=np.empty(8192,np.int64); nbest=0
    for i in range(len(init)):
        K[nK]=init[i]; nK+=1; inK[init[i]]=True
        upd(cnt,init[i],1,f,dig,pw,popc,NB,N3,r,d)
    nbest=nK
    for i in range(nK): best[i]=K[i]
    stagn=0
    nfree0=-1
    for it in range(iters):
        c0=-1;n0=0;c1=-1;n1=0
        for v in range(NV):
            cv=cnt[v]
            if cv==0:
                buf0[n0]=v;n0+=1
            elif cv==1 and n0==0 and (not inK[v]) and tabu[v]<=it:
                buf1[n1]=v;n1+=1
        if it==0: nfree0=n0
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
        elif c1>=0 and stagn<maxstag:
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
            nrem=1+np.random.randint(3)
            stagn=0
            for _ in range(nrem):
                if nK<=1: break
                u=np.random.randint(nK)
                uu=K[u]
                K[u]=K[nK-1];nK-=1;inK[uu]=False
                upd(cnt,uu,-1,f,dig,pw,popc,NB,N3,r,d)
                tabu[uu]=it+5+np.random.randint(10)
    return best[:nbest].copy(), nfree0
