# src/producer/producer_demo_with_callback.py
import logging
from confluent_kafka import Producer
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Producer Properties
# Java uses Properties object with .setProperty() — verbose
# Python uses a plain dict — that's it
# No serializer config needed in confluent-kafka — you pass bytes or str directly when producing.
# The Java client forces you to declare serializers upfront; Python handles it at send time.
config = {
    'bootstrap.servers': 'localhost:9092',
}
# 2. Create the Producer
producer = Producer(config)

logger.info("hello world!")


def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'key: {msg.key()} partition: {msg.partition()}')


# 3. Send data
for j in range(2):
    for i in range(10):
        topic = 'demo_python'
        key = f'id_{i}'  # Using a key to ensure messages with the same key go to the same partition
        value = f'hello world! {i}'
        producer.produce(topic, key=key, value=value, on_delivery=delivery_report)
        time.sleep(0.5)
    producer.flush()



