#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt16

global velocity

velocity = 0

def velocity_callback(msgs):
    global velocity
    velocity = msgs.data

    
def listener():

    rospy.init_node('velocity', anonymous=True)
    # rospy.Subscriber("velocity", UInt16, velocity_control)


    rospy.Subscriber("velocity", UInt16, velocity_callback)

    # rospy.Subscriber("velocity_gps", UInt16,)
    #rospy.Subscriber("throttle", UInt16)
    
def velocity_control():
    global velocity

    pub = rospy.Publisher('servo_th', UInt16)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        velocity_pwm = velocity * 30 + 1475

        if gps=True:
            velocity_pwm += gain*(velocity_gps - velocity)

        rospy.loginfo(velocity_pwm)
        pub.publish(velocity_pwm)
        rate.sleep()

if __name__ == '__main__':
    try:
        listener()
        velocity_control()
    except rospy.ROSInterruptException:
        pass