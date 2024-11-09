from scripts.run_search import search_quran


query = "للذين استجابوا لربهم الحسنى"
result, hits, best_hit = search_quran(query)
# print(best_hit)
# for hit in hits:
#     print(hit["_source"]["Ayah"])
