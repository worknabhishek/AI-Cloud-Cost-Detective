"""Coordinates all resource scanners and assembles a structured scan report."""

from datetime import datetime, timezone

from app.models.scan_schemas import ScanResources, ScanResponse, ScanSummary
from app.scanners.aws_cli import get_caller_identity
from app.scanners.ebs_scanner import fetch_ebs_volumes
from app.scanners.ec2_scanner import fetch_ec2_instances
from app.scanners.elastic_ip_scanner import fetch_elastic_ips


def scan_region(region: str) -> ScanResponse:
    """Run all scanners for a single AWS region and return structured JSON.

    Each scanner invokes the AWS CLI via subprocess to list live resources.
    """
    identity = get_caller_identity()
    account_id = identity.get("Account", "unknown")

    ec2_instances = fetch_ec2_instances(region)
    ebs_volumes = fetch_ebs_volumes(region)
    elastic_ips = fetch_elastic_ips(region)

    resources = ScanResources(
        ec2_instances=ec2_instances,
        ebs_volumes=ebs_volumes,
        elastic_ips=elastic_ips,
    )

    summary = ScanSummary(
        ec2_instance_count=len(ec2_instances),
        ebs_volume_count=len(ebs_volumes),
        elastic_ip_count=len(elastic_ips),
        total_resources=len(ec2_instances) + len(ebs_volumes) + len(elastic_ips),
    )

    return ScanResponse(
        account_id=account_id,
        region=region,
        summary=summary,
        resources=resources,
        scanned_at=datetime.now(timezone.utc).isoformat(),
    )
