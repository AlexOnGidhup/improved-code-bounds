# Matrix method over Z_q: C = {x in Z_q^n : [I_r|D] x in S}, |C| = |S| q^(n-r).
# Exact best-response coordinate descent for S via FFT group correlation on Z_q^r, plus moves on D.
# usage: python fftmm.py q n R r m seconds seed [out_prefix]
import sys, time, numpy as np
q,n,R,r,m=map(int,sys.argv[1:6]); secs=float(sys.argv[6]); seed=int(sys.argv[7])
pref=sys.argv[8] if len(sys.argv)>8 else f"fm_q{q}n{n}R{R}r{r}"
rng=np.random.default_rng(seed)
shape=(q,)*r; N=q**r
def cols(D):
    A=np.concatenate([np.eye(r,dtype=np.int64),D],axis=1); return A
def ball(A):
    # indicator of {sum of <=R multiples of distinct columns} in Z_q^r
    B=np.zeros(shape,dtype=np.float64); B[(0,)*r]=1
    vecs=[(A[:,i]*lam)%q for i in range(n) for lam in range(1,q)]
    cur=B
    for w in range(R):
        nxt=cur.copy()
        for v in vecs:
            sh=cur
            for ax in range(r):
                if v[ax]: sh=np.roll(sh,int(v[ax]),axis=ax)
            nxt=np.maximum(nxt,sh)
        if (nxt==cur).all(): break
        cur=nxt
    return cur
def cover(B,S):
    c=np.zeros(shape,dtype=np.int32)
    ib=np.argwhere(B>0.5)
    for s in S:
        c[tuple(((ib+np.array(s))%q).T)]+=1
    return c
def descent(B,S,sweeps,tlimit):
    FB=np.conj(np.fft.fftn(B))
    cnt=cover(B,S); cost=int((cnt==0).sum())
    ib=np.argwhere(B>0.5)
    for sw in range(sweeps):
        improved=False
        for j in rng.permutation(len(S)):
            if time.time()>tlimit: return S,cost
            s=S[j]
            idx=tuple(((ib+np.array(s))%q).T); cnt[idx]-=1
            U=(cnt==0).astype(np.float64)
            g=np.fft.ifftn(np.fft.fftn(U)*FB).real
            gm=g.max(); cand=np.argwhere(g>gm-0.5)
            new=tuple(cand[rng.integers(len(cand))])
            S[j]=new
            idx=tuple(((ib+np.array(new))%q).T); cnt[idx]+=1
            nc=int((cnt==0).sum())
            if nc<cost: improved=True
            cost=nc
            if cost==0: return S,0
        if not improved and sw>3: break
    return S,cost
def main():
    t0=time.time(); tl=t0+secs
    D=rng.integers(1,q,size=(r,n-r)); A=cols(D); B=ball(A)
    S=[tuple(rng.integers(0,q,size=r)) for _ in range(m)]
    S,cost=descent(B,S,30,tl)
    best=cost; print("init",cost,flush=True); it=0
    while time.time()<tl and cost>0:
        it+=1
        D2=D.copy()
        for _ in range(1 if rng.random()<0.7 else 2):
            D2[rng.integers(r),rng.integers(n-r)]=rng.integers(0,q)
        A2=cols(D2); B2=ball(A2)
        S2=[tuple(s) for s in S]
        # kick: re-randomize one syndrome sometimes
        if rng.random()<0.5: S2[rng.integers(m)]=tuple(rng.integers(0,q,size=r))
        S2,c2=descent(B2,S2,6,tl)
        if c2<=cost:
            D,B,S,cost=D2,B2,S2,c2
            if cost<best: best=cost; print(f"[{time.time()-t0:6.1f}] it{it} cost {cost}",flush=True)
    print("final",cost,"best",best,"it",it)
    if cost==0:
        np.savetxt(pref+"_D.txt",D,fmt="%d"); np.savetxt(pref+"_S.txt",np.array(S),fmt="%d")
        print("COVER saved",pref,"size",m*q**(n-r))
main()
