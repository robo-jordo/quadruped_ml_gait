#!/usr/bin/env python

# Full implementation

import random
import numpy as np
import rospy 
import os
import math
import tf
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
## Defaults
population_size = 64
length = 32
limit = 1.6
hip_position = 0
phased_gait = False
static_hip = True
bias = True


## Structures and constants
pop = []
surv = []
sco = []
hei = []
dis = []
xml_string = ''
final_position = 0
initial_position = 0
height_count = 0
height_average = 0
pitch_average = 0
roll_average = 0
ride_height = 0
rec_count = 0
unfit_count = []
num_unfit = 0
unfit = False 


def create_individual(length):
	individual_string = []
	offsets = []
	for i in range(length):
		if (bias ==True):
			individual_string.append(random.randint(-6, 6))
		else:
			individual.append(random.randint(-8, 4))
	if (phased_gait == True):
		for i in range(3):
			offsets.append(random.randint(0, length))
		individual = [individual_string, offsets]
	return individual

def first_population(pop_size, length):
	global pop
	for i in range(pop_size):
		pop.append(create_individual(length))

def fitness(individual_given):
	global height_average
	global pitch_average
	global roll_average
	global height_count
	global rec_count
	global length
	global unfit

	pose = Pose()
	pose.position.x = 0
	pose.position.y = 0
	pose.position.z = 0.2
	pose.orientation.x = 0
	pose.orientation.y = 0
	pose.orientation.z = 0
	pose.orientation.w = 1

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
	try:
		load_controllers()
	except:
        try:
		    delete_model("rupert")
        except:
		    rospy.sleep(2)
            try:
		        spawn_model("rupert")
            except: 
                pass
		load_controllers()

	height_average = 0
	pitch_average = 0
	roll_average = 0
	height_count = 0
    if (phased_gait == True):
	    individual = individual_given[0]
	    offset = individual_given[1]
	else:
		individual = individual_given
	for i in range(len(individual)):
        if (static_hip == True):
			wrap = 8
			hip_offset = 0
		    hip1.publish(hip_position)
		    hip2.publish(hip_position)
		    hip3.publish(hip_position)
		    hip4.publish(hip_position)
		else:
			hip1.publish((individual[i]/bias_div)*limit)
			hip2.publish((individual[i+1]/bias_div)*limit)
			hip3.publish((individual[i+2]/bias_div)*limit)
			hip4.publish((individual[i+3]/bias_div)*limit)
			wrap = 12
			hip_offset = 4
		if (unfit == True):
			performance = -1000
			unfit = False
			delete_model("rupert")
			return performance, 0 ,0
        if (phased_gait==True):
			if(i%2==0):
				knee1.publish((individual[i]/bias_div)*limit)
				ankle1.publish((individual[i+1]/bias_div)*limit)
				if((i+offset[0]+1)<length):
					knee2.publish((individual[(i+offset[0])]/bias_div)*limit)
					ankle2.publish((individual[(i+offset[0]+1)]/bias_div)*limit)
				else:
					knee2.publish((individual[(i+offset[0]-length)]/bias_div)*limit)
					ankle2.publish((individual[(i+offset[0]+1-length)]/bias_div)*limit)
				if((i+offset[1]+1)<length):
					knee3.publish((individual[(i+offset[1])]/bias_div)*limit)
					ankle3.publish((individual[(i+offset[1]+1)]/bias_div)*limit)
				else:
					knee3.publish((individual[(i+offset[1]-length)]/bias_div)*limit)
					ankle3.publish((individual[(i+offset[1]+1-length)]/bias_div)*limit)
				if((i+offset[2]+1)<length):
					knee4.publish((individual[(i+offset[2])]/bias_div)*limit)
					ankle4.publish((individual[(i+offset[2]+1)]/bias_div)*limit)
				else:
					knee4.publish((individual[(i+offset[2]-length)]/bias_div)*limit)
					ankle4.publish((individual[(i+offset[2]+1-length)]/bias_div)*limit)
		else:
			if(i%wrap==0):
				knee1.publish((individual[i+hip_offset]/bias_div)*limit)
				knee2.publish((individual[i+hip_offset+1]/bias_div)*limit)
				knee3.publish((individual[i+hip_offset+2]/bias_div)*limit)
				knee4.publish((individual[i+hip_offset+3]/bias_div)*limit)
				ankle1.publish(((individual[i+hip_offset+4])/bias_div)*limit)
				ankle2.publish(((individual[i+hip_offset+5])/bias_div)*limit)
				ankle3.publish(((individual[i+hip_offset+6])/bias_div)*limit)
				ankle4.publish(((individual[i+hip_offset+7])/bias_div)*limit)

		rospy.sleep(1)
	performance = final_position - initial_position + height_average/height_count - roll_average/height_count - pitch_average/height_count
	rec_count = 0
	delete_model("rupert")
	if (unfit == True):
		performance = -1000
		unfit = False
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
	local_count = 0
	for i in range(n):
		weighted_random = []
		mid = np.mean(scores)
		minimum = np.min(scores)
		for j in range(population_size-i):
			weighted_random = weighted_random + ([j] * int(math.ceil((scores[j]-minimum)*10)))
		index = random.choice(weighted_random)
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
	individual1_string = individual1[0]
	individual2_string = individual2[0]
	individual1_offset = individual1[1]
	individual2_offset = individual2[1]
	#print(individual1)
	#print(individual2)
	index = random.randint(0, len(individual1_string)-1)
	index2 = random.randint(0, 3)
	child1_string = individual1_string[:index]+individual2_string[index:]
	child2_string = individual2_string[:index]+individual1_string[index:]
	child1_offset = individual1_offset[:index2]+individual2_offset[index2:]
	child2_offset = individual2_offset[:index2]+individual1_offset[index2:]
	child1 = [child1_string,child1_offset]
	child2 = [child2_string,child2_offset]
	#print("child:"+str(child1))
	#print("child:"+str(child2))
	return child1, child2

