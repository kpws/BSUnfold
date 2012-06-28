import pylab as pl
import csv

def plot(name='default'):
	E=[]
	rate6=[]
	rate7=[]
	reader=csv.reader(open('results/'+name, 'rb'), delimiter='\t')
	reader.next()
	for row in reader:
		E.append(float(row[0]))
		rate6.append(float(row[1]))
		rate7.append(float(row[2]))

	pl.loglog(E, rate6, 'o-', label='Li6F')
	pl.hold(True)	
	pl.loglog(E, rate7, 'o-', label='Li7F')
	pl.legend()
	pl.xlabel('Beam energy [GeV]')
	pl.ylabel('Energy/hit [GeV].')
	pl.show()
