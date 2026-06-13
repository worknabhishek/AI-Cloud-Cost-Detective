"""AWS resource scanner modules powered by the AWS CLI."""

from app.scanners.orchestrator import scan_region

__all__ = ["scan_region"]
