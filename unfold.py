import numpy as np
from scipy.optimize import fmin_l_bfgs_b

#args:
#	detector is a function taking an energy range and a spectrum function
#	responses are the measured responses with given detector
#	bases are tuples of base functions.and their range
#ret:
#	it returns a coefficients for the base functions

def unfold(detector, responses, bases):
	if len(responses)<len(bases):
		raise Exception('Too many base functions, need more detectors.')
	M=np.transpose([detector(*b) for b in bases])
	

	x, residuals, rank, singVals = np.linalg.lstsq(M, responses)
	
	#test if didn't get a negative response, otherwise use constrained opt
	if sum(1 for i in x if i<0)==0:
		return x
		
	#should obviously use an nnls algorithm here, there are many but found none with good licensing
	#one is included in up to date versions of scipy but I didn't have any success compiling it for SL5.
	#awaiting book from CERN library to make own implementation. This will have to do for now:
	
	def f(fx):
		e=np.dot(M,fx)-np.array(responses)
		return ( np.dot(e,e), 2*np.dot(np.transpose(e), M) )
	
	#TODO, investigate if this really works
	x,f,d = fmin_l_bfgs_b(f,x,bounds=[(0,None)]*len(bases), factr=1e-10, iprint=1, pgtol=-1)
	return x
	

