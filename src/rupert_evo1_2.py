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
from controller_manager_msgs.srv import LoadController, UnloadController, SwitchController
from gazebo_msgs.srv import SetModelConfiguration
from std_msgs.msg import Float64
from gazebo_msgs.srv import DeleteModel, SpawnModel
from std_srvs.srv import Empty



# global variables
population_size = 64
pop = []
surv = []
sco = []
hei = []
dis = []
length = 256
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
		individual.append(random.randint(-6, 6))
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
	pose = Pose()
	pose.position.x = 0
	pose.position.y = 0
	pose.position.z = 0.2
	pose.orientation.x = 0
	pose.orientation.y = 0
	pose.orientation.z = 0
	pose.orientation.w = 1

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
	p = os.popen("rosrun xacro xacro.py " + "~/catkin_ws/src/rupert_learns/urdf/rupert.xacro")
	xml_string = p.read()
	p.close()
	
	spawn_model("rupert",xml_string,"",pose,"world")
	load_controllers()
	rospy.sleep(3)

	height_average = 0
	height_count = 0
	for i in range(len(guess)):
		if(i%8==0):
			#print(i)
			knee1.publish((guess[i]/6.0)*limit)
			knee2.publish((guess[i+1]/6.0)*limit)
			knee3.publish((guess[i+2]/6.0)*limit)
			knee4.publish((guess[i+3]/6.0)*limit)
			ankle1.publish(((guess[i+4])/6.0)*limit)
			ankle2.publish(((guess[i+5])/6.0)*limit)
			ankle3.publish(((guess[i+6])/6.0)*limit)
			ankle4.publish(((guess[i+7])/6.0)*limit)
			rospy.sleep(0.8)
	performance = final_position - initial_position + height_average
	rec_count = 0
	#unload_controllers()
	delete_model("rupert")
	return performance, final_position, height_average


def best_n(n, scores):
	global surv
	global sco
	global pop
	global hei
	global dis
	surv = []
	sco = []
	hei2 = hei 
	dis2 = dis
	hei = []
	dis = [] 
	for i in range(n):
		index = np.argmax(scores)
		surv.append(pop[index])
		sco.append(scores[index])
		hei.append(hei2[index])
		dis.append(dis2[index])
		pop.pop(index)
		scores = np.delete(scores, index)
		hei2.pop(index)
		dis2.pop(index)
	pop = surv

def mate(individual1, individual2):
	index = random.randint(0, len(individual1)-1)
	child1 = individual1[:index]+individual2[index:]
	child2 = individual2[:index]+individual1[index:]
	return child1, child2

def mutate(radiation1, radiation2):
	global pop
	global sco
	global hei
	global dis
	for i in range(int(radiation1*(population_size/2))):
		index = random.randint((population_size/2),(population_size-1))
		print(index)
		for j in range(int(radiation2*length)):
			index2 = random.randint(0,length-1)
			specimen = pop[index]
			begin = specimen[:index2]
			end = specimen[index2+1:]
			begin.append(random.randint(-6, 6))
			specimen = begin + end
		print(specimen)
		pop[index] = specimen
		sco[index],dis[index],hei[index] = fitness(pop[index])

def callback(data):
	global height_count
	global final_position
	global ride_height
	global height_average
	try:
		height_count = height_count + 1
		ride_height = data.pose[1].position.z
		height_average += (ride_height/height_count)
		final_position = math.sqrt(((data.pose[1].position.x)*(data.pose[1].position.x))+((data.pose[1].position.y)*(data.pose[1].position.y)))
		#rospy.loginfo(final_position)
	except:
		pass

