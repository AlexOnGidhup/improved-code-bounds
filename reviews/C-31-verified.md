# Verified: K_7(5,1) <= 766: expliziter septenärer Überdeckungscode der Länge 5, Radius 1, mit 766 verschiedenen Wörtern (jedes der 16807 Wörter in {0..6}^5 hat Hamming-Abstand <= 1 zu einem Codewort). Beste veröffentlichte obere Schranke laut Kéri-Tabelle (6-21_tables.pdf, abgerufen 2026-11-25): 769 (Eintrag "r 606–769 l", Marke l = abgeleitete Regel K_tq(n,1)<=t^(n-1)K_q(n,1)).

- Proof card: **C-31** — Überdeckung R=1 über q=5,6,7 (n=4..6): Bahnen unter affiner Gruppe + Tabu-Mengenüberdeckung (by gentle-fermat)
- Review card: **C-33** (by curious-hopper, an agent that did not work on the proof)
- Verdict: **verified**

## 1. What was found
Die Karte C-31 behauptet K_7(5,1) <= 766. Gemeint ist ein Überdeckungscode über dem Alphabet {0..6} mit Länge 5 und Radius 1. Die Tabelle von Kéri nennt als beste bekannte obere Schranke 769. Die Datei code_K7_5_1_766.txt enthält 766 Wörter. Ich habe sie mit drei eigenen Methoden geprüft: Sie sind alle verschieden, haben Länge 5 und nur Ziffern 0..6, und jedes der 16807 Wörter liegt höchstens Abstand 1 von einem Codewort entfernt. Die Behauptung stimmt. Der Code verbessert den Tabelleneintrag um 3. Ein Fehler steckt in QUELLE.md: Die Marke "l" bedeutet laut Legende der Tabelle "Konstruktionen mit adjungierten Codes". Die Regel t^(n-1)·K_q(n,1) trägt die Marke "j". Das ändert weder den Wert 769 noch das Ergebnis.

## 2. Why the reviewer believes it is correct
Prüfung des Codes (alles mit eigenem Code, nicht mit verify.py des Autors):
1. chk.py (reines Python, ohne numpy) zählt die Vereinigung aller Kugeln vom Radius 1 um die Codewörter. Ergebnis: 766 Zeilen, 766 verschiedene Wörter, 16807 von 16807 Wörtern überdeckt. Es gibt keine Nicht-ASCII-Bytes. Die Datei hat 5362 Bytes, das sind 766·7 = 5362 mit Zeilenumbruch, also keine versteckten Zeichen.
2. Ein unabhängiger Brute-Force-Test (Mindestabstand jedes Wortes in {0..6}^5 zu allen 766 Codewörtern) fand 0 unüberdeckte Wörter.
3. verify.py des Autors lief ebenfalls durch und gab "size=766 ... uncovered=0". Das Skript ist inhaltlich korrekt: Es prüft Länge, Alphabet und Verschiedenheit und rechnet den Mindestabstand für alle Wörter vollständig nach.
Plausibilität: Die Kugelüberdeckungsschranke ist 16807/31 = 542,2. Die Tabelle gibt als untere Schranke 606. 766 liegt darüber, also ist kein Widerspruch zu bekannten unteren Schranken da.

Prüfung des Vergleichsstands:
- Ich habe 6-21_tables.pdf von old.sztaki.hu selbst geladen (abgerufen 2026-11-25) und den Text extrahiert. Der Eintrag lautet "Bounds on K7(n,R), n=5, R=1: r 606–769 l". Das passt zu QUELLE.md.
- Kéris Indexseite listet als letzte Änderung den 21.11.2011. Die Kéri-Tabelle ist also nicht neuer als 2011.
- Marosi (arXiv:2608.19872 v3, Sept. 2026) schreibt: "Für q>=6 kennen wir keine veröffentlichte Verbesserung seit 2011, und auf der oberen Seite keine für q>=5". Ich habe den Volltext nach K7(5,1) und R=1 durchsucht. Es gibt keinen Eintrag, der 769 verbessert.
- Meine Websuche fand keine neuere Arbeit mit einer besseren oberen Schranke für K_7(5,1).
Restunsicherheit: Ein Fehlen in der Websuche beweist nicht, dass es keine Verbesserung gibt. Zum Beispiel könnte eine unveröffentlichte oder schlecht indizierte Arbeit 766 oder weniger bereits kennen. Der Autor räumt das selbst ein. Das ändert aber nichts an der Richtigkeit des Codes. Es betrifft nur die Frage, ob 766 gegen den neuesten Stand neu ist. Nach Tabelle und Marosi-Überblick ist es neu.
Formale Anforderungen: code-Datei, verify.py und QUELLE.md sind vorhanden. Bei QUELLE.md ist nur die Deutung der Marke "l" falsch.

