from fastapi import APIRouter
from rag.retriever import Retriever
from rag.context_builder import build_context
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
router = APIRouter()

@router.post("/query")
async def rag_query(payload: dict):
    query = payload["query"]

    # Retrieve relevant chunks
    chunks = Retriever().retrieve(query, k=5)

    # Build LLM prompt
    context = build_context(chunks)

    # Ask the LLM
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": query}
        ]
    )

    answer = response.choices[0].message.content
    # print("🔍 Query:", query)
    # print("🔍 Retrieved chunks:", len(chunks))

    return {"answer": answer, "chunks_used": chunks}


