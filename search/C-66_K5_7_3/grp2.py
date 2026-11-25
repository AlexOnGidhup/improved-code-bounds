import numpy as np, sys, time
from scipy.sparse import csr_matrix
from tabu import make_tables, ball_idx
from grp import *
from sa import sa_cover

def matrix(q,n,R,inv,sz,reps,D,E,pw):
    K=len(sz); rows=[];cols=[]
    buf=np.zeros(E.shape[0],dtype=np.int64)
    for t in range(K):
        ball_idx(reps[t],D,E,pw,q,buf)
        o=np.unique(inv[buf]); rows+=[t]*len(o); cols+=list(o)
    return csr_matrix((np.ones(len(rows),dtype=np.int8),(rows,cols)),shape=(K,K))

if __name__=="__main__":
    q,n,R,target,tmax,seed=map(int,sys.argv[1:7])
    lo=int(sys.argv[7]); hi=int(sys.argv[8]); iters=int(float(sys.argv[9]))
    D,E,pw=make_tables(q,n,R)
    add,mul,frob=gf_tables(q)
    rng=np.random.default_rng(seed)
    t0=time.time(); best=10**9; tries=0
    while time.time()-t0<tmax:
        gens=randgroup(q,n,rng,add,mul,frob,0)
        inv,sz,reps=build(q,n,R,gens,D,E,pw)
        K=len(sz)
        if K>hi or K<lo: continue
        A=matrix(q,n,R,inv,sz,reps,D,E,pw)
        # column j covers row t iff A[t,j]; CSC
        C=A.tocsc()
        tries+=1
        x0=np.ones(K,dtype=np.int8)
        bs=10**9
        for s in range(3):
            b,bx=sa_cover(C.indptr.astype(np.int64),C.indices.astype(np.int64),sz.astype(np.int64),sz.astype(np.int64),iters,3.0,0.15,1.5,seed*100+tries*3+s,x0)
            if b<bs: bs=b;bxs=bx
        print(f"try{tries} K={K} val={bs} t={time.time()-t0:.0f}",flush=True)
        if bs<best:
            best=bs
            sel=np.where(bxs>0)[0]
            code=np.concatenate([np.where(inv==j)[0] for j in sel])
            np.save(f"g2_q{q}n{n}R{R}_{bs}.npy",code)
            print("NEW BEST",bs,"target",target,flush=True)
