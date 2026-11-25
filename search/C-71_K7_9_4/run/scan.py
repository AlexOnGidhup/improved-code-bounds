import sys, subprocess, math, time, itertools
from concurrent.futures import ThreadPoolExecutor
best = {  # (q,n,R): best known upper bound (Keri 2011 / Marosi 2026)
 (7,7,4):49,(7,8,4):316,(7,8,5):49,(7,9,4):1475,(7,9,5):240,(7,10,4):6517,(7,10,5):980,(7,9,6):37,(7,10,6):175,
 (8,7,4):92,(8,8,4):505,(8,8,5):79,(8,9,4):2944,(8,9,5):384,(8,9,6):48,(8,10,6):324,
 (9,7,4):120,(9,8,4):729,(9,8,5):120,(9,9,4):5103,(9,9,5):684,(9,9,6):81,(9,10,6):477,(9,8,6):17,
 (10,7,4):168,(10,8,4):1156,(10,8,5):168,(10,9,4):8500,(10,9,5):1055,(10,9,6):114,(10,10,6):802,(10,8,6):22,
}
jobs=[]
for (q,n,R),b in best.items():
    K = math.comb(n-1,R)*(q-1)**R
    if K>400000: continue
    for r in range(R+1, n):
        N=q**r
        if N>1.2e6 or N<200: continue
        ker=q**(n-r); m=(b-1)//ker
        if m<1 or m>80: continue
        jobs.append((q,n,R,r,m,K))
jobs.sort(key=lambda j:(j[5]*j[4]))
print(len(jobs),"jobs",flush=True)
secs=int(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3])
def run(j):
    q,n,R,r,m,K=j; N=q**r
    T0=5e-4*N; T1=T0/4
    cmd=["python","mm_cover.py",str(q),str(n),str(R),str(r),str(m),str(secs),"1",f"{T0}:{T1}","-"]
    try:
        out=subprocess.run(cmd,capture_output=True,text=True,timeout=secs+400,cwd="out").stdout
    except Exception as e:
        return j,"ERR"+str(e)
    lines=out.strip().splitlines()
    return j,lines[-1] if lines else ""
import os
os.makedirs("out",exist_ok=True)
for f in ["mm_cover.py"]:
    if not os.path.exists("out/"+f): import shutil; shutil.copy(f,"out/"+f)
with ThreadPoolExecutor(4) as ex:
    for j,l in ex.map(run,jobs[lo:hi]):
        print(j,l,flush=True)
