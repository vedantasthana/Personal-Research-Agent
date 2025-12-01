from fastapi import FastAPI
from api import ingest, query, agent

app = FastAPI()
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(agent.router)
