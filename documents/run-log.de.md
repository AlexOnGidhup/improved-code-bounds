# Nachtprotokoll 2026-11-25: wwresearch auf Codes und Überdeckungscodes

Ziel: `documents/wwresearch-ziel-codes.md`. Board: http://localhost:4777. Zustand: `.wwresearch/`.
Logs: `results/wwresearch-codes-run*.log`.

## Verlauf

- 01:35 Start Lauf 1: 3 × Mythos 5.2, Effort high, harte Agenten-Obergrenze (`WWR_HARD_LIMIT=1`).
  Karten C-1 (Matrixmethode gemischte/ternäre Überdeckungen R≥2), C-2 (Tabellen-Kreuzvergleich
  Packungsseite), C-3 (Überdeckungen q=4,5 mit Gruppe).
- 01:58 Verbrauchsmessung nach 20 Minuten: 5-Stunden-Fenster 10 % → 41 %, Woche (alle Modelle)
  2 % → 6 %, Woche (Mythos/Fable-Topf) 3 % → 11 %. Hochgerechnet wäre das 5-Stunden-Fenster gegen
  02:40 voll und die Woche bis zum Morgen fast aufgebraucht. **Lauf 1 gestoppt.** Karten, Notizen,
  Findings und Dateien bleiben erhalten.
- 02:00 Start Lauf 2 auf demselben Board: 2 × Sonnet 5.5, Effort high. Die drei offenen Karten
  werden von frischen Agenten übernommen.

## Änderung am Harness

`bin/wwresearch.js`: Umgebungsvariable `WWR_CLAUDE_ARGS` reicht Zusatzargumente an jeden
Claude-Code-Agenten durch (hier `--effort high`). Nicht committet.
- 02:19 Sonnet-Rate nach 20 Minuten: 5-Stunden-Fenster 41 % → 46 % (etwa 15 %/h), Woche unverändert
  6 %. Reicht knapp bis zum Reset um 05:40. Es bleibt bei 2 Agenten.

## Ergebnisse

### Neue untere Schranken für gemischte binär/ternäre Codes (Karte C-2, eingereicht 02:01)

Notation von Brouwer: N(m,n,d) = größte Zahl von Wörtern mit m binären und n ternären Stellen und
Mindestabstand d.

| Parameter | Tabelle Brouwer (Abruf 25.11.2026) | Neu | Datei |
|---|---|---|---|
| N(2,12,7) | 162–432 | **171** | `.wwresearch/workspaces/A-5-lucid-riemann/code_N_2_12_7_171.txt` |
| N(3,11,7) | 108–288 | **116** | `.wwresearch/workspaces/A-5-lucid-riemann/code_N_3_11_7_116.txt` |

Vom Orchestrator geprüft (02:22), unabhängig vom Agenten:
- Eigenes Prüfskript (alle Paare, nur Standardbibliothek): 171 bzw. 116 verschiedene Wörter,
  Länge 14, genau 2 bzw. 3 rein binäre Stellen, Mindestabstand 7.
- Tabelle selbst abgerufen (`https://aeb.win.tue.nl/codes/23codes.html`): Einträge 162–432 und
  108–288; beide unteren Schranken sind dort nur aus N(0,13,7) ≥ 162 abgeleitet, also nie direkt
  gesucht worden. Das erklärt, warum sie so leicht fallen.
- Offen: Die Board-Prüfung (Karte C-4) läuft noch. Die Seite wird gerade von anderen aktualisiert
  (letzter Eintrag: N(4,10,7) ≥ 86, 22.11.2026), vor einer Meldung an Brouwer also erneut abrufen.

### Board-Prüfung von C-2 (02:29): bestätigt

Bericht: `.wwresearch/reports/C-2-verified.md`.

### Neue obere Schranke für einen quinären Überdeckungscode (Karte C-1, eingereicht 02:58)

