#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from std_msgs.msg import String
import pika


# 建立talkerProducer类，封装Producer的功能
class talkerProducer():
    def __init__(self):
        username = 'admin'
        pwd = 'admin12345'
        user_pwd = pika.PlainCredentials(username, pwd)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.204.130', credentials=user_pwd)) # 使用前面定义好的用户名密码远程登录Rabbit
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='test2')

    # 向mq推送消息函数
    def pubBody(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key='test2',
                                   body=message)
        print  " [x] Sent '%s' " % message

    # 接收到ROS topic的回调函数
    def rosCallback(self, body):
        rospy.loginfo(rospy.get_caller_id() + " I heard %s", body.data + " time2:%s" % rospy.get_time()) # 记录消息接收的时间
        message = str(body.data) + " time2:%s" % rospy.get_time()
        self.pubBody(message)

    # 接收ROS topic的函数
    def rosListener(self):
        print  " listening the topic "
        rospy.init_node('mq_producer', anonymous=True)
        rospy.Subscriber("chatter1", String, self.rosCallback)
        rospy.spin()


def main():
    mq_talker = talkerProducer()
    try :
        mq_talker.rosListener()
    except rospy.ROSInterruptException:
        print "Shutting down mq_producer node."
        mq_talker.connection.close()
        rospy.signal_shutdown("mq_producer Shutdown")


if __name__ == '__main__':
    main()
