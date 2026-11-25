# QUELLE.md — A_3(15,5) >= 8748

**Parameter:** q=3, n=15, d=5. **Erreichte Größe:** 8748 Wörter (Datei `code_3_15_5_8748.txt`, geprüft mit `verify.py`: `python verify.py code_3_15_5_8748.txt 3 5`).

## Vergleichstabelle
- Brouwer, Tabelle ternärer Codes A_3(n,d): https://aeb.win.tue.nl/codes/ternary-1.html (301 von https://www.win.tue.nl/~aeb/codes/ternary-1.html), abgerufen 2026-11-25 (zweimal, zuletzt nach Fund).
- Wörtlicher Eintrag Zeile n=15, lb, d=5: **7929** (ub 29213). Notiz auf der Seite: "A3(14,8) ≥ 123, A3(15,5) ≥ 7929 (Oscar Sanchez, email, 2026-10-17)."
- Frühere Notiz: "A3(15,5) ≥ 7812 (Antti Laaksonen & Patric R. J. Östergård, New Lower Bounds on Error-Correcting Ternary, Quaternary and Quinary Codes, ICMCTA 2017, LNCS 10495)". Obere Schranke 29213: Gijswijt–Schrijver–Tanaka, JCT A 113 (2006).
- Jüngste datierte Notizen der Seite: 2026-11-22 (Meadows). Keine Notiz nach 2026-11-22; 7929 steht unverändert.

## Suche nach neueren Arbeiten
- WebSearch (2026-11-25): "ternary code length 15 minimum distance 5 new lower bound A_3(15,5)", "Laaksonen Östergård new lower bounds ... ternary quaternary quinary 2025 2026": keine Arbeit mit besserer Schranke für A_3(15,5) gefunden (nur Laaksonen–Östergård 2017/2019, Cryptogr. Commun. 11 (2019); Helsinki-Seite https://www.cs.helsinki.fi/u/ahslaaks/codes/ nicht im Detail abgeglichen). arXiv-Treffer 2026 betreffen nur binäre Codes.
- Offen: private E-Mail-Einsendungen an Brouwer (wie Sanchez/Meadows) sind nicht einsehbar; neuer als der Stand der Seite vom 2026-11-25 kann es Unbekanntes geben.

## Konstruktion (Kurzfassung)
Kern C0 = zufälliger linearer [15,6,>=5]_3-Code (Generatormatrix `bestG_3_15_5_k6_8748.npy`, systematisch [I|A]); Code = Vereinigung von 12 Nebenklassen von C0 (12*729 = 8748), deren Syndrome (`best_3_15_5_k6_8748.npy`, Basis-3-Ziffernindex, erstes Element 0) paarweise Differenzen mit Nebenklassengewicht >= 5 haben (Clique im Cayley-Graphen von F_3^9). Werkzeug: `cos2.py`, Erzeugung der Datei: `mk.py`.
