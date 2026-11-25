# Focused local search for K_q(n,1): code = M words, minimize #uncovered
import numpy as np, numba as nb, sys, time
from numba import njit

def tables(q,n):
    N=q**n
    w=np.arange(N,dtype=np.int64)
    dig=np.zeros((N,n),dtype=np.int8)
    for i in range(n): dig[:,i]=(w//q**i)%q
    nbt=np.zeros((N,n*(q-1)),dtype=np.int32)
    k=0
    for i in range(n):
        for s in range(1,q):
            di=dig[:,i].astype(np.int64); nd=(di+s)%q
            nbt[:,k]=w+(nd-di)*q**i; k+=1
    return dig,nbt

@njit(cache=True)
def dec_ball(w,cnt,nbt,unc,pos,nu):
    # returns new nu
    for k in range(-1,nbt.shape[1]):
        x = w if k<0 else nbt[w,k]
        cnt[x]-=1
        if cnt[x]==0:
            pos[x]=nu; unc[nu]=x; nu+=1
    return nu
@njit(cache=True)
def inc_ball(w,cnt,nbt,unc,pos,nu):
    for k in range(-1,nbt.shape[1]):
        x = w if k<0 else nbt[w,k]
        if cnt[x]==0:
            nu-=1
            y=unc[nu]; p=pos[x]; unc[p]=y; pos[y]=p
        cnt[x]+=1
    return nu

@njit(cache=True)
def run(q,n,M,code,dig,nbt,iters,seed,tabulen,noise):
    np.random.seed(seed)
    N=q**n
    pw=np.ones(n,dtype=np.int64)
    for i in range(1,n): pw[i]=pw[i-1]*q
    cnt=np.zeros(N,dtype=np.int32)
    unc=np.zeros(N,dtype=np.int32); pos=np.zeros(N,dtype=np.int32)
    nu=0
    for x in range(N):
        unc[nu]=x; pos[x]=nu; nu+=1
    isc=np.zeros(N,dtype=np.int32)
    for j in range(M):
        nu=inc_ball(code[j],cnt,nbt,unc,pos,nu); isc[code[j]]+=1
    # index of codeword by position: find via isc and search; keep list
    where=-np.ones(N,dtype=np.int32)  # one codeword idx at word (multiset rare)
    for j in range(M): where[code[j]]=j
    tabu=np.zeros(N,dtype=np.int64)
    best=nu
    maxc=n*(n-1)//2*(q-1)*(q-1)
    cj=np.zeros(2*maxc,dtype=np.int32); cn=np.zeros(2*maxc,dtype=np.int32)
    for it in range(iters):
        if nu==0: return 0,code
        u=unc[np.random.randint(nu)]
        nc=0
        # codewords at distance 2 from u
        for i in range(n):
            for j2 in range(i+1,n):
                for a in range(1,q):
                    for b in range(1,q):
                        v=u+((dig[u,i]+a)%q-dig[u,i])*pw[i]+((dig[u,j2]+b)%q-dig[u,j2])*pw[j2]
                        if isc[v]>0:
                            jj=where[v]
                            # move coordinate i to u_i
                            cj[nc]=jj; cn[nc]=v+(dig[u,i]-dig[v,i])*pw[i]; nc+=1
                            cj[nc]=jj; cn[nc]=v+(dig[u,j2]-dig[v,j2])*pw[j2]; nc+=1
        bj=-1; bn=-1; bd=1<<30; ties=0
        if nc==0 or np.random.random()<noise:
            # relocate random codeword onto u (best of few)
            for t in range(8):
                jj=np.random.randint(M)
                cn_=u
                nu0=nu
                c0=code[jj]
                nu=dec_ball(c0,cnt,nbt,unc,pos,nu); isc[c0]-=1
                nu=inc_ball(cn_,cnt,nbt,unc,pos,nu)
                d=nu-nu0
                nu=dec_ball(cn_,cnt,nbt,unc,pos,nu)
                nu=inc_ball(c0,cnt,nbt,unc,pos,nu); isc[c0]+=1
                if d<bd or (d==bd and np.random.random()<0.5):
                    bd=d; bj=jj; bn=cn_
        else:
            for t in range(nc):
                jj=cj[t]; c0=code[jj]; c1=cn[t]
                if tabu[c1]>it or isc[c1]>0: continue
                nu0=nu
                nu=dec_ball(c0,cnt,nbt,unc,pos,nu); isc[c0]-=1
                nu=inc_ball(c1,cnt,nbt,unc,pos,nu)
                d=nu-nu0
                nu=dec_ball(c1,cnt,nbt,unc,pos,nu)
                nu=inc_ball(c0,cnt,nbt,unc,pos,nu); isc[c0]+=1
                if d<bd:
                    bd=d; bj=jj; bn=c1; ties=1
                elif d==bd:
                    ties+=1
                    if np.random.randint(ties)==0: bj=jj; bn=c1
            if bj<0:
                bj=np.random.randint(M); bn=u
        c0=code[bj]
        nu=dec_ball(c0,cnt,nbt,unc,pos,nu); isc[c0]-=1
        if where[c0]==bj: where[c0]=-1
        nu=inc_ball(bn,cnt,nbt,unc,pos,nu); isc[bn]+=1
        code[bj]=bn; where[bn]=bj
        tabu[c0]=it+tabulen
        if nu<best: best=nu
    return nu,code

def check(code,q,n,dig):
    N=q**n
    cov=np.zeros(N,bool)
    ds=dig.astype(np.int16)
    cd=ds[code]
    for x0 in range(0,N,2000):
        d=(ds[x0:x0+2000,None,:]!=cd[None,:,:]).sum(2).min(1)
        cov[x0:x0+2000]=d<=1
    return int((~cov).sum())

if __name__=="__main__":
    q=int(sys.argv[1]); n=int(sys.argv[2]); M=int(sys.argv[3]); secs=float(sys.argv[4]); seed=int(sys.argv[5])
    tabulen=int(sys.argv[6]) if len(sys.argv)>6 else 10
    noise=float(sys.argv[7]) if len(sys.argv)>7 else 0.02
    dig,nbt=tables(q,n); N=q**n
    rng=np.random.default_rng(seed)
    code=rng.choice(N,M,replace=False).astype(np.int32)
    if len(sys.argv)>8:
        W=[l.strip() for l in open(sys.argv[8]) if l.strip()]
        idx=np.array([sum(int(ch)*q**i for i,ch in enumerate(w)) for w in W],dtype=np.int32)
        idx=idx[:M] if len(idx)>=M else np.concatenate([idx,rng.choice(N,M-len(idx),replace=False).astype(np.int32)])
        code=np.unique(idx).astype(np.int32)
        while len(code)<M: code=np.unique(np.append(code,rng.integers(N)).astype(np.int32))
    t0=time.time(); k=0; bestM=None
    while time.time()-t0<secs:
        nu,code=run(q,n,M,code,dig,nbt,2_000_000,seed*1000+k,tabulen,noise); k+=1
        print(f"M={M} unc={nu} t={time.time()-t0:.0f}",flush=True)
        if nu==0:
            assert check(code,q,n,dig)==0
            np.savetxt(f"c_{q}_{n}_{M}_s{seed}.txt",dig[code],fmt="%d",delimiter="")
            print("FOUND",M,flush=True); bestM=M
            # remove codeword covering fewest uniquely: just drop random
            M-=1; code=np.delete(code,rng.integers(M+1)).astype(np.int32)
