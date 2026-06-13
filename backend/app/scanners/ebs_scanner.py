"""Scanner for EBS volumes using the AWS CLI."""

from typing import Any

from app.models.scan_schemas import EBSVolume
from app.scanners.aws_cli import run_aws_cli


def _tags_to_dict(tag_list: list[dict[str, str]] | None) -> dict[str, str]:
    """Convert AWS TagList format [{Key, Value}, ...] to a flat dict."""
    if not tag_list:
        return {}
    return {tag["Key"]: tag["Value"] for tag in tag_list if "Key" in tag and "Value" in tag}


def _attached_instance_id(attachments: list[dict[str, Any]] | None) -> str | None:
    """Return the instance ID of the first volume attachment, if any."""
    if not attachments:
        return None
    return attachments[0].get("InstanceId")


def _parse_volume(volume: dict[str, Any], region: str) -> EBSVolume:
    """Normalize a single EBS volume record from describe-volumes."""
    return EBSVolume(
        volume_id=volume["VolumeId"],
        size_gb=volume.get("Size", 0),
        volume_type=volume.get("VolumeType", "unknown"),
        state=volume.get("State", "unknown"),
        region=region,
        availability_zone=volume.get("AvailabilityZone", "unknown"),
        encrypted=volume.get("Encrypted", False),
        attached_instance_id=_attached_instance_id(volume.get("Attachments")),
        tags=_tags_to_dict(volume.get("Tags")),
    )


def fetch_ebs_volumes(region: str) -> list[EBSVolume]:
    """Fetch all EBS volumes in a region via `aws ec2 describe-volumes`."""
    response = run_aws_cli("ec2", "describe-volumes", region=region)
    return [_parse_volume(volume, region) for volume in response.get("Volumes", [])]
