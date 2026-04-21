"""Tool implementations for the agent receipt validator MCP server."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from secrets import token_hex
from typing import Any
from uuid import uuid4

from verifiable_tool_invocation_flow.guarded_tool_call import guarded_tool_call
from verifiable_tool_invocation_flow.models import ExecutionRequest, PolicySnapshot, ToolManifest
from verifiable_tool_invocation_flow.resources import load_example_json
from verifiable_tool_invocation_flow.signer import ReceiptSigner
from verifiable_tool_invocation_flow.tools.demo_metadata_lookup_tool import demo_metadata_lookup_tool
from verifiable_tool_invocation_flow.validator import validate_receipt

DEFAULT_AUDIENCE = "demo-validator"


def validate_receipt_json(
    receipt_json: str,
    evidence_bundle_json: str,
    public_key_pem: str,
    audience: str = DEFAULT_AUDIENCE,
) -> dict[str, Any]:
    """Validate a signed execution receipt JSON string against an evidence bundle JSON string."""
    try:
        receipt = _parse_json_object(receipt_json, "receipt_json")
        evidence_bundle = _parse_json_object(evidence_bundle_json, "evidence_bundle_json")
    except ValueError as exc:
        return {"verdict": "invalid", "report": None, "errors": [str(exc)]}

    if not public_key_pem.strip():
        return {"verdict": "invalid", "report": None, "errors": ["public_key_pem is required"]}

    try:
        report = validate_receipt(
            receipt=receipt,
            evidence_bundle=evidence_bundle,
            public_key_pem=public_key_pem.encode("utf-8"),
            audience=(audience or DEFAULT_AUDIENCE).strip() or DEFAULT_AUDIENCE,
            replay_cache_path=None,
            update_replay_cache=False,
        )
    except Exception as exc:  # noqa: BLE001 - MCP tools should return controlled JSON errors.
        return {"verdict": "invalid", "report": None, "errors": [f"validation_failed: {exc}"]}

    return {"verdict": report["verdict"], "report": report}


def generate_demo_artifacts(audience: str = DEFAULT_AUDIENCE) -> dict[str, Any]:
    """Generate fresh demo receipt artifacts and validate them immediately."""
    effective_audience = (audience or DEFAULT_AUDIENCE).strip() or DEFAULT_AUDIENCE
    signer = ReceiptSigner.generate_demo()
    result = guarded_tool_call(
        request=_build_demo_request(effective_audience),
        policy=PolicySnapshot.model_validate(load_example_json("policy_snapshot.json")),
        tool_manifest=ToolManifest.model_validate(load_example_json("tool_manifest.json")),
        tool_input=load_example_json("tool_input.json"),
        tool_fn=demo_metadata_lookup_tool,
        signer=signer,
        audience=effective_audience,
        replay_cache_path=None,
        update_replay_cache=False,
    )

    return {
        "receipt_json": _pretty_json(result.receipt),
        "evidence_bundle_json": _pretty_json(result.evidence_bundle),
        "public_key_pem": signer.public_key_pem().decode("utf-8"),
        "verification_report_json": _pretty_json(result.verification_report),
        "verdict": result.verification_report["verdict"],
    }


def summarize_verification_report(verification_report_json: str) -> dict[str, Any]:
    """Summarize a verification report into verdict, failed checks, warnings, and errors."""
    try:
        report = _parse_json_object(verification_report_json, "verification_report_json")
    except ValueError as exc:
        return {"verdict": "invalid", "failed_checks": [], "warnings": [], "errors": [str(exc)]}

    failed_checks: list[str] = []
    for key, value in report.items():
        if not isinstance(value, bool):
            continue
        if key == "replay_check_performed":
            continue
        if key == "replay_detected":
            if value:
                failed_checks.append(key)
            continue
        if value is False:
            failed_checks.append(key)

    return {
        "verdict": str(report.get("verdict", "invalid")),
        "failed_checks": failed_checks,
        "warnings": _string_list(report.get("warnings")),
        "errors": _string_list(report.get("errors")),
    }


def _build_demo_request(audience: str) -> ExecutionRequest:
    payload = load_example_json("input_request.json")
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload.update(
        {
            "request_id": f"req-{uuid4()}",
            "execution_id": f"exec-{uuid4()}",
            "nonce": token_hex(16),
            "requested_at": now,
            "audience": audience,
        }
    )
    return ExecutionRequest.model_validate(payload)


def _parse_json_object(value: str, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {exc.msg}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must be a JSON object")
    return parsed


def _pretty_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]
