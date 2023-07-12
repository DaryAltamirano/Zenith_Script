from django.conf import settings
import pika

class ConnectionRabbitMQ:
    
    def __init__(self):
        self.host = settings.RABBITMQ["default"]["HOST"]
        self.port = settings.RABBITMQ["default"]["PORT" ]
        self.user = settings.RABBITMQ["default"]["USER"]
        self.password = settings.RABBITMQ["default"]["PASSWORD"]
        self.queue= settings.RABBITMQ["default"]["QUEUE"]

    def channel(self):

        credentials = pika.PlainCredentials(self.user, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host = self.host, port = self.port, credentials=credentials))

        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        return channel

    def basicConsume(self, channel, callback, queue = None): 
        if queue == None:
            queue = self.queue
        else:
            channel.queue_declare(queue)
        
        
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        
        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.start_consuming()

    def basicPublish(self, channel, body, queue = None): 
        if queue == None:
            queue = self.queue

        channel.basic_publish(exchange='', routing_key=queue, body=body)
        
        print(" [x] Sent 'cambio!'")
        channel.connection.close()