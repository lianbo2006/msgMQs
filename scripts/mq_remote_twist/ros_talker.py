#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import String

# 函数以rate速率发送ROS topic
def talker(rate):
    rospy.init_node('talker', anonymous=True)
    pub_str = rospy.Publisher('/chatter1', String, queue_size=10)
    pub_twist = rospy.Publisher('/cmd_vel1', Twist, queue_size=10) # 初始化topic
    angular_speed = 1
    linear_speed = 0.2

     # 初始化node
    rate =rospy.Rate(rate)
    num = 0 #topic计数器
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        num = num + 1
        num_str = "{:0>5d}".format(num)
        hello_str = "twist topic" + num_str + " time1:%s"% rospy.get_time() # 记录消息发出的时间
        hello_twist = Twist()
        hello_twist.angular.z = 1
        pub_str.publish(hello_str)
        pub_twist.publish(hello_twist)
        print "NO.%s publish is done"%num_str
        rate.sleep()

if __name__ == '__main__':
    try:
        rate = int(input("please input the RATE:")) or 10
        talker(rate)
    except rospy.ROSInterruptException:
        rospy.signal_shutdown("ros_talker Shutdown")


