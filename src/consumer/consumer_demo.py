# src/producer/producer_demo.py
import logging
from confluent_kafka import Consumer, KafkaException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Producer Properties


# Java uses Properties object with .setProperty() — verbose
# Python uses a plain dict — that's it
# No serializer config needed in confluent-kafka — you pass bytes or str directly when producing. The Java client forces you to declare serializers upfront; Python handles it at send time.
group_id = 'my-python-consumer-group'  
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # Start from the earliest message if no offset is committed for this group
}

# 2. Create the Producer
consumer = Consumer(config)

logger.info("hello world!")

# 3. consume data
try:
    consumer.subscribe(['demo_python'])
    while True:         
        msg = consumer.poll(1.0)  # timeout in seconds
        if msg is None:
            logger.info("No message received, polling again...")
            continue  # No message received, continue polling
        if msg.error():
            raise KafkaException(msg.error())
        else:
            logger.info(f"Received message: {msg.value().decode('utf-8')} from partition {msg.partition()} at offset {msg.offset()}")
except KeyboardInterrupt:
    pass
finally:    
    consumer.close()    