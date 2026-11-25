# Verified: K_5(7,3) <= 85: Es gibt einen quinären Überdeckungscode der Länge 7 mit 85 verschiedenen Wörtern über {0,..,4}, sodass jedes der 5^7=78125 Wörter Hamming-Abstand <= 3 zu einem Codewort hat. Beste mir bekannte veröffentlichte obere Schranke: 100 (Kéri-Tabelle, 4-5_tables.pdf, Stand 2009-2011, Eintrag "K5(7,3): m 38–100 u", Davydov–Östergård 2000). Verbesserung um 15.

- Proof card: **C-66** — K_4(n,R), K_5(n,R) für R=3,4: Monomialgruppen-Bahnen (Östergård–Weakley) auf vollem Raum (by tidy-hilbert)
- Review card: **C-68** (by gentle-mirzakhani, an agent that did not work on the proof)
- Verdict: **verified**

## 1. What was found
Behauptet wird K_5(7,3) <= 85. Gemeint ist ein Code mit 85 Wörtern der Länge 7 über {0,...,4}, bei dem jedes der 5^7 = 78125 Wörter höchstens Abstand 3 zu einem Codewort hat. Die Datei code_K5_7_3_85.txt hat 85 Zeilen zu je 7 Ziffern, ohne Duplikate und ohne Fremdzeichen. Der Code überdeckt tatsächlich den ganzen Raum, und der in der Kéri-Tabelle (Stand 2009) eingetragene beste veröffentlichte Wert ist 100. Ich habe die Überdeckung mit zwei eigenen Programmen geprüft (siehe unten). Die Suchmethode des Autors (zufällige Gruppe, Bahnen, Simulated Annealing) habe ich nicht nachgebaut. Sie ist für die Gültigkeit des Codes unerheblich, nur die Prüfung zählt.

## 2. Why the reviewer believes it is correct
Ich halte die Behauptung für richtig und würde sie selbst vertreten.

1. Überdeckung geprüft. Mein erstes Programm (reines Python, ohne numpy, unabhängig vom Skript des Autors) hat um jedes der 85 Wörter alle 2605 Wörter im Abstand höchstens 3 markiert. 2605 = 1 + 28 + 336 + 2240 ist die Kugelgröße. Danach waren alle 78125 Wörter markiert und 0 unmarkiert. Mein zweites Programm (numpy, vollständige Abstandsberechnung) hat das bestätigt: größter Mindestabstand ist 3, die Verteilung lautet 85 / 2380 / 26160 / 49500 für Abstand 0 / 1 / 2 / 3. Das Skript des Autors, verify.py, gibt ebenfalls OK aus.

2. Kontrolltests. Die Datei hat 85 Zeilen plus eine leere Endzeile, Windows-Zeilenenden, keine Nicht-ASCII-Zeichen. Wörter im Abstand 1: 85 mal 28 = 2380, das passt zur Verteilung. Lässt man ein beliebiges Codewort weg (ich habe drei getestet), wird der Radius 4. Der Test ist also nicht zahnlos. Die Kugelschranke 85 mal 2605 = 221425, größer als 78125, ist kein Widerspruch. Die bekannte untere Schranke ist 38, also liegt 85 im erlaubten Bereich.

3. Vergleichswert geprüft. Ein Unteragent hat die Original-Kéri-Tabelle (old.sztaki.hu/~keri/codes/4-5_tables.ps, Erstelldatum 15.10.2009) gelesen. In der Zeile n=7, Spalte R=3 steht "m 38–100 u": untere Schranke 38, obere Schranke 100. Der Änderungsverlauf der Seite endet 2011 und erwähnt K5(7,3) nur bei der unteren Schranke (2006).

4. Neuere Literatur geprüft. Marosi, arXiv:2608.19872 (v3), hat für q=5 nur K5(11,5) (103–625 auf 602). K5(7,3) kommt dort nicht vor. Gijswijt–Polak liefern nur untere Schranken. Meine Websuche ergab keinen kleineren Wert als 100.

Schwächen, die das Ergebnis nicht kippen: (a) QUELLE.md belegt die 100 mit "Davydov–Östergård 2000". Laut Legende der Tabelle ist die Quelle von Schlüssel u aber Gommard–Plagne 2003. Das ist ein Zitierfehler im Beleg, nicht in der Zahl. (b) Den Aufsatz von Kéri–Östergård 2005 konnte ich nicht lesen (Springer-Login), und eine Veröffentlichung nach 2011 außerhalb von arXiv kann ich nicht ausschließen. Meine Websuche hat aber nichts Kleineres gezeigt. (c) Dass 85 laut Autor ein "Glückstreffer" bei einer zufälligen Gruppenwahl war (andere Läufe 117–125), ist unauffällig, weil der Code explizit vorliegt und vollständig geprüft ist. Dass eine so einfache Suche einen alten Rekord um 15 verbessert, ist ungewöhnlich, aber für q=5, R=3 (weniger bearbeitete Tabelle) glaubhaft. Es ändert nichts an der nachgerechneten Tatsache.

