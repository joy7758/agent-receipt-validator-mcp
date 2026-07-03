#!/usr/bin/env python3
"""Local smoke check for Agent Receipt Validator MCP.

This script is intentionally offline and non-networked. It exercises the
package's public tool implementations without starting an MCP client.
"""

from __future__ import annotations

import json

from agent_receipt_validator_mcp.tools import (
    generate_demo_artifacts,
    summarize_verification_report,
    validate_receipt_json,
)


def main() -> int:
    first = generate_demo_artifacts()
    second = generate_demo_artifacts()

    assert first["verdict"] == "valid", "generated demo artifacts must validate"

    roundtrip = validate_receipt_json(
        first["receipt_json"],
        first["evidence_bundle_json"],
        first["public_key_pem"],
    )
    assert roundtrip["verdict"] == "valid", "generated artifacts must validate roundtrip"

    cross_run = validate_receipt_json(
        first["receipt_json"],
        second["evidence_bundle_json"],
        first["public_key_pem"],
    )
    assert cross_run["verdict"] == "invalid", "cross-run evidence bundle must be rejected"

    summary = summarize_verification_report(json.dumps(cross_run["report"]))
    assert summary["verdict"] == "invalid", "invalid report summary must preserve verdict"
    assert summary["failed_checks"], "invalid report summary must include failed checks"

    print("smoke_check_status=pass")
    print("generated_demo_verdict=valid")
    print("validation_roundtrip_verdict=valid")
    print("cross_run_bundle_verdict=invalid")
    print("summary_failed_checks_present=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
