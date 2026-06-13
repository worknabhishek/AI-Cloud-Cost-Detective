"""Scanner for EC2 instances using the AWS CLI."""

from typing import Any

from app.models.scan_schemas import EC2Instance
from app.scanners.aws_cli import run_aws_cli


def _tags_to_dict(tag_list: list[dict[str, str]] | None) -> dict[str, str]:
    """Convert AWS TagList format [{Key, Value}, ...] to a flat dict."""
    if not tag_list:
        return {}
    return {tag["Key"]: tag["Value"] for tag in tag_list if "Key" in tag and "Value" in tag}


def _parse_instance(instance: dict[str, Any], region: str) -> EC2Instance:
    """Normalize a single EC2 instance record from describe-instances."""
    state = instance.get("State", {}).get("Name", "unknown")
    placement = instance.get("Placement", {})

    return EC2Instance(
        instance_id=instance["InstanceId"],
        instance_type=instance.get("InstanceType", "unknown"),
        state=state,
        region=region,
        availability_zone=placement.get("AvailabilityZone", "unknown"),
        launch_time=instance.get("LaunchTime"),
        private_ip_address=instance.get("PrivateIpAddress"),
        public_ip_address=instance.get("PublicIpAddress"),
        tags=_tags_to_dict(instance.get("Tags")),
    )


def fetch_ec2_instances(region: str) -> list[EC2Instance]:
    """Fetch all EC2 instances in a region via `aws ec2 describe-instances`."""
    response = run_aws_cli("ec2", "describe-instances", region=region)
    instances: list[EC2Instance] = []

    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instances.append(_parse_instance(instance, region))

    return instances
