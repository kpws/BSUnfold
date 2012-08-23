import numpy as np

def fluence(cutoffs,bumpe,bumpw,bumph,p,e):
	#if not cutoffs[0]<e<cutoffs[1]:
	#	return 0.0
	return 1e8*(np.exp(-(cutoffs[0]/e)**2)*
	np.exp(-(e/cutoffs[1])**2)*
	10.0**(np.exp(-((np.log10(e)-np.log10(bumpe))/bumpw)**2/2)*bumph)*
	1/e**p)
