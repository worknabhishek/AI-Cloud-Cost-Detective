"""Pydantic models for API request and response validation."""

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Application name")


class AWSResource(BaseModel):
    """Represents a single AWS resource submitted for cost analysis."""

    resource_id: str = Field(..., description="Unique identifier for the resource")
    resource_type: str = Field(..., description="AWS resource type, e.g. ec2, rds, s3")
    region: str = Field(..., description="AWS region where the resource is deployed")
    tags: dict[str, str] = Field(
        default_factory=dict,
        description="Optional key-value tags attached to the resource",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional resource-specific attributes (instance type, size, etc.)",
    )


class AnalyzeRequest(BaseModel):
    """Request body for the cost analysis endpoint."""

    account_id: str = Field(..., description="AWS account ID")
    resources: list[AWSResource] = Field(
        ...,
        min_length=1,
        description="List of AWS resources to analyze",
    )


class CostFinding(BaseModel):
    """A single cost optimization or risk finding."""

    resource_id: str = Field(..., description="Resource associated with this finding")
    category: str = Field(
        ...,
        description="Finding category, e.g. idle, oversized, untagged",
    )
    severity: str = Field(..., description="Severity level: low, medium, or high")
    title: str = Field(..., description="Short summary of the finding")
    description: str = Field(..., description="Detailed explanation of the issue")
    estimated_monthly_savings_usd: float = Field(
        ...,
        description="Estimated monthly savings if the recommendation is applied",
    )


class CostSummary(BaseModel):
    """Aggregated cost metrics for the analyzed resources."""

    total_estimated_monthly_cost_usd: float = Field(
        ...,
        description="Total estimated monthly spend across all resources",
    )
    total_potential_savings_usd: float = Field(
        ...,
        description="Total potential monthly savings from all findings",
    )
    resources_analyzed: int = Field(..., description="Number of resources analyzed")
    findings_count: int = Field(..., description="Number of findings generated")


class AnalyzeResponse(BaseModel):
    """Mock cost analysis report returned by the analyze endpoint."""

    account_id: str = Field(..., description="AWS account that was analyzed")
    summary: CostSummary = Field(..., description="High-level cost summary")
    findings: list[CostFinding] = Field(
        default_factory=list,
        description="List of cost optimization findings",
    )
    report_generated_at: str = Field(
        ...,
        description="ISO-8601 timestamp when the report was generated",
    )
