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

def getRate(E,r,LiMass,rho,n,parts,runId,detector):
	defines=''
	if detector=='tld':
		defines+='#define USE_TLD\n'
	if r>2.0:
		defines+='#define USE_SPHERE\n'
	replacements={'defines':defines,
	'E':str(E),
	'LiMass':str(LiMass),
	'r':str(r),
	'seed':str(round(time.time()*100))[6:],
	'rho':str(rho),
	'parts':str(parts),
	'includes':includesLinkPath
	}

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
	def __init__(self,E,r,n,parts,rho,detector,runId,LiMass='not used'):
		self.E=E #TODO: ugly code, fix
		self.r=r
		self.LiMass=LiMass
		self.rho=rho
		self.n=n
		self.parts=parts
		self.runId=runId
		self.detector=detector
		threading.Thread.__init__(self)
	def run(self):
		self.result=getRate(self.E,self.r,self.LiMass,rho=self.rho,n=self.n,parts=self.parts,runId=self.runId,detector=self.detector)
