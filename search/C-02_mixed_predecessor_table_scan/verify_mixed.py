# Unabhaengige Pruefung eines gemischten binaer/ternaeren Codes: python verify_mixed.py datei m n d
import sys
path,m,n,d=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
W=[l.strip() for l in open(path) if l.strip()]
assert all(len(w)==m+n for w in W), "Laenge falsch"
assert all(set(w[:m])<=set('01') and set(w[m:])<=set('012') for w in W), "Alphabet falsch"
assert len(set(W))==len(W), "Woerter nicht verschieden"
md=min((sum(a!=b for a,b in zip(W[i],W[j])) for i in range(len(W)) for j in range(i)),default=None)
print(f"m={m} n={n} Woerter={len(W)} Mindestabstand={md} (gefordert {d}) ->", "OK" if md is not None and md>=d else "FEHLER")
