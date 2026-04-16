# src/consumer/consumer_demo_with_shutdown.py
import signal
import logging
from confluent_kafka import Consumer, KafkaException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("I am a Kafka Consumer!")

# 1. Consumer Properties
# group.id: consumers with the same group.id share the work (each partition assigned to one consumer)
# auto.offset.reset: where to start reading if no committed offset exists for this group
#   'earliest' → read from beginning
#   'latest'   → read only new messages
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-python-consumer-group',
    'auto.offset.reset': 'earliest'
}

# 2. Create the Consumer
consumer = Consumer(config)

# 3. Graceful shutdown
# Java uses Runtime.addShutdownHook() + consumer.wakeup() + catches WakeupException
# Python uses signal handlers — cleaner, no extra exception type needed
# SIGINT  = Ctrl+C (keyboard interrupt)
# SIGTERM = sent by Docker/Kubernetes/Airflow when stopping a container
# Without SIGTERM handling, your consumer in production won't close cleanly
running = True

def shutdown(_signum, _frame):
    global running
    logger.info("Detected a shutdown, let's exit...")
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

# 4. Consume data
try:
    consumer.subscribe(['demo_python'])
    logger.info("Subscribed to topic, polling for messages...")

    while running:
        msg = consumer.poll(1.0)  # block for up to 1 second waiting for a message
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        logger.info(f"Key: {msg.key()}, Value: {msg.value().decode('utf-8')}")
        logger.info(f"Partition: {msg.partition()}, Offset: {msg.offset()}")

    logger.info("Consumer is starting to shut down")

except Exception as e:
    logger.error(f"Unexpected exception in the consumer: {e}")
finally:
    # close() commits offsets and leaves the consumer group cleanly
    consumer.close()
    logger.info("The consumer is now gracefully shut down")
