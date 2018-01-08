#!/usr/bin/env python
#-*-coding:utf-8-*-
import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True) #建立随机唯一队列
        self.callback_queue = result.method.queue #获得唯一队列队列名

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue) #实例化的时候就开始消费随机队列中的内容，一旦收到消息执行on_response

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id: #使用corr_id对消息是否为自己发出的进行验证
            self.response = body  #验证成功则获得消息中的内容

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4()) #uuid生成随机字符串作为corr_id
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue, #为随机队列的名称，服务端的消息要发进这个队列
                                         correlation_id = self.corr_id,  #为之后的消息确认发送一个corr_id
                                         ), #pika.BasicProperties传递一些自定义参数，但是不作为消息显示
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events() #非阻塞版的start_consuming
            print "no msg..."
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got %r" % response