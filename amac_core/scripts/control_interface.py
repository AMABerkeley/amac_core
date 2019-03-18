#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt16
from std_msgs.msg import Float32

global velocity
global gps
global steering_angle
global aux
aux = 0
steering_angle = 0
velocity = 0
gps=False

def velocity_callback(msgs):
    global velocity
    velocity = msgs.data

def steering_callback(msgs):
    global steering_angle
    steering_angle = msgs.data

def aux_callback(msgs):
    global aux
    aux = msgs.data

    
def listener():

    rospy.init_node('cmd_car', anonymous=True)
    # rospy.Subscriber("velocity", UInt16, velocity_control)


    rospy.Subscriber("velocity_ms", Float32, velocity_callback)
    rospy.Subscriber("turning", Float32, steering_callback)
    rospy.Subscriber("aux", UInt16, aux_callback)

    # rospy.Subscriber("velocity_gps", UInt16,)
    #rospy.Subscriber("throttle", UInt16)
    
def car_control():
    global velocity
    global gps
    global steering_angle
    global aux

    pub_th = rospy.Publisher('servo_th', UInt16, queue_size=10)
    pub_st = rospy.Publisher('servo_st', UInt16, queue_size=10)
    pub_speed = rospy.Publisher('speed', Float32, queue_size=10)
    pub_st_ang = rospy.Publisher('steering_angle', Float32, queue_size=10)

    rate = rospy.Rate(40)  # Publishes at 40 Hz, used at 10 Hz (limited by LIDAR)
    while not rospy.is_shutdown():
        if (velocity < 1.8):
            # TODO: must be calibrated
            gain = 140
        else:
            # TODO: must be calibrated
            gain = 30

        # velocity PWM is centered around 1475, reference calibration excel spreadsheet.
        velocity_pwm = velocity * gain + 1475
        # steering PWM is centered around 1450, reference calibration excel spreadsheet.
        steering_pwm = steering_angle * 10 + 1450

        # TODO: This will all be moved to the future AMAC drive by wire or control dir.
        # We want dead reckoning control (with encoders) as well as a GPS mode
        if gps == True:
            velocity_pwm += gain * (velocity_gps - velocity)
            
        if aux < 1500:
            rospy.loginfo("throttle pwm")
            rospy.loginfo(int(round(velocity_pwm)))
            pub_th.publish(int(round(velocity_pwm)))
            rospy.loginfo("steering pwm")
            rospy.loginfo(int(round(steering_pwm)))
            pub_st.publish(int(round(steering_pwm)))

        rospy.loginfo("speed")
        rospy.loginfo(velocity)
        pub_speed.publish(velocity)
        rospy.loginfo("steering angle")
        rospy.loginfo(steering_angle)
        pub_st_ang.publish(steering_angle)
           

        rate.sleep()



if __name__ == '__main__':
    try:
        listener()
        car_control()
    except rospy.ROSInterruptException:
        pass