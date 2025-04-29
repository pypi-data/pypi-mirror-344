import os
import yaml

def load_kafka_config():
    """
    Load Kafka configuration from local config file.
    
    Returns:
        dict: Kafka configuration parameters
    """
    config_path = os.path.join(os.path.expanduser("~"), ".kafkahood", "config.yaml")
    try:
        with open(config_path) as f:
            return yaml.load(f, Loader=yaml.Loader)
    except Exception as e:
        raise RuntimeError("Failed to load Kafka config. Please reinstall the package.") from e

# Load config when needed
kafka_config = load_kafka_config()
