import pylab as pl
import result
import numpy as np
import milanoReference
import string

colors=['b','g','r','c','m']
lines=['-','--','-.']
res=result.StatisticResult('milanoB')

E=map(float,res.dims[0])
r=map(float,res.dims[1])
detectors=res.dims[2]
pl.subplot(111, xscale="log", yscale="linear")

s=sum(sum(i) for i in milanoReference.rate)
for j in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[mr[j]/s for mr in milanoReference.rate],'-o',
		label=(['Absorbtions, MCNPX by M.Ferrarini']+['']*100)[j])

for i in range(len(detectors)):
	s=0
	for j in range(len(r)):
		s+=sum(res.mean[k][j][i]*(2*r[j])**2 for k in range(len(E)))
	for j in range(len(r)):
		rate=[res.mean[k][j][i]*(2*r[j])**2/s for k in range(len(E))]

		std=[res.std[k][j][i]*(2*r[j])**2/abs(s) for k in range(len(E))]
		pl.errorbar(E,rate , yerr=std, fmt=lines[i+1]+colors[j],
		label=([string.capwords(detectors[i])+', FLUKA']+['']*100)[j])		
		
pl.legend(loc=2)
pl.ylabel('Normalized response')
pl.xlabel('Beam energy [GeV]')
pl.title('Errorbars $\pm\sigma$')
pl.show()

