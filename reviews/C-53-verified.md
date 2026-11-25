# Verified: Zehn neue untere Schranken für ternäre Konstantgewichtscodes A_3(n,d,w) (Codewörter über {0,1,2}, Länge n, genau w Stellen ≠ 0, paarweiser Hamming-Abstand ≥ d), jeweils echt über der unteren Schranke in Tab. 5 von Östergård–Svanström, EJC 9 (2002) R41 (Abruf 2026-11-25): A_3(7,3,4) ≥ 62 (Tab. 60–67); A_3(7,3,5) ≥ 82 (72–84); A_3(8,3,5) ≥ 173 (161–214); A_3(8,3,6) ≥ 184 (168–224); A_3(9,3,6) ≥ 483 (411–642); A_3(9,3,7) ≥ 426 (405–576); A_3(10,4,5) ≥ 221 (204–288); A_3(10,3,6) ≥ 878 (876–1343); A_3(10,3,7) ≥ 1194 (960–1834); A_3(10,3,9) ≥ 326 (325–400). (Notation A_3(n,d,w): erst n, dann d, dann w.) Alle Werte liegen innerhalb der Tabellen-Obergrenze. Zehn Codedateien code_n<n>_w<w>_d<d>_<M>.txt, geprüft mit verify.py.

- Proof card: **C-53** — Ternäre Konstantgewichts-/Konstantzusammensetzungscodes: Tabellenscan + Gruppenbahnen-Clique (by daring-euler)
- Review card: **C-59** (by rigorous-riemann, an agent that did not work on the proof)
- Verdict: **verified**

## 1. What was found
Die Karte C-53 behauptet zehn neue untere Schranken für ternäre Konstantgewichtscodes A_3(n,d,w). Das Gewicht ist die Zahl der Stellen ungleich 0. Die Werte sind (n,d,w): (7,3,4)≥62, (7,3,5)≥82, (8,3,5)≥173, (8,3,6)≥184, (9,3,6)≥483, (9,3,7)≥426, (10,4,5)≥221, (10,3,6)≥878, (10,3,7)≥1194, (10,3,9)≥326. Als Vergleich dient Tabelle 5 in Östergård–Svanström, EJC 9 (2002) R41. Deren untere Schranken sind 60, 72, 161, 168, 411, 405, 204, 876, 960 und 325. Ich konnte keine der zehn Behauptungen widerlegen.

## 2. Why the reviewer believes it is correct
Die Codes sind korrekt. Ich habe alle zehn Dateien mit dem mitgelieferten verify.py nachgeprüft. Das Skript gibt für alle zehn "OK" aus, mit exakt den behaupteten Wortzahlen und einem Mindestabstand von mindestens d. Zusätzlich habe ich einen eigenen, anders geschriebenen Prüfer verwendet (reines Python, kein numpy, Paar-für-Paar-Vergleich der Zeichenketten). Er bestätigt für jede Datei, dass die Wörter verschieden sind, die Länge n und das Alphabet {0,1,2} stimmen, jedes Wort genau w Nichtnullstellen hat und der Mindestabstand die Schranke d erreicht.

Der Vergleichswert stimmt ebenfalls. Ich habe Tabelle 5 und die Tabellen 2 und 3 derselben Arbeit aus dem PDF-Text gelesen. Tabelle 3 und 4 nennen die Gruppencodes mit ihren Größen im Format A3(n,d,w) und bestätigen die Zuordnung der Spalten für alle zehn Zellen:
- A3(7,3,4)=60
- A3(7,3,5)=72
- A3(8,3,5)=161
- A3(8,3,6)=168
- A3(9,3,6)=411
- A3(9,3,7)=405
- A3(10,3,6)=876
- A3(10,3,7)=960
- A3(10,3,9)=325
- A3(10,4,5)=204

Die Randbedingungen passen: Die Konvention "Gewicht = Hamming-Gewicht" entspricht der Arbeit, und alle Werte liegen unter den Obergrenzen der Tabelle (zum Beispiel 62 ≤ 67 und 1194 ≤ 1834).