| Parameter | Tabelle Kéri (Stand 21.11.2011) | Neu | Datei |
|---|---|---|---|
| K_5(9,5) | 19–55 | **50** | `.wwresearch/workspaces/A-4-nimble-hilbert/code_K5_9_5_50.txt` |

- Vom Orchestrator geprüft (03:03): eigenes Skript zählt alle 5^9 = 1 953 125 Wörter durch; 50
  verschiedene Codewörter, Überdeckungsradius 5.
- Nicht von mir geprüft: der Tabelleneintrag 55 (aus dem PDF, das ein Agent abgerufen hat) und ob
  es seit 2011 eine bessere Schranke gibt. Laut Agent enthält Marosi, arXiv:2608.19872 (2026)
  nichts zu K_5(9,5); das dort genannte Repository `github.com/Mapika/coldcase` konnte der Agent
  nicht einsehen. Board-Prüfung (Karte C-7) läuft.

### Weitere Karten

- C-3 (Überdeckungen q=4,5 mit additivem Kern): Sackgasse, K_4(8,4) ≤ 28 nicht erreicht.
- C-5 (konstantes Gewicht, zyklische Gruppen): nur Gleichstände; Folgekarte C-6 mit größeren
  Gruppen läuft.

## Verlauf (Fortsetzung)

- 03:00 Verbrauch: 5-Stunden-Fenster 49 % (+3 % in 40 Minuten), Woche 7 %. Sonnet ist viel billiger
  als zuerst gemessen; auf 3 Agenten erhöht.
- 03:45 Verbrauch: 5-Stunden-Fenster 54 %, Woche 7 %. Auf 4 Agenten erhöht (Obergrenze wegen
  16 Kernen und RAM).

### Board-Prüfung von C-1 (03:07): bestätigt

Bericht: `.wwresearch/reports/C-1-verified.md`.

### Neue untere Schranke für einen ternären Code (Karte C-10, eingereicht 03:43, Board-Prüfung 03:45 bestätigt)

| Parameter | Tabelle Brouwer `ternary-1.html` (Abruf 25.11.2026) | Neu | Datei |
|---|---|---|---|
| A_3(15,5) | 7929–29213 (7929: O. Sanchez, 17.10.2026; davor 7812 Laaksonen–Östergård 2017) | **8748** | `.wwresearch/workspaces/A-13-lucid-ramanujan/code_3_15_5_8748.txt` |

- Konstruktion: Vereinigung von 12 Nebenklassen eines linearen [15,6,≥5]-Codes über GF(3);
  die 12 Syndrome per Clique-Suche (8 Minuten, 1 Kern).
- Vom Orchestrator geprüft (03:47): eigenes Skript über alle 38 Mio. Paare, 8748 verschiedene
  Wörter, Mindestabstand 5. Den Tabelleneintrag 7929 hat der Prüf-Agent selbst abgerufen, ich nicht.
- Bericht: `.wwresearch/reports/C-10-verified.md`.

### Weitere Karten

- C-8 (lineare Codes über GF(8)/GF(9), quasi-zyklisch): Sackgasse, 1–6 unter der Tabelle.
- C-9 (quaternäre Codes, Nebenklassen): Sackgasse, A_4(8,5) = 76 nicht erreicht.
- C-6 (konstantes Gewicht, größere Gruppen): kein Rekord; Folgekarte C-12 läuft.
- C-11 (binäre Überdeckungen, stückweise konstant + ILP): läuft.

### Neue obere Schranke für einen senären Überdeckungscode (Karte C-14, eingereicht 04:17, Board-Prüfung 04:24 bestätigt)

| Parameter | Tabelle Kéri `6-21_tables.pdf` (2009) | Neu | Datei |
|---|---|---|---|
| K_6(6,2) | 133–274 (274: Rivas Soriano) | **216** | `.wwresearch/workspaces/A-17-stubborn-franklin/code_K6_6_2_216.txt` |

