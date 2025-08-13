import json
import signal
import sys

from confluent_kafka import Consumer, KafkaError

# --- Config ---
TOPIC = 'math_operations'
BOOTSTRAP_SERVERS = 'localhost:9092'
GROUP_ID = 'math_service_logger'

# --- Setup Consumer ---
consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',
})


def shutdown_handler():
    """
    Handle graceful shutdown of the Kafka consumer.
    """
    print("\nGracefully shutting down Kafka consumer...")
    consumer.close()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# --- Subscribe to Topic ---
consumer.subscribe([TOPIC])
print(f"Kafka consumer started and listening on topic '{TOPIC}'")

# --- Poll Loop ---
try:
    while True:
        msg = consumer.poll(1.0)  # Timeout of 1 second

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(f"Kafka error: {msg.error()}")
            continue

        try:
            data = json.loads(msg.value().decode("utf-8"))
            print(f"Received message: {json.dumps(data, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"Failed to decode message: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
    consumer.close()
