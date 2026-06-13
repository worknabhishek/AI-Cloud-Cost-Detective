"""Low-level AWS CLI integration via Python subprocess.

Each scanner delegates to these helpers so CLI invocation, JSON parsing,
and error handling stay in one place.
"""

import json
import shutil
import subprocess
from typing import Any


class AWSCLINotFoundError(Exception):
    """Raised when the `aws` executable is not on PATH."""


class AWSCLIExecutionError(Exception):
    """Raised when an AWS CLI command exits with a non-zero status."""

    def __init__(self, command: list[str], returncode: int, stderr: str) -> None:
        self.command = command
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(f"AWS CLI failed (exit {returncode}): {stderr.strip()}")


def _resolve_aws_executable() -> str:
    """Locate the AWS CLI binary or raise if it is not installed."""
    aws_path = shutil.which("aws")
    if not aws_path:
        raise AWSCLINotFoundError(
            "AWS CLI not found. Install it and ensure `aws` is on your PATH."
        )
    return aws_path


def run_aws_cli(
    service: str,
    operation: str,
    *,
    region: str | None = None,
    extra_args: list[str] | None = None,
) -> dict[str, Any]:
    """Execute an AWS CLI command and return the parsed JSON response.

    Args:
        service: AWS service name, e.g. "ec2" or "sts".
        operation: CLI operation, e.g. "describe-instances".
        region: Optional AWS region passed via --region.
        extra_args: Additional CLI flags appended before --output json.
    """
    aws_executable = _resolve_aws_executable()

    command = [aws_executable, service, operation]
    if region:
        command.extend(["--region", region])
    if extra_args:
        command.extend(extra_args)
    command.extend(["--output", "json"])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise AWSCLIExecutionError(command, result.returncode, result.stderr)

    # Some successful calls return empty stdout (e.g. no resources); treat as {}.
    stdout = result.stdout.strip()
    if not stdout:
        return {}

    return json.loads(stdout)


def get_caller_identity() -> dict[str, Any]:
    """Return the current AWS account identity via `aws sts get-caller-identity`."""
    return run_aws_cli("sts", "get-caller-identity")
