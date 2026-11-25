import sys
path,m,n=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
W=[tuple(int(c) for c in l.strip()) for l in open(path) if l.strip()]
S=set(W)
mod=[2]*m+[3]*n
def sub(a,b): return tuple((x-y)%q for x,y,q in zip(a,b,mod))
def add(a,b): return tuple((x+y)%q for x,y,q in zip(a,b,mod))
w0=W[0]
stab=[]
for w in W:
    t=sub(w,w0)
    if all(add(x,t) in S for x in W): stab.append(t)
print(path,'|C|=',len(W),'Translationsstabilisator:',len(stab))
for t in stab[:30]: print(''.join(map(str,t)), 'wt',sum(1 for x in t if x))
