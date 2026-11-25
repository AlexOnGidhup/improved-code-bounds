import numpy as np, sys, time, math, itertools
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
from fls import tables

def rand_elem(q,n,rng):
    perm=rng.permutation(n)
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    a=rng.choice(units,n); b=rng.integers(0,q,n)
    return perm,a,b

def apply(q,n,dig,perm,a,b):
    # new digit at position perm[i] = a_i*d_i+b_i
    N=dig.shape[0]; nd=np.zeros_like(dig,dtype=np.int64)
    for i in range(n): nd[:,perm[i]]=(a[i]*dig[:,i]+b[i])%q
    return (nd*(q**np.arange(n))).sum(1)

def orbits(perms,N):
    lab=-np.ones(N,dtype=np.int64); k=0
    # union-find style via BFS on permutations
    lab=np.arange(N)
    changed=True
    while changed:
        changed=False
        for p in perms:
            m=np.minimum(lab,lab[p])
            m2=np.minimum(m,m[np.argsort(p)]) if False else m
            # propagate both directions
            new=m.copy(); np.minimum.at(new,p,m)
            if (new!=lab).any(): changed=True; lab=new
    uniq,inv=np.unique(lab,return_inverse=True)
    return inv,len(uniq)

def solve(q,n,dig,nbt,perms,tl,rng_unused=None):
    N=dig.shape[0]
    orb,K=orbits(perms,N)
    size=np.bincount(orb,minlength=K)
    rep=np.zeros(K,dtype=np.int64); rep[orb[::-1]]=np.arange(N)[::-1]
    ball=np.concatenate([rep[:,None],nbt[rep]],1)  # K x (1+n(q-1))
    cols=orb[ball]  # orbit ids
    rows=np.repeat(np.arange(K),cols.shape[1])
    A=csr_matrix((np.ones(rows.size),(rows,cols.ravel())),shape=(K,K)); A.data[:]=1
    res=milp(size.astype(float),constraints=LinearConstraint(A,1,np.inf),integrality=np.ones(K),bounds=Bounds(0,1),options={"time_limit":tl,"disp":False})
    if res.x is None: return None,K,None
    x=np.round(res.x).astype(bool)
    return int(size[x].sum()),K,np.nonzero(x[orb])[0]

if __name__=="__main__":
    q=int(sys.argv[1]); n=int(sys.argv[2]); seed=int(sys.argv[3]); secs=float(sys.argv[4]); tl=float(sys.argv[5])
    omin=int(sys.argv[6]); omax=int(sys.argv[7])
    dig,nbt=tables(q,n); N=q**n
    rng=np.random.default_rng(seed); best=10**9; t0=time.time()
    while time.time()-t0<secs:
        perm,a,b=rand_elem(q,n,rng)
        p=apply(q,n,dig,perm,a,b)
        # order
        seen=np.zeros(N,bool); o=1
        for s in range(N):
            if not seen[s]:
                l=0;x=s
                while not seen[x]: seen[x]=True; x=p[x]; l+=1
                o=o*l//math.gcd(o,l)
        if o<omin or o>omax: continue
        val,K,code=solve(q,n,dig,nbt,[p],tl)
        print(f"ord={o} orbits={K} size={val} perm={perm.tolist()} a={a.tolist()} b={b.tolist()} t={time.time()-t0:.0f}",flush=True)
        if val is not None and val<best:
            best=val; np.savetxt(f"g_{q}_{n}_{val}_s{seed}.txt",dig[code],fmt="%d",delimiter="")
