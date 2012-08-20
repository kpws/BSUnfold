import csv

reader=csv.reader(open('data/milanoReference', 'rb'), delimiter='\t')
firstRow=reader.next()

names=[]
for i in range(1,len(firstRow)):
	names.append(firstRow[i])

E=[]
rate=[]
for row in reader:
	rate.append([])
	E.append(float(row[0])/1000)
	for c in range(1,len(row)):
		rate[-1].append(float(row[c])/1000)

r={'81':81.0/10/2,
   '108':108.0/10/2,
   '133':133.0/10/2,
   '178':178.0/10/2,
   '233':233.0/10/2,
   '81+lead':81.0/10/2+2.0,
   'Linus':12.5}