- Vom Orchestrator geprüft (04:40): eigenes Skript über alle 6^6 = 46 656 Wörter, 216 verschiedene
  Codewörter, Überdeckungsradius 2. Tabellenwert nicht selbst abgerufen; laut Prüf-Agent steht 274
  auch in der Zusammenführung `Mapika/coldcase`.
- Bericht: `.wwresearch/reports/C-14-verified.md`.

### Weitere Karten

- C-15 (binäre Codes über Z4-Nebenklassen): Werkzeug, kein Rekord; Folgekarte C-16 läuft.
- C-11 (binäre Überdeckungen, stückweise konstant): Sackgasse.
- C-17 (quaternäre Codes, n = 14–20): Sackgasse.
- C-12 (A(27,6,5) per CP-SAT): bleibt bei 260 gegen Rekord 262; Folgekarte C-19 läuft.
- C-20 (ternäre Überdeckungen R = 1, 2) und C-21 (konstantes Gewicht d = 4, 10): laufen.

## Verlauf (Fortsetzung)

- 04:36 Verbrauch: 5-Stunden-Fenster 60 %, Woche 8 %.
- 04:37 **Speicherüberlauf abgefangen:** `sweep.py` von Karte C-21 belegte 13,7 GB, freier RAM 0 GB.
  Prozess beendet, danach 18,9 GB frei. Der Agent hat die 3-GB-Regel aus der Zieldatei missachtet.
- 04:40 RAM-Wächter gestartet (`documents/ram-watchdog.ps1`): beendet alle 15 Sekunden
  Python-Prozesse dieser Nacht mit mehr als 4 GB; Protokoll in `results/ram-watchdog.log`.
- 05:27 Verbrauch: 5-Stunden-Fenster 67 % (Reset 05:40), Woche 9 %. 4 Agenten aktiv, 13,9 GB RAM
  frei, Wächter ohne Eingriff. Seit 04:40 kein neuer Rekord: Gleichstände bei A(20,4) = 24576,
  K_3(7,2) = 34; A(27,6,5) bleibt bei 260 gegen 262; Sackgassen C-21 (konstantes Gewicht d = 4, 10),
  C-22 (quinäre Packung), C-26 (binäre Überdeckung per Matrixmethode). Folgekarten C-25, C-27,
  C-28 und neue Karte C-29 (Regelabschluss der Überdeckungstabellen) laufen.
- 06:22 Verbrauch nach Reset: 5-Stunden-Fenster 4 %, Woche 10 %. 4 Agenten, 13,4 GB RAM frei,
  Wächter ohne Eingriff.

### Folgerungen aus K_6(6,2) ≤ 216 (Karte C-29, eingereicht 05:31, Board-Prüfung 05:38 bestätigt)

| Parameter | Bisher | Neu | Datei in `.wwresearch/workspaces/A-32-rigorous-noether/` |
|---|---|---|---|
| K_6(7,3) | 246 (Kéri 2009), 227 (Marosi 2026) | **216** | `code_K6_7_3_216.txt` |
| K_6(9,3) | 4752 (Kéri) | **3888** | `code_K6_9_3_3888.txt` |
| K_6(10,3) | 19347 (Kéri) | **15552** | `code_K6_10_3_15552.txt` |

- Einordnung des Orchestrators: Das sind keine eigenständigen Funde, sondern Standardfolgerungen
  aus dem Code von C-14 (Stelle anhängen: 216; direkte Summe mit K_6(3,1) = 18: 216·18 = 3888;
  mit K_6(4,1) ≤ 72: 216·72 = 15552). Sie zählen als Tabelleneinträge, hängen aber alle an C-14.
- Vom Orchestrator geprüft (06:25): eigenes Skript markiert alle Kugeln, 0 unüberdeckte Wörter
  von 6^7, 6^9 bzw. 6^10. Bisherige Tabellenwerte nicht selbst abgerufen.

