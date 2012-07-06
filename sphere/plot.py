import pylab as pl
import csv
import numpy as np

def plot(name='default'):
	E=[]
	allE=[]
	allr=[]
	allRate6Mean=[]
	allRate7Mean=[]
	allRate6Std=[]
	allRate7Std=[]
	reader=csv.reader(open('results/'+name, 'rb'), delimiter='\t')
	reader.next()
	for row in reader:
		allE.append(float(row[0]))
		allr.append(float(row[1]))
		n=(len(row)-2)/2
		rate6=map(float,row[2:n+1])
		rate7=map(float,row[n+2:])
		allRate6Mean.append(np.mean(rate6))
		allRate7Mean.append(np.mean(rate7))
		allRate6Std.append(np.std(rate6)/np.sqrt(n))
		allRate7Std.append(np.std(rate7)/np.sqrt(n))
	E=[allE[0]]
	r=[allr[0]]
	for i in range(len(allE)):
		if E[-1]!=allE[i]:
			E.append(allE[i])
		if r[-1]<allr[i]:
			r.append(allr[i])
	
	foldAndNormalize=lambda l:np.array([[ l[i+len(r)*j]*r[i]**2 for j in range(len(E))] for i in range(len(r))])
	[rate6Mean,rate7Mean,rate6Std,rate7Std]=map(foldAndNormalize,[allRate6Mean,allRate7Mean,allRate6Std,allRate7Std])
	neutronRateMean=rate6Mean-rate7Mean
	neutronRateStd=np.sqrt(rate6Std**2+rate7Std**2)
	pl.hold(True)
	nstd=3
	pl.subplot(111, xscale="log", yscale="linear")
	pl.title('Errorbars $\pm '+str(nstd)+'\sigma$')
	for i in range(len(r)):
		pl.errorbar(E, neutronRateMean[i], yerr=neutronRateStd[i]*nstd, fmt='-',label='r='+str(r[i])+' cm')
		#pl.errorbar(E, rate7Mean[i], yerr=rate7Std[i]*nstd, fmt='g-',label='$\pm '+str(nstd)+'\sigma$, r='+str(r[i]))
	pl.legend(loc=2)
	pl.xlabel('Beam energy [GeV]')
	pl.ylabel('Energy / incidence in cm^2[GeV]')
	pl.show()

if __name__=="__main__":
    plot()

