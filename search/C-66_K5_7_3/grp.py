import numpy as np, sys, time, itertools, random
from numba import njit
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix
from tabu import make_tables, ball_idx

def gf_tables(q):
    if q==5:
        add=np.array([[(a+b)%5 for b in range(5)] for a in range(5)])
        mul=np.array([[(a*b)%5 for b in range(5)] for a in range(5)])
        frob=[list(range(5))]
    elif q==4:
        add=np.array([[a^b for b in range(4)] for a in range(4)])
        # GF(4)={0,1,w,w+1}=0,1,2,3; w^2=w+1
        def m(a,b):
            r=0
            for i in range(2):
                if (b>>i)&1: r^=a<<i
            if r&4: r^=0b111
            return r
        mul=np.array([[m(a,b) for b in range(4)] for a in range(4)])
        frob=[list(range(4)),[0,1,3,2]]
    elif q in (2,3,7):
        add=np.array([[(a+b)%q for b in range(q)] for a in range(q)])
        mul=np.array([[(a*b)%q for b in range(q)] for a in range(q)])
        frob=[list(range(q))]
    return add,mul,frob

def rand_symbol_perm(q,rng,add,mul,frob,kind):
    # returns a permutation of symbols
    a=int(rng.integers(1,q)) if kind in('aff','mul') else 1
    b=int(rng.integers(0,q)) if kind in('aff','tr') else 0
    f=frob[int(rng.integers(len(frob)))] if kind=='aff' else list(range(q))
    return np.array([add[mul[a][f[x]]][b] for x in range(q)])

@njit(cache=True)
def apply_gen(D,pw,perm,smaps,out):
    V=D.shape[0]; n=D.shape[1]
    for v in range(V):
        s=0
        for i in range(n):
            s+=smaps[i,D[v,perm[i]]]*pw[i]
        out[v]=s

@njit(cache=True)
def find(p,x):
    while p[x]!=x:
        p[x]=p[p[x]]; x=p[x]
    return x

@njit(cache=True)
def orbits(img,V):
    p=np.arange(V)
    for g in range(img.shape[0]):
        for v in range(V):
            a=find(p,v); b=find(p,img[g,v])
            if a!=b: p[a]=b
    lab=np.zeros(V,dtype=np.int64)
    for v in range(V): lab[v]=find(p,v)
    return lab

def build(q,n,R,gens,D,E,pw):
    V=q**n
    img=np.zeros((len(gens),V),dtype=np.int64)
    for k,(perm,smaps) in enumerate(gens):
        apply_gen(D,pw,perm,smaps,img[k])
    lab=orbits(img,V)
    u,inv,sz=np.unique(lab,return_inverse=True,return_counts=True)
    reps=np.zeros(len(u),dtype=np.int64)
    reps[inv[::-1]]=np.arange(V)[::-1]
    return inv,sz,reps

def solve(q,n,R,inv,sz,reps,D,E,pw,tl=30,ub=None):
    K=len(sz)
    rows=[];cols=[]
    buf=np.zeros(E.shape[0],dtype=np.int64)
    for t in range(K):
        ball_idx(reps[t],D,E,pw,q,buf)
        o=np.unique(inv[buf])
        rows+= [t]*len(o); cols+=list(o)
    A=csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(K,K))
    cons=[LinearConstraint(A,lb=1,ub=np.inf)]
    if ub is not None: cons.append(LinearConstraint(sz.reshape(1,-1).astype(float),lb=0,ub=ub))
    res=milp(sz.astype(float),constraints=cons,integrality=np.ones(K),bounds=Bounds(0,1),options={'time_limit':tl,'disp':False})
    return res

def randgroup(q,n,rng,add,mul,frob,order_hint):
    gens=[]
    ng=int(rng.integers(1,3))
    for _ in range(ng):
        # coordinate permutation: random with cycle structure
        kind=rng.choice(['cyc','rand','id','blocks'])
        if kind=='cyc': perm=np.roll(np.arange(n),1)
        elif kind=='id': perm=np.arange(n)
        elif kind=='rand': perm=rng.permutation(n)
        else:
            k=int(rng.integers(2,n)); p=list(range(n))
            perm=np.array(list(range(1,k))+[0]+list(range(k,n))) if rng.random()<.5 else np.array(list(range(k,n))+list(range(0,k)))
            perm=np.arange(n); perm[:k]=np.roll(np.arange(k),1); perm[k:]=np.roll(np.arange(k,n),1)
        sk=rng.choice(['tr','mul','aff'])
        samecol=rng.random()<.6
        if samecol:
            m=rand_symbol_perm(q,rng,add,mul,frob,sk); smaps=np.tile(m,(n,1))
        else:
            smaps=np.array([rand_symbol_perm(q,rng,add,mul,frob,sk) for _ in range(n)])
        gens.append((perm,smaps))
    return gens

if __name__=="__main__":
    q,n,R,target,tmax,seed=map(int,sys.argv[1:7])
    maxorb=int(sys.argv[7]) if len(sys.argv)>7 else 2500
    D,E,pw=make_tables(q,n,R)
    add,mul,frob=gf_tables(q)
    rng=np.random.default_rng(seed)
    t0=time.time(); best=10**9; tries=0
    while time.time()-t0<tmax:
        gens=randgroup(q,n,rng,add,mul,frob,0)
        inv,sz,reps=build(q,n,R,gens,D,E,pw)
        K=len(sz)
        if K>maxorb or K<20: continue
        tries+=1
        res=solve(q,n,R,inv,sz,reps,D,E,pw,tl=20,ub=min(best-1,target+0.5*0) if best<10**9 else None)
        if res.x is None: 
            continue
        val=int(round(res.fun))
        print(f"try{tries} K={K} val={val} status={res.status} t={time.time()-t0:.0f}",flush=True)
        if val<best:
            best=val
            sel=np.where(res.x>0.5)[0]
            code=np.concatenate([np.where(inv==j)[0] for j in sel])
            np.save(f"grp_q{q}n{n}R{R}_{val}.npy",code)
            print("NEW BEST",val,"target",target,flush=True)
