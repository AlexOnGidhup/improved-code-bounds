# QUELLE.md – A_4^GC(12,7), w = 6

## Verglichene Tabelle
- URL: https://rambutan.umassmed.edu/king/dnacodes.html (Gaborit/King, "Lower bounds for A_4^GC(n,d,w)"), Stand der Tabelle 2010-06-23, abgerufen 2026-11-25 (lokal: ../A-48-tidy-franklin/king.html, king.txt).
- Wörtlicher Eintrag Zeile n=12, Spalte d=7: `183 v` (v = Variable-Neighbourhood-Search aus Montemanni & Smith, J. Math. Model. Algorithms 7(3), 311–326 (2008) bzw. MIC 2009).
- Tabellenkonvention: konstanter GC-Gehalt w = n/2 (für n=12: w=6); Hamming-Abstand >= d; Symbole {G,C} zählen als Gewicht.

## Suche nach neueren Arbeiten (2026-11-25)
- GitHub owhs/DNA_GC_codes_2026 (2026-10-14): 39 Verbesserungen gegenüber der King-Tabelle; Zelle (12,7) ist dort NICHT enthalten (unverändert 183). Die Repo-Codes (17 GC-Codes) wurden von mir mit eigenem Prüfer bestätigt (vrepo.py), darunter keine für n=12,d=7. Das Repo nennt als geprüfte Literatur Chee–Ling 2008, Montemanni–Smith 2008/2009, Aboluion-Thesis 2011 / Aboluion–Smith–Perkins (Discrete Math. 312, 2012), Montemanni–Smith–Koul 2014, Sangroniz–Martinez 2019; "Zellen, in denen eine spätere Arbeit schon einen größeren Code hatte, wurden ausgelassen".
- Eigene Websuchen (Standard-Modus, 2 Anfragen) nach "A_4^GC(12,7)", Montemanni–Smith–Koul, Aboluion, neueren Tabellen: kein Treffer mit einem Wert > 183 für (12,7) gefunden; Einsicht in die Originalarbeiten von 2012/2014/2019 nicht möglich (Volltext nicht abgerufen). **Das ist eine Lücke: ein späterer Wert > 183 in der Thesis von Aboluion (2011) oder bei Montemanni–Smith–Koul (2014) ist nicht ausgeschlossen.**

## Ergebnis
- Code: `code_A4GC_12_7_236.txt` – 236 Wörter der Länge 12 über {0,1,2,3} (0=A,1=T,2=G,3=C), GC-Gewicht 6, Mindestabstand 7; `python verify.py` bestätigt (volles Paarweises Nachrechnen, reines Python).
- Konstruktion: Vereinigung von Bahnen einer Gruppe der Ordnung 48 aus Koordinatenpermutationen mal Symbolabbildungen (globaler Klassentausch A<->G, T<->C sowie ein zweiter Erzeuger aus einer Koordinatenpermutation mit Symbolabbildung (2 3 1 0) auf allen Koordinaten); genaue Erzeuger in `rbest_12_7_s1.json`; gewichtete Clique (Tabu) auf 7458 selbstverträglichen Bahnen (orb.py, rnd.py).
