# Verifiziert: Datei = Ueberdeckungscode, q-aeres Alphabet, Laenge n, Radius R.
# Aufruf: python verify.py code_K5_7_3_85.txt 5 7 3
import sys, itertools
import numpy as np
fn,q,n,R=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
W=[l.strip() for l in open(fn) if l.strip()]
assert all(len(w)==n and all(ch in "0123456789"[:q] for ch in w) for w in W), "Format"
assert len(set(W))==len(W), "nicht verschieden"
C=np.array([[int(ch) for ch in w] for w in W],dtype=np.int8)
# alle q^n Woerter in Bloecken pruefen
idx=np.arange(q**n)
worst=0
for s in range(0,q**n,20000):
    ids=idx[s:s+20000]
    X=np.stack([(ids//q**i)%q for i in range(n)],axis=1).astype(np.int8)
    dmin=np.full(len(X),n+1)
    for c in C:
        dmin=np.minimum(dmin,(X!=c).sum(1))
    worst=max(worst,int(dmin.max()))
print("Woerter:",len(W),"q=",q,"n=",n,"Ueberdeckungsradius (max min-Abstand):",worst)
print("OK" if worst<=R else "FEHLER")
