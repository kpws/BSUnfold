import numpy as np

#these models are flat and linear in loglog space.
def flat(ERange,n):
	es=np.exp(np.linspace(np.log(ERange[0]), np.log(ERange[1]), n+1))
	return [( (es[i],es[i+1]), lambda e,a=es[i],b=es[i+1]: int(bool(a<=e<b)))  for i in range(n)]
	
def linear(ERange,n):
	es=np.exp(np.linspace(np.log(ERange[0]), np.log(ERange[1]), n+2))
	return [( (es[i],es[i+2]), lambda e,a=es[i],b=es[i+1],c=es[i+2]:
			int(bool(a<=e<b))*np.exp(np.log(e/a)/np.log(b/a)) +
			int(bool(b<=e<c))*np.exp((1-np.log(e/b)/np.log(c/b))) )
			for i in range(n)]

#thermal distribution from 0 to 0.0025 eV, then flat
def flatThermal(End,n):
	pass #TODO: implement


####some utilities
def fluence(bases,x):
	return lambda e:sum(bases[i][1](e)*x[i] for i in range(len(x)))
	
def ERange(bases):
	return (min(b[0][0] for b in bases),max(b[0][1] for b in bases))

#A is an arbitrary energy unit.
#Energy in A, mass in A, temp in A.
#Returns probability per A.
def maxwellDistribution(E,T=25e-12):
	return 2*np.sqrt(E/np.pi)*(1/T)**(3.0/2)*np.exp(-E/T)
