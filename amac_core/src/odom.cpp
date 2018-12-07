#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <cmath>
#include <geometry_msgs/TransformStamped.h>
#include <std_msgs/Float32>



void car_controlCallback(const std_msgs::Float32::ConstPtr& msg)
{
  ROS_INFO("I heard: [%s]", msg->data);
}

int main(int argc, char** argv){
  ros::init(argc, argv, "odometry_publisher");

  ros::NodeHandle n;
  ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
  tf::TransformBroadcaster odom_broadcaster;
  ros::Subscriber sub_st = n.subscribe("turning", 1000, car_controlCallback);
  ros::Subscriber sub_vel = n.subscribe("velocity", 1000, car_controlCallback);
  wheelbase_ = .290
  double current_speed = velocity->data
  double current_steering_angle(0.0), current_angular_velocity(0.0);
  current_steering_angle = turning->data;
  current_angular_velocity = current_speed * tan(current_steering_angle) / wheelbase_;

  ros::Time current_time, last_time;
  current_time = ros::Time::now();
  last_time = ros::Time::now();

  ros::Rate r(1.0);
  while(n.ok()){

    ros::spinOnce();               // check for incoming messages
    current_time = ros::Time::now();

    speed = velocity
    steering_angle = turning
    angular_velocity = speed * tan(steering_angle) / wheelbase_
    ros::Duration dt = time_duration


    double x_dot = current_speed * cos(yaw_)
    double y_dot = current_speed * sin(yaw_)
    x_ += x_dot * dt.toSec()
    y_ += y_dot * dt.toSec()

    yaw_ += current_angular_velocity * dt.toSec()



    odom->pose.pose.position.x = x_
    odom->pose.pose.position.y = y_
    odom->pose.pose.orientation.x = 0.0
    odom->pose.pose.orientation.y = 0.0
    odom->pose.pose.orientation.z = sin(yaw_/2.0)
    odom->pose.pose.orientation.w = cos(yaw_/2.0)

    // Co variance should be cacluated empirically
    odom->pose.covariance[0]  = 0.2 ///< x
    odom->pose.covariance[7]  = 0.2 ///< y
    odom->pose.covariance[35] = 0.4 ///< yaw

    // Velocity
    odom->twist.twist.linear.x = current_speed
    odom->twist.twist.linear.y = 0.0
    odom->twist.twist.angular.z = current_angular_velocity

    geometry_msgs::TransformStamped tf;
    tf.header.frame_id = "odom";
    tf.child_frame_id = "base_link";
    tf.header.stamp = ros::Time::now();
    tf.transform.translation.x = x_;
    tf.transform.translation.y = y_;
    tf.transform.translation.z = 0.0;
    tf.transform.rotation = odom->pose.pose.orientation;
    tf_pub_->sendTransform(tf);



    //since all odometry is 6DOF we'll need a quaternion created from yaw

    //first, we'll publish the transform over tf
    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = current_time;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "base_link";

    odom_trans.transform.rotation = odom_quat;

    //send the transform
    odom_broadcaster.sendTransform(odom_trans);

    //next, we'll publish the odometry message over ROS
    nav_msgs::Odometry odom;
    odom.header.stamp = current_time;
    odom.header.frame_id = "odom";


    //publish the message
    odom_pub.publish(odom);

    last_time = current_time;
    r.sleep();
  }
}