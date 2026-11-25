# usage: python expand2.py q n r D.txt S.txt out.txt   (S rows = r-digit syndromes)
import sys, itertools, numpy as np
q,n,r=map(int,sys.argv[1:4]); D=np.loadtxt(sys.argv[4],dtype=np.int64).reshape(r,n-r); S=np.loadtxt(sys.argv[5],dtype=np.int64).reshape(-1,r)
T=np.array(list(itertools.product(range(q),repeat=n-r)),dtype=np.int64)
words=set()
for y in S:
    X=np.concatenate([(y[None,:]-T@D.T)%q,T],axis=1)
    for x in X: words.add("".join(map(str,x)))
open(sys.argv[6],"w").write("\n".join(sorted(words))+"\n"); print(len(words))
