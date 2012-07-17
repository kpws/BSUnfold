import os
import time
import numpy as np
import threading
import shutil
from collections import deque

expName='sphere'

def readRate(runId,runNum,fileNum,row):
	num=str(runNum+1)
	while len(num)<3: num='0'+num
	resultFile=open('run'+runId+'/'+expName+num+'_fort.'+str(fileNum),'r')
	for j in range(row-1):
		resultFile.readline()
	res=float(resultFile.readline())
	resultFile.close()
	return res

def getRate(E,r,LiMass,rho=0.96,n=1,source='',runId='',detector='tld'):
	defines=''
	if detector=='tld':
		defines+='#define USE_TLD\n'
	
	replacements={'defines':defines,
	'E':str(E),
	'LiMass':str(LiMass),
	'r':str(r),
	'seed':str(round(time.time()*100))[6:],
	'rho':str(rho)
	}
	
	if source=='':
		inFile=open(expName+'.inp','r');source=inFile.read();inFile.close()
	os.mkdir('run'+runId)
	
	processedFile=open('run'+runId+'/'+expName+'.inp','w')
	processedFile.write( source % replacements )
	processedFile.close()
	
	os.system('cd run'+runId+'; rfluka -N0 -M'+str(n)+' '+expName)
	result=[]
	for i in range(n):
		
		
		if detector=='tld':
			result.append(readRate(runId,i,21,17))
		elif detector =='boron10':
			result.append(readRate(runId,i,21,16))
			result.append(readRate(runId,i,22,16))
			result.append(readRate(runId,i,23,16))
			result.append(readRate(runId,i,24,18))
	
	hasDeletedFile = False
	while hasDeletedFile == False:
		try:
			shutil.rmtree('run'+runId)
			hasDeletedFile = True
		except OSError:
			print(runId+': All files not gone, waiting to redelete...')
			time.sleep(0.5)
			
	return result

class getRateThread(threading.Thread):
	def __init__(self,E,r,n,source,runId,rho=0.96,LiMass='not used',detector='tld'):
		self.E=E
		self.r=r
		self.LiMass=LiMass
		self.rho=rho
		self.n=n
		self.source=source
		self.runId=runId
		self.detector=detector
		threading.Thread.__init__(self)
	def run(self):
		self.result=getRate(self.E,self.r,self.LiMass,rho=self.rho,n=self.n,source=self.source,runId=self.runId,detector=self.detector)
