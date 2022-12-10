from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
 

def MergeSort(list):
	half = int(len(list)/2)
	left = list[0:half]
	right = list[half:len(list)]
	if len(list) > 2:
		left = MergeSort(left)
	if len(right) >=2:
		right = MergeSort(right)
	new = []
	while(len(left)>0 and len(right)>0):
		if right[0] <= left[0]:
			new.append(right.pop(0))
		else:
			new.append(left.pop(0))
	return new +  left + right
	
def RangeFind(*args):
	Quart = len(args) <= 1
	l2 = MergeSort(args[0])
	listhalf = 0
	if len(l2)%2 == 0:
		listhalf=int(len(l2)/2)
		mean = ((l2[listhalf-1] + l2[listhalf])/2)
	else:
		listhalf = int((len(l2)/2)-0.5)
		mean = l2.pop(listhalf)

	if Quart:		
		Q1 = RangeFind(l2[0:listhalf], False)
		Q3 = RangeFind(l2[listhalf:len(l2)], False)
		IQR = Q3 - Q1
		mina = l2.pop(0)
		maxa = l2.pop(-1)
		while (Q1 - (1.5*IQR)) > mina:
			mina = l2.pop(0)
		
		while (Q3 + (1.5*IQR)) < maxa:
			maxa = l2.pop(-1)
			
		mean = [mina, Q1, mean,Q3, maxa]
	return mean





Activations = ["He", "Nox", "Plu", "Ser", "Xav"]
Relu = []
Swish = []
Tanh = []

for Acti in Activations:
	r = open(Acti + "-US1990/ErrorAvrageRelu copy.txt")
	Rline = r.readlines()
	r.close()

	s = open(Acti + "-US1990/ErrorAvrageSwish copy.txt")
	Sline = s.readlines()
	s.close()

	t = open(Acti + "-US1990/ErrorAvrageTanh copy.txt")
	Tline = t.readlines()
	t.close()

	NewlisR = []
	NewlisS = []
	NewlisT = []
	for num in range(20):
		NewlisR.append(float(Rline[num]))
		NewlisS.append(float(Sline[num]))
		NewlisT.append(float(Tline[num]))

	Relu.append(NewlisR)
	Swish.append(NewlisS)
	Tanh.append(NewlisT)

	

ax = plt.subplot(322)
ax.boxplot(Relu, vert = 0)
plt.xlim(0, 0.6)
ax.set_yticklabels(Activations)
plt.title("Relu")
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

ax = plt.subplot(324)
ax.boxplot(Swish, vert = 0)
plt.xlim(0.04, 0.5)
ax.set_yticklabels(Activations)
plt.title("Swish")
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()


ax = plt.subplot(326)
ax.boxplot(Tanh, vert = 0)
plt.xlim(0.032, 0.08)
ax.set_yticklabels(Activations)
plt.title("Tanh")
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()



plt.tight_layout(pad=0.75)
# show plot
plt.show()