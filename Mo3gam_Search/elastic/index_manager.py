class IndexManager:
    def __init__(self, es_client, index_name):
        self.es = es_client
        self.index_name = index_name

    def create_index(self, mapping):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, body=mapping)
        print(f"Index '{self.index_name}' created.")

    def index_document(self, doc_id, document):
        self.es.index(index=self.index_name, id=doc_id, body=document)

    def bulk_index(self, df):
        for idx, row in df.iterrows():
            document = {
                "mo3gam_verse": row["mo3gam_verse"]
            }
            self.index_document(idx, document)
        print("Indexing completed.")
