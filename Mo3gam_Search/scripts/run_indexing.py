import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from Mo3gam_Search.config.elastic_config import ElasticConfig
from Mo3gam_Search.elastic.index_manager import IndexManager

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Specify the log file path
data_file_path = os.path.join(parent_directory, "data", "merged_data.pkl")


def index_mo3gam():
    # Load data
    df = pd.read_pickle(data_file_path)

    # Elasticsearch setup
    config = ElasticConfig(
        host=os.getenv("ELASTIC_HOST", "localhost"),
        port=os.getenv("ELASTIC_PORT", "9200"),
        username=os.getenv("ELASTIC_USER", "elastic"),
        password=os.getenv("ELASTIC_PASSWORD", "changeme"),
    )
    es_client = config.get_client()

    # Index settings and mapping
    mapping = {
        "settings": {
            "analysis": {
                "filter": {
                    "arabic_normalization": {"type": "arabic_normalization"},
                    "diacritic_filter": {
                        "type": "asciifolding",
                        "preserve_original": True,
                    },
                },
                "analyzer": {
                    "default": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "arabic_normalization",
                            "diacritic_filter",
                        ],
                    }
                },
            }
        },
        "mappings": {
            "properties": {"mo3gam_verse": {"type": "text", "analyzer": "default"}}
        },
    }

    # Indexing
    index_name = "mo3gam_verse"
    index_manager = IndexManager(es_client, index_name)

    # Check if the index already exists
    if not es_client.indices.exists(index=index_name):
        index_manager.create_index(mapping)
        index_manager.bulk_index(df)
        print(f"Index '{index_name}' created and data indexed.")
