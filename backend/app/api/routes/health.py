"""Health check route."""

from fastapi import APIRouter

from app.models.schemas import HealthResponse

# Router for operational endpoints (health, readiness, etc.)
router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return service health status for load balancers and monitoring."""
    return HealthResponse(status="ok", service="Cloud Cost Detective")
