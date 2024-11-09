import pandas as pd
from config.elastic_config import ElasticConfig
from elastic.index_manager import IndexManager


def index_quran():
    # Load data
    df = pd.read_pickle("data/merged_data.pkl")

    # Elasticsearch setup
    config = ElasticConfig(
        host="localhost", port=9200, username="elastic", password="A0hMtZ=pRxRwbi1qigAZ"
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
            "properties": {
                "Ayah": {"type": "text", "analyzer": "default"},
                "I3rab": {"type": "text"},
                "Tafseer_Mokhtasar": {"type": "text"},
                "Tafseer_Jalalayn": {"type": "text"},
                "Tafseer_Saadi": {"type": "text"},
                "telawa": {"type": "keyword"},
            }
        },
    }

    # Indexing
    index_name = "quran_ayah"
    index_manager = IndexManager(es_client, index_name)
    index_manager.create_index(mapping)
    index_manager.bulk_index(df)
