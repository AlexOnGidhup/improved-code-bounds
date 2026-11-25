# QUELLE: K_7(5,1) <= 766 (vorher Tabelle: 769)

Vergleichstabelle: G. Kéri, "Tables for bounds on covering codes", Kéri-Tabelle q=6..21,
https://old.sztaki.hu/~keri/codes/6-21_tables.pdf (abgerufen 2026-11-25; eigene Kopie in dl/6-21_tables.pdf).
Wörtlicher Eintrag Bounds on K7(n,R), Zeile n=5, Spalte R=1: "r 606–769 l"
(untere Schranke 606 Marke r = Nichtexistenz perfekter Code; obere Schranke 769 Marke l = Regel
K_{tq}(n,1) <= t^{n-1} K_q(n,1), also eine abgeleitete Schranke, keine direkte Suche).
Tabellenstand laut Kéri/Marosi: 2009–Nov. 2011.

Suche nach neueren Arbeiten (2026-11-25):
- Marosi, arXiv:2608.19872 v3 (5<=q<=21, Table 1 mit 26 neuen oberen Schranken): enthält KEINE R=1-Zeile
  (alle R>=2); K7(5,1) wird nicht verbessert.
- Gijswijt/Polak SDP (arXiv 2025) betrifft untere Schranken.
- WebSearch nach "K_7(5,1) 769" fand keine neuere obere Schranke. (Kein Nachweis, dass keine existiert.)

Ergebnis: code_K7_5_1_766.txt, 766 verschiedene Wörter der Länge 5 über {0..6}, Überdeckungsradius 1.
Prüfung: python verify.py code_K7_5_1_766.txt 7 5 1  -> size=766 uncovered=0.
