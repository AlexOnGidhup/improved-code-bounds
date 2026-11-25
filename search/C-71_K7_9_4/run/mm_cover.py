# Matrix method (Blokhuis-Lam / Oestergard) + simulated annealing for q-ary covering codes.
# Code C = { x in Z_q^n : A x in S },  A = [I_r | D] (r x n over Z_q),  S subset Z_q^r, |C| = |S| q^(n-r).
# C has covering radius <= R  iff  every y in Z_q^r equals s + A e with s in S, wt(e) <= R.
# SA state: S (m syndromes); move: s -> s + lam * a_i (a_i column of A); cost = #uncovered y.
# usage: python mm_cover.py q n R r m seconds seed T [Dfile|-] [startS]
import sys, time, itertools
import numpy as np
from numba import njit

def shell_vectors(m, q, w):
    out = []
    for pos in itertools.combinations(range(m), w):
        for vals in itertools.product(range(1, q), repeat=w):
            v = [0] * m
            for p, x in zip(pos, vals):
                v[p] = x
            out.append(v)
    return np.array(out, dtype=np.int64).reshape(len(out), m)

@njit(cache=True)
def add_ball(cnt, shi, slo, Fhi, Flo, addH, addL, QL, sign):
    unc = 0
    for k in range(Fhi.shape[0]):
        idx = addH[shi, Fhi[k]] * QL + addL[slo, Flo[k]]
        if sign > 0:
            if cnt[idx] == 0:
                unc -= 1
            cnt[idx] += 1
        else:
            cnt[idx] -= 1
            if cnt[idx] == 0:
                unc += 1
    return unc

@njit(cache=True)
def anneal(Shi, Slo, cnt, cost, Yhi, Ylo, Chi, Clo, addH, addL, QL, q, T, iters, seed, buf):
    np.random.seed(seed)
    m = Shi.shape[0]
    n = Yhi.shape[0]
    K = Yhi.shape[1]
    for it in range(iters):
        j = np.random.randint(m)
        i = np.random.randint(n)
        lam = 1 + np.random.randint(q - 1)
        h0 = Shi[j]; l0 = Slo[j]
        h1 = addH[h0, Chi[i, lam]]; l1 = addL[l0, Clo[i, lam]]
        delta = 0
        for k in range(K):
            a = addH[h0, Yhi[i, k]] * QL + addL[l0, Ylo[i, k]]
            b = addH[h1, Yhi[i, k]] * QL + addL[l1, Ylo[i, k]]
            buf[k, 0] = a
            buf[k, 1] = b
            if cnt[a] == 1:
                delta += 1
            if cnt[b] == 0:
                delta -= 1
        # note: a multiset may hit the same index twice; exact delta is recomputed by apply
        if delta <= 0 or np.random.random() < np.exp(-delta / T):
            d2 = 0
            for k in range(K):
                a = buf[k, 0]
                cnt[a] -= 1
                if cnt[a] == 0:
                    d2 += 1
            for k in range(K):
                b = buf[k, 1]
                if cnt[b] == 0:
                    d2 -= 1
                cnt[b] += 1
            Shi[j] = h1; Slo[j] = l1
            cost += d2
            if cost == 0:
                return cost, it + 1
    return cost, iters

