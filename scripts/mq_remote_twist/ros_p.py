#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import String
import pika
import json
import socket


# 建立talkerProducer类，封装Producer的功能
class talkerProducer():
    def __init__(self):
        username = 'admin'
        pwd = 'admin12345'
        user_pwd = pika.PlainCredentials(username, pwd)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host= '192.168.204.130', credentials=user_pwd)) # 使用前面定义好的用户名密码远程登录Rabbit
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='test3')
        self.twist_dict = {}
        self.twist_topic = "/cmd_vel1"

    # 向mq推送消息函数
    def pubBody(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key='test3',
                                   body=message)
        print  " [x] Sent '%s' " % message

    #将Twist解析成字典列表
    def twist2Dic(self, data):
        seq = ["x", "y", "z"]
        linear = dict.fromkeys(seq, 0.0)
        angular = dict.fromkeys(seq,  0.0)
        linear["x"] = data.linear.x or 0.0
        linear["y"] = data.linear.y or 0.0
        linear["z"] = data.linear.z or 0.0
        angular["x"] = data.linear.x or 0.0
        angular["y"] = data.angular.y or 0.0
        angular["z"] = data.angular.z or 0.0
        self.twist_dict = {"linear": linear, "angular": angular}

    # # 接收到ROS topic的回调函数
    # def rosCallbac_str(self, body):
    #     rospy.loginfo(rospy.get_caller_id() + " I heard %s",
    #                   body.data + " time2:%s" % rospy.get_time())  # 记录消息接收的时间
    #     message = str(body.data) + " time2:%s" % rospy.get_time()
    #     self.pubBody(message)

    # 接收到ROS topic的回调函数
    def rosCallback_twist(self, body):
        self.twist2Dic(body)
        json_dict = {}
        json_dict["data"] =self.twist_dict
        json_dict["topic"] = self.twist_topic
        json_dict["type"] = "Twist"
        json_dict["time2"] = rospy.get_time()
        json_str = json.dumps(json_dict)
        message = json_str
        self.pubBody(message)

    # 接收ROS topic的函数
    def rosListener(self):
        print  " listening the topic "
        rospy.init_node('mq_producer', anonymous=True)
        # rospy.Subscriber("/chatter1", String, self.rosCallback_str)
        rospy.Subscriber(self.twist_topic, Twist, self.rosCallback_twist)
        rospy.spin()




def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def main():
    global ip
    ip = get_host_ip()
    mq_talker = talkerProducer()
    try :
        mq_talker.rosListener()
    except rospy.ROSInterruptException:
        print "Shutting down mq_producer node."
        mq_talker.connection.close()
        rospy.signal_shutdown("mq_producer Shutdown")


if __name__ == '__main__':
    main()

