"""OpenAI-powered cost analysis route."""

from fastapi import APIRouter, HTTPException, Query

from app.models.ai_schemas import AIAnalyzeRequest, AIAnalyzeResponse
from app.models.scan_schemas import ScanResponse
from app.scanners.aws_cli import AWSCLIExecutionError, AWSCLINotFoundError
from app.scanners.orchestrator import scan_region
from app.services.ai_analyzer import (
    OpenAIAnalysisError,
    OpenAIConfigurationError,
    analyze_resources,
    analyze_scan_result,
)

router = APIRouter(tags=["ai-analyze"])


@router.post("/ai-analyze", response_model=AIAnalyzeResponse)
def ai_analyze_resources(request: AIAnalyzeRequest) -> AIAnalyzeResponse:
    """Send AWS resource data to OpenAI and return cost optimization insights.

    Accepts the same resource structure produced by GET /scan. Returns
    recommendations, estimated savings, and AWS CLI remediation commands.
    """
    try:
        return analyze_resources(request)
    except OpenAIConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OpenAIAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("/ai-analyze/scan", response_model=AIAnalyzeResponse)
def ai_analyze_from_scan(scan: ScanResponse) -> AIAnalyzeResponse:
    """Analyze a complete ScanResponse payload (e.g. output from GET /scan)."""
    try:
        return analyze_scan_result(scan)
    except OpenAIConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OpenAIAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/ai-analyze", response_model=AIAnalyzeResponse)
def ai_analyze_region(
    region: str = Query(
        default="us-east-1",
        description="AWS region to scan and analyze with OpenAI",
        examples=["us-east-1"],
    ),
) -> AIAnalyzeResponse:
    """Scan a region via AWS CLI, then send results to OpenAI for analysis.

    End-to-end pipeline: AWS CLI scan → OpenAI cost recommendations.
    """
    try:
        scan_result = scan_region(region)
        return analyze_scan_result(scan_result)
    except AWSCLINotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except AWSCLIExecutionError as exc:
        raise HTTPException(
            status_code=502,
            detail={
                "message": str(exc),
                "command": exc.command,
                "stderr": exc.stderr.strip(),
            },
        ) from exc
    except OpenAIConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except OpenAIAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
