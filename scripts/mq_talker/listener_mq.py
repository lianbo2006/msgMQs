#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from std_msgs.msg import String
import pika
import sys

class mqListener():
    def __init__(self):
        username = 'admin'
        pwd = 'admin12345'
        user_pwd = pika.PlainCredentials(username, pwd)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.204.129', credentials=user_pwd))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='test1')
        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.init_node('mq_listener', anonymous=True)


    def mqCallback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        topic = str(body)
        rospy.loginfo(topic)
        self.pub.publish(topic)


def main():
    mq_listener = mqListener()
    try:
        channel = mq_listener.channel
        channel.basic_consume(mq_listener.mqCallback,
                              queue='test1',
                              no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print "Shutting down listener node."
        mq_listener.connection.close()

if __name__ == '__main__':
    main()