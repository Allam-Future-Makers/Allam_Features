from config.elastic_config import ElasticConfig
from elastic.search_manager import SearchManager


def search_mo3gam(query):
    # Elasticsearch setup
    config = ElasticConfig(
        host="localhost", port=9200,username="elastic", password="A0hMtZ=pRxRwbi1qigAZ" 
    )
    es_client = config.get_client()

    # Searching
    index_name = "mo3gam_verse"
    search_manager = SearchManager(es_client, index_name)

    result, hits, best_hit = search_manager.search_ayah(query)
    if best_hit:
        print(f"Mo3gam Verse: {best_hit['mo3gam_verse']}")
    else:
        print("No results found.")

    return result, hits, best_hit


