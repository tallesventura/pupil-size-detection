from matplotlib import pyplot as plt 
import numpy as np 



def plot_graph(x1,y1,x2,y2,x3,y3,x4,y4,name1,name2,name3,name4):
	plt.plot(x1,y1,'r',label=name1,linewidth=2.0)
	plt.plot(x2,y2,'g',label=name2,linewidth=2.0)
	plt.plot(x3,y3,'b',label=name3,linewidth=2.0)
	plt.plot(x4,y4,'k',label=name4,linewidth=2.0)
	plt.xlabel("Time (sec.)")
	plt.ylabel('% \of Baseline Area')
	plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,
           ncol=4, borderaxespad=0.)
	plt.show()