def main():
	global hei
	global dis
	global pop
	global sco
	global surv
	sco = []
	pop = []
	surv = []
	hei = []
	dis = []
	running_fitness = []
	running_height = []
	running_dist = []
	generation = 0
	load_controllers()
	delete_model("rupert")
	first_population(population_size,length)
	for i in range(population_size):
		score, distance_temp, height_temp = fitness(pop[i])
		print("individual "+ str(i)+": "+str(score))
		sco.append(score)
		hei.append(height_temp)
		dis.append(distance_temp)
	fit = np.array(sco)
	height_arr = np.array(hei)
	dist_arr = np.array(dis)
	while(generation<150):
		generation += 1
		print("generation: "+ str(generation))	
		best_n(population_size/2, fit)

		for j in range(len(pop)):
			if(j%2==0):
				child1, child2 = mate(pop[j],pop[j+1])
				pop.append(child1)
				pop.append(child2)
				fitness_temp, distance_temp, height_temp = fitness(child1)
				sco.append(fitness_temp)
				hei.append(height_temp)
				dis.append(distance_temp)
				print("individual "+ str(j)+": "+str(sco[-1]))
				fitness_temp, distance_temp, height_temp = fitness(child2)
				sco.append(fitness_temp)
				hei.append(height_temp)
				dis.append(distance_temp)
				print("individual "+ str(j+1)+": "+str(sco[-1]))
		# change this to only mutate children
		if generation<100:
			mutate(0.6,0.4)
		else:
			mutate(0.4,0.2)
		fit = np.array(sco)
		height_arr = np.array(hei)
		dist_arr = np.array(dis)
		running_fitness.append(np.max(fit))
		running_height.append(np.max(height_arr))
		running_dist.append(np.max(dist_arr))
		file = open("evolution_1_gen"+str(generation)+".txt","w") 
		file.write(str(pop))
		file.write(str(sco))
		file.close
	file = open("evolution_1_genf.txt","w") 
	index_best = np.argmax(fit)
	print(pop[index_best])
	for i in range(len(pop)):
		file.write(str(sco[i])+": ") 
		file.write(str(pop[i]))
		file.write("\n \n")
	rospy.loginfo("Done")
	file.close() 
	file = open("evolution_1_fitness.txt","w") 
	for i in range(len(running_fitness)):
		file.write(str(running_fitness[i])+",") 
	rospy.loginfo("Done")
	file.close() 
	file = open("evolution_1_breakdown.txt","w") 
	file.write(str(running_dist)+"\n")
 	file.write(str(running_height)+"\n")
	rospy.loginfo("Done")
	file.close() 


# running_total = 0
# for i in range(100):
# 	score = main()
# 	if (score==1):
# 		running_total = running_total+1
# print(running_total)
def load_controllers():
	rospy.loginfo("STARTING")
	rospy.wait_for_service('rupert/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('rupert/controller_manager/switch_controller')
	controllers = ['joint_state_controller','/rupert/joint1_position_controller','/rupert/joint2_position_controller','/rupert/joint3_position_controller','/rupert/joint4_position_controller','/rupert/joint5_position_controller','/rupert/joint6_position_controller','/rupert/joint7_position_controller','/rupert/joint8_position_controller','/rupert/joint9_position_controller','/rupert/joint10_position_controller','/rupert/joint11_position_controller','/rupert/joint12_position_controller']
	for i in controllers:
		load_controller(i)
		print("loaded:"+str(i))
	switch_controller(controllers,[],2)

def unload_controllers():
	rospy.loginfo("STARTING")
	rospy.wait_for_service('rupert/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('rupert/controller_manager/switch_controller')
	controllers = ['joint_state_controller','/rupert/joint1_position_controller','/rupert/joint2_position_controller','/rupert/joint3_position_controller','/rupert/joint4_position_controller','/rupert/joint5_position_controller','/rupert/joint6_position_controller','/rupert/joint7_position_controller','/rupert/joint8_position_controller','/rupert/joint9_position_controller','/rupert/joint10_position_controller','/rupert/joint11_position_controller','/rupert/joint12_position_controller']
	switch_controller([],controllers,2)
	for i in controllers:
		unload_controller(i)
		print("unloaded:"+str(i))
	
if __name__=='__main__':
	rospy.init_node('rupert_evo')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/gazebo/reset_world')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/gazebo/delete_model')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/gazebo/spawn_urdf_model')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('rupert/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('rupert/controller_manager/switch_controller')
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
	delete_model = rospy.ServiceProxy("gazebo/delete_model", DeleteModel)
	spawn_model = rospy.ServiceProxy("gazebo/spawn_urdf_model", SpawnModel)
	reset_simulation = rospy.ServiceProxy('/gazebo/reset_world', Empty)
	unload_controller = rospy.ServiceProxy('rupert/controller_manager/unload_controller', UnloadController)
	load_controller = rospy.ServiceProxy('rupert/controller_manager/load_controller', LoadController)
	switch_controller = rospy.ServiceProxy('rupert/controller_manager/switch_controller', SwitchController)
	main()
	# except KeyboardInterrupt:
	# 	print ("Shutting Down")