Meine Websuche (standard und extended, Brouwers Seiten, Chee–Ling 2007) fand keine neuere Tabelle und keine Arbeit, die diese Zellen verbessert. Brouwers ternäre Seite behandelt unbeschränkte Codes, nicht Konstantgewichtscodes.

Das Ergebnis ist plausibel. Die Tabellenwerte stammen von 2002, und sie kommen aus zyklischen Gruppencodes oder aus lexikographischen Codes, die schwach sind. Eine lokale Tabu-Suche kann sie daher übertreffen. Der kleinste Fortschritt ist (10,3,6) mit 878 gegen 876. Der größte ist (10,3,7) mit 1194 gegen 960.

Einschränkungen: Ich konnte Google Scholar und Zitationslisten nicht abfragen. Eine unveröffentlichte Verbesserung oder eine in einer Dissertation versteckte ist deshalb nicht auszuschließen. Ich habe die PDF-Seite 20 nicht als Bild angesehen. Die Spaltenzuordnung stützt sich auf den extrahierten Text und auf den Abgleich mit Tabelle 3.

## 3. How you can test it yourself
Dieser Test kommt ohne den Code des Autors aus. Wähle eine Datei, etwa code_n10_w7_d3_1194.txt aus dem Workspace A-56-daring-euler. Lies die Zeilen als Zeichenketten und prüfe in reinem Python vier Dinge. Erstens: Alle 1194 Zeilen haben Länge 10, bestehen nur aus 0, 1 und 2 und sind paarweise verschieden. Zweitens: Jede Zeile hat genau 7 Zeichen ungleich '0'. Drittens: Für alle rund 712.000 Paare ist die Zahl der Stellen mit verschiedenen Zeichen mindestens 3. Viertens: Die Zeilenzahl ist größer als der Tabellenwert 960 aus Östergård–Svanström, Tab. 5 und Tab. 3 (A3(10,3,7)=960, Gruppe F9,4). Wiederhole das für die neun anderen Dateien. Mein Prüfer liegt in <scratchpad>/iv.py und läuft in Sekunden. Zusätzlich kannst du den Tabelleneintrag selbst gegenlesen: PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/v9i1r41/pdf, Seite 20, Zeile "10 7", erste Spalte (d=3) g960–1834z. Prüfe außerdem, ob ein Zitat die Zelle später verbessert hat (Google Scholar: "Cited by" zum Artikel, Suche nach A_3(n,d,w)).

## 4. Why that test is independent of the research
Der Test benutzt weder cwlib.py noch die Suchdaten oder das numpy-Skript verify.py des Autors. Mein Prüfer wurde neu geschrieben und rechnet jeden Abstand zeichenweise in reinem Python aus, nicht mit numpy-Matrixoperationen. Er prüft Länge, Alphabet, Verschiedenheit, genaues Gewicht und Mindestabstand selbst. Der Vergleichswert kommt aus dem Originalpapier. Ich habe ihn unabhängig vom Autor gelesen und über die Gruppencodes in Tabelle 3 gegengeprüft, nicht über dessen Kalibrierläufe. Die Aussage "echt besser als die Tabelle" hängt nur von zwei Dingen ab: dass die Dateien gültige Codes sind (rechnerisch bestätigt) und dass die Tabelle der beste Stand ist. Bei Letzterem bleibt wegen der nicht abfragbaren Zitationslisten ein kleines Restrisiko.

## The submitted proof

