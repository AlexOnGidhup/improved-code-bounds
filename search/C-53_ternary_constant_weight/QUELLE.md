# QUELLE.md — ternäre Konstantgewichtscodes A_3(n,d,w)

Verglichen wird mit der einzigen mir bekannten Tabelle für ternäre Konstantgewichtscodes (Hamming-Gewicht = Zahl der Stellen ≠ 0, Hamming-Abstand ≥ d):

* P. R. J. Östergård, M. Svanström, "Ternary Constant Weight Codes", Electronic Journal of Combinatorics 9 (2002), #R41, **Table 5** ("Bounds on A3(n,d,w) for n ≤ 10").
  URL: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v9i1r41/pdf
  Abruf: 2026-11-25 (PDF lokal als dl/os.pdf, Text dl/os.txt; Seite 20/21 der Zeitschriftenpaginierung).
  Spaltenzuordnung der Tabelle: je Zeile "n w" und dann d=3,4,5,... aufsteigend, Einträge "Marke untere[–obere]Marke". Geprüft durch Reproduktion der exakten Einträge mit meinem Programm: A3(4,3,3)=8, (5,3,3)=12, (5,4,3)=10, (6,3,3)=18, (6,4,3)=30, (6,5,3)=24, (7,3,3)=28, (7,5,4)=32, (8,3,3)=36 (alle gleich der Tabelle).
  Die Marken: c = (quasi)zyklischer Code / Gruppe, g = lexikographischer Code (Bogdanova), l/r/t/x/y/z = andere Konstruktionen bzw. obere Schranken.

Wörtliche Tabelleneinträge (Zeile n w, Spalte d) der verbesserten Zellen:

| n | w | d | Tabelle (wörtlich) | hier gefunden | Datei |
|---|---|---|---|---|---|
| 7 | 4 | 3 | c60–67x | 62 | code_n7_w4_d3_62.txt |
| 7 | 5 | 3 | c72–84y | 82 | code_n7_w5_d3_82.txt |
| 8 | 5 | 3 | c161–214z | 173 | code_n8_w5_d3_173.txt |
| 8 | 6 | 3 | c168–224y | 184 | code_n8_w6_d3_184.txt |
| 9 | 6 | 3 | g411–642z | 483 | code_n9_w6_d3_483.txt |
| 9 | 7 | 3 | g405–576y | 426 | code_n9_w7_d3_426.txt |
| 10 | 5 | 4 | g204–288z | 221 | code_n10_w5_d4_221.txt |
| 10 | 6 | 3 | g876–1343z | 878 | code_n10_w6_d3_878.txt |
| 10 | 7 | 3 | g960–1834z | 1194 | code_n10_w7_d3_1194.txt |
| 10 | 9 | 3 | g325–400y | 326 | code_n10_w9_d3_326.txt |

In allen zehn Zellen liegt der gefundene Wert über der unteren und höchstens bei der oberen Tabellenschranke.

Weitere Tabellen / Quellen, die ich auf neuere Einträge geprüft habe (alle 2026-11-25):

* A. E. Brouwer, https://www.win.tue.nl/~aeb/codes/ (Verzeichnisliste): enthält Tabellen für binäre, konstantes Gewicht (binär, `Andw.html`), ternäre/quaternäre/5-äre unbeschränkte (`ternary-1.html` usw.) und gemischte Codes (`23codes.html`), **keine** Tabelle für ternäre Konstantgewichtscodes.
* E. Agrell et al. (Chalmers / codes.se/bounds): nur binär.
* GitHub `owhs/code-table-improvements` (Dateiliste per API geprüft): ternäre Einträge nur für *unbeschränkte* Codes (A_3(15,5), A_3(14,8)) und gemischte; keine ternären Konstantgewichtscodes.
* WebSearch (standard und extended, mehrere Anfragen zu "ternary constant weight codes", "A_3(n,d,w)", "new lower bounds", 2024–2026): kein Treffer auf eine Arbeit, die Zellen n ≤ 10 der Tabelle verbessert. Gefunden wurden nur: G. Bogdanova, "New bounds for the maximum size of ternary constant weight codes", Serdica Math. J. 26 (2000) (lexikographische Codes; deren Werte sind in Tab. 5 mit Marke g enthalten), Svanström (1997), Wei, sowie Arbeiten über optimale Codes mit festem kleinem Gewicht (w=3,4; Chee, Ge, Ling, Zhang, Zhou u. a.), die die hier verbesserten Parameter (w ≥ 4, n ≤ 10, d=3, bzw. (10,5,4)) nicht betreffen.
* Grenzen dieser Prüfung: Ich konnte Google Scholar / Zitationslisten nicht abfragen; eine unveröffentlichte oder in einer Dissertation versteckte Verbesserung ist nicht auszuschließen.

## Dateien

* `cwlib.py` – Suchprogramm (numba, Tabu/Swap-Lokalsuche auf dem vollen Raum aller ternären Wörter mit Gewicht w; Konfliktgraph "Abstand < d"). Nur zum Finden; **nicht** Teil der Prüfung.
* `verify.py` – eigenständiges Prüfskript (nur numpy): `python verify.py <datei> n w d`. Prüft Wortlänge, Alphabet {0,1,2}, Verschiedenheit, konstantes Gewicht w und paarweisen Mindestabstand ≥ d durch vollständiges Nachrechnen aller Paare.
* `code_n<n>_w<w>_d<d>.txt` – die Codes (ein Wort je Zeile).
