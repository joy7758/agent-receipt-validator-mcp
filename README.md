# Agent Receipt Validator MCP

A local stdio MCP server for validating signed agent execution receipts against evidence bundles.

This server wraps the `verifiable-tool-invocation-flow` Python package and exposes receipt validation as MCP tools for local clients such as Claude Desktop, Cursor, and other MCP-compatible agent runtimes.

## What This MCP Server Does

- Validates an `execution_receipt.json` payload against an `evidence_bundle.json` payload and a public key PEM.
- Generates fresh demo artifacts using the same deterministic demo flow as the core package.
- Summarizes verification reports into verdict, failed checks, warnings, and errors.
- Runs locally over stdio.

## Installation From Local Checkout

```bash
cd agent-receipt-validator-mcp
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## MCP Client Config

Use this stdio configuration after installing the package in your local environment:

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

## Tools

### `validate_receipt_json`

Inputs:

- `receipt_json`: JSON string containing an execution receipt.
- `evidence_bundle_json`: JSON string containing the evidence bundle.
- `public_key_pem`: public key PEM string.
- `audience`: expected audience, default `demo-validator`.

Output:

```json
{
  "verdict": "valid",
  "report": {
    "verdict": "valid"
  }
}
```

### `generate_demo_artifacts`

Inputs:

- `audience`: expected audience, default `demo-validator`.

Output:

```json
{
  "receipt_json": "{...}",
  "evidence_bundle_json": "{...}",
  "public_key_pem": "-----BEGIN PUBLIC KEY-----...",
  "verification_report_json": "{...}",
  "verdict": "valid"
}
```

The demo artifacts are generated fresh at runtime. The server does not use static expired samples.

### `summarize_verification_report`

Inputs:

- `verification_report_json`: JSON string containing a verification report.

Output:

```json
{
  "verdict": "invalid",
  "failed_checks": ["tool_output_hash_match"],
  "warnings": [],
  "errors": ["tool_output_hash_mismatch"]
}
```

## Boundary Statement

This MCP server validates signed execution evidence.
It does not prove semantic correctness of the tool output.
It does not prove that the policy itself is correct.
It does not protect against a compromised signer.
It does not replace sandboxing, IAM, access control, monitoring, or human approval.
Do not pass private keys, API tokens, confidential evidence bundles, or production receipts to untrusted MCP clients.

This first release is a local stdio MCP server. Remote Streamable HTTP hosting and Smithery publication are future tasks.

## Related Projects

- Core repo: <https://github.com/joy7758/verifiable-tool-invocation-flow>
- PyPI package: <https://pypi.org/project/verifiable-tool-invocation-flow/0.1.1/>
- GitHub Action: <https://github.com/marketplace/actions/verify-agent-execution-receipt>
- Hugging Face Space: <https://huggingface.co/spaces/joy7759/agent-receipt-validator>

## Publishing

This package is intended to be published through PyPI Trusted Publishing using GitHub Actions OIDC.

Workflow:

- `.github/workflows/publish.yml`
- TestPyPI environment: `testpypi`
- PyPI environment: `pypi`

No PyPI API token is stored in this repository.

Trusted Publishing must be configured once in TestPyPI/PyPI before the workflow can publish.

## Development

```bash
pytest tests/test_tools.py
agent-receipt-validator-mcp --help
```
