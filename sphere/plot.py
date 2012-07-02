import pylab as pl
import csv
import numpy as np

def plot(name='default'):
	E=[]
	rate6mean=[]
	rate7mean=[]
	rate6std=[]
	rate7std=[]
	reader=csv.reader(open('results/'+name, 'rb'), delimiter='\t')
	reader.next()
	for row in reader:
		E.append(float(row[0]))
		n=(len(row)-1)/2
		rate6=map(float,row[1:n+1])
		rate7=map(float,row[n+1:])
		rate6mean.append(np.mean(rate6))
		rate7mean.append(np.mean(rate7))
		rate6std.append(np.std(rate6)/np.sqrt(n))
		rate7std.append(np.std(rate7)/np.sqrt(n))
	
	pl.hold(True)
	nstd=3
	pl.subplot(111, xscale="log", yscale="log") 
	pl.errorbar(E, rate6mean, yerr=np.array(rate6std)*nstd, fmt='-',label='Li6F $\pm '+str(nstd)+'\sigma$')
	pl.errorbar(E, rate7mean, yerr=np.array(rate7std)*nstd, fmt='-',label='Li7F $\pm '+str(nstd)+'\sigma$')
	pl.legend(loc=4)
	pl.xlabel('Beam energy [GeV]')
	pl.ylabel('Energy / incidence [GeV]')
	pl.show()

if __name__=="__main__":
    plot()