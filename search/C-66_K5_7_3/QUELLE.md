# QUELLE: K_5(7,3) <= 85 (quinärer Überdeckungscode, Länge 7, Radius 3)

Vergleichstabelle: G. Kéri, "Tables for Bounds on Covering Codes", https://old.sztaki.hu/~keri/codes/ (Datei 4-5_tables.pdf, "Bounds on K5(n,R)"),
Tabellenstand 2009-2011 (Marosi nennt "last revised November 2011"). Lokale Kopie (Abruf durch Vorgängerkarte, Text in
../A-3-eager-fermat/tables/4-5_tables.txt, am 2026-11-25 gelesen).
Wörtlicher Eintrag, Zeile n=7: `7  z 2722–3125   m 225–525 o   m 38–100 u`  -> R=3: untere Marke 38 (Haas–Schlage-Puchta–Quistorff), obere Marke 100 (Schlüssel u: Davydov–Östergård 2000).
Neuer Wert: 85 (Differenz -15).

Suche nach neueren Arbeiten (2026-11-25):
- Marosi, arXiv:2608.19872 v3 (2026-09-02), "New upper and lower bounds on covering codes K_q(n,R) for 5<=q<=21": enthält für q=5 nur K5(11,5) 625->602; K5(7,3) kommt nicht vor (Auszug durch Subagent gelesen).
- Gijswijt–Polak arXiv:2504.01932: nur untere Schranken.
- Websuche (Standard) nach "K_5(7,3)": nur Hinweis auf obere Schranke 100 (MaRDI-Eintrag zu Gommard–Plagne 2004); keine kleinere Marke gefunden.
Nicht geprüft: Zeitschriftenartikel nach 2011 außerhalb arXiv, die Kéris Seite nicht kennt; aktuelle Fassung der Kéri-Seite (nur Kopie).

Datei: code_K5_7_3_85.txt (85 Wörter, Ziffern 0..4), Prüfung: `python verify.py code_K5_7_3_85.txt 5 7 3` (alle 78125 Wörter, Radius 3).
