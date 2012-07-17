import pylab as pl
import csv
import numpy as np



class Result:
	def __init__(self, fileName, nbrOfDim, fill=True):
		reader=csv.reader(open('results/'+fileName, 'rb'), delimiter='\t')
		reader.next()#skip header
		self.dims=[ []for i in range(nbrOfDim)]
		self.dataList=[]
		for row in reader:
			for i in range(nbrOfDim):
				if not row[i] in self.dims[i]:
					self.dims[i].append(row[i])
			self.dataList.append(([self.dims[i].index(row[i]) for i in range(nbrOfDim)],row[nbrOfDim:]))

		if fill:
			fillZero=lambda n:[fillZero(n[1:]) for i in range(n[0])]
			self.data=fillZero(map(len,self.dims)+[0])
			def fillData(i,d,dl):
				if len(i)==0:
					dl.append(d)
				else:
					fillData(i[1:],d,dl[i[0]])

			for i,d in self.dataList:
				fillData(i,d,self.data)
				
class StatisticResult(Result):
	def __init__(self, fileName, nbrOfDim, fill=True):
		super(StatisticResult, self).__init__(fileName, nbrOfDim, fill)
		def kdmap(f,)
			r=fillZero(map(len,self.dims)+[0])
		self.mean=
		self.std
		def fillData(i,d,dl):
				if len(i)==0:
					dl.append(d)
				else:
					fillData(i[1:],d,dl[i[0]])
