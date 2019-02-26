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
from controller_manager_msgs.srv import LoadController, UnloadController, SwitchController

final_position = 0

best = [2, -5, -5, -6, 4, -3, 4, 5, -5, 5, 5, 0, 6, -3, 1, 5, -6, -6, 3, -6, -1, -6, 6, -1, 0, 2, -4, -2, -6, 3, 0, 4, 3, 6, -5, -3, 2, -2, -4, 0, -3, -5, 6, -4, 4, 1, 4, 0, -2, -4, 2, -5, 1, -4, 0, -2, 2, -3, -1, -4, -5, 1, -6, 2, -5, 6, 6, -1, 0, 1, -1, 4, 1, -4, -5, 6, -2, -3, 5, 1, -1, 1, 3, 4, -3, -3, -1, -1, -2, -3, -5, -6, -2, -4, 4, 3, 0, -2, -6, -4, 5, -1, -4, 2, -3, 6, -5, -6, -3, 4, 1, 6, -1, -2, 3, -6, 1, -4, 5, 1, -4, -6, -4, -1, 3, -5, 6, -3, 4, -6, 2, -5, -3, -6, 2, -1, -2, -1, 5, -6, 4, -2, 2, -5, 1, -6, -3, -2, 1, 1, 1, -6, 6, -5, -6, 3, -3, 3, 4, -4, -2, -4, 6, -6, 4, -2, -6, -2, -3, -6, 2, 4, -5, -5, 6, -1, 6, 0, -6, 5, -3, -1, -5, -3, 4, 5, 1, 0, 5, 2, 6, 1, 4, 5, -3, 2, 3, 6, -6, 1, 2, -4, 5, 5, -1, 6, 3, -6, 2, 3, 2, 1, -6, 3, -6, -2, -5, -2, -1, -2, 2, -6, -4, -4, 5, 0, -4, -4, 1, -3, -4, -6, -3, -2, 6, 5, 2, -1, 1, -1, -1, -6, -5, -5, -5, 4, 3, 4, 3, 1, -5, 2, 4, 2, 0, 3]
limit = 1.6

def callback(data):
	global final_position 
	final_position = math.sqrt(((data.pose[1].position.x)*(data.pose[1].position.x))+((data.pose[1].position.y)*(data.pose[1].position.y)))
	#rospy.loginfo(final_position)


def main():
	load_controllers()
	hip1.publish(0)
	hip2.publish(0)
	hip3.publish(0)
	hip4.publish(0)
	rospy.loginfo("START")
	for j in range(5):
		for i in range(len(best)/4):
			if(i%8==0):
				#print(i)
				hip1.publish(0)
				hip2.publish(0)
				hip3.publish(0)
				hip4.publish(0)
				knee1.publish((best[i]/6.0)*limit)
				knee2.publish((best[i+1]/6.0)*limit)
				knee3.publish((best[i+2]/6.0)*limit)
				knee4.publish((best[i+3]/6.0)*limit)
				ankle1.publish((best[i+4]/6.0)*limit)
				ankle2.publish((best[i+5]/6.0)*limit)
				ankle3.publish((best[i+6]/6.0)*limit)
				ankle4.publish((best[i+7]/6.0)*limit)
				rospy.sleep(1)
				rospy.loginfo("STARTING")
	performance = final_position
	
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

if __name__=='__main__':
	rospy.init_node('runner')
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
	rospy.loginfo("STAR")
		# maybe do some 'wait for service' here
	reset_simulation = rospy.ServiceProxy('/gazebo/reset_world', Empty)
	main()
