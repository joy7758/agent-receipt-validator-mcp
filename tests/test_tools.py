from __future__ import annotations

import json

from agent_receipt_validator_mcp.tools import (
    generate_demo_artifacts,
    summarize_verification_report,
    validate_receipt_json,
)


def test_generate_demo_artifacts_returns_valid() -> None:
    artifacts = generate_demo_artifacts()

    assert artifacts["verdict"] == "valid"
    assert json.loads(artifacts["receipt_json"])["audience"] == "demo-validator"
    assert json.loads(artifacts["verification_report_json"])["verdict"] == "valid"
    assert "BEGIN PUBLIC KEY" in artifacts["public_key_pem"]


def test_validate_receipt_json_accepts_generated_artifacts() -> None:
    artifacts = generate_demo_artifacts()

    result = validate_receipt_json(
        artifacts["receipt_json"],
        artifacts["evidence_bundle_json"],
        artifacts["public_key_pem"],
    )

    assert result["verdict"] == "valid"
    assert result["report"]["verdict"] == "valid"


def test_tampered_evidence_returns_invalid() -> None:
    artifacts = generate_demo_artifacts()
    evidence = json.loads(artifacts["evidence_bundle_json"])
    evidence["tool_output"]["metadata"]["title"] = "Tampered Dataset"

    result = validate_receipt_json(
        artifacts["receipt_json"],
        json.dumps(evidence),
        artifacts["public_key_pem"],
    )

    assert result["verdict"] == "invalid"
    assert result["report"]["verdict"] == "invalid"
    assert "tool_output_hash_mismatch" in result["report"]["errors"]


def test_summarize_verification_report_lists_failed_checks() -> None:
    report = {
        "verdict": "invalid",
        "schema_valid": True,
        "tool_output_hash_match": False,
        "replay_check_performed": False,
        "replay_detected": True,
        "warnings": ["demo warning"],
        "errors": ["tool_output_hash_mismatch"],
    }

    summary = summarize_verification_report(json.dumps(report))

    assert summary["verdict"] == "invalid"
    assert summary["failed_checks"] == ["tool_output_hash_match", "replay_detected"]
    assert summary["warnings"] == ["demo warning"]
    assert summary["errors"] == ["tool_output_hash_mismatch"]


def test_malformed_json_returns_controlled_error() -> None:
    result = validate_receipt_json("{not-json", "{}", "public-key")

    assert result["verdict"] == "invalid"
    assert result["report"] is None
    assert "receipt_json is not valid JSON" in result["errors"][0]
