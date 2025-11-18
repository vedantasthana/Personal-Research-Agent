from fastapi import FastAPI
from api import ingest, query

app = FastAPI()
app.include_router(ingest.router)
app.include_router(query.router)
