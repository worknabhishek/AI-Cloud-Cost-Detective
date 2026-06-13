"""FastAPI application entry point for Cloud Cost Detective."""

from fastapi import FastAPI

from app.api.routes import ai_analyze, analyze, health, scan

# Application metadata shown in the auto-generated OpenAPI docs
app = FastAPI(
    title="Cloud Cost Detective",
    description="Analyze AWS resource data and surface cost optimization opportunities.",
    version="0.1.0",
)

# Mount feature routers — keeps endpoint definitions modular
app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(scan.router)
app.include_router(ai_analyze.router)
