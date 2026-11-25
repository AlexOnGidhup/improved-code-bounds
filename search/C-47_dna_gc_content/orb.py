"""Orbit-Clique-Werkzeug fuer A_4^GC(n,d,w=n//2). Symbole 0=A,1=T,2=G,3=C (GC = Bit1). Wort = 2 Bit je Koordinate.
Gruppenelement: (perm p, maps[i][s]); y[p[i]] = maps[i][x[i]]. Gruppe wird per Abschluss aus Erzeugern erzeugt."""
import numpy as np, numba as nb, itertools, sys, time, json
from numba import njit, prange


def compose(g, h):  # erst g dann h
    pg, mg = g
    ph, mh = h
    n = len(pg)
    p = tuple(ph[pg[i]] for i in range(n))
    m = tuple(tuple(mh[pg[i]][mg[i][s]] for s in range(4)) for i in range(n))
    return (p, m)


def ident(n):
    return (tuple(range(n)), tuple((0, 1, 2, 3) for _ in range(n)))


def closure(gens, n, limit=5000):
    e = ident(n)
    S = {e}
    fr = [e]
    while fr:
        nf = []
        for g in fr:
            for h in gens:
                k = compose(g, h)
                if k not in S:
                    S.add(k)
                    nf.append(k)
                    if len(S) > limit:
                        raise ValueError("Gruppe zu gross")
        fr = nf
    return sorted(S)


SW = {'none': (0, 1, 2, 3), 'AT': (1, 0, 2, 3), 'GC': (0, 1, 3, 2), 'both': (1, 0, 3, 2),
      'comp': (2, 3, 0, 1), 'compx': (3, 2, 1, 0)}


def gen_perm(p, n, sym='none', coords=None):
    """Permutation p (i->p[i]); auf Koordinaten 'coords' (Default alle) wirkt zusaetzlich Symbolabbildung sym."""
    maps = []
    for i in range(n):
        maps.append(SW[sym] if (coords is None or i in coords) else (0, 1, 2, 3))
    return (tuple(p), tuple(maps))


def gen_global(n, sym):
    return gen_perm(range(n), n, sym)


def tables(G, n):
    P = np.array([g[0] for g in G], dtype=np.int64)
    M = np.array([g[1] for g in G], dtype=np.int64)
    return P, M


