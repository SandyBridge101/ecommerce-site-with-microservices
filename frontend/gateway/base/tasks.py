from __future__ import absolute_import, unicode_literals

from celery import shared_task
from gateway.celery import app


@shared_task
def publish_message(message,routing_key):
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            message,
            exchange='myexchange',
            routing_key=routing_key,
        )