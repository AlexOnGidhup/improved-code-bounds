import re,itertools
from parse2 import rows
INF=10**18
def build_bin(N=33,Rm=10):
    U={}
    for R in range(1,Rm+1):
        for n in range(1,N+1):
            if n<=R: U[(n,R)]=1
            elif n<=2*R+1: U[(n,R)]=2
            elif n==2*R+2: U[(n,R)]=4
            elif n==2*R+3: U[(n,R)]=7
    # hand exact
    U.update({(7,1):16,(8,1):32,(9,1):62,(15,1):2048,(16,1):4096,(31,1):2**26,(32,1):2**27,
              (8,2):12,(9,2):16,(10,3):12,(11,3):16,(12,4):12,(13,4):16,(23,3):4096,
              (6,1):12,(14,5):12,(15,5):16,(16,6):12,(17,6):16,(18,7):12,(19,7):16,(20,8):12,(21,8):16,(22,9):12,(23,9):16,(24,10):12,(25,10):16})
    for (cols,n),cells in rows.items():
        if n<10: continue
        for R,(lo,hi) in zip(cols,cells):
            if hi is not None and n<=N: U.setdefault((n,R),hi); U[(n,R)]=min(U[(n,R)],hi) if (n,R) in U else hi
    return U
def tableU(U):  # original upper bounds as published
    return dict(U)
def closure(U,N,Rm,q):
    U=dict(U); orig=dict(U); changed=True; hist={}
    def g(n,R):
        if R>=n: return 1
        if R<=0: return q**n
        return U.get((n,R),INF)
    while changed:
        changed=False
        for n in range(1,N+1):
            for R in range(1,Rm+1):
                cands={}
                cands['mono R']=g(n,R+1) if False else INF
                cands['R-1']=g(n,R-1) if R>1 else INF
                cands['n+1']=g(n+1,R) if n+1<=N else INF
                cands['q*(n-1)']=q*g(n-1,R) if n>1 else INF
                cands['(n-1,R-1)']=g(n-1,R-1) if n>1 and R>1 else INF
                for n1 in range(1,n):
                    n2=n-n1
                    for R1 in range(0,R+1):
                        R2=R-R1
                        a=g(n1,R1) if R1>0 else q**n1
                        b=g(n2,R2) if R2>0 else q**n2
                        if a<INF and b<INF: cands[('ds',n1,R1,n2,R2)]=a*b
                best=min(cands.items(),key=lambda kv:kv[1])
                if best[1]<g(n,R) and not (R>=n):
                    U[(n,R)]=best[1]; hist[(n,R)]=best[0]; changed=True
    return U,orig,hist
if __name__=='__main__':
    U=build_bin()
    V,orig,hist=closure(U,33,10,2)
    for k in sorted(V):
        if V[k]<orig.get(k,INF): print(k,orig.get(k),'->',V[k],hist[k])
    # missing cells
    miss=[(n,R) for n in range(1,34) for R in range(1,11) if (n,R) not in V and R<n]
    print('missing',miss[:30])
