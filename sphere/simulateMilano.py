import simulate
import milanoReference
import numpy as np

r=[2.0]+milanoReference.r
E=[]
for i in range(len(milanoReference.E)):
	E.append(milanoReference.E[i])
	if i!=len(milanoReference.E)-1:
		E.append(np.sqrt(milanoReference.E[i]*milanoReference.E[i+1]))
rho=0.96
runs=4
partNum=1e6
detectors=['boron10','tld']

for d in detectors:
	simulate.simulate('milano'+d,runs,partNum, r,E,rho,d)

