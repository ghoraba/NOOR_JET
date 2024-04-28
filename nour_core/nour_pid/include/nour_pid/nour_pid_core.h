#ifndef SR_NOUR_PID_CORE_H
#define SR_NOUR_PID_CORE_H

#include "ros/ros.h"
#include "ros/time.h"

// Custom message includes. Auto-generated from msg/ directory.
#include <nour_msgs/PID.h>

// Dynamic reconfigure includes.
#include <dynamic_reconfigure/server.h>
// Auto-generated from cfg/ directory.
#include <nour_pid/nourPIDConfig.h>

class NourPID
{
public:
  NourPID();
  ~NourPID();
  void configCallback(nour_pid::nourPIDConfig &config, double level);
  void publishMessage(ros::Publisher *pub_message);
  void messageCallback(const nour_msgs::PID::ConstPtr &msg);

  double p_;
  double d_;
  double i_;

};
#endif
