#!/usr/bin/env python

import matplotlib.pyplot as plt
runs = 1
for i in range(runs):
	file = open("/home/msr/catkin_ws/src/rupert_learns/src/run"+str(i+1)+"/evolution_1_fitness.txt")
	text = file.read()
	numbers = text.split(",")[:-1]
	plt.plot(numbers,label=str(i+1))
plt.legend()
plt.show()
