#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt16
from std_msgs.msg import Float32

global velocity
global gps
global steering_angle
steering_angle = 0
velocity = 0
gps=False

def velocity_callback(msgs):
    global velocity
    global gps
    global steering_angle
    velocity = msgs.data
    steering_angle = msgs.data

def steering_callback(msgs):
    global steering_angle
    steering_angle = msgs.data
    
def listener():

    rospy.init_node('cmd_car', anonymous=True)
    # rospy.Subscriber("velocity", UInt16, velocity_control)


    rospy.Subscriber("velocity", Float32, velocity_callback)
    rospy.Subscriber("turning", Float32, steering_callback)

    # rospy.Subscriber("velocity_gps", UInt16,)
    #rospy.Subscriber("throttle", UInt16)
    
def car_control():
    global velocity
    global gps
    global steering_angle

    pub_th = rospy.Publisher('servo_th', UInt16, queue_size=10)
    pub_st = rospy.Publisher('servo_st', UInt16, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        velocity_pwm = velocity * 30 + 1475
        steering_pwm = steering_angle * 10 + 1450


        if gps==True:
            velocity_pwm += gain*(velocity_gps - velocity)

        rospy.loginfo("throttle pwm")
        rospy.loginfo(int(round(velocity_pwm)))
        pub_th.publish(int(round(velocity_pwm)))
        rospy.loginfo("steering pwm")
        rospy.loginfo(int(round(steering_pwm)))
        pub_st.publish(int(round(steering_pwm)))
        rate.sleep()



if __name__ == '__main__':
    try:
        listener()
        car_control()
    except rospy.ROSInterruptException:
        pass