import plot
import plotBoron
import pylab as pl
import milanoReference

pl.subplot(111, xscale="log", yscale="linear")
for i in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[r[i] for r in milanoReference.rate],'-o'
		,label='r='+str(milanoReference.r[i])+' cm')
pl.legend(loc=1)
pl.ylim([0,0.002])
pl.xlim([1e-11,1])
#pl.title('Reference from Marco. Same legend, no room.')
'''
pl.subplot(222, xscale="log", yscale="linear")
plot.plot('milano')
pl.title('TLD detector. Errorbars $\pm '+str(3)+'\sigma$')
pl.ylim([0,0.002])
pl.xlim([1e-11,1])

pl.subplot(223, xscale="log", yscale="linear")
plotBoron.plot('milanoB1')
pl.title('Boron10 detector, PET. Errorbars $\pm '+str(3)+'\sigma$')
pl.ylim([0,1.3])
pl.xlim([1e-11,1])


pl.subplot(224, xscale="log", yscale="linear")
plotBoron.plot('milanoB2polyeth')
pl.title('Boron10 detector, POLYETHY. Errorbars $\pm '+str(3)+'\sigma$')
pl.ylim([0,1.3])
pl.xlim([1e-11,1])'''
pl.show()
