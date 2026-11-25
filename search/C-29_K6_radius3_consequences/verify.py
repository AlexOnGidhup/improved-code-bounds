# verify.py  <datei> <q> <R> : prueft Laenge, Anzahl, Verschiedenheit, Alphabet und Ueberdeckungsradius
# durch vollstaendiges Nachrechnen (R-fache Hamming-Dilatation der Indikatormenge auf Z_q^n, nur numpy).
import sys, numpy as np
f, q, R = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
words = [l.strip() for l in open(f) if l.strip()]
n = len(words[0])
assert all(len(w) == n and all(c.isdigit() and int(c) < q for c in w) for w in words), "Laenge/Alphabet"
distinct = len(set(words)) == len(words)
assert q ** n <= 2 * 10 ** 8, "zu gross"
A = np.zeros((q,) * n, np.uint8)
for w in words:
    A[tuple(int(c) for c in w)] = 1
for _ in range(R):
    B = A.copy()
    for ax in range(n):
        B |= A.max(axis=ax, keepdims=True)
    A = B
unc = int((A == 0).sum())
print(f"n={n} q={q} Anzahl={len(words)} verschieden={'ja' if distinct else 'NEIN'} unueberdeckt(R={R})={unc} -> {'OK' if distinct and unc == 0 else 'FEHLER'}")
