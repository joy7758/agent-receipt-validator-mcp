"""Stdio MCP server entrypoint for agent receipt validation."""

from __future__ import annotations

import sys

from mcp.server.fastmcp import FastMCP

from .tools import (
    generate_demo_artifacts as generate_demo_artifacts_impl,
    summarize_verification_report as summarize_verification_report_impl,
    validate_receipt_json as validate_receipt_json_impl,
)

SERVER_NAME = "Agent Receipt Validator MCP"

mcp = FastMCP(SERVER_NAME)


@mcp.tool(name="validate_receipt_json")
def validate_receipt_json(
    receipt_json: str,
    evidence_bundle_json: str,
    public_key_pem: str,
    audience: str = "demo-validator",
) -> dict:
    """Validate a signed execution receipt JSON string against an evidence bundle JSON string."""
    return validate_receipt_json_impl(receipt_json, evidence_bundle_json, public_key_pem, audience)


@mcp.tool(name="generate_demo_artifacts")
def generate_demo_artifacts(audience: str = "demo-validator") -> dict:
    """Generate fresh demo receipt artifacts and validate them."""
    return generate_demo_artifacts_impl(audience)


@mcp.tool(name="summarize_verification_report")
def summarize_verification_report(verification_report_json: str) -> dict:
    """Summarize a verification report into verdict, failed checks, warnings, and errors."""
    return summarize_verification_report_impl(verification_report_json)


def main() -> None:
    """Run the stdio MCP server."""
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print(
            "Agent Receipt Validator MCP\n\n"
            "Runs a local stdio MCP server exposing:\n"
            "- validate_receipt_json\n"
            "- generate_demo_artifacts\n"
            "- summarize_verification_report\n\n"
            "Configure your MCP client to run: agent-receipt-validator-mcp"
        )
        return
    mcp.run()


if __name__ == "__main__":
    main()
