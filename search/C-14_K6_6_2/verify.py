# Eigenstaendige Pruefung: liest Codewoerter (eine Zeile je Wort, Ziffern 0..q-1), prueft Laenge, Anzahl,
# Verschiedenheit und den Ueberdeckungsradius durch Nachrechnen ALLER q^n Woerter.
import sys, itertools, numpy as np
fn, q, R = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = [l.strip() for l in open(fn) if l.strip()]
n = len(W[0]); assert all(len(w) == n and all(c in "0123456789"[:q] for c in w) for w in W)
assert len(set(W)) == len(W), "Woerter nicht verschieden"
C = np.array([[int(c) for c in w] for w in W], dtype=np.int8)
worst = 0
for x in itertools.product(range(q), repeat=n):
    d = int((C != np.array(x, dtype=np.int8)).sum(axis=1).min())
    worst = max(worst, d)
    if d > R: print("NICHT ueberdeckt:", x, "Abstand", d); sys.exit(1)
print(f"q={q} n={n} Anzahl={len(W)} verschieden=ja Ueberdeckungsradius={worst} <= R={R}: OK")
