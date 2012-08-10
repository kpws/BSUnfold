import csv

reader=csv.reader(open('data/milanoReference', 'rb'), delimiter='\t')
firstRow=reader.next()

r=[]
for i in range(1,len(firstRow)-2):
	r.append(float(firstRow[i])/10/2)

E=[]
rate=[]
for row in reader:
	rate.append([])
	E.append(float(row[0])/1000)
	for c in range(1,len(row)-2):
		rate[-1].append(float(row[c])/1000)
