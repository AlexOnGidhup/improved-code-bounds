# Verified: Gemischte binär/ternäre Codes (m binäre, n ternäre Koordinaten, Brouwer-Notation N(m,n,d)): N(2,12,7) >= 171 (Tabelle Brouwer 23codes.html, Abruf 2026-11-25: 162-432) und N(3,11,7) >= 116 (Tabelle: 108-288). Explizite Codes: code_N_2_12_7_171.txt (171 Wörter, Länge 14, ein weiterer unabhängiger Code code_N_2_12_7_171_b.txt) und code_N_3_11_7_116.txt (116 Wörter, Länge 14), jeweils paarweiser Hamming-Abstand >= 7.

- Proof card: **C-2** — Tabellen-Kreuzvergleich (Packungsseite): A(n,d,w) und A_q(n,d), q=4,5 (by lucid-riemann)
- Review card: **C-4** (by nimble-lovelace, an agent that did not work on the proof)
- Verdict: **verified**

## 1. What was found
Die Karte C-2 behauptet zwei neue Untergrenzen für gemischte Binär/Ternär-Codes (m binäre, n ternäre Stellen, Mindestabstand 7): N(2,12,7) ≥ 171 (Tabelle: 162) und N(3,11,7) ≥ 116 (Tabelle: 108). Die Codes stammen aus regelabgeleiteten Tabellencodes, die um freie Wörter ergänzt wurden. Ich habe alle drei abgegebenen Codedateien neu geprüft. Es gibt keinen Fehler, und die Tabelle steht heute unverändert.

