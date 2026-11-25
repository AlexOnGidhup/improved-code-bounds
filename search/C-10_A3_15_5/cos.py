"""Union of cosets of a GF(q)-linear kernel C0=[n,k,>=d]_q (q prime) + Cayley-graph clique search.
Code = {x : Hx in S}; S subset of F_q^m (m=n-k), all differences of S must have coset weight >= d.
Usage: python cos.py q n k d seconds seed
"""
import sys, time, numpy as np
from numba import njit


def rand_code(q, n, k, d, rng, tries=2000):
    for _ in range(tries):
        A = rng.integers(0, q, size=(k, n - k))
        G = np.concatenate([np.eye(k, dtype=np.int64), A], axis=1)
        if mind(G, q) >= d:
            return G
    return None


def mind(G, q):
    k, n = G.shape
    # enumerate all nonzero messages
    N = q ** k
    idx = np.arange(1, N)
    msgs = np.zeros((N - 1, k), dtype=np.int64)
    t = idx.copy()
    for i in range(k):
        msgs[:, i] = t % q
        t //= q
    W = (msgs @ G) % q
    return int((W != 0).sum(axis=1).min())


def parity_from_G(G, q):
    k, n = G.shape
    A = G[:, k:]
    H = np.concatenate([(-A.T) % q, np.eye(n - k, dtype=np.int64)], axis=1)  # m x n
    return H


@njit(cache=True)
def build_D(Hcols, q, m, d):
    # Hcols: n x m digits. coset weight BFS over F_q^m, index = sum digit*q^i
    N = q ** m
    n = Hcols.shape[0]
    pw = np.ones(m, dtype=np.int64)
    for i in range(1, m):
        pw[i] = pw[i - 1] * q
    w = np.full(N, 99, dtype=np.int8)
    w[0] = 0
    frontier = np.zeros(N, dtype=np.int64)
    fc = 1
    frontier[0] = 0
    for layer in range(1, d):
        nf = np.zeros(N, dtype=np.int64)
        nc = 0
        for t in range(fc):
            v = frontier[t]
            # digits of v
            dig = np.zeros(m, dtype=np.int64)
            x = v
            for i in range(m):
                dig[i] = x % q
                x //= q
            for j in range(n):
                for c in range(1, q):
                    u = 0
                    for i in range(m):
                        u += ((dig[i] + c * Hcols[j, i]) % q) * pw[i]
                    if w[u] == 99:
                        w[u] = layer
                        nf[nc] = u
                        nc += 1
        frontier = nf
        fc = nc
    return w


@njit(cache=True)
def subtab(q, m, N):
    # sub[a,b] = a-b (digitwise mod q) for all pairs -- only if N small
    S = np.zeros((N, N), dtype=np.int32)
    pw = np.ones(m, dtype=np.int64)
    for i in range(1, m):
        pw[i] = pw[i - 1] * q
    for a in range(N):
        for b in range(N):
            x = a
            y = b
            r = 0
            for i in range(m):
                r += (((x % q) - (y % q)) % q) * pw[i]
                x //= q
                y //= q
            S[a, b] = r
    return S


@njit(cache=True)
def adj_matrix(good, sub):
    # vertices = indices where good[v] (v nonzero, neighbors of 0). adjacency: good[sub[a,b]]
    V = np.nonzero(good)[0]
    nv = V.shape[0]
    A = np.zeros((nv, nv), dtype=np.uint8)
    for i in range(nv):
        for j in range(nv):
            if i != j and good[sub[V[i], V[j]]]:
                A[i, j] = 1
    return V, A


@njit(cache=True)
def search(A, iters, seed, target):
    # swap-based local search for max clique (plateau + random restarts); returns best clique
    np.random.seed(seed)
    n = A.shape[0]
    inS = np.zeros(n, dtype=np.uint8)
    conf = np.zeros(n, dtype=np.int32)  # number of S members NOT adjacent (excluding self)
    S = np.zeros(n, dtype=np.int64)
    sz = 0
    best = 0
    bestS = np.zeros(n, dtype=np.int64)
    tabu = np.zeros(n, dtype=np.int64)
    for it in range(1, iters + 1):
        # collect add candidates (conf==0, not in S)
        nadd = 0
        cand = np.empty(n, dtype=np.int64)
        for v in range(n):
            if inS[v] == 0 and conf[v] == 0:
                cand[nadd] = v
                nadd += 1
        if nadd > 0:
            v = cand[np.random.randint(nadd)]
            inS[v] = 1
            S[sz] = v
            sz += 1
            for u in range(n):
                if u != v and A[v, u] == 0:
                    conf[u] += 1
            if sz > best:
                best = sz
                bestS[:sz] = S[:sz]
                if best >= target:
                    return best, bestS
            continue
        # swap candidates: conf==1, not tabu
        nsw = 0
        for v in range(n):
            if inS[v] == 0 and conf[v] == 1 and tabu[v] < it:
                cand[nsw] = v
                nsw += 1
        if nsw > 0 and np.random.random() < 0.97:
            v = cand[np.random.randint(nsw)]
            # find the conflicting member
            r = -1
            for t in range(sz):
                if A[v, S[t]] == 0:
                    r = t
                    break
            u0 = S[r]
            S[r] = S[sz - 1]
            sz -= 1
            inS[u0] = 0
            for u in range(n):
                if u != u0 and A[u0, u] == 0:
                    conf[u] -= 1
            tabu[u0] = it + 7 + np.random.randint(10)
            inS[v] = 1
            S[sz] = v
            sz += 1
            for u in range(n):
                if u != v and A[v, u] == 0:
                    conf[u] += 1
        else:
            # perturb: drop random members
            nd = 1 + np.random.randint(3)
            for _ in range(nd):
                if sz == 0:
                    break
                r = np.random.randint(sz)
                u0 = S[r]
                S[r] = S[sz - 1]
                sz -= 1
                inS[u0] = 0
                for u in range(n):
                    if u != u0 and A[u0, u] == 0:
                        conf[u] -= 1
    return best, bestS


def run(q, n, k, d, secs, seed, maxN=7000, chunk=20000):
    rng = np.random.default_rng(seed)
    m = n - k
    N = q ** m
    assert N <= maxN, N
    sub = subtab(q, m, N)
    t0 = time.time()
    bestall = 0
    bestinfo = None
    while time.time() - t0 < secs:
        G = rand_code(q, n, k, d, rng)
        if G is None:
            print('no kernel found'); return
        H = parity_from_G(G, q)
        w = build_D(np.ascontiguousarray(H.T), q, m, d)
        good = (w == 99)  # coset weight >= d  (0 has weight 0)
        V, A = adj_matrix(good, sub)
        if len(V) == 0:
            continue
        best, bs = search(A, chunk, int(rng.integers(1 << 30)), 10 ** 9)
        size = (best + 1) * q ** k
        if size > bestall:
            bestall = size
            bestinfo = (G, H, [0] + [int(V[i]) for i in bs[:best]])
            print(f'q={q} n={n} k={k} d={d}: |S|={best+1} size={size} nV={len(V)} t={time.time()-t0:.0f}s', flush=True)
    return bestall, bestinfo


if __name__ == '__main__':
    q, n, k, d = map(int, sys.argv[1:5])
    secs = float(sys.argv[5]); seed = int(sys.argv[6])
    r = run(q, n, k, d, secs, seed)
    if r and r[1]:
        np.save(f'best_{q}_{n}_{d}_k{k}_{r[0]}.npy', np.array(r[1][2]))
        np.save(f'bestG_{q}_{n}_{d}_k{k}_{r[0]}.npy', r[1][0])