@njit(cache=True)
def popc(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


@njit(cache=True)
def dist(x, y, mask):
    z = x ^ y
    return popc((z | (z >> 1)) & mask)


@njit(cache=True)
def apply(x, P, M, k, n):
    y = 0
    for i in range(n):
        s = (x >> (2 * i)) & 3
        y |= M[k, i, s] << (2 * P[k, i])
    return y


@njit(cache=True)
def enum_orbits(n, w, d, P, M, maxorb):
    mask = 0
    for i in range(n):
        mask |= 1 << (2 * i)
    hmask = mask << 1
    G = P.shape[0]
    vis = np.zeros(1 << (2 * n), dtype=np.uint8)
    reps = np.zeros(maxorb, dtype=np.int64)
    cnt = 0
    tmp = np.zeros(G, dtype=np.int64)
    for x in range(1 << (2 * n)):
        if vis[x]:
            continue
        if popc(x & hmask) != w:
            continue
        ok = True
        m = 0
        for k in range(G):
            y = apply(x, P, M, k, n)
            if vis[y] == 0:
                vis[y] = 1
                tmp[m] = y
                m += 1
        for a in range(m):
            if tmp[a] != x and dist(x, tmp[a], mask) < d:
                ok = False
                break
        if ok:
            if cnt < maxorb:
                reps[cnt] = x
            cnt += 1
    return reps[:min(cnt, maxorb)], cnt


@njit(cache=True)
def orbit_members(x, P, M, n):
    G = P.shape[0]
    tmp = np.empty(G, dtype=np.int64)
    for k in range(G):
        tmp[k] = apply(x, P, M, k, n)
    tmp.sort()
    out = np.empty(G, dtype=np.int64)
    m = 0
    for k in range(G):
        if k == 0 or tmp[k] != tmp[k - 1]:
            out[m] = tmp[k]
            m += 1
    return out[:m]


@njit(parallel=True, cache=True)
def build_adj(reps, P, M, n, d):
    N = len(reps)
    G = P.shape[0]
    mask = 0
    for i in range(n):
        mask |= 1 << (2 * i)
    W = (N + 63) // 64
    A = np.zeros((N, W), dtype=np.uint64)
    mem = np.empty((N, G), dtype=np.int64)
    msz = np.zeros(N, dtype=np.int32)
    for i in range(N):
        o = orbit_members(reps[i], P, M, n)
        msz[i] = len(o)
        mem[i, :len(o)] = o
    for i in prange(N):
        x = reps[i]
        for j in range(i + 1, N):
            ok = True
            for t in range(msz[j]):
                if dist(x, mem[j, t], mask) < d:
                    ok = False
                    break
            if ok:
                A[i, j >> 6] |= np.uint64(1) << np.uint64(j & 63)
    for i in range(N):
        for j in range(i + 1, N):
            if (A[i, j >> 6] >> np.uint64(j & 63)) & np.uint64(1):
                A[j, i >> 6] |= np.uint64(1) << np.uint64(i & 63)
    return A, mem, msz


@njit(cache=True)
def getbit(A, i, j):
    return (A[i, j >> 6] >> np.uint64(j & 63)) & np.uint64(1)


@njit(cache=True)
def mwc_tabu(A, wt, iters, seed, Lrestart):
    np.random.seed(seed)
    N = len(wt)
    inC = np.zeros(N, dtype=np.uint8)
    adjc = np.zeros(N, dtype=np.int32)
    tabu = np.zeros(N, dtype=np.int64)
    csz = 0
    cw = 0
    best = 0
    bestC = np.zeros(N, dtype=np.uint8)
    last_imp = 0
    for it in range(1, iters + 1):
        bgain = -10 ** 9
        bv = -1
        bout = -1
        nb_ = 0
        for u in range(N):
            if inC[u]:
                continue
            if tabu[u] > it:
                continue
            miss = csz - adjc[u]
            if miss == 0:
                g = wt[u]
                o = -1
            elif miss == 1:
                o = -1
                for v in range(N):
                    if inC[v] and getbit(A, u, v) == 0:
                        o = v
                        break
                g = wt[u] - wt[o]
            else:
                continue
            if g > bgain:
                bgain = g
                bv = u
                bout = o
                nb_ = 1
            elif g == bgain:
                nb_ += 1
                if np.random.randint(nb_) == 0:
                    bv = u
                    bout = o
        dv = -1
        if bv < 0 or bgain < 0:
            # Drop-Option nur, wenn keine nichtnegative Bewegung
            if csz > 0:
                nd = 0
                dg = -10 ** 9
                for v in range(N):
                    if inC[v]:
                        g = -wt[v]
                        if g > dg:
                            dg = g
                            dv = v
                            nd = 1
                        elif g == dg:
                            nd += 1
                            if np.random.randint(nd) == 0:
                                dv = v
                if bv >= 0 and dg > bgain:
                    pass
                else:
                    dv = -1 if bv >= 0 else dv
        if bv >= 0 and (dv < 0 or bgain >= -wt[dv]):
            if bout >= 0:
                inC[bout] = 0
                csz -= 1
                cw -= wt[bout]
                for u in range(N):
                    if getbit(A, bout, u):
                        adjc[u] -= 1
                tabu[bout] = it + 7 + np.random.randint(10)
            inC[bv] = 1
            csz += 1
            cw += wt[bv]
            for u in range(N):
                if getbit(A, bv, u):
                    adjc[u] += 1
        elif dv >= 0:
            v = dv
            inC[v] = 0
            csz -= 1
            cw -= wt[v]
            for u in range(N):
                if getbit(A, v, u):
                    adjc[u] -= 1
            tabu[v] = it + 7 + np.random.randint(10)
        else:
            break
        if cw > best:
            best = cw
            bestC[:] = inC
            last_imp = it
        if it - last_imp > Lrestart:
            for v in range(N):
                if inC[v] and np.random.random() < 0.5:
                    inC[v] = 0
                    csz -= 1
                    cw -= wt[v]
                    for u in range(N):
                        if getbit(A, v, u):
                            adjc[u] -= 1
            last_imp = it
    return best, bestC


def word_to_str(x, n):
    return ''.join(str((x >> (2 * i)) & 3) for i in range(n))


def run(n, d, gens, iters=200000, seeds=3, maxorb=200000, verbose=True):
    w = n // 2
    G = closure(gens, n)
    P, M = tables(G, n)
    t = time.time()
    reps, cnt = enum_orbits(n, w, d, P, M, maxorb)
    if cnt > maxorb:
        print(f"  |G|={len(G)} Orbits(selbst-kompat)={cnt} > maxorb")
        return None
    N = len(reps)
    if verbose:
        print(f"  |G|={len(G)} Orbits={N} (enum {time.time()-t:.1f}s)", flush=True)
    if N == 0:
        return (0, [], len(G), 0)
    est = N * N / 8 + N * len(G) * 8
    if est > 1.5e9:
        print("  Speicher zu gross", est / 1e9)
        return None
    t = time.time()
    A, mem, msz = build_adj(reps, P, M, n, d)
    if verbose:
        print(f"  Adjazenz {time.time()-t:.1f}s", flush=True)
    wt = msz.astype(np.int64)
    best = 0
    bC = None
    for s in range(seeds):
        b, C = mwc_tabu(A, wt, iters, s + 1, max(2000, iters // 20))
        if b > best:
            best = b
            bC = C.copy()
    words = []
    for i in np.nonzero(bC)[0]:
        for t_ in range(msz[i]):
            words.append(int(mem[i, t_]))
    return best, words, len(G), N
