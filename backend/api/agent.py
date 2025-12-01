from fastapi import APIRouter
from agent.runtime import AgentRuntime

router = APIRouter()
runtime = AgentRuntime()


@router.post("/agent")
async def agent_query(payload: dict):
    """
    Generic agent entrypoint.

    Example body:
    {
      "query": "Summarize the PDF I uploaded about RAG pipelines."
    }
    """
    query = payload["query"]
    answer = runtime.run(query)
    return {"answer": answer}
