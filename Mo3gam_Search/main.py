from scripts.run_search import search_mo3gam

from scripts.run_indexing import index_mo3gam

#index_mo3gam()   # created indices are stored here: sudo ls /var/lib/elasticsearch/indices/

query = "للذين استجابوا لربهم الحسنى"
result, hits, best_hit = search_mo3gam(query)
print(best_hit)
print("----------")
for hit in hits:
    print(hit["_source"]["mo3gam_verse"])