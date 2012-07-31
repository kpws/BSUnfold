import simulate
import milanoReference

r=[2.0]+milanoReference.r
E=milanoReference.E
rho=0.96
runs=4
partNum=1e6
detectors=['boron10','tld']

for d in detectors:
	simulate.simulate('milano'+d,runs,partNum, r,E,rho,d)