## 3. How you can test it yourself
Der Nutzer kann das ohne den Code des Autors prüfen. Er nimmt die Datei code_K5_7_3_85.txt (85 Zeilen, je 7 Ziffern 0–4) und führt eines meiner beiden Programme aus. Sie liegen unter D:\CodingTheory_Research\.wwresearch\workspaces\A-71-gentle-mirzakhani\indep.py und indep2.py. Aufruf: `python indep.py <Datei>` bzw. `python indep2.py <Datei>`.
- indep.py markiert um jedes Codewort alle 2605 Wörter im Abstand höchstens 3 und zählt unmarkierte. Erwartet: "covered 78125 of 78125", "uncovered 0".
- indep2.py berechnet für alle 78125 Wörter den kleinsten Abstand zum Code. Erwartet: "max min-dist 3", Verteilung [85 2380 26160 49500], und beim Weglassen eines Codeworts Radius 4.
Den Tabellenwert kann man selbst nachsehen: auf https://old.sztaki.hu/~keri/codes/ die Datei 4-5_tables, Zeile n=7, Spalte R=3 (soll "38–100" zeigen), und dann auf arxiv.org nach neueren Arbeiten zu K_5(7,3) suchen. Wer einen Eintrag unter 100 findet, widerlegt den Vergleichswert, nicht den Code.

## 4. Why that test is independent of the research
Die Überdeckung wurde mit zwei neu geschriebenen Programmen geprüft, die weder Code noch Daten des Autors benutzen. Das erste arbeitet über Kugeln (Markieren aller Wörter im Abstand höchstens 3) ohne numpy, das zweite über direkte Abstandsberechnung, anders aufgebaut als verify.py. Der Quelltext des Autors wurde nicht importiert, und die Suche (grp2.py, sa.py) wurde nicht wiederholt, weil sie für die Gültigkeit irrelevant ist. Den Vergleichswert 100 hat ein separater Agent direkt aus der Originaldatei der Tabelle im Netz gelesen, nicht aus der lokalen Kopie des Autors. Die Literatursuche lief mit eigenen Suchanfragen und durch Lesen des Marosi-Papiers im Volltext.

## The submitted proof

Der Code ist explizit und vollständig prüfbar: Datei code_K5_7_3_85.txt (85 Zeilen, je 7 Ziffern 0..4). Prüfskript verify.py (nur numpy): liest die Datei, prüft Länge/Alphabet/Verschiedenheit und berechnet für alle 5^7 Wörter den minimalen Abstand zum Code; Aufruf `python verify.py code_K5_7_3_85.txt 5 7 3` gibt "Woerter: 85 ... Ueberdeckungsradius 3, OK" aus (Laufzeit wenige Sekunden).
Gefunden mit grp2.py: zufällige Gruppe G aus Koordinatenpermutationen x Symbol-Affinabbildungen x->ax+b (K=665 Bahnen auf Z_5^7), Bahn-Überdeckungsmatrix (Bahn t überdeckt Bahn u, wenn der Ball um einen Repräsentanten von t die Bahn u trifft), dann gewichtete Mengenüberdeckung über Bahnen (Gewicht = Bahnlänge) per Simulated Annealing (sa.py, 3 Seeds x 1e7 Schritte). Aufruf des Laufs: `python grp2.py 5 7 3 100 1100 11 200 3000 1e7` (Treffer in try2 nach ca. 94 s). Die Suchmethode ist für die Korrektheit irrelevant; der Beleg ist die vollständige Prüfung. Weitere 3 Läufe (je 540 s, andere Seeds) fanden nur 120-125, d.h. 85 war ein Glückstreffer der Gruppenwahl; Gleichstand-Kalibrierung: dasselbe Werkzeug reproduziert K5(6,3)=25 (Tabelle 25).
Tabellenvergleich und Literatursuche: siehe QUELLE.md (Kéri-Tabelle wörtlich; Marosi arXiv:2608.19872 v3 enthält für q=5 nur K5(11,5) 625->602, nichts zu K5(7,3); Gijswijt–Polak nur untere Schranken; Websuche ohne kleinere Marke; die aktuelle Online-Fassung der Kéri-Seite selbst habe ich nicht erneut abgerufen, nur die lokale Kopie).

### Stated assumptions

Die Kéri-Tabelle (Kopie in workspaces/A-3-eager-fermat/tables/4-5_tables.txt, Text aus PDF extrahiert, Spalten teils verstümmelt) gibt K5(7,3) <= 100 an; die Spaltenzuordnung (n=7, R=3) wurde über Konsistenz (K5(6,3)<=25=5^2, K5(7,1)<=3125) geprüft. Eine neuere Veröffentlichung mit Marke <100 außerhalb der durchsuchten Quellen kann nicht ausgeschlossen werden (Suche: Kéri-Kopie, Marosi 2026, Gijswijt–Polak, Websuche). Die Aussage hängt nur von verify.py ab.</assumptions>
<parameter name="artifacts">["D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\code_K5_7_3_85.txt","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\verify.py","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\QUELLE.md","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\grp2.py","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\grp.py","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\sa.py","D:\\CodingTheory_Research\\.wwresearch\\workspaces\\A-69-tidy-hilbert\\tabu.py"]
