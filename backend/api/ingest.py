from fastapi import APIRouter, UploadFile, File
from ingestion.pipeline import IngestionPipeline
import os
from vectorstore.chroma_store import ChromaStore


router = APIRouter()
pipeline = IngestionPipeline()

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    path = f"data/uploads/{file.filename}"
    os.makedirs("data/uploads", exist_ok=True)
    with open(path, "wb") as f:
        f.write(await file.read())

    count = pipeline.ingest_pdf(path)
    return {"status": "ok", "chunks_stored": count}


@router.post("/ingest/url")
async def ingest_url(payload: dict):
    url = payload["url"]
    count = pipeline.ingest_url(url)
    return {"status": "ok", "chunks_stored": count}


## Debug endpoints
@router.get("/debug/chunks")
def debug_chunks():
    store = ChromaStore()
    results = store.collection.get(include=["documents"])
    return {"documents": results["documents"], "ids": results["ids"]}

@router.get("/debug/embeddings")
def debug_embeddings():
    store = ChromaStore()
    results = store.collection.get(include=["embeddings"])
    return {"embeddings_shape": len(results["embeddings"][0])}
