from kafka import KafkaConsumer, KafkaProducer

class KafkaClient:
    def __init__(self, config=None):
        """
        Initialize Kafka client with consumer and producer.
        
        Args:
            config (dict): Kafka configuration parameters. If None, uses default config.
        """
        self.config = config
        self._consumer = None
        self._producer = None

    @property 
    def consumer(self):
        """Lazy initialization of Kafka consumer"""
        if self._consumer is None:
            self._consumer = KafkaConsumer(
                bootstrap_servers=self.config["bootstrap_servers"],
                client_id=self.config["client_id"],
                group_id=self.config["group_id"],
                auto_offset_reset=self.config["auto_offset_reset"],
                enable_auto_commit=self.config["enable_auto_commit"],
                security_protocol=self.config["security_protocol"],
                max_poll_records=self.config["max_poll_records"],
                session_timeout_ms=self.config["session_timeout_ms"]
            )
        return self._consumer

    @property
    def producer(self):
        """Lazy initialization of Kafka producer"""
        if self._producer is None:
            self._producer = KafkaProducer(
                bootstrap_servers=self.config["bootstrap_servers"],
                client_id=self.config["client_id"],
                security_protocol=self.config["security_protocol"]
            )
        return self._producer

    def subscribe(self, topics):
        """
        Subscribe consumer to topics.
        
        Args:
            topics (list): List of topic names to subscribe to
        """
        self.consumer.subscribe(topics)

    def send(self, topic, value, key=None):
        """
        Send message to Kafka topic.
        
        Args:
            topic (str): Topic name
            value (bytes): Message value
            key (bytes, optional): Message key
        """
        self.producer.send(topic, value=value, key=key)

    def receive(self, timeout_ms=1000):
        """
        Receive messages from subscribed topics.
        
        Args:
            timeout_ms (int): Maximum time to block waiting for messages
            
        Returns:
            list: List of consumed messages
        """
        return self.consumer.poll(timeout_ms=timeout_ms)

    def close(self):
        """Close both consumer and producer connections"""
        if self._consumer:
            self._consumer.close()
        if self._producer:
            self._producer.close()

# Global client instance for convenience
_kafka_client = None

def configure_kafka_client(config=None):
    """
    Configure the global Kafka client.
    
    Args:
        config (dict): Kafka configuration parameters
    """
    global _kafka_client
    _kafka_client = KafkaClient(config)

def get_kafka_client():
    """
    Get the global Kafka client instance.
    
    Returns:
        KafkaClient: Global Kafka client instance
    """
    if not _kafka_client:
        raise RuntimeError("Kafka client not configured. Call configure_kafka_client first.")
    return _kafka_client
