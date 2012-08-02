import pylab as pl
import result
import numpy as np
import milanoReference
import string

colors=['k','b','g','r','c','m']
lines=['-','-.','--']
res=result.StatisticResult('results/milanoboron10')

E=map(float,res.dims[0])
r=map(float,res.dims[1])
detectors=res.dims[2]
pl.subplot(111, xscale="log", yscale="linear")

s=np.mean([sum(i) for i in milanoReference.rate])
for j in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[mr[j]/s for mr in milanoReference.rate],'-o',
		label=(['Absorbtions, MCNPX by M.Ferrarini']+['']*100)[j])

for i in [detectors.index('neubal')]: #range(len(detectors)):
	s=0
	for j in range(1,len(r)):
		rate=[res.mean[k][j][i]*r[j]**2*np.pi for k in range(len(E))]
		for k in range(len(rate)):
			if str(rate[k])=='nan':
				rate[k]=0
		s+=np.mean(rate)
	for j in range(1,len(r)):
		rate=[res.mean[k][j][i]*r[j]**2*np.pi/s for k in range(len(E))]
		for k in range(len(rate)):
			if str(rate[k])=='nan':
				rate[k]=0
		std=[res.std[k][j][i]*r[j]**2*np.pi/abs(s) for k in range(len(E))]
		pl.errorbar(E,rate , yerr=std, fmt=lines[i+1]+colors[j],
		label=(['',string.capwords(detectors[i])+', FLUKA']+['']*100)[j])		
		
pl.legend(loc=2)
pl.ylabel('Normalized response')
pl.xlabel('Beam energy [GeV]')
pl.title('Errorbars $\pm\sigma$')
pl.show()

