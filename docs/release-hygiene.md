# Release Hygiene

```text
document_id = AGENT_RECEIPT_VALIDATOR_MCP_RELEASE_HYGIENE
version = 0.1.1
artifact = agent-receipt-validator-mcp
```

## Generated surfaces

The repository `.gitignore` excludes common generated and local-only artifacts:

```text
.venv/
__pycache__/
.pytest_cache/
dist/
build/
*.egg-info/
.env
*.pem
*.key
tmp/
test-output/
.DS_Store
```

## Before a release

```text
version_metadata_consistent = pyproject.toml and package __version__ match
tests_pass = python -m pytest tests/test_tools.py
cli_help_pass = agent-receipt-validator-mcp --help
smoke_check_pass = python scripts/smoke_check.py
license_present = LICENSE
citation_present = CITATION.cff
agent_readable_index_present = llms.txt
docs_present = docs/
examples_present = examples/
```

## Trusted publishing note

The README documents the intended PyPI Trusted Publishing flow through GitHub
Actions OIDC. No PyPI API token should be stored in the repository.

## Secret handling

Do not commit private keys, API tokens, production receipts, confidential
evidence bundles, or local `.env` files. The package's demo flow generates
fresh demo keys and artifacts at runtime.
