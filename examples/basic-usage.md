# Basic Usage Walkthrough

```text
example_id = AGENT_RECEIPT_VALIDATOR_MCP_BASIC_USAGE
version = 0.1.1
artifact = agent-receipt-validator-mcp
```

## Install locally

```bash
cd agent-receipt-validator-mcp
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## Check the command surface

```bash
agent-receipt-validator-mcp --help
```

The help output should list:

```text
validate_receipt_json
generate_demo_artifacts
summarize_verification_report
```

## Run a local behavior smoke check

```bash
python scripts/smoke_check.py
```

The smoke check generates fresh demo artifacts, validates them, verifies that a
cross-run evidence bundle is rejected, and summarizes the invalid report.

## MCP client configuration

After installing the package in the environment used by the MCP client, use:

```json
{
  "mcpServers": {
    "agent-receipt-validator": {
      "command": "agent-receipt-validator-mcp",
      "args": []
    }
  }
}
```

## Reviewer boundary

This walkthrough demonstrates receipt/evidence validation plumbing. A valid
receipt means the evidence bundle matches the signed execution evidence under
the expected audience and public key. It does not mean the underlying software
change is semantically correct.
