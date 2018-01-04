#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct') #声明交换机，类型为direct

severity = sys.argv[1] if len(sys.argv) > 2 else 'info' #sys.argv[0]值.py本身，argv[1]是第一个参数
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity, #包含路由键，只有正确的键才能发送给对应队列
                      body=message)
print " [x] Sent %r:%r" % (severity, message)
connection.close()