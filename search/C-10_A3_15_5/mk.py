import numpy as np, itertools
G=np.load('bestG_3_15_5_k6_8748.npy'); S=np.load('best_3_15_5_k6_8748.npy')
k,n=G.shape; m=n-k
msgs=np.array(list(itertools.product(range(3),repeat=k)),dtype=np.int64)
C0=(msgs@G)%3
words=[]
for s in S:
    dig=[(int(s)//3**i)%3 for i in range(m)]
    lead=np.array([0]*k+dig,dtype=np.int64)
    words.append((C0+lead)%3)
W=np.concatenate(words)
print(W.shape)
np.savetxt('code_3_15_5_8748.txt',W,fmt='%d',delimiter='')
