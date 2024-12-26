import pika

class PikaMessenger:
    def produce(self, body):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='seat')
        channel.basic_publish(exchange='', routing_key='seat', body=body)
        connection.close()

    def consume(self, callback):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'),
        )
        channel = connection.channel()
        channel.queue_declare(queue='seat')

        channel.basic_consume(
            queue='seat',
            auto_ack=True,
            on_message_callback=callback
        )

        print(' [*] RABBITMQ: Waiting for messages.')
        channel.start_consuming()
