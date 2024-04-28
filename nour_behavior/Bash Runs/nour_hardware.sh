#!/bin/bash

# Launch the nodes

xterm  -e "rosrun nour_behave move.py" &
sleep 1

xterm  -e "rosrun nour_behave goto.py" &
sleep 1

xterm  -e "rosrun nour_behave IsGoalReached.py" &
sleep 1

xterm  -e "rosrun nour_behave move_hardware_service.py" &
sleep 1

xterm -e "rostopic pub -1 /dialogflow_client/requests/string_msg std_msgs/String 'Say All Hardware Systems are up and running!'"&
sleep 10

xterm -e "./nav.sh"&
sleep 1

xterm -e "rostopic pub -1 /dialogflow_client/requests/string_msg std_msgs/String 'Say Navigation System is up and running!'"&
sleep 1
