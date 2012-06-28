import os

def getRate(E,LiMass):

	replacements={'E':str(E),'LiMass':str(LiMass)}

	inFile=open('tld.inp','r')
	os.system('mkdir run')
	processedFile=open('run/tld.inp','w')
	processedFile.write( inFile.read() % replacements )
	inFile.close()
	processedFile.close()
	
	os.system('cd run; rfluka -N0 -M1 tld')
	
	resultFile=open('run/tld001_fort.21','r')
	for i in range(16):
		resultFile.readline()
	result=float(resultFile.readline())
	resultFile.close()
	os.system('rm -r run')
	return result
	
def simulate(name='default'):
	E=1e-9
	rate6=[]
	rate7=[]
	Es=[]
	resultFile=open('results/'+name,'w')
	resultFile.write('E\trate6\trate7')
	resultFile.close()
	for i in range(100):
		Es.append(E)
		rate6.append(getRate(E,6))
		rate7.append(getRate(E,7))
		resultFile=open('results/'+name,'a')
		resultFile.write('\n'+str(E)+'\t'+str(rate6[-1])+'\t'+str(rate7[-1]))
		resultFile.close()
		E*=1.3
