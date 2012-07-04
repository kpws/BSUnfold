import os
import time
import numpy as np
import threading
from collections import deque

expName='sphere'

def getRate(E,r,LiMass,n=1,source='',runId=''):
	replacements={'E':str(E),'LiMass':str(LiMass),'r':str(r),'seed':str(round(time.time()*100))[6:]}
	
	if source=='':
		inFile=open(expName+'.inp','r');source=inFile.read();inFile.close()
	os.system('mkdir run'+runId)
	
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
		
	os.system('rm -r run'+runId)
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
	def getResult(self):
		return self.result
    	
def simulate(name='default',n=2):
	inFile=open(expName+'.inp','r');source=inFile.read();inFile.close()
	os.system('mkdir -p results')
	EStart=0.0255e-9
	EEnd=1e-1
	rStart=0.03
	rEnd=0.5

	threads= deque([])
	E=EStart
	while E<EEnd:
		r=rStart
		while r<rEnd:
			threads.append(getRateThread(E,r,6,n,source,str(len(threads))))
			threads.append(getRateThread(E,r,7,n,source,str(len(threads))))
			r*=1.5
		E*=1.5
	
	runNum=24;
	
	for i in range(min(runNum,len(threads))):
		threads[i].start()
		
	resultFile=open('results/'+name,'w')
	resultFile.write('E\tr\trate6\trate7')
	resultFile.close()
	while len(threads)!=0:
		t=threads.popleft()   
		t.join()
		if len(threads)>=runNum:
			threads[runNum-1].start()	
		
		resultFile=open('results/'+name,'a')
		if t.LiMass==6:
			resultFile.write('\n'+str(t.E)+'\t'+str(t.r))
		rateCols=''		
		for col in t.getResult():
			rateCols+='\t'+str(col)
		resultFile.write(rateCols)
		resultFile.close()

if __name__=="__main__":
	simulate()
