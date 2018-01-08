#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue') #声明固定队列，队列名称为'rpc_queue'

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body): #props可以拿到服务端pika.BasicProperties中定义的参数
    n = int(body)

    print " [.] fib(%s)" % n
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to, #将结果返回给收到的随机队列
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id), #将收到的客户端correlation_id用pika.BasicProperties发回
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag) #消费时需要返回确认，代表服务端消费完成

channel.basic_qos(prefetch_count=1)  #或许我们希望能在服务器上多开几个线程。为了能将负载平均地分摊到多个服务器，我们需要将 prefetch_count 设置好。
channel.basic_consume(on_request, queue='rpc_queue')  #server消费固定队列中的消息，队列名称为'rpc_queue

print " [x] Awaiting RPC requests"
channel.start_consuming()