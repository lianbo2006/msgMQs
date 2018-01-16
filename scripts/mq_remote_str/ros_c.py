#!/usr/bin/env python
#-*-coding:utf-8-*-
import rospy
from std_msgs.msg import String
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
        self.channel.queue_declare(queue='test2')
        self.pub = rospy.Publisher('chatter2', String, queue_size=10)
        rospy.init_node('mq_customer', anonymous=True)


    # 接收的mq消息的回调函数
    def mqCallback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        topic = str(body)  + " time3:%s" % rospy.get_time() # 记录在mq的停留时间
        self.pub.publish(topic)

    # mq的消费函数
    def mqCustomer(self):
        self.channel.basic_consume(self.mqCallback,
                              queue='test2',
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