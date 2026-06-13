"""Scanner for Elastic IP addresses using the AWS CLI."""

from typing import Any

from app.models.scan_schemas import ElasticIP
from app.scanners.aws_cli import run_aws_cli


def _tags_to_dict(tag_list: list[dict[str, str]] | None) -> dict[str, str]:
    """Convert AWS TagList format [{Key, Value}, ...] to a flat dict."""
    if not tag_list:
        return {}
    return {tag["Key"]: tag["Value"] for tag in tag_list if "Key" in tag and "Value" in tag}


def _parse_address(address: dict[str, Any], region: str) -> ElasticIP:
    """Normalize a single Elastic IP record from describe-addresses."""
    return ElasticIP(
        allocation_id=address.get("AllocationId"),
        public_ip=address.get("PublicIp", "unknown"),
        domain=address.get("Domain", "unknown"),
        association_id=address.get("AssociationId"),
        instance_id=address.get("InstanceId"),
        network_interface_id=address.get("NetworkInterfaceId"),
        region=region,
        tags=_tags_to_dict(address.get("Tags")),
    )


def fetch_elastic_ips(region: str) -> list[ElasticIP]:
    """Fetch all Elastic IPs in a region via `aws ec2 describe-addresses`."""
    response = run_aws_cli("ec2", "describe-addresses", region=region)
    return [_parse_address(address, region) for address in response.get("Addresses", [])]
