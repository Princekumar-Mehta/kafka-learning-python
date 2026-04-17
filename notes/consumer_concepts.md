# Kafka Consumer Concepts

## Wikimedia OpenSearch Project — Python Libraries

| Java | Python equivalent |
|------|------------------|
| `okhttp3` | `requests` |
| `okhttp-eventsource` | `sseclient-py` |

```bash
uv add sseclient-py requests
```

---


## Rebalancing

### Eager Rebalance (Stop the World)
- ALL consumers drop ALL partitions
- No consumption during rebalance
- Partitions reassigned from scratch
- Strategies: `RangeAssignor`, `RoundRobinAssignor`

### Cooperative Rebalance (Incremental)
- Only partitions that need to move are revoked
- Other consumers keep consuming unaffected partitions
- No stop the world
- Strategy: `CooperativeStickyAssignor` — default since Kafka 3.0+

```python
config = {
    'partition.assignment.strategy': 'cooperative-sticky'
}
```

---

## Session Timeout & Static Group Membership

### `session.timeout.ms`
- How long Kafka waits for a heartbeat before declaring a consumer dead
- Default: 45 seconds
- If consumer doesn't heartbeat within this window → rebalance triggered

### Static Group Membership — `group.instance.id`
- Assigns a fixed identity to a consumer
- If it restarts within `session.timeout.ms`, Kafka skips the rebalance
- Consumer gets its old partitions back directly — no disruption

```python
config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'group.instance.id': 'consumer-1',  # static identity
    'session.timeout.ms': 30000         # 30 seconds to come back
}
```

**Without static membership:** any restart triggers a full rebalance.  
**With static membership:** restart within timeout → same partitions, no rebalance.

**PySpark use case:** when a Spark executor restarts, it comes back and picks up its partition without disrupting the whole streaming job.

---

## Partition Assignment Callbacks

```python
def on_assign(consumer, partitions):
    logger.info(f"Partitions assigned: {[p.partition for p in partitions]}")

def on_revoke(consumer, partitions):
    logger.info(f"Partitions revoked: {[p.partition for p in partitions]}")

consumer.subscribe(['topic'], on_assign=on_assign, on_revoke=on_revoke)
```

---

## Key Reminders
- Max consumers in a group = number of partitions (extras sit idle)
- Same `group.id` = same consumer group = partitions shared
- Different `group.id` = independent consumer = reads all partitions independently
- `consumer.close()` always commits offsets and leaves group cleanly
