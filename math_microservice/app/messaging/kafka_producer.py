import json
import logging


from confluent_kafka import Producer

logger = logging.getLogger(__name__)


class KafkaLogger:
    def __init__(self, broker='localhost:9092', topic='math_operations'):
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def send(self, data: dict):
        try:
            self.producer.produce(self.topic, json.dumps(data).encode('utf-8'))
            self.producer.poll(0)  # Non-blocking delivery
            logger.info(f"[Kafka] Sent to topic {self.topic}: {data}")
        except Exception as e:
            logger.error(f"[Kafka] Failed to send message: {e}")
