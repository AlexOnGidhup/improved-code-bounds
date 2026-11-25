# QUELLE.md – K_6(7,3) <= 216, K_6(9,3) <= 3888, K_6(10,3) <= 15552

Dateien (dieses Verzeichnis): code_K6_7_3_216.txt, code_K6_9_3_3888.txt, code_K6_10_3_15552.txt, verify.py
Prüfung: `python verify.py code_K6_7_3_216.txt 6 3`  (ebenso für die beiden anderen; Laufzeit je < 5 s, nur numpy;
Dilationsverfahren: Indikatorfeld auf Z_6^n, R-mal Hamming-Radius-1-Dilatation, zählt unüberdeckte Wörter; Negativkontrolle: c6_2_216_src.txt mit R=1 -> FEHLER).

## Verglichene Tabelle (Abruf 2026-11-25)
Kéri, "Tables for bounds on covering codes", https://old.sztaki.hu/~keri/codes/6-21_tables.pdf (Stand 2009; Index bis 2011-11-21):
- K6(7,3):  `m 70–246 e`   (R=3, n=7)
- K6(9,3):  `y 921–4752 f` (R=3, n=9)
- K6(10,3): `y 3815–19347 k` (R=3, n=10)
Neuere Arbeit: Marosi, arXiv:2608.19872 v3 (2026-09-02), Table 1: K6(7,3) <= 227 (vorher 246). K6(9,3) und K6(10,3) stehen dort NICHT in Table 1 (obere Schranken unverändert 4752 / 19347; nur untere Schranken verbessert: 926, 3836).
Suche nach weiteren neueren Arbeiten (WebSearch 2026-11-25): keine neuere obere Schranke für K6(7,3), K6(9,3), K6(10,3) gefunden (Treffer: Marosi; Lean-4-Arbeit arXiv:2606.09600 ohne neue Schranken; Shapiro 2605.19094, Ta-Vu 2606.29236 asymptotisch). Grenze: Google Scholar/Lobstein-Bibliographie nicht durchsucht.

## Konstruktion
1. Baustein A: K6(6,2) <= 216 (Board C-14/F-22, verifiziert durch C-18; Matrixmethode über Z_6, Datei c6_2_216_src.txt = Kopie von workspaces/A-17-stubborn-franklin/code_K6_6_2_216.txt, verify.py bestätigt Radius 2). Tabelle Kéri: 133–274.
2. (7,3): C x {0}: (n+1,R+1) <= K(n,R). 216 Wörter.  (Marosi 227, Kéri 246.)
3. (9,3): Direkte Summe K6(3,1) x K6(6,2): Baustein B = 18 Wörter Länge 3 Radius 1 (c3_1_18.txt, Matrixmethode Z_6, m=2,s=3, mm.py aus C-14, 4 s; Tabelle `g 18 g`). 18*216 = 3888.
4. (10,3): K6(4,1) x K6(6,2): Baustein C = 72 Wörter Länge 4 Radius 1 (c4_1_72.txt, Matrixmethode m=2,s=2, 4 s; Tabelle `i 72 i`). 72*216 = 15552.
Regelabschluss (closure.py/closure6.py): Kéri-q=6-Tabelle + Marosi Table 1 sind ohne die 216 unter Monotonie, n+1->q*K, (n+1,R+1), direkter Summe abgeschlossen (0 Verbesserungen); mit K6(6,2)=216 ergeben sich genau diese drei.
Binär (n<=33,R<=10), ternär (n<=14,R<=8), q=5 (n<=11): ebenfalls abgeschlossen, keine Verbesserung (auch mit K5(9,5)<=50 aus C-1).
