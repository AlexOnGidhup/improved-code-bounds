import re,html,json
s=open('dl/23codes.html',encoding='utf-8',errors='replace').read()
# split by d sections
T={}
secs=re.split(r'<h2><a name="d(\d+)">',s)
for i in range(1,len(secs),2):
    d=int(secs[i]); body=secs[i+1]
    for tab in re.findall(r'<table.*?</table>',body,flags=re.S):
        rows=re.findall(r'<tr.*?</tr>',tab,flags=re.S)
        hdr=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<th.*?</th>',rows[0],flags=re.S)]
        cols=[int(x) for x in hdr[1:]]
        for r in rows[1:]:
            th=re.findall(r'<th.*?</th>',r,flags=re.S)
            m=int(re.sub(r'<[^>]+>','',th[0]).strip())
            tds=[html.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<td.*?</td>',r,flags=re.S)]
            for n,v in zip(cols,tds):
                if not v: continue
                v=v.replace(' ','')
                if '-' in v: lb,ub=v.split('-')
                else: lb=ub=v
                T[(m,n,d)]=(int(lb),int(ub))
json.dump({f"{m},{n},{d}":v for (m,n,d),v in T.items()},open('table23.json','w'))
print(len(T))
opn=[(k,v) for k,v in sorted(T.items(),key=lambda x:(x[0][2],x[0][0]+x[0][1],x[0][0])) if v[0]<v[1]]
print(len(opn))
# consistency rules on lower bounds
def lb(m,n,d):
    if m<0 or n<0: return None
    if (m,n,d) in T: return T[(m,n,d)][0]
    return None
viol=[]
for (m,n,d),(L,U) in T.items():
    cands=[]
    def add(v,why):
        if v is not None: cands.append((v,why))
    x=lb(m+1,n-1,d); add(x,'embed bin->ter from (%d,%d)'%(m+1,n-1))
    x=lb(m-1,n+1,d); add(None if x is None else -(-2*x//3),'restrict ter->bin from (%d,%d)'%(m-1,n+1))
    x=lb(m+1,n,d); add(None if x is None else -(-x//2),'shorten bin')
    x=lb(m,n+1,d); add(None if x is None else -(-x//3),'shorten ter')
    x=lb(m+1,n,d+1) if d+1<=10 else None; add(x,'puncture bin')
    x=lb(m,n+1,d+1) if d+1<=10 else None; add(x,'puncture ter')
    x=lb(m-1,n,d); add(x,'pad bin')
    x=lb(m,n-1,d); add(x,'pad ter')
    x=lb(m-2,n+1,d); add(x,'ter->2bin from (%d,%d)'%(m-2,n+1))
    for v,why in cands:
        if v>L: viol.append(((m,n,d),L,U,v,why))
for v in sorted(viol): print(v)
print('open entries:')
for k,v in opn: print(k,v, round(v[1]/v[0],2))
