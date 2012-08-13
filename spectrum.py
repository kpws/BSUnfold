import numpy as np
import pylab as pl

class SpectrumModel:
	def isLinear(self):
		return self._isLinear
		
	def hasD(self):
		return self._hasD
		
	def getERange(self):
		return self._ERange
		
	def getN(self):
		return self._n
		
	def getFluence(self,params):
		return lambda e: self(params, e)
		
	def getBase(self,i):
		if True:#self._isLinear:
			return lambda e, i=i: self([int(i==j) for j in range(self._n)],e)
		else:
			raise Exception('Non-linear models do not have base functions.')
		
#these models are flat and linear in loglog space.
class Flat(SpectrumModel):
	def __init__(self,ERange,n):
		self._isLinear=True
		self._ERange=ERange
		self._n=n
		self._hasD=False
	def __call__(self, params, e):
		i=int(self._n*np.log(e/self._ERange[0])/np.log(self._ERange[1]/self._ERange[0]))
		if 0<=i<self._n:
			return params[i]
		else:
			return 0.0

class Linear(SpectrumModel):
	def __init__(self,ERange,n):
		self._isLinear=False
		self._hasD=True
		self._ERange=ERange
		self._n=n
	def __call__(self, params, e):
		f=(self._n-1)*np.log(e/self._ERange[0])/np.log(self._ERange[1]/self._ERange[0])
		i=int(f)
		if  0<=i<self._n-1:
			return params[i+1]**(f-i)*params[i]**(1-(f-i))
		else:
			return 0.0
	def D(self,params,di,e):
		f=(self._n-1)*np.log(e/self._ERange[0])/np.log(self._ERange[1]/self._ERange[0])
		i=int(f)
		if  0<=i<self._n-1:
			if di==i+1:
				return (f-i)*params[i+1]**(f-i-1)*params[i]**(1-(f-i))
			elif di==i:
				return params[i+1]**(f-i)*(1-(f-i))*params[i]**(1-(f-i)-1)
			else:
				return 0
		else:
			return 0.0
	def plot(self,params):
		E=np.exp(np.linspace(np.log(self._ERange[0]),np.log(self._ERange[1]),self._n))
		pl.plot(E,[self(params, e) for e in E],'-o')

class LinLinear(SpectrumModel):
	def __init__(self,ERange,n):
		self._isLinear=True
		self._hasD=False
		self._ERange=ERange
		self._n=n
	def __call__(self, params, e):
		f=(self._n-1)*np.log(e/self._ERange[0])/np.log(self._ERange[1]/self._ERange[0])
		i=int(f)
		if  0<=i<self._n-1:
			return params[i+1]*(f-i)+params[i]*(1-(f-i))
		else:
			return 0.0
	def plot(self,params):
		E=np.exp(np.linspace(np.log(self._ERange[0]),np.log(self._ERange[1]),self._n))
		pl.plot(E,[self(params, e) for e in E],'-o')
			
#thermal distribution from 0 to 0.0025 eV, then flat
def flatThermal(End,n):
	pass #TODO: implement


####some utilities

#A is an arbitrary energy unit.
#Energy in A, mass in A, temp in A.
#Returns probability per A.
def maxwellDistribution(E,T=25e-12):
	return 2*np.sqrt(E/np.pi)*(1/T)**(3.0/2)*np.exp(-E/T)
