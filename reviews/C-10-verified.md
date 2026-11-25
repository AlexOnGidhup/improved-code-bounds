# Verified: A_3(15,5) >= 8748. Expliziter ternärer Code, Länge 15, 8748 verschiedene Wörter, Mindestabstand 5. Brouwer-Tabelle (https://aeb.win.tue.nl/codes/ternary-1.html, abgerufen 2026-11-25) nennt als beste untere Schranke 7929 (Oscar Sanchez, E-Mail 2026-10-17; davor 7812 Laaksonen–Östergård 2017); obere Schranke 29213.

- Proof card: **C-10** — Ternäre/quinäre Packung A_3(n,d), A_5(n,d): Nebenklassenvereinigung + Clique (by lucid-ramanujan)
- Review card: **C-13** (by skeptical-curie, an agent that did not work on the proof)
- Verdict: **verified**

## 1. What was found
Behauptet wird A_3(15,5) >= 8748. Der Autor gibt dafür eine Datei mit 8748 ternären Wörtern der Länge 15 an. Sie entsteht als Vereinigung von 12 Nebenklassen eines linearen [15,6,>=5]_3-Codes. Die Tabelle von Brouwer (https://aeb.win.tue.nl/codes/ternary-1.html) nennt als bisherige untere Schranke 7929. Das ist ein Eintrag von Oscar Sanchez per E-Mail vom 2026-10-17. Davor stand dort 7812 von Laaksonen und Östergård (2017). Ich habe die Datei selbst geprüft und die Tabelle selbst abgerufen. Die Datei ist ein gültiger Code mit Mindestabstand 5. Die Tabelle nennt weiterhin 7929.

## 2. Why the reviewer believes it is correct
Ich habe den Beweis nicht über die Konstruktion geprüft, sondern über die Datei selbst. Nebenklassen, Syndrome und Clique-Suche spielen für die Gültigkeit keine Rolle. Gültig ist, was in der Datei steht.

1. **Datei.** Ich habe `code_3_15_5_8748.txt` unverändert kopiert und mit sha256 verglichen. Die Prüfsummen sind identisch. In den Rohbytes finde ich 8748 Zeilen zu je genau 15 Zeichen. Es gibt keine Leerzeilen, keine CR-Zeichen und nur die Zeichen 0, 1 und 2.
2. **Verschiedenheit und Abstand.** Es gibt 8748 verschiedene Zeilen. Ich habe alle 38 259 378 Paare vollständig durchgerechnet. Der Mindestabstand ist 5. Das Histogramm beginnt bei 5 (380 538 Paare), es gibt keine Paare mit Abstand 1 bis 4.
3. **Tabelle.** Ich habe die Seite selbst abgerufen und gelesen. In der Zeile `15lb` stehen für d=3, 4, 5 die Werte 354294, 83106 und 7929. In der Zeile `15ub` steht für d=5 der Wert 29213. Die Notiz "A3(15,5) >= 7929 (Oscar Sanchez, email, 2026-10-17)" steht dort wörtlich. Die jüngste Notiz auf der Seite stammt von Meadows vom 2026-11-20 bis 22. Der Eintrag 7929 ist unverändert. 8748 liegt klar über 7929 und ist keine Gleichheit.
4. **Plausibilität.** Der Sprung von etwa 10 Prozent über den bisherigen Eintrag ist auffällig groß. Die vollständige Prüfung der Datei lässt aber keinen Raum für einen Fehler. Nach der Tabelle gehört 6561 (= 3^8) zu einem linearen Code der Länge 14. Auch der Eintrag 7929 für Länge 15 ist nichtlinear.
5. **Verifier.** Das Prüfskript des Autors liest die Datei und rechnet vollständig nach. Es importiert nichts aus der Suche. Es lief bei mir durch (PASS) und stimmt mit meinem Ergebnis überein.
6. **Literatur.** Meine Websuche (standard-Modus) zu neueren Arbeiten über A_3(15,5) hat nichts Relevantes ergeben. Private E-Mail-Einsendungen an Brouwer kann ich wie der Autor nicht einsehen. Das ist ein Restrisiko für das Wort "neuester Rekord". Es betrifft aber nicht die Richtigkeit des Codes.

## 3. How you can test it yourself
Der Nutzer kann zwei Prüfungen ohne Code des Autors ausführen. Beide brauchen nur die Datei `code_3_15_5_8748.txt`.

**(a) Bitmasken-Prüfung.**
- Die Datei roh einlesen und die Wörter als Zahlen 0 bis 2 interpretieren.
- Pro Wort zwei Bitmasken bilden: eine für die Stellen mit Wert 1, eine für die Stellen mit Wert 2.
- Für jedes Paar ist der Abstand die Anzahl gesetzter Bits in ((a1 xor b1) or (a2 xor b2)). Dafür eine Popcount-Tabelle über 2^15 Einträge verwenden.
- Das Minimum über alle 38 259 378 Paare bilden.
- Erwartet: 8748 Zeilen, 8748 verschiedene Wörter, Minimum 5.
- Mein Skript: `D:\CodingTheory_Research\.wwresearch\workspaces\A-16-skeptical-curie\myverify.py`.

**(b) Kugeldisjunktheit.**
- Mindestabstand ≥ 5 gilt genau dann, wenn die Kugeln vom Radius 2 um alle Codewörter paarweise disjunkt sind.
- Jede Kugel hat 1 + 30 + 420 = 451 Punkte. Für 8748 Wörter ergibt das 3 945 348 Punkte, jeweils als Zahl zur Basis 3 kodiert.
- Prüfen, dass alle diese Zahlen verschieden sind.
- Erwartet: 3 945 348 Punkte, alle verschieden. Das ist bei mir der Fall.
- Mein Skript: `D:\CodingTheory_Research\.wwresearch\workspaces\A-16-skeptical-curie\ball.py`.

**Mutationstest.** Ersetzt man das letzte Wort durch `111100000000000`, das Abstand 4 zu einem Codewort hat, melden beide Prüfungen den Fehler. (a) meldet Minimum 2, (b) meldet nicht disjunkt (3 945 209 verschiedene Punkte statt 3 945 348). Die Prüfungen schlagen also an, wenn der Code fehlerhaft ist.

**Tabelle.** Zusätzlich https://aeb.win.tue.nl/codes/ternary-1.html aufrufen. In der Zeile 15lb, Spalte d=5 muss ein Wert unter 8748 stehen, bei mir 7929. Neuere E-Mail-Einsendungen an Brouwer bleiben ein Restrisiko.

## 4. Why that test is independent of the research
Mein Prüfskript (a) arbeitet mit Bitmasken und einer Popcount-Tabelle. Das Skript des Autors vergleicht dagegen Zeichen mit numpy. Ich habe ein eigenes Skript für Dateiformat und Verschiedenheit geschrieben. Mein zweiter Test (b) nutzt eine andere mathematische Äquivalenz, nämlich disjunkte Kugeln vom Radius 2 statt direkter Paarabstände. Beide Prüfungen sehen weder die Nebenklassen-Konstruktion noch die Clique-Suche des Autors. Ich habe den Mutationstest als Gegenprobe benutzt und die Tabelle direkt von der Brouwer-Seite gelesen, ohne Angaben aus QUELLE.md zu übernehmen. Der gemeinsame Punkt ist nur die Datei selbst. Das ist hier auch richtig, weil die Datei der Beweis ist.

## The submitted proof

Konstruktion: Kern C0 = linearer [15,6,>=5]_3-Code mit systematischer Generatormatrix G=[I6|A] (zufällig gezogen, Mindestabstand per Enumeration aller 728 Codewörter geprüft = >=5). H=[-A^T|I9] ist die Kontrollmatrix. Code C = {x in F_3^15 : Hx in S}, wobei S eine Menge von 12 Syndromen in F_3^9 ist (0 in S), deren paarweise Differenzen Nebenklassen-Mindestgewicht >=5 haben (per BFS über die Syndromspalten berechnet, Gewichte <=4 ausgeschlossen). Dann ist C eine Vereinigung von 12 Nebenklassen von C0, |C|=12*729=8748, und Abstand >=5 folgt: innerhalb einer Nebenklasse durch d(C0)>=5, zwischen zwei Nebenklassen durch das Nebenklassengewicht der Differenz. S wurde mit einer numba-Clique-Lokalsuche (cos2.py, Laufzeit ca. 8 min, 1 Kern) im Cayley-Graphen auf F_3^9 gefunden. Dies ist aber nur der Suchweg; der Beweis ist die Prüfung der Datei: `python verify.py code_3_15_5_8748.txt 3 5` liest die Datei (nur numpy), prüft Länge 15, Alphabet {0,1,2}, Verschiedenheit (8748 verschiedene Zeilen) und berechnet den Mindestabstand aller Paare vollständig (8748x8748 Paare in Blöcken); Ausgabe: 'length=15 words=8748 distinct=ok min_distance=5 (required >= 5) PASS'. Laufzeit Sekunden. Vergleichsstand in QUELLE.md (Tabelle zweimal am 2026-11-25 abgerufen, Eintrag 7929 unverändert; Suche nach neueren Arbeiten ohne Treffer, private E-Mail-Einsendungen an Brouwer nicht einsehbar).

### Stated assumptions

Tabellenstand wie am 2026-11-25 abgerufen; unbekannte private Einsendungen an Brouwer können den Eintrag inzwischen verbessert haben.

### Artifacts

- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\code_3_15_5_8748.txt`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\verify.py`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\QUELLE.md`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\cos2.py`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\mk.py`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\bestG_3_15_5_k6_8748.npy`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-13-lucid-ramanujan\best_3_15_5_k6_8748.npy`
