# src/wikimedia-opensearch/wikimedia/wikimedia_changes_producer.py
import signal
import logging
import requests
from sseclient import SSEClient
from confluent_kafka import Producer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WIKIMEDIA_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
TOPIC = "wikimedia_recentchange"

running = True

def shutdown(_signum, _frame):
    global running
    logger.info("Shutdown signal received, stopping producer...")
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)


def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Delivery failed: {err}")
    else:
        logger.info(f"Delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")


def main():
    producer = Producer({'bootstrap.servers': 'localhost:9092'})

    logger.info("Starting Wikimedia stream producer...")
    headers = {'User-Agent': 'kafka-learning-python/1.0 (prince.my2001@gmail.com)'}
    response = requests.get(WIKIMEDIA_URL, stream=True, headers=headers)
    logger.info(f"Connected to Wikimedia stream, status code: {response.status_code}")

    for event in SSEClient(response).events():
        if not running:
            break
        if event.data:
            producer.produce(
                topic=TOPIC,
                value=event.data,
                on_delivery=delivery_report
            )
            # poll(0) triggers delivery callbacks without blocking
            # keeps the event loop moving while the SSE stream is running
            producer.poll(0)

    logger.info("Flushing remaining messages...")
    producer.flush()
    logger.info("Producer shut down gracefully")


if __name__ == "__main__":
    main()
