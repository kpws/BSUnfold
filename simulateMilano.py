import simulate
import milanoReference
import numpy as np

#use last two spheres
names=milanoReference.names[-2:]

#name '2.0' means no sphere, the name is used because the beam has this size.
#Uncomment next line to use.
#names=['2.0']+milanoReference.names

E=[]
for i in range(len(milanoReference.E)):
	E.append(milanoReference.E[i])
	if i!=len(milanoReference.E)-1:
		E.append(np.sqrt(milanoReference.E[i]*milanoReference.E[i+1]))

E+=[1.0e-16,1.0e-14,1.0e-13,3.0e-13,1.0e-12,3.0e-12,1.0e-11,3e0]
rho=0.96
runs=6
partNum=2e6
detectors=['tld'] #['boron10','tld']
runNum=10 #We have 12 cpus

for d in detectors:
	simulate.simulate('milano'+d,runNum,runs,partNum, names[-2:],E,rho,d)
