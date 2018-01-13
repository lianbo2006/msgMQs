#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika
import sys

class mqTalker():
    def __init__(self):
        username = 'admin'
        pwd = 'admin12345'
        user_pwd = pika.PlainCredentials(username, pwd)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.204.129', credentials=user_pwd))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='test1')

    def pubBody(self,message):
        self.channel.basic_publish(exchange='',
                              routing_key='test1',
                              body=message)

def main():
    mq_talker = mqTalker()
    message = ' '.join(sys.argv[1:]) or "Hello World!"
    mq_talker.pubBody(message)
    print  " [x] Sent '%s' " % message
    print "Shutting down talker node."
    mq_talker.connection.close()
if __name__ == '__main__':
    main()
