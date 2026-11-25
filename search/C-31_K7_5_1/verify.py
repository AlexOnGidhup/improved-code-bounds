#!/usr/bin/env python3
"""Standalone check of a q-ary covering code (numpy only).

usage: python verify.py code_file q n R
Checks: every line has exactly n digits in 0..q-1, all words distinct,
and EVERY one of the q^n words has Hamming distance <= R to some codeword
(full recomputation, no shortcuts). Prints size and number of uncovered words.
"""
import sys
import numpy as np

f, q, n, R = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
lines = [l.strip() for l in open(f) if l.strip()]
assert all(len(w) == n and all(c in "0123456789"[:q] for c in w) for w in lines), "bad line"
assert len(set(lines)) == len(lines), "duplicate words"
C = np.array([[int(c) for c in w] for w in lines], dtype=np.int8)
N = q ** n
idx = np.arange(N)
X = np.stack([(idx // q ** i) % q for i in range(n)], axis=1).astype(np.int8)
unc = 0
for s in range(0, N, 1000):
    blk = X[s:s + 1000]
    d = (blk[:, None, :] != C[None, :, :]).sum(2).min(1)
    unc += int((d > R).sum())
print(f"size={len(lines)} q={q} n={n} R={R} uncovered={unc}")
sys.exit(0 if unc == 0 else 1)
