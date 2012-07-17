import pylab as pl
import result
import numpy as np


res=result.StatisticResult('milanoB')

E=map(float,res.dims[0])
r=map(float,res.dims[1])
detectors=res.dims[2]

for i in range(len(detectors)):
	pl.subplot(121+i, xscale="log", yscale="linear")
	for j in range(len(r)):
		if i==0:
			rate=[-res.mean[k][j][i]*(2*r[j])**2 for k in range(len(E))] 
			std=[res.std[k][j][i]*(2*r[j])**2 for k in range(len(E))]
		elif i==1:
			rate=[res.mean[k][j][i]*(2*r[j])**2 for k in range(len(E))] 
			std=[res.std[k][j][i]*(2*r[j])**2 for k in range(len(E))]
		pl.errorbar(E,rate , yerr=std,label='r='+str(r[j])+' cm')
	#pl.legend(loc=2)
	#pl.ylabel('Energy / (incidence per cm^2) [GeV]')
	pl.xlabel('Beam energy [GeV]')
	pl.title(detectors[i]+', errorbars $\pm\sigma$')

pl.show()

