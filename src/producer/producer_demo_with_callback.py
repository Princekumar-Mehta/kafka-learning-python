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
    'batch.size':400 #never set batch.size in production, just for demo to show sticky partitioning more clearly. In production, leave it to default and let Kafka manage batching for you.
}
# 2. Create the Producer
producer = Producer(config)

logger.info("hello world!")


def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()} at time {msg.timestamp()[1]}')


# 3. Send data
for j in range(1):
    for i in range(30):
        producer.produce('demo_python', value=f'hello world! {i}', on_delivery=delivery_report)
    time.sleep(0.5) # wait a bit before sending the next batch

producer.flush()

# NOTE - STICKY PARTITIONER (default since Kafka 2.4+):
# Sticky behaviour is controlled by Kafka's internal batching, NOT by flush() placement.
# Kafka sticks to one partition until the batch is full or linger.ms expires, then switches.
# Even with flush() inside the loop, messages sent quickly enough still get batched
# to the same partition — as seen in our output above.
# flush() outside loop → gives Kafka more messages at once → more pronounced stickiness
# flush() inside loop  → waits per message, but Kafka may still batch several before switching
#
# No key  → sticky partitioner → no ordering guarantee across partitions
# With key → same key → same partition → ordering guaranteed per key
# PySpark: use keys when ordered processing per entity (e.g. user_id) is needed

