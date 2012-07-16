import os
import time
def getRate(E,LiMass,n=1):

	replacements={'E':str(E),'LiMass':str(LiMass),'seed':str(round(time.time()*100))[6:]}

	inFile=open('tld.inp','r')
	os.system('mkdir run')
	processedFile=open('run/tld.inp','w')
	processedFile.write( inFile.read() % replacements )
	inFile.close()
	processedFile.close()
	
	os.system('cd run; rfluka -N0 -M'+str(n)+' tld')
	result=[]
	for i in range(n):
		num=str(i+1)
		while len(num)<3: num='0'+num
		resultFile=open('run/tld'+num+'_fort.21','r')
		for j in range(16):
			resultFile.readline()
		result.append(float(resultFile.readline()))
		resultFile.close()
		
	os.system('rm -r run')
	return result
	
def simulate(name='default',n=1):
	os.system('mkdir -p results')
	Estart=1e-11
	Eend=1e1
	resultFile=open('results/'+name,'w')
	resultFile.write('E\trate6\trate7')
	resultFile.close()
	E=Estart
	while E<Eend:
		resultFile=open('results/'+name,'a')
		rateCols=''
		for r in getRate(E,6,n)+getRate(E,7,n):
			rateCols+='\t'+str(r)
		resultFile.write('\n'+str(E)+rateCols)
		resultFile.close()
		E*=1.3

if __name__=="__main__":
    simulate(n=3)
