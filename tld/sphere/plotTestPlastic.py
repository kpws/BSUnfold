import pylab as pl
import csv
import numpy as np
import milanoReference
import scipy.interpolate

def plot(name='testPlastic',ls='-'):
	Ei1=7
	Ei2=14
	
	allrho=[]
	allr=[]
	allRate1Mean=[]
	allRate2Mean=[]
	allRate1Std=[]
	allRate2Std=[]
	reader=csv.reader(open('results/'+name, 'rb'), delimiter='\t')
	reader.next()
	for row in reader:
		allrho.append(float(row[0]))
		allr.append(float(row[1]))
		n=(len(row)-2)/2
		rate1=map(float,row[2:n+1])
		rate2=map(float,row[n+2:])
		allRate1Mean.append(np.mean(rate1))
		allRate2Mean.append(np.mean(rate2))
		allRate1Std.append(np.std(rate1)/np.sqrt(n))
		allRate2Std.append(np.std(rate2)/np.sqrt(n))
	rho=[allrho[0]]
	r=[allr[0]]
	for i in range(len(allrho)):
		if rho[-1]<allrho[i]:
			rho.append(allrho[i])
		if r[-1]<allr[i]:
			r.append(allr[i])
	
	foldAndNormalize=lambda l:np.array([[ l[j+len(rho)*i]*r[i]**2 for j in range(len(rho))] for i in range(len(r))])
	[rate1Mean,rate2Mean,rate1Std,rate2Std]=map(foldAndNormalize,[allRate1Mean,allRate2Mean,allRate1Std,allRate2Std])
	ratio=rate1Mean/rate2Mean
	ratioStd=np.sqrt((rate1Std/rate2Mean)**2+(rate2Std*rate1Mean/rate2Mean**2)**2)
	pl.hold(True)
	nstd=1
	colors=['b','g','r','c','m']
	#pl.title('Errorbars $\pm '+str(nstd)+'\sigma$')
	intRhos=[]
	for i in range(len(r)):
		pl.errorbar(rho ,ratio[i], yerr=ratioStd[i], fmt=ls+colors[i],label='r='+str(r[i])+' cm')
		refRatio=milanoReference.rate[Ei1][i]/milanoReference.rate[Ei2][i]
		pl.plot([rho[0],rho[-1]],[refRatio]*2,colors[i])
		if i<666:
			spl = scipy.interpolate.splrep(-ratio[i][:10],rho[:10])
			intRhos.append(scipy.interpolate.splev(-refRatio, spl))
			pl.plot([intRhos[-1]]*2,[refRatio-0.1,refRatio+0.1],colors[i])
	meanRho=np.mean(intRhos)
	pl.plot([meanRho]*2,[0,3],'k--',label='Mean intersection rho\nAt '+'%1.2f'%meanRho+' $\mathrm{g}/\mathrm{cm}^3$')
	print('Mean intersection rho: '+str(meanRho))
	pl.legend(loc=1)
	pl.ylabel('Ratio')
	pl.xlabel('$rho [g/cm^3]$')
	pl.xlim([0.4,1.2])
	
if __name__=="__main__":
	pl.subplot(111, xscale="linear", yscale="linear")
	plot()
	pl.show()

