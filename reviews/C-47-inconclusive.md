# Inconclusive: A_4^GC(12,7,w=6) >= 236: Code der Länge 12 über {0=A,1=T,2=G,3=C}, 236 verschiedene Wörter, jedes mit genau 6 Symbolen in {G,C}, paarweiser Hamming-Abstand >= 7. King/Gaborit-Tabelle (rambutan.umassmed.edu/king/dnacodes.html, Stand 2010-06-23, abgerufen 2026-11-25): Eintrag 183 (Superscript v, Montemanni–Smith 2008). Das Repo owhs/DNA_GC_codes_2026 (2026-10-14) hat diese Zelle unverändert gelassen (183).

- Proof card: **C-47** — A4GC: Gruppenbahn-Clique auf vom Repo unveränderte Zellen (by quiet-mirzakhani)
- Review card: **C-52** (by careful-godel, an agent that did not work on the proof)
- Verdict: **inconclusive**

## 1. What was found
Der Code ist korrekt. Ob 236 den besten veröffentlichten Wert wirklich übertrifft, konnte ich nicht klären.

Was ich nachgerechnet habe:
- Die Datei code_A4GC_12_7_236.txt hat 236 Zeilen zu je 12 Ziffern aus {0,1,2,3}. Es gibt keine Leerzeilen und keine Duplikate. Zeilenende ist CRLF, Leerzeichen gibt es nicht.
- Jedes Wort hat genau 6 Symbole aus {2,3} (G oder C).
- Der kleinste Abstand über alle Paare ist 7. Die Abstände 7 bis 12 kommen vor; 7 tritt 9408-mal auf, gezählt über geordnete Paare.
- Das Skript verify.py des Autors läuft und meldet "OK".
- Mein eigener numpy-Prüfer (nicht aus dem Material des Autors) kommt auf dasselbe Ergebnis.

Der Vergleichswert stimmt mit der Tabelle überein. Ich habe die King/Gaborit-Seite selbst abgerufen (rambutan.umassmed.edu/king/dnacodes.html, "Last updated June 23, 2010"). Die Zeile n=12 der Tabelle A4^GC(n,d,w) lautet: d=3: 118272c, d=4: 29568c, d=5: 3696x, d=6: 1888x, d=7: 183v, d=8: 118v, d=9: 24v. Der Eintrag 183 trägt "v", das steht für Variable-Neighbourhood-Search nach Montemanni–Smith.

Die Lesart w=6 für n=12 ist richtig. Der d=3-Eintrag 118272 ist gleich 924·4096/32, wobei 924 = C(12,6) die Zahl der GC-Positionsmuster und 4096 = 2^12 die Zahl der G/C-Belegungen auf den GC-Stellen und der A/T-Belegungen auf den übrigen Stellen ist. Das passt zu w=6.

Offen bleibt die Neuheit gegenüber der Literatur nach 2010. Die Aufgabe verlangt, den aktuell besten veröffentlichten Wert zu verbessern:
- Montemanni–Smith–Koul 2014 ("Three metaheuristics …", Lecture Notes in Management Science 6) berichtet "many new best-known codes". Die Zahlen habe ich nicht gesehen.
- Aboluion–Smith–Perkins 2012, die Aboluion-Thesis 2011 und Sangroniz–Martínez 2019 konnte ich ebenfalls nicht einsehen.
- Meine Websuchen fanden keinen Wert über 183 für (12,7). Die Suche ist aber ausdrücklich unvollständig.
- arXiv 1505.06262 (Bennenni–Guenda–Gulliver) hat keine Tabelle für diese Zelle.
- Das GitHub-Repo owhs/DNA_GC_codes_2026 hat die Zelle (12,7) nicht angefasst. Das Repo gibt an, dass es Zellen ausgelassen hat, in denen eine spätere Arbeit schon mehr hatte. Das könnte ein Hinweis auf einen späteren höheren Wert sein, ist aber ebenso mit "nie versucht" vereinbar.

Der Autor hat diese Lücke in QUELLE.md selbst offen vermerkt.

## 2. Assessment
Ich halte den Code für korrekt und habe ihn nicht brechen können. Die Aussage "236 Wörter, Länge 12, GC-Gewicht 6, Abstand ≥ 7" ist durch vollständiges Nachrechnen belegt, mit zwei voneinander unabhängigen Prüfern. Die Behauptung, 183 sei der Tabellenwert der King-Tabelle, ist ebenfalls bestätigt.

Der Sprung von 183 auf 236 (+29 %) ist groß, aber nicht unplausibel. Gruppenbahn-Konstruktionen schlagen lokale Suche oft deutlich. Außerdem wäre ein 4-ärer Code der Länge 12 mit Abstand 7 und rund 1000 Wörtern grundsätzlich möglich. Davon hätte ein Anteil von etwa 22 % passendes GC-Gewicht 6, also rund 230 Wörter. Das ist nur eine Plausibilitätsüberlegung, nicht gerechnet.

Zwei Dinge hindern mich, "verified" zu sagen:
1. Die Neuheit gegenüber der Literatur nach 2010 ist nicht geklärt (siehe oben). Die Tabelle vom Juni 2010 ist 16 Jahre alt, und mehrere spätere Arbeiten haben genau diese Tabellen verbessert. Wenn dort ein Wert ≥ 236 steht, wäre das kein neuer Rekord, der Code bliebe aber gültig.
2. Der Autor hat sich auf die Tabellenseite von 2010 und auf das Repo verlassen. Ich habe nur die Tabellenseite und die Websuche geprüft. Die Primärquellen von 2011 bis 2019 hat keiner von uns gelesen.

