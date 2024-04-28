#!/bin/bash

# Start system check
#xterm  -e "./nour_system_check.sh" & 
#sleep 12

xterm  -e "echo 'Starting System Check'" & 
sleep 5

outputString=$(rosrun nour_behave system_check.py)

if [ $outputString  ==  'success' ]
then
  clear
  echo "System check success, bringing up Nour Robot!" 
  
else
  echo "System check fail!"
  exit
fi

xterm  -e "./contextual_engine.sh" & 
sleep 20

xterm  -e "./nour_hardware.sh" & 
sleep 15

xterm  -e "./nour_vision.sh" & 

exit