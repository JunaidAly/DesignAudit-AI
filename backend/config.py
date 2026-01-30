"""
Backend Configuration
Environment setup and credentials
"""
import os
from typing import Optional

# Environment
ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

# Server
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# Database
# Default to SQLite for development (no installation needed)
# For production, set DATABASE_URL env var to PostgreSQL connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./designaudit.db"
)

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Storage
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "designaudit-uploads")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Alternative: Vercel Blob
VERCEL_BLOB_TOKEN = os.getenv("VERCEL_BLOB_TOKEN")

# AI APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Authentication
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"

# Clerk (Alternative auth)
CLERK_API_KEY = os.getenv("CLERK_API_KEY")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Task Queue
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Monitoring
SENTRY_DSN = os.getenv("SENTRY_DSN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Rate limiting
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 3600))

# File upload
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", 10))
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]

# Audit settings
AUDIT_TIMEOUT_SECONDS = int(os.getenv("AUDIT_TIMEOUT_SECONDS", 300))  # 5 minutes
INSPECTOR_TIMEOUT = int(os.getenv("INSPECTOR_TIMEOUT", 60))
ANALYST_TIMEOUT = int(os.getenv("ANALYST_TIMEOUT", 30))
ADVISOR_TIMEOUT = int(os.getenv("ADVISOR_TIMEOUT", 120))
