import pylab as pl
import result
import numpy as np
import milanoReference
import string
import scipy.interpolate

colors=['k','b','g','r','c','m']
lines=['-','--','-.']
res=result.StatisticResult('results/milanoboron10')
#res=result.StatisticResult('results/milanotld')

E=map(float,res.dims[0])
r=map(float,res.dims[1])
detectors=res.dims[2]
pl.subplot(111, xscale="log", yscale="log")
i=1
for j in [0]:
	s=-1
	rate=[res.mean[k][j][i]*r[j]**2*np.pi/s for k in range(len(E))]

	std=[res.std[k][j][i]*r[j]**2*np.pi/abs(s) for k in range(len(E))]
	pE=[iE for iE,iRate in zip(E,rate) if str(iRate)!='nan']
	pRate=[iRate for iRate in rate if str(iRate)!='nan']
	pStd=[iStd for iStd,iRate in zip(std,rate) if str(iRate)!='nan']
	pl.errorbar(pE,pRate , yerr=pStd)
pl.ylim([0,3])
pl.ylabel('Response')
pl.xlabel('Beam energy [GeV]')
#pl.title('Errorbars $\pm\sigma$')
pl.show()

