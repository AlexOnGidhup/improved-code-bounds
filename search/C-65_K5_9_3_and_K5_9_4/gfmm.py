# Matrixmethode ueber GF(p): Code = {x in GF(p)^n : H x in S}, H m x n, S Menge von Syndromen.
# Ueberdeckung Radius R  <=>  S + B = GF(p)^m, B = {sum_{i in T} c_i h_i : |T|<=R}
import numpy as np, numba as nb, sys, time

def digits_add_tables(p, m):
    a = m//2; b = m-a
    Q1 = p**a; Q2 = p**b   # lo has a digits, hi has b digits
    def tab(Q, d):
        D = np.zeros((Q, d), dtype=np.int64)
        for x in range(Q):
            y = x
            for j in range(d):
                D[x, j] = y % p; y //= p
        T = np.zeros((Q, Q), dtype=np.int32); N = np.zeros(Q, dtype=np.int32)
        pw = p**np.arange(d)
        for x in range(Q):
            for y in range(Q):
                T[x, y] = int(((D[x]+D[y]) % p) @ pw)
            N[x] = int(((-D[x]) % p) @ pw)
        return T, N
    TL, NL = tab(Q1, a) if a>0 else (np.zeros((1,1),np.int32), np.zeros(1,np.int32))
    TH, NH = tab(Q2, b)
    return TL, NL, TH, NH, Q1

@nb.njit(cache=True)
def addf(x, y, TL, TH, Q1):
    return TH[x//Q1, y//Q1]*Q1 + TL[x % Q1, y % Q1]

def ball(p, m, H, R):
    # H: n columns as ints (base p digits). returns sorted unique array of ball syndromes
    n = len(H)
    TL, NL, TH, NH, Q1 = digits_add_tables(p, m)
    cur = {0}
    layer = [(0, -1)]
    allset = {0}
    def mul(c, h):
        d = []; y = h
        for j in range(m):
            d.append((y % p)*c % p); y //= p
        return sum(v*p**j for j, v in enumerate(d))
    # BFS by number of columns used (indices increasing)
    frontier = [(0, -1)]
    for _ in range(R):
        nf = []
        for (s, last) in frontier:
            for i in range(last+1, n):
                for c in range(1, p):
                    t = int(addf(s, mul(c, H[i]), TL, TH, Q1))
                    nf.append((t, i)); allset.add(t)
        frontier = list(set(nf))
    return np.array(sorted(allset), dtype=np.int32)

@nb.njit(cache=True)
def search(M, N, B, TL, NL, TH, NH, Q1, iters, seed, T0, S0, hasS0):
    np.random.seed(seed)
    nb_ = len(B)
    negB = np.empty(nb_, np.int32)
    S = np.empty(M, np.int32)
    cnt = np.zeros(N, np.int32)
    if hasS0:
        for i in range(M): S[i] = S0[i]
    else:
        for i in range(M): S[i] = np.random.randint(N)
    for i in range(M):
        for j in range(nb_):
            cnt[addf(S[i], B[j], TL, TH, Q1)] += 1
    unc = 0
    for x in range(N):
        if cnt[x] == 0: unc += 1
    best = unc; bestS = S.copy()
    # uncovered list maintained lazily by scanning random start
    for it in range(iters):
        if unc == 0: break
        # pick random uncovered
        x = np.random.randint(N)
        k = 0
        while cnt[x] != 0 and k < N:
            x += 1
            if x == N: x = 0
            k += 1
        # new center covering x : s' = x - b  (b random in B); -b computed via NL/NH
        b = B[np.random.randint(nb_)]
        nbv = NH[b//Q1]*Q1 + NL[b % Q1]
        snew = addf(x, nbv, TL, TH, Q1)
        i = np.random.randint(M)
        sold = S[i]
        # remove old
        d = 0
        for j in range(nb_):
            y = addf(sold, B[j], TL, TH, Q1)
            cnt[y] -= 1
            if cnt[y] == 0: d += 1
        for j in range(nb_):
            y = addf(snew, B[j], TL, TH, Q1)
            if cnt[y] == 0: d -= 1
            cnt[y] += 1
        # d = change in unc
        if d <= 0 or np.random.random() < np.exp(-d/T0):
            S[i] = snew; unc += d
            if unc < best:
                best = unc; bestS = S.copy()
        else:
            for j in range(nb_):
                cnt[addf(snew, B[j], TL, TH, Q1)] -= 1
            for j in range(nb_):
                cnt[addf(sold, B[j], TL, TH, Q1)] += 1
    return best, bestS

def run(p, n, R, m, M, iters, seed, T0=0.5, tries=1):
    rng = np.random.default_rng(seed)
    N = p**m
    TL, NL, TH, NH, Q1 = digits_add_tables(p, m)
    res = []
    for t in range(tries):
        # random columns, first m = identity (wlog), rest random nonzero
        cols = [p**j for j in range(m)] + [int(rng.integers(1, N)) for _ in range(n-m)] if n >= m else None
        B = ball(p, m, cols, R)
        best, S = search(M, N, B, TL, NL, TH, NH, Q1, iters, int(rng.integers(1<<30)), T0, np.zeros(M, np.int32), False)
        res.append((best, len(B)))
        print(f"p={p} n={n} R={R} m={m} M={M} |B|={len(B)}/{N} try {t}: unc={best}", flush=True)
        if best == 0: return cols, S
    return None
if __name__ == "__main__":
    p, n, R, m, M, iters, seed = map(int, sys.argv[1:8])
    t = time.time()
    r = run(p, n, R, m, M, iters, seed, tries=int(sys.argv[8]) if len(sys.argv)>8 else 3)
    print("time", time.time()-t, "FOUND" if r else "no")
