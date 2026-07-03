from __future__ import annotations

import json

from agent_receipt_validator_mcp.tools import (
    generate_demo_artifacts,
    summarize_verification_report,
    validate_receipt_json,
)


def test_cross_run_diagnostic_surface_is_stable() -> None:
    first = generate_demo_artifacts()
    second = generate_demo_artifacts()

    result = validate_receipt_json(
        first["receipt_json"],
        second["evidence_bundle_json"],
        first["public_key_pem"],
    )

    assert result["verdict"] == "invalid"
    assert result["report"]["verdict"] == "invalid"
    assert "request_binding_mismatch" in result["report"]["errors"]
    assert "pre_execution_commitment_mismatch" in result["report"]["errors"]

    summary = summarize_verification_report(json.dumps(result["report"]))
    assert summary["verdict"] == "invalid"
    assert "replay_detected" in summary["failed_checks"]
