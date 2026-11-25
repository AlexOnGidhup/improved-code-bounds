# QUELLE.md – K_7(9,4) <= 1372

Behauptung: Es gibt einen septenären Überdeckungscode der Länge 9 mit Radius 4 und 1372 verschiedenen Wörtern
(`code_K7_9_4_1372.txt`, Ziffern 0..6). Prüfung: `python -I verify.py code_K7_9_4_1372.txt 7 9 4`
(markiert die Radius-4-Kugel um jedes Codewort in einer Tabelle aller 7^9 Wörter, prüft Länge, Alphabet, Verschiedenheit, 0 ungedeckt).

## Verglichene Tabellen
- G. Kéri, "Tables for bounds on covering codes", http://old.sztaki.hu/~keri/codes/ , Datei 6-21_tables.pdf (Kopie
  workspaces/A-3-eager-fermat/tables/6-21_tables.txt, Abruf 2026-11-25). Wörtlich: Bounds on K7(n,R), n=9, R=4: `m 264–1843 f`
  (obere Schranke 1843 aus Regel f: K_q(n+1,R+1) <= K_q(n,R); untere Schranke Haas–Schlage-Puchta–Quistorff).
- Marosi, "New upper and lower bounds on covering codes K_q(n,R) for alphabets of size 5<=q<=21", arXiv:2608.19872 v3 (2.9.2026),
  Table 1: K7(9,4) <= 1475 (alt 1843, Methode lokale Suche). Das ist der neueste mir bekannte Stand; 1372 < 1475 < 1843.
- Kontrolle: github.com/Mapika/coldcase cov/bounds.json (Kéri-Stand 2011, ub 1843).

## Suche nach neueren Arbeiten (2026-11-25)
- arXiv:2608.19872 (Marosi) enthält K7(9,4)<=1475 als letzten Stand; Gijswijt–Polak arXiv:2504.01932 behandelt nur untere Schranken, q<=5;
  Florath arXiv:2606.09600 (Lean) ohne neue Schranken (laut Angabe anderer Karten, A-17/A-4 QUELLE.md). Keine Arbeit mit besserer oberer
  Schranke für K7(9,4) gefunden. Grenzen: unbegutachtete Preprints, kein Google Scholar, Volltext von Marosi nur über Unteragent-Bericht gelesen.

## Konstruktion
Matrixmethode über Z_7: C = { x in Z_7^9 : [I_6 | D] x in S }, D eine 6x3-Matrix über Z_7, S eine Menge von 4 Syndromen in Z_7^6,
|C| = 4 * 7^3 = 1372. C hat Radius <= 4 genau dann, wenn S + {Syndrome der Fehler vom Gewicht <= 4} = Z_7^6.
Gefunden durch exakte Best-Response-Iteration (FFT-Korrelation auf Z_7^6) + Zufallsänderungen von D (fftmm.py, < 5 s).
Dateien: run/fftmm.py, run/fm_q7n9R4r6_D.txt, run/fm_q7n9R4r6_S.txt, run/expand2.py (Expansion zu Codewörtern).
