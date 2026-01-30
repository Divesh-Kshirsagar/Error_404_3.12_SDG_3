"""
AarogyaQueue Backend - FastAPI REST API
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import create_db_and_tables
from api import auth, patients, doctors, visits

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for app startup and shutdown
    Creates database tables on startup
    """
    print("🚀 Starting AarogyaQueue Backend...")
    create_db_and_tables()
    yield
    print("👋 Shutting down AarogyaQueue Backend...")

# Initialize FastAPI app
app = FastAPI(
    title="AarogyaQueue API",
    description="Telemedicine Queue Optimizer - Backend API",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware (development mode - allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(visits.router)

# Root endpoint
@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "AarogyaQueue API is running",
        "version": "2.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )
