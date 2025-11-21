from vectorstore.chroma_store import ChromaStore
from ingestion.embedder import embed_texts

# --------------------------
# Optional BM25 Implementation
# --------------------------

from rank_bm25 import BM25Okapi

class Retriever:
    def __init__(self):
        self.store = ChromaStore()

        # Load all documents from Chroma
        docs = self.store.collection.get(include=["documents"])["documents"]

        # Flatten as needed (Chroma returns list of list)
        if docs and isinstance(docs[0], list):
            docs = docs[0]

        self.documents = docs

        # Build BM25 index if docs exist
        if self.documents:
            tokenized = [doc.split() for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized)
        else:
            self.bm25 = None

    # --------------------------
    # Pure Vector Retrieval
    # --------------------------
    def vector_search(self, query: str, k: int = 5):
        embedding = embed_texts([query])[0].embedding
        results = self.store.search(embedding, k)
        return results

    # --------------------------
    # BM25 Search
    # --------------------------
    def bm25_search(self, query: str, k: int = 5):
        if not self.bm25:
            return []
        scores = self.bm25.get_scores(query.split())
        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [doc for doc, score in ranked[:k]]

    # --------------------------
    # Hybrid Retrieval
    # --------------------------
    def hybrid_search(self, query: str, k: int = 5):
        vec_results = self.vector_search(query, k)
        bm25_results = self.bm25_search(query, k)

        # Merge results (no duplicates)
        combined = list(dict.fromkeys(vec_results + bm25_results))

        return combined[:k]
