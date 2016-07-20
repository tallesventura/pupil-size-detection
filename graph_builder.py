from matplotlib import pyplot as plt 
import numpy as np 


# ===Description: ----------------------------------------------------------------------------------
# Plots the graph for the 4 combinations of light intensity and frequency
# ---Arguments: ------------------------------------------------------------------------------------
# x1:		list of the x axis values for the 1st light exposure
# x2:		list of the x axis values for the 2nd light exposure
# x3:		list of the x axis values for the 3rd light exposure
# x4:		list of the x axis values for the 4th light exposure
# y1:		list of the y axis values for the 1st light exposure
# y2:		list of the y axis values for the 2nd light exposure
# y3:		list of the y axis values for the 3rd light exposure
# y4:		list of the y axis values for the 4th light exposure
# name1:	label for the 1st light exposure graph
# name2:	label for the 2nd light exposure graph
# name3:	label for the 3rd light exposure graph
# name4: 	label for the 4th light exposure graph
# --------------------------------------------------------------------------------------------------
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