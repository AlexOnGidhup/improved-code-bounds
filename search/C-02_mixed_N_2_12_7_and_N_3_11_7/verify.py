# Eigenstaendige Pruefung gemischter binaer/ternaerer Codes (nur Standardbibliothek).
# Koordinaten: erste m binaer (0/1), dann n ternaer (0/1/2). Vollstaendiges Nachrechnen aller Paarabstaende.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CODES = {  # Datei: (m, n, d, Tabellenwert Brouwer 23codes.html, Abruf 2026-11-25)
    "code_N_2_12_7_171.txt": (2, 12, 7, 162),
    "code_N_2_12_7_171_b.txt": (2, 12, 7, 162),
    "code_N_3_11_7_116.txt": (3, 11, 7, 108),
}
ok_all = True
for name, (m, n, d, rec) in CODES.items():
    W = [l.strip() for l in open(os.path.join(HERE, name)) if l.strip()]
    fmt = all(len(w) == m + n and set(w[:m]) <= set("01") and set(w[m:]) <= set("012") for w in W)
    distinct = len(set(W)) == len(W)
    md = min(sum(a != b for a, b in zip(W[i], W[j])) for i in range(len(W)) for j in range(i))
    good = fmt and distinct and md >= d and len(W) > rec
    ok_all &= good
    print(f"{name}: N({m},{n},{d}) Woerter={len(W)} Format={fmt} verschieden={distinct} "
          f"Mindestabstand={md} (gefordert {d}) Tabelle={rec} -> {'BESSER' if good else 'FEHLER'}")
sys.exit(0 if ok_all else 1)
