import json
T={tuple(map(int,k.split(','))):tuple(v) for k,v in json.load(open('table23.json')).items()}
def lb(m,n,d):
    return T.get((m,n,d),(None,))[0] if m>=0 and n>=0 else None
out=[]
for (m,n,d),(L,U) in sorted(T.items(),key=lambda x:(x[0][2],x[0][0]+x[0][1],x[0][0])):
    if L==U: continue
    c=[]
    def add(v,why):
        if v is not None: c.append((v,why))
    x=lb(m+1,n-1,d); add(x,'embed(%d,%d)'%(m+1,n-1))
    x=lb(m-1,n+1,d); add(None if x is None else -(-2*x//3),'2/3 of (%d,%d)'%(m-1,n+1))
    x=lb(m+1,n,d); add(None if x is None else -(-x//2),'shortbin')
    x=lb(m,n+1,d); add(None if x is None else -(-x//3),'shortter')
    x=lb(m+1,n,d+1); add(x,'puncbin')
    x=lb(m,n+1,d+1); add(x,'puncter')
    x=lb(m-1,n,d); add(x,'padbin')
    x=lb(m,n-1,d); add(x,'padter')
    x=lb(m-2,n+1,d); add(x,'ter->2bin(%d,%d)'%(m-2,n+1))
    best=max(c) if c else (0,'')
    if best[0]>=L and m>0 and n>0:
        out.append(((m,n,d),L,U,best[1], 2**m*3**n))
for o in out: print(o)
