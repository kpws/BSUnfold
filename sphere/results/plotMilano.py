import plot
import pylab as pl
import milanoReference

for i in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[r[i] for r in milanoReference.rate] ,label='B-10 reaction rate, r='+str(milanoReference.r[i])+' cm')


#plot.plot('milano')
