import os
import pika

class ConnectionRabbitMQ:
    
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST')
        self.port = os.getenv('RABBITMQ_PORT')
        self.user = os.getenv('RABBITMQ_USER')
        self.password = os.getenv('RABBITMQ_PASSWORD')
        self.queue_consumer= os.getenv('RABBITMQ_CONSUMER_QUEUE')
        self.queue_publisher= os.getenv('RABBITMQ_PUBLISH_QUEUE')


    def channel(self):

        credentials = pika.PlainCredentials(self.user, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host, port = self.port, credentials=credentials))

        channel = connection.channel()

        return channel

    def basicConsume(self, channel, callback, queue = None): 
        if queue == None:
            queue = self.queue_consumer
        
        channel.queue_declare(queue)
        
        
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        
        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.start_consuming()

    def basicPublish(self, channel, body, queue = None): 
        if queue == None:
            queue = self.queue_publisher
        
        channel.queue_declare(queue)

        channel.basic_publish(exchange='', routing_key=queue, body=body)
        
        print(" [x] Sent 'cambio!'")
        channel.connection.close()