#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate =rospy.Rate(10) #10hz
    num = 0
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        num = num + 1
        num_str = "{:0>4d}".format(num)
        hello_str = "hello world " + num_str + " %s"% rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass