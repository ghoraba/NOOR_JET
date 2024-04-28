#!/usr/bin/env python

import rospy                                      # the main module for ROS-python programs
from nour_behave.srv import ServiceExample, ServiceExampleResponse
from std_msgs.msg import String

def trigger_response(request):
    ''' 
    Callback function used by the service server to process
    requests from clients. It returns a ServiceExampleResponse
    '''
    pub = rospy.Publisher('/move_hardware', String, queue_size=1)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #pub.publish(str(request.actionPlace)) # This will pass the location to go to
        pub.publish(str(request.actionPlace)) # This will pass the direction to move toward
        rate.sleep()
        break
    
    return ServiceExampleResponse("Starting to move "+ request.actionPlace)
    

rospy.init_node('move_hardware_service')                  # initialize a ROS node
my_service = rospy.Service(                        # create a service, specifying its name,
    '/nour_naviagte', ServiceExample, trigger_response       # type, and callback
)
rospy.loginfo("Move hardware service ready and running")
rospy.spin()                                       # Keep the program from exiting, until Ctrl + C is pressed                   
