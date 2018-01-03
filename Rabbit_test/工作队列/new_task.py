#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True) #durable=True确保task_queue队列持久化

message = ' '.join(sys.argv[1:]) or "Hello World!" #可以读取系统输入的参数，通过加.来延长处理时间
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent 让消息持久化
                      ))
print " [x] Sent %r" % (message,)
connection.close()