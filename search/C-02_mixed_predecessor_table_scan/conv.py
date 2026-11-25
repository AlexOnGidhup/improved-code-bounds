# Forum-Block (1X2-Notation) -> kanonische Datei. python conv.py page titlesubstr out
import sys
from forumparse import blocks
page,key,out=sys.argv[1:4]
B=[b for t,b in blocks(page) if key in t]
b=B[0]
L=len(b[0]); cols=[sorted(set(w[i] for w in b)) for i in range(L)]
bins=[i for i in range(L) if len(cols[i])==2]; ters=[i for i in range(L) if len(cols[i])==3]
mp={'1':'0','X':'1','2':'2','0':'0'}
lines=[]
for w in b:
    lines.append(''.join(str(cols[i].index(w[i])) for i in bins)+''.join(mp[w[i]] if w[i] in '1X' or cols[i]==['1','2','X'] else w[i] for i in ters))
open(out,'w').write('\n'.join(lines)+'\n')
print(out,len(lines),'bin',len(bins),'ter',len(ters))
