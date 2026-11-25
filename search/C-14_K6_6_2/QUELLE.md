# QUELLE.md – K_6(6,2) <= 216

Behauptung: Überdeckungscode über Z_6, Länge 6, Radius 2, 216 Wörter (`code_K6_6_2_216.txt`);
Prüfung: `python verify.py code_K6_6_2_216.txt 6 2` (prüft alle 6^6 Wörter, Ergebnis Radius 2, OK).

## Verglichene Tabelle
- Kéri, "Tables for bounds on covering codes", `https://old.sztaki.hu/~keri/codes/6-21_tables.pdf` (.ps, Datei vom 2009-10-15, Abruf 2026-11-25).
  Eintrag q=6, n=6, R=2 wörtlich: `m 133–274 q` (untere Schranke Haas–Halupczok–Schlage-Puchta 2009; obere Schranke 274 Rivas Soriano 2005–2008, im Index vermerkt als "K6(6,2)<=274" vom 2006.08.30).
- Gegenprobe: `https://raw.githubusercontent.com/Mapika/coldcase/refs/heads/master/cov/bounds.json` (Abruf 2026-11-25): K_6(6,2) lb 133, ub 274 (Keri 2011, "frozen").

## Suche nach neueren Arbeiten (2026-11-25)
- Kéri-Indexseite: letzte Notiz 2011.11.21, keine spätere Notiz zu q=6.
- Marosi, arXiv:2608.19872 v3 (Sep 2026): Tabelle 1 (neue obere Schranken) enthält keine Zeile q=6, R=2; Tabelle 2 nur untere Schranken K6(8,2), K6(9,2).
- Florath, arXiv:2606.09600 (Lean 4): keine neuen Schranken, kein K6(6,2).
- Web-Suche "K_6(6,2)": kein Treffer. Keine neuere obere Schranke als 274 gefunden.
Grenzen: unrefereed Preprints, keine Volltextsuche in Google Scholar möglich; Lobsteins Bibliographie (bib-a-jour.pdf) nicht geprüft.

## Konstruktion
Matrixmethode über dem Z_6-Modul: C = { x in Z_6^6 : H x in S }, H eine 4x6-Matrix über Z_6, S eine Menge von 6 Syndromen
in Z_6^4; |C| = |S| * |ker H| = 6*36 = 216. C überdeckt mit Radius 2 genau dann, wenn S + {Syndrome der Wörter vom Gewicht <=2} = Z_6^4.
Gefunden mit simulated annealing über (H,S) (`mm.py`, ~1 Min, 1 Kern).
