# Independent, exhaustive verification of a q-ary covering code (standard library + numpy only).
# usage: python verify.py code_file q n R
# The file has one codeword per line, digits 0..q-1.  Checks: word length, alphabet, distinctness,
# and that EVERY one of the q^n words lies within Hamming distance R of some codeword.
# Check 1 (always): mark the radius-R ball of every codeword in a table of all q^n words and
#                   test that no word is left unmarked.
# Check 2 (if q^n * M * n <= 6e9): direct distance of every word to every codeword (second method).
# This script shares no code with the search programs.
import sys, itertools
import numpy as np

def main():
    fn = sys.argv[1]; q, n, R = map(int, sys.argv[2:5])
    lines = [l.strip() for l in open(fn) if l.strip()]
    assert all(len(l) == n for l in lines), "wrong word length"
    assert all(ch.isdigit() and int(ch) < q for l in lines for ch in l), "symbol outside alphabet"
    assert len(set(lines)) == len(lines), "repeated codeword"
    C = np.array([[int(ch) for ch in l] for l in lines], dtype=np.int64)
    M = len(C); N = q ** n
    pw = np.array([q ** (n - 1 - j) for j in range(n)], dtype=np.int64)
    # all error vectors of weight <= R
    errs = []
    for w in range(R + 1):
        for pos in itertools.combinations(range(n), w):
            for vals in itertools.product(range(1, q), repeat=w):
                v = [0] * n
                for p, x in zip(pos, vals):
                    v[p] = x
                errs.append(v)
    E = np.array(errs, dtype=np.int64)
    covered = np.zeros(N, dtype=bool)
    for c in C:
        covered[((E + c) % q) @ pw] = True
    unc = int(N - covered.sum())
    print(f"file={fn} q={q} n={n} R={R} codewords={M} q^n={N} ball={len(E)}")
    print(f"check 1 (ball marking): uncovered words = {unc}")
    ok = unc == 0
    if N * M * n <= 6_000_000_000:
        chunk = max(1, min(N, 30_000_000 // (M * n)))
        C8 = C.astype(np.int8); hist = np.zeros(n + 1, dtype=np.int64)
        for a in range(0, N, chunk):
            t = np.arange(a, min(N, a + chunk), dtype=np.int64)
            X = np.empty((len(t), n), dtype=np.int8)
            for j in range(n - 1, -1, -1):
                X[:, j] = t % q
                t = t // q
            dmin = np.full(len(X), n + 1, dtype=np.int64)
            for c in C8:
                np.minimum(dmin, (X != c).sum(axis=1), out=dmin)
            hist += np.bincount(dmin, minlength=n + 1)[: n + 1]
        rad = int(np.nonzero(hist)[0].max())
        print("check 2 (all distances): histogram of distance to code =", hist.tolist(), "covering radius =", rad)
        ok = ok and rad <= R and int(hist.sum()) == N
    if ok:
        print(f"OK: K_{q}({n},{R}) <= {M}")
    else:
        print("FAIL"); sys.exit(1)

main()
