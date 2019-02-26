#!/usr/bin/env python

# Changed selection to be probabilistic since v1.4
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
length = 32
limit = 1.6
ruperts = 1
gazebos = 2
clearance = 9
xml_string = ''
final_position = 0
initial_position = 0
height_count = 0
height_average = 0
ride_height = 0
rec_count = 0

def create_individual(length):
	individual_string = []
	offsets = []
	for i in range(length):
		individual_string.append(random.randint(-6, 6))
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
	global height_count
	global rec_count
	global length


	
	make_models()


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


	height_average = 0
	height_count = 0

	individual = individual_given[0]
	offset = individual_given[1]
	print(individual)
	for i in range(len(individual)):
		if(i%2==0):
			knee1.publish((individual[i]/6.0)*limit)
			ankle1.publish((individual[i+1]/6.0)*limit)
			if((i+offset[0]+1)<length):
				knee2.publish((individual[(i+offset[0])]/6.0)*limit)
				ankle2.publish((individual[(i+offset[0]+1)]/6.0)*limit)
			else:
				knee2.publish((individual[(i+offset[0]-length)]/6.0)*limit)
				ankle2.publish((individual[(i+offset[0]+1-length)]/6.0)*limit)
			if((i+offset[1]+1)<length):
				knee3.publish((individual[(i+offset[1])]/6.0)*limit)
				ankle3.publish((individual[(i+offset[1]+1)]/6.0)*limit)
			else:
				knee3.publish((individual[(i+offset[1]-length)]/6.0)*limit)
				ankle3.publish((individual[(i+offset[1]+1-length)]/6.0)*limit)
			if((i+offset[2]+1)<length):
				knee4.publish((individual[(i+offset[2])]/6.0)*limit)
				ankle4.publish((individual[(i+offset[2]+1)]/6.0)*limit)
			else:
				knee4.publish((individual[(i+offset[2]-length)]/6.0)*limit)
				ankle4.publish((individual[(i+offset[2]+1-length)]/6.0)*limit)
		if(i%2==0):
			one_knee_0_1.publish((individual[i]/6.0)*limit)
			one_ankle_0_1.publish((individual[i+1]/6.0)*limit)
			if((i+offset[0]+1)<length):
				one_knee_0_2.publish((individual[(i+offset[0])]/6.0)*limit)
				one_ankle_0_2.publish((individual[(i+offset[0]+1)]/6.0)*limit)
			else:
				one_knee_0_2.publish((individual[(i+offset[0]-length)]/6.0)*limit)
				one_ankle_0_2.publish((individual[(i+offset[0]+1-length)]/6.0)*limit)
			if((i+offset[1]+1)<length):
				one_knee_0_3.publish((individual[(i+offset[1])]/6.0)*limit)
				one_ankle_0_3.publish((individual[(i+offset[1]+1)]/6.0)*limit)
			else:
				one_knee_0_3.publish((individual[(i+offset[1]-length)]/6.0)*limit)
				one_ankle_0_3.publish((individual[(i+offset[1]+1-length)]/6.0)*limit)
			if((i+offset[2]+1)<length):
				one_knee_0_4.publish((individual[(i+offset[2])]/6.0)*limit)
				one_ankle_0_4.publish((individual[(i+offset[2]+1)]/6.0)*limit)
			else:
				one_knee_0_4.publish((individual[(i+offset[2]-length)]/6.0)*limit)
				one_ankle_0_4.publish((individual[(i+offset[2]+1-length)]/6.0)*limit)
		if(i%2==0):
			two_knee_0_1.publish((individual[i]/6.0)*limit)
			two_ankle_0_1.publish((individual[i+1]/6.0)*limit)
			if((i+offset[0]+1)<length):
				two_knee_0_2.publish((individual[(i+offset[0])]/6.0)*limit)
				two_ankle_0_2.publish((individual[(i+offset[0]+1)]/6.0)*limit)
			else:
				two_knee_0_2.publish((individual[(i+offset[0]-length)]/6.0)*limit)
				two_ankle_0_2.publish((individual[(i+offset[0]+1-length)]/6.0)*limit)
			if((i+offset[1]+1)<length):
				two_knee_0_3.publish((individual[(i+offset[1])]/6.0)*limit)
				two_ankle_0_3.publish((individual[(i+offset[1]+1)]/6.0)*limit)
			else:
				two_knee_0_3.publish((individual[(i+offset[1]-length)]/6.0)*limit)
				two_ankle_0_3.publish((individual[(i+offset[1]+1-length)]/6.0)*limit)
			if((i+offset[2]+1)<length):
				two_knee_0_4.publish((individual[(i+offset[2])]/6.0)*limit)
				two_ankle_0_4.publish((individual[(i+offset[2]+1)]/6.0)*limit)
			else:
				two_knee_0_4.publish((individual[(i+offset[2]-length)]/6.0)*limit)
				two_ankle_0_4.publish((individual[(i+offset[2]+1-length)]/6.0)*limit)
			rospy.sleep(0.8)
	performance = final_position - initial_position + height_average
	rec_count = 0
	#unload_controllers()
	for i in range(ruperts):
		one_delete_model("/one/rupert"+str(i))
		two_delete_model("/two/rupert"+str(i))
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
			print(int(math.ceil((scores[j]-minimum)*10)))
			weighted_random = weighted_random + ([j] * int(math.ceil((scores[j]-minimum)*10)))
			print(weighted_random)
		index = random.choice(weighted_random)
		#print(weighted_random)
		print(index)
		#index = np.argmax(scores)
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
	index = random.randint(0, len(individual1_string)-1)
	index = random.randint(0, 3)
	child1_string = individual1_string[:index]+individual2_string[index:]
	child2_string = individual2_string[:index]+individual1_string[index:]
	child1_offset = individual1_string[:index]+individual2_string[index:]
	child2_offset = individual2_string[:index]+individual1_string[index:]
	child1 = [child1_string,child1_offset]
	child2 = [child2_string,child2_offset]
	return child1, child2

