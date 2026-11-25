import sys, time, numpy as np
from tabu import make_tables, search
q,n,R,M0,iters,tmax,seed=map(int,sys.argv[1:8])
D,E,pw=make_tables(q,n,R)
t0=time.time(); M=M0; start=None
rng=np.random.default_rng(seed)
while time.time()-t0<tmax:
    ok=False
    for rep in range(3):
        b,c=search(q,n,R,M,iters,seed+rep+M*7,start=start,D=D,E=E,pw=pw)
        print(f"q{q} n{n} R{R} M={M} rep{rep} unc={b} t={time.time()-t0:.0f}",flush=True)
        if b==0: ok=True;break
        start=None
    if not ok: break
    np.save(f"best_q{q}n{n}R{R}_M{M}.npy",c)
    start=np.delete(c,rng.integers(M))
    M-=1
