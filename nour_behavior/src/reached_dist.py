#!/usr/bin/env python
import rospy                                      # the main module for ROS-python programs

from std_msgs.msg import String

# Only for testing -- Deprecated
def Reached_dist(dist):
    pub = rospy.Publisher('/dialogflow_client/requests/string_msg', String, queue_size=1)
    rospy.init_node('ReachedDist', anonymous=True)
    pub.publish('Reached_Dist '+ str(dist))

#Example    
Reached_dist('Dr. Mostafa')
