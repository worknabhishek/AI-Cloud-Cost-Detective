"""Mock cost analysis service.

This module simulates a cost detective engine. In production, it would query
AWS Cost Explorer, CloudWatch metrics, and resource inventories to produce
real recommendations.
"""

from datetime import datetime, timezone

from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    CostFinding,
    CostSummary,
)

# Base monthly cost estimates (USD) used to mock per-resource spend by type.
_BASE_COST_BY_TYPE: dict[str, float] = {
    "ec2": 85.0,
    "rds": 120.0,
    "s3": 25.0,
    "lambda": 12.0,
    "ebs": 18.0,
}

# Default cost when the resource type is not in the lookup table.
_DEFAULT_BASE_COST = 40.0


def _estimate_resource_cost(resource_type: str) -> float:
    """Return a mock monthly cost for a given AWS resource type."""
    return _BASE_COST_BY_TYPE.get(resource_type.lower(), _DEFAULT_BASE_COST)


def _build_findings(request: AnalyzeRequest) -> list[CostFinding]:
    """Generate mock findings based on simple heuristics over the input data."""
    findings: list[CostFinding] = []

    for resource in request.resources:
        resource_type = resource.resource_type.lower()

        # Flag resources missing an Environment tag — common cost attribution gap.
        if "Environment" not in resource.tags:
            findings.append(
                CostFinding(
                    resource_id=resource.resource_id,
                    category="untagged",
                    severity="low",
                    title="Missing Environment tag",
                    description=(
                        f"Resource {resource.resource_id} ({resource_type}) in "
                        f"{resource.region} lacks an Environment tag, making cost "
                        "allocation and chargeback difficult."
                    ),
                    estimated_monthly_savings_usd=0.0,
                )
            )

        # EC2 instances without instance type metadata are flagged as potentially idle.
        if resource_type == "ec2" and not resource.metadata.get("instance_type"):
            findings.append(
                CostFinding(
                    resource_id=resource.resource_id,
                    category="idle",
                    severity="medium",
                    title="Potentially idle EC2 instance",
                    description=(
                        f"EC2 instance {resource.resource_id} in {resource.region} "
                        "has no instance type metadata and may be underutilized."
                    ),
                    estimated_monthly_savings_usd=45.0,
                )
            )

        # RDS instances flagged as oversized when storage exceeds 500 GB.
        storage_gb = resource.metadata.get("allocated_storage_gb", 0)
        if resource_type == "rds" and isinstance(storage_gb, (int, float)) and storage_gb > 500:
            findings.append(
                CostFinding(
                    resource_id=resource.resource_id,
                    category="oversized",
                    severity="high",
                    title="Oversized RDS storage allocation",
                    description=(
                        f"RDS instance {resource.resource_id} has {storage_gb} GB "
                        "allocated storage. Right-sizing could reduce monthly spend."
                    ),
                    estimated_monthly_savings_usd=75.0,
                )
            )

    return findings


def generate_mock_analysis(request: AnalyzeRequest) -> AnalyzeResponse:
    """Build a complete mock cost analysis report from AWS resource data."""
    findings = _build_findings(request)

    total_cost = sum(
        _estimate_resource_cost(resource.resource_type)
        for resource in request.resources
    )
    total_savings = sum(finding.estimated_monthly_savings_usd for finding in findings)

    summary = CostSummary(
        total_estimated_monthly_cost_usd=round(total_cost, 2),
        total_potential_savings_usd=round(total_savings, 2),
        resources_analyzed=len(request.resources),
        findings_count=len(findings),
    )

    return AnalyzeResponse(
        account_id=request.account_id,
        summary=summary,
        findings=findings,
        report_generated_at=datetime.now(timezone.utc).isoformat(),
    )