### Neue obere Schranke für einen septenären Überdeckungscode (Karte C-31, eingereicht 05:53, Board-Prüfung 05:55 bestätigt)

| Parameter | Tabelle Kéri `6-21_tables.pdf` | Neu | Datei |
|---|---|---|---|
| K_7(5,1) | 606–769 | **766** | `.wwresearch/workspaces/A-34-gentle-fermat/code_K7_5_1_766.txt` |

- Vom Orchestrator geprüft (06:25): 766 verschiedene Wörter, 0 unüberdeckte von 7^5 = 16 807.
  Tabellenwert nicht selbst abgerufen.

### Weitere Karten

- C-25 (A(21,6,5), Ziel 111 gegen Rekord 110): Teilergebnis, Folgekarte C-32 läuft.
- C-28 (K_3(9,2)): kein Rekord, Folgekarte C-35 läuft.
- C-34 (gemischte binär/ternäre Überdeckung R = 1): läuft.
- 07:18 Verbrauch: 5-Stunden-Fenster 12 %, Woche 11 %. Kein neuer Rekord seit 05:55.
- 07:25 Alle neun Rekord-Codes nach `results/rekorde/` kopiert, gemeinsames Prüfskript
  `pruefe_alle.py` meldet neunmal OK. Board-Export: `results/wwresearch-codes-report.md`.
- 08:08 Verbrauch: 5-Stunden-Fenster 18 %, Woche 12 %. 57 Agenten bisher. Neu: C-47 reicht
  A_4^GC(12,7,6) ≥ 236 ein (DNA-Codes mit festem GC-Gehalt, Tabelle 183); Board-Prüfung
  **unentschieden**, weil der aktuelle Rekord nicht zu klären war. Sackgassen C-42, C-44, C-46,
  C-48, C-49, C-50. Zusammenfassung in `documents/BERICHT-2026-11-25.md`.
- 08:59 Verbrauch: 5-Stunden-Fenster 26 %, Woche 13 %. 69 Agenten bisher, 13,7 GB RAM frei.

### Ternäre Konstantgewichtscodes (Karte C-53, eingereicht 08:38, Board-Prüfung 08:40 bestätigt) – Rekordstatus ungesichert

Zehn Codes A_3(n,d,w) (Länge n, genau w Stellen ≠ 0, Abstand ≥ d), verglichen mit Tabelle 5 in
Östergård–Svanström, EJC 9 (2002) R41:

| A_3(n,d,w) | Tabelle 2002 | Neu |
|---|---|---|
| (7,3,4) | 60–67 | 62 |
| (7,3,5) | 72–84 | 82 |
| (8,3,5) | 161–214 | 173 |
| (8,3,6) | 168–224 | 184 |
| (9,3,6) | 411–642 | 483 |
| (9,3,7) | 405–576 | 426 |
| (10,4,5) | 204–288 | 221 |
| (10,3,6) | 876–1343 | 878 |
| (10,3,7) | 960–1834 | 1194 |
| (10,3,9) | 325–400 | 326 |

- Vom Orchestrator geprüft (09:02): alle zehn Dateien gültig (Anzahl, Gewicht, Mindestabstand).
  Kopie in `results/rekorde/ternaer_konstantgewicht_ungesichert/`.
- **Vorbehalt des Orchestrators:** Die Vergleichstabelle ist 24 Jahre alt. Zu ternären
  Konstantgewichtscodes gibt es seither viele Arbeiten; ob diese zehn Werte den heutigen Stand
  übertreffen, ist nicht belegt. Die Board-Prüfung dauerte knapp zwei Minuten. Bis eine
  Literatursuche vorliegt, zähle ich sie nicht als Rekorde.

### Weitere Karten

- Gleichstand A_3(13,8) = 54 (C-58); K(3,5,1) Ziel 91 gegen 92 noch offen (C-56, C-64 läuft).
- Sackgassen: C-55 (binär d = 6, 8 mit Zufallskernen), C-60 (SDP-Unterschranken für
  Überdeckungen), C-61 (binäre K(n,1)), C-63 (K_4, K_5 mit R = 2).
