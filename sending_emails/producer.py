import json
import pika
from mongoengine import connect, Document, StringField, BooleanField
import certifi


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)


def generate_fake_contacts(num_contacts):
    # Генерация фейковых контактов
    contacts = []
    for i in range(num_contacts):
        contact = Contact(
            full_name=f"Contact {i+1}",
            email=f"contact{i+1}@example.com",
        )
        contacts.append(contact)
    Contact.objects.insert(contacts)


def send_contact_message(contact_id):
    # Заглушка для отправки сообщения по email
    print(f"Sending email to contact with ID: {contact_id}")


def publish_message(channel, message):
    # Публикация сообщения в RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # делаем сообщение персистентным
        )
    )


def main():
    # Подключение к MongoDB
    # connect('mydb')
    uri = "mongodb+srv://oland2726:llRPcLo2d4iN4Ay0@cluster0.chqoczf.mongodb.net/web_hw_8?retryWrites=true&w=majority"
    connection = connect(host=uri, tlsCAFile=certifi.where(), ssl=True)

    # Подключение к RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue', durable=True)

    # Генерация фейковых контактов
    num_contacts = 10
    generate_fake_contacts(num_contacts)


    # Отправка сообщений и публикация в RabbitMQ
    for contact in Contact.objects:
        contact_id = str(contact.id)
        message = json.dumps({'contact_id': contact_id})
        send_contact_message(contact_id)
        publish_message(channel, message)

    # Закрытие соединения с RabbitMQ
    connection.close()


if __name__ == '__main__':
    main()
