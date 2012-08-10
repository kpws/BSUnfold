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
for j in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[mr[j]/s for mr in milanoReference.rate],'-o',
		label=(['CR39, MCNPX by M.Ferrarini']+['']*(len(milanoReference.r)-1))[j])
lineI+=1
for detectorName in ['boron10','tld']:
	
	res=result.StatisticResult('results/milano'+detectorName)

	E=map(float,res.dims[0])
	r=map(float,res.dims[1])
	detectors=res.dims[2]
	
	if detectorName=='boron10':
		i=detectors.index('neubal')
	if detectorName=='tld':
		i6=detectors.index(6)	
		i7=detectors.index(7)	
	rate=[]
	std=[]
	for j in range(1,len(r)):
		if detectorName=='boron10':
			rate.append([res.mean[k][j][i]*r[j]**2*np.pi for k in range(len(E))])
			std.append([res.std[k][j][i]*r[j]**2*np.pi for k in range(len(E))])
		if detectorName=='tld':
			rate.append([(res.mean[k][j][i6]-res.mean[k][j][i7])*r[j]**2*np.pi for k in range(len(E))])
			std.append([np.sqrt(res.std[k][j][i6]**2+res.std[k][j][i7]**2)*r[j]**2*np.pi for k in range(len(E))])
		for k in range(len(rate[-1])):
			if str(rate[-1][k])=='nan':
				rate[-1][k]=0
	s=np.mean(np.sum(rate,axis=0))
	if detectorName=='boron10':
		label='CR39, FLUKA'
	if detectorName=='tld':
		label='TLD, FLUKA'
	for j in range(len(rate)):
		pl.errorbar(E,np.array(rate[j])/s , yerr=np.array(std[j])/abs(s), fmt=lines[lineI]+colors[j+1],
		label=([label]+['']*(len(milanoReference.r)-1))[j])		
	lineI+=1
pl.legend(loc=2)
pl.ylabel('Normalized response')
pl.xlabel('Beam energy [GeV]')
pl.title('Errorbars $\pm\sigma$')
pl.ylim([0,0.7])
pl.show()

