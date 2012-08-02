import numpy as np

def flat(ERange,n):
	es=np.logspace(ERange[0],ERange[1],n+1)
	return [((es[i],es[i+1]),lambda e,a=a,b=b:int(e>a and e<b))  for i in range(n)]
	
def linear(ERange,n):
	pass #TODO: implement

#thermal distribution from 0 to 0.0025 eV, then flat
def flatThermal(End,n):
	pass #TODO: implement


