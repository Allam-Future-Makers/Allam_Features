from scripts.run_search import search_quran

from scripts.run_indexing import index_quran

#index_quran()   # created indices are stored here: sudo ls /var/lib/elasticsearch/indices/

query = "للذين استجابوا لربهم الحسنى"
result, hits, best_hit = search_quran(query)
print(best_hit)
print("----------")
for hit in hits:
    print(hit["_source"]["Ayah"])