## 2. Why the reviewer believes it is correct
Ich habe versucht, die Behauptung zu brechen, und sie hält.
1. Eigener Prüfer (numpy, ohne Code des Autors): Dateien als rohe Bytes gelesen, CR/LF entfernt. Länge 14 bei allen Wörtern, nur Ziffern 0/1/2, bei m=2 bzw. m=3 nur 0/1 auf den binären Stellen. Alle Wörter verschieden. Die vollständige Paarabstandsmatrix wurde berechnet. Ergebnis: code_N_2_12_7_171.txt hat 171 Wörter und Mindestabstand 7 (3600 Paare genau auf Abstand 7). code_N_2_12_7_171_b.txt hat 171 Wörter, Mindestabstand 7. code_N_3_11_7_116.txt hat 116 Wörter und Mindestabstand 7 (1903 Paare auf Abstand 7). Der Mindestabstand liegt genau bei 7, das ist plausibel.
2. Das mitgelieferte verify.py läuft in unter 1 s und liefert dasselbe. Ich habe darin keine Schwäche gesehen, nur ein harmloses UTF-8-BOM am Dateianfang.
3. Vergleichswert neu abgerufen (https://aeb.win.tue.nl/codes/23codes.html, 2026-11-25 ca. 02:28): Tabelle d=7, Zeile m=2, n=12 steht bei 162-432. Zeile m=3, n=11 steht bei 108-288. Die Fußnote lautet wörtlich: 'The bounds N(1,12,7) ≥ 108 and N(2,12,7) ≥ 162 and N(3,11,7) ≥ 108 follow from N(0,13,7) ≥ 162.' Beide Werte sind also nur per Regel abgeleitet, ohne eigenen Code. Das stützt die Idee des Autors, dass abgeleitete Codes nicht maximal sein müssen.
4. Konsistenz mit der Nachbarschaft der Tabelle: N(2,11,7) ≥ 77, N(4,10,7) ≥ 86 und N(1,13,7) ≥ 243 widersprechen den neuen Werten nicht. Aus 171 folgt 2/3·171 = 114 ≤ 116, aus 116 folgt 2/3·116 ≈ 77 ≤ 86. Die Obergrenzen 432 und 288 sind weit entfernt.
5. Literatursuche (nur eine Websuche): keine Arbeit gefunden, die diese Zellen verbessert. Gefunden wurden nur Arbeiten zu oberen Schranken (Litjens arXiv:1606.06930, MILP-Arbeit arXiv:2310.01883). Die Brouwer-Seite wird aktuell von Sanchez und Meadows geändert, daher können sich die Einträge jederzeit verbessern.
Einschränkungen: Ich habe die Herkunft der Seed-Codes (PacoHH 243-Code) nicht neu rekonstruiert. Das ist nicht nötig, weil die abgegebenen Dateien selbst den Beweis tragen. Dass Brouwers Tabelle der beste veröffentlichte Wert ist, ist eine Annahme. Ob 171 und 116 in anderen Archiven (z. B. Sanchez' Dateien) schon vorkommen, habe ich nicht geprüft.

## 3. How you can test it yourself
Selbst nachprüfen ohne das Skript des Autors: Dieses Python-Programm als t.py speichern: `import numpy as np, sys; L=[l for l in open(sys.argv[1],'rb').read().decode().replace('\r','').split('\n') if l]; m=int(sys.argv[2]); A=np.array([[int(c) for c in l] for l in L]); assert A.shape[1]==14 and A[:,:m].max()<=1 and A.max()<=2 and len(set(L))==len(L); D=(A[:,None,:]!=A[None,:,:]).sum(-1); np.fill_diagonal(D,99); print(len(L), D.min())`. Aufruf je Datei: `python t.py code_N_2_12_7_171.txt 2`, `python t.py code_N_2_12_7_171_b.txt 2`, `python t.py code_N_3_11_7_116.txt 3`. Erwartet: '171 7', '171 7', '116 7'. Meine Kopie dieses Tests: D:\CodingTheory_Research\.wwresearch\workspaces\A-7-nimble-lovelace\mycheck.py (Aufruf: python mycheck.py <Datei> <m> <n>). Danach die Tabelle https://aeb.win.tue.nl/codes/23codes.html im Abschnitt d=7 erneut ansehen: Zeile 2/Spalte 12 und Zeile 3/Spalte 11 müssen noch 162 bzw. 108 zeigen, sonst ist der Vergleich zu aktualisieren. Meine gespeicherte Kopie des Abrufs: D:\CodingTheory_Research\.wwresearch\workspaces\A-7-nimble-lovelace\dl\23codes.html.

## 4. Why that test is independent of the research
Mein Prüfer ist eine eigene Neuimplementierung (numpy-Matrixvergleich statt der Doppelschleife des Autors). Er liest die Dateien als Bytes mit eigener Behandlung der Zeilenenden und prüft die Binärstellen getrennt. Die Tabelle habe ich selbst direkt von Brouwers Seite neu geladen und die Zellen aus dem HTML gelesen, ohne QUELLE.md zu benutzen. Von der Suche des Autors habe ich weder Code noch Zwischenstände verwendet. Nur die fertigen Codedateien wurden geprüft. Bei einer Untergrenze zählt nur das: Ein Code mit Mindestabstand 7 und genügend Wörtern ist ein Beweis, egal wie er gefunden wurde.

## The submitted proof

Pfad: D:\CodingTheory_Research\.wwresearch\workspaces\A-5-lucid-riemann\ (code_N_2_12_7_171.txt, code_N_2_12_7_171_b.txt, code_N_3_11_7_116.txt, verify.py, QUELLE.md).

Verfahren: (1) Rekordcode N(1,13,7)=243 (PacoHH 2011, free1x2.com t=27028 via Wayback) an einer Ternärkoordinate auf 2 Symbole eingeschränkt -> 162 Wörter in (2,12,7); das ist genau die Regelableitung, aus der der Tabellenwert 162 stammt (Tabellenfußnote: "follow from N(0,13,7) >= 162"). (2) Dieser abgeleitete Code ist nicht maximal: 9 freie Wörter (Abstand >=7 zu allen 162), die gleichzeitig hinzufügbar sind -> 171. Analog: N(1,12,7)=108-Code, ter->bin-Koordinate umgewandelt als (3,11,7)-Seed mit 108 Wörtern, 6 freie Wörter plus Tausch-Lokalsuche -> 116. Weitere 25 Minuten Lokalsuche fanden keine weiteren Wörter (171/116 stabil).

Nachprüfung: `python verify.py` (nur Standardbibliothek, <1 s) liest die Dateien, prüft Länge 14, Alphabet (erste m Stellen 0/1, Rest 0/1/2), Verschiedenheit und vollständig alle Paarabstände: Ausgabe "N(2,12,7) Woerter=171 Mindestabstand=7 -> BESSER", dito 171 (zweiter Code) und "N(3,11,7) Woerter=116 Mindestabstand=7 -> BESSER". Zusätzlich vom Vorgänger mit verify_mixed.py bestätigt.

Vergleichstabelle (QUELLE.md): Brouwer 23codes.html, zweimal abgerufen 2026-11-25 (Seite zuletzt geändert durch Ben Meadows 2026-11-22), Einträge N(2,12,7) 162-432, N(3,11,7) 108-288, beide nur per Regel aus N(0,13,7)>=162 abgeleitet. Ableitungsabschluss der Tabelle (Einbetten, Restriktion, Kürzen, Punktieren, ter->bin) liefert keine bessere Schranke für diese Zellen. Literatursuche (arXiv/Web, 2025/2026): keine Arbeit gefunden, die diese Zellen verbessert (Litjens SDP 1606.06930 liefert nur obere Schranken).

Hinweis: Orphan-Prozesse des Vorgängers (deep.py/coset3.py) liefen noch; mir wurde das Beenden vom System verweigert, sie sind für den Beweis irrelevant.

### Stated assumptions

Die Tabelle von Brouwer (Stand Abruf 2026-11-25) ist die maßgebliche 'beste veröffentlichte' Schranke; die Tabelle wird derzeit aktiv geändert (Sanchez, Meadows), daher sollte der Reviewer sie vor Annahme erneut abrufen. Notation N(m,n,d): m binär, n ternär.</assumptions>
<parameter name="summary">Zwei Tabellenrekorde in Brouwers gemischter Binär/Ternär-Tabelle verbessert: N(2,12,7) 162 -> 171 und N(3,11,7) 108 -> 116, durch Augmentierung regelabgeleiteter Codes. Explizite Codes mit eigenständigem verify.py (volle Paarprüfung) und QUELLE.md im Workspace.

### Artifacts

- `D:\CodingTheory_Research\.wwresearch\workspaces\A-5-lucid-riemann\code_N_2_12_7_171.txt`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-5-lucid-riemann\code_N_2_12_7_171_b.txt`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-5-lucid-riemann\code_N_3_11_7_116.txt`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-5-lucid-riemann\verify.py`
- `D:\CodingTheory_Research\.wwresearch\workspaces\A-5-lucid-riemann\QUELLE.md`
