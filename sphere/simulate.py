import os
import time
import numpy as np
import threading
import shutil
from collections import deque
from getRate import *

expName='sphere'

def simulate(name='default',n=4,r=[],E=[],rho=0.96,detector='tld'):
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
			if detector=='tld':
				threads.append(getRateThread(aE,ar,n,source,str(len(threads)),LiMass=6,rho=rho))
				threads.append(getRateThread(aE,ar,n,source,str(len(threads)),LiMass=7,rho=rho))
			elif detector=='boron10':
				threads.append(getRateThread(aE,ar,n,source,str(len(threads)),detector=detector,rho=rho))
			else: raise Exception('Not implemented detector: '+detector)
	
	runNum=10;#we have 12 cpu's
	
	for i in range(min(runNum,len(threads))):
		threads[i].start()
		
	resultFile=open('results/'+name,'w')
	if detector=='tld':
		resultFile.write('E\tr\tLiMass\tvalue')
	else:
		resultFile.write('E\tr\tscoring\tvalue')
	resultFile.close()
	while len(threads)>0:
		t=threads.popleft()   
		t.join()
		if len(threads)>=runNum:
			threads[runNum-1].start()	
		
		resultFile=open('results/'+name,'a')
		if detector=='tld':
			for r in t.result:
				resultFile.write('\n'+str(t.E)+'\t'+str(t.r)+'\t'+str(t.LiMass)+'\t'+str(r))
		elif detector=='boron10':
			for r in t.result:
				for i in range(len(r)):
					resultFile.write('\n'+str(t.E)+'\t'+str(t.r)+'\t'+
						['neubal','alpha'][i]+'\t'+str(r[i]))
		
		resultFile.close()

if __name__=="__main__":
	simulate()
