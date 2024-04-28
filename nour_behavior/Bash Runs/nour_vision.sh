#!/bin/bash

# Start system check
xterm  -e "roslaunch ros_deep_learning detectnet.ros1.launch input:=v4l2:///dev/video3 output:=--headless" & 
sleep 5

xterm  -e "rosrun nour_behave detect_service.py" & 
sleep 5

xterm -e "rostopic pub -1 /dialogflow_client/requests/string_msg std_msgs/String 'Say Vision System is up and running!'"&
sleep 5