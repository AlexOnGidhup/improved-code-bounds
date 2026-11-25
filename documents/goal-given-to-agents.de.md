Fehlerkorrigierende Codes und Überdeckungscodes: eine veröffentlichte Schranke mit einem expliziten, nachprüfbaren Code verbessern

## Aufgabe (wörtlich vom Auftraggeber)

"Maximize the number of codewords of length $n$ with minimum Hamming distance $d$, or minimize
the size of a covering code (where every possible string is within distance $R$ of a codeword)."

## Genaue Fassung

Alphabet $Q$ mit $q$ Symbolen (binär $q=2$, ternär $q=3$, auch $q=4,5,\dots$ und gemischte
Alphabete wie $2^a3^b$). Hamming-Abstand = Anzahl der Stellen, an denen sich zwei Wörter
unterscheiden.

- **Packungsseite:** $A_q(n,d)$ = größte Zahl von Wörtern der Länge $n$ mit paarweisem Abstand
  $\ge d$. Varianten mit eigenen Tabellen: Codes mit konstantem Gewicht $A(n,d,w)$, lineare Codes
  (größtes $d$ zu gegebenem $[n,k]_q$), gemischte Alphabete.
  Ein **expliziter Code** ist eine untere Schranke; ein Unmöglichkeitsbeweis (LP, SDP,
  Zählargumente, vollständige Suche) ist eine obere Schranke.
- **Überdeckungsseite:** $K_q(n,R)$ = kleinste Zahl von Wörtern, so dass jedes Wort aus $Q^n$
  Abstand $\le R$ zu mindestens einem Codewort hat. Ein **expliziter Überdeckungscode** ist eine
  obere Schranke; ein Unmöglichkeitsbeweis ist eine untere Schranke. Die ternäre Fassung mit
  $R=1$ ist das Fußballtoto-Problem.

Für fast alle Parameter außerhalb sehr kleiner Längen klafft eine Lücke zwischen bester unterer
und bester oberer Schranke. Diese Lücken sind das Arbeitsfeld.

## Was als gelöst zählt (`submit_proof`)

Eines von beiden, jeweils für **mindestens einen** konkret benannten Parametersatz:

1. Ein expliziter Code (Packung) oder Überdeckungscode, der die **aktuell beste veröffentlichte**
   Schranke **echt** verbessert. Pflichtbestandteile im Workspace:
   - `code_<parameter>.txt`: ein Codewort je Zeile, Ziffern 0..q-1, nichts sonst;
   - `verify.py`: ein kurzes, eigenständiges Prüfskript (nur Standardbibliothek oder numpy), das
     die Datei liest und Länge, Anzahl, Verschiedenheit und Mindestabstand bzw. Überdeckungsradius
     **durch vollständiges Nachrechnen** prüft. Es darf keinen Code aus der Suche importieren und
     muss in unter 10 Minuten laufen;
   - `QUELLE.md`: die Tabelle, mit der verglichen wird (URL, Abrufdatum, wörtlicher Eintrag und
     dessen Quelle), und eine Suche nach neueren Arbeiten (arXiv, Google Scholar), die den Eintrag
     seit dem Tabellenstand verbessert haben könnten.
2. Ein vollständiger Beweis einer verbesserten Schranke auf der Gegenseite (obere Schranke für
   $A$, untere für $K$) mit maschinell nachprüfbarem Zertifikat (z. B. duale LP/SDP-Lösung in
   exakter rationaler Arithmetik, oder vollständige Suche mit nachvollziehbarer Fallzählung).

Ein Gleichstand mit dem Rekord ist **kein** Beweis, sondern ein Teilergebnis.

## Teilergebnisse (`submit_derivation`, immer mit konkretem nächsten Schritt)

- Rekord eingestellt (Gleichstand) mit einem Verfahren, das sich auf größere Parameter übertragen
  lässt; dazu: welcher Parametersatz als nächstes, mit welcher Rechenzeit.
- Ein Suchwerkzeug, das mehrere bekannte Rekorde in Minuten reproduziert (Liste der Parameter,
  erreichte Größe, Rekord), samt Einschätzung, wo es dem Rekord am nächsten kommt.
