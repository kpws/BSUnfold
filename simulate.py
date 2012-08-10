import os
import time
import numpy as np
import threading
import shutil
import random
from collections import deque
from getRate import *

def simulate(name,n,partNum,r,E,rho,detector):
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


	jobs=[]
	for aE in E:
		for ar in r:
			if detector=='tld':
				jobs.append(getRateThread(aE,ar,n,partNum,rho,detector,str(len(jobs)),LiMass=6))
				jobs.append(getRateThread(aE,ar,n,partNum,rho,detector,str(len(jobs)),LiMass=7))
			elif detector=='boron10':
				jobs.append(getRateThread(aE,ar,n,partNum,rho,detector,str(len(jobs))))
			else: raise Exception('Not implemented detector: '+detector)
	
	runNum=10;#we have 12 cpu's but want to run only 10 cores
	
	runningJobs = []
	for i in range(min(runNum,len(jobs))):
		runningJobs.append(jobs.pop(random.randrange(len(jobs))))
		runningJobs[-1].start()
		
	resultFile=open('results/'+name,'w')
	if detector=='tld':
		resultFile.write('E\tr\tLiMass\tvalue')
	else:
		resultFile.write('E\tr\tscoring\tvalue')
	resultFile.close()
	
	i=0
	while len(runningJobs)>0:
		time.sleep(0.05)
		if not runningJobs[i].isAlive():
			t=runningJobs.pop(i)
			
			if len(jobs)>0:	
				runningJobs.append(jobs.pop(random.randrange(len(jobs))))
				runningJobs[-1].start()
				
			resultFile=open('results/'+name,'a')
			if detector=='tld':
				for r in t.result:
					for i in range(len(r)):
						resultFile.write('\n'+str(t.E)+'\t'+str(t.r)+'\t'+str(t.LiMass)+'\t'+str(r[i]))
			elif detector=='boron10':
				for r in t.result:
					for i in range(len(r)):
						resultFile.write('\n'+str(t.E)+'\t'+str(t.r)+'\t'+
							['neubal','alpha'][i]+'\t'+str(r[i]))
			resultFile.close()
		i+=1
		if i>=len(runningJobs): i=0

if __name__=="__main__":
	simulate()
