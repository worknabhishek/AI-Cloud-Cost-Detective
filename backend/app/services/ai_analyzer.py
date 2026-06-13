"""OpenAI-powered AWS cost analysis service.

Sends scanned AWS resource inventories to OpenAI and returns structured
recommendations with estimated savings and AWS CLI remediation commands.
"""

import json
import os
from datetime import datetime, timezone

from openai import APIError, OpenAI

from app.models.ai_schemas import (
    AIAnalysisResult,
    AIAnalyzeRequest,
    AIAnalyzeResponse,
)
from app.models.scan_schemas import ScanResponse

# Configurable via environment; gpt-4o-mini balances cost and quality.
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are Cloud Cost Detective, an expert AWS cost optimization analyst.

Analyze the provided AWS resource inventory (EC2 instances, EBS volumes, Elastic IPs)
and identify concrete cost-saving opportunities.

For each recommendation you MUST provide:
1. The specific resource_id and resource_type (ec2, ebs, or elastic_ip)
2. A clear title and detailed recommendation
3. A realistic estimated_monthly_savings_usd (USD per month)
4. One or more exact AWS CLI remediation_commands the operator can run

Focus on common waste patterns:
- Stopped or idle EC2 instances still incurring EBS/storage costs
- Unattached EBS volumes (state: available)
- Unassociated Elastic IPs (no association_id / instance_id)
- Oversized instance types for light workloads
- Missing cost-allocation tags

Rules:
- Use only valid AWS CLI commands with correct --region flags
- Include the region from the input data in every command
- Flag destructive commands (terminate, delete) clearly in the recommendation text
- If no issues are found, return an empty recommendations list with an explanatory summary
- total_estimated_monthly_savings_usd must equal the sum of individual recommendation savings
"""


class OpenAIConfigurationError(Exception):
    """Raised when required OpenAI configuration is missing."""


class OpenAIAnalysisError(Exception):
    """Raised when the OpenAI API call or response parsing fails."""


def _get_openai_client() -> OpenAI:
    """Build an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIConfigurationError(
            "OPENAI_API_KEY environment variable is not set. "
            "Export your API key before calling the AI analyzer."
        )
    return OpenAI(api_key=api_key)


def _get_model() -> str:
    """Return the OpenAI model name from env or the default."""
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def _build_user_prompt(payload: dict) -> str:
    """Serialize AWS resource data into the user message for OpenAI."""
    return (
        "Analyze the following AWS resource inventory and return cost optimization "
        f"recommendations with AWS CLI remediation commands:\n\n"
        f"{json.dumps(payload, indent=2, default=str)}"
    )


def _call_openai(client: OpenAI, model: str, resource_payload: dict) -> AIAnalysisResult:
    """Send resource data to OpenAI and parse the structured JSON response."""
    try:
        response = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_prompt(resource_payload)},
            ],
            response_format=AIAnalysisResult,
        )
    except APIError as exc:
        raise OpenAIAnalysisError(f"OpenAI API error: {exc}") from exc

    analysis = response.choices[0].message.parsed
    if analysis is None:
        raise OpenAIAnalysisError("OpenAI returned an unparseable response")

    return analysis


def analyze_resources(request: AIAnalyzeRequest) -> AIAnalyzeResponse:
    """Analyze AWS resource data with OpenAI and return structured recommendations."""
    client = _get_openai_client()
    model = _get_model()

    resource_payload = request.model_dump(mode="json")
    analysis = _call_openai(client, model, resource_payload)

    return AIAnalyzeResponse(
        account_id=request.account_id,
        region=request.region,
        summary=analysis.summary,
        total_estimated_monthly_savings_usd=analysis.total_estimated_monthly_savings_usd,
        recommendations=analysis.recommendations,
        analyzed_at=datetime.now(timezone.utc).isoformat(),
        model=model,
    )


def analyze_scan_result(scan: ScanResponse) -> AIAnalyzeResponse:
    """Convenience wrapper that accepts a ScanResponse from GET /scan."""
    request = AIAnalyzeRequest(
        account_id=scan.account_id,
        region=scan.region,
        resources=scan.resources,
    )
    return analyze_resources(request)
