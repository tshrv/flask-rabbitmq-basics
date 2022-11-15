from pika import BlockingConnection, ConnectionParameters

QUEUE_HOST = 'message-service'

class Producer:
    def __init__(self, queue_name: str) -> None:
        self.queue_name = queue_name
        conn_params = ConnectionParameters(host=QUEUE_HOST)
        self.connection = BlockingConnection(conn_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue_name)
    
    def send(self, message:str):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message
        )
    
    def close(self):
        self.connection.close()