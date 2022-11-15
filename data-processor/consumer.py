from pika import ConnectionParameters, BlockingConnection

QUEUE_HOST = 'message-service'


class Consumer:
    def __init__(self, queue_name: str, callback) -> None:
        self.queue_name = queue_name
        conn_params = ConnectionParameters(host=QUEUE_HOST)  # type: ignore
        self.connection = BlockingConnection(conn_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue_name)
    
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True,
        )
    
    def consume(self):
        self.channel.start_consuming()