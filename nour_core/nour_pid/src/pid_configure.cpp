#include "nour_pid/nour_pid_core.h"

int main(int argc, char **argv)
{

  ros::init(argc, argv, "pid_configure");
  ros::NodeHandle nh;

  NourPID *nour_pid = new NourPID();

  dynamic_reconfigure::Server<nour_pid::nourPIDConfig> dr_srv;
  dynamic_reconfigure::Server<nour_pid::nourPIDConfig>::CallbackType cb;
  cb = boost::bind(&NourPID::configCallback, nour_pid, _1, _2);
  dr_srv.setCallback(cb);

  double p;
  double d;
  double i;
  int rate;

  ros::NodeHandle pnh("~");
  pnh.param("p", p, 0.6);
  pnh.param("d", d, 0.3);
  pnh.param("i", i, 0.5);
  pnh.param("rate", rate, 1);

  ros::Publisher pub_message = nh.advertise<nour_msgs::PID>("pid", 10);

  ros::Rate r(rate);

  while (nh.ok())
  {
    nour_pid->publishMessage(&pub_message);
    ros::spinOnce();
    r.sleep();
  }

  return 0;
}
