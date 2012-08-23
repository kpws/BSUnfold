import result
import numpy as np
import scipy as sp
from beamRadii import beamRadii

#this could have been done a LOT nicer with newer versions of python/python packages installed.
intSteps=2e1

class _Detector:
	def __call__(self,ERange,rateDensity,n=intSteps): #trapezoidal integration, error ~1/N^2
		if ERange[0]<max([e[0] for e in self.E]) or ERange[1]>min([e[-1] for e in self.E]):
			raise Exception('Detector response not calculated for this energy range: '+str(ERange[0])
			+' GeV - '+str(ERange[1])+' GeV. Detector calculations cover '+str(max([e[0] for e in self.E]))
			+' GeV - '+str(min([e[-1] for e in self.E]))+' GeV.')
		e=np.exp(np.linspace(np.log(ERange[0]), np.log(ERange[1]), n))
		ig=lambda x,r: r(x)*rateDensity(x)  #integrand
		resp=[sum((ig(e[i],r)+ig(e[i+1],r))*(e[i+1]-e[i]) for i in range(len(e)-1))/2 for r in self.resp]
		return (resp,[e(r) for e,r in zip(self.errors,resp)])

class _CR39(_Detector):
	def __init__(self):
		r=result.StatisticResult("responses/milanoboron10Total")
		t=r.dims[2].index('alpha')
		projs=[r.project([-1,i,t]) for i in range(len(r.dims[1]))]
		self.respData=[[pi*np.pi*
			beamRadii[str(r.dims[1][i])]**2/2.5**2  for pi in projs[i][1]] for i in range(0,len(r.dims[1]))]
		self.E=[[pi for pi in projs[i][0]] for i in range(0,len(r.dims[1]))]
		self.resp=[lambda e,i=i: sp.interp(e,self.E[i],self.respData[i]) for i in range(len(self.respData))]#use smarter interpolator in future
		self.errors=[lambda r:r*0.1]*len(self.resp)#10% error (standard deviation)
	
class _TLD(_Detector):
	def __init__(self):
		r=result.StatisticResult("responses/milanotld")
		l6=r.dims[2].index(6)
		l7=r.dims[2].index(7)
		self.E=r.dims[0]
		self.respData=[[(r.mean[ei][i][l6]-r.mean[ei][i][l7])*np.pi*
			r.dims[1][i]**2  for ei in range(len(self.E))] for i in range(0,len(r.dims[1]))]
		self.resp=[lambda e,r=r:sp.interp(e,self.E,r) for r in self.respData]#use smarter interpolator in future
		self.errors=[lambda r:r*0.1]*len(self.resp)#10% error (standard deviation)
		
class _Both(_Detector):
	def __init__(self,a,b):
		self._a=a
		self.resp=a.resp+b.resp
		self.errors=a.errors+b.errors
		
#response is tracks per cm^2
cr39=_CR39()

#respons is GeV/g (TLD600 - TLD700)
tld=_TLD()

tldCr39=_Both(cr39, tld)

