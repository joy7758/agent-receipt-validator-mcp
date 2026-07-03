# Software Architecture

```text
document_id = AGENT_RECEIPT_VALIDATOR_MCP_SOFTWARE_ARCHITECTURE
version = 0.1.1
artifact = agent-receipt-validator-mcp
```

## Purpose

Agent Receipt Validator MCP provides a local Model Context Protocol (MCP)
server that lets an MCP-compatible agent client validate signed execution
receipts against evidence bundles. The package is intentionally small: it
adapts the core `verifiable-tool-invocation-flow` receipt toolkit into a local
stdio MCP tool surface.

## Component map

```text
MCP client
  -> stdio command: agent-receipt-validator-mcp
  -> src/agent_receipt_validator_mcp/server.py
  -> src/agent_receipt_validator_mcp/tools.py
  -> verifiable_tool_invocation_flow validator/signer/demo resources
```

## Runtime components

```text
server.py
  FastMCP server
  tool registration
  CLI --help surface

tools.py
  validate_receipt_json
  generate_demo_artifacts
  summarize_verification_report
  controlled JSON error handling

verifiable-tool-invocation-flow
  receipt models
  evidence-bundle validation
  demo signing flow
  bundled example resources
```

## Exposed MCP tools

### `validate_receipt_json`

Validates a receipt JSON object against an evidence-bundle JSON object and a
public key PEM. The tool returns a JSON-safe verdict and validation report or a
controlled invalid result.

### `generate_demo_artifacts`

Generates fresh demo artifacts using the core package's deterministic demo
flow. The output includes receipt JSON, evidence bundle JSON, public key PEM,
verification report JSON, and verdict.

### `summarize_verification_report`

Extracts a compact reviewer-facing summary from a verification report:
verdict, failed checks, warnings, and errors.

## Design boundary

This package is an integration and accessibility layer, not a new cryptographic
primitive and not a formal verifier. The core trust assumptions remain those of
the signed receipt and evidence-bundle validation model:

```text
does_not_prove_semantic_correctness = true
does_not_prove_policy_correctness = true
does_not_protect_against_compromised_signer = true
does_not_replace_human_review = true
local_stdio_only_in_current_release = true
```

## Software-publication relevance

For software-publication review, the package should be evaluated as local
developer/reviewer infrastructure for making execution-receipt validation
available to MCP-compatible agents. Its main software contribution is the
agent-facing interface, controlled error behavior, and documented local use
path around the underlying receipt validator.
