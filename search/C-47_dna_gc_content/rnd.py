"""Zufaellige Gruppenwahl: Erzeuger = (Permutation mit strukturiertem Zyklentyp, Symbolabbildungen je Koordinate).
Aufruf: python rnd.py n d minutes lo hi seed iters"""
import sys, time, json, random, math
import numpy as np
from orb import *

CLS = [(0, 1, 2, 3), (1, 0, 2, 3), (0, 1, 3, 2), (1, 0, 3, 2)]
COMP = [(2, 3, 0, 1), (3, 2, 1, 0)]


def rand_perm(n, rng):
    pts = list(range(n))
    rng.shuffle(pts)
    typ = rng.random()
    p = list(range(n))
    if typ < 0.6:
        Ls = [rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, n, n - 1, n // 2, n // 3])]
    else:
        Ls = [rng.choice([2, 3, 4, 5, 6]), rng.choice([2, 3, 4, 5, 6, 7])]
    i = 0
    for L in Ls:
        L = max(2, L)
        k = 0
        while i + L <= n and k < n // L:
            cyc = pts[i:i + L]
            for a in range(L):
                p[cyc[a]] = cyc[(a + 1) % L]
            i += L
            k += 1
            if rng.random() < 0.3:
                break
    return p


def rand_gen(n, rng, allow_comp):
    p = rand_perm(n, rng)
    mode = rng.random()
    maps = []
    if mode < 0.35:
        s = rng.choice(CLS)
        maps = [s] * n
    elif mode < 0.7:
        maps = [rng.choice(CLS) for _ in range(n)]
    else:
        # nur wenige Koordinaten getwistet
        maps = [(0, 1, 2, 3)] * n
        for _ in range(rng.randint(0, 2)):
            maps[rng.randrange(n)] = rng.choice(CLS)
    if allow_comp and rng.random() < 0.3:
        c = rng.choice(COMP)
        # komponieren: erst maps, dann c
        maps = [tuple(c[m[s]] for s in range(4)) for m in maps]
    return (tuple(p), tuple(tuple(m) for m in maps))


if __name__ == '__main__':
    n, d, minutes, lo, hi, seed, iters = map(int, sys.argv[1:8])
    rng = random.Random(seed)
    t0 = time.time()
    best = 0
    tried = 0
    stat = {}
    while time.time() - t0 < minutes * 60:
        k = rng.choice([1, 2, 2, 3])
        gens = [rand_gen(n, rng, n % 2 == 0) for _ in range(k)]
        try:
            G = closure(gens, n, limit=hi)
        except ValueError:
            continue
        if len(G) < lo:
            continue
        tried += 1
        r = run(n, d, gens, iters=iters, seeds=2, verbose=False, maxorb=40000)
        if r is None:
            continue
        b, words, g, N = r
        stat[len(G)] = max(stat.get(len(G), 0), b)
        if b > best:
            best = b
            fn = f"rbest_{n}_{d}_s{seed}.txt"
            with open(fn, 'w') as f:
                for x in words:
                    f.write(word_to_str(x, n) + "\n")
            json.dump({'size': b, 'G': len(G), 'N': N, 'gens': gens}, open(f"rbest_{n}_{d}_s{seed}.json", 'w'))
            print(f"[{time.time()-t0:.0f}s] tried={tried} neues Bestes {b} |G|={len(G)} Orbits={N}", flush=True)
    print("fertig", n, d, "best", best, "tried", tried, "perG", sorted(stat.items()))
