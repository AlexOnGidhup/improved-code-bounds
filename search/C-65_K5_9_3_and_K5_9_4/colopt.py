import numpy as np, numba as nb, sys, time
@nb.njit(cache=True)
def vec_add(a, b, p, m):
    r = 0; pw = 1
    for j in range(m):
        r += ((a % p + b % p) % p) * pw
        a //= p; b //= p; pw *= p
    return r
@nb.njit(cache=True)
def vec_mul(c, a, p, m):
    r = 0; pw = 1
    for j in range(m):
        r += ((a % p) * c % p) * pw
        a //= p; pw *= p
    return r
@nb.njit(cache=True)
def ballsize(cols, p, m, R, N):
    n = len(cols)
    G = np.empty(n*(p-1), np.int64); k = 0
    for i in range(n):
        for c in range(1, p):
            G[k] = vec_mul(c, cols[i], p, m); k += 1
    reach = np.zeros(N, np.bool_); reach[0] = True
    cur = np.zeros(N, np.bool_); cur[0] = True
    for r in range(R):
        nxt = cur.copy()
        for x in range(N):
            if cur[x]:
                for g in G:
                    nxt[vec_add(x, g, p, m)] = True
        cur = nxt
    return cur.sum()
@nb.njit(cache=True)
def opt(p, n, R, m, iters, seed):
    np.random.seed(seed)
    N = p**m
    cols = np.empty(n, np.int64)
    for j in range(m): cols[j] = p**j
    for j in range(m, n): cols[j] = np.random.randint(1, N)
    best = ballsize(cols, p, m, R, N)
    for it in range(iters):
        j = np.random.randint(m, n)
        old = cols[j]; cols[j] = np.random.randint(1, N)
        v = ballsize(cols, p, m, R, N)
        if v >= best: best = v
        else: cols[j] = old
        if best == N: break
    return best, cols
if __name__ == "__main__":
    p, n, R, m, iters, seed = map(int, sys.argv[1:7])
    t=time.time(); b, c = opt(p, n, R, m, iters, seed)
    print(p, n, R, m, "ball", b, "of", p**m, list(c), f"{time.time()-t:.0f}s")
