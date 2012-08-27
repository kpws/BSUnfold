import result
import numpy as np
import scipy as sp
from beamRadii import beamRadii

#this could have been done a LOT nicer with newer versions of python/python packages installed.
intSteps=1e2

class _Detector:
    def __call__(self,ERange,rateDensity,n=intSteps): #trapezoidal integration, error ~1/N^2
        if ERange[0]<self.ERange[0] or ERange[1]>self.ERange[1]:
            raise Exception('Detector response not calculated for this energy range: '+str(ERange[0])
            +' GeV - '+str(ERange[1])+' GeV. Detector calculations cover '+str(self.ERange[0])
            +' GeV - '+str(self.ERange[1])+' GeV.')
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
        self.ERange=(max(e[0] for e in self.E),min(e[-1] for e in self.E))
        self.resp=[lambda e,i=i: sp.interp(e,self.E[i],self.respData[i]) for i in range(len(self.respData))]#use smarter interpolator in future
        self.errors=[lambda r:r*0.1]*len(self.resp)#10% error (standard deviation)
    
class _TLD(_Detector):
    def __init__(self):
        r=result.StatisticResult("responses/milanotldTotal")
        l6=r.dims[2].index(6)
        l7=r.dims[2].index(7)
        projs6=[r.project([-1,i,l6]) for i in range(len(r.dims[1]))]
        projs7=[r.project([-1,i,l7]) for i in range(len(r.dims[1]))]
        self.E6=[[pi for pi in projs6[i][0]] for i in range(0,len(r.dims[1]))]
        self.E7=[[pi for pi in projs7[i][0]] for i in range(0,len(r.dims[1]))]
        self.ERange=(max(e[0] for e in self.E6+self.E7),min(e[-1] for e in self.E6+self.E7))
        self.respData6=[[pi*np.pi*
            beamRadii[str(r.dims[1][i])]**2 for pi in projs6[i][1]] for i in range(0,len(r.dims[1]))]
        self.respData7=[[pi*np.pi*
            beamRadii[str(r.dims[1][i])]**2 for pi in projs7[i][1]] for i in range(0,len(r.dims[1]))]
        self.resp=[lambda e,i=i: sp.interp(e,self.E6[i],self.respData6[i])-sp.interp(e,self.E7[i],self.respData7[i]) for i in range(len(self.respData6))]#use smarter interpolator in future
        self.errors=[lambda r:r*0.1]*len(self.resp)#10% error (standard deviation)
        
class _Both(_Detector):
    def __init__(self,a,b):
        self.resp=a.resp+b.resp
        self.errors=a.errors+b.errors
        self.ERange=(max(a.ERange[0],b.ERange[0]),min(a.ERange[1],b.ERange[1]))
        
#response is tracks per cm^2
cr39=_CR39()

#respons is GeV/g (TLD600 - TLD700)
tld=_TLD()

tldCr39=_Both(cr39, tld)

