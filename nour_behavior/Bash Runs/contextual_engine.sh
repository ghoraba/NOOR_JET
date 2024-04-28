#!/bin/bash

# Launch the nodes

xterm  -e "roscore" & 
sleep 5

xterm  -e "export GOOGLE_APPLICATION_CREDENTIALS=/home/jetson/gcpkey/noor1.json && gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS && roslaunch dialogflow_ros hotword_df.launch" &
sleep 10

xterm  -e "rostopic pub -1 /dialogflow_client/requests/string_msg std_msgs/String 'Say Contexual Engine is up and running!'" &
sleep 5