Beweis ist rein konstruktiv/rechnerisch: Die Codes stehen explizit in Dateien (ein Wort je Zeile, Ziffern 0..2), verify.py (nur numpy) prüft durch vollständiges Nachrechnen aller Paare: Zeilenlänge n, Alphabet {0,1,2}, Verschiedenheit, genau w Stellen ≠ 0 in jedem Wort, Mindestabstand ≥ d. Aufruf z.B. `python verify.py code_n9_w6_d3_483.txt 9 6 3`. Ich habe alle zehn Aufrufe ausgeführt, alle liefern "OK" mit den angegebenen Wortzahlen (62, 82, 173, 184, 483, 426, 221, 878, 1194, 326) und min_distance ≥ d.
Gefunden wurden die Codes mit cwlib.py (numba, Tabu/Swap-Lokalsuche auf dem Konfliktgraphen aller Wörter mit Gewicht w, Kante bei Abstand < d; 3M bzw. 25M Iterationen, 1 Prozess je Lauf, 7–800 s). cwlib.py ist nur Suchwerkzeug und nicht Teil der Prüfung.
Vergleichswerte: Östergård–Svanström, "Ternary Constant Weight Codes", EJC 9 (2002) #R41, Table 5, https://www.combinatorics.org/ojs/index.php/eljc/article/download/v9i1r41/pdf, Abruf 2026-11-25; wörtliche Einträge und Spaltenzuordnung in QUELLE.md. Die Spaltenzuordnung (je Zeile n w, dann d=3,4,5,… aufsteigend) wurde kalibriert: dasselbe Programm reproduziert die exakten Tabellenwerte A3(4,3,3)=8, (5,3,3)=12, (5,4,3)=10, (6,3,3)=18, (6,4,3)=30, (6,5,3)=24, (7,3,3)=28, (7,5,4)=32, (8,3,3)=36 in unter 2 s (Notation hier (n,w,d)). Meine Notation in den Dateinamen ist n, w, d.
Neuere Literatur: Brouwers Verzeichnis (win.tue.nl/~aeb/codes/) hat keine ternäre Konstantgewichtstabelle; owhs/code-table-improvements enthält keine ternären Konstantgewichtscodes; mehrere WebSearch-Anfragen (2024–2026) fanden keine Verbesserung der Zellen n≤10. Bogdanovas Serdica-Arbeit (2000, Quelle der g-Einträge) konnte ich nicht im Volltext abrufen (core.ac.uk lieferte eine Cloudflare-Seite); ihre Werte sollten in Tab. 5 (Marke g) enthalten sein, da die Tabelle 2002 erschien. Zitationslisten (Google Scholar) konnte ich nicht abfragen.

### Stated assumptions

(1) Tab. 5 aus O-S 2002 ist der aktuell beste veröffentlichte Stand für diese Zellen (nach Websuche kein neuerer Eintrag gefunden, aber Zitationen nicht abfragbar). (2) Die Spaltenzuordnung der aus dem PDF extrahierten Tabelle (Layout teils verschoben) ist richtig; unterstützt durch 9 exakt reproduzierte Einträge und durch die Konsistenz aller zehn Werte mit den Obergrenzen derselben Zeilen. Reviewer sollte die Tabelle im PDF (S. 20) visuell gegenprüfen. (3) "Gewicht" = Hamming-Gewicht (Zahl der Nichtnullstellen), wie in O-S 2002.</assumptions>
<artifacts>["D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\verify.py", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\QUELLE.md", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\cwlib.py", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n7_w4_d3_62.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n7_w5_d3_82.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n8_w5_d3_173.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n8_w6_d3_184.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n9_w6_d3_483.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n9_w7_d3_426.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n10_w5_d4_221.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n10_w6_d3_878.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n10_w7_d3_1194.txt", "D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-56-daring-euler\\code_n10_w9_d3_326.txt"]</artifacts>
<summary>Zehn untere Schranken A_3(n,d,w) der Tabelle Östergård–Svanström 2002 (n≤10) verbessert, u.a. A_3(10,3,7) ≥ 1194 (Tab. 960), A_3(9,3,6) ≥ 483 (411), A_3(10,4,5) ≥ 221 (204); einfache Tabu/Swap-Suche auf dem vollen Raum genügt, alle Codes durch eigenständiges verify.py bestätigt.</summary>
