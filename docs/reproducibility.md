# Reproducibility Workflow

```text
document_id = AGENT_RECEIPT_VALIDATOR_MCP_REPRODUCIBILITY
version = 0.1.1
artifact = agent-receipt-validator-mcp
```

## Local environment

Use Python `>=3.10,<3.14`.

```bash
cd agent-receipt-validator-mcp
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## Unit tests

```bash
python -m pytest tests/test_tools.py
```

Expected evidence:

```text
valid_demo_artifacts = pass
generated_artifacts_validate = pass
tampered_evidence_rejected = pass
cross_run_bundle_rejected = pass
verification_report_summary = pass
malformed_json_controlled_error = pass
```

## CLI help check

```bash
agent-receipt-validator-mcp --help
```

Expected evidence:

```text
help_mentions_server = true
help_mentions_validate_receipt_json = true
help_mentions_generate_demo_artifacts = true
help_mentions_summarize_verification_report = true
```

## Smoke check

```bash
python scripts/smoke_check.py
```

Expected evidence:

```text
generated_demo_verdict = valid
validation_roundtrip_verdict = valid
cross_run_bundle_verdict = invalid
summary_failed_checks_present = true
```

## Reproducibility boundary

The checks above exercise package behavior and receipt/evidence validation
plumbing. They do not prove semantic correctness of arbitrary tool output, do
not prove policy correctness, and do not replace independent source review.