- Ein neuer, zum bekannten nicht äquivalenter optimaler Code, eine Klassifikation, oder eine
  bewiesene Strukturaussage ("jeder Code dieser Größe muss ... erfüllen"), die den Suchraum
  nachweislich verkleinert.
- Eine sauber belegte Liste "weicher" Tabelleneinträge: Parameter, bei denen der Rekord alt ist,
  aus einer einfachen Konstruktion stammt oder sichtlich wenig Rechenzeit gesehen hat.

Sackgassen (`report_dead_end`) bitte präzise: welches Verfahren, welche Parameter, wie weit vom
Rekord entfernt, nach wie viel Rechenzeit, und warum mehr Rechenzeit vermutlich nicht hilft.

## Was schon bekannt ist (aus dem Gedächtnis des Auftraggebers, **vor Gebrauch nachprüfen**)

Tabellen, die als Vergleichsmaßstab gelten. Ruft sie zuerst ab; Einträge ändern sich:

- Binäre Codes $A(n,d)$ und konstantes Gewicht $A(n,d,w)$: Tabellen von A. E. Brouwer
  (`https://www.win.tue.nl/~aeb/codes/`, dort `binary-1.html` und `Andw.html`).
- Lineare Codes über $GF(q)$, $q\le 9$: M. Grassl, `http://www.codetables.de`.
- Überdeckungscodes (binär, ternär, gemischt): Tabellen von G. Kéri
  (`http://old.sztaki.hu/~keri/codes/`), dazu das Buch Cohen/Honkala/Litsyn/Lobstein
  "Covering Codes" und Arbeiten von Östergård.
- Nichtbinäre unbeschränkte Codes ($q=3,4,5$): Tabellen von Bogdanova, Brouwer, Kapralov,
  Östergård u. a.; neuere Einträge bei Laaksonen/Östergård.
- Obere Schranken für $A(n,d)$: Delsarte-LP, Schrijvers SDP, Gijswijt/Mittelmann/Schrijver,
  Polak. Untere Schranken für $K$: Kugelüberdeckung, Van-Wee-Ungleichungen, LP mit Symmetrie.

Größenordnung einiger Lücken zur Orientierung (ungeprüft): $A(16,3)$ zwischen etwa 2720 und 3276;
$A(17,6)$ zwischen 256 und 340; $K(9,1)$ zwischen 57 und 62; $K(10,1)$ zwischen 105 und 120;
ternär $K_3(6,1)$ zwischen 71 und 73, $K_3(7,1)$ zwischen 156 und 186.

Bekannte Erfahrung des Fachs: Die kleinen binären Einträge sind über Jahrzehnte mit viel
Rechenzeit bearbeitet worden. Blindes Simulated Annealing oder Tabu-Suche auf dem vollen Raum
stellt dort Rekorde bestenfalls ein. Verbesserungen der letzten Jahre kamen fast immer aus
**Struktur**: vorgeschriebene Automorphismengruppen (Bahnen zusammenfassen, dann exakt oder
heuristisch lösen), Codes über $\mathbb{Z}_4$ und andere Ringe, Verkettung/Verklebung
($u|u+v$, Konstruktion X, Partitionskonstruktionen), Matrixmethode für Überdeckungscodes,
Clique-/Stabilitätszahl-Löser auf Bahn-Graphen, SAT/ILP mit Symmetriebrechung. Jüngere
Arbeiten haben auch LLM-gestützte Programmsuche (FunSearch/AlphaEvolve-Art) auf solche
Tabellen angesetzt; prüft, was dort schon erreicht wurde.

## Denkrichtungen (Anregung, keine Liste zum Abarbeiten)

Jede Karte nimmt **eine** Richtung **und einen eigenen Parameterbereich**, den noch niemand auf
dem Board hat. Zwei Karten mit demselben Verfahren auf verschiedenen Tabellen sind verschieden;
zwei Karten auf demselben Tabelleneintrag mit ähnlichem Verfahren sind es nicht.

