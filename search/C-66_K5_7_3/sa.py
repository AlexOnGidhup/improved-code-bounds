import numpy as np
from numba import njit

@njit(cache=True)
def sa_cover(indptr,indices,sz,rowsz,iters,T0,T1,P,seed,x0):
    # columns j cover rows indices[indptr[j]:indptr[j+1]] (symmetric matrix: use CSC of A)
    np.random.seed(seed)
    K=len(sz)
    x=x0.copy()
    cnt=np.zeros(K,dtype=np.int32)
    w=0
    for j in range(K):
        if x[j]:
            w+=sz[j]
            for k in range(indptr[j],indptr[j+1]): cnt[indices[k]]+=1
    unc=0
    for t in range(K):
        if cnt[t]==0: unc+=rowsz[t]
    best=10**9; bestx=x.copy()
    for it in range(iters):
        T=T0*(T1/T0)**(it/iters)
        j=np.random.randint(K)
        # delta
        if x[j]:
            dw=-sz[j]; du=0
            for k in range(indptr[j],indptr[j+1]):
                r=indices[k]
                if cnt[r]==1: du+=rowsz[r]
        else:
            dw=sz[j]; du=0
            for k in range(indptr[j],indptr[j+1]):
                r=indices[k]
                if cnt[r]==0: du-=rowsz[r]
        d=dw+P*du
        if d<=0 or np.random.random()<np.exp(-d/T):
            if x[j]:
                x[j]=0
                for k in range(indptr[j],indptr[j+1]): cnt[indices[k]]-=1
            else:
                x[j]=1
                for k in range(indptr[j],indptr[j+1]): cnt[indices[k]]+=1
            w+=dw; unc+=du
            if unc==0 and w<best:
                best=w; bestx=x.copy()
    return best,bestx
