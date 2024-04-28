#!/usr/bin/env python
import rospy                                      # the main module for ROS-python programs
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionResult

def Reached_dist(dist):
    pub = rospy.Publisher('/dialogflow_client/requests/string_msg', String, queue_size=1)
    pub.publish('Reached_Dist '+ str(dist))

def callback(data):
    Distination= rospy.get_param('Distination')
    rospy.loginfo(data.status.text + ' : ' + Distination) 
    Reached_dist(Distination)
    
rospy.init_node('IsGoalReached', anonymous=True)
rospy.Subscriber('/move_base/result', MoveBaseActionResult, callback)

rospy.loginfo("Ready to receive reached destination notifications")
rospy.spin()                                       # Keep the program from exiting, until Ctrl + C is pressed                   