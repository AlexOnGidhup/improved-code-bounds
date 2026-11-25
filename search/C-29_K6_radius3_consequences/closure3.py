from closure import closure,INF
R1=[1,3,5,9,27,73,186,486,1269,3645,9477,27702,59049,177147]
R2=[1,1,3,3,8,17,34,81,219,555,729,2187,6561,19683]
R3=[1,1,1,3,3,8,12,27,54,105,243,657,1215,2187]
tab={}
for R,L in ((1,R1),(2,R2),(3,R3)):
    for i,v in enumerate(L): tab[(i+1,R)]=v
rows2={4:[1],5:[3,1],6:[3,3,1],7:[3,3,3,1],8:[9,3,3,3,1],9:[18,6,3,3,3],10:[36,12,3,3,3],11:[81,27,9,3,3],12:[175,54,18,6,3],13:[335,108,36,12,3],14:[729,243,81,27,9]}
for n,L in rows2.items():
    for j,v in enumerate(L): tab[(n,4+j)]=v
# n<=R -> 1 for all R handled in g
U,orig,hist=closure(tab,14,8,3)
for k in sorted(U):
    if U[k]<orig.get(k,INF): print(k,orig.get(k),'->',U[k],hist[k])
print('done',len(U))
