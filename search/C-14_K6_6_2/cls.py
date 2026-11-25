# WalkSAT-artige Lokalsuche fuer q-aere Ueberdeckungscodes, R=2 (Ball on the fly)
import numpy as np, numba as nb, sys, time, os
@nb.njit(cache=True)
def upd(x, sgn, q, n, pw, cov, unc, pos, nu):
    # addiert sgn (+1/-1) auf die Ueberdeckung des Balls B_2(x); nu[0]=Anzahl unueberdeckt
    d = np.empty(n, np.int64); t = x
    for i in range(n):
        d[i] = t % q; t //= q
    for k in range(3):
        pass
    # Mitte
    ys = x
    _set(ys, sgn, cov, unc, pos, nu)
    for i in range(n):
        for a in range(q):
            if a == d[i]: continue
            y = x + (a - d[i]) * pw[i]
            _set(y, sgn, cov, unc, pos, nu)
            for j in range(i + 1, n):
                for b in range(q):
                    if b == d[j]: continue
                    _set(y + (b - d[j]) * pw[j], sgn, cov, unc, pos, nu)
@nb.njit(cache=True, inline='always')
def _set(y, sgn, cov, unc, pos, nu):
    c = cov[y]
    if sgn > 0:
        if c == 0:
            p = pos[y]; last = unc[nu[0] - 1]; unc[p] = last; pos[last] = p; nu[0] -= 1
        cov[y] = c + 1
    else:
        if c == 1:
            unc[nu[0]] = y; pos[y] = nu[0]; nu[0] += 1
        cov[y] = c - 1
@nb.njit(cache=True)
def run(q, n, M, code, iters, seed, tlimit_steps, noise):
    np.random.seed(seed)
    N = q ** n
    pw = np.empty(n, np.int64); pw[0] = 1
    for i in range(1, n): pw[i] = pw[i-1] * q
    cov = np.zeros(N, np.int16); unc = np.arange(N).astype(np.int64); pos = np.arange(N).astype(np.int64)
    nu = np.array([N], np.int64)
    dig = np.zeros((M, n), np.int64)
    for m in range(M):
        t = code[m]
        for i in range(n):
            dig[m, i] = t % q; t //= q
        upd(code[m], 1, q, n, pw, cov, unc, pos, nu)
    best = nu[0]
    bestcode = code.copy()
    tabu = np.zeros(M, np.int64)
    for it in range(iters):
        if nu[0] == 0:
            return 0, code, it
        u = unc[np.random.randint(nu[0])]
        ud = np.empty(n, np.int64); t = u
        for i in range(n):
            ud[i] = t % q; t //= q
        # Kandidaten: Codewoerter mit minimalem Abstand zu u (R+1 erwartet)
        dmin = 99
        dist = np.empty(M, np.int64)
        for m in range(M):
            s = 0
            for i in range(n):
                if dig[m, i] != ud[i]: s += 1
            dist[m] = s
            if s < dmin: dmin = s
        bestv = 1 << 60; bm = -1; bi = -1; cnt = 0
        for m in range(M):
            if dist[m] != dmin or tabu[m] > it: continue
            for i in range(n):
                if dig[m, i] == ud[i]: continue
                c0 = code[m]
                c1 = c0 + (ud[i] - dig[m, i]) * pw[i]
                u0 = nu[0]
                upd(c0, -1, q, n, pw, cov, unc, pos, nu)
                upd(c1, 1, q, n, pw, cov, unc, pos, nu)
                v = nu[0]
                upd(c1, -1, q, n, pw, cov, unc, pos, nu)
                upd(c0, 1, q, n, pw, cov, unc, pos, nu)
                if np.random.random() < noise: v += np.random.randint(0, 3 * n)
                if v < bestv:
                    bestv = v; bm = m; bi = i; cnt = 1
                elif v == bestv:
                    cnt += 1
                    if np.random.randint(cnt) == 0:
                        bm = m; bi = i
        if bm < 0:
            continue
        c0 = code[bm]; c1 = c0 + (ud[bi] - dig[bm, bi]) * pw[bi]
        upd(c0, -1, q, n, pw, cov, unc, pos, nu)
        upd(c1, 1, q, n, pw, cov, unc, pos, nu)
        code[bm] = c1; dig[bm, bi] = ud[bi]
        tabu[bm] = it + 2 + np.random.randint(0, 6)
        if nu[0] < best:
            best = nu[0]; bestcode = code.copy()
    return nu[0], bestcode, iters

def drop_one(q, n, code):
    # entferne Codewort mit geringstem Verlust (Python/numpy, selten)
    N = q**n
    M = len(code)
    pw = np.array([q**i for i in range(n)], dtype=np.int64)
    cov = np.zeros(N, np.int16); unc = np.arange(N).astype(np.int64); pos = np.arange(N).astype(np.int64); nu = np.array([N], np.int64)
    for c in code: upd(int(c), 1, q, n, pw, cov, unc, pos, nu)
    assert nu[0] == 0
    best = None
    for m in range(M):
        upd(int(code[m]), -1, q, n, pw, cov, unc, pos, nu)
        if best is None or nu[0] < best[0]: best = (nu[0], m)
        upd(int(code[m]), 1, q, n, pw, cov, unc, pos, nu)
    return np.delete(code, best[1])

def check(q, n, R, code):
    N = q**n
    digs = np.array([[ (c // q**i) % q for i in range(n)] for c in code], dtype=np.int8)
    ok = True
    for x in range(N):
        pass
    return True

if __name__ == "__main__":
    q, n, M0, secs, seed = map(int, sys.argv[1:6])
    iters = int(sys.argv[6]) if len(sys.argv) > 6 else 200000
    noise = 0.02
    N = q**n
    rng = np.random.default_rng(seed)
    code = rng.choice(N, M0, replace=False).astype(np.int64)
    t0 = time.time(); M = M0
    out = f"best_q{q}_n{n}_R2.txt"
    while time.time() - t0 < secs:
        nu, bc, it = run(q, n, M, code.copy(), iters, int(rng.integers(1<<30)), 0, noise)
        print(f"q={q} n={n} M={M} unc={nu} it={it} t={time.time()-t0:.0f}s", flush=True)
        if nu == 0:
            with open(out, "w") as f:
                for c in bc: f.write("".join(str((int(c)//q**i)%q) for i in range(n)) + "\n")
            code = drop_one(q, n, bc); M -= 1
        else:
            # weiter ab bestem Stand
            code = bc
