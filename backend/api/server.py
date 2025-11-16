from fastapi import FastAPI
from api import ingest

app = FastAPI()
app.include_router(ingest.router)
