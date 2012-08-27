import numpy as np

import unfold
import detector
from spectrumModel import Flat, Linear
import testSpectrum
import CMSNeutrons
import milanoReference
import optimizeFlat

#########################################simulate responses################################

#spectrum, used to calculate responses when no experimental values are available
spectrum=(CMSNeutrons.ERange, CMSNeutrons.fluence)
#spectrum=((1e-11,1e0),lambda e:testSpectrum.fluence((1e-11,2e-1),1e-3,1.5,2,0.9,e))  #bump spectrum

#what detector is used, can be detector.cr39, detector.tld or detector.tldCr39
#do not uncomment this when results are availible
det=detector.tld

#resp=calculated responses, replace this with actuall responses like this:
#resp=[no sphere resp, sphere 1 resp, ..., 81=lead response, Linus response]
resp=det(*spectrum)

print('Expected detector responses:')
#for i in range(len(resp[0])):
#	print((['No sphere']+milanoReference.names)[i]+' & %.1f'%resp[0][i]+' \\\\')
	
#########################################Do unfolding################################	
#number of parameters in model
n=5

#energy range for model
ERange=(5e-13,3e0)

#first linear model, used for guess to nonlinear
#modelForGuess = Flat(ERange,splitE=optimizeFlat.optimize(det,ERange,n)) #use this instead for pptimized base function shapes
modelForGuess = Flat(ERange,n) 
#second non-linear model, set to Flat also to get faster results, (or comment everywhere)
model = Linear(ERange,n)

#set to True for an error estimate, also gives slight error on unfold
#increase 50 for better accuracy and slower execution, nmbr of MC steps
errorEstimate=False
if errorEstimate:
	guess=[]
	x=[]
	for i in range(7):
		r=(np.array(resp[0])+[np.random.normal()*ri for ri in resp[1]],resp[1])
		guess.append([max(0,p) for p in unfold.unfold(det, r, modelForGuess)])
		x.append(unfold.unfold(det, r, model, guess=np.array(guess[-1])))

	guessErrors=np.std(guess,axis=0)
	errors=np.std(x,axis=0)
	guess=np.mean(guess,axis=0)
	x=np.mean(x,axis=0)
else:
	guess=unfold.unfold(det, resp, modelForGuess)
	x=unfold.unfold(det, resp, model, guess=guess)
	guessErrors=[0]*len(guess)
	errors=[0]*len(x)

print('Optimal parameters:')
for xp in x:
	print(str(xp))
	
#print responses in latex table friendly way
respx=det(model.getERange(), model.getFluence(x))
respguess=det(modelForGuess.getERange(), modelForGuess.getFluence(guess))
print('Expected detector responses with calculated spectrum:')
#for i in range(len(respx[0])):
#	print((['No sphere']+milanoReference.names)[i]+' & %.1f'%resp[0][i]+' & %.1f'%respguess[0][i]+' & %.1f'%respx[0][i]+' \\\\')
	

#plot stuff!!!
import pylab as pl
pl.subplot(111, xscale="log", yscale="log")
pn=1e3

E=np.exp(np.linspace(np.log(1e-14), np.log(1e3), pn))
pl.plot(E,[spectrum[1](e) for e in E])
#pl.plot(E,[max(CMSNeutrons.fluence(e),1e-10) for e in E])
#E=np.exp(np.linspace(np.log(model.getERange()[0]), np.log(model.getERange()[1]), pn))
#pl.plot(E,[model(x,e) for e in E])

modelForGuess.plot(guess,errors=guessErrors)
model.plot(x,errors=errors)

#E=np.exp(np.linspace(np.log(1e-13), np.log(2e-10), pn))
#pl.plot(E,[maxwellDistribution(e)/2e10*1.4e4 for e in E])
pl.xlim([1e-13,1e1])
pl.ylim([1e0,1e20])
pl.grid()
pl.xlabel('$E$ [GeV]')
pl.ylabel('$\phi(E)$ [$(\mathrm{fb}^{-1}\ \mathrm{cm}^{2}\mathrm{GeV})^{-1}$]')
pl.show()
