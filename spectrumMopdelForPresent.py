import unfold
import detector
from spectrumModel import Flat, Linear
import testSpectrum
import CMSNeutrons
import numpy as np

#spectrum=(CMSNeutrons.ERange, CMSNeutrons.fluence)
spectrum=((1e-11,1e0),lambda e:testSpectrum.fluence((1e-11,2e-1),1e-3,1.5,0,0.9,e))

errorEstimate=False
det=detector.cr39
modelForGuess = Flat((1e-12,1e0),4)
model = Linear((1e-12,1e0),4)           #This is were the assumption on spectrum shape is made


resp=det(*spectrum)

print('Expected detector responses:')
for r in resp[0]:
	print(str(r))


if errorEstimate:
	guess=[]
	x=[]
	for i in range(7):
		r=(np.array(resp[0])+[np.random.normal()*ri for ri in resp[1]],resp[1])
		guess.append(unfold.unfold(det, r, modelForGuess))
		x.append(unfold.unfold(det, r, model, guess=np.array(guess[-1])))

	guessErrors=np.std(guess,axis=0)
	errors=np.std(x,axis=0)
	guess=np.mean(guess,axis=0)
	x=np.mean(x,axis=0)
else:
	guess=unfold.unfold(det, resp, modelForGuess)
	x=unfold.unfold(det, resp, model, guess=guess*2)
	guessErrors=[0]*len(guess)
	errors=[0]*len(x)
print('Base weights:')
for xp in x:
	print(str(xp))
	
resp2=det(model.getERange(), model.getFluence(x))
print('Expected detector responses with calculated spectrum:')
for r in resp2[0]:
	print(str(r))
	
	
import pylab as pl
pl.subplot(111, xscale="log", yscale="log")
pn=1e3

#E=np.exp(np.linspace(np.log(1e-14), np.log(1e3), pn))
#pl.plot(E,[spectrum[1](e) for e in E])
#pl.plot(E,[CMSNeutrons.fluence(e) for e in E])
#E=np.exp(np.linspace(np.log(model.getERange()[0]), np.log(model.getERange()[1]), pn))
#pl.plot(E,[model(x,e) for e in E])

modelForGuess.plot(guess,errors=guessErrors)
#model.plot(x,errors=errors)

#E=np.exp(np.linspace(np.log(1e-13), np.log(2e-10), pn))
#pl.plot(E,[maxwellDistribution(e)/2e10*1.4e4 for e in E])
pl.ylabel('$\phi(E)$ [$\mathrm{mb}\ \mathrm{cm}^{-2}\mathrm{GeV}^{-1}$]')
pl.xlabel('$E$ [GeV]')
pl.xlim([1e-13,1e1])
pl.ylim([1e-10,1e6])
pl.grid()
pl.show()
