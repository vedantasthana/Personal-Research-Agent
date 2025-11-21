from fastapi import APIRouter
from rag.retriever import Retriever
from rag.hybrid_retrieval import HybridRetriever
from rag.context_builder import build_context
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()

# # --------------------------
# # Test Endpoints
# # --------------------------

# @router.post("/test/vector")
# def test_vector(payload: dict):
#     q = payload["query"]
#     retriever = Retriever()
#     res = retriever.vector_search(q, k=5)
#     return {"vector_results": res}

# @router.post("/test/bm25")
# def test_bm25(payload: dict):
#     q = payload["query"]
#     retriever = Retriever()
#     res = retriever.bm25_search(q, k=5)
#     return {"bm25_results": res}

# @router.post("/test/hybrid")
# def test_hybrid(payload: dict):
#     q = payload["query"]
#     hybrid = HybridRetriever()
#     res = hybrid.get(q, k=5)
#     return {"hybrid_results": res}

# --------------------------
# Full RAG Query
# --------------------------

@router.post("/query")
def rag_query(payload: dict):
    query = payload["query"]

    # Hybrid retrieval + reranking
    hybrid = HybridRetriever()
    passages = hybrid.get(query, k=5)

    context = build_context(passages)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]
    )

    answer = response.choices[0].message.content
    return {"answer": answer, "used_passages": passages}
