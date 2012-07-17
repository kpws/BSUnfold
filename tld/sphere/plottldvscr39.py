import plot
import plotBoron
import pylab as pl
import milanoReference

ax1=pl.subplot(111, xscale="log", yscale="linear")
plotBoron.plot(name='milanoB1',ls='--')
pl.ylim([0,1.2])
pl.xlim([1e-11,1])

ax2 = ax1.twinx()

plot.plot('milano1',ls='-')
pl.ylim([0,0.002])
pl.xlim([1e-11,1])

pl.show()
