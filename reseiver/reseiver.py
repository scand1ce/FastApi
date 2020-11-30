import sys
import pika

credentials = pika.PlainCredentials(username='user', password='password')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue='privat')


def callback(ch, method, properties, body):
    print("[x] Received --> %r" % body, file=sys.stdout)


channel.basic_consume(queue='privat', on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
