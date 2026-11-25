"""Prueft einen quaternaeren Code mit konstantem GC-Gehalt (Symbole 0=A,1=T,2=G,3=C; GC = Symbole 2,3).
Aufruf: python verify.py code.txt n d w   (Standard: code_A4GC_12_7_236.txt 12 7 6)
Prueft: Laenge n, nur Ziffern 0..3, Verschiedenheit, GC-Gewicht == w je Wort, Mindest-Hamming-Abstand >= d ueber alle Paare."""
import sys
f,n,d,w=(sys.argv[1:5] if len(sys.argv)>4 else ["code_A4GC_12_7_236.txt","12","7","6"])
n,d,w=int(n),int(d),int(w)
ws=[l.strip() for l in open(f) if l.strip()]
assert all(len(x)==n and set(x)<=set('0123') for x in ws),"Format"
assert len(set(ws))==len(ws),"nicht verschieden"
assert all(sum(c in '23' for c in x)==w for x in ws),"GC-Gewicht"
m=min(sum(a!=b for a,b in zip(x,y)) for i,x in enumerate(ws) for y in ws[:i])
print("Woerter",len(ws),"Laenge",n,"GC-Gewicht",w,"Mindestabstand",m)
assert m>=d
print("OK")
