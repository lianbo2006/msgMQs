#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',exchange_type='fanout') #声明交换机,注意在实际使用中发现type参数无法识别，改成了exchange_type，可能与pika版本有关

result = channel.queue_declare(exclusive=True) #exclusive 排他的，自动生成的队列会唯一指定，这个queue在消费者断开后自动删除
                                               # 声明的这个queue去绑定交换机
queue_name = result.method.queue #获得随机队列名

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print " [x] %r" % (body,)
    time.sleep(body.count('.'))
    print " [x] Done"

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()