import sys, subprocess
from concurrent.futures import ThreadPoolExecutor
secs=sys.argv[1]; jobs=[tuple(map(int,l.split())) for l in sys.argv[2].split(";")]
def run(j):
    q,n,R,r,m=j
    p=f"fm_q{q}n{n}R{R}r{r}m{m}"
    out=subprocess.run(["python","fftmm.py",*map(str,j),secs,"1",p],capture_output=True,text=True).stdout.strip().splitlines()
    return j,(out[-2:] if out else "")
with ThreadPoolExecutor(int(sys.argv[3])) as ex:
    for j,l in ex.map(run,jobs): print(j,l,flush=True)