def digits(x, q, r):
    return [(x // q ** t) % q for t in range(r)]

def main():
    q, n, R, r, m = map(int, sys.argv[1:6])
    secs = float(sys.argv[6]); seed = int(sys.argv[7])
    Tp = [float(x) for x in sys.argv[8].split(":")]
    T0 = Tp[0]; T1 = Tp[1] if len(Tp) > 1 else Tp[0]; cyc = int(Tp[2]) if len(Tp) > 2 else 200
    Dfile = sys.argv[9] if len(sys.argv) > 9 and sys.argv[9] != "-" else None
    startS = sys.argv[10] if len(sys.argv) > 10 else None
    tag = f"q{q}n{n}R{R}r{r}"
    rng = np.random.default_rng(seed)
    if Dfile:
        D = np.loadtxt(Dfile, dtype=np.int64).reshape(r, n - r)
    else:
        D = rng.integers(1, q, size=(r, n - r)).astype(np.int64)
    A = np.concatenate([np.eye(r, dtype=np.int64), D], axis=1)
    rl = r // 2; rh = r - rl
    QL = q ** rl; QH = q ** rh
    pwl = np.array([q ** t for t in range(rl)], dtype=np.int64)
    pwh = np.array([q ** t for t in range(rh)], dtype=np.int64)
    def mk_add(k, Q):
        dg = np.array([digits(x, q, k) for x in range(Q)], dtype=np.int64)
        pw = np.array([q ** t for t in range(k)], dtype=np.int64)
        return (((dg[:, None, :] + dg[None, :, :]) % q) * pw).sum(axis=2).astype(np.int32)
    addL = mk_add(rl, QL); addH = mk_add(rh, QH)
    def syn_idx(E, cols):
        Y = (E @ A[:, cols].T) % q  # K x r
        return (Y[:, rl:] * pwh).sum(axis=1).astype(np.int32), (Y[:, :rl] * pwl).sum(axis=1).astype(np.int32)
    Efull = np.concatenate([shell_vectors(n, q, w) for w in range(R + 1)])
    Fhi, Flo = syn_idx(Efull, list(range(n)))
    Esh = shell_vectors(n - 1, q, R)
    K = len(Esh)
    Yhi = np.zeros((n, K), dtype=np.int32); Ylo = np.zeros((n, K), dtype=np.int32)
    for i in range(n):
        Yhi[i], Ylo[i] = syn_idx(Esh, [j for j in range(n) if j != i])
    Chi = np.zeros((n, q), dtype=np.int32); Clo = np.zeros((n, q), dtype=np.int32)
    for i in range(n):
        for lam in range(q):
            y = (lam * A[:, i]) % q
            Chi[i, lam] = (y[rl:] * pwh).sum(); Clo[i, lam] = (y[:rl] * pwl).sum()
    N = q ** r
    print(tag, "m", m, "|C|", m * q ** (n - r), "quot", N, "ball", len(Efull), "shell", K, "D", D.tolist(), flush=True)
    if startS:
        S = np.loadtxt(startS, dtype=np.int64).reshape(-1)
        S = S[rng.permutation(len(S))[:m]]
    else:
        S = rng.integers(0, N, size=m)
    Shi = (S // QL).astype(np.int32); Slo = (S % QL).astype(np.int32)
    cnt = np.zeros(N, dtype=np.int32)
    cost = N
    for j in range(m):
        cost += add_ball(cnt, Shi[j], Slo[j], Fhi, Flo, addH, addL, QL, 1)
    buf = np.zeros((K, 2), dtype=np.int64)
    t0 = time.time(); s = seed * 100000; nch = 0
    chunk = max(200, int(2e7 / K / 10))
    bestcost = cost
    while time.time() - t0 < secs:
        if cost == 0:
            m = len(Shi)
            fn = f"S_{tag}_m{m}_s{seed}.txt"
            np.savetxt(fn, Shi.astype(np.int64) * QL + Slo, fmt="%d")
            np.savetxt(f"D_{tag}_m{m}_s{seed}.txt", D, fmt="%d")
            print(f"[{time.time()-t0:7.1f}s] COVER m={m} |C|={m*q**(n-r)} saved {fn}", flush=True)
            if m == 1:
                break
            bestj, bestu = -1, N + 1
            for j in range(m):
                u = add_ball(cnt, Shi[j], Slo[j], Fhi, Flo, addH, addL, QL, -1)
                add_ball(cnt, Shi[j], Slo[j], Fhi, Flo, addH, addL, QL, 1)
                if u < bestu:
                    bestu, bestj = u, j
            cost += add_ball(cnt, Shi[bestj], Slo[bestj], Fhi, Flo, addH, addL, QL, -1)
            Shi = np.delete(Shi, bestj); Slo = np.delete(Slo, bestj)
            bestcost = cost
            continue
        s += 1; nch += 1
        T = T0 * (T1 / T0) ** ((nch % cyc) / cyc)
        cost, used = anneal(Shi, Slo, cnt, cost, Yhi, Ylo, Chi, Clo, addH, addL, QL, q, T, chunk, s, buf)
        bestcost = min(bestcost, cost)
        if nch % 100 == 0:
            print(f"[{time.time()-t0:7.1f}s] m={len(Shi)} cost={cost} best={bestcost}", flush=True)
    print("final m", len(Shi), "cost", cost, "best", bestcost)

if __name__ == "__main__":
    main()
