#!/usr/bin/env python
"""
goto.py is a simple navigation system that can go to a location
  based on a voice command. 
"""

import roslib 
import rospy
import math

import tf
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String

goals = { 
          "Dr. Samy": [0.361708790064, 11.8248758316, 0.000, 1.000],
          "Rasha": [0.721633136272, 8.3423614502, 0.000, 1.000],
          "Dr. Tamer": [0.889028131962, 4.72344923019, 0.000, 1.000],
          "Dr. Said": [-0.877423346043, -3.05380368233, 0.000, 1.000 ],
          "Dr. Mostafa": [1.09572780132, 1.25844812393, 0.000, 1.000]
          #"Dr. Mostafa": [0.388139724731, 1.59907722473, 0.000, 1.000]   # For Testing On Turtlebot3
          }

class nour_goto:

    def __init__(self):
        self.msg = PoseStamped()
        self.msg.header.frame_id = "map"

        self.pub_ = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)
        rospy.Subscriber('/move_hardware', String, self.speechCb)
        rospy.spin()

    def setMsg(self, goal):
        self.msg.pose.position.x = goals[goal][0]
        self.msg.pose.position.y = goals[goal][1]
        self.msg.pose.position.z = goals[goal][2]
        q = quaternion_from_euler(0, 0, goals[goal][3], 'sxyz')
        self.msg.pose.orientation.x = q[0]
        self.msg.pose.orientation.y = q[1]
        self.msg.pose.orientation.z = q[2]
        self.msg.pose.orientation.w = q[3]
        rospy.set_param('Distination',str(goal))

    def speechCb(self, msg):
        rospy.loginfo(msg.data)
        self.msg.header.stamp = rospy.Time.now()

        if msg.data.find("Dr. Said") > -1: 
            self.setMsg("Dr. Said")
        elif msg.data.find("Dr. Mostafa") > -1:
            self.setMsg("Dr. Mostafa")
        elif msg.data.find("Dr. Tamer") > -1:
            self.setMsg("Dr. Tamer")
        elif msg.data.find("Rasha") > -1:
            self.setMsg("Rasha")
        elif msg.data.find("Dr. Samy") > -1:
            self.setMsg("Dr. Samy")
        else:
            rospy.loginfo("unknown goal!")
            return

        self.pub_.publish(self.msg)

    def cleanup(self):
        # stop the robot!
        twist = Twist()
        self.pub_.publish(twist)

if __name__=="__main__":
    rospy.init_node('nour_goto')
    try:
        rospy.loginfo("Ready to receive move destination commands")
        nour_goto()
    except:
        pass
