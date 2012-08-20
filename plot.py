import pylab as pl
import result
import numpy as np
import milanoReference
import string

colors=['k','b','g','r','c','m']
lines=['-','--','-.']
lineI=0

pl.subplot(111, xscale="log", yscale="linear")

s=np.mean([sum(i) for i in milanoReference.rate])
for j in range(len(milanoReference.names)):
	pl.plot(milanoReference.E,[mr[j]/s for mr in milanoReference.rate],'-o',
		label=(['CR39, MCNPX by M.Ferrarini']+['']*(len(milanoReference.names)-1))[j])
lineI+=1
for detectorName in ['boron10']:#,'tld']:
	
	res=result.StatisticResult('results/milano'+detectorName)#+'Total')

	E=map(float,res.dims[0])
	r=[milanoReference.r[n] for n in res.dims[1]]
	detectors=res.dims[2]
	
	if detectorName=='boron10':
		i=detectors.index('alpha')
	elif detectorName=='tld':
		i6=detectors.index(6)	
		i7=detectors.index(7)	
	else: assert(False)
	rate=[]
	std=[]
	for j in range(0,len(r)):
		if detectorName=='boron10':
			rate.append([res.mean[k][j][i]*r[j]**2*np.pi for k in range(len(E))])
			std.append([res.std[k][j][i]*r[j]**2*np.pi for k in range(len(E))])
		elif detectorName=='tld':
			rate.append([(res.mean[k][j][i6]-res.mean[k][j][i7])*r[j]**2*np.pi for k in range(len(E))])
			std.append([np.sqrt(res.std[k][j][i6]**2+res.std[k][j][i7]**2)*r[j]**2*np.pi for k in range(len(E))])
		else: assert(False)
		for k in range(len(rate[-1])):
			if str(rate[-1][k])=='nan':
				rate[-1][k]=0
	s=4e-6#np.mean([np.sum(rate,axis=0)[i] for i in range(len(E)) if 1e-11<E[i]<2e0])*12
	if detectorName=='boron10':
		label='CR39, FLUKA'
	elif detectorName=='tld':
		label='TLD, FLUKA'
	else: assert(False)
	for j in range(len(rate)):
		pl.errorbar(E,np.array(rate[j])/s , yerr=np.array(std[j])/abs(s), fmt=lines[lineI]+colors[j+1],
		label=([label]+['']*(len(milanoReference.names)-1))[j])		
	lineI+=1
pl.legend(loc=2)
pl.ylabel('Normalized response')
pl.xlabel('Beam energy [GeV]')
pl.title('Errorbars $\pm\sigma$')
pl.ylim([0,0.7])
pl.show()

