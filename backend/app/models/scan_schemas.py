"""Pydantic schemas for AWS resource scan requests and responses."""

from datetime import datetime

from pydantic import BaseModel, Field


class EC2Instance(BaseModel):
    """Normalized EC2 instance returned by the scanner."""

    instance_id: str = Field(..., description="EC2 instance identifier")
    instance_type: str = Field(..., description="Instance family and size, e.g. t3.micro")
    state: str = Field(..., description="Instance state, e.g. running, stopped")
    region: str = Field(..., description="AWS region")
    availability_zone: str = Field(..., description="Availability zone")
    launch_time: datetime | None = Field(None, description="When the instance was launched")
    private_ip_address: str | None = Field(None, description="Private IPv4 address")
    public_ip_address: str | None = Field(None, description="Public IPv4 address")
    tags: dict[str, str] = Field(default_factory=dict, description="Resource tags")


class EBSVolume(BaseModel):
    """Normalized EBS volume returned by the scanner."""

    volume_id: str = Field(..., description="EBS volume identifier")
    size_gb: int = Field(..., description="Provisioned size in GiB")
    volume_type: str = Field(..., description="Volume type, e.g. gp3, io2")
    state: str = Field(..., description="Volume state, e.g. in-use, available")
    region: str = Field(..., description="AWS region")
    availability_zone: str = Field(..., description="Availability zone")
    encrypted: bool = Field(..., description="Whether the volume is encrypted")
    attached_instance_id: str | None = Field(
        None,
        description="EC2 instance the volume is attached to, if any",
    )
    tags: dict[str, str] = Field(default_factory=dict, description="Resource tags")


class ElasticIP(BaseModel):
    """Normalized Elastic IP address returned by the scanner."""

    allocation_id: str | None = Field(None, description="VPC allocation ID")
    public_ip: str = Field(..., description="Public IPv4 address")
    domain: str = Field(..., description="Address domain: vpc or standard")
    association_id: str | None = Field(None, description="Association ID when in use")
    instance_id: str | None = Field(None, description="Associated EC2 instance, if any")
    network_interface_id: str | None = Field(
        None,
        description="Associated ENI, if any",
    )
    region: str = Field(..., description="AWS region")
    tags: dict[str, str] = Field(default_factory=dict, description="Resource tags")


class ScanResources(BaseModel):
    """Grouped resource lists produced by the scanners."""

    ec2_instances: list[EC2Instance] = Field(
        default_factory=list,
        description="EC2 instances discovered in the region",
    )
    ebs_volumes: list[EBSVolume] = Field(
        default_factory=list,
        description="EBS volumes discovered in the region",
    )
    elastic_ips: list[ElasticIP] = Field(
        default_factory=list,
        description="Elastic IP addresses discovered in the region",
    )


class ScanSummary(BaseModel):
    """Aggregate counts for a regional scan."""

    ec2_instance_count: int = Field(..., description="Number of EC2 instances found")
    ebs_volume_count: int = Field(..., description="Number of EBS volumes found")
    elastic_ip_count: int = Field(..., description="Number of Elastic IPs found")
    total_resources: int = Field(..., description="Total resources across all scanners")


class ScanResponse(BaseModel):
    """Structured JSON report returned by GET /scan."""

    account_id: str = Field(..., description="AWS account that was scanned")
    region: str = Field(..., description="AWS region that was scanned")
    summary: ScanSummary = Field(..., description="Resource counts by type")
    resources: ScanResources = Field(..., description="Detailed resource inventories")
    scanned_at: str = Field(..., description="ISO-8601 timestamp of the scan")
