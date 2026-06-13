"""Cost analysis route."""

from fastapi import APIRouter

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.cost_analyzer import generate_mock_analysis

# Router for cost analysis endpoints
router = APIRouter(tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_costs(request: AnalyzeRequest) -> AnalyzeResponse:
    """Accept AWS resource data and return a mock cost analysis report.

    The request body should include an account ID and a list of resources.
    Each resource should specify its ID, type, region, and optional tags/metadata.
    """
    return generate_mock_analysis(request)
