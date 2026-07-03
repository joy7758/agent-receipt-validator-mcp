from __future__ import annotations

import tomllib
from pathlib import Path

from agent_receipt_validator_mcp import __version__


def test_package_version_matches_pyproject() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    assert metadata["project"]["version"] == __version__


def test_console_script_points_to_server_main() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    metadata = tomllib.loads(pyproject.read_text(encoding="utf-8"))

    assert metadata["project"]["scripts"]["agent-receipt-validator-mcp"] == "agent_receipt_validator_mcp.server:main"