- 09:50 Verbrauch: 5-Stunden-Fenster 32 %, Woche 14 %. 75 Agenten bisher, 13,3 GB RAM frei.

### Drei weitere quinäre Überdeckungscodes (Karten C-66 und C-65, eingereicht 09:17/09:19, Board-Prüfung 09:22/09:23 bestätigt)

| Parameter | Tabelle Kéri `4-5_tables.pdf` | Neu | Karte |
|---|---|---|---|
| K_5(7,3) | 38–100 (Davydov–Östergård 2000) | **85** | C-66 |
| K_5(9,4) | 64–255 (Bhandari–Durairajan 1996) | **250** | C-65 |
| K_5(9,3) | 330–1275 (Bhandari–Durairajan 1996) | **1250** | C-65 |

- Vom Orchestrator geprüft (09:55): 0 unüberdeckte Wörter von 5^7 bzw. 5^9; Dateien in
  `results/rekorde/`, in `pruefe_alle.py` aufgenommen (jetzt zwölf Codes, alle OK).
  Tabellenwerte nicht selbst abgerufen.

### Weitere Karten

- C-64: K(3,5,1) mit Kern [5,2,3] bewiesen nicht unter 96, also kein Weg zu 91.
- C-62: Klassifikation für A_3(13,8), A_3(12,7) negativ.
- Laufend: C-67 (ternäre Überdeckung R = 3, 4), C-70 (exakte Gegenschranken konstantes Gewicht),
  C-71 (K_q für q = 7..10), C-72 (binäre Überdeckung R = 2, 3).
- 10:40 Verbrauch nach Reset: 5-Stunden-Fenster 0 %, Woche 15 %. 85 Agenten bisher, 11,4 GB RAM
  frei. **RAM-Wächter hat um 10:20 zweimal eingegriffen** (`exw.py` von Karte C-74 mit 7,5 und
  10,5 GB beendet).

### Septenärer Überdeckungscode (Karte C-71, eingereicht 10:05, Board-Prüfung 10:10 bestätigt)

| Parameter | Bisher | Neu |
|---|---|---|
| K_7(9,4) | 1843 (Kéri), 1475 (Marosi 2026) | **1372** |

- Vom Orchestrator geprüft (10:45): 0 unüberdeckte Wörter von 7^9 = 40 353 607; Datei in
  `results/rekorde/`, in `pruefe_alle.py` aufgenommen (13 Codes). Vergleichswerte nicht selbst
  abgerufen.

### Weitere Karten

- Sackgassen: C-67 (ternäre Überdeckung R = 3, 4), C-70 (Gegenschranken konstantes Gewicht),
  C-74 (binär A(17,6), Rekord 258 nicht erreicht), C-78 (senäre Packung: keine Vergleichstabelle),
  C-79 (binäre K(n,1), n = 16..23).
- Laufend: C-80 (additive quaternäre Codes), C-81 (A_5(9,6)), C-82 (K_6 mit R = 4, 5).
- 10:41 **Lauf auf Wunsch gestoppt.** Board, alle vier Agenten, deren Suchskripte (samt
  Neustart-Schleifen) und der RAM-Wächter sind beendet. Vier Karten waren noch in Arbeit (C-80,
  C-81, C-82 und eine weitere); ihre Notizen und Dateien bleiben in `.wwresearch/` erhalten.
  Fortsetzen: im Ordner `D:\CodingTheory_Research` denselben `run`-Befehl ohne Ziel starten.
  Endstand: 85 Agenten, 44 Ideen-Karten, Woche 15 %. Abschlussprüfung `pruefe_alle.py`: 13 von 13 OK.
- 10:50 Literaturrecherche abgeschlossen, Ergebnis in `documents/LITERATURSTAND-2026-11-25.md`.
