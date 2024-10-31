import logging, os
from elasticsearch import Elasticsearch

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Specify the log file path
log_file_path = os.path.join(parent_directory, "logs", "elastic_logs.log")

# Setup logging
logging.basicConfig(
    filename=log_file_path,  # Specify the log file path
    level=logging.INFO,  # Log messages with INFO level and above
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format of log messages
)


class ElasticConfig:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_client(self):
        try:
            es = Elasticsearch(
                [f"http://{self.host}:{self.port}"],
                basic_auth=(self.username, self.password),
            )
            if es.ping():
                logging.info("Successfully connected to Elasticsearch.")
            else:
                logging.error("Elasticsearch connection failed.")
                raise Exception("Elasticsearch connection failed")
            return es
        except Exception as e:
            logging.exception(
                "An error occurred while trying to connect to Elasticsearch."
            )
            raise e