#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import SetModelConfiguration
from std_msgs.msg import Float64

def main():
    rospy.init_node('rr_wiggle')
    time  = rospy.get_rostime()
    t = rospy.Time(10,10)
    count = 0
    delta = -0.5
    hip1 = rospy.Publisher('/rupert/joint5_position_controller/command', Float64, queue_size=10)
    hip2 = rospy.Publisher('/rupert/joint6_position_controller/command', Float64, queue_size=10)
    hip3 = rospy.Publisher('/rupert/joint7_position_controller/command', Float64, queue_size=10)
    hip4 = rospy.Publisher('/rupert/joint8_position_controller/command', Float64, queue_size=10)
    knee1 = rospy.Publisher('/rupert/joint1_position_controller/command', Float64, queue_size=10)
    knee2 = rospy.Publisher('/rupert/joint2_position_controller/command', Float64, queue_size=10)
    knee3 = rospy.Publisher('/rupert/joint3_position_controller/command', Float64, queue_size=10)
    knee4 = rospy.Publisher('/rupert/joint4_position_controller/command', Float64, queue_size=10)
    ankle1 = rospy.Publisher('/rupert/joint9_position_controller/command', Float64, queue_size=10)
    ankle2 = rospy.Publisher('/rupert/joint10_position_controller/command', Float64, queue_size=10)
    ankle3 = rospy.Publisher('/rupert/joint11_position_controller/command', Float64, queue_size=10)
    ankle4 = rospy.Publisher('/rupert/joint12_position_controller/command', Float64, queue_size=10)
    joint_effort = rospy.ServiceProxy('/gazebo/set_model_configuration', SetModelConfiguration)
    servo1 = 0
    val = 0
    hip1.publish(0)
    hip2.publish(0)
    hip3.publish(0)
    hip4.publish(0)
    rospy.sleep(10)
    ankle1.publish(-1)
    ankle2.publish(-1)
    ankle3.publish(-1)
    ankle4.publish(-1)

    while not rospy.is_shutdown():
        if (val<-1.4):
            delta = 0.5
        elif (val>1.4):
            delta = -0.5
        val = val +delta

        knee1.publish(-val)
        knee2.publish(-val)
        knee3.publish(-val)
        knee4.publish(-val)
        # ankle1.publish(val)
        # ankle2.publish(val)
        # ankle3.publish(val)
        # ankle4.publish(val)
        rospy.sleep(2)
        # joint_effort("rupert",'',["hip_j1","hip_j2","hip_j3","hip_j4"],[0,0,0,0])
        # joint_effort("rupert",'',["knee_j1","knee_j2","knee_j3","knee_j4"],[-0.5,-0.5,-0.5,-0.5])
        # joint_effort("rupert",'',["ankle_j1","ankle_j2","ankle_j3","ankle_j4"],[servo1 ,servo1 , servo1,servo1])



if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ("Shutting Down")
