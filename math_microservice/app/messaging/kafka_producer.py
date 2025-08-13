import json
import logging


from confluent_kafka import Producer

logger = logging.getLogger(__name__)


class KafkaLogger:
    """
    A simple Kafka producer for logging messages to a specified topic.
    """
    def __init__(self, broker='localhost:9092', topic='math_operations'):
        """
        Initialize the Kafka producer with the specified broker and topic.

        :param broker: Kafka broker address
        :param topic: Kafka topic to send messages to
        """
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def send(self, data: dict):
        """
        Send a dictionary as a JSON message to the Kafka topic.

        :param data: Dictionary to send as a message"""
        try:
            self.producer.produce(self.topic, json.dumps(data).encode('utf-8'))
            self.producer.poll(0)  # Non-blocking delivery
            logger.info(f"[Kafka] Sent to topic {self.topic}: {data}")
        except Exception as e:
            logger.error(f"[Kafka] Failed to send message: {e}")
