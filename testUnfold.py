import unfold
import detector
import spectrum
import CMSNeutrons


det=detector.cr39

resp=det(CMSNeutrons.ERange, CMSNeutrons.fluence)

print('Expected detector responses:')
for r in resp:
	print(str(r))

model = spectrum.linear((1e-12,1),4) #This is were the assumption on spectrum shape is made

x = unfold.unfold(det, resp, model)
print('Base weights:')
for xp in x:
	print(str(xp))
	
resp2=det(spectrum.ERange(model), spectrum.fluence(model, x))

print('Expected detector responses with calculated spectrum:')
for r in resp2:
	print(str(r))
	
	
import pylab as pl
import numpy as np
pl.subplot(111, xscale="log", yscale="linear")
pn=1e3
E=np.exp(np.linspace(np.log(CMSNeutrons.ERange[0]), np.log(CMSNeutrons.ERange[1]), pn))
pl.plot(E,[CMSNeutrons.fluence(e) for e in E])
E=np.exp(np.linspace(np.log(spectrum.ERange(model)[0]), np.log(spectrum.ERange(model)[1]), pn))
pl.plot(E,[spectrum.fluence(model, x)(e) for e in E])
E=np.exp(np.linspace(np.log(1e-13), np.log(2e-10), pn))
pl.plot(E,[spectrum.maxwellDistribution(e)/2e10*1.4e4 for e in E])
pl.show()
