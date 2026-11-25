# Eigenstaendige Pruefung: Ueberdeckungsradius eines Codes ueber {0..q-1}. Aufruf: python verify.py datei q R
import sys, numpy as np
fn, q, R = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
words = [l.strip() for l in open(fn) if l.strip()]
n = len(words[0]); assert all(len(w) == n and all(ch in "0123456789"[:q] for ch in w) for w in words)
assert len(set(words)) == len(words), "doppelte Woerter"
C = np.array([[int(c) for c in w] for w in words], dtype=np.int8)
X = np.indices((q,)*n, dtype=np.int8).reshape(n, -1).T       # alle q^n Woerter
covered = np.zeros(len(X), dtype=bool)
for c in C:
    covered |= ((X != c).sum(axis=1) <= R)
print(f"n={n} q={q} Woerter={len(C)} R={R} ungedeckt={int((~covered).sum())} von {len(X)}")
print("OK" if covered.all() else "FEHLER")
