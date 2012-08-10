import os
import time
import numpy as np
import threading
import shutil
from getRate import *
from collections import deque
import milanoReference

expName='sphere'

def simulate(name='testPlastic',n=10,detector='tld'):
	inFile=open(expName+'.inp','r');source=inFile.read();inFile.close()
	os.system('mkdir -p results')

	Ei1=7
	Ei2=14
	E1=milanoReference.E[Ei1]
	E2=milanoReference.E[Ei2]

	threads= deque([])
	for r in milanoReference.r:
		for rho in np.linspace(0.3,1.7,20):
			threads.append(getRateThread(E1,r,n,source,str(len(threads)),rho=rho,detector='boron10'))
			threads.append(getRateThread(E2,r,n,source,str(len(threads)),rho=rho,detector='boron10'))
	
	runNum=13;#we have 12 cpu's
	
	
	for i in range(min(runNum,len(threads))):
		threads[i].start()
		
	resultFile=open('results/'+name,'w')

	resultFile.write('rho\tr\trate at E['+str(Ei1)+']\t'+'rate at E['+str(Ei2)+']')
	resultFile.close()
	while len(threads)>0:
		t=threads.popleft()   
		t.join()
		if len(threads)>=runNum:
			threads[runNum-1].start()	
		
		resultFile=open('results/'+name,'a')
		if t.E==E1:
			resultFile.write('\n'+str(t.rho)+'\t'+str(t.r))
		rateCols=''		
		for col in t.result:
			rateCols+='\t'+str(col)
		resultFile.write(rateCols)
		resultFile.close()

if __name__=="__main__":
	simulate()
