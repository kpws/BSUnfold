import pylab as pl
import result
import numpy as np
import milanoReference
import string
import scipy.interpolate

colors=['k','b','g','r','c','m']
lines=['-','--','-.']
res=result.StatisticResult('responses/milanoboron10')

E=map(float,res.dims[0])
r=map(float,res.dims[1])
detectors=res.dims[2]
print detectors
pl.subplot(111, xscale="log", yscale="log")
i=detectors.index('alpha')
for j in [0,1,2,3,4,5]:
	s=1
	E,rate,std=res.project([-1,j,i])
	rate=[res.mean[k][j][i]*r[j]**2*np.pi/s for k in range(len(E))]
	std=[res.std[k][j][i]*r[j]**2*np.pi/abs(s) for k in range(len(E))]

	pl.errorbar(E,rate , yerr=std)
pl.ylim([0,3])
pl.ylabel('Response')
pl.xlabel('Beam energy [GeV]')
#pl.title('Errorbars $\pm\sigma$')
pl.show()

