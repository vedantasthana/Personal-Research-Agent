from vectorstore.chroma_store import ChromaStore
from ingestion.embedder import embed_texts

class Retriever:
    def __init__(self):
        self.store = ChromaStore()

    def retrieve(self, query: str, k: int = 5):
        # Embed the query text
        embedding = embed_texts([query])[0].embedding

        # Query vector database
        results = self.store.search(embedding, k)

        # results is a list of chunk strings
        return results
