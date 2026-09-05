"""
Central place to read configuration from environment variables.

Why: every credential and deployment-specific value must come from the
environment, never be hardcoded (Rules.md, Rule o) — this is what lets
someone else self-host their own instance just by filling in their own
.env with their own accounts, and keeps a future hosted version possible
without ripping out hardcoded assumptions later.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./cadenza.db")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    make_webhook_url: str = os.getenv("MAKE_WEBHOOK_URL", "")
    environment: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()