def mutate(radiation1, radiation2):
	global pop
	global sco
	global hei
	global dis
	new_offsets = []
	for i in range(int(radiation1*(population_size))):
		index = random.randint(0,(population_size-1))
		print(index)
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
		print(specimen)
		pop[index] = new_specimen
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

def make_models():
	env = ["one","two"]
	pattern = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
	for g in range(gazebos):
		for i in range(ruperts):
			p = os.popen("rosrun xacro xacro.py " + "~/catkin_ws/src/rupert_learns/urdf/rupert"+env[g]+str(i)+".xacro")
			xml_string = p.read()
			p.close()
			if (i==0):
				pose = Pose()
				pose.position.x = 0
				pose.position.y = 0
				pose.position.z = 0.2
				pose.orientation.x = 0
				pose.orientation.y = 0
				pose.orientation.z = 0
				pose.orientation.w = 1

			elif(i<len(pattern)+1):
				pose = Pose()
				pose.position.x = clearance*pattern[i-1][0]
				pose.position.y = clearance*pattern[i-1][1]
				pose.position.z = 0.2
				pose.orientation.x = 0
				pose.orientation.y = 0
				pose.orientation.z = 0
				pose.orientation.w = 1
			if g == 0:
				one_spawn_model("/"+env[g]+"/rupert"+str(i),xml_string,"",pose,"world")
			else:
				two_spawn_model("/"+env[g]+"/rupert"+str(i),xml_string,"",pose,"world")

			load_controllers(env[g],0)

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
	try:
		delete_model("rupert")
	except:
		pass
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
				partner1 = random.randint(0, len(pop)-1)
				partner2 = random.randint(0, len(pop)-1)
				child1, child2 = mate(pop[partner1],pop[partner2])
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
			mutate(0.4,0.5)
		else:
			mutate(0.4,0.3)
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
def load_controllers(num, model_num):
	unload_controller = rospy.ServiceProxy('/'+num+'/rupert'+str(model_num)+'/controller_manager/unload_controller', UnloadController)
	load_controller = rospy.ServiceProxy('/'+num+'/rupert'+str(model_num)+'/controller_manager/load_controller', LoadController)
	switch_controller = rospy.ServiceProxy('/'+num+'/rupert'+str(model_num)+'/controller_manager/switch_controller', SwitchController)
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/rupert'+str(model_num)+'/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/rupert'+str(model_num)+'/controller_manager/switch_controller')
	controllers = ['/'+num+'/joint_state_controller','/'+num+'/rupert'+str(model_num)+'/joint1_position_controller','/'+num+'/rupert'+str(model_num)+'/joint2_position_controller','/'+num+'/rupert'+str(model_num)+'/joint3_position_controller','/'+num+'/rupert'+str(model_num)+'/joint4_position_controller','/'+num+'/rupert'+str(model_num)+'/joint5_position_controller','/'+num+'/rupert'+str(model_num)+'/joint6_position_controller','/'+num+'/rupert'+str(model_num)+'/joint7_position_controller','/'+num+'/rupert'+str(model_num)+'/joint8_position_controller','/'+num+'/rupert'+str(model_num)+'/joint9_position_controller','/'+num+'/rupert'+str(model_num)+'/joint10_position_controller','/'+num+'/rupert'+str(model_num)+'/joint11_position_controller','/'+num+'/rupert'+str(model_num)+'/joint12_position_controller']
	for i in controllers:
		print("HERE")
		load_controller(i)
		#print("loaded:"+str(i))
	switch_controller(controllers,[],2)

