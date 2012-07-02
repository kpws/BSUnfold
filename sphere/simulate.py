import os
import time
import numpy as np

expName='sphere'

def getRate(E,LiMass,r,n=1):

	replacements={'E':str(E),'LiMass':str(LiMass),'r':str(r),'seed':str(round(time.time()*100))[6:]}

	inFile=open(expName+'.inp','r')
	os.system('mkdir run')
	processedFile=open('run/'+expName+'.inp','w')
	processedFile.write( inFile.read() % replacements )
	inFile.close()
	processedFile.close()
	
	os.system('cd run; rfluka -N0 -M'+str(n)+' '+expName)
	result=[]
	for i in range(n):
		num=str(i+1)
		while len(num)<3: num='0'+num
		resultFile=open('run/'+expName+num+'_fort.21','r')
		for j in range(16):
			resultFile.readline()
		result.append(float(resultFile.readline()))
		resultFile.close()
		
	os.system('rm -r run')
	return result
	
def simulate(name='default',n=1):
	os.system('mkdir -p results')
	EStart=1e-9
	EEnd=1e3
	rStart=0.05
	rEnd=0.3
	resultFile=open('results/'+name,'w')
	resultFile.write('E\tr\trate6\trate7')
	resultFile.close()
	E=EStart
	r=rStart
	while E<EEnd:
		while r<rEnd:
			resultFile=open('results/'+name,'a')
			rateCols=''
			for col in getRate(E,6,r,n)+getRate(E,7,r,n):
				rateCols+='\t'+str(col)
			resultFile.write('\n'+str(E)+'\n'+str(r)+rateCols)
			resultFile.close()
			r*=1.5
		E*=2.0

if __name__=="__main__":
    simulate()
