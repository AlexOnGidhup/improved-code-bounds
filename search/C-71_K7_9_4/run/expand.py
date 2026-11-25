# expand matrix-method solution (S, D) to explicit code file: C = {x in Z_q^n : [I_r|D] x in S}
# x = (y - D t, t) for y in S, t in Z_q^(n-r)
import sys, itertools
import numpy as np
q, n, r = map(int, sys.argv[1:4]); Sf, Df, out = sys.argv[4:7]
S = np.loadtxt(Sf, dtype=np.int64).reshape(-1)
D = np.loadtxt(Df, dtype=np.int64).reshape(r, n - r)
rl = r // 2; QL = q ** rl
words = set()
for s in S:
    hi, lo = divmod(int(s), QL)
    y = [(lo // q ** t) % q for t in range(rl)] + [(hi // q ** t) % q for t in range(r - rl)]
    y = np.array(y)
    for t in itertools.product(range(q), repeat=n - r):
        x = list((y - D @ np.array(t)) % q) + list(t)
        words.add("".join(map(str, x)))
with open(out, "w") as f:
    for w in sorted(words):
        f.write(w + "\n")
print(out, len(words))
