import numpy as np
#from scipy.optimize import fmin_l_bfgs_b
#from scipy.optimize import fmin_bfgs
from scipy.optimize import leastsq
#args:
#	detector is a function taking an energy range and a spectrum function
#	responses are the measured responses with given detector
#	bases are tuples of base functions.and their range
#ret:
#	it returns a coefficients for the base functions

def unfold(detector, responses, model, guess=None):
	if len(responses)<model.getN():
		raise Exception('Too many base functions, need more detectors.')
	if model.isLinear() and False:
		M=np.transpose([detector(model.getERange(), model.getBase(i)) for i in range(model.getN())])
		x, residuals, rank, singVals = np.linalg.lstsq(M, responses)
	else:
		if guess==None: guess=np.zeros(model.getN())
		def f(x):
			return detector(model.getERange(), model.getFluence(x))-np.array(responses)
		if model.hasD():
			def jac(x):
				#print x
				return [detector(model.getERange(), lambda e,i=i: model.D(x,i,e)) for i in range(model.getN())]
			
			x,cov_x,infodict,mesg,ier=leastsq(f, guess, Dfun=jac, col_deriv=1, full_output=True)
		else:
			x,cov_x,infodict,mesg,ier=leastsq(f, guess, full_output=True)
			
		print mesg
		
		if model.getN()==1:
			x=[x]
			
	return x
		
		
