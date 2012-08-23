import os
import time
import numpy as np
import threading
import shutil
from collections import deque

workPath='/home/ksatersk/tmp'
includesLinkPath=workPath+'/includes'
includesPath=os.path.abspath('flukaInput/')
if not os.path.exists(includesLinkPath):
	os.symlink(includesPath, includesLinkPath) 
# fluka can't handle long paths in includes, no warning whatsover,
# just crash. Not even mentioned in docs. So uncomment above if your path is 'short',
# otherwise make a link with shorter path (if you have permissions) and write link path above
# Impossible to know if this was the actual cause but this solves it so seems very likely.

inFile=open(includesPath+'/sphere.inp','r')
source=inFile.read()
inFile.close()

expName='sphere'


def readRate(runId,runNum,fileNum,row):
	num=str(runNum+1)
	while len(num)<3: num='0'+num
	resultFile=open(workPath+'/run'+runId+'/'+expName+num+'_fort.'+str(fileNum),'r')
	for j in range(row-1):
		resultFile.readline()
	res=float(resultFile.readline())
	resultFile.close()
	return res

def getMilanoRate(E,name,LiMass,rho,n,parts,runId,detector):
	defines=''
	
	import UserDict
	class DefaultDict(UserDict.UserDict):
		default_value = 'not defined'
		def __getitem__(self, key) :
			return self.data.get(key, DefaultDict.default_value)

	replacements=DefaultDict()
	if name=='81+lead':
		leadThickness=2.0
		r1=81.0/10/2
		r=r1+leadThickness
		defines+='#define USE_R1BALL\n'
		replacements['r1']=str(r1)
		replacements['outerMat']='LEAD'
	elif name=='Linus':
		leadThickness=0.6
		r1=5.6
		r=12.5
		buttonThickness=0.1
		buttonRadius=2.5
		coneBodyCode=''
		from icosahedron import v
		for i in range(1,len(v)): #topless
			coneBodyCode+=('RCC B_CYL'+str(i)+' 0.0 0.0 0.0 '+str(v[i][0]*r)+
				' '+str(v[i][1]*r)+' '+str(v[i][2]*r)+' '+str(buttonRadius))+'\n'
		coneBodyCode=coneBodyCode[:-1]
		defines+='#define USE_R1BALL\n'
		defines+='#define USE_R2BALL\n'
		defines+='#define USE_BUTTONS\n'
		replacements['r1']=str(r1)
		replacements['r2']=str(r1+leadThickness)
		replacements['buttonInnerRadius']=str(r1-buttonThickness)
		replacements['middleMat']='LEAD'
		replacements['outerMat']='POLYETHY'
		replacements['cones']=coneBodyCode
	else:
		r=float(name)

	if detector=='tld':
		defines+='#define USE_TLD\n'
	if r>2.0:
		defines+='#define USE_SPHERE\n'
		
	replacements['E']=str(E)
	replacements['LiMass']=str(LiMass)
	replacements['r']=str(r)
	replacements['seed']=str(round(time.time()*100))[6:]
	replacements['rho']=str(rho)
	replacements['parts']=str(parts)
	replacements['includes']=includesLinkPath
	replacements['defines']=defines
	
	os.mkdir(workPath+'/run'+runId)
	
	processedFile=open(workPath+'/run'+runId+'/'+expName+'.inp','w')
	processedFile.write( source % replacements )
	processedFile.close()
	
	os.system('cd '+workPath+'/run'+runId+'; rfluka -N0 -M'+str(n)+' '+expName)
	result=[]
	for i in range(n):
		result.append([])
		if detector=='tld':
			result[-1].append(readRate(runId,i,21,17))
		elif detector =='boron10':
			result[-1].append(readRate(runId,i,21,16))
			#result[-1].append(readRate(runId,i,22,16))
			#result[-1].append(readRate(runId,i,23,16))
			result[-1].append(readRate(runId,i,22,18))
	
	hasDeletedFile = False
	while hasDeletedFile == False:
		try:
			shutil.rmtree(workPath+'/run'+runId)
			hasDeletedFile = True
		except OSError:
			print(runId+': All files not gone, waiting to redelete...')
			time.sleep(0.5)
			
	return result

class getRateThread(threading.Thread):
	def __init__(self,E,name,n,parts,rho,detector,runId,LiMass='not used'):
		self.E=E #TODO: ugly code, fix
		self.name=name
		self.LiMass=LiMass
		self.rho=rho
		self.n=n
		self.parts=parts
		self.runId=runId
		self.detector=detector
		threading.Thread.__init__(self)
	def run(self):
		self.result=getMilanoRate(self.E,self.name,self.LiMass,self.rho,self.n,self.parts,self.runId,self.detector)
