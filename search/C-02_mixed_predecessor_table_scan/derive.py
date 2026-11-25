# Erzeugt abgeleitete Saaten: restrict (ter->bin, 2/3) bzw. split (ter->2bin) an Ternaerkoordinate j
# python derive.py src m n mode outprefix
import sys
src,m,n,mode,pre=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],sys.argv[5]
W=[l.strip() for l in open(src) if l.strip()]
cnt=0
for j in range(n):
    for s in range(3):
        out=[]
        for w in W:
            b,t=w[:m],w[m:]
            x=int(t[j]); rest=t[:j]+t[j+1:]
            if mode=='restrict':
                if x==s: continue
                y=[a for a in range(3) if a!=s].index(x)
                out.append(b+str(y)+rest)
            else: # split: Symbol s und (s+1)%3 auf Abstand 2 (00,11), drittes auf 01
                mp={s:'00',(s+1)%3:'11',(s+2)%3:'01'}
                out.append(b+mp[x]+rest)
        open(f"{pre}_j{j}_s{s}.txt",'w').write('\n'.join(out)+'\n'); cnt+=1
print(cnt,'Saaten',len(out))
