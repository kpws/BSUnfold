import numpy as np

v=[[[[-1.0,1.0][i/6],(1+np.sqrt(5))/2*[-1.0,1.0][i/3%2],0][(j+i)%3] for j in range(3)] for i in range(12)]

#normalize
v=[iv/np.linalg.norm(iv) for iv in v]

#householder transformation to get one of the axes on y-axis
mirror=np.array([0,1,0])-v[0]
mirror/=np.linalg.norm(mirror)
v=[iv-2*mirror*np.dot(mirror,iv) for iv in v]



if __name__ == '__main__':
	for i in v:
		print np.linalg.norm(i)
	
	import matplotlib as mpl
	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = Axes3D(fig)

	for i in v:
		ax.plot(*[[0,i[j]] for j in range(3)])
	ax.plot([0,0],[-1,1],[0,0],'o-k')
	plt.show()
