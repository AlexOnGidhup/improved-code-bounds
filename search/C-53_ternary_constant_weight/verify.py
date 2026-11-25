#!/usr/bin/env python3
"""Standalone check: ternary code file, one word per line (digits 0..2).
usage: python verify.py code_file n w d   (w=-1: do not check constant weight)"""
import sys, itertools
import numpy as np
f, n, w, d = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
lines = [l.strip() for l in open(f) if l.strip()]
assert all(len(l) == n and set(l) <= set("012") for l in lines), "bad line"
assert len(set(lines)) == len(lines), "duplicates"
X = np.array([[int(c) for c in l] for l in lines], dtype=np.int8)
if w >= 0:
    assert all(int((r != 0).sum()) == w for r in X), "weight"
md = n + 1
for i in range(len(X)):
    dist = (X[i + 1:] != X[i]).sum(axis=1)
    if len(dist): md = min(md, int(dist.min()))
print(f"file={f} n={n} w={w} words={len(lines)} distinct=True min_distance={md}")
assert md >= d, "min distance too small"
print("OK")
