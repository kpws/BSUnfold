import pylab as pl
import csv
import numpy as np

def toNum(s):
	try:
		return int(s)
	except ValueError:
		try:
			return float(s)
		except ValueError:
			return s

#makes kd-matrix, n is list of sizes, last size must be 0
fillZero=lambda n:[fillZero(n[1:]) for i in range(n[0])]

#as map, but on kd-matrices.
def kdmap(f,d,n):
	if len(n)==1:
		return map(f,d)
	else:
		return [kdmap(f,d[i],n[1:]) for i in range(n[0])]
		
class Result(object):
	def __init__(self, fileName, fill=True, sort=True):
		reader=csv.reader(open('results/'+fileName, 'rb'), delimiter='\t')
		nbrOfDim=len(reader.next())-1
		self.dims=[[] for i in range(nbrOfDim)]
		self.dataList=[]
		for row in reader:
			if len(row)!=nbrOfDim+1: raise Exception('Error in resultfile, wrong number of tabs on line.')
			for i in range(nbrOfDim):
				if not toNum(row[i]) in self.dims[i]:
					self.dims[i].append(toNum(row[i]))
			self.dataList.append(([self.dims[i].index(toNum(row[i])) for i in range(nbrOfDim)],toNum(row[-1])))

		if sort:
			dperms=[sorted(range(len(d)),key=lambda k:d[k]) for d in self.dims]
			self.dims=[[self.dims[i][dperms[i][j]] for j in range(len(self.dims[i]))] for i in range(nbrOfDim)]
			self.dataList=[([dperms[i].index(d[i]) for i in range(len(d))],v) for d,v in self.dataList]
		
		if fill:
			self.data=fillZero(map(len,self.dims)+[0])
			def fillData(i,d,dl):
				if len(i)==0:
					dl.append(d)
				else:
					fillData(i[1:],d,dl[i[0]])

			for i,d in self.dataList:
				fillData(i,d,self.data)
				
class StatisticResult(Result):
	def __init__(self, fileName, fill=True):
		super(StatisticResult, self).__init__(fileName, fill)
		self.mean=kdmap(lambda s:np.mean(s),self.data,map(len,self.dims))
		self.std=kdmap(lambda s:np.std(s)/np.sqrt(len(s)),self.data,map(len,self.dims))
