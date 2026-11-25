import sys, time, numpy as np
from gfmm import *
p=5
specs = [tuple(map(int,s.split(','))) for s in sys.argv[1:]]   # n,R,m,M,iters,tries
for (n,R,m,M,iters,tries) in specs:
    t=time.time()
    r = run(p,n,R,m,M,iters,seed=n*100+R*10+m,tries=tries)
    print(f"SPEC n={n} R={R} m={m} M={M} size={M*p**(n-m)} {'FOUND' if r else 'no'} {time.time()-t:.0f}s", flush=True)
    if r:
        cols,S=r; print("COLS",cols,"S",list(map(int,S)),flush=True)
