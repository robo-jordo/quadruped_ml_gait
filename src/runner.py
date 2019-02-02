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

final_position = 0
best = [3, 4, -3, -5, -1, 0, 3, 1, 6, -5, -1, -6, 1, -6, 3, -2, -3, 3, 2, -5, -4, -5, -2, 0, 3, 3, -6, 4, -5, -6, 6, 0, -2, 4, -6, -6, -1, 5, 3, 3, 6, -2, 4, 2, -6, 0, 4, -3, -4, 2, 0, -5, 4, 4, 2, -6, -4, 1, 1, -6, 6, -5, -3, 2]
limit = 1.6

def callback(data):
	global final_position 
	final_position = math.sqrt(((data.pose[1].position.x)*(data.pose[1].position.x))+((data.pose[1].position.y)*(data.pose[1].position.y)))
	#rospy.loginfo(final_position)


def main():
	for j in range(5):
		for i in range(len(best)):
			if(i%8==0):
				#print(i)
				knee1.publish((best[i]/6.0)*limit)
				knee2.publish((best[i+1]/6.0)*limit)
				knee3.publish((best[i+2]/6.0)*limit)
				knee4.publish((best[i+3]/6.0)*limit)
				ankle1.publish((best[i+4]/6.0)*limit)
				ankle2.publish((best[i+5]/6.0)*limit)
				ankle3.publish((best[i+6]/6.0)*limit)
				ankle4.publish((best[i+7]/6.0)*limit)
				rospy.sleep(1)
	performance = final_position

if __name__=='__main__':
	rospy.init_node('runner')
	rospy.loginfo("STARTING")
	rospy.wait_for_service('/gazebo/reset_world')
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
	main()