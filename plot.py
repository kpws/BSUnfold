import pylab as pl
import result
import numpy as np
import milanoReference
import string

colors=[[0.7,0.2,0.2],'b','g','r','c','m','y','k']
lines=['-','-','-.']
lineI=0

pl.subplot(111, xscale="log", yscale="linear")

s=np.mean([sum(i) for i in milanoReference.rate])
for j in range(len(milanoReference.names)):
	pl.plot(milanoReference.E,[mr[j]/s for mr in milanoReference.rate],'o',
		label=(['CR39, MCNPX by M.Ferrarini']+['']*(len(milanoReference.names)-1))[j])
lineI+=1
for detectorName in ['boron10','tld']:
	
	res=result.StatisticResult('results/milano'+detectorName+'Total')

	E=map(float,res.dims[0])
	r=[n for n in res.dims[1]]
	r[-2]=milanoReference.r[r[-2]]
	r[-1]=milanoReference.r[r[-1]]
	detectors=res.dims[2]
	
	if detectorName=='boron10':
		i=detectors.index('neubal')
	elif detectorName=='tld':
		i6=detectors.index(6)	
		i7=detectors.index(7)	
	else: assert(False)
	rate=[]
	for j in range(1,len(r)):
		if detectorName=='boron10':
			rate.append([res.mean[k][j][i]*r[j]**2*np.pi for k in range(len(E))])
		elif detectorName=='tld':
			rate.append([(res.mean[k][j][i6]-res.mean[k][j][i7])*r[j]**2*np.pi for k in range(len(E))])
		else: assert(False)
		for k in range(len(rate[-1])):
			if str(rate[-1][k])=='nan':
				rate[-1][k]=0
	s=np.mean([np.sum(rate,axis=0)[ii] for ii in range(len(E)) if 1e-11<E[ii]<2e0])
	if detectorName=='boron10':
		label='CR39, FLUKA'
	elif detectorName=='tld':
		label='TLD, FLUKA'
	else: assert(False)
	for j in range(len(res.dims[1])):
		if detectorName=='boron10':
			pData=res.project([-1,j,i])
			pl.errorbar(pData[0],np.array(pData[1])*r[j]**2*np.pi/s , yerr=np.array(pData[2])*r[j]**2*np.pi/abs(s), fmt=lines[lineI],
			label=(['']+[label]+['']*(len(milanoReference.names)))[j],color=colors[j])	
		elif detectorName=='tld':
			#########################Fix for different number of Li-6 and Li-7 results, damn ugly###########
			pData6=[[iii for iii in ii] for ii in res.project([-1,j,i6])]
			pData7=[[iii for iii in ii] for ii in res.project([-1,j,i7])]
			ii=0
			while ii<min(len(pData6[0]),len(pData7[0])):
				if pData6[0][ii]!=pData7[0][ii]:
					if pData6[0][ii]<pData7[0][ii]:
						pData6[0].pop(ii)
						pData6[1].pop(ii)
						pData6[2].pop(ii)
						continue
					else:
						pData7[0].pop(ii)
						pData7[1].pop(ii)
						pData7[2].pop(ii)
						continue
				ii+=1
			if len(pData6[0])<len(pData7[0]):
				pData7[0]=pData7[0][:len(pData6[0])]
				pData7[1]=pData7[1][:len(pData6[1])]
				pData7[2]=pData7[2][:len(pData6[2])]
			if len(pData7[0])<len(pData6[0]):
				pData6[0]=pData6[0][:len(pData7[0])]
				pData6[1]=pData6[1][:len(pData7[1])]
				pData6[2]=pData6[2][:len(pData7[2])]
			####################################End fix#################################################
			pl.errorbar(pData6[0],(np.array(pData6[1])-np.array(pData7[1]))*r[j]**2*np.pi/s , yerr=np.sqrt(np.array(pData6[2])**2+np.array(pData6[2])**2 )*r[j]**2*np.pi/abs(s), fmt=lines[lineI],
			label=(['']+[label]+['']*(len(milanoReference.names)))[j],color=colors[j])
		else: assert(False)
	lineI+=1
pl.legend(loc=2)
pl.ylabel('Normalized response')
pl.xlabel('Beam energy [GeV]')
pl.title('Errorbars $\pm\sigma$')
pl.ylim([0,0.7])
pl.show()