## 3. How you can test it yourself
1. Datei laden: D:\CodingTheory_Research\.wwresearch\workspaces\A-34-gentle-fermat\code_K7_5_1_766.txt.
2. Mit einem selbst geschriebenen Skript lesen: je Zeile 5 Ziffern aus 0..6, 766 Zeilen, alle verschieden.
3. Für jedes der 7^5 = 16807 Wörter den kleinsten Hamming-Abstand zu allen 766 Codewörtern ausrechnen und prüfen, dass er höchstens 1 ist. Dauer: Sekunden bis eine Minute in reinem Python.
4. Alternativ das Bälle-Verfahren: Für jedes Codewort das Wort selbst und alle 30 Wörter, die sich an genau einer Stelle unterscheiden, in eine Menge legen. Die Menge muss genau 16807 Elemente haben.
5. Vergleichswert selbst nachlesen: https://old.sztaki.hu/~keri/codes/6-21_tables.pdf, Seite "Bounds on K7(n,R)", Zeile n=5, Spalte R=1, Eintrag 606–769.
6. Neuere Arbeiten selbst suchen: arXiv-Suche nach "covering codes q=7" und "K_7(5,1)", Kéri-Seite auf neuere Änderungen prüfen, und Marosi arXiv:2608.19872 nach R=1 durchsehen.

## 4. Why that test is independent of the research
Die Prüfung nutzt weder den Suchcode (fls.py) noch verify.py des Autors noch dessen Zwischenstände. Sie braucht nur die Codewörter als Daten. Die Überdeckungseigenschaft ist eine reine Zähleigenschaft: Entweder deckt jedes Wort ab oder nicht. Mein chk.py nutzt die Kugelvereinigung statt Abstandsmatrix und kommt ohne numpy aus. Der Brute-Force-Test ist ein dritter, davon unabhängiger Weg. Der Vergleichswert 769 stammt aus der von mir selbst geladenen Originaltabelle, nicht aus dem Bericht des Autors. Die Ausschlusssuche nach neueren Arbeiten stützt sich auf Marosis eigene Literaturübersicht und eine eigene Websuche.

## The submitted proof

Konstruktiv, kein Beweis im klassischen Sinn: Der Code steht in code_K7_5_1_766.txt (766 Zeilen, Ziffern 0..6). Prüfung: verify.py (nur numpy) liest die Datei, prüft Länge 5, Alphabet, Verschiedenheit und berechnet für alle 7^5=16807 Wörter den Mindestabstand zu den Codewörtern (voll durchgerechnet); Ausgabe 'size=766 q=7 n=5 R=1 uncovered=0'. Aufruf: python verify.py code_K7_5_1_766.txt 7 5 1. Gefunden mit fls.py (numba, fokussierte Tabu-Lokalsuche: zufälliges unüberdecktes Wort wählen, Codewörter im Abstand 2 um eine Koordinate zu ihm hinbewegen, bestes Ergebnis wählen) in rund 1 Min auf einem Kern; Schrittfolge 820 -> 769 (Gleichstand) -> 767 -> 766, Zwischenstände c_7_5_*.txt. Vergleich mit Literatur in QUELLE.md: Kéri-Tabelle (Stand 2009/2011); Marosi arXiv:2608.19872 v3 hat keine R=1-Zeilen; eine Websuche fand keine neuere obere Schranke für K7(5,1) (das beweist nicht, dass keine existiert, z. B. ein neuerer Kéri-Stand oder eine Arbeit, die die Websuche nicht fand). Nebenergebnisse: Gleichstände K7(4,1)<=123, K5(5,1)<=184 und K5(4,1)<=51 (letzteres über Gruppenlöser grp.py, Datei g_5_4_51_s1.txt); K6(5,1) nur 434 gegen 414.

### Stated assumptions

Die Kéri-Tabelle (Datei 6-21_tables.pdf, Eintrag K7(5,1)=606–769) ist der aktuelle Vergleichsstand; ich habe keine neuere Kéri-Version und keine Arbeit gefunden, die 769 verbessert, aber nur per Websuche gesucht. Der Reviewer sollte QUELLE.md gegen die Live-Tabelle und gegen Marosi (R=1) gegenprüfen.</assumptions>
<parameter name="artifacts">["D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-34-gentle-fermat\\code_K7_5_1_766.txt","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-34-gentle-fermat\\verify.py","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-34-gentle-fermat\\QUELLE.md","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-34-gentle-fermat\\fls.py"]
