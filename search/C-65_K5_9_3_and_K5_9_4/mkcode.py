import numpy as np, sys, itertools
from gfmm import *
def build(p, n, R, m, M, iters, seed, out):
    rng = np.random.default_rng(seed)
    N = p**m
    TL, NL, TH, NH, Q1 = digits_add_tables(p, m)
    for t in range(200):
        cols = [p**j for j in range(m)] + [int(rng.integers(1, N)) for _ in range(n-m)]
        B = ball(p, m, cols, R)
        best, S = search(M, N, B, TL, NL, TH, NH, Q1, iters, int(rng.integers(1<<30)), 0.5, np.zeros(M, np.int32), False)
        print(t, best, len(B), flush=True)
        if best == 0: break
    else: return False
    # explicit code
    Hm = np.array([[(c//p**j) % p for c in cols] for j in range(m)], dtype=np.int64)  # m x n
    allx = np.indices((p,)*n).reshape(n, -1).T.astype(np.int64)   # p^n x n
    syn = (allx @ Hm.T) % p
    sidx = syn @ (p**np.arange(m))
    mask = np.isin(sidx, np.array(S))
    code = allx[mask]
    print("code size", len(code))
    np.savetxt(out, code, fmt="%d", delimiter="")
    # keep as plain digit strings
    with open(out, "w") as f:
        for w in code: f.write("".join(map(str, w))+"\n")
    return True
if __name__ == "__main__":
    p, n, R, m, M, iters, seed = map(int, sys.argv[1:8]); out = sys.argv[8]
    build(p, n, R, m, M, iters, seed, out)
