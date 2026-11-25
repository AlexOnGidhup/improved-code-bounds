# Matrixmethode ueber Z_q: Code = {x in Z_q^n : H x in S}, H: m x n ueber Z_q, S Menge von s Syndromen.
# Ueberdeckungsradius R=2 (R=1/3 per Parameter).  Gesamtgroesse = s * q^(n-m) (H voller Rang vorausgesetzt, q prim).
import numpy as np, numba as nb, sys, time
@nb.njit(cache=True)
def enc(v, q, m):
    r = 0
    for i in range(m - 1, -1, -1): r = r * q + v[i]
    return r
@nb.njit(cache=True)
def dec(x, q, m, out):
    for i in range(m):
        out[i] = x % q; x //= q
@nb.njit(cache=True)
def build_B(H, q, n, m, R, B):
    # H[j,:] = Spalte j (digits). B enthaelt digit-Vektoren aller Syndrome von Gewicht<=R
    cnt = 0
    for i in range(m): B[0, i] = 0
    cnt = 1
    # Gewicht 1
    for j in range(n):
        for a in range(1, q):
            for i in range(m): B[cnt, i] = (a * H[j, i]) % q
            cnt += 1
    if R >= 2:
        for j in range(n):
            for k in range(j + 1, n):
                for a in range(1, q):
                    for b in range(1, q):
                        for i in range(m): B[cnt, i] = (a * H[j, i] + b * H[k, i]) % q
                        cnt += 1
    if R >= 3:
        for j in range(n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    for a in range(1, q):
                        for b in range(1, q):
                            for c in range(1, q):
                                for i in range(m): B[cnt, i] = (a * H[j, i] + b * H[k, i] + c * H[l, i]) % q
                                cnt += 1
    return cnt
@nb.njit(cache=True)
def addball(sd, sgn, B, nb_, q, m, cov, unc, pos, nu):
    for t in range(nb_):
        r = 0
        for i in range(m - 1, -1, -1):
            r = r * q + (sd[i] + B[t, i]) % q
        c = cov[r]
        if sgn > 0:
            if c == 0:
                p = pos[r]; last = unc[nu[0] - 1]; unc[p] = last; pos[last] = p; nu[0] -= 1
            cov[r] = c + 1
        else:
            if c == 1:
                unc[nu[0]] = r; pos[r] = nu[0]; nu[0] += 1
            cov[r] = c - 1
@nb.njit(cache=True)
def search(q, n, m, s, R, iters, seed, pH, T):
    np.random.seed(seed)
    Q = q ** m
    maxB = 1 + n * (q - 1) + (n * (n - 1) // 2) * (q - 1) ** 2
    if R >= 3: maxB += (n * (n - 1) * (n - 2) // 6) * (q - 1) ** 3
    B = np.zeros((maxB, m), np.int64)
    H = np.random.randint(0, q, (n, m))
    nbb = build_B(H, q, n, m, R, B)
    cov = np.zeros(Q, np.int32); unc = np.arange(Q); pos = np.arange(Q); nu = np.array([Q])
    S = np.random.randint(0, Q, s)
    sd = np.zeros(m, np.int64); sd2 = np.zeros(m, np.int64)
    for k in range(s):
        dec(S[k], q, m, sd); addball(sd, 1, B, nbb, q, m, cov, unc, pos, nu)
    best = nu[0]; bestH = H.copy(); bestS = S.copy()
    for it in range(iters):
        if nu[0] == 0:
            return 0, H, S, it
        if np.random.random() < pH:
            # Spaltenwechsel: alles neu
            j = np.random.randint(n)
            oldcol = H[j].copy()
            oldnu = nu[0]
            for i in range(m): H[j, i] = np.random.randint(0, q)
            B2 = np.zeros((maxB, m), np.int64)
            nb2 = build_B(H, q, n, m, R, B2)
            cov2 = np.zeros(Q, np.int32); unc2 = np.arange(Q); pos2 = np.arange(Q); nu2 = np.array([Q])
            for k in range(s):
                dec(S[k], q, m, sd); addball(sd, 1, B2, nb2, q, m, cov2, unc2, pos2, nu2)
            d = nu2[0] - oldnu
            if d <= 0 or np.random.random() < np.exp(-d / T):
                B = B2; nbb = nb2; cov = cov2; unc = unc2; pos = pos2; nu = nu2
            else:
                for i in range(m): H[j, i] = oldcol[i]
        else:
            u = unc[np.random.randint(nu[0])]
            k = np.random.randint(s)
            t = np.random.randint(nbb)
            dec(u, q, m, sd2)
            # neues sigma = u - B[t]
            r = 0
            for i in range(m - 1, -1, -1): r = r * q + (sd2[i] - B[t, i] + q) % q
            old = nu[0]
            dec(S[k], q, m, sd); addball(sd, -1, B, nbb, q, m, cov, unc, pos, nu)
            dec(r, q, m, sd); addball(sd, 1, B, nbb, q, m, cov, unc, pos, nu)
            d = nu[0] - old
            if d <= 0 or np.random.random() < np.exp(-d / T):
                S[k] = r
            else:
                dec(r, q, m, sd); addball(sd, -1, B, nbb, q, m, cov, unc, pos, nu)
                dec(S[k], q, m, sd); addball(sd, 1, B, nbb, q, m, cov, unc, pos, nu)
        if nu[0] < best:
            best = nu[0]; bestH = H.copy(); bestS = S.copy()
    return best, bestH, bestS, iters

def rank_mod(H, q):
    # q prim; H: n x m
    A = [list(map(int, r)) for r in H]; rk = 0
    cols = len(A[0])
    for c in range(cols):
        p = None
        for r in range(rk, len(A)):
            if A[r][c] % q: p = r; break
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]
        inv = pow(A[rk][c], -1, q)
        A[rk] = [(x * inv) % q for x in A[rk]]
        for r in range(len(A)):
            if r != rk and A[r][c] % q:
                f = A[r][c]; A[r] = [(x - f * y) % q for x, y in zip(A[r], A[rk])]
        rk += 1
    return rk

def expand(q, n, m, H, S):
    # alle x in Z_q^n mit Hx^T in S  (H: n Spalten der Laenge m)
    import itertools
    Sset = set(int(x) for x in S)
    words = []
    X = np.array(list(itertools.product(range(q), repeat=n)), dtype=np.int64)[:, ::-1]
    syn = (X @ np.array(H, dtype=np.int64)) % q  # (N, m)
    idx = np.zeros(len(X), np.int64)
    for i in range(m - 1, -1, -1): idx = idx * q + syn[:, i]
    mask = np.isin(idx, list(Sset))
    return X[mask]

if __name__ == "__main__":
    q, n, m, s, R, secs, seed = map(int, sys.argv[1:8])
    iters = int(sys.argv[8]) if len(sys.argv) > 8 else 2000000
    T = float(sys.argv[9]) if len(sys.argv) > 9 else 0.5
    pH = float(sys.argv[10]) if len(sys.argv) > 10 else 0.02
    t0 = time.time(); sd = seed; bestu = 10**9
    while time.time() - t0 < secs:
        u, H, S, it = search(q, n, m, s, R, iters, sd, pH, T); sd += 1000
        rk = rank_mod(H, q) if all(q % p for p in range(2, int(q**.5) + 1)) else -1
        print(f"q={q} n={n} m={m} s={s} R={R}: unc={u} rank={rk} size={s*q**(n-m)} t={time.time()-t0:.0f}s", flush=True)
        if u == 0 and (rk == m or rk == -1):
            X = expand(q, n, m, H, S)
            fn = f"mm_q{q}_n{n}_R{R}_{len(X)}.txt"
            with open(fn, "w") as f:
                for w in X: f.write("".join(map(str, w)) + "\n")
            print("saved", fn, len(X), flush=True)
            break
