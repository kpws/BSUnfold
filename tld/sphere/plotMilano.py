import plot
import plotBoron
import pylab as pl
import milanoReference

ax1=pl.subplot(111, xscale="log", yscale="linear")
plotBoron.plot(name='milanoB1',ls='--')
pl.ylim([0,1.2])
pl.xlim([1e-11,1])

ax2 = ax1.twinx()

for i in range(len(milanoReference.r)):
	pl.plot(milanoReference.E,[r[i] for r in milanoReference.rate],'-o'
		,label='r='+str(milanoReference.r[i])+' cm')
pl.legend(loc=1)
pl.ylim([0,0.002])
pl.xlim([1e-11,1])

pl.show()
