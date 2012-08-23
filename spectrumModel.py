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
		if self._isLinear:
			return lambda e, i=i: self([int(i==j) for j in range(self._n)], e)
		else:
			raise Exception('Non-linear models do not have base functions.')
		
#these models are flat and linear in loglog space.
class Flat(SpectrumModel):
	def __init__(self, ERange, n=-1, splitE=None):
		self._ERange=ERange
		if splitE==None:
			assert(n!=-1)
			self._n=n
			self._splitE=np.exp(np.linspace(np.log(self._ERange[0]),np.log(self._ERange[1]),self._n+1))[1:-1]
		else:
			self._splitE=splitE
			assert(n==-1)
			self._n=len(splitE)+1
		self._isLinear=True
		
		self._hasD=False
	def __call__(self, params, e):
		if e<self._ERange[0] or e>self._ERange[1]: return 0.0
		i=0
		while i<self._n-1 and e>self._splitE[i]: i+=1
		return params[i]
		
	def plot(self, params, errors=None):
		params=[max(1e-100,p) for p in params]
		E=np.concatenate(([self._ERange[0]],self._splitE,[self._ERange[1]]))
		pl.plot(reduce(lambda a,b:a+b,[[e,e] for e in E]),[1e-10]+reduce(lambda a,b:a+b,[[p,p] for p in params])+[1e-10])
		if errors!=None:
			for i in range(len(E)-1):
				pl.errorbar([np.sqrt(E[i]*E[i+1])],[params[i]],yerr=[errors[i]],fmt='r')
				
	#return matrix condition number where errors are weighted by base upper energy
	def getCond(self,det):
		E=np.concatenate(([self._ERange[0]],self._splitE,[self._ERange[1]]))
		M=np.transpose([np.array(det((E[i],E[i+1]), lambda e:1)[0])/E[i+1] for i in range(self._n)])
		return np.linalg.cond(M)

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
	def plot(self,params,errors=None):
		E=np.exp(np.linspace(np.log(self._ERange[0]),np.log(self._ERange[1]),self._n))
		if errors==None:
			pl.plot(E,params,'-o')
		else:
			pl.errorbar(E,params,yerr=errors,fmt='-o')
		

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
	def plot(self,params,errors=None):
		E=np.exp(np.linspace(np.log(self._ERange[0]),np.log(self._ERange[1]),1e3))
		pl.plot(E,[self(params, e) for e in E])
		if errors!=None:
			E=np.exp(np.linspace(np.log(self._ERange[0]),np.log(self._ERange[1]),self._n))
			pl.errorbar(E,params,yerr=errors)
		
			
#thermal distribution from 0 to 0.0025 eV, then flat
def flatThermal(End,n):
	pass #TODO: implement


####some utilities

#A is an arbitrary energy unit.
#Energy in A, mass in A, temp in A.
#Returns probability per A.
def maxwellDistribution(E,T=25e-12):
	return 2*np.sqrt(E/np.pi)*(1/T)**(3.0/2)*np.exp(-E/T)
