import unfold
import detector
from spectrumModel import Flat, Linear
import testSpectrum
import CMSNeutrons
import numpy as np
import milanoReference
import pylab as pl
from scipy.optimize import leastsq, fmin_l_bfgs_b, fmin_tnc
import random

det=detector.cr39

ERange=(5e-13,2.9e0)
n=5
def cond(logSplitE):
	logSplitE.sort()
	print logSplitE
	c=Flat(ERange,splitE=np.exp(logSplitE)).getCond(det)
	print c
	return c

#splitE,f,d=fmin_tnc(cond,np.exp(np.linspace(np.log(ERange[0]),np.log(ERange[1]),n+1))[1:-1], bounds=[ERange]*(n-1),approx_grad=True)
#print np.log([ERange]*(n-1))
#print np.linspace(np.log(ERange[0]),np.log(ERange[1]),n+1)[1:-1]
#logSplitE,f,d=fmin_tnc(cond, np.linspace(np.log(ERange[0]),np.log(ERange[1]),n+1)[1:-1],
#	bounds=np.log([ERange]*(n-1)),approx_grad=True)
#logSplitE.sort()
#splitE=np.exp(logSplitE)
best=np.linspace(np.log(ERange[0]),np.log(ERange[1]),n+1)[1:-1]
bestCond=Flat(ERange,splitE=np.exp(best)).getCond(det)
bounds=np.log(ERange)
print('Global search...')
for i in range(200):
	if i<100:
		test=[random.uniform(bounds[0],bounds[1]) for j in range(n-1)]
	else:
		test=[max(bounds[0],min(bounds[1],best[j]+random.gauss(0.0,0.5))) for j in range(n-1)]
	if i==100: print('Local search...')
	test.sort()
	c=Flat(ERange,splitE=np.exp(test)).getCond(det)
	if c<bestCond:
		best=test
		bestCond=c
		print best
		print bestCond
		
splitE=np.exp(best)
'''
conds=[]
ss=np.linspace(0,1,150)
for s in ss:
	splitE=np.exp(np.linspace(np.log(ERange[0]),np.log(ERange[1]),n+1))[1:-1]
	splitE[1]=splitE[0]**(1-s**2)*splitE[3]**(s**2)
	splitE[2]=splitE[0]**(1-s**0.5)*splitE[3]**(s**0.5)
	print(splitE)
	conds.append(Flat(ERange,splitE=splitE).getCond(det))
	print conds[-1]
pl.subplot(111, xscale="linear", yscale="log")
pl.plot(ss,conds)
'''

spectrum=(CMSNeutrons.ERange, CMSNeutrons.fluence)
#spectrum=((1e-11,1e0),lambda e:testSpectrum.fluence((1e-11,2e-1),1e-3,1.5,2,0.9,e))

errorEstimate=True
print splitE
model=Flat(ERange,splitE=splitE)

resp=det(*spectrum)

print('Expected detector responses:')
for i in range(len(resp[0])):
	print((['No sphere']+milanoReference.names)[i]+' & %.1f'%resp[0][i]+' \\\\')

if errorEstimate:
	guess=[]
	x=[]
	for i in range(50):
		r=(np.array(resp[0])+[np.random.normal()*ri for ri in resp[1]],resp[1])
		x.append(unfold.unfold(det, r, model))
	errors=np.std(x,axis=0)
	x=np.mean(x,axis=0)
else:
	x=unfold.unfold(det, resp, model)
	errors=[0]*len(x)
	
#print('Base weights:')
#for xp in x:
#	print(str(xp))
	
#resp2=det(modelForGuess.getERange(), model.getFluence(x))#TODO guess-> x
#print('Expected detector responses with calculated spectrum:')
#for i in range(len(resp2[0])):
#	print((['No sphere']+milanoReference.names)[i]+' & %.1f'%resp[0][i]+' & %.1f'%resp2[0][i]+' \\\\')

pl.subplot(111, xscale="log", yscale="log")
pn=1e3

E=np.exp(np.linspace(np.log(1e-14), np.log(1e3), pn))
pl.plot(E,[spectrum[1](e) for e in E])
#pl.plot(E,[max(CMSNeutrons.fluence(e),1e-10) for e in E])
E=np.exp(np.linspace(np.log(model.getERange()[0]), np.log(model.getERange()[1]), pn))
#pl.plot(E,[modelForGuess(guess,e) for e in E])

#modelForGuess.plot(guess,errors=guessErrors)
model.plot(x,errors=errors)

#E=np.exp(np.linspace(np.log(1e-13), np.log(2e-10), pn))
#pl.plot(E,[maxwellDistribution(e)/2e10*1.4e4 for e in E])
pl.xlim([1e-13,1e1])
pl.ylim([1e0,1e20])
pl.grid()
pl.xlabel('$E$ [GeV]')
pl.ylabel('$\phi(E)$ [$(\mathrm{fb}^{-1}\ \mathrm{cm}^{2}\mathrm{GeV})^{-1}$]')

pl.show()
