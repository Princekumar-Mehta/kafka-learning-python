# Kafka Rebalancing

## What triggers a rebalance?
- A new consumer joins the group
- A consumer leaves or crashes
- A consumer doesn't heartbeat within `session.timeout.ms`
- Partitions are added to a topic

---

## Eager Rebalance ("Stop the World")
- All consumers stop consuming
- All partitions are revoked from everyone
- Kafka reassigns all partitions from scratch
- Brief period where NO consumer is consuming — hence "stop the world"
- Strategies: `RangeAssignor`, `RoundRobinAssignor`, `StickyAssignor`

---

## Cooperative Rebalance (Incremental)
- Only the partitions that need to move are revoked
- Consumers keeping their partitions continue consuming uninterrupted
- Happens in multiple small rounds — no stop the world
- Strategy: `CooperativeStickyAssignor`
- Default since Kafka 3.0+

```python
config = {
    'partition.assignment.strategy': 'cooperative-sticky'
}
```

---

## Comparison

| | Eager | Cooperative |
|--|-------|-------------|
| Consumption during rebalance | Stops completely | Continues for unaffected partitions |
| Speed | Slower | Faster |
| Disruption | High | Low |
| Default since | Always | Kafka 3.0+ |

---

## PySpark Impact
- Eager rebalance pauses all micro-batches during reassignment
- Cooperative rebalance only pauses micro-batches for partitions being moved
- For long-running Spark streaming jobs, cooperative rebalance is strongly preferred

---

## Static Group Membership (avoid unnecessary rebalance)
- Set `group.instance.id` on each consumer
- If consumer restarts within `session.timeout.ms`, rebalance is skipped entirely
- Consumer gets its old partitions back directly

```python
config = {
    'group.instance.id': 'consumer-1',
    'session.timeout.ms': 30000
}
```
