# src/producer/producer_demo.py
import logging
from confluent_kafka import Producer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Producer Properties


# Java uses Properties object with .setProperty() — verbose
# Python uses a plain dict — that's it
# No serializer config needed in confluent-kafka — you pass bytes or str directly when producing. The Java client forces you to declare serializers upfront; Python handles it at send time.

config = {
    'bootstrap.servers': 'localhost:9092'
}

# 2. Create the Producer
producer = Producer(config)

logger.info("hello world!")

# 3. send data
producer.produce('demo_python',value='hello world!')
# 4. flush and close
producer.flush() 

#confluent-kafka uses flush() not close(). Make sure your file has producer.flush() and remove producer.close().
# producer.close() # in python this is not needed and will raise an error since Producer doesn't have a close() method. Just remove this line.
