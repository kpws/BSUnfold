import os
import time
import numpy as np
import threading
import shutil
from collections import deque

expName='sphere'

def getRate(E,r,LiMass,rho=0.94,n=1,source='',runId='',detector='tld'):
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
		num=str(i+1)
		while len(num)<3: num='0'+num
		resultFile=open('run'+runId+'/'+expName+num+'_fort.21','r')
		if detector=='tld':
			skipRows=16
		elif detector =='boron10':
			skipRows=15
		for j in range(skipRows):
			resultFile.readline()
		result.append(float(resultFile.readline()))
		resultFile.close()
	
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
	def __init__(self,E,r,n,source,runId,rho=0.94,LiMass='not used',detector='tld'):
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
