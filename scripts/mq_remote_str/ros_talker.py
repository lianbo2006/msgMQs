#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from std_msgs.msg import String
import sys

# 函数以rate速率发送ROS topic
def talker(rate):
    pub = rospy.Publisher('chatter1', String, queue_size=10) # 初始化topic
    rospy.init_node('talker', anonymous=True) # 初始化node
    rate =rospy.Rate(rate)
    num = 0 #topic计数器
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        num = num + 1
        num_str = "{:0>5d}".format(num)
        hello_str = "hello world " + num_str + " time1:%s"% rospy.get_time() # 记录消息发出的时间
        # rospy.loginfo(hello_str)
        pub.publish(hello_str)
        print "publish %s"%hello_str
        rate.sleep()

if __name__ == '__main__':
    try:
        if type(sys.argv[1:]) == int :
            rate = sys.argv[1:] # 取得程序运行时的第一个参数，若为整数设为rate
        else:
            rate = 10 # 默认rate
        talker(rate)
    except rospy.ROSInterruptException:
        rospy.signal_shutdown("ros_talker Shutdown")