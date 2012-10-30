import csv
import numpy as np
r=csv.reader(open('expData/cms1_tld.csv'))

for i in range(8):
    r.next()

types=r.next()[2:]
typeorder=[0,1,1,0]
typenames=['TLD-600','TLD-700']
for i in range(4):
    assert(types[i]==typenames[typeorder[i]])

r.next()
raw=dict()

for i in r:
    raw[i[1]]=map(float,i[2:6])

resp67=dict([(k,[(lambda a:[np.mean(a),np.std(a)/np.sqrt(len(a))])([raw[k][i] for i in range(4) if typeorder[i]==t]) for t in [0,1]]) for k in raw.keys()])
respAll=dict([(k,[resp67[k][0][0]-resp67[k][1][0],np.sqrt(resp67[k][0][1]**2+resp67[k][1][1]**2)]) for k in resp67.keys()])

resp=zip(*[respAll['20'+str(i)+' / Moderator'] for i in range(1,7)])
order=[4.05, 5.4, 6.65, 8.9, 11.65, 'Linus']
if __name__=='__main__':
    print resp
