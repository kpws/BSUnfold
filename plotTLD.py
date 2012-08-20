import pylab as pl
import result
import numpy as np
import milanoReference
import string
import scipy.interpolate

colors=['k','b','g','r','c','m']
lines=['-','--','-.']
res=result.StatisticResult('results/milanotld')
#res=result.StatisticResult('results/milanotld')

E=map(float,res.dims[0])
r=[milanoReference.r[n] for n in res.dims[1]]
detectors=res.dims[2]
pl.subplot(111, xscale="log", yscale="log")
for i in [0,1]:
	for j in [0]:
		print res.project([-1,j,i])
		E,rate,std= res.project([-1,j,i])
		
		rate=[rate[k]*r[j]**2*np.pi for k in range(len(E))]
		std=[std[k]*r[j]**2*np.pi for k in range(len(E))]
		
		
		pl.errorbar(E,rate , yerr=std,label=['$^6$Li','$^7$Li'][i])
		
pl.plot(E,(np.array(E)+4.78e-3)*(2*0.15875)**2,label='Reaction product energy times detector area')
#pl.ylim([0,3])	
pl.legend(loc=0)
pl.ylabel('Dose rate per flux [GeVcm$^2$]')
pl.xlabel('Beam energy [GeV]')
#pl.title('Errorbars $\pm\sigma$')
pl.show()
