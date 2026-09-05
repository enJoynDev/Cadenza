"""
Cadenza FastAPI application entry point.

Run locally with: uvicorn app.main:app --reload
"""
from fastapi import FastAPI

from app.api import health
from app.db import models  # noqa: F401 — imported so Base.metadata sees the tables
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cadenza",
    description="GTM lead enrichment and outreach automation pipeline.",
    version="0.1.0",
)

app.include_router(health.router)


@app.get("/")
def root():
    return {"service": "cadenza", "status": "running"}