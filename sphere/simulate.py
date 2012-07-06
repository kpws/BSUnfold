import os
import time
import numpy as np
import threading
import shutil
from collections import deque

expName='sphere'

def getRate(E,r,LiMass,n=1,source='',runId=''):
	replacements={'E':str(E),'LiMass':str(LiMass),'r':str(r),'seed':str(round(time.time()*100))[6:]}
	
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
		for j in range(16):
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
	def __init__(self,E,r,LiMass,n,source,runId):
		self.E=E
		self.r=r
		self.LiMass=LiMass
		self.n=n
		self.source=source
		self.runId=runId
		threading.Thread.__init__(self)
	def run(self):
		self.result=getRate(self.E,self.r,self.LiMass,self.n,self.source,self.runId)

def simulate(name='default',n=4,r=[],E=[]):
	inFile=open(expName+'.inp','r');source=inFile.read();inFile.close()
	os.system('mkdir -p results')
	if E==[]:
		EStart=0.0255e-9 #thermal
		EEnd=1e-1
		E=[EStart]
		while E[-1]<EEnd:
			E.append(E[-1]*1.2)
	if r==[]:
		rStart=3.0
		rEnd=50.0
		r=[rStart]
		while r[-1]<rEnd:
			r.append(r[-1]*1.5)


	threads= deque([])
	for aE in E:
		for ar in r:
			threads.append(getRateThread(aE,ar,6,n,source,str(len(threads))))
			threads.append(getRateThread(aE,ar,7,n,source,str(len(threads))))
	
	runNum=13;
	
	for i in range(min(runNum,len(threads))):
		threads[i].start()
		
	resultFile=open('results/'+name,'w')
	resultFile.write('E\tr\trate6\trate7')
	resultFile.close()
	while len(threads)>0:
		t=threads.popleft()   
		t.join()
		if len(threads)>=runNum:
			threads[runNum-1].start()	
		
		resultFile=open('results/'+name,'a')
		if t.LiMass==6:
			resultFile.write('\n'+str(t.E)+'\t'+str(t.r))
		rateCols=''		
		for col in t.result:
			rateCols+='\t'+str(col)
		resultFile.write(rateCols)
		resultFile.close()

if __name__=="__main__":
	simulate()
