#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from vision_msgs.msg import Detection2DArray
from nour_behave.srv import ServiceDetect, ServiceDetectResponse

classes= ["unlabeled","person","bicycle","car","motorcycle","airplane","bus","train","truck","boat","traffic light","fire hydrant","street sign","stop sign","parking meter","bench","bird","cat","dog","horse","sheep","cow","elephant","bear","zebra","giraffe","hat","backpack","umbrella","shoe","eye glasses","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball","kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket","bottle","plate","wine glass","cup","fork","knife","spoon","bowl","banana","apple","sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair","couch","potted plant","bed","mirror","dining table","window","desk","toilet","door","tv","laptop","mouse","remote","keyboard","cell phone","microwave","oven","toaster","sink","refrigerator","blender","book","clock","vase","scissors","teddy bear","hair drier","toothbrush"]

def trigger_response(request):
    message= rospy.wait_for_message("detectnet/detections/", Detection2DArray)
    classname= classes[message.detections[0].results[0].id]
    print(classname)
    pub = rospy.Publisher('/dialogflow_client/requests/string_msg', String, queue_size=1)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish('Detected_Obj '+ str(classname))
        rate.sleep()
        break
    return ServiceDetectResponse("Detected_Obj "+ str(classname))
    

rospy.init_node('detect_service')                      # initialize a ROS node
detect_service = rospy.Service(                        # create a service, specifying its name,
    '/nour_detect', ServiceDetect, trigger_response    # type, and callback
)
rospy.loginfo("Vision detection service ready and running")
rospy.spin()    

