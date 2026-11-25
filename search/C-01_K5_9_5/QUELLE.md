# QUELLE.md – Vergleich für K5(9,5) ≤ 50

Behauptung: K_5(9,5) ≤ 50 (quinäres Überdeckungscode, Länge 9, Radius 5, 50 Wörter).
Datei: `code_K5_9_5_50.txt`, Prüfung: `python -I verify.py code_K5_9_5_50.txt 5 9 5` (ca. 3 s).

## Verglichene Tabelle
- G. Kéri, "Tables for Bounds on Covering Codes", https://old.sztaki.hu/~keri/codes/index.htm,
  Datei `4-5_tables.pdf` (Bounds on K5(n,R)), Stand der Tabelle 2011-11-21, abgerufen 2026-11-25
  (Rohtext: `../A-3-eager-fermat/tables/4-5_tables.txt`, Zeile "9 m 64–255 d | m 19–55 d | k 10–12 q | 5471 | 5").
- Wörtlicher Eintrag K5(9,5): **19–55**, obere Schranke mit Schlüssel **d = (Bhandari–Durairajan, 1996)**,
  untere Schranke Schlüssel m = (Haas–Schlage-Puchta–Quistorff 2008/2009).
- Nachbarn zur Einordnung: K5(8,4) 25–65 (d); K5(9,4) 64–255 (d); K5(9,6) 10–12 (k, "using known bound for smaller q").

## Suche nach neueren Arbeiten (2026-11-25)
- Marosi, "New upper and lower bounds on covering codes K_q(n,R) for alphabets of size 5 ≤ q ≤ 21",
  arXiv:2608.19872 (v1 20.8.2026, v3 2.9.2026), https://arxiv.org/abs/2608.19872. Nach dieser Arbeit sind seit Kéri 2011 die
  ersten Verbesserungen oberer Schranken für q≥5 erschienen. Ein Subagent hat die HTML-Fassung v3 vollständig gelesen
  (Tabellen 1–5, Anhänge A–C, Literatur) und die Liste der 88 Ancillary-Dateien: **keine Zeile und kein Text zu K5(9,5)**;
  das einzige q=5-Feld in Table 1 ist K5(11,5)≤602; Ancillary-Datei nur `K5_11_5_M602.txt`.
  (Subagent-Bericht, nicht selbst gelesen; das README der Ancillary-Dateien wurde nicht gelesen.)
- Florath, arXiv:2606.09600 (Lean-4-Formalisierung für q-äre Überdeckungscodes): nach Abstract keine neuen Schranken.
- Websuche (WebSearch, "K_5(9,5) upper bound covering codes quinary 2012..2026"): kein Treffer, der K5(9,5) verbessert.
- Nicht prüfbar geblieben: das von Marosi genannte GitHub-Repository https://github.com/Mapika/coldcase (maschinenlesbare
  Zusammenführung). Der Abruf per Subagent ist am Turn-Limit gescheitert, Inhalt NICHT gesehen.
  Ebenfalls nicht geprüft: Google Scholar, Kéris aktuelle Seiten nach 2011 außer dem oben genannten Stand.

## Erzeugung
Matrixmethode: Code = {x in Z_5^9 : [I_8 | D] x in S}, D = (3,4,1,4,2,3,3,2)^T (Spalte), |S| = 10 Syndrome in Z_5^8,
|C| = 10·5 = 50. Suche: Simulated Annealing über S (Skript `run/mm_cover.py`, Seed 5, T 3→0.8, 157 s).
Dateien: `run/S_q5n9R5r8_m10_s5.txt`, `run/D_q5n9R5r8_m10_s5.txt`, Expansion `run/expand.py`.
Die Prüfung `verify.py` importiert nichts aus der Suche.
