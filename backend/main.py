"""
FastAPI Backend for DesignAudit AI
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from backend.database import init_db
from backend.routes.audits import router as audits_router

# Load environment variables
load_dotenv()

# Initialize database
init_db()

# Initialize FastAPI app
app = FastAPI(
    title="DesignAudit AI API",
    description="Multi-agent AI system for design quality auditing",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "healthy",
        "service": "DesignAudit AI API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "ok",
        "service": "DesignAudit AI API",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
    }


# Include routers
app.include_router(audits_router, prefix="/api")


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV") == "development",
    )