def mutate(radiation1, radiation2):
	global pop
	global sco
	global hei
	global dis
	for i in range(int(radiation1*(population_size))):
		new_offsets = []
		index = random.randint(0,(population_size-1))
		for j in range(int(radiation2*length)):
			index2 = random.randint(0,length-1)
			specimen = pop[index][0]
			begin = specimen[:index2]
			end = specimen[index2+1:]
			begin.append(random.randint(-6, 6))
			specimen = begin + end
		print(specimen)
		for k in range(3):
			new_offsets.append(random.randint(0, length))
		new_specimen = [specimen,new_offsets] 
		print("mutt:"+str(new_specimen))
		pop[index] = new_specimen
		sco[index],dis[index],hei[index] = fitness(pop[index])

def callback(data):
	global height_count
	global final_position
	global ride_height
	global height_average
	global pitch_average
	global roll_average
	global unfit
	try:
		quaternion = (data.pose[1].orientation.x,data.pose[1].orientation.y,data.pose[1].orientation.z,data.pose[1].orientation.w)
		euler = tf.transformations.euler_from_quaternion(quaternion)
		roll = math.sqrt(euler[0]*euler[0])
		pitch = math.sqrt(euler[1]*euler[1])
		yaw = math.sqrt(euler[2]*euler[2])
		if (roll>0.785398):
			print("flipped")
			unfit = True
		if (pitch>0.785398):
			print("flipped")
			unfit = True
		height_count = height_count + 1
		ride_height = data.pose[1].position.z
		pitch_average = pitch_average+pitch
		roll_average = roll_average+pitch
		height_average = height_average + ride_height
		final_position = math.sqrt(((data.pose[1].position.x)*(data.pose[1].position.x)))
	except:
		pass


def main():
	global hei
	global dis
	global pop
	global sco
	global surv
	global unfit_count
	global num_unfit
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
		while(score == -1000):
			num_unfit = num_unfit + 1
			pop[i] = create_individual(length)
			score, distance_temp, height_temp = fitness(pop[i])
			print("replacing pop 0 individual")
		print("individual "+ str(i)+": "+str(score))
		sco.append(score)
		hei.append(height_temp)
		dis.append(distance_temp)
	fit = np.array(sco)
	height_arr = np.array(hei)
	dist_arr = np.array(dis)
	unfit_count.append(num_unfit)
	num_unfit = 0
	while(generation<150):
		generation += 1
		print("generation: "+ str(generation))	
		best_n(population_size/2, fit)



		for j in range(len(pop)):
			if(j%2==0):
				partner1 = random.randint(0, len(pop)-1)
				partner2 = random.randint(0, len(pop)-1)
				child1, child2 = mate(pop[partner1],pop[partner2])
				pop.append(child1)
				pop.append(child2)
				fitness_temp, distance_temp, height_temp = fitness(child1)
				while(fitness_temp == -1000):
					num_unfit = num_unfit + 1
					pop[-2] = create_individual(length)
					fitness_temp, distance_temp, height_temp = fitness(pop[-2])
					print("replacing child")
				sco.append(fitness_temp)
				hei.append(height_temp)
				dis.append(distance_temp)
				print("individual "+ str(j)+": "+str(sco[-1]))
				fitness_temp, distance_temp, height_temp = fitness(child2)
				while(fitness_temp == -1000):
					num_unfit = num_unfit + 1
					pop[-1] = create_individual(length)
					fitness_temp, distance_temp, height_temp = fitness(pop[-1])
					print("replacing child")
				sco.append(fitness_temp)
				hei.append(height_temp)
				dis.append(distance_temp)
				print("individual "+ str(j+1)+": "+str(sco[-1]))
		# change this to only mutate children
		if generation<100:
			mutate(0.4,0.5)
		else:
			mutate(0.4,0.3)
		unfit_count.append(num_unfit)
		num_unfit = 0
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
		file = open("evolution_invalids.txt","w") 
		file.write(str(unfit_count))
		file.close
	file = open("evolution_1_genf.txt","w") 
	index_best = np.argmax(fit)
	
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
		#print("loaded:"+str(i))
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
		#print("unloaded:"+str(i))
	
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
	
	
	if (bias == True):
		bias_div = 8.0
	else:
		bias_div = 6.0
		
	main()
	# except KeyboardInterrupt:
	# 	print ("Shutting Down")

