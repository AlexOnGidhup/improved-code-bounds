# QUELLE.md – Vergleichstabelle und Literatursuche

## Tabelle
- Brouwer, "Mixed binary/ternary codes", https://www.win.tue.nl/~aeb/codes/23codes.html
  (301 -> https://aeb.win.tue.nl/codes/23codes.html), Abruf 2026-11-25 (zweimal: durch Vorgaenger-Agent
  und erneut durch mich, beide Male gleiche Eintraege). Neuester Eintrag auf der Seite: N(4,10,7) >= 86, Ben Meadows, 2026-11-22.
- Notation woertlich: "N(m,n,d) is defined as the maximum number of vectors of length m+n with m binary and n ternary
  coordinates and mutual distance at least d."
- Tabelle d=7, woertliche Eintraege:
  - N(2,12,7): 162-432
  - N(3,11,7): 108-288
  - Fussnote: "The bounds N(1,12,7) >= 108 and N(2,12,7) >= 162 and N(3,11,7) >= 108 follow from N(0,13,7) >= 162."
    (also nur per Ableitungsregel aus dem ternaeren Code, kein eigener expliziter Code)
  - Zugrunde liegende Quellen: N(0,13,7) >= 162: spaik, 2011-06-11 (free1x2.com, t=27028, start=692);
    N(1,13,7) >= 243: PacoHH, 2011-06-12 (start=696).
- Auch ternary-1.html: A3(13,7) >= 162, A3(14,7) >= 243; keine Verbesserung der gemischten Zellen dort.

## Konstruktion der neuen Codes
- N(1,13,7)=243 (PacoHH) an einer Ternaerkoordinate auf zwei Symbole einschraenken -> N(2,12,7) >= 162 (die Tabellenregel).
  Dieser abgeleitete Code ist nicht maximal: 9 Woerter koennen gleichzeitig hinzugefuegt werden -> 171.
- N(1,12,7)=108 -> (ter->bin) N(2,11,7)/N(3,11,7)-Seed 108, 6 freie Woerter + Tausch-Lokalsuche -> 116.
- Dateien: code_N_2_12_7_171.txt (+ unabhaengig zweiter, _b), code_N_3_11_7_116.txt; Pruefung: `python verify.py`.

## Suche nach neueren Arbeiten (2026-11-25)
- Websuchen (Stichworte: mixed binary/ternary codes, N(n2,n3,d), lower bound, 2025/2026, "N(2,12,7)", "N(3,11,7)"):
  keine Arbeit gefunden, die N(2,12,7) oder N(3,11,7) verbessert. Gefunden: Litjens, "Semidefinite bounds for mixed binary/ternary
  codes", arXiv:1606.06930 (Discrete Math 2018) – nur obere Schranken; Yehezkeally et al. arXiv:2212.09314 (mixed codes, allgemein);
  MDPI Mathematics 13(16):2633 (2025), ILP fuer gemischte Hamming-Packungen (kleine Raeume, Obere Schranken).
- Brouwers Seite selbst wird aktuell (2026-11-20..24) von O. Sanchez und B. Meadows aktualisiert; es kann zwischen Abruf und Pruefung
  zu Aenderungen kommen -> vor Uebernahme Tabelle erneut abrufen.
