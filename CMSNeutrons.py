import pylab as pl
import csv
import numpy as np

#cm
r1 = 220
r2 = 270
z1 = 1390
z2 = 1433

def removeSpaces(l): return [i for i in l if not i is '']

data=[[]]
reader=csv.reader(open('data/CMSpp_usrtrack_21_tab.lis', 'rb'), delimiter=' ')
for row in reader:
	row=removeSpaces(row)
	if len(row)==0:
		if data[-1]!=[]:
			data.append([])
		continue
	if '#' in row[0]:
		continue
	data[-1].append(map(float,row))

VRing=(z2-z1)*(r2**2-r1**2)*np.pi
VSmall=VRing*np.arctan(1.0/2)/np.pi
VBig=VRing-VSmall
V=[VSmall,VBig]*2

E=[[(d[0], d[1]) for d in i] for i in data]
fluence=[[d[2]/V[i] for d in data[i]] for i in range(len(data))]
relStd=[[d[3] for d in i] for i in data]

EMean=[]
fluenceMean=[]
n=3
for k in range(len(E)):
	EMean.append([])
	fluenceMean.append([])
	i=0
	while i+n<=len(E[k]):
		EMean[k].append((E[k][i][0],E[k][i+n-1][1]))
		fluenceMean[k].append(sum(fluence[k][i+j]*(E[k][i+j][1]-E[k][i+j][0]) for j in range(n))/(EMean[k][-1][1]-EMean[k][-1][0]))
		i+=n

for e1 in E:
	for e2 in E:
		assert(e1==e2)
	
fluenceAll=[sum(fluence[j][i]*V[j] for j in range(len(fluence)))/(2*VRing) for i in range(len(fluence[0]))]
fluenceAllMean=[sum(fluenceMean[j][i]*V[j] for j in range(len(fluence)))/(2*VRing) for i in range(len(fluenceMean[0]))]
crossSection=73.5e-3*1e15 #fb
def fluence(e):
	for i in range(len(E[0])):
		if E[0][i][0] <= e <= E[0][i][1]:
			return fluenceAll[i]*crossSection
	return 0.0
	#raise Exception('Neutron fluence at energy '+str(e)+' GeV has not been calculated.')
	
ERange=(  min(E[0][i][0] for i in range(len(E[0])) if fluenceAll[i]!=0.0)  ,
		  max(E[0][i][1] for i in range(len(E[0])) if fluenceAll[i]!=0.0))

if __name__ == "__main__":
	pl.hold(True)
	#for i in range(len(data)):
	#	pl.loglog([(e[0]+e[1])/2 for e in E[i]],fluence[i],label=str(i))


	#for i in range(len(data)):
	#	pl.loglog([(e[0]+e[1])/2 for e in EMean[i]],fluenceMean[i],label=str(i))

	#pl.loglog([(e[0]+e[1])/2 for e in E[0]],fluenceAll)
	#pl.loglog([(e[0]+e[1])/2 for e in EMean[0]],fluenceAllMean)
	
	pl.loglog([EMean[0][i/2][i%2] for i in range(2*len(fluenceAllMean))], [crossSection*fluenceAllMean[i/2] for i in range(2*len(fluenceAllMean))])
	pl.legend()
	pl.xlabel('$E$ [GeV]')
	pl.ylabel('$\phi(E)$ [$(\mathrm{fb}^{-1}\ \mathrm{cm}^{2}\mathrm{GeV})^{-1}$]')
	pl.grid()
	pl.show()
