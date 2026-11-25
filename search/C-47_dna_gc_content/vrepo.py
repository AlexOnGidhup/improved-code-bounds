import sys,glob,re,numpy as np,json
cons=json.load(open('ghdata/codes.json'))
for f in sorted(glob.glob('ghdata/codes/GC_n*.txt'),key=lambda s:[int(x) for x in re.findall(r'\d+',s)]):
    n,d=map(int,re.findall(r'n(\d+)_d(\d+)',f)[0]); w=n//2
    ws=[l.strip() for l in open(f) if l.strip()]
    m={'A':0,'T':1,'G':2,'C':3}
    X=np.array([[m[c] for c in x] for x in ws],dtype=np.int8)
    ok=X.shape[1]==n and len(set(ws))==len(ws) and ((X>=2).sum(1)==w).all()
    N=len(X);md=99
    for i in range(0,N,500):
        D=(X[i:i+500,None,:]!=X[None,:,:]).sum(2)
        for k in range(D.shape[0]): D[k,i+k]=99
        md=min(md,D.min())
    key=f"GC_n{n}_d{d}"
    print(key,N,"gc ok" if ok else "FORMAT/GC FAIL","mind",md,"OK" if ok and md>=d else "FAIL",'|',cons[key]['construction'][:70])