Der Code ist ein sauberes Ergebnis. Als Rekordverbesserung im Sinne der Aufgabe ist er erst belegt, wenn die Aboluion-Thesis, Aboluion–Smith–Perkins 2012, Montemanni–Smith–Koul 2014 und Sangroniz–Martínez 2019 keinen Wert ≥ 236 für (n=12, d=7, w=6) enthalten.

## 3. How you can test it yourself
Die Prüfung des Codes und die Prüfung der Neuheit sind zwei getrennte Schritte.

1. Code prüfen. Eigenes Skript schreiben, das nur code_A4GC_12_7_236.txt liest. Zeilen am Zeilenende trennen. Dann prüfen: genau 236 verschiedene Zeilen, jede mit 12 Zeichen aus {0,1,2,3}, in jeder Zeile genau 6 Zeichen aus {'2','3'} und für alle Paare mindestens 7 Stellen mit verschiedenen Zeichen. Mit numpy: Matrix A (236×12), D = (A[:,None,:] != A[None,:,:]).sum(2), Diagonale ausnehmen, D.min() ≥ 7. Das dauert Sekunden. Erwartet: Mindestabstand 7, Abstandsverteilung (geordnete Paare) 7:9408, 8:11592, 9:14528, 10:10176, 11:6912, 12:2844.

2. Neuheit prüfen. Von Hand in die vier Quellen schauen und den Eintrag für n=12, d=7 ablesen:
 - Aboluion, Smith, Perkins, Discrete Mathematics 312 (2012);
 - Aboluion, Doktorarbeit, University of South Wales, 2011;
 - Montemanni, Smith, Koul, Lecture Notes in Management Science 6 (2014), S. 167–175;
 - Sangroniz, Martínez (2019).
 Dazu die Tabelle bei rambutan.umassmed.edu/king/dnacodes.html noch einmal ansehen, ob der Eintrag 183 dort steht. Steht in einer Quelle ein Wert ≥ 236, ist die Rekordaussage widerlegt. Steht überall höchstens 183, ist die Aussage bestätigt.

## 4. Why that test is independent of the research
Prüfschritt 1 benutzt weder verify.py noch rnd.py, orb.py oder die Gruppenerzeuger des Autors. Er liest nur die fertige Wortliste und rechnet Länge, Verschiedenheit, GC-Gewicht und Abstand mit eigenem Code nach. Ich habe ihn selbst so ausgeführt. Er hängt auch nicht davon ab, wie der Code gefunden wurde.

Prüfschritt 2 stützt sich nicht auf die Suchen oder Zusammenfassungen des Autors, sondern auf die gedruckten Tabellen der Originalarbeiten. Die King-Tabelle habe ich selbst abgerufen. Die vier späteren Arbeiten konnte ich nicht lesen. Deshalb bleibt mein Urteil "inconclusive" und nicht "verified".

## The submitted proof

Dateien in D:\CodingTheory_Research\.wwresearch\workspaces\A-50-quiet-mirzakhani: code_A4GC_12_7_236.txt (236 Zeilen, Ziffern 0..3), verify.py (reines Python, prüft Länge 12, Ziffernformat, Verschiedenheit, GC-Gewicht = 6 je Wort, Mindestabstand über alle Paare; Aufruf `python verify.py`, Ausgabe "Woerter 236 ... Mindestabstand 7 / OK", Laufzeit Sekunden), QUELLE.md (Tabelleneintrag, Abrufdatum, Literatursuche). Konstruktion: Gruppe G der Ordnung 48, erzeugt von (a) globalem Klassentausch A<->G, T<->C und (b) einer Koordinatenpermutation mit Symbolabbildung (2 3 1 0) auf allen Koordinaten (genaue Erzeuger: rbest_12_7_s1.json); alle Elemente erhalten Hamming-Abstand und GC-Gewicht 6 (n=12, Klassentausch bildet 6 auf 12-6=6 ab). Es wurden die 7458 selbstverträglichen G-Bahnen (innerer Abstand >= 7) bestimmt, ihre Verträglichkeitsmatrix berechnet und mit gewichtetem Tabu-Clique (orb.py/rnd.py, Gruppen zufällig gezogen, ~4 min) eine Bahnvereinigung der Größe 236 gefunden. Reproduktion der Suche: `NUMBA_NUM_THREADS=1 python rnd.py 12 7 12 8 120 1 20000` (Zufallsgruppen, Ergebnis seed-abhängig). Der Code selbst ist unabhängig von der Suche per verify.py prüfbar. Grenzen: (1) Literatur nach 2010: Das Repo nennt Aboluion-Thesis 2011/Aboluion–Smith–Perkins 2012, Montemanni–Smith–Koul 2014, Sangroniz–Martinez 2019 als geprüft und hat (12,7) unverändert gelassen; meine eigenen Websuchen fanden keinen Wert > 183, die Volltexte/Tabellen konnte ich nicht einsehen – ein späterer größerer Wert ist nicht ausgeschlossen (in QUELLE.md vermerkt). (2) Lesart der Tabelle als w=n/2=6 (wie Repo, w=floor(n/2)); falls die Tabelle für (12,7) ein anderes w meint, gilt der Vergleich nicht. Weitere Läufe: (12,7) andere Seeds nur 176-208 (Gruppenwahl entscheidet), (12,8) 88 vs 118 und (11,6) 246 vs 472 nicht nahe; (8,6)=28, (9,7)=18 gleich Tabelle, (8,5)=62 vs 63. Die 17 GC-Codes des Repos (n=7..13) wurden zusätzlich mit eigenem numpy-Prüfer (vrepo.py) bestätigt (alle OK).
