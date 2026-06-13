"""Pydantic schemas for OpenAI-powered cost analysis."""

from pydantic import BaseModel, Field

from app.models.scan_schemas import ScanResources


class OptimizationRecommendation(BaseModel):
    """A single AI-generated cost optimization recommendation."""

    resource_id: str = Field(..., description="AWS resource identifier")
    resource_type: str = Field(
        ...,
        description="Resource type: ec2, ebs, or elastic_ip",
    )
    title: str = Field(..., description="Short title for the recommendation")
    recommendation: str = Field(
        ...,
        description="Detailed explanation of the optimization opportunity",
    )
    estimated_monthly_savings_usd: float = Field(
        ...,
        description="Estimated monthly savings if the recommendation is applied",
    )
    remediation_commands: list[str] = Field(
        ...,
        description="AWS CLI commands to remediate the issue",
    )


class AIAnalysisResult(BaseModel):
    """Structured JSON schema returned by the OpenAI model."""

    summary: str = Field(
        ...,
        description="High-level narrative summary of cost optimization opportunities",
    )
    total_estimated_monthly_savings_usd: float = Field(
        ...,
        description="Sum of estimated monthly savings across all recommendations",
    )
    recommendations: list[OptimizationRecommendation] = Field(
        default_factory=list,
        description="List of actionable cost optimization recommendations",
    )


class AIAnalyzeRequest(BaseModel):
    """Request body for AI analysis using pre-collected AWS resource data."""

    account_id: str = Field(..., description="AWS account ID")
    region: str = Field(..., description="AWS region that was scanned")
    resources: ScanResources = Field(..., description="Scanned AWS resource inventory")


class AIAnalyzeResponse(BaseModel):
    """Full AI cost analysis report returned to the client."""

    account_id: str = Field(..., description="AWS account that was analyzed")
    region: str = Field(..., description="AWS region that was analyzed")
    summary: str = Field(..., description="AI-generated executive summary")
    total_estimated_monthly_savings_usd: float = Field(
        ...,
        description="Total estimated monthly savings across all recommendations",
    )
    recommendations: list[OptimizationRecommendation] = Field(
        default_factory=list,
        description="Cost optimization recommendations with remediation commands",
    )
    analyzed_at: str = Field(..., description="ISO-8601 timestamp when analysis completed")
    model: str = Field(..., description="OpenAI model used for the analysis")
