"""
CareerPilot AI Backend - Main Application
FastAPI application with authentication and database integration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, ai, mock_tests, performance, career_intelligence, code_execution

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for CareerPilot AI - Your personalized career roadmap assistant",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)  # Phase 2: Authentication
app.include_router(ai.router)    # Phase 3: AI/LLM Integration

# Phase 6A: Mock Tests & Performance
app.include_router(mock_tests.router, prefix="/api")
app.include_router(performance.router, prefix="/api")

# Phase 6B: Career Intelligence
app.include_router(career_intelligence.router, prefix="/api")

# Code Execution Engine
app.include_router(code_execution.router)


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Welcome to CareerPilot AI Backend API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Run the application if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
