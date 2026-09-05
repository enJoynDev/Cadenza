"""
Health check endpoint.

Why it checks the DB, not just returns 200: a backend that's "up" but can't
reach its database isn't actually healthy — this is the first, cheapest
piece of the observability requirement.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}