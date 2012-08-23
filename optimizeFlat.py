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

def optimize(det,ERange,n):
	best=np.linspace(np.log(ERange[0]),np.log(ERange[1]),n+1)[1:-1]
	bestCond=Flat(ERange,splitE=np.exp(best)).getCond(det)
	bounds=np.log(ERange)
	
	#A simulated annealing algo could be useful here, but this works ok
	print('Global search...')
	for i in range(200):
		if i<100: #local search
			test=[random.uniform(bounds[0],bounds[1]) for j in range(n-1)]
		else: #global search
			test=[max(bounds[0],min(bounds[1],best[j]+random.gauss(0.0,0.5))) for j in range(n-1)]
		if i==100: print('Local search...')
		test.sort()
		c=Flat(ERange,splitE=np.exp(test)).getCond(det)
		if c<bestCond:
			best=test
			bestCond=c
			print best
			print bestCond
			
	return np.exp(best)
