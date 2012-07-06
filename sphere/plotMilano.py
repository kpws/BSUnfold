import plot
import pylab as pl
import milanoReference

pl.subplot(111, xscale="log", yscale="linear")

for i in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[r[i] for r in milanoReference.rate],'-o'
		,label='B-10 reaction rate, r='+str(milanoReference.r[i])+' cm')


plot.plot('milano')
