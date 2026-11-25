import numpy as np, sys, time, itertools
from numba import njit

def make_tables(q,n,R):
    V=q**n
    pw=np.array([q**i for i in range(n)],dtype=np.int64)
    idx=np.arange(V)
    D=np.zeros((V,n),dtype=np.uint8)
    for i in range(n): D[:,i]=(idx//pw[i])%q
    # error vectors weight<=R
    E=[]
    for w in range(R+1):
        for sup in itertools.combinations(range(n),w):
            for vals in itertools.product(range(1,q),repeat=w):
                e=[0]*n
                for s,v in zip(sup,vals): e[s]=v
                E.append(e)
    E=np.array(E,dtype=np.uint8)
    return D,E,pw

@njit(cache=True)
def ball_idx(c,D,E,pw,q,out):
    n=D.shape[1]
    for k in range(E.shape[0]):
        s=0
        for i in range(n):
            a=D[c,i]+E[k,i]
            if a>=q: a-=q
            s+=a*pw[i]
        out[k]=s
    return E.shape[0]

@njit(cache=True)
def dist(a,b,D):
    d=0
    for i in range(D.shape[1]):
        if D[a,i]!=D[b,i]: d+=1
    return d

@njit(cache=True)
def run(code,D,E,pw,q,R,iters,seed,tenure,tl):
    np.random.seed(seed)
    n=D.shape[1]; V=D.shape[0]; M=code.shape[0]
    cnt=np.zeros(V,dtype=np.int32)
    buf=np.zeros(E.shape[0],dtype=np.int64)
    buf2=np.zeros(E.shape[0],dtype=np.int64)
    for m in range(M):
        ball_idx(code[m],D,E,pw,q,buf)
        for k in range(E.shape[0]): cnt[buf[k]]+=1
    unc=0
    for v in range(V):
        if cnt[v]==0: unc+=1
    best=unc; bestcode=code.copy()
    tabu=np.zeros((M,n),dtype=np.int64)
    uncl=np.zeros(V,dtype=np.int64)
    t0=time.time() if False else 0
    for it in range(iters):
        if unc==0: break
        # collect uncovered list occasionally: pick random uncovered by sampling
        # sample random points until uncovered (fast when unc not tiny), else scan
        x=-1
        if unc*20>V:
            for _ in range(200):
                v=np.random.randint(V)
                if cnt[v]==0:
                    x=v;break
        if x<0:
            r=np.random.randint(unc); 
            for v in range(V):
                if cnt[v]==0:
                    if r==0:
                        x=v;break
                    r-=1
        # candidate moves
        bc=-1;bj=-1;bd=1<<30;nb=0
        for m in range(M):
            d=dist(code[m],x,D)
            if d==R+1:
                for j in range(n):
                    if D[code[m],j]!=D[x,j]:
                        # new word
                        cn=code[m]+(D[x,j]-D[code[m],j])*pw[j]
                        # delta
                        ball_idx(code[m],D,E,pw,q,buf)
                        loss=0
                        for k in range(E.shape[0]):
                            p=buf[k]
                            if cnt[p]==1 and dist(p,cn,D)>R: loss+=1
                        ball_idx(cn,D,E,pw,q,buf2)
                        gain=0
                        for k in range(E.shape[0]):
                            if cnt[buf2[k]]==0: gain+=1
                        delta=loss-gain
                        istabu = tabu[m,j]>it
                        if istabu and not (unc+delta<best): continue
                        if delta<bd or (delta==bd and np.random.randint(nb+1)==0):
                            if delta<bd: nb=0
                            bd=delta;bc=m;bj=j
                        nb+=1
        if bc<0:
            # random move: random codeword, random coordinate
            bc=np.random.randint(M); bj=np.random.randint(n)
            nv=np.random.randint(q)
            cn=code[bc]+(nv-D[code[bc],bj])*pw[bj]
        else:
            cn=code[bc]+(D[x,bj]-D[code[bc],bj])*pw[bj]
        # apply
        ball_idx(code[bc],D,E,pw,q,buf)
        for k in range(E.shape[0]):
            p=buf[k]; cnt[p]-=1
            if cnt[p]==0: unc+=1
        ball_idx(cn,D,E,pw,q,buf)
        for k in range(E.shape[0]):
            p=buf[k]
            if cnt[p]==0: unc-=1
            cnt[p]+=1
        code[bc]=cn
        tabu[bc,bj]=it+tenure+np.random.randint(tl)
        if unc<best:
            best=unc; bestcode=code.copy()
    return best,bestcode

def search(q,n,R,M,iters,seed,tenure=10,tl=10,start=None,D=None,E=None,pw=None):
    if D is None: D,E,pw=make_tables(q,n,R)
    V=q**n
    rng=np.random.default_rng(seed)
    code=rng.integers(0,V,size=M).astype(np.int64) if start is None else start.copy()
    return run(code,D,E,pw,q,R,iters,seed,tenure,tl)

if __name__=="__main__":
    q,n,R,M,iters,seed=map(int,sys.argv[1:7])
    t=time.time()
    D,E,pw=make_tables(q,n,R)
    print("tables",time.time()-t, "ball",len(E),flush=True)
    t=time.time()
    b,c=search(q,n,R,M,iters,seed,D=D,E=E,pw=pw)
    print("M",M,"best unc",b,"time",time.time()-t)
