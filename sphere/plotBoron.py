import pylab as pl
import csv
import numpy as np

def plot(name='default',ls='-'):
	E=[]
	allE=[]
	allr=[]
	allRateMean=[]
	allRateStd=[]
	reader=csv.reader(open('results/'+name, 'rb'), delimiter='\t')
	reader.next()
	for row in reader:
		allE.append(float(row[0]))
		allr.append(float(row[1]))
		n=len(row)-2
		rate=map(lambda a:-float(a),row[2:])
		allRateMean.append(np.mean(rate))
		allRateStd.append(np.std(rate)/np.sqrt(n))
	E=[allE[0]]
	r=[allr[0]]
	for i in range(len(allE)):
		if E[-1]!=allE[i]:
			E.append(allE[i])
		if r[-1]<allr[i]:
			r.append(allr[i])
	
	foldAndNormalize=lambda l:np.array([[ l[i+len(r)*j]*r[i]**2 for j in range(len(E))] for i in range(len(r))])
	[rateMean,rateStd]=map(foldAndNormalize,[allRateMean,allRateStd])
	pl.hold(True)
	nstd=1
	for i in range(len(r)):
		pl.errorbar(E, rateMean[i], yerr=rateStd[i]*nstd, fmt=ls,label='r='+str(r[i])+' cm')
	pl.legend(loc=2)
	pl.xlabel('Beam energy [GeV]')
	pl.ylabel('Absorbed n / (incidence per cm^2)')
	
if __name__=="__main__":
    plot()
    pl.show()

