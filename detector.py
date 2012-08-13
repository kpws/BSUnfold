import result
import numpy as np
import scipy as sp

#this could have been done a LOT nicer with newer versions of python/python packages installed.
intSteps=2e2

class _Detector:
	def __call__(self,ERange,rateDensity,n=intSteps): #trapezoidal integration, error ~1/N^2
		e=np.exp(np.linspace(np.log(ERange[0]), np.log(ERange[1]), n))
		ig=lambda x,r: r(x)*rateDensity(x)  #integrand
		return [sum((ig(e[i],r)+ig(e[i+1],r))*(e[i+1]-e[i]) for i in range(len(e)-1))/2 for r in self.resp]

class _CR39(_Detector):
	def __init__(self):
		r=result.StatisticResult("responses/milanoboron10")
		t=r.dims[2].index('alpha')
		self.E=r.dims[0]
		self.respData=[[-r.mean[ei][i][t]*np.pi*
			r.dims[1][i]**2/2.5**2  for ei in range(len(r.dims[0]))] for i in range(1,len(r.dims[1]))]
		self.resp=[lambda e,r=r:-sp.interp(e,self.E,r) for r in self.respData]#use smarter interpolator in future
		
class _TLD(_Detector):
	def __init__(self):
		r=result.StatisticResult("responses/milanotld")
		l6=r.dims[2].index(6)
		l7=r.dims[2].index(7)
		self.E=r.dims[0]
		self.respData=[[(r.mean[ei][i][l6]-r.mean[ei][i][l7])*np.pi*
			r.dims[1][i]**2  for ei in range(len(self.E))] for i in range(len(r.dims[1]))]
		self.resp=[lambda e,r=r:sp.interp(e,self.E,r) for r in self.respData]#use smarter interpolator in future

#response is tracks per cm^2
cr39=_CR39()

#respons is GeV/g (TLD600 - TLD700)
tld=_TLD()
