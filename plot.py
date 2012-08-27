import pylab as pl
import result
import numpy as np
import milanoReference
import string
from beamRadii import beamRadii

colors=[[0.7,0.2,0.2],'b','g','r','c','m','y','k']
lines=['-','-','-.']
lineI=0

pl.subplot(111, xscale="log", yscale="linear")

s=np.mean([np.sum(i) for i in milanoReference.rate])
for j in range(len(milanoReference.names)):
	pl.plot(milanoReference.E,[mr[j]/s for mr in milanoReference.rate],'o',
		label=(['CR39, MCNPX by M.Ferrarini']+['']*(len(milanoReference.names)-1))[j])
lineI+=1
for detectorName in ['boron10','tld']:
    s=0
    for getS in [True,False]:
        res=result.StatisticResult('results/milano'+detectorName+'Total')
        if detectorName=='boron10':
            label='CR39, FLUKA'
        elif detectorName=='tld':
            label='TLD, FLUKA'
        else: assert(False)
        for j in range(len(res.dims[1])):
            r=beamRadii[str(res.dims[1][j])]
            if detectorName=='boron10':
                i=res.dims[2].index('alpha')
                pData=res.project([-1,j,i])
                E=pData[0]
                rate=np.array(pData[1])*r**2*np.pi 
                error=np.array(pData[2])*r**2*np.pi
            elif detectorName=='tld':
                i6=res.dims[2].index(6)
                i7=res.dims[2].index(7)
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
                E=pData6[0]
                rate=(np.array(pData6[1])-np.array(pData7[1]))*r**2*np.pi
                error=np.sqrt(np.array(pData6[2])**2+np.array(pData6[2])**2 )*r**2*np.pi
            else: assert(False)
            if getS:
                if j!=0:
                    s+=np.mean([rate[ii] for ii in range(len(E)) if milanoReference.E[0]<=E[ii]<=milanoReference.E[-1]])
            else:
                pl.errorbar(E, rate/s, yerr=error/abs(s), fmt=lines[lineI], 
                    label=(['']+[label]+['']*(len(milanoReference.names)))[j],color=colors[j])
    lineI+=1
pl.legend(loc=2)
pl.ylabel('Normalized response')
pl.xlabel('Beam energy [GeV]')
pl.title('Errorbars $\pm\sigma$')
pl.ylim([0,0.5])
pl.show()

