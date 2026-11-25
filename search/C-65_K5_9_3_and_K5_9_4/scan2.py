import sys, time, numpy as np
from gfmm import *
import colopt
p=5
for s in sys.argv[1:]:
    n,R,m,M,iters,copt,seed = map(int, s.split(','))
    N=p**m; TL,NL,TH,NH,Q1 = digits_add_tables(p,m)
    t=time.time()
    b,cols = colopt.opt(p,n,R,m,copt,seed)
    cols=[int(c) for c in cols]
    B = ball(p,m,cols,R)
    print(f"n={n} R={R} m={m} M={M} size={M*p**(n-m)} |B|={len(B)}/{N} need>={N/M:.0f}", flush=True)
    best,S = search(M,N,B,TL,NL,TH,NH,Q1,iters,seed,0.5,np.zeros(M,np.int32),False)
    print(f"SPEC n={n} R={R} m={m} M={M} size={M*p**(n-m)} unc={best} {time.time()-t:.0f}s", flush=True)
    if best==0: print("COLS",cols,"S",list(map(int,S)),flush=True)
