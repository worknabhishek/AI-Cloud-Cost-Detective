"""HTTP route handlers grouped by feature."""

from app.api.routes import ai_analyze, analyze, health, scan

__all__ = ["ai_analyze", "analyze", "health", "scan"]
