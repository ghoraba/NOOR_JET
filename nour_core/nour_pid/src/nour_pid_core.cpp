#include "nour_pid/nour_pid_core.h"

NourPID::NourPID()
{
}

NourPID::~NourPID()
{
}

void NourPID::publishMessage(ros::Publisher *pub_message)
{
  nour_msgs::PID msg;
  msg.p = p_;
  msg.d = d_;
  msg.i = i_;
  pub_message->publish(msg);
}

void NourPID::messageCallback(const nour_msgs::PID::ConstPtr &msg)
{
  p_ = msg->p;
  d_ = msg->d;
  i_ = msg->i;

  //echo P,I,D
  ROS_INFO("P: %f", p_);
  ROS_INFO("D: %f", d_);
  ROS_INFO("I: %f", i_);
}

void NourPID::configCallback(nour_pid::nourPIDConfig &config, double level)
{
  //for PID GUI
  p_ = config.p;
  d_ = config.d;
  i_ = config.i;

}
