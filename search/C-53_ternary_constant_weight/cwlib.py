import numpy as np, itertools, numba as nb, time, sys

def words(n,w):
    out=[]
    for supp in itertools.combinations(range(n),w):
        for vals in itertools.product((1,2),repeat=w):
            x=[0]*n
            for p,v in zip(supp,vals): x[p]=v
            out.append(x)
    return np.array(out,dtype=np.int8)

@nb.njit(cache=True)
def build_adj(X,d):
    N,n=X.shape
    cnt=np.zeros(N,np.int64)
    for i in range(N):
        for j in range(N):
            if i!=j:
                s=0
                for k in range(n):
                    if X[i,k]!=X[j,k]: s+=1
                if s<d: cnt[i]+=1
    ptr=np.zeros(N+1,np.int64)
    for i in range(N): ptr[i+1]=ptr[i]+cnt[i]
    adj=np.empty(ptr[N],np.int32)
    for i in range(N):
        p=ptr[i]
        for j in range(N):
            if i!=j:
                s=0
                for k in range(n):
                    if X[i,k]!=X[j,k]: s+=1
                if s<d:
                    adj[p]=j; p+=1
    return ptr,adj

@nb.njit(cache=True)
def search(ptr,adj,iters,seed,init,tabu_len):
    np.random.seed(seed)
    N=len(ptr)-1
    insol=np.zeros(N,np.bool_)
    tight=np.zeros(N,np.int32)   # number of solution neighbours
    tabu=np.zeros(N,np.int64)
    size=0
    for v in init:
        if v>=0 and tight[v]==0 and not insol[v]:
            insol[v]=True; size+=1
            for e in range(ptr[v],ptr[v+1]): tight[adj[e]]+=1
    best=size
    bestsol=insol.copy()
    for it in range(1,iters+1):
        # try add free vertex (tight==0) : random start scan
        start=np.random.randint(N)
        added=False
        for t in range(N):
            v=(start+t)%N
            if (not insol[v]) and tight[v]==0 and tabu[v]<=it:
                insol[v]=True; size+=1
                for e in range(ptr[v],ptr[v+1]): tight[adj[e]]+=1
                added=True
                break
        if added:
            if size>best:
                best=size; bestsol=insol.copy()
            continue
        # swap: pick random vertex with tight==1 (non tabu), swap in
        # sample candidates
        cand=-1
        for tr in range(200):
            v=np.random.randint(N)
            if (not insol[v]) and tight[v]==1 and tabu[v]<=it:
                cand=v; break
        if cand<0:
            # perturb: add random vertex with tight 2
            for tr in range(200):
                v=np.random.randint(N)
                if (not insol[v]) and tight[v]==2 and tabu[v]<=it:
                    cand=v; break
        if cand<0: continue
        v=cand
        for e in range(ptr[v],ptr[v+1]):
            u=adj[e]
            if insol[u]:
                insol[u]=False; size-=1
                tabu[u]=it+tabu_len+np.random.randint(10)
                for f in range(ptr[u],ptr[u+1]): tight[adj[f]]-=1
        insol[v]=True; size+=1
        for e in range(ptr[v],ptr[v+1]): tight[adj[e]]+=1
        if size>best:
            best=size; bestsol=insol.copy()
    return best,bestsol

def run(n,w,d,iters,seed,tabu_len=20,init=None):
    X=words(n,w)
    ptr,adj=build_adj(X,d)
    if init is None: init=np.full(1,-1,np.int64)
    t=time.time()
    best,sol=search(ptr,adj,iters,seed,init,tabu_len)
    return best,X[sol],time.time()-t

if __name__=="__main__":
    n,w,d,iters,seed=map(int,sys.argv[1:6])
    b,C,t=run(n,w,d,iters,seed)
    print(n,w,d,b,round(t,1))
    np.save(f"best_{n}_{w}_{d}_s{seed}_{b}.npy",C)