- Weniger abgegraste Tabellen: $q=4,5$, gemischte Alphabete, Überdeckungen mit $R\ge 2$,
  konstantes Gewicht mit größerem $n$, lineare Codes über $GF(7),GF(8),GF(9)$.
- Vorgeschriebene Symmetrie: zyklische, quasi-zyklische, affine oder Produktgruppen; Bahnen als
  Knoten, dann gewichtete Clique (Packung) oder Mengenüberdeckung (Überdeckung).
- Exakte Verfahren auf kleinen offenen Fällen: ILP/SAT mit Symmetriebrechung, auch als Beweis
  einer Gegenschranke.
- Konstruktionen statt Suche: aus guten kurzen Codes längere bauen, Teilcodes/Nebenklassen
  vereinigen, nichtlineare Codes aus $\mathbb{Z}_4$-, $\mathbb{Z}_2\mathbb{Z}_4$- oder
  additiven Codes.
- Überdeckungen: Matrixmethode (Blokhuis–Lam, Östergård), direkte Summen und
  amalgamierte direkte Summe, Normalität, stückweise konstante Codes.
- Gegenschranken: LP/SDP mit exakter Rundung, verfeinerte Zählargumente für Überdeckungen.
- Übertragung aus Nachbarfeldern: Designs, Graphfärbung, endliche Geometrie (Kappen, Bögen,
  sättigende Mengen), Gitterpackungen, Tabu-Suche mit gelernter Nachbarschaft.

## Rahmen (bindend)

- Der Rechner hat 16 logische Kerne und 31 GB RAM, davon ist viel durch andere Arbeiten belegt.
  **Je Agent höchstens 4 Prozesse/Threads und höchstens 3 GB RAM.** Keine GPU benutzen.
  Ein Speicherüberlauf hat diesen Rechner schon einmal über Nacht lahmgelegt: Schätzt den
  Speicherbedarf **vor** jedem Lauf ab (z. B. $q^n$ Wörter × Bytes) und brecht ab, statt
  auszulagern.
- Vorhanden: Python 3.12 mit numpy, scipy, numba, networkx, sympy. **Kein C-Compiler, kein Rust.**
  Für schnelle Schleifen numba oder numpy-Bitoperationen. Weitere Pakete (z. B. `ortools`,
  `python-sat`, `highspy`, `galois`) nur in ein eigenes venv im Workspace installieren
  (`python -m venv <workspace>/venv`), nie global.
- Einzelne Rechenläufe höchstens 25 Minuten, mit Zwischenständen auf Platte (bester Code bisher),
  damit ein Nachfolger weitermachen kann. Im Hintergrund gestartete Prozesse am Ende der Karte
  beenden.
- **Mindestens alle 30 Minuten eine `note` auf das Board** (Stand, beste Größe, nächster Schritt).
  Karten ohne Lebenszeichen werden nach 60 Minuten neu vergeben, und nach 120 Minuten wird jeder
  Agent beendet: plant so, dass die Karte nach spätestens 100 Minuten mit einem der drei
  Abschlüsse endet. Lieber ein ehrliches Teilergebnis mit nächstem Schritt als ein Abbruch.
- Zuerst den Stand des Wissens prüfen (Tabelle abrufen, nach neueren Arbeiten suchen), dann
  rechnen. Material aus dem Netz nur lesen; keine heruntergeladenen Programme ausführen.
  Codes aus Tabellen als Daten zu laden ist in Ordnung.
- Jede Größenangabe, die ihr meldet, muss von einem unabhängigen Prüfskript bestätigt sein
  (siehe oben). Nennt in Findings immer Parameter, erreichte Größe, Rekord laut Tabelle und Pfad
  zur Datei.
- Sprache auf dem Board: Deutsch, knapp, mit Zahlen. Dateien nur im eigenen Workspace anlegen.
- Nicht im Rahmen: Löschungs-/Einfügungscodes, Quantencodes, asymptotische Schranken ohne
  konkreten Tabelleneintrag, Rang- und Unterraumcodes.
