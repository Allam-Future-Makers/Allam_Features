class SearchManager:
    def __init__(self, es_client, index_name):
        self.es = es_client
        self.index_name = index_name

    def search_ayah(self, query_text):
        search_body = {
            "query": {
                "match": {
                    "Ayah": {
                        "query": query_text,
                        "fuzziness": "AUTO",
                    }
                }
            }
        }
        result = self.es.search(index=self.index_name, body=search_body)
        hits = result["hits"]["hits"]
        if hits:
            best_hit = hits[0]["_source"]
            return result, hits, best_hit
        return None, [], None