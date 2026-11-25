# Eigenstaendige Pruefung gemischter binaer/ternaerer Codes N(m,n,d) (nur Standardbibliothek).
# Aufruf:  python verify.py            (prueft alle unten gelisteten Dateien im Verzeichnis dieses Skripts)
# Format der Codedateien: ein Codewort je Zeile, erst m Binaerziffern (0/1), dann n Ternaerziffern (0/1/2).
# Geprueft wird vollstaendig: Laenge, Alphabet je Koordinate, Anzahl, Verschiedenheit, Mindest-Hammingabstand.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
# Datei: (m, n, d, bisherige untere Schranke laut Brouwer 23codes.html, Abruf 2026-11-25)
CODES = {
    "code_N_2_12_7.txt": (2, 12, 7, 162),
    "code_N_3_11_7.txt": (3, 11, 7, 108),
}
ok_all = True
for name, (m, n, d, rec) in CODES.items():
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        print(name, "fehlt"); ok_all = False; continue
    W = open(path).read().split("\n")
    if W and W[-1] == "": W.pop()
    ok = True
    for w in W:
        if len(w) != m + n or any(c not in "01" for c in w[:m]) or any(c not in "012" for c in w[m:]):
            ok = False
    distinct = len(set(W)) == len(W)
    md = min((sum(a != b for a, b in zip(W[i], W[j])) for i in range(len(W)) for j in range(i)), default=0)
    good = ok and distinct and md >= d and len(W) > rec
    ok_all &= good
    print(f"{name}: m={m} n={n} Laenge={m+n} Woerter={len(W)} Format_ok={ok} verschieden={distinct} "
          f"Mindestabstand={md} (gefordert {d}) Tabellenwert={rec} -> {'BESSER ALS TABELLE' if good else 'FEHLER/KEIN FORTSCHRITT'}")
sys.exit(0 if ok_all else 1)
