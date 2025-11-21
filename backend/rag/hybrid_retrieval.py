from rag.retriever import Retriever
from rag.reranker import Reranker

class HybridRetriever:
    def __init__(self):
        self.retriever = Retriever()
        self.reranker = Reranker()

    def get(self, query: str, k: int = 5):
        # Get combined (vector + BM25)
        candidates = self.retriever.hybrid_search(query, k=k)

        # Rerank with LLM
        ranked = self.reranker.rerank(query, candidates)

        # Return top-k
        return ranked[:k]
