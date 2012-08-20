import simulate
import milanoReference
import numpy as np

#names=['2.0']+milanoReference.names
names=milanoReference.names[-2:]
E=[]
for i in range(len(milanoReference.E)):
	E.append(milanoReference.E[i])
	if i!=len(milanoReference.E)-1:
		E.append(np.sqrt(milanoReference.E[i]*milanoReference.E[i+1]))

E+=[1.0e-16,1.0e-14,1.0e-13,3.0e-13,1.0e-12,3.0e-12,1.0e-11,3e0,1e1,3e1,1e2]
rho=0.96
runs=6
partNum=2e6
detectors=['tld']
runNum=8 #We have 12 cpus

for d in detectors:
	simulate.simulate('milanoOnlyTld',runNum,runs,partNum, names[-2:],E,rho,d)

#['4.0','81+lead','Linus']
#for d in detectors:
#	simulate.simulate('test'+d,3,1,1e4,['Linus'] ,[5e-1],rho,d)
