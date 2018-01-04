#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True) #durable=True确保task_queue队列持久化
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag) #发送消息确认，消息队列收到后会删除对应的消息

channel.basic_qos(prefetch_count=1) #保证消息公平调度
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()