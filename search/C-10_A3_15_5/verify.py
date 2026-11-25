import sys, numpy as np
fn=sys.argv[1]; q=int(sys.argv[2]); dmin=int(sys.argv[3])
rows=[l.strip() for l in open(fn) if l.strip()]
n=len(rows[0]); assert all(len(r)==n and set(r)<=set('0123456789'[:q]) for r in rows)
W=np.array([[int(c) for c in r] for r in rows],dtype=np.int8)
M=len(W); assert len(set(rows))==M, 'duplicates'
best=n
for i in range(0,M,500):
    B=W[i:i+500]
    D=(B[:,None,:]!=W[None,:,:]).sum(axis=2)
    for t in range(len(B)): D[t,i+t]=99
    best=min(best,int(D.min()))
print(f'length={n} words={M} distinct=ok min_distance={best} (required >= {dmin})', 'PASS' if best>=dmin else 'FAIL')
