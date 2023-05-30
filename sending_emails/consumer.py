import json
import pika
from mongoengine import connect, Document, StringField, BooleanField
import certifi


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)


def process_message(ch, method, properties, body):
    # Обработка сообщения из RabbitMQ
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email_to_contact(contact_id)

    # Установка полю "sent" значение True
    contact = Contact.objects.get(id=contact_id)
    contact.sent = True
    contact.save()

    # Подтверждение обработки сообщения
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_email_to_contact(contact_id):
    # Заглушка для отправки сообщения по email
    print(f"Sending email to contact with ID: {contact_id}")


def main():
    # Подключение к MongoDB
    # connect('mydb')
    uri = "mongodb+srv://oland2726:llRPcLo2d4iN4Ay0@cluster0.chqoczf.mongodb.net/web_hw_8?retryWrites=true&w=majority"
    connection = connect(host=uri, tlsCAFile=certifi.where(), ssl=True)

    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=process_message)

    print('Waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    main()
