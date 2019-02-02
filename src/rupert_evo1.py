#!/usr/bin/env python

import random
import numpy as np
import rospy 
import os
import math
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import SetModelConfiguration
from std_msgs.msg import Float64
from gazebo_msgs.srv import DeleteModel, SpawnModel
from std_srvs.srv import Empty



# global variables
population_size = 32
pop = []
surv = []
sco = []
length = 128
limit = 1.6
xml_string = ''
final_position = 0
initial_position = 0
height_count = 0
height_average = 0
ride_height = 0
rec_count = 0

def create_individual(length):
	individual = []
	for i in range(length):
		individual.append(random.randint(-8, 4))
	return individual

def first_population(pop_size, length):
	global pop
	for i in range(pop_size):
		pop.append(create_individual(length))


# def fitness(password, guess):
# 	if (len(password)!=len(guess)):
# 		print("wrong length")
# 		return -1
# 	else:
# 		score = 0
# 		for i in range(len(password)):
# 			if(password[i]==guess[i]):
# 				score = score + 1.0
# 		return score/(len(password))

def fitness(guess):
	global height_average
	global height_count
	global rec_count
	knee1.publish(0)
	knee2.publish(0)
	knee3.publish(0)
	knee4.publish(0)
	ankle1.publish(0)
	ankle2.publish(0)
	ankle3.publish(0)
	ankle4.publish(0)
	hip1.publish(0)
	hip2.publish(0)
	hip3.publish(0)
	hip4.publish(0)
	reset_simulation()
	rospy.sleep(3)
	reset_simulation()
	rospy.sleep(3)
	height_average = 0
	height_count = 0
	for i in range(len(guess)):
		if(i%8==0):
			#print(i)
			knee1.publish((guess[i]/8.0)*limit)
			knee2.publish((guess[i+1]/8.0)*limit)
			knee3.publish((guess[i+2]/8.0)*limit)
			knee4.publish((guess[i+3]/8.0)*limit)
			ankle1.publish(((guess[i+4]-4)/8.0)*limit)
			ankle2.publish(((guess[i+5]-4)/8.0)*limit)
			ankle3.publish(((guess[i+6]-4)/8.0)*limit)
			ankle4.publish(((guess[i+7]-4)/8.0)*limit)
			rospy.sleep(0.8)
	performance = final_position-initial_position + height_average/8
	if (final_position>2 and rec_count<2):
		print("recheck")
		rec_count = rec_count + 1
		performance = fitness(guess)
	rec_count = 0
	return performance


def best_n(n, scores):
	global surv
	global sco
	global pop
	surv = []
	sco = []
	for i in range(n):
		index = np.argmax(scores)
		surv.append(pop[index])
		sco.append(scores[index])
		pop.pop(index)
		scores = np.delete(scores, index)
	pop = surv

def mate(individual1, individual2):
	index = random.randint(0, len(individual1)-1)
	child1 = individual1[:index]+individual2[index:]
	child2 = individual2[:index]+individual1[index:]
	return child1, child2

def mutate(radiation):
	global pop
	global sco
	for i in range(int(radiation*(population_size/2))):
		index = random.randint((population_size/2),(population_size-1))
		print(index)
		for j in range(int(radiation*length)):
			index2 = random.randint(0,length-1)
			specimen = pop[index]
			begin = specimen[:index2]
			end = specimen[index2+1:]
			begin.append(random.randint(-8, 4))
			specimen = begin + end
		print(specimen)
		pop[index] = specimen
		sco[index] = fitness(pop[index])

def callback(data):
	global height_count
	global final_position
	global ride_height
	global height_average
	height_count = height_count + 1
	ride_height = data.pose[1].position.z
	height_average += (ride_height/height_count)
	final_position = math.sqrt(((data.pose[1].position.x)*(data.pose[1].position.x))+((data.pose[1].position.y)*(data.pose[1].position.y)))
	#rospy.loginfo(final_position)

def main():

	global pop
	global sco
	global surv
	sco = []
	pop = []
	surv = []
	generation = 0

	first_population(population_size,length)
	for i in range(population_size):
		score = fitness(pop[i])
		print("individual "+ str(i)+": "+str(score))
		sco.append(score)
	fit = np.array(sco)
	while(generation<30):
		generation += 1
		print("generation: "+ str(generation))	
		best_n(population_size/2, fit)

		for j in range(len(pop)):
			if(j%2==0):
				child1, child2 = mate(pop[j],pop[j+1])
				pop.append(child1)
				pop.append(child2)
				sco.append(fitness(child1))
				print("individual "+ str(j)+": "+str(sco[-1]))
				sco.append(fitness(child2))
				print("individual "+ str(j+1)+": "+str(sco[-1]))
		# change this to only mutate children
		if generation<15:
			mutate(0.4)
		else:
			mutate(0.2)
		fit = np.array(sco)
	file = open("evolution1.txt","w") 
	index_best = np.argmax(fit)
	print(pop[index_best])
	for i in range(len(pop)):
		file.write(str(sco[i])+": ") 
		file.write(str(pop[i]))
		file.write("\n \n")
	rospy.loginfo("Done")
	file.close() 


# running_total = 0
# for i in range(100):
# 	score = main()
# 	if (score==1):
# 		running_total = running_total+1
# print(running_total)
if __name__=='__main__':
	rospy.init_node('rupert_evo')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/gazebo/reset_world')
	rospy.wait_for_service('/rupert/controller_manager/relaod_controller_libraries')
	rospy.Subscriber('/gazebo/model_states', ModelStates, callback)
	hip1 = rospy.Publisher('/rupert/joint5_position_controller/command', Float64, queue_size=1)
	hip2 = rospy.Publisher('/rupert/joint6_position_controller/command', Float64, queue_size=1)
	hip3 = rospy.Publisher('/rupert/joint7_position_controller/command', Float64, queue_size=1)
	hip4 = rospy.Publisher('/rupert/joint8_position_controller/command', Float64, queue_size=1)
	knee1 = rospy.Publisher('/rupert/joint1_position_controller/command', Float64, queue_size=1)
	knee2 = rospy.Publisher('/rupert/joint2_position_controller/command', Float64, queue_size=1)
	knee3 = rospy.Publisher('/rupert/joint3_position_controller/command', Float64, queue_size=1)
	knee4 = rospy.Publisher('/rupert/joint4_position_controller/command', Float64, queue_size=1)
	ankle1 = rospy.Publisher('/rupert/joint9_position_controller/command', Float64, queue_size=1)
	ankle2 = rospy.Publisher('/rupert/joint10_position_controller/command', Float64, queue_size=1)
	ankle3 = rospy.Publisher('/rupert/joint11_position_controller/command', Float64, queue_size=1)
	ankle4 = rospy.Publisher('/rupert/joint12_position_controller/command', Float64, queue_size=1)
	rospy.loginfo("STARTING")
		
		# maybe do some 'wait for service' here
	reset_simulation = rospy.ServiceProxy('/gazebo/reset_world', Empty)
	reset_controller = rospy.ServiceProxy('/rupert/controller_manager/relaod_controller_libraries')
	main()
	# except KeyboardInterrupt:
	# 	print ("Shutting Down")

