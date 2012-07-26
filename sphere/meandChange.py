import milanoReference
import numpy as np

s1=2.
s2=2.5
print(1./3*(np.sqrt(2)+np.log(1+np.sqrt(2))))

for i in range(len(milanoReference.r)):
	r=milanoReference.r[i]
	print(str(r)+
	'&%1.2f'%(r-1./3*(np.sqrt(2)+np.log(1+np.sqrt(2)))*s1/2)+
	'&%1.2f'%(r-1./3*(np.sqrt(2)+np.log(1+np.sqrt(2)))*s2/2 )+
	'&%1.2f'%(   ((r-1./3*(np.sqrt(2)+np.log(1+np.sqrt(2)))*s1/2)-(r-1./3*(np.sqrt(2)+np.log(1+np.sqrt(2)))*s2/2))
	/ ((r-1./3*(np.sqrt(2)+np.log(1+np.sqrt(2)))*s1/2)-(milanoReference.r[i-1]-1./3*(np.sqrt(2)+np.log(1+np.sqrt(2)))*s1/2))   )+
	'\\\\')
