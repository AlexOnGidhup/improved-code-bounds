#!/usr/bin/env python3
"""Independent verifier for every code in this repository.

    python verify.py            # check everything (about one minute, needs numpy)
    python verify.py K6_6_2     # check only files whose name contains the given text

The checks are exhaustive and do not use any code from the searches:
  packing          every pair of codewords is compared
  covering         the ball around every codeword is marked; every word of the space must be hit
  constant weight  as packing, plus the number of nonzero coordinates of every word
  GC content       as packing, plus the number of coordinates in {2,3} (G, C) of every word

File format: one codeword per line, digits 0..q-1, nothing else.
"Previous" is the best published bound we are aware of (see README and documents/LITERATURE.md);
the script only checks that the code is valid and has the stated size.
"""
import itertools
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))

# (file, kind, parameters, previous best published bound)
RESULTS = [
    # mixed binary/ternary packings N(m, n, d): m binary coordinates first, then n ternary
    ("codes/packing/N_2_12_7__171.txt", "packing", dict(alphabets=[2] * 2 + [3] * 12, d=7), 162),
    ("codes/packing/N_3_11_7__116.txt", "packing", dict(alphabets=[2] * 3 + [3] * 11, d=7), 108),
    # ternary packing A_3(n, d)
    ("codes/packing/A3_15_5__8748.txt", "packing", dict(alphabets=[3] * 15, d=5), 7929),
    # covering codes K_q(n, R)
    ("codes/covering/K5_7_3__85.txt", "covering", dict(q=5, n=7, R=3), 100),
    ("codes/covering/K5_9_3__1250.txt", "covering", dict(q=5, n=9, R=3), 1275),
    ("codes/covering/K5_9_4__250.txt", "covering", dict(q=5, n=9, R=4), 255),
    ("codes/covering/K5_9_5__50.txt", "covering", dict(q=5, n=9, R=5), 55),
    ("codes/covering/K6_6_2__216.txt", "covering", dict(q=6, n=6, R=2), 274),
    ("codes/covering/K6_7_3__216.txt", "covering", dict(q=6, n=7, R=3), 227),
    ("codes/covering/K6_9_3__3888.txt", "covering", dict(q=6, n=9, R=3), 4752),
    ("codes/covering/K6_10_3__15552.txt", "covering", dict(q=6, n=10, R=3), 19347),
    ("codes/covering/K7_5_1__766.txt", "covering", dict(q=7, n=5, R=1), 769),
    ("codes/covering/K7_9_4__1372.txt", "covering", dict(q=7, n=9, R=4), 1475),
    # ternary constant-weight codes A_3(n, d, w); compared with a table from 2002 only
    ("codes/unconfirmed/ternary-constant-weight/A3cw_7_3_4__62.txt", "weight", dict(n=7, d=3, w=4), 60),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_7_3_5__82.txt", "weight", dict(n=7, d=3, w=5), 72),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_8_3_5__173.txt", "weight", dict(n=8, d=3, w=5), 161),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_8_3_6__184.txt", "weight", dict(n=8, d=3, w=6), 168),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_9_3_6__483.txt", "weight", dict(n=9, d=3, w=6), 411),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_9_3_7__426.txt", "weight", dict(n=9, d=3, w=7), 405),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_10_4_5__221.txt", "weight", dict(n=10, d=4, w=5), 204),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_10_3_6__878.txt", "weight", dict(n=10, d=3, w=6), 876),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_10_3_7__1194.txt", "weight", dict(n=10, d=3, w=7), 960),
    ("codes/unconfirmed/ternary-constant-weight/A3cw_10_3_9__326.txt", "weight", dict(n=10, d=3, w=9), 325),
    # DNA code with constant GC content A_4^GC(n, d, w); symbols 0=A, 1=T, 2=G, 3=C
    ("codes/unconfirmed/dna-gc-content/A4GC_12_7_6__236.txt", "gc", dict(n=12, d=7, w=6), 183),
]


def read_code(path, alphabets):
    with open(os.path.join(ROOT, path)) as fh:
        words = [line.strip() for line in fh if line.strip()]
    if len(set(words)) != len(words):
        raise ValueError("duplicate codewords")
    n = len(alphabets)
    for w in words:
        if len(w) != n or not w.isdigit():
            raise ValueError(f"bad line {w!r}")
    code = np.array([[int(c) for c in w] for w in words], dtype=np.int64)
    for i, q in enumerate(alphabets):
        if code[:, i].max() >= q:
            raise ValueError(f"coordinate {i} leaves the alphabet of size {q}")
    return code


def min_distance(code):
    return min(int((code[i + 1:] != code[i]).sum(axis=1).min()) for i in range(len(code) - 1))


def uncovered(code, q, n, R):
    """Number of words of {0..q-1}^n at distance > R from every codeword."""
    powers = q ** np.arange(n - 1, -1, -1, dtype=np.int64)
    base = code @ powers
    hit = np.zeros(q ** n, dtype=bool)
    hit[base] = True
    for r in range(1, R + 1):
        for positions in itertools.combinations(range(n), r):
            for shifts in itertools.product(range(1, q), repeat=r):
                index = base.copy()
                for p, s in zip(positions, shifts):
                    index += (((code[:, p] + s) % q) - code[:, p]) * powers[p]
                hit[index] = True
    return int((~hit).sum())


def check(path, kind, p, previous):
    size = int(path.rsplit("__", 1)[1].split(".")[0])
    if kind == "packing":
        code = read_code(path, p["alphabets"])
        d = min_distance(code)
        ok = len(code) == size and d >= p["d"] and size > previous
        detail = f"{len(code)} words, minimum distance {d} (need {p['d']}), previous lower bound {previous}"
    elif kind == "covering":
        code = read_code(path, [p["q"]] * p["n"])
        miss = uncovered(code, p["q"], p["n"], p["R"])
        ok = len(code) == size and miss == 0 and size < previous
        detail = f"{len(code)} words, {miss} of {p['q'] ** p['n']} words uncovered at radius {p['R']}, previous upper bound {previous}"
    elif kind == "weight":
        code = read_code(path, [3] * p["n"])
        d = min_distance(code)
        weights_ok = bool(((code != 0).sum(axis=1) == p["w"]).all())
        ok = len(code) == size and d >= p["d"] and weights_ok and size > previous
        detail = f"{len(code)} words, minimum distance {d} (need {p['d']}), all weights {p['w']}: {weights_ok}, 2002 table {previous}"
    elif kind == "gc":
        code = read_code(path, [4] * p["n"])
        d = min_distance(code)
        gc_ok = bool(((code >= 2).sum(axis=1) == p["w"]).all())
        ok = len(code) == size and d >= p["d"] and gc_ok and size > previous
        detail = f"{len(code)} words, minimum distance {d} (need {p['d']}), GC content {p['w']} everywhere: {gc_ok}, 2010 table {previous}"
    else:
        raise ValueError(kind)
    print(f"{'OK  ' if ok else 'FAIL'} {path}: {detail}", flush=True)
    return ok


def main():
    needle = sys.argv[1] if len(sys.argv) > 1 else ""
    selected = [r for r in RESULTS if needle in r[0]]
    if not selected:
        sys.exit(f"no file name contains {needle!r}")
    results = [check(*r) for r in selected]
    print(f"\n{sum(results)} of {len(results)} codes verified")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
