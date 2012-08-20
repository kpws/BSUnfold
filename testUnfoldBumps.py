import unfold
import detector
import spectrum
import testSpectrum


det=detector.cr39

ERange=[1e-14, 1e3]
fluence=lambda e: testSpectrum.fluence([1e-11,1e-1], 1e-5, 1.0, 1e3, 1.5,e)
resp=det([1e-13,1e1], fluence)

print('Expected detector responses:')
for r in resp:
	print(str(r))

modelForGuess = spectrum.Flat((1e-12,1e0),4)
model = spectrum.Flat((1e-12,1e0),4) #This is were the assumption on spectrum shape is made

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

E=np.exp(np.linspace(np.log(ERange[0]), np.log(ERange[1]), pn))
pl.plot(E,[fluence(e) for e in E])

E=np.exp(np.linspace(np.log(model.getERange()[0]), np.log(model.getERange()[1]), pn))
#pl.plot(E,[model(x,e) for e in E])
model.plot(x)
pl.ylim([1e-3,1e13])
pl.grid()
pl.show()
