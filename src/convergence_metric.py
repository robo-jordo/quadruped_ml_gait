#!/usr/bin/env python

import numpy as np
import math
import matplotlib.pyplot as plt

generations = 149
pop_size = 64
convergence_metric = 0
gen = []
plot_score = []

def main(run):
	plot_score_temp = []
	for i in range(generations):
		gen = []
		file = open("/home/jordan/catkin_ws/src/rupert_learns/src/run"+str(run)+"/evolution_1_gen"+str(i+1)+".txt")
		text = file.read()
		text = text.split("]]")
		genes = text[0][1:]+']'
		genes = genes.split("]")

		#print(genes[0][1:])
		for i in range(pop_size):
			start = genes[i].find("[")
			item = genes[i][start+1:]
			listed = item.split(",")
			for j in range(len(listed)):
				listed[j]=int(listed[j])
			gen.append(listed)

		gen_arry = np.array(gen)
		#print(gen)
		gen_score = dist(gen_arry)
		plot_score_temp.append(gen_score)
		#print(gen_score)
	plot_score.append(plot_score_temp)
	print(plot_score)

def dist(generation):
	global convergence_metric
	convergence_metric= 0
	for i in range(len(generation)):

		for j in range(len(generation)):
			if (j>i):
				dist = np.linalg.norm(generation[i]-generation[j])
				convergence_metric = convergence_metric + dist
	return convergence_metric/(math.factorial(len(generation)))

main(1)
main(2)
main(3)
main(4)
plt.plot(plot_score[0],label='1')
plt.plot(plot_score[1],label='2')
plt.plot(plot_score[2],label='3')
plt.plot(plot_score[3],label='4')
plt.legend()
plt.show()

