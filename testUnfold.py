import unfold
import detector
import spectrum
import CMSNeutrons


det=detector.tld

resp=det(CMSNeutrons.ERange, CMSNeutrons.fluence)

print('Expected detector responses:')
for r in resp:
	print(str(r))

modelForGuess = spectrum.Flat((1e-12,1e0),5)
model = spectrum.Linear((1e-12,1e0),5) #This is were the assumption on spectrum shape is made

guess = unfold.unfold(det, resp, modelForGuess)
x = unfold.unfold(det, resp, model, guess=guess)

print('Base weights:')
for xp in x:
	print(str(xp))
	
resp2=det(model.getERange(), model.getFluence(x))

print('Expected detector responses with calculated spectrum:')
for r in resp2:
	print(str(r))
	
	
import pylab as pl
import numpy as np
pl.subplot(111, xscale="log", yscale="log")
pn=1e3

E=np.exp(np.linspace(np.log(CMSNeutrons.ERange[0]), np.log(CMSNeutrons.ERange[1]), pn))
pl.plot(E,[CMSNeutrons.fluence(e) for e in E])

E=np.exp(np.linspace(np.log(model.getERange()[0]), np.log(model.getERange()[1]), pn))
pl.plot(E,[model(x,e) for e in E])
#model.plot(x)

E=np.exp(np.linspace(np.log(1e-13), np.log(2e-10), pn))
pl.plot(E,[spectrum.maxwellDistribution(e)/2e10*1.4e4 for e in E])

pl.show()
