#!/bin/bash

# Build the catkin_ws
# cd $(pwd)/../..; catkin_make

# Launch the nodes
xterm  -e " roslaunch nourrobot bringup.launch" &
sleep 10

xterm  -e "rosrun teleop_twist_keyboard teleop_twist_keyboard.py" &
sleep 5

xterm  -e " roslaunch nourrobot navigate.launch" &
sleep 5

#xterm  -e "roscd nourrobot/rviz/; rviz -d navigation.rviz"

