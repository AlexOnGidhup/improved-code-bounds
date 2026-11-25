from closure import closure,INF
tab={}
def put(R,d):
    for n,v in d.items(): tab[(n,R)]=v
put(1,{1:1,2:6,3:18,4:72,5:414,6:1840,7:11040,8:62208,9:324864,10:1866240})
put(2,{2:1,3:6,4:15,5:66,6:274,7:1296,8:5184,9:29808,10:132480})
put(3,{3:1,4:6,5:12,6:41,7:246,8:1080,9:4752,10:19347})
put(4,{4:1,5:6,6:10,7:36,8:216,9:738,10:2952})
put(5,{5:1,6:6,7:6,8:30,9:144,10:615})
put(6,{6:1,7:6,8:6,9:22,10:72})
put(7,{7:1,8:6,9:6,10:18})
put(8,{8:1,9:6,10:6})
base=dict(tab)
mar={(7,3):227,(8,3):1005,(8,4):166,(9,4):660,(9,5):119,(10,4):2751,(10,5):484}
for k,v in mar.items(): tab[k]=min(tab[k],v)
U0,o0,h0=closure(dict(tab),10,8,6)
print('closure of Kéri+Marosi (no 216):',[ (k,o0[k],U0[k],h0[k]) for k in U0 if U0[k]<o0.get(k,INF)])
tab[(6,2)]=216
U,o,h=closure(dict(tab),10,8,6)
for k in sorted(U):
    if U[k]<o.get(k,INF): print(k,o[k],'->',U[k],h[k])
