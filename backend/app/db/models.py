"""
Core database schema.

Why a status field on Lead plus a separate LeadEvent log: the database is
the single source of truth for pipeline state (Plan.md §5) — every stage
reads/writes here, and the dashboard reads from here directly instead of
guessing. LeadEvent satisfies the Observability NFR (RequirementsAndSetup.md
§2): every pipeline stage writes a structured log entry, not just a status
flip.
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class LeadSource(str, enum.Enum):
    csv = "csv"
    scraper = "scraper"


class LeadStatus(str, enum.Enum):
    new = "new"
    enriching = "enriching"
    enriched = "enriched"
    no_email_found = "no_email_found"
    in_review = "in_review"
    personalizing = "personalizing"
    ready_to_send = "ready_to_send"
    delivered = "delivered"
    failed = "failed"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=_uuid)
    domain = Column(String, nullable=False, index=True)
    company_name = Column(String, nullable=True)
    contact_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    personalized_message = Column(Text, nullable=True)

    source = Column(Enum(LeadSource), nullable=False, default=LeadSource.csv)
    status = Column(Enum(LeadStatus), nullable=False, default=LeadStatus.new, index=True)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=_now)
    updated_at = Column(DateTime(timezone=True), default=_now, onupdate=_now)

    events = relationship("LeadEvent", back_populates="lead", cascade="all, delete-orphan")


class LeadEvent(Base):
    """One row per pipeline-stage transition for a lead — the audit trail
    the dashboard and future debugging read from."""

    __tablename__ = "lead_events"

    id = Column(String, primary_key=True, default=_uuid)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    stage = Column(String, nullable=False)  # e.g. ingestion, enrichment, orchestration, personalization, delivery
    status = Column(Enum(LeadStatus), nullable=False)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_now)

    lead = relationship("Lead", back_populates="events")