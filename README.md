# Kafka Learning in Python

Following **"Apache Kafka Series - Learn Apache Kafka for Beginners v3"** by Stephane Maarek.
Course uses Java — all examples here are translated to Python.

## Goal

Learn Kafka concepts deeply using production-ready Python tools, applicable to a Data Engineering stack (Airflow + PySpark).

## Libraries

| Library | Purpose |
|---------|---------|
| `confluent-kafka` | Primary Kafka client — wraps `librdkafka`, industry standard |
| `quixstreams` | Pythonic streaming/transformations, similar to Pandas |

**Never use:** `kafka-python`, `pykafka`

## Local Setup

- Kafka running in Docker (KRaft mode, no Zookeeper)
- Conduktor as the UI
- Connect via `bootstrap.servers: localhost:9092`

## Project Structure

```
src/
├── producer/   # Kafka producer examples
├── consumer/   # Kafka consumer examples
└── admin/      # Topic management
```

## Course Progress

### Section: Producer
- [x] Basic producer (`producer_demo.py`)
- [x] Producer with delivery callback (`producer_demo_with_callback.py`)
- [x] Producer with keys (`producer_demo_keys.py`)

### Section: Consumer
- [x] Consumer with graceful shutdown (`consumer_demo_with_shutdown.py`)

### Key Concepts Covered
- **Producer flow:** config → create → produce → flush
- **Serializers:** Java requires explicit serializer config; Python passes bytes/str directly
- **Sticky Partitioner:** default since Kafka 2.4+. Messages batched quickly go to same partition. Kafka switches partition when batch is full or `linger.ms` expires.
- **Keys:** same key → same partition → ordering guaranteed per key. No key → sticky/round-robin → no ordering guarantee.
- **PySpark:** use message keys when ordered processing per entity (e.g. `user_id`) is needed in Structured Streaming.
- **Graceful shutdown:** Java uses `Runtime.addShutdownHook()` + `consumer.wakeup()` + catches `WakeupException`. Python uses `signal.signal(SIGTERM/SIGINT)` + `running = False` flag — cleaner, no extra exception needed. Always ends with `consumer.close()` to commit offsets and leave consumer group cleanly.
