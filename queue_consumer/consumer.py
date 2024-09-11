# queue_consumer/consumer.py
import pika
import json
from elasticsearch import Elasticsearch
from django.conf import settings

def callback(ch, method, properties, body):
    es = Elasticsearch([settings.ELASTICSEARCH_HOST])
    blog_entry = json.loads(body)
    
    # Index the blog entry in Elasticsearch
    es.index(index='blog_entries', body={
        'title': blog_entry['title'],
        'text': blog_entry['text'],
        'user_id': blog_entry['user_id']
    })
    
    print(f" [x] Received {blog_entry['title']}")

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='blog_entries')
    channel.basic_consume(queue='blog_entries', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    start_consuming()