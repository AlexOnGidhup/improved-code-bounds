import sys, numpy as np, os
from cwlib import run
n,w,d,iters,seed=map(int,sys.argv[1:6])
b,C,t=run(n,w,d,iters,seed)
fn=f"res/cw_{n}_{w}_{d}_{b}_s{seed}.txt"
open(fn,'w').write("\n".join("".join(map(str,r)) for r in C)+"\n")
print(n,w,d,"seed",seed,"iters",iters,"->",b,f"{t:.0f}s",flush=True)