def unload_controllers():
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/rupert'+str(model_num)+'/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/rupert'+str(model_num)+'/controller_manager/switch_controller')
	controllers = ['/'+num+'/joint_state_controller','/'+num+'/rupert'+str(model_num)+'/joint1_position_controller','/'+num+'/rupert'+str(model_num)+'/joint2_position_controller','/'+num+'/rupert'+str(model_num)+'/joint3_position_controller','/'+num+'/rupert'+str(model_num)+'/joint4_position_controller','/'+num+'/rupert'+str(model_num)+'/joint5_position_controller','/'+num+'/rupert'+str(model_num)+'/joint6_position_controller','/'+num+'/rupert'+str(model_num)+'/joint7_position_controller','/'+num+'/rupert'+str(model_num)+'/joint8_position_controller','/'+num+'/rupert'+str(model_num)+'/joint9_position_controller','/'+num+'/rupert'+str(model_num)+'/joint10_position_controller','/'+num+'/rupert'+str(model_num)+'/joint11_position_controller','/'+num+'/rupert'+str(model_num)+'/joint12_position_controller']
	switch_controller([],controllers,2)
	for i in controllers:
		unload_controller(i)
		#print("unloaded:"+str(i))


if __name__=='__main__':
	num = 'one'
	rospy.init_node('rupert_evo')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/gazebo/reset_world')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/gazebo/delete_model')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/gazebo/spawn_urdf_model')
	rospy.loginfo("STARTING")
	#rospy.wait_for_service('rupert/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	#rospy.wait_for_service('rupert/controller_manager/switch_controller')
	rospy.Subscriber('/'+num+'/gazebo/model_states', ModelStates, callback)

	hip1 = rospy.Publisher('/'+num+'/rupert/joint5_position_controller/command', Float64, queue_size=1)
	hip2 = rospy.Publisher('/'+num+'/rupert/joint6_position_controller/command', Float64, queue_size=1)
	hip3 = rospy.Publisher('/'+num+'/rupert/joint7_position_controller/command', Float64, queue_size=1)
	hip4 = rospy.Publisher('/'+num+'/rupert/joint8_position_controller/command', Float64, queue_size=1)
	knee1 = rospy.Publisher('/'+num+'/rupert/joint1_position_controller/command', Float64, queue_size=1)
	knee2 = rospy.Publisher('/'+num+'/rupert/joint2_position_controller/command', Float64, queue_size=1)
	knee3 = rospy.Publisher('/'+num+'/rupert/joint3_position_controller/command', Float64, queue_size=1)
	knee4 = rospy.Publisher('/'+num+'/rupert/joint4_position_controller/command', Float64, queue_size=1)
	ankle1 = rospy.Publisher('/'+num+'/rupert/joint9_position_controller/command', Float64, queue_size=1)
	ankle2 = rospy.Publisher('/'+num+'/rupert/joint10_position_controller/command', Float64, queue_size=1)
	ankle3 = rospy.Publisher('/'+num+'/rupert/joint11_position_controller/command', Float64, queue_size=1)
	ankle4 = rospy.Publisher('/'+num+'/rupert/joint12_position_controller/command', Float64, queue_size=1)
	
	one_hip_0_1 = rospy.Publisher('/'+num+'/rupert0/joint5_position_controller/command', Float64, queue_size=1)
	one_hip_0_2 = rospy.Publisher('/'+num+'/rupert0/joint6_position_controller/command', Float64, queue_size=1)
	one_hip_0_3 = rospy.Publisher('/'+num+'/rupert0/joint7_position_controller/command', Float64, queue_size=1)
	one_hip_0_4 = rospy.Publisher('/'+num+'/rupert0/joint8_position_controller/command', Float64, queue_size=1)
	one_knee_0_1 = rospy.Publisher('/'+num+'/rupert0/joint1_position_controller/command', Float64, queue_size=1)
	one_knee_0_2 = rospy.Publisher('/'+num+'/rupert0/joint2_position_controller/command', Float64, queue_size=1)
	one_knee_0_3 = rospy.Publisher('/'+num+'/rupert0/joint3_position_controller/command', Float64, queue_size=1)
	one_knee_0_4 = rospy.Publisher('/'+num+'/rupert0/joint4_position_controller/command', Float64, queue_size=1)
	one_ankle_0_1 = rospy.Publisher('/'+num+'/rupert0/joint9_position_controller/command', Float64, queue_size=1)
	one_ankle_0_2 = rospy.Publisher('/'+num+'/rupert0/joint10_position_controller/command', Float64, queue_size=1)
	one_ankle_0_3 = rospy.Publisher('/'+num+'/rupert0/joint11_position_controller/command', Float64, queue_size=1)
	one_ankle_0_4 = rospy.Publisher('/'+num+'/rupert0/joint12_position_controller/command', Float64, queue_size=1)

	one_delete_model = rospy.ServiceProxy("/"+num+"/gazebo/delete_model", DeleteModel)
	one_spawn_model = rospy.ServiceProxy("/"+num+"/gazebo/spawn_urdf_model", SpawnModel)
	one_reset_simulation = rospy.ServiceProxy('/'+num+'/gazebo/reset_world', Empty)
	one_unload_controller = rospy.ServiceProxy('/'+num+'/rupert/controller_manager/unload_controller', UnloadController)

	num = "two"
	rospy.init_node('rupert_evo')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/gazebo/reset_world')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/gazebo/delete_model')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/'+num+'/gazebo/spawn_urdf_model')
	rospy.loginfo("STARTING")
	#rospy.wait_for_service('rupert/controller_manager/load_controller')
	rospy.loginfo("STARTING")
	#rospy.wait_for_service('rupert/controller_manager/switch_controller')
	rospy.Subscriber('/'+num+'/gazebo/model_states', ModelStates, callback)
	two_hip_0_1 = rospy.Publisher('/'+num+'/rupert0/joint5_position_controller/command', Float64, queue_size=1)
	two_hip_0_2 = rospy.Publisher('/'+num+'/rupert0/joint6_position_controller/command', Float64, queue_size=1)
	two_hip_0_3 = rospy.Publisher('/'+num+'/rupert0/joint7_position_controller/command', Float64, queue_size=1)
	two_hip_0_4 = rospy.Publisher('/'+num+'/rupert0/joint8_position_controller/command', Float64, queue_size=1)
	two_knee_0_1 = rospy.Publisher('/'+num+'/rupert0/joint1_position_controller/command', Float64, queue_size=1)
	two_knee_0_2 = rospy.Publisher('/'+num+'/rupert0/joint2_position_controller/command', Float64, queue_size=1)
	two_knee_0_3 = rospy.Publisher('/'+num+'/rupert0/joint3_position_controller/command', Float64, queue_size=1)
	two_knee_0_4 = rospy.Publisher('/'+num+'/rupert0/joint4_position_controller/command', Float64, queue_size=1)
	two_ankle_0_1 = rospy.Publisher('/'+num+'/rupert0/joint9_position_controller/command', Float64, queue_size=1)
	two_ankle_0_2 = rospy.Publisher('/'+num+'/rupert0/joint10_position_controller/command', Float64, queue_size=1)
	two_ankle_0_3 = rospy.Publisher('/'+num+'/rupert0/joint11_position_controller/command', Float64, queue_size=1)
	two_ankle_0_4 = rospy.Publisher('/'+num+'/rupert0/joint12_position_controller/command', Float64, queue_size=1)


	rospy.loginfo("STARTING")
		
		# maybe do some 'wait for service' here

	two_delete_model = rospy.ServiceProxy("/"+num+"/gazebo/delete_model", DeleteModel)
	two_spawn_model = rospy.ServiceProxy("/"+num+"/gazebo/spawn_urdf_model", SpawnModel)
	two_reset_simulation = rospy.ServiceProxy('/'+num+'/gazebo/reset_world', Empty)
	two_unload_controller = rospy.ServiceProxy('/'+num+'/rupert/controller_manager/unload_controller', UnloadController)
	main()
	# except KeyboardInterrupt:
	# 	print ("Shutting Down")
