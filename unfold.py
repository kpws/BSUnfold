import numpy as np
#from scipy.optimize import fmin_l_bfgs_b
#from scipy.optimize import fmin_bfgs
from scipy.optimize import leastsq, fmin_l_bfgs_b, fmin_tnc
#args:
#	detector is a function taking an energy range and a spectrum function
#	responses are the measured responses with given detector
#	bases are tuples of base functions.and their range
#ret:
#	it returns a coefficients for the base functions

def unfold(detector, responses, model, guess=None):
	errors=responses[1]
	responses=responses[0]
	
	if len(responses)<model.getN():
		raise Exception('Too many base functions, need more detectors.')
	if errors==None: errors=np.ones(len(responses))
	if model.isLinear() and False:
		M=np.transpose([detector(model.getERange(), model.getBase(i))[0] for i in range(model.getN())])
		x, residuals, rank, singVals = np.linalg.lstsq([row for row in M], responses)
	else:
		if guess==None: guess=np.zeros(model.getN())
		def f(x):
			return (detector(model.getERange(), model.getFluence(x))[0]-np.array(responses))/errors
		def jac(x):
			return [np.array(detector(model.getERange(), lambda e,i=i: model.D(x,i,e))[0])/errors for i in range(model.getN())]
		
		if model.hasD():
			def sqrErr(x):
				return sum(fi**2 for fi in f(x))
			def gradS(x):
				return 2*np.dot(jac(x),f(x))
			#for i in range(model.getN()):  #verify that gradS is correct
			#	h=1e-6
			#	print str(gradS(guess)[i])+', '+str((sqrErr(guess+([0]*i+[h]+[0]*(model.getN()-i-1)))-sqrErr(guess))/h)
			
			#x,cov_x,infodict,mesg,ier=leastsq(f, guess, Dfun=jac, col_deriv=1, full_output=True)
			x,f,d=fmin_tnc(sqrErr,guess,fprime=gradS, bounds=[(1e-10,None)]*len(guess),maxfun=1000)
		else:
			#x,cov_x,infodict,mesg,ier=leastsq(f, guess, full_output=True)
			#x,f,d=fmin_l_bfgs_b(lambda x:sum(fi**2 for fi in f(x)), guess, bounds=[(0,None)]*len(guess),approx_grad=True)
			x,f,d=fmin_tnc(lambda x:sum(fi**2 for fi in f(x)), guess, bounds=[(1e-10,None)]*len(guess),approx_grad=True,maxfun=1000)

			
		#print mesg
		
		if model.getN()==1:
			x=[x]
	return x
		
		
