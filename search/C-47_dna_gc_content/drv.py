import sys, time, json, itertools, math
import numpy as np
from orb import *


def shift(n, sym='none', wrap_only=True):
    p = [(i + 1) % n for i in range(n)]
    return gen_perm(p, n, sym, coords={n - 1} if wrap_only else None)


def mult(n, a):
    return gen_perm([(a * i) % n for i in range(n)], n)


def refl(n):
    return gen_perm([(-i) % n for i in range(n)], n)


def gl(n, sym):
    return gen_global(n, sym)


def groups(n):
    """Liste (name, gens) fuer Gruppenwahl."""
    out = []
    syms = ['none', 'AT', 'GC', 'both'] + (['comp', 'compx'] if n % 2 == 0 else [])
    units = [a for a in range(2, n) if math.gcd(a, n) == 1]
    for ws in ['none', 'AT', 'GC', 'both']:
        for gs in syms:
            g = [shift(n, ws)]
            if gs != 'none':
                g.append(gl(n, gs))
            out.append((f"Z{n}[tw={ws}]+glob={gs}", g))
    for a in units:
        for gs in ['none', 'AT', 'both'] + (['comp'] if n % 2 == 0 else []):
            g = [shift(n), mult(n, a)]
            if gs != 'none':
                g.append(gl(n, gs))
            out.append((f"Z{n}x*{a}+glob={gs}", g))
    for gs in ['none', 'AT', 'both'] + (['comp'] if n % 2 == 0 else []):
        g = [shift(n), refl(n)]
        if gs != 'none':
            g.append(gl(n, gs))
        out.append((f"D{n}+glob={gs}", g))
    return out


if __name__ == '__main__':
    n = int(sys.argv[1])
    d = int(sys.argv[2])
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
    minG = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    maxG = int(sys.argv[5]) if len(sys.argv) > 5 else 200
    best = 0
    for name, gens in groups(n):
        try:
            G = closure(gens, n)
        except ValueError:
            continue
        if not (minG <= len(G) <= maxG):
            continue
        print(name, len(G), flush=True)
        t = time.time()
        r = run(n, d, gens, iters=iters, seeds=2)
        if r is None:
            continue
        b, words, g, N = r
        print(f"  => {b}  ({time.time()-t:.0f}s)", flush=True)
        if b > best:
            best = b
            with open(f"best_{n}_{d}.txt", 'w') as f:
                for x in words:
                    f.write(word_to_str(x, n) + "\n")
            print("  ** neues Bestes", best, name, flush=True)
