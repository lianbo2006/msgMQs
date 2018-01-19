#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import String
import json
import pika


# 建立talkerCustomer类，封装Customer的功能
class talkerCustomer():
    def __init__(self):
        username = 'admin'
        pwd = 'admin12345'
        user_pwd = pika.PlainCredentials(username, pwd)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.204.130', credentials=user_pwd))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='test3')
        rospy.init_node('mq_customer', anonymous=True)


    # 接收的mq消息的回调函数
    def mqCallback(self,ch, method, properties, body):
        json_dict, twist_topic = self.str2info(body)
        topic = json_dict["topic"]
        time2 = json_dict["time2"]
        pub1 = rospy.Publisher(topic, Twist, queue_size=10)
        pub2 = rospy.Publisher("/chatter", String, queue_size=10)
        print(" [x] Received %r" % body)
        topic_str = "time2:%s" %str(time2)  + " time3:%s" %rospy.get_time() # 记录在mq的停留时间
        pub1.publish(twist_topic)
        pub2.publish(topic_str)

    def str2info(self, message):
        json_dict = json.loads(message)
        twist_dict = json_dict["data"]
        linear, angular = twist_dict["linear"], twist_dict["angular"]
        twist_topic = Twist()
        twist_topic.linear.x = linear["x"]
        twist_topic.linear.y = linear["y"]
        twist_topic.linear.z = linear["z"]
        twist_topic.angular.x = angular["x"]
        twist_topic.angular.y = angular["y"]
        twist_topic.angular.z = angular["z"]
        return json_dict, twist_topic


    # mq的消费函数
    def mqCustomer(self):
        self.channel.basic_consume(self.mqCallback,
                              queue='test3',
                              no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

def main():
    mq_customer = talkerCustomer()
    try :
        mq_customer.mqCustomer()
    except rospy.ROSInterruptException:
        print "Shutting down mq_customer node."
        mq_customer.connection.close()
        rospy.signal_shutdown("mq_customer Shutdown")

if __name__ == '__main__':
    main()