"""AWS resource scan route."""

from fastapi import APIRouter, HTTPException, Query

from app.models.scan_schemas import ScanResponse
from app.scanners.aws_cli import AWSCLIExecutionError, AWSCLINotFoundError
from app.scanners.orchestrator import scan_region

router = APIRouter(tags=["scan"])


@router.get("/scan", response_model=ScanResponse)
def scan_aws_resources(
    region: str = Query(
        default="us-east-1",
        description="AWS region to scan for EC2, EBS, and Elastic IP resources",
        examples=["us-east-1"],
    ),
) -> ScanResponse:
    """Scan live AWS resources via the AWS CLI and return structured JSON.

    Requires the AWS CLI to be installed and configured with valid credentials.
    """
    try:
        return scan_region(region)